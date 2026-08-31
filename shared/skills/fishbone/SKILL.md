---
name: fishbone
description: Runs a focused fishbone only — breadth-first cause-category map. Invoke via /fishbone only.
disable-model-invocation: true
metadata:
  version: "8.24.0"
license: MIT
---
# Focused Fishbone Mode

You are running in focused-fishbone mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

{{PROCEDURE:fishbone}}

{{FOCUSED_VALIDATION}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
