---
name: inversion
description: Runs a focused inversion only — enumerates failure preconditions. Invoke via /inversion only.
disable-model-invocation: true
metadata:
  version: "8.19.0"
license: MIT
---
# Focused Inversion Mode

You are running in focused-inversion mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

{{PROCEDURE:inversion}}

{{FOCUSED_VALIDATION}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
