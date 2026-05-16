---
phase: 01-sharpen-the-methodology-and-harden-the-output-format
plan: "01"
subsystem: methodology-content
tags: [methodology, first-principles, markdown-content, standing-instructions]
dependency_graph:
  requires: []
  provides:
    - methodology.md -- sharpened 5-phase procedure with entry/exit criteria, named artifacts, and rationales
  affects:
    - 01-02-PLAN.md -- output-template.md plan consumes this file's phase definitions
    - 01-03-PLAN.md -- test-run draft will apply the methodology authored here
tech_stack:
  added: []
  patterns:
    - Phase Definition Block (Why/Entry/Operation/Named artifact/Exit)
    - 4-type assumption classification (physical law / current constraint / convention / untested belief)
    - Stakes-escalation rule for high-stakes conclusions
    - Standing instruction phrasing (imperative present tense, no first/then/next)
    - Observable exit criteria (state checks, not subjective confidence)
key_files:
  created:
    - .planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/methodology.md
  modified: []
decisions:
  - "Phase 4 (Reason Upward) authored as deliberately high-freedom per D-04 — no prescribed sub-steps, mandatory self-documenting narration only"
  - "Phase 4 exit criterion uses AND (not OR): core question answered AND complete derivation chains per D-05"
  - "Phase 2 includes the full 4-type classification scheme with prescribed treatments and stakes-escalation rule per D-06"
  - "Phase 5 references applying a validation rubric without authoring its criteria — rubric authorship is Phase 3 scope"
  - "How the phases connect orientation note positions each named artifact as the next phase's entry condition"
metrics:
  duration: "~261s"
  completed: "2026-05-16"
  tasks_completed: 2
  tasks_total: 2
  files_created: 1
  files_modified: 0
---

# Phase 01 Plan 01: Author Sharpened 5-Phase Methodology Summary

**One-liner:** Sharpened 5-phase first-principles reasoning procedure as standing instructions — each phase carrying explicit entry/exit criteria, a named artifact, a rationale naming its failure mode, and a 4-type assumption classification scheme with prescribed treatments.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Author four reasoning phase definitions (Phases 1-4) | 4668f57 | `.planning/phases/01-.../methodology.md` (created) |
| 2 | Author Validate phase definition and complete methodology | 2859a0f | `.planning/phases/01-.../methodology.md` (modified) |

## What Was Built

`methodology.md` — a sharpened 5-phase first-principles reasoning procedure written as standing instructions (imperative present tense, not one-time steps). The file contains:

- **Phase 1 (Identify Essence):** Separates core problem from symptoms; produces the Essence Statement.
- **Phase 2 (Challenge Assumptions):** Classifies every assumption using the 4-type scheme (physical law / current constraint / convention / untested belief) with prescribed treatments per D-06 and the stakes-escalation rule; produces the Classified Assumptions Table with 5 columns.
- **Phase 3 (Establish Ground Truths):** Compiles verified facts with stable GT-IDs using the irreducibility test; produces the Ground Truths list.
- **Phase 4 (Reason Upward):** Deliberately high-freedom per D-04 — no prescribed sub-steps, mandatory self-documenting narration, AND exit criterion (D-05); produces Derivation Chains.
- **Phase 5 (Validate):** Adversarial stress-test of derivation chains; references applying a validation rubric (rubric defined elsewhere per architectural responsibility map); produces the signed-off analysis.
- **"How the phases connect"** orientation note stating each named artifact is the next phase's entry condition.

## Decisions Made

1. Phase 4 authored with zero prescribed sub-steps — the only constraints are self-documenting narration, dead-end recording before course-change, and no analogies as direct evidence. This is the deliberate guard against over-prescription (Success Criterion 5, D-04).
2. Phase 4 exit criterion is explicitly AND: "(1) the core question is answered, AND (2) every conclusion has a complete derivation chain." OR would allow incomplete traceability to pass (A3 risk from RESEARCH.md).
3. Phase 5 operation says "Apply a validation rubric as a systematic check — a separate rubric document defines the criteria, levels, and scoring. Do not re-author the rubric criteria here; apply them." This keeps the rubric authorship cleanly in Phase 3 scope.
4. Stakes-escalation rule included inline in Phase 2: "The higher the stakes of the conclusion resting on an assumption, the more that assumption must be pushed toward physical law or verified ground truth." This satisfies D-06's escalation clause.

## Verification Results

All plan-level verification criteria satisfied:

- **METH-01:** All 5 phases have explicit entry and exit criteria (5/5 Entry criterion fields, 5/5 Exit criterion fields)
- **METH-02:** All 5 phases name a concrete artifact (Essence Statement, Classified Assumptions Table, Ground Truths list, Derivation Chains, signed-off analysis)
- **METH-03:** Phase 2 encodes all 4 locked types (physical law, current constraint, convention, untested belief) with prescribed treatments and stakes-escalation rule
- **METH-06:** All 5 rationales name a specific failure mode of omitting the step — none are circular or use "because it is important"
- **D-04:** Phase 4 contains no sub-steps (4a/4b/4c, Step 4, etc.); Operation is prose with mandatory narration constraint
- **D-05:** Phase 4 exit criterion contains "BOTH conditions must hold" joined by AND
- **Success Criterion 5:** Phase 4 is verifiably the deliberate high-freedom phase
- **min_lines:** 92 lines (minimum 90)
- **Automated check:** `grep -c '^### Phase [1-5]:' methodology.md` = 5, `grep -c '\*\*Exit criterion:\*\*'` = 5, `grep -c '\*\*Entry criterion:\*\*'` = 5

## Deviations from Plan

None — plan executed exactly as written.

The only navigation issue encountered: the Write tool initially created the file at the main repo path rather than the worktree path. This was immediately corrected by re-writing to the correct worktree absolute path and removing the main-repo copy. No commits were affected.

## Known Stubs

None. The methodology.md is complete content with no placeholder text.

## Threat Flags

None. `methodology.md` is a pure Markdown content file — no executables, no network surface, no auth paths, no data persistence, no user input handling.

## Self-Check: PASSED

- [x] `methodology.md` exists at worktree path `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/methodology.md`
- [x] Task 1 commit `4668f57` exists in git log
- [x] Task 2 commit `2859a0f` exists in git log
- [x] 5 phase headings, 5 entry criteria, 5 exit criteria, 5 named artifacts, 5 rationales verified by grep
- [x] Phase 2 contains all 4 locked assumption types and 5-column table header
- [x] Phase 4 is high-freedom with BOTH/AND exit criterion and no sub-step labels
- [x] Phase 5 references rubric without authoring its criteria
- [x] 92 lines (min 90 satisfied)
- [x] No stubs, no threat flags
