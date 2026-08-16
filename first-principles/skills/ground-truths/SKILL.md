---
name: ground-truths
description: Slash-only Phase 3 stub — compile GT-ID-anchored verified facts for derivation chains.
disable-model-invocation: true
metadata:
  version: "8.17.1"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/ground-truths/SKILL.md by sync-content.py -->

# Focused Ground Truths Mode

You are running in focused-ground-truths mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

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

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
