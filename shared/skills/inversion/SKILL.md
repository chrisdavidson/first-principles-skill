---
name: inversion
description: Runs a focused inversion only — enumerates failure preconditions. Invoke via /inversion only.
disable-model-invocation: true
metadata:
  version: "3.8.0"
license: MIT
---
# Focused Inversion Mode

You are running in focused-inversion mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

{{PROCEDURE:inversion}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
