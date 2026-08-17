---
name: validate
description: Slash-only Phase 5 stub — stress-test each derivation chain for weak links.
disable-model-invocation: true
metadata:
  version: "8.17.3"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/validate/SKILL.md by sync-content.py -->

# Focused Validate Mode

You are running in focused-validate mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

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

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
