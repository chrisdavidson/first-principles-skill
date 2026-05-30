# Validate

> The adversarial pass — stress-test the derivation chains to find flaws that
> forward-direction reasoning was not looking for.

---

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
