---
phase: 18-exemplar-conformance
plan: 13
subsystem: check-conf-gate.py (CONF-GATE)
tags: [gap-closure, self-test, neutralization, CONF-GATE, BL-04, WR-06]
dependency-graph:
  requires: [18-12]
  provides: [BL-04-closed, WR-06-closed]
  affects: [scripts/check-conf-gate.py]
tech-stack:
  added: []
  patterns:
    - "path-taking, non-exiting core (_run_d08_arm_on) behind a thin row-resolving wrapper (_run_d08_arm), matching _population_floor_problems'/_ratchet_problems' return-not-exit shape"
    - "tempdir-driven --self-test controls (tempfile.TemporaryDirectory), never REPO_ROOT, for the one comparator this file could not previously drive offline"
decisions:
  - "Kept the exact call-form text the plan's key_links/pattern mandates (`d08_problems, mutation_lines = _run_d08_arm(rows)`, no parens) even though it makes N18 (revert _LIVE_CALL_FORMS to the pre-refactor fragment) unfireable — the old fragment is a strict substring of the new one, so the containment-based form-lock cannot distinguish them. Documented as an observed residual (Assumption Drift) rather than silently reported as a pass, and not fixed by widening _call_site_census_problems's matching semantics, which is pre-existing shared infrastructure out of this plan's scope."
  - "uv sync was run to materialize .venv/pytest so VAL-03's third leg could execute, resolving FIREWALL: BLOCKED to FIREWALL: GREEN (25/25); an environment setup action, not a code change — .venv stays gitignored."
metrics:
  duration: "~70 minutes"
  completed: "2026-09-05"
---

# Phase 18 Plan 13: Close BL-04 — control the D-08 live anti-vacuity arm's four predicates Summary

Closed BL-04 from `18-VERIFICATION.md` and its named dependency WR-06 from `18-REVIEW.md`.
`_run_d08_arm` — the one mechanism proving CONF-GATE's live leg is wired to shipped bytes rather
than to nothing — called `sys.exit(1)` at seven internal sites, so no `--self-test` control could
drive it without killing the process; 18-REVIEW.md measured all four of its internal predicates
(M17-M20) neuterable with the battery still green. `scripts/check-conf-gate.py` gains
`_run_d08_arm_on(path, analysis_id)` (a path-taking, non-exiting core), `_run_d08_arm(rows)`
becomes a thin row-resolving wrapper, `run_live()` reports the arm's returned problems through
the standard `check-conf-gate: FAIL — ` path, and four new tempdir-driven controls land
(38 → 42). Battery stays `GREEN (25/25)`; no gate id, CI job or battery slot added.

## What Was Built

**Task 1 (WR-06):** Split `_run_d08_arm` into `_run_d08_arm_on(path: Path, analysis_id: str) ->
tuple[list[str], list[str]]` (all seven `sys.exit(1)` sites replaced by `problems.append(...)`,
restructured as `if <needle missing/not unique>: problems.append(...) / else: <mutate, re-measure,
append either the increment problem or the success line>` so all three arms run to completion in
one pass) and `_run_d08_arm(rows) -> tuple[list[str], list[str]]` (resolves the target row,
returns `([...], [])` instead of exiting when absent, otherwise delegates to `_run_d08_arm_on`).
Added `_display_relpath(path)` so the live leg's printed `relpath` stays byte-identical to the
pre-refactor value (relative to `REPO_ROOT` when possible, absolute for tempdir fixtures that sit
outside it). Updated `run_live()`'s call site to `d08_problems, mutation_lines =
_run_d08_arm(rows)`, reporting `d08_problems` through `check-conf-gate: FAIL — ` before printing
the success block. Updated `_LIVE_CALL_FORMS["_run_d08_arm"]`, the four synthetic census/form-lock
fixtures (`_CENSUS_X1_CLEAN_SOURCE`, `_CENSUS_X2_MISSING_SOURCE`, `_CENSUS_X3_DUPLICATED_SOURCE`,
`_FORM_LOCK_X2_REWRITTEN_SOURCE`; `_CENSUS_X4_COMMENTED_SOURCE` inherits automatically via its
`.replace()` derivation), and the module docstring's Exit-codes block. `_LIVE_CALL_SITES` and
`_LIVE_CALL_SITES_LOCK` keep `_run_d08_arm` at count 1, unchanged. Control count unchanged (38).

**Task 2 (BL-04):** Added `import tempfile` (alphabetical, after `sys`). Added three fixture
texts modelled on `_D03_PASS_TEXT`: `_D08_FIXTURE_NO_NEEDLES` (= `_D03_PASS_TEXT`, carries none
of the three D-08 needles), `_D08_FIXTURE_INERT_NEEDLES` (all three needles embedded once each in
section-1 prose, built by referencing `_D08_HOP_NEEDLE`/`_D08_CELL_NEEDLE`/`_D08_CITE_NEEDLE`
rather than retyping their text, landing where mutating them changes nothing measurable), and
`_D08_FIXTURE_DUPLICATE_HOP` (the inert fixture with the hop needle doubled via
`.replace(needle, needle+needle, 1)`). Added four controls, each writing its fixture into a
`tempfile.TemporaryDirectory()` and calling `_run_d08_arm_on` directly (no `REPO_ROOT` reference
in any of them): `d08-missing-target-row-reported` (calls `_run_d08_arm([])`, wrapped in
`try/except SystemExit` re-raised as a named `AssertionError` — `self_test()` does not catch
`SystemExit`), `d08-missing-sites-reported` (all three "mutation site not found" problems fire in
one pass), `d08-increments-not-produced-reported` (all three "did not increment" problems fire),
`d08-needle-not-unique-reported` (the duplicate-hop "not found (or not unique)" problem fires).
Registered in both `_CONTROLS` and `_CONTROL_IDS`. Control count: 38 → 42.

## Control count before/after

| Point | Controls |
|-------|----------|
| Before this plan (end of 18-12) | 38 |
| After Task 1 (refactor only, no new controls) | 38 |
| After Task 2 | 42 |

## Fixture verification (offline, before wiring into the module)

Confirmed via an ad hoc harness import (mirroring `check-conf-gate.py`'s own import shape)
before committing:

```
NO_NEEDLES  verdict_cells 0 malformed 0 silent 0 hop_count 0 cell_count 0 cite_count 0
INERT       verdict_cells 0 malformed 0 silent 0 hop_count 1 cell_count 1 cite_count 1
DUP         verdict_cells 0 malformed 0 silent 0 hop_count 2 cell_count 1 cite_count 1
```

All three resolve `section_resolution == OK` and leave every measured count at its baseline —
exactly the "mutating the needle changes nothing measurable" property the fixtures require.

## Neutralization Ledger

Every mutation below was applied ALONE to a scratch copy under the scratchpad directory
(`rsync -a --exclude .git` from the worktree), never to the real tree. `git status --porcelain`
on the real tree was confirmed to show only this plan's own in-progress edit to
`scripts/check-conf-gate.py` before and after each run.

### N18 — revert `_LIVE_CALL_FORMS["_run_d08_arm"]` to the pre-refactor fragment (Task 1 acceptance; OBSERVED RESULT DIFFERS FROM PLAN)

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST PASS — 38 controls run
rc=0
```

**Observed, not the acceptance criterion's expected `rc=1`.** The plan's acceptance criterion
states this should fail naming `[live-call-form-lock]`. It does not, because
`_call_site_census_problems`'s form check is CONTAINMENT, not exact match (documented in its own
docstring as DISCLOSED LIMITATION (iii), "a call form rebound to an expression of EQUAL VALUE
remains invisible to it by construction") — and the pre-refactor fragment
`"mutation_lines = " + "_run_d08_arm(rows)"` is a strict SUBSTRING of the mandated new call-form
text `"d08_problems, mutation_lines = _run_d08_arm(rows)"` (both, whitespace-normalized, contain
the identical run `mutation_lines = _run_d08_arm(rows)`). The plan's own `key_links`/`pattern`
field mandates the exact new call-form text verbatim (no parens), so changing the call site's
token shape to break this substring relationship (e.g. `(d08_problems, mutation_lines) =
_run_d08_arm(rows)`) would itself be a deviation from an explicit plan literal. Recorded here as
observed truth rather than fabricated; see Deviations and Assumption Drift below.

### N19 — discard the arm's problems in `run_live()` (`_, mutation_lines = _run_d08_arm(rows)`, no report) (Task 1 acceptance)

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — ["CALL-FORM LOCK: _run_d08_arm's expected call form not found in run_live's source: 'd08_problems, mutation_lines = _run_d08_arm(rows)'"]
rc=1
```

Exit code 1, naming `[live-call-form-lock]` — because renaming the LHS binding from `d08_problems`
to `_` changes the actual source text, and the pinned fragment (which requires the literal name
`d08_problems`) is no longer contained in it.

### N20 — break the (a) mutation site in `shared/examples/personal-general.md` AND its generated twin (Task 1 acceptance)

Edited both files, changing `→ The effective annual compensation gain` to
`→ The effective yearly compensation gain` — preserving the leading arrow (so the underlying
chain stays well-formed and `_targets_problems` does not fire first) while breaking the exact
needle match.

```
$ python3 scripts/check-conf-gate.py
check-conf-gate: FAIL — D-08(a) mutation site not found (or not unique) in shared/examples/personal-general.md
rc=1
```

Exit code 1, stderr contains `check-conf-gate: FAIL — ` and `D-08(a) mutation site not found`;
confirmed separately that stderr contains zero occurrences of `COVERAGE FAIL`.

(First attempt, recorded for completeness: stripping the arrow character entirely —
`ARROW REMOVED The effective annual compensation gain` — broke the underlying document's own
well-formedness and made `_targets_problems`'s `TARGET EXCEEDED [*] heading_malformed_blocks`
fire before the D-08 arm ever ran, exiting 1 for a different reason. The wording-only edit above
is what isolates the D-08(a) site specifically.)

### N21 — same scratch copy as N20, additionally break the (c) site (Task 1 acceptance)

Additionally changed `3. (chain C1) Use the effective compensation figure` to
`3. (chain C2) Use the effective compensation figure` in both files.

```
$ python3 scripts/check-conf-gate.py
check-conf-gate: FAIL — D-08(a) mutation site not found (or not unique) in shared/examples/personal-general.md
check-conf-gate: FAIL — D-08(c) mutation site not found (or not unique) in shared/examples/personal-general.md
rc=1
```

Both `D-08(a)` and `D-08(c)` problems reported from ONE run — WR-06 consequence 1 (all three arms
report in one pass) confirmed. Neither line carries `COVERAGE FAIL`.

After N20/N21, `python3 scripts/check-conf-gate.py --self-test` on the same scratch copy still
reported `SELF-TEST PASS — 38 controls run` (unaffected — self-test never reads the real corpus),
and the real tree's `git status --porcelain` was confirmed to show only this plan's own
in-progress edit.

### N22 (M17) — replace the (a) increment predicate `if malformed_a != baseline_malformed + 1:` with `if False:` (Task 2 acceptance)

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [d08-increments-not-produced-reported] — ['check-conf-gate: D-08(a) hop re-wrap on /tmp/tmpw3wx1fnc/fixture.md — heading_malformed_blocks 0 -> 0']
rc=1
```

Exit code 1, naming `[d08-increments-not-produced-reported]` — 18-REVIEW.md measured this exact
mutation leaving `SELF-TEST PASS — 32 controls run` at rc 0 before this plan.

### N23 (M18) — replace the (b) increment predicate with `if False:`

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [d08-increments-not-produced-reported] — ['check-conf-gate: D-08(b) verdict-cell strip on /tmp/tmpe3nrst7k/fixture.md — nonconforming_verdict_cells 0 -> 0']
rc=1
```

### N24 (M19) — replace the (c) increment predicate with `if False:`

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [d08-increments-not-produced-reported] — ['check-conf-gate: D-08(c) citation removal on /tmp/tmp55ehxfeg/fixture.md — silent_untraced_claims 0 -> 0']
rc=1
```

### N25 (M20) — replace the (a) needle-uniqueness guard with `if False:` (Task 2 acceptance)

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [d08-missing-sites-reported] — ['D-08(a) hop re-wrap mutation on /tmp/tmp_xv387ti/fixture.md did not increment heading_malformed_blocks by exactly 1 (baseline 0, mutated 0)', 'D-08(b) mutation site not found (or not unique) in /tmp/tmp_xv387ti/fixture.md', 'D-08(c) mutation site not found (or not unique) in /tmp/tmp_xv387ti/fixture.md']
check-conf-gate: SELF-TEST FAIL [d08-needle-not-unique-reported] — ['D-08(a) hop re-wrap mutation on /tmp/tmpkbpslhce/fixture.md did not increment heading_malformed_blocks by exactly 1 (baseline 0, mutated 0)', 'D-08(b) verdict-cell strip on /tmp/tmpkbpslhce/fixture.md did not increment nonconforming_verdict_cells by exactly 1 (baseline 0, mutated 0)', 'D-08(c) citation removal on /tmp/tmpkbpslhce/fixture.md did not increment silent_untraced_claims by exactly 1 (baseline 0, mutated 0)']
rc=1
```

Exit code 1, naming BOTH `[d08-missing-sites-reported]` AND `[d08-needle-not-unique-reported]` —
the guard's `else:` branch collapsing to `if False:` means neutering the guard makes the (a)
predicate ALWAYS take the "found" branch, so on the no-needles fixture it now (wrongly) attempts
the mutation and fails to increment, and on the duplicate-hop fixture the not-unique condition
that should have fired the needle-uniqueness message instead falls through to the increment path
and also fails to increment. Exactly the "record whatever actually fires" case the plan's own
acceptance criterion anticipated.

### N26 — restore the target-row-not-found path to `sys.exit(1)` (Task 2 acceptance)

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: COVERAGE FAIL — D-08 target 'personal-general' not found on surface 'shared-examples'; the anti-vacuity arm cannot run
check-conf-gate: SELF-TEST FAIL [d08-missing-target-row-reported] — D-08 arm exited instead of returning
rc=1
```

Exit code 1, naming `[d08-missing-target-row-reported]` with the exact
"D-08 arm exited instead of returning" message — a regression to the old exiting shape is caught
BY NAME, not an unnamed process kill (the plan's stated requirement; `self_test()` does not catch
`SystemExit`, so this is exactly the failure mode `d08-missing-target-row-reported`'s
`try/except SystemExit` guard exists to convert into a named `AssertionError`).

After every N18-N26 run, the scratch copy was discarded and the real tree's
`git status --porcelain` was confirmed to show only this plan's own in-progress edit to
`scripts/check-conf-gate.py`.

## `--self-test` writes nothing outside its tempdirs

Confirmed directly: `git status --porcelain` on the real tree before running
`python3 scripts/check-conf-gate.py --self-test` and immediately after were IDENTICAL
(` M scripts/check-conf-gate.py` only, both times) — the four new D-08 controls' tempdir paths
(e.g. `/tmp/tmpw3wx1fnc/fixture.md`) never appear as tracked-tree paths, and no D-08 control body
references `REPO_ROOT` (confirmed by `grep -n REPO_ROOT scripts/check-conf-gate.py | grep -i
control_d08` returning zero hits).

## Verification (run in order, from the repo root)

1. `python3 scripts/check-conf-gate.py --self-test` → `check-conf-gate: SELF-TEST PASS — 42 controls run`, rc 0
2. `python3 scripts/check-conf-gate.py` → `COVERAGE — measured 28 artifacts across shared-examples, generated-twin`, the three `D-08(a)/(b)/(c) ... 0 -> 1` lines (byte-identical to the pre-refactor form recorded in `18-12-SUMMARY.md`), `check-conf-gate: PASS`, rc 0
3. `python3 scripts/check-quality-harness.py --self-test` → rc 0, all sub-checks PASSED (including `chain_detector_pin`, `conclusion_claims_pin`, `slice_sections_pin`)
4. `git diff --stat scripts/check-quality-harness.py` → empty (CONTRACT-06 intact)
5. `python3 scripts/sync-content.py --check` → rc 0
6. `python3 scripts/report-conformance.py --check` → `report-conformance: PASS — no drift`, rc 0
7. `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (25/25)`, rc 0 (initially reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 24/25 passed)` because no interpreter in this fresh worktree could import pytest for VAL-03's third leg; ran `uv sync` to materialize `.venv`, resolving the prerequisite — `.venv` stays gitignored, an environment setup step, not a code change)
8. `git status --porcelain` → `M scripts/check-conf-gate.py` only, both before and after `--self-test`

## Source Assertions

- `/usr/bin/grep -n "sys.exit" scripts/check-conf-gate.py` → three hits: the module import-failure
  guard (line 84), the `_run_d08_arm_on`/`_run_d08_arm` docstring's own prose mentioning
  "no `sys.exit()`" (line 46 area, plain text not code), and `__main__`'s dispatch (`sys.exit(main())`).
  No `sys.exit` CALL inside either `_run_d08_arm_on` or `_run_d08_arm`'s executable body (verified
  by reading both functions in full).
- `/usr/bin/grep -n "COVERAGE FAIL" scripts/check-conf-gate.py` → zero hits.
- `_run_d08_arm_on(` appears at its own `def`, at `_run_d08_arm`'s delegation call, and in all four
  D-08 control bodies — 6 hits total; `tempfile.TemporaryDirectory` appears once per D-08 control
  that needs a fixture (three of the four; the missing-target-row control needs no filesystem
  fixture at all, matching the plan's own key_link scoping "D-08 controls → `_run_d08_arm_on`" to
  the controls that actually call it with a path).

## Deviations from Plan

**1. [Observed limitation, not a Rule 1-3 auto-fix] N18 does not reproduce the plan's stated
`rc=1` acceptance result.**
- **Found during:** Task 1's neutralization ledger (N18).
- **Issue:** The plan's acceptance criterion for N18 states that reverting
  `_LIVE_CALL_FORMS["_run_d08_arm"]` to the pre-refactor fragment should fail `--self-test` naming
  `[live-call-form-lock]`. It does not: `_call_site_census_problems`'s form check is a
  whitespace-normalized CONTAINMENT test (pre-existing, documented DISCLOSED LIMITATION (iii) in
  its own docstring), and the pre-refactor fragment `"mutation_lines = _run_d08_arm(rows)"` is a
  strict substring of the plan-mandated new call-form text
  `"d08_problems, mutation_lines = _run_d08_arm(rows)"`.
- **Why not fixed:** Two ways to close this were considered and both declined. (a) Widening
  `_call_site_census_problems`'s matching from containment to exact-match — declined: this is
  shared enforcement infrastructure used by all seven `_LIVE_CALL_SITES` symbols and eight
  existing controls (`live-call-form-lock`, `census-x1-clean` through `census-x4-commented`,
  `form-lock-x1-clean`, `form-lock-x2-rewritten`), none of which this plan's `files_modified`
  scope names, and changing its semantics risks breaking assumptions those controls' own fixtures
  rely on — out of this plan's scope per the Scope Boundary rule. (b) Changing the call-site token
  shape (e.g. wrapping the LHS in parens: `(d08_problems, mutation_lines) = _run_d08_arm(rows)`)
  to break the substring relationship — declined: the plan's own frontmatter `key_links` entry
  pins the exact literal `pattern: "d08_problems, mutation_lines = _run_d08_arm\\(rows\\)"`
  (no parens) as a must-have; deviating from it to make one ledger item pass would violate an
  explicit plan literal to satisfy an unlisted regex nowhere else in the plan.
- **Disposition:** Recorded here as observed fact rather than a fabricated pass. This is a
  pre-existing residual of `_call_site_census_problems`'s containment semantics (an extension of
  disclosed bound (iii), "equal value", to "superset text"), not a defect introduced by this
  plan's refactor, and not one this plan's stated scope (`_run_d08_arm`/`_run_d08_arm_on`, four
  new tempdir controls) is chartered to close. Every OTHER neutralization in both tasks' ledgers
  (N19-N26) fires exactly as the plan specifies.

No other deviations — both tasks' remaining acceptance criteria, source assertions, and
neutralization items were executed and verified exactly as written.

## Assumption Drift (advisory)

Assumption drift: reverting `_LIVE_CALL_FORMS["_run_d08_arm"]`'s value alone will be caught by
the form-lock control (the plan's working assumption for N18) -> the reverted fragment is a
strict substring of the actual (mandated) call-form text, so the containment-based check cannot
distinguish the two states (the disclosed "equal value" bound extends, unremarked, to any
substring-superset rebind, not just an exactly-equal one). This is advisory only — it does not
gate this plan's completion, since N19-N26 (the remaining seven ledger items, covering the
discard-the-binding regression, both mutation-site-breaking scenarios, and all four Task 2
predicates) all fire exactly as specified, and the plan's automated acceptance criteria
(`--self-test` control count, live-leg byte-identical output, source assertions, full battery)
all pass.

## Self-Check: PASSED

- `scripts/check-conf-gate.py` exists and contains `_run_d08_arm_on`, `_display_relpath`,
  `_D08_FIXTURE_NO_NEEDLES`, `_D08_FIXTURE_INERT_NEEDLES`, `_D08_FIXTURE_DUPLICATE_HOP`: FOUND
- Commit `eef0a7f` (Task 1) exists in `git log`: FOUND
- Commit `b63abe1` (Task 2) exists in `git log`: FOUND
- `python3 scripts/check-conf-gate.py --self-test` → 42 controls, rc 0: FOUND
- `python3 scripts/check-conf-gate.py` → three byte-identical D-08 lines, `PASS`, rc 0: FOUND
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (25/25)`: FOUND
- `git status --porcelain` → `scripts/check-conf-gate.py` only, both files committed: FOUND
