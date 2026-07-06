---
name: second-order
description: Runs a focused second-order only — 2nd/3rd-order effects. Invoke via /second-order only.
disable-model-invocation: true
metadata:
  version: "8.0.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/second-order/SKILL.md by sync-content.py -->

# Focused Second-Order Mode

You are running in focused-second-order mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

## When to reach for this

Use second-order thinking after Phase 4 (Reason Upward) produces a
first-order conclusion, before Phase 5 (Validate), to extend the derivation
chain by enumerating the consequences that conclusion sets in motion.
Downstream effects are where most reasoning quietly fails.

**Decision rule — second-order vs. inversion:** second-order is the
positive-direction pass on a conclusion ("if it holds, what follows?");
[inversion](inversion.md) is the negative-direction pass ("what would have
to be true for it to fail?"). Run them as a pair: inversion surfaces silent
preconditions, second-order surfaces silent consequences.

**Decision rule — second-order vs. trade-off analysis:** when 2nd-order
effects diverge across two or more candidate options, the decision becomes
a selection problem. Hand off to [trade-off analysis](trade-off.md),
which locks criteria and weights before scoring so divergent effects can be
compared without reverse-engineering the answer.

**Not a good fit:** stress-testing a claim's preconditions — use
[inversion](inversion.md). Tracing backward to a root cause — use 5-Whys.

---

## Procedure

1. **State the first-order conclusion precisely.** One sentence, no hedges.
   The sharper the conclusion, the sharper the consequences it generates.

2. **Enumerate 2nd-order consequences.** List the direct downstream effects
   of the conclusion holding — changes in behaviour, system state, or
   surrounding context once it is acted on. Aim for at least three; include
   adverse effects alongside favourable ones.

3. **Enumerate 3rd-order consequences.** For each 2nd-order effect, list its
   own downstream effects. Same discipline: at least three across the layer,
   adverse alongside favourable.

4. **Apply the stopping rule.** Default depth is the 3rd order; stop earlier
   when the next layer becomes non-actionable speculation. Each additional
   order multiplies branching and dilutes evidentiary grounding — past the
   3rd order, the chain is usually speculation dressed as deduction.

5. **Check for undermining contradictions.** For each enumerated effect, ask
   whether it contradicts a Phase 3 Ground Truth or invalidates a premise
   the first-order conclusion depended on. Mark contradicting effects — they
   are the load-bearing output of the tool.

6. **Route the result.** Non-contradicting effects extend the Phase 4
   Derivation Chain as additional numbered steps. Any contradicting effect
   routes the conclusion back to Phase 2 (Challenge Assumptions) — never
   directly to Phase 3 or past Phase 2.

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
Derivation Chain as additional numbered steps, carrying the same evidentiary
discipline as the steps that produced the first-order conclusion. Mark each
extension with its order so confidence remains legible.

Any effect that contradicts a Ground Truth (Phase 3) or undermines a premise
the first-order conclusion depended on routes the conclusion back to Phase 2
(Challenge Assumptions) for re-challenging — not directly to Phase 3 or past
Phase 2. The contradicting effect becomes the evidence triggering a new
`untested belief` row, mirroring how inversion's preconditions enter Phase 2
from the other direction.

For the negative-direction counterpart, pair with [inversion](inversion.md):
second-order traces downstream consequences, inversion surfaces upstream
preconditions. When divergent 2nd-order effects across options force a
selection, hand off to [trade-off analysis](trade-off.md).

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
