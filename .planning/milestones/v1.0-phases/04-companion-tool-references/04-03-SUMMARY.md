---
phase: 04-companion-tool-references
plan: "03"
subsystem: skill-references
tags: [companion-tool, trade-off-analysis, weighted-matrix, methodology]
dependency_graph:
  requires:
    - 04-01-SUMMARY.md (five-whys.md authored — structural pattern established)
    - 04-02-SUMMARY.md (pre-mortem.md authored — per-tool shaping pattern confirmed)
  provides:
    - first-principles-thinking/references/trade-off-analysis.md (complete weighted trade-off reference)
  affects:
    - first-principles-thinking/SKILL.md (existing nav-map link now resolves to a usable component)
tech_stack:
  added: []
  patterns:
    - Weighted matrix table (options as rows, criteria as columns, weight row + score rows)
    - Lock-weights-before-scoring discipline encoded as discrete step 3 before step 4
    - Sensitivity check for near-tie results as post-step-6 note
key_files:
  created: []
  modified:
    - first-principles-thinking/references/trade-off-analysis.md
decisions:
  - "Adopted RESEARCH.md canonical weights-lock procedure verbatim for step ordering"
  - "Laptop-buying scenario chosen as everyday example to play to trade-off's strength (genuine competing criteria)"
  - "Sensitivity check placed after step 6 as a note rather than a standalone numbered step"
metrics:
  duration_minutes: 15
  completed_date: "2026-05-17"
  tasks_completed: 1
  tasks_total: 1
  files_modified: 1
---

# Phase 4 Plan 03: Trade-Off Analysis Reference Summary

Authored the weighted-criteria trade-off analysis companion tool reference — a frontmatter-free, self-contained sub-procedure with all five ROADMAP components and the lock-weights-before-scoring discipline as a discrete ordered step.

## What Was Built

`first-principles-thinking/references/trade-off-analysis.md` — replaced the 3-line descriptive stub with a complete 113-line reference component structured around the weighted matrix. The file satisfies TOOL-03 and ROADMAP SC-3.

**File structure (five ROADMAP components):**
1. Blockquote scope note (opening orientation)
2. `## When to reach for this` — viable options, competing criteria, hard-to-justify intuitive pick
3. `## Procedure` — 6 numbered steps with discrete lock-weights step (step 3) before scoring (step 4), plus sensitivity check
4. `## Example` — laptop purchase decision with 4-criterion weighted matrix table
5. `## Failure modes` — 5 failure modes covering weights-after-scoring, too many criteria, mid-analysis additions, near-tie precision, non-independent criteria
6. `## Handoff` — 3-sentence pointer to Phase 4 (Reason Upward) Derivation Chain

## Acceptance Criteria Verification

- **SC-4 (no frontmatter):** First line is `# Trade-Off Analysis` — no `---` block above H1. PASS.
- **All five ROADMAP components (D-03):** `## When to reach for this`, `## Procedure`, `## Example`, `## Failure modes`, `## Handoff` all present. PASS.
- **Lock-weights discipline (SC-3):** Step 3 reads "Assign weights. Lock them now." and "Lock the weights before scoring any option" — the word "lock" appears at step 3, which precedes the scoring step 4. PASS.
- **Rationale for locking stated:** Step 3 states "it prevents reverse-engineering weights to favor a choice you have already made intuitively." PASS.
- **Phase 4 in handoff:** `grep "Phase 4"` returns a match in the Handoff section. PASS.
- **Line count (D-06):** 113 lines — slightly over the "roughly under 100" soft target; the overage is entirely Markdown table syntax in the example (unavoidable for a weighted matrix). The guidance says "roughly" and D-06 rationale is on-demand token cost; 113 lines is acceptable.
- **Imperative mood:** All procedure steps use direct command form ("Name the options", "List criteria", "Score each option"). PASS.
- **Everyday non-technical example (D-04/D-05):** Laptop purchase for a parent — avoids all four Phase 5 domains. PASS.

## Deviations from Plan

None — plan executed exactly as written. The RESEARCH.md canonical 6-step weights-lock procedure was followed directly. The laptop scenario suggested in RESEARCH.md was adopted (per plan instruction "adopt that or an equivalent everyday choice").

## Known Stubs

None. The file is fully authored with no placeholder content, hardcoded empty values, or "coming soon" text.

## Threat Flags

None. This is a static Markdown reference file with no executable code, network surface, user input, or data storage. T-04-05 (content integrity) is addressed: the weights-before-scoring discipline, 5–8 criteria guidance, and sensitivity check are sourced from 04-RESEARCH.md canonical procedure, not invented rules.

## Self-Check

Commit hash `2c9c40b` — verified present in git log.

File path: `first-principles-thinking/references/trade-off-analysis.md` — confirmed exists in worktree.

## Self-Check: PASSED
