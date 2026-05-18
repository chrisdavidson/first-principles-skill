---
status: diagnosed
phase: 05-domain-spread-worked-examples
source: [05-VERIFICATION.md]
started: "2026-05-17"
updated: "2026-05-17"
---

## Current Test

[complete — issues reported, routed to gap closure]

## Tests

### 1. Rubric gate confirmation
expected: Each of the four example files, scored against the validation rubric, has all six criteria at Sound or above — no criterion at the lowest band (Absent), at most one Hand-wavy per file.
result: issue — rubric-rigor defects found (see GAP-01, GAP-03 in 05-VERIFICATION.md): undeclared ground truth in a chain header, Section 6 synthesis-only violation, invented "Phase 4 rule" terminology, incomplete loss accounting in the solar panel chain, plus Info-level advisory items.

### 2. Structural variety depth check
expected: The designated "deepest section" in each example is visibly more developed than the corresponding section in the other three examples — genuine methodology variety, not the same skeleton with domain nouns swapped.
result: issue — cross-example inconsistency found (see GAP-02 in 05-VERIFICATION.md): lettered vs unlabelled Conclusion headings across the four files, which also blurs the one-chain-per-conclusion rule.

## Summary

total: 2
passed: 0
issues: 2
pending: 0
skipped: 0
blocked: 0

## Gaps

| Gap | Source test | Tracked in |
|-----|-------------|------------|
| GAP-01 — Rubric-rigor defects | 1 | 05-VERIFICATION.md |
| GAP-02 — Cross-example inconsistency | 2 | 05-VERIFICATION.md |
| GAP-03 — Remaining advisory items | 1 | 05-VERIFICATION.md |

Close via `/gsd:plan-phase 5 --gaps` → `/gsd:execute-phase 5 --gaps-only`.
