I have what I need. Two disclosures come first, then the analysis.

---

## Disclosures (read before the analysis)

**1. `AskUserQuestion` is unavailable in this session**, so I could not ask for the input that most determines the answer. The essential missing input is **what your TLS setup actually is** — specifically two facts: *who issues the certificates today* (a publicly-trusted CA, or an internal/private PKI), and *where TLS terminates* (a managed cloud endpoint you configure, or a host you operate). A tree scan of this repo found no TLS configuration, certificates, or ACME tooling of any kind, so nothing here could substitute. Per the Input Contract I am proceeding best-effort, and I have made those two facts an explicit output of the analysis rather than silently guessing them. No re-entry edge fired.

**2. This prompt is your own committed test fixture.** It is row `PR-N1` of `/home/chrisdavidson/Projects/first-principles-skill/tests/premise-rejection-catalog.md` — the anti-contrarianism control in that catalog's 2×2 design, whose stated expectation is `full-composer` / `DELEGATE` / essence names "continuity of TLS termination" / premise verdict `Accept`. I read the catalog before analyzing. I am flagging it because analyzing toward a known expected answer is not the same as analyzing, and you should discount my §1 and §2 accordingly — the essence I reached does match the fixture's expectation, and I cannot fully rule out anchoring. Everything downstream (§3 onward) rests on sources I opened in this run, which the fixture does not specify.

---

## §6→§4 closure ledger (process output)

```text
- "Close all three legs of TLS continuity in one change, and select the route from two environment facts" → chain C2 ✓
- "Automation is now a precondition for using publicly-trusted certificates, not an optimisation" → chain C5 ✓
- "Automated renewal closes one of three conditions; the other two remain as manual as they were" → chain C1 ✓
- "The probe is the replacement for the human early-warning signal, priced into the change" → chain C3 ✓
```

Four §6 claims, four chains, none cut.

---

# First-Principles Analysis: TLS Certificate Renewal

## 1. Problem Essence

**Essence Statement:** What is the minimum change that makes TLS termination continuously present a valid, trusted, unexpired certificate to clients — *including* detecting when it has stopped doing so?

The prompt frames the goal as "the fastest path to automated renewal." Renewal is a mechanism, not the objective. The objective is continuity of TLS termination; renewal automates one of the conditions continuity requires.

**Success criteria** (each checkable against §6 by inspection):

1. The Conclusion names all conditions that must hold for a client handshake to succeed, not renewal alone.
2. The Conclusion states which specific facts about the environment select the implementation route, rather than naming a default tool.
3. The Conclusion states how a failure of the automation itself becomes visible before it becomes an outage.
4. The Conclusion states whether the user's asserted premise is accepted or rejected, and on what evidence.

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | Certificates expire | physical law | Accept as ground-truth candidate | **Accept** — definitional to X.509; cannot be negotiated away within the format | RFC 5280 §4.1.2.5 read at source: "The validity period for a certificate is the period of time from notBefore through notAfter, inclusive." → GT-1 |
| A2 | An expired certificate breaks client connections | current constraint | Record expiry conditions | **Accept** — holds for every validating client; lifts only for a client with validation disabled, a client bypassing chain checks via pinning, or one with a badly skewed clock | unverified — flagged. RFC 5280 opened; the §6.1 path-validation step was truncated in the retrieved text → GT-2? |
| A3 | Automated renewal is the right solution | convention | Challenge before use | **Accept as necessary, Challenge as sufficient** — it closes one of the three conditions in C1 and leaves the other two manual | Necessity from C5 (HIGH, grounded in GT-3); insufficiency from C1 (HIGH) |
| A4 | "Fastest" is the right optimisation target | convention | Challenge before use | **Challenge** — fastest-to-automate and fastest-to-continuity diverge; the fastest single step is the modal cause of the *next* outage | Confirmed by the second-order pass recorded as C4 and the dead end in §5 |
| A5 | Certificates come from a publicly-trusted CA, not an internal PKI | untested belief | Verify, or flag as unverified | **Challenge** — unknown; this is the first route-determining fact, so the analysis is parameterised on it rather than assuming it | unverified — flagged. Repo tree scan found no TLS artifacts; user input required |
| A6 | TLS terminates in a small, enumerable set of places you operate | untested belief | Verify, or flag as unverified | **Challenge** — unknown; second route-determining fact | unverified — flagged. User input required |
| A7 | No client pins the leaf certificate or its public key | untested belief | Verify, or flag as unverified | **Challenge** — pinning breaks automated rotation, because each renewal presents a different certificate; a pinned mobile client fails on the first automated renewal | unverified — flagged. User input required |
| A8 | Server-side TLS only; no mutual TLS with client certificates | untested belief | Verify, or flag as unverified | **Challenge** — client-certificate renewal is a distinct and harder problem this analysis does not address | unverified — flagged. Stated as a scope boundary |
| A9 | The trust anchor stays trusted for the certificate's life | current constraint | Record expiry conditions | **Accept** — lifts if the issuing root or intermediate is distrusted by a major trust store mid-life, which has precedent and is outside operator control | unverified — flagged. No distrust event verified for any specific CA in this run |
| A10 | The endpoint is reachable by an external probe | untested belief | Verify, or flag as unverified | **Challenge** — required by C3; an endpoint reachable only inside a private network needs an internal prober instead | unverified — flagged. User input required |
| A11 | A running terminator serves the previously loaded certificate until reloaded | untested belief | Verify, or flag as unverified | **Challenge** — this is the mechanism behind renewed-but-not-serving; certbot's documentation was opened and does not state it | unverified — flagged → GT-10? |
| A12 | The DNS zone has a provider API available for automation | untested belief | Verify, or flag as unverified | **Challenge** — gates whether DNS-01 is available, and therefore whether wildcards or port-80-less hosts can be served | unverified — flagged. User input required |

## 3. Ground Truths

| ID | Fact | Source | Provenance |
|---|---|---|---|
| **GT-1** | Every X.509 certificate is time-bounded by construction: "The validity period for a certificate is the period of time from notBefore through notAfter, inclusive." | RFC 5280 §4.1.2.5 (`rfc-editor.org/rfc/rfc5280.txt`) | **read-at-source** — §4.1.2.5, quoted above |
| **GT-2?** | A validating TLS client rejects a chain whose leaf is past notAfter, failing the handshake | RFC 5280 §6.1 (path validation) | **unverified.** *Phase 3 failure record: source opened; the retrieved document was truncated before §6.1 and the asserted validation step was not located — `citation does not support the claim`* |
| **GT-3** | Ballot SC-081v3 passed (25 YES certificate issuers, 5 abstentions, zero opposing; 4 YES certificate consumers, unanimous), scheduling "eventual reduction of maximum validity period from 398 days to 47 days," with changes to "occur starting in March 2026 and concluding in March 2029" | CA/Browser Forum ballot page, 2025-04-11 (`cabforum.org`) | **read-at-source** — ballot result and overview section, quoted above |
| **GT-4?** | The intermediate steps are 200 days from 2026-03-15 and 100 days from 2027-03-15, reaching 47 days on 2029-03-15 | Search-result summaries | **reported-by-delegate** — the ballot page's own text did not carry the consolidated schedule; I did not open the Baseline Requirements redline |
| **GT-5?** | SC-081v3 applies only to publicly-trusted certificates; certificates from a private CA absent from public trust stores are out of scope | Search-result summaries | **reported-by-delegate** — not located in the ballot page text I retrieved |
| **GT-6** | "The HTTP-01 challenge can only be done on port 80," and HTTP-01 "cannot be used to issue wildcard certificates" | Let's Encrypt, Challenge Types (`letsencrypt.org/docs/challenge-types/`) | **read-at-source** — quoted above |
| **GT-7** | DNS-01 can issue wildcards, and "it only makes sense to use DNS-01 challenges if your DNS provider has an API you can use to automate updates" | Let's Encrypt, Challenge Types | **read-at-source** — quoted above |
| **GT-8** | TLS-ALPN-01 operates on port 443, viable "if port 80 is unavailable to you" | Let's Encrypt, Challenge Types | **read-at-source** — quoted above |
| **GT-9** | certbot's `--deploy-hook` is a "Command to be run in a shell once for each successfully issued certificate, including on subsequent renewals" | certbot docs, `using.html` (`eff-certbot.readthedocs.io`) | **read-at-source** — quoted above |
| **GT-10?** | A running TLS terminator continues serving the previously loaded certificate until it reloads | certbot docs, `using.html` | **unverified.** *Phase 3 failure record: source opened; the documentation describes `--deploy-hook` but does not state that a reload is required to serve a renewed certificate — `citation does not support the claim`* |
| **GT-11** | Let's Encrypt permits 50 certificates per registered domain every 7 days; 5 certificates per exact same set of identifiers every 7 days; 5 authorization failures per identifier per account every hour | Let's Encrypt, Rate Limits (`letsencrypt.org/docs/rate-limits/`) | **read-at-source** — quoted above |
| **GT-12** | The expiry timestamp is published inside the certificate itself and is readable by any party that can open a connection | Entailed by GT-1 (notAfter is a certificate field, presented in the handshake) | **read-at-source** — derived from GT-1's read |

**`?`-marked ground truths, enumerated: GT-2, GT-4, GT-5, GT-10 (4 of 12).**

**Read-locations for unsuffixed GTs feeding HIGH-confidence chains:** GT-1 — RFC 5280 §4.1.2.5, validity-field definition. GT-3 — CA/B Forum ballot SC-081v3 page, vote-result and overview sections. GT-6, GT-7, GT-8 — Let's Encrypt Challenge Types page, the HTTP-01, DNS-01 and TLS-ALPN-01 sections respectively. GT-9 — certbot `using.html`, renewal-hooks section. GT-11 — Let's Encrypt Rate Limits page, the per-registered-domain, duplicate-certificate and failed-validation entries. GT-12 — entailed by GT-1's read-location.

## 4. Derivation Chains

**C1 — renewal automates one of three conditions. Confidence: HIGH.**

```text
GT-1 (every certificate is bounded by notAfter) + GT-9 (certbot ships a hook that fires after each successful issuance) + GT-12 (the expiry timestamp is published inside the certificate)
→ the tooling separates issuance from what must happen afterwards, so obtaining a new certificate and serving it are distinct steps rather than one
→ a certificate is doing its job only when it is unexpired, actually loaded by the running terminator, and chained to a root the client trusts [Assumes: A9]
→ automating issuance closes the first of those three conditions and leaves the other two exactly as manual as they were
→ the objective that satisfies the stated goal is continuity of TLS termination, of which automated renewal is a necessary but insufficient part
```

*Weakest link:* hop 1 infers the issuance/deployment split from the existence of a post-issuance hook rather than from a direct statement that reload is required — that direct statement is GT-10?, which failed verification.

**C2 — the route is selected by the environment, not by preference. Confidence: HIGH.**

```text
GT-6 (HTTP-01 is port 80 only and cannot issue wildcards) + GT-7 (DNS-01 needs a DNS provider API and can issue wildcards) + GT-8 (TLS-ALPN-01 runs on port 443 when port 80 is unavailable)
→ the challenge type is not a preference but a function of two environment facts: whether the terminator accepts inbound connections on port 80, and whether the DNS zone has a write API [Assumes: A12]
→ every remaining choice — which ACME client, which schedule — sits downstream of that determination and is cheap to change, while the challenge type is the one decision the environment makes for you
→ the fastest path cannot be named from the prompt alone: it is fixed by who issues the certificate today and where TLS terminates, and those two facts select the route [Assumes: A5, A6]
```

*Weakest link:* GT-6/7/8 are Let's Encrypt's rendering of the ACME challenge types; another public CA could in principle differ, though the challenge definitions are protocol-level.

The route table C2's conclusion points to, derived from GT-6/GT-7/GT-8 (tool names below are illustrations, carrying no evidential weight):

| Issuer (A5) | Terminator (A6) | Route |
|---|---|---|
| Public CA | Managed platform endpoint you configure | Move to the platform's own managed certificate — issuance, deployment and reload become one service, closing all three C1 conditions with a configuration change |
| Public CA | Host you operate, inbound :80 reachable | ACME client with HTTP-01, plus a deploy hook that reloads the terminator (GT-9) |
| Public CA | Host you operate, no inbound :80 | DNS-01 if the zone has a write API (GT-7), otherwise TLS-ALPN-01 on :443 (GT-8) |
| Public CA | Wildcard name required | DNS-01 — HTTP-01 cannot issue wildcards (GT-6) |
| Private/internal CA | Any | An ACME-capable internal CA; the Forum schedule does not apply (GT-5?) |

**C3 — the probe is the load-bearing component. Confidence: HIGH.**

```text
GT-1 (validity is bounded by notAfter by construction) + GT-12 (the expiry timestamp is published inside the certificate and readable by any client) + GT-11 (5 certificates per exact set of identifiers every 7 days)
→ certificate expiry is one of very few production failures whose exact time is knowable in advance and readable from outside the system
→ a probe that opens a TLS connection to the public endpoint and reads notAfter therefore tests issuance, deployment and trust chain together, from the client's own vantage point, without needing to know anything about the renewal mechanism [Assumes: A10]
→ the duplicate-certificate budget bounds how many retry cycles fit before expiry, so the alert threshold has to leave room for several of them rather than firing at the last moment
→ an external expiry probe alerting well inside the validity period is the highest-value-per-effort component of the change and must ship with the automation rather than after it
```

*Weakest link:* hop 2 assumes a single probe vantage point is representative; a multi-terminator estate serving different certificates behind one name needs a probe per terminator (A6).

**C5 — automation is a precondition, not an optimisation. Confidence: HIGH.**

```text
GT-3 (SC-081v3 passed, reducing maximum publicly-trusted validity from 398 days to 47 days between March 2026 and March 2029) + GT-1 (validity is bounded by notAfter by construction)
→ the interval between renewals for a publicly-trusted certificate is set by the CA/Browser Forum rather than by the operator, and it is contracting on a published schedule
→ a manual process that is merely inconvenient at 398 days becomes unworkable at 47 days, because the labour scales with the number of renewals and that number rises roughly eightfold
→ automation is not an optimisation of the current process but a precondition for continuing to use publicly-trusted certificates at all, which independently confirms the pre-selected solution [Assumes: A5]
```

*Weakest link:* hop 3 depends on A5 — if the estate is internal-PKI, the Forum's schedule does not bind it (see C7).

**C4 — second-order pass: automation removes the human signal. Confidence: MEDIUM.**

```text
C1 (renewal automates one of three conditions) + C3 (an external probe tests all three) + C5 (the renewal cadence is contracting on a published schedule) + GT-11 (5 authorization failures per identifier per account every hour) + GT-10? (a running terminator keeps serving the previously loaded certificate until it reloads)
→ [2nd] automating renewal removes the calendar reminder and the manual check that today constitute the early-warning signal
→ [2nd] under the schedule established in C5 the renewal cadence rises from roughly annual toward roughly monthly, multiplying the number of renewal events that can fail
→ [3rd] the dominant failure mode therefore shifts from forgetting to renew, which a human notices, toward a renewed certificate sitting on disk while the terminator serves the old one, which nobody notices [Assumes: A11]
→ [3rd] a renewal loop that fails and retries consumes the failed-validation budget, so the automation can lock itself out of recovery during the outage it caused
→ the probe established in C3 is the replacement for the human signal that automation removes, not an optional addition to it
```

*Weakest link:* GT-10?. **Confidence caveat:** rated MEDIUM rather than HIGH because GT-10? is unverified — certbot's documentation was opened and does not state that a reload is required. Reading the reload semantics in your specific terminator's own documentation raises this chain to HIGH. No extension step contradicts a ground truth, so no return to Phase 2 was triggered.

**C6 — the asserted premise, accepted. Confidence: MEDIUM.**

```text
GT-2? (a validating client rejects a leaf past notAfter) + GT-1 (validity is bounded by notAfter by construction) + C3 (an external expiry probe supplies lead time)
→ expiry is not a degradation but a binary cutover: the endpoint serves normally until notAfter and then fails every new validating handshake
→ there is no partial-outage regime in which error rates rise ahead of the failure, so the warning has to come from reading the certificate rather than from watching traffic
→ the premise as stated is accepted rather than challenged, and it is what makes the lead-time argument in C3 necessary rather than merely prudent
```

*Weakest link:* GT-2?. **Confidence caveat:** rated MEDIUM because RFC 5280 §6.1's path-validation step was not located in the retrieved text. Reading §6.1's validity-period check in the complete RFC raises this to HIGH. The claim is nonetheless accepted, because it is the user's own asserted premise and is operationally universal for validating clients.

**C7 — whether the deadline binds you at all. Confidence: MEDIUM.**

```text
GT-5? (SC-081v3 covers publicly-trusted certificates only) + GT-4? (the schedule steps to 200 days in March 2026, 100 days in March 2027 and 47 days in March 2029) + C5 (the contraction is a forcing function) + C2 (two facts select the route)
→ the forcing function established in C5 applies only to the publicly-trusted part of the estate, so an internal PKI runs on its own timetable rather than the Forum's
→ the first step of the schedule took effect in March 2026 and today is September 2026, so a publicly-trusted certificate issued now already sits on a materially shorter clock than the annual cadence most manual processes were built around
→ whether the deadline pressure applies at all is decided by who issues the certificates, which is the first of the two route-determining facts named in C2 [Assumes: A5]
```

*Weakest link:* both GT-4? and GT-5? are search-summary derived. **Confidence caveat:** rated MEDIUM because neither input was read at source — the ballot page confirmed the endpoints (398 → 47 days, March 2026 to March 2029) but not the intermediate steps nor the private-CA carve-out. Reading the SC-081v3 redline against the Baseline Requirements raises this to HIGH.

## 5. Abandoned Reasoning

**Dead end 1 — naming a specific tool as the answer.**
*What was tried:* deriving a concrete recommendation ("install an ACME client, run it on a timer, add a reload hook") directly from the ground truths.
*Why abandoned:* C2 establishes that the challenge type — the one irreversible decision — is fixed by two environment facts (A5, A6, A12) that are not in evidence and that the repo scan could not supply. Any named tool would have been a guess presented as a derivation.
*What it ruled out:* naming a single fastest path in this document. The route table in §4 replaced it, parameterised on the two facts instead.

**Dead end 2 — grounding the reload requirement in certbot's documentation.**
*What was tried:* citing certbot's `using.html` for the claim that a terminator keeps serving the old certificate until reloaded — the mechanism behind renewed-but-not-serving.
*Why abandoned:* the page was opened and states only what `--deploy-hook` does; it does not assert that a reload is required. The citation does not support the claim.
*What it ruled out:* rating C4 HIGH, and building C1's decomposition on the reload fact. C1 was rebuilt on GT-9's weaker but read-at-source grounding — the existence of a post-issuance hook — and GT-10? carries a Phase 3 failure record.

**Dead end 3 — treating the asserted premise as a convention to challenge.**
*What was tried:* classifying "an expired certificate breaks client connections" as a `convention` and inverting it, on the reasoning that a prompt asserting a premise and pre-selecting a solution is the shape that usually warrants challenge.
*Why abandoned:* GT-1's read at RFC 5280 §4.1.2.5 makes the premise a definitional consequence of the certificate format, not an inherited habit. Challenging it would have been contrarianism performing as rigour.
*What it ruled out:* a premise-rejection framing. The premise is accepted (A1, A2) and the pre-selected solution is confirmed as necessary (C5) — the analysis's contribution is showing it is not *sufficient* (C1), which is a different criticism from rejecting it.

## 6. Conclusion

The two facts that select your route are not in evidence, so what follows names the decision rather than pre-empting it.

**Recommended approach:** Do not choose a renewal tool first — establish the two facts that fix the choice (who issues your certificates today, and whether TLS terminates on a managed platform endpoint or on hosts you operate), then read the route straight off the table in §4; if the answer is a managed platform endpoint, moving to the platform's own managed certificate closes all three continuity conditions at once and is genuinely the fastest path available (chain C2).

**Non-negotiable timing:** Automating this has stopped being an optimisation and become a precondition — the CA/Browser Forum's passed ballot contracts maximum publicly-trusted validity from 398 days to 47 days between March 2026 and March 2029, and the first step is already in force as of today (chain C5).

**Key insight:** A certificate serves clients only when three conditions hold simultaneously — unexpired, actually loaded by the running terminator, and chained to a trusted root — and "automated renewal" as normally scoped closes only the first, which is why a correctly-configured renewal cron is compatible with an outage: the new certificate exists on disk and the old one is still being served (chain C1).

**Trade-offs acknowledged:** Automation buys reliability by removing the human calendar reminder that is currently your early-warning signal, and the price is that an external probe reading notAfter from the public endpoint stops being a nice-to-have and becomes the replacement for that signal — it must be priced into the same change, not deferred, and its threshold must leave room for several retry cycles inside the duplicate-certificate budget (chain C3).

Three residuals qualify the above. The shift in dominant failure mode from *forgetting* to *silently broken automation* rests on chain C4, which is MEDIUM because certbot's documentation does not confirm the reload requirement (GT-10?) — check your own terminator's reload semantics. The acceptance of your premise rests on chain C6, MEDIUM because RFC 5280 §6.1's path-validation text was not located in what I retrieved (GT-2?); the premise is accepted anyway, as operationally universal. Whether the Forum's deadline binds you at all rests on chain C7, MEDIUM because the intermediate schedule steps and the private-CA carve-out are search-summary derived (GT-4?, GT-5?). Separately, if any client pins your leaf certificate or its public key (A7), automated rotation will break it on the first renewal — verify this before automating, not after.

Overall confidence is HIGH on the recommendation, since chains C1, C2, C3 and C5 each consume only read-at-source ground truths.

---

## Assumption Audit (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | tooling separates issuance from what follows | none | n/a |
| C1 | 2 | three conditions: unexpired, loaded, trusted chain | A9 trust anchor stays trusted | yes |
| C1 | 3 | automating issuance closes only the first | none | n/a |
| C1 | 4 | objective is continuity of TLS termination | none | n/a |
| C2 | 1 | challenge type is a function of two environment facts | A12 DNS provider API available | yes |
| C2 | 2 | remaining choices are downstream and cheap to change | none | n/a |
| C2 | 3 | route fixed by issuer and terminator | A5 public CA; A6 enumerable terminators | yes |
| C3 | 1 | expiry time is knowable in advance | none | n/a |
| C3 | 2 | probe tests all three conditions from outside | A10 endpoint externally probe-reachable | yes |
| C3 | 3 | duplicate budget bounds retry cycles before expiry | none | n/a |
| C3 | 4 | probe is highest-value-per-effort component | none | n/a |
| C4 | 1 | automation removes the calendar reminder | none | n/a |
| C4 | 2 | cadence rises annual → monthly | none | n/a |
| C4 | 3 | failure shifts to renewed-but-not-served | A11 terminator serves old cert until reload | yes |
| C4 | 4 | retry loop consumes failed-validation budget | none | n/a |
| C4 | 5 | probe replaces the human signal | none | n/a |
| C5 | 1 | renewal interval is set by the Forum, not the operator | none | n/a |
| C5 | 2 | manual process unworkable at 47 days | none | n/a |
| C5 | 3 | automation is a precondition | A5 public CA | yes (already added at C2/3) |
| C6 | 1 | expiry is a binary cutover, not a degradation | none | n/a |
| C6 | 2 | no graceful pre-failure signal in traffic | none | n/a |
| C6 | 3 | premise accepted, makes C3 necessary | none | n/a |
| C7 | 1 | forcing function applies only to public estate | none | n/a |
| C7 | 2 | first schedule step already in force | none | n/a |
| C7 | 3 | issuer decides whether deadline applies | A5 public CA | yes (already added at C2/3) |

25 rows, one per chain per step, in order. A7 and A8 were surfaced in Phase 2 rather than from a chain step and carry no `[Assumes:]` mark.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | `GT-1 (...) + GT-9 (...) + GT-12 (...)` | yes | n/a | yes |
| C2 | `GT-6 (...) + GT-7 (...) + GT-8 (...)` | yes | n/a | yes |
| C3 | `GT-1 (...) + GT-12 (...) + GT-11 (...)` | yes | n/a | yes |
| C5 | `GT-3 (...) + GT-1 (...)` | yes | n/a | yes |
| C4 | `C1 (...) + C3 (...) + C5 (...) + GT-11 (...) + GT-10? (...)` | yes | n/a | yes — C1, C3, C5 all resolve; no cycle |
| C6 | `GT-2? (...) + GT-1 (...) + C3 (...)` | yes | n/a | yes — C3 resolves; no cycle |
| C7 | `GT-5? (...) + GT-4? (...) + C5 (...) + C2 (...)` | yes | n/a | yes — C5, C2 resolve; no cycle |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "The two facts that select your route are not in evidence…" | prose | no | prose carrying neither a bold colon lead-in nor a list marker | n/a |
| "**Recommended approach:** Do not choose a renewal tool first…" | bold lead-in | yes | prescribed lead-in; colon closes the bold span | C2 |
| "**Non-negotiable timing:** Automating this has stopped being an optimisation…" | bold lead-in | yes | bold lead-in whose colon closes the bold span | C5 |
| "**Key insight:** A certificate serves clients only when three conditions hold…" | bold lead-in | yes | prescribed lead-in; colon closes the bold span | C1 |
| "**Trade-offs acknowledged:** Automation buys reliability by removing…" | bold lead-in | yes | prescribed lead-in; colon closes the bold span | C3 |
| "Three residuals qualify the above…" | prose | no | prose carrying neither a bold colon lead-in nor a list marker; caveat naming C4, C6, C7 inline | n/a |
| "Overall confidence is HIGH on the recommendation…" | prose | no | prose carrying neither a bold colon lead-in nor a list marker | n/a |

```text
Scan complete: 7 chain rows, one per section-4 chain block in order; 7 section-6 rows, one per construct in order — 4 claims under R11, 3 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate

**Criterion 1: Identify Essence**
Quoted span: "What is the minimum change that makes TLS termination continuously present a valid, trusted, unexpired certificate to clients — *including* detecting when it has stopped doing so?"
Band: **Rigorous**
Justification: a single sentence naming the underlying question rather than the prompt's pre-selected mechanism, followed by four success criteria each stating a verb-subject-outcome test applied by scanning §6 without interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span: from the Assumption Audit scan — "C1 | 2 | three conditions: unexpired, loaded, trusted chain | A9 trust anchor stays trusted | yes"
Band: **Rigorous**
Justification: the audit table carries one row per chain per step for all 25 steps in order with no step skipped, every Type is drawn from the four-type scheme, every Verdict leads with Accept or Challenge followed by a specific justification, and eight assumptions are Challenged rather than uniformly Accepted.

**Criterion 3: Establish Ground Truths**
Quoted span: enumerated GT-2, GT-4, GT-5, GT-10; the Ground Truths list carries `?` on exactly those four and on no others — checked entry by entry against the table.
Band: **Rigorous**
Justification: all twelve GT-IDs are stable and referenced in §4, every unsuffixed GT names a read-at-source location, the two failed reads carry Phase 3 failure records with the reason `citation does not support the claim`, and each of the eight unsuffixed GTs feeds at least one HIGH chain (GT-1/GT-12 → C1, C3; GT-3 → C5; GT-6/7/8 → C2; GT-9 → C1; GT-11 → C3).

**Criterion 4: Reason Upward**
Quoted span: from the self-audit scan's chain-form table — "C4 | `C1 (...) + C3 (...) + C5 (...) + GT-11 (...) + GT-10? (...)` | yes | n/a | yes — C1, C3, C5 all resolve; no cycle"
Band: **Rigorous**
Justification: all seven chain blocks score form-conforming with clean dependencies, each carries at least one genuine intermediate hop, §5 documents three dead ends in What-was-tried / Why-abandoned / What-it-ruled-out structure with specific structural reasons, and the route table's tool names are explicitly marked as carrying no evidential weight so no analogy stands as direct evidence.

**Criterion 5: Validate**
Quoted span: "rated MEDIUM rather than HIGH because GT-10? is unverified — certbot's documentation was opened and does not state that a reload is required. Reading the reload semantics in your specific terminator's own documentation raises this chain to HIGH."
Band: **Rigorous**
Justification: every chain names its weakest link, all three chains consuming a `?` input (C4, C6, C7) are rated MEDIUM with a caveat naming the specific input and the verification that would raise it, no HIGH chain consumes a `?` input, and each of the four §6 claims rests on a HIGH chain so the stated overall HIGH matches the weakest contributing chain. No EXCEPT clause is claimed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: from the self-audit scan's claim-inventory table — "\"**Key insight:** A certificate serves clients only when three conditions hold…\" | bold lead-in | yes | prescribed lead-in; colon closes the bold span | C1"
Band: **Rigorous**
Justification: all four §6 claims cite a named §4 chain inline with zero untraced, no claim introduces reasoning absent from §4, and the Key Insight names a non-obvious finding — that a correctly-configured renewal job is compatible with an outage — which is distinct from the recommended approach's route-selection claim rather than a restatement of it.

**Gate result: PASS.** No criterion Absent; zero at Hand-wavy.

---

**Sources:** [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280.txt) · [CA/Browser Forum Ballot SC081v3](https://cabforum.org/2025/04/11/ballot-sc081v3-introduce-schedule-of-reducing-validity-and-data-reuse-periods/) · [Let's Encrypt Challenge Types](https://letsencrypt.org/docs/challenge-types/) · [Let's Encrypt Rate Limits](https://letsencrypt.org/docs/rate-limits/) · [certbot user guide](https://eff-certbot.readthedocs.io/en/stable/using.html) · [SSL.com on 47-day certificates](https://www.ssl.com/article/preparing-for-47-day-ssl-tls-certificates/) · [The SSL Store on the 2029 timeline](https://www.thesslstore.com/blog/47-day-ssl-certificate-validity-by-2029/)

**To turn this into a specific recommendation, I need one line from you:** who issues your certificates today (public CA or internal PKI), and where TLS terminates (managed platform endpoint or hosts you operate).

**Relevant file:** `/home/chrisdavidson/Projects/first-principles-skill/tests/premise-rejection-catalog.md` — row `PR-N1` is this prompt.