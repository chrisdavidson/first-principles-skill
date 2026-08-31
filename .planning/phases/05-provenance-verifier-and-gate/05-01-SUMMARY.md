---
phase: 05-provenance-verifier-and-gate
plan: 01
subsystem: testing
tags: [python, defect-schema, self-test, tsv, quality-harness]

# Dependency graph
requires:
  - phase: 04-capture-retention-and-fixture-foundation
    provides: "the frozen tests/quality-provenance-v8.24/ fixture and _capture_subagent_tool_calls entry point"
provides:
  - "_DEFECT_RECORD_FIELDS widened from 13 to 22 names (PROV-05, D-11) — nine provenance columns appended, never inserted"
  - "detect_defects fills the nine new keys with the string \"n/a\" sentinel (D-09, D-10), so run_detect_defects's emit line cannot KeyError"
  - "_selftest_incidence_schema_compat extended to prove ten-, thirteen- and twenty-two-column defect-incidence files parse to identical untraced/verdict/chain sums (D-12), that the n/a sentinel perturbs none of them, and that ragged-row / missing-chain_flag failures stay loud at the new width"
affects: [05-02-provenance-verifier, 06-gate-registration-and-ci]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Appended-not-inserted schema columns with header-keyed readers (repeats the v8.18 10->13 widening pattern at 13->22)"
    - "Explicit non-numeric string sentinel (\"n/a\") for not-yet-computed record fields, distinct from a numeric default"

key-files:
  created: []
  modified:
    - scripts/check-quality-harness.py

key-decisions:
  - "D-11/D-12 implemented exactly as locked: nine names appended after selfaudit_disagreements, first 13 names byte-unchanged and in order"
  - "wide_header re-anchored to _DEFECT_RECORD_FIELDS[:13] (pinned to the v8.18-era shape) rather than left as an unsliced join, which the widening would otherwise silently break"
  - "widest_header/widest_row (22-column, n/a-filled) added once and reused across controls (c), (i), (j), (k) — no second TSV reader introduced"

patterns-established:
  - "Three-width TSV compatibility self-test (ten/thirteen/twenty-two columns) as the template for any future _DEFECT_RECORD_FIELDS widening"

requirements-completed: [PROV-05]

# Metrics
duration: 25min
completed: 2026-08-31
---

# Phase 5 Plan 1: Widen the defect-record schema for provenance findings Summary

**`_DEFECT_RECORD_FIELDS` grows from 13 to 22 named columns with a string `"n/a"` sentinel default, and `_selftest_incidence_schema_compat` now proves ten-, thirteen- and twenty-two-column defect-incidence files parse to identical flag sums.**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-08-31T16:41:39Z (per STATE.md `last_activity`)
- **Completed:** 2026-08-31T16:48:05Z
- **Tasks:** 2/2
- **Files modified:** 1

## Accomplishments
- `_DEFECT_RECORD_FIELDS` widened 13 → 22 names, appended not inserted; the first 13 are byte-identical to their pre-plan state.
- `detect_defects` fills the nine new keys with the string `"n/a"` via a single `record.update({...})`, computing no real provenance value and gaining no capture argument (D-09).
- `_selftest_incidence_schema_compat` extended with controls (i), (j), (k): three widths agree, the sentinel perturbs no int-summed flag, and loudness (ragged row, missing `chain_flag`) survives the widening while a renamed `provenance_flag` column does not raise (it is deliberately outside `_REQUIRED`).
- `python3 scripts/check-quality-harness.py --self-test` exits 0; `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (22/22)` after provisioning a pytest-capable `.venv` via `uv sync` (the worktree had none).
- `git diff --name-only` against the plan's start lists exactly `scripts/check-quality-harness.py`; nothing was written into the frozen `tests/quality-provenance-v8.24/` fixture directory.

## Task Commits

Each task was committed atomically:

1. **Task 1: Append the nine provenance names and the `n/a` sentinel, and re-anchor the two derived-width controls** - `ef416b8` (feat)
2. **Task 2: Extend `_selftest_incidence_schema_compat` to prove three widths and the sentinel row (D-12)** - `2c298c0` (test)

_Note: this plan's tasks were not marked `tdd="true"`; the `feat`/`test` typing above reflects each task's dominant change (schema + sentinel vs. self-test controls), not a RED/GREEN/REFACTOR gate sequence._

## Files Created/Modified
- `scripts/check-quality-harness.py` - `_DEFECT_RECORD_FIELDS` widened to 22 names; `detect_defects` fills the nine new keys with `"n/a"`; `_selftest_incidence_schema_compat` re-anchored to three pinned widths (10/13/22) with new controls (i)/(j)/(k) and an updated docstring

## Decisions Made
- Followed the plan's locked design exactly: `widest_row` is a literal string concatenation (`wide_row + "\tn/a" * 9`), not derived by calling `detect_defects` — this keeps controls (i)-(k) width/sentinel-focused per D-12, not a field-name-alignment check (see Issues Encountered for the consequence of this).
- No new self-test item was added and no second TSV reader was introduced, per Task 2's explicit scope constraint.

## Deviations from Plan

None - plan executed exactly as written. Both tasks' `<action>` instructions were followed literally; no Rule 1-4 auto-fixes were needed.

## Issues Encountered

**Two acceptance-criteria mismatches, observed and recorded rather than silently worked around:**

1. **`grep -c '# (i)\|# (j)\|# (k)' scripts/check-quality-harness.py` returns `6`, not the `3` the acceptance criteria predicted.** The file already contained three pre-existing, unrelated `# (i)`-style comments elsewhere (lines 5494, 5814, 6725 — different self-test functions with their own lettered control lists) before this plan touched it. The three new markers this plan added (`# (i)`, `# (j)`, `# (k)`, one each, inside `_selftest_incidence_schema_compat`) are present exactly once each, confirmed by `grep -n`. The acceptance criteria's literal grep command is file-wide and was not scoped to the new function, so it could not have returned `3` even before this plan ran.

2. **`python3 scripts/check-quality-harness.py --self-test 2>&1 | grep -ci 'incidence_schema_compat'` returns `1`, not the `0` the acceptance criteria predicted.** The harness always prints a completion line (`self-test: incidence_schema_compat sub-check PASSED`) that contains the search string on every successful run — this is the normal PASS confirmation, not a FAIL line, and would return `1` on any green run of this repo regardless of what this plan changed. No FAIL line was ever printed under this control family; confirmed by a full self-test run and by the exit-0 mutation test below.

3. **The mutation test instructed by Task 2's acceptance criteria was run exactly as specified, and its predicted outcome did not hold — recorded honestly per the instruction to "record both observations."** Renamed `provenance_flag` → `provenance_flagXX` in `_DEFECT_RECORD_FIELDS` (the tuple only; `detect_defects`'s literal key stayed `"provenance_flag"`), then ran `python3 scripts/check-quality-harness.py --self-test`: **exit 0, no FAIL lines** — controls (i)/(j)/(k) did not catch the rename. This is a direct consequence of following Task 1's own locked design: `widest_header`/`widest_row` are built from `_DEFECT_RECORD_FIELDS` and a hardcoded string literal respectively, never from a `detect_defects()` call, so controls (i)-(k) validate column-count/width compatibility and sentinel-safety, not name-alignment between the tuple and `detect_defects`'s returned dict. That alignment was instead verified manually per Task 1's own acceptance criteria (`all(f in record for f in _DEFECT_RECORD_FIELDS)` — confirmed `True` before this rename was applied) and is enforced at runtime by `run_detect_defects`'s `str(record[field])` emit line, which would raise a loud `KeyError` on a real invocation, not silently mismatch — the T-164-12 loud-failure discipline is intact even though no self-test control specifically drills it. The rename was fully reverted; `python3 scripts/check-quality-harness.py --self-test` confirmed exit 0 again afterward, and `git diff --stat` shows only the plan's intended 56-line addition (no leftover mutation).

Neither mismatch changes the plan's substantive outcome — `_DEFECT_RECORD_FIELDS` is 22 names, the first 13 unchanged; `detect_defects` fills the nine new keys with `"n/a"`; three widths are proven to parse identically; the sentinel is proven to perturb nothing; and ragged-row / missing-`chain_flag` loudness survives the widening. Both are documented here as observed fact rather than silently claimed as passing, per the definition-of-done rule.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `_DEFECT_RECORD_FIELDS` now carries the nine named columns plan 05-02 (`check-provenance.py`) needs to land its findings in, with the `"n/a"` sentinel proven safe through three widths.
- Nothing blocks plan 05-02: `check-provenance.py` can import the harness one-way (`spec_from_file_location`, D-09) and overwrite the nine sentinel keys with real values from its own capture-aware logic; the harness computes no provenance value itself.
- A worktree-local gap (no `.venv`) was closed via `uv sync` to run the firewall battery to completion; this is environment provisioning, not a code change, and required no plan-file edits.

---
*Phase: 05-provenance-verifier-and-gate*
*Completed: 2026-08-31*

## Self-Check: PASSED

- FOUND: scripts/check-quality-harness.py
- FOUND: .planning/phases/05-provenance-verifier-and-gate/05-01-SUMMARY.md
- FOUND: ef416b8 (Task 1 commit)
- FOUND: 2c298c0 (Task 2 commit)
- FOUND: ddd3df7 (SUMMARY commit)
