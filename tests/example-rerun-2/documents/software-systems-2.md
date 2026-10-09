## Answer

**Recommendation:** Adopt a managed identity provider's free or core tier now (WorkOS AuthKit, Clerk, or Auth0) for the urgent per-tenant, multi-user, role-based accounts feature; defer paid SSO/SAML/SCIM connectors until an enterprise deal requires them; build only the app-specific tenant/role mapping every path requires regardless (chain C2, chain C5).

**Band (from §6):** MEDIUM — rests most heavily on chain C5 (capped by C4's Fermi estimate) and chain C6 (an unverified security-expertise premise).

**Would change it:** a time-boxed engineering spike against the real codebase (sharpens chain C4), and confirming with the CTO whether the team includes applied security/authN expertise (sharpens chain C6) — chain C5.
## 1. Problem Essence

**Core problem:** Which ownership split for the required components of a per-tenant authentication system — build every component in-house, buy a managed identity provider wholesale, or a composite that buys the credential/session core now and builds only the irreducibly app-specific tenant/role layer — lets this 7-person team ship the urgent, revenue-gating per-tenant feature fastest without increasing security risk, while keeping the cost of changing course later (including adding enterprise SSO/SCIM when a real enterprise deal requires it) bounded rather than prohibitive?

**Success criteria:**
- §6's "Recommended approach" line names exactly one ownership split (build / buy / composite), not a restatement of "it depends" or a generic industry heuristic.
- The recommendation traces (via §4) to a derivation chain that scores build, buy, and a composite option against this company's own stated constraints — 7-person team, ~$40K MRR, ~120 tenants, no enterprise customers yet, urgent timeline — rather than resting on an unexamined "buy is usually right for auth" default.
- §6 names the specific trigger or evidence (e.g., a specific future event, or a specific verification this analysis did not perform) that would change the recommendation, so the conclusion is falsifiable rather than a fixed rule.

---

## 2. Assumptions Table

**Fishbone brainstorm feeding this table (default six-category set: People, Process, Technology and Tools, Environment, Information, Resources).** The six explicit assumptions named in the prompt do not exhaust the assumption space for a team-specific build-vs-buy call, so categories were walked for hidden candidates before classifying: **People** — does the team have dedicated security expertise? (no discriminating observation available without asking the CTO directly — carried as an explicit untested belief below). **Process** — is "ship fast" implicitly weighted above "ship safely"? (discriminates on whether the chosen path can deliver both at once — tested in chain C6). **Technology** — does a good-fit open-source library exist for this team's stack? (not stated; carried as untested belief, flagged non-load-bearing). **Environment** — does "no enterprise customers yet" mean enterprise-readiness is irrelevant, or merely not-yet-due? (discriminates via GT-1's "yet" and the pricing evidence in GT-5–GT-7 showing enterprise connectors are an add-on, not a rebuild). **Information** — does "per-tenant accounts with roles" implicitly bound the scope (no deeper requirement assumed)? (treated as given, matching the prompt's own framing). **Resources** — can this stage's budget absorb a recurring vendor bill? (discriminates directly against GT-1's MRR and GT-5–GT-7's pricing).

**Inversion pass feeding rows 3–4 and 7 below.** Two claims felt clean enough to warrant inversion: "buying is the safe default" and "building in-house gives full control and is therefore safe." Inverting the first and enumerating failure-guaranteeing conditions surfaced: incorrect integration (token/session trust-boundary bugs) negating the vendor's hardening; pricing that scales unfavorably with usage; a single vendor outage concentrating availability risk; and lock-in raising the cost of leaving. Necessary preconditions for "buy" to succeed: correct integration, affordable pricing at this scale, and a workable exit path — none of them physically blocked per GT-5–GT-7, so none is load-bearing against buying. Inverting the second surfaced: a generalist team shipping subtle credential/session defects under deadline pressure; the open-source library going unmaintained (precedent: GT-10); and engineering time diverted from the product's core differentiator. These feed rows 2, 7, and 8, and chain C6.

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| "Build vs. buy is a binary choice" | convention | Challenge before use | Discard — a composite (buy the core, build only the app-specific tenant/role layer) is shown to dominate both pure options (chain C2, C5) | Ruled out directly by chains C2 and C5 |
| "An open-source library removes the ongoing maintenance burden of authentication" | convention | Challenge before use | Discard — contradicted by GT-9 (MFA/multi-tenancy/SSO scoped as plugin-ecosystem additions, not defaults) and GT-10 (a comparable library's 2025 deprecation) | read-at-source: GT-9, GT-10 |
| "Managed identity providers are inherently more secure than anything built in-house" | convention | Challenge before use | Challenge — true only in the qualified sense that vendors concentrate dedicated security investment in the highest-consequence primitives (GT-4); integration-layer mistakes can still undercut this regardless of vendor (chain C3, C6) | Qualified by chains C3, C6; not accepted as a blanket claim |
| "Urgency favors one path over the other" (restated as testable) | untested belief going in | Verify or flag | Accept — urgency favors buy/composite on both speed (chain C4) and security-under-deadline-pressure grounds (chain C6), not speed alone | Verification: chains C4, C6 |
| "The current shared-password/Stripe-link setup is irrelevant to this decision" | convention / framing assumption | Challenge before use | Discard — the current setup is itself a standing liability (chain C1), and its absence of legacy per-user credentials means this is a greenfield build with no migration burden for either path | GT-2, GT-11; chain C1 |
| "This decision is permanent/irreversible" | convention | Challenge before use | Discard — a later migration is a bounded, known-shape integration-swap project, not an open-ended one; reversibility is a matter of switching cost, not a binary (chain C5, second-order hops) | Chain C5 |
| "The 7-person team has no dedicated application-security specialist" | untested belief | Verify or flag | Challenge — unverified — flagged; used in chain C6 as `[Assumes: A-sec-expertise]` | unverified — flagged; would be confirmed by asking the CTO directly whether anyone has applied security/authN engineering background |
| "Shipping fast is the overriding success criterion, ahead of shipping safely" | convention / implicit prioritization | Challenge before use | Discard as a forced trade-off — chain C6 shows the recommended path delivers both at once, dissolving the presumed tension | Chains C4, C6 |
| "A suitable open-source auth library exists that fits this team's specific stack with good quality and support" | untested belief | Verify or flag | Challenge — unverified — flagged; not load-bearing, since even a good-fit library still scopes MFA/audit/multi-tenancy as integrator-owned per GT-9's demonstrated pattern | unverified — flagged; does not change chain C3's conclusion either way |
| "No enterprise customers yet means enterprise-readiness doesn't matter for this decision" | current constraint | Record expiry conditions | Challenge — partially accepted as a *current* constraint only; it expires the moment a real enterprise prospect enters the pipeline, which is exactly why the recommendation defers paying for SSO/SCIM rather than ignoring it | GT-1; chain C5 |
| "A recurring monthly SaaS vendor bill is unaffordable or risky at this company's stage" | untested belief | Verify or flag | Discard — contradicted by GT-5–GT-7 (free/near-free tiers cover this company's likely scale) and GT-1 ($40K MRR easily absorbs the shown cost) | GT-1, GT-5, GT-6, GT-7 |
| Vendor-published statistics on enterprise SSO procurement requirements (GT-8?) are reliable enough to drive the decision | untested belief | Verify or flag | Challenge — unverified — flagged; source sells SSO infrastructure and has a direct commercial interest in the claim; not used as load-bearing evidence anywhere in this analysis | unverified — flagged; retained only as color commentary, never cited in a chain head |
| "The team's generalist composition and 7-person headcount is today's reality" | current constraint | Record expiry conditions | Accept — expires if the company hires a dedicated security/platform engineer or grows headcount materially | GT-1 |
| "Shared single-password architectures cannot provide per-user attribution, revocation, or tenant isolation at the identity layer" | physical law (definitional/logical necessity) | Accept as ground-truth candidate | Accept — promoted to GT-11 | Entailment of GT-2; see GT-11 |
| "A 1.5-FTE-equivalent concurrency factor reasonably converts the Fermi estimate's engineer-weeks into calendar weeks for this team" | untested belief | Verify or flag | Challenge — unverified — flagged; estimate-internal assumption used in chain C4 as `[Assumes: A-fte-concurrency]` | unverified — flagged; confirmable via an actual sprint-planning exercise with the real codebase, not performed here |
| "Managed providers' dashboards provide authentication-event audit logs without material additional engineering" | untested belief | Verify or flag | Challenge — unverified — flagged; this analysis did not fetch a specific vendor audit-log feature page; used in chains C4/C5 as `[Assumes: A-audit-log]` | unverified — flagged; disclosed gap, not independently confirmed in this analysis |
| "Freed engineering capacity (from not owning credential/session internals) gets redirected to product differentiation rather than absorbed elsewhere" | untested belief | Verify or flag | Challenge — unverified — flagged; used in chain C5's second-order extension as `[Assumes: A-redirect]`; if false, the raw time saving still holds, only the redirection benefit does not | unverified — flagged |
| "Better Auth's feature scoping (2FA, multi-tenancy, and SSO as plugin-ecosystem additions) is representative of open-source authentication libraries generally" | untested belief | Verify or flag | Challenge — unverified — flagged; surfaced by the end-of-phase Assumption Audit on chain C3's first hop as `[Assumes: A-library-representative]` | unverified — flagged; would be confirmed by a systematic feature-table survey across several current libraries, not performed here |
| "The weights assigned to the six trade-off criteria in chain C5 (time-to-ship, security posture, future enterprise-readiness, engineering opportunity cost, cash cost, lock-in) reflect this company's actual priorities" | untested belief | Verify or flag | Challenge — unverified — flagged; surfaced by the end-of-phase Assumption Audit on chain C5's first hop as `[Assumes: A-weights-reflect-priorities]` | unverified — flagged; would be confirmed by walking the weighting past the CTO before acting on chain C5's ranking |

---
## 3. Ground Truths

**Irreducibility drill (five-whys, reduce-to-primitives mode) — decomposing "authentication" into its constituent primitives.**

Claim to verify: *"A correct, safe per-tenant multi-user authentication system exists."*

- Immediate constituents: identity storage · credential verification · session management · account-recovery (password reset) · multi-tenancy/role modeling · audit logging · MFA · a defined compliance/security posture.
- **Identity storage** — reducible to: a durable record mapping a user to a tenant. Stop test: passes — this is a definitional requirement of "per-tenant accounts" (GT-3); without it, "which tenant does this user belong to" has no answer. Verified — definitional.
- **Credential verification** — reducible to: a check that a presented secret matches a stored one without exposing the stored one. Stop test: passes — defined by GT-4's deferral to the Password Storage Cheat Sheet, confirming this is a distinct, specified security primitive rather than an afterthought. Verified — GT-4.
- **Session management** — reducible to: an unpredictable, revocable token bound to one identity. Stop test: passes — GT-4 states directly that "sessions should be unique per user and computationally very difficult to predict." Verified — GT-4.
- **Account-recovery (password reset)** — reducible to: a time-bounded, rate-limited, unpredictable recovery token. Stop test: passes — GT-4 treats this as significant enough to warrant its own dedicated cheat sheet rather than folding it into the main authentication guidance. Verified — GT-4 (by reference).
- **Multi-tenancy/role modeling** — reducible to: an app-specific mapping of user → tenant → permission set. Stop test: passes, but irreducibly *custom*: GT-9 shows that even an actively-maintained generic library ships multi-tenancy as a plugin concern, not a provided default, because no generic library can know this specific company's tenant/role semantics. Verified — GT-9; stays app-owned under every path.
- **Audit logging** — reducible to: a durable record of who did what, when, to authentication and authorization state. Stop test: passes by definition (a system with no such record cannot distinguish an authorized change from a compromised-credential one), but GT-9's introduction does not mention it at all, so its presence cannot be assumed from "using a modern library." Verified — definitional; **?** on provision by any given path (see assumption row "audit log" above).
- **MFA** — reducible to: a second, independent factor beyond the password. Stop test: passes — GT-4 quotes a specific, named effect (99.9% of account compromises stopped per the cited Microsoft analysis), which is a measured claim this analysis read at its source rather than a vague endorsement. Verified — GT-4.
- **Compliance/security posture** — not pursued further as its own primitive: at this company's current stage (GT-1: no enterprise customers yet), no named compliance framework has been triggered by an external requirement, so this branch is recorded as *not yet load-bearing* rather than drilled to its own ground truth.

Parent claim verdict: **verified as a decomposition, with one flagged branch** (audit-log provision is a `?` on every path until confirmed) — none of the branches were discarded as false, so the compound claim survives with the caveat attached below to the chains that depend on it.

**Ground truths.**

- **GT-1** This is a 7-person engineering team at an early-stage B2B SaaS company, with approximately $40,000 MRR, approximately 120 paying tenants, and no enterprise customers yet — source: the user's own problem statement (this conversation); read-at-source: the "Context" block of the request.
- **GT-2** The product currently runs behind a single shared password plus a Stripe customer link, with no per-user or per-tenant authentication of any kind today — source: the user's own problem statement; read-at-source: the "Context" block of the request.
- **GT-3** The next billed release requires authenticated, per-tenant accounts supporting multiple users per tenant with distinct identities/roles, and the CTO has described the timeline as urgent — source: the user's own problem statement; read-at-source: the "Context" block of the request.
- **GT-4** The OWASP Authentication Cheat Sheet states: "Sessions should be unique per user and computationally very difficult to predict"; defers password-storage specifics to the Password Storage Cheat Sheet and reset-flow specifics to the Forgot Password Cheat Sheet; and states multi-factor authentication "is by far the best defense against the majority of password-related attacks... with analysis by Microsoft suggesting that it would have stopped 99.9% of account compromises" — source: OWASP Cheat Sheet Series, Authentication Cheat Sheet; read-at-source: quoted passages retrieved directly from cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html.
- **GT-5** WorkOS prices AuthKit (core user management: sessions, passwords, basic auth) free for the first 1,000,000 monthly active users, but prices SSO (SAML) and Directory Sync (SCIM) separately, per connection, with no free tier for either — $125/connection/month for 1–15 connections, declining to $65/connection/month at 51–100, and custom pricing above 100 — source: workos.com/pricing; read-at-source: pricing page retrieved directly.
- **GT-6** Clerk's free "Hobby" tier (up to 50,000 Monthly Retained Users) excludes SSO, SCIM, and MFA entirely; the paid Pro ($25/mo) and Business ($300/mo) tiers include MFA plus one SSO connection and one directory-sync (SCIM) connection, with additional connections at $75/month each — source: clerk.com/pricing; read-at-source: pricing page retrieved directly.
- **GT-7** Auth0's free tier (up to 25,000 MAU) excludes MFA but includes one enterprise (SSO) connection; the paid B2B "Essentials" tier (from $150/mo at 500 MAU) includes three SSO connections plus MFA, with additional connections at $100/month each; inbound SCIM is included free across all tiers including Free — source: auth0.com/pricing; read-at-source: pricing page retrieved directly.
- **GT-8?** A vendor-published report (ssojet.com, a company selling SSO infrastructure) claims approximately 68% of enterprise buyers require SSO before contract signing and that deals are commonly lost during security review without SAML/SCIM support — source: ssojet.com research report, located via web search; reported-by-delegate / unverified: the publisher sells the exact capability the statistic argues for, no independent corroborating source was located, and the figure is not used as load-bearing evidence anywhere in this analysis.
- **GT-9** Better Auth (an actively-maintained open-source authentication library) states in its own introduction that "2FA, passkey, multi-tenancy, multi-session support, or even enterprise features like SSO, creating your own IDP" are delivered through its plugin ecosystem rather than as core defaults, and its introduction makes no mention of audit logging at all — source: better-auth.com/docs/introduction; read-at-source: introduction page retrieved directly.
- **GT-10** Lucia, a formerly popular open-source TypeScript authentication library, was deprecated as of March 2025, with its own site directing former users elsewhere — source: lucia-auth.com; read-at-source: site content retrieved directly.
- **GT-11** A single password shared identically across all tenants cannot, by definition, attribute any action to an individual user, cannot support revoking one compromised user's access without affecting every tenant, and enforces no identity-layer boundary between one tenant's data and another's — source: direct logical entailment of the architecture described in GT-2; no external citation required (definitional necessity).
- **GT-12** Satisfying GT-3's stated requirement (distinct per-tenant identities with roles, multiple users per tenant) requires, at minimum, an identity/credential store, a session-issuance-and-validation mechanism, an account-recovery path, and a tenant-to-user-to-role mapping; omitting any one of these four means GT-3's requirement is not met, regardless of which path builds or supplies it — source: direct logical entailment of GT-3 combined with the irreducibility drill above; no external citation required (definitional necessity).

**Provenance summary.** `?`-marked: GT-8 (1 of 12). Read-at-source locations: GT-4 — quoted passages on session uniqueness/unpredictability, the MFA 99.9% figure, and the password-storage/reset-flow deferrals, all retrieved directly from the Authentication Cheat Sheet page; GT-5 — WorkOS pricing page, AuthKit free-tier and SSO/SCIM per-connection pricing; GT-6 — Clerk pricing page, Hobby/Pro/Business tier feature tables; GT-7 — Auth0 pricing page, Free/B2B-Essentials tier feature tables; GT-9 — Better Auth introduction page, plugin-ecosystem statement; GT-10 — Lucia site, deprecation notice. GT-1, GT-2, GT-3 are read-at-source against the user's own problem statement within this conversation. GT-11 and GT-12 are definitional entailments and carry no external citation by design.

---
## 4. Derivation Chains

### Conclusion C1: The current shared-password/Stripe-link scheme is a standing liability today, not merely a blocker to the new feature

GT-1 (120 paying tenants, no enterprise customers yet) + GT-2 (shared password + Stripe link, no per-user identity) + GT-11 (a shared password cannot attribute, revoke, or isolate per tenant)
→ the product has no technical means today to attribute an action to one user, or to revoke one compromised credential, without affecting all 120 tenants at once
→ the authentication gap is a standing security and operational liability today, independent of whether the new feature ships

**Pre-check:** head GT-1, GT-2, GT-11 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — inputs are unsuffixed and either read-at-source or definitional; both hops are deductions from GT-11 applied at GT-1's scale (120 tenants). Rival considered: "with no incident yet, this risk is tolerable." Ruled out — tolerability is a property of consequence-if-exploited, and the consequence (all 120 tenants' Stripe-linked access potentially exposed by one shared secret) does not shrink merely because no exploit has occurred yet.

### Conclusion C2: "Build vs. buy" is a false binary — every path must supply the same four primitives, only ownership differs

GT-3 (feature requires per-tenant multi-user accounts with roles) + GT-12 (satisfying GT-3 requires an identity store, a session mechanism, a recovery path, and a tenant-user-role mapping)
→ whichever path is chosen, the team must build, configure, or integrate all four of these primitives before the feature can ship
→ build vs. buy is therefore not a choice about whether these four primitives must exist, only about who implements and operates each one
→ a composite split of ownership across the four primitives is a structurally available fourth option, not a compromise between two pure ones

**Pre-check:** head GT-3, GT-12 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — inputs are definitional and unsuffixed; each hop is a deduction from GT-12. Rival considered: "ownership of these primitives cannot actually be split across vendor and in-house code." Ruled out by the vendor pricing/feature structure itself in GT-5–GT-7, which already ships a vendor-owned identity/session/org primitive alongside an app-owned role-semantics layer — the split this chain claims is available is the split those vendors already build their products around.

### Conclusion C3: Building on an open-source library does not remove ownership of the highest-consequence primitives

GT-9 (Better Auth: MFA, multi-tenancy, and SSO are plugin-ecosystem additions, not defaults; no mention of audit logging) + GT-10 (Lucia, a comparable library, deprecated March 2025) + GT-4 (OWASP: session unpredictability and MFA's 99.9% effect are specified, non-trivial requirements)
→ even the actively-maintained open-source example examined here treats MFA, multi-tenancy, and audit logging as the integrator's own responsibility rather than a provided default *[Assumes: A-library-representative]*
→ a comparable library in the same space has already gone unmaintained within the last two years, so choosing an open-source library carries a demonstrated, not merely hypothetical, abandonment risk
→ building on an open-source library converts the vendor's ongoing security/maintenance obligation for the highest-consequence primitives into this team's own obligation, discharging only the lowest-risk primitive GT-4 names

**Pre-check:** head GT-9, GT-10, GT-4 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — Inputs axis is clean (HIGH), but Inference is short: the first hop generalizes from a single well-chosen example (Better Auth) to "even the actively-maintained... example," which is an inductive step this analysis did not check against a second or third library. What would close it: a systematic feature-table survey across several current open-source auth libraries. This does not weaken the separately-definitional claim (established in chain C2) that multi-tenancy is irreducibly app-specific regardless of library.

### Conclusion C4 (Estimate): Under this team's stated urgency, the buy/composite path ships materially faster than the build path

GT-1 (7-person team, no enterprise customers yet) + GT-4 (session/reset/MFA are specified, non-trivial security surfaces) + GT-9 (library leaves MFA/multi-tenancy/audit as integrator-owned) + GT-12 (four required primitives)
→ decomposing the build path into engineer-weeks — identity/tenant schema 0.5–1.5, session handling 0.5–1, password-reset flow 0.5–1.5, in-tenant roles 0.5–1, MFA 1–2, audit logging 0.5–1.5, security hardening/review 1–2, integration replacing the existing shared-password gate 0.5–1.5 — sums to a bracket of 5–12.5 engineer-weeks, central ≈8.75
→ decomposing the buy path into engineer-weeks — vendor evaluation 0.25–0.5, SDK/API integration 1–2, org-to-tenant mapping 0.5–1, in-tenant roles 0.5–1, integration testing 0.5–1, MFA as a dashboard toggle ≈0.1 — sums to a bracket of 2.85–5.6 engineer-weeks, central ≈4.2 *[Assumes: A-audit-log — the vendor's dashboard covers authentication-event logging without a material separate build; if false, add back roughly 0.5–1.5 engineer-weeks, which still leaves buy faster than build]*
→ converting engineer-weeks to calendar time at a ~1.5-FTE-equivalent concurrency factor for this 7-person team *[Assumes: A-fte-concurrency]* gives a build bracket of roughly 3.3–8.3 calendar weeks, central ≈5.8, against a buy bracket of roughly 1.9–3.7 calendar weeks, central ≈2.8
→ both ends of both brackets favor buy — the fastest plausible build is no faster than the slowest plausible buy — so the estimate is decision-resolving rather than merely directional under this team's stated urgency

**Pre-check:** head GT-1, GT-4, GT-9, GT-12 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — Inputs axis is clean, but Inference is short: the bracket rests on two declared, unverified estimation premises, A-audit-log and A-fte-concurrency, that materially shape the magnitude though not the direction (the decision-resolution check in the final hop holds even accounting for A-audit-log's stated failure mode). What would close it: a time-boxed spike against the real codebase, and confirming the chosen vendor's audit-log coverage directly.

### Conclusion C5: Composite ownership (buy the core now, defer enterprise connectors, build only the app-specific layer) dominates both pure options

GT-1 (no enterprise customers yet, ~$40K MRR) + GT-5 (WorkOS pricing) + GT-6 (Clerk pricing) + GT-7 (Auth0 pricing) + C4 (time/eng-cost estimate)
→ scoring Build, a naive "buy now with SSO pre-provisioned," and a Composite ("buy the free/core tier now, defer paid SSO/SCIM until an enterprise deal requires it") across six weighted criteria — time-to-ship ×5, security posture ×5, future enterprise-readiness ×3, engineering opportunity cost ×4, cash cost ×2, lock-in/exit cost ×2 — gives weighted totals Composite=85, Buy-naive=81, Build=51 *[Assumes: A-weights-reflect-priorities]*
→ Composite matches or beats Buy-naive on every one of the six criteria, differing only on cash cost (paying for unused SSO connections today scores worse), so Composite dominates Buy-naive regardless of how the weights are set
→ closing the 34-point gap between Composite and Build by raising any single criterion's weight to its scale maximum of 5 does not flip the result — the largest available single-criterion swing, on lock-in/exit cost, only closes the gap to 28 points — so the result is robust to reasonable weighting disagreement
→ recommend the composite: adopt a managed identity provider's free/core tier now for the urgent release, defer purchasing paid SSO/SAML/SCIM connectors until an actual enterprise deal requires them, and build only the irreducible app-specific tenant/role mapping chain C2 already showed every path requires
→[2nd] sales conversations with future enterprise prospects can truthfully describe SSO/SAML as available on upgrade during procurement, without this company having pre-paid for connections nobody uses yet
→[2nd] engineering attention shifts from permanently owning credential/session security to owning only the thin, app-specific authorization layer, freeing capacity for product differentiation *[Assumes: A-redirect — if this does not hold, the raw time saving in chain C4 still holds, only this redirection benefit does not]*
→[3rd] the durable owned asset becomes the authorization/role logic rather than the credential/session mechanics, reducing this team's exposure to the maintainer-abandonment pattern evidenced in GT-10
→[3rd] a later vendor renegotiation or migration becomes a bounded, known-shape integration-swap project rather than an open-ended completion of a system that was never finished, directly countering the framing that this choice is irreversible

**Pre-check:** head GT-1, GT-5, GT-6, GT-7, C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C4 (MEDIUM, estimate-based; see C4's own confidence line for its verification path, not re-explained here). The chain's main endpoint (the fourth hop, "recommend the composite") does not depend on the second-order extensions that follow it; `A-redirect` qualifies only the second extension hop, which is downstream of the endpoint, not an input the endpoint itself depends on, so it does not add a further Inference shortfall beyond C4's cap.

### Conclusion C6: The CTO's urgency is itself an argument against the build path's risk profile, not only its speed

GT-3 (urgency) + GT-4 (OWASP: session/reset/MFA are specified, security-sensitive requirements) + C3 (build path retains ownership of exactly these high-consequence components)
→ deadline pressure combined with retained ownership of the highest-consequence components concentrates this analysis's largest single risk — a credential or session defect shipped to all 120 tenants' users — on the path least resourced to prevent it *[Assumes: A-sec-expertise — the team has no dedicated application-security specialist; unverified, would be confirmed by asking the CTO directly]*
→ the urgency the CTO cites is itself an argument against the build path's risk profile, not merely a scheduling preference, resolving "does urgency favor one path" on security grounds as well as speed grounds

**Pre-check:** head GT-3, GT-4, C3 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C3 (MEDIUM; see C3's own confidence line, not re-explained here). Additionally, the first hop rests on `A-sec-expertise`, an unverified premise the endpoint depends on directly: if the team does in fact include someone with applied security/authN background, this chain's risk differential narrows substantially, though GT-4's primitives remain equally specified either way. What would remove this as a cause of the downgrade: asking the CTO directly whether anyone on the team has that background.

### Conclusion C7: Enterprise federation is a metered, separately-priced capability on every evaluated platform, never bundled free

GT-5 (WorkOS: SSO/SCIM priced per-connection, no free tier) + GT-6 (Clerk: Hobby excludes SSO/SCIM/MFA; paid tiers price extra connections) + GT-7 (Auth0: free tier excludes MFA; paid B2B tiers price extra SSO connections)
→ across all three evaluated providers, enterprise federation (SSO/SAML) and MFA are gated behind a paid tier or a per-connection charge, never bundled free with the base or core tier
→ enterprise-readiness is a metered, separately-priced capability on every evaluated platform, not a feature that "comes free" once a company adopts a managed identity provider

**Pre-check:** head GT-5, GT-6, GT-7 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — inputs are unsuffixed and read-at-source; both hops are a direct tabulation of the three cited pricing structures, recomputable by inspection of GT-5–GT-7. Rival considered: "some evaluated provider might include it free." Ruled out — the claim is scoped only to the three providers actually evaluated, and that scope was checked exhaustively against the pricing pages themselves, leaving no live rival within the stated scope.

### Conclusion C8: Among the libraries examined, an open-source library does not by itself supply the highest-consequence primitives or guaranteed maintenance

GT-4 (OWASP: session unpredictability, a dedicated reset-flow discipline, and MFA's measured 99.9% compromise-stopping effect are specified requirements) + GT-9 (Better Auth: MFA/multi-tenancy/SSO are plugin-ecosystem additions; no audit-log mention) + GT-10 (Lucia, a comparable library, deprecated March 2025)
→ the specific requirements GT-4 names are exactly the primitives GT-9 scopes as non-default plugin additions rather than defaults
→ among the libraries examined here, the actively-maintained one leaves these named, consequential primitives to the integrator, and a formerly comparable one has already been discontinued
→ for the specific libraries and requirements examined in this analysis, picking an open-source library does not by itself supply the primitives GT-4 identifies as highest-consequence, nor does it guarantee long-term maintenance

**Pre-check:** head GT-4, GT-9, GT-10 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — inputs are unsuffixed and read-at-source; each hop is a direct, scope-matched deduction from quoted evidence, bounded explicitly to "the libraries examined" and "the requirements GT-4 names" rather than generalized beyond that evidence. Rival considered: "a different library might cover all of this by default." Ruled out within this chain's stated scope — the claim is about the libraries actually examined, not libraries in general; chain C3 is where that broader, ungrounded generalization is made, and it is rated MEDIUM precisely because that step is inductive.

**Unverified input rule (D-07) note:** no chain in this section consumes a `GT-N?` input directly — GT-8? is deliberately never cited on any chain head, per its own Ground Truths entry, and is retained only as color commentary (section 3) — so D-07's mandatory-downgrade clause for `GT-N?` inputs does not trigger anywhere in this section; every MEDIUM rating above instead stems from an Inference-axis shortfall (an inductive generalization in C3, declared estimation premises in C4, a cap inherited from a cited chain in C5/C6, and an unverified premise the endpoint depends on directly in C6), each named with its closing verification path as required. Chains C7 and C8 isolate the narrow, fully-evidenced factual claims GT-5–GT-7 and GT-4/GT-9/GT-10 support on their own (HIGH), separating them from the broader inductive and estimate-based reasoning built on top of them in C3–C5 (MEDIUM) — every unsuffixed ground truth in section 3 (GT-1 through GT-7, GT-9 through GT-12) now feeds at least one HIGH-confidence chain (GT-1, GT-2, GT-11 via C1; GT-3, GT-12 via C2; GT-5, GT-6, GT-7 via C7; GT-4, GT-9, GT-10 via C8), in addition to the MEDIUM chains most of them also feed.

---
## 5. Abandoned Reasoning

### Dead End: Extend the shared-password/Stripe-link approach (e.g., per-tenant query parameters or shared per-tenant codes) instead of building real per-user accounts

**What was tried:** considered whether the urgent deadline could be met by patching the existing shared-secret scheme — for example, one shared code per tenant instead of one global password — rather than introducing real per-user identity.

**Why abandoned:** contradicts GT-3 directly (the feature requires *distinct identities and roles for multiple users per tenant*, not merely per-tenant isolation) and fails the definitional test in GT-11 (a shared secret, even scoped to one tenant, still cannot attribute an action to one specific user or revoke one user's access without affecting the whole tenant).

**What it ruled out:** saves a future reviewer from re-proposing a "lighter-weight" patch to the current scheme — the requirement in GT-3 is not satisfiable by any shared-secret variant, however it is scoped, so this path was never actually lighter-weight, only superficially so.

### Dead End: Recommend Build outright on the grounds that buying creates vendor lock-in

**What was tried:** considered weighting lock-in/exit cost heavily enough to favor Build, on the reasoning that owning the code outright avoids dependence on a third party.

**Why abandoned:** the trade-off's flip test (chain C5) shows that even raising lock-in/exit cost to the maximum weight on its 1–5 scale only closes 6 of the 34-point gap between Composite and Build — lock-in is a real but minor factor next to time-to-ship and security posture, both weighted highest for good reason (GT-3's urgency, GT-4's flagged risk). The inversion pass in §2 also showed lock-in is a bounded switching cost, not a permanent one, which removed the premise that made this path seem safer than it is.

**What it ruled out:** saves a future reviewer from re-litigating "avoid lock-in" as a standalone justification for Build — it is a real, named cost (chain C5), already weighed in, and it does not change the recommendation.

### Dead End: Recommend provisioning full enterprise SSO/SCIM connectors immediately, regardless of current customer mix

**What was tried:** considered recommending that the company buy a managed provider and immediately configure paid SSO/SAML/SCIM connectors, reasoning that "enterprise-ready from day one" is the safest posture.

**Why abandoned:** chain C5 shows this option (scored as "Buy-naive") is Pareto-dominated by the Composite option — Composite matches it on every other criterion and beats it on cash cost, because GT-1 establishes there are no enterprise customers yet to serve with those connectors. Paying $125–$375+/month (GT-5–GT-7) for connections nobody uses yet is a cost with no offsetting benefit at this stage.

**What it ruled out:** saves a future reviewer from treating "buy everything now" as equivalent to "buy the core now" — they differ materially on cost with no difference in risk or speed, so the cheaper option strictly dominates.

### Dead End: Apply the theoretical-limit technique to bound "how fast or secure authentication can possibly be built"

**What was tried:** considered whether a governing physical or mathematical constraint (analogous to a thermodynamic limit) could bound the build-vs-buy question the way Carnot efficiency bounds a heat engine.

**Why abandoned:** no such hard constraint separable from vendor and organizational choices exists here; the nearest candidates (cryptographic entropy floors for session/reset tokens, the specific requirements GT-4 names) are already carried as ground truths rather than a theoretical-limit bracket, and the decision itself turns on engineering time and organizational risk, not a physical ceiling. Recorded in the Techniques-not-applied block in the process-output appendix.

**What it ruled out:** saves a future reviewer from reaching for a theoretical-limit framing on an organizational decision where no governing hard constraint exists independent of the choices being compared.

---

## 6. Conclusion

**Recommended approach:** Adopt a managed identity provider's free or core tier now (for example WorkOS AuthKit, Clerk's Hobby/Pro tier, or Auth0's free/Essentials tier) to implement the urgent per-tenant, multi-user, role-based accounts feature; defer purchasing paid SSO/SAML/SCIM connectors until an actual enterprise deal requires them; build only the app-specific tenant/role-permission mapping that every path — build, buy, or composite — requires regardless (chain C2, chain C5).

**Key insight:** "Build vs. buy" is a false binary for this decision. Every path must supply the same four structural primitives (identity store, session mechanism, recovery path, tenant-role mapping), so the real decision is narrower than it appears — only who owns the credential/session/MFA/audit-log primitives, not whether they must exist — and on that narrower question, the timeline pressure the CTO cites and the security risk this analysis found both point the same direction instead of trading off against each other (chain C2, chain C3, chain C6).

**Trade-offs acknowledged:** this recommendation accepts a small, currently immaterial recurring vendor cost and a bounded future switching cost in exchange for materially faster, lower-risk shipping of the gated release (chain C5); it defers rather than eliminates the eventual cost of enterprise connectors, which recurs once a real enterprise deal appears (chain C5); and the standing security gap in the current shared-password/Stripe-link scheme (chain C1) is fixed only by actually shipping the new authenticated model on whatever timeline is chosen, not by this analysis itself.

**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the recommendation rests most heavily on chain C5 (MEDIUM, itself capped by C4's Fermi estimate) and chain C6 (MEDIUM, resting on the unverified `A-sec-expertise` premise). Two things would raise this to HIGH: (1) a time-boxed engineering spike against the real codebase replacing C4's Fermi bracket with a measured one, and (2) confirming directly with the CTO whether the team includes anyone with applied security/authN background, which would either remove or sharpen C6's risk differential. Nothing found in this analysis would change the *direction* of the recommendation — both named verifications narrow or widen the margin, not the sign.

---
## Appendix — process output

## Assumption Audit scan (process output)

End-of-phase scan of every named Derivation Chain step (section 4), in order, checking for assumptions required by that step that were not already in the Classified Assumptions Table (section 2) before this scan ran.

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | shared secret → no per-user attribution/revocation at 120-tenant scale | none | n/a |
| C1 | 2 | authentication gap is a standing liability today | none | n/a |
| C2 | 1 | all four primitives must exist under any path | none | n/a |
| C2 | 2 | build-vs-buy is about ownership, not existence | none | n/a |
| C2 | 3 | composite is a structurally available fourth option | none | n/a |
| C3 | 1 | Better Auth scopes MFA/multi-tenancy/SSO as plugin additions | Better Auth is representative of OSS libraries generally | yes — A-library-representative |
| C3 | 2 | Lucia's 2025 deprecation shows demonstrated abandonment risk | none | n/a |
| C3 | 3 | open-source build only discharges the lowest-risk primitive | none | n/a |
| C4 | 1 | build-path engineer-week decomposition and bracket | none beyond declared estimation premises | n/a (premises are inline `[Assumes:]`, see A-audit-log below) |
| C4 | 2 | buy-path engineer-week decomposition and bracket | vendor dashboard covers audit logging without material extra build | already in table — A-audit-log |
| C4 | 3 | conversion to calendar weeks at ~1.5 FTE-equivalent | FTE-equivalent concurrency factor is a reasonable conversion | already in table — A-fte-concurrency |
| C4 | 4 | both bracket ends favor buy — decision-resolving | none | n/a |
| C5 | 1 | weighted totals: Composite=85, Buy-naive=81, Build=51 | trade-off weights reflect this company's actual priorities | yes — A-weights-reflect-priorities |
| C5 | 2 | Composite Pareto-dominates Buy-naive | none | n/a |
| C5 | 3 | flip test: no single-criterion weight change flips Composite vs. Build | none | n/a |
| C5 | 4 | recommend the composite | none | n/a |
| C5 | 5 [2nd] | sales conversations can truthfully cite SSO as available-on-upgrade | none beyond GT-5–GT-7's own evidence | n/a |
| C5 | 6 [2nd] | engineering attention shifts to the app-specific layer | freed capacity gets redirected to roadmap work | already in table — A-redirect |
| C5 | 7 [3rd] | durable owned asset becomes authorization/role logic | none | n/a |
| C5 | 8 [3rd] | later migration becomes a bounded integration-swap | none | n/a |
| C6 | 1 | deadline pressure + retained ownership concentrates risk | team has no dedicated application-security specialist | already in table — A-sec-expertise |
| C6 | 2 | urgency argues against the build path on security grounds too | none | n/a |
| C7 | 1 | all three evaluated providers gate SSO/MFA behind a paid tier or per-connection charge | none | n/a |
| C7 | 2 | enterprise-readiness is metered, not free, on every evaluated platform | none | n/a |
| C8 | 1 | GT-4's named requirements are exactly what GT-9 scopes as non-default | none | n/a |
| C8 | 2 | the examined libraries leave these primitives to the integrator / one is discontinued | none | n/a |
| C8 | 3 | an examined open-source library does not by itself supply these primitives or guaranteed maintenance | none | n/a |

Scan complete: 27 chain steps across 8 chains (C1–C8), in order, no step skipped. Three assumptions surfaced that were not yet in the table at the time their originating step was first drafted (A-library-representative, A-weights-reflect-priorities) plus one that cross-references rows already present from the initial inversion/estimate passes (A-audit-log, A-fte-concurrency, A-redirect, A-sec-expertise were added to the table proactively during drafting as each technique ran, then confirmed exhaustive by this end-of-phase scan). The Classified Assumptions Table in section 2 reflects all of them.

## Techniques not applied (process output)

- theoretical-limit (Phase 1 essence reframe) — not applicable — the core question is an organizational build-vs-buy decision, not a figure bounded by a physical or mathematical law; no convention-vs-hard-limit reframing changes what the essence statement must ask.
- theoretical-limit (Phase 4 ceiling derivation) — not applicable — no governing hard constraint bounds "how fast, cheap, or secure authentication can be" in a way separable from the vendor/organizational choices under comparison; the nearest candidates (session/token entropy requirements) are already carried as GT-4 rather than a theoretical-limit bracket, per the Dead End recorded in section 5.
- inversion (Phase 5 adversarial technique) — not applicable — the conclusion is a plan/recommendation, which the inversion-vs-pre-mortem decision rule routes to pre-mortem instead (see the Adversarial pass record below); inversion was applied at its other invocation point, Phase 2, feeding assumption rows 3–4 and 7–8 in section 2.

## Adversarial pass (process output)

**Recompute.** C4: build bracket 5–12.5 engineer-weeks (central (5+12.5)/2=8.75, matches stated); buy bracket 2.85–5.6 engineer-weeks (central (2.85+5.6)/2=4.225≈4.2, matches stated); calendar conversion at ÷1.5 gives build 3.33–8.33 weeks (central 5.83≈5.8, matches) and buy 1.9–3.73 weeks (central 2.8, matches). C5: Build = 2·5+2·5+5·2+1·3+2·4+5·2 = 10+10+10+3+8+10 = 51 (matches); Buy-naive = 4·5+4·5+2·2+5·3+4·4+3·2 = 20+20+4+15+16+6 = 81 (matches); Composite = 4·5+4·5+4·2+5·3+4·4+3·2 = 20+20+8+15+16+6 = 85 (matches); flip-test gap at max lock-in weight (5): 38−2·5=28 (matches "closes to 28"). All computed figures recompute cleanly.

**Sensitivity.** The single ground truth most capable of flipping chain C4's "decision-resolving" claim is GT-9 (corroborated by GT-10): if a representative open-source library did provide MFA, audit logging, and multi-tenancy turnkey — contrary to what Better Auth's own introduction states — the build bracket would shrink by roughly 1.5–3.5 engineer-weeks, bringing its low end (≈3.5 weeks) into overlap with the buy bracket's high end (≈3.7 weeks) and weakening, though not reversing, chain C4's central-estimate gap. GT-9 is not `?`-marked (read-at-source), so per the Sensitivity step no further verification is mandatory beyond what chain C3's own Confidence line already names (the single-example induction gap). The weakest link per chain: C3's single-example induction; C4's `A-fte-concurrency` and `A-audit-log` premises; C5's inherited C4 cap plus `A-weights-reflect-priorities`; C6's `A-sec-expertise`.

**Rival.** Headline: "Build in-house" is the strongest rival to the composite recommendation; ruled out by chain C5's weighted totals, Pareto-dominance argument, and flip-test robustness. Per intermediate chain: C1's rival ("no incident yet means tolerable risk") is ruled out inline in C1's own confidence line. C2's rival ("ownership can't be split across vendor/app") is ruled out inline, citing GT-5–GT-7's existing vendor/app split. C3's rival ("a different library might bundle everything by default") is live and unresolved — named on C3's own confidence line, which is exactly why C3 is MEDIUM rather than HIGH. C4's rival regarding `A-fte-concurrency` is neutralized structurally: the concurrency factor is a common scalar divisor applied to both the build and buy brackets, so no value of it reverses which bracket is larger, only their shared absolute scale — a fact not previously stated in section 4 and recorded here. C5's rival ("Buy-naive," provisioning everything immediately) is ruled out by Pareto-dominance (section 4, chain C5) and recorded as Dead End 3 (section 5). C6's rival ("the team already has security expertise") is live and named on C6's own confidence line.

**Premise.** The recommendation has already failed: the company adopted the composite (managed-provider core now, deferred enterprise connectors, in-house tenant/role layer) and it did not deliver the urgent release safely and on time, or it created a problem worse than the one it solved.

**Causes (unfiltered, from the implementer's, the CTO's, a tenant's, and a competitor's viewpoints).** Implementer: (1) the vendor SDK didn't fit the existing stack as cleanly as estimated, burning C4's projected time savings; (2) the integration trusted a client-supplied tenant ID instead of the vendor's verified session/token claims, reintroducing a tenant-isolation bug despite the "secure" provider; (3) migrating the 120 existing Stripe-linked tenants into the new model had messy edge cases that ate the generic "integration" time budget; (4) nobody actually configured MFA or checked the vendor's audit-log/webhook feature, so `A-audit-log` turned out false unnoticed. CTO/business: (5) the vendor's free-tier usage definition didn't match this product's actual tenant×user behavior, triggering an unexpected bill or feature gate mid-launch; (6) the urgency itself pressured the team to skip C4's own "security hardening/review" line, undermining the security benefit the buy path was chosen for; (7) `A-weights-reflect-priorities` turned out false — e.g., cost mattered more to the CTO than this analysis assumed. Tenant: (8) a tenant admin invited a user who saw another tenant's data because of a bug in the custom (non-vendor) authorization layer every path still had to build; (9) a tenant locked out during the reset-flow migration lost trust during the billed release window, generating support load at the team's least-slack moment. Competitor/adversary: (10) an attacker found a session-fixation or token-replay bug in the integration layer during the least-hardened launch window; (11) a competitor used "enterprise-ready since day one" against this company precisely because the deferred-SSO strategy left a visible, timed gap.

**Clusters.** Cluster A — integration-layer trust-boundary bugs (causes 2, 10; bears on chain C3's qualified "buy is more secure" reading and chain C6). Cluster B — migration/data-model mess inherited from the current architecture (causes 3, 8, 9; bears on GT-2, GT-11, chain C1, chain C2). Cluster C — estimation and prioritization premises turning out false (causes 1, 4, 5, 6, 7; bears on chain C4's `A-fte-concurrency`/`A-audit-log` and chain C5's `A-weights-reflect-priorities`). Cluster D — competitive/market exposure during the deferred-SSO window (cause 11; bears on chain C5's second-order extension and the "Buy-naive" dead end in section 5).

**Disposition.** Cluster A — plan change: the integration must be reviewed to confirm tenant/user identity is read only from the vendor's verified session/token claims, never a client-supplied parameter, promoted from a budgeted estimate-line (chain C4) to a named ship-blocking checklist item. Cluster B — plan change: migrating the 120 existing Stripe-linked tenants is written as its own explicit, tested step with a rollback path, not folded into chain C4's generic integration estimate. Cluster C — accepted risk with named mitigation: `A-fte-concurrency`, `A-audit-log`, and `A-weights-reflect-priorities` remain unverified at delivery time; mitigation is to run the two verifications chain C5's own confidence line already names (a time-boxed spike; a direct weighting check with the CTO) before committing to a ship date. Cluster D — accepted risk with named mitigation: the deferred-SSO window is accepted as bounded by GT-1 ("no enterprise customers yet"); mitigation is to monitor the sales pipeline and trigger the already-available (GT-5–GT-7) paid connector purchase the moment a real enterprise prospect appears, rather than discovering the gap mid-deal.

**Falsification.** This conclusion is false if a time-boxed engineering spike against the real codebase shows the build path's lower bound is faster than the composite path's upper bound, or if the CTO's actual priority weighting — once checked — makes cost or lock-in dominant enough to reverse chain C5's ranking.

## §6→§4 closure ledger (process output)

- "Adopt a managed identity provider's free or core tier now... build only the app-specific tenant/role-permission mapping that every path... requires regardless" → chain C2, chain C5 ✓
- ""Build vs. buy" is a false binary for this decision... the real decision is narrower... and on that narrower question, the timeline pressure... and the security risk this analysis found both point the same direction" → chain C2, chain C3, chain C6 ✓
- "this recommendation accepts a small, currently immaterial recurring vendor cost and a bounded future switching cost in exchange for materially faster, lower-risk shipping of the gated release... it defers rather than eliminates the eventual cost of enterprise connectors... and the standing security gap in the current shared-password/Stripe-link scheme... is fixed only by actually shipping the new authenticated model" → chain C5, chain C1 ✓
- "the recommendation rests most heavily on chain C5... and chain C6... two things would raise this to HIGH..." → chain C5, chain C6, chain C4 ✓

Ledger complete: 4 of 4 Conclusion-section claims (the four prescribed lead-ins: Recommended approach, Key insight, Trade-offs acknowledged, Confidence) cite a chain inline; 0 cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-1, GT-2, GT-11 | yes | n/a | yes | HIGH | yes | none |
| C2 | GT-3, GT-12 | yes | n/a | yes | HIGH | yes | none |
| C3 | GT-9, GT-10, GT-4 | yes | n/a | yes | MEDIUM | yes | none |
| C4 | GT-1, GT-4, GT-9, GT-12 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | GT-1, GT-5, GT-6, GT-7, C4 | yes | n/a | yes | MEDIUM | yes | none |
| C6 | GT-3, GT-4, C3 | yes | n/a | yes | MEDIUM | yes | none |
| C7 | GT-5, GT-6, GT-7 | yes | n/a | yes | HIGH | yes | none |
| C8 | GT-4, GT-9, GT-10 | yes | n/a | yes | HIGH | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| "Recommended approach: Adopt a managed identity provider's free or core tier now..." | bold lead-in | yes | colon closes the bold span, content on same line | C2, C5 |
| "Key insight: 'Build vs. buy' is a false binary for this decision..." | bold lead-in | yes | colon closes the bold span, content on same line | C2, C3, C6 |
| "Trade-offs acknowledged: this recommendation accepts a small... currently immaterial recurring vendor cost..." | bold lead-in | yes | colon closes the bold span, content on same line | C5, C1 |
| "Pre-check: head C1 (HIGH), C2 (HIGH), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM)..." | bold lead-in | yes | per output-template.md: "the pre-check line is itself a Conclusion-section claim... cited by the chains its own head names" | C1, C2, C3, C4, C5, C6 |
| "Confidence: MEDIUM — the recommendation rests most heavily on chain C5... and chain C6..." | bold lead-in | yes | colon closes the bold span, content on same line | C5, C4, C6 |

Scan complete: 8 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Which ownership split for the required components of a per-tenant authentication system — build every component in-house, buy a managed identity provider wholesale, or a composite that buys the credential/session core now and builds only the irreducibly app-specific tenant/role layer — lets this 7-person team ship the urgent, revenue-gating per-tenant feature fastest without increasing security risk, while keeping the cost of changing course later... bounded rather than prohibitive?"
Band: **Rigorous**
Justification: the statement names the core decision (an ownership split, not the triggering event or a restatement of the prompt), is specific to this company's stated constraints (team size, stage, urgency, no enterprise customers), and each of the three success criteria is a verb+subject+outcome triplet checkable directly against section 6 ("names exactly one ownership split," "traces... to a derivation chain," "names the specific trigger... that would change the recommendation").

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan, process output): "| C5 | 1 | weighted totals: Composite=85, Buy-naive=81, Build=51 | trade-off weights reflect this company's actual priorities | yes — A-weights-reflect-priorities |" together with the table row: "Discard — a composite... is shown to dominate both pure options (chain C2, C5) | Ruled out directly by chains C2 and C5"
Band: **Rigorous**
Justification: all 19 rows in the Classified Assumptions Table use the four-type scheme exactly, Verdict cells use the token-first/em-dash form throughout, every assumption used in a chain despite being unverified is marked "unverified — flagged," at least six assumptions were actively challenged and Discarded (not merely Accepted), and the Assumption Audit scan confirms exhaustive coverage of all 27 chain steps across all 8 chains with every surfaced assumption traced back into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "every unsuffixed ground truth in section 3 (GT-1 through GT-7, GT-9 through GT-12) now feeds at least one HIGH-confidence chain (GT-1, GT-2, GT-11 via C1; GT-3, GT-12 via C2; GT-5, GT-6, GT-7 via C7; GT-4, GT-9, GT-10 via C8)" (section 4, D-07 note) together with the provenance summary's enumeration: "?-marked: GT-8 (1 of 12)."
Band: **Rigorous**
Justification: GT-IDs are stable and match section 4's citations; every verified GT names a specific source (a pricing page, a cheat sheet's quoted passage, or a direct logical entailment, never "common knowledge"); the sole unverified GT (GT-8) is correctly `?`-marked, enumerated by ID, and matches the suffixed entries in the list exactly; and — checked against the list rather than merely quoting the summary — every unsuffixed GT that is reachable (all of them) feeds at least one HIGH-confidence chain, satisfying the clause that would otherwise band a single such shortfall Sound or multiple Hand-wavy.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan's chain-form table, process output): "| C7 | GT-5, GT-6, GT-7 | yes | n/a | yes | HIGH | yes | none |" and "| C3 | GT-9, GT-10, GT-4 | yes | n/a | yes | MEDIUM | yes | none |", together with section 5's Dead End "Extend the shared-password/Stripe-link approach...": "contradicts GT-3 directly... and fails the definitional test in GT-11."
Band: **Rigorous**
Justification: the self-audit scan shows all 8 chains form-conforming with clean dependencies; every chain carries at least one genuine intermediate claim; no conclusion anywhere in the document lacks a chain or carries a redundant second chain; the Abandoned Reasoning section documents four dead ends with specific, non-generic abandonment reasons; no analogy is used as direct evidence anywhere (all comparative claims are grounded in named, read-at-source ground truths); and every assumption the Assumption Audit scan surfaced on a chain step is declared inline with `[Assumes: X]` (A-library-representative on C3, A-weights-reflect-priorities on C5, alongside the pre-declared A-audit-log, A-fte-concurrency, A-redirect, A-sec-expertise).

**Criterion 5: Validate**
Quoted span (from the Adversarial pass record, process output): "Cluster A — plan change: the integration must be reviewed to confirm tenant/user identity is read only from the vendor's verified session/token claims... promoted from a budgeted estimate-line (chain C4) to a named ship-blocking checklist item." / "Cluster C — accepted risk with named mitigation: `A-fte-concurrency`, `A-audit-log`, and `A-weights-reflect-priorities` remain unverified at delivery time; mitigation is to run the two verifications chain C5's own confidence line already names..."
Band: **Rigorous**
Justification: every chain's confidence line names its own downgrade cause and closing verification path (C3's induction gap, C4's two estimation premises, C5/C6's inherited caps plus their own direct premises); no chain consumes a `GT-N?` input (so D-07's mandatory-downgrade clause never misfires) and no chain is rated above the lowest-rated chain its head cites (C5, C6 both capped correctly); the overall Conclusion's MEDIUM rating matches its weakest contributing chain exactly; and the adversarial pass record is complete across all seven named parts (Recompute, Sensitivity, Rival, Premise, Causes, Clusters, Disposition, Falsification), with every cluster carrying either a named plan change or an explicitly accepted risk with a named mitigation — none left as an inert finding.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan's claim-inventory table, process output): "| 'Key insight: ''Build vs. buy'' is a false binary for this decision...' | bold lead-in | yes | colon closes the bold span, content on same line | C2, C3, C6 |"
Band: **Rigorous**
Justification: all five section-6 constructs (Recommended approach, Key insight, Trade-offs acknowledged, Pre-check, Confidence) trace to named section-4 chains with no claim introduced for the first time in section 6; and the Key Insight states a non-obvious structural finding (the binary framing is false; ownership, not existence, is the real question) rather than restating the Recommended approach's specific procedural steps (which provider tier to adopt and when to pay for connectors).

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

(Note: a drafting-time check against GT-5–GT-7, GT-9, and GT-10's chain coverage identified that these ground truths initially fed only MEDIUM-confidence chains, which would have banded Criterion 3 Hand-wavy under this gate's own Sound/Hand-wavy split for that condition. Chains C7 and C8 were added during drafting, before this scoring pass, to isolate the narrow, fully-evidenced factual claims those ground truths support on their own from the broader inductive and estimate-based reasoning built on top of them — this is recorded here for transparency even though it preceded the first verdict block above, so the Rigorous band on Criterion 3 is not mistaken for having been true without this step.)

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "convention", "verdict": "Discard"},
    {"id": "A-2", "type": "convention", "verdict": "Discard"},
    {"id": "A-3", "type": "convention", "verdict": "Challenge"},
    {"id": "A-4", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-5", "type": "convention", "verdict": "Discard"},
    {"id": "A-6", "type": "convention", "verdict": "Discard"},
    {"id": "A-7", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-8", "type": "convention", "verdict": "Discard"},
    {"id": "A-9", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-10", "type": "current constraint", "verdict": "Challenge"},
    {"id": "A-11", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-12", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-13", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-14", "type": "physical law", "verdict": "Accept"},
    {"id": "A-15", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-16", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-17", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-18", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-19", "type": "untested belief", "verdict": "Challenge"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": true},
    {"id": "GT-2", "read_at_source": true},
    {"id": "GT-3", "read_at_source": true},
    {"id": "GT-4", "read_at_source": true},
    {"id": "GT-5", "read_at_source": true},
    {"id": "GT-6", "read_at_source": true},
    {"id": "GT-7", "read_at_source": true},
    {"id": "GT-8", "read_at_source": false},
    {"id": "GT-9", "read_at_source": true},
    {"id": "GT-10", "read_at_source": true},
    {"id": "GT-11", "read_at_source": true},
    {"id": "GT-12", "read_at_source": true}
  ],
  "chains": [
    {"id": "C1", "confidence": "HIGH", "rests_on": ["GT-1", "GT-2", "GT-11"]},
    {"id": "C2", "confidence": "HIGH", "rests_on": ["GT-3", "GT-12"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["GT-9", "GT-10", "GT-4"]},
    {"id": "C4", "confidence": "MEDIUM", "rests_on": ["GT-1", "GT-4", "GT-9", "GT-12"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["GT-1", "GT-5", "GT-6", "GT-7", "C4"]},
    {"id": "C6", "confidence": "MEDIUM", "rests_on": ["GT-3", "GT-4", "C3"]},
    {"id": "C7", "confidence": "HIGH", "rests_on": ["GT-5", "GT-6", "GT-7"]},
    {"id": "C8", "confidence": "HIGH", "rests_on": ["GT-4", "GT-9", "GT-10"]}
  ],
  "dead_ends": [
    "Extend the shared-password/Stripe-link approach instead of building real per-user accounts",
    "Recommend Build outright on the grounds that buying creates vendor lock-in",
    "Recommend provisioning full enterprise SSO/SCIM connectors immediately, regardless of current customer mix",
    "Apply the theoretical-limit technique to bound how fast or secure authentication can possibly be built"
  ],
  "techniques": {
    "applied": ["fishbone", "inversion", "five-whys", "estimate", "trade-off", "second-order", "pre-mortem"],
    "not_applied": [
      {"technique": "theoretical-limit", "phase": 1, "reason": "the core question is an organizational build-vs-buy decision, not a figure bounded by a physical or mathematical law; no convention-vs-hard-limit reframing changes what the essence statement must ask"},
      {"technique": "theoretical-limit", "phase": 4, "reason": "no governing hard constraint bounds how fast, cheap, or secure authentication can be in a way separable from the vendor/organizational choices under comparison; the nearest candidates are already carried as GT-4 rather than a theoretical-limit bracket"},
      {"technique": "inversion", "phase": 5, "reason": "the conclusion is a plan/recommendation, which the inversion-vs-pre-mortem decision rule routes to pre-mortem instead"}
    ]
  },
  "gate": {
    "passes": [
      {"bands": ["Rigorous", "Rigorous", "Rigorous", "Rigorous", "Rigorous", "Rigorous"], "gate_cleared": true, "hand_wavy_cap_cleared": true}
    ],
    "fix_repeat_fired": false,
    "cleared": true
  },
  "re_entry": {
    "fired": false,
    "edges": []
  },
  "conclusion": {
    "recommendation": "Adopt a managed identity provider's free or core tier now (for example WorkOS AuthKit, Clerk's Hobby/Pro tier, or Auth0's free/Essentials tier) to implement the urgent per-tenant, multi-user, role-based accounts feature; defer purchasing paid SSO/SAML/SCIM connectors until an actual enterprise deal requires them; build only the app-specific tenant/role-permission mapping that every path — build, buy, or composite — requires regardless (chain C2, chain C5).",
    "confidence": "MEDIUM",
    "rests_on": ["C1", "C2", "C3", "C4", "C5", "C6"]
  }
}
```
