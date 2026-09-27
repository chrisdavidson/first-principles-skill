# TLS Certificate Renewal Automation — First-Principles Analysis

**Scope note (stated once, not part of the six-section deliverable):** No specific stack was given, so this treats "our TLS setup" as a generic internet-facing deployment terminating TLS on ordinary infrastructure (a web server, a load balancer, or a small fleet of app-server nodes), using certificates from a public CA on the standard ACME renewal path. Where the topology assumption matters, the analysis names the branch point rather than picking silently.

---

## 1. Problem Essence

**Core problem:** What is the fastest deployable process that keeps a TLS certificate renewed before expiry without human action, and keeps failing silently *cheap to detect* rather than *invisible*, given that the industry's renewal cadence is being mandated shorter every year through 2029?

**Success criteria:**
1. A renewal completes across at least 3 consecutive cycles with zero human action taken on the renewing host.
2. Any renewal failure — regardless of cause — produces a human-visible alert *before* the certificate's actual `notAfter` date, verified by checking the live served certificate, not just the renewal job's own exit code.
3. The chosen validation method (HTTP-01 or DNS-01) continues to function as the CA/Browser Forum's mandated lifetime reduction (398 → 47 days by March 2029) compresses the renewal interval, without requiring a redesign at each step of that schedule.
4. The solution requires configuring existing, actively-maintained tooling — no bespoke renewal code that only the original author understands.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A-1: "Automation" means installing Certbot and cron-ing it | convention | Challenge before use | Challenge — em dash — the ACME protocol (GT-2) is client-agnostic; certbot is one of several actively maintained clients (GT-9?), and cron execution alone doesn't satisfy the essence's alerting criterion | unverified — flagged, feeds C3 |
| A-2: DNS-01 and HTTP-01 are interchangeable | untested belief | Verify or flag | Challenge — em dash — GT-7 (read-at-source) shows HTTP-01 is single-server/port-80-only and cannot validate wildcards, while DNS-01 is multi-server-safe and wildcard-capable; they are not interchangeable, they are topology-dependent | GT-7, letsencrypt.org/docs/challenge-types/ |
| A-3: Certs terminate at one single, named server | untested belief (topology unspecified) | Verify or flag | Challenge — em dash — no stack was given; treated generically, with the load-balancer/app-server/sidecar branch named explicitly at the point it matters (C4, GT-7) | unverified — flagged, topology not specified by user |
| A-4: A public CA (Let's Encrypt-class) is the intended CA | convention/untested belief | Challenge before use | Challenge — em dash — internal-only services commonly use internal PKI (GT-10?) instead, which changes the fastest-path answer entirely; the analysis proceeds on the public-CA branch because the task frames "our TLS setup" as a public web server/services, and names the internal-PKI branch as a documented alternative (Abandoned Reasoning #4) | unverified — flagged |
| A-5: A cron job running `renew` on a schedule constitutes reliable automated renewal | untested belief | Verify or flag | Discard as sufficient — em dash — necessary but not sufficient; a renewal that errors fails silently unless its exit status is captured and alerted on, which is exactly what success criterion 2 requires and cron alone doesn't provide | unverified — flagged, this is the belief the whole analysis exists to correct |
| A-6: Renewing once, right before the deadline, is as good as renewing early with margin | convention | Challenge before use | Accept, reclassified as an operational design pattern rather than mere convention — em dash — running the renewal check on a frequent timer (e.g. twice daily) against a threshold well before expiry converts a hard deadline into a soft one with multiple retries | certbot/acme.sh default renewal-threshold behavior, standard operational practice |
| A-7: Once renewal is "set up," it keeps working indefinitely with no revisiting | untested belief | Verify or flag | Discard — em dash — contradicted by GT-3/GT-4 (the mandated interval keeps shrinking) and by the pre-mortem's causes 3/5/6/9 below (credential rotation, CAA changes, account deactivation, threshold no longer fitting a shorter window) | unverified — flagged, this is the belief the pre-mortem directly targets |
| A-8: A certificate's validity cannot be extended in place; a renewal is a wholly new signed object | physical law (cryptographic definition) | Accept as ground-truth candidate | Accept — em dash — a digital signature covers a fixed byte structure including the validity dates; changing `notAfter` invalidates the existing signature and requires the CA to sign a new structure, which is definitionally a new issuance | promoted into C1's reasoning as a definitional premise |
| A-9: The CA/Browser Forum's shrinking-validity mandate (GT-4) is a policy constraint, not physics, and could in principle be relaxed | current constraint | Record expiry conditions | Accept — expires only if a future CA/Browser Forum ballot reverses SC-081v3's schedule; no current source indicates that trajectory — em dash — until then the constraint is contractual/industry-policy, not physical | cabforum.org SC-081v3 |
| A-10: A calendar reminder / manual expiry-watch email is an adequate substitute for automation | untested belief | Verify or flag | Discard — em dash — it doesn't remove human action, it just moves it earlier; fails success criterion 1 outright | unverified — flagged |
| A-11 *(surfaced by Assumption Audit, from C1 hop 1)*: A digital signature over the certificate structure cannot be altered without invalidating it | physical law | Accept as ground-truth candidate | Accept — em dash — this is the cryptographic-definitional fact underlying A-8; restated here because the audit found it declared inline on a chain step rather than in this table before that point | added at Phase 4 end-of-phase audit |
| A-12 *(surfaced by Assumption Audit, from C3)*: The team has host/shell access sufficient to add a systemd timer or cron entry and a small deploy-hook script | current constraint | Record expiry conditions | Accept — em dash — expires if the platform is a fully-managed PaaS with no host access, in which case the fastest path is the platform's own built-in cert management, not a self-run ACME client (see Abandoned Reasoning #2's boundary) | added at Phase 4 end-of-phase audit |
| A-13 *(surfaced by Assumption Audit, from C4)*: The team can add an external TLS-expiry probe independent of the renewing host | untested belief / current constraint | Verify or flag | Accept, flagged — em dash — this is genuinely new (small) tooling, not something most setups already have | added at Phase 4 end-of-phase audit |
| A-14 *(surfaced by Assumption Audit, second-order actor lens)*: The alerting channel itself (Slack/PagerDuty/email) is reliable and monitored | untested belief | Verify or flag | Accept, flagged — em dash — this is itself a single point of failure the pre-mortem surfaces (cause 1/7 below) | added at Phase 4 end-of-phase audit |

**Fishbone brainstorm (Phase 2, default six-category set)** — used to widen the assumption space around *why automated renewal fails in practice*, since intuition alone under-samples a multi-causal space:

- **People:** on-call rotation doesn't know who owns the renewal config; the engineer who wrote the deploy-hook has left.
- **Process:** no monitoring wired to the renewal job's exit code; no runbook for a renewal failure; the setup is never drilled/tested end-to-end.
- **Technology and Tools:** unmaintained/pinned ACME client falls behind CA API changes; missing or misdirected reload hook; multiple nodes renewing independently without shared state.
- **Environment:** firewall/NAT change blocks inbound port 80/443 after initial setup; DNS-provider API credential rotates or expires, breaking DNS-01 automation; host IP changes, breaking an A-record HTTP-01 setup.
- **Information:** no dashboard surfaces days-to-expiry; a CAA DNS record added for an unrelated reason silently restricts issuance to a different CA than the one configured.
- **Resources:** disk fills up and the renewal write fails silently; duplicate renewal attempts across environments sharing one domain name interact with rate limits.

Discriminating observations for the three highest-priority branches: **(Technology) missing/misdirected reload hook** — distinguishing observation: the certificate file on disk has a newer `notAfter` than the one the live TLS handshake serves; **(Process) no monitoring on exit code** — distinguishing observation: `certbot renew` logs show failures with no corresponding alert ever fired; **(Environment) DNS/API credential rotation** — distinguishing observation: the renewal job's error output names an authentication failure specifically, not a network or rate-limit error. Each of these three feeds a distinct Ground Truth or pre-mortem cause below rather than staying an undifferentiated worry.

---

## 3. Ground Truths

- **GT-1** An X.509 certificate carries a fixed validity interval; "the validity period for a certificate is the period of time from notBefore through notAfter, inclusive," and the CA's warranty of status information is bounded to that window — source: RFC 5280 §4.1.2.5; read-at-source: quoted clause above.
- **GT-2** ACME (RFC 8555) "describes a protocol that a CA and an applicant can use to automate the process of verification and certificate issuance," and requires the client to "demonstrate that it controls the identifiers in the requested certificate" via challenge-response, at each order — source: RFC 8555 Abstract and protocol description; read-at-source: quoted clauses above.
- **GT-3** Let's Encrypt currently issues 90-day certificates and has published a phased shortening: the `tlsserver` profile moved to opt-in 45-day certs on May 13, 2026; the default `classic` profile moves to a 64-day maximum on February 10, 2027; and to 45 days on February 16, 2028 — source: letsencrypt.org/2025/12/02/from-90-to-45; read-at-source: quoted timeline above.
- **GT-4** CA/Browser Forum Ballot SC-081v3 (approved April 11, 2025) mandates an industry-wide reduction of maximum public TLS certificate validity from 398 days to 47 days, "starting in March 2026 and concluding in March 2029" — source: cabforum.org/2025/04/11/ballot-sc081v3…; read-at-source: quoted clause above.
- **GT-5?** Secondary industry reporting states the SC-081v3 phase-in as a 200-day maximum from March 15, 2026 and a 100-day maximum from a 2027 date, en route to 47 days by March 2029 — cited to: AppViewX, SSL.com, DigiCert, Sectigo blog posts; reported-by-delegate — the exact intermediate day-counts were not located verbatim in the primary ballot page this analysis opened (it names only the two endpoints, 398 and 47 days, and the March 2026 – March 2029 window).
- **GT-6** Let's Encrypt allows "up to 50 certificates... per registered domain... every 7 days," but "renewals coordinated by ARI offer the unique benefit of being exempt from all rate limits" — source: letsencrypt.org/docs/rate-limits/; read-at-source: quoted clauses above.
- **GT-7** The HTTP-01 challenge "can only be done on port 80" and requires the challenge file be "available on all" servers in a multi-server deployment; DNS-01 "works well even if you have multiple web servers" and supports wildcard issuance, since validation happens at the DNS layer — source: letsencrypt.org/docs/challenge-types/; read-at-source: quoted clauses above.
- **GT-8?** Most TLS-terminating server software does not automatically reload a rewritten certificate file; ACME clients such as Certbot expose an explicit deploy-hook mechanism (e.g., a script under `renewal-hooks/deploy` calling `systemctl reload nginx`) precisely because this step is not automatic — cited to: Certbot documentation and multiple independent operator write-ups surfaced by search; reported-by-delegate — this analysis did not WebFetch Certbot's own hook-reference page directly.
- **GT-9?** Mature, actively-maintained ACME clients that support ARI exist (certbot, acme.sh, and others), and some server/platform software (Caddy, Traefik, cert-manager) issues and renews ACME certificates natively without a separate client — cited to: general ecosystem knowledge; unverified — not independently confirmed at source this session (e.g., no check of certbot's or acme.sh's repository for current ARI-support status).
- **GT-10?** Internal-only (non-internet-facing) services commonly use internal PKI (e.g., HashiCorp Vault's PKI secrets engine, smallstep step-ca, Active Directory Certificate Services autoenrollment) instead of a public CA, sidestepping public rate limits and public validation entirely — unverified — general knowledge, not fetched this session.
- **GT-11?** Let's Encrypt made short-lived (6-day) and IP-address certificates generally available in January 2026 — cited to: a search-result title ("6-day and IP Address Certificates are Generally Available – Let's Encrypt," dated 2026-01-15); unverified — this analysis saw only the search snippet/title and did not WebFetch the announcement itself.

**Provenance summary:**
```text
?-marked: GT-5, GT-8, GT-9, GT-10, GT-11 (5 of 11)
Read-at-source: GT-1 — RFC 5280 §4.1.2.5, validity-period clause
Read-at-source: GT-2 — RFC 8555 abstract + challenge-response description
Read-at-source: GT-3 — letsencrypt.org/2025/12/02/from-90-to-45, phased timeline
Read-at-source: GT-4 — cabforum.org SC-081v3 announcement, 398→47-day/March-2026–2029 clause
Read-at-source: GT-6 — letsencrypt.org/docs/rate-limits/, 50/7-days + ARI-exemption clauses
Read-at-source: GT-7 — letsencrypt.org/docs/challenge-types/, HTTP-01 port-80/multi-server clause and DNS-01 multi-server clause
```

No assumption that received a Discard verdict in Phase 2 (A-5, A-7, A-10) appears in this list.

---

## 4. Derivation Chains

### Conclusion C1: Certificate renewal is unavoidably a recurring operational task, and the recurrence interval is shrinking, not stabilizing, through at least 2029

GT-1 (fixed validity interval, definitional) + GT-4 (398→47-day mandated ceiling, March 2026–2029)
→ a certificate's signature binds its own validity dates, so extending validity in place would invalidate the CA's existing signature over the certificate structure *[Assumes: A-8/A-11 — a digital signature cannot be altered without invalidation]*
→ obtaining a new, validly-signed certificate therefore requires re-proving domain control under GT-2, so each renewal is a full re-issuance rather than a lightweight extension
→ because the industry-mandated ceiling on that validity window is being cut roughly eightfold by 2029 (GT-4), the number of required re-issuances per host per year rises on a fixed published schedule, not by accident or neglect

**Pre-check:** head GT-1, GT-4 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every head input is read-at-source; every hop is deductive from a cited fact plus a stated cryptographic-definitional premise (A-8/A-11); the strongest rival — "obtain a long-lived certificate once and avoid the recurring problem" — is named and ruled out for the public-CA branch this analysis assumes (Abandoned Reasoning #4: the rival is live only under assumption A-4 being false, i.e. an internal-PKI deployment, which GT-4's mandate does not constrain).

### Conclusion C2 [Speculative — not load-bearing]: The theoretical floor on renewal cadence is far below current convention, so a design that "just barely" works today has shrinking headroom by design

GT-4 (47-day mandated ceiling by 2029) + GT-11? (Let's Encrypt 6-day certificates GA'd January 2026)
→ the governing constraint behind short validity is risk containment against slow/unreliable revocation infrastructure (CRLs/OCSP), not a hard physical bound, so the "ideal floor" is set by how fast the ACME protocol itself can complete an order — minutes, not days
→ a CA has already productized a 6-day certificate today, well below the 2029-mandated 47-day ceiling, showing the gap between convention and what's already achievable is large and shrinking from the top, not from headroom running out at the bottom

**Pre-check:** head GT-4, GT-11? · ?-marked: GT-11? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-11? was seen only as a search-result title and not opened at source; verification: WebFetch letsencrypt.org/2026/01/15/6day-and-ip-general-availability directly. This chain is marked **[Speculative]**: it is offered as explanatory texture for why the recurrence problem only gets harder, not as a claim the Conclusion section rests on, and it is not cited on any other chain's head.

### Conclusion C3: The fastest reliable path is to keep the existing TLS-terminating technology and add a timer-driven, ARI-aware ACME client with a deploy/reload hook and an independent expiry probe — not to migrate to a self-ACME-ing platform

**Trade-off (Phase 4 companion technique).** Must-haves: works regardless of the unspecified topology (A-3); requires no bespoke code (A-1 discarded as insufficient); provides failure visibility independent of the renewal job itself (success criterion 2). Option "cron + certbot, no alerting, no ARI awareness" is **knocked out** here — it fails the failure-visibility must-have outright, so it is not scored.

Criteria (weighted before scoring, 1–5): Operational reliability (5), Failure visibility (5), Setup speed (3), Maintenance burden (3), Portability across unspecified topology (2). Anchors: reliability 1 = fails silently on first hiccup, 5 = automatic retries plus an independent out-of-band check; visibility 1 = no signal until outage, 5 = alert fires pre-expiry via a channel independent of the renewal job; setup speed 1 = >1 day of new infra, 5 = <30 minutes with tools already likely present; maintenance 1 = bespoke code to maintain forever, 5 = zero bespoke code on an actively-maintained upstream project; portability 1 = requires replacing the terminating server, 5 = works unmodified regardless of LB/app-server/sidecar placement.

| Option | Reliability (×5) | Visibility (×5) | Setup speed (×3) | Maintenance (×3) | Portability (×2) | Weighted total |
|---|---|---|---|---|---|---|
| B: ARI-aware client (certbot/acme.sh, GT-9?) + timer + deploy-hook (GT-8?) + independent probe | 5 | 5 | 4 | 5 | 5 | **87** |
| C: Adopt a self-ACME-ing terminating platform (Caddy/Traefik/cert-manager, GT-9?) | 5 | 3 | 2 | 5 | 1 | **63** |

Recompute (shown, not merely asserted): B = 5·5+5·5+4·3+5·3+5·2 = 25+25+12+15+10 = 87 ✓. C = 5·5+3·5+2·3+5·3+1·2 = 25+15+6+15+2 = 63 ✓.

**Flip test:** to make C win, Portability's weight would need to rise from 2 to roughly 8 — more than the combined weight of every other criterion — which is implausible for a question framed around speed on an unspecified, presumably already-deployed stack. No single-criterion weight change flips the result; the ranking is robust.

GT-2 (ACME automates verification+issuance, no bespoke code required) + GT-6 (ARI-coordinated renewals exempt from all rate limits) + GT-9? (mature, ARI-capable ACME clients and native-ACME platforms both exist)
→ weighted totals: keeping the existing terminating technology and adding an ARI-aware client scores 87 against 63 for migrating to a self-ACME-ing platform, the margin driven by setup speed and topology portability, and the flip test shows this ranking survives plausible reweighting
→ recommend: add a timer-driven, ARI-aware ACME client with a deploy/reload hook to the existing stack, rather than replacing the TLS-terminating technology

**Pre-check:** head GT-2, GT-6, GT-9? · ?-marked: GT-9? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-9? (client/platform ecosystem maturity) is unverified this session; verification: check certbot's and acme.sh's repositories directly for current ARI-support status and release cadence. The Inference axis is clean despite the trade-off's judgment-scored criteria, because the flip test above prices the sensitivity of those judgment calls and shows the ranking is not fragile to them. The rival (Option C) is named and ruled out by the trade-off itself, and the ruling-out is recorded at Abandoned Reasoning #2.

### Conclusion C4: A renewal job reporting success and a live endpoint actually serving the new certificate are two different facts, and reliable automation must check both

GT-7 (HTTP-01 is single-server/port-80-only; multi-server deployments must replicate the challenge file or use DNS-01) + GT-8? (most terminating servers require an explicit reload signal to pick up a renewed certificate file)
→ a multi-node deployment renewing independently, or a reload hook that is missing or misdirected, can leave the certificate file on disk newer than the certificate the live TLS handshake actually serves
→ a renewal job's own exit code cannot detect this gap, because the gap occurs downstream of the renewal step, in the reload/propagation step it does not observe
→ reliable automation therefore requires a second, independent check that probes the live TLS handshake's served certificate expiry, and alerts if that observed expiry is not receding on schedule — not only if the renewal job itself reports an error *[Assumes: A-13 — the team can add such an external probe]*

**Pre-check:** head GT-7, GT-8? · ?-marked: GT-8? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-8? is unverified at source; verification: this is directly and cheaply checkable in the reader's own environment (test whether the terminating process picks up a replaced certificate file without a reload signal). The A-13 premise on the last hop is priced: if the team cannot add an external probe, the endpoint of this chain does not hold and the design falls back to trusting the renewal job's self-report, which is exactly the weaker design this chain argues against — so the confidence caveat carries through to the Conclusion rather than being silently absorbed. Rival — "trust the renewal job's exit code and logs alone" — is named and ruled out by the reload-mismatch and multi-node scenarios above (Abandoned Reasoning #3).

---

## 5. Abandoned Reasoning

### Dead End: Plan renewal timing around Let's Encrypt's standard rate limit rather than adopting ARI
**What was tried:** An early framing considered staggering renewal times across environments to stay under the 50-certificates-per-7-days limit.
**Why abandoned:** GT-6 shows ARI-coordinated renewals are exempt from all rate limits — adopting ARI removes this entire failure class rather than managing around it, so "plan around the limit" is strictly dominated once ARI support (GT-9?) is available.
**What it ruled out:** Any design that manually schedules or throttles renewal timing instead of using ARI-aware clients.

### Dead End: Migrate the TLS-terminating layer to a self-ACME-ing platform (Caddy/Traefik/cert-manager) as "the fastest path"
**What was tried:** Considered as Option C in the C3 trade-off.
**Why abandoned:** Scored 63 against 87 for adding a client to the existing stack, driven by setup speed and portability — for an unspecified, presumably already-deployed stack, swapping the actual termination technology is a larger, slower change than the question asked for, even though steady-state reliability is comparable.
**What it ruled out:** Treating "switch termination technology" as faster than "add a well-configured client to what's already there," for a generic/unspecified deployment.

### Dead End: Trust the renewal job's own exit code and logs as the terminal reliability check
**What was tried:** An early framing of "reliable automation" as simply capturing and alerting on the ACME client's own exit status.
**Why abandoned:** C4 shows the reload-mismatch and multi-node scenarios produce a false "success" — the job can exit 0 while the live endpoint still serves the old certificate — so an exit-code-only design cannot distinguish "renewed" from "verifiably live."
**What it ruled out:** Any design that treats the renewal command's self-report as sufficient without an independent, out-of-band check.

### Dead End: Present a single universal recommendation covering internal-only deployments too
**What was tried:** Considered folding internal PKI (Vault/step-ca/ADCS, GT-10?) into the same recommendation as the public-CA path.
**Why abandoned:** This branch only applies when assumption A-4 (public CA intended) is false; the essence statement's default framing (a public web server/services) puts it out of scope, and conflating the two would misapply the public-CA-specific reasoning of C1/C3/C4 (built on GT-4's public-CA mandate and GT-6/GT-7's public-CA-specific mechanics) to a topology the user didn't describe.
**What it ruled out:** A single blended recommendation that would be wrong for either branch.

---

## 6. Conclusion

**Recommended approach:** Keep the existing TLS-terminating technology; add an ARI-aware ACME client (e.g., certbot or acme.sh) driven by a systemd timer or cron running at least twice daily, wired to a deploy/reload hook for the actual terminating process, and back it with an independent, external TLS-expiry probe that checks the live handshake — not the renewal job's exit code — and alerts on both failure and silence (chain C3).

**Key insight:** The bottleneck isn't the ACME protocol or which client you pick — GT-2 and GT-6 show issuance and rate limits are already solved for renewal by design, via ARI. The actual failure surface is coordination and independent verification: whether "renewed" and "verifiably live" are checked as two separate facts, and whether the whole chain (timer, credentials, reload hook, alert channel) is provisioned durably rather than as a manual one-off (chains C3, C4).

**Trade-offs acknowledged:** This recommendation deliberately does not migrate to a "renewal-native" platform (Caddy/Traefik/cert-manager) even though such platforms have comparable steady-state reliability, because that migration is a bigger, slower change than the question asked for (chains C1, C3). It also acknowledges that the mandated compression of the renewal interval (398→47 days by 2029) means a hardcoded "renew at N days left" threshold is not set-and-forget and needs periodic revisiting on the same cadence as the published CA/Browser Forum schedule (chain C1).

**Pre-check:** head C1 (HIGH), C3 (MEDIUM), C4 (MEDIUM) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — C3 and C4 each rest on one `?`-marked input (GT-9?, GT-8? respectively) even though the most load-bearing protocol and policy facts (GT-1, GT-2, GT-4, GT-6, GT-7) are read-at-source. Verification that would remove each cause: for C3, confirm certbot's/acme.sh's current ARI support directly against their repositories; for C4, test in your own environment whether the terminating process reloads a replaced certificate file without an explicit signal — this is a five-minute check available to any reader, not a barrier to acting on the recommendation now.

---

## Adversarial pass (process output)

**Recompute.** B = 5·5+5·5+4·3+5·3+5·2 = 87 ✓. C = 5·5+3·5+2·3+5·3+1·2 = 63 ✓. Both reproduce the values stated in C3.

**Sensitivity.** The single ground truth whose falsity would most threaten the headline recommendation is GT-9? (whether mature, ARI-capable ACME clients genuinely require "no bespoke code" today) — it is `?`-marked; verification path: check certbot's/acme.sh's ARI-support status and release cadence directly. Weakest link per chain: C1's weakest point is the cryptographic-definitional premise A-8/A-11 (well-established but not independently re-derived here); C3's weakest link is the judgment-scored trade-off criteria themselves, priced by the flip test; C4's weakest link is GT-8? (reload-on-renewal not independently fetched at source).

**Rival.** C1's rival (long-lived internal-CA certificate) is ruled out by scope at Abandoned Reasoning #4. C3's rival (migrate to a self-ACME-ing platform) is ruled out by the trade-off's own weighted totals, recorded at Abandoned Reasoning #2. C4's rival (trust exit code/logs alone) is ruled out at Abandoned Reasoning #3.

**Premise.** The automated renewal system described in C3 has already failed: a certificate expired in production despite everything in the recommendation being "set up."

**Causes** (unfiltered, from the on-call engineer's, the security/compliance owner's, the 18-months-later inheritor's, and an external/adversarial viewpoint):
1. The alert fired into a channel nobody watches (wrong channel, muted, or the on-call rotation changed without re-pointing it).
2. The renewal timer silently stopped because the host was rebuilt and the timer unit wasn't reprovisioned via infrastructure-as-code.
3. DNS-01 API credentials for the DNS provider expired or were rotated, and the ACME client's config was never updated.
4. The reload hook pointed at the wrong service name after a refactor, so renewal "succeeded" but the live process never picked up the new cert.
5. A CAA DNS record was added for an unrelated compliance reason, restricting issuance to a different CA than the one configured, silently blocking all future issuance.
6. The ACME account was deactivated during a security incident response and never re-registered.
7. The independent expiry probe's own credentials or network access were removed during a security lockdown, blinding the exact check meant to catch this.
8. The person who understood the deploy-hook script left; the script depends on an undocumented environment variable or path convention.
9. The CA's default validity dropped from 90 to 45 days (GT-3) between build time and now, and a hardcoded "renew if <30 days left, check daily" threshold no longer leaves adequate retry headroom under the shorter window.
10. Multiple environments (staging, prod, a forgotten canary) issuing for the same domain intermittently exhausted the non-ARI-recognized share of GT-6's rate limit.
11. An attacker who compromised the DNS provider or ACME account key could redirect or block issuance — showing the same DNS/ACME credential trust boundary that causes 3 and 6 also depend on is a security, not just reliability, single point of failure.

**Clusters** (structural weaknesses, cited to the chains/ground truths they bear on):
- **Silent infra drift** (causes 2, 4, 8) — bears on C3, GT-8?: the automation's correctness depends on host state (timer unit, script, path conventions) captured nowhere durable.
- **The independent check has its own single point of failure** (causes 1, 7) — bears on C4: the visibility layer C4 argues for can itself go dark.
- **External policy changes invalidate hardcoded assumptions** (causes 5, 6, 9) — bears on C1, GT-3, GT-4: CA-side and DNS-side policy changes break an automation that assumed a static external environment.
- **Shared-domain multi-environment interference** (cause 10) — bears on GT-6, GT-9?.
- **Credential trust boundary** (causes 3, 6, 11) — bears on GT-7/A-2: the DNS-01/ACME credentials are a security-sensitive point of both failure and compromise.

**Disposition:**
- Silent infra drift → **plan change**: provision the timer, deploy-hook script, and its configuration through the same infrastructure-as-code path as the rest of the host, with a named owner in a runbook.
- Independent check's own SPOF → **plan change**: the expiry probe's alerting must use a dead-man's-switch pattern (alerts if it hasn't reported successfully in N days), so silence itself is detectable, not just detected failures.
- External policy changes → **accepted risk with named mitigation**: cannot prevent CA/DNS policy changes; mitigation is a recurring review of the renewal threshold and CAA records, tied to the same calendar as the published CA/Browser Forum schedule (GT-4).
- Shared-domain interference → **plan change**: use ARI-aware clients in every environment issuing for the same domain, and inventory those environments before relying on GT-6's exemption.
- Credential trust boundary → **accepted risk with named mitigation**: scope DNS/ACME API credentials to the minimum required record type and shortest supported TTL, and fold credential rotation into a planned runbook rather than treating it as a surprise that breaks automation.

**Falsification.** This conclusion is false if a team that implements the described design (ARI-aware client, frequent timer, deploy-hook, independent probe with dead-man's-switch alerting) still experiences a silent, undetected certificate expiry in production.

---

## §6→§4 closure ledger (process output)

- "Keep the existing TLS-terminating technology; add an ARI-aware ACME client... independent expiry probe..." → chain C3 ✓
- "The bottleneck isn't the ACME protocol... coordination and independent verification..." → chains C3, C4 ✓
- "This recommendation deliberately does not migrate... acknowledges... compressing cadence... needs periodic revisiting" → chains C1, C3 ✓
- "Confidence: MEDIUM — C3 and C4 each rest on one `?`-marked input..." → chains C1, C3, C4 ✓

Scan complete: 4 §6 claims, 0 cut, 0 untraced.

---

## Techniques not applied (process output)

- `estimate` — not applicable — no conclusion turns on a quantity whose magnitude is uncertain; the decision hinges on protocol/policy facts and a qualitative trade-off, not an order-of-magnitude figure.
- `inversion` (Phase 5, second invocation) — not applicable — the headline conclusion is a plan/recommendation, not a claim, so the decision rule at Phase 5 routes the adversarial pass to pre-mortem instead; pre-mortem ran above.
- `five-whys` (causal mode) — not applicable — there is no specific past incident to root-cause here; only reduce-to-primitives mode was used, in Phase 3's irreducibility reasoning behind C1 (a certificate's fixed validity reduces to the definitional fact that a signature covers its own validity dates, which is a physical/mathematical primitive, not a further-reducible claim).

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | signature invalidated by altering validity dates | A-8/A-11 (cryptographic-definitional) | yes |
| C1 | 2 | new issuance requires re-proving control | none | n/a |
| C1 | 3 | mandated ceiling rising re-issuance frequency | none | n/a |
| C2 | 1 | governing constraint is risk containment, not physics | none | n/a |
| C2 | 2 | 6-day cert already productized | none | n/a |
| C3 | 1 (trade-off) | must-haves knock out cron-only option | A-1 (already in table) | n/a |
| C3 | 2 | weighted totals favor keeping existing stack | A-12 (host/shell access) | yes |
| C3 | 3 | recommend add ARI-aware client | none | n/a |
| C4 | 1 | multi-server/reload gap can desync file vs. served cert | none | n/a |
| C4 | 2 | exit code cannot see downstream gap | none | n/a |
| C4 | 3 | requires independent probe | A-13 (external probe capability) | yes |
| C3 (2nd-order, actor lens) | 4 | alert channel assumed reliable | A-14 (alert-channel reliability) | yes |

---

## Self-audit scan (process output)

**Table 1 — chain form**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 + GT-4 | yes | n/a | yes | HIGH | yes | none |
| C2 | GT-4 + GT-11? | yes | n/a | yes | MEDIUM [Speculative] | no | none |
| C3 | GT-2 + GT-6 + GT-9? | yes | n/a | yes | MEDIUM | yes | none |
| C4 | GT-7 + GT-8? | yes | n/a | yes | MEDIUM | yes (GT-7 fetched; GT-8 left `?`) | none |

**Table 2 — claim inventory (§6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach:" lead-in | bold lead-in | yes | colon closes bold span, carries assertion | C3 |
| "Key insight:" lead-in | bold lead-in | yes | colon closes bold span, carries assertion | C3, C4 |
| "Trade-offs acknowledged:" lead-in | bold lead-in | yes | colon closes bold span, carries assertion | C1, C3 |
| "Pre-check:" line | bold lead-in | yes | pre-check for Confidence line | C1, C3, C4 |
| "Confidence:" lead-in | bold lead-in | yes | colon closes bold span, carries assertion + D-07 explanation | C1, C3, C4 |

Scan complete: 4 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

---

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "What is the fastest deployable process that keeps a TLS certificate renewed before expiry without human action, and keeps failing silently *cheap to detect* rather than *invisible*, given that the industry's renewal cadence is being mandated shorter every year through 2029?"
Band: **Rigorous**
Justification: names the underlying question (not the triggering prompt or a symptom), and each of the four success criteria is a scannable verb+subject+outcome test checkable against §6 without further interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "C3 | 2 | weighted totals favor keeping existing stack | A-12 (host/shell access) | yes"
Band: **Rigorous**
Justification: all 14 rows use the four-type scheme, verdicts are token+em-dash+justification, multiple assumptions are Discarded (A-5, A-7, A-10) rather than uniformly Accepted, unverified entries used in chains are marked "unverified — flagged," and the audit scan shows the Phase 4 sweep ran exhaustively over every chain step.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-5, GT-8, GT-9, GT-10, GT-11 (5 of 11)" checked against the Ground Truths list, which carries `?` on exactly those five IDs.
Band: **Rigorous**
Justification: IDs are stable, every unsuffixed GT carries a read-at-source location (RFC/CA-org citations quoted verbatim), the enumeration matches the list on inspection, and every unsuffixed GT feeding a HIGH chain (GT-1, GT-4 on C1) names its read-at-source location.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan Table 1): "C1 | GT-1 + GT-4 | yes | n/a | yes | HIGH | yes | none" (and equivalent rows for C2–C4, all form-conforming and dependency-clean).
Band: **Rigorous**
Justification: every chain has a genuine intermediate, exactly one chain per conclusion, all four scan rows read `yes` for form and dependency, Abandoned Reasoning documents four specific dead ends with the prescribed structure, no analogy is used as direct evidence, and the one surfaced-but-undeclared-at-table-time premise (A-8/A-11) carries an inline `[Assumes:]` mark.

**Criterion 5: Validate**
Quoted span: "Sensitivity. The single ground truth whose falsity would most threaten the headline recommendation is GT-9?... Weakest link per chain: C1's weakest point is..."
Band: **Rigorous**
Justification: every chain's confidence line names its `?`-marked inputs with a verification path (or, for C2, is explicitly marked `[Speculative]` and not load-bearing per the EXCEPT clause); the §6 Confidence rating (MEDIUM) matches its weakest contributing chains; no chain with a `?` input is rated HIGH; the adversarial pass record is complete with all parts present and every cluster carrying a named disposition.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan Table 2): all five §6 constructs cite a chain id, none read "none — untraced."
Band: **Rigorous**
Justification: every §6 claim traces to a named §4 chain, no new reasoning is introduced in §6, and the Key Insight ("the bottleneck isn't the protocol... it's coordination and independent verification") is a non-obvious finding distinct from the Recommended Approach's action statement.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy (well under the one-Hand-wavy cap). The analysis clears the Self-Audit Gate.