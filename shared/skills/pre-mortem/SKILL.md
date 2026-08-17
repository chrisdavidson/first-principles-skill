---
name: pre-mortem
description: Runs a focused pre-mortem only — prospective-hindsight failure analysis. Invoke via /pre-mortem only.
disable-model-invocation: true
metadata:
  version: "8.17.4"
license: MIT
---
# Focused Pre-Mortem Mode

You are running in focused-pre-mortem mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

{{PROCEDURE:pre-mortem}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
