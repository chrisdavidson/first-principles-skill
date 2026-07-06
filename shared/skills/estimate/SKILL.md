---
name: estimate
description: Runs a focused estimate only — magnitude rebuild from units. Invoke via /estimate only.
disable-model-invocation: true
metadata:
  version: "8.0.0"
license: MIT
---
# Focused Estimate Mode

You are running in focused-estimate mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

{{PROCEDURE:estimate}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
