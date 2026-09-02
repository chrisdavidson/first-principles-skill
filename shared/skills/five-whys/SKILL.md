---
name: five-whys
description: Runs a focused 5-Whys only — root-cause drill on a symptom or a reduce-to-primitives irreducibility drill on a claim. Invoke via /five-whys only.
disable-model-invocation: true
metadata:
  version: "8.25.0"
license: MIT
---
# Focused 5-Whys Mode

You are running in focused-five-whys mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

{{PROCEDURE:five-whys}}

{{FOCUSED_VALIDATION}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
