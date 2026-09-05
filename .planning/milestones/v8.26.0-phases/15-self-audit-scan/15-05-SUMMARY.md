---
phase: 15-self-audit-scan
plan: 05
subsystem: testing
tags: [validation-gate, self-audit-scan, scan-guard, anti-masking, fail-closed]

# Dependency graph
requires:
  - phase: 15-self-audit-scan
    provides: SCAN-GUARD gate (scripts/check-selfaudit-scan.py), registered in the battery and CI (15-03, 15-04)
provides:
  - Fail-closed ordering arms in SCAN-GUARD's Rubric-9/Rubric-10 placement checks, routed through a shared normalized-index helper (_find_flat)
  - Wrap-and-relocate negative controls reproducing CR-01's exact fail-open malformation
  - An equality-floored REQUIRED_BRANCHES registry (_BRANCH_ROSTER_LOCK) closing WR-02's silent-narrowing gap
  - Corrected module docstring, doc rows and battery-registration comment stating the gate's real branch count (31) and registration status
affects: [15-06 (clause-level split of remaining multi-arm checks), 15-07 (rubric/agent-body prose)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Normalized-index lookup helper (_find_flat) shared by every ordering/placement assertion in a gate, so one normalization discipline governs the whole file"
    - "Anti-masking registry floored by equality against a second, independently transcribed roster (_BRANCH_ROSTER_LOCK / _roster_problems), with SYNTHETIC-id isolation arms and a source-text call-site census proving the floor's single real call cannot be silently deleted"

key-files:
  created: []
  modified:
    - scripts/check-selfaudit-scan.py
    - scripts/check-firewall-battery.sh
    - CLAUDE.md
    - docs/ARCHITECTURE.md

key-decisions:
  - "Split R-09-crit4/R-10-crit6 into -count/-order branch ids rather than reusing one id for two arms, so the anti-masking registry can see each arm's coverage independently"
  - "_find_flat flattens both haystack and needle on every call rather than caching a pre-flattened haystack across sibling lookups — simpler and correctness-preserving since _flat is idempotent; the file is small enough that the extra normalization pass is not a performance concern"
  - "_BRANCH_ROSTER_LOCK is a hand-typed second transcription, not a derived set — matching the disclosed limitation check-quality-harness.py's ENTRY-SOURCE LOCK states for its own required sides: a transcription of equal value written a different way is harmless and therefore invisible to the floor"

requirements-completed: [SCAN-03]

# Metrics
duration: 25min
completed: 2026-09-04
---

# Phase 15 Plan 05: Close SCAN-GUARD's fail-open ordering arms and unfloored branch registry Summary

**Routed every SCAN-GUARD ordering lookup through a shared `_find_flat` normalized-index helper (closing CR-01's hard-wrap fail-open) and floored `REQUIRED_BRANCHES` by equality against an independently transcribed `_BRANCH_ROSTER_LOCK` (closing WR-02's silent-narrowing gap), then corrected every surface that overstated the gate's branch count or registration status.**

## Performance

- **Duration:** 25 min
- **Started:** 2026-09-04T07:24:55-04:00 (first task commit)
- **Completed:** 2026-09-04T07:28:37-04:00 (second task commit)
- **Tasks:** 2 completed
- **Files modified:** 4 (`scripts/check-selfaudit-scan.py`, `scripts/check-firewall-battery.sh`, `CLAUDE.md`, `docs/ARCHITECTURE.md`)

## Accomplishments
- Closed CR-01: Rubric-9 and Rubric-10's placement assertions no longer fail open when the quoted-span sentence is hard-wrapped and relocated after the Rigorous band bullet — the verifier's own reproduction (hard-wrap + move) now correctly exits 1 with a `Rubric-9` failure, where before this task it measured `Rubric-9 failures: NONE`.
- Closed WR-02: deleting entries from `REQUIRED_BRANCHES` (verifier's exact reproduction: dropping `X-01-cols`/`X-02-heading`) now fails `--self-test` naming `missing=['X-01-cols', 'X-02-heading']`, instead of silently passing with a smaller "All N branches covered" message.
- Deleting the roster floor's own single real call site (not just the isolation arms) now fails `--self-test` by name via a source-text call-site census, closing the R4-CR-01-shaped forgeability gap before it could be introduced.
- Corrected the gate's false "not yet registered" docstring statement and removed the dead `global _SCANGUARD_DISPATCH_REENTRANT` declaration.
- Updated all three surfaces that stated SCAN-GUARD's branch count (`scripts/check-firewall-battery.sh`, `CLAUDE.md`, `docs/ARCHITECTURE.md`) from the stale "twenty-nine" to the actual 31, and replaced the unqualified "each with a per-source negative control" claim with the honest, measured form plus the WR-01 residual note (clause-level splitting for the remaining multi-arm checks is plan 15-06's).

## Task Commits

Each task was committed atomically:

1. **Task 1: Route every ordering lookup through a normalized-index helper and add wrap-and-relocate controls** - `52f84f7` (fix)
2. **Task 2: Floor the branch registry by equality, and correct the gate's own false current-fact statements** - `8f6b815` (fix)

_No separate plan-metadata commit — SUMMARY.md is committed together with the self-check append per the worktree-parallel-executor protocol._

## Files Created/Modified
- `scripts/check-selfaudit-scan.py` - Added `_find_flat` (normalized-index lookup), routed Body-3/Rubric-2/Rubric-9/Rubric-10 through it with fail-closed `-1` guards; added `_hardwrap_relocate_in_range` fixture helper and `R-09c`/`R-10c` wrap-and-relocate negative controls; split `R-09-crit4`/`R-10-crit6` into `-count`/`-order` branch ids (29 → 31 total); added `_BRANCH_ROSTER_LOCK` and `_roster_problems`, wired as a roster-equality-plus-coverage-subset floor ahead of the anti-masking assertion, with three synthetic-id isolation arms and a call-site census; corrected the module docstring's registration paragraph; deleted the dead `global _SCANGUARD_DISPATCH_REENTRANT` statement.
- `scripts/check-firewall-battery.sh` - SCAN-GUARD registration comment updated from "29 named branches" to "31 named branches ... floored by an independent transcription".
- `CLAUDE.md` - SCAN-GUARD gate-table row updated: branch count 29 → 31, added the roster-floor and `_find_flat` closure description, and the WR-01/plan-15-06 residual note.
- `docs/ARCHITECTURE.md` - SCAN-GUARD canonical-inventory row updated with the same count and residual note.

## Decisions Made
- Kept `_find_flat` as a simple two-argument normalize-both-sides function rather than caching a pre-flattened haystack across the two anchor lookups in each ordering arm — the plan's action text illustrated the fix with a locally-precomputed `flat_slice`, but since `_flat` is idempotent and the haystacks here are small (single-criterion slices, not the whole file), calling `_find_flat(crit4_slice, ...)` twice is correctness-equivalent and simpler to read. No behavior difference from the plan's illustrated fix.
- `_BRANCH_ROSTER_LOCK` is a hand-typed second literal rather than a derived set (e.g. `frozenset(x.split('-count')[0] for x in ...)`) — per the plan's explicit instruction to follow `check-quality-harness.py`'s ENTRY-SOURCE LOCK idiom, where the disclosed limitation is that a transcription of equal value is harmless and invisible to the floor; deriving one set from the other would defeat the two-place-edit property the floor exists to provide.
- Did not add a relocate-only (unwrapped) control pair alongside the wrap-and-relocate `R-09c`/`R-10c` controls — the plan said to add one only if the wrapped form couldn't be constructed for a criterion slice, and it could be, using the same helper for both Criterion 4 and Criterion 6.

## Deviations from Plan

None - plan executed exactly as written. Both tasks' acceptance criteria were verified by mutation (not by reading) on `rsync --exclude .git` scratch copies, with `git status --porcelain` confirmed empty in the real tree before and after each scratch run, per the plan's binding constraint.

## Issues Encountered
- `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 23/24 passed)` because VAL-03's pytest-capable interpreter was unavailable in this worktree (`.venv` did not exist). Ran `uv sync` (already-available tool, no new dependency introduced by this plan) to create `.venv`, after which the battery reported `FIREWALL: GREEN (24/24)` as required by the plan's acceptance criteria. This is an environment-setup step, not a code or gate change.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- SCAN-GUARD's two live-reproduced fail-open/silent-narrowing defects (CR-01, WR-02) are closed and mutation-verified; `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)`.
- WR-01 (18 of 22 targeted neutralizations survive the self-test — most checks still carry only one control per multi-arm check) remains open and is explicitly plan 15-06's scope; this plan's `CLAUDE.md`/`docs/ARCHITECTURE.md` rows now state that residual rather than implying full clause-level coverage already exists.
- CR-02/CR-03 (the quoted-span redirect vs. Verdict Block Format contradiction, and the redirect's unsatisfiability for several band-determining limbs) are `shared/`/rubric-prose defects out of this plan's scope (binding constraint: "Do not touch `shared/` or `first-principles/` in this plan") — they belong to plan 15-07.

---
*Phase: 15-self-audit-scan*
*Completed: 2026-09-04*

## Self-Check: PASSED

- FOUND: scripts/check-selfaudit-scan.py
- FOUND: scripts/check-firewall-battery.sh
- FOUND: CLAUDE.md
- FOUND: docs/ARCHITECTURE.md
- FOUND: .planning/phases/15-self-audit-scan/15-05-SUMMARY.md
- FOUND commit: 52f84f7
- FOUND commit: 8f6b815
