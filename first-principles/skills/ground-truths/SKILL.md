---
name: ground-truths
description: Slash-only Phase 3 stub — compile GT-ID-anchored verified facts for derivation chains.
disable-model-invocation: true
metadata:
  version: "8.17.5"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/ground-truths/SKILL.md by sync-content.py -->

# Focused Ground Truths Mode

You are running in focused-ground-truths mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

## When to reach for this

Use this phase once the Classified Assumptions Table from Phase 2 is finalized.
Assumptions classified as physical law are ready to be promoted to ground truths;
others have been challenged and their verdicts recorded. Reasoning from assumptions
treats contested claims as solid foundations. Ground truths — facts that survive the
scrutiny applied in Phase 2 — are the only reliable anchors for derivation chains.
Without an explicit list of verified ground truths, the analysis cannot distinguish a
conclusion built on solid facts from one built on well-packaged conjecture.

---

## Procedure

Compile the verified ground truths from the Phase 2 analysis. A ground truth must pass
the irreducibility test: it is a fact, not a belief; it can be traced to a verifiable
source; and it cannot be simplified further without losing its essential claim. Assign
each ground truth a stable identifier (GT-1, GT-2, etc.) that does not change for the
life of the analysis. Unverified facts that must be used may be included but get the
`GT-N?` suffix and inherit the confidence caveat rules from D-07. Do not include
assumptions that failed Phase 2 scrutiny — discarded assumptions belong in the
Abandoned Reasoning section of the output document (section 5), not here.

**Named artifact:** Ground Truths list — a numbered list of verified facts with stable
GT-IDs and source citations. Unverified entries are marked with the `?` suffix.

**Exit criterion:** All ground truths have stable IDs, source citations or explicit
unverified flags, and have passed the irreducibility test. No assumption that was
discarded in Phase 2 appears in this list. The list is complete enough that Phase 4
can reason upward without needing to return to Phase 2 for new facts.

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
