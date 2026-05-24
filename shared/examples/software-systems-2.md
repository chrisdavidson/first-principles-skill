# Worked Example: Software and Systems (Build vs. Buy)

A complete first-principles analysis of a software-systems decision whose reasoning shape is a
capability-cost-risk trade-off rather than a measurement-first bottleneck diagnosis. The
question — "build our own authentication, or adopt a managed identity provider?" — is the
second SW worked example and is meaningfully distinct from `software-systems.md` (CI/CD
pipeline diagnosis). Authored to the standard 6-section output template.

**Scenario.** A 7-person engineering team at an early-stage B2B SaaS company (≈$40K MRR,
≈120 paying tenants, no enterprise customers yet) is about to ship a feature whose access
requires authenticated, per-tenant accounts. Until now the product has run behind a single
shared password and a Stripe customer link. The team must choose between (a) building auth
in-house on top of an open-source library (sessions, password reset, MFA, audit log) and
(b) adopting a managed identity provider — Auth0, Clerk, WorkOS, or similar — and wiring
it into the existing service. The CTO has framed the choice as urgent because the gated
feature is the next billed release.

---

## 1. Problem Essence

**Core problem:** For this team, at this stage, with this product surface, which of the two
viable paths — build auth in-house or adopt a managed identity provider — minimizes the
combined cost of capability, ongoing operation, and security/lock-in risk over the next
24 months, conditional on a few load-bearing assumptions about the team and the customer
trajectory?

The triggering framing — "we need auth, what should we pick?" — does not specify which
dimension dominates the choice. Both build and buy are technically viable; both have
shipped competitors. The first-principles move is to refuse a universal answer (the
internet has dozens, all of them context-free), classify the assumptions that actually
decide the question, and surface where each path wins. A specific recommendation is
produced only after the assumption table is resolved against the team's measured state.

**Success criteria:**

- The gated feature ships, with working per-tenant authenticated access, within 8 weeks
  of the decision — measurable from the deploy log.
- Ongoing auth-related operating cost stays within budget for the chosen path: under
  ~$400/month for the buy path at the current tenant count, or under ~0.3 FTE of
  ongoing maintenance for the build path (incident response, security patches, library
  upgrades).
- Zero auth-related security incidents in the first 12 months, where "incident" means a
  CVE-class vulnerability exploited in production or a credential-exposure event traced
  to the auth implementation.
- The chosen path does not foreclose the company's known 24-month roadmap: SSO/SAML
  support for the first enterprise customer (already in pipeline conversations), and
  SCIM provisioning if any enterprise customer requests it.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| The team can build, harden, and operate session-based auth + MFA + audit log to a security floor acceptable for B2B SaaS without prior in-production auth experience on this team | untested belief — economic-hinge | If false, the entire build-side economic case collapses regardless of headline implementation cost — the team will either ship an under-secured product or absorb a much larger ongoing cost than estimated. Do not enter the decision with this flagged | Challenge | Unverified — flagged; nobody on the current team has shipped and operated production auth at this team's previous companies; the assumption is the load-bearing hinge for the build-side TCO |
| A managed identity provider's published pricing remains within budget at the team's projected tenant count over a 24-month horizon | untested belief | Verify by walking each candidate provider's published pricing tier against the company's tenant growth projection; flag the specific tier crossings where monthly cost jumps materially | Challenge | Partially verifiable — Auth0 / Clerk / WorkOS pricing pages and the company's 24-month tenant projection are both available; the verification is a tier-crossing calculation, not a vendor claim |
| Migrating off a managed identity provider 18–36 months from now (if pricing trajectory or vendor terms change) is feasible at acceptable cost | untested belief — economic-hinge | If false, the buy path is a one-way door at the moment the first enterprise customer's identity records are stored in the vendor; expiry probability and migration cost must be characterised before signing | Challenge | Unverified — flagged; user-record export formats are typically supported by the major providers, but social-login linkage, MFA enrollment state, and tenant-specific provider configuration are not always round-trippable; the realistic migration cost is the second economic hinge |
| The team's current security posture (no prior CVEs to inherit, no compliance audit yet, no production secrets manager in place) is the floor the auth implementation has to clear | current constraint | Record the floor explicitly; the floor moves up when the first enterprise customer requires SOC2 or signs a DPA with security clauses; the build path then absorbs the cost of meeting the new floor, the buy path inherits the provider's existing posture | Accept | Observed: no current compliance audit, no auth-related CVE inheritance, no secrets manager; the floor is documented and the expiry condition (first enterprise customer's security review) is named |
| "Roll your own auth" is irresponsible in 2026; reputable engineering practice is to adopt a managed provider | convention — analogy-as-evidence | The claim circulates as a community default but is not grounded in a named ground truth about this team's situation; treat as discarded unless re-expressed as a chain anchored in named GTs | Discard | The claim is an analogy-as-evidence move per `assumption-taxonomy.md`; it may not anchor a chain; the actual question is whether THIS team's specific risk profile clears the security floor for THIS product surface, which the build-vs-buy chains evaluate from named GTs rather than from the convention |
| The build-vs-buy decision is binary — adopt one provider fully or build from scratch | untested belief — false-dichotomy | Challenge the binary framing; enumerate intermediate options (e.g., adopt the provider only for login + MFA while owning session, audit log, and tenant model in-house) and check whether any of them dominates either pole on cost, risk, or reversibility | Challenge | The hybrid path — adopt the provider for the high-blast-radius surfaces (password storage, MFA, social login) while owning the lower-risk, vendor-lock-in-prone surfaces (tenant model, audit log, session policy) in-house — is documented in vendor integration guides and is not captured by either of the two original poles |

---

## 3. Ground Truths

- **GT-1** The team comprises 7 engineers; none has shipped and operated production
  authentication (session management + MFA + password reset + audit log) end-to-end in
  a prior role — source: direct team-experience inventory taken at the start of this
  analysis; verified by 1:1 confirmation with each engineer.

- **GT-2** The company currently has ~120 paying tenants at ~$40K MRR; the 24-month
  projection (used for capacity planning) assumes growth to 600–1,200 tenants and
  $200K–$400K MRR, with no enterprise customer requiring SSO/SAML in the next 6 months
  but at least one such customer expected in months 9–18 — source: company finance and
  pipeline records (CRM-tracked enterprise leads; board capacity-planning model).

- **GT-3** As of the analysis date, Auth0 / Okta CIAM, Clerk, and WorkOS publish
  per-monthly-active-user (MAU) pricing tiers that include MFA, password reset, social
  login, and SOC2-certified infrastructure within their managed offering. Concrete tier
  examples on the candidate providers' published pricing pages place the cost for 1,000
  MAUs (a midpoint of the 24-month projection if every tenant has 1–2 active users) in
  the rough range of $200–$800/month depending on provider, feature mix, and tier — source:
  provider pricing pages, retrieved at the analysis date; cited as `GT-3?` because the
  retrieved values represent published list prices and may not reflect negotiated rates,
  feature bundles, or pricing changes within the 24-month horizon.

- **GT-3?** The specific cost trajectory of any chosen managed provider over the next 24
  months is asserted but unverified — list-price snapshots only; the providers reserve
  the right to revise pricing tiers, and the actual MAU count at month 24 is itself a
  projection — unverified: list prices are a snapshot, not a contract; the 24-month
  cost path depends on both the provider's pricing decisions and the actual MAU
  trajectory.

- **GT-4** Building production-grade auth in-house — session-based login, secure password
  storage (bcrypt/argon2), email-based password reset with rate limiting, TOTP MFA, audit
  log of authentication events, account lockout, and basic anomalous-login detection —
  is a 4–8 week initial implementation by an experienced engineer using a maintained
  open-source library (e.g., the auth library shipped with the team's web framework, or
  a dedicated identity library); it is NOT a one-week task and it carries an ongoing
  ~0.1–0.3 FTE maintenance cost (security patches, library upgrades, incident response,
  CVE monitoring) for as long as it is in production — source: published engineering
  retrospectives from similar-stage SaaS companies that have shipped both paths, cross-
  referenced against the team-experience GT-1.

- **GT-5** A managed identity provider stores user records in its own data model; user
  records, password hashes, MFA enrollment state, and tenant-to-user mappings are
  exportable for the major providers, but the formats vary by provider and the
  round-trippability of social-login provider linkages, MFA enrollment seeds, and
  tenant-specific configuration is partial — source: published provider documentation
  (data-export endpoints and formats) cross-referenced with engineering write-ups of
  documented provider migrations.

- **GT-6** The current team has no production secrets manager, no SOC2 audit, and no
  documented incident-response playbook for authentication-related incidents; the first
  enterprise customer's security review (expected in months 9–18 per GT-2) will require
  remediation of these gaps regardless of which auth path is chosen — source: direct
  observation of the team's current infrastructure (secret material is in environment
  variables in the deploy platform; no audit log of access; no documented IR runbook).

---

## 4. Derivation Chains

### Conclusion: The build path's headline cost is lower than the buy path at the current MAU, but only if the build-side economic hinge holds

GT-4 (4–8 weeks initial build + 0.1–0.3 FTE ongoing maintenance) + GT-3 (managed
provider list prices ≈ $200–$800/month at the projected 1,000-MAU midpoint)
→ At the current ~120 tenants and an immediate launch budget, the buy path costs
  approximately $0–$300/month (the lowest tier of most providers covers a small MAU
  count) and the build path costs 4–8 weeks of engineering time once plus ~0.1–0.3 FTE
  ongoing. Converted at typical fully-loaded engineering cost ($15K–$25K/month per
  FTE), the build path's ongoing cost is approximately $1,500–$7,500/month — strictly
  higher than the buy path at every tier through the 24-month horizon's midpoint.
  The build path's apparent advantage exists only at the initial-implementation
  one-time cost line, not in the steady-state operating cost. This inverts the common
  "buy is more expensive" intuition.
→ The build path's economic case rests on GT-4's lower-bound 0.1 FTE estimate holding,
  which is itself conditional on the team being able to build and operate auth to the
  security floor — the load-bearing assumption flagged as `untested belief — economic-hinge`
  in Section 2. If the team requires 0.3 FTE rather than 0.1 FTE because they hit
  unfamiliar territory (MFA flow edge cases, account-takeover protections, audit-log
  correctness for a future compliance audit), the build path's ongoing cost is
  ~$4,500–$7,500/month and the buy path dominates on cost alone at every tier the
  24-month projection crosses.

**Confidence:** MEDIUM — downgraded because the chain consumes GT-4's lower-bound and
  the unverified team-capability hinge. Raising to HIGH requires either (a) a 4-week
  spike on the build path that demonstrates the team is operating at the lower-bound
  FTE estimate, or (b) a measured incident in production that disambiguates which
  estimate the team is actually at.

---

### Conclusion: The buy path is reversible only if the migration-cost hinge holds, and the reversal window narrows as enterprise customers are added

GT-5 (provider data exports are partial — user records yes, MFA enrollment seeds and
social-login linkages partial) + GT-2 (first enterprise customer expected in months
9–18)
→ Migrating off a managed provider before the first enterprise customer lands is
  cheap — the team re-issues credentials to ~120 tenants, walks each through an MFA
  re-enrollment, and accepts the social-login linkage loss as a one-time cost. Migrating
  AFTER the first enterprise customer's identity records (potentially including SAML
  federation configuration, SCIM provisioning state, and audited access logs the customer
  has retention requirements on) are stored in the vendor is materially harder — the
  migration is no longer "re-issue credentials" but "preserve the customer's federation
  configuration and audit-log continuity through the migration."
→ The buy path is reversible at low cost for ≈9 months, becomes a one-way door once the
  first enterprise customer is onboarded onto the vendor's SSO surface, and stays a
  one-way door for the rest of the 24-month horizon. The reversal window is the
  observable, decision-relevant quantity, not the binary "can we migrate?" question.
  Any future re-evaluation of the buy path must happen inside the 9-month window — after
  that, the decision is locked in regardless of how the cost trajectory in GT-3? resolves.

**Confidence:** MEDIUM — downgraded because the chain consumes GT-3? (pricing trajectory)
  and the conditional in GT-2 (first enterprise customer timing is a projection, not a
  signed contract). Raising to HIGH requires a signed enterprise customer with stated
  SSO/SAML requirements, at which point the reversal window has already closed and the
  decision is effectively committed.

---

### Conclusion: The hybrid path dominates the binary framing on the load-bearing security surfaces while preserving optionality on the lock-in surfaces

GT-6 (no secrets manager, no SOC2, no IR runbook — the security floor must be cleared
regardless) + GT-1 (no engineer on the team has shipped production auth before) +
GT-5 (vendor exports are partial; lock-in concentrates where the vendor owns the most
state)
→ The highest-blast-radius surfaces in any auth implementation are password storage,
  MFA enrollment, and account-recovery flow — the surfaces where a defect leaks
  credentials or enables account takeover. These are also the surfaces where the team's
  inexperience (GT-1) is most expensive: a CVE-class defect here is a company-existential
  event, not a fixable bug. The lowest-blast-radius surfaces are the tenant model, the
  audit log, the session policy, and the in-app authorization layer — defects here are
  recoverable, and these surfaces are also where vendor lock-in concentrates (the tenant
  model and audit log are exactly the data the vendor "owns" once committed).
→ A hybrid path — adopt the managed provider for the credential, MFA, and account-recovery
  surfaces (where the buy-side capability gap is largest and the lock-in concentration is
  lowest) while owning the tenant model, audit log, session policy, and in-app
  authorization in-house (where the build-side risk is lowest and the lock-in cost of
  buying is highest) — dominates both poles on the joint capability-cost-risk metric.
  It clears the security floor by delegating the surfaces the team cannot safely build,
  retains the surfaces the team can safely build and where lock-in would be most
  expensive, and preserves the migration option at lower cost than the full-buy path
  because the lock-in-prone surfaces are not stored in the vendor.

**Confidence:** HIGH — the chain rests on GT-1, GT-5, and GT-6, all directly observed
  rather than projected. The hybrid path's existence collapses the `false-dichotomy`
  assumption in Section 2 and reduces the dependence on the two economic-hinge
  assumptions.

---

## 5. Abandoned Reasoning

### Dead End: Pure cost comparison over a 3-year TCO model

**What was tried:** Compare the two paths purely on total cost of ownership over a
36-month horizon. Build a spreadsheet of the build-path costs (initial 4–8 weeks of
engineering effort + 0.1–0.3 FTE ongoing maintenance over 36 months at fully-loaded
engineering rates) against the buy-path costs (monthly subscription at each tier
crossing as MAU grows from ~120 to ~1,000–2,000 over 36 months). Pick the path whose
3-year TCO is lower. The motivation was that engineering teams routinely make this kind
of build-vs-buy decision via TCO comparison, and the input data (GT-3 on provider
pricing tiers, GT-4 on build effort and maintenance burden) is partially available.

The TCO model was constructed: at the lower-bound build estimate (0.1 FTE) the build
path's 3-year cost is ≈$54K–$90K; at the upper-bound (0.3 FTE) it is ≈$162K–$270K. The
buy path's 3-year cost at projected MAU growth is ≈$15K–$40K cumulative at the lower
tier crossings and $40K–$100K if the team crosses into the next tier (typically at
1,000+ MAUs or when enterprise SSO is enabled).

**Why abandoned:** The TCO model produces a defensible-looking comparison whose answer
is sensitive to the FTE-loading assumption (the build-side hinge) and the MAU-trajectory
assumption (the buy-side cost driver), but it OMITS two costs that the assumption table
surfaces as decision-relevant:

1. The migration-out cost from the buy path once the first enterprise customer lands
   (months 9–18 per GT-2) is not a 3-year-TCO line item — it is a one-time cost incurred
   at a future date conditional on a future decision. A TCO model that puts $0 in that
   line because no migration is currently planned is implicitly assuming the buy path
   will be retained for the full horizon, which is exactly the assumption the chain on
   reversibility shows is the load-bearing one. The TCO answer for "buy is cheaper" is
   conditional on never wanting to migrate, but the analysis has not established that
   the team would never want to.

2. The security-incident tail risk on the build path (a CVE-class auth defect from an
   inexperienced team, GT-1 + GT-4) is not a 3-year-TCO line item either — it is a
   low-probability, high-magnitude event whose expected cost is hard to estimate but
   whose realized cost can be a company-existential event for an early-stage SaaS. A
   TCO model that puts $0 in that line is implicitly assuming the build-side capability
   hinge holds, which is exactly the assumption flagged as `untested belief —
   economic-hinge` in Section 2.

The TCO answer is therefore a function of two assumptions the TCO model itself does not
expose. Abandoned because answering build-vs-buy via TCO alone collapses the analysis
back into the assumptions the first-principles framing was supposed to surface. The
contingent recommendation from Section 6 is strictly more useful than the TCO point
estimate because it names the conditions under which each path is preferred.

**What it ruled out:** This dead end establishes that a pure-TCO comparison may not
anchor the recommendation for this decision class. TCO is a useful input — it bounds
the cost magnitudes — but the answer is over-determined by two unverified assumptions
whose treatment belongs in the assumption table, not in a spreadsheet cell. Future
build-vs-buy analyses on this team should produce a contingent recommendation first
and use TCO to size the cost band of each branch, not to pick the branch.

---

### Dead End: "We have a senior engineer who built auth before — therefore build"

**What was tried:** Reason from an individual engineer's prior auth-building experience
(at a previous company, on a different team, at a different stage) directly to a build
recommendation. The chain attempted was: a senior engineer on the team has shipped auth
once before → that engineer can architect and lead the build here → the team's
collective auth capability is sufficient → the build path is safe → choose build.

**Why abandoned:** Two reasons surfaced on probing:

1. GT-1 documents that NO engineer currently on the team has shipped and operated
   production auth end-to-end — re-checking the team-experience inventory specifically
   for this dead end confirmed the inventory result. The "senior engineer with auth
   experience" turned out, on closer inspection, to have integrated a managed provider
   at a prior role (NOT built auth from scratch), and to have authored a session-handling
   helper at an even earlier role on a product surface that never required MFA or a
   compliance audit. Neither prior experience is the same load-bearing capability the
   build path actually requires.

2. Even if the prior experience had been a clean match, "this person built it once before,
   so we should build" is a `convention — analogy-as-evidence` move per the assumption
   taxonomy — reasoning of the form "someone solved a similar problem this way, so we
   should too," without the analogue's situation being characterised in terms of a named
   GT that links their situation to ours. The taxonomy prescribes Discarding this
   pattern as a standalone justification. The prior context had a different team size, a
   different threat model, and different compliance obligations. The maintenance burden in GT-4 — security patches, CVE
   monitoring, incident response — falls on the CURRENT team, not on the engineer who
   shipped auth at a prior company. The single-engineer experience is not transitive to
   the team's collective ongoing capability.

Abandoned because the chain anchors on an individual-experience claim that does not
clear the GT bar (the experience does not match the load-bearing capability) and the
assumption-classification step shows the chain shape itself is a convention-as-evidence
move that the taxonomy prescribes Discarding.

**What it ruled out:** This dead end establishes that "we have someone who has done it
before" is not a sufficient anchor for the build path on this decision. Individual
prior experience can be a useful input — it lowers the cost of the build-side spike
that would verify the economic hinge — but it cannot SUBSTITUTE for the team-capability
GT. Any future analysis that attempts to anchor a build-vs-buy decision on an individual
engineer's prior work must first re-verify the experience against the actual capability
the new context requires, AND must check whether the maintenance burden remains on the
same engineer or transfers to a team for whom the experience is not transitive.

---

## 6. Conclusion

**Recommended approach:** Adopt the **hybrid path** — use a managed identity provider for
password storage, MFA enrollment, and account-recovery flows; own the tenant model, audit
log, session policy, and in-app authorization in-house. Specifically:

1. Within 2 weeks, select a managed provider whose published pricing tier covers the
   projected 24-month MAU range without crossing a tier that materially exceeds the
   $400/month budget criterion, and whose data-export surface covers user records
   AND audit-log export (the two surfaces the team must be able to round-trip if the
   migration-cost hinge later resolves against the buy decision).

2. Within 6 weeks, ship the gated feature with provider-backed login + MFA + account
   recovery, and in-house tenant model + audit log + session policy + authorization
   layer. The gated-feature ship deadline (8 weeks) is achievable on the hybrid path
   because the high-risk surfaces (credential storage, MFA) are delegated and the
   in-house surfaces are the ones the team can build safely.

3. Within 9 months, BEFORE the first enterprise customer's onboarding closes the
   reversal window from the Section 4 chain on reversibility, re-evaluate the
   migration-cost hinge: rehearse a buy→build migration of the credential surfaces (in a
   staging environment, not production) against the chosen provider's data-export
   surface, and decide whether the build path is now feasible enough that the team
   wants to migrate before the enterprise customer locks in the buy decision.

4. Concurrent with steps 1–3 and independent of the build-vs-buy choice: address the
   GT-6 gaps (secrets manager, IR runbook, eventual SOC2 path). These are required
   regardless of the auth path and represent shared cost the build-vs-buy decision
   does not change.

**Key insight:** The "build vs buy" framing is a `false-dichotomy` assumption masquerading
as the actual decision. The real decision is a per-surface choice: for each auth surface
(password storage, MFA, account recovery, tenant model, audit log, session policy,
authorization), which path minimizes the joint capability-cost-risk cost on THAT
surface for THIS team. The per-surface answer differs across surfaces — the high-risk
surfaces favor buy, the high-lock-in surfaces favor build — and the hybrid path is the
only path that does not pay the wrong cost on at least some surfaces. The community
convention "roll your own auth is irresponsible" is correct about the credential
surfaces (where the team's capability gap is largest) and incorrect about the tenant and
session surfaces (where the team can safely build and where lock-in would be most
expensive). Conflating the two leads to either over-building (incurring the
inexperienced-team security risk on the credential surfaces) or over-buying (incurring
the lock-in cost on the tenant and session surfaces that the team would have paid less
to own).

**Trade-offs acknowledged:**

- The hybrid path is more architectural work than either pole. The team must define and
  maintain the integration seam between the managed provider and the in-house
  components (e.g., the provider-issued user identifier becomes a foreign key in the
  in-house tenant model; the provider's MFA enrollment state must be synchronized with
  the in-house audit log; session expiry policy must be coordinated between the
  provider's session and the in-house session). This is genuine ongoing complexity that
  the pure-build and pure-buy paths do not carry.

- The recommendation defers a hard re-evaluation step to month 9 (before the first
  enterprise customer onboards). This defers the binding decision but does not
  eliminate it — the team must actually do the re-evaluation, and if the re-evaluation
  is skipped, the buy path becomes a one-way door without the team having decided to
  walk through it. The Section 4 reversibility chain depends on this re-evaluation
  actually happening.

- The recommendation does not produce a universal "build vs buy" verdict — it produces
  a verdict contingent on the assumption-table verdicts that hold for THIS team. If
  another team applied the same first-principles analysis to the same scenario with
  different GT-1 (a team with deep auth experience), GT-2 (no enterprise customers in
  the foreseeable horizon), or GT-4 (a smaller security floor because the product
  surface does not store regulated data), the contingent recommendation could land on
  a different path. The methodology, not the specific verdict, is the transferable
  output.

**Confidence:** MEDIUM — the hybrid-path chain itself is HIGH confidence, but the
overall recommendation inherits the MEDIUM rating from the chain on reversibility
(which depends on GT-3? — the pricing trajectory — and the projection in GT-2 of the
first enterprise customer's timing). Raising to HIGH requires either (a) a signed
enterprise customer with stated SSO/SAML requirements, which would resolve GT-2's
projection into a fact and either confirm or close the 9-month reversal window, or
(b) a signed contract with the chosen managed provider that pins the pricing
trajectory through the 24-month horizon, which would resolve GT-3?.
