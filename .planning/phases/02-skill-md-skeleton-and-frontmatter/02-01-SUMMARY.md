---
phase: 02-skill-md-skeleton-and-frontmatter
plan: 01
subsystem: content
tags: [markdown, skill, first-principles, output-template, stubs]

# Dependency graph
requires:
  - phase: 01-sharpen-the-methodology-and-harden-the-output-format
    provides: output-template.md (full annotated six-section template ported here)
provides:
  - first-principles-thinking/references/output-template.md (full annotated template, Layer 3)
  - first-principles-thinking/references/validation-rubric.md (stub slot for Phase 3)
  - first-principles-thinking/references/five-whys.md (stub slot for Phase 4)
  - first-principles-thinking/references/pre-mortem.md (stub slot for Phase 4)
  - first-principles-thinking/references/trade-off-analysis.md (stub slot for Phase 4)
  - first-principles-thinking/examples/software-systems.md (stub slot for Phase 5)
  - first-principles-thinking/examples/product-business.md (stub slot for Phase 5)
  - first-principles-thinking/examples/personal-general.md (stub slot for Phase 5)
  - first-principles-thinking/examples/science-engineering.md (stub slot for Phase 5)
affects: [02-02, 03, 04, 05, 06]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "D-08 stub convention: hash-1 heading + 1-2 sentence placeholder naming authoring phase, no YAML frontmatter"
    - "D-05 split: condensed skeleton resident in SKILL.md, full annotated template in references/output-template.md"

key-files:
  created:
    - first-principles-thinking/references/output-template.md
    - first-principles-thinking/references/validation-rubric.md
    - first-principles-thinking/references/five-whys.md
    - first-principles-thinking/references/pre-mortem.md
    - first-principles-thinking/references/trade-off-analysis.md
    - first-principles-thinking/examples/software-systems.md
    - first-principles-thinking/examples/product-business.md
    - first-principles-thinking/examples/personal-general.md
    - first-principles-thinking/examples/science-engineering.md
  modified: []

key-decisions:
  - "No YAML frontmatter on any references/ or examples/ file — triple-dash delimiters would make them appear as independent skills"
  - "output-template.md ported verbatim from Phase 1 with one framing note added at top"
  - "Stub files use plain CommonMark with a descriptive placeholder naming the future content and authoring phase"

patterns-established:
  - "Stub convention: # heading + 1-2 sentences + 'Authored in Phase N' — obvious placeholder, never mistakes for real content"
  - "Layer-3 file discipline: no frontmatter, forward-slash relative paths, one level deep from SKILL.md"

requirements-completed: [FOUND-03]

# Metrics
duration: 12min
completed: 2026-05-17
---

# Phase 02 Plan 01: Layer-3 File Scaffold Summary

**Full annotated output-template (150 lines) ported from Phase 1 plus eight descriptive stub files creating zero-dangling nav-map targets for SKILL.md**

## Performance

- **Duration:** 12 min
- **Started:** 2026-05-17T00:30:00Z
- **Completed:** 2026-05-17T00:42:00Z
- **Tasks:** 3
- **Files modified:** 9 created

## Accomplishments

- Authored references/output-template.md as a direct port of the Phase 1 source: all six sections in fixed order, GT-N + GT-M chain format, D-07 unverified-input rule, escape valve, type definitions, verdict vocabulary — 150 lines, no frontmatter
- Created four references stub files (validation-rubric, five-whys, pre-mortem, trade-off-analysis) — each a hash-1 heading plus a descriptive placeholder naming its authoring phase, no frontmatter
- Created four examples stub files (software-systems, product-business, personal-general, science-engineering) — same stub convention, all naming Phase 5

## Task Commits

Each task was committed atomically:

1. **Task 1: Author references/output-template.md from Phase 1 source** - `6d2ddc0` (feat)
2. **Task 2: Create the four references stub files** - `0b1abe1` (feat)
3. **Task 3: Create the four examples stub files** - `ea84bf1` (feat)

## Files Created/Modified

- `first-principles-thinking/references/output-template.md` - Full annotated six-section output template (150 lines), ported verbatim from Phase 1 with one framing note
- `first-principles-thinking/references/validation-rubric.md` - Stub slot for Phase 3 falsifiable self-check rubric
- `first-principles-thinking/references/five-whys.md` - Stub slot for Phase 4 root-cause drill-down procedure
- `first-principles-thinking/references/pre-mortem.md` - Stub slot for Phase 4 prospective-hindsight failure analysis
- `first-principles-thinking/references/trade-off-analysis.md` - Stub slot for Phase 4 structured option-comparison
- `first-principles-thinking/examples/software-systems.md` - Stub slot for Phase 5 software/systems worked example
- `first-principles-thinking/examples/product-business.md` - Stub slot for Phase 5 product/business worked example
- `first-principles-thinking/examples/personal-general.md` - Stub slot for Phase 5 personal/general worked example
- `first-principles-thinking/examples/science-engineering.md` - Stub slot for Phase 5 science/engineering worked example

## Decisions Made

- No YAML frontmatter on any references/ or examples/ file: triple-dash delimiters would make companion files look like independent skills, violating Phase 4 SC4.
- output-template.md ported verbatim with only one framing note added at the top to explain the resident/full split (D-05).
- Stub content is a descriptive placeholder naming authoring phase so no reader or agent mistakes a stub for finished content (D-08).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed line-break splitting "Authored in Phase" across two lines in trade-off-analysis.md**
- **Found during:** Task 2 verification
- **Issue:** The stub body wrapped "Authored in" at end of line 4 and "Phase 4." at start of line 5, causing grep for "Authored in Phase" to fail
- **Fix:** Collapsed the two-line body into a single unwrapped line so the literal phrase appears on one line
- **Files modified:** first-principles-thinking/references/trade-off-analysis.md
- **Verification:** Verify loop printed OK with exit code 0
- **Committed in:** 0b1abe1 (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 - Bug)
**Impact on plan:** Necessary for acceptance criterion compliance. No scope creep.

## Issues Encountered

None — all tasks completed on first attempt after the auto-fixed line-break bug.

## Known Stubs

All eight stub files are intentional stubs by design (D-07/D-08). They will be filled by later phases:

| File | Stub | Future Phase |
|------|------|-------------|
| references/validation-rubric.md | Placeholder for self-check rubric | Phase 3 |
| references/five-whys.md | Placeholder for 5-Whys procedure | Phase 4 |
| references/pre-mortem.md | Placeholder for pre-mortem procedure | Phase 4 |
| references/trade-off-analysis.md | Placeholder for trade-off analysis procedure | Phase 4 |
| examples/software-systems.md | Placeholder for software/systems worked example | Phase 5 |
| examples/product-business.md | Placeholder for product/business worked example | Phase 5 |
| examples/personal-general.md | Placeholder for personal/general worked example | Phase 5 |
| examples/science-engineering.md | Placeholder for science/engineering worked example | Phase 5 |

Note: references/output-template.md is NOT a stub — it is real content (150 lines, full annotated template).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- All nine Layer-3 file targets exist on disk; plan 02-02 (SKILL.md skeleton and frontmatter) can link to them without dangling references
- output-template.md is the complete annotated template for Phase 3 rubric calibration and Phase 5 example authoring
- Stub files carry descriptive placeholders naming authoring phases so no agent will mistake them for finished content

---
*Phase: 02-skill-md-skeleton-and-frontmatter*
*Completed: 2026-05-17*
