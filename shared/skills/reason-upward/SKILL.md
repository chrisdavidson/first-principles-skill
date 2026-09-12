---
name: reason-upward
description: Slash-only Phase 4 stub — build derivation chains upward from named ground truths.
disable-model-invocation: true
metadata:
  version: "9.2.2"
license: MIT
---
# Focused Reason Upward Mode

You are running in focused-reason-upward mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

{{PROCEDURE:reason-upward}}

{{FOCUSED_VALIDATION}}

---

If a fuller analysis is needed afterward, invoke the main
`first-principles` agent with this output as Derivation Chains for Phase 5
validation, with the ground truths those chains cite entering Phase 2 as
candidates — the chains rest on inputs this run did not verify. Carry the
`?` marks with it — this run opened no cited source.
