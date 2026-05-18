---
phase: 05-domain-spread-worked-examples
plan: "05"
subsystem: examples
tags: [gap-closure, worked-examples, software-systems, rubric-conformance]
dependency_graph:
  requires: []
  provides: [EX-01-gap-closure]
  affects: [first-principles-thinking/examples/software-systems.md]
tech_stack:
  added: []
  patterns: [derivation-chain-format, synthesis-only-conclusion, template-conclusion-headings]
key_files:
  modified:
    - first-principles-thinking/examples/software-systems.md
decisions:
  - "Moved pipeline-stage taxonomy and time characterizations into the Conclusion C chain so Section 6 restates rather than originates"
  - "Scoped absolute 'no architectural change is needed' to 'remove the deploy-frequency bottleneck' to resolve tension with schema-decomposition recommendation"
  - "Added explicit '(Section 1, Problem Essence)' mapping on first use of 'Essence Statement'"
metrics:
  duration: ~5 min
  completed: "2026-05-18"
  tasks_completed: 2
  files_modified: 1
---

# Phase 05 Plan 05: software-systems.md gap closure Summary

Closed GAP-01 (WR-03, WR-04), GAP-02 (WR-01, WR-02), and GAP-03 advisory items (IN-02, IN-06) for `examples/software-systems.md` — bringing the calibration specimen into full template conformance with correct chain headers, synthesis-only Section 6, and consistent Conclusion headings.

## What Was Built

Revised `first-principles-thinking/examples/software-systems.md` to pass the validation-rubric gate and match the format used by the other three worked examples.

### Task 1: Chain header fixes and heading relabelling (WR-03, WR-01/WR-02)

- Added GT-3 to the first chain's header (was GT-1 + GT-2; now GT-1 + GT-2 + GT-3) so every GT the chain relies on is declared.
- Rewrote the chain's intermediate step as a genuine three-GT inference: the pipeline structure (sequential execution + full-suite requirement) is the sufficient cause of the measured 2-deploy/day ceiling — this is only statable by combining all three GTs.
- Applied IN-06 fix within the same intermediate: "no architectural change is needed to achieve that outcome" → "no architectural change is needed to remove the deploy-frequency bottleneck", scoping the claim so it does not read as contradicted by the later schema-decomposition recommendation.
- Renamed `### Conclusion A/B/C:` headings to the bare template form `### Conclusion: [text]` matching `output-template.md:105` and the other three examples.
- Zero lettered labels remain anywhere in the file.

### Task 2: Synthesis-only Section 6 and advisory fixes (WR-04, IN-02, IN-06)

- Moved the pipeline-stage taxonomy (test suite execution, artifact build, deployment and restart, health-check wait) and the time characterizations ("approximately 1 day" for profiling, "days to 2 weeks" for parallelization) into the Conclusion C chain, where they are established as part of the cost/risk analysis.
- Section 6 steps now cite the chain as their source and no longer introduce new reasoning, stage names, or time figures that do not appear in Section 4.
- First use of "Essence Statement" in Section 6 is now written "the Essence Statement (Section 1, Problem Essence)" so readers can map the SKILL.md artifact name to the section heading (IN-02).

## Verification

- Zero occurrences of "Conclusion A", "Conclusion B", "Conclusion C" anywhere in the file.
- Exactly 3 `### Conclusion:` headings in template form.
- First chain's GT header names GT-1, GT-2, and GT-3.
- Every pipeline-stage term and time figure in Section 6 also appears in the Conclusion C derivation chain.
- First use of "Essence Statement" includes "(Section 1, Problem Essence)" mapping.
- No unscoped "no architectural change is needed" remains — all occurrences are scoped to the deploy-frequency bottleneck.
- Six section headings in fixed order, single H1, no rubric verdict blocks, preamble paragraph retained.

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| Task 1 + Task 2 | 27a763b | fix(05-05): fix chain headers, Conclusion headings, synthesis-only Section 6, and advisory items |

## Deviations from Plan

### Auto-adjustments

**1. [Combined Tasks 1 and 2 into single commit]**
- **Reason:** Both tasks edit the same file and the IN-06 fix (scoping the intermediate phrasing) was naturally applied while fixing the chain header in Task 1. The changes are semantically coupled: Task 1 restructures the chain intermediate, Task 2's IN-06 fix scopes that same intermediate. Separating them into two commits on the same file would have required writing an intermediate state that combines some but not all fixes.
- **Impact:** None — both tasks' acceptance criteria are verifiably satisfied.

Otherwise: plan executed exactly as written.

## Known Stubs

None. The file is a complete worked example with no placeholder content.

## Threat Flags

None. Pure-Markdown content edits with no new network endpoints, auth paths, file access patterns, or schema changes.

## Self-Check: PASSED

- `first-principles-thinking/examples/software-systems.md` exists in worktree at expected path: FOUND
- Commit `27a763b` exists: FOUND
- Zero "Conclusion A/B/C" occurrences: VERIFIED
- Exactly 3 `### Conclusion:` headings: VERIFIED
- Pipeline-stage terms in Section 6 also present in Section 4 chain: VERIFIED
- "Essence Statement (Section 1, Problem Essence)" on first use: VERIFIED
