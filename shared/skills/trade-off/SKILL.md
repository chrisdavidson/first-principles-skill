---
name: trade-off
description: Runs a focused trade-off only — weighted-criteria scoring. Invoke via /trade-off only.
disable-model-invocation: true
metadata:
  version: "8.17.0"
license: MIT
---
# Focused Trade-off Mode

You are running in focused-trade-off mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

{{PROCEDURE:trade-off}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
