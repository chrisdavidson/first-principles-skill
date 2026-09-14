---
name: estimate
description: Runs a focused estimate only — magnitude rebuild from units. Invoke via /estimate only.
disable-model-invocation: true
metadata:
  version: "9.3.0"
license: MIT
---
# Focused Estimate Mode

You are running in focused-estimate mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

{{PROCEDURE:estimate}}

{{FOCUSED_VALIDATION}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as candidate inputs for Phase 2. Carry the `?` marks
with it — this run opened no cited source.
