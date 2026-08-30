---
name: challenge-assumptions
description: Slash-only Phase 2 stub — classify and test every assumption before reasoning.
disable-model-invocation: true
metadata:
  version: "8.19.0"
license: MIT
---
# Focused Challenge Assumptions Mode

You are running in focused-challenge-assumptions mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

{{PROCEDURE:challenge-assumptions}}

{{FOCUSED_VALIDATION}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
