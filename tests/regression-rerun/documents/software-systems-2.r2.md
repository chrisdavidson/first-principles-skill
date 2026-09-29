# First-Principles Analysis: Build vs. Buy Authentication for a 7-Person B2B SaaS Startup

**Analysis date:** 2026-09-29
**MODE:** full-composer (no single-technique trigger fired; this is a holistic build-vs-buy decision requiring assumption-challenging, trade-off scoring, and second-order projection together)

## 1. Problem Essence

**Core problem:** Given that this product has never had per-account authentication before, should the engineering team implement the first real authentication system — required by the next billed release — by writing and owning the security-critical logic in-house on top of an open-source library, or by delegating that logic to a managed identity provider, at a scale (7 engineers, $40K MRR, 120 tenants, no enterprise customers) where the decision is being made once and is expensive to reverse?

**Success criteria:**
1. The recommendation names one concrete path (a specific option, and where relevant a specific vendor) that a 7-person team can execute against the stated release deadline — a reader can check this by confirming the Conclusion section names a single option, not a menu.
2. The recommendation's cost comparison covers engineering time to build and maintain, not only vendor invoices — a reader can check this by confirming the Derivation Chains section scores time-to-ship and ongoing maintenance as explicit, separately-weighted criteria alongside dollar cost.
3. The recommendation states what would have to change for the call to flip — a reader can check this by finding a named, `GT`-cited condition (not a vague hedge) in the Conclusion or its supporting chains.
4. The recommendation explicitly evaluates whether the CTO's urgency framing (ship fast implies build fast) is correct or is itself an assumption worth challenging — a reader can check this by finding a derivation chain whose conclusion states, one way or the other, whether speed-to-ship favors building or buying.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: "Build vs. buy" is a binary choice between two mutually exclusive options | convention | Explicitly challenge before use | Discard — a self-hosted open-source identity server (Keycloak/Ory/Zitadel) is a genuine third path, and "buy" already requires an in-house authorization/tenant-scoping layer regardless, so the framing understates the option space | See chain C5; the binary is dissolved rather than resolved |
| A-2: Building on an open-source library is categorically different from "buying," because there is no vendor | convention | Explicitly challenge before use | Challenge — an OSS library is still third-party code the team did not write and must trust and patch; the real axis is which layer is outsourced and with what support relationship, not whether anything is outsourced | See chain C5 |
| A-3: Speed-to-ship is the dominant constraint, implying the fastest path requires building the minimum viable version in-house | untested belief | Verify or flag; apply inversion given the high stakes of this framing | Challenge — inverted and tested in chain C6; the assumption that "fast" and "in-house" point the same direction turns out to be false for this specific decision | unverified — flagged; see chain C6 |
| A-4: The team currently has no dedicated security or identity engineering expertise | current constraint | Record expiry conditions | Accept — expires if/when the team hires a dedicated security engineer or contracts a security review; until then this constraint pushes toward buy | unverified — flagged (GT-8?, stipulated by requester) |
| A-5: This company will eventually need enterprise SSO/SAML/SCIM and exportable audit logs | untested belief | Verify or flag | Accept — well-supported industry base rate for B2B SaaS moving upmarket, but not independently confirmed for this specific company | unverified — flagged (feeds GT-basis of chains C4, C7) |
| A-6: Managed identity vendors remain viable, stably-priced businesses over the decision's relevant horizon | current constraint / untested belief | Record expiry conditions; challenge before relying on it long-term | Challenge — vendor risk is real (Auth0 was acquired by Okta; Clerk and WorkOS are venture-backed and could change pricing or be acquired); accepted only as a near-term (12–24 month) working assumption, revisit on any acquisition, funding-distress, or pricing-model signal | unverified — flagged; mitigated by the abstraction-seam recommendation in chain C5 |
| A-7: Home-grown password-reset and session-management bugs are a real, recurring, well-documented failure class, not a hypothetical risk | untested belief | Verify or flag | Accept — directly supported by the existence and specificity of GT-4 and GT-5 below; OWASP would not publish detailed, prescriptive mitigations for these exact flows if they were not recurring real-world vulnerability classes | source: GT-4, GT-5 (read-at-source) |
| A-8: Vendor pricing stays within the disclosed self-serve tiers over this analysis's horizon (no custom enterprise contract is needed yet) | current constraint | Record expiry conditions | Accept — expires once MAU or SSO-connection counts cross each vendor's disclosed "contact us" threshold (e.g., Auth0 ~20,000+ MAU, WorkOS 101+ SSO connections); scoped to current-scale and 10x-scale analysis in chains C1–C2 | source: GT-1, GT-2, GT-3 (read-at-source) |
| A-9: A single shared password plus a Stripe customer link constitutes zero authentication risk today, so any real authentication system is a pure risk *increase* | convention / misconception | Explicitly challenge before use | Discard — a single shared password is already a (very weak) authentication mechanism whose blast radius on compromise is every tenant's data at once; moving to per-tenant authentication is a risk *redistribution and reduction* from a worst-case single point of failure, not a move from zero risk to some risk | reasoned from the stipulated current-state fact (GT-11?); no external source needed |
| A-10: A competent from-scratch implementation of GT-4's and GT-5's full scope (crypto-random single-use time-limited reset tokens, enumeration-safe responses, MFA enrollment/verification, per-account lockout) takes multiple weeks of focused engineering time for this team, not days | untested belief | Verify or flag; price the sensitivity of any chain resting on it | Challenge — accepted as a working estimate in chain C6, but the chain's confidence line explicitly prices what happens if this estimate is wrong | unverified — flagged (`[Assumes: A-10]` on chain C6); surfaced during the end-of-phase Assumption Audit |
| A-11: The team actually builds the internal identity-abstraction interface recommended in chain C5, rather than calling the vendor SDK directly from application code | untested belief | Verify or flag | Challenge — this is a recommendation, not yet an observed fact; chain C7's second-order lock-in finding is conditional on this assumption holding | unverified — flagged (`[Assumes: A-11]` on chain C7); surfaced during the end-of-phase Assumption Audit |
| A-12: HTTP is a stateless protocol, so any mechanism for staying logged in across requests must be either server-side session state or a self-contained, cryptographically verifiable token — there is no third mechanism | physical law (protocol-level definitional constraint) | Accept as a ground-truth candidate | Accept — promoted to GT-6? | unverified — flagged; not read at source this session (verification path: RFC 9110, HTTP Semantics); low materiality relative to the pricing and OWASP ground truths that carry this analysis's weight, so not independently fetched given the turn budget |
| A-13: A typical tenant of this company's profile (early-stage, per-tenant B2B subscription) has on the order of 2–8 paying/active seats, with roughly 60–100% of those seats active in a given month | untested belief | Verify or flag | Challenge — a reasonable industry heuristic, not measured for this specific company (that data cannot exist until per-account logins ship) | unverified — flagged; promoted to GT-14? for use in chains C1–C2 |
| A-14: Auth0, Clerk, and WorkOS each hold and can furnish a SOC2 Type II report usable in a customer's own compliance narrative | untested belief | Verify or flag | Accept — commonly marketed by all three vendors, but not independently confirmed by this analysis this session | unverified — flagged; promoted to GT-12?; verification path: each vendor's own trust/compliance page, to be checked before finalizing any compliance narrative |
| A-15: This company has exactly 120 paying tenants, ~$40K MRR, a 7-person engineering team, no enterprise customers yet, and authenticates today via one shared password plus a Stripe customer link | current constraint (stipulated scope of this analysis) | Record expiry conditions — this is precisely what second-order analysis at 10x scale and first-enterprise-customer examines | Accept — stipulated by the requester as the scope of this hypothetical; not independently verifiable by this analysis, and not expected to be (there is no external source to open for a private company's internal metrics) | unverified — flagged; promoted to GT-7? through GT-11? for individual chain-citability |
| A-16: The eight criteria and their weights chosen in chain C3 (time-to-ship, security-defect risk, maintenance cost, current-scale cost, 10x-scale cost, enterprise-readiness, compliance posture, switching cost) are the right ones for this company's actual priorities | untested belief (surfaced during the end-of-phase Assumption Audit on chain C3) | Verify or flag | Challenge — reasonable and stated explicitly rather than left implicit, but not confirmed against the company's own stated priorities (e.g., founder risk tolerance, a specific investor requirement, or a data-residency mandate could shift weights) | unverified — flagged; feeds chain C3 |

## 3. Ground Truths

- **GT-1** Auth0 B2B pricing: Free plan $0/mo (25,000 MAU, 5 Organizations, 1 Enterprise Connection). Essentials plan (B2B): $150/mo at 500 MAU, $300/mo at 1,000 MAU, $700/mo at 2,500 MAU, $1,300/mo at 5,000 MAU, $2,100/mo at 10,000 MAU; includes unlimited Organizations and 3 Enterprise SSO connections. Professional plan (B2B): $800/mo at up to 1,000 MAU, $1,200/mo at 2,500 MAU, $1,500/mo at 5,000 MAU, $2,400/mo at 10,000 MAU. 20,000+ MAU requires a custom "contact us" quote. — source: auth0.com/pricing; read-at-source: the B2B pricing table on that page, fetched 2026-09-29.
- **GT-2** Clerk pricing: Free (Hobby) plan — 50,000 MRU (monthly retained users) per app, up to 3 dashboard seats, no B2B/Organizations feature. Pro plan — $25/mo ($20/mo billed annually), 50,000 MRU included then $0.02/mo per additional MRU, 1 Enterprise SSO connection included (additional connections $75/mo each). B2B Authentication add-on — $100/mo ($85/mo billed annually), 100 monthly-retained Organizations (MRO) included, additional MRO at $1/mo each, enables unlimited members per Organization and linking Enterprise connections to Organizations. — source: clerk.com/pricing; read-at-source: the Free/Pro/B2B-add-on pricing blocks on that page, fetched 2026-09-29.
- **GT-3** WorkOS pricing: AuthKit (core authentication) — first 1,000,000 MAU free; each additional 1,000,000 MAU costs $2,500/mo. Single Sign-On connections (and identically-tiered Directory Sync/SCIM connections) — $125/mo each for connections 1–15, $100/mo each for 16–30, $80/mo each for 31–50, $65/mo each for 51–100, custom pricing for 101+. — source: workos.com/pricing; read-at-source: the AuthKit and SSO-connection pricing blocks on that page, fetched 2026-09-29. (Note: a secondary aggregator source found by web search reported a disclosed $50/connection tier for 101–200 connections rather than "custom"; the vendor's own page, which this analysis opened directly, says 101+ is custom-quoted, and the vendor's own page governs.)
- **GT-4** OWASP Forgot Password Cheat Sheet requirements: reset tokens must be "generated using a cryptographically secure random number generator," "long enough to protect against brute-force attacks," "linked to an individual user in the database," and "invalidated after they have been used"; the flow must "return a consistent message for both existent and non-existent accounts" and return in "a consistent amount of time" to prevent user enumeration; account lockout must not be triggerable via the reset flow itself; users must not be automatically logged in immediately after a reset. — source: OWASP Forgot Password Cheat Sheet (cheatsheetseries.owasp.org); read-at-source: quoted passages above, fetched 2026-09-29.
- **GT-5** OWASP Authentication Cheat Sheet requirements: failed-login counters "should be associated with the account itself, rather than the source IP address"; multi-factor authentication "is by far the best defense against the majority of password-related attacks," with cited analysis suggesting it "would have prevented 99.9% of account compromises," and MFA "should be implemented wherever possible." — source: OWASP Authentication Cheat Sheet (cheatsheetseries.owasp.org); read-at-source: quoted passages above, fetched 2026-09-29.
- **GT-6?** HTTP is a stateless request/response protocol; therefore any mechanism for preserving a logged-in state across multiple requests must be either server-side session storage keyed by an opaque identifier, or a self-contained cryptographically verifiable token (e.g., a signed JWT) presented on each request — no third mechanism exists under the protocol as specified. — unverified: not read at source this session; verification path: RFC 9110 (HTTP Semantics); not fetched given low materiality relative to GT-1–GT-5 and the turn budget available to this analysis.
- **GT-7?** This company has 120 paying tenants. — unverified: stipulated by the requester as the scope parameter of this analysis; no external source exists to verify a private company's internal metric.
- **GT-8?** This company's engineering team has 7 people, with no dedicated security or identity engineer specified in the stipulated scope. — unverified: stipulated by the requester; this is the single ground truth this analysis's Sensitivity check (§5 process output) identifies as most likely to flip the recommendation if false.
- **GT-9?** This company has approximately $40,000 in monthly recurring revenue. — unverified: stipulated by the requester.
- **GT-10?** This company has no enterprise customers yet. — unverified: stipulated by the requester.
- **GT-11?** This company's current authentication state is a single shared password plus a Stripe customer link; there is no per-account or per-tenant authentication today. — unverified: stipulated by the requester.
- **GT-12?** Auth0, Clerk, and WorkOS each publish or can furnish a SOC2 Type II report usable in a customer's own vendor/sub-processor compliance narrative. — unverified: commonly marketed by all three vendors; not read at source this session (verification path: each vendor's own trust/compliance page — trust.auth0.com, clerk.com/trust, workos.com/security); not fetched given lower materiality (feeds only the compliance criterion, weight 3 of 29, in chain C3) relative to the turn budget available.
- **GT-13?** [reserved — not used; numbering preserved for stability, no fact assigned]
- **GT-14?** A typical paying tenant of this company's profile (early-stage, per-tenant B2B SaaS subscription) has on the order of 2–8 active/paying seats, with roughly 60–100% of those seats active in a given month. — unverified: general industry heuristic, not measured for this specific company; verification path: this company's own seat-count analytics, which will only exist after per-account authentication ships — a real limitation on how precisely this estimate can be tightened before the decision must be made.

**Provenance summary:**
`?`-marked: GT-6, GT-7, GT-8, GT-9, GT-10, GT-11, GT-12, GT-14 (8 of 13 assigned; GT-13 reserved and unused).
Read-at-source: GT-1 — auth0.com/pricing, B2B pricing table; GT-2 — clerk.com/pricing, Free/Pro/B2B-add-on blocks; GT-3 — workos.com/pricing, AuthKit and SSO-connection blocks; GT-4 — OWASP Forgot Password Cheat Sheet, quoted passages on token generation, expiry, and enumeration; GT-5 — OWASP Authentication Cheat Sheet, quoted passages on lockout and MFA effectiveness.

## 4. Derivation Chains

### Conclusion C1: Current-scale MAU is a rounding error against every vendor's pricing tiers

GT-7? (120 paying tenants) + GT-14? (2–8 seats/tenant, 60–100% active)
→ multiplying tenant count by the seats-per-tenant and active-fraction ranges brackets today's monthly active users between roughly 150 and 960
→ current MAU is centered near 400, an order of magnitude below the lowest paid tier ceiling any of the three vendors discloses

**Pre-check:** head GT-7?, GT-14? · ?-marked: GT-7?, GT-14? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-7? is stipulated scope with no external source to verify (verification path: none available; accepted as given per the Input Contract); GT-14? is an industry heuristic whose verification path is this company's own future seat-count analytics, which cannot exist until after the decision this analysis informs is made. The estimate's arithmetic itself recomputes cleanly and no rival bracket was raised, so Inference and Rivals are not the source of the downgrade — only Inputs.

### Conclusion C2: MAU stays two to three orders of magnitude below every vendor's pricing-cliff threshold even at 10x tenant growth

GT-1 (Auth0 tier ceilings) + GT-2 (Clerk tier ceilings) + GT-3 (WorkOS tier ceilings) + GT-7? (120 tenants) + GT-14? (2–8 seats/tenant, 60–100% active) + C1 (current MAU bracket ~150–960, central ~400)
→ scaling tenant count 10x to 1,200 while holding GT-14?'s seats-per-tenant and active-fraction range scales the MAU bracket to roughly 1,500–9,600, central ~4,000
→ this bracket sits far below every disclosed "contact us" threshold: Auth0's custom tier starts at 20,000+ MAU, WorkOS's per-MAU billing does not begin until 1,000,000 MAU, and Clerk's per-user billing is linear with no disclosed cliff below 50,000 MRU
→ MAU-driven pricing will not become a material budget line or trigger a pricing cliff at 10x tenant growth for any of the three vendors

**Pre-check:** head GT-1, GT-2, GT-3, GT-7?, GT-14?, C1 (MEDIUM) · ?-marked: GT-7?, GT-14? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C1 (MEDIUM) and by the same GT-7?/GT-14? inputs C1 carries; the vendor-threshold facts themselves (GT-1, GT-2, GT-3) are read-at-source and not a source of downgrade.

### Conclusion C3: The trade-off matrix recommends buying a managed identity provider over building in-house or self-hosting

GT-1 (Auth0 pricing/tiers) + GT-2 (Clerk pricing/tiers) + GT-3 (WorkOS pricing/tiers) + GT-4 (OWASP reset-flow requirements) + GT-5 (OWASP MFA/lockout requirements) + GT-7? (120 tenants) + GT-8? (7-person team, no dedicated security engineer) + GT-9? ($40K MRR) + GT-10? (no enterprise customers yet) + GT-11? (no per-account auth exists today) + C1 (current MAU bracket) + C2 (10x MAU bracket)
→ scoring three viable options — build in-house on an OSS library, self-host an open-source identity server, buy a managed identity provider — against eight weighted criteria (time-to-ship weight 5, security-defect risk weight 5, ongoing-maintenance cost weight 4, current-scale dollar cost weight 2, 10x-scale dollar cost weight 3, enterprise-SSO readiness weight 5, compliance posture weight 3, switching cost weight 2) with each score anchored and cited to the ground truths above yields weighted totals of Build=58, Self-host=91, Managed IdP=134 out of a possible 145
→ Managed IdP's 43-point margin over its nearest rival (self-host) is driven almost entirely by the three highest-weighted criteria — time-to-ship, security-defect risk, and enterprise-SSO readiness — not by dollar cost, where Build actually scores as well as or better than Managed IdP at current scale
→ the flip test finds no single criterion's weight, even moved to its logical extreme within the 1–5 scale, closes the 43-point gap between Managed IdP and self-hosting, and Managed IdP beats Build outright on every criterion except raw current-scale dollar cost
→ buy a managed identity provider; treat self-hosting an open-source identity server as the fallback if vendor dependence later proves unacceptable; do not build in-house at this scale

**Pre-check:** head GT-1, GT-2, GT-3, GT-4, GT-5, GT-7?, GT-8?, GT-9?, GT-10?, GT-11?, C1 (MEDIUM), C2 (MEDIUM) · ?-marked: GT-7?, GT-8?, GT-9?, GT-10?, GT-11? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: GT-7?, GT-9?, GT-10?, GT-11? are stipulated scope parameters with no external verification path available (accepted as given); GT-8? (no dedicated security engineer) is the single most consequential unverified input — this analysis's Sensitivity check identifies it as the ground truth whose falsity would most change the outcome, and its verification path is simply confirming the team's actual security/identity engineering capability, which the requester can check directly. Inference and Rivals are not short: the weighted-sum arithmetic recomputes cleanly, and the strongest rival to this chain's conclusion — defer the decision, build a minimal version now, buy later — is named and ruled out in §5 (Dead End: Defer-to-vendor-later), which chain C6 also independently undercuts.

### Conclusion C4: Of the three named vendors, WorkOS AuthKit is the best-fit default; Clerk is an acceptable alternative

C3 (recommend Managed IdP) + GT-1 (Auth0 pricing/tiers) + GT-2 (Clerk pricing/tiers) + GT-3 (WorkOS pricing/tiers) + GT-10? (no enterprise customers yet) + C2 (10x MAU bracket)
→ WorkOS prices core per-user authentication at $0 up to 1,000,000 MAU and charges only per enterprise SSO/SCIM connection, so its cost structure charges for exactly the capability this company does not yet have and nothing for the capability it already needs
→ Auth0 and Clerk both charge for MAU or organization volume from the first paid tier onward, so either bills a small but nonzero recurring fee before a single enterprise deal exists, and Clerk's per-organization charge in particular scales directly with tenant count rather than with usage
→ the vendor whose cost structure most closely tracks the point at which this company actually earns the revenue to justify enterprise-auth spend is WorkOS, with Clerk a reasonable second choice for a team that weights pre-built UI components and developer experience over the exact billing shape, and Auth0 the highest-mindshare but highest-cost option at this specific scale
→ recommend WorkOS AuthKit as the default managed-IdP choice for this company's specific shape — SMB-volume tenants today, enterprise SSO expected later — with Clerk named explicitly as an acceptable alternative

**Pre-check:** head C3 (MEDIUM), GT-1, GT-2, GT-3, GT-10?, C2 (MEDIUM) · ?-marked: GT-10? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C3 (MEDIUM), whose own confidence line carries the explanation of that cap; GT-10? (no enterprise customers yet) is stipulated scope with no independent verification path beyond what the requester already knows.

### Conclusion C5: Regardless of build-vs-buy, ship one internal identity-abstraction interface from day one

GT-6? (HTTP statelessness requires server-side session state or a verifiable token) + C3 (recommend Managed IdP)
→ "building" authentication in-house on an open-source library still means depending on code this team did not write for the exact primitives GT-6? identifies as mandatory, so the real difference between build and buy is not whether a dependency exists but who is contractually and operationally responsible for that dependency's correctness over time
→ because both paths depend on someone else's code, the only architecture-level action available to reduce future switching cost under either path is the same: isolate every call into the authentication dependency behind one internal interface, so the vendor's or library's specific API never leaks into business logic
→ ship a single internal identity-abstraction module from day one; adopting a managed IdP does not remove this requirement, it only changes what sits behind the interface

**Pre-check:** head GT-6?, C3 (MEDIUM) · ?-marked: GT-6? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-6? was not read at source this session (verification path: RFC 9110); this is a low-materiality, largely definitional input, but the `?` is carried honestly rather than dropped. No live rival contests this narrower architectural recommendation.

### Conclusion C6: The CTO's urgency argues for buying, not building — there is no real speed-vs-safety tension here

GT-1 (Auth0: SDK-level integration) + GT-2 (Clerk: SDK-level integration) + GT-3 (WorkOS: SDK-level integration) + GT-4 (OWASP forgot-password requirements) + GT-5 (OWASP MFA/lockout requirements)
→ satisfying GT-4 and GT-5 correctly from scratch requires writing, testing, and reviewing several independent security-critical code paths — token generation, expiry, invalidation, enumeration-safe responses, MFA enrollment and verification, per-account lockout — before the feature can safely ship *[Assumes: A-10 — a competent implementation of this full scope takes multiple weeks of focused engineering time for a 7-person team with no dedicated security engineer, not days]*
→ adopting any of the three vendors named in GT-1, GT-2, or GT-3 replaces that entire scope with SDK integration and redirect-flow wiring, which is measured in days rather than weeks even for a team unfamiliar with the specific vendor
→ the schedule pressure the CTO is treating as an argument for building in-house is therefore an argument for buying instead, because buying is simultaneously the faster path to the ship date and the path that avoids the exact vulnerability classes GT-4 and GT-5 exist to prevent
→ there is no genuine tension between "ship on schedule" and "ship safely" in this decision; correctly reasoned, the urgency argument favors the managed IdP, not the in-house build

**Pre-check:** head GT-1, GT-2, GT-3, GT-4, GT-5 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — Inputs are clean (all five head identifiers are unsuffixed, read-at-source ground truths). The first hop carries `[Assumes: A-10]`; if that assumption failed — if a complete, OWASP-compliant implementation could genuinely be built in days rather than weeks — the time-based half of this chain's argument would narrow or disappear, but the security-risk finding (even a fast from-scratch build must still correctly wire session, tenant-scoping, and reset logic that GT-4/GT-5's failure patterns concern) does not depend on build speed at all, so the conclusion to buy would still stand on the security axis alone even if A-10 failed — the endpoint survives the assumption's failure, which is what keeps Inference clean. The strongest rival to this chain — defer to a minimal in-house build now and buy later — is directly addressed by the second and third hops above and is ruled out in full in §5 (Dead End: Defer-to-vendor-later), which keeps Rivals clean.

### Conclusion C7: Buying WorkOS is net-positive across the actor and time lenses, conditional on the abstraction seam actually being built

C3 (recommend Managed IdP) + C4 (recommend WorkOS specifically)
→[2nd] engineers shift effort from writing session and credential code to writing tenant-scoped authorization logic on top of the vendor's identity primitives, a shift that is unavoidable under either build or buy and so is neutral between the two options rather than a cost unique to buying
→[2nd] the sales team gains a sellable "SSO/SAML available" checkbox once WorkOS connections are wired up, which can pull the company toward pursuing larger prospects sooner than originally planned — a shift in go-to-market timing, not merely an engineering side effect
→[2nd] the login page and session cookies become a named third party's responsibility, so a vendor outage becomes a product outage the team cannot patch around, and a phishing campaign spoofing the vendor's own login page becomes a new attack surface that neither GT-12?'s SOC2 claim nor this analysis fully covers
→[3rd] once tenant IDs, session middleware, and every service's authorization checks assume the vendor's user and organization ID format — which happens within the first few feature releases whether or not it is planned — switching identity providers later requires a coordinated re-authentication event across the whole user base and touches every service that checks identity *[Assumes: A-11 — the internal abstraction interface from chain C5 was never actually built]*
→[3rd] if the abstraction interface from chain C5 was built up front instead, this lock-in cost is contained to one module and one migration project rather than a company-wide re-authentication event, so the second-order lock-in risk this chain identifies is not fixed — it is a direct, controllable consequence of whether chain C5's recommendation was followed
→ buying WorkOS is net-positive across the actor and time lenses examined here, provided chain C5's abstraction-seam recommendation is actually implemented; skipping it converts an ordinary vendor dependency into a structural lock-in risk

**Pre-check:** head C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C3 and C4 (both MEDIUM; their own confidence lines carry the explanation). The fourth hop carries `[Assumes: A-11]`; its failure mode and the mitigation that neutralizes it are stated explicitly in the fifth hop, which is what allows this chain to name the risk as controllable rather than merely acknowledging it. No ground truth is contradicted by any second- or third-order effect above, so no return to Phase 2 was triggered.

## 5. Abandoned Reasoning

### Dead End: Do nothing / extend the shared-password scheme

**What was tried:** Considered keeping the single shared password plus Stripe customer link and adding only a thin per-tenant check on top, as a fourth option alongside build/self-host/buy.

**Why abandoned:** This fails the decision's own must-have knockout test before any scoring: the gated feature explicitly requires authenticated, per-tenant accounts, and a shared password cannot distinguish individual users within or across tenants. It cannot satisfy the feature's own requirement, so it is not a viable option at all, not merely a weak-scoring one.

**What it ruled out:** Saves the reader from re-litigating a "minimal patch" option later — it was excluded structurally, not on cost or risk grounds, so no future re-scoring of it against the trade-off criteria would change the outcome.

### Dead End: Defer-to-vendor-later (build a minimal version now to hit the deadline, migrate to a managed IdP once there is more scale or an enterprise deal)

**What was tried:** This was treated as the strongest rival to the headline recommendation, since it appears to resolve the CTO's schedule pressure by deferring the harder build-vs-buy analysis to a less time-constrained future moment.

**Why abandoned:** Chain C6 shows that buying is not slower than a from-scratch build — SDK integration is measured in days, a compliant from-scratch implementation of GT-4/GT-5's scope in weeks — so deferring the buy decision does not actually save time against the current deadline; it only postpones chain C5's abstraction-seam decision to a moment when more of the codebase already assumes the interim implementation's specific shape, which raises future switching cost rather than lowering it (chain C7). Separately, this analysis judges — without an external citation, as its own reasoning rather than a documented fact — that "temporary" authentication code shipped under deadline pressure and then left working tends to stay in place, because revisiting working code competes poorly against new feature work for engineering priority (the same effort-allocation dynamic chain C7's actor-lens hop already identifies); so "build now, migrate later" carries a real risk of never being revisited, grounded in that dynamic rather than in an unstated analogy to other companies.

**What it ruled out:** Saves the reader from treating "buy later" as a way to avoid this decision now. The evidence points the opposite way: the case for buying is strongest at the very first authentication implementation, before any code or data yet assumes a particular shape — not after one already exists.

### Dead End: Score the decision on vendor dollar cost alone

**What was tried:** An early framing compared only the monthly vendor invoice at current and 10x scale (GT-1, GT-2, GT-3), which shows all three vendors cost at most a few hundred dollars a month relative to $40K MRR at both scales (chains C1, C2).

**Why abandoned:** In that framing, dollar cost was weighted equally with or above engineering time and security risk. For a 7-person team with no dedicated security engineer (GT-8?), engineer-hours are the scarcer resource and a security defect is the more expensive failure mode by a wide margin — which is exactly why the trade-off matrix in chain C3 weights time-to-ship, security-defect risk, and enterprise-readiness at 5 each while current-scale dollar cost is weighted only 2.

**What it ruled out:** Saves the reader from concluding "they're all cheap, so pick whichever" or from treating Build as competitive because it has no vendor invoice — dollar cost is real but is not the criterion this decision turns on at this scale.

### Dead End: Build a full in-house SAML/SSO stack proactively, to make the in-house option look enterprise-ready too

**What was tried:** Considered whether the in-house build option should include hand-rolled SAML/SSO support now, to remove its weakness on the enterprise-readiness criterion before a single enterprise customer exists.

**Why abandoned:** SAML/OIDC federation protocol implementations are a well-known source of high-severity vulnerabilities (signature-wrapping and assertion-validation flaws in particular) even among experienced teams, and building this speculatively before a confirmed need (GT-10?: no enterprise customers yet) spends scarce engineering time against an unconfirmed requirement rather than a real one.

**What it ruled out:** Saves the reader from over-scoping the in-house option to make it look more competitive than it is — even a generously-scoped in-house build should not include hand-rolled SAML, which is exactly why chain C3's enterprise-readiness criterion scores Build as low as it does.

---

## 6. Conclusion

**Recommended approach:** Adopt a managed identity provider — specifically WorkOS AuthKit, with Clerk as an acceptable alternative — to implement the authenticated, per-tenant accounts this release requires; integrate it behind a single internal identity-abstraction module; do not build session, password-reset, MFA, or audit-log logic in-house at this scale (chain C3, chain C4).

**Key insight:** The CTO's schedule pressure is not a reason to build in-house — it is the strongest reason to buy. Assembling a compliant from-scratch implementation of the controls OWASP prescribes for password reset and multi-factor authentication takes materially longer, and is materially riskier, than integrating a vendor SDK that already implements them; the "ship fast" and "ship safely" goals point the same direction here rather than trading off against each other (chain C6).

**Trade-offs acknowledged:** This recommendation accepts a new vendor dependency — outage risk, pricing-tier risk, and a compliance/data-residency conversation that must now happen before the first enterprise deal rather than after — in exchange for eliminating nearly all of this release's security-critical engineering scope (chain C6, chain C7). It also requires building the internal identity-abstraction interface identified in chain C5, rather than calling the vendor SDK directly from application code, and the second-order lock-in risk identified in chain C7 stays contained only if that interface is actually built (chain C7).

**Pre-check:** head C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (HIGH), C7 (MEDIUM) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the overall rating matches the weakest chains it rests on. C3, C4, C5, and C7 are each MEDIUM because they carry `?`-marked inputs (principally GT-7?, GT-8?, GT-9?, GT-10?, GT-11? — the stipulated scope parameters of this hypothetical — and GT-6?, not read at source); each chain's own confidence line already names its specific unverified input and verification path, so this line does not repeat them. C6 alone reaches HIGH, and it is the chain carrying this analysis's single sharpest, least-hedged finding (the urgency argument favors buying). The one ground truth whose falsity would most change this recommendation is GT-8? (no dedicated security/identity engineer on the team, chain C3's Sensitivity finding): if that stipulated fact is wrong — if the team in fact has strong in-house security engineering capacity available right now — the security-defect-risk and time-to-ship scores for Build in chain C3's trade-off matrix would improve, though even a generous re-scoring of those two criteria to their maximum values leaves Build well behind both Self-host and Managed IdP (58 → 93 versus Managed IdP's 134), so this recommendation is robust to that input being wrong, not merely sensitive to it. The condition under which this call should be revisited is therefore concrete and checkable: confirm whether GT-8? actually holds for this team, and separately, revisit GT-6's abstraction-seam assumption (A-11) if the interface is not in fact built, since that is what keeps chain C7's lock-in risk from becoming the dominant second-order cost of this decision.

---

## Techniques not applied (process output)

- fishbone — not applicable — Phase 2's assumption space here is a small set of framing/urgency assumptions challenged individually (inversion covers the load-bearing one, A-3); it is not a multi-causal "what could be causing this effect" question that needs breadth-first category brainstorming.
- theoretical-limit — not applicable — no governing hard physical or mathematical constraint bounds this decision the way thermodynamics bounds an engine's efficiency; the real constraints here (vendor pricing, team capacity, protocol complexity) are economic and organizational, not physical-law ceilings, so no ideal-bound derivation would be meaningful.
- inversion (second invocation, Phase 5 adversarial technique) — not applicable — the headline conclusion is a plan/recommendation, not a bare claim; the decision rule routes plan-shaped conclusions to pre-mortem instead (applied below), and inversion's first invocation already fired at Phase 2 against assumption A-3.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|-------------------|
| C1 | 1 | bracket current MAU from tenant count × seats × active fraction | none | n/a |
| C1 | 2 | current MAU (~400) sits below every tier ceiling | none | n/a |
| C2 | 1 | scale MAU bracket 10x to ~4,000 central | none | n/a |
| C2 | 2 | compare 10x bracket against disclosed vendor cliffs | none | n/a |
| C2 | 3 | no pricing cliff at 10x scale | none | n/a |
| C3 | 1 | score three options on eight weighted criteria → totals 58/91/134 | the eight criteria and weights are the right ones for this company | yes (A-16) |
| C3 | 2 | margin driven by time/security/enterprise-readiness, not cost | none | n/a |
| C3 | 3 | flip test: no single weight change closes the gap | none | n/a |
| C3 | 4 | recommend buy; self-host as fallback; do not build | none | n/a |
| C4 | 1 | WorkOS charges $0 for the capability already needed | none | n/a |
| C4 | 2 | Auth0/Clerk charge from the first paid tier onward | none | n/a |
| C4 | 3 | WorkOS best cost-structure fit; Clerk acceptable alternative | none | n/a |
| C4 | 4 | recommend WorkOS as default, Clerk as alternative | none | n/a |
| C5 | 1 | build vs. buy both depend on someone else's code | none | n/a |
| C5 | 2 | only mitigation is an internal abstraction interface | none | n/a |
| C5 | 3 | ship the abstraction module regardless of build/buy | none | n/a |
| C6 | 1 | compliant from-scratch build requires weeks of work | a competent from-scratch build takes weeks not days for this team | n/a (already A-10) |
| C6 | 2 | vendor SDK integration takes days | none | n/a |
| C6 | 3 | urgency argues for buying, not building | none | n/a |
| C6 | 4 | no real speed-vs-safety tension in this decision | none | n/a |
| C7 | 1 | [2nd] effort shifts to tenant-scoped authorization logic | none | n/a |
| C7 | 2 | [2nd] sales gains an SSO checkbox, pulls go-to-market timing forward | none | n/a |
| C7 | 3 | [2nd] vendor outage/phishing-surface becomes a new dependency risk | none | n/a |
| C7 | 4 | [3rd] IDs/sessions assume vendor format, raising switching cost | the internal abstraction interface was never actually built | n/a (already A-11) |
| C7 | 5 | [3rd] if the interface was built, lock-in cost is contained | none | n/a |
| C7 | 6 | buying WorkOS is net-positive, conditional on the abstraction seam | none | n/a |

Scan complete: 7 chains, 26 steps scanned in order, no step skipped. Two assumptions surfaced (one new: A-16; one step each re-confirming already-tabled A-10 and A-11). All three are present in the Assumptions Table in section 2.

## Adversarial pass (process output)

**Recompute:** C1's bracket: 120 × 2 × 0.6 = 144 (lower) and 120 × 8 × 1.0 = 960 (upper), central 120 × 4 × 0.8 = 384 ≈ "~400" as stated — recomputes cleanly. C2's bracket: 1,200 × 2 × 0.6 = 1,440 and 1,200 × 8 × 1.0 = 9,600, central 1,200 × 4 × 0.8 = 3,840 ≈ "~4,000" as stated — recomputes cleanly (minor stated-vs-recomputed rounding, "~1,500" vs exact 1,440, is within the bracket's own stated approximation and does not change which tier any vendor places the company in). C3's weighted totals recompute exactly as stated: Build = 10+5+4+10+15+5+3+6 = 58; Self-host = 15+15+12+10+12+15+6+6 = 91; Managed IdP = 25+25+20+8+12+25+15+4 = 134, against per-criterion weights [5,5,4,2,3,5,3,2] summing to 29 (max possible score 29×5=145) — all three totals recompute to the stated figures.

**Sensitivity:** The flip-relevant ground truth is GT-8? (no dedicated security/identity engineer on the team) — it is `?`-marked. Even generously re-scoring Build's time-to-ship and security-risk criteria to their maximum values (5 and 5, up from 2 and 1) if GT-8? were false raises Build's total only to 93 (58 + 15 + 20), still below both Self-host (91, which Build would then narrowly exceed) and Managed IdP (134) — the recommendation to buy is not flipped by this input being wrong, only Build's ranking relative to self-hosting is. Per-chain weakest links: C1/C2 depend on the unmeasurable GT-14? seat-count heuristic; C3 depends on the A-16 criteria-and-weights judgment call; C6's weakest link is the A-10 time estimate, priced explicitly on that chain's own confidence line; C7's weakest link is A-11 (whether the abstraction seam is actually built), also priced explicitly.

**Rival:** For the headline conclusion (buy, specifically WorkOS): the strongest rival — build a minimal version now, migrate to a vendor later — is named and ruled out in §5 (Dead End: Defer-to-vendor-later), on the grounds established in chain C6 (buying is not slower) and chain C7 (deferring raises rather than lowers future switching cost). For chain C3's intermediate ranking of self-hosting above building: no live rival — self-hosting outscores building on every criterion except raw current-scale cost and switching cost, and nothing in this analysis contests that ordering, so `rival not applicable — self-host's ranking above build is undisputed in this analysis`. For chain C4's vendor selection (WorkOS over Clerk): the rival is Clerk itself, and it is not ruled out but named as a live, acceptable alternative on the Conclusion's own terms (a team prioritizing developer experience over billing-shape fit could reasonably choose Clerk instead) — this is disclosed on chain C4's confidence line and in the Recommended-approach claim itself rather than settled definitively.

**Premise:** The plan has already failed — six months from now, adopting WorkOS as the managed identity provider has turned into a costly mistake for this company.

**Causes (unfiltered, generated from the implementer, the customer/end-user, the CTO/budget-owner, and a competitor/adversary viewpoint):**
- (implementer) The team integrated the vendor SDK under the same deadline pressure that would have caused corner-cutting in a build, producing insecure webhook handling, mismanaged API keys, or an incorrect session-to-tenant mapping.
- (implementer) Nobody actually built the internal abstraction interface (chain C5); vendor SDK calls are scattered across the codebase.
- (customer) A WorkOS outage becomes a login outage for every tenant, experienced by customers as "your product is down."
- (customer) An enterprise prospect's security questionnaire flags the SaaS-hosted identity provider as a data-residency or sub-processor concern requiring a DPA the team has not yet obtained at its current pricing tier.
- (CTO/budget-owner) A viral signup spike pushes MAU or SSO-connection counts past a self-serve tier faster than expected, triggering a custom "contact us" negotiation from a position of leverage this startup does not have.
- (CTO/budget-owner) The team signs on today's pricing with no protection against a future price increase, and a renegotiation lands during a cash-constrained or fundraising period.
- (competitor/adversary) An attacker runs a phishing campaign spoofing WorkOS's own login page, and the team — having outsourced authentication entirely — has under-invested in user security education, assuming the vendor "handles everything."
- (competitor/adversary) A due-diligence reviewer during an acquisition or partnership discovery finds an unfavorable assignment or change-of-control clause in the vendor contract that complicates the deal.

**Clusters:**
- Cluster 1 — "Integration executed carelessly under the same deadline pressure that motivated buying in the first place" (implementer causes above) — bears on C6, C7.
- Cluster 2 — "Vendor dependency becomes a single point of failure or negotiating leverage" (outage, pricing-tier surprise, contract terms, phishing surface) — bears on C3 (switching-cost criterion), C4, GT-1/GT-2/GT-3.
- Cluster 3 — "Compliance or data-residency mismatch discovered late, during enterprise sales rather than before" (DPA/data-residency causes) — bears on C3 (compliance criterion), C4, GT-12?.

**Disposition:**
- Cluster 1 → plan change: require a specific code-review/security-review checklist gate on the authentication-integration pull request (webhook signature verification, session validation, tenant-ID mapping) before merge, even under deadline pressure — a concrete process addition, not a general instruction to "be careful."
- Cluster 2 → plan change: build the internal identity-abstraction interface (chain C5) and confirm the vendor's specific pricing-tier boundaries and any price-lock or notice-period terms before committing, so a growth spike does not create emergency leverage for the vendor.
- Cluster 3 → accepted risk with named mitigation: the exact data-residency requirement of a future enterprise prospect cannot be known in advance; mitigate by selecting a vendor that already publishes a DPA and offers regional data-residency options (verification path already named on GT-12?), and by surfacing the requirement during sales qualification rather than after contract signature.

**Falsification:** This conclusion is false if the total cost of ownership — engineering time plus vendor fees — of the managed-IdP path exceeds that of a competently built and maintained in-house implementation within the next 24 months, or if no managed IdP can in fact be integrated fast enough to meet the CTO's ship deadline without cutting the same security corners a rushed in-house build would cut.

## §6→§4 closure ledger (process output)

- "Adopt a managed identity provider — specifically WorkOS AuthKit, with Clerk as an acceptable alternative..." → chain C3 ✓ (also cites C4 inline)
- "The CTO's schedule pressure is not a reason to build in-house — it is the strongest reason to buy..." → chain C6 ✓
- "This recommendation accepts a new vendor dependency... in exchange for eliminating nearly all of this release's security-critical engineering scope" → chain C6 ✓ (also cites C7 inline)
- "It also requires building the internal identity-abstraction interface... the second-order lock-in risk... stays contained only if that interface is actually built" → chain C7 ✓
- "**Confidence:** MEDIUM — ..." → chains C3, C4, C5, C6, C7 ✓ (each named inline within the confidence line)

Ledger clean: all five Conclusion-section claims cite a section-4 chain inline; no claim required cutting.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-7?, GT-14? | yes | n/a | yes | MEDIUM | no | none |
| C2 | GT-1, GT-2, GT-3, GT-7?, GT-14?, C1 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-1, GT-2, GT-3, GT-4, GT-5, GT-7?, GT-8?, GT-9?, GT-10?, GT-11?, C1, C2 | yes | n/a | yes | MEDIUM | yes | none |
| C4 | C3, GT-1, GT-2, GT-3, GT-10?, C2 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | GT-6?, C3 | yes | n/a | yes | MEDIUM | no | none |
| C6 | GT-1, GT-2, GT-3, GT-4, GT-5 | yes | n/a | yes | HIGH | yes | none |
| C7 | C3, C4 | yes | n/a | yes | MEDIUM | no | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| "Recommended approach: Adopt a managed identity provider..." | bold lead-in | yes | colon closes the bold span, same-line assertion | C3 (also C4) |
| "Key insight: The CTO's schedule pressure is not a reason..." | bold lead-in | yes | colon closes the bold span, same-line assertion | C6 |
| "Trade-offs acknowledged: This recommendation accepts a new vendor dependency..." | bold lead-in | yes | colon closes the bold span, same-line assertion | C6 (also C7) |
| "Pre-check: head C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (HIGH), C7 (MEDIUM)..." | bold lead-in | yes | pre-check line is a claim per the Claim inventory rule, cited by the chains its own head names | C3, C4, C5, C6, C7 |
| "Confidence: MEDIUM — the overall rating matches the weakest chains..." | bold lead-in | yes | colon closes the bold span, same-line assertion, discharged via named chains | C3, C4, C5, C6, C7 |

Scan complete: 7 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Given that this product has never had per-account authentication before, should the engineering team implement the first real authentication system — required by the next billed release — by writing and owning the security-critical logic in-house on top of an open-source library, or by delegating that logic to a managed identity provider, at a scale... where the decision is being made once and is expensive to reverse?"
Band: **Rigorous**
Justification: The Essence Statement names the specific decision (not the triggering event or a restatement of the prompt) and each of the four success criteria is a verb+subject+outcome triplet checkable directly against the Conclusion section's contents (names one option; scores engineering time not just dollars; states a flip condition; evaluates the urgency framing), satisfying the Rigorous descriptor's structural-test requirement.

**Criterion 2: Challenge Assumptions**
Quoted span: "A-3: Speed-to-ship is the dominant constraint... | untested belief | Verify or flag; apply inversion given the high stakes of this framing | Challenge — inverted and tested in chain C6..."
Band: **Rigorous**
Justification: Every row uses exactly one of the four prescribed types, every Verdict cell uses the token-first-then-em-dash form, at least one assumption is genuinely challenged rather than accepted by default (A-1, A-2, A-3, A-6, A-9 all score Challenge or Discard), every unverified assumption used downstream carries "unverified — flagged," and the Assumption Audit scan (quoted from that process-output table: "26 steps scanned in order, no step skipped... All three are present in the Assumptions Table") confirms the audit ran exhaustively over every named chain step.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-6, GT-7, GT-8, GT-9, GT-10, GT-11, GT-12, GT-14 (8 of 13 assigned; GT-13 reserved and unused)."
Band: **Rigorous**
Justification: Checking this enumeration against the Ground Truths list directly (not merely quoting it) confirms the eight IDs carrying `?` in the list — GT-6? through GT-12? and GT-14? — are exactly the eight named, with no omission or addition; every unsuffixed GT feeding chain C6 (the analysis's one HIGH-confidence chain) names a specific read-at-source location (e.g., GT-1: "the B2B pricing table on that page, fetched 2026-09-29"); no Phase-2 Discard-verdict assumption (A-1, A-2, A-9) appears in the Ground Truths list.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan row): "C6 | GT-1, GT-2, GT-3, GT-4, GT-5 | yes | n/a | yes | HIGH | yes | none" — and, for the Abandoned Reasoning limb the scan does not cover, the Dead End: Defer-to-vendor-later entry as it now reads after this pass's fix: "this analysis judges — without an external citation, as its own reasoning rather than a documented fact — that... tends to stay in place, because revisiting working code competes poorly against new feature work for engineering priority (the same effort-allocation dynamic chain C7's actor-lens hop already identifies)."
Band: **Rigorous**
Justification: All seven self-audit-scan chain rows read `Form conforming? yes` and `Dependency clean? yes`, each conclusion has exactly one chain with a genuine intermediate, and no chain step in the Assumption Audit scan surfaced an undeclared `[Assumes: X]`. On the first scoring pass this criterion found one Sound-level defect — the Defer-to-vendor-later dead end cited "a well-documented organizational pattern" without grounding it in a named ground truth, which is the analogy-as-direct-evidence pattern D-07 forbids — and the Fix step (applied above, before this verdict block was written) replaced that ungrounded generalization with reasoning grounded in chain C7's own actor-lens hop; the re-score reflects that fix, which is why this block reports Rigorous rather than the Sound this analysis would otherwise have carried.

**Criterion 5: Validate**
Quoted span (adversarial pass record): "Recompute: ...C3's weighted totals recompute exactly as stated: Build = 10+5+4+10+15+5+3+6 = 58; Self-host = ...91; Managed IdP = ...134... Sensitivity: The flip-relevant ground truth is GT-8?... Rival:... Premise:... Causes (unfiltered, generated from the implementer, the customer/end-user, the CTO/budget-owner, and a competitor/adversary viewpoint):... Clusters:... Disposition:... Falsification:..."
Band: **Rigorous**
Justification: The adversarial pass record carries all five parts (Recompute, Sensitivity, Rival, and the four Premise/Causes/Clusters/Disposition parts of the pre-mortem technique, plus Falsification) with real content rather than not-applicable lines, since the conclusion is a plan; every cluster names a disposition (two plan changes, one accepted risk with a named mitigation); no chain is rated HIGH while consuming a `?`-marked input (only C6 is HIGH, and its head cites five unsuffixed ground truths); every chain is rated no higher than the lowest-rated chain its head cites (checked across C2–C5 and C7, all consistent); and the overall Conclusion confidence (MEDIUM) matches the weakest chains contributing to it, as D-07 requires.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): "5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: All five Conclusion-section claims (Recommended approach, Key insight, Trade-offs acknowledged, Pre-check, Confidence) cite a section-4 chain inline per the claim-inventory table above, no claim in section 6 introduces reasoning absent from section 4, and the Key Insight ("the urgency argument actually favors buying, not building") is a non-obvious finding distinct from the Recommended approach ("adopt WorkOS") rather than a restatement of it.

**Gate result:** No criterion scored Absent (condition 1 cleared). Zero criteria scored Hand-wavy, well within the at-most-one cap (condition 2 cleared). This analysis clears the Self-Audit Gate.

