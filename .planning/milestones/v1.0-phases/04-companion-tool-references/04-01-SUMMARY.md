---
phase: 04-companion-tool-references
plan: "01"
subsystem: references
tags: [five-whys, companion-tool, root-cause, procedure]
dependency_graph:
  requires: []
  provides: [five-whys.md root-cause drill-down reference component]
  affects: [first-principles-thinking/references/five-whys.md]
tech_stack:
  added: []
  patterns: [branching-procedure, test-based-stop-criterion, companion-tool-reference]
key_files:
  created: []
  modified:
    - first-principles-thinking/references/five-whys.md
decisions:
  - "Stop criterion is test-based (Corrective Action Test), not count-based — 'five' appears only as a typical depth note in failure modes"
  - "Bread-goes-stale scenario chosen for 5-Whys mini-example — recurring household problem plays to the tool's root-cause strength"
  - "Lateral scan instruction ('What else caused this?') placed explicitly at each level, not just once in the procedure"
metrics:
  duration: "~10 min"
  completed: "2026-05-17"
---

# Phase 4 Plan 1: Author five-whys.md Summary

## One-liner

Branching root-cause drill-down reference with Corrective Action Test stop criterion, bread-goes-stale mini-example, and Phase 2/4 handoff.

## What Was Built

Replaced the five-line descriptive stub in `first-principles-thinking/references/five-whys.md` with a complete, self-contained 5-Whys reference component. The file is 92 lines and frontmatter-free.

**Five components delivered (D-03):**
1. `## When to reach for this` — use case (recurring symptom, surface fix failed) plus contrast clause (multiple interacting subsystems → use fishbone instead)
2. `## Procedure` — imperative bold-step procedure with lateral scan instruction at each level, Corrective Action Test as stop criterion, evidence-validation step
3. `## Example` — bread-goes-stale everyday scenario, two branches, annotated stop points
4. `## Failure modes` — count-based stopping, single-thread drilling, inference without evidence, confirmation bias
5. `## Handoff` — 3 sentences naming Phase 2 (Classified Assumptions Table) and Phase 4 (Derivation Chain) as integration points

## Acceptance Criteria Verification

| Criterion | Status |
|-----------|--------|
| No YAML frontmatter — `---` dividers only after H1 | PASS |
| First line is `# 5-Whys` | PASS |
| All five `##` headings present | PASS |
| Stop criterion is test-based, "five" not a stop rule | PASS |
| Branching instruction ("What else caused this?") present | PASS |
| Handoff names Phase 2 and Phase 4, grep matches | PASS |
| Line count 92 (roughly under 100) | PASS |
| Procedure in imperative mood | PASS |

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

None — file is complete and self-contained.

## Threat Flags

None — static Markdown reference file, no trust boundaries crossed.

## Self-Check: PASSED

- `first-principles-thinking/references/five-whys.md` exists and contains all five components
- Commit `15ac140` confirmed in git log
- No unexpected file deletions
