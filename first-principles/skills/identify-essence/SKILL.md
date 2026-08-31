---
name: identify-essence
description: Slash-only Phase 1 stub — expose core question by stripping framing artifacts.
disable-model-invocation: true
metadata:
  version: "8.22.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/identify-essence/SKILL.md by sync-content.py -->

# Focused Identify Essence Mode

You are running in focused-identify-essence mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

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

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
