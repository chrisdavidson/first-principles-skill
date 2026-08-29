---
name: second-order
description: Runs a focused second-order only — 2nd/3rd-order effects. Invoke via /second-order only.
disable-model-invocation: true
metadata:
  version: "8.17.5"
license: MIT
---
# Focused Second-Order Mode

You are running in focused-second-order mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

{{PROCEDURE:second-order}}

{{FOCUSED_VALIDATION}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
