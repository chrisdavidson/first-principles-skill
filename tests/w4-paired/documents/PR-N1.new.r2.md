# First-Principles Analysis: Fastest Path to Automated TLS Certificate Renewal

**Step 0 (technique selection):** No technique-specific trigger phrase fires in the request ("fastest path to automated renewal" matches none of the pre-mortem/theoretical-limit/inversion/fishbone/five-whys/trade-off/second-order/estimate patterns). `MODE = full-composer`. All five phases run; companion techniques are invoked where a phase's own trigger fires (inversion at Phase 2, trade-off and mandatory second-order at Phase 4, pre-mortem at Phase 5) and logged as not-applicable where they don't (see the "Techniques not applied" block below).

**Pre-analysis repo search (performed before drafting anything):** grepped the whole tree for cert/ACME/TLS/SSL/nginx/Caddy/Traefik/CNAME keywords, globbed for `*.pem`/`*.crt`/`*.key`/`Caddyfile`/`nginx.conf`/`Dockerfile*`/`docker-compose*`/`CNAME`, listed the repo root, and read the sole GitHub Actions workflow in full. Result: no TLS-terminating infrastructure of any kind exists in this repository. This finding is Ground Truths GT-1 through GT-4 below and drives Chain C2.

---

## 1. Problem Essence

**Core problem:** Before any renewal automation can be designed, it must first be established whether this repository actually operates TLS-terminating infrastructure that could suffer expiry-driven failure; and — for whatever infrastructure the answer implicates (this repo, some other system, or none yet built) — what is the fastest engineering pattern that removes "certificate expired" as a possible cause of a broken client connection, treating issuance, deployment, and monitoring as three distinct problems rather than one.

**Success criteria:**
1. The Conclusion section states, citing a repo search, whether this repository terminates TLS anywhere (yes/no).
2. The Conclusion section gives a general-purpose recommendation, not invented repo-specific detail, given that no infrastructure was found.
3. The Conclusion section's recommended approach treats renewal (issuance) and reload/deployment as two separately-automated steps, not one.
4. The Conclusion section names an independent monitoring mechanism for the renewal automation itself, distinct from monitoring the certificate.
5. The Conclusion section states a numeric renewal-attempt margin (days before expiry) and names its source.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: This repository operates the TLS-terminating infrastructure "our TLS setup" refers to | untested belief | Verify by searching the repo | Discard — contradicted by GT-1 through GT-4; four independent search strategies found no TLS surface anywhere in the tracked tree | source: this session's own grep/find/read output |
| A2: An expired X.509 certificate causes a TLS client to reject the connection rather than silently degrade | physical law | Accept as ground-truth candidate | Accept — the validity-period check is a mandatory, protocol-level part of certificate path validation, not a deployer-configurable option | source: RFC 5280 §4.1.2.5 (read-at-source, GT-5); RFC 8446 §4.4.2.2 wording not located this session (GT-6?, unverified — flagged) |
| A3: "Renewal" (issuing a new certificate) and "reload/deployment" (making the terminating process serve it) are one operation that can be automated as a single step | convention | Explicitly challenge | Discard — same category error the user's own prompt named; issuing a certificate that is never loaded by the serving process leaves the expiring one live | unverified — flagged (not opened at source this session; carried forward into A9 below as the load-bearing form) |
| A4: A periodic scheduler (cron) is a reliable-enough trigger for an unattended renewal check | convention | Explicitly challenge | Challenge — cron's default failure mode is silent (no MTA/MAILTO ⇒ no signal on failure), and many minimal/container images ship no MTA at all | unverified — flagged; attempted verification of systemd's alternative (`systemd.timer(5)`) returned HTTP 403 this session — see Phase 3 failure record |
| A5: The renewal automation itself needs no monitoring separate from the certificate — "if it's automated, it stays working" | untested belief | Verify or flag | Discard — this is exactly the single point of failure the request names ("monitor the monitor"); an automation loop with no independent liveness check converts a page-worthy expiry into a silent one | source: derived from the Phase 2 inversion pass below, precondition P2/A10 |
| A6: ACME (RFC 8555) is available as the issuance protocol for whatever service eventually needs a certificate | current constraint | Record expiry conditions | Accept — holds for any CA that speaks ACME (Let's Encrypt, ZeroSSL, Google Trust Services, many enterprise CAs); expires the moment the certificate must come from an ACME-incapable internal PKI or an EV/manually-vetted CA | source: RFC 8555 abstract (read-at-source, GT-7) |
| A7: Renewing exactly once, right before expiry, with no retry margin, is an adequate cadence | untested belief | Verify | Discard — contradicted by GT-8 (Let's Encrypt's own guidance: check at least twice daily, renew with roughly a third of the certificate's lifetime remaining, retry failures with backoff rather than treat one failure as fatal) | source: read-at-source, GT-8 |
| A8: Publicly-trusted certificate maximum validity is shrinking on a CA/Browser-Forum policy schedule, not because of a cryptographic change | convention | Challenge — is this a convention or a hard bound? | Accept directionally; the specific schedule is unresolved — em-dash — plausible and consistent with well-known industry direction, but every attempted citation this session failed | unverified — flagged; three source URLs (CA/Browser Forum ballot, DigiCert blog, Google Security Blog) all returned HTTP 404 — see Phase 3 failure record (GT-9?) |
| A9 *(load-bearing, surfaced by inversion precondition P1)*: Automated issuance implies automated deployment/reload | untested belief | Verify | Discard — restates A3 as a formal precondition; every realistic renewal-automation failure mode traces back to this being false in practice | source: Phase 2 inversion procedure, precondition P1 |
| A10 *(load-bearing, surfaced by inversion precondition P2)*: The renewal scheduler's own liveness is observable independent of certificate state | untested belief | Verify | Challenge — true only if a heartbeat, dead-man's-switch, or `OnFailure=`-style alert is deliberately added; not true by default of cron or a bare timer | unverified — flagged; source attempt (systemd.timer man page) returned HTTP 403 — see Phase 3 failure record |
| A11 *(load-bearing, surfaced by inversion preconditions P3/P4)*: Retry margin and challenge-path monitoring are wide enough to absorb a transient CA/DNS failure before expiry | current constraint | Record expiry conditions | Accept — holds as long as the ~30-day margin (GT-8) is preserved end-to-end; expires the moment the margin is not widened proportionally to any future shortening of the underlying certificate's validity period (GT-9?) | source: Phase 2 inversion procedure, combined with GT-8 |

**Phase 2 inversion pass (trigger fired — "automate renewal" is exactly the too-obvious-a-goal case):** Inverted claim tested: *"Automating renewal does not eliminate expiry-driven client-connection failure."* Failure-guaranteeing conditions enumerated (≥5, from the operator, on-call, and external/adversary viewpoints): (1) renewal succeeds but nothing triggers reload; (2) the scheduler itself stops running unnoticed; (3) a CA rate limit or policy tightening outruns the retry/backoff window; (4) the ACME challenge target (DNS record, webroot, routing) silently changes after setup; (5) automation covers one node but the service actually runs behind multiple TLS-terminating replicas; (6) the ACME account/private key is rotated out-of-band by an unrelated process; (7) an adversary with transient control of the DNS-01 challenge zone interferes with a renewal window. Necessary preconditions derived: P1 (renewal always triggers deployment to every consumer) → A9; P2 (the scheduler's liveness is independently observable) → A10; P3/P4 (retry margin and challenge-path monitoring have enough headroom) → A11; P5 (every replica is covered) → carried narratively into the pre-mortem's Cluster 3, not promoted to a numbered row since no fleet exists yet (GT-1..4).

---

## 3. Ground Truths

- **GT-1** This repository's tracked tree contains no certificate files, no ACME/Let's Encrypt configuration, and no nginx/Caddy/Traefik configuration anywhere — source: this session's own content-keyword grep across the whole tree; read-at-source: direct Bash output, this session, repo root.
- **GT-2** The repository's only CI workflow (`.github/workflows/validation.yml`) runs `claude plugin validate`, `markdownlint-cli2`, and a battery of Python checks; none of its jobs stand up, terminate, or configure TLS for any service — source: direct read of the workflow file; read-at-source: lines 1–60, jobs `plugin-validate`/`markdownlint`/`check-links` visible, no deploy/TLS job present.
- **GT-3** There is no `CNAME`, `Dockerfile`, or `docker-compose*` file anywhere in the repository, and the repo root contains only documentation, Python scripts, the `shared/`/`first-principles/`/`tests/` trees, and packaging metadata — source: this session's `find`/`ls` output; read-at-source: this session's Bash output, repo root.
- **GT-4** CLAUDE.md, this repository's own maintained self-description, states the deliverable is "pure Markdown — no executable code ships inside the plugin," with no mention of a hosted service, custom domain, or deployment target — source: `/home/chrisdavidson/Projects/first-principles-skill/CLAUDE.md`, "Project" section; read-at-source: first paragraph.
- **GT-5** RFC 5280 defines a certificate's validity period as "the period of time from notBefore through notAfter, inclusive" (§4.1.2.5) — i.e., every X.509 certificate carries a hard, self-describing expiration boundary as part of its format — source: RFC 5280 (IETF); read-at-source: §4.1.2.5, quoted verbatim via WebFetch this session.
- **GT-6?** RFC 8446 (TLS 1.3) §4.4.2.2 is understood to require an endpoint to reject a certificate chain outside its validity period — unverified: the WebFetch attempt this session reached only §4.2.2 of the retrieved content and did not reach §4.4.2.2. **Phase 3 failure record:** source opened (`datatracker.ietf.org/doc/html/rfc8446`) but the asserted clause was not located in the retrieved excerpt — reason: citation does not support the claim (content not reached).
- **GT-7** RFC 8555 (ACME) "describes a protocol that a CA and an applicant can use to automate the process of verification and certificate issuance" — i.e., issuance is designed to be fully machine-drivable — source: RFC 8555 abstract; read-at-source: abstract text, quoted verbatim via WebFetch this session.
- **GT-8** Let's Encrypt's own integration guidance recommends checking ACME renewal information "at least twice a day," renewing once a certificate has "a third of their total lifetime left" (≈30 days before expiry for a 90-day certificate), and retrying a failed renewal "with exponential backoff, maxing out at once daily per certificate" rather than treating one failure as fatal — source: `https://letsencrypt.org/docs/integration-guide/`; read-at-source: quoted verbatim via WebFetch this session.
- **GT-9?** CA/Browser Forum policy is understood to be scheduling a reduction of maximum publicly-trusted certificate validity to a much shorter period by the end of the decade — unverified: three attempted source URLs (a CA/Browser Forum ballot page, a DigiCert blog post, a Google Security Blog post) all returned HTTP 404 this session. **Phase 3 failure record:** source unreachable ×3, no successful open. Retained only as directional context; not used as a load-bearing input to any chain below.

**Provenance summary.**
`?`-marked: GT-6, GT-9 (2 of 9).
Read-at-source: GT-1 (this session's grep/find scan of the working tree), GT-2 (`.github/workflows/validation.yml` lines 1–60), GT-3 (this session's find/ls output), GT-4 (CLAUDE.md "Project" section, first paragraph), GT-5 (RFC 5280 §4.1.2.5), GT-7 (RFC 8555 abstract), GT-8 (Let's Encrypt integration guide, quoted verbatim).

---

## 4. Derivation Chains

### Conclusion C1: Expiry-driven client-connection failure is an automation-coverage problem, not a protocol limitation

```text
GT-5 (X.509 validity period is a defined, hard boundary) + GT-7 (ACME/RFC 8555 makes verification-and-issuance fully machine-drivable)
→ every certificate's expiration is a designed-in, self-describing property of the certificate itself, and the protocol for replacing a certificate before that boundary is reached requires no manual step by design
→ expiry-driven client-connection failure is entirely a question of automation coverage — whether a machine-drivable replacement happened in time — not an inherent limitation of the TLS/PKI protocol stack
```

**Pre-check:** head GT-5, GT-7 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — both inputs are unsuffixed and read at source; the inference is a direct deduction with no live rival identified beyond a refinement (shortening validity periods raise the *required frequency* of automation but do not change the *category* of the problem — ruled compatible, not competing, by GT-7).

### Conclusion C2: This repository does not operate any TLS-terminating infrastructure today

```text
GT-1 (no cert/ACME/proxy config found by content search) + GT-2 (sole CI workflow has no TLS/deploy job) + GT-3 (no CNAME/Dockerfile/compose anywhere) + GT-4 (repo's own CLAUDE.md: pure Markdown, no executable code, no service)
→ four independently-designed search strategies — content-keyword search, filename globbing for standard cert/proxy/deploy files, a full top-level directory listing, and a complete read of the only CI workflow — converge on the same result with zero partial hits
→ this repository does not operate any TLS-terminating infrastructure today, so it has no certificate that can expire and no expiry-driven client-connection failure it can currently suffer
```

**Pre-check:** head GT-1, GT-2, GT-3, GT-4 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — rival considered: an undiscovered TLS artifact using naming outside the searched keyword/filename set. Ruled out by: four independently-designed search strategies converging on the same negative result with no partial hits (GT-1 through GT-4). This claim is deliberately scoped to *this repository's tracked tree*; whether "our TLS setup" refers to something outside that scope is a separate, open question addressed in the Conclusion, not a rival to this narrower claim.

### Conclusion C3: The fastest general-purpose path is a built-in-ACME or fully-managed termination layer, not a hand-rolled renew+reload script

```text
C1 (expiry is an automation-coverage problem) + GT-8 (LE guidance: check ≥2×/day, renew at ~1/3-lifetime margin, retry with backoff)
→ a weighted trade-off across five candidate automation architectures scores built-in-ACME edge termination 89 of 95 and a fully platform-managed certificate 87 of 95, well ahead of certbot-plus-systemd-timer at 59 and certbot-plus-cron at 44
→ that gap is driven by the time-to-working and atomicity criteria, weighted highest at 5 of 5 each, because only the top two options fold renewal and deployment into one upstream-maintained mechanism rather than gluing a separate reload step onto a separate renewal step [Assumes: A9]
→ the fastest general-purpose path to automated renewal is built-in ACME support at the edge — Caddy or Traefik — or an already-managed platform certificate wherever TLS termination already sits at that kind of boundary
```

**Pre-check:** head C1 (HIGH), GT-8 · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** MEDIUM — Inputs and Inference axes are clean (the `[Assumes: A9]` premise is priced: even if certbot-style clients did bundle reload automatically, contradicting A9, the top two options would still lead on the Time-to-working and Expertise criteria alone, since they require zero custom scripting versus "install and correctly configure a client," so the endpoint survives A9's failure, just with a smaller margin). What is short is **Rivals**: the top two options are a near-tie (89 vs. 87 of 95) and the flip test below shows the ranking inverts on a one-point change to a single criterion's weight. Closing path: pin down whether the actual deployment target needs self-hosted portability (favors built-in-ACME) or already sits at a managed platform boundary (ties or favors managed) — this is unknowable in the abstract because no live infrastructure exists yet to weight against (C2).

**Trade-off detail (flip test):** Criteria and weights: Time-to-working (5), Atomicity (5), Risk-surface (4), Portability (2), Expertise (3); max 95. Scores — certbot+cron 44, certbot+systemd-timer 59, Caddy/Traefik built-in ACME 89, cert-manager (k8s) 66, managed-platform cert 87. Smallest weight change that flips the top two: reducing the Portability weight from 2 to 1 makes the managed-platform option win by one point (87 vs. 86-equivalent); raising it above 2 only widens Caddy/Traefik's lead. No single-criterion change flips either option below third place — the certbot options and cert-manager stay decisively behind regardless of any single weight's adjustment.

### Conclusion C4: The fastest-path recommendation is incomplete without a monitor of the renewal mechanism itself, independent of the certificate

```text
C3 (recommend built-in-ACME or managed-platform termination) + GT-8 (a single renewal failure is not fatal and should be retried, per Let's Encrypt's own guidance)
→ a scheduler or built-in ACME client can itself stop running, drift out of configuration, or exhaust its retry budget without a human noticing, because a renewal that succeeded last cycle is not evidence the next cycle will also succeed [Assumes: A10]
→ any fastest-path recommendation is incomplete unless it also includes a liveness check that is independent of the renewal mechanism itself — a probe of the live TLS handshake's actual expiry date, alerting well inside the margin GT-8 establishes, rather than trusting the renewal tool's own exit status
→[2nd] adopting this pattern moves operator effort from writing and babysitting a renewal script to choosing a stack with ACME built in and wiring one external monitor, while also moving failure-mode visibility away from the operator and into whatever the built-in mechanism chooses to expose
→[3rd] if the chosen mechanism is ever replaced years later, the operators at that time may not be the people who made this choice, so the reasoning behind monitoring renewal separately from the certificate itself is at risk of being lost precisely because the fast path made the original decision invisible in day-to-day operation
```

**Pre-check:** head C3 (MEDIUM), GT-8 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes short: (1) **Inputs**, capped because the head cites C3 (MEDIUM) — closing path is whatever resolves C3's near-tie (see C3's own line, not re-explained here); (2) **Inference**, because the `[Assumes: A10]` premise is *not* priced the way A9 was — if A10 is false (the scheduler's failure genuinely is self-evidently observable by default), the conclusion weakens from "you must add independent monitoring" to "belt-and-suspenders," so the endpoint does not survive A10's failure unchanged. Closing path: empirically verify whether the chosen mechanism exposes a failure signal by default (e.g., Caddy's admin health endpoint, a systemd `OnFailure=` unit, or cert-manager's `Certificate` `Ready` condition) before relying on its absence being safe.

**Second-order pass (mandatory, not conditional):** Actor lens — operators shift from script-maintenance to stack-selection-plus-one-monitor; end users see fewer expiry outages but, if the built-in mechanism itself fails, less granular warning than a hand-built setup might have offered; cost shifts from engineer-time toward either $0 (self-hosted open source) or a platform fee; no adversarial/competitive dynamic identified beyond the CA-rate-limit scenario already covered in the Phase 2 inversion pass. Time lens — immediately, the "renewal script" bug class disappears because there is no custom script; after a few renewal cycles, the independent monitor's own reliability becomes empirically testable; once the arrangement is old enough to be assumed, the team's institutional memory of *why* renewal is monitored separately from the certificate is at risk (chain step →[3rd]). No extension step contradicts GT-1 through GT-9; no return to Phase 2 required. Checked against the decision's own success criterion (eliminate expiry-driven outages at minimum ongoing effort): the institutional-memory risk works against the "minimum effort forever" framing without defeating the immediate goal — reported honestly rather than smoothed over.

---

## 5. Abandoned Reasoning

### Dead End: Assuming "our TLS setup" must be inside this repository and inventing plausible specifics

**What was tried:** Considered skipping the search and proceeding as though this repo had, e.g., an nginx config or a Let's Encrypt cron job, and reasoning about *that*.
**Why abandoned:** No evidence supports it; GT-1 through GT-4 directly contradict it, and the task's own instructions explicitly bar presenting invented specifics as fact.
**What it ruled out:** Saves a future reader from re-deriving repo-specific TLS recommendations for a repository that has no TLS surface at all.

### Dead End: Defaulting to certbot+cron as "the" fastest path because it is the most commonly written-about pattern

**What was tried:** Reasoning by convention/analogy — "this is what tutorials show, so it must be fastest."
**Why abandoned:** The trade-off in chain C3 shows certbot+cron scores lowest of five real candidates (44/95) once setup-time and atomicity are weighted explicitly; tutorials optimize for teaching ACME internals, not engineering speed. Reasoning from "commonly documented" as direct evidence is barred by D-07 and would have produced a slower recommendation than the ground truths actually support.
**What it ruled out:** Saves a future reader from defaulting to certbot+cron out of familiarity when a built-in or managed mechanism is faster and available.

### Dead End: Asserting the specific CA/Browser-Forum shortened-validity schedule (e.g., a numeric day-count and year) as verified fact

**What was tried:** Citing a specific figure to strengthen the urgency argument for "why fast automation matters more every year."
**Why abandoned:** All three attempted source URLs returned HTTP 404 this session; the claim could not be verified at source.
**What it ruled out:** Saves a future reader from citing a specific numeric shortened-validity schedule from this analysis as though it were confirmed here — it is retained only as unverified directional context (GT-9?).

---

## 6. Conclusion

**Recommended approach:** First, verify before automating: this repository terminates no TLS today, so there is nothing here to renew (chain C2). Second, wherever "our TLS setup" actually lives — this repo's future infrastructure, another repository, or a platform boundary — the fastest general path is to put renewal and reload behind one upstream-maintained mechanism (Caddy's or Traefik's built-in ACME support, or an already-managed platform certificate) rather than hand-rolling certbot plus a cron or systemd-timer glue script (chain C3). Third, that automation must be paired with an independent liveness/expiry monitor that does not trust the renewal tool's own success signal (chain C4).

**Key insight:** The everyday phrase "automate renewal" silently bundles two separate operations — issuing a new certificate, and getting the terminating process to actually use it — and every realistic failure mode surfaced in this analysis traces back to that bundling being false in practice, not to renewal itself failing (chains C3, C4).

**Trade-offs acknowledged:** Built-in and managed mechanisms win decisively on setup speed and atomicity but sit in a near-tie with self-hosted certbot-plus-systemd-timer once portability and failure-mode transparency are weighted more heavily — a one-point shift in how much vendor lock-in matters is enough to flip which of the top two wins, and a black-box renewal mechanism gives less legible failure signals than one written in-house (chain C3).

**Pre-check:** head C2 (HIGH), C3 (MEDIUM), C4 (LOW) · ?-marked: none · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — the weakest contributing chain is C4 (LOW; see C4's own line for its two causes and closing paths), and per the calibration rule the Conclusion is rated no higher than its weakest contributing chain. C3 also contributes below HIGH (MEDIUM; see C3's own line — the top-two near-tie). This is a legitimate, honestly-caveated result, not a hedge: the repo-negative finding (C2) is solidly HIGH, but the "what to build if/when you do need this" recommendation is genuinely less certain because it hinges on an unweighted trade-off (no live infrastructure exists to weight against) and on an unverified premise about scheduler self-observability.

If "our TLS setup" actually refers to infrastructure outside this repository or session's visibility — a separate host, a different repository, or purely operational knowledge not committed anywhere — say so and point at it; this analysis found nothing to reason about here and gave the general-purpose pattern instead, per the task's own instruction to do exactly that rather than invent specifics.

---

## Techniques not applied (process output)

- **theoretical-limit** (Phase 1 essence-reframe invocation) — not applicable — the essence is already the operative question (verify infrastructure, then find the fastest safe automation path); it does not hinge on a conventional figure being mistaken for a hard bound.
- **theoretical-limit** (Phase 4 ceiling-derivation invocation) — not applicable — the decision at hand is which automation *architecture* to adopt (a setup-speed/ops-risk trade-off), not the physical/protocol ceiling on how fast a single ACME transaction can complete; no conclusion here turns on that ceiling, so trade-off analysis was used instead.
- **inversion** (Phase 5 adversarial-technique invocation) — not applicable — the conclusion is a plan/recommendation, not a bare claim; per the decision rule (inversion stress-tests a claim, pre-mortem stress-tests a plan), pre-mortem is used instead (see Adversarial pass record below).

(Inversion's Phase 2 invocation *did* fire — see the inversion pass under section 2.)

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | expiry is designed-in, replacement is machine-drivable | none | n/a |
| C1 | 2 | expiry-driven failure is a coverage problem, not a protocol limit | none | n/a |
| C2 | 1 | four search strategies converge with zero partial hits | none | n/a |
| C2 | 2 | repo operates no TLS infra today | none | n/a |
| C3 | 1 | trade-off ranks built-in-ACME/managed cert highest | none | n/a |
| C3 | 2 | gap driven by time-to-working/atomicity; only top two fold renewal+reload | A9 | yes (existing row) |
| C3 | 3 | recommend built-in-ACME/managed cert as fastest path | none | n/a |
| C4 | 1 | scheduler can fail silently; past success isn't evidence of future success | A10 | yes (existing row) |
| C4 | 2 | independent liveness monitor required | none | n/a |
| C4 | 3 [2nd] | operator effort and visibility shift | none | n/a |
| C4 | 4 [3rd] | institutional-memory risk on later replacement | none | n/a |

---

## Adversarial pass (process output)

**Recompute:** Trade-off totals independently redone: certbot+cron = 5(2)+5(2)+4(2)+2(5)+3(2) = 44; certbot+systemd = 5(3)+5(3)+4(3)+2(4)+3(3) = 59; Caddy/Traefik = 5(5)+5(5)+4(4)+2(4)+3(5) = 89; cert-manager = 5(3)+5(4)+4(4)+2(3)+3(3) = 66; managed-platform = 5(5)+5(5)+4(5)+2(1)+3(5) = 87. All figures match chain C3's text.

**Sensitivity:** For C2, the flip ground truth is GT-1 (a false negative in the search) — not `?`-marked; addressed by the multi-strategy convergence named on C2's own confidence line. For C3/C4, the flip ground truth is GT-8 — not `?`-marked. The decision-relevant sensitivity is the trade-off's own flip test (Portability weight 2→1 flips the top two), already stated under C3.

**Rival:** Headline — certbot+systemd-timer (score 59) as a legitimate rival to the top two, live and unsettled (drives C3's MEDIUM band). C2 — "TLS infra exists outside this repo's visibility," live and addressed in the Conclusion's closing line rather than settled outright.

**Premise (past tense):** This plan has already failed — six months after adopting built-in-ACME/managed-cert termination with an independent monitor, an expired certificate broke client connections anyway.

**Causes (unfiltered, ≥3 stakeholder viewpoints):**
*Operator/implementer:* (1) Caddy's ACME resolver was left in manual-cert mode by accident, so auto-renewal never ran. (2) The independent expiry monitor was pointed at the wrong hostname/port after a later infra change. (3) The managed-platform's custom domain was added via a legacy path that requires manual cert upload, so "managed" didn't actually mean "auto-renewed" for this domain.
*On-call engineer:* (4) The monitor fired weeks in advance, but to a channel nobody watches. (5) Renewal and reload both succeeded, but a stale replica behind a load balancer, pinned to an old image, never picked it up.
*External/adversary:* (6) A CA rate limit or validity-period shortening (GT-9?, once it actually lands) shrinks the safety margin faster than the retry/backoff logic was tuned for. (7) An adversary with transient control of the DNS-01 challenge zone interferes with a renewal window unnoticed. (8) The proxy's failure-open default silently falls back to a stale certificate rather than surfacing the renewal failure.

**Clusters:**
- **Cluster 1 — configuration silently didn't do what was assumed** (causes 1, 3, 8) — bears on C3 (A9) and GT-8.
- **Cluster 2 — monitoring exists but doesn't reach a human in time** (causes 2, 4) — bears on C4 (A10).
- **Cluster 3 — fleet/propagation gaps** (cause 5) — bears on C3's Atomicity criterion and precondition P5 (no fleet exists today, per GT-1..4).
- **Cluster 4 — external/adversarial and policy drift** (causes 6, 7) — bears on GT-9? and A11.

**Disposition:**
- Cluster 1 — *plan change:* require a post-change smoke test that performs a live TLS handshake against the public endpoint and asserts the served certificate's `notAfter` is fresh, not just "the config parsed" or "the process started."
- Cluster 2 — *plan change:* route the monitor's alert through an enforced on-call escalation (paging, not a Slack post) and periodically fire a test alert to verify the path itself, not just the certificate.
- Cluster 3 — *accepted risk, named mitigation:* no fleet exists today (GT-1..4); accepted, mitigated by stating explicitly that any future move to multiple TLS-terminating replicas must re-verify the renewal/reload path covers every replica before this recommendation can be relied on.
- Cluster 4 — *accepted risk, named mitigation:* the retry margin should be re-validated whenever the underlying certificate's maximum validity period changes; GT-9?'s shortening trend (direction, not the unverified number) is the trigger to revisit the margin periodically.

**Falsification:** This analysis's headline recommendation is false if a rigorous, apples-to-apples study shows hand-rolled certbot-plus-systemd-timer setups reach full automation-with-independent-monitoring in equal or less engineer-time than adopting/migrating to Caddy, Traefik, cert-manager, or a managed platform cert — or if this repository's actual undisclosed TLS infrastructure (per C2's stated scope limit) already runs a hand-rolled pattern successfully and migrating would cost more than it saves.

---

## §6→§4 closure ledger (process output)

- "First, verify before automating: this repository terminates no TLS today..." → chain C2 ✓
- "...the fastest general path is to put renewal and reload behind one upstream-maintained mechanism..." → chain C3 ✓
- "...that automation must be paired with an independent liveness/expiry monitor..." → chain C4 ✓
- "The everyday phrase 'automate renewal' silently bundles two separate operations..." → chain C3 ✓ (and C4)
- "Built-in and managed mechanisms win decisively on setup speed and atomicity but sit in a near-tie..." → chain C3 ✓
- "Confidence: LOW..." → chains C3, C4 ✓ (D-07 discharge)

---

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-5 + GT-7 | yes | n/a | yes | HIGH | yes (WebFetch RFC 5280, RFC 8555) | none |
| C2 | GT-1 + GT-2 + GT-3 + GT-4 | yes | n/a | yes | HIGH | yes (Bash grep/find/read, this session) | none |
| C3 | C1 + GT-8 | yes | n/a | yes | MEDIUM | yes (WebFetch letsencrypt.org integration guide) | none |
| C4 | C3 + GT-8 | yes | n/a | yes | LOW | yes (WebFetch systemd.timer man page — failed, 403) | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach: First, verify..." | bold lead-in | yes | colon closes bold span, content on same line | C2, C3, C4 |
| "Key insight: The everyday phrase..." | bold lead-in | yes | colon closes bold span, content on same line | C3 |
| "Trade-offs acknowledged: Built-in and managed..." | bold lead-in | yes | colon closes bold span, content on same line | C3 |
| "Pre-check: head C2 (HIGH), C3 (MEDIUM), C4 (LOW)..." | bold lead-in | yes | pre-check line is itself a claim per template rule | C2, C3, C4 |
| "Confidence: LOW — the weakest contributing chain..." | bold lead-in | yes | colon closes bold span, content on same line | C3, C4 |
| "If 'our TLS setup' actually refers to infrastructure outside..." | prose | no | no bold-colon lead-in, no list marker | n/a |

Scan complete: 4 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 5 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.

---

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "the fastest engineering pattern that removes 'certificate expired' as a possible cause of a broken client connection, treating issuance, deployment, and monitoring as three distinct problems rather than one"
Band: **Rigorous**
Justification: The statement names this specific problem (not a generic template phrase), each success criterion is a checkable verb+subject+outcome triplet scanning the Conclusion, and it distills past the triggering event ("reason about our TLS setup") to the real, verification-first question.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): rows for C3 Step 2 and C4 Step 1 show `A9`/`A10` "Added to Table? yes (existing row)"
Band: **Rigorous**
Justification: All 11 rows use the four-type scheme, verdicts carry token+em-dash+specific justification, unverified entries are flagged, at least five rows are Challenge/Discard rather than blanket Accept, and the Assumption Audit scan confirms every chain step introducing a new premise (A9, A10) was already reconciled against the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "GT-8 ... feeds C3 (MEDIUM), C4 (LOW)" versus GT-1/GT-2/GT-3/GT-4 feeding C2 (HIGH) and GT-5/GT-7 feeding C1 (HIGH)
Band: **Sound**
Justification: `?`-marked GTs are correctly enumerated (GT-6, GT-9) and match the list; every other unsuffixed, reachable GT feeds at least one HIGH chain except GT-8, which feeds only C3 (MEDIUM) and C4 (LOW) — a single unsuffixed-GT shortfall, which the rubric bands Sound rather than Hand-wavy.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): all four rows read `Form conforming? = yes`, `Dependency clean? = yes`
Band: **Rigorous**
Justification: Every conclusion has exactly one chain, each contains genuine intermediates, hops follow the arrow-led one-per-line form with no GT-leading hops and no early sentence closure, both `[Assumes: X]` steps are declared inline, no analogy is used as direct evidence, and Abandoned Reasoning documents three specific (non-generic) dead ends.

**Criterion 5: Validate**
Quoted span: "two axes short: (1) Inputs, capped because the head cites C3 (MEDIUM)... (2) Inference, because the `[Assumes: A10]` premise is not priced..."
Band: **Rigorous**
Justification: Every chain's band matches what its three axes license (C1/C2 HIGH with named rivals ruled out, C3 MEDIUM with the Rivals axis named and bounded, C4 LOW with two named axes and closing paths), the adversarial pass record carries every part (Recompute/Sensitivity/Rival/Premise/Causes/Clusters/Disposition/Falsification) with every cluster carrying a disposition, and the overall Conclusion rating (LOW) matches its weakest contributing chain rather than being inflated.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): all five claim rows carry a named chain in `Chain cited`, and the sixth row (the clarification-invitation prose) is correctly excluded as non-claim prose
Band: **Rigorous**
Justification: Every Conclusion-section claim traces to a chain established in section 4, no new reasoning is introduced in section 6, and the Key Insight (the renewal/reload conflation) is a non-obvious finding distinct from the Recommended Approach rather than a restatement of it.

**Gate result:** No criterion scored Absent; at most one criterion (Criterion 3) scored Hand-wavy-adjacent but actually landed Sound. **Gate cleared. Hand-wavy cap cleared (0 Hand-wavy).** No re-perception pass required.