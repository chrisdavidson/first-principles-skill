---
name: five-whys
description: Runs a focused 5-Whys only — depth-first root-cause drill on a single recurring symptom. Invoke via /five-whys only.
disable-model-invocation: true
metadata:
  version: "3.8.0"
license: MIT
---
# Focused 5-Whys Mode

You are running in focused-five-whys mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

{{PROCEDURE:five-whys}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
