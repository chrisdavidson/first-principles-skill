---
name: validate
description: Slash-only Phase 5 stub — stress-test each derivation chain for weak links.
disable-model-invocation: true
metadata:
  version: "9.10.0"
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
— a Criterion 1 Absent verdict returns to Phase 1 to re-frame the Essence
Statement, any other Absent verdict is fixed in place under the Self-Audit
Gate's Fix/Repeat loop, and each unresolved weak link is carried with the
confidence caveat it was flagged with. Carry the `?` marks with it — this
run opened no cited source.
