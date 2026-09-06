---
phase: 20-live-conformance
plan: 05
subsystem: testing
tags: [conformance, live-capture, quality-harness, report-generator, self-test, floors]

# Dependency graph
requires:
  - phase: 20-live-conformance
    provides: "plan 20-04's live-conformance surface (build_live_row, compute_live_headline, the published 5-of-8 rate, and 71 --self-test controls)"
provides:
  - "scripts/report-conformance.py: _live_roster_problems, _live_disposition_problems, _LIVE_POPULATION_FLOORS/_live_population_problems, _LIVE_CALL_SITES/_LIVE_CALL_FORMS/_LIVE_CALL_SITES_LOCK/_live_call_site_census_problems/_live_call_sites_roster_problems, all wired into cmd_check(), plus 19 new offline --self-test controls (90 total)"
  - "a 10-row mutation census on a disposable scratch copy proving each floor fails by name when its own target is broken"
affects: [20-06]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "the four Phase-19 corpus-floor shapes (roster EQUALITY, union-of-non-clean-shapes disposition, DENOMINATOR population floors, source-text call-site census with a second independently-transcribed lock) copied verbatim and renamed for the live-conformance surface, rather than generalized into shared helpers"
    - "collect-then-report: the three live floors sit in cmd_check() immediately after the five pre-existing corpus floors, in the same list-concatenation shape, so a live floor breach and a corpus floor breach both surface in one run"

key-files:
  created: []
  modified:
    - scripts/report-conformance.py

key-decisions:
  - "_LIVE_POPULATION_FLOORS pinned at conclusion_claims=64, verdict_cells=153, chain_blocks=64 -- derived by running the same one-liner _CORPUS_POPULATION_FLOORS' own comment prescribes against docs/data/conformance.json's live_conformance.rows (all 8 rows resolved OK), not guessed and not copied from 20-04-SUMMARY.md's table (which does not carry these three fields)"
  - "_live_disposition_problems collapses the three non-clean shapes (no analysis / unreadable / scored non-zero) onto the single `clean` field _live_row_clean already computes, rather than re-deriving the union from two separate booleans the way the corpus floor does (`target_missed`/`no_column_fired`) -- the live surface has no catalogued-target join, so `clean is not True` is already the exact union CONF-10 needs, and the reported message states which of the three conditions triggered the check"
  - "The call-site census functions (_live_call_site_census_problems, _live_call_sites_roster_problems) are never called from inside cmd_check() itself -- matching the corpus precedent exactly, they are self-test-only tools that inspect cmd_check's own source text via inspect.getsource(cmd_check); only the three real floor calls (roster, disposition, population) are wired into cmd_check's live body"
  - "Split the single combined diff into two atomic commits (Task 1: roster+disposition; Task 2: population+call-site census) after authoring both together, by mechanically removing and re-inserting the Task-2-only hunks -- byte-diffed against a full backup before the second commit to confirm no content was lost in the split"

requirements-completed: [CONF-09, CONF-10]

# Metrics
duration: "~1h"
completed: 2026-09-06
---

# Phase 20 Plan 05: Live-Conformance Floors and Mutation-Verified Falsifiability Summary

**Wired four new floors (roster EQUALITY, union-of-non-clean-shapes disposition, three DENOMINATOR population floors, and a source-text call-site census with a second independently-transcribed lock) into `cmd_check()` for the live-conformance surface, then broke each one on a disposable scratch copy and confirmed it fails by name — all ten scripted mutations CAUGHT, published rate unchanged at 5 of 8, battery GREEN 25/25.**

## Performance

- **Duration:** ~1h
- **Started:** continuation of same session lineage as 20-01 through 20-04
- **Completed:** 2026-09-06
- **Tasks:** 3 (all auto, each committed)
- **Files modified:** 1 (`scripts/report-conformance.py`)

## Accomplishments

- `_live_roster_problems` compares the live catalog's row-id set against the discovered `.jsonl` capture-stem set by set EQUALITY (never subset), folding in `_read_live_catalog`'s own parse problems first — copied from `_corpus_roster_problems` verbatim in shape, renamed, and documented against the D-20-A landmine (compares capture stems, never `.md` analysis stems, so a stub run with no persisted analysis is still a roster member).
- `_live_disposition_problems` checks every row whose `clean` is not `True` — the union of "no analysis produced", "unreadable", and "scored non-zero on one or more measured fields" — for a disposition that is non-empty, not the literal `"MISSING"`, and begins with `fix` / `accept-with-reason` / `defer-with-owner`, reusing `_VALID_DISPOSITION_PREFIXES` unchanged.
- `_LIVE_POPULATION_FLOORS` (`conclusion_claims=64`, `verdict_cells=153`, `chain_blocks=64`) and `_live_population_problems` report a per-item zero (`conclusion_claims`/`chain_blocks`) and a surface-wide denominator breach, summed over resolved (`section_resolution == "OK"`) rows only — an unreadable or no-analysis row is skipped here, never double-reported (its own state is already carried by the roster/disposition floors).
- `_LIVE_CALL_SITES`/`_LIVE_CALL_FORMS`/`_LIVE_CALL_SITES_LOCK` plus `_live_call_site_census_problems` (reusing `_strip_line_comments` unmodified) and `_live_call_sites_roster_problems` — a pure source-text census over `cmd_check()`'s own body, locked by a second, independently transcribed roster of the three enforcement symbol names, asserted by set equality against the census tables.
- All three real floors (`_live_roster_problems`, `_live_disposition_problems`, `_live_population_problems`) wired into `cmd_check()` in the collect-then-report block, immediately after the five pre-existing corpus floors. The two census functions are never called from inside `cmd_check()` — matching the corpus precedent exactly, they inspect `cmd_check`'s own source at self-test time via `inspect.getsource(cmd_check)`.
- 19 new offline `--self-test` controls registered in both `_CONTROLS` and `_CONTROL_IDS` (90 total, up from 71); none reads the real `tests/live-conformance-v9.0/` fixture.
- A 10-row mutation census (Task 3, below) on a disposable `rsync`-copied scratch tree, each mutation applied and reverted independently, proving every floor fires by name when its own target is broken.

## Task Commits

1. **Task 1: Roster equality floor and disposition floor, wired into cmd_check** - `7fb3927` (feat)
2. **Task 2: Population denominator floors and the call-site census** - `d5e2ac6` (feat)
3. **Task 3: Break every floor on a scratch copy and watch it fire by name** - no code changes (scratch-only); documented below

**Plan metadata:** (this commit, immediately following)

## Files Created/Modified

- `scripts/report-conformance.py` — `_live_roster_problems`, `_live_disposition_problems`, `_LIVE_POPULATION_FLOORS`, `_live_population_problems`, `_LIVE_CALL_SITES`, `_LIVE_CALL_FORMS`, `_LIVE_CALL_SITES_LOCK`, `_live_call_site_census_problems`, `_live_call_sites_roster_problems`, three new lines in `cmd_check()`, 19 new `--self-test` controls (90 total)

## Decisions Made

See `key-decisions` in the frontmatter above for the population-floor derivation, the disposition-predicate collapse onto `clean`, the census/cmd_check wiring boundary, and the two-commit split methodology.

## Population Floor Values: Measured vs. Pinned

Derived 2026-09-06 by running `_CORPUS_POPULATION_FLOORS`'s own prescribed one-liner against the live surface:

```
python3 -c "
import json
data = json.load(open('docs/data/conformance.json'))
rows = data['live_conformance']['rows']
for f in ('conclusion_claims', 'verdict_cells', 'chain_blocks'):
    print(f, sum(r[f] for r in rows if r['section_resolution'] == 'OK'))
"
```

| field | measured total (all 8 rows resolved OK) | pinned floor |
|---|---|---|
| conclusion_claims | 64 | 64 |
| verdict_cells | 153 | 153 |
| chain_blocks | 64 | 64 |

All three match exactly (the floor is set from the measurement, never guessed), and `--self-test` control `live-population-floor-values-locked` pins these as an inline literal independent of the module constant.

## Task 3: Mutation Census

Method (phase invariant 4): `rsync -a --exclude .git` the repo to a scratchpad temp directory, confirmed `git status --porcelain` empty in the real tree before starting and after every mutation. Each mutation was applied to the scratch copy only, the relevant command run, the exact failure line recorded, then the scratch copy was fully re-synced (deleted and re-copied) before the next mutation so no mutation could mask another. The scratch directory was deleted at the end.

| # | Mutation | Command | Verbatim failure line | CAUGHT? |
|---|---|---|---|---|
| 1 | Deleted `PR-P2.jsonl` from the scratch fixture | `--check` | At N=8 exactly matching `MIN_LIVE_CONFORMANCE_RUNS`, the pre-existing plan-20-04 discovery floor trips FIRST: `report-conformance: COUNT FLOOR FAIL — expected >= 8 files matching tests/live-conformance-v9.0/*.jsonl, found 7`. To isolate and directly exercise this plan's own roster floor (not masked by the earlier floor), `MIN_LIVE_CONFORMANCE_RUNS` was additionally lowered to 7 in the scratch copy only for this one mutation (a disclosed methodological adjustment, not a defect — the discovery floor is out of scope for this plan). With that adjustment: `report-conformance: FAIL — D-20 LIVE ROSTER DRIFT: missing=[] extra=['PR-P2']` | CAUGHT (by the pre-existing discovery floor first; the new roster floor fires as designed once that earlier floor is worked around) |
| 2 | Added an untracked `ZZ-EXTRA.jsonl` (a synthetic "completed"-shaped terminal-result line, no `.md` sibling) not in the catalog | `--check` | `report-conformance: FAIL — D-20 LIVE ROSTER DRIFT: missing=['ZZ-EXTRA'] extra=[]` (also fired `LIVE SILENT PASS [ZZ-EXTRA]: unreadable, no disposition recorded` as a bonus finding from the disposition floor — see Issues Encountered) | CAUGHT |
| 3 | Replaced `PR-N1`'s real disposition text with the literal `MISSING` in the scratch catalog | `--check` | `report-conformance: FAIL — LIVE SILENT PASS [PR-N1]: scored non-zero on one or more measured fields, no disposition recorded`. The non-clean branch was exercised **directly** — `PR-N1` is a genuinely non-clean landed run (1 nonconforming verdict cell), no synthesis needed | CAUGHT |
| 4 | Replaced `PR-N1`'s disposition with `probably fine` | `--check` | `report-conformance: FAIL — LIVE DISPOSITION FORM [PR-N1]: 'probably fine' does not begin with fix / accept-with-reason / defer-with-owner` | CAUGHT |
| 5 | Truncated `PR-P1.md`'s §6 Conclusion to plain prose with no bold claims, so its `conclusion_claims` reads 0 | `--check` | `report-conformance: FAIL — LIVE POPULATION [PR-P1] conclusion_claims: 0 — a form-clean reading over an empty population is not a probe` (also breached the surface-wide `conclusion_claims` floor as a side effect: `58 < floor 64`) | CAUGHT |
| 6 | Deleted one Assumptions Table row (A16) from `PR-P2.md`, dropping its own `verdict_cells` from 16 to 15 (never zero) and the surface-wide sum from 153 to 152 | `--check` | `report-conformance: FAIL — LIVE POPULATION FLOOR BREACH verdict_cells: 152 < floor 153 — a zero defect count against a shrunken population is not conformance` (no per-item-zero message fired, confirming this exercises the surface-wide floor distinctly from mutation 5) | CAUGHT |
| 7 | Deleted the `_live_roster_problems(...)` call line from `cmd_check` | `--self-test` | `report-conformance: SELF-TEST FAIL [live-call-site-census-positive] — ["CALL-SITE CENSUS: _live_roster_problems occurs 0 time(s) in cmd_check's source, expected 1", "CALL-FORM LOCK: _live_roster_problems's expected call form not found in cmd_check's source: 'problems += _live_roster_problems(live_catalog_entries, live_catalog_problems, live_rows)'"]` | CAUGHT |
| 8 | Commented out the `_live_disposition_problems(...)` call with a leading `#` | `--self-test` | `report-conformance: SELF-TEST FAIL [live-call-site-census-positive] — ["CALL-SITE CENSUS: _live_disposition_problems occurs 0 time(s) in cmd_check's source, expected 1", "CALL-FORM LOCK: _live_disposition_problems's expected call form not found in cmd_check's source: 'problems += _live_disposition_problems(live_rows)'"]` — the exact case `_strip_line_comments` exists for | CAUGHT |
| 9 | Rewrote the `_live_population_problems(...)` call's argument from `live_rows` to `rows` | `--self-test` | `report-conformance: SELF-TEST FAIL [live-call-site-census-positive] — ["CALL-FORM LOCK: _live_population_problems's expected call form not found in cmd_check's source: 'problems += _live_population_problems(live_rows)'"]` (the count census alone still passed — the symbol name is unchanged, only its argument moved — confirming the CALL-FORM LOCK layer, not the CALL-SITE CENSUS layer, is what catches an argument rewrite) | CAUGHT |
| 10 | Narrowed `_LIVE_CALL_SITES_LOCK` to two symbols (dropped `_live_population_problems`) | `--self-test` | `report-conformance: SELF-TEST FAIL [live-call-sites-roster-lock-narrowed] — ["ROSTER LOCK: _LIVE_CALL_FORMS diverges from lock: ['_live_population_problems']"]`. The dropped symbol is named, though via a different control than anticipated: narrowing the real module-level `_LIVE_CALL_SITES_LOCK` also changed the *default* `lock` argument that control `live-call-sites-roster-lock-narrowed` itself calls with, so its own `narrowed_sites` (built from `_LIVE_CALL_SITES`, minus `_live_population_problems`) now coincidentally matches the mutated 2-item lock exactly, and the `_LIVE_CALL_SITES` half of that control's own assertion goes vacuously true; the `_LIVE_CALL_FORMS` half (still the real 3-item table) diverges instead and fails the assertion, naming the same dropped symbol | CAUGHT |

**10 of 10 mutations CAUGHT.** No mutation was left uncaught or required a fix landed in this plan.

Real-tree confirmation after every mutation and after the whole census: `git status --porcelain` empty; `git diff HEAD --stat` empty; the scratch directory (and its two intermediate scratchpad file extracts used only during the Task 1/Task 2 commit split, described below) do not touch the working tree.

## Call-Site Census Disclosed Bound

Stated in the same voice `CLAUDE.md`'s CONF-GATE row uses: `_live_call_site_census_problems` and `_live_call_sites_roster_problems` read **source text** and observe **no behaviour**. They catch a call site that was **deleted**, **commented out**, or **rewritten** (mutations 7, 8, 9 above) — they do **not** catch a call whose returned `problems` list is computed correctly and then discarded before reaching `cmd_check`'s failure reporter. This bound is unchanged from `_corpus_call_site_census_problems`'s own documented limit and is restated verbatim in the new functions' docstrings.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `_control_live_population_per_item_unreadable_skipped`'s first draft asserted `== []` on a single unreadable row, which always fails**
- **Found during:** Task 2, first `--self-test` run after authoring the population floor and its controls
- **Issue:** A single-row list containing only an unreadable row is skipped by the per-item check (correct), but `_live_population_problems` still runs the **surface-wide** floor check unconditionally, and a one-row population is always below `_LIVE_POPULATION_FLOORS`' pinned totals — so the control's `== []` assertion could never pass regardless of correctness.
- **Fix:** Paired the unreadable row with a second, readable "healthy" row whose own counts exactly meet the three floors (`conclusion_claims=64, verdict_cells=153, chain_blocks=64`), so the pair together produces `== []` — proving the unreadable row is neither summed nor named, without the surface-wide floor firing for an unrelated reason.
- **Files modified:** `scripts/report-conformance.py`
- **Verification:** `python3 scripts/report-conformance.py --self-test` — 90/90 controls pass.
- **Committed in:** `d5e2ac6` (Task 2 commit; the fix was made before either commit was created, so both commits already carry the corrected control)

---

**Total deviations:** 1 auto-fixed (bug)
**Impact on plan:** The fix was necessary for the control to be a valid test of its own claim; no scope creep, no change to any floor's production behavior.

## Issues Encountered

- **Mutation 2's bonus finding is a synthetic-only edge case, not a defect.** The synthetic `ZZ-EXTRA.jsonl` I added carries a "completed"-shaped terminal-result line but no `.md` sibling — a state `build_live_row`'s own docstring says is produced by "every non-`completed` outcome," never a `completed` one. Because no real capture can be `completed` with no persisted analysis (a genuine completion always attempts the write), `_live_disposition_problems`'s condition text labeled this row `"unreadable"` rather than `"no analysis produced"` (my `elif` branch checks `section_resolution != "OK"` before distinguishing `"no-analysis"` from a genuine `SectionResolutionError` string). The `LIVE SILENT PASS` message still fired correctly and named the row; only the human-readable condition phrase was imprecise for this unreachable-in-practice combination. Not fixed — it does not affect any floor's pass/fail behavior, only wording on a state that cannot occur from a real capture, and fixing it is out of this plan's scope (Task 1/2's `<action>` text did not ask for a fourth condition branch).
- No other issues.

## User Setup Required

None.

## Next Phase Readiness

- `scripts/report-conformance.py` now falsifies the published live-conformance rate on four independent axes (roster, disposition, population, call-site enforcement), each demonstrated failing by name on a disposable scratch copy.
- Published rate unchanged: `docs/conformance-baseline.md` / `docs/data/conformance.json` were not regenerated by this plan (floors do not alter rendered output) and still publish 5 of 8. `git diff --name-only` after both task commits listed only `scripts/report-conformance.py`.
- `--self-test` at 90 controls (up from 71); `--check` byte-reproducible; `check-quality-harness.py --self-test` green with all three CONTRACT-06 pins byte-unchanged; `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (25/25)`.
- `_GATED_SURFACES` unchanged (still the 2-tuple `("shared-examples", "generated-twin")`); no new CI job; battery total unchanged at 25.
- No blockers for plan 20-06.

---
*Phase: 20-live-conformance*
*Completed: 2026-09-06*
