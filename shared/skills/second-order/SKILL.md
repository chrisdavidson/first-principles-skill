---
name: second-order
description: Runs a focused second-order analysis only — enumerates 2nd/3rd-order consequences of a stated conclusion. Slash-only; orchestrator uses the main agent.
disable-model-invocation: true
metadata:
  version: "3.8.0"
license: MIT
---
# Focused Second-Order Mode

You are running in focused-second-order mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

{{PROCEDURE:second-order}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
