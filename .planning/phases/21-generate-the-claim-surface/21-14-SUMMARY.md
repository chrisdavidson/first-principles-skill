---
phase: 21-generate-the-claim-surface
plan: 14
subsystem: infra
tags: [gate-registry, claim-surface, self-test, executed-vs-registered-floor, sync-content, version-stamps]

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    provides: "plan 21-11's CONF-SURFACE claim-surface generator/drift gate and plan 21-13's pre-commit gate disambiguation"
provides:
  - "sync-content.py's control roster (_SELF_TEST_CONTROL_IDS) floored against what cmd_self_test() actually executes, in both directions, via _control_roster_problems()"
  - "check-version-stamps.py's registered_surfaces un-inverted to publish the four walked source kinds (not the excluded globs), floored against collect_stamps()'s own walk sites via _stamp_roster_problems()"
  - "check-version-stamps.py's argparse dispatch (WR-12): a mistyped flag now exits non-zero instead of silently running the live scan"
  - "scripts/_gate_registry.py --self-test's 16 controls wired into gen-gate-docs.py --self-test (registry-self-test), running in the battery, CI and both pre-commit hooks"
  - "SlugCollisionError / _assert_no_slug_collisions(): a duplicate docs/gates/<slug>.md page slug now raises at generation time instead of silently overwriting a page"
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Executed-vs-registered floor as a first-statement-of-block append (executed.append(id) before any try/fixture setup) so a raising control still counts as executed -- sync-content.py's cmd_self_test()"
    - "Module-level _LAST_WALKED_SOURCE_KINDS collector, reset at entry / assigned at exit, letting a pure function record which of several unconditional/conditional walk sites actually ran without changing the caller's return signature -- check-version-stamps.py's collect_stamps()"
    - "Asymmetric missing=/extra= naming per baseline: sync-content.py's floor treats REGISTERED as baseline (missing = registered-not-executed); check-version-stamps.py's floor treats WALKED as baseline (missing = walked-not-registered, i.e. the roster under-claims). Each direction is spelled out in-comment because the two scripts' floors intentionally use opposite polarities for the same English words."
    - "Subprocess-driven self-test wiring: gen-gate-docs.py's registry-self-test control runs scripts/_gate_registry.py --self-test via subprocess.run with capture_output+timeout, surfacing the child's stderr in the parent's assertion message so a failure names which nested control broke."

key-files:
  created: []
  modified:
    - scripts/sync-content.py
    - scripts/check-version-stamps.py
    - scripts/gen-gate-docs.py
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - docs/gates/VERSION-01.md
    - docs/gates/DUAL-04.md
    - docs/gates/CONF-SURFACE.md

key-decisions:
  - "sync-content.py's floor keeps missing=/extra= polarity as (registered - executed)/(executed - registered) -- matching check-registration.py's and check-loop-closure.py's existing in-repo idiom -- while check-version-stamps.py's floor deliberately uses the opposite polarity, (walked - registered)/(registered - walked), because the plan's own acceptance criteria name 'over-claim -> extra=' and 'under-claim -> missing=' for that script specifically. Both are documented in-comment as intentional, not accidental drift between the two floors."
  - "check-version-stamps.py's kept _EXCLUDED_GENERATED_GLOBS as a constant (not deleted) but removed it from describe()'s registered_surfaces; it now backs a new self-test sanity control (excluded-globs-never-walked) plus the hand-written VERSION-01.md narrative, so it stays a real, exercised piece of code rather than a dead constant."
  - "Task 2's docs/gates/VERSION-01.md regeneration (gen-gate-docs.py --write) ran inside Task 2, ahead of Task 3's own regeneration, because Task 2's acceptance criteria required the Facts fence and hand-written narrative to already agree by set equality before Task 3 begins. Task 3's later --write on top of this was idempotent for VERSION-01.md/DUAL-04.md (no further diff) and only moved CONF-SURFACE's own control_count (51 -> 53)."
  - "_control_slug_collision_raises() uses two DIFFERENT synthetic keys (FAKE-01 and FAKE:01) that collide via _page_slug's ':' -> '-' rewrite, rather than two identical keys -- proving the floor catches a collision between distinct registry entries, the actual shape T-21-14-02 threatens, not merely a duplicate-key typo (which _gate_registry.py's own no-gate-id-duplicated control already covers)."

requirements-completed: [CONF-11]

# Metrics
duration: 74min
completed: 2026-09-07
---

# Phase 21 Plan 14: Close CONF-11's live-constants gap on two wrong emissions and wire the orphaned registry self-test Summary

**Floored sync-content.py's and check-version-stamps.py's `--describe` control/surface rosters against what actually executes/walks in both directions (closing CR-02 and CR-03's inverted `registered_surfaces`), wired `_gate_registry.py --self-test`'s 16 controls (including the sole duplicate-key check) into every automated path via `gen-gate-docs.py --self-test`, and made a duplicate detail-page slug raise at generation time instead of silently deleting a page.**

## Performance

- **Duration:** 74 min
- **Started:** 2026-09-07 (first Read)
- **Completed:** 2026-09-07
- **Tasks:** 3
- **Files modified:** 8 (scripts/sync-content.py, scripts/check-version-stamps.py, scripts/gen-gate-docs.py, CLAUDE.md, docs/ARCHITECTURE.md, docs/gates/VERSION-01.md, docs/gates/DUAL-04.md, docs/gates/CONF-SURFACE.md)

## Accomplishments

- `scripts/sync-content.py`'s `_SELF_TEST_CONTROL_IDS` roster (11 hand-typed ids) now equals `cmd_self_test()`'s actual twelve-then-thirteen lettered blocks (a-m): each block appends its own id to a local `executed` list as its first statement, and a new `_control_roster_problems()` pure helper floors `set(executed) == set(_SELF_TEST_CONTROL_IDS)` in one message covering both directions. Control `(m)` is a permanent registered negative arm proving the floor fires, driven against a synthetic executed/registered pair through the SAME helper the live floor calls (not a re-implementation).
- `scripts/check-version-stamps.py`'s `describe()` now publishes `sorted(_STAMP_SOURCE_KINDS)` -- the four kinds `collect_stamps()` actually walks -- under `registered_surfaces`, replacing the previous inverted emission of `_EXCLUDED_GENERATED_GLOBS` (the surfaces the gate explicitly does NOT read). `collect_stamps()` now records which of its four walk sites ran into a module-level `_LAST_WALKED_SOURCE_KINDS` (reset at entry, assigned at exit), and `self_test()` gained four new controls: a live-tree positive floor, an over-claim negative arm (fabricated roster entry -> `extra=`), an under-claim negative arm (fixture tree missing a source -> `missing=`), and a sanity control confirming the excluded generated-tree globs are never among what was walked.
- Replaced `check-version-stamps.py`'s `if "--flag" in sys.argv[1:]` dispatch with `argparse` (WR-12, mutually exclusive `--self-test`/`--describe` group): a mistyped flag (`--decribe`) now exits non-zero via argparse's own usage/error path instead of silently falling through to the live scan and exiting 0. A registered control drives this via `main(["--decribe"])` and asserts `SystemExit` with a non-zero code.
- `scripts/_gate_registry.py --self-test`'s 16 controls -- previously invoked nowhere automated -- are now wired into `gen-gate-docs.py --self-test` via a new `registry-self-test` control that runs the registry script as a subprocess and asserts exit 0, surfacing `proc.stderr` on failure. `generate_all()` now calls `_assert_no_slug_collisions()` before building its `targets` dict, raising a named `SlugCollisionError` listing every colliding key when two registry entries would resolve to the same `docs/gates/<slug>.md` page -- structurally impossible rather than merely asserted by `_control_page_per_entry`'s set comparison (which cannot see a same-cardinality collision).
- Regenerated the claim surface twice (once inside Task 2 to converge `docs/gates/VERSION-01.md`'s Facts fence with its already-corrected narrative, once at the end of Task 3 to pick up the two new `gen-gate-docs.py` controls): `CLAUDE.md`'s and `docs/ARCHITECTURE.md`'s DUAL-04 row moved `control_count` 11 -> 13, VERSION-01 row moved `registered_surfaces` 2 -> 4, and CONF-SURFACE's own row/page moved `control_count` 51 -> 53. No other gate's row or page changed.

## Task Commits

1. **Task 1: Make sync-content.py's control roster equal to what actually executes** - `895504c` (feat)
2. **Task 2: Un-invert VERSION-01's registered_surfaces and floor it against the walk sites** - `890dd1e` (feat)
3. **Task 3: Run the registry self-test automatically, make slug collision impossible, regenerate** - `5a72c5a` (feat)

_No plan-metadata commit in this worktree run — orchestrator handles STATE.md/ROADMAP.md centrally after merge._

## Files Created/Modified

- `scripts/sync-content.py` - `_SELF_TEST_CONTROL_IDS` roster 11 -> 13 ids (a-m); `_control_roster_problems()` pure helper (3 occurrences: def + 2 calls); every lettered block appends its id as its first statement; new control (m), a permanent negative arm; rewrote the roster's comment, which previously falsely claimed control (l) kept the roster in sync
- `scripts/check-version-stamps.py` - `describe()`'s `registered_surfaces` un-inverted to the 4 walked kinds; `_STAMP_SOURCE_KINDS` entries cleaned of a prose suffix; `collect_stamps()` records `_LAST_WALKED_SOURCE_KINDS`; `_stamp_roster_problems()` pure helper; 4 new self-test controls (positive floor, over-claim, under-claim, excluded-globs sanity) + 1 typo-dispatch control; `argparse` replaces the substring dispatch; `main()` gained an optional `argv` parameter
- `scripts/gen-gate-docs.py` - `SlugCollisionError` + `_assert_no_slug_collisions()`, called at the top of `generate_all()`; `_control_registry_self_test_passes` (subprocess-driven) and `_control_slug_collision_raises` (synthetic two-entry list), both registered in `_CONTROLS` and `_CONTROL_IDS` (51 -> 53 controls)
- `CLAUDE.md` - regenerated gate table (DUAL-04, VERSION-01, CONF-SURFACE rows moved; generated region only)
- `docs/ARCHITECTURE.md` - regenerated gate table (same three rows; generated region only)
- `docs/gates/VERSION-01.md` - regenerated Facts fence (`registered_surfaces` 2 -> 4, un-inverted); hand-written narrative updated to name the 4 walked kinds and separately state the generated-tree exclusion, so fence and narrative agree by mechanical set equality
- `docs/gates/DUAL-04.md` - regenerated Facts fence (`control_ids`/`control_count` 11 -> 13)
- `docs/gates/CONF-SURFACE.md` - regenerated Facts fence (`control_ids`/`control_count` 51 -> 53; `literal_scan_hits` 157 -> 158, a byproduct of the new count literals introduced elsewhere, still fully exempt -- `literal_scan_non_exempt` stayed 0)

## Decisions Made

See `key-decisions` in frontmatter above (polarity choice for the two floors' missing=/extra= naming, keeping `_EXCLUDED_GENERATED_GLOBS` alive via a sanity control rather than deleting it, running Task 2's own `gen-gate-docs.py --write` ahead of Task 3's, and the two-distinct-keys shape of the slug-collision negative control).

## Deviations from Plan

None — plan executed exactly as written. One nuance worth recording: the plan's Task 2 acceptance criteria required `docs/gates/VERSION-01.md`'s Facts fence and hand-written narrative to already agree by mechanical set equality, which meant running `gen-gate-docs.py --write` inside Task 2 rather than deferring all regeneration to Task 3 as the action prose for Task 3 implied ("Then run `python3 scripts/gen-gate-docs.py --write`"). Task 3's own `--write` at the end was idempotent on top of Task 2's earlier one for `VERSION-01.md`/`DUAL-04.md` (no further diff on those two pages), and only moved `CONF-SURFACE`'s own control count. This is a sequencing clarification, not a scope or behavior change — the plan's Task 2 acceptance criteria itself required the earlier regeneration.

## Falsification Arms Recorded (verbatim failure text, scratch copies, real tree untouched before/after every run)

**sync-content.py, `missing=` direction (deleted `executed.append("k")`):**
```
control roster/executed mismatch: missing=['k'] extra=[]
```
Exit 1.

**sync-content.py, `extra=` direction (removed `"l"` from `_SELF_TEST_CONTROL_IDS`):**
```
control roster/executed mismatch: missing=[] extra=['l']
```
Exit 1.

**check-version-stamps.py, over-claim direction (fabricated fifth roster entry):**
```
check-version-stamps --self-test: kind-roster-matches-walked FAIL (["stamp-source-kind roster/walked mismatch: missing=[] extra=['fabricated-fifth-kind']"])
```
Exit 1. This is the direction CR-05 named as previously undetectable.

**check-version-stamps.py, under-claim direction (removed `shared/spine/SKILL.meta.yml` from the roster):**
```
check-version-stamps --self-test: kind-roster-matches-walked FAIL (["stamp-source-kind roster/walked mismatch: missing=['shared/spine/SKILL.meta.yml'] extra=[]"])
```
Exit 1. (A second, expected side effect: the `kind-roster-underclaim-detected` control also failed on this same scratch copy with `[]`, because its own fixture-vs-roster comparison converged once the roster itself permanently lacked the spine entry — this does not weaken the falsification, it demonstrates the SAME defect being caught by a second control.)

**check-version-stamps.py, flag typo:**
```
$ python3 scripts/check-version-stamps.py --decribe
usage: check-version-stamps.py [-h] [--self-test | --describe]
check-version-stamps.py: error: unrecognized arguments: --decribe
```
Exit 2 (was exit 0 before this task, running the live scan silently).

**gen-gate-docs.py, broken registry control (duplicated a `VAL-01` `GateEntry` in `_gate_registry.py`'s `ENTRIES`):**
```
gen-gate-docs: SELF-TEST FAIL [registry-self-test] — scripts/_gate_registry.py --self-test exited 1: _gate_registry: SELF-TEST FAIL [entries-count-matches-architecture-table] — len(documented ENTRIES)=32 != docs/ARCHITECTURE.md data rows=31
_gate_registry: SELF-TEST FAIL [no-gate-id-duplicated] — duplicate gate_id in ENTRIES: ['VAL-01', 'VAL-01', 'VAL-02', ...]
```
Exit 1 (also caught independently by `check-dispatch-wired`, `region-preserves-surrounding-prose`, `page-per-entry` and `check-reports-full-drift-count`, each reporting the new `SlugCollisionError` from `generate_all()`, since a duplicate key is also a duplicate slug). Before this task the same mutation left `--self-test`, `--check`, the battery and CI all green.

**gen-gate-docs.py, slug collision (appended a `GateEntry` with a distinct key `VAL:01` colliding on the rendered slug `VAL-01`):**
```
$ python3 scripts/gen-gate-docs.py --check
Traceback (most recent call last):
  ...
  File ".../scripts/gen-gate-docs.py", line 1632, in generate_all
    _assert_no_slug_collisions(_gate_registry.ENTRIES)
  File ".../scripts/gen-gate-docs.py", line 359, in _assert_no_slug_collisions
    raise SlugCollisionError(...)
SlugCollisionError: duplicate docs/gates/<slug>.md page slug(s): 'VAL-01' shared by ['VAL-01', 'VAL:01']
```
Exit 1. `docs/gates/` page count in the scratch copy: 31 before and after — confirming no page was silently deleted (the raise fires before any target is written).

## Before/After `--describe` Figures Moved Onto the Generated Surface

| Field | Script | Before | After |
|---|---|---|---|
| `control_count` / `control_ids` | `sync-content.py --describe` | 11 | 13 |
| `registered_surfaces` | `check-version-stamps.py --describe` | 2 (`first-principles/agents/**`, `first-principles/skills/**` — inverted) | 4 (`shared/skills/*/SKILL.md`, `shared/spine/SKILL.meta.yml`, `.claude-plugin/marketplace.json`, `first-principles/.claude-plugin/plugin.json`) |
| `control_count` / `control_ids` | `gen-gate-docs.py --describe` (backs CONF-SURFACE) | 51 | 53 |

`CLAUDE.md`'s DUAL-04 row `control_count`, VERSION-01 row `registered_surfaces`, and CONF-SURFACE row `control_count` all confirmed mechanically equal to their live `--describe` figures (see Verification Evidence).

## Verification Evidence

- `python3 scripts/sync-content.py --self-test` -> `sync-content.py --self-test: ALL PASS` (13/13 controls, including the new roster/executed floor and control (m))
- `python3 scripts/sync-content.py --check` -> exit 0
- `python3 scripts/check-version-stamps.py --self-test` -> `check-version-stamps --self-test: PASS (8 fixture trees, 16 named assertions)`
- `python3 scripts/check-version-stamps.py` (live leg) -> `check-version-stamps: 17 stamps, all '8.26.0'` / `PASS`
- `python3 scripts/check-version-stamps.py --decribe` -> exit 2
- `python3 scripts/_gate_registry.py --self-test` -> `_gate_registry: SELF-TEST PASS — 20 controls run`
- `python3 scripts/gen-gate-docs.py --self-test` -> `gen-gate-docs: SELF-TEST PASS — 53 controls run`
- `python3 scripts/gen-gate-docs.py --check` -> exit 0, `harvested 22/22 expected script-backed entries (22 total)`
- `bash scripts/check-firewall-battery.sh` -> `FIREWALL: GREEN (26/26)` (total unchanged)
- `python3 scripts/check-registration.py` -> `PASS (... 23/24 battery gates CI-registered + 1 battery-only by design)` — REG-GUARD's CI-job axis unchanged, no new battery-only exemptions
- `sh .githooks/pre-commit` -> exit 0; `sh scripts/git-hooks/pre-commit` -> exit 0
- `docs/gates/VERSION-01.md`'s Facts fence and hand-written narrative confirmed to name the same 4 walked source kinds by mechanical set-equality check (not by eye)
- `git diff -- scripts/sync-content.py` reviewed: contains no hunk altering any pre-existing control's assertion text or verdict — roster/floor change only

## Issues Encountered

- This worktree checkout had no `.planning/` plan/state files and no `.venv` (matching the note left by plan 21-13's executor) — copied `21-14-PLAN.md`, `21-13-SUMMARY.md`, `21-13-PLAN.md`, `21-VERIFICATION.md`, `21-CONTEXT.md`, `21-PATTERNS.md`, `PROJECT.md`, `STATE.md`, `config.json` from the main repo working tree, and ran `uv sync` to create `.venv` so VAL-03's pytest leg could resolve.
- The worktree's HEAD merge-base initially did not match the expected parent commit at agent start; corrected via `git reset --hard 55c139fb5a9523ffe41ca6c4f61e3d90263118a5` per the mandatory branch-check protocol before any work began.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- CR-02 (sync-content.py's inverted control roster) and CR-03 (check-version-stamps.py's inverted `registered_surfaces`) are both closed with executed/walked-vs-registered floors in both directions, each with a permanent registered negative-arm control.
- CR-06 (the orphaned `_gate_registry.py --self-test`) is closed: its 16 controls, including the sole duplicate-key check, now run in the battery, CI, and both pre-commit hooks via `gen-gate-docs.py`'s new `registry-self-test` control.
- T-21-14-02 (silent detail-page deletion on a duplicate slug) is closed structurally: `SlugCollisionError` fires at generation time, before any write.
- This closes the first half of GAP 2 (CONF-11's "live constants" promise on `sync-content.py` and `check-version-stamps.py`, plus the orphaned registry self-test). Any remaining CR-05 rosters (the six `--describe` rosters CONF-11's GAP 2 named as unfloored against execution, beyond these two scripts) are out of this plan's scope and remain for a future plan if prioritized.

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-07*

## Self-Check: PASSED

All 8 modified files confirmed present on disk; all 3 task commit hashes (`895504c`, `890dd1e`, `5a72c5a`) confirmed present in `git log --oneline --all`.
