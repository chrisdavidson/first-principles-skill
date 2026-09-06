---
phase: 21-generate-the-claim-surface
plan: 02
subsystem: infra
tags: [ci, gates, registry, dataclasses, drift-guard, self-test]

# Dependency graph
requires:
  - phase: 20-live-conformance
    provides: set-equality-never-subset floor precedent (20-D-07), the
      discretion-with-evidence handling this phase's decisions of record reuse
provides:
  - "scripts/_gate_registry.py: GateEntry frozen dataclass, ENTRIES (28 entries:
    27 documented gate/pre-commit rows + the anticipatory CONF-SURFACE entry)"
  - "battery_gate_ids() / registry_id_problems(): D-01's bidirectional
    equality floor against scripts/check-firewall-battery.sh's own
    gate/gate_prereq registrations"
  - "DESCRIBE_FIELD_VOCABULARY / field_resolution_problems() /
    vocabulary_problems(): D-04's bidirectional field-resolution floor and
    the closed --describe field-name vocabulary batch plans 21-03/04/05
    implement against"
  - "--self-test (16 controls) and --describe (JSON) CLI, in this repo's
    _CONTROLS/_CONTROL_IDS house style"
affects: [21-03, 21-04, 21-05, 21-06, 21-07, 21-11]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "frozen dataclass registry with a derived (regex-extracted) equality
      floor against a second source of truth, never a hand-retyped roster
      (D-21-K's explicit deferral of a second-transcription lock to Phase 22)"
    - "bidirectional set-difference floor reported in one run (both
      missing= and extra=/unconsumed= in the same failure list), matching
      the SCAN-GUARD/CONF-GATE _roster_problems / _LIVE_CALL_SITES_LOCK shape"

key-files:
  created: [scripts/_gate_registry.py]
  modified: []

key-decisions:
  - "Two _gate_registry.py bugs found and fixed during Task 1/2 verification
    (see Deviations): the initial registry_id_problems() 'leaked precommit
    id' check was backwards and always fired; INVARIANT-CHECK/FROZEN-EVIDENCE
    needed the same battery-floor exclusion as the pre-commit rows because
    they are inline checks the gate()/gate_prereq() regex structurally
    cannot see."
  - "The len(ENTRIES) vacuity control compares against docs/ARCHITECTURE.md's
    27 parsed data rows MINUS the one anticipatory CONF-SURFACE entry
    (D-21-C), rather than against len(ENTRIES) directly — CONF-SURFACE is
    deliberately ahead of its own documentation and is named via
    _ANTICIPATORY_KEYS so this is a derived exclusion, not a silent one."

patterns-established:
  - "Anticipatory registry entries (not yet battery/CI/table-registered) are
    named in a frozen exclusion set (_ANTICIPATORY_KEYS) rather than left
    out of ENTRIES entirely, so the registry can describe its own future
    drift gate the moment its script exists (D-08's self-description
    uniformity, applied reflexively) without breaking the live equality
    floors that run today."

requirements-completed: [CONF-11]

# Metrics
duration: ~15min
completed: 2026-09-06
---

# Phase 21 Plan 02: Gate Registry (D-01 battery-id floor + D-04 field floor) Summary

**`scripts/_gate_registry.py` — a 28-entry frozen-dataclass gate registry with two live,
mutation-proven equality floors: D-01 (registry ids vs. the battery's own regex-derived
`gate`/`gate_prereq` registrations) and D-04 (bidirectional `--describe` field
request/emission), plus the closed `DESCRIBE_FIELD_VOCABULARY` batch plans 21-03/04/05
extend.**

## Performance

- **Duration:** ~15 min
- **Started:** ~2026-09-06T17:06:00Z (session start, estimated from worktree mtime)
- **Completed:** 2026-09-06T17:16:57Z
- **Tasks:** 2 (both landed in one commit — the file was designed and built as one
  coherent module; see Task Commits)
- **Files modified:** 1 created

## Accomplishments

- `scripts/_gate_registry.py` created with `GateEntry` (frozen dataclass) and `ENTRIES`
  (28 entries: one per row in `docs/ARCHITECTURE.md`'s 27-row "CI and pre-commit gate
  inventory" table, plus the anticipatory `CONF-SURFACE` entry D-21-C requires ahead of
  its own registration).
- D-01's battery-id equality floor (`battery_gate_ids()` + `registry_id_problems()`) is
  green live against the real `scripts/check-firewall-battery.sh` and is proven by
  mutation: an `rsync --exclude .git` scratch copy with one real `gate "CONF-GATE" ...`
  block deleted fails `--self-test` naming `CONF-GATE` by id; the real repo tree was
  confirmed clean (`git status --porcelain`) before and after the scratch mutation.
- D-04's bidirectional field-resolution floor (`field_resolution_problems()`) and the
  closed `DESCRIBE_FIELD_VOCABULARY` (13 named fields, each with a written
  contract comment in `_FIELD_DESCRIPTIONS`) plus `vocabulary_problems()` for
  out-of-vocabulary emissions.
- `--self-test` runs 16 named controls in the `_CONTROLS`/`_CONTROL_IDS` house style
  (coverage floor included); `--describe` emits parseable JSON
  (`python3 scripts/_gate_registry.py --describe | python3 -m json.tool` exits 0).
- Neutralization proof for `d04-both-directions-in-one-run`: commenting out the
  unconsumed-field loop in a scratch copy of the module causes that control to fail,
  reporting only the missing-field problem (`branch_count`) instead of both — confirming
  the control genuinely exercises both directions rather than one direction alone.

## Task Commits

Both tasks (registry entries + D-01 floor, and D-04 floor + field vocabulary) were
designed and implemented together as one coherent new module and landed in a single
commit — the D-04 floor's `field_resolution_problems()` and vocabulary machinery use the
same `ENTRIES`/`GateEntry` structures Task 1 defines, so splitting the file into two
partial commits would have left the intermediate commit's `--self-test` failing (Task 1
alone has no D-04 controls to run against, but the coverage-floor arm would still expect
them once `_CONTROL_IDS` is populated). Both tasks' acceptance criteria were verified
independently before committing (see below).

1. **Task 1 + Task 2: Gate registry, D-01 battery-id floor, D-04 field floor** -
   `0ba2ab1` (feat)

**Plan metadata:** this commit (SUMMARY + STATE/ROADMAP excluded per worktree mode)

## Files Created/Modified

- `scripts/_gate_registry.py` - `GateEntry` frozen dataclass; `ENTRIES` (28 rows);
  `battery_gate_ids()`/`registry_id_problems()` (D-01); `DESCRIBE_FIELD_VOCABULARY`/
  `field_resolution_problems()`/`vocabulary_problems()` (D-04); `describe()`;
  `self_test()`/`main()` CLI (`--self-test`, `--describe`)

## Decisions Made

- **CONF-SURFACE is added now, per D-21-C, but excluded from the two live-equality
  floors via `_ANTICIPATORY_KEYS`.** The plan's Task 1 action explicitly requires adding
  a placeholder-free `CONF-SURFACE` entry ahead of its own script/battery/CI/table
  registration; the plan's own acceptance criterion also requires
  `len(ENTRIES) == docs/ARCHITECTURE.md`'s parsed row count. Both are satisfied by
  scoping the vacuity control to "documented" entries (`ENTRIES` minus
  `_ANTICIPATORY_KEYS`) — `len(documented) == 27` (parsed live) and
  `len(ENTRIES) == 27 + 1` (derived, not asserted as a bare literal). This resolves an
  implicit tension between the plan's Task 1 action (add CONF-SURFACE now) and its
  acceptance criterion (entries count must equal the CURRENT table's row count) in favor
  of both being true under an explicit, named exclusion rather than silently picking one
  and breaking the other.
- **INVARIANT-CHECK and FROZEN-EVIDENCE are excluded from the D-01 battery-id equality
  floor**, alongside the two pre-commit rows, via the same `precommit_ids` parameter
  (`registry_id_problems`'s third argument). These two ids are real battery-tallied rows
  documented in `docs/ARCHITECTURE.md`, but they increment the battery's PASS/FAIL/TOTAL
  tally through bespoke inline bash blocks, never through a `gate "<ID>"` /
  `gate_prereq "<ID>"` call — `battery_gate_ids()`'s regex structurally cannot see them,
  so leaving them un-excluded would make the floor report both as a permanent phantom
  `extra=` (this was in fact the second bug found during verification; see Deviations).
  The parameter name stays `precommit_ids` per the plan's own `<interfaces>` contract;
  its docstring documents the broadened real-world membership.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `registry_id_problems()`'s pre-commit-exclusion check was inverted**
- **Found during:** Task 1 (running `--self-test` for the first time)
- **Issue:** The first draft added a "leaked precommit id" pre-check
  (`entry_ids & precommit_ids`) intended to catch a caller that forgot to exclude
  pre-commit keys — but it fired whenever `precommit_ids` correctly named an id already
  present in `entry_ids`, which is the NORMAL, correct case, not an error. This made the
  `d01-precommit-excluded` control fail even though the exclusion logic below it
  (`comparable = entry_ids - precommit_ids`) was itself correct.
- **Fix:** Removed the inverted pre-check entirely; `registry_id_problems()` now only
  computes `comparable = entry_ids - precommit_ids` and compares that against
  `derived_ids`, matching the documented "excluded by construction" behavior.
- **Files modified:** `scripts/_gate_registry.py`
- **Verification:** `python3 scripts/_gate_registry.py --self-test` — `d01-precommit-excluded`
  now passes, and its own second assertion (verifying the SAME registry set without the
  exclusion produces exactly one `extra=` problem) confirms the exclusion is
  load-bearing, not a no-op.
- **Committed in:** `0ba2ab1` (part of the single task commit; caught and fixed before
  the file was staged)

**2. [Rule 1 - Bug] `_registry_entry_ids()` did not exclude the two truly-inline battery
checks from the live D-01 floor**
- **Found during:** Task 1 (running the live-equality control for the first time)
- **Issue:** `INVARIANT-CHECK` and `FROZEN-EVIDENCE` are real, documented battery rows
  with `gate_id` set, so the first draft's `_registry_entry_ids()` included them in the
  comparison set. But `scripts/check-firewall-battery.sh` increments their PASS/FAIL/TOTAL
  tally through bespoke inline bash (an inline `python3 - <<'PYEOF'` block and a
  `git diff --quiet` check, respectively), never through a `gate "<ID>"` /
  `gate_prereq "<ID>"` call — so `battery_gate_ids()`'s regex, which is scoped precisely
  to those two call forms, can never see either id. The live floor reported both as a
  permanent phantom `extra=`.
- **Fix:** `_registry_precommit_ids()` (the helper supplying `registry_id_problems()`'s
  third argument) now returns the two pre-commit mechanism keys UNION
  `{"INVARIANT-CHECK", "FROZEN-EVIDENCE"}`, with an expanded docstring explaining why —
  this is a real, structural exclusion (the regex cannot see these two ids by
  construction), not a workaround.
- **Files modified:** `scripts/_gate_registry.py`
- **Verification:** `python3 scripts/_gate_registry.py --self-test` — `d01-live-battery-equality`
  passes; `bash scripts/check-firewall-battery.sh` confirms both ids are still real,
  passing battery rows (`[PASS] INVARIANT-CHECK`, `[PASS] FROZEN-EVIDENCE`), so the
  exclusion is scoped to the comparison mechanics, not a claim that these gates don't
  exist.
- **Committed in:** `0ba2ab1` (part of the single task commit; caught and fixed before
  the file was staged)

---

**Total deviations:** 2 auto-fixed (both Rule 1 — bugs found and fixed during the plan's
own required self-test/live-equality verification, before the file was ever committed).
**Impact on plan:** Both fixes were necessary for the D-01 floor to be genuinely green
(not vacuously green) against the real tree. No scope creep — both stayed inside
`scripts/_gate_registry.py`, the single file this plan creates.

## Issues Encountered

- `bash scripts/check-firewall-battery.sh` reports `FIREWALL: BLOCKED (1 prerequisite(s)
  unmet; 24/25 passed)` in this worktree, not `GREEN 25/25` — confirmed this is a
  pre-existing environment condition (`VAL-03`'s pytest-capable interpreter is not
  resolvable in this worktree: neither `.venv/bin/python3` nor `python3` can `import
  pytest`), unrelated to this plan's change. `scripts/_gate_registry.py` is not yet
  referenced anywhere in the battery, CI, or generator — it is a new, currently-inert
  file — so it cannot itself have caused a battery-outcome change, and all 24 gates that
  do run report `[PASS]` with zero `[FAIL]` lines, including `QUAL-01` (whose self-test
  covers the three CONTRACT-06 sha256 pins). This is recorded here as observed-not-fixed
  per the plan's non-goal ("this is a documentation-source change, not a gate-behaviour
  change") — installing pytest is out of this plan's scope and would be a Rule-3
  package-manager action requiring the blocking-human checkpoint protocol, not warranted
  for a pre-existing, unrelated environment gap.

## Next Phase Readiness

- `scripts/_gate_registry.py`'s exported interface (`ENTRIES`, `GateEntry`,
  `battery_gate_ids`, `registry_id_problems`, `field_resolution_problems`,
  `DESCRIBE_FIELD_VOCABULARY`, `self_test`, `main`) matches the `<interfaces>` contract
  this plan's frontmatter declares, so plans 21-03/04/05 (the `--describe` limb batches)
  and 21-06/07 (the generator) have a stable module to import against.
- Every `GateEntry.consumes` is currently empty (pinned by the
  `live-requested-fields-vacuous-today` control) — no script has a `--describe` limb yet,
  so `field_resolution_problems()` is vacuously green today. This is the expected
  starting state per D-03/D-04; the first batch plan that adds a `--describe` limb and a
  matching `consumes` entry will be the first real exercise of the D-04 floor outside its
  own self-test.
- `DESCRIBE_FIELD_VOCABULARY` currently carries the 13 seed field names named in this
  plan's own `<action>` text (`control_ids`, `control_count`, `branch_roster`,
  `branch_count`, `registered_surfaces`, `population_floors`, `call_site_census`,
  `scan_globs`, `frozen_paths`, `disclosed_bounds_anchors`, `checked_files`,
  `self_test_dispatch_anchors`, `run_commands`) — batch plans extend `_FIELD_DESCRIPTIONS`
  in the same commit as the limb that emits a new name, per this module's own
  documented convention.
- No blockers. `git status --porcelain` in the real repo shows only the tracked commit;
  no stray scratch/temp files remain (confirmed after the mutation-verification cleanup).

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-06*

## Self-Check: PASSED

- FOUND: `scripts/_gate_registry.py`
- FOUND: `.planning/phases/21-generate-the-claim-surface/21-02-SUMMARY.md`
- FOUND: commit `0ba2ab1` (`git log --oneline --all`)
