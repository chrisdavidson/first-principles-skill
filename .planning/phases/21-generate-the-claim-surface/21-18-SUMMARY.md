---
phase: 21-generate-the-claim-surface
plan: 18
subsystem: testing
tags: [gate-scripts, self-test, roster-floor, falsification, python]

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    provides: "plan 21-16's ledger ratchet/staleness floors and the wave-15 roster-floor negative arms this plan hardens"
provides:
  - "A `_roster_arm_clauses(text) -> tuple[str, str]` helper, textually identical across five gate scripts, that splits a roster-floor message into its `missing=`/`extra=` clauses and raises `ValueError` on a malformed message instead of silently degrading"
  - "Five roster-floor negative arms (check-act-limb.py, check-selfaudit-scan.py, sync-content.py, check-step0-live.py, check-step0-emulator.py) that assert their synthetic id landed in the correct clause, not merely somewhere in the joined message"
affects: [21-19]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Roster-floor negative arm: split the shared missing=/extra= message into clauses via a copied (not imported) pure helper, then assert per-clause membership so a polarity swap is caught by name"

key-files:
  created: []
  modified:
    - scripts/check-act-limb.py
    - scripts/check-selfaudit-scan.py
    - scripts/sync-content.py
    - scripts/check-step0-live.py
    - scripts/check-step0-emulator.py

key-decisions:
  - "Copied the `_roster_arm_clauses` helper body verbatim into all five files rather than importing it — matches the repo's standing idiom of copied text over cross-script imports (the `_BATTERY_GATE_RE` precedent in `scripts/_gate_registry.py`), and plan 21-19's planned census keys on the literal token appearing identically in all five."
  - "Left `check-act-limb.py`'s WR-09 `(describe)`-registration adjacency untouched, per the plan's explicit out-of-scope note — it sits a few lines below this plan's edit in the same function but is a separate, already-backlogged defect."

requirements-completed: [CONF-11]

# Metrics
duration: 5min
completed: 2026-09-07
---

# Phase 21 Plan 18: Clause-Asserting Roster Negative Arms Summary

**Five gate scripts' roster-floor negative arms now assert which of `missing=`/`extra=` their synthetic id landed in, via a copied `_roster_arm_clauses` helper that raises loudly on a malformed message instead of degrading silently — closing GAP A item 2's five-file blind spot where a polarity swap previously passed green.**

## Performance

- **Duration:** ~5 min (task work); commits at 14:54 and 14:58 local
- **Started:** 2026-09-07T18:49:00Z (approx, worktree base reset)
- **Completed:** 2026-09-07T18:58:43Z
- **Tasks:** 2 completed
- **Files modified:** 5

## Accomplishments
- Ported the `check-agent.py:675-676` clause-split idiom into `check-act-limb.py`, `check-selfaudit-scan.py` and `sync-content.py` (Task 1), then into `check-step0-live.py` and `check-step0-emulator.py` (Task 2) — five textually-identical `_roster_arm_clauses` helpers, verified via AST-extracted body diff (all five identical, zero diff output).
- Rewrote all five roster-floor negative arms to split the joined message and assert `synthetic-b` is in the MISSING clause and `synthetic-c` is in the EXTRA clause, replacing the whole-joined-message `"synthetic-b" not in <text>` shape (now 0 occurrences across the entire `scripts/` directory, was 5).
- Added a message-shape guard: `_roster_arm_clauses` raises `ValueError` naming the offending text if `"missing="` or `" extra="` is absent, so a future message-format change fails loudly across all five files at once instead of silently restoring the blindness this plan removes.
- Ran all seven falsification arms specified by the plan on `rsync -a --exclude .git` scratch copies (never the real tree — `git status --porcelain` confirmed empty of unintended changes before and after every scratch run).
- Full `bash scripts/check-firewall-battery.sh` run: FIREWALL GREEN, 26/26 (installed pytest via `uv sync` per the documented remedy to clear VAL-03's third leg, which reported `[PREREQ]`/BLOCKED on the first run due to no pytest-capable interpreter in this fresh worktree). `check-registration.py` and `sh .githooks/pre-commit` both exit 0.

## Task Commits

Each task was committed atomically:

1. **Task 1: Port the clause split into check-act-limb, check-selfaudit-scan and sync-content** - `b9da854` (fix)
2. **Task 2: Port the clause split into check-step0-live and check-step0-emulator** - `8577c10` (fix)

**Plan metadata:** (this commit, docs: complete plan — committed by the orchestrator's worktree-merge step, not by this executor)

## Files Created/Modified
- `scripts/check-act-limb.py` - Added `_roster_arm_clauses`; rewrote `(roster-floor-missing/extra)` arm to assert per-clause membership.
- `scripts/check-selfaudit-scan.py` - Same, on `_selfaudit_meta_floor_problems`'s arm (block position before `(describe)` preserved unchanged).
- `scripts/sync-content.py` - Same, on control `(m)` (the `try/except Exception` wrapper and `FAIL (m): ...` prefix preserved unchanged).
- `scripts/check-step0-live.py` - Same, on `_step0_control_roster_problems`'s arm.
- `scripts/check-step0-emulator.py` - Same, on the `SEMGATE02-floor-negative` arm against `set[str]`-typed synthetic pairs (types preserved, not converted to list/tuple).

## Decisions Made
- Helper placement: immediately after each file's own roster-floor helper function, per the plan's explicit instruction — keeps the helper adjacent to the one function it exists to support in each file.
- Diagnostic text: extended each arm's PASS/FAIL print to show both `missing_clause=` and `extra_clause=` explicitly (plan-required: "extend the printed diagnostic to show both clauses so a future failure is diagnosable from the log alone").

## Deviations from Plan

None - plan executed exactly as written. The only environment-level action beyond the plan's own tasks was running `uv sync` to install pytest for the firewall battery's VAL-03 third leg — this is CLAUDE.md's own documented remedy for a fresh worktree lacking a pytest-capable interpreter, not a change to any file the plan modifies, and is required by the plan's own verification block (`bash scripts/check-firewall-battery.sh` GREEN, total 26).

## Falsification Arms — Exact Recorded Results

**Falsification 1 (`check-act-limb.py` polarity swap):** `--self-test` exit 1.
`check-act-limb --self-test: FAIL — (m): main(['--self-test']) returned 1, expected 0; (roster-floor-missing/extra): floor did not name both directions`
`(roster-floor-missing/extra) negative arms: WRONGLY FAILED — fired but did not name both the missing and extra synthetic ids in their correct clauses: missing_clause="['synthetic-c']" extra_clause="['synthetic-b']"`

**Falsification 2 (`check-selfaudit-scan.py` polarity swap):** `--self-test` exit 1.
`check-selfaudit-scan --self-test: FAIL — (dispatch): main(['--self-test']) returned 1, expected 0; (roster-floor-missing/extra): floor did not name both directions`
`(roster-floor-missing/extra) negative arms: WRONGLY FAILED — fired but did not name both the missing and extra synthetic ids in their correct clauses: missing_clause="['synthetic-c']" extra_clause="['synthetic-b']"`

**Falsification 3 (`sync-content.py` polarity swap):** `--self-test` exit 1.
`FAIL (m): _control_roster_problems fired but did not name both the missing and extra synthetic ids in their correct clauses: missing_clause="['synthetic-c']" extra_clause="['synthetic-b']"`

**Falsification 4 (message-shape guard, `check-act-limb.py`, `" extra="` marker deleted):** `--self-test` exit 1, via raised `ValueError`, not a silent pass.
`(m) dispatch control: WRONGLY FAILED — unexpected exception: ValueError('roster arm message missing \'missing=\'/\' extra=\' markers: "control roster/executed mismatch: missing=[\'synthetic-b\'] [\'synthetic-c\']"')`
followed by the same `ValueError` propagating to top-level traceback output.

**Falsification 5 (`check-step0-live.py` polarity swap):** `--self-test` exit 1.
`self-test FAIL: (roster-floor-missing/extra) negative arms — fired but did not name both the missing and extra synthetic ids in their correct clauses: missing_clause="['synthetic-c']" extra_clause="['synthetic-b']"`

**Falsification 6 (`check-step0-emulator.py` polarity swap):** `--self-test` exit 1.
`check-step0-emulator --self-test: FAIL — SEMGATE02-floor-negative (floor did not name both directions)`
`check-step0-emulator --self-test: SEMGATE02-floor-negative WRONGLY FAILED — fired but did not name both synthetic ids in their correct clauses: missing_clause="['synthetic-c']" extra_clause="['synthetic-b']"`

**Falsification 7 (cross-file completeness, `check-act-limb.py`):** File reverted to the whole-joined-message arm shape, then polarity-swapped.
- Verdict 1 (reverted shape, no polarity swap): `--self-test` exit 0 — `(roster-floor-missing/extra) negative arms: PASS — fires and names both directions: ["control roster/executed mismatch: missing=['synthetic-b'] extra=['synthetic-c']"]`
- Verdict 2 (reverted shape + polarity swap): `--self-test` exit 0 (WRONGLY green) — `(roster-floor-missing/extra) negative arms: PASS — fires and names both directions: ["control roster/executed mismatch: missing=['synthetic-c'] extra=['synthetic-b']"]`

This confirms the clause-split fix is what does the work: a single un-ported file's arm silently accepts a swapped message, reopening exactly the hole this plan closes elsewhere — the case plan 21-19's standing census exists to prevent recurring undetected.

Real tree `git status --porcelain` confirmed empty of unintended changes before and after every scratch-copy falsification run (only the plan's five named files were ever modified in the real tree, each staged and committed per-task).

## WR-09 Adjacency (deliberately not touched)

`21-REVIEW.md`'s WR-09 — `check-act-limb.py`'s `(describe)` control executes but is not registered in `_CONTROL_IDS`, so `docs/gates/HARN-01.md` publishes 78 for a run that executes 79 — sits a few lines below this plan's edit in the same self-test function. Per the plan's explicit instruction this was noted but not fixed, not renumbered, and not expanded into; it remains parked to backlog by the verifier's own recommendation.

## Verification Evidence

- `python3 scripts/check-act-limb.py --self-test`, `check-selfaudit-scan.py --self-test`, `sync-content.py --self-test`, `sync-content.py --check`, `check-step0-live.py --self-test`, `check-step0-emulator.py --self-test` — all exit 0.
- `def _roster_arm_clauses(` count = 1 in each of the five files; AST-extracted function bodies diffed pairwise — all five identical (zero diff output).
- `/usr/bin/grep -rc '"synthetic-b" not in _synthetic_text\|"synthetic-b" not in _semgate02_synthetic_text\|"synthetic-b" not in problem_text' scripts/` = 0 across the whole directory (was 5 files carrying the shape).
- `--describe` JSON captured before (via `git show HEAD:<file>`) and after for all five scripts: byte-identical in every case (act-limb, selfaudit-scan, sync-content, step0-live, step0-emulator).
- `python3 scripts/sync-content.py --check` exit 0.
- `python3 scripts/gen-gate-docs.py --check` exit 0, 0 `DRIFT:` lines.
- `bash scripts/check-firewall-battery.sh`: `FIREWALL: GREEN (26/26)` (after `uv sync` installed pytest for VAL-03's third leg — first run without it reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 25/26 passed)`, the documented BLOCKED/exit-2 outcome distinct from a genuine RED failure).
- `python3 scripts/check-registration.py` exit 0.
- `sh .githooks/pre-commit` exit 0.
- `git status --porcelain` empty (real tree) before and after every falsification arm; only the five plan-named files carried real, committed changes.

## Issues Encountered
None beyond the expected first-run VAL-03 PREREQ/BLOCKED state in a fresh worktree lacking `.venv` — resolved via `uv sync` per CLAUDE.md's own documented remedy, not a plan deviation.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All five wave-15 roster-floor negative arms now name the clause they assert, with the shared helper carrying the message-shape guard.
- Plan 21-19's standing census (referenced throughout this plan and directly motivated by Falsification 7) is unblocked: the identical `_roster_arm_clauses` token now exists verbatim in all five files for that census to key on.
- No blockers.

## Self-Check: PASSED

- FOUND: scripts/check-act-limb.py (modified, contains `_roster_arm_clauses`)
- FOUND: scripts/check-selfaudit-scan.py (modified, contains `_roster_arm_clauses`)
- FOUND: scripts/sync-content.py (modified, contains `_roster_arm_clauses`)
- FOUND: scripts/check-step0-live.py (modified, contains `_roster_arm_clauses`)
- FOUND: scripts/check-step0-emulator.py (modified, contains `_roster_arm_clauses`)
- FOUND: commit b9da854 (Task 1)
- FOUND: commit 8577c10 (Task 2)

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-07*
