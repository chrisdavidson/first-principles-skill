## Ground-truth check, stated up front

Per your explicit instruction, I scanned the working tree before reasoning about "our TLS setup." **This repository has no TLS/certificate surface.** A direct `grep -rniE` for `letsencrypt|acme|certbot|cert(ificate)?s?|tls|ssl|nginx|caddy|traefik|\.pem|\.crt|\.key` and a `find` for `Dockerfile*`, `docker-compose*`, and deploy/infra/server directories turned up: no Dockerfile, no docker-compose file, no nginx/caddy/traefik config, no ACME/certbot/letsencrypt reference anywhere in the tracked tree. The only keyword hits were false positives (a mill-certification example in an unrelated worked example, a Python dict `.key`, and an illustrative TLS-handshake RTT figure in an unrelated serialization-cost analysis doc). This repo is exactly what `CLAUDE.md` says it is: a pure-Markdown Claude Code plugin with no web-facing component.

So what follows is **general infrastructure guidance** about the fastest reliable path to automated certificate renewal, decomposed from first principles and grounded in read-at-source facts about the ACME protocol, Let's Encrypt, certbot, Caddy, and AWS ACM — not a verified fix to anything observed in this repository, because there is nothing here to fix. This is disclosed again formally in Ground Truth GT-1 and Chain C5 below, and it is the reason Chain C5 is rated MEDIUM rather than HIGH: I cannot rule out that you mean a different, unscanned system.

---

## Companion-technique workings (process output)

**Five-whys (reduce-to-primitives), applied to "an expired certificate breaks client connections":** an X.509 certificate carries a `notBefore`/`notAfter` validity window (RFC 5280 §4.1.2.5, definitional — read at source) → a TLS client's path-validation step checks the current time against that window as part of chain validation (RFC 5280's validation algorithm; the specific §6.1.3 algorithmic clause was not retrieved in full text during this session's fetches, so this specific linking claim is carried as GT-7? rather than folded into the fully-verified GT-6) → therefore the failure is a transport-layer rejection, not an application bug — the primitive bottoms out at a protocol definition (GT-6) plus a near-universally-documented client behavior (GT-7?, flagged). This feeds Ground Truths GT-6/GT-7? and is **not** load-bearing for the mechanism-choice conclusion below (C1–C5 never cite GT-7? on their heads).

**Trade-off matrix (Phase 4), options B = ACME-capable reverse proxy (Caddy/Traefik) vs. C = certbot + existing webserver + systemd timer/cron + deploy-hook + independent monitoring**, with D = manual/status-quo renewal knocked out by the must-have "removes the human-triggered renewal step" (FAIL — that's the outage cause the user names), and A = managed-provider (LB/CDN) auto-renewal excluded from scoring as not a like-for-like alternative (see Abandoned Reasoning, Dead End 3) and instead handled as a precondition check (Chain C2):

| Criterion (anchor: 1 = worst, 5 = best) | Weight | B score | C score |
|---|---|---|---|
| Setup speed for a fresh self-hosted deployment | 4 | 5 | 2 |
| Silent-failure surface (does renewal-success ⇒ live listener, or are they separable?) | 5 | 5 | 2 |
| Fit with an existing, hard-to-replace webserver | 3 | 1 | 5 |
| Challenge-type/plugin flexibility (http-01 + dns-01) | 3 | 4 | 5 |
| Operational maturity / production track record | 2 | 4 | 5 |

Weighted totals: **B = 4·5+5·5+3·1+3·4+2·4 = 68**; **C = 4·2+5·2+3·5+3·5+2·5 = 58**. B wins by 10.

**Flip test:** solving weight·(B−C)-sum = 0 per criterion, the smallest single-weight move that flips the winner is on the silent-failure-surface criterion: it would have to drop from weight 5 to below 5/3≈1.67 (i.e., to weight 1) before C overtakes B (at w=1: B=43, C=48). Every other criterion, even pushed to the scale's maximum (5), fails to flip the result (checked: criterion 3 at weight 5 still leaves B=70 > C=68). **No single plausible weight change flips this** — the one lever that could is exactly the criterion the user's own stated concern ("expired certificate breaks client connections") says should be weighted *highest*, not lowest.

**Second-order extension (mandatory pass), on the recommendation to adopt B:**
- *Actor lens:* the operator now has one standing process to watch instead of a cron script to watch (a smaller monitoring problem, not zero); a DNS provider (if DNS-01 is used) now holds a standing, credentialed, machine-writable relationship with the ACME client — that credential becomes its own expiry/rotation/security risk; the CA (Let's Encrypt) sees continuous automated retries rather than sporadic manual renewals, which interacts with published rate limits; an adversary gains a brief additional exposure window only during the edge-process migration itself.
- *Time lens:* immediately, B is faster to reach a first working state (setup-speed criterion); after several renewal cycles (a 90-day cert renews 3-4×/year), C's hook/timer has had that many silent chances to break with B having had zero, because the seam doesn't exist; over a multi-year horizon, C's deploy-hook script is exactly the kind of artifact a future engineer "cleans up" during an unrelated refactor, a risk B's architecture has no analog for.

No extension effect contradicts a ground truth; both effects are carried into the Conclusion's trade-offs rather than hidden.

**Theoretical-limit + estimate (Phase 4), on "is calendar margin the bottleneck?":** governing constraint is the CA-imposed certificate lifetime (GT-2: 90 days default, 6 days opt-in short-lived) bounding how much slack any renewal cadence can provide. **Ideal ceiling** (direction: more days of slack is better): continuous in-process automation (GT-5) against a 90-day cert. **Best demonstrated:** certbot's own documented trigger — ready for renewal at <1/3 lifetime remaining (GT-4) ≈ 30 days of slack on a 90-day cert, i.e., already close to the ceiling *when it fires and lands*. **Fermi bracket** of the realistic detect-and-fix window a monitoring alert would need: (alert-response latency 0.5–3 days) + (fix-and-redeploy time 0.5–1 day), × a 2.5–3 retry-cycle safety multiplier ⇒ **[2.5, 12] days**. Recomputed: low = (0.5+0.5)×2.5 = 2.5; high = (3+1)×3 = 12. Certbot's ~30-day trigger clears even the 12-day conservative bound with room to spare. **Conventional-in-practice figure** (naive, unmonitored cron): effectively 0 days, because a silently-broken timer or an un-fired reload (documented failure mode) converts the nominal 30-day margin into the same outcome as no automation at all. **Gap 1** (conventional → best demonstrated) is closeable by configuration alone (fix the hook, verify the timer). **Gap 2** (best demonstrated → ideal ceiling) is closeable only by removing the seam architecturally (adopting B) — no amount of correct cron configuration reaches it, because the seam is structural to C, not a configuration defect.

---

## 1. Problem Essence

**Core problem:** Given that no verified TLS-terminating surface exists in this repository to ground the analysis locally, the irreducible question is: what mechanism eliminates — architecturally, not merely procedurally — the gap between "a renewal was attempted" and "a client-facing listener is actually serving a non-expired certificate," since that gap (not insufficient calendar margin) is what turns "automated renewal" into an outage anyway.

**Success criteria:**
1. The Conclusion names a specific mechanism per infrastructure topology (managed edge / self-hosted-replaceable edge / self-hosted-fixed edge) and states, for each, why it closes the renewal-success-to-live-listener gap rather than merely automating the CA-facing half of it.
2. The Conclusion states the concrete numbers (certificate lifetime, renewal-trigger threshold, realistic fix-window bracket) that make "fastest" a measured claim rather than a vibe.
3. The Conclusion explicitly discloses that this repository has no TLS surface, so nothing here is a verified fix to observed local infrastructure.
4. The Conclusion names at least one trade-off the recommended mechanism does not remove (a residual risk), per the second-order pass and pre-mortem.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A-1: "Our TLS setup" refers to infrastructure inside this git repository | untested belief | verify or flag | Discard — contradicted directly by GT-1 | GT-1 (this analysis's own scan) |
| A-2: "Fastest path" means fastest-to-initially-set-up, not fewest silent-failure modes | convention | challenge before use | Challenge — the user's own sentence pairs "fastest" with preventing an outage, a reliability goal, so "fastest" is read as "fewest moving parts likely to silently fail" | the user's stated framing itself |
| A-3: Once configured, a renewal automation loop (cron/timer) needs no further attention to keep firing indefinitely | untested belief | verify or flag | Challenge — accepted only as a bounded premise inside chain C3, not as a standalone fact | unverified — flagged |
| A-4: An ACME CA (e.g. Let's Encrypt) is a usable CA for the reader's actual service | current constraint | record expiry | Accept — expires if the service is not publicly HTTP-reachable, has no automatable DNS, or falls under a policy requiring a private/enterprise CA | conditional acceptance; not tested against any real service (none exists here, GT-1) |
| A-5: http-01 challenge validation requires port 80 publicly reachable at renewal time | physical/protocol fact | accept as ground-truth candidate | Accept — backed by GT-3 (RFC 8555 §8.3) | RFC 8555 §8.3, folded into GT-3 |
| A-6: dns-01 challenge validation requires giving the ACME client write access to the authoritative DNS zone | physical/protocol fact | accept as ground-truth candidate | Accept — backed by GT-3 (RFC 8555 §8.4) | RFC 8555 §8.4, folded into GT-3 |
| A-7: If TLS terminates at a managed load balancer/CDN with the provider's native cert service, renewal is already solved without any ACME client | current constraint | record expiry | Accept — backed by GT-8; expires if the topology moves off that managed edge | GT-8 (AWS ACM docs) |
| A-8: A certbot renewal that succeeds at the CA level also guarantees the running webserver reloads the new certificate | untested belief | verify or flag | Challenge — this is the documented reason `--deploy-hook` exists at all; not automatically true | unverified — flagged; motivates chain C3's mandatory hook+monitoring bundle, and Abandoned Reasoning Dead End 2 |
| A-9: Automated renewal, once running, needs no independent monitoring/alerting to be trustworthy | convention | challenge before use | Discard — contradicted by A-3/A-8 and by the pre-mortem's Cluster C finding | contradicted by A-3, A-8, and the adversarial pass below |
| A-10: Other managed LB/CDN providers (Cloudflare, GCP LB, etc.) offer equivalent auto-renewal behavior to AWS ACM's documented managed renewal | untested belief | verify or flag | Challenge — only AWS ACM's specific behavior was read at source (GT-8); generalizing to other providers is unread | unverified — flagged; `[Assumes: A-10]` on chain C2 |

---

## 3. Ground Truths

- **GT-1** No Dockerfile, docker-compose file, nginx/caddy/traefik configuration, or ACME/certbot/letsencrypt reference exists anywhere in this repository's tracked files; the only keyword hits are unrelated false positives — source: direct `grep -rniE` + `find` scan of the working tree, run by this analysis in this session; read-at-source: the command output quoted in the ground-truth check above (no matching infra files found).
- **GT-2** Let's Encrypt's default issued certificates are valid for 90 days; subscribers may opt into short-lived certificates valid for 6 days — source: Let's Encrypt FAQ (letsencrypt.org/docs/faq/); read-at-source: quoted text "Our default certificates are valid for 90 days" / "short-lived certificates which are valid for six days."
- **GT-3** RFC 8555 ("Automatic Certificate Management Environment," Proposed Standard, March 2019) defines the ACME protocol for automated issuance/validation/renewal and defines two domain-validation challenge types: http-01 (§8.3) and dns-01 (§8.4) — source: RFC 8555 (datatracker.ietf.org); read-at-source: section titles and defining text quoted above.
- **GT-4** Certbot (as of 4.0.0) treats a certificate as ready for renewal when less than 1/3 of its lifetime remains (prior versions used a fixed 30-day threshold), and its documented automation recipe is a twice-daily cron/systemd-timer call to `certbot renew`, a no-op unless the threshold is crossed — source: Certbot docs (eff-certbot.readthedocs.io/en/stable/using.html); read-at-source: quoted renewal-threshold and cron-recipe text above.
- **GT-5** Caddy's "automatic HTTPS" obtains and renews ACME certificates and swaps them into the live TLS listener entirely in-process and in the background, with no separate cron job, restart, or reload hook required — source: Caddy docs (caddyserver.com/docs/automatic-https); read-at-source: quoted text above ("no downtime, extra configuration, or separate tooling is required").
- **GT-6** RFC 5280 §4.1.2.5 defines a certificate's validity period as the inclusive interval from `notBefore` through `notAfter` — source: RFC 5280 (rfc-editor.org/rfc/rfc5280.txt); read-at-source: §4.1.2.5, quoted above.
- **GT-7?** TLS/X.509 path-validation implementations reject (fail the handshake for) a certificate whose current time falls outside its `notBefore`/`notAfter` window — unverified: the specific algorithmic clause of RFC 5280 §6.1.3 was summarized, not quoted verbatim, in this session's fetches; the claim is standard, uncontested engineering fact but is carried with the `?` on principle rather than overclaimed, and it feeds only the motivational Five-Whys framing above, not any numbered chain's head.
- **GT-8** AWS Certificate Manager provides automatic "managed renewal" for certificates that are DNS-validated and associated with an AWS service (e.g., ELB, CloudFront); ACME-issued certificates are explicitly excluded from this managed renewal, which is instead the responsibility of the ACME client — source: AWS ACM docs (docs.aws.amazon.com/acm/latest/userguide/managed-renewal.html); read-at-source: quoted eligibility list and the "Certificates issued through ACME certificate automation are not eligible for ACM managed renewal" note.

**Provenance summary:** `?`-marked: GT-7 (1 of 8). Read-at-source: GT-1 — this session's own grep/find output; GT-2 — letsencrypt.org FAQ, "90 days"/"six days" sentences; GT-3 — RFC 8555 §8.3/§8.4 titles and text; GT-4 — Certbot docs, renewal-threshold and cron-recipe text; GT-5 — Caddy docs, automatic-HTTPS description; GT-6 — RFC 5280 §4.1.2.5; GT-8 — AWS ACM managed-renewal page, eligibility list and ACME-exclusion note.

---

## 4. Derivation Chains

### Conclusion C1: Where you control the TLS-terminating edge process, adopt an ACME-capable reverse proxy (Caddy or Traefik) rather than certbot + a traditional webserver

GT-4 (certbot's renewal-readiness is a CA-side event only) + GT-5 (Caddy's renewal is an in-process CA-side-and-listener-side single event)
→ certbot-style automation can succeed at the CA level while never reaching the live listener, whereas Caddy's automatic-HTTPS architecture has no such separable step for that failure to hide in
→ the weighted trade-off across setup speed, silent-failure surface, fit with an existing webserver, challenge-type flexibility, and operational maturity totals B (ACME-proxy) = 68 versus C (certbot+webserver) = 58, driven by the silent-failure-surface criterion (weight 5) and the setup-speed criterion (weight 4)
→ recommend adopting an ACME-capable reverse proxy as the fastest reliable path whenever the reader controls the TLS-terminating edge process
→[2nd] adopting this typically means replacing whatever currently terminates TLS, concentrating migration risk into a single cutover window
→[3rd] choosing dns-01 for wildcard or internal-only coverage trades the just-removed cert-expiry risk for a smaller, less-monitored DNS-API-credential rotation/security risk

**Pre-check:** head GT-4, GT-5 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every head input is unsuffixed and read-at-source; the weighted-total arithmetic recomputes independently (68 vs 58, verified above); the strongest rival — "prefer C anyway for its greater plugin maturity" — is named and ruled out by the flip test within this same chain's own arithmetic: flipping the winner requires dropping the silent-failure-surface weight from 5 to 1, an implausible re-weighting given that failure mode is exactly what the user's stated concern names.

### Conclusion C2: If TLS already terminates at a managed load balancer/CDN using that provider's native certificate service, verify eligibility rather than build any new automation

GT-8 (ACM managed renewal is automatic for DNS-validated, service-associated certs, and explicitly excludes ACME-issued certs)
→ if the edge is already a managed LB/CDN using the provider's own certificate service (not an ACME-issued cert layered on top), renewal is already automatic, and adding ACME automation on top would create a second, non-eligible, potentially conflicting renewal path *[Assumes: A-10 — that other major providers behave like AWS ACM; if false for the reader's specific provider, the recommended action — verify eligibility before assuming coverage — is unchanged, only the expected verification result would differ]*
→ the correct action in that case is to verify eligibility (association + validation method) rather than build anything new

**Pre-check:** head GT-8 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — GT-8 is unsuffixed and read-at-source; the `[Assumes: A-10]` hop is priced per the HIGH exception clause (the endpoint, "verify eligibility," still stands even if A-10 fails for a given provider); the rival — "layer ACME on top for defense-in-depth" — is named and ruled out directly by GT-8's own text, which states ACME-issued certs are not eligible for ACM's managed renewal, making the layered cert strictly redundant rather than additive protection.

### Conclusion C3: If the edge process cannot be replaced, use certbot on a timer with both a deploy-hook and an independent, end-to-end-tested monitoring backstop — never certbot's renewal success alone

GT-4 (certbot's documented timer-based renewal recipe) + C1 (the architectural-seam finding: renewal-success and going-live are separable events in a certbot-style setup)
→ when the existing webserver cannot be replaced, ruling out C1's recommended mechanism, certbot's own documented automation still leaves the renewal-success-to-live-listener seam open
→ closing that seam requires pairing the timer with an explicit `--deploy-hook` (to force reload atomically with renewal) and an independent expiry-monitoring alert as backstop *[Assumes: A-3 — that the timer itself keeps firing indefinitely without silent failure; if false, the hook never runs at all, and only the independent monitoring check — not the hook — catches it, so the endpoint still recommends bundling both]*
→ recommend certbot + timer + deploy-hook + independently-tested monitoring as the correct, not merely the fastest, path only under this precondition

**Pre-check:** head GT-4, C1 (HIGH) · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** MEDIUM — Inputs and Rivals are clean (the rival "hook alone, no separate monitoring" is ruled out by Abandoned Reasoning Dead End 2), but the Inference axis carries a residual the `[Assumes: A-3]` exception only partially covers: the pre-mortem below (Cluster C) shows the monitoring backstop itself can exist without ever reaching a human, an unpriced "who watches the watcher" gap. Closes when the monitoring path has been end-to-end tested at least once (a synthetic low-threshold or staging trigger confirmed to actually page someone) — until then this chain stays MEDIUM.

### Conclusion C4: Calendar margin is not the bottleneck in automated-renewal failures; the renewal-success-to-live-listener seam is

GT-2 (Let's Encrypt cert lifetimes: 90-day default / 6-day opt-in) + GT-4 (certbot's <1/3-lifetime-remaining trigger, ≈30 days of margin on a 90-day cert)
→ the calendar margin a correctly-firing trigger provides (≈30 days) is roughly 2.5×–12× the realistic detect-and-fix window a monitoring alert would need, per a Fermi bracket of [2.5, 12] days built from alert-response latency, fix time, and a retry-cycle safety multiplier
→ therefore the bottleneck in real-world renewal failures is whether the trigger fires and reaches the live listener at all, not whether there is enough calendar time — confirming chain C1's architectural finding rather than a separate concern
→ moving toward shorter-lived certificates (GT-2's 6-day option) only becomes safe once that seam is already eliminated, since a 6-day lifetime leaves far less absolute slack for a human-in-the-loop fix cycle

**Pre-check:** head GT-2, GT-4 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — both head inputs are unsuffixed and read-at-source; the Fermi bracket recomputes independently (low = (0.5+0.5)×2.5 = 2.5; high = (3+1)×3 = 12); the rival — "checking renewal status more frequently than twice daily would meaningfully help" — is named and ruled out by the same bracket, since certbot's cadence (GT-4) already checks far more often than the 2.5–12 day window requires.

### Conclusion C5: None of the above mechanism choices apply to anything that exists in this repository today

GT-1 (no TLS-terminating process, certificate, or deploy pipeline exists in this repository's tracked tree)
→ chains C1, C2, and C3 have no target here to attach to, because there is no component in first-principles-skill for any of them to automate
→ this analysis is general infrastructure guidance the reader can apply to whatever actual service prompted the question, not a verified fix to something observed in first-principles-skill

**Pre-check:** head GT-1 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — Inputs and Inference are clean (GT-1 is a direct, read-at-source negative finding; both hops are direct deductions from it), but the Rivals axis is short and not fully settleable from here: a rival reading — "the TLS surface exists outside the tracked tree, in a separate deployment repo, or the reader means a different project entirely" — is live and this analysis cannot rule it out from inside this repository alone. What would close it: the reader names the actual service/repository they mean, or that system is scanned directly the same way this one was.

**Unverified input rule (D-07):** no chain above carries a `GT-N?` head input (GT-7? is deliberately never head-cited), so D-07's mandatory-downgrade clause is not triggered by any chain; C3 and C5 are MEDIUM for the Inference/Rivals reasons stated on their own lines, not for an unverified-input reason.

---

## 5. Abandoned Reasoning

### Dead End: A single universal recommendation ("always use Caddy") with no topology branching

**What was tried:** Considered giving one mechanism as the answer regardless of context.
**Why abandoned:** Contradicted by GT-8 and A-7 — GT-8's own text states ACME-issued certificates are explicitly *not* eligible for ACM's managed renewal, so recommending an ACME proxy to someone already behind a managed LB/CDN with a native, DNS-validated certificate would add a redundant, competing renewal path rather than solving anything.
**What it ruled out:** Any single-mechanism universal answer; establishes that the first step must always be "identify what already terminates TLS today," which is exactly Chain C2.

### Dead End: Scoring bare certbot (no deploy-hook, no monitoring) as a real contender

**What was tried:** Considered scoring option C as "certbot + cron" alone, matching the most common way it is actually documented and deployed in the wild.
**Why abandoned:** A-8 shows renewal success and "the cert is live" are separable events under this architecture; without an explicit hook and independent monitoring this is the exact absent-fails situation for the user's stated goal — "automated" in name while still reproducing the outage it was built to prevent.
**What it ruled out:** Treating bare certbot as a legitimate contender in the trade-off matrix; C is only defined, and only scored, as certbot-plus-hook-plus-monitoring for this reason.

### Dead End: Scoring managed-provider auto-renewal (A) against B and C on the same weighted criteria

**What was tried:** Considered adding managed-LB/CDN auto-renewal as a fourth row in the trade-off matrix.
**Why abandoned:** A is not a mechanism you adopt independently to solve a renewal problem — it is an emergent property of a much larger, unrelated infrastructure choice (which edge/LB/CDN to run), and GT-8's own conditional eligibility carve-outs (excludes ACME-issued, imported, and private-CA-API-issued certs) mean it doesn't fit a clean weighted score against B/C in the first place.
**What it ruled out:** A four-way matrix that would have conflated "which edge topology to run" with "given I terminate TLS myself, how do I automate renewal"; replaced by the precondition check in Chain C2, applied before the B-vs-C trade-off.

---

## 6. Conclusion

**Recommended approach — a three-step decision procedure, in this order:**
1. Check first whether TLS already terminates at a managed load balancer/CDN using that provider's own certificate service — if so, verify renewal eligibility rather than building anything (chain C2).
2. If you control the TLS-terminating edge process, adopt an ACME-capable reverse proxy such as Caddy or Traefik — it collapses issuance, renewal, and going-live into one in-process event with no cron job or reload hook to maintain or forget (chain C1).
3. Only if an existing, hard-to-replace webserver must stay in place, run certbot on a systemd timer/cron job with an explicit `--deploy-hook` **and** an independently, end-to-end-tested expiry-monitoring alert — never certbot's renewal success by itself (chain C3).

**Key insight:** The failure mode behind "we had automated renewal and the cert still expired" is essentially never insufficient calendar margin — even a naive 30-day trigger clears a realistic 2.5–12 day detect-and-fix window by a wide margin (chain C4). It is whether "a renewal was attempted" and "a client is served a valid certificate" are the same event or two events that can silently diverge. Reasoning by convention says "install certbot and a cron job"; that convention treats CA-side renewal success as the finish line, when the actual finish line — a client not seeing an expired certificate — sits one seam further downstream, and only an architecture with no seam (chain C1) or an explicitly-verified backstop closing that seam (chain C3) actually reaches it (chain C1).

**Trade-offs acknowledged:** Choosing the ACME-proxy path usually means replacing whatever currently terminates TLS, not adding to it — a real migration cost, not a drop-in change (chain C1). Using dns-01 challenges for wildcard or internal-only coverage trades the cert-expiry risk just removed for a smaller, less-monitored DNS-API-credential rotation/security risk (chain C1). Even the recommended fallback mechanism (chain C3) still depends on a monitoring backstop that must itself be verified to actually reach a human — an unpriced residual this analysis names but does not fully close (chain C3). None of this is verified against a real system, because none exists in this repository (chain C5) — if the service you actually mean has a different topology than the three branches above, that branch, not this whole conclusion, is what to re-check.

**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (MEDIUM), C4 (HIGH), C5 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the recommended approach and key insight rest on C1/C2/C4, all HIGH; but the overall rating is capped by C3 (MEDIUM: the monitoring-backstop's own unverified-until-tested residual) and by C5 (MEDIUM: this analysis cannot rule out that the reader means a different, unscanned system). Both caps are explained on their own §4 confidence lines and are not re-explained here. Closing C3 requires end-to-end testing the monitoring path once; closing C5 requires naming or scanning the actual system in question.

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | architectural distinction (seam exists in certbot-style, not in Caddy) | none | n/a |
| C1 | 2 | weighted totals 68 vs 58 | none | n/a |
| C1 | 3 | recommend B | none | n/a |
| C1 | 2nd | cutover/migration risk | none (direct consequence of C1's own criterion-3 score) | n/a |
| C1 | 3rd | DNS-credential risk on dns-01 | none (stated as an explicit conditional, not a hidden premise) | n/a |
| C2 | 1 | already-automatic if managed LB/CDN, unless ACME-layered | A-10 | yes |
| C2 | 2 | verify eligibility rather than build | none | n/a |
| C3 | 1 | seam still open under certbot | none | n/a |
| C3 | 2 | close seam via hook + monitoring | A-3 (already in table) | yes (referencing existing row) |
| C3 | 3 | recommend under precondition | none | n/a |
| C4 | 1 | margin bracket [2.5, 12] days | none | n/a |
| C4 | 2 | bottleneck isn't margin | none | n/a |
| C4 | 3 | short-lived certs need seamless architecture | none | n/a |
| C5 | 1 | no target here for C1/C2/C3 | none | n/a |
| C5 | 2 | general-guidance disclosure | none | n/a |

Scan complete: 15 rows across 5 chains (including C1's two second-order steps), in order; 2 assumptions surfaced (A-10, A-3-reference), both added/referenced in the Assumptions Table.

---

## Adversarial pass (process output)

**Recompute.** B = 4·5+5·5+3·1+3·4+2·4 = 20+25+3+12+8 = **68** ✓. C = 4·2+5·2+3·5+3·5+2·5 = 8+10+15+15+10 = **58** ✓. Flip threshold on criterion 2's weight: 43+5w=48+2w ⇒ w=5/3≈1.667 ✓. Fermi bracket: low=(0.5+0.5)×2.5=2.5 ✓; high=(3+1)×3=12 ✓. All four recompute cleanly.

**Sensitivity.** The single ground truth whose falsity would most flip the headline conclusion is **GT-5** (Caddy's claimed hook-free, in-process renewal+swap): if false, the silent-failure-surface gap (5 vs 2) collapses and, per the flip-test math, C overtakes B. GT-5 is not `?`-marked — it is read-at-source from Caddy's own documentation — so this is a real but currently well-grounded sensitivity, not an open unverified risk. Weakest link per chain: C1 — the silent-failure-surface criterion's score gap; C2 — A-10's cross-provider generalization; C3 — the monitoring-watches-the-watcher residual; C4 — none material (both bracket endpoints are conservative by construction); C5 — the unruled-out "different system" rival.

**Rival.** Headline: "prefer C for plugin maturity" — ruled out on C1's own line via the flip test. C2: "layer ACME on top for defense-in-depth" — ruled out by GT-8's explicit exclusion text. C4: "check more frequently than twice daily" — ruled out by the same Fermi bracket. C5: "the TLS surface exists outside the tracked tree, or you mean a different project" — **live, not ruled out**; carried as C5's MEDIUM band and as an explicit Conclusion caveat.

**Premise.** This renewal-automation plan has already failed — an expired certificate broke client connections despite "automated renewal" nominally being in place. What caused it?

**Causes** (unfiltered, from the implementer, the on-call/ops person, whoever pays for it, and an adversary):
1. (implementer) The deploy-hook script silently broke during an unrelated OS/package upgrade that changed the webserver's reload syntax.
2. (implementer) DNS-01 API credentials rotated or expired independently of the TLS cert, breaking the challenge with no alert distinguishing that from a network blip.
3. (ops/on-call) The monitoring backstop exists on a dashboard but was never wired to actually page anyone.
4. (ops/on-call) The renewal automation ran on a host that was decommissioned/replaced without the timer being migrated along with it.
5. (whoever pays for it) Consolidation moved services onto a new host; the person who understood the original renewal setup left; no documentation existed.
6. (adversary) An attacker with DNS-zone or ACME-account access interferes with a pending order to force an outage or substitute their own certificate.
7. (implementer) A retry-storm bug tripped the CA's rate limit right as the real cert approached expiry, blocking renewal for the cooldown window.
8. (ops/on-call) Host clock drift caused the client to mistime the renewal check.
9. (implementer) A later migration away from Caddy/Traefik for unrelated reasons silently dropped "automatic HTTPS," reverting to a manually-managed cert without anyone flagging it as renewal-relevant.

**Clusters:**
- **A — Silent infrastructure drift** (causes 1, 4, 8, 9): bears on C1's architectural-seam finding and its [3rd]-order migration-risk extension.
- **B — Credential/identity lifecycle separate from cert lifecycle** (causes 2, 6, 7): bears on C1's [3rd]-order DNS-credential finding and A-6.
- **C — Monitoring exists but doesn't reach a human** (cause 3): bears directly on C3 and its `[Assumes: A-3]` hop — the cluster that most threatens the plan's core defense.
- **D — Institutional knowledge loss** (cause 5): bears on the plan's durability over C1's time-lens horizon.

**Disposition:**
- Cluster A: named plan change — the hook/timer definitions live in the same infrastructure-as-code pipeline as the webserver config, so a host migration that drops them is a visible diff, not a silent gap; tripwire — export "last successful renewal check" as a metric with a staleness alert (e.g., none in >7 days), owned by the deploy pipeline.
- Cluster B: explicitly accepted risk, named mitigation — use a scoped, dedicated API token for ACME DNS challenges only, and alert on rate-limit errors as a distinct class from generic renewal failure.
- Cluster C: named plan change — the monitoring backstop is not verified until it has actually paged a human at least once (a synthetic low threshold or staging test); this directly grounds C3's MEDIUM band above.
- Cluster D: explicitly accepted risk, named mitigation — document which mechanism was chosen and why in the same place other on-call runbooks live.

**Falsification.** This analysis's headline recommendation is false if an ACME-capable reverse proxy is shown to actually require an external reload/cron step after all (falsifying GT-5), or if a correctly-configured, end-to-end-tested certbot+hook+monitoring setup is shown to have an equal or lower real-world failure rate than an ACME-proxy setup in comparable production use.

---

## §6→§4 closure ledger (process output)

- "Check first whether TLS already terminates at a managed load balancer/CDN..." → chain C2 ✓
- "If you control the TLS-terminating edge process, adopt an ACME-capable reverse proxy..." → chain C1 ✓
- "Only if an existing, hard-to-replace webserver must stay in place, run certbot..." → chain C3 ✓
- "The failure mode behind 'we had automated renewal and the cert still expired' is essentially never insufficient calendar margin..." → chain C4 ✓
- "...only an architecture with no seam (chain C1) or an explicitly-verified backstop closing that seam (chain C3) actually reaches it" → chains C1, C3 ✓ (inline)
- "Choosing the ACME-proxy path usually means replacing whatever currently terminates TLS..." → chain C1 ✓ (inline)
- "Using dns-01 challenges... trades the cert-expiry risk just removed for a smaller... DNS-API-credential... risk" → chain C1 ✓ (inline)
- "Even the recommended fallback mechanism (chain C3) still depends on a monitoring backstop..." → chain C3 ✓ (inline)
- "None of this is verified against a real system, because none exists in this repository (chain C5)" → chain C5 ✓ (inline)
- "**Confidence:** MEDIUM — ...capped by C3... and by C5..." → chains C3, C5 ✓ (inline)

All ten §6 claims trace inline; no CUT rows.

---

## Techniques not applied (process output)

- fishbone — not applicable — the assumption space (managed-edge / self-hosted-replaceable-edge / self-hosted-fixed-edge) was directly enumerable from the ground truths without needing a category brainstorm.
- inversion (Phase 2 point) — not applicable — the assumption set was not suspiciously thin; each was addressed directly by classification and the trade-off's own must-have knockout.
- inversion (Phase 5 point) — not applicable — the conclusion is a plan/recommendation, not a bare claim, so the decision rule routes the adversarial pass to pre-mortem instead, which ran above.
- theoretical-limit (Phase 1 point) — not applicable — the Essence Statement doesn't hinge on whether a single stated figure is a mere convention versus a hard bound; it turns on mechanism choice, not on relaxing a numeric convention. (Theoretical-limit's Phase 4 point *did* fire, as chain C4.)

---

## Self-audit scan (process output)

**Table 1 — chain form:**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-4 + GT-5 | yes | n/a | yes | HIGH | yes | none |
| C2 | GT-8 | yes | n/a | yes | HIGH | yes | none |
| C3 | GT-4 + C1 | yes | n/a | yes | MEDIUM | yes | none |
| C4 | GT-2 + GT-4 | yes | n/a | yes | HIGH | yes | none |
| C5 | GT-1 | yes | n/a | yes | MEDIUM | yes | none |

**Table 2 — claim inventory (§6):**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach — a three-step decision procedure, in this order:" | bold lead-in | no | section-intro label: whole-line colon span, no citation of its own | n/a |
| list item 1 (managed LB/CDN check) | list item | yes | closes own sentence, >40 chars | C2 |
| list item 2 (adopt ACME proxy) | list item | yes | closes own sentence, >40 chars | C1 |
| list item 3 (certbot fallback) | list item | yes | closes own sentence, >40 chars | C3 |
| "Key insight:" span | bold lead-in | yes | colon closes bold span, carries assertion on same line | C4, C1 |
| "Trade-offs acknowledged:" span | bold lead-in | yes | colon closes bold span, carries assertion; caveats each cite inline | C1, C1, C3, C5 |
| "Pre-check:" line | prose | no | fenced-adjacent structural line, not a bold-colon lead-in or list item | n/a |
| "Confidence:" span | bold lead-in | yes | colon closes bold span | C1, C2, C3, C4, C5 |

**Reconciliation:** Scan complete: 5 chain rows, one per section-4 chain block in order; 8 section-6 rows, one per construct in order — 6 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced.

---

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "the irreducible question is: what mechanism eliminates — architecturally, not merely procedurally — the gap between 'a renewal was attempted' and 'a client-facing listener is actually serving a non-expired certificate'..."
Band: **Rigorous**
Justification: names the core question (the renewal-success/live-listener gap), not the triggering event ("our TLS setup") or a restatement of the prompt; each success criterion is a checkable verb+subject+outcome triplet scannable against the Conclusion.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "C2 | 1 | already-automatic if managed LB/CDN, unless ACME-layered | A-10 | yes" and Assumptions Table row A-8: "Challenge — this is the documented reason `--deploy-hook` exists at all; not automatically true | unverified — flagged"
Band: **Rigorous**
Justification: all rows use the four-type scheme with token-first, em-dash verdicts; at least three assumptions are challenged/discarded (not merely Accepted); the end-of-phase audit ran exhaustively over all named chain steps and surfaced A-10, recorded in the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-7 (1 of 8)." — checked against the list: GT-7 is the only entry carrying `?`; all others (GT-1–GT-6, GT-8) are unsuffixed with named read-at-source locations.
Band: **Rigorous**
Justification: every GT has a stable ID matching chain references, a specific (non-"common knowledge") citation, a provenance label, and the enumeration matches the list on inspection; every unsuffixed GT feeding a HIGH chain (GT-1, GT-2, GT-4, GT-5, GT-8) names its read-at-source location; no Phase-2-discarded assumption appears here.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, Table 1): all five rows read "Form conforming? = yes ... Dependency clean? = yes"; Abandoned Reasoning carries three dead ends each with What-was-tried/Why-abandoned/What-it-ruled-out.
Band: **Rigorous**
Justification: every conclusion has exactly one chain, each with named head inputs, at least one genuine intermediate, arrow-led one-hop-per-line form, no hop leading with a `GT-N` identifier, no analogy used as unsourced direct evidence, and both surfaced assumptions declared inline via `[Assumes: X]`.

**Criterion 5: Validate**
Quoted span: "C3 ... Confidence: MEDIUM — Inputs and Rivals are clean... but the Inference axis carries a residual the `[Assumes: A-3]` exception only partially covers... Closes when the monitoring path has been end-to-end tested at least once."
Band: **Rigorous**
Justification: every chain's weakest link is named with a specific closing condition (not a generic "some uncertainty remains"); no chain with a `GT-N?` head input is rated HIGH; C3 is rated no higher than C1 (its own head citation, HIGH) permits and is itself independently capped by its own axes; the adversarial pass (pre-mortem, run above) is complete with all parts present and every cluster carrying a named disposition.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, Table 2): 6 of 8 constructs scored "Claim under R11? = yes," each with a "Chain cited" entry naming C1–C5; the closure ledger's 10 rows all resolve inline with no CUT.
Band: **Rigorous**
Justification: every Conclusion-section claim traces to a specific named §4 chain with no new reasoning introduced in §6; the Key Insight ("the bottleneck is the seam, not the margin") is a non-obvious finding distinct from the recommended approach itself, not a restatement of it.

**Gate result:** No criterion Absent; zero criteria Hand-wavy (all six Rigorous). Both clearing conditions met — the analysis clears the gate with no re-perception pass required.