**Disclosed:** the Self-Audit Gate's Fix/Repeat loop fired once. Pass 1 scored Criterion 2 Sound, because A-1 lacked the "unverified — flagged" note. It scored Criterion 3 Hand-wavy, because C4 was under-rated at MEDIUM on a rival that GT-4 settles, which left read-at-source GTs feeding only MEDIUM chains. The Fix flagged A-1 and re-rated C4 to HIGH, and the downstream pre-checks were updated. On re-score the gate cleared.

## Answer

**Recommendation:** Adopt a managed identity provider for credentials, sessions, reset and MFA. Keep tenancy, membership, roles, the isolation check and the product audit log in your own database, keyed by vendor user ID (chain C7). Do a one-day SDK and hash-export spike before committing (chain C7).

**Band (from §6):** MEDIUM. "Do not build" holds at every bracket end and under every single weight change (chains C3, C7). Choosing C over B is the soft part (chain C7).

**Would change it:** measured figures for the bracketed estimates §6 names (loaded cost, build and buy effort, MAU, ΔMRR), each through the verification path its chain's §4 line gives (chains C3, C7).
## 1. Problem Essence

**Core problem:** Which way of giving each user of ~120 paying tenants their own authenticated account gets the gated, billed feature to market soonest, at acceptable security, while costing the least 7-person-team engineering capacity, now and over the next year, and without closing off enterprise sales later?

The trigger (the CTO calls it urgent; the next release is billed) is not the question itself. The question is how to allocate the scarce resource, engineer-weeks, between authentication plumbing and the billed feature. "Build vs. buy" is how the problem is framed, and the answer can mix the two: buy part of the stack and own the rest.

**Success criteria:**
- The answer names an approach that satisfies the must-have: every request to the gated feature is tied to one individual, authenticated user who belongs to one specific tenant.
- The answer states the year-1 engineering-plus-subscription cost of each surviving option, with lower and upper bounds, and every figure recomputes.
- The answer states how many engineer-weeks each option takes away from the billed feature before it can ship.
- The answer names which security obligations (credential storage, MFA, NIST SP 800-63B SHALL requirements, tenant isolation) the team still owns under each option.
- The answer names the evidence that would reverse it.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: The gated feature needs individual per-tenant accounts. A shared password with a Stripe link cannot meet this. | current constraint | Record the expiry conditions | Accept — expires only if the feature is re-scoped to need no per-user identity; user-stated product requirement | unverified — flagged (GT-5?); user-stated product requirement, no source named |
| A-2: The quoted figures (~$40K MRR, ~120 tenants, 7 engineers, no enterprise customers) are accurate | untested belief | Verify, or flag as unverified | Accept — used as stated; carried as GT-5? | unverified — flagged (GT-5?) |
| A-3: A fully loaded engineer costs $150k–$250k a year (central $200k) | untested belief | Verify, or flag as unverified | Challenge — no payroll data supplied; bracketed instead of point-estimated | unverified — flagged (GT-7?) |
| A-4: Building auth on an OSS library to the NIST 800-63B level takes 4–10 engineer-weeks (central 6), covering sessions, reset, MFA, audit log, and invites. Upkeep is 0.10–0.25 FTE. | untested belief | Verify, or flag as unverified | Challenge — estimate, not measurement; bracketed | unverified — flagged (GT-8?) |
| A-5: Integrating a managed IdP takes 1–3 engineer-weeks (central 2), and upkeep is 0.02–0.05 FTE | untested belief | Verify, or flag as unverified | Challenge — estimate, not measurement; bracketed | unverified — flagged (GT-9?) |
| A-6: Each tenant has 2–20 active users (central 5), so 240–2,400 MAU (central 600) | untested belief | Verify, or flag as unverified | Challenge — drives vendor tier; bracketed | unverified — flagged (GT-10?) |
| A-7: "Auth is a core competency we should own" | convention | Explicitly challenge before use | Discard — the product's revenue does not come from authentication. The security-critical part it does own, tenant isolation, stays in-house under every option (GT-11), so the convention does not separate the options. | Ruled out by C6 |
| A-8: "Managed IdPs get expensive at scale" | convention | Explicitly challenge before use | Discard — at 240–2,400 MAU the published prices (GT-1, GT-2, GT-3) are at most $9,600/yr even for an over-specified plan. That is below the build option's upkeep alone (C3). | Read at source: GT-1, GT-2, GT-3 |
| A-9: The CTO's urgency is real: a slip in the billed release costs revenue | untested belief | Verify, or flag as unverified | Accept — direction accepted; magnitude unknown and carried as ΔMRR | unverified — flagged (GT-12?) |
| A-10: A managed IdP traps user credentials (no way out without forcing every password to be reset) | untested belief | Verify, or flag as unverified | Discard — Clerk exports hashed passwords from its dashboard, and Auth0 exports them by support ticket on paid tiers (GT-13). WorkOS was not checked. | Read at source: GT-13 |
| A-11: The IdP does not sit between the application and its database, so the app's own code must enforce tenant isolation | physical law | Accept as a ground-truth candidate | Accept — logical consequence of the architecture (tokens assert identity; queries run in the app) | GT-11 (definition) |
| A-12: A team-built auth stack gets no external security review unless one is paid for | untested belief | Verify, or flag as unverified | Accept — flagged; it affects the Security score of option A | unverified — flagged; surfaced in the Assumption Audit (C4 step) |
| A-13: The vendor's MFA and session handling stay as secure as published, with no outage or price change within year 1 | untested belief | Verify, or flag as unverified | Accept — flagged; the pre-mortem handles it as a named risk | unverified — flagged; surfaced in the Assumption Audit (C7 second-order step) |
| A-14: Engineer-weeks moved off the billed feature delay it roughly one-for-one (the work cannot be parallelised for free) | untested belief | Verify, or flag as unverified | Accept — flagged; if the team has slack, the delay cost in C5 shrinks but the cash-cost result (C3) does not change | unverified — flagged; surfaced in the Assumption Audit (C5 step) |

Inversion (Phase 2) was applied to the claim "buying a managed IdP will work for this team". It asked which conditions would guarantee that buying fails: credential lock-in, pricing jumps inside the MAU bracket, the vendor not covering MFA, the vendor owning tenant isolation, and SDK mismatch with the stack. Those conditions produced rows A-6, A-8, A-10, A-11 and A-13. The SDK fit for the team's stack is not covered by any of these rows. It is not known, and it is carried into the Conclusion as a pre-commit check rather than a ground truth.

## 3. Ground Truths

- **GT-1** Clerk pricing:
  - Pro costs "$25/mo" ("$20/mo billed annually"), with a "50,000 MRU limit per app".
  - MFA is a Pro and Business feature and is absent from Hobby.
  - B2B auth is "Included (Free in all plans)" with "100 MRO included per app". The enhanced add-on costs "$100/mo ($85/mo billed annually)".
  - Enterprise SSO has "1 connection included per app", then "$75/mo each" for connections 2–15.
  - Application logs are kept "7 day retention" on Pro.
  - source: clerk.com/pricing; read-at-source: pricing page, quoted passages above (fetched 2026-09-30). Limitation: the overage price for organizations beyond 100 MRO was not located.
- **GT-2** WorkOS pricing:
  - AuthKit's "First 1M MAUs" are "Free". AuthKit "includes … MFA … and enterprise SSO".
  - SSO costs "$125/ea" for connections 1–15.
  - Audit Logs cost "$125/mo" per SIEM stream plus "$99/mo" per 1M events.
  - source: workos.com/pricing; read-at-source: pricing page, quoted passages above.
- **GT-3** Auth0 pricing:
  - Free is "Up to 25,000 monthly active users" with 5 organizations.
  - B2B Essentials starts at "$150/month for 500 MAUs" and includes "Pro Multi-Factor Authentication" and unlimited organizations, with 3 enterprise SSO connections and extra connections at $100/month.
  - B2B Professional starts at "$800/month for 500 MAUs".
  - source: auth0.com/pricing; read-at-source: pricing page, quoted passages above. Limitation: the Essentials price between 500 and 2,400 MAU was not located.
- **GT-4** NIST SP 800-63B (rev. 4):
  - Verifiers "SHALL require passwords that are used as a single-factor authentication mechanism to be a minimum of 15 characters".
  - They "SHALL compare the prospective secret against a blocklist".
  - They "SHALL limit consecutive failed authentication attempts … to no more than 100".
  - They "SHALL NOT require subscribers to change passwords periodically".
  - source: pages.nist.gov/800-63-4/sp800-63b.html; read-at-source: the password-verifier requirements, quoted.
- **GT-5?** The company has ~$40K MRR, ~120 paying tenants, 7 engineers and no enterprise customers. Access is currently a shared password plus a Stripe customer link. The gated feature requires authenticated per-tenant accounts and is the next billed release. — unverified: supplied by the user with no source named.
- **GT-6** Definitions used in the arithmetic: annual = monthly × 12; weekly cost = annual cost ÷ 52; team capacity per month = engineers × 52 ÷ 12 engineer-weeks; ARR = MRR × 12. — source: definition; read-at-source: not applicable (identities, not citations).
- **GT-7?** A fully loaded engineer costs $150k / $200k / $250k a year (low / central / high), which is $2,884.62 / $3,846.15 / $4,807.69 per week. — unverified: estimate; no payroll data supplied.
- **GT-8?** Building in-house takes 4 / 6 / 10 engineer-weeks initially and 0.10 / 0.15 / 0.25 FTE of upkeep. — unverified: estimate; no codebase or library named.
- **GT-9?** Integrating a managed IdP takes 1 / 2 / 3 engineer-weeks and 0.02 / 0.03 / 0.05 FTE of upkeep. Owning tenancy alongside it (option C) adds 1 week (3 weeks) and 0.04 FTE. — unverified: estimate.
- **GT-10?** Users per tenant are 2 / 5 / 20, so MAU = 120 × that = 240 / 600 / 2,400. — unverified: no usage data supplied.
- **GT-11** A managed IdP authenticates the user and issues a token. The application's own queries select the tenant's data, so tenant isolation is enforced by application code under every option. — source: definition of token-based authentication architecture; read-at-source: not applicable (structural definition).
- **GT-12?** The gated feature's revenue uplift ΔMRR is unknown. It is used only symbolically, with an illustrative $4,000. — unverified: not supplied.
- **GT-13** Clerk: admins "can export and download a CSV file containing a list of their application's users that includes their hashed passwords". Auth0: hash export is requested "by opening a support ticket" and is "not available for our Free subscription tier". — source: clerk.com/docs/deployments/exporting-users; auth0.com/docs/…/export-data; read-at-source: the quoted passages.

**Provenance summary:**

```text
?-marked: GT-5?, GT-7?, GT-8?, GT-9?, GT-10?, GT-12? (6 of 13)
Read-at-source: GT-1 — clerk.com/pricing (Pro price, MRU, MFA tier, B2B/MRO, SSO lines quoted)
Read-at-source: GT-2 — workos.com/pricing (AuthKit 1M MAU free, SSO $125/ea, MFA included quoted)
Read-at-source: GT-3 — auth0.com/pricing (B2B Essentials $150/500 MAU, MFA included, Professional $800 quoted)
Read-at-source: GT-4 — NIST SP 800-63B-4 password verifier SHALL clauses quoted
Read-at-source: GT-13 — Clerk export-users doc and Auth0 export-data doc, quoted
Definitions (no citation to read): GT-6, GT-11
Phase 3 failure records: none — every source opened and located the asserted wording; the unlocated sub-figures (Clerk >100 MRO overage, Auth0 500–2,400 MAU price) are recorded as limitations on GT-1/GT-3 and bounded in C3 by an over-specified plan price
```
## 4. Derivation Chains

### Conclusion C1: The status quo (shared password + Stripe link) is knocked out, not scored

GT-5? (feature requires per-tenant accounts; current access is one shared password) + GT-4 (NIST verifier SHALLs are per-subscriber)
→ a single shared secret authenticates "someone who knows the password", not a specific user of a specific tenant
→ no request can be attributed to an individual or bound to one tenant, so MFA, rate-limiting per account and a per-user audit trail cannot exist on it
→ the status quo fails the must-have and is eliminated before scoring

**Pre-check:** head GT-5?, GT-4 · ?-marked: GT-5? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short: GT-5? (the feature requirement) is user-stated with no source; confirming the feature spec requires per-user, per-tenant identity would remove it. Inference is deductive; the rival (per-tenant shared passwords) is ruled out in §5.

### Conclusion C2: Year-1 cost of building in-house is $26,538 / $53,077 / $110,577 (low / central / high)

GT-6 (weekly = annual ÷ 52) + GT-7? (loaded cost $150k/$200k/$250k) + GT-8? (4/6/10 eng-weeks; 0.10/0.15/0.25 FTE)
→ initial build: 4 × 150,000/52 = $11,538.46; 6 × 200,000/52 = $23,076.92; 10 × 250,000/52 = $48,076.92
→ year-1 upkeep: 0.10 × 150,000 = $15,000; 0.15 × 200,000 = $30,000; 0.25 × 250,000 = $62,500
→ year-1 build total: 11,538.46 + 15,000 = $26,538.46; 23,076.92 + 30,000 = $53,076.92; 48,076.92 + 62,500 = $110,576.92

**Pre-check:** head GT-6, GT-7?, GT-8? · ?-marked: GT-7?, GT-8? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short: GT-7? (replace with actual payroll-plus-overhead per engineer) and GT-8? (replace with a one-day spike sizing the chosen OSS library against the feature list) are estimates; arithmetic recomputes exactly; the bracket bounds the shortfall.

### Conclusion C3: Buying is cheaper in year 1 at every bracket end — paired saving $785 / $37,885 / $100,769

C2 (build total bracket) + GT-1 (Clerk $25 + $100 B2B add-on) + GT-2 (WorkOS AuthKit free to 1M MAU) + GT-3 (Auth0 B2B $150 / $800 per month at 500 MAU) + GT-7? (loaded cost) + GT-9? (1/2/3 eng-weeks; 0.02/0.03/0.05 FTE) + GT-10? (240–2,400 MAU)
→ subscription at 240–2,400 MAU: WorkOS $0 × 12 = $0; Clerk (25 + 100) × 12 = $1,500; Auth0 Professional, an over-specified upper bound, 800 × 12 = $9,600
→ buy-favourable end: 1 × 250,000/52 + 0.02 × 250,000 + 0 = 4,807.69 + 5,000 = $9,807.69, against build $110,576.92, saving $100,769.23
→ central: 2 × 200,000/52 + 0.03 × 200,000 + 1,500 = 7,692.31 + 6,000 + 1,500 = $15,192.31, against build $53,076.92, saving $37,884.62
→ build-favourable end: 3 × 150,000/52 + 0.05 × 150,000 + 9,600 = 8,653.85 + 7,500 + 9,600 = $25,753.85, against build $26,538.46, saving $784.62
→ the saving stays positive at both ends, so the cash comparison does not depend on which estimate is right
→ the largest plausible subscription ($9,600) is 9,600 / 480,000 = 2.0% of ARR, while Clerk at $1,500 is 0.3125% of ARR

**Pre-check:** head C2 (MEDIUM), GT-1, GT-2, GT-3, GT-7?, GT-9?, GT-10? · ?-marked: GT-7?, GT-9?, GT-10? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short: C2 is MEDIUM. GT-7? (actual loaded cost) and GT-9? (an integration spike against the chosen vendor's SDK) are estimates. GT-10? (count MAU from the planned user list) is also an estimate, but its effect is bounded by pricing an over-specified plan. The build-favourable end pairs the cheapest build with the most expensive buy on the same rate, which is the sign test; it still clears zero by only $785, which is why this is not HIGH even apart from inputs.

### Conclusion C4: Building makes the team the owner of at least four NIST SHALL clauses plus MFA; buying moves MFA to an included vendor feature

GT-4 (15-char minimum, blocklist, ≤100 failed attempts, no forced rotation) + GT-1 (MFA in Clerk Pro) + GT-2 (MFA in AuthKit) + GT-3 (MFA in Auth0 B2B Essentials)
→ any in-house verifier must implement and keep current at least those four SHALL clauses, plus MFA enrolment, recovery and reset flows *[Assumes: A-12 — no external security review unless paid for]*
→ each of the three vendors read lists MFA as included in a plan priced at or below $150/month
→ buying removes MFA and credential storage from the team's code, while building leaves every one of those obligations on the team

**Pre-check:** head GT-4, GT-1, GT-2, GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — inputs are all read at source (GT-1, GT-2, GT-3 pricing pages; GT-4 SHALL clauses quoted). Each hop is a deduction from those quotes. The strongest rival is that a well-chosen OSS library already implements the blocklist, rate limit and MFA, so building owns nothing extra. GT-4 rules it out: its SHALLs bind "verifiers", and a self-hosted stack makes the team the verifier. A library changes how much code the team writes, not who owns the obligation. That magnitude effect is priced in C2's 4-week low end. A-12 qualifies the first hop: if the team pays for external review, building costs more and the endpoint still stands.

### Conclusion C5: Buying frees ~4 engineer-weeks for the billed feature — 13.2% of one team-month — and each week of slip costs ΔMRR × 12/52

GT-6 (capacity = 7 × 52/12) + GT-8? (central build 6 eng-weeks) + GT-9? (central buy 2 eng-weeks) + GT-12? (ΔMRR unknown)
→ central diversion difference: 6 − 2 = 4 engineer-weeks
→ team capacity: 7 × 52 / 12 = 30.33 engineer-weeks per month, so 4 / 30.33 = 13.19% of one month *[Assumes: A-14 — diverted weeks delay the feature one-for-one]*
→ revenue at stake per week of slip: ΔMRR × 12 / 52, e.g. 4,000 × 12 / 52 = $923.08 a week, so $3,692.31 over 4 weeks at an illustrative $4,000 ΔMRR
→ the CTO's urgency points the same way as the cash result in C3, which is buying

**Pre-check:** head GT-6, GT-8?, GT-9?, GT-12? · ?-marked: GT-8?, GT-9?, GT-12? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short: GT-8? and GT-9? (spike both), GT-12? (the expected ΔMRR of the billed feature from pricing/pipeline). A-14 is priced: if the team has slack, the slip cost falls toward $0 but the direction (buy ships no later) is unaffected, since building's 4–10 weeks exceeds buying's 1–3 at every bracket point.

### Conclusion C6: Tenant isolation is built in-house under every option, so the bought component is credentials, sessions and MFA — not authorization

GT-11 (app queries select tenant data) + GT-1 (Clerk organizations) + GT-3 (Auth0 organizations)
→ a vendor's organization claim in a token only says which tenant the user belongs to; the application's query must still filter by that tenant
→ the per-tenant access check, the most security-critical line for a B2B product, is written and tested by this team whether it builds or buys
→ "own your auth because it is security-critical" does not tell the options apart, because the critical part is owned under both

**Pre-check:** head GT-11, GT-1, GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — inputs are a structural definition (GT-11) and pricing pages read at source (GT-1, GT-3); every hop is deductive. The rival, that the vendor's org model enforces isolation, is ruled out by GT-11 in §5 ("Let the vendor own tenancy and isolation"); C6 rests on GT-11, GT-1 and GT-3.

### Conclusion C7: Weighted trade-off — buy authentication, own tenancy (option C) scores 103 vs. buy-everything (B) 101 vs. build (A) 58 — recommend C

C1 (status quo out) + C3 (cost) + C4 (security obligations) + C5 (time-to-ship) + C6 (tenancy owned anyway) + GT-1 (SSO $75/conn) + GT-2 (SSO $125/conn) + GT-3 (SSO $100/conn) + GT-13 (hash export exists)
→ weighted totals on locked weights: C = 103, B = 101, A = 58, driven by time-to-ship ×5 and security ×5, with A losing on both
→ no single weight change in the 1–5 range closes the 45-point gap between A and C, so "do not build" is robust
→ C beats B only on exit flexibility, and on unrounded scores B leads by 2.31, so C vs B is a near-tie
→ recommend C, because the tenant-membership table it adds is already needed for isolation (C6), so its extra cost is small
→[2nd] actor lens: every tenant user must now create an account, so a one-time invite-and-migrate step off the shared password is needed under every option
→[2nd] actor lens: once accounts are individual, attackers move from guessing the one shared password to credential stuffing individual accounts; the vendor's rate-limiting and MFA absorb this *[Assumes: A-13 — vendor security and pricing hold through year 1]*
→[2nd] time lens: at a few cycles, MAU growth crosses vendor tier boundaries (Auth0 Essentials is priced from 500 MAU, inside the 240–2,400 bracket), but the over-bound in C3 already prices it
→[3rd] time lens: once enterprise customers arrive, SSO becomes a per-connection cost of $75–$125 a month, passed into enterprise pricing, instead of a SAML project
→[3rd] actor lens: the vendor gains pricing leverage as the user base grows; owning tenancy and keeping hash export available (GT-13) caps that leverage

**Pre-check:** head C1 (MEDIUM), C3 (MEDIUM), C4 (HIGH), C5 (MEDIUM), C6 (HIGH), GT-1, GT-2, GT-3, GT-13 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short: C1, C3 and C5 are MEDIUM, each explaining its own downgrade. The A-vs-buy result is robust. The C-vs-B choice is a near-tie that rests on the exit-flexibility criterion. Checking that the chosen vendor exports hashes (GT-13 covers Clerk and Auth0; WorkOS is unread) would settle whether B's exit cost is really higher. No second-order effect contradicts a ground truth. A-13 qualifies a second-order step only, not the endpoint.
## 5. Abandoned Reasoning

### Dead End: Per-tenant shared passwords as a cheap middle path

**What was tried:** Keep the existing mechanism and give each tenant its own shared password, so access is "per-tenant" without user accounts.

**Why abandoned:** The feature requires per-tenant accounts (GT-5?). A per-tenant secret still identifies only "someone at tenant X". Per-account MFA, per-account lockout and a per-user audit trail are therefore impossible (C1, GT-4).

**What it ruled out:** Any option without individual identities. The status quo and every variation of it fail the must-have.

### Dead End: Build, because vendor subscriptions grow with users

**What was tried:** Argue that a managed IdP's per-MAU pricing makes building cheaper over time (convention A-8).

**Why abandoned:** At 240–2,400 MAU, the most expensive plan considered costs $9,600 a year, which is less than the build option's lowest-case upkeep of $15,000. The paired saving stays positive even at the build-favourable end, at $784.62 (C3, from GT-1, GT-2 and GT-3). Clerk's 50,000-MRU Pro allowance and WorkOS's free 1M MAU are 20× and 416× above the top of the bracket (50,000 / 2,400 = 20.8; 1,000,000 / 2,400 = 416.7).

**What it ruled out:** Cost growth is not a reason to build at this company's scale. Revisit only if MAU approaches tens of thousands.

### Dead End: Let the vendor own tenancy and isolation (option B as "enforcement")

**What was tried:** Treat the vendor's organization model as the source of truth for tenancy, and as enforcement of tenant isolation, which would save the membership table.

**Why abandoned:** Organization claims only say which tenant a user belongs to. The app's own queries still have to filter by tenant (GT-11, C6). The membership mapping and the isolation check are built either way, so B saves less than it seems to. It scores 101 against C's 103, a near-tie decided on exit flexibility (C7).

**What it ruled out:** That buying removes the team's security-critical code. It removes credential, session and MFA code only.

### Dead End: Theoretical-limit floor on build effort

**What was tried:** Derive a hard lower bound on build engineer-weeks from first principles.

**Why abandoned:** Build effort is set by conventions (the library chosen, the feature scope) and no physical law sets it. No law gives a floor tighter than "more than zero". The estimate procedure with explicit brackets (C2) is the right tool.

**What it ruled out:** Any claim that building "cannot" be fast. A fast build is possible, and C3 shows that even the fastest build in the bracket, against the slowest buy, does not reverse the cash result.

## 6. Conclusion

**Recommended approach:** Adopt a managed identity provider for authentication (credentials, sessions, password reset, MFA). Keep tenancy, membership, roles, the per-tenant isolation check and the product's own audit log in your database, keyed by the vendor's user ID — option C (chain C7). Before committing to a vendor, run a one-day spike against your stack's SDK and confirm that hashed passwords can be exported (chain C7).

**Key insight:** The security-critical code in a B2B product, tenant isolation, is written by this team under every option (chain C6). So the build-vs-buy decision is only about credential, session and MFA plumbing. There, building costs $26.5k–$110.6k in year 1 against $9.8k–$25.8k for buying (chain C3), and it takes about 4 more engineer-weeks away from the billed release (chain C5).

**Trade-offs acknowledged:** You accept a vendor dependency, a price that rises with MAU, and roughly $1,500–$9,600 a year in subscription, at most 2.0% of ARR (chain C3). You also accept a near-tie between owning tenancy (C) and handing it to the vendor (B), which this analysis breaks on exit flexibility rather than cost (chain C7). Enterprise SSO later costs $75–$125 per connection per month instead of a SAML project (chain C7).

**Pre-check:** head C1 (MEDIUM), C3 (MEDIUM), C4 (HIGH), C5 (MEDIUM), C6 (HIGH), C7 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Conclusion rests on C1, C3, C5 and C7, all MEDIUM, and on C4 and C6, both HIGH (chain C7). The estimates behind them (loaded cost, build and buy effort, MAU, ΔMRR) are bracketed rather than measured, and each named chain's §4 line gives its verification path. "Do not build" is robust: it holds at every bracket end and under every single weight change (chains C3, C7). The choice of C over B is the soft part (chain C7).
## Appendix — process output

## Trade-off analysis (process output)

### Options
- **A** — build in-house on an OSS library: sessions, reset, MFA, audit log, invites, tenancy.
- **B** — managed IdP for everything, including tenancy and roles in the vendor's organization model.
- **C** — composite: managed IdP for credentials, sessions and MFA; tenancy, membership, roles, isolation and the product audit log in your own DB, keyed by vendor user ID.
- **D** — status quo (shared password + Stripe link). **Knocked out** by the must-have "each request is attributable to one authenticated user of one tenant" (C1).
- Build-now-buy-later is a composite folded into A's exit cost. It was not scored separately, because migrating off a self-built store later costs an A build plus a B integration.

### Criteria & Weights (locked before scoring)
| Criterion | Weight | 1 means | 5 means |
|---|---|---|---|
| Time-to-ship (eng-weeks before release) | 5 | ≥10 | ≤2 (linear between: 1 + 4(10−w)/8, rounded) |
| Authn security posture | 5 | team-written crypto, sessions and MFA with no external review | vendor-maintained MFA and credential store |
| Year-1 cost | 3 | ≥$80k | ≤$15k (linear: 1 + 4(80k−x)/65k, rounded) |
| Ongoing engineering load | 4 | ≥0.25 FTE | ≤0.03 FTE (linear: 1 + 4(0.25−f)/0.22, rounded) |
| Exit flexibility | 2 | identities and tenancy only in the vendor; leaving forces every password to be reset | all identity data in own DB |
| Enterprise path (SSO/SCIM) | 2 | SAML built in-house | per-connection toggle |

### Scoring
Unrounded values, recomputed:
- A: time 1 + 4(10−6)/8 = 3; cost 1 + 4(80,000−53,076.92)/65,000 = 2.657 → 3; load 1 + 4(0.10)/0.22 = 2.818 → 3.
- B: time 1 + 4(8)/8 = 5; cost 1 + 4(80,000−15,192.31)/65,000 = 4.988 → 5; load 5.
- C: time 1 + 4(7)/8 = 4.5 → 5; cost on $21,038.46, which is 3 × 50,000/52 + 0.04 × 200,000 + 1,500 = 11,538.46 + 8,000 + 1,500, gives 1 + 4(58,961.54)/65,000 = 4.628 → 5; load 1 + 4(0.21)/0.22 = 4.818 → 5.

Exit flexibility for B was scored 3, not 2, because GT-13 (hash export exists) was read before the totals were computed. This is disclosed: it is a score change backed by evidence, not a weight change.

| Option | Time ×5 | Security ×5 | Cost ×3 | Load ×4 | Flex ×2 | Enterprise ×2 | Total |
|---|---|---|---|---|---|---|---|
| A | 3×5=15 (GT-8?) | 2×5=10 (C4) | 3×3=9 (C2) | 3×4=12 (GT-8?) | 5×2=10 | 1×2=2 (GT-1/2/3) | **58** |
| B | 5×5=25 (GT-9?) | 5×5=25 (C4) | 5×3=15 (C3) | 5×4=20 (GT-9?) | 3×2=6 (GT-13) | 5×2=10 (GT-1/2/3) | **101** |
| C | 5×5=25 (GT-9?) | 5×5=25 (C4) | 5×3=15 (C3) | 5×4=20 (GT-9?) | 4×2=8 (GT-13, C6) | 5×2=10 (GT-1/2/3) | **103** |

Recompute: A = 15+10+9+12+10+2 = 58. B = 25+25+15+20+6+10 = 101. C = 25+25+15+20+8+10 = 103.

### Recommendation
C (103), then B (101), then A (58).

**Flip test, A vs C:** the most A can gain from one weight change is Security 5→1, a gain of 4 × (5−2) = 12, which leaves A behind by 33. Time 5→1 gains 4 × 2 = 8. Flex 2→5 gains 3 × 1 = 3. **No single weight change flips A vs C.**

**Flip test, C vs B:** the rounded totals differ only on Flex, so C − B = w_flex × (4−3). That stays positive for every w_flex from 1 to 5, so no single weight change flips the result. On unrounded scores, however, C − B = 5(4.5−5) + 3(4.628−4.988) + 4(4.818−5) + 2(4−3) = −2.5 − 1.08 − 0.73 + 2 = −2.31, so B leads. **C vs B is a near-tie**, and the result above comes from rounding. The tie is broken toward C because its extra component, the membership table, is needed for isolation anyway (C6).
## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | shared secret identifies "someone" | no | n/a |
| C1 | 2 | no attribution → no MFA/lockout/audit | no | n/a |
| C1 | 3 | status quo knocked out | no | n/a |
| C2 | 1 | initial build $ bracket | no (GT-7?, GT-8? already A-3/A-4) | n/a |
| C2 | 2 | upkeep $ bracket | no | n/a |
| C2 | 3 | year-1 build totals | no | n/a |
| C3 | 1 | subscription bracket | no (A-6, A-8) | n/a |
| C3 | 2 | buy-favourable end | no | n/a |
| C3 | 3 | central | no | n/a |
| C3 | 4 | build-favourable end | no | n/a |
| C3 | 5 | sign holds at both ends | no | n/a |
| C3 | 6 | ≤2.0% ARR | no (A-2) | n/a |
| C4 | 1 | in-house must implement SHALLs + MFA | yes — A-12 no external review unless paid | yes (A-12) |
| C4 | 2 | vendors include MFA ≤$150/mo | no | n/a |
| C4 | 3 | buy moves MFA/credential code off team | no | n/a |
| C5 | 1 | 6 − 2 = 4 eng-weeks | no | n/a |
| C5 | 2 | 13.19% of a team-month | yes — A-14 diverted weeks delay feature one-for-one | yes (A-14) |
| C5 | 3 | ΔMRR × 12/52 per week | no (A-9) | n/a |
| C5 | 4 | urgency aligns with buy | no | n/a |
| C6 | 1 | org claim ≠ query filter | no (A-11) | n/a |
| C6 | 2 | isolation check written either way | no | n/a |
| C6 | 3 | security-criticality doesn't discriminate | no (A-7) | n/a |
| C7 | 1 | weighted totals | no | n/a |
| C7 | 2 | A-vs-C robust | no | n/a |
| C7 | 3 | C vs B near-tie | no | n/a |
| C7 | 4 | recommend C | no | n/a |
| C7 | 5 | [2nd] user migration | no (A-1) | n/a |
| C7 | 6 | [2nd] attacker shift absorbed by vendor | yes — A-13 vendor security/pricing hold year 1 | yes (A-13) |
| C7 | 7 | [2nd] MAU tier crossing priced | no (A-6) | n/a |
| C7 | 8 | [3rd] SSO per connection | no | n/a |
| C7 | 9 | [3rd] vendor leverage capped by export | no (A-10) | n/a |

## Techniques not applied (process output)

- theoretical-limit (Phase 1) — not applicable — the core question is an allocation choice, and no figure is a convention mistaken for a hard bound
- theoretical-limit (Phase 4) — not applicable — no physical law bounds build effort; see §5, "Theoretical-limit floor on build effort"
- fishbone — not applicable — the assumption space was listable through inversion and is not multi-causal
- five-whys (reduce-to-primitives) — not applicable — the ground truths are quoted vendor or NIST text, definitions, or bracketed estimates, with no compound claim left to reduce
## Adversarial pass (process output)

**Recompute:** every figure was redone independently with an exact-fraction calculator.
- C2:
  - 4×150,000/52 = 11,538.46; 6×200,000/52 = 23,076.92; 10×250,000/52 = 48,076.92.
  - Upkeep: 15,000; 30,000; 62,500.
  - Totals: 26,538.46; 53,076.92; 110,576.92 ✓
- C3:
  - Buy totals: 4,807.69 + 5,000 = 9,807.69; 7,692.31 + 6,000 + 1,500 = 15,192.31; 8,653.85 + 7,500 + 9,600 = 25,753.85.
  - Savings: 100,769.23; 37,884.62; 784.62.
  - Subscriptions: (25+100)×12 = 1,500; 800×12 = 9,600. Shares of ARR: 9,600/480,000 = 2.0% and 1,500/480,000 = 0.3125% ✓
- C5: 7×52/12 = 30.33; 4/30.33 = 13.19%; 4,000×12/52 = 923.08; ×4 = 3,692.31 ✓
- §5: 50,000/2,400 = 20.83; 1,000,000/2,400 = 416.67 ✓
- Trade-off totals: 58 / 101 / 103, and the unrounded C−B is −2.31 ✓
- Every scaled figure lands above its base. One correction was made during drafting: an early C-cost figure of $18,153.85 used the $150k rate where the central $200k rate belongs. It was corrected to $21,038.46 before any chain used it.

**Sensitivity:** the flip ground truth is **GT-8?** (build effort and upkeep), which is `?`-marked. At the central rate and a 2-engineer-week build, building matches buying only if build upkeep is ≤ 15,192.31 − 2×3,846.15 = $7,500 a year, which is 7,500/200,000 = 0.0375 FTE. That is about the same as the vendor's upkeep, so the flip needs a build that is as cheap to keep running as a bought one. A confidence caveat is applied, with no new cap; C2 and C3 already carry MEDIUM.

Weakest link per chain:
- C1: GT-5? (the feature spec)
- C2: GT-8? (upkeep FTE)
- C3: the $784.62 margin at the build-favourable end
- C4: the unnamed OSS library's coverage, which changes effort (C2) but not ownership
- C5: GT-12? (ΔMRR)
- C6: none (deductive)
- C7: C vs B decided by rounding

**Rival:**
- Headline rival: build is better because a framework-native auth library makes it ~2 weeks. This is ruled out unless upkeep is ≤0.0375 FTE (Sensitivity, C3). Recorded in §5, "Build, because vendor subscriptions grow with users", for the cost side.
- C1 rival: per-tenant shared passwords, ruled out in §5.
- C2: rival not applicable — it is a bracketed computation, and the bracket is the rival range.
- C3 rival: building is cheaper over a longer horizon, ruled out in §5 by the 20.8× / 416.7× headroom.
- C4 rival: an OSS library already covers the SHALLs. Ruled out on C4's Confidence line by GT-4: the SHALLs bind the verifier, which a self-hosted stack makes the team.
- C5 rival: the team has slack, so there is no slip. Priced via A-14 on C5's Confidence line.
- C6 rival: the vendor enforces isolation, ruled out in §5 by GT-11.
- C7 rival: option B, a near-tie recorded in §5, "Let the vendor own tenancy and isolation".

**Premise:** it is March 2027. Adopting a managed IdP and owning tenancy (option C) failed badly. The billed feature slipped, tenants churned during the account migration, and the team is now ripping out the vendor.

**Causes** (unfiltered, from four viewpoints):
- Implementer (engineer):
  1. The vendor SDK did not fit the backend framework, and the integration took 6 weeks, not 2.
  2. Vendor user records and the local membership table drifted apart through missed webhooks.
  3. The vendor session model conflicted with the existing Stripe-link flow.
  4. Migrating existing users off the shared password was never estimated.
- Tenant user / admin:
  5. Invite emails went to spam.
  6. Users locked themselves out and support was overwhelmed.
  7. Tenants used to one shared login resisted per-user accounts.
  8. MFA prompts annoyed users at a launch-critical moment.
- Payer (CFO):
  9. 120 orgs exceeded Clerk's 100 included MRO and the overage was a surprise.
  10. Auth0's price stepped up above 500 MAU.
  11. The first enterprise prospect also needed SCIM, priced per connection.
- Attacker / competitor:
  12. Credential stuffing hit the newly created accounts.
  13. A vendor outage during launch week locked every tenant out.
  14. A competitor won a deal on "we already have SSO" while the release slipped.

**Clusters:**
- **K1 — local vs vendor identity sync** (causes 2, 3): bears on C6 and C7. Costly but survivable.
- **K2 — pricing edges this analysis did not read** (causes 9, 10, 11): bears on GT-1, GT-3, GT-10? and C3. Costly but survivable, bounded at 2.0% of ARR.
- **K3 — user migration and adoption** (causes 4, 5, 6, 7, 8): bears on GT-5?, A-1, and the C7 second-order step on user migration. Costly but survivable.
- **K4 — single vendor dependency at launch** (causes 12, 13): bears on A-13 and C4. Costly but survivable.
- **K5 — integration-effort estimate** (causes 1, 14): bears on GT-9? and C5. Costly but survivable. This cluster embarrasses the conclusion most directly: if no vendor SDK fits, the time-to-ship advantage disappears.
- No cluster is fatal: each one has a working fallback (another vendor, or delaying migration of non-gated features).

**Disposition:**
- **K1** — plan change: the local membership table is authoritative; vendor webhooks are consumed idempotently; a nightly reconcile job compares the two. Tripwire: reconcile finds more than 0 mismatches on two consecutive nights. Owner: auth engineer, daily.
- **K2** — accepted risk with mitigation: read the org- or MAU-overage line before signing; C3's $9,600 over-bound caps the exposure. Tripwire: first invoice above $200 a month. Owner: CTO, monthly.
- **K3** — plan change: staged rollout. Non-gated surfaces stay on the old access path through a migration window, tenant admins send invites, and passwordless magic links are offered. Tripwire: fewer than 60% of tenants have at least one activated account 14 days after invites go out. Owner: customer-success lead, weekly.
- **K4** — accepted risk with mitigation: subscribe to the vendor status page; keep a break-glass admin path for support staff; turn on the vendor's rate-limiting and MFA from day one. Tripwire: a vendor incident during launch week, or failed-login rate above 5× the baseline. Owner: on-call.
- **K5** — plan change, already in §6: a one-day spike before committing, reaching end-to-end login plus one tenant-scoped request. Tripwire: the spike has not reached that point by the end of day 2, in which case switch to the next vendor. Owner: tech lead.

**Falsification:** the conclusion is false if either of these holds:
- A spike shows the team's framework provides MFA-capable, NIST-SHALL-compliant auth in ≤2 engineer-weeks with measured upkeep of ≤0.0375 FTE.
- No managed IdP's SDK supports the stack well enough to pass the K5 spike.
## §6→§4 closure ledger (process output)

- "Adopt a managed identity provider for authentication … option C" → chain C7 ✓
- "Key insight: tenant isolation written either way; build $26.5k–$110.6k vs buy $9.8k–$25.8k; ~4 more eng-weeks diverted" → chains C6, C3, C5 ✓
- "Trade-offs acknowledged: vendor dependency, $1,500–$9,600/yr ≤2.0% ARR, C-vs-B near-tie, SSO per connection" → chains C3, C7 ✓
- "Pre-check: head C1…C7 (C4 HIGH after Fix)" → chains C1, C3, C4, C5, C6, C7 ✓
- "Confidence: MEDIUM …" → chains C7, C3 ✓

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-5? + GT-4 | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-6 + GT-7? + GT-8? | yes | n/a | yes | MEDIUM | no | none |
| C3 | C2 + GT-1 + GT-2 + GT-3 + GT-7? + GT-9? + GT-10? | yes | n/a | yes | MEDIUM | yes | none |
| C4 | GT-4 + GT-1 + GT-2 + GT-3 | yes | n/a | yes | HIGH | yes | none |
| C5 | GT-6 + GT-8? + GT-9? + GT-12? | yes | n/a | yes | MEDIUM | no | none |
| C6 | GT-11 + GT-1 + GT-3 | yes | n/a | yes | HIGH | yes | none |
| C7 | C1 + C3 + C4 + C5 + C6 + GT-1 + GT-2 + GT-3 + GT-13 | yes | n/a | yes | MEDIUM | yes | none |

Form `yes` on chains with three or more hops reflects a hand inspection of every later hop: none begins with a `GT-N` identifier, none closes its sentence, and every head input is an identifier with a parenthesised gloss. C2 and C5 have `Act attempted? = no` because their `?` inputs are internal estimates (payroll, effort, ΔMRR) with no external source to open; their verification paths are named on their confidence lines.

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: adopt managed IdP, own tenancy … spike | bold lead-in | yes | bold lead-in whose colon closes the bold span | C7 |
| Key insight: isolation written either way … | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6, C3, C5 |
| Trade-offs acknowledged: vendor dependency … | bold lead-in | yes | bold lead-in whose colon closes the bold span | C3, C7 |
| Pre-check: head C1 … | bold lead-in | yes | bold lead-in whose colon closes the bold span; cited by its head chains | C1, C3, C4, C5, C6, C7 |
| Confidence: MEDIUM … | bold lead-in | yes | bold lead-in whose colon closes the bold span | C7, C3 |

```text
Scan complete: 7 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```
## Self-Audit Gate (process output)

**Pass 1 (before re-score):** Criterion 1 Rigorous · Criterion 2 Sound · Criterion 3 Hand-wavy · Criterion 4 Rigorous · Criterion 5 Rigorous · Criterion 6 Rigorous · Gate cleared: yes · Hand-wavy cap cleared: yes

Pass 1 found two problems:
- **Criterion 2:** A-1, which is used in C1 as GT-5?, had a Verification cell without "unverified — flagged".
- **Criterion 3:** GT-4 and GT-2, both reachable sources and read at source, fed only MEDIUM chains. The reason was that C4 was rated MEDIUM on a rival that GT-4 itself settles. This was banded under Criterion 3 per the precedence rule. The C4 under-rating overlaps with Criterion 5 and is noted there, not banded twice.

The Fix changed the A-1 Verification cell and re-rated C4 to HIGH, ruling out the rival via GT-4. The C7 and §6 pre-checks and confidence lines, the scan's C4 Band, and the adversarial Rival line were updated to match. Re-scored below.

**Criterion 1: Identify Essence**
Quoted span: "Which way of giving each user of ~120 paying tenants their own authenticated account gets the gated, billed feature to market soonest, at acceptable security, while costing the least 7-person-team engineering capacity…" and "The answer states the year-1 engineering-plus-subscription cost of each surviving option, with lower and upper bounds, and every figure recomputes."
Band: **Rigorous**
Justification: The statement is one sentence naming the allocation decision, not the CTO's urgency trigger. Each success criterion is a verb + subject + outcome test checkable against §6/§4, and none requires picking exactly one named option.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "| C5 | 2 | 13.19% of a team-month | yes — A-14 diverted weeks delay feature one-for-one | yes (A-14) |". From the table: "| unverified — flagged (GT-5?); user-stated product requirement, no source named |".
Band: **Rigorous**
Justification: Every row uses the four-type scheme with an em-dash verdict. Challenges and discards are present (A-3–A-6, A-7, A-8, A-10). Every unverified input used in a chain reads "unverified — flagged". The audit has one row per step for all 31 chain steps.

**Criterion 3: Establish Ground Truths**
Quoted span (comparison): enumerated "GT-5?, GT-7?, GT-8?, GT-9?, GT-10?, GT-12? (6 of 13)". The list carries `?` on exactly those six. The unsuffixed reachable sources feed HIGH chains:
- GT-1, GT-2, GT-3 and GT-4 feed C4 (HIGH).
- GT-1, GT-3 and GT-11 feed C6 (HIGH).
- GT-13 feeds only C7 (MEDIUM).
Band: **Sound**
Justification: The enumeration matches the list, and every unsuffixed GT feeding a HIGH chain names its read location. One reachable, read GT (GT-13) feeds only a MEDIUM chain, which is the single-GT Sound clause. GT-6 and GT-11 are definitions with no source to reach.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan): "| C3 | C2 + GT-1 + GT-2 + GT-3 + GT-7? + GT-9? + GT-10? | yes | n/a | yes | MEDIUM | yes | none |" and "0 chains malformed". From §4 text: "→ build-favourable end: 3 × 150,000/52 + 0.05 × 150,000 + 9,600 = 8,653.85 + 7,500 + 9,600 = $25,753.85, against build $26,538.46, saving $784.62".
Band: **Rigorous**
Justification: All seven chains are in arrow-led form with identifier heads and genuine intermediates. Every arithmetic hop recomputes (Adversarial Recompute). Premises are declared via [Assumes: A-12/A-13/A-14]. §5 holds four dead ends in What-was-tried / Why-abandoned / What-it-ruled-out form, and no analogy is used as evidence.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — Inputs axis short: C1, C3 and C5 are MEDIUM, each explaining its own downgrade" (C7) and "**Sensitivity:** the flip ground truth is **GT-8?** … build upkeep is ≤ … 0.0375 FTE".
Band: **Rigorous**
Justification: Each chain's weakest link is named. Every MEDIUM line names its `?` inputs or sub-HIGH Cn together with a verification path. §6 MEDIUM equals the weakest contributing chain. The adversarial record carries every part, and all five clusters have a disposition. The Pass-1 C4 under-rating was the same defect banded under Criterion 3 and has been fixed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan): "| Key insight: isolation written either way … | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6, C3, C5 |" and "5 claims under R11, 0 excluded … 0 claims untraced". From §6: "The security-critical code in a B2B product, tenant isolation, is written by this team under every option (chain C6)".
Band: **Rigorous**
Justification: All five §6 claims cite §4 chains inline. The Key Insight states a finding the "own your auth" convention misses (isolation is owned anyway), and it is not a restatement of the recommendation.

**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {
      "id": "A-1",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-2",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-3",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-4",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-5",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-6",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-7",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-8",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-9",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-10",
      "type": "untested belief",
      "verdict": "Discard"
    },
    {
      "id": "A-11",
      "type": "physical law",
      "verdict": "Accept"
    },
    {
      "id": "A-12",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-13",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-14",
      "type": "untested belief",
      "verdict": "Accept"
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": true
    },
    {
      "id": "GT-2",
      "read_at_source": true
    },
    {
      "id": "GT-3",
      "read_at_source": true
    },
    {
      "id": "GT-4",
      "read_at_source": true
    },
    {
      "id": "GT-5",
      "read_at_source": false
    },
    {
      "id": "GT-6",
      "read_at_source": true
    },
    {
      "id": "GT-7",
      "read_at_source": false
    },
    {
      "id": "GT-8",
      "read_at_source": false
    },
    {
      "id": "GT-9",
      "read_at_source": false
    },
    {
      "id": "GT-10",
      "read_at_source": false
    },
    {
      "id": "GT-11",
      "read_at_source": true
    },
    {
      "id": "GT-12",
      "read_at_source": false
    },
    {
      "id": "GT-13",
      "read_at_source": true
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-5?",
        "GT-4"
      ]
    },
    {
      "id": "C2",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-6",
        "GT-7?",
        "GT-8?"
      ]
    },
    {
      "id": "C3",
      "confidence": "MEDIUM",
      "rests_on": [
        "C2",
        "GT-1",
        "GT-2",
        "GT-3",
        "GT-7?",
        "GT-9?",
        "GT-10?"
      ]
    },
    {
      "id": "C4",
      "confidence": "HIGH",
      "rests_on": [
        "GT-4",
        "GT-1",
        "GT-2",
        "GT-3"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-6",
        "GT-8?",
        "GT-9?",
        "GT-12?"
      ]
    },
    {
      "id": "C6",
      "confidence": "HIGH",
      "rests_on": [
        "GT-11",
        "GT-1",
        "GT-3"
      ]
    },
    {
      "id": "C7",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C3",
        "C4",
        "C5",
        "C6",
        "GT-1",
        "GT-2",
        "GT-3",
        "GT-13"
      ]
    }
  ],
  "dead_ends": [
    "Per-tenant shared passwords as a cheap middle path",
    "Build, because vendor subscriptions grow with users",
    "Let the vendor own tenancy and isolation (option B as \"enforcement\")",
    "Theoretical-limit floor on build effort"
  ],
  "techniques": {
    "applied": [
      "inversion",
      "estimate",
      "trade-off",
      "second-order",
      "pre-mortem"
    ],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "the core question is an allocation choice, and no figure is a convention mistaken for a hard bound"
      },
      {
        "technique": "theoretical-limit",
        "phase": 4,
        "reason": "no physical law bounds build effort; see §5, \"Theoretical-limit floor on build effort\""
      },
      {
        "technique": "fishbone",
        "phase": 2,
        "reason": "the assumption space was listable through inversion and is not multi-causal"
      },
      {
        "technique": "five-whys",
        "phase": 3,
        "reason": "the ground truths are quoted vendor or NIST text, definitions, or bracketed estimates, with no compound claim left to reduce"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Rigorous",
          "Sound",
          "Hand-wavy",
          "Rigorous",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      },
      {
        "bands": [
          "Rigorous",
          "Rigorous",
          "Sound",
          "Rigorous",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": true,
    "cleared": true
  },
  "re_entry": {
    "fired": true,
    "edges": [
      {
        "edge": "the Self-Audit Gate's Fix/Repeat loop",
        "trigger": "Pass 1 scored Criterion 2 Sound and Criterion 3 Hand-wavy (A-1 lacked the unverified flag; C4 was under-rated so read GTs fed only MEDIUM chains)."
      }
    ]
  },
  "conclusion": {
    "recommendation": "Adopt a managed identity provider for authentication (credentials, sessions, password reset, MFA). Keep tenancy, membership, roles, the per-tenant isolation check and the product's own audit log in your database, keyed by the vendor's user ID — option C (chain C7). Before committing to a vendor, run a one-day spike against your stack's SDK and confirm that hashed passwords can be exported (chain C7).",
    "confidence": "MEDIUM"
  }
}
```
