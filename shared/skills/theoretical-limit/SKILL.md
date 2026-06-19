---
name: theoretical-limit
description: Strips conventions to the law-permitted ceiling. Invoke via /theoretical-limit only.
disable-model-invocation: true
metadata:
  version: "7.3.0"
license: MIT
---
# Focused Theoretical-Limit Mode

You are running in focused-theoretical-limit mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

{{PROCEDURE:theoretical-limit}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
