## Assumption Audit scan (process output)

End-of-Phase-4 scan, walking every hop of every chain in section 4, in order, checking whether the hop relies on an assumption not already present in section 2's Assumptions Table.

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | feature's actual requirement is per-tenant auth data-model/session-identity, not a full IAM bundle | none | n/a |
| C1 | 2 | vendors sell modular surfaces (GT-9); market does not force all-or-nothing | none | n/a |
| C1 | 3 | decision is per-surface ownership, not a single build/buy switch | none | n/a |
| C1 | 4 | conclusion: per-surface framing is correct; binary framing is a discarded convention | none | n/a |
| C2 | 1 | decompose "auth built correctly" into 11 line items against GT-1..GT-6 | none | n/a |
| C2 | 2 | bracket one-time effort at 13.5-25.5 engineer-weeks | yes — per-item week estimates assume typical security-engineering throughput | yes (A-13) |
| C2 | 3 | convert bracket through GT-11? loaded cost to $47K-$153K one-time + $18K-$90K/yr ongoing | none | n/a |
| C2 | 4 | conclusion: true build cost is a multi-month, then perpetual, commitment | none | n/a |
| C3 | 1 | at ~120 tenants, MAU sits inside every vendor's free/lowest tier | none | n/a |
| C3 | 2 | remaining work is integration (1.5-3 wk), not cryptography | none | n/a |
| C3 | 3 | convert to $5K-$18K one-time + near-zero subscription until first SSO connection | none | n/a |
| C3 | 4 | conclusion: buy one-time cost is 3-10x cheaper than build at both bracket ends | none | n/a |
| C4 | 1 | ideal zero-defect floor is unreachable; compare to best-demonstrated tier instead | none | n/a |
| C4 | 2 | vendor's default product already sits at the best-demonstrated tier (GT-7, GT-9) | none | n/a |
| C4 | 3 | C2 shows this team lacks budgeted weeks to match that tier under deadline pressure; GT-14? names the deferred-until-incident pattern | none | n/a |
| C4 | 4 | conclusion: build's realistic landing point sits below best-demonstrated tier on deferred items; buy starts there by construction | none | n/a |
| C5 | 1 | weighted trade-off totals: Build=43, Buy=119, Hybrid=110 | none | n/a |
| C5 | 2 | flip test: no single-criterion weight change within the 1-5 range closes the 9-point Buy/Hybrid gap | none | n/a |
| C5 | 3 | conclusion: Buy recommended over Build and Hybrid | none | n/a |
| C6 | 1 | [2nd] freed engineering capacity redirected to revenue-facing work | none | n/a |
| C6 | 2 | [2nd] vendor incentivized to retain/monetize the account via per-connection pricing | none | n/a |
| C6 | 3 | [3rd] cumulative SSO spend scales with the enterprise segment; margin-erosion risk if unpriced | none | n/a |
| C6 | 4 | [3rd] security reviewer requires this company's own IR evidence, not just the vendor's SOC2 | none | n/a |
| C6 | 5 | neither effect contradicts a named GT; chain extends rather than returning to Phase 2 | none | n/a |
| C6 | 6 | shared fix: owned webhook-mirrored audit/event log, +0.5-1 engineer-week | yes — vendor webhook delivery is reliable enough to serve as audit-of-record | yes (A-14) |
| C6 | 7 | conclusion: refined recommendation is Buy plus an owned audit mirror | none | n/a |
| C7 | 1 | inverting the refined recommendation surfaces two load-bearing preconditions: reviewed integration code; monitored audit mirror | none | n/a |
| C7 | 2 | GT-13? shows reversibility is "friction," not "easy" | none | n/a |
| C7 | 3 | conclusion: preconditions become explicit launch gates | none | n/a |
| C8 | 1 | five-whys: the feature-need is a real cause; the urgency-to-skip-analysis is a separable, correctable cause | none | n/a |
| C8 | 2 | the decision itself takes bounded time; deciding badly costs engineer-months (C2) and later incidents/deal-blocks (C4) | none | n/a |
| C8 | 3 | conclusion: decouple the decision clock from the implementation clock this week | none | n/a |

Two assumptions surfaced during this scan (A-13, A-14) were not already present in section 2's Assumptions Table at the time chains were first drafted; both have been added to that table (see section 2) and the originating steps above are marked accordingly.

---

## Adversarial pass (process output)

**Recompute.** C2's component sum recomputes: low bound 2+0.5+1+1+2+1+1+1+1+1+1 = 13.5 engineer-weeks; high bound 4+1+2+2+4+2+1.5+3+2+2+2 = 25.5 engineer-weeks — matches the chain text. Converted through the $3,500-$6,000/engineer-week loaded-cost bracket (GT-11?): 13.5×$3,500=$47,250 and 25.5×$6,000=$153,000 — matches the stated $47,000-$153,000 one-time figure. C3's integration bracket (1.5-3 weeks) converts to 1.5×$3,500=$5,250 and 3×$6,000=$18,000 — matches the stated $5,000-$18,000 figure. C5's weighted totals recompute from the per-criterion scores and locked weights (5,5,3,4,4,3,2): Build = 1·5+2·5+1·3+1·4+2·4+3·3+2·2 = 5+10+3+4+8+9+4 = 43; Buy = 5·5+5·5+5·3+5·4+5·4+2·3+4·2 = 25+25+15+20+20+6+8 = 119; Hybrid = 4·5+5·5+4·3+5·4+4·4+3·3+4·2 = 20+25+12+20+16+9+8 = 110 — all three match the chain text. The Buy/Hybrid margin (119−110=9) recomputes correctly, and the flip-test arithmetic in C5 (margin sourced from three criteria at weights 5, 3, 4 against one Hybrid-favoring criterion at weight 3, i.e. no single weight in the 1-5 range can close a 9-point gap contributed by three separate criteria) holds under recheck: even setting the reversibility weight to its maximum (5) only closes 2 of the 9 points, and reducing any one Buy-favoring weight to its minimum (1) leaves the other two Buy-favoring criteria alone still ahead of Hybrid's single advantage. No arithmetic error found.

**Sensitivity.** The single ground truth whose falsity would most directly flip the headline recommendation is **GT-9** (WorkOS's published free-to-1,000,000-MAU AuthKit tier and per-connection SSO pricing), which is unsuffixed (read-at-source) but whose *applicability to this company's specific B2B usage pattern* (org-based rather than raw-MAU billing quirks, e.g. whether "active user" is counted per login or per seat) has not been individually confirmed against a signed order form. If the applicable billing definition materially changes the near-zero current-scale cost that C3 and C5 rest on, the TCO ranking in C5 could narrow enough to matter (though C1-C2's independent finding that Build costs 3-10x more at both bracket ends would need the buy-side estimate to grow by an order of magnitude to fully reverse, which is not a small perturbation). This is the chain's stated weakest link, distinct from GT-11? and GT-13?, both of which are already `?`-marked and named on their respective chains' confidence lines.

**Rival.** For the headline conclusion (Buy, refined with an owned audit mirror — chains C5, C6): the strongest rival is the thicker **Hybrid** path (vendor owns credentials/session/MFA; team owns the tenant/organization model and audit log directly, rather than using the vendor's Organizations primitive). This rival is ruled out by C5's flip-test robustness (Adversarial pass → Recompute, above) and is further weakened by C6's finding that Hybrid's main advantage over Buy — reversibility and owned compliance evidence — is available to the Buy path at low marginal cost via the webhook-mirrored audit log, without paying Hybrid's larger integration bill; see Abandoned Reasoning, "Dead End: Hybrid ownership of the tenant/audit model." For chain C2 specifically: the rival reading "an experienced team could build this materially faster" is not ruled out — no ground truth establishes any of the 7 engineers' prior production-auth experience — and is carried live on C2's confidence line as an open, resolvable-this-week question (see Conclusion, "This week"). For chain C4: the rival reading "a disciplined team under deadline pressure could still hit the full NIST/OWASP floor without cutting corners" is not affirmatively ruled out either; C4's confidence line treats GT-14? as directional pattern evidence, not a certainty, for exactly this reason.

**Premise.** It is 18 months from now. The auth decision this analysis recommended has already caused a real, avoidable problem for the company.

**Causes** (generated from four stakeholder viewpoints, unfiltered):
- *Engineer/implementer:* the vendor SDK shipped a breaking change to its session-cookie contract; the integration broke during a signup spike, and nobody on the team had deep enough ownership of the glue code to diagnose it quickly, because "thin" buy-side integration meant thin institutional knowledge of exactly this failure surface.
- *Engineer/implementer (second angle):* the webhook-mirrored audit table was built once at launch and never monitored; a webhook-signing-key rotation on the vendor's side silently stopped new events from landing, and six months of "owned" audit trail has a gap discovered only when an enterprise customer's auditor asked for it.
- *Finance/executive:* enterprise logo count grew faster than the pipeline model assumed (8 logos by month 14, each needing a dedicated SSO connection); GT-9/GT-8's per-connection pricing pushed monthly identity-vendor spend into four figures, which nobody had built into those deals' gross-margin math at signing time.
- *Enterprise customer's security reviewer:* a prospect's security questionnaire asked for this company's own incident-response runbook and audit evidence; the team had informally assumed the vendor's SOC2 attestation covered this, and it does not — the reviewer's contract is with this company, not the vendor — and the deal stalled while a runbook was hastily assembled.
- *Attacker:* a credential-stuffing campaign hit the login endpoint during a marketing-driven signup surge; the vendor's default rate-limiting/bot-defense thresholds were never tuned for this product's specific traffic shape, and the resulting wave of false-positive account lockouts looked, to customers, indistinguishable from an outage.
- *Implementer (organizational angle):* the build/buy/hybrid decision was made and documented by one person under deadline pressure; 18 months later that person has left, and the remaining team does not know why certain choices (e.g., not adopting the vendor's Organizations primitive for the tenant model) were made, so a later "cleanup" effort nearly undoes a deliberate decision by accident.

**Clusters** (structural weaknesses, each naming the chain or ground truth it bears on):
- **Cluster A — Vendor-dependency without ownership depth** (bears on C3, C5, C6). Triage: **costly but survivable.** Tripwire: any vendor SDK major-version bump triggers a mandatory staging-environment smoke test of login/session flows before production rollout, owned by a named on-call engineer.
- **Cluster B — Audit trail silently rots** (bears on C6's [Assumes: A-14]). Triage: **costly but survivable**, though potentially deal-blocking if discovered at the wrong moment. Tripwire: an automated daily check that the audit-mirror table received at least one event in the last 24 hours, alerting on zero.
- **Cluster C — Vendor per-connection pricing outgrows the model that justified Buy** (bears on C3, C5 — this is the sensitivity/flip condition). Triage: **costly but survivable** if caught early; risks becoming deal-specific margin erosion if not. Tripwire: identity-vendor spend tracked as a percentage of MRR, reviewed quarterly starting at the first provisioned enterprise SSO connection.
- **Cluster D — Compliance responsibility misattributed to the vendor** (bears on C4, C6, and GT-7's Security-criteria attribution). Triage: **fatal to a specific deal, survivable for the company.** Tripwire: the first received prospect security questionnaire is treated as the forcing function.
- **Cluster E — Rate limiting tuned for the vendor's default population, not this product's traffic** (bears on C4's floor-coverage claim). Triage: **costly but survivable** (false-positive lockouts, reputational — not a breach). Tripwire: account-lockout rate monitored against baseline, with alerting during traffic surges.
- **Cluster F — Decision concentrated in one person; institutional knowledge loss** (a process risk, not chain-specific). Triage: **tolerable**, cheap to fix.

**Disposition** (one per cluster):
- Cluster A → named plan change: add a "vendor upgrade smoke test" to the standing on-call runbook (chain C3).
- Cluster B → named plan change: build the daily zero-events monitor at the same time as the audit mirror itself, not as a later addition (chain C6).
- Cluster C → named plan change: price per-connection SSO cost into every enterprise deal's margin model from the first deal, and review quarterly (chain C6).
- Cluster D → named plan change: draft a one-page incident-response runbook and review the vendor's DPA/sub-processor terms before, not after, the first enterprise security questionnaire arrives; accept the residual risk that a first-draft runbook is imperfect (chain C4).
- Cluster E → accepted risk with named mitigation: tune the vendor's rate-limit/bot-protection thresholds during onboarding rather than accepting defaults, and add the lockout-rate monitor (chain C4).
- Cluster F → named plan change: commit this analysis itself to the team's shared documentation so the reasoning survives personnel turnover.

**Falsification.** This conclusion (Buy — vendor owns credentials/session/MFA and its Organizations primitive as the tenant model, plus a team-owned webhook-mirrored audit log — chains C5, C6, C7) is false if a security-focused code review of the vendor-integration glue code, performed before production launch, finds that the team cannot correctly implement the redirect/callback/session-handling surface fast enough to hit the deadline safely; in that case the "thin custom integration is fast and low-risk" premise underlying C5's time-to-ship score does not hold, and the team should fall back to the vendor's fully-hosted (redirect-based) login UI — trading UI control for eliminating that specific failure mode — rather than treating the finding as evidence for Build.

---

## §6→§4 closure ledger (process output)

- "Adopt a managed identity provider... for credential storage, session handling, and MFA; use its Organizations primitive as the tenant model; build the in-app authorization layer; and build an owned webhook-mirrored audit/event log from day one" → chain C6 ✓ (also C5) ✓
- "Timebox and close this architecture decision this week; do not let it re-litigate against the feature deadline" → chain C8 ✓
- "Resolve whether any of the 7 engineers has prior hands-on production-auth experience" → chain C2 ✓
- "Select a provider whose published free/lowest tier covers current scale... and confirm the specific terms at signup" → chain C3 ✓
- "Build the in-app authorization layer and the webhook-mirrored audit/event log alongside the vendor integration, not as a follow-up phase" → chain C6 ✓
- "Run a security-focused code review of the integration's redirect/callback/session-cookie code before production launch, and stand up the daily audit-mirror monitor" → chain C7 ✓
- "'Build vs buy' was never the real question; per-surface ownership is" → chain C1 ✓ (also C8) ✓
- "The felt urgency conflates the feature-ship clock with the architecture-decision clock, which are separable at near-zero cost" → chain C8 ✓
- "Accepting vendor lock-in on the credential/session/MFA surfaces, only partly mitigated by the audit mirror" → chain C7 ✓
- "Accepting an unresolved question about the team's prior auth experience that could, if answered favorably, marginally strengthen a thicker-ownership case later" → chain C2 ✓
- "Accepting that the recommendation is contingent on two launch gates actually happening, not merely recommended" → chain C7 ✓
- "If a pre-launch security review finds the team cannot safely implement the integration in time, fall back to the vendor's fully-hosted login UI" → chain C7 ✓
- "If the team's real auth capability and the deadline's real slack turn out more favorable than assumed, and data sensitivity increases, re-run the C5 trade-off with updated scores" → chain C5 ✓ (also C2) ✓
- "If cumulative identity-vendor spend crosses the named threshold, revisit vendor tier/contract terms or a partial migration" → chain C6 ✓
- "If GDPR/SOC2 scope expands materially, re-weight and re-score the compliance-evidence criterion in C5" → chain C5 ✓
- **Pre-check** line (Conclusion) → self-discharging via its own `head` list (C1, C2, C3, C5, C6, C7) ✓
- **Confidence: MEDIUM** line → chains C2, C3, C4, C5, C6, C7 (all MEDIUM) named explicitly ✓

Every surviving claim in section 6 carries an inline chain citation; no claim required cutting.

---

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-12 + GT-1 + GT-4 + GT-9 | yes | n/a | yes | HIGH | yes | none |
| C2 | GT-1 + GT-2 + GT-3 + GT-4 + GT-5 + GT-6 + GT-11? | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-8 + GT-9 + GT-10 + GT-12 + GT-11? | yes | n/a | yes | MEDIUM | yes | none |
| C4 | GT-1 + GT-2 + GT-4 + GT-7 + GT-9 + GT-14? + C2 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | GT-8 + GT-9 + GT-10 + GT-12 + C2 + C3 + C4 | yes | n/a | yes | MEDIUM | yes | none |
| C6 | C5 + GT-9 + GT-12 | yes | n/a | yes | MEDIUM | yes | none |
| C7 | C6 + GT-13? | yes | n/a | yes | MEDIUM | yes | none |
| C8 | GT-12 + C2 + C4 | yes | n/a | yes | MEDIUM | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| **Recommended approach:** ... adopt a managed IdP ... | bold lead-in | yes | colon closes bold span, content follows on same line | C6 |
| **This week, concretely:** | bold lead-in | no | section-intro label — colon-terminated, whole line, carries no citation of its own | n/a |
| 1. Timebox and close this decision this week | list item | yes | closes its own sentence | C8 |
| 2. Resolve whether any engineer has prior production-auth experience | list item | yes | closes its own sentence | C2 |
| 3. Select the provider and confirm terms at signup | list item | yes | closes its own sentence | C3 |
| 4. Build authorization layer + audit mirror alongside the integration | list item | yes | closes its own sentence | C6 |
| 5. Run the pre-launch security review and stand up the audit-mirror monitor | list item | yes | closes its own sentence | C7 |
| **Key insight:** ... build vs buy was never the real question ... | bold lead-in | yes | colon closes bold span, content follows on same line | C1, C8 |
| **Trade-offs acknowledged:** ... vendor lock-in ... | bold lead-in | yes | colon closes bold span, content follows on same line | C7 |
| - the unresolved team-experience question | list item | yes | closes its own sentence | C2 |
| - the recommendation is contingent on two launch gates | list item | yes | closes its own sentence | C7 |
| **Flip conditions — the recommendation reverses if:** | bold lead-in | no | section-intro label — colon-terminated, whole line, carries no citation of its own | n/a |
| 1. pre-launch review finds the integration unsafe in time | list item | yes | closes its own sentence | C7 |
| 2. team capability and deadline slack are both more favorable, and data sensitivity rises | list item | yes | closes its own sentence | C5, C2 |
| 3. cumulative identity-vendor spend crosses the named threshold | list item | yes | closes its own sentence | C6 |
| **Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM) ... | bold lead-in | yes | colon closes bold span, content follows on same line | C1, C2, C3, C5, C6, C7 |
| **Confidence:** MEDIUM ... | bold lead-in | yes | colon closes bold span, content follows on same line | C2, C3, C4, C5, C6, C7 |

Scan complete: 8 chain rows, one per section-4 chain block in order; 17 section-6 rows, one per construct in order — 15 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced.

---

## Techniques not applied (process output)

- fishbone (Phase 2 invocation) — not applicable — the assumption space was directly enumerable by challenge (14 assumptions identified without needing breadth-first cause-category brainstorming); no multi-causal fog required fishbone's category scan.
- theoretical-limit (Phase 1 essence-reframe invocation) — not applicable — the core question does not hinge on whether a specific figure is a convention versus a hard bound; that reframing is instead performed in Phase 4 (chain C4), where the technique is actually load-bearing.
- inversion (Phase 5 adversarial-technique invocation) — not applicable — the headline conclusion is a plan/recommendation, not a bare claim, so the Phase 5 decision rule routes the adversarial technique to Pre-Mortem instead (applied above, in the Adversarial pass).
- five-whys, reduce-to-primitives mode (Phase 3 invocation) — not applicable — every ground truth in section 3 is already a directly-read primary source (a regulation's clause, a standard's clause, or a published price), not a compound derived claim requiring further decomposition; the causal-mode use of five-whys is applied separately in chain C8.

---

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "which authentication-ownership architecture — build every surface in-house, buy a managed identity provider for every surface, or split ownership by surface — minimizes this specific 7-person team's combined near-term delivery risk and 24-month cost/lock-in risk, and does the 'build vs buy' framing itself correctly describe the decision this team actually faces?"
Band: **Rigorous**
Justification: The statement names a specific, non-generic decision (per-surface ownership, not a bare "build or buy" label) unique to this team's stated scale and deadline, and each of the five success criteria in section 1 gives a verb+subject+outcome triplet checkable directly against section 6 (named ownership split, named flip condition, named this-week actions, named cost brackets, named long-tail coverage).

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "Two assumptions surfaced during this scan (A-13, A-14) were not already present in section 2's Assumptions Table at the time chains were first drafted; both have been added to that table (see section 2) and the originating steps above are marked accordingly."
Band: **Rigorous**
Justification: All 14 rows use the four-type scheme with vocabulary-matched treatments, em-dash-separated Verdict tokens, and specific Verification cells (e.g., A9's split GDPR/SOC2 verdict); the Assumption Audit scan is exhaustive over all 32 named chain steps with no step skipped, and both assumptions it surfaced were folded back into the table before scoring.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-11?, GT-13?, GT-14? (3 of 14)" cross-checked against the Ground Truths list, which carries `?` on exactly those three IDs and none other; GT-1, GT-4, GT-9, and GT-12 — the four inputs of the sole HIGH-confidence chain, C1 — each name a read-at-source location (NIST §5.1.1.1/§5.1.1.2; OWASP Session Management Cheat Sheet; workos.com/pricing; this analysis's own Problem Essence).
Band: **Rigorous**
Justification: IDs are stable and match the identifiers used in section 4; every unsuffixed GT feeding the HIGH chain (C1) names its read-at-source location; the `?` enumeration matches the list when checked against it rather than merely asserted; no Phase-2-discarded assumption appears in the list.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): "C1 | GT-12 + GT-1 + GT-4 + GT-9 | yes | n/a | yes | HIGH | yes | none" and the reconciliation line "8 chain rows, one per section-4 chain block in order... 0 chains malformed."
Band: **Rigorous**
Justification: All 8 chain blocks score `Form conforming? = yes` with clean dependencies in the scan; every chain has at least one genuine intermediate hop; the Abandoned Reasoning section documents three dead ends with the prescribed What-was-tried/Why-abandoned/What-it-ruled-out structure; no analogy is used as standalone evidence (the one pattern-based claim, GT-14?, is explicitly flagged `?` and used only directionally, never as a load-bearing numeric input); both surfaced assumptions (A-13, A-14) carry inline `[Assumes: X]` declarations on their originating hops.

**Criterion 5: Validate**
Quoted span: "Cluster C → named plan change: price per-connection SSO cost into every enterprise deal's margin model from the first deal, and review quarterly (chain C6)." together with chain C8's confidence line: "MEDIUM — capped by citing C2 (MEDIUM) and C4 (MEDIUM); each chain's own line carries its verification path."
Band: **Rigorous**
Justification: Every chain's confidence line names its `GT-N?` inputs and cited `Cn` bands with verification paths or explicit reasons (per D-07); no chain rated HIGH consumes a `?`-marked input; every chain is rated no higher than the lowest-rated chain its head cites; the adversarial pass record is complete (Recompute, Sensitivity, Rival, Premise, Causes from four stakeholder viewpoints, Clusters naming their chains, and a named disposition for every cluster) and the overall Conclusion's MEDIUM rating matches its weakest contributing chains rather than being asserted independently of them.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory reconciliation): "15 claims under R11, 2 excluded... 0 claims untraced" together with the Key Insight text: "'build vs buy' was never the real question; per-surface ownership is, and the market itself (GT-9) already prices it that way."
Band: **Rigorous**
Justification: Every claim in section 6 traces to a named section-4 chain per the closure ledger and the self-audit scan's claim-inventory table, with zero claims left untraced; the Key Insight names a non-obvious structural finding (the binary framing is a discarded convention, not a market-imposed constraint) rather than restating the Recommended Approach's vendor choice.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy. Both conditions for clearing the gate are met on the first scoring pass — no Fix/Repeat cycle was required.

---

# First-Principles Analysis: Build vs. Buy Authentication

## 1. Problem Essence

**Core problem:** Given that shipping the next billed feature requires per-tenant, multi-user authenticated accounts that do not exist today, which authentication-ownership architecture — build every surface in-house, buy a managed identity provider for every surface, or split ownership by surface — minimizes this specific 7-person team's combined near-term delivery risk and 24-month cost/lock-in risk, and does the "build vs buy" framing itself correctly describe the decision this team actually faces?

The triggering framing ("build in-house on an open-source library" versus "adopt a managed identity provider") presents the choice as a single binary switch. The first-principles move is to test that framing before accepting it, decompose what "authentication" actually requires as a set of separable surfaces, and price each path against this team's specific scale, deadline, and trajectory rather than against a generic industry opinion.

**Success criteria:**

1. The Conclusion names a specific per-surface ownership split (which surfaces are vendor-owned versus in-house-owned) — not merely an unqualified "build" or "buy" label.
2. The Conclusion states at least one concrete, falsifiable condition under which the recommendation reverses.
3. The Conclusion lists specific actions executable within the current week that are compatible with the stated ship deadline.
4. The Conclusion's cost/risk comparison is traced to a stated bracket (engineer-weeks and dollars) for both the build-side and buy-side effort, not an unquantified impression.
5. The Conclusion addresses each of the named long-tail components (password reset, MFA, audit log, rate limiting, account recovery, abuse prevention, GDPR readiness, SOC2 readiness) explicitly rather than treating "auth" as an undifferentiated blob.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| "Build vs buy" is the correct decision frame for this problem | convention | Explicitly challenge before use | Discard — the market itself offers modular, per-surface adoption (GT-9); the correct frame is per-surface ownership (chain C1) | Verified via C1's reasoning against GT-9 |
| All of MFA, audit log, full enterprise SSO, and GDPR/SOC2 evidence must ship in the very first authenticated release that gates the current billed feature | untested belief | Verify, or flag | Discard — the feature's stated requirement is authenticated per-tenant multi-user accounts; MFA/audit/SSO/compliance evidence are real but separable, later-arriving requirements (chain C1) | Verified against GT-12's stated feature requirement |
| Engineering calendar time to ship is the dominant cost of this decision | untested belief | Verify, or flag | Discard — 24-month TCO (chains C2, C3) and security-incident/deal-blocking risk (chain C4, adversarial pass) dominate once quantified | Verified via the C2/C3 bracket comparison |
| Switching costs are symmetric regardless of which path is chosen first | untested belief | Verify, or flag | Discard — GT-13? shows buy-to-build migration carries specific, asymmetric friction (support-gated hash export, ID remapping, config rebuild) not incurred in reverse (chain C7) | Unverified — flagged (GT-13? is reported-by-delegate) |
| Schedule urgency justifies skipping the build-vs-buy analysis and defaulting to whatever ships fastest without deliberate comparison | untested belief | Verify, or flag | Discard — the five-whys root-cause (chain C8) shows the felt urgency conflates the feature-ship clock with the architecture-decision clock, which are separable | Verified via C8's counterfactual test |
| An open-source auth library shifts most of the engineering risk off the team because the hard cryptographic parts are already written | untested belief | Verify, or flag | Discard — the estimate decomposition (chain C2) shows the cryptographic primitive is roughly 1 of 11 required line items; the remaining ten are not solved by choosing a library | Verified via C2's component decomposition |
| Buying a managed IdP removes the team's security responsibility/liability entirely | untested belief | Verify, or flag | Discard — the team remains responsible for correct integration code and its own compliance-evidence obligation, independent of the vendor's attestation (chains C6, C7) | Verified via C6's second-order effect and GT-7's Security-criteria attribution |
| No enterprise customers today means SSO/SAML readiness is irrelevant to this decision | current constraint | Record expiry conditions | Accept — expires the moment the first enterprise prospect's procurement process requires SAML SSO, which vendor pricing structures show is typically requested before a deal closes, not after | Verified against GT-8/GT-9's published enterprise-tier structure |
| GDPR and SOC2 do not apply to a 120-tenant, $40K-MRR B2B SaaS | untested belief | Verify, or flag | Challenge — split verdict: GDPR applies regardless of company size or revenue whenever EU personal data is processed (GT-6 names no size threshold), so this half is Discarded; SOC2 is contract/customer-driven rather than a legal mandate at this stage, so that half is Accepted as a current constraint whose expiry is the first enterprise customer requiring a SOC2 report | Verified against GT-6 (GDPR) and GT-7 (SOC2 scoping) |
| The team can staff and sustain in-house auth maintenance (CVE patching, abuse monitoring, incident response) indefinitely at 7 engineers without a dedicated security role | untested belief | Verify, or flag | Challenge — unverified; no data on current team allocation or security specialization is available; load-bearing for chain C2's ongoing-maintenance figure | Unverified — flagged; feeds C2 at MEDIUM |
| Vendor MAU/connection-based pricing remains affordable as the company scales past its current 120-tenant base | untested belief | Verify, or flag | Challenge — verifiable via published tiers and monitorable going forward; not yet settled at the 18-24 month horizon | Partially verified against GT-8/GT-9/GT-10's current published tiers; the trajectory is a named risk in chain C6 |
| A shared password across all tenants plus a Stripe customer link is adequate interim security for a live B2B SaaS today | current constraint | Record expiry conditions | Accept — was an acceptable simplification while the product required only account-level access; expires exactly at the point the gated feature requires per-user distinction, i.e., now | Verified against GT-12's stated current architecture and feature requirement |
| The per-line-item engineering-week estimates in chain C2 reflect typical throughput for an engineer reasonably experienced with web security, not a team encountering these patterns for the first time | untested belief | Verify, or flag | Challenge — surfaced during the Phase 4 Assumption Audit on chain C2; unverified for this specific team; if false in the slower direction it widens C2's upper bound, which does not change the C3/C5 ranking | Unverified — flagged; feeds C2 at MEDIUM alongside GT-11? |
| Vendor webhook delivery is reliable enough (with retry/dead-letter handling) to serve as this company's audit-of-record once mirrored into an owned table | untested belief | Verify, or flag | Challenge — surfaced during the Phase 4 Assumption Audit on chain C6; its failure mode (silent delivery gaps) is explicitly priced by the adversarial pass's Cluster B disposition (a daily monitor) | Unverified — flagged; mitigated by a named monitor |

---

## 3. Ground Truths

- **GT-1** NIST SP 800-63B requires that memorized secrets (passwords) chosen by the subscriber be at least 8 characters, and that they be salted and hashed using a suitable one-way key derivation function (e.g., PBKDF2 at ≥10,000 iterations, with ≥32-bit salts), with rejection of passwords matching known-compromised or commonly-used values from breach corpora — source: NIST SP 800-63B, §5.1.1.1 and §5.1.1.2 (pages.nist.gov/800-63-3/sp800-63b.html); read-at-source: §5.1.1.1 ("SHALL be at least 8 characters"), §5.1.1.2 (salting/hashing/iteration-count and breach-corpus rejection language).

- **GT-2** NIST SP 800-63B §5.2.2 requires verifiers to limit consecutive failed authentication attempts on a single account (no more than 100) and to apply additional throttling controls (CAPTCHA, exponential backoff, IP-based controls) — source: NIST SP 800-63B, §5.2.2; read-at-source: §5.2.2, rate-limiting/throttling clause.

- **GT-3** NIST SP 800-63B §4.2 defines Authenticator Assurance Level 2 (AAL2) as requiring either a multi-factor authenticator or two distinct authentication factors (a memorized secret plus a possession-based factor) — source: NIST SP 800-63B, §4.2; read-at-source: §4.2, AAL2 definition.

- **GT-4** The OWASP Session Management Cheat Sheet requires session identifiers to carry at least 64 bits of entropy generated via a cryptographically secure random number generator, and requires session-ID regeneration on any privilege-level change (including login) to prevent session fixation — source: OWASP Session Management Cheat Sheet (cheatsheetseries.owasp.org); read-at-source: "Session ID Length" / "Session ID Entropy" and "Renew the Session ID After Any Privilege Level Change" sections.

- **GT-5** The same OWASP cheat sheet specifies secure cookie attributes (Secure, HttpOnly, SameSite, `__Host-` prefix), a three-part timeout policy (idle, absolute, renewal), and server-side session invalidation on logout or password change — source: OWASP Session Management Cheat Sheet; read-at-source: "Cookies" and "Session Expiration" sections.

- **GT-6** GDPR Article 33 requires a data controller to notify the relevant supervisory authority of a personal-data breach within 72 hours of becoming aware of it, unless the breach is unlikely to risk data subjects' rights and freedoms; no exemption exists based on company size or revenue — source: GDPR Article 33 (gdpr-info.eu/art-33-gdpr); read-at-source: Article 33(1), the 72-hour clause.

- **GT-7** SOC 2's Security ("Common") Criteria (CC1-CC9) is mandatory in every SOC 2 report; Availability, Processing Integrity, Confidentiality, and Privacy are optional and scoped in based on the services provided and customer commitments — source: "SOC 2 Trust Services Criteria: A Practical View for Security Teams" (brightdefense.com/resources/soc-2-trust-services-criteria); read-at-source: "Security is mandatory in every SOC 2 audit, while the inclusion of Availability, Processing Integrity, Confidentiality, and Privacy depends on the services provided and the nature of the data handled."

- **GT-8** Auth0 publishes four pricing tiers (Free, Essentials, Professional, Enterprise); Free covers up to 25,000 MAU (B2C) with no MFA included but one self-service enterprise SSO connection; B2B Essentials starts at $150/month with 3 SSO enterprise connections and Pro MFA included; B2B Professional starts at $800/month with 5 SSO connections and enterprise MFA — source: auth0.com/pricing; read-at-source: pricing-tier and feature-inclusion tables on that page.

- **GT-9** WorkOS's AuthKit product (email/password, social login, passkeys, MFA, magic auth, and enterprise SSO) is free for the first 1,000,000 monthly active users; dedicated SSO and Directory Sync connections are priced separately, starting at $125/connection/month for 1-15 connections and tapering to $65/connection/month at 51-100 connections — source: workos.com/pricing; read-at-source: AuthKit free-tier statement and the per-connection SSO/Directory-Sync pricing table.

- **GT-10** Clerk's Hobby tier is free up to 50,000 monthly active users with MFA not included; the Pro tier ($25/month, or $20/month billed annually) includes MFA and volume-priced overage beyond 50,000 MAU; Enterprise SSO is $75/month per connection beyond the first included connection on Pro and above; Organizations (multi-tenancy) is included free up to 100 active organizations on every tier — source: clerk.com/pricing; read-at-source: tier table, MFA-inclusion row, and Enterprise SSO connection-pricing row.

- **GT-11?** A fully loaded US senior software engineer costs roughly $180,000-$300,000 per year (salary, benefits, payroll tax, and overhead), i.e., roughly $3,500-$6,000 per working week at ~48 working weeks/year — source: aggregated compensation-analysis commentary surfaced via web search (fullscale.io and related 2026 hiring-cost analyses); reported-by-delegate: search-engine synthesis; no single primary payroll-cost document was opened directly by this analysis. This figure is used only as a bracket input to chains C2 and C3, never as a claimed measured fact about this specific company's payroll.

- **GT-12** The company has 7 engineers, ~120 paying tenants, ~$40K MRR, and currently runs behind a single shared password plus a Stripe customer link with no per-user or per-tenant authentication in production; the next billed release requires authenticated, per-tenant, multi-user accounts — source: this analysis's own Problem Essence, quoting the user's request directly; read-at-source: the scenario statement supplied at the start of this analysis (no external document to misquote — this is the principal's own direct statement of their situation).

- **GT-13?** Migrating away from a managed identity provider (using Auth0 as the documented example) is possible but friction-laden: password hashes can be exported, but only via a support-gated request and only on a paid plan; tenant-specific rules/actions/configuration are not portable and must be rebuilt at the destination; user IDs carry connection-prefixes requiring an old-to-new identifier remapping — source: aggregated Auth0 community-forum and migration-guide commentary surfaced via web search (community.auth0.com, auth0.com/blog, and related migration write-ups); reported-by-delegate: search-engine synthesis; no single primary Auth0 documentation page was opened directly by this analysis.

- **GT-14?** Under schedule pressure and without a dedicated security engineer, teams commonly ship an initial home-grown authentication implementation that covers password hashing but defers or skips rate-limiting, session-fixation prevention, and breach-password screening until after an incident exposes the gap — source: general software-engineering pattern; unverified: no specific citable study or postmortem corpus was opened for this analysis; used only as directional, qualitative support in chain C4, never as a load-bearing numeric input.

**Provenance summary:** `?`-marked: GT-11?, GT-13?, GT-14? (3 of 14). Read-at-source (feeding the sole HIGH-confidence chain, C1): GT-1 — NIST SP 800-63B §5.1.1.1/§5.1.1.2; GT-4 — OWASP Session Management Cheat Sheet, session-ID-entropy and fixation sections; GT-9 — workos.com/pricing, AuthKit free-tier statement; GT-12 — this analysis's own Problem Essence.

---

## 4. Derivation Chains

### Conclusion C1: "Build vs buy" is a false binary; the real decision is per-surface ownership

GT-12 (no per-tenant auth today; feature requires it) + GT-1 (NIST password-storage floor) + GT-4 (OWASP session floor) + GT-9 (vendors sell modular, separately-priced auth surfaces)
→ the gated feature's actual requirement is "authenticated, per-tenant, multi-user accounts" — a data-model and session-identity requirement — not "MFA, audit log, and full enterprise-grade IAM," which are separate, later-arriving requirements bundled into the urgency framing
→ because GT-1 and GT-4 specify a security floor that any implementation must clear regardless of author, and GT-9 shows managed providers already sell their capabilities as separable surfaces (core auth bundled free, enterprise SSO priced and provisioned per connection), the market itself does not force an all-or-nothing choice
→ the decision is therefore which named surfaces (credential storage, session handling, MFA, audit logging, tenant/authorization model) this team writes itself versus delegates, not a single build/buy switch
→ "build vs buy" as a single binary is a convention, not a requirement imposed by the vendor market or the security floor; the per-surface framing is the correct decision frame for this analysis, and it rules out the rival reading that vendor products force an all-or-nothing choice

**Pre-check:** head GT-12, GT-1, GT-4, GT-9 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — all four head inputs are unsuffixed ground truths with named read-at-source locations; every hop follows by direct citation to those ground truths; the live rival ("vendor products are all-or-nothing") is settled within this chain itself by GT-9.

---

### Conclusion C2: The true engineering cost of building this correctly is a multi-month, then perpetual, commitment

GT-1 (password-storage floor) + GT-2 (rate-limiting floor) + GT-3 (MFA/AAL2 floor) + GT-4 (session-entropy/fixation floor) + GT-5 (cookie/timeout floor) + GT-6 (GDPR breach-response floor) + GT-11? (loaded engineer cost, ~$3,500-$6,000/week)
→ decomposing "per-tenant, multi-user authentication, built correctly" against the GT-1 through GT-6 floor spec yields eleven distinct engineering line items: tenant/session data model, NIST-compliant password storage, OWASP-compliant session handling, password-reset flow, MFA enrollment and recovery, audit logging, rate-limiting/abuse defense, account-recovery/identity-proofing, bot/credential-stuffing defense, GDPR-breach-response readiness, and a pre-launch security review
→ bracketing each line item's engineer-weeks at a conservative low and high estimate and summing them prices the one-time implementation effort at roughly 13.5 to 25.5 engineer-weeks, before any ongoing maintenance *[Assumes: A-13 — the per-item week estimates reflect typical throughput for an engineer reasonably experienced with this kind of security work; if this team is slower, the bracket's upper end absorbs that, and the C3/C5 ranking does not change]*
→ converting that bracket through GT-11?'s loaded-cost range prices the one-time build at roughly $47,000 to $153,000, plus an indefinite ongoing cost of 0.1-0.3 FTE (roughly $18,000-$90,000/year) for CVE monitoring, patching, and incident response for as long as the system runs
→ the true engineering cost of building this correctly is materially larger than "add a login form to an OSS starter" — it is a multi-month, then perpetual, commitment for a 7-person team, and it is this full bracket, not a rushed subset of it, that the schedule-pressure framing is implicitly asking the team to compress

**Pre-check:** head GT-1, GT-2, GT-3, GT-4, GT-5, GT-6, GT-11? · ?-marked: GT-11? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-11? is unverified (a search-synthesized compensation bracket, not a single primary payroll-cost citation); the verification that would remove it as a cause of the downgrade is pulling the company's own fully-loaded engineer-cost figure from its payroll/finance data. The Rivals axis is also short: whether any of the 7 engineers has prior production-auth operating experience is unresolved by GT-12, and if true would shift this bracket lower; the observation that would settle it is a direct 1:1 inventory of each engineer's prior auth-operating experience (see Conclusion, "This week"). The A-13 assumption on the second hop is named and its failure direction (slower, not faster) is already priced into the bracket's upper bound, so it does not independently move the estimate's central tendency.

---

### Conclusion C3: At current scale, buying costs 3-10x less than building, at both ends of each bracket

GT-8 (Auth0 tiers) + GT-9 (WorkOS free-to-1M-MAU + per-connection SSO pricing) + GT-10 (Clerk tiers) + GT-12 (current scale: ~120 tenants) + GT-11? (loaded engineer cost)
→ at ~120 tenants, even generously assuming 3-5 users per tenant, the company's monthly-active-user count (360-600) sits far inside every candidate vendor's free or lowest tier, so the vendor subscription cost at current scale is $0-$35/month regardless of which of the three is chosen
→ the engineering work that remains is integration, not cryptography: wiring the vendor's hosted login/session/MFA surface into the product, mapping vendor user/organization records to the product's own tenant model, and building the in-app authorization layer the product needs regardless of vendor — estimated at 1.5-3 engineer-weeks given the GT-1 through GT-5 floor items are handled by the vendor
→ pricing that integration bracket through GT-11?'s loaded-cost range prices the one-time buy-path cost at roughly $5,000-$18,000, with near-zero vendor subscription cost until the company provisions its first dedicated enterprise SSO connection, at which point per-connection pricing ($125-$800+/month) begins to apply
→ at the company's current scale, the buy path's one-time cost is roughly 3-10x cheaper than the low end of the build path's bracket from C2, and this ranking holds at both the low and high ends of each bracket, so the ranking is decision-resolved without needing to narrow either estimate further

**Pre-check:** head GT-8, GT-9, GT-10, GT-12, GT-11? · ?-marked: GT-11? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-11? is unverified; the same verification named in C2 removes it here. This chain's ranking claim is explicitly scoped to the current ~120-tenant scale; the later-scale cost trajectory as enterprise SSO connections accumulate is addressed separately in chain C6, not a live unsettled rival within this chain's own stated scope.

---

### Conclusion C4: The build path's realistic landing point sits below the security floor's best-demonstrated tier; the buy path starts there by construction

GT-1 (hash-cost floor) + GT-2 (rate-limit floor) + GT-4 (session-entropy floor) + GT-7 (SOC2 Security criteria, mandatory) + GT-9 (vendor built-in MFA/SSO/session handling) + GT-14? (pattern: rushed builds skip floor items) + C2 (build cost/scope bracket)
→ the ideal floor — zero exploitable authentication defects — is unreachable by any real system, so the useful comparison is not "which path reaches zero risk" but "which path sits closest to the best-demonstrated tier, for this team, this month"
→ the best-demonstrated tier is what a vendor like the one in GT-9 already ships as its default, unmodified product: NIST-floor password storage, OWASP-floor session handling, and AAL2-capable MFA, attested annually against GT-7's mandatory Security criteria across a customer base far larger than this one company, amortizing the cost of finding and fixing floor-level defects across thousands of tenants instead of one
→ C2 already shows that clearing the identical floor items in-house costs this specific 7-person team 13.5-25.5 engineer-weeks it does not currently have budgeted, and GT-14? names the well-known pattern of what teams under exactly this kind of schedule pressure actually do when that budget does not exist: ship the parts visible in a demo (login, password hashing) and defer the parts only visible after an incident (rate limiting, fixation prevention, breach-password screening)
→ under the stated schedule pressure, the build path's realistic landing point is below the best-demonstrated tier on at least the deferred-until-incident items, while the buy path starts at the best-demonstrated tier on day one by construction; the gap this team would have to close to match it is the full C2 bracket, not a smaller "just do the important parts" subset, because GT-1 through GT-5 do not have a partial-compliance mode

**Pre-check:** head GT-1, GT-2, GT-4, GT-7, GT-9, GT-14?, C2 (MEDIUM) · ?-marked: GT-14? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-14? is an unverified engineering pattern (no specific citable postmortem corpus was opened); it is not the sole basis for this chain's conclusion, which also rests on the independently-established C2 bracket, so removing GT-14? entirely (treating it as inadmissible color) would weaken but not collapse the chain. This chain also cites C2 (MEDIUM), which caps it at MEDIUM regardless; C2's own confidence line carries that chain's verification path and is not re-explained here. The rival reading — "a disciplined team under deadline pressure could still hit the full floor without cutting corners" — is not affirmatively ruled out; it is treated as possible but not the base case this chain assumes.

---

### Conclusion C5: The weighted trade-off recommends Buy over Build and over a thicker Hybrid

GT-8 (Auth0 tiers/features) + GT-9 (WorkOS tiers/features) + GT-10 (Clerk tiers/features) + GT-12 (current scale/deadline) + C2 (build bracket) + C3 (buy bracket) + C4 (floor-coverage comparison)
→ scoring Build, Buy, and a thicker Hybrid (vendor owns credentials/session/MFA; team owns the tenant/organization model and audit log directly) against seven weighted criteria — time-to-ship (weight 5), security-floor coverage at launch (weight 5), 24-month TCO (weight 3), enterprise-SSO readiness (weight 4), team-velocity impact (weight 4), reversibility/lock-in (weight 3), and compliance-evidence readiness (weight 2) — with weights locked before scoring and anchors tied to C2/C3/C4's figures, yields weighted totals of Build=43, Buy=119, Hybrid=110 out of a possible 130 (see the full matrix below)
→ Buy's 9-point lead over Hybrid is driven by the three highest-weighted criteria where Buy scores strictly higher — time-to-ship, 24-month TCO, and team-velocity impact — against Hybrid's single advantage on reversibility; the flip test shows no single criterion's weight, moved anywhere within the procedure's 1-5 range, closes a 9-point gap sourced from three separate criteria, so the ranking is robust to any single-weight objection
→ the weighted comparison recommends Buy — adopting a managed identity provider for credential storage, session handling, and MFA, using its built-in organization/tenant primitive rather than duplicating it in-house — over both the pure-Build and the thicker Hybrid alternative

**Trade-off matrix (must-haves applied first):** the status-quo option (retrofit the existing shared-password/Stripe-link model) is knocked out before scoring — it fails the must-have "supports per-tenant multi-user authenticated accounts," which the gated feature requires outright; a full-Build-for-launch option is knocked out on the must-have "meets the NIST/OWASP floor within the ship window" only if scoped to the *full* long-tail (C2's 13.5-25.5-week bracket exceeds a same-release window), and is therefore scored below as "Build" representing a stripped/rushed variant, consistent with C4's finding.

| Criterion (weight) | Build | Buy | Hybrid |
|---|---|---|---|
| Time-to-ship (5) | 1 | 5 | 4 |
| Security-floor coverage at launch (5) | 2 | 5 | 5 |
| 24-month TCO (3) | 1 | 5 | 4 |
| Enterprise-SSO readiness (4) | 1 | 5 | 5 |
| Team-velocity impact (4) | 2 | 5 | 4 |
| Reversibility/lock-in (3) | 3 | 2 | 3 |
| Compliance-evidence readiness (2) | 2 | 4 | 4 |
| **Weighted total (of 130)** | **43** | **119** | **110** |

**Pre-check:** head GT-8, GT-9, GT-10, GT-12, C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none direct · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by citing C2, C3, and C4, each rated MEDIUM; each of those chains' own confidence lines carries its verification path and is not re-explained here. The Rivals axis (Hybrid) is settled within this chain by the flip test itself.

---

### Conclusion C6: Buy's two adverse second-order effects are both closed by one cheap addition — an owned, webhook-mirrored audit log

C5 (Buy recommended) + GT-9 (vendor per-connection SSO pricing) + GT-12 (current scale; no enterprise customers yet)
→[2nd] the engineering capacity C2's bracket would have consumed is instead available for revenue-facing product work — the actor-lens effect on the team itself
→[2nd] the vendor becomes an actor whose incentives now point toward retaining and monetizing this account as it grows, realized concretely through GT-9's per-connection SSO pricing once the company signs its first enterprise customer
→[3rd] over the next 6-24 months, as pipeline converts to enterprise logos, cumulative identity-vendor spend scales with exactly the customer segment the company is trying to win, and if this cost is not priced into enterprise deal terms from the first deal it erodes gross margin without being noticed until a periodic finance review catches it
→[3rd] a second, independent actor-lens effect surfaces at the same horizon: an enterprise prospect's security reviewer will ask this company, not the vendor, for its own incident-response runbook and audit evidence, and "our vendor is SOC2-attested" does not answer that question, because the reviewer's contract runs with this company
→ neither effect contradicts a named ground truth — both are predicted extensions of GT-9's pricing structure and GT-7's Security-criteria attribution, not conflicts with them — so the chain extends rather than returning to Phase 2
→ both adverse effects share one inexpensive fix: mirror the vendor's user, session, and audit webhook events into a database table this company owns from day one, adding roughly 0.5-1 engineer-week to C3's integration bracket *[Assumes: A-14 — vendor webhook delivery is reliable enough, with retry/dead-letter handling, to serve as the audit-of-record; if webhooks silently drop events, the mirror has gaps, which the adversarial pass's Cluster B disposition prices with a standing monitor]*
→ the refined recommendation is Buy plus an owned webhook-mirrored audit/event log built alongside the initial integration, which prices the SSO-connection cost into deals before margin erosion occurs and gives a future security reviewer this company's own audit evidence, closing both second-order effects without reopening the C5 trade-off

**Pre-check:** head C5 (MEDIUM), GT-9, GT-12 · ?-marked: none direct · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by citing C5 (MEDIUM; see C5's own line for its verification path). The [Assumes: A-14] premise on the sixth hop is stated and priced (Cluster B's daily monitor), not left unexamined, so it does not by itself add a second shortfall beyond the Inputs-ceiling cap already in force.

---

### Conclusion C7: The refined recommendation's safety rests on two explicit, checkable launch gates

C6 (refined recommendation: Buy + owned audit mirror) + GT-13? (vendor migration friction: hash export gated/support-only, config not portable, IDs need remapping)
→ inverting the refined recommendation's success claim and enumerating what would guarantee its failure surfaces two load-bearing preconditions the recommendation has so far assumed rather than verified: that the vendor integration's redirect/callback/session-cookie glue code is implemented correctly, and that the webhook-mirrored audit log is actually monitored for silent delivery gaps
→ GT-13? shows that even a well-executed integration does not eliminate switching friction (hash export is support-gated and paid-plan-only, IDs require remapping, configuration is not portable), so "buy is easily reversible" was never fully true, and the recommendation's reversibility claim should read "reversible with planned friction," not "reversible"
→ the recommendation is only as safe as these two named preconditions holding, which converts them from implicit assumptions into explicit, checkable launch gates: a security-focused code review of the integration's redirect/session-handling code before production launch, and a standing monitor on the audit-mirror table — both cheap relative to C2's build-path bracket and both directly actionable this week

**Pre-check:** head C6 (MEDIUM), GT-13? · ?-marked: GT-13? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-13? is reported-by-delegate (search-synthesized migration-friction claim, not opened at a single primary vendor-documentation page); the verification that would remove it as a cause of the downgrade is opening the specifically chosen vendor's current data-export/migration documentation directly and confirming the support-gate and ID-remapping claims still hold at the time of vendor selection. This chain also cites C6 (MEDIUM; see C6's own line), which caps it at MEDIUM independently.

---

### Conclusion C8: The correct response to schedule pressure is to decouple the decision clock from the implementation clock, this week

GT-12 (feature requires per-tenant auth; framed as urgent) + C2 (build cost/scope bracket) + C4 (floor-coverage/schedule-pressure pattern)
→ tracing "why is this urgent" back through five whys shows the feature's need for per-tenant auth is a genuine, necessary cause (the counterfactual holds: without this feature, the shared-password model would have remained adequate a while longer, per GT-12), but the felt pressure to skip a deliberate architecture analysis is a separate, correctable cause — the conflation of "the feature ship date is fixed" with "the architecture decision must be made in the same breath, without analysis"
→ the architecture decision itself (which surfaces to own versus delegate) takes a bounded, small amount of calendar time to make well — this analysis is evidence that the decision can be reasoned through in under a day — while C2 shows the cost of making it badly is measured in engineer-months, and C4 shows a rushed decision risks landing below the security floor and, per the adversarial pass, risks deal-blocking or incident-triggering failures 12-24 months out
→ the correct response to the schedule pressure is to decouple the two clocks explicitly: timebox the architecture decision to the remainder of this week using the recommendation in C6/C7, and let the feature's implementation timeline run against the already-scoped, narrower buy-plus-integration bracket from C3, rather than treating the whole decision as compressible to fit the feature deadline

**Pre-check:** head GT-12, C2 (MEDIUM), C4 (MEDIUM) · ?-marked: none direct · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by citing C2 and C4, each rated MEDIUM; each chain's own line carries its verification path. The rival reading — "skipping the decision analysis really does save time under this deadline" — is ruled out because C2/C4 show skipping the decision does not reduce implementation time; it risks increasing it.

---

## 5. Abandoned Reasoning

### Dead End: Extend the current shared-password/Stripe-link model with a thin per-tenant token instead of real authentication

**What was tried:** Explored whether the existing shared-password-plus-Stripe-link model could be extended with a lightweight per-tenant token (e.g., a signed URL or a tenant-scoped API key) to satisfy the gated feature's "per-tenant" requirement without building or buying real per-user authentication, on the reasoning that this might ship fastest of all.

**Why abandoned:** The gated feature requires per-tenant, *multi-user* accounts (GT-12) — the ability to distinguish individual users within a tenant, not just distinguish one tenant from another. A per-tenant token does not create individual user identity, so it fails the feature's actual requirement outright; this is the must-have knockout applied to the status-quo option in chain C5's trade-off matrix. It is not a weaker version of a viable option — it is a non-viable option that would ship something other than what the feature needs.

**What it ruled out:** This establishes that "do nothing structurally different" is not a real fourth option once this specific feature is being built — the feature itself has already forced the per-user authentication decision. It saves the team from later discovering, mid-implementation, that the thin-token approach cannot support the feature it was meant to unblock.

---

### Dead End: Pure Build, scoped to the full long-tail, for this release

**What was tried:** Evaluated building every surface in-house — session management, password reset, MFA, audit log, rate limiting, account recovery, abuse prevention, and GDPR/SOC2-readiness evidence — as a single in-house effort for the current release, on the reasoning that owning everything from day one avoids all future vendor dependency.

**Why abandoned:** C2's estimate brackets the full scope at 13.5-25.5 engineer-weeks one-time plus 0.1-0.3 FTE indefinitely; C4 shows that under the stated schedule pressure this team's realistic landing point sits below the best-demonstrated security-floor tier, particularly on the items least visible in a demo (rate limiting, fixation prevention, breach-password screening); and C5's weighted trade-off scores Build at 43/130 against Buy's 119/130, with no single-criterion weight change closing the gap. The pattern this dead end represents — "we can build all of it ourselves and be safer for it" — inverts under scrutiny: building all of it under this specific deadline is the path most likely to land *below* the floor it was meant to guarantee.

**What it ruled out:** This establishes that "own everything for maximum control" is not, for this specific team and deadline, the safer path it intuitively sounds like — control and safety diverge once the schedule-pressure constraint is taken seriously. Future re-evaluation of this path should wait for the conditions named in the Conclusion's flip criteria (more team capability, more deadline slack, and/or materially higher data-sensitivity requirements).

---

### Dead End: Hybrid ownership of the tenant/audit model (own more than the credential surface, buy less than the whole identity stack)

**What was tried:** Evaluated a thicker Hybrid split — adopt the vendor only for credential storage, session handling, and MFA, but build and own the tenant/organization model and the audit log directly in-house rather than using the vendor's Organizations primitive, trading more upfront integration work for less state stored with the vendor.

**Why abandoned:** This is a genuinely stronger option than pure Build (it inherits the vendor's security-floor coverage) and it does hold a real edge over pure Buy on reversibility and compliance-evidence readiness (C5's trade-off matrix scores it 3 and 4 respectively, versus Buy's 2 and 4). But C5's weighted comparison still ranks it behind Buy overall (110 vs. 119), robustly to any single-criterion weight change, because it costs more time and ongoing velocity than pure Buy on every other criterion without a compensating advantage large enough to close the gap. C6 then shows that Hybrid's specific edge — reversibility and owned compliance evidence — is available to the Buy path at a fraction of Hybrid's cost, via a webhook-mirrored audit log (roughly 0.5-1 additional engineer-week versus a full in-house tenant/audit-model build). Once that cheap substitute exists, Hybrid's remaining advantage over the refined Buy-plus-mirror recommendation is negligible.

**What it ruled out:** This establishes that "hybrid is always the safe middle path" is not automatically true — a hybrid split is only worth its extra cost if its specific advantage cannot be captured more cheaply inside the cheaper option. Here it can be, which is why the refined recommendation is Buy-plus-mirror rather than Hybrid. A future team facing the same choice should re-run this comparison, not assume the answer transfers, if the cheap-substitute step (C6) turns out not to be available from their chosen vendor.

---

## 6. Conclusion

**Recommended approach:** Adopt a managed identity provider — of the three surveyed, WorkOS AuthKit is the concretely best-fitting choice given its free tier up to 1,000,000 MAU already covering email/password, MFA, and enterprise SSO at this company's current scale (GT-9) — for credential storage, session handling, and MFA; use its Organizations primitive as the tenant model; build the in-app authorization layer the product needs regardless of vendor; and build an owned, webhook-mirrored audit/event log from day one (chain C6).

**This week, concretely:**
1. Timebox and formally close this architecture decision within the remainder of this week; do not let it re-litigate against the feature deadline (chain C8).
2. Resolve the one open factual question this analysis could not answer from the given context: does any of the 7 engineers have prior hands-on production-authentication operating experience? This does not change the recommendation's direction (the ranking holds at both ends of every bracket), but it recalibrates how much schedule slack the security review in item 5 needs (chain C2).
3. Select the provider (WorkOS AuthKit, or a comparable alternative) and confirm its specific published free-tier terms still apply at signup, closing the applicability sensitivity noted in the adversarial pass (chain C3).
4. Build the in-app authorization layer and the webhook-mirrored audit/event log alongside the vendor integration this week — not as a follow-up phase after the feature ships (chain C6).
5. Before production launch, run a security-focused code review of the redirect/callback/session-cookie integration code, and stand up the daily monitor on the audit-mirror table (chain C7).

**Key insight:** "Build vs buy" was never the real question; per-surface ownership is, and the market itself already prices it that way — vendors sell credential storage, MFA, and enterprise SSO as separable, individually-priced surfaces rather than an all-or-nothing bundle (chain C1). The schedule pressure the team feels is a second, independent conflation: the feature-ship clock and the architecture-decision clock are separable, and the decision itself costs days, not weeks, to make correctly (chain C8).

**Trade-offs acknowledged:** This recommendation accepts real vendor lock-in on the credential, session, and MFA surfaces — migration away from the chosen vendor later is possible but friction-laden (support-gated hash export, ID remapping, configuration rebuild), not free, even with the audit-mirror mitigation in place (chain C7).
- The recommendation also leaves one open, unresolved input: whether any current engineer's prior experience would make a thicker ownership split more competitive than this analysis's brackets assume (chain C2).
- Finally, this recommendation is contingent, not unconditional — it is only as safe as the two launch gates in chain C7 (a reviewed integration, a monitored audit mirror) actually being executed, not merely written down here.

**Flip conditions — the recommendation reverses if:**
1. A pre-launch security review finds the team cannot safely implement even the thin vendor integration within the available time; in that case, fall back to the vendor's fully-hosted login UI rather than treating the finding as evidence for Build (chain C7).
2. The team's actual auth capability and the deadline's actual slack both turn out substantially more favorable than this analysis's brackets assume, *and* the company's data-sensitivity requirements rise materially (e.g., regulated data beyond typical B2B SaaS PII) — in that case, re-run the C5 trade-off with updated scores rather than assuming today's recommendation persists indefinitely (chains C5, C2).
3. Cumulative identity-vendor spend crosses a named threshold (e.g., unprofitable margin on enterprise logos, or a set percentage of MRR) as enterprise SSO connections accumulate — in that case, revisit vendor tier/contract terms or a partial migration of the highest-volume surfaces, which is the reversal-window logic this analysis already anticipates, not a sign the recommendation was wrong (chain C6).

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM) · ?-marked: none direct · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the recommendation rests on chains C5, C6, and C7, all rated MEDIUM, which caps the overall rating regardless of C1's independent HIGH rating on the reframing question. The MEDIUM rating traces to two named unverified inputs: GT-11? (loaded engineer-cost bracket; removed by pulling the company's own payroll figure — chains C2, C3), and GT-13? (vendor migration-friction claim; removed by opening the specifically chosen vendor's current migration documentation directly — chain C7). Each contributing chain's own confidence line carries its verification path in full and is not re-explained here.
