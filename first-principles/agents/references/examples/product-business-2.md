<!-- GENERATED — DO NOT EDIT. Source: shared/examples/product-business-2.md. Regenerate via: scripts/sync-content.py --write. -->

# Worked Example: Product and Business (Feature Prioritization)

A second product-and-business analysis, peer to `product-business.md`. The earlier
example reasons about free-tier pricing economics; this one reasons about a
feature-prioritization / build-next decision under a binding engineering-capacity
constraint. The reasoning shape is value-vs-cost-vs-evidence: which of two
well-defined candidates returns more measured customer value per unit of the same
scarce engineering quarter, and which of the two evidence stories is actually
load-bearing.

---

## 1. Problem Essence

**Core problem:** Given that one engineering quarter of capacity can fund at most
one of two candidate investments, which one should a B2B SaaS team build next —
the Slack integration repeatedly requested by sales prospects, or the reporting
rewrite that an existing enterprise account has committed contract expansion
against?

**Success criteria:**
- The choice is grounded in measured customer signal (usage data, churn
  instrumentation, signed contract language) rather than aggregated anecdote.
- The expected post-ship outcome of each candidate is stated in observable
  terms: retention delta within two quarters, account-expansion ARR closing
  within one quarter, or a documented falsification trigger if neither
  materializes.
- The opportunity cost of the unbuilt candidate is named explicitly, not
  absorbed silently.
- A skeptic can re-run the decision from the same ground truths and reach the
  same conditional verdict, or identify exactly which ground truth they
  disagree with.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| The Slack integration is in high customer demand | untested belief (economic-hinge) | The demand claim is load-bearing for the Slack-side value chain; if the demand signal collapses on inspection, the Slack candidate has no remaining value case. Verify by sourcing it to instrumentation (in-product feature requests, churn-survey reason codes), not aggregated sales anecdote. | Challenge | unverified — flagged. The "high demand" claim is sourced to sales-call notes, an inbound channel with strong selection bias (the prospects loud enough to ask are the prospects loud enough to reach sales). No churn-survey reason code or in-product request signal has been pulled to confirm. |
| The reporting rewrite is required to close the named enterprise contract expansion | current constraint (external-actor) | The constraint binds because a specific customer's procurement decision is contingent on it. Name the external party, the specific decision (sign the expansion order form by quarter-end), and the realistic timeline. Expiry is a negotiation move, not a measurement. | Accept | Verified against the signed letter-of-intent from the enterprise account (GT-3); the expansion ARR is contingent on the rewrite shipping within the quarter and is documented in the LOI's exit clause. |
| Both candidates fit inside one engineering quarter | untested belief (methodology) | The cost estimates are produced by the engineering manager's top-down judgement, not by decomposition. Verification is constructing an alternative bottom-up estimate (ticket-level breakdown × historical per-ticket cycle time) and comparing. | Challenge | unverified — flagged. Only top-down estimates exist. The Slack integration's "one quarter" estimate has not been decomposed; the reporting rewrite's estimate has a partial decomposition through the schema-migration step but no estimate beyond it. |
| The team is the B2B-integrations-first kind of company, so integrations come first when in doubt | convention (default-response) | Challenge by asking whether the default response addresses the highest-frequency observed signal versus the cognitively-available response. If the observed signal is contract-expansion risk on a named account, the integrations-first default is reaching past the actual signal. | Discard | The integrations-first heuristic is a cultural default with no named ground truth tying it to current quarter's revenue or retention outcomes. Discard as standalone justification; revisit if a Slack-side GT later emerges. |
| Competitors with Slack integrations are winning deals against us because of the integration | convention (analogy-as-evidence) | Discard as standalone justification. An analogy may be revived only if re-expressed as a named ground truth about the analogue — here, a measured win/loss-reason analysis where Slack-integration absence is the named loss driver. | Discard | No win/loss analysis exists that isolates Slack-integration presence as a deal-deciding factor. The claim is sales-team conjecture about competitor advantage, not measured evidence. The methodology forbids analogy as direct evidence (cross-ref `validation-rubric.md` Criterion 4). |
| Capacity is genuinely binary this quarter (one candidate, not both) | current constraint (quantifiable-cost) | Quantify before recording expiry. Confirm via the engineering manager's actual headcount × historical ship velocity (GT-4) that the budget does not stretch to a partial scope of the other candidate. Expiry condition should reference the measured value. | Accept | Verified: GT-4 establishes 3.2 engineer-quarters of build capacity for the upcoming quarter; either candidate's top-down estimate consumes ≥ 3 of those quarters. A partial scope of the second candidate would not be shippable as a customer-facing increment. |
| Post-ship retention/expansion effects materialize on a timeline that lets us learn before the next quarter's planning | untested belief | Verify by stating the falsification trigger and the data source up front. If the effect would not be observable within one quarter, the recommendation must be downgraded to a pilot whose stated purpose is to measure the effect. | Challenge | unverified — flagged. The Slack-side retention hypothesis has no pre-specified falsification trigger; the reporting-rewrite-side expansion has a contractual trigger (signed expansion order or not) that is observable within the quarter. |

---

## 3. Ground Truths

- **GT-1** The team's last two quarters of customer-feedback data show 41
  inbound Slack-integration requests across 240 active accounts (~17% of
  accounts have asked at least once), with no churn-survey reason code
  attributing departure to the missing integration. — source: in-product
  feedback log + post-cancellation churn-survey instrument, both queried
  Q-1.
- **GT-2** The current reporting product surface has a documented enterprise
  blocker: three of the top-ten accounts by ARR have filed support tickets
  in the last two quarters citing reporting limitations as a contract-renewal
  risk; one of those three has the formal expansion contingency in GT-3. —
  source: support-ticket export tagged `reporting-limitation`, cross-referenced
  with the account-management ARR roll-up.
- **GT-3** A signed letter-of-intent from one top-ten account commits to
  $180,000/year in expansion ARR contingent on the reporting rewrite shipping
  within the upcoming quarter. Failure to ship triggers a written exit clause
  permitting non-renewal at the contract anniversary. — source: signed LOI
  filed with finance and legal.
- **GT-4** Engineering capacity for the upcoming quarter is 3.2 engineer-
  quarters of build capacity, net of on-call and maintenance budget; the
  remaining ~0.8 engineer-quarters is already allocated to the rolling
  maintenance and security-patch budget and is not available for either
  candidate. — source: engineering manager's capacity plan, derived from
  headcount × historical sustained ship velocity over the last four quarters.
- **GT-5?** The Slack integration, if shipped, would convert some fraction of
  the 41 requesting accounts from at-risk-of-churn to retained, and would
  contribute to net new logo acquisition through deal-cycle de-risking. —
  unverified: no churn-survey reason code attributes departure to the missing
  integration, and no win/loss instrument isolates Slack-integration absence
  as a deal-deciding factor. The retention-delta and acquisition-uplift
  magnitudes are unmeasured.

---

## 4. Derivation Chains

### Conclusion: The reporting-rewrite candidate has a verified expansion-revenue case that the Slack candidate does not

GT-2 (three top-ten accounts cite reporting limitations as renewal risk) + GT-3
(signed LOI commits $180K/year contingent on the rewrite shipping this quarter)
→ The reporting-rewrite value chain rests on a named, signed, quantified
customer commitment with a contractually-observable falsification trigger
(expansion order signed or not by quarter-end); the Slack-side value chain
rests on GT-1's inbound request volume plus GT-5?'s unmeasured retention
hypothesis, neither of which is contractually anchored
→ At equivalent engineering cost (GT-4), the reporting rewrite returns a
defined, verifiable $180K expansion ARR plus reduced renewal risk on two
other named top-ten accounts; the Slack integration returns a hypothesized
retention and acquisition uplift with no instrumented anchor

**Confidence:** MEDIUM. The downgrade is driven by GT-5? (Slack-side retention
and acquisition magnitudes are unmeasured). Raising the Slack-side case to a
comparable level would require either (a) a churn-survey reason code
attributing exits to the missing integration, or (b) a win/loss instrument
isolating Slack-integration absence as a deal-deciding factor — neither
exists today.

---

### Conclusion: The opportunity cost of not building the Slack integration this quarter is bounded and recoverable; the opportunity cost of not shipping the reporting rewrite is not

GT-1 (Slack requests are inbound but no churn signal attributes departure to
the gap) + GT-3 (the reporting LOI's exit clause permits non-renewal at the
contract anniversary if the rewrite slips)
→ A one-quarter delay to the Slack integration costs the team a quarter of
hypothesized retention/acquisition uplift on an unmeasured base; a one-quarter
slip on the reporting rewrite triggers a contractual non-renewal right on a
$180K+ account and signals to the two adjacent at-risk accounts that the
reporting gap remains unaddressed
→ The two opportunity-cost profiles are asymmetric: the Slack delay is
revisitable next quarter without contractually irreversible consequences; the
reporting slip permits a contractually-irreversible customer loss

**Confidence:** HIGH. Both inputs are verified ground truths; the asymmetry
follows from contract language (GT-3) and the absence of a counterpart
contractual trigger on the Slack side.

---

### Conclusion: The recommendation flips only if the Slack-side evidence picture changes materially before planning lock

GT-5? (Slack-side retention and acquisition effects unmeasured) + GT-4
(capacity is binary this quarter — no partial-scope path)
→ The decision is contingent on the Slack-side evidence story remaining
anecdotal; if before planning lock the churn-survey instrument is re-coded
and surfaces a Slack-attributed reason code on a material fraction of
exits, or if a win/loss audit isolates Slack-integration absence as a
deal-deciding factor on multiple lost deals, the Slack candidate gains the
kind of contractual-equivalent evidence the reporting candidate has
→ Until that evidence appears, the reporting rewrite dominates on
verified-value-per-engineer-quarter; if it appears, the analysis must be
re-run with the new GT promoted from GT-5? to a verified GT

**Confidence:** MEDIUM. The downgrade is again driven by GT-5?; the chain's
own conclusion is that the recommendation is conditional on GT-5?'s
verification status.

---

## 5. Abandoned Reasoning

### Dead End: Sixty percent of polled customers said they want Slack, therefore build Slack

**What was tried:** Use an aggregated count of Slack-integration mentions
across sales calls, in-product requests, and a recent customer panel as
direct evidence that the Slack integration is the higher-value build. The
reasoning chain was: "a strong majority of contacted customers asked for
this feature; therefore building it will materially improve retention and
acquisition relative to the alternative."

**Why abandoned:** The aggregated count conflates three response surfaces
with different selection biases. The sales-call mentions come from
prospects who reached sales (a self-selected, deal-stage-skewed pool, per
GT-1's churn-survey gap). The in-product requests come from engaged
existing users (the cohort least likely to churn for the missing feature).
The customer-panel result over-samples customers willing to spend an hour
on a panel call — again the engaged-and-retained tail. None of these
surfaces measures the load-bearing quantity: the rate at which absence of
the Slack integration causes paying accounts to leave or prospective
accounts to choose a competitor. The Phase 4 no-analogies guidance applies
by extension: counting stated preferences is not the same as measuring
revealed retention or paid acquisition impact, and conflating them is the
preference-vs-revealed-behavior error that converts an `untested belief`
into the appearance of evidence. The taxonomy classifies the underlying
demand assumption as `untested belief (economic-hinge)` precisely because
the entire Slack-side value case hinges on it; an aggregated stated-preference
count does not discharge that classification.

**What it ruled out:** The "majority asked for it" framing as a sufficient
basis for a feature-prioritization decision under a binding capacity
constraint. The dead end establishes that the Slack-side value case
requires churn-survey reason-code evidence or win/loss-isolated evidence —
the kinds of instrumented signals that measure revealed behavior — not
aggregated stated-preference counts. It also pre-emptively rules out a
sibling failure mode in which a future panel result is read as the missing
evidence.

---

## 6. Conclusion

**Recommended approach:** Build the reporting rewrite this quarter and
defer the Slack integration to the next planning cycle. Before planning
lock for the next quarter, instrument the churn-survey reason codes and
run a win/loss audit specifically isolating Slack-integration presence, so
that the Slack-side evidence picture is either promoted from GT-5? to a
verified GT or explicitly retired. If the audit surfaces a material
Slack-attributed signal, the next-quarter decision is reconsidered with
that GT in hand; if it does not, the deferral becomes permanent rather
than rolling.

**Key insight:** A high inbound-request count and a signed contract
contingency are not the same kind of evidence and cannot be compared on
volume. One is a stated-preference signal with strong selection bias;
the other is a revealed-behavior commitment with a contractual
falsification trigger. The first-principles methodology forces the
comparison onto a single axis (verified value per engineer-quarter under
the GT-4 capacity constraint) and exposes that the Slack candidate's
value case is anchored on an unverified `untested belief (economic-hinge)`
while the reporting candidate's value case is anchored on a `current
constraint (external-actor)` whose expiry condition is contractually
specified. The cultural default of "we are an integrations-first
company" is a `convention (default-response)` that reaches past the
highest-frequency observed signal (the contract-expansion risk on a
named account) toward the cognitively-available answer.

**Trade-offs acknowledged:** The deferral incurs real cost: prospects
asking sales for Slack continue to hear "on the roadmap"; some fraction
of the 41 requesting accounts may quietly disengage during the deferral
window; a competitor closing a deal during the quarter on integration
strength is a possible but unmeasured loss. The next-quarter
re-evaluation is contingent on the team actually performing the
instrumentation work named above; if that work slips, the Slack
candidate stays in the same evidence position next planning cycle and
the deferral compounds.

**Confidence:** MEDIUM. The downgrade is driven by GT-5? (Slack-side
retention and acquisition magnitudes are unmeasured) and by the
challenged methodology assumption on cost estimation (top-down estimates
not bottom-up-validated for either candidate). Raising to HIGH requires
either bottom-up cost decompositions for both candidates and verified
Slack-side retention/acquisition instrumentation, or the explicit
acceptance that the verified contractual case for the reporting rewrite
(GT-3) is sufficient on its own and the comparison need not be
quantitatively symmetric.
