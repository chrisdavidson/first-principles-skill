---
name: reason-upward
description: Slash-only Phase 4 stub — build derivation chains upward from named ground truths.
disable-model-invocation: true
metadata:
  version: "8.18.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/reason-upward/SKILL.md by sync-content.py -->

# Focused Reason Upward Mode

You are running in focused-reason-upward mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

## When to reach for this

Use this phase once the Ground Truths list is complete — all ground truths carry IDs and
verification notes — and the Classified Assumptions Table from Phase 2 is finalized. The
methodology has established what is true (ground truths) and what can be discarded (false
assumptions). The task now is to construct an answer from those truths. This phase is
deliberately high-freedom because the right method for combining ground truths depends
entirely on the problem's structure.

---

## Procedure

Reason upward from the ground truths toward an answer using whatever approach the problem
calls for. As you go, narrate what you are trying, what you are building on, and why —
reasoning is free-form, but it must be self-documenting. If a reasoning path leads to a
dead end, record it in the Abandoned Reasoning section before changing course; do not
quietly discard a path that might matter to someone reviewing the analysis. Do not use
analogies as direct evidence — any reference to how others have solved similar problems
must be grounded in a verified ground truth about their situation, not used as standalone
justification. Before handing off to Phase 5, apply the second-order effects procedure
to extend the relevant Derivation Chain with 2nd/3rd-order effects. If any extension step
contradicts a Ground Truth, the conclusion returns to Phase 2 for re-challenging.

**Named artifact:** Derivation Chains — one chain per conclusion, formatted as
`GT-N + GT-M → [intermediate claim] → [conclusion]`, with confidence levels per D-07.
Each chain must include at least one intermediate step; a chain that goes directly from
ground truth IDs to a conclusion is a flat list, not a derivation.

**Exit criterion:** ALL THREE conditions must hold: (1) the problem's core question as
stated in the Essence Statement is answered, AND (2) every conclusion offered has a
complete derivation chain back to named ground truths, AND (3) the second-order effects
procedure pass has been applied and no extension step contradicts a Ground Truth. Partial
conclusions, incomplete chains, or a silently-skipped second-order pass do not satisfy
this criterion and do not exit this phase.

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
