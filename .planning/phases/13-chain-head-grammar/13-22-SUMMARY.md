---
phase: 13-chain-head-grammar
plan: 22
subsystem: testing
tags: [quality-harness, self-test, fixture-guard, mutation-testing, chain-head-grammar]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar
    provides: R-HEAD-GTHOP-LATE fixture (plan 13-19) and R9's positional-bound disclosure (plan 13-18)
provides:
  - A discriminating third needle on R-HEAD-GTHOP-LATE that actually pins the GT-led hop the fixture exists to prove is undetected
  - Mutation-based proof (M1/M2/M3) that the guard now fails when the property it claims to check is broken
affects: [13-chain-head-grammar round-7 verification, any future QUAL-01 fixture work touching the GTHOP pair]

# Tech tracking
tech-stack:
  added: []
  patterns: ["disposable rsync scratch-copy mutation reproduction, never touching the tracked tree"]

key-files:
  created: []
  modified: [scripts/check-quality-harness.py]

key-decisions:
  - "Used the exact needle literal from 13-REVIEW.md CR-01's fix sketch ('binding one\\n→ GT-4's stated duty cycle') rather than inventing a new one, per the plan's read_first instruction"
  - "Kept the two needle-tuple transcriptions (_RENDER_FIXTURE_SHAPE and the registry-lock expected_fixture_shape copy) as independent hand-written literals, not factored into a shared constant, matching the plan's explicit instruction and the file's existing convention"

patterns-established:
  - "Every mode-2 shape-guard needle addition on this file follows the same lineage-comment convention: state what changed, cite the round/plan that found the gap, and prove the both-directions discrimination property"

requirements-completed: [CHAINHEAD-04, CHAINHEAD-05]

# Metrics
duration: 25min
completed: 2026-09-03
---

# Phase 13 Plan 22: Close CR-01 — R-HEAD-GTHOP-LATE's Undiscriminating Needle Summary

**Added a third needle to `R-HEAD-GTHOP-LATE`'s shape guard (both the primary tuple and its independent registry-lock transcription) that pins the GT-led hop by the hop that must precede it, closing the round-6 finding that the fixture's guard was satisfiable without any GT-led hop at all.**

## Performance

- **Duration:** 25 min
- **Started:** 2026-09-03T06:57:00-04:00 (approx, worktree provisioning)
- **Completed:** 2026-09-03T07:20:00-04:00 (approx)
- **Tasks:** 2 completed
- **Files modified:** 1 (`scripts/check-quality-harness.py`)

## Accomplishments
- `R-HEAD-GTHOP-LATE`'s needle tuple now names the offending hop AND its late position, in both `_RENDER_FIXTURE_SHAPE` and the registry-lock `expected_fixture_shape` copy
- Proved by direct mutation (M1) that deleting the GT-led hop line — which previously left `--self-test` at EXIT 0 — now fails naming `R-HEAD-GTHOP-LATE` and the missing `binding one` substring
- Proved by direct mutation (M2) that the `R-HEAD-GTHOP-BAD` / `R-HEAD-GTHOP-LATE` pair discriminates in both directions: swapping the two fenced blocks' bodies fails naming both fixture ids
- Proved by direct mutation (M3) that the registry-lock copy is load-bearing on its own: reverting only that copy to the old two-needle tuple fails with a `fixture_shape: R-HEAD-GTHOP-LATE` mismatch even though the primary tuple still carries three needles
- Real tree closes clean: `--self-test` exits 0, `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (23/23)`, `git status --porcelain` empty before the first mutation and after the last

## Task Commits

1. **Task 1: Give R-HEAD-GTHOP-LATE a needle that pins the GT-led hop in late position** - `5aa0ffc` (fix)
2. **Task 2: Reproduce the defect by mutation and confirm the new needle fails by name** - no commit (verification-only task; all mutation work ran on disposable `rsync` scratch copies outside the tracked tree per the plan's own instruction, and `git status --porcelain` confirmed clean before/after)

**Plan metadata:** (this SUMMARY commit)

## Files Created/Modified
- `scripts/check-quality-harness.py` - Added third needle `"binding one\n→ GT-4's stated duty cycle"` to `R-HEAD-GTHOP-LATE` in `_RENDER_FIXTURE_SHAPE` (~line 6615) and in the registry-lock `expected_fixture_shape` copy (~line 7858); rewrote the explanatory comment above `_RENDER_FIXTURE_SHAPE` to state the both-directions discrimination property and record the round-6 (`13-VERIFICATION-round6.md`, CR-01) reproduction of the prior vacuity

## Decisions Made
- Reused the literal needle text from `13-REVIEW.md` CR-01's fix sketch verbatim, as instructed, rather than deriving a new discriminating substring
- Left `_chain_block_well_formed` and the fixture's expected verdict (`True`) untouched — the fixture pins a violation the frozen detector does NOT catch, so `True` remains the measured, correct expectation

## Deviations from Plan

None - plan executed exactly as written. `uv sync` was run to provision `.venv`/pytest so the full `bash scripts/check-firewall-battery.sh` could reach VAL-03's pytest leg and report a genuine 23/23 GREEN rather than a BLOCKED prerequisite state; this is routine environment setup already documented in CLAUDE.md's own battery instructions, not a plan deviation.

## Issues Encountered

None. The mutation reproductions in Task 2 confirmed the pre-fix defect (M1 exited 0 before this plan's Task 1 change would have applied; verified post-fix it now exits non-zero) and the post-fix guard behaves exactly as the plan's acceptance criteria specify.

### Mutation Reproduction Detail (Task 2)

All three mutations ran on disposable `rsync -a --exclude .git --exclude .venv --exclude .planning ./ <scratchdir>/` copies under the session scratchpad directory. `git status --porcelain` on the real tracked tree was confirmed empty before the first mutation and after the last (and after the closing full-battery run). Each scratch copy was deleted immediately after its mutation was confirmed.

**M1 (round-6 reproduction, now expected to FAIL):** Deleted the line `→ GT-4's stated duty cycle is the binding term in both estimates` from the `**Non-conforming, and undetected by the form check — the GT-led hop in a later position:**` fenced block in `shared/spine/references/output-template.md` (line 262 of that file). Ran `python3 scripts/check-quality-harness.py --self-test` from the scratch root.

Result: EXIT 1. Red line produced:
```
self-test FAIL: render_contract (a) extraction [mode 2: shape mismatch] R-HEAD-GTHOP-LATE: extracted text is missing required substring(s) ["binding one\n→ GT-4's stated duty cycle"]
self-test: render_contract sub-check FAILED
```
This is the delta the plan exists to produce: before this plan the identical mutation exited 0 with every sub-check PASSED.

**M2 (cross-direction, BAD guard):** On a fresh scratch copy, swapped the two fenced blocks' bodies — the late-position block's four lines now sit under the `**Non-conforming — a hop beginning with a GT-N identifier:**` label, and the first-position block's three lines now sit under the `**Non-conforming, and undetected by the form check — the GT-led hop in a later position:**` label.

Result: EXIT 1. Red lines produced:
```
self-test FAIL: render_contract (a) extraction [mode 2: shape mismatch] R-HEAD-GTHOP-BAD: extracted text is missing required substring(s) ["threshold)\n→ GT-4's stated duty cycle"]
self-test FAIL: render_contract (a) extraction [mode 2: shape mismatch] R-HEAD-GTHOP-LATE: extracted text is missing required substring(s) ['the second reading is the binding one', "binding one\n→ GT-4's stated duty cycle"]
```
Both fixture ids are named, proving the pair discriminates in both directions.

**M3 (anti-vacuity of the registry lock):** On a fresh scratch copy, reverted ONLY the registry-lock copy of `R-HEAD-GTHOP-LATE`'s tuple (in `expected_fixture_shape`) to the old two-needle form, leaving the primary `_RENDER_FIXTURE_SHAPE` tuple with all three needles.

Result: EXIT 1. Red line produced:
```
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: fixture_shape: R-HEAD-GTHOP-LATE shape ('the second reading is the binding one', '2.20× at full duty', "binding one\n→ GT-4's stated duty cycle") != expected discriminating shape ('the second reading is the binding one', '2.20× at full duty')
```
Proving the second transcription is load-bearing on its own.

**Post-mutation confirmation on the real tree:** `python3 scripts/check-quality-harness.py --self-test` exits 0; `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (23/23)`; `git status --porcelain` is empty.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `R-HEAD-GTHOP-LATE`'s guard now genuinely backs the claim published in both `| QUAL-01 |` doc rows — that it "pins the measured non-detection with two hops preceding" — closing round-6 gap 1 (CR-01)
- No known residual defect in this fixture pair; the phase's round-7 verification can re-check this closure alongside the other round-6 findings (CR-02 through CR-05) that this plan did not touch

---
*Phase: 13-chain-head-grammar*
*Completed: 2026-09-03*
