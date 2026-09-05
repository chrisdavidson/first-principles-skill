---
phase: 18-exemplar-conformance
plan: 09
subsystem: testing
tags: [python, self-test, source-text-census, anti-masking, conformance]

# Dependency graph
requires:
  - phase: 18-exemplar-conformance (plans 18-01..18-08)
    provides: CONF-GATE's original run_live() and 18-control self-test battery, registered in the battery/CI at 25/25
provides:
  - A source-text call-site census (_call_site_census_problems) floors run_live()'s six enforcement call sites by name
  - Independent second-transcription locks for _CLAIM_FLOORS and _MARKED_RATCHET, with every consuming control fixture rewritten to an inline literal
  - Per-literal _PRESCRIBED_LEAD_INS controls (generated from the tuple, hand-transcribed into _CONTROL_IDS) plus a negative control for the CAVEAT_MARKER conjunct
  - Control battery moved 18 -> 31; 13 neutralization mutations (M1-M13) plus the verifier's exact reproduction replayed and confirmed closed
affects: [18-10 (moves _MARKED_RATCHET and its lock to 4 together)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Source-text call-site census (inspect.getsource + string count), copied from check-selfaudit-scan.py's (validate-census)/(roster-entry-source) idiom"
    - "Independent second-transcription lock (a _X_LOCK constant compared for equality, never derived from X) for every tunable a control consumes"
    - "Generated per-literal control ids (one per tuple member) hand-transcribed into a second roster so narrowing the tuple fails the existing coverage-floor by name"

key-files:
  created: []
  modified:
    - scripts/check-conf-gate.py

key-decisions:
  - "Built _LIVE_CALL_FORMS' fragments via string concatenation, never one contiguous literal, so the census's own table cannot self-match if its scan scope is later widened from run_live to the module"
  - "Rewrote all five self-referential control fixtures (d04-floor-fires, d04-floor-passes-at-floor, ratchet-fires-above, ratchet-passes-at-pin, ratchet-passes-below) to inline integer literals rather than reading the constant under test"
  - "Retired _control_d03_fires_on_prescribed_leadin in favor of three GENERATED per-literal controls, derived from _PRESCRIBED_LEAD_INS and hand-transcribed into _CONTROL_IDS, so narrowing the source tuple fails the existing coverage-floor by name instead of needing a new mechanism"
  - "Left _MARKED_RATCHET at its current value of 2 in this plan, per the plan's explicit instruction; plan 18-10 moves the constant and its new inline-literal lock to 4 together as one two-place edit"

patterns-established:
  - "Every self-test control that asserts a constant's tunable value must do so against an INLINE literal or a second, independently transcribed table — never against the constant under test itself"

requirements-completed: [CONF-03, CONF-04, CONF-05, CONF-06]

# Metrics
duration: 45min
completed: 2026-09-05
---

# Phase 18 Plan 09: CONF-GATE Standing-Enforcement Closure Summary

**Floored run_live()'s six enforcement call sites with a source-text census, and closed four self-referential control fixtures with independent literal locks — CONF-GATE's control battery moved 18 -> 31, closing the 18-VERIFICATION.md blocking gap where a one-line deletion left both `--self-test` and the live leg reporting PASS.**

## Performance

- **Duration:** 45 min
- **Started:** 2026-09-05T11:29:00Z
- **Completed:** 2026-09-05T11:45:04Z
- **Tasks:** 3 completed
- **Files modified:** 1 (`scripts/check-conf-gate.py`)

## Accomplishments

- `_call_site_census_problems`, a pure source-text census over `inspect.getsource(run_live)`, floors all six `problems +=` / `mutation_lines =` enforcement call sites by count AND by whitespace-normalized call form, with five isolation arms (`census-x1/x2/x3`, `form-lock-x1/x2`) driven only by synthetic source strings.
- `_CLAIM_FLOORS_LOCK` and an inline `ratchet-value-locked` assertion break the self-reference CR-02(a)/(b) identified: every consuming control fixture (`d04-floor-fires`, `d04-floor-passes-at-floor`, `ratchet-fires-above`, `ratchet-passes-at-pin`, `ratchet-passes-below`) now uses an inline integer literal rather than reading `_CLAIM_FLOORS[...]` or `_MARKED_RATCHET` to build its own fixture.
- `_PRESCRIBED_LEAD_INS_LOCK` plus three GENERATED per-literal controls (`d03-fires-on-leadin-recommended-approach`, `-key-insight`, `-trade-offs-acknowledged`) close CR-02(c); `d03-passes-on-unmarked-prescribed-leadin`, with its own inline non-vacuity assertion, closes CR-02d)'s missing negative control on the `CAVEAT_MARKER in claim_text` conjunct.
- Control count: 18 -> 25 (Task 1) -> 27 (Task 2) -> 31 (Task 3), matching the plan's target exactly.
- Full neutralization ledger (13 mutations + the verifier's exact reproduction) run on disposable `rsync --exclude .git` scratch copies, `git status --porcelain` confirmed empty on the real tree before and after every scratch operation (verbatim output below).

## Task Commits

Each task was committed atomically:

1. **Task 1: Floor run_live()'s six enforcement call sites with a source-text census and a call-form lock (CR-01)** - `81c99f3` (feat)
2. **Task 2: Break the self-reference in the _CLAIM_FLOORS and _MARKED_RATCHET controls with independent literal locks (CR-02a, CR-02b)** - `5c440a7` (feat)
3. **Task 3: Parameterize the D-03 lead-in controls per literal and add the missing CAVEAT_MARKER negative control (CR-02c, CR-02d)** - `c6403c8` (feat)

**Plan metadata:** (this commit — SUMMARY.md, staged next)

## Files Created/Modified

- `scripts/check-conf-gate.py` - Added the census/form-lock (Task 1), the two independent-lock controls (Task 2), and the per-literal D-03 controls plus the CAVEAT_MARKER negative control (Task 3). Control battery 18 -> 31.

## Decisions Made

- `_LIVE_CALL_FORMS`' fragments are built by string concatenation (`"problems += " + "_targets_problems(rows)"`), never as one contiguous literal, per the `(roster-entry-source)` convention in `check-selfaudit-scan.py` — this avoids the census's own table becoming a self-match hazard if its scan scope is ever widened from `run_live` to the whole module.
- `_MARKED_RATCHET` is left at 2 in this plan (per the plan's explicit `<interfaces>` instruction); the `ratchet-value-locked` control asserts an inline `2` literal at the control site. Plan 18-10 moves both the constant and this lock to 4 as one deliberate two-place edit.
- `_control_d03_fires_on_prescribed_leadin` was retired rather than kept alongside the generated controls — the generated `d03-fires-on-leadin-recommended-approach` entry is its exact superset (identical fixture construction, identical assertion), so keeping both would have been a redundant, unregistered duplicate.

## Deviations from Plan

None — plan executed exactly as written. All three tasks landed at their specified control counts (25, 27, 31) with no rework.

## Neutralization Ledger (verbatim, per the phase's verify-by-mutation discipline)

All mutations below were applied on disposable `rsync -a --exclude .git` scratch copies under the session scratchpad. `git status --porcelain` on the real tree was confirmed empty (aside from the plan's own staged/committed edits) before and after every scratch-copy operation — the scratch mutations never touched the real tree.

### Task 1 — CR-01 (six call sites + call-form lock)

**Before Task 1:** `check-conf-gate: SELF-TEST PASS — 18 controls run`
**After Task 1:** `check-conf-gate: SELF-TEST PASS — 25 controls run`

**M1 — delete `problems += _targets_problems(rows)`:**
```
check-conf-gate: SELF-TEST FAIL [live-call-site-census] — ["CALL-SITE CENSUS: _targets_problems occurs 0 time(s) in run_live's source, expected 1"]
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — ["CALL-SITE CENSUS: _targets_problems occurs 0 time(s) in run_live's source, expected 1", "CALL-FORM LOCK: _targets_problems's expected call form not found in run_live's source: 'problems += _targets_problems(rows)'"]
RC=1
```

**M2 — delete `problems += _claim_floor_roster_problems(...)`:**
```
check-conf-gate: SELF-TEST FAIL [live-call-site-census] — ["CALL-SITE CENSUS: _claim_floor_roster_problems occurs 0 time(s) in run_live's source, expected 1"]
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — ["CALL-SITE CENSUS: _claim_floor_roster_problems occurs 0 time(s) in run_live's source, expected 1", "CALL-FORM LOCK: _claim_floor_roster_problems's expected call form not found in run_live's source: 'problems += _claim_floor_roster_problems(set(_CLAIM_FLOORS), discovered_ids)'"]
RC=1
```

**M3 — delete `problems += _claim_floor_problems(rows)`:**
```
check-conf-gate: SELF-TEST FAIL [live-call-site-census] — ["CALL-SITE CENSUS: _claim_floor_problems occurs 0 time(s) in run_live's source, expected 1"]
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — ["CALL-SITE CENSUS: _claim_floor_problems occurs 0 time(s) in run_live's source, expected 1", "CALL-FORM LOCK: _claim_floor_problems's expected call form not found in run_live's source: 'problems += _claim_floor_problems(rows)'"]
RC=1
```

**M4 — delete the whole D-03 loop:**
```
check-conf-gate: SELF-TEST FAIL [live-call-site-census] — ["CALL-SITE CENSUS: _d03_rule_problems_from_text occurs 0 time(s) in run_live's source, expected 1"]
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — ["CALL-SITE CENSUS: _d03_rule_problems_from_text occurs 0 time(s) in run_live's source, expected 1", "CALL-FORM LOCK: _d03_rule_problems_from_text's expected call form not found in run_live's source: 'problems += _d03_rule_problems_from_text(text, r[\"analysis_id\"], r[\"relpath\"])'"]
RC=1
```

**M5 — delete `problems += _ratchet_problems(rows)`:**
```
check-conf-gate: SELF-TEST FAIL [live-call-site-census] — ["CALL-SITE CENSUS: _ratchet_problems occurs 0 time(s) in run_live's source, expected 1"]
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — ["CALL-SITE CENSUS: _ratchet_problems occurs 0 time(s) in run_live's source, expected 1", "CALL-FORM LOCK: _ratchet_problems's expected call form not found in run_live's source: 'problems += _ratchet_problems(rows)'"]
RC=1
```

**M6 — delete `mutation_lines = _run_d08_arm(rows)` and its consumer loop:**
```
check-conf-gate: SELF-TEST FAIL [live-call-site-census] — ["CALL-SITE CENSUS: _run_d08_arm occurs 0 time(s) in run_live's source, expected 1"]
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — ["CALL-SITE CENSUS: _run_d08_arm occurs 0 time(s) in run_live's source, expected 1", "CALL-FORM LOCK: _run_d08_arm's expected call form not found in run_live's source: 'mutation_lines = _run_d08_arm(rows)'"]
RC=1
```

**M7 — rewrite `problems += _targets_problems(rows)` to `_targets_problems(rows)` (form-only, count unchanged):**
```
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — ["CALL-FORM LOCK: _targets_problems's expected call form not found in run_live's source: 'problems += _targets_problems(rows)'"]
RC=1
```
`[live-call-site-census]` did NOT fire (confirmed absent from stderr) — the count is unchanged at 1; only the form lock catches the rewrite, proving the form lock adds a property the count census does not have.

**THE BLOCKING-GAP ACCEPTANCE CRITERION — the verifier's exact reproduction, replayed.** On one scratch copy: (a) stripped `(chain C2) ` from line 89 of `shared/examples/personal-general.md` (the `1. (chain C2) Verify, through direct conversations…` claim), AND (b) deleted `problems += _targets_problems(rows)` from `run_live()`:

```
=== --self-test ===
check-conf-gate: SELF-TEST FAIL [live-call-site-census] — ["CALL-SITE CENSUS: _targets_problems occurs 0 time(s) in run_live's source, expected 1"]
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — ["CALL-SITE CENSUS: _targets_problems occurs 0 time(s) in run_live's source, expected 1", "CALL-FORM LOCK: _targets_problems's expected call form not found in run_live's source: 'problems += _targets_problems(rows)'"]
RC=1
=== live leg ===
check-conf-gate: COVERAGE — measured 28 artifacts across shared-examples, generated-twin
check-conf-gate: D-08(a) hop re-wrap on shared/examples/personal-general.md — heading_malformed_blocks 0 -> 1
check-conf-gate: D-08(b) verdict-cell strip on shared/examples/personal-general.md — nonconforming_verdict_cells 0 -> 1
check-conf-gate: D-08(c) citation removal on shared/examples/personal-general.md — silent_untraced_claims 1 -> 2
check-conf-gate: PASS
RC=0
```
Before this plan, this exact reproduction printed `SELF-TEST PASS — 18 controls run` at rc 0 on BOTH legs. Now `--self-test` correctly exits 1 naming `live-call-site-census` and `_targets_problems`. The live leg still exits 0/PASS — the census is what catches the deletion, not the live leg itself, exactly as the acceptance criterion specifies (the defect remains unreported by the live leg; the standing regression protection lives in `--self-test`). `git status --porcelain` on the real tree confirmed empty both before and after this replay.

### Task 2 — CR-02(a)/(b) (independent locks)

**Before Task 2:** `check-conf-gate: SELF-TEST PASS — 25 controls run`
**After Task 2:** `check-conf-gate: SELF-TEST PASS — 27 controls run`

**M8 — set every `_CLAIM_FLOORS` value to 0 (leave `_CLAIM_FLOORS_LOCK` untouched):**
```
check-conf-gate: SELF-TEST FAIL [d04-floor-fires] — []
check-conf-gate: SELF-TEST FAIL [claim-floor-values-locked] — D-04 LOCK MISMATCH: ['composed-inversion-second-order', 'decompose-irreducibility', 'estimate-fermi', 'ishikawa-fishbone', 'personal-general', 'personal-general-2', 'product-business', 'product-business-2', 'science-engineering', 'science-engineering-2', 'self-application', 'software-systems', 'software-systems-2', 'theoretical-limit-carnot']
RC=1
```
Two named failures where CR-02 measured zero: `[claim-floor-values-locked]` names all fourteen ids, and `[d04-floor-fires]` additionally fires because the inline fixture (6) no longer breaches a floor of 0 — direct proof the fixture is no longer self-referential.

**M9 — `_MARKED_RATCHET: 2` -> `99`:**
```
check-conf-gate: SELF-TEST FAIL [ratchet-fires-above] — 
check-conf-gate: SELF-TEST FAIL [ratchet-value-locked] — 99
RC=1
```
Two named failures: `[ratchet-value-locked]` (the inline-literal lock) and `[ratchet-fires-above]` (the inline fixture 3 no longer exceeds 99).

**M10 — change one `_CLAIM_FLOORS_LOCK` value (`software-systems-2` 10 -> 9):**
```
check-conf-gate: SELF-TEST FAIL [claim-floor-values-locked] — D-04 LOCK MISMATCH: ['software-systems-2']
RC=1
```
Names `software-systems-2` only — proves the lock is bidirectional and reports by name, not by count.

### Task 3 — CR-02(c)/(d) (D-03 lead-in parameterization)

**Before Task 3:** `check-conf-gate: SELF-TEST PASS — 27 controls run`
**After Task 3:** `check-conf-gate: SELF-TEST PASS — 31 controls run`

**M11 — narrow `_PRESCRIBED_LEAD_INS` to `("**Recommended approach:**",)`:**
```
check-conf-gate: SELF-TEST FAIL [d03-leadin-set-locked] — D-03 LEAD-IN LOCK MISMATCH: ['**Key insight:**', '**Trade-offs acknowledged:**']
check-conf-gate: SELF-TEST FAIL [coverage-floor] — registered/executed control-id mismatch: missing=['d03-fires-on-leadin-key-insight', 'd03-fires-on-leadin-trade-offs-acknowledged'] extra=[]
RC=1
```

**M12 — delete the `CAVEAT_MARKER in claim_text and` conjunct from `_d03_rule_problems_from_text`:**
```
check-conf-gate: SELF-TEST FAIL [d03-passes-on-unmarked-prescribed-leadin] — 
RC=1
```

**M13 — replace `_D03_UNMARKED_TEXT`'s section 6 body with a non-claim string (the vacuity probe):**
```
check-conf-gate: SELF-TEST FAIL [d03-passes-on-unmarked-prescribed-leadin] — {'analysis_id': 'u', 'conclusion_claims': 0, 'untraced_claims': 0, ...}
RC=1
```
Fails on the control's own inline non-vacuity assertion (`untraced_claims: 0`) BEFORE the main assertion runs — proving the fixture cannot pass by silently producing zero claims.

**`git status --porcelain` on the real tree, checked before/after every scratch operation in every task:** empty (aside from this plan's own staged/committed edit to `scripts/check-conf-gate.py`).

## Overall Verification (plan `<verification>` block, run in order after all three tasks)

```
1. python3 scripts/check-conf-gate.py --self-test
   -> check-conf-gate: SELF-TEST PASS — 31 controls run

2. python3 scripts/check-conf-gate.py
   -> check-conf-gate: COVERAGE — measured 28 artifacts across shared-examples, generated-twin
      check-conf-gate: D-08(a) hop re-wrap ... heading_malformed_blocks 0 -> 1
      check-conf-gate: D-08(b) verdict-cell strip ... nonconforming_verdict_cells 0 -> 1
      check-conf-gate: D-08(c) citation removal ... silent_untraced_claims 0 -> 1
      check-conf-gate: PASS  (rc 0)

3. python3 scripts/check-quality-harness.py --self-test
   -> rc 0; chain_detector_pin / conclusion_claims_pin / slice_sections_pin all PASSED

4. git diff --stat scripts/check-quality-harness.py
   -> (empty — CONTRACT-06 untouched)

5. python3 scripts/sync-content.py --check
   -> rc 0

6. python3 scripts/check-registration.py --self-test && python3 scripts/check-registration.py
   -> both rc 0

7. python3 scripts/report-conformance.py --check
   -> report-conformance: PASS — no drift (rc 0)

8. bash scripts/check-firewall-battery.sh
   -> FIREWALL: GREEN (25/25)

9. git status --porcelain
   -> (empty; all changes committed across the three task commits)
```

**Environment note (not a deviation):** `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 24/25 passed)` because this worktree had no `.venv` with pytest for VAL-03's third leg. Ran `uv sync` (the CLAUDE.md-documented remedy) to create `.venv` in the worktree, after which the battery reported `FIREWALL: GREEN (25/25)`. No code or gate behavior was changed; this is the standard BLOCKED-vs-RED distinction CLAUDE.md documents, resolved by the documented remedy.

## Issues Encountered

None beyond the environment note above.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `scripts/check-conf-gate.py`'s `--self-test` now floors its own live-leg enforcement wiring; the blocking gap `18-VERIFICATION.md` recorded is closed.
- Plan 18-10 can proceed to move `_MARKED_RATCHET` (and its new `ratchet-value-locked` inline lock) from 2 to 4 together, as the plan's own out-of-scope note anticipates.
- No blockers. Battery GREEN 25/25; `check-quality-harness.py` byte-unchanged (CONTRACT-06 intact); `git status --porcelain` clean.

---
*Phase: 18-exemplar-conformance*
*Completed: 2026-09-05*
