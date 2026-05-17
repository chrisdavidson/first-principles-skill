---
phase: 04-companion-tool-references
plan: "02"
subsystem: skill-references
tags: [pre-mortem, companion-tools, prospective-hindsight, failure-analysis, references]
dependency_graph:
  requires: []
  provides: [TOOL-02]
  affects: [first-principles-thinking/references/pre-mortem.md]
tech_stack:
  added: []
  patterns: [prospective-hindsight-framing, imperative-procedure, section-dividers, pointer-handoff]
key_files:
  modified:
    - first-principles-thinking/references/pre-mortem.md
decisions:
  - "Wrote procedure as solo-compatible (independent write step) per RESEARCH.md Open Questions item 2 resolution"
  - "Used dinner-party scenario from RESEARCH.md suggestions (D-05) — everyday domain, plays to pre-mortem's failure-anticipation strength"
  - "Kept framing blockquote verbatim from canonical RESEARCH.md pattern with minor adaptation (specific date → 'approximately six months')"
  - "Included group-facilitation anchoring in Failure modes rather than Procedure (solo-primary framing per plan)"
metrics:
  duration: "~8 minutes"
  completed: "2026-05-17T14:52:46Z"
  tasks_completed: 1
  files_modified: 1
---

# Phase 04 Plan 02: Pre-Mortem Reference Component Summary

Authored `first-principles-thinking/references/pre-mortem.md` — a frontmatter-free, self-contained pre-mortem reference built around mandatory prospective-hindsight framing. Replaces the descriptive stub with a complete, runnable sub-procedure covering all five ROADMAP components plus the extra Framing section required by SC-2.

## Tasks Completed

| # | Task | Commit | Files |
|---|------|--------|-------|
| 1 | Author pre-mortem.md — prospective-hindsight failure analysis reference | 8b3d842 | first-principles-thinking/references/pre-mortem.md |

## What Was Built

`first-principles-thinking/references/pre-mortem.md` is a 106-line Layer-3 on-demand reference component containing:

- **Opening blockquote** — one-sentence orientation (what the tool does, the trigger condition)
- **When to reach for this** — use case with timing guidance and negative contrast (not for option evaluation or past-failure tracing)
- **Framing** — mandatory past-tense prospective-hindsight premise as a blockquote, with explanation of why the grammatical shift matters and instruction not to soften it
- **Procedure** — 5-step imperative-mood solo procedure: restate premise → write independently → interrogate adversarially → identify patterns → act on findings
- **Example** — dinner-party scenario showing framing applied, backward-derived causes, and pattern identified
- **Failure modes** — forward-looking framing, premature application, anchoring (group and first-speaker), no follow-through
- **Handoff** — 3-sentence pointer to Phase 5 (Validate), naming the adversarial validation pass as the artifact

All sections separated by `---` dividers per established pattern. No YAML frontmatter (SC-4).

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Solo-primary procedure framing | RESEARCH.md Open Questions item 2 resolved: write for Claude applying the tool alone; group facilitation notes belong in Failure modes |
| Dinner-party mini-example | Suggested in RESEARCH.md (D-05 Claude's discretion); everyday domain, enough specificity, plays directly to pre-mortem's failure-anticipation strength |
| Canonical framing blockquote with minor adaptation | RESEARCH.md Framing Block Pattern used verbatim structure; adapted "specific future date" to "approximately six months from now" for generality |
| 106 lines (slightly over "roughly under 100") | All content carries weight; removing more would sacrifice coverage of distinct failure modes or example clarity. "Roughly" in D-06 accommodates this |

## Deviations from Plan

None — plan executed exactly as written. The file path is unchanged (stub replaced in place), no frontmatter was added, all five ROADMAP components plus the Framing section are present.

## Verification Results

- First line: `# Pre-Mortem` (SC-4 satisfied)
- No `---` block above the title (no frontmatter)
- All six sections present: When to reach for this, Framing, Procedure, Example, Failure modes, Handoff (D-03 + D-01 extra Framing section)
- Framing blockquote uses past tense: "has failed — not merely underperformed, but failed badly"
- Framing appears at line 18; Procedure at line 33 (Framing precedes Procedure — SC-2)
- Procedure step 1 re-invokes the premise ("The plan has already failed. What caused it?")
- Handoff contains "Phase 5" (grep confirmed)
- Line count: 106 (roughly within D-06 budget)
- Procedure steps use imperative mood throughout

## Known Stubs

None — the stub was replaced with complete, self-contained content. No placeholder text remains.

## Threat Flags

None — static Markdown file with no network surface, no executable code, no user input handling.

## Self-Check: PASSED

- [x] `first-principles-thinking/references/pre-mortem.md` exists and contains full content
- [x] Commit 8b3d842 exists on worktree-agent branch
- [x] No YAML frontmatter
- [x] All required sections present
- [x] Phase 5 reference present in Handoff
- [x] SUMMARY.md created at correct path
