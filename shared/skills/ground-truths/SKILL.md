---
name: ground-truths
description: Slash-only Phase 3 stub — compile GT-ID-anchored verified facts for derivation chains.
disable-model-invocation: true
metadata:
  version: "8.18.0"
license: MIT
---
# Focused Ground Truths Mode

You are running in focused-ground-truths mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

{{PROCEDURE:ground-truths}}

{{FOCUSED_VALIDATION}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
