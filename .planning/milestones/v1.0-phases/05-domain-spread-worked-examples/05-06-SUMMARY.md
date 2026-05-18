---
phase: 05-domain-spread-worked-examples
plan: "06"
subsystem: examples
tags: [markdown, worked-examples, product-business, gap-closure, cross-references]

# Dependency graph
requires:
  - phase: 03-validation-rubric
    provides: validation-rubric.md used to verify no criterion Absent
  - phase: 05-domain-spread-worked-examples
    provides: product-business.md initial authoring (plans 01-04)
provides:
  - "product-business.md (EX-02) with accurate SKILL.md Phase 4 cross-references"
  - "product-business.md preamble consistent with the other three example files"
  - "GAP-01 WR-05 closed: no invented rule name"
  - "GAP-03 IN-01 closed: preamble added"
  - "GAP-02 confirmed: bare Conclusion headings in template form"
affects: [phase-06-wiring, skill-calibration-set]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Cross-reference descriptive form: 'Phase 4 no-analogies guidance (SKILL.md, Phase 4 Operation)' — never invent rule names"
    - "Preamble pattern: one paragraph naming the example's distinctive methodology emphasis + 'Authored in Phase N' + '---' rule"

key-files:
  created: []
  modified:
    - first-principles-thinking/examples/product-business.md

key-decisions:
  - "Replace invented rule names with descriptive citations of actual SKILL.md guidance — never capitalize or number guidance that SKILL.md does not name"
  - "Preamble names EX-02's distinctive emphasis: the Phase 2 Assumptions Table depth and the Phase 4 no-analogies dead-end"

patterns-established:
  - "Example cross-references: cite guidance by description and location, not by invented rule names"
  - "Example preamble: one-paragraph between H1 and first section, ending with Authored in Phase N, followed by ---"

requirements-completed: [EX-02]

# Metrics
duration: 10min
completed: 2026-05-18
---

# Phase 05 Plan 06: Product-Business Example Gap Closure Summary

**Replaced invented "Phase 4 no-analogies-as-direct-evidence rule" terminology with accurate descriptive SKILL.md citations, and added the missing explanatory preamble to product-business.md to close GAP-01 WR-05 and GAP-03 IN-01**

## Performance

- **Duration:** ~10 min
- **Started:** 2026-05-18T11:00:00Z
- **Completed:** 2026-05-18T11:06:34Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments

- Removed all occurrences of the invented "no-analogies-as-direct-evidence rule" string — both the Section 1 success criterion and the Section 5 Abandoned Reasoning paragraph now cite the Phase 4 guidance descriptively
- Added a preamble paragraph between the H1 and `## 1. Problem Essence` consistent with the other three example files, naming EX-02's distinctive emphasis (dense Phase 2 Assumptions Table, Phase 4 no-analogies dead-end) and noting "Authored in Phase 5"
- Confirmed the three `### Conclusion:` headings remain in the bare template form (GAP-02 confirmed)

## Task Commits

Each task was committed atomically:

1. **Task 1: Replace invented rule name with accurate SKILL.md Phase 4 citation** - `07121b1` (fix)
2. **Task 2: Add explanatory preamble and confirm Conclusion heading conformance** - `2cebb3c` (feat)

**Plan metadata:** (see final commit below)

## Files Created/Modified

- `first-principles-thinking/examples/product-business.md` - Replaced two invented "no-analogies-as-direct-evidence rule" occurrences with descriptive citations; added preamble paragraph after H1

## Decisions Made

- Cited the Phase 4 no-analogies guidance as "the Phase 4 no-analogies guidance (SKILL.md, Phase 4 Operation)" in the success criterion, and as "the Phase 4 instruction not to use analogies as direct evidence (SKILL.md, Phase 4 Operation)" in the Abandoned Reasoning paragraph — both are descriptive, lowercase, not capitalized as proper rule names
- Preamble prose matches the register of the other three examples: plain (not italic), one paragraph, ends with "Authored in Phase 5"
- Did not edit SKILL.md (out of scope per 05-CONTEXT.md — Phase 6 handles wiring)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

Minor: Initial edits were made to the main repo working tree instead of the worktree file. Corrected by re-applying changes to the correct worktree path and restoring the main repo file via `git checkout`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- EX-02 (product-business.md) is now a faithful calibration specimen whose cross-references match the skill it demonstrates
- All four example files share a consistent preamble structure
- All four example files use bare `### Conclusion:` headings per the template form
- GAP-01 WR-05, GAP-03 IN-01, and GAP-02 (for this file) are closed
- Ready for Phase 6 wiring (SKILL.md wiring and cross-linking)

## Self-Check

- [x] Modified file exists: `first-principles-thinking/examples/product-business.md`
- [x] Task 1 commit `07121b1` exists in git log
- [x] Task 2 commit `2cebb3c` exists in git log
- [x] Zero occurrences of "no-analogies-as-direct-evidence rule" in product-business.md
- [x] Preamble present between H1 and `## 1. Problem Essence`
- [x] "Phase 5" mentioned at least once (preamble)
- [x] Three `### Conclusion:` headings, bare form, no letters/numbers

---
*Phase: 05-domain-spread-worked-examples*
*Completed: 2026-05-18*
