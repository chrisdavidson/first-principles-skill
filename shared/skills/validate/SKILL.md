---
name: validate
description: Slash-only Phase 5 stub — stress-test each derivation chain for weak links.
disable-model-invocation: true
metadata:
  version: "8.22.0"
license: MIT
---
# Focused Validate Mode

You are running in focused-validate mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

{{PROCEDURE:validate}}

{{FOCUSED_VALIDATION}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
