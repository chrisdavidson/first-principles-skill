---
name: second-order
description: Runs a focused second-order only — 2nd/3rd-order effects. Invoke via /second-order only.
disable-model-invocation: true
metadata:
  version: "9.12.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/second-order/SKILL.md by sync-content.py -->

# Focused Second-Order Mode

You are running in focused-second-order mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

## When to reach for this

Use second-order thinking after Phase 4 (Reason Upward) produces a
first-order conclusion, before Phase 5 (Validate), to extend the derivation
chain by enumerating the consequences that conclusion sets in motion.
Downstream effects are where most reasoning quietly fails.

**Decision rule — second-order vs. inversion:** second-order is the
positive-direction pass on a conclusion ("if it holds, what follows?");
[inversion](${CLAUDE_PLUGIN_ROOT}/skills/inversion/SKILL.md) is the negative-direction pass ("what would have
to be true for it to fail?"). Run them as a pair: inversion surfaces silent
preconditions, second-order surfaces silent consequences.

**Decision rule — second-order vs. trade-off analysis:** when 2nd-order
effects diverge across two or more candidate options, the decision becomes
a selection problem. Hand off to [trade-off analysis](${CLAUDE_PLUGIN_ROOT}/skills/trade-off/SKILL.md),
which locks criteria and weights before scoring so divergent effects can be
compared without reverse-engineering the answer.

**Not a good fit:** stress-testing a claim's preconditions — use
[inversion](${CLAUDE_PLUGIN_ROOT}/skills/inversion/SKILL.md). Tracing backward to a root cause — use 5-Whys.

---

## Procedure

1. **State the first-order conclusion precisely.** One sentence, no hedges.
   The sharper the conclusion, the sharper the consequences it generates.

2. **Enumerate 2nd-order consequences through two lenses.** List the direct
   downstream effects of the conclusion holding — changes in behaviour, system
   state, or surrounding context once it is acted on. Walk both lenses rather
   than counting to a number:

   - **The actor lens.** Who changes what they do once this holds? Name the
     parties — the people executing it, the people living with the result, the
     people paying for it, and anyone whose incentives now point somewhere new,
     including a competitor or an adversary. Effects that arrive through *other
     people reacting* are the ones a single-perspective pass misses, and they
     are usually the expensive ones.
   - **The time lens.** What is true immediately, what after a few cycles, and
     what once this has been in place long enough to be assumed? Many
     second-order effects are invisible at one horizon and dominant at another —
     a cost that is trivial per week and structural per year.

   Cover both lenses and include adverse effects alongside favourable ones. The
   lenses are coverage checks, not quotas: a pass that finds two real effects
   across both lenses is complete, and one padded to a count is not.

3. **Enumerate 3rd-order consequences.** For each 2nd-order effect, list its
   own downstream effects, through the same two lenses. Adverse alongside
   favourable.

4. **Apply the stopping rule.** Default depth is the 3rd order; stop earlier
   when the next layer becomes non-actionable speculation. Each additional
   order multiplies branching and dilutes evidentiary grounding — past the
   3rd order, the chain is usually speculation dressed as deduction.

5. **Check for undermining contradictions.** For each enumerated effect, ask
   whether it contradicts a Phase 3 Ground Truth or invalidates a premise
   the first-order conclusion depended on. Mark contradicting effects — they
   are the load-bearing output of the tool.

6. **Check the effects against the decision's own success criteria.** Name what
   this decision is *for* — the outcome it is meant to produce — and ask of each
   enumerated effect whether it works against that outcome. An effect can be
   perfectly consistent with every Ground Truth and still defeat the purpose:
   the flag system ships faster and makes the codebase unreadable, the incentive
   raises the reported number and not the thing it proxies for. Step 5 catches
   contradictions with what is *true*; this catches contradictions with what is
   *wanted*, and nothing else in the methodology looks for them.

   An effect that undermines the success criteria is reported as such even when
   the conclusion survives on the evidence. If the success criteria were never
   stated, say so — that is itself the finding, and it routes back to Phase 1.

7. **Route the result.** Non-contradicting effects extend the Phase 4
   Derivation Chain as additional order-marked steps (`→[2nd]`, `→[3rd]`).
   Any contradicting effect routes the conclusion back to Phase 2
   (Challenge Assumptions) — never directly to Phase 3 or past Phase 2.

**Exit criterion:** Every first-order effect in scope has been carried to at least
its second order through both the actor and time lenses, each derived effect carries
its order mark, contradicting effects are identified as contradicting, every effect
has been checked against the decision's stated success criteria (or their absence
recorded), and each effect is routed — non-contradicting effects into the Derivation
Chain, contradicting effects back to Phase 2.

---

## Worked mini-example

**First-order conclusion:** "Adopting feature flags for all new product
changes will let us release continuously without coordinating deploys."

- **2nd-order consequences:**
  - Long-lived branches disappear; branch-by-abstraction becomes default
  - Flag-configuration surface grows linearly with in-flight features
  - QA shifts from pre-deploy gates to in-production flag-off verification
- **3rd-order consequences:**
  - Engineers treat flags as permanent config — flag debt accumulates
  - On-call must correlate the active flag set at failure time, not the deployed version alone
  - Analytics must segment every metric by flag state, or aggregates mix behaviours silently
- **Undermining check:** the "flag debt accumulates" effect contradicts the
  Phase 3 Ground Truth that the team retires flags promptly.
- **Revised conclusion:** route back to Phase 2 — the conclusion holds only
  if a flag-retirement policy is verified as an `untested belief`.

---

## Failure modes

**Confusing speculation with deduction at the nth order.** As depth
increases, each step's evidentiary basis weakens; treating a 3rd-order
effect as derived rather than guessed is the most common silent failure.
Mark each layer's evidentiary status and downgrade chain confidence.

**Recursing past actionable depth.** Past the 3rd order — or past where
consequences stop being actionable — additional layers add no decision value
and crowd out attention. Stop when the stopping rule fires.

**Cherry-picking favourable 2nd-order effects while ignoring adverse ones.**
Enumerating only consequences that support the conclusion converts a stress
test into a confirmation exercise. Enumerate adverse effects with the same
discipline as favourable ones.

---

## Handoff

Non-contradicting 2nd- and 3rd-order effects extend the relevant Phase 4
Derivation Chain in place as additional order-marked steps (`→[2nd]`, `→[3rd]`),
carrying the same evidentiary discipline as the steps that produced the
first-order conclusion — the canonical extension form is defined in
output-template.md §4 ("Converting structured-technique outputs into chains").

Any effect that contradicts a Ground Truth (Phase 3) or undermines a premise
the first-order conclusion depended on routes the conclusion back to Phase 2
(Challenge Assumptions) for re-challenging — not directly to Phase 3 or past
Phase 2. The contradicting effect becomes the evidence triggering a new
`untested belief` row, mirroring how inversion's preconditions enter Phase 2
from the other direction.

For the negative-direction counterpart, pair with [inversion](${CLAUDE_PLUGIN_ROOT}/skills/inversion/SKILL.md):
second-order traces downstream consequences, inversion surfaces upstream
preconditions. When divergent 2nd-order effects across options force a
selection, hand off to [trade-off analysis](${CLAUDE_PLUGIN_ROOT}/skills/trade-off/SKILL.md).

## Focused-mode validation

**Check the output against its own completion condition before presenting it.** The
procedure above states one, in whichever form this technique uses — an exit criterion, a
stop test, or an output contract. Read that condition again and confirm the output actually
produced meets every requirement it names, not just the ones that were easiest to satisfy.

**This is a scope-proportionate check, not the six-criterion Self-Audit Gate.** That gate
scores a six-section analysis document; this run produced one technique's output sections,
not six, so walking all six criteria against it would score structure that was never
produced. The larger of the two components: a focused run does not acquire evidence — it
opens no cited source — so a claim resting on a source this run did not open stays marked
rather than being resolved as confirmed.

**Carry the mark forward.** Anything this run could not verify is carried into the output
marked with a `?` rather than dropped or silently asserted as fact.

**Run the technique's own semantic check before declaring the output satisfied.** The
completion condition above is structural — it asks whether the required parts are present.
This asks whether the content holds up. One question, per technique:

- **five-whys** — is each cause counterfactually necessary: would the symptom still have
  happened without it?
- **fishbone** — does each prioritised cause carry an observation that distinguishes it
  from its siblings?
- **inversion** — is each precondition stated as a claim that can be false, and tagged for
  whether the conclusion survives it being false?
- **estimate** — does the bracket's whole width drive the same decision? If the low and
  high ends point different ways, the bracket has not yet answered the question.
- **trade-off** — does the winner survive the smallest weight flip, and is the status quo
  among the options?
- **pre-mortem** — does every fatal or costly cluster carry a tripwire that someone is
  positioned to see?
- **second-order** — has any effect been checked against what the decision is *for*, not
  only against what is true?
- **theoretical-limit** — is the bound the tightest applicable one, and is the demonstrated
  tier an observed figure rather than a calculated one?

A failed semantic check is a `not satisfied` result, not a caveat to attach to a satisfied
one.

**Escalate to the full composer when a `?` becomes load-bearing.** If a claim this run could
not verify turns out to be one the answer does not survive being false — load-bearing in the
validation rubric's sense — stop and say so, in this form:

- `Focused-mode escalation: <the ?-marked claim> is load-bearing - recommend a full analysis`

A focused run acquires no evidence, so it cannot resolve that claim; continuing produces a
confident-looking answer resting on exactly the thing nobody checked. Escalation is the
honest exit, and it is the only case where a focused run should decline to answer in its own
terms. Recommend the escalation; do not silently perform a full analysis instead — the run
was asked for one technique.

**Revise once, then stop.** If the check fails, revise the output and check it again.
Revise at most one time. If it still fails after that pass, present the output with the
gap named rather than revising again.

**End every run with a validation line, without exception.** State exactly one of the
following, verbatim, never silently:

- `Focused-mode validation: satisfied`
- `Focused-mode validation: revised once, now satisfied`
- `Focused-mode validation: not satisfied - <reason>`

Close with the reason this line is unconditional: a silent run is indistinguishable from a
run that skipped the check.

**Then state the residual, on its own line, every time — including after `satisfied`.**
Verbatim:

- `Focused-mode residual: this run opened no cited source, so any ?-marked claim is unverified, not merely uncited.`

This is the one thing the reader of a focused run cannot infer from the output. The
completion-condition check above is a rule *this document* gives the model; the residual is a
fact about the run that its reader needs, and until it is emitted the reader has no way to
tell a focused analysis from a full one that happened to be short. `satisfied` means the
output met its completion condition — never that its claims were verified against a source.

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as candidate inputs for Phase 2. Carry the `?` marks
with it — this run opened no cited source.
