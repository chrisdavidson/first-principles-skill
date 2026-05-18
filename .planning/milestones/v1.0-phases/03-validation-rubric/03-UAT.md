---
status: complete
phase: 03-validation-rubric
source: [03-01-SUMMARY.md, 03-02-SUMMARY.md]
started: 2026-05-17T13:00:00Z
updated: 2026-05-17T13:25:00Z
---

## Current Test

[testing complete]

## Tests

### 1. Rubric file is complete and well-formed
expected: Opening validation-rubric.md shows a complete rubric — "# Validation Rubric" heading, a Scoring Model section, a Verdict Block Format section, and 6 analytic criteria each scored on the same 4 named levels (Rigorous / Sound / Hand-wavy / Absent). No leftover one-sentence stub.
result: pass

### 2. Pass condition is self-consistent (CR-01 fix)
expected: The Scoring Model section's Pass definition matches the gate + cap rule — passes when no criterion scores Absent and at most one scores Hand-wavy — with no self-contradicting "every criterion Sound or above" clause. A reviewer scoring an analysis with exactly one Hand-wavy criterion can determine the verdict unambiguously.
result: pass

### 3. Cross-references resolve to shipped files (CR-02 fix)
expected: The criterion "Folds in:" lines cite only design-decision IDs D-07 and D-03 — both defined in shipped files (SKILL.md / output-template.md). No dangling D-01 or D-08 references that resolve to nothing.
result: pass

### 4. Gate scoring catches hand-waving (falsifiability demo)
expected: Opening .planning/phases/03-validation-rubric/03-weak-sample.md shows a deliberately-weak analysis scored with 6 evidence-quoting verdict blocks; at least one criterion scores Absent and the Overall Verdict is FAIL, fired by the gate. The rubric demonstrably fails a known-weak input rather than certifying it.
result: pass

### 5. Heading nesting and section citations are clean (IN fixes)
expected: The 6 "Criterion N" headings render as H3 nested under an H2 "Criteria" (correct document outline), and gap-citation examples name output-template sections (e.g. "section 4 (Derivation Chains)") rather than bare numbers.
result: pass

## Summary

total: 5
passed: 5
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

[none yet]
