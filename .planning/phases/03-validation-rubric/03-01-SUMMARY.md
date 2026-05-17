---
phase: 03-validation-rubric
plan: 01
subsystem: validation-rubric
tags: [rubric, analytic-rubric, scoring-model, gate, hand-wavy-cap, observable-descriptors]
dependency_graph:
  requires: [first-principles-thinking/SKILL.md, first-principles-thinking/references/output-template.md]
  provides: [first-principles-thinking/references/validation-rubric.md]
  affects: [Phase 5 — worked examples must pass this rubric's gate]
tech_stack:
  added: []
  patterns: [analytic rubric, conjunctive gate scoring, evidence-quoting verdict blocks, observable descriptors]
key_files:
  created: []
  modified:
    - first-principles-thinking/references/validation-rubric.md
decisions:
  - "Band labels: Rigorous / Sound / Hand-wavy / Absent (D-06 choice — preserves 'Hand-wavy' and 'Absent' from stub; 'Sound' replaces 'Adequate' as less ambiguous for rank direction)"
  - "Hand-wavy cap set at 2 of 6 (D-05 — minimum that catches mediocre-everywhere analyses while tolerating one isolated weaker section)"
  - "Criteria written in methodology-phase order: Identify Essence → Challenge Assumptions → Establish Ground Truths → Reason Upward → Validate → Traceability"
  - "All 6 criteria authored in a single write operation (Task 1 and Task 2 committed together as ba84526)"
metrics:
  duration_minutes: 6
  completed_date: "2026-05-17T03:02:54Z"
  tasks_completed: 2
  files_modified: 1
---

# Phase 03 Plan 01: Author Validation Rubric — Summary

**One-liner:** 6-criterion analytic rubric with Rigorous/Sound/Hand-wavy/Absent scale, conjunctive gate + hand-wavy cap (2/6), and evidence-quoting verdict blocks replacing a one-sentence stub.

## What Was Built

`first-principles-thinking/references/validation-rubric.md` — the complete operative analytic rubric
for the first-principles-thinking skill. Replaces the one-sentence stub with a fully authored
Layer-3 reference file: 285 lines, no YAML frontmatter, frontmatter-free per Phase 2 D-08.

### Structure of the authored rubric

1. **Block-quote scope note** — states this is the scoring instrument for SKILL.md's
   validator-fix-repeat loop and names the relationship to output-template.md without
   duplicating the loop instruction.

2. **How to Apply This Rubric** — two-condition pass rule: gate cleared (no Absent) AND
   hand-wavy cap cleared (at most one Hand-wavy).

3. **Scoring Model** — shared 4-level scale defined with bold-lead-in bullets in explicit
   rank order (Rigorous > Sound > Hand-wavy > Absent). Gate and cap rules reference band
   labels not level numbers, per RESEARCH Pitfall 5.

4. **Verdict Block Format** — two fenced code blocks (no language tag):
   - Standard form: Quoted span / Band / Justification
   - Gap-citation form (D-09): Gap / Band / Justification for Absent verdicts where no span exists

5. **6 Analytic Criteria** in methodology-phase order:
   - Criterion 1: Identify Essence (escape-valve policing per D-08)
   - Criterion 2: Challenge Assumptions (4-type scheme + unverified-flag discipline, D-01)
   - Criterion 3: Establish Ground Truths (GT-IDs, GT-N? suffix, discard exclusion)
   - Criterion 4: Reason Upward (intermediate steps, no-analogies ban, Abandoned Reasoning escape-valve policing, D-01, D-08)
   - Criterion 5: Validate (confidence caveats, GT-N? chain rules)
   - Criterion 6: Conclusion-to-Ground-Truth Traceability

6. **Usage Note** — closing statement reinforcing gate + cap before presenting.

## Success Criteria Status

- [x] VALID-01: exactly 6 criteria covering 5 phases + traceability
- [x] VALID-02: 4 named levels per criterion, each with a concrete observable descriptor
- [x] VALID-03: gate scoring model (any Absent fails) + hand-wavy cap (2+ Hand-wavy fails)
- [x] VALID-04: per-criterion verdict block format with quoted span or gap citation

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| Task 1 + Task 2 | ba84526 | feat(03-01): author validation rubric preamble and scoring model |

## Deviations from Plan

### Process Deviation — Tasks 1 and 2 authored in a single write

**Found during:** Task 1 execution
**Issue:** The plan separates preamble authoring (Task 1) from criteria authoring (Task 2),
anticipating an append operation. Writing both in a single operation was more reliable and
eliminated the risk of partial file state between commits.
**Fix:** Both the preamble/scoring model and all 6 criteria were authored and written in one
operation, then committed as Task 1's commit. Task 2's acceptance criteria were verified
against the committed file and all pass.
**Impact:** One commit instead of two; no functional difference.
**Classification:** [Rule 3 - Process] minor sequencing optimization, no content deviation.

## Threat Surface Scan

No new network endpoints, auth paths, file access patterns, or schema changes introduced.
The authored file is pure Markdown with no executable code, no fenced blocks with language
tags (verified by check), and no `scripts/` directory. T-03-01 (tampering) mitigation is satisfied.

## Known Stubs

None. The rubric is a complete, operative scoring instrument with no placeholder content.
The prior one-sentence stub in validation-rubric.md has been fully replaced.

## Self-Check

### Files exist
- [x] `first-principles-thinking/references/validation-rubric.md` — 285 lines, verified

### Commits exist
- [x] ba84526 — feat(03-01): author validation rubric preamble and scoring model

### Acceptance criteria verified
- [x] Line 1 is exactly `# Validation Rubric`
- [x] No YAML frontmatter (no `---` in first 3 lines)
- [x] Block-quote (`>`) scope note immediately under H1
- [x] H2 "Scoring Model" and H2 "Verdict Block Format" headings present
- [x] Rigorous, Sound, Hand-wavy, Absent defined with bold-lead-in bullets in rank order
- [x] Gate references `Absent` label; cap references `Hand-wavy` label with "two or more"
- [x] Exactly 2 fenced code blocks in Verdict Block Format section (both no language tag)
- [x] No fenced code block carries a language specifier (4 total fence markers, 0 with language)
- [x] Exactly 6 `## Criterion` H2 headings in methodology-phase order
- [x] Each band label appears >=6 times (Rigorous:7, Sound:7, Hand-wavy:8, Absent:8)
- [x] Criterion 2 references four-type scheme and Assumptions Table columns
- [x] Criterion 3 references GT-IDs and `GT-N?` suffix
- [x] Criterion 4 references derivation chains, intermediate step requirement, no-analogies ban
- [x] Criterion 6 references Conclusion section tracing to named derivation chains
- [x] Criterion 1 and Criterion 4 each contain escape-valve policing descriptor
- [x] No level descriptor uses "adequate", "sufficient", or "thorough"
- [x] File ends with `---` and H2 "Usage Note" section
- [x] File is 285 lines (minimum 120)

## Self-Check: PASSED
