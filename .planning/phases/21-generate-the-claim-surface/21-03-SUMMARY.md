---
phase: 21-generate-the-claim-surface
plan: 03
subsystem: tooling
tags: [gate-registry, describe, self-test, ci-gates]

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    plan: 02
    provides: "scripts/_gate_registry.py's GateEntry/ENTRIES, DESCRIBE_FIELD_VOCABULARY,
      field_resolution_problems()/vocabulary_problems() (D-04), registry_id_problems() (D-01)"
provides:
  - "7 working --describe limbs (sync-content.py, check-links.py,
    check-trigger-collisions.py, check-description-budget.py,
    check-version-stamps.py, check-install-collisions.py, check-agent.py),
    each emitting a flat, gate-agnostic, vocabulary-conformant JSON blob
    derived live from module-level constants (D-03)"
  - "check-agent.py's _CHECK_DESCRIPTIONS roster (D-21-J): GATE-01's
    published check count is len() of a roster the checker's own gating
    logic reads, not a hand-typed literal beside untouched inline code"
  - "3 new DESCRIBE_FIELD_VOCABULARY members (derived_counts,
    locked_constants, scoped_branches) with GateEntry.consumes wired for
    all 7 batch-A registry entries"
  - "_gate_registry.py's live D-04 floor control (d04-live-field-equality):
    subprocess-invokes every script ENTRIES declares a non-empty consumes
    against and asserts field_resolution_problems()/vocabulary_problems()
    are clean in both directions — derived from ENTRIES itself, so later
    batches (21-04/05) need no further self-test edits here"
affects: [21-04, 21-05, 21-06, 21-07, 21-11]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "describe() purity: reads module-level constants and (for
      check-trigger-collisions.py) one function signature default via
      inspect.signature — never disk I/O, matching D-03's explicit 'pure,
      no disk I/O' interface contract even where the plan's <action> prose
      gestured at a live population count"
    - "index-gated check roster (check-agent.py): each of Checks 2-8 is
      wrapped in `if IDX < len(_CHECK_DESCRIPTIONS):`, so shrinking the
      roster measurably disables the highest-numbered check — proven by
      scratch-copy mutation, not merely declared"
    - "subprocess-based live D-04 floor: _gate_registry.py shells out to
      each script's --describe (never a Python import, preserving D-21-A's
      'this module does not import the scripts it describes')"

key-files:
  created: []
  modified:
    - scripts/sync-content.py
    - scripts/check-links.py
    - scripts/check-trigger-collisions.py
    - scripts/check-description-budget.py
    - scripts/check-version-stamps.py
    - scripts/check-install-collisions.py
    - scripts/check-agent.py
    - scripts/_gate_registry.py

key-decisions:
  - "describe() purity took precedence over the plan's <action> prose
    where they conflicted: check-trigger-collisions.py's 'scanned-skill
    population' and check-version-stamps.py's 'stamp count' both
    naturally require live disk reads (iter_plugin_skills()/glob), which
    the binding <interfaces> contract ('pure: no disk I/O') forbids inside
    describe(). Resolved by deriving a structurally-equivalent PURE fact
    instead: check-trigger-collisions.py emits ngram_width via
    inspect.signature (no I/O); check-version-stamps.py emits
    stamp_source_kind_count from a new static _STAMP_SOURCE_KINDS roster
    (4 source KINDS the checker is configured to walk) rather than a live
    COUNT of discovered stamps. Recorded as Assumption Drift below."
  - "check-agent.py's roster gates Checks 2-8 uniformly by index
    (IDX < len(_CHECK_DESCRIPTIONS)); Check 1 (frontmatter-fence parse)
    stays unconditional because later checks cannot run without it. This
    means deleting ANY single roster entry disables the highest-numbered
    active check (not necessarily the deleted entry's own check) — a
    deliberate, simple, uniform design documented in-code rather than a
    per-check dispatch table."
  - "check-description-budget.py had zero --self-test before this plan;
    added the script's first self-test control (describe()/CAP
    consistency) rather than treating 'pre-change count 0' as exempting
    it from the plan's self-test requirement."

requirements-completed: [CONF-11]

# Metrics
duration: ~90min
completed: 2026-09-06
---

# Phase 21 Plan 03: Batch A --describe Limbs (D-03/D-21-A/D-21-J) Summary

**7 gate scripts (sync-content, check-links, check-trigger-collisions,
check-description-budget, check-version-stamps, check-install-collisions,
check-agent) gained a pure, vocabulary-conformant `--describe` JSON limb
derived live from module constants, plus check-agent.py's GATE-01 check
count is now `len()` of an extracted, index-gated roster rather than a
hand-typed "8".**

## Performance

- **Duration:** ~90 min
- **Tasks:** 2 (Task 1: six constant-reachable scripts; Task 2:
  check-agent.py's roster extraction + describe())
- **Files modified:** 8 (7 gate scripts + `scripts/_gate_registry.py`)

## Accomplishments

- All 7 batch-A scripts answer `--describe` with parseable JSON on stdout,
  exit 0.
- 3 new `DESCRIBE_FIELD_VOCABULARY` members added
  (`derived_counts`, `locked_constants`, `scoped_branches`), each with a
  written meaning comment; every field every script emits is a member.
- Every batch-A `GateEntry.consumes` tuple in `_gate_registry.py` is wired
  to exactly the fields that script's `describe()` emits — proven live by
  a new subprocess-based self-test control (`d04-live-field-equality`)
  that shells out to each script's real `--describe` leg (never a Python
  import — D-21-A) and asserts `field_resolution_problems()` /
  `vocabulary_problems()` report nothing in either direction. The script
  set is derived from `ENTRIES` itself, so batches 21-04/05 need no
  further edits to this control.
- `check-agent.py`'s `_CHECK_DESCRIPTIONS` roster is load-bearing, proven
  by scratch-copy mutation: deleting the roster's last entry drops
  `--describe`'s `branch_count` from 8 to 7 and disables Check 8, which
  the script's own `--self-test` then catches and fails on (exit 1) —
  demonstrating the roster is read by the checking logic, not a parallel
  list beside untouched inline code.
- `sync-content.py`'s `describe()` contains no gate-id branch (confirmed
  by grepping the function body, docstring excluded, for `DUAL-04`/
  `GATE-02`: zero matches) — one limb serves DUAL-04, GATE-02-v8.5 and the
  sync-drift pre-commit row.

## Self-test control counts (before -> after this plan)

| Script | Metric | Before | After |
|---|---|---|---|
| `sync-content.py` | lettered `cmd_self_test()` controls | 11 (a-k) | 12 (a-l) |
| `check-links.py` | `wrong.append()` assertion call sites | 16 | 17 |
| `check-trigger-collisions.py` | `_run_self_test()` `sys.exit(1)`-guarded assertions | 1 | 2 |
| `check-description-budget.py` | `--self-test` controls (script had none before) | 0 | 1 |
| `check-version-stamps.py` | named `expect()` assertions | 11 | 12 |
| `check-install-collisions.py` | `_run_self_test()` `sys.exit(1)`-guarded assertions | 3 | 4 |
| `check-agent.py` | fixture count (Task 2 — must be UNCHANGED, not risen) | 10 | 10 (unchanged) |

`check-agent.py` is the one exception to "rises": D-21-J's hard bound is
that the roster lift adds no checks and removes none, so its fixture count
(9 in `fixtures` + `fixture-i`) is required to stay identical, which it
does — confirmed by running `--self-test` on the pre-Task-2 commit (via
`git stash`) and diffing every fixture's reported failure count/message
against the post-Task-2 run: byte-identical.

## Derivation proved by mutation (constant -> emitted value moves)

- **`check-description-budget.py`** (scratch copy): `CAP = 2000 -> 1999`
  in source; `--describe`'s `locked_constants.cap` moved `2000 -> 1999`.
- **`check-version-stamps.py`** (scratch copy): inserted a fifth entry
  into `_STAMP_SOURCE_KINDS`; `--describe`'s
  `derived_counts.stamp_source_kind_count` moved `4 -> 5`.
- Both scratch-copy mutations confirmed via `rsync -a --exclude .git`
  copies under the scratchpad directory; `git status --porcelain` on the
  real repo was captured before and diffed clean after each mutation (no
  drift into the real tree).

## check-agent.py mutation arms (D-21-J behaviour-preservation proof)

All three run on a `rsync -a --exclude .git` scratch copy; real-tree
`git status --porcelain` confirmed unchanged before and after each:

1. **`maxTurns` 60 -> 20** in the scratch copy's shipped agent file:
   `python3 scripts/check-agent.py` (live leg) exits 1, observed output:
   `check-agent: FAIL — 'maxTurns' must be 60 (Phase 5 Self-Audit Gate
   budget headroom), got 20`.
2. **Strip `name:`** from the scratch copy's shipped agent file:
   the live leg still exits 1 and correctly fails, observed output:
   `check-agent: FAIL — frontmatter missing required key 'name'`. This is
   Check 2 catching it directly (Check 2 is unconditionally active since
   `n_checks == 8` is unchanged) — the input-file mutation does not reach
   `_assert_live_coverage()` because `_validate_agent_file()` returns
   before that call whenever `_check_agent_text()` already reports a
   failure. `_assert_live_coverage()`'s own teeth (catching a checker that
   has gone vacuous, as opposed to an input that is invalid) are what arm
   3 below exercises instead, via the roster itself.
3. **Delete the last entry** from `_CHECK_DESCRIPTIONS`: `--describe`'s
   `branch_count` drops `8 -> 7`; `python3 scripts/check-agent.py
   --self-test` now exits 1, observed output:
   `fixture-h (missing trigger phrase) failed for the WRONG reason
   (expected 'missing required trigger phrase', got: 'maxTurns' must be 60
   ..., got 30)` — proving Check 8 stopped running and the roster is
   load-bearing.

During this arm a real bug was found and fixed (Rule 1, see Deviations):
`describe()`'s `scoped_branches` computation indexed
`_SKIP_NAME_CHECK_SCOPED_INDICES` unconditionally, which raised
`IndexError` once the roster shrank below index 7. Fixed with a bounds
guard (`if i < len(_CHECK_DESCRIPTIONS)`) before the mutation test above
was re-run successfully.

## Task Commits

1. **Task 1: `--describe` for the six constant-reachable batch-A scripts** -
   `6a5dbe7` (feat)
2. **Task 2: `check-agent.py` roster extraction (D-21-J) + `--describe`** -
   `41f6e73` (feat)

**Plan metadata:** this commit (SUMMARY only — STATE/ROADMAP excluded per
worktree mode; the orchestrator owns those writes after the wave completes)

## Files Created/Modified

- `scripts/sync-content.py` — `_SELF_TEST_CONTROL_IDS`, `describe()`,
  `--describe` CLI flag, control (l) (mutation-proof)
- `scripts/check-links.py` — `describe()`, `--describe` CLI flag,
  describe()-consistency control appended to `_run_self_test()`
- `scripts/check-trigger-collisions.py` — `describe()` (ngram width via
  `inspect.signature`), `--describe` CLI flag, mutation-proof control
- `scripts/check-description-budget.py` — `describe()`, first-ever
  `self_test()`/`--self-test`, `--describe` CLI flag
- `scripts/check-version-stamps.py` — `_STAMP_SOURCE_KINDS`,
  `_EXCLUDED_GENERATED_GLOBS`, `describe()`, `--describe` CLI flag,
  control (h) (mutation-proof)
- `scripts/check-install-collisions.py` — `describe()`, `--describe` CLI
  flag, mutation-proof control appended to `_run_self_test()`
- `scripts/check-agent.py` — `_CHECK_DESCRIPTIONS`,
  `_SKIP_NAME_CHECK_SCOPED_INDICES`, index-gated `_check_agent_text()`,
  `describe()`, `--describe` CLI flag
- `scripts/_gate_registry.py` — 3 new `DESCRIBE_FIELD_VOCABULARY`
  members; `consumes` wired on VAL-03, VAL-04, VAL-05, VERSION-01,
  COLLIDE-01, DUAL-04 and GATE-01; `_control_live_requested_fields_vacuous_today`
  replaced with `_control_d04_live_field_equality` (subprocess-driven,
  derived script set)

## Decisions Made

- **describe() purity over action-prose literalism.** D-03's `<interfaces>`
  contract is explicit and binding: "pure: no disk I/O". Two scripts'
  `<action>` text asked for facts that structurally require a live
  directory read — `check-trigger-collisions.py`'s "scanned-skill
  population" (needs `iter_plugin_skills()`, a disk walk) and
  `check-version-stamps.py`'s "stamp count" (needs `collect_stamps()`'s
  own glob). Both were resolved by deriving a structurally-equivalent PURE
  fact instead of the literal live count — see Assumption Drift below.
- **check-install-collisions.py's "vacuous-when-monolith-absent" fact**
  is emitted as a `disclosed_bounds_anchors` identifier
  (`"vacuous-when-monolith-absent"`) rather than a live
  `MONOLITH_DIR.exists()` boolean, for the same purity reason —
  checking existence is disk I/O.
- **check-agent.py's uniform index-gating** (Checks 2-8 gated by
  `IDX < len(_CHECK_DESCRIPTIONS)`, Check 1 always active) was chosen
  over a per-check dispatch table for simplicity and because it still
  makes the roster provably load-bearing (arm 3), even though a single
  deletion always disables the highest-numbered *active* check rather
  than the specifically-deleted entry's own check. This is documented
  in-code on `_CHECK_DESCRIPTIONS`'s own comment block.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `describe()`'s `scoped_branches` crashed on a shrunk roster**
- **Found during:** Task 2, mutation arm 3 (deleting `_CHECK_DESCRIPTIONS`'s
  last entry on a scratch copy)
- **Issue:** `[_CHECK_DESCRIPTIONS[i] for i in _SKIP_NAME_CHECK_SCOPED_INDICES]`
  unconditionally indexed index 7 (Check 8's scoped-out marker), which
  raised `IndexError` once the roster shrank to length 7 — `describe()`
  crashed instead of reporting a shorter `branch_count`.
- **Fix:** Added a bounds guard: `if i < len(_CHECK_DESCRIPTIONS)` inside
  the list comprehension, so `scoped_branches` gracefully omits an
  out-of-range scoped index rather than crashing.
- **Files modified:** `scripts/check-agent.py`
- **Verification:** re-ran the scratch-copy mutation; `--describe` now
  reports `branch_count: 7` cleanly instead of raising.
- **Committed in:** `41f6e73` (part of Task 2's single commit; caught and
  fixed before the file was staged)

**Total deviations:** 1 auto-fixed (Rule 1 — bug found and fixed during
this plan's own required mutation-proof verification, before either task's
commit).

## Assumption Drift (advisory)

**1. describe() cannot emit a live-tree "population" or "count" fact —
   deriving a structurally-equivalent static fact instead.**
- **Found during:** Task 1, `check-trigger-collisions.py` and
  `check-version-stamps.py`
- **Planned:** the plan's `<action>` text for `check-trigger-collisions.py`
  asked for "the n-gram width and the scanned-skill population, derived";
  for `check-version-stamps.py`, "the stamp count as `len()` of whatever
  roster the checker walks."
- **Actual:** `check-trigger-collisions.py`'s `describe()` emits only
  `ngram_width` (via `inspect.signature(ngrams).parameters["n"].default`,
  no I/O) — "scanned-skill population" is omitted from the pure blob
  because it requires `iter_plugin_skills()`, a live directory walk.
  `check-version-stamps.py`'s `describe()` emits
  `stamp_source_kind_count` — `len()` of a new static
  `_STAMP_SOURCE_KINDS` tuple naming the 4 SOURCE KINDS the checker is
  configured to walk — rather than a live COUNT of stamps actually
  discovered on disk (which `collect_stamps()` computes via `glob`, disk
  I/O).
- **Why:** the plan's own `<interfaces>` section, which the plan states is
  "restated here so no executor has to go looking" and therefore binding,
  requires `describe()` to be "pure: no disk I/O, no argv, no subprocess."
  A live population/count read is disk I/O by construction. Where the
  interface contract and the action prose conflicted, the interface
  contract took precedence, and a structurally-equivalent static fact was
  substituted rather than silently dropping the field.

## Next Phase Readiness

- Batches 21-04/05's `--describe` limbs need no changes to
  `_gate_registry.py`'s live D-04 floor control — it derives its script
  set from `ENTRIES` itself.
- `DESCRIBE_FIELD_VOCABULARY` now carries 16 members (13 from 21-02 + 3
  added here); later batches should check this vocabulary before adding a
  new field name, since `derived_counts`/`locked_constants` cover most
  "a mapping of name -> scalar" needs already.
- No blockers. `git status --porcelain` in the real repo is clean after
  both task commits.

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-06*

## Self-Check: PASSED

- FOUND: `scripts/sync-content.py` (modified)
- FOUND: `scripts/check-links.py` (modified)
- FOUND: `scripts/check-trigger-collisions.py` (modified)
- FOUND: `scripts/check-description-budget.py` (modified)
- FOUND: `scripts/check-version-stamps.py` (modified)
- FOUND: `scripts/check-install-collisions.py` (modified)
- FOUND: `scripts/check-agent.py` (modified)
- FOUND: `scripts/_gate_registry.py` (modified)
- FOUND: commit `6a5dbe7` (`git log --oneline --all`)
- FOUND: commit `41f6e73` (`git log --oneline --all`)
