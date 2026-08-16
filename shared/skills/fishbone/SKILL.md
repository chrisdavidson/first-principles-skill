---
name: fishbone
description: Runs a focused fishbone only — breadth-first cause-category map. Invoke via /fishbone only.
disable-model-invocation: true
metadata:
  version: "8.15.0"
license: MIT
---
# Focused Fishbone Mode

You are running in focused-fishbone mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

{{PROCEDURE:fishbone}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
