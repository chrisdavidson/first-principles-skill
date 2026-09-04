---
phase: 15-self-audit-scan
plan: 09
subsystem: testing
tags: [validation-gate, self-audit-scan, scan-guard, placement-predicate, live-leg-registration, call-site-census]

# Dependency graph
requires:
  - phase: 15-self-audit-scan
    provides: SCAN-GUARD's 86 clause-level branch ids and the Verdict Block Format admission scoped to Criteria 4/6 and Criterion 2 (15-01..15-08)
provides:
  - Rubric-2's combined placement predicate split into two independently falsifiable halves (Assumption Audit half, Precedence half), each with its own detail and fixture, closing the fail-open the verifier reproduced live (a scan block relocated BEFORE the Assumption Audit block previously passed --self-test undetected)
  - New branch R-02-placement-aa (86 -> 87), registered in both REQUIRED_BRANCHES and _BRANCH_ROSTER_LOCK
  - _live_exit_code(failures) — a pure helper extracting _validate_files' failure-to-exit-code decision, driven by two isolation arms (live-x1, live-x2) with synthetic lists
  - Two new call-site censuses (_validate_files' four legs; _live_exit_code's two isolation arms) plus an in-process live-leg dispatch control (main([])) with its own call-site census, so deleting any leg, arm or the control itself fails --self-test by name
  - SCAN-GUARD's live CLI leg registered in scripts/check-firewall-battery.sh (two-command gate form) and .github/workflows/validation.yml (second `uv run` step), under the unchanged SCAN-GUARD gate id, battery tally unchanged at 24
affects: [Phase 16 (version stamps, matrix rows, coverage headline, CHANGELOG, REQUIREMENTS.md checkboxes, doc-surface branch-count/registration-shape claims deferred to plan 15-10)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A combined placement predicate split into per-half guards, each evaluated only when both indices it compares are != -1, each emitting a distinct detail token so narrowing either half alone fails a named control instead of being covered by the other half's fixture — a stronger property than the existing Body-3 precedent (single shared 'placement violated' message, disambiguated only by which fixture is run)"
    - "A pure decision-extraction helper (_live_exit_code) driven by synthetic isolation arms in the _roster_problems idiom, plus TWO call-site censuses per addition: one counting the helper's real call site inside its caller's own source (floors the caller still uses it), one counting the isolation arms' call sites inside the self-test's own source (floors the arms themselves still exist) — a third census, added mid-task after review-by-mutation found the first two alone left the whole dispatch-control block deletable with --self-test still green, closes that gap by counting the control's own real call-site line"
    - "Live-leg registration matches the REG-GUARD/PROV-GUARD two-command `gate` shape exactly: a gate id's display string and CI job name stay fixed while the commands under it grow, keeping the battery tally a function of gate-id count, not leg count"

key-files:
  created: []
  modified:
    - scripts/check-selfaudit-scan.py
    - scripts/check-firewall-battery.sh
    - .github/workflows/validation.yml

key-decisions:
  - "Added a third census (live-dispatch-census) beyond what the plan's action text explicitly named, after a scratch-copy mutation test proved the live-leg dispatch control's own deletion was invisible to both the leg-census and the isolation-arm census the plan did name. The plan's acceptance criteria required this ('Deleting the live-leg dispatch control ... makes --self-test exit 1 naming the corresponding census'), so this follows directly from re-reading the acceptance criteria against a measured gap rather than trusting the action text's enumeration was exhaustive — the same discipline 15-08's SUMMARY records for its own scope."
  - "The R-02-placement-aa fixture co-fires Rubric-7 (Assumption-Audit near-twin sentence, now inside the widened scan slice) and Rubric-12 alongside Rubric-2 — measured, printed by the fixture itself, and kept per the plan's explicit instruction rather than narrowing expected_check_id to hide it."

requirements-completed: [SCAN-03]

# Metrics
duration: 10min
completed: 2026-09-04
---

# Phase 15 Plan 09: Close SCAN-03's placement fail-open and register SCAN-GUARD's live leg Summary

**Split Rubric-2's combined placement predicate into two independently falsifiable halves (closing the verifier's reproduced fail-open where a scan block relocated before the Assumption Audit block passed undetected), then registered the documented CLI in both the firewall battery and CI and floored every leg of `_validate_files` with call-site censuses, isolation arms and an in-process dispatch control.**

## Performance

- **Duration:** ~10 min
- **Started:** 2026-09-04T13:53:58Z (first read)
- **Completed:** 2026-09-04T14:04:00Z (final task commit)
- **Tasks:** 2 completed
- **Files modified:** 3 (`scripts/check-selfaudit-scan.py`, `scripts/check-firewall-battery.sh`, `.github/workflows/validation.yml`)

## Accomplishments

- Split Rubric-2's combined `if not (aa_idx < scan_idx < precedence_idx)` guard into two independent halves — `aa_idx < scan_idx` (Assumption Audit half) and `scan_idx < precedence_idx` (Precedence half) — each evaluated only when both indices it compares are `!= -1`, each with a distinct failure detail.
- Retargeted `R-02-placement-order`'s `expected_detail` from the shared `"placement violated"` text to the Precedence half's own token, so it can no longer be satisfied by the Assumption Audit half's message.
- Added `R-02-placement-aa`: relocates the scan block heading to immediately after `## How to Apply This Gate` (before the Assumption Audit block) via `_relocate`, proving the arm is a placement check and not a disguised presence check. Registered in `REQUIRED_BRANCHES` and `_BRANCH_ROSTER_LOCK` (86 -> 87).
- Extracted `_validate_files`' failure-to-exit-code decision into a pure helper, `_live_exit_code(failures)`, in `_roster_problems`' voice; added two isolation arms (`live-x1`, `live-x2`) driving it with synthetic lists.
- Added a call-site census over `inspect.getsource(_validate_files)` asserting all four legs (`_check_body_text`, `_check_rubric_text`, `_check_cross_surface`, `_live_exit_code`) occur exactly once, and a second census over `inspect.getsource(_run_self_test)` asserting the two isolation arms' call sites.
- Added an in-process live-leg dispatch control driving `main([])` with stdout/stderr captured, asserting rc=0 and both the `COVERAGE —` and `PASS` markers in captured stdout — the documented CLI's first coverage from any control.
- Found by scratch-copy mutation (not in the plan's action text) that deleting the entire dispatch-control block left `--self-test` green, because neither existing census counted the control's own presence. Added a third census (`live-dispatch-census`) counting the control's real call-site line in `_run_self_test`'s own source, closing the gap.
- Registered the live leg in `scripts/check-firewall-battery.sh` (two-command `gate "SCAN-GUARD"` form matching REG-GUARD/PROV-GUARD) and in `.github/workflows/validation.yml` (second `uv run python3 scripts/check-selfaudit-scan.py` step in the existing job), leaving the gate id, CI job key and `name:` field unchanged.
- `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)` — tally unchanged, as required.

## Task Commits

Each task was committed atomically:

1. **Task 1: Split Rubric-2's placement predicate into two independently falsifiable halves and add the R-02-placement-aa branch, fixture and control** - `a1b6574` (test)
2. **Task 2: Register the live CLI leg in the battery and CI, and floor every leg of `_validate_files` with a call-site census, isolation arms and an in-process dispatch control** - `b6e075a` (feat)

## Files Created/Modified
- `scripts/check-selfaudit-scan.py` — Rubric-2 split into two per-half guards; `R-02-placement-order` retargeted; new `R-02-placement-aa` fixture and control; `REQUIRED_BRANCHES`/`_BRANCH_ROSTER_LOCK` extended 86 -> 87. New `_live_exit_code` helper; `_validate_files` calls it in place of its inline `if failures:` branch; two new isolation arms (`live-x1`, `live-x2`); three new censuses (`validate-census`, `live-census`, `live-dispatch-census`); new in-process live-leg dispatch control driving `main([])`.
- `scripts/check-firewall-battery.sh` — `gate "SCAN-GUARD"` call changed from one command (`--self-test` only) to the two-command form (`--self-test` + live), display string updated to `"check-selfaudit-scan.py --self-test + live"`. Composition comment above the call left untouched (out of scope, plan 15-10).
- `.github/workflows/validation.yml` — added a second `run` step (`uv run python3 scripts/check-selfaudit-scan.py`) to the existing `check-selfaudit-scan` job, immediately after the `--self-test` step. Job key and `name:` field unchanged.

## Decisions Made
See `key-decisions` in the frontmatter above for the two substantive ones (the mid-task third census, and keeping the R-02-placement-aa co-firing rather than hiding it).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - bug] Added a third census (`live-dispatch-census`) to close a fail-open the plan's action text did not explicitly enumerate**
- **Found during:** Task 2, while proving the live-leg dispatch control by neutralization on a disposable scratch copy, per the plan's own binding constraint ("Every new control is proven by neutralization, not by reading").
- **Issue:** The plan's action text named a call-site census over `_validate_files`' four legs and a call-site census over `_live_exit_code`'s isolation arms, but did not separately name a census over the live-leg dispatch control's own presence. Deleting the entire dispatch-control block (comment through the closing `except`) left `--self-test` at rc=0 — neither of the two named censuses inspects `_run_self_test`'s source for the dispatch control's own call site, only for `_live_exit_code`'s isolation-arm call sites. This directly violates the plan's own acceptance criterion: "Deleting the live-leg dispatch control, or any single isolation arm, makes `--self-test` exit 1 naming the corresponding census."
- **Fix:** Added `(live-dispatch-census)`, counting the literal `"live_dispatch_rc = main(" + "[])"` (built from two concatenated halves so the census line's own source cannot self-match) inside `inspect.getsource(_run_self_test)`, expected exactly 1. Verified this specific census — not the other two — is what catches the control's deletion.
- **Files modified:** `scripts/check-selfaudit-scan.py`.
- **Verification:** On a disposable scratch copy, deleting only the dispatch-control block (keeping the new census) makes `--self-test` exit 1 with `(live-dispatch-census): observed 0 live-dispatch call site(s), expected 1`. Restored; `git status --porcelain` empty in the real tree before and after.
- **Committed in:** `b6e075a` (Task 2).

---

**Total deviations:** 1 auto-fixed (Rule 1).
**Impact on plan:** Additive only — one new census function, no existing helper, check function or pinned literal was modified beyond what the plan specified. `--self-test` still reports 87/87 branches (the census is not a `REQUIRED_BRANCHES` entry — it floors the dispatch control the same way `roster-census` floors `_roster_problems`' real call site, as an unconditional part of the self-test rather than a named branch).

## Verifier Reproduction Table (Task 1, `15-VERIFICATION.md` gap 2)

| Mutation | Command | Observed output | Exit code |
|---|---|---|---|
| Narrow the Assumption Audit half to constant-true (`if not (aa_idx < scan_idx):` -> `if False:`) | `python3 scripts/check-selfaudit-scan.py --self-test` on scratch copy | `check-selfaudit-scan --self-test: FAIL — R-02c: wrong-reason failure; Anti-masking: 1 branches uncovered; ...` / `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['R-02-placement-aa']` | 1 |
| Narrow the Precedence half instead (`if not (scan_idx < precedence_idx):` -> `if False:`) | `python3 scripts/check-selfaudit-scan.py --self-test` on scratch copy | `check-selfaudit-scan --self-test: FAIL — R-02a: wrong-reason failure; Anti-masking: 1 branches uncovered; ...` / `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['R-02-placement-order']` — **not** `R-02-placement-aa`, proving the two halves are independently falsifiable | 1 |

`R-02-placement-aa`'s fixture failure list (Task 1's isolation-by-measurement requirement): check IDs `['Rubric-12', 'Rubric-2', 'Rubric-7']` — Rubric-2 fires as the arm's own reason; Rubric-7 and Rubric-12 co-fire because the widened `[_RUBRIC_SCAN_BLOCK, _RUBRIC_PRECEDENCE)` slice now also encloses the Assumption Audit block content (Rubric-7's near-twin sentence, and whatever Rubric-12's halt-sentence count guard reacts to inside the widened range). Per the plan's explicit instruction, the fixture and its `expected_check_id="Rubric-2"` were kept as-is rather than weakened, since `Rubric-2`'s own message is present and correctly attributed regardless of the siblings.

## Neutralization Census (Task 2, four review mutations plus isolation-arm and dispatch-control deletion)

Run on a disposable scratch copy (`rsync -a --exclude .git --exclude .venv`), one mutation applied and reverted at a time via a Python driver script. `git status --porcelain` confirmed empty in the real tree before and after the whole census.

| Mutation | Observed `--self-test` output (relevant line) | Exit code |
|---|---|---|
| Delete `+ _check_cross_surface(body_text, rubric_text)` from `_validate_files` | `(validate-census): _check_cross_surface occurs 0 time(s) in _validate_files, expected 1` | 1 |
| Delete `+ _check_rubric_text(rubric_text)` from `_validate_files` | `(validate-census): _check_rubric_text occurs 0 time(s) in _validate_files, expected 1` | 1 |
| Replace `_check_body_text(body_text)` with `[]` in `_validate_files` | `(validate-census): _check_body_text occurs 0 time(s) in _validate_files, expected 1` | 1 |
| Make `_live_exit_code` always return 0 (`if failures: ... return 1 / return 0` -> `return 0`) | `(live-x2): fail case wrongly reported rc=0` — `(live-x2) ISOLATION FAIL: expected rc=1 / stderr containing 'Rubric-1: synthetic', got rc=0, stderr=''` | 1 |
| Delete the `(live-x1)` isolation arm | `(live-census): observed 1 _live_exit_code call site(s) inside _run_self_test, expected 2` | 1 |
| Delete the `(live-x2)` isolation arm | `(live-census): observed 1 _live_exit_code call site(s) inside _run_self_test, expected 2` | 1 |
| Delete the entire live-leg dispatch-control block | `(live-dispatch-census): observed 0 live-dispatch call site(s), expected 1` (only after adding this census — see Deviations) | 1 |

All seven mutations were named by exactly the control or census whose absence they created; no mutation's failure list named an unrelated id.

## Issues Encountered

- `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED` (VAL-03's pytest-capable interpreter unavailable — this worktree's `.venv` did not exist, the same environment-setup issue plans 15-07 and 15-08 recorded). Ran `uv sync` (environment setup only, no new dependency added by this plan) to create `.venv`; the battery then reported `FIREWALL: GREEN (24/24)`.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Both `15-VERIFICATION.md` gap-2 `missing[]` items (the placement fail-open, the unregistered/unfloored live CLI leg) are closed and re-reproduced live.
- `python3 scripts/check-selfaudit-scan.py --self-test` exits 0 (87/87 branches covered); `python3 scripts/check-selfaudit-scan.py` exits 0 with its `COVERAGE —` line.
- `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)` — tally unchanged; `SCAN-GUARD`'s display string reads `check-selfaudit-scan.py --self-test + live`.
- `python3 scripts/check-registration.py --self-test && python3 scripts/check-registration.py` both exit 0 — REG-GUARD's CI-job axis still resolves `SCAN-GUARD` to the `check-selfaudit-scan (SCAN-GUARD)` job.
- Out of scope per this plan's own binding constraints, carried forward to plan 15-10: every doc-surface branch-count and registration-shape claim (`CLAUDE.md:169`, `CLAUDE.md:178`, `docs/ARCHITECTURE.md:150`, `docs/ARCHITECTURE.md:165-168`) and the SCAN-GUARD composition comment in `scripts/check-firewall-battery.sh` — none of these were touched by this plan and all still read `72 branches`/`58 to 72` today; the branch count is now 87, not 72.
- `15-REVIEW.md`'s WR-03 (seven arms with no branch id), WR-04, IN-04 and IN-05 remain out of scope, per this plan's own binding constraint — none appears in either gap's `missing[]` list in `15-VERIFICATION.md`.
- Phase 16 still owns: version stamps, `docs/requirements-matrix.md` SCAN-01..04 rows, the coverage headline, CHANGELOG, and `REQUIREMENTS.md` checkboxes.

---
*Phase: 15-self-audit-scan*
*Completed: 2026-09-04*

## Self-Check: PASSED

- FOUND: scripts/check-selfaudit-scan.py
- FOUND: scripts/check-firewall-battery.sh
- FOUND: .github/workflows/validation.yml
- FOUND commit: a1b6574
- FOUND commit: b6e075a
