---
name: validate
description: Slash-only Phase 5 stub — stress-test each derivation chain for weak links.
disable-model-invocation: true
metadata:
  version: "8.17.5"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/validate/SKILL.md by sync-content.py -->

# Focused Validate Mode

You are running in focused-validate mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below
- do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

## When to reach for this

Use this phase once the Derivation Chains artifact from Phase 4 is complete — all
conclusions have chains and the core question is answered. Completing a derivation chain
does not guarantee the chain is sound. A chain built on an unverified assumption that is
load-bearing, or one whose weakest link is never examined, produces a conclusion that
looks rigorous but collapses under scrutiny. Validation is the adversarial pass that
exists to find the flaws forward-direction reasoning was not looking for.

---

## Procedure

Stress-test the analysis. For each conclusion, trace the derivation chain back to its
named ground truths and check that every link holds. Identify the weakest link in each
chain — the step where the reasoning is most dependent on an assumption that is not
fully verified, or where the inferential gap is largest. Check whether any unverified
assumption (`GT-N?`) is load-bearing for a high-stakes conclusion; if it is, either
verify it now or apply a confidence caveat to the conclusion. Apply the Validation
Rubric as a systematic check — that document defines the criteria, levels, and scoring.
Do not re-author the rubric criteria here; apply them.

**Named artifact:** Signed-off analysis — the complete output document with all sections
present, all conclusions traced to named ground truths, and all weak links either resolved
or explicitly flagged with confidence caveats.

**Exit criterion:** Every conclusion traces to a named ground truth via a complete
derivation chain, AND every weak link is either resolved (the assumption has been
verified or reclassified) or explicitly flagged with a confidence caveat that a reader
can evaluate. A skeptic inspecting the signed-off analysis can verify both conditions
hold without asking the analyst for clarification.

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
