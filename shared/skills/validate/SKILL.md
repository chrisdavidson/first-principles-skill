---
name: validate
description: Slash-only Phase 5 stub — stress-test each derivation chain for weak links.
disable-model-invocation: true
metadata:
  version: "9.2.0"
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

If a fuller analysis is needed afterward, invoke the main
`first-principles` agent with this output as the Phase 5 verdict to act on
— each Absent verdict routed to the phase that owns the artifact it names,
each unresolved weak link carried with the confidence caveat it was flagged
with. Carry the `?` marks with it — this run opened no cited source.
