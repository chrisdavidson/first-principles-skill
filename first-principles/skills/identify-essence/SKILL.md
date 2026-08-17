---
name: identify-essence
description: Slash-only Phase 1 stub — expose core question by stripping framing artifacts.
disable-model-invocation: true
metadata:
  version: "8.17.4"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/identify-essence/SKILL.md by sync-content.py -->

# Focused Identify Essence Mode

You are running in focused-identify-essence mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

## When to reach for this

Use this phase at the start of every first-principles analysis. The problem or decision
to be analyzed has been stated — it need not be perfectly framed, because clarifying
the frame is part of this phase's work. Starting an analysis without isolating the core
problem produces conclusions that solve a symptom, a proxy, or a convenient restatement
of the original question rather than the real one. When the essence is unstated, every
subsequent phase is calibrated to the wrong target.

---

## Procedure

Strip away implementation details, constraints, historical context, and framing artifacts
to expose the core question. Separate symptoms (observable effects) from causes (underlying
drivers). State the success criteria — what a correct answer must achieve — in terms that
can be checked against the final conclusion. Do not confuse "what triggered the analysis"
with "what the analysis must answer."

**Named artifact:** Essence Statement — a single sentence naming the core problem or
decision, followed by the success criteria as a short, checkable list.

**Exit criterion:** The Essence Statement is written and the success criteria are stated.
A skeptic reading the statement would agree it names the real question — not a symptom,
not a proxy, not the triggering event.

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
