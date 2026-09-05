---
phase: 14-closure-ledger-claim-inventory
plan: 01
subsystem: testing
tags: [quality-harness, closure-ledger, section-slicer, self-test, mutation-testing]

# Dependency graph
requires: []
provides:
  - "_slice_sections' section-6 boundary that stops at the next heading of ANY depth (D-02)"
  - "_STRUCTURAL_LEDGER_ROW_RE narrowing _closure_ledger_fragments to the prescribed row shape (D-03)"
  - "per-analysis frozen-corpus assertion in control (i) with a LENGTH FLOOR (D-11)"
affects: [14-02, 14-03, 14-04, 14-05, 15-scan]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "verify-by-mutation on disposable rsync --exclude .git scratch copies, git status --porcelain confirmed empty before/after"

key-files:
  created: []
  modified:
    - scripts/check-quality-harness.py

key-decisions:
  - "D-02: delete the depth guard entirely rather than widen it — section 6 now stops at the FIRST heading of any depth"
  - "D-03: narrow ledger discharge to the structural row shape, keeping _cites_chain as a second gate after the structural match"
  - "D-11: per-analysis comparison plus a LENGTH FLOOR, not a parallel mechanism alongside the existing whole-vector pin"

patterns-established:
  - "Per-analysis / per-field failure messages that name what moved, not just that a vector differs"

requirements-completed: [LEDGER-01, LEDGER-04]

# Metrics
duration: 5min
completed: 2026-09-03
---

# Phase 14 Plan 01: Ledger Detector Fixes (D-02, D-03, D-11) Summary

**Fixed the section-6 slicer's depth-guard bug and narrowed the closure-ledger scanner to the prescribed structural row shape, both proven against the frozen v8.7 corpus by execution rather than by reading.**

## Performance

- **Duration:** ~5 min (first commit 13:52:57 -0400 to last commit 13:56:28 -0400, local worktree clock)
- **Tasks:** 3 completed
- **Files modified:** 1 (`scripts/check-quality-harness.py`)

## Accomplishments

- `_slice_sections`' section-6 boundary loop no longer requires the following heading to be at the same or shallower hash depth — it now breaks at the first heading of any depth. On the 2026-09-02 capture (`#` sections + `##` process-output appendices) this stops the Assumption Audit scan and Self-Audit Gate from being folded into "section 6".
- `_closure_ledger_fragments` now requires the line to match `_STRUCTURAL_LEDGER_ROW_RE` (the `- "quote" → chain Cn` / `-> chain Cn` shape `output-template.md` prescribes) before `_cites_chain` is even consulted — removing the mechanism's only-ever-false-positive discharge path (measured `LOAD_BEARING = 0` across all six frozen v8.7 analyses).
- Control (i) in `_selftest_ledger_traceability` now names the analysis and field when the frozen v8.7 baseline moves, behind a LENGTH FLOOR that fails rather than passing vacuously if any calibration vector is emptied or resized.
- `python3 scripts/check-quality-harness.py --self-test` exits 0; `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (23/23)` (required creating a local `.venv` via `uv sync` in this worktree, since VAL-03's pytest-capable-interpreter prerequisite was unmet before that — a one-time environment setup, not a code change; see Issues Encountered).

## Task Commits

Each task was committed atomically:

1. **Task 1: Fix the section-6 slice boundary (D-02)** - `45a693a` (fix)
2. **Task 2: Narrow the ledger-row rule to the prescribed structural shape (D-03)** - `a773812` (fix)
3. **Task 3: Make the frozen-corpus assertion name the analysis (D-11)** - `2499cc2` (fix)

_No TDD tasks in this plan._

## Files Created/Modified

- `scripts/check-quality-harness.py` - `_slice_sections` boundary fix (D-02); `_STRUCTURAL_LEDGER_ROW_RE` + narrowed `_closure_ledger_fragments` (D-03); per-analysis frozen-corpus control (i) + LENGTH FLOOR (D-11)

## Decisions Made

- Deleted the `if len(hm.group(1)) <= depth:` depth guard entirely, per plan instruction, rather than widening it — the loop now breaks at the first heading match unconditionally. The `depth` element of the `anchors` tuples is now unused inside that branch; left the tuple/unpacking shape alone rather than restructuring it, per the plan's explicit instruction.
- Kept `_cites_chain` as a second gate AFTER the structural regex match in `_closure_ledger_fragments`, preserving the "a ledger cannot invent its own authority" guarantee and keeping control (d) non-vacuous.
- Kept the existing whole-vector comparison in control (i) alongside the new per-analysis loop — the whole-vector check is what catches a length/order change that a per-element loop over a shortened list would silently miss.
- Extended control (i)'s per-analysis loop and LENGTH FLOOR inline in `_selftest_ledger_traceability` rather than adding a new self-test function or battery gate, per the plan's explicit "no new file, no new gate" instruction.

## Mutation Verdicts (verbatim, per plan `<output>` instruction)

All mutations were performed on disposable `rsync -a --exclude .git` scratch copies under the scratchpad directory; `git status --porcelain` on the real worktree was confirmed empty before and after every mutation.

### Task 2 — controls (d), (e), (f) re-derived under the D-03 narrowing

**(d) — `_cites_chain` forced to `return True` unconditionally:**
```
self-test FAIL: ledger_traceability (d) ledger citing non-existent chains yielded fragments
```
Still fails for its own stated reason: the narrowed regex still matches the row SHAPE (`- "..." -> chain C9`), so the failure is produced by `_cites_chain` no longer being able to reject the bogus id — proving `_cites_chain` is still the thing doing the rejecting today, and that mutating it away is what breaks the guarantee.

**(e) — `_MIN_LEDGER_FRAGMENT_TOKENS` set to `0`:**
```
self-test FAIL: ledger_traceability (e) sub-minimum fragment wrongly discharged a claim
```
Still fails for its own stated reason: the narrowed regex still matches `- "serverless is cheaper" -> chain C1`, so the failure comes from the token-count floor no longer rejecting the sub-minimum fragment, not from the row losing its ledger shape.

**(f) — `_LEDGER_COVERAGE_THRESHOLD` set to `0.0`:**
```
self-test FAIL: ledger_traceability (f) unrelated fragment wrongly discharged a claim
```
Still fails for its own stated reason: the narrowed regex still matches the well-formed-but-unrelated row, so the failure comes from the coverage-fraction floor no longer rejecting it.

**(g) — out of scope for this narrowing.** Confirmed by reading: control (g) calls `_ledger_fragment_covers` directly with hand-built strings and never calls `_closure_ledger_fragments`, so D-03's regex change cannot affect it either way. No mutation was run for it, per the plan's explicit instruction.

### Task 3 — control (i) and its LENGTH FLOOR

**Mutation 1 — first element of `_CALIBRATION_CONCLUSION_CLAIMS` changed from `9` to `8`:**
```
self-test FAIL: ledger_traceability (i) conclusion_claims moved: [9, 9, 8, 5, 6, 4] != [8, 9, 8, 5, 6, 4]
self-test FAIL: ledger_traceability (i) condA-P1: conclusion_claims moved: measured 9 != pinned 8
```
The second line names both `condA-P1` (`_CALIBRATION_ANALYSIS_ORDER[0]`) and the substring `conclusion_claims`, as required.

**Mutation 2 — `_CALIBRATION_ANALYSIS_ORDER` set to `()`:**
```
self-test FAIL: ledger_traceability (i) LENGTH FLOOR: calibration vectors are not all length 6: {'_CALIBRATION_ANALYSIS_ORDER': 0, '_CALIBRATION_CONCLUSION_CLAIMS': 6, '_CALIBRATION_UNTRACED_CLAIMS': 6}
```
The LENGTH FLOOR fires and names all three lengths, rather than the per-analysis loop silently running zero times and passing.

## Measured Readings (verified by execution)

```
                       claims  ledger_frags  untraced
today (pre-D-02)          8         7           1
D-02 alone                7         3           1
D-02 + D-03 (final)       7         0           1   <- confirmed final reading
```

Untraced claim in every row above: `**Trade-offs acknowledged:** step 2's ~73% is a ceiling requiring a long-term, a...` (same claim throughout, as CONTEXT.md predicted).

```
frozen v8.7 claims:   [9, 9, 8, 5, 6, 4]   (unmoved, before and after both changes)
frozen v8.7 untraced: [4, 5, 6, 3, 3, 4]   (unmoved, before and after both changes)
```

## Deviations from Plan

None - plan executed exactly as written. `.planning/captures/pr-p1-v8.25.0-2026-09-02/` (gitignored) was copied locally into this worktree so the plan's verify commands could resolve the relative path — this is a local-only, uncommitted copy of already-committed-elsewhere fixture data, not a tracked-tree change.

## Issues Encountered

- The worktree had no pytest-capable interpreter, so `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 22/23 passed)` naming `[PREREQ] VAL-03`. Resolved per CLAUDE.md's documented remedy: ran `uv sync` to create `.venv` (ships pytest 9.1.1), after which the battery reported `FIREWALL: GREEN (23/23)`. `.venv` is gitignored and was not committed.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- D-02 and D-03 land the mechanical fixes this phase's remaining plans (14-02..14-05) build the R11/R12 rule text and the `tests/quality-ledger-v8.26/` fixture against — the capture now reads 7/0/1, the number D-04's fixture is designed to pin.
- Phase 15's claim-inventory scan depends on D-02 (its enumeration must match what `_conclusion_claims` extracts from the true Conclusion section, which is only true now that "section 6" means the Conclusion section).
- No blockers.

---
*Phase: 14-closure-ledger-claim-inventory*
*Completed: 2026-09-03*

## Self-Check: PASSED

- FOUND: scripts/check-quality-harness.py
- FOUND: .planning/phases/14-closure-ledger-claim-inventory/14-01-SUMMARY.md
- FOUND commit: 45a693a (Task 1)
- FOUND commit: a773812 (Task 2)
- FOUND commit: 2499cc2 (Task 3)
