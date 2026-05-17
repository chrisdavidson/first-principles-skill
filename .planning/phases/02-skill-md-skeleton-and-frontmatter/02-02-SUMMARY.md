---
phase: 02-skill-md-skeleton-and-frontmatter
plan: "02"
subsystem: skill-entry-point
tags: [skill-authoring, frontmatter, methodology-embed, nav-map, valid-05]

dependency_graph:
  requires: ["02-01"]
  provides: ["first-principles-thinking/SKILL.md"]
  affects: ["Phase 3 (validation rubric)", "Phase 4 (companion tools)", "Phase 5 (examples)", "Phase 6 (schema validation)"]

tech_stack:
  added: []
  patterns:
    - "Agent Skills open-standard YAML frontmatter (name, description, metadata.version)"
    - "Verbatim Phase 1 methodology embed with heading-level framing adaptation only"
    - "Condensed resident output skeleton + full annotated template deferred to references/"
    - "VALID-05 validator-fix-repeat loop instruction linking stub rubric"
    - "Navigation map: one-level-deep relative forward-slash links to all Layer-3 files"

key_files:
  created:
    - first-principles-thinking/SKILL.md
  modified: []

decisions:
  - "Embedded Phase 1 methodology verbatim (D-06) — heading levels adjusted, no rewording"
  - "Description uses >- YAML scalar so newlines collapse to single-line string at parse time"
  - "Stakes-Escalation Rule preserved verbatim in Phase 2 body section"
  - "Output skeleton resident in SKILL.md covers shape rules only; full annotations deferred to references/output-template.md"

metrics:
  duration: "~10 minutes"
  completed: "2026-05-17T00:37:00Z"
  tasks_completed: 2
  files_created: 1
---

# Phase 02 Plan 02: SKILL.md Skeleton and Frontmatter Summary

## One-liner

Authored `first-principles-thinking/SKILL.md` — valid Agent Skills frontmatter with seven ported English trigger phrases, Phase 1 5-phase methodology embedded verbatim, condensed output skeleton, VALID-05 validator-fix-repeat loop, and a navigation map linking all nine Layer-3 files.

## What Was Built

`first-principles-thinking/SKILL.md` (176 lines) is the installable entry point of the skill. It consists of:

1. **YAML frontmatter** — `name: first-principles-thinking` matching the parent directory; `description` with seven ported English trigger phrases plus extended triggers for architectural evaluation, 5-Whys, pre-mortem, and soundness checking; pushy clause for under-triggering avoidance; `license: MIT`; `metadata.version: "2.0"` (quoted string, nested under `metadata`, never top-level).

2. **Resident 5-phase methodology** — All 92 lines from `.planning/phases/01-.../methodology.md` embedded essentially verbatim. The only adaptation: heading levels adjusted to nest under SKILL.md's hierarchy (`###` phases promoted to `###` under a `## Methodology` section) and a single intro sentence added. All phase content preserved: standing-procedure framing, phase-connection chain, every phase's Why/Entry/Operation/Named Artifact/Exit criterion, the four-type assumption table, and the Stakes-escalation rule.

3. **Condensed output skeleton** — Six required section names in fixed order, honest-depth escape valve instruction, `GT-N + GT-M → [intermediate] → [conclusion]` chain format, `GT-N?` unverified-input notation, and a pointer to `references/output-template.md` for full annotated guidance.

4. **VALID-05 instruction** — Explicit validator-fix-repeat loop: Validate (quote spans), Fix (revise failures), Repeat (re-score until gate cleared); Markdown link to `references/validation-rubric.md`; final gate line prohibiting conclusions until rubric clears.

5. **Navigation map** — Companion tools section (five-whys, pre-mortem, trade-off-analysis with when-to-use notes) and worked examples section (four domain stubs). All nine Layer-3 links are relative forward-slash paths that resolve to files created by plan 02-01.

## Tasks Completed

| Task | Description | Commit | Files |
|------|-------------|--------|-------|
| 1 | Write frontmatter and embed the resident 5-phase methodology | 0eafb7d | first-principles-thinking/SKILL.md (created) |
| 2 | Add condensed output skeleton, VALID-05 loop instruction, and navigation map | 0eafb7d | first-principles-thinking/SKILL.md (appended) |

Note: Tasks 1 and 2 together produced a single file in one creation action — committed as one atomic unit.

## Verification Results

All automated checks passed:

- FOUND-01: frontmatter first line is `---`, `name: first-principles-thinking` matches directory name, `metadata:` key present, indented `version: "2.0"` present
- FOUND-02: description is third person, opens with "Decomposes", "Use when" clause present, all seven ported trigger phrases present, no Chinese characters, no XML tags
- FOUND-03: 176 lines — under the 500-line ceiling
- VALID-05: `references/validation-rubric.md` linked in body and exists on disk; Validate/Fix/Repeat loop instruction present
- Link audit: all nine Layer-3 links (`references/output-template.md`, `references/validation-rubric.md`, `references/five-whys.md`, `references/pre-mortem.md`, `references/trade-off-analysis.md`, `examples/software-systems.md`, `examples/product-business.md`, `examples/personal-general.md`, `examples/science-engineering.md`) referenced in SKILL.md and exist on disk

## Deviations from Plan

None — plan executed exactly as written.

The two tasks were committed in a single commit rather than two separate commits because Tasks 1 and 2 together produce a single file (`SKILL.md`) and the Write operation creates the complete file. This is a mechanical execution detail, not a deviation from the plan's intent.

## Known Stubs

SKILL.md itself contains no stubs — it is complete content. The nav-map links point to stub files created in plan 02-01; those stubs are expected and tracked in the plan.

## Threat Flags

None. SKILL.md contains only methodology guidance — no secrets, credentials, tokens, or private data. The `description` field follows the verified RESEARCH.md pattern: descriptive what-plus-when with literal trigger phrases only, no imperative directives beyond the one recommended pushy clause, no XML tags. T-02-02 mitigation applied as designed.

## Self-Check: PASSED

- `first-principles-thinking/SKILL.md`: FOUND (176 lines)
- Commit `0eafb7d`: confirmed in git log
- All nine Layer-3 link targets: FOUND on disk
- All acceptance criteria: met
