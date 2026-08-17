---
name: pre-mortem
description: Runs a focused pre-mortem only — prospective-hindsight failure analysis. Invoke via /pre-mortem only.
disable-model-invocation: true
metadata:
  version: "8.17.3"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/pre-mortem/SKILL.md by sync-content.py -->

# Focused Pre-Mortem Mode

You are running in focused-pre-mortem mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

## When to reach for this

Use a pre-mortem once a plan has enough specificity to reason about particular
failure modes, but before it is finalised and carries organizational momentum.
Not the right tool for evaluating options (use trade-off analysis) or for tracing
something that already went wrong (use 5-Whys).

---

## Framing

Before any other step, adopt this premise explicitly:

> It is approximately six months from now. This plan has failed — not merely
> underperformed, but failed badly. That outcome is a fact.
> Working backward: what caused it?

This past-tense framing is not rhetorical. It bypasses the optimism bias that
makes forward-looking risk lists generic. Do not skip it or soften it to
"might fail" — the grammatical shift from possibility to accomplished fact is
the mechanism.

---

## Procedure

1. **Restate the premise.** Before writing anything, say or write: "The plan has
   already failed. What caused it?" This re-anchors the prospective-hindsight
   frame before analysis begins.

2. **Write independently.** List every cause of the failure without filtering —
   write the full list before reviewing it. Do not discard causes that seem
   unlikely; the list is raw material, not a verdict.

3. **Interrogate the list adversarially.** Re-read each item and ask: "Would I
   have suppressed this in a group?" Items flagged by that question are often
   the highest-signal findings.

4. **Identify recurring patterns.** Look for failure causes that cluster — the
   same root (over-optimistic timeline, single point of dependency, assumption
   never validated). A cluster is a structural weakness in the plan, not an
   isolated risk.

5. **Act on findings.** Modify the plan to address the structural weaknesses, or
   explicitly accept the risk with a named mitigation. A pre-mortem with no
   downstream plan change was box-ticking.

---

## Example

**Plan:** Host a dinner party for twelve people in two weeks, cooking a full
three-course meal from scratch for the first time at this scale.

**Framing applied:** It is two weeks from now. The dinner party has failed badly.
What caused it?

**Backward-derived failure causes:**
- Underestimated preparation time; last two courses were served an hour late
- A key ingredient unavailable the day before; no substitution plan
- One course required equipment not owned and not sourced in advance
- Two guests had dietary restrictions not asked about until the day of
- Energy depleted by the time guests arrived; host unable to enjoy the evening

**Pattern identified:** Every cause traces back to a single structural weakness —
no dry run at smaller scale and no contingency check before commitment. The plan
assumed novelty would resolve itself on the day.

---

## Failure modes

**Forward-looking framing.** "What could go wrong?" produces a generic risk list.
If causes feel speculative and mild, the past-tense premise was not adopted.

**Running it too early.** A pre-mortem on a plan with insufficient specificity
yields generic concerns. The plan must have enough detail to reason about
particular failure modes — vague plans produce vague analyses.

**Anchoring (in group settings).** When facilitated, the most senior voice in the
room shapes the list. Run independent writing before any sharing — each
participant writes silently before the group compares lists.

**First-speaker anchoring.** The first cause named draws subsequent thinking
toward it. Write exhaustively before ranking or grouping.

**No follow-through.** A pre-mortem with no downstream plan change was
box-ticking. Findings must modify the plan or be explicitly accepted with
named mitigations.

---

## Handoff

The probable failure causes identified here feed Phase 5 (Validate). Add the
highest-signal structural weaknesses to the adversarial validation pass — each
one is a weak-link candidate for the signed-off analysis to address or explicitly
accept.

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
