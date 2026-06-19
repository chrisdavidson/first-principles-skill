---
name: decompose
description: Runs a focused decompose only — reduces a claim to its irreducible primitives via a recursive drill that stops at a physical law, definition, or measurement. Invoke via /decompose only.
disable-model-invocation: true
metadata:
  version: "7.1.0"
license: MIT
---
# Focused Decompose Mode

You are running in focused-decompose mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

{{PROCEDURE:decompose}}

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
