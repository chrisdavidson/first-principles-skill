---
name: reason-upward
description: Slash-only Phase 4 stub — build derivation chains upward from named ground truths.
disable-model-invocation: true
metadata:
  version: "8.17.1"
license: MIT
---
# Focused Reason Upward Mode

You are running in focused-reason-upward mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

{{PROCEDURE:reason-upward}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
