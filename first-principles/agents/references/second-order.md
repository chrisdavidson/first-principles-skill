<!-- GENERATED — DO NOT EDIT. Source: shared/references/second-order.md. Regenerate via: scripts/sync-content.py --write. -->

# Second-Order Thinking

> A positive-direction extension of a *conclusion*. Following Howard Marks's
> "Second-Level Thinking" chapter in *The Most Important Thing*, this tool
> asks not "is the conclusion right?" but "what follows from it — and from
> what follows?" The downstream effects extend the Phase 4 Derivation Chain;
> any effect that contradicts a Ground Truth routes the conclusion back to
> Phase 2 for re-challenging.

---

- [When to reach for this](#when-to-reach-for-this)
- [Procedure](#procedure)
- [Worked mini-example](#worked-mini-example)
- [Failure modes](#failure-modes)
- [Handoff](#handoff)

---

## When to reach for this

Use second-order thinking after Phase 4 (Reason Upward) produces a
first-order conclusion, before Phase 5 (Validate), to extend the derivation
chain by enumerating the consequences that conclusion sets in motion.
Downstream effects are where most reasoning quietly fails.

**Decision rule — second-order vs. inversion:** second-order is the
positive-direction pass on a conclusion ("if it holds, what follows?");
[inversion](${CLAUDE_PLUGIN_ROOT}/agents/references/inversion.md) is the negative-direction pass ("what would have
to be true for it to fail?"). Run them as a pair: inversion surfaces silent
preconditions, second-order surfaces silent consequences.

**Decision rule — second-order vs. trade-off analysis:** when 2nd-order
effects diverge across two or more candidate options, the decision becomes
a selection problem. Hand off to [trade-off analysis](${CLAUDE_PLUGIN_ROOT}/agents/references/trade-off.md),
which locks criteria and weights before scoring so divergent effects can be
compared without reverse-engineering the answer.

**Not a good fit:** stress-testing a claim's preconditions — use
[inversion](${CLAUDE_PLUGIN_ROOT}/agents/references/inversion.md). Tracing backward to a root cause — use 5-Whys.

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

For the negative-direction counterpart, pair with [inversion](${CLAUDE_PLUGIN_ROOT}/agents/references/inversion.md):
second-order traces downstream consequences, inversion surfaces upstream
preconditions. When divergent 2nd-order effects across options force a
selection, hand off to [trade-off analysis](${CLAUDE_PLUGIN_ROOT}/agents/references/trade-off.md).
