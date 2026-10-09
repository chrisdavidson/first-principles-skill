## Assumption Audit (process output)

End-of-phase scan of every Derivation Chain step (section 4) for assumptions not already present
in the Assumptions Table (section 2) at the time chains were drafted. Four new assumptions were
surfaced and have been added to the Assumptions Table as A-14 through A-17; all are marked inline
on their originating chain step with `[Assumes: A-N]`.

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|------------------------|------------------|
| C1 | 1 | free tier's acquisition value depends on a self-serve/inbound funnel | none | n/a |
| C1 | 2 | absence of funnel means the mechanism that gives competitors' tiers value is missing here | none | n/a |
| C1 | 3 | copying the SKU without the funnel only replicates the SKU, not the outcome | none | n/a |
| C1 | 4 (conclusion) | competitor parity is not, on its own, a load-bearing reason | yes — competitors' free-tier value derives primarily from their funnel, not from product-inherent virality or brand power | yes (A-14) |
| C2 | 1 | cost is a function of total active users, so every free signup has positive marginal cost | none | n/a |
| C2 | 2 | C_f bracketed at $50-$600/year | yes — A-cost-bracket (declared inline already) | yes (A-5) |
| C2 | 3 | breakeven conversion rate = C_f / ACV, giving 0.5%-6% | none (arithmetic) | n/a |
| C2 | 4 | no internal conversion rate exists, so expected value cannot be estimated | none | n/a |
| C2 | 5 (conclusion) | unit economics are indeterminate today | none | n/a |
| C2 | 6 | resolving indeterminacy requires first-principles measurement, not a borrowed benchmark | none (resolved in §5 Dead End 1) | n/a |
| C3 | 1 | reps' prospects gain a no-cost alternative mid-funnel, deals stall | none (maps to existing A-9) | n/a |
| C3 | 2 | paying teams could shadow-split seats into free accounts | yes — no technical/contractual barrier currently prevents seat-splitting | yes (A-15) |
| C3 | 3 | support volume lands on a team sized for high-touch service (GT-6?) | none (maps to existing A-7 / GT-6?) | n/a |
| C3 | 4 | near-term effects are cost/risk only, no offsetting funnel benefit | none | n/a |
| C3 | 5 | sustained 18+ months, free tier normalizes as an entrenched cost center | yes — once a cost center is politically embedded, reversing or resourcing it later is harder than deciding upfront | yes (A-16) |
| C3 | 6 (conclusion) | effects work against the decision's own success criterion, reinforcing C1/C2 | none | n/a |
| C4 | 1 | must-have knockout rules out a full public free tier today | none (maps to existing A-8 / A-10) | n/a |
| C4 | 2 | weighted trade-off: status quo 90, invest-first 87, scoped trial 81 | yes — locked weights reflect this company's actual strategic priorities, not merely the analyst's judgment | yes (A-17) |
| C4 | 3 | flip test: +1 weight-point on strategic optionality inverts the ranking | none (arithmetic) | n/a |
| C4 | 4 | invest-first matches status quo's protections while making bounded progress | none (synthesis) | n/a |
| C4 | 5 (conclusion) | recommended action: run named experiments, revisit later | none | n/a |

---

## Techniques not applied (process output)

Full-composer mode (no single-technique trigger fired in the request). Companion techniques
applied: Inversion (Phase 2), Estimate (Phase 4, within C2), Second-Order (Phase 4, within C3),
Trade-off (Phase 4, within C4), Pre-Mortem (Phase 5 adversarial technique, since the headline
conclusion is a plan/recommendation). Techniques whose invocation did not fire:

- theoretical-limit — not applicable — no governing physical or mathematical hard constraint is
  relevant to this pricing/go-to-market decision; the nearest candidate (infrastructure cost
  scaling with active users) is a cost-accounting fact (GT-3?), not a law-bound ceiling, so there
  is no ideal-bound/best-demonstrated/conventional bracket to derive.
- fishbone — not applicable — the assumption space was adequately enumerated through
  stakes-escalation and inversion without needing a breadth-first category brainstorm; no
  multi-causal, intuition-defeating assumption space was encountered.
- five-whys (reduce-to-primitives mode) — not applicable — every candidate ground truth (GT-1?
  through GT-6?) is already an atomic, single-fact claim as stipulated; none is a compound claim
  requiring decomposition into deeper constituent facts.
- five-whys (causal mode) — not applicable — this is a forward go/no-go decision, not a diagnostic
  "why did this symptom occur" investigation.
- inversion (Phase 5 invocation) — not applicable — the headline conclusion is a plan/recommendation
  rather than a bare claim, which routes Phase 5's adversarial technique to Pre-Mortem per the
  inversion-vs-pre-mortem decision rule, not to a second inversion pass; inversion's Phase 2
  invocation (assumption-challenging) did fire and is recorded in section 2.
## Adversarial pass (process output)

**Recompute.** Breakeven conversion rate = C_f / ACV at both bracket ends: $50 / $10,000 = 0.5%;
$600 / $10,000 = 6% — recomputed, confirmed. Trade-off weighted totals recomputed independently:
status quo = 5(4)+5(5)+5(5)+5(3)+1(3)+2(1) = 20+25+25+15+3+2 = 90; scoped trial =
4(4)+4(5)+4(5)+4(3)+3(3)+4(1) = 16+20+20+12+9+4 = 81; invest-first =
2(4)+5(5)+5(5)+4(3)+5(3)+2(1) = 8+25+25+12+15+2 = 87 — all three recomputed, confirmed. Flip test:
difference (status quo − invest-first) = 90 − 87 = 3; per-criterion contribution to that
difference = (5−2)·4 [cost] + (5−5)·5 [anchor] + (5−5)·5 [cannibalization] + (5−4)·3 [support] +
(1−5)·3 [optionality] + (2−2)·1 [signaling] = 12+0+0+3−12+0 = 3 — matches, confirmed. Solving
15 − 4w = 0 for the optionality weight gives w = 3.75 against a locked weight of 3 — a move of
well under one full point flips the ranking — recomputed, confirmed.

**Sensitivity.** The single ground truth whose falsity would most flip the conclusion is **GT-2?**
(no self-serve/inbound channel exists today). It is `?`-marked. If false — e.g., some
non-outbound-sourced signup trickle already exists and was simply never instrumented — chain
C1's funnel-gap argument weakens, the trade-off's must-have knockout on a full free tier no
longer clearly applies, and the recommended sequencing could skip straight to a bounded free-tier
test rather than a self-serve-starter-tier test first. Verification: an audit of existing
website/product traffic and signup-source logs for any non-outbound-attributed leads —
Experiment #1 effectively performs this check as a byproduct.

Weakest link per chain: **C1** — GT-5?'s unverified claim about *how* competitors actually use
their free tier (demand-gen vs. sales-assist), compounded by the live, unresolved rival named
below. **C2** — the $50–$600 bracket on C_f spans an order of magnitude; the true figure is
unmeasured. **C3** — GT-6? (support team's capacity/tooling posture) is asserted from the user's
own framing, not measured. **C4** — the trade-off is a genuine near-tie (flip distance ≈ 0.75 of
one weight-point on Strategic Optionality).

**Rival.**
- Headline: rival "add a full free tier now, matching competitors" is ruled out by the trade-off's
  must-have knockout (no signup-generation mechanism exists) — see §5 Dead End 2.
- Headline: rival "reject a free tier permanently, no further action" is not ruled out cleanly —
  the inversion preconditions (A-11, A-12, A-13) and the trade-off's near-tie mean this rival is not
  clearly inferior either — see §5 Dead End 3. The recommendation resolves this by choosing the
  conditional, experiment-gated middle path rather than either pole.
- C1: rival "competitors' free tiers function as sales-assisted trial tools, not organic demand-gen,
  so the funnel gap matters less" is live and unresolved — carried on C1's own confidence line below.
- C2: no live rival to "unit economics are indeterminate" — any claim of clear favorability or
  unfavorability would itself require the same unmeasured data, so indeterminacy is the most
  defensible reading; Rivals axis clean for C2.
- C3: rival "a bounded trial shortens sales cycles by letting prospects self-qualify before engaging
  a rep" (inversion Precondition D's milder cousin) is live, not settled; Experiment #2 is designed
  to test it directly.

**Adversarial technique — Pre-Mortem** (the headline conclusion is a plan/recommendation, which
routes here rather than to a second Inversion pass per the decision rule).

*Premise:* The plan has already failed. Eighteen months from now, the company either (a) burned
real engineering and support budget on a free tier that generated negligible paying conversions
and measurably slowed the outbound sales cycle, or (b) sat on the sidelines while a competitor's
free tier captured the self-serve segment permanently — and there is nothing to show for either
the investment or the inaction.

*Causes* (unfiltered, generated from four stakeholder viewpoints):
1. (VP Sales / rep) Reps stopped pushing urgency once prospects said "we'll just try the free
   version first," elongating deal cycles.
2. (VP Sales / rep) Comp plans were never updated, so reps had no incentive to guide prospects into
   the bounded trial, and it was used inconsistently or not at all.
3. (VP Sales / rep) A top account quietly moved half its paid seats into shadow free accounts and
   nobody noticed until the renewal came in low.
4. (Support/Ops) Free-tier signups — even a small scoped trial — generated enough tickets that SLA
   for paying accounts slipped, and a renewal was lost over a support complaint.
5. (Support/Ops) No self-serve knowledge base or tiered ticketing was ever built, because "we're
   not doing a real free tier yet," so when any free users did show up there was no cheap way to
   absorb them.
6. (Competitor) A well-funded competitor doubled down on content/SEO around their free tier during
   this exact window and locked in developer mindshare that cannot be dislodged by a late entry.
7. (Competitor) The competitor's free tier became the de facto category evaluation path, so even
   outbound-sourced prospects started asking "why can't we just try it for free," compressing the
   $10k ACV conversation.
8. (CFO) The experiments were approved but never resourced with a real budget or owner, so they
   dragged on for a year without producing a clean signal either way.
9. (CFO) Infra/billing work to measure C_f properly was deprioritized behind feature work, so the
   single most load-bearing unknown was never actually measured.
10. (CFO) "Revisit later" became "never" because no decision checkpoint was calendared, and the
    status quo calcified by default rather than by deliberate choice.

*Clusters:*
- **Cluster A — Experiments never get resourced** (causes 8, 9, 10; bears on C2's GT-3?/GT-4?
  inputs and C4's entire "revisit later" premise): without a real owner and budget, the
  conditional-recommendation structure collapses into a de facto permanent "no" by neglect.
- **Cluster B — Sales motion erodes silently even from a bounded trial** (causes 1, 2, 3; bears on
  C3's actor-lens hops and A-9, A-15): even the recommended scoped trial carries real
  cannibalization/seat-shadowing risk without comp-plan and seat-governance guardrails.
- **Cluster C — Support absorbs cost with no tooling investment** (causes 4, 5; bears on GT-6? and
  C3): any experiment touching real free users needs a minimal triage plan before launch.
- **Cluster D — Competitive window closes faster than our diligence** (causes 6, 7; bears on C1's
  live rival and A-11/A-13): the de-risking path assumes time is available to run experiments
  sequentially; that assumption itself needs an early, fast check.

*Disposition:*
- Cluster A — **Plan change:** name a single accountable owner and a fixed, one-quarter time-box
  for Experiments #1–#5, with a calendared decision checkpoint at the end, not an open-ended
  "revisit later."
- Cluster B — **Plan change:** pair Experiment #2 with explicit rep guidance, a comp-plan
  clarification (trial counts toward pipeline credit), and seat-level usage monitoring on existing
  paying accounts, before the trial launches, not after.
- Cluster C — **Accepted risk, named mitigation:** accept that even a bounded trial generates some
  support load; cap participant count explicitly and stand up a minimal triage queue before
  Experiment #2 launches, rather than building full self-serve support tooling up front.
- Cluster D — **Plan change:** move Experiment #5 (competitive teardown) to the front of the
  sequence and run it fast (weeks, not months), specifically to test whether Precondition A-11
  (fast-forming lock-in) is plausible before committing the full quarter to the rest of the set.

**Falsification.** This analysis's headline conclusion is false if a bounded experiment
(Experiment #1 or #2), run within the next two quarters, produces either: (a) a measurable,
non-trivial trickle of organic self-serve signups despite no dedicated marketing push — evidence
that GT-2?'s "no inbound motion" is less absolute than stipulated and that fuller free-tier
investment is justified sooner than "later"; or (b) clear evidence that outbound deal cycles and
existing-account seat composition are unaffected by a bounded free/trial offer — removing the
cannibalization concern that currently caps chains C3 and C4 at LOW confidence.
## §6→§4 closure ledger (process output)

- "Do not add a free tier now; instead run a time-boxed set of five de-risking experiments and
  revisit the decision" → chain C4 ✓
- "The decisive variable is whether any mechanism exists to generate free signups at all, not
  whether a free tier is a good idea in the abstract" → chain C1 ✓
- "This path accepts a near-term strategic-optionality cost relative to launching immediately"
  → chain C4 ✓
- "If competitor lock-in is accelerating faster than assumed, a quarter of diligence has a real
  opportunity cost, which is why the competitive teardown is sequenced first" → chain C4 ✓

All surviving §6 claims cite a chain inline; no claim required cutting.

## Self-audit scan (process output)

**Table 1 — chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-2?, GT-5? | yes | n/a | yes | LOW | no | none |
| C2 | GT-1?, GT-3?, GT-4? | yes | n/a | yes | MEDIUM | no | none |
| C3 | C1, C2, GT-6? | yes | n/a | yes | LOW | no | none |
| C4 | C1, C2, C3 | yes | n/a | yes | LOW | no | none |

`Act attempted?` is `no` for every chain because none of GT-1?–GT-6? cites an external,
openable source — they are the user's own stipulated internal-business facts supplied directly in
the prompt with no named document, URL, or file to open (see §3 for the per-GT provenance note).
No bounded re-entry edge fired during this run (no Criterion 1 Absent, no mid-run input re-open, no
second-order contradiction routing back to Phase 2, no Fix/Repeat pass needed).

**Table 2 — claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| Recommended approach: do not add a free tier now; run experiments | bold lead-in | yes | colon closes bold span, content follows on same line | C4 |
| Key insight: decisive variable is whether a signup-generation mechanism exists | bold lead-in | yes | colon closes bold span, content follows on same line | C1 |
| Trade-offs acknowledged: accepts near-term optionality cost; flip test named | bold lead-in | yes | colon closes bold span, content follows on same line | C4 |
| Pre-check: head C1(LOW), C2(MEDIUM), C3(LOW), C4(LOW) | bold lead-in | yes | Pre-check line is a claim per R11, cited by chains its own head names | C1, C2, C3, C4 |
| Confidence: LOW — corroborated by three lines of reasoning, capped by unverified inputs | bold lead-in | yes | colon closes bold span, content follows on same line | C1, C2, C3, C4 |

Scan complete: 4 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per
construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Whether this company should commit now to adding a free tier to its B2B SaaS
product given an acquisition model (outbound sales + referral) that includes no mechanism for
generating or converting free signups, and if not now, what specific, verifiable conditions
would make that decision correct."
Band: **Rigorous**
Justification: the statement names the actual decision point (funnel-existence conditioned
go/no-go) rather than restating "should we add a free tier," and each success criterion is a
checkable verb+subject+outcome triplet against the Conclusion section (e.g., "the Conclusion
section names concrete, named experiments").

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan): "C1 | 4 (conclusion) | competitor parity is not,
on its own, a load-bearing reason | yes — competitors' free-tier value derives primarily from
their funnel... | yes (A-14)."
Band: **Rigorous**
Justification: all 17 rows use the four-type scheme with prescribed-treatment vocabulary and a
token-led Verdict cell with specific justification; at least ten rows are Challenge or Discard,
not bare Accept; the Assumption Audit scan is exhaustive over every named chain step and the four
assumptions it surfaced (A-14–A-17) are present in the table with "unverified — flagged"
Verification cells.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6 (6 of 6)" checked against the
Ground Truths list, which carries `?` on exactly GT-1 through GT-6 and no unsuffixed entries.
Band: **Rigorous**
Justification: all six GT-IDs are stable, each carries a specific "unverified: [reason]" note
(not "common knowledge"), the enumeration matches the list exactly, and the
"every unsuffixed GT feeds a HIGH chain" clause is vacuously satisfied since no unsuffixed GT
exists; no Phase-2 Discard-verdict assumption (A-4, A-8, A-10) appears in this list.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan's Table 1): "C1 | GT-2?, GT-5? | yes | n/a | yes | LOW |
no | none" and the remaining three rows, all `Form conforming? = yes`, `Dependency clean? = yes`.
Band: **Rigorous**
Justification: every chain block conforms to the scan (no malformed rows), every surfaced
assumption carries an inline `[Assumes: A-N]` tag matching a table row, Abandoned Reasoning
documents four specific dead ends (not vague reasons), and Dead End 1 explicitly names and
rejects using an external conversion-rate benchmark as direct analogical evidence.

**Criterion 5: Validate**
Quoted span: "Capped at LOW by C1 (lowest-rated chain on this head); also carries GT-6?
unverified directly" (C3's confidence line) and the adversarial pass record's five parts, all
present with content (Recompute, Sensitivity, Rival, Pre-Mortem, Falsification).
Band: **Rigorous**
Justification: every chain's band matches what its own Inputs/Inference/Rivals axes license
(per the self-audit scan's Band column), no chain with a GT-N? input is rated HIGH, every chain
is rated no higher than the lowest-rated chain its head cites (C3, C4 both capped at LOW via
C1), and the adversarial pass record is complete rather than a weakest-link paragraph alone.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan's Table 2): "Recommended approach: do not add a free tier
now; run experiments | bold lead-in | yes | ... | C4" and the remaining four rows, all citing a
chain.
Band: **Rigorous**
Justification: every section-6 claim (including the Pre-check and Confidence lines) cites a
named section-4 chain, no new reasoning is introduced in section 6 that was not established in
section 4, and the Key Insight (the funnel-existence variable, not the abstract merit of a free
tier) is a non-obvious finding distinct from the Recommended approach rather than a restatement
of it.

**Gate result:** 6 of 6 criteria Rigorous. No criterion Absent; zero criteria Hand-wavy. Both
clearing conditions met on the first pass — no Fix/Repeat loop and no bounded re-entry edge were
required.
# First-Principles Analysis: Should We Add a Free Tier?

## 1. Problem Essence

**Core problem:** Whether this company should commit now to adding a free tier to its B2B SaaS
product, given an acquisition model (outbound sales plus referral) that includes no mechanism for
generating or converting free signups, and — if not now — what specific, verifiable conditions
would make that decision correct.

**Success criteria:**
1. The Conclusion section states a definite decision (yes / no / conditional) on adding a free
   tier now.
2. The Conclusion section names the specific chain(s) establishing whether "competitors have a
   free tier" is load-bearing for that decision, rather than treating competitive parity as
   self-evidently sufficient.
3. The Conclusion section names concrete, specific experiments — not generic advice — that would
   de-risk the decision before any full commitment.
4. The Conclusion section's confidence rating accounts for every unverified ground truth the
   recommendation rests on, and names what would resolve each one.

---

## 2. Assumptions Table

### Inversion pass (companion technique, applied here because the natural first-read conclusion —
"we lack a funnel, so don't bother" — felt too clean and the assumption set behind it looked thin)

**Claim inverted:** "Not adding a free tier now is the correct decision" → inverted to "adding a
free tier now would in fact be the correct move, and NOT adding one is the costly error."
Failure-guaranteeing conditions enumerated for the inverted claim, each reduced to a necessary
precondition and tagged for load-bearing status:

1. The market has fast-forming network effects or lock-in, so any delay in offering self-serve
   access permanently forecloses that segment to a later entrant. → Precondition **A-11**
   (load-bearing: if true, it could override the funnel-gap finding entirely).
2. Latent bottom-up/PLG demand exists for this product that outbound/referral is structurally
   blind to, and only a free offer — even without heavy marketing — would surface it. →
   Precondition **A-12** (load-bearing: directly tests whether C1's funnel-gap framing is even
   the right model for this product).
3. The true marginal cost per free user is low enough that volume isn't economically painful,
   making the cost-structure concern overstated. → Precondition **A-13's narrower cousin, folded
   into A-5** (load-bearing: caps how bad C2's unit-economics indeterminacy actually is).
4. The cost of losing competitive mindshare during a delay exceeds the cost of a hasty,
   funnel-less rollout. → Precondition **A-13** (load-bearing: this is the time-pressure case
   for acting now rather than diligence-first).

None of A-11, A-12, or A-13 is verified false — which is exactly why the Conclusion below is
conditional and experiment-gated rather than an unconditional "never." See §5, Dead End 3.

### Classified Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: Competitors having a free tier is itself a sufficient reason for us to add one | convention | explicitly challenge the convention before accepting it | Challenge — the mechanism (self-serve funnel) that makes competitors' free tiers valuable is absent here (GT-2?); mimicry alone does not transfer the outcome (chain C1) | unverified — flagged |
| A-2: A free tier will generate meaningful top-of-funnel signups for us | untested belief | verify, or flag as unverified | Challenge — directly contradicted by GT-2? (no inbound/self-serve motion exists today) (chain C1) | unverified — flagged |
| A-3: A workable free-to-paid conversion rate exists for our product/market | untested belief | verify, or flag as unverified; do not substitute an external industry benchmark (see §5 Dead End 1) | Challenge — explicitly speculative per GT-4?; treated algebraically as a breakeven requirement rather than assumed (chain C2) | unverified — flagged |
| A-4: Free users impose zero or negligible marginal cost | untested belief | verify | Discard — directly contradicted by GT-3? (Finance: costs scale with total active users) | unverified — flagged; superseded by GT-3? |
| A-5: Marginal annual cost per free active user (C_f) has no company-specific measurement, so it is bracketed at $50-$600/year spanning a lightweight metered-API profile to a heavier compute/support-touch profile | untested belief | flag as unverified and bracket per the Estimate procedure rather than asserting a point value | Challenge — a defensible range, not a measurement; the true figure could fall outside it either way (chain C2) | unverified — flagged; closed by Experiment #3 |
| A-6: A free tier will not compress or erode the ~$10,000/team ACV anchor for the existing enterprise motion | untested belief, stakes-escalated (threatens the pricing basis for 100% of current ARR) | push toward verified status; verify via second-order analysis and direct customer signal | Challenge — no evidence either way; a load-bearing second-order risk (chain C3) | unverified — flagged; closed by Experiment #4 |
| A-7: The current support team can absorb free-tier ticket and signup volume without new hires or tooling | current constraint | record the expiry conditions | Challenge — true only until low-touch support tooling/staffing exists; expires once a self-serve KB, tiered ticketing, or community support is built | unverified — flagged (feeds C3 via GT-6?) |
| A-8: Self-serve signup, billing, and onboarding infrastructure exists or is trivial to add | current constraint | record the expiry conditions | Discard — directly contradicted by GT-2? (no self-serve/inbound channel exists today); expires once that infrastructure investment is deliberately made | unverified — flagged |
| A-9: Outbound sales reps' motion is unaffected by the presence of a public free tier | untested belief | verify via second-order analysis | Challenge — second-order reasoning shows plausible deal-stalling and seat-shadowing risk (chain C3) | unverified — flagged; closed by Experiment #2 |
| A-10: A full, forever-free, publicly-discoverable tier is the only way to test free-tier economics | convention | explicitly challenge | Discard — smaller, reversible experiments test the same economics with far less exposure (feeds the must-have knockout in chain C4) | unverified — flagged |
| A-11 (inversion, Precondition A): Our market has fast-forming lock-in such that any delay permanently forecloses the self-serve segment | untested belief | verify via competitive teardown | Challenge — no evidence either way; the live rival named on chain C1's confidence line | unverified — flagged; closed by Experiment #5 |
| A-12 (inversion, Precondition B): Latent bottom-up/PLG demand exists that outbound/referral is structurally blind to | untested belief | verify via a self-serve starter-tier experiment | Challenge — no evidence either way | unverified — flagged; closed by Experiment #1 |
| A-13 (inversion, Precondition D): The cost of competitive mindshare loss from delay exceeds the cost of a hasty, funnel-less rollout | untested belief | verify via competitive teardown and ongoing monitoring | Challenge — no evidence either way; the fastest-moving risk per the pre-mortem's Cluster D | unverified — flagged; closed by Experiment #5, sequenced first |
| A-14 (surfaced in Assumption Audit, chain C1 step 4): Competitors' free-tier value derives primarily from their self-serve funnel, not from product-inherent virality or brand power independent of any funnel | untested belief | verify via competitive teardown | Challenge — plausible but unconfirmed; if false, chain C1's conclusion weakens | unverified — flagged; closed by Experiment #5 |
| A-15 (surfaced in Assumption Audit, chain C3 step 2): No technical or contractual barrier currently prevents a paying account from splitting usage across a paid seat and a separate free account | current constraint | record the expiry conditions — expires once seat-pooling or account-linking restrictions are added | Challenge — plausible given no stated barrier, but unverified against the actual product's account model | unverified — flagged |
| A-16 (surfaced in Assumption Audit, chain C3 step 5): Once a cost center is politically embedded, reversing or resourcing it later is harder than deciding deliberately upfront | convention (organizational-behavior pattern, not a hard law) | explicitly challenge before relying on it | Accept — a reasonable heuristic consistent with the pre-mortem's Cluster A finding; low-stakes relative to the main economic claims | unverified — flagged |
| A-17 (surfaced in Assumption Audit, chain C4 step 2): The locked trade-off weights reflect this company's actual strategic priorities, not merely the analyst's judgment | untested belief | verify with the company's actual decision-makers before acting | Challenge — a reasoned default calibrated to the stipulated fact that the enterprise motion generates 100% of current ARR; not confirmed with leadership | unverified — flagged |

---

## 3. Ground Truths

All six ground truths below are the "known facts" supplied directly in the prompt. None names an
external document, URL, or file this analysis could open — they are the company's own internal
figures and characterizations, stated as given context rather than cited to a source. Per the
Input Contract, supplying a fact this way does not discharge verification: each therefore carries
the `?` suffix and an "unverified" provenance label, and none is independently read-at-source by
this analysis.

- **GT-1?** Current ARR is $2.4M from 240 paying teams, averaging ~$10,000/team/year (ACV) —
  unverified: user-stipulated internal business metric; no financial report, invoice system, or
  billing export was opened by this analysis.
- **GT-2?** The current customer acquisition channel is outbound sales and referrals only; no
  self-serve inbound channel or motion exists today — unverified: user-stipulated characterization
  of current acquisition channels; no CRM, analytics, or traffic-source data was opened.
- **GT-3?** Finance has confirmed that infrastructure and support costs scale with total active
  users (free and paid), not just paying users — unverified: user-stipulated Finance determination;
  no cost model, cloud-billing breakdown, or finance report was opened by this analysis.
- **GT-4?** No internal freemium pilot has ever been run, so no internal free-to-paid conversion
  rate exists for this product/market, and any assumed rate would be speculative — unverified:
  user-stipulated absence of pilot data; no experimentation log was reviewed (there being, by the
  claim's own nature, no source to open for an absence of data).
- **GT-5?** All known competitors currently have a free tier — unverified: user-stipulated
  competitive-landscape claim; no competitor pricing page, product site, or review was examined by
  this analysis.
- **GT-6?** The support team is organized and staffed for high-touch service of ~240 paying
  accounts, not for high-volume, low-touch support — unverified: user-stipulated characterization
  ("likely not staffed") of support-team posture; no staffing plan or ticket-volume data was opened.

**Provenance summary:** `?`-marked: GT-1, GT-2, GT-3, GT-4, GT-5, GT-6 (6 of 6). No unsuffixed
ground truth exists in this analysis, so no HIGH-confidence chain exists and no read-at-source
enumeration applies — every derivation chain in section 4 is capped at MEDIUM or below by this
fact alone, independent of any inference-quality issue. No assumption that received a Discard
verdict in section 2 (A-4, A-8, A-10) appears in this list.

---

## 4. Derivation Chains

### Conclusion C1: "Competitors have a free tier" is not, by itself, a load-bearing reason to add one now

GT-2? (no self-serve/inbound motion exists today) + GT-5? (all known competitors have a free tier)
→ a free tier's acquisition value depends on a self-serve/inbound funnel that discovers, onboards, and meters free users at scale
→ the absence of that funnel here means the mechanism that makes a competitor's free tier valuable is exactly the piece this company lacks
→ copying the pricing SKU without the funnel that gives the SKU its acquisition value only replicates the SKU, not the outcome
→ the bare fact of competitor parity is therefore not, on its own, a load-bearing reason to add a free tier now *[Assumes: A-14 — competitors' free-tier value derives primarily from their self-serve funnel, not from product-inherent virality or brand power independent of any funnel]*

**Pre-check:** head GT-2?, GT-5? · ?-marked: GT-2?, GT-5? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — three things are outstanding on this chain, not one. Inputs: both GT-2? and
GT-5? are unverified (verification: an internal traffic/signup-source audit for GT-2?; Experiment
#5's competitive teardown for GT-5?). Inference: the final hop rests on an unpriced `[Assumes:
A-14]` premise — if competitors' free-tier value in fact comes mainly from brand or inherent
virality rather than their funnel, this chain's conclusion weakens, and that failure mode is not
yet priced (closed by Experiment #5). Rivals: a live, unresolved rival survives — competitors'
free tiers may function as sales-assisted trial tools rather than organic demand-gen, in which
case the funnel gap matters less (see Adversarial pass, Rival); nothing in this analysis settles
it yet (closed by Experiments #2 and #5).

### Conclusion C2: The free tier's unit economics are formally indeterminate today, not merely "probably good" or "probably bad"

GT-1? (ACV ~$10,000/team/year) + GT-3? (costs scale with total active users, not just paying ones) + GT-4? (no internal conversion data exists)
→ because cost is a function of total active users, every free signup adds a determinate, positive marginal cost regardless of whether it ever converts
→ no company-specific measurement of that marginal cost exists, so it is bracketed at $50-$600 per free active user per year *[Assumes: A-5 — spanning a lightweight metered-API profile to a heavier compute/support-touch profile]*
→ dividing the bracket by the $10,000 ACV gives a breakeven free-to-paid conversion rate of roughly 0.5% to 6%, before any actual conversion number is known
→ because GT-4? establishes no internal conversion rate exists, the expected value of a free signup cannot be estimated with any confidence today
→ therefore the free tier's unit economics are indeterminate today, not merely probably-good or probably-bad
→ resolving that indeterminacy requires first-principles measurement of our own figures, not a borrowed industry benchmark — the concrete steps are named in §6

**Pre-check:** head GT-1?, GT-3?, GT-4? · ?-marked: GT-1?, GT-3?, GT-4? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — only the Inputs axis is short here. All three head ground truths are
unverified: GT-1? (verification: an actual ARR/ACV export from billing), GT-3? (verification:
Experiment #3's direct cost-accounting breakdown), GT-4? (verification: Experiments #1/#2's
pilot data). Inference is not short: the `[Assumes: A-5]` cost bracket is priced on this line — if
the true C_f fell outside the $50-$600 bracket, the breakeven percentage would shift but the
endpoint itself (economics are indeterminate without a measured conversion rate) would still
hold; a higher-than-bracketed C_f would, if anything, strengthen rather than undermine that
conclusion. Rivals is clean: any claim that unit economics are clearly favorable or clearly
unfavorable would itself require the same missing data this chain says is missing, so
indeterminacy is the most defensible reading and no live rival contests it.

### Conclusion C3: Launching a free tier without the missing preconditions works against the decision's own success criterion

C1 (LOW — competitor parity not load-bearing absent a funnel) + C2 (MEDIUM — unit economics indeterminate) + GT-6? (support team sized for high-touch service of ~240 accounts)

*Hops 1-3 apply the actor lens; hops 4-5 apply the time lens, per the second-order procedure's two
required lenses.*

→[2nd] if a public free tier were launched despite the funnel gap C1 identifies, outbound reps' prospects would gain a no-cost alternative mid-funnel, creating an incentive for deals to stall as prospects self-serve instead of signing
→[2nd] existing paying teams could redistribute casual-user seats into shadow free accounts on the same team, eroding realized ACV from the installed base with no offsetting support-cost benefit *[Assumes: A-15 — no technical or contractual barrier currently prevents an account from splitting usage across a paid seat and a separate free account]*
→[2nd] the support-ticket volume from any meaningful free-user base would land on a team GT-6? describes as sized for high-touch service of ~240 accounts, degrading SLA for the paying accounts that generate all current ARR
→[2nd] in the near term these effects would surface mostly as cost and risk with no offsetting funnel benefit, since organic self-serve discovery takes many months to ramp even for a well-suited product
→[3rd] sustained for 18+ months without a deliberate self-serve investment, the free tier would normalize internally as a cost center that is politically hard to shut down and operationally under-resourced either way *[Assumes: A-16 — once a cost center is politically embedded, reversing or resourcing it later is harder than deciding deliberately upfront]*
→ none of these effects contradicts a ground truth, but each works against growing ARR efficiently without harming the core enterprise motion, reinforcing rather than overturning C1 and C2

**Pre-check:** head C1 (LOW), C2 (MEDIUM), GT-6? · ?-marked: GT-6? · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped at LOW by C1, the lowest-rated chain this head cites (C1's own
unresolved Inputs/Inference/Rivals gaps are inherited here, not re-explained — see C1's confidence
line). Independently, GT-6? is unverified (verification: a support-capacity review — actual ticket
volume per account tier and current tooling/staffing plan). Two further hops carry their own
unpriced `[Assumes]` premises (A-15, A-16); A-15 is closed by reviewing the product's actual
account/seat model, A-16 is a low-stakes organizational heuristic accepted in section 2 without
separate verification.

### Conclusion C4: Run bounded de-risking experiments now; do not launch any version of a free tier yet

**Trade-off analysis (supporting detail — the full matrix, collapsed into this chain's head per
the trade-off-to-chain conversion rule).**

*Options, including the status quo:* (1) full public free tier now, matching competitors; (2) do
nothing; (3) a scoped, sales-assisted, usage-capped trial attached only to existing outbound
leads (not publicly discoverable); (4) defer the full decision and invest first in minimal
self-serve infrastructure (landing page, lightweight onboarding, metering/billing) paired with
the bounded experiments named in §6, then revisit.

*Must-have knockout (applied before scoring):* a viable option must have some mechanism for
generating free signups, or be explicitly scoped to avoid needing one. Option 1 fails this
knockout outright — under the current outbound/referral-only acquisition model (GT-2?) there is
no mechanism to generate signups, so a full public free tier would sit nearly idle at best or
leak existing outbound-sourced prospects into a free alternative at worst (chain C3). Option 1 is
therefore **knocked out, not scored** (see §5, Dead Ends 2 and 4).

*Criteria, locked weights (1-5), and anchors for the three surviving options:*
cost exposure (w=4; 1=high uncontrolled new cost now, 5=none), pricing-anchor protection (w=5;
1=severe compression risk to the $10k ACV, 5=none), sales-motion protection (w=5; 1=high
cannibalization risk, 5=none), support-burden fit (w=3; 1=far exceeds current capacity, 5=fits
comfortably), strategic optionality (w=3; 1=forecloses a future low-CAC channel, 5=builds toward
it), competitive signaling (w=1; 1=looks weak vs. competitors, 5=matches/exceeds them).

*Scores (cited to GT-2?, GT-3?, GT-6?, and chains C1-C3 as the factual basis):* status quo scores
5,5,5,5,1,2; scoped trial scores 4,4,4,4,3,4; invest-first scores 2,5,5,4,5,2.

GT-2? (no inbound/self-serve motion) + GT-3? (costs scale with active users) + GT-6? (support team sized for high-touch) + C1 (LOW) + C2 (MEDIUM) + C3 (LOW)
→ the must-have knockout rules out a full public free tier today because no mechanism exists to generate free signups under the current acquisition model, independent of its weighted score
→ among the three surviving options, the weighted trade-off gives status quo 90, invest-first-then-reconsider 87, and scoped sales-assisted trial 81, with the gap driven almost entirely by near-term cost exposure versus strategic optionality *[Assumes: A-17 — the locked trade-off weights reflect this company's actual strategic priorities, not merely the analyst's judgment]*
→ the flip test shows this ranking inverts with only a ~0.75-point increase in the weight on strategic optionality (from the locked value of 3), so the result is a genuine near-tie rather than a clear winner
→ because invest-first matches status quo's protection of the $10k ACV anchor and the outbound sales motion while making deliberate, bounded progress on the one missing precondition, it is the more defensible path despite its slightly lower raw score
→ the recommended action now is to run the named de-risking experiments rather than launch any version of a free tier, and to revisit the full decision once self-serve pull and true unit-cost data exist

**Pre-check:** head GT-2?, GT-3?, GT-6?, C1 (LOW), C2 (MEDIUM), C3 (LOW) · ?-marked: GT-2?, GT-3?, GT-6? · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — capped at LOW by C1 and C3, the lowest-rated chains this head cites (their
own gaps — C1's unverified GT-2?/GT-5? plus live rival; C3's inherited cap plus unverified GT-6? —
are not re-explained here; see their own confidence lines). Independently, this chain's own hop 2
rests on an unpriced `[Assumes: A-17]` premise about weight validity (verification: confirm the
locked weights with actual company decision-makers before acting), and the trade-off itself is a
near-tie (flip distance ≈0.75 of one weight-point), which is a Rivals-axis-style shortfall on the
"invest-first beats status quo" sub-claim even though the must-have knockout on Option 1 is not in
doubt. All of these close via the experiments named in §6.

---

## 5. Abandoned Reasoning

### Dead End: Industry-benchmark conversion rate as a substitute for internal data

**What was tried:** considered using a commonly-cited B2B freemium conversion-rate range borrowed
from public SaaS commentary (e.g., a low-single-digit-percent figure) to compute the expected
value of a free signup directly, instead of leaving the unit economics as an algebraic bracket.

**Why abandoned:** this is reasoning by analogy from other companies' products and markets, which
the methodology prohibits as direct evidence. GT-4? explicitly establishes that this company has
no internal conversion data and that any assumed rate would be speculative; importing an external
benchmark would silently reintroduce exactly the speculation the input facts flagged, and the
benchmark's applicability to this specific product and market is itself untested.

**What it ruled out:** rules out treating any single "expected conversion rate" as an input to
this analysis; replaced by the breakeven-bracket framing in chain C2, which states what
conversion rate would be needed rather than asserting what conversion rate will occur.

### Dead End: Full public free tier now, matching competitors

**What was tried:** evaluated launching a full, forever-free, self-serve-discoverable tier
immediately, mirroring the competitive landscape described in GT-5?.

**Why abandoned:** fails the trade-off's must-have knockout in chain C4 — there is no mechanism
to generate free signups under the current outbound/referral-only acquisition model (GT-2?), so
the option is structurally non-viable, not merely low-scoring, until that precondition is built.
Scoring it alongside viable options would let a weighted total out-vote this hard constraint.

**What it ruled out:** rules out treating "competitors have one" as sufficient justification on
its own (chain C1); this is the first rival to the headline conclusion, ruled out by the must-have
knockout named on chain C4's first hop.

### Dead End: Permanent rejection of a free tier, no further action

**What was tried:** considered concluding "never add a free tier" outright, stopping the analysis
at the cost-mismatch (chain C2) and funnel-gap (chain C1) findings.

**Why abandoned:** the inversion pass (assumptions A-11, A-12, A-13) surfaced genuine scenarios —
fast-forming competitive lock-in, latent bottom-up demand, or a sales-cycle-shortening effect —
under which not adding a free tier would be the costly mistake; none of these preconditions is
verified false, so an unconditional "never" is no better supported than an unconditional "yes."
The trade-off's own numbers (status quo 90 vs. invest-first 87, flip distance ≈0.75 of one
weight-point) show this is a genuine near-tie, not a case where inaction is clearly superior.

**What it ruled out:** rules out treating the cost/funnel findings as grounds for a permanent,
un-revisitable "no"; this is the second rival to the headline conclusion, resolved instead into
the conditional, experiment-gated recommendation in chain C4 rather than either extreme.

### Dead End: Scoring the knocked-out full-free-tier option numerically instead of excluding it

**What was tried:** initially included "full public free tier now" as a fourth scored option in
the weighted trade-off matrix alongside status quo, the scoped trial, and invest-first.

**Why abandoned:** the trade-off procedure requires must-have knockouts to be applied before
scoring, specifically to prevent a high weighted total on secondary criteria (e.g., competitive
signaling) from out-voting a hard structural failure (no signup-generation mechanism at all).
Scoring it risked exactly that outcome.

**What it ruled out:** rules out any trade-off result in this analysis that would have numerically
favored the full-free-tier option; confirms the knockout-then-score sequencing actually used in
chain C4.

---

## 6. Conclusion

**Recommended approach:** Do not add a free tier now. Instead, run a time-boxed (one-quarter),
single-owner set of five de-risking experiments, and revisit the full free-tier decision against
that evidence (chain C4): (1) stand up a minimal self-serve signup flow for a low-priced,
non-free "starter" tier to test whether any self-serve signups materialize at all before any free
price point is introduced; (2) run a sales-assisted, time-boxed, usage-capped free trial offered
only to existing outbound-pipeline leads (not publicly discoverable), measuring impact on deal
cycle length and close rate against a control group; (3) have Finance/Infra measure the true
marginal annual cost per active user directly, replacing the assumed $50-$600 bracket with a
measured figure; (4) survey existing paying teams and recently lost deals on price sensitivity and
whether a free tier would have changed their purchase path; (5) run a competitive teardown of how
2-3 named competitors actually use their free tiers (demand-gen engine vs. sales-assist trial
tool), sequenced first and run fast, per the pre-mortem's Cluster D disposition.

**Key insight:** The decisive variable is not whether a free tier is a good idea in the abstract,
and not what conversion rate it might achieve — it is whether any mechanism exists to generate
free signups at all. Without the self-serve/inbound funnel that gives a free tier its acquisition
value elsewhere, "competitors have one" describes the effect of a system this company has not
built, not a cause worth copying on its own (chain C1).

**Trade-offs acknowledged:** This path accepts a near-term strategic-optionality cost relative to
launching immediately — the trade-off's flip test shows the invest-first path loses to pure
inaction by only 3 weighted points, and would win outright if strategic optionality were weighted
roughly one point higher (chain C4). It also accepts that if competitor lock-in is accelerating
faster than assumed — an unresolved rival on chain C1 — a quarter of diligence has a real
opportunity cost, which is exactly why the competitive teardown is sequenced first among the
experiments rather than last (chain C4).

**Pre-check:** head C1 (LOW), C2 (MEDIUM), C3 (LOW), C4 (LOW) · ?-marked: none directly (all
GT-N? inputs are routed through the cited chains) · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — the directional recommendation (not now; run bounded experiments; revisit)
is corroborated by three independent lines of reasoning that converge in chain C4: the funnel-gap
finding in chain C1, the indeterminate unit economics in chain C2, and the second-order
cannibalization/support/anchor risk in chain C3. The formal confidence label is nonetheless capped
at LOW because chain C1 rests on two unverified ground truths (GT-2?, GT-5?) and carries a live,
unresolved rival (competitors' free tiers may function as sales-assist tools rather than organic
demand-gen); chain C3 inherits that cap and additionally rests on an unverified GT-6?; and chain
C4's own invest-first-vs-status-quo result is a near-tie. Each gap is closable: GT-2?/GT-5? by
Experiment #5 and an internal traffic-source audit; GT-6? by a support-capacity review; C1's live
rival by Experiments #2 and #5; and C2's narrower MEDIUM rating by Experiment #3 and the
conversion data Experiments #1/#2 would produce. The LOW label reflects how much about this
specific company's situation is still unmeasured, not doubt about the direction of the argument.
