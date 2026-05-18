---
phase: 01-sharpen-the-methodology-and-harden-the-output-format
plan: 02
subsystem: output-template
tags: [methodology, output-format, derivation-chains, assumptions-table, strict-shape]
dependency_graph:
  requires: []
  provides: [output-template.md]
  affects: [01-03-PLAN.md (test-run uses this template), Phase 2 SKILL.md embed]
tech_stack:
  added: []
  patterns: [strict-shape-document, honest-depth-escape-valve, derivation-chain-format, five-column-assumptions-table, stable-gt-ids]
key_files:
  created:
    - .planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/output-template.md
  modified: []
decisions:
  - Honest-depth escape valve (`Nothing material here — [reason]`) defined in the preamble and in the Abandoned Reasoning section — prevents box-ticking while keeping the six-section audit shape intact (D-01)
  - Five-column Assumptions Table (Assumption, Type, Treatment, Verdict, Verification) with four locked types and prescribed treatments per D-06
  - Derivation chains require at least one intermediate step per D-02 (Pitfall 5 guard); a GT-N + GT-M -> conclusion chain without an intermediate is explicitly declared incomplete
  - D-07 confidence caveat rule stated inline in Section 4: any chain including a GT-N? input must end with MEDIUM or LOW confidence naming the unverified input
  - Abandoned Reasoning section declared required in every analysis (D-03), with Nothing material here escape valve for analyses with no dead ends
metrics:
  duration_minutes: 3
  completed_date: "2026-05-16T19:36:55Z"
  tasks_completed: 2
  tasks_total: 2
  files_created: 1
  files_modified: 0
---

# Phase 01 Plan 02: Author Output Template Summary

## One-liner

Strict-shape six-section output template with five-column classified assumptions table, stable GT-ID ground truths, per-conclusion derivation chains with mandatory intermediates, required Abandoned Reasoning section, and D-07 confidence caveats.

## What Was Built

`output-template.md` — the standardized document shape every first-principles analysis fills in. The template enforces the strict-shape / honest-depth contract (D-01): all six sections must appear in fixed order; any section with no genuine content is marked `Nothing material here — [reason]` rather than omitted or box-ticked.

### Section inventory

1. **Problem Essence** — single-sentence core problem + measurable success criteria
2. **Assumptions Table** — five-column classified form (Assumption, Type, Treatment, Verdict, Verification) with four types (physical law, current constraint, convention, untested belief) and their prescribed treatments per D-06, plus the stakes-escalation rule and verdict vocabulary (Accept / Challenge / Discard)
3. **Ground Truths** — stable GT-ID notation: verified form `**GT-N** fact — source: [...]` and unverified form `**GT-N?** fact — unverified: [...]` per D-07; IDs declared stable once assigned
4. **Derivation Chains** — `GT-N + GT-M → [intermediate claim] → [conclusion]` format per D-02; one chain per conclusion; intermediate mandatory (Pitfall 5 guard); unverified-input confidence caveat rule stated inline
5. **Abandoned Reasoning** — required section with three bold fields (`**What was tried:**`, `**Why abandoned:**`, `**What it ruled out:**`) per D-03; `Nothing material here` escape valve defined for analyses with no dead ends
6. **Conclusion** — four fields (`**Recommended approach:**`, `**Key insight:**`, `**Trade-offs acknowledged:**`, `**Confidence:**`) with D-07 caveat requirement for MEDIUM/LOW conclusions

## Task Completion

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Author sections 1-3 (Problem Essence, Assumptions Table, Ground Truths) | 5254467 | output-template.md (created, 84 lines) |
| 2 | Author sections 4-6 (Derivation Chains, Abandoned Reasoning, Conclusion) | 6a735f1 | output-template.md (appended, 145 lines total) |

## Requirements Satisfied

| Requirement | Satisfied By |
|-------------|-------------|
| METH-04 (strict output template with required sections) | Six numbered H2 sections in fixed order; preamble states the strict-shape rule; escape valve defined |
| METH-05 (explicit conclusion-to-ground-truth traceability map) | Section 4 Derivation Chains with stable GT-IDs, per-conclusion chains, mandatory intermediates |

## Key Decisions Made

- **Strict-shape preamble as the first thing the template states** — the user reading the template sees the rule before any section, not buried in a footnote
- **Escape valve placed both in preamble and at section level** — preamble defines it globally; Abandoned Reasoning also shows the specific form for that section because D-03 required vs. optional status needed clarification
- **Intermediate requirement stated as a testable rule** — "A chain that goes directly from GT-IDs to conclusion is incomplete" is a falsifiable statement a reviewer can check without interpretation

## Deviations from Plan

None — plan executed exactly as written. Both tasks produced exactly the sections specified. No additional content was added beyond what the plan required.

## Known Stubs

None. `output-template.md` is a pure template document — all fill-in placeholders (`[fact text]`, `[Conclusion text]`, etc.) are intentional template markers, not stubs. The template is the deliverable; the filled-in form is produced by Plan 03 (test-run-draft.md).

## Threat Flags

None. `output-template.md` is non-executable Markdown content with no network surface, no user input handling, no data persistence, and no executable code. Plan threat model T-01-02 disposition: accept.

## Self-Check: PASSED

- [x] `output-template.md` exists at correct worktree path
- [x] Commit 5254467 exists (Task 1)
- [x] Commit 6a735f1 exists (Task 2)
- [x] File has exactly 6 numbered H2 sections in order `## 1.` through `## 6.`
- [x] File is 145 lines (exceeds 60-line minimum)
- [x] All must_haves truths verified by grep checks
