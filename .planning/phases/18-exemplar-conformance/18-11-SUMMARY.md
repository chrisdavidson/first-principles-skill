---
phase: 18-exemplar-conformance
plan: 11
subsystem: check-conf-gate.py (CONF-GATE)
tags: [gap-closure, self-test, neutralization, CONF-GATE, BL-01, BL-02]
dependency-graph:
  requires: [18-10]
  provides: [BL-01-closed, BL-02-closed]
  affects: [scripts/check-conf-gate.py]
tech-stack:
  added: []
  patterns:
    - "comment-stripping census (line.split('#', 1)[0] idiom, matching scripts/check-traceability.py)"
    - "second, independently transcribed roster floored by set equality (matching _CLAIM_FLOORS_LOCK / _BRANCH_ROSTER_LOCK)"
key-files:
  created: []
  modified:
    - scripts/check-conf-gate.py
decisions:
  - "Used the 'Recommended approach: (chain C2)' lead-in citation as the real corpus defect for the BL-01 replay (a D-03 violation), matching the class of defect 18-VERIFICATION.md's exact reproduction used."
  - "uv sync was run to materialize .venv/pytest so VAL-03's third leg could execute, resolving the FIREWALL: BLOCKED prerequisite gap to FIREWALL: GREEN (25/25); this is an environment setup action, not a code change, and .venv stays gitignored."
metrics:
  duration: "~40 minutes"
  completed: "2026-09-05"
---

# Phase 18 Plan 11: Close BL-01/BL-02 — comment-stripping census and roster equality lock Summary

Closed the two independently-reproduced neutralization vectors that defeated plan 18-09's
call-site census: a `# `-prefix on any enforcement line satisfied the raw-text census (BL-01),
and four of six enforcement symbols could be deleted from both roster tables plus their call
sites with the battery still green (BL-02). `scripts/check-conf-gate.py`'s `--self-test` now
runs 34 controls (was 32), gained `_strip_line_comments` wired before both the count census and
the form-lock match, and gained `_LIVE_CALL_SITES_LOCK` — a second, independently transcribed
six-symbol roster floored by set equality against both `_LIVE_CALL_SITES` and
`_LIVE_CALL_FORMS`.

## What Was Built

**Task 1 (BL-01):** Added `_strip_line_comments(source)` — drops everything from the first `#`
on each line, the same idiom `check-traceability.py` uses at its own comment-stripping site.
Wired as the first statement of `_call_site_census_problems`, so a commented-out enforcement
call no longer satisfies the count census or the whitespace-normalized form-lock match. Added
`_CENSUS_X4_COMMENTED_SOURCE` (derived from `_CENSUS_X1_CLEAN_SOURCE` by `.replace()`, never
hand-duplicated) and control `census-x4-commented`. Amended the function's DISCLOSED
LIMITATION paragraph and the module docstring's closing paragraph to state the commented-out
case as caught and the discarded-result case as the remaining, named residual.

**Task 2 (BL-02):** Added `_LIVE_CALL_SITES_LOCK`, a tuple of the same six enforcement symbol
names, deliberately not derived from either census table by any expression. Added control
`live-call-site-roster-locked`, which asserts (a) `_LIVE_CALL_SITES` agrees with the lock by
set equality, (b) `_LIVE_CALL_FORMS` agrees with the lock by set equality (a separate assertion,
so a FORMS-only narrowing is caught independently of the COUNTS table), and (c) every
`_LIVE_CALL_SITES` value equals 1. Both `_CONTROLS` and `_CONTROL_IDS` grew by one entry per
task (32 → 33 → 34).

## Control count before/after

| Point | Controls |
|-------|----------|
| Before this plan (end of 18-10) | 32 |
| After Task 1 | 33 |
| After Task 2 | 34 |

## Neutralization Ledger

Every mutation below was applied ALONE to a scratch copy under the scratchpad directory
(`rsync -a --exclude .git` from the worktree), never to the real tree. `git status --porcelain`
on the real tree was confirmed empty of scratch artifacts before and after each run (it showed
only this plan's own in-progress edit to `scripts/check-conf-gate.py`, which is expected and
was committed at the end of each task).

### N1 — prefix `# ` to `problems += _targets_problems(rows)` (Task 1 acceptance)

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [live-call-site-census] — ["CALL-SITE CENSUS: _targets_problems occurs 0 time(s) in run_live's source, expected 1"]
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — ["CALL-SITE CENSUS: _targets_problems occurs 0 time(s) in run_live's source, expected 1", "CALL-FORM LOCK: _targets_problems's expected call form not found in run_live's source: 'problems += _targets_problems(rows)'"]
rc=1
```
Exit code 1, naming `[live-call-site-census]`, `_targets_problems`, `occurs 0 time`. Before this
task, 18-REVIEW.md M24 measured `SELF-TEST PASS — 32 controls run`, rc 0, for this mutation.

### N2 — prefix `# ` to `mutation_lines = _run_d08_arm(rows)`

```
check-conf-gate: SELF-TEST FAIL [live-call-site-census] — ["CALL-SITE CENSUS: _run_d08_arm occurs 0 time(s) in run_live's source, expected 1"]
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — ["CALL-SITE CENSUS: _run_d08_arm occurs 0 time(s) in run_live's source, expected 1", "CALL-FORM LOCK: _run_d08_arm's expected call form not found in run_live's source: 'mutation_lines = _run_d08_arm(rows)'"]
rc=1
```
Exit 1, naming `_run_d08_arm` by name.

### N3 — revert `source = _strip_line_comments(source)` (delete that one line), leaving the new fixture/control in place

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [census-x4-commented] — []
rc=1
```
Exit code 1, naming `[census-x4-commented]` — proof the new control fires ALONE when its own fix
is reverted (the empty `[]` is the assertion's own `problems` list, which the control expected
to hold exactly one entry).

### BL-01 acceptance criterion — the verifier's exact reproduction, replayed

Applied on one scratch copy, BOTH:
(a) prefixed `# ` to all five `problems += ...` lines and the `mutation_lines = _run_d08_arm(rows)`
line in `run_live()`;
(b) stripped the `(chain C2) ` citation from the `**Recommended approach:**` lead-in in
`shared/examples/personal-general.md` AND its byte-identical twin
`first-principles/agents/references/examples/personal-general.md` (a real corpus defect: this
lead-in is one of the three D-03 prescribed lead-ins, so removing its citation is exactly the
class of defect `_d03_rule_problems_from_text` exists to catch — the same defect class
18-VERIFICATION.md's reproduction used).

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [live-call-site-census] — ["CALL-SITE CENSUS: _targets_problems occurs 0 time(s) in run_live's source, expected 1", "CALL-SITE CENSUS: _claim_floor_roster_problems occurs 0 time(s) in run_live's source, expected 1", "CALL-SITE CENSUS: _claim_floor_problems occurs 0 time(s) in run_live's source, expected 1", "CALL-SITE CENSUS: _d03_rule_problems_from_text occurs 0 time(s) in run_live's source, expected 1", "CALL-SITE CENSUS: _ratchet_problems occurs 0 time(s) in run_live's source, expected 1", "CALL-SITE CENSUS: _run_d08_arm occurs 0 time(s) in run_live's source, expected 1"]
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — [... same six CALL-SITE CENSUS entries, plus six CALL-FORM LOCK entries naming the same six symbols ...]
rc=1
```
Exit code **1**, stderr names `live-call-site-census` (18-VERIFICATION.md measured
`SELF-TEST PASS — 32 controls run`, rc 0, for this exact pair — now caught).

```
$ python3 scripts/check-conf-gate.py
check-conf-gate: COVERAGE — measured 28 artifacts across shared-examples, generated-twin
Traceback (most recent call last):
  ...
  File "scripts/check-conf-gate.py", line 633, in run_live
    for line in mutation_lines:
                ^^^^^^^^^^^^^^
NameError: name 'mutation_lines' is not defined
rc=1
```
The live leg crashed with `rc=1` (a `NameError`, because `mutation_lines` is referenced later in
`run_live()` but its assignment line was commented out in this replay). This is recorded as
observed, not claimed as fixed by this task — per the plan's own scope statement, **the census
is what catches this, not the live leg**. 18-VERIFICATION.md's prior measurement of this exact
mutation reported the live leg as `PASS, rc 0`; the live-leg outcome differs across the two runs
because the exact set of lines commented differs slightly (this replay comments all six lines
including the `mutation_lines` assignment, which then makes the later `for line in
mutation_lines` reference undefined) — either way, `--self-test` is now what stands between this
class of mutation and a silent green battery, which is the property this plan closes.

After this replay, the scratch copy was discarded and the real tree's `git status --porcelain`
was confirmed to show only this plan's own in-progress edit (never the scratch mutations).

### N4 — delete `_run_d08_arm` from `_LIVE_CALL_SITES` AND `_LIVE_CALL_FORMS` AND its call site AND its `for line in mutation_lines` print loop

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [live-call-site-roster-locked] — CALL-SITE ROSTER DRIFT: ['_run_d08_arm']
rc=1
```
18-VERIFICATION.md measured `SELF-TEST PASS — 32 controls run`, rc 0, for this exact coordinated
edit — now caught by name.

### N5 — same coordinated deletion for `_claim_floor_problems`

```
check-conf-gate: SELF-TEST FAIL [live-call-site-roster-locked] — CALL-SITE ROSTER DRIFT: ['_claim_floor_problems']
rc=1
```

### N6 — same for `_d03_rule_problems_from_text` (delete the whole D-03 loop)

```
check-conf-gate: SELF-TEST FAIL [live-call-site-roster-locked] — CALL-SITE ROSTER DRIFT: ['_d03_rule_problems_from_text']
rc=1
```

### N7 — same for `_claim_floor_roster_problems`

```
check-conf-gate: SELF-TEST FAIL [live-call-site-roster-locked] — CALL-SITE ROSTER DRIFT: ['_claim_floor_roster_problems']
rc=1
```

N4-N7 are the four symbols 18-VERIFICATION.md measured as deletable (from both tables plus call
site) with the battery reporting green; all four now fail `--self-test` by name.

### N8 — delete `_ratchet_problems` from `_LIVE_CALL_FORMS` ONLY (leave `_LIVE_CALL_SITES` whole)

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [live-call-site-roster-locked] — CALL-SITE ROSTER DRIFT: ['_ratchet_problems']
rc=1
```
Proves the FORMS arm is independently load-bearing — the COUNTS table was untouched and still
caught the narrowing via its own equality assertion against `_LIVE_CALL_SITES_LOCK`.

### N9 — change `_LIVE_CALL_SITES["_ratchet_problems"]` from `1` to `2`

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [live-call-site-census] — ["CALL-SITE CENSUS: _ratchet_problems occurs 1 time(s) in run_live's source, expected 2"]
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — [...]
check-conf-gate: SELF-TEST FAIL [census-x1-clean] — [...]
check-conf-gate: SELF-TEST FAIL [census-x2-missing] — [...]
check-conf-gate: SELF-TEST FAIL [census-x3-duplicated] — []
check-conf-gate: SELF-TEST FAIL [form-lock-x1-clean] — [...]
check-conf-gate: SELF-TEST FAIL [form-lock-x2-rewritten] — [...]
check-conf-gate: SELF-TEST FAIL [census-x4-commented] — [...]
check-conf-gate: SELF-TEST FAIL [live-call-site-roster-locked] — CALL-SITE ROSTER DRIFT: expected-count != 1 for ['_ratchet_problems']
rc=1
```
Both the value arm of the roster lock (`live-call-site-roster-locked`, "expected-count != 1")
AND `live-call-site-census` (and several downstream fixture controls, since the synthetic
fixtures are all checked against the mutated `_LIVE_CALL_SITES` too) fire.

## Verification (run in order, from the repo root)

1. `python3 scripts/check-conf-gate.py --self-test` → `check-conf-gate: SELF-TEST PASS — 34 controls run`, rc 0
2. `python3 scripts/check-conf-gate.py` → `COVERAGE — measured 28 artifacts across shared-examples, generated-twin`, three `D-08(a)/(b)/(c) ... 0 -> 1` lines, `check-conf-gate: PASS`, rc 0
3. `python3 scripts/check-quality-harness.py --self-test` → rc 0, all six sub-checks PASSED (including `chain_detector_pin`, `conclusion_claims_pin`, `slice_sections_pin`)
4. `git diff --stat scripts/check-quality-harness.py` → empty (CONTRACT-06 intact)
5. `python3 scripts/sync-content.py --check` → rc 0
6. `python3 scripts/report-conformance.py --check` → `report-conformance: PASS — no drift`, rc 0
7. `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (25/25)`, rc 0 (initially reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 24/25 passed)` because no interpreter in this fresh worktree could import pytest for VAL-03's third leg; ran `uv sync` to materialize `.venv`, which resolved the prerequisite — `.venv` stays gitignored, this is an environment setup step, not a code change)
8. `git status --porcelain` → `M scripts/check-conf-gate.py` only

## Source Assertions

- `/usr/bin/grep -n "_strip_line_comments(source)" scripts/check-conf-gate.py` → exactly one hit
  (line 348, the first statement of `_call_site_census_problems`'s body).
- `_LIVE_CALL_SITES_LOCK` declared once (as a bare tuple of string literals), referenced only
  inside `_control_live_call_site_roster_locked`; no occurrence of it is built from
  `_LIVE_CALL_SITES` or `_LIVE_CALL_FORMS`.

## Deviations from Plan

None — plan executed exactly as written. The one judgment call made explicit: the plan's BL-01
replay instruction said "strip the `(chain C2)` citation" without pinning which of the three
`(chain C2)` occurrences in `personal-general.md`; this session used the `**Recommended
approach:**` lead-in instance because it converts the strip into a genuine D-03 rule violation
(a prescribed lead-in without its citation), which is the corpus-defect class
`_d03_rule_problems_from_text` exists to catch and matches 18-VERIFICATION.md's own description
of "a real corpus defect."

## Assumption Drift (advisory)

None material. The live leg's exact failure mode in the BL-01 replay (a `NameError` crash, rc 1)
differs from 18-VERIFICATION.md's prior measurement of the same scenario (`PASS`, rc 0) — this is
disclosed above rather than treated as a discrepancy to resolve, since the plan explicitly scopes
this replay to the census/`--self-test` leg ("the census is what catches this, not the live leg;
do not claim the live leg was fixed by this task").

## Self-Check: PASSED

- `scripts/check-conf-gate.py` exists and contains `_strip_line_comments`, `_LIVE_CALL_SITES_LOCK`: FOUND
- Commit `6eb5808` (Task 1) exists in `git log`: FOUND
- Commit `ba044ae` (Task 2) exists in `git log`: FOUND
- `python3 scripts/check-conf-gate.py --self-test` → 34 controls, rc 0: FOUND
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (25/25)`: FOUND
