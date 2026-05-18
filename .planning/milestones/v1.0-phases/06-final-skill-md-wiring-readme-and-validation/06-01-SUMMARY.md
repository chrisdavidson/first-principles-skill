---
phase: 06-final-skill-md-wiring-readme-and-validation
plan: "01"
subsystem: dev-tooling
tags: [markdownlint, validation, md040-fixes, link-check]
dependency_graph:
  requires: []
  provides: [markdownlint-gate, link-resolution-gate]
  affects: [first-principles-thinking/SKILL.md, first-principles-thinking/references/output-template.md, first-principles-thinking/references/validation-rubric.md, first-principles-thinking/examples/software-systems.md]
tech_stack:
  added: [markdownlint-cli2 (npx), bash link-check script]
  patterns: [jsonc config, host-side validation tooling]
key_files:
  created:
    - .markdownlint.jsonc
    - dev/check-links.sh
  modified:
    - first-principles-thinking/SKILL.md
    - first-principles-thinking/references/output-template.md
    - first-principles-thinking/references/validation-rubric.md
    - first-principles-thinking/examples/software-systems.md
decisions:
  - "MD013 intentionally excluded from .markdownlint.jsonc per D-06 (skill prose is long-line)"
  - "Link-resolution script committed to dev/ (not inside skill directory) per D-05 and pure-Markdown v1 constraint"
  - "Used 'text' as language specifier for all 5 MD040 fixes (format strings, not code)"
metrics:
  duration: "1 min"
  completed: "2026-05-18"
  tasks: 2
  files_changed: 6
---

# Phase 6 Plan 1: Validation Tooling and MD040 Fixes Summary

## One-liner

Markdownlint config (MD003/MD040/MD041 on, MD013 off) and host-side link-check script created; 5 MD040 fenced-code violations fixed across 4 skill files, markdownlint-cli2 now reports 0 errors.

## What Was Built

**Task 1: Create the markdownlint config and link-resolution check**

Created `.markdownlint.jsonc` at repo root with `default: false` and MD003/MD040/MD041 enabled (MD013 intentionally absent per D-06). Created `dev/check-links.sh` — a bash script that greps relative Markdown links from `SKILL.md references/*.md examples/*.md` and asserts each target file exists. The script is executable and reports "All links resolve OK" for all 9 skill cross-references.

**Task 2: Fix the 5 MD040 fenced-code violations**

Added `text` language specifier to 5 opening code fence lines that had no language specifier:
- `first-principles-thinking/SKILL.md` line 136: derivation chain format block
- `first-principles-thinking/references/output-template.md` line 99: chain format block
- `first-principles-thinking/references/validation-rubric.md` line 95: standard verdict block template
- `first-principles-thinking/references/validation-rubric.md` line 108: gap-citation verdict block template
- `first-principles-thinking/examples/software-systems.md` line 162: failed reasoning chain example

## Commits

| Task | Commit | Files |
|------|--------|-------|
| Task 1: markdownlint config + link check | 6b46498 | `.markdownlint.jsonc`, `dev/check-links.sh` |
| Task 2: MD040 fixes | 0b010ac | `SKILL.md`, `output-template.md`, `validation-rubric.md`, `software-systems.md` |

## Verification Results

All four plan-level verification checks passed:
- `.markdownlint.jsonc` exists at repo root, contains `"MD040": true`, does not contain `MD013`
- `dev/check-links.sh` exists, is executable, line 1 is `#!/usr/bin/env bash`
- `bash dev/check-links.sh` prints `All links resolve OK` and exits 0
- `npx markdownlint-cli2 "first-principles-thinking/**/*.md" --config .markdownlint.jsonc` reports `Summary: 0 error(s)` across 10 files
- No Layer-3 file (`references/`, `examples/`) gained YAML frontmatter

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

None. All files are fully functional validation tooling and content fixes.

## Threat Flags

None. This plan created a local config file, a local bash script, and fixed 5 whitespace-level Markdown attributes. No network endpoints, auth paths, file access patterns at trust boundaries, or schema changes were introduced.

## Self-Check: PASSED

- `.markdownlint.jsonc` exists: FOUND
- `dev/check-links.sh` exists and executable: FOUND
- Commit 6b46498 exists: FOUND
- Commit 0b010ac exists: FOUND
- markdownlint 0 errors: VERIFIED
- No Layer-3 frontmatter added: VERIFIED
