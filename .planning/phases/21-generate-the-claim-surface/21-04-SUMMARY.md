---
phase: 21-generate-the-claim-surface
plan: 04
subsystem: tooling
tags: [gate-registry, describe, self-test, ci-gates, harness, batt-06, step0-08, reg-guard]

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    plan: 03
    provides: "scripts/_gate_registry.py's GateEntry/ENTRIES, DESCRIBE_FIELD_VOCABULARY,
      field_resolution_problems()/vocabulary_problems() (D-04), registry_id_problems() (D-01),
      the live D-04 floor control (d04-live-field-equality) that derives its script set from
      ENTRIES itself"
provides:
  - "7 working --describe limbs (check-act-limb.py, check-loop-closure.py,
    check-focused-parity.py, check-high-confidence-bound.py, check-registration.py,
    check-routing-battery.py, check-step0-emulator.py), each emitting a flat,
    gate-agnostic, vocabulary-conformant JSON blob derived live from module-level
    constants (D-03)"
  - "_battery_core.py's RR_SENTINEL_IDS: the 11 RR-* residual sentinel ids
    CLAUDE.md's ownership map documents, lifted from prose to an enumerable
    roster (D-21-J), proved load-bearing by scratch-copy removal"
  - "check-registration.py's _CONTROL_IDS + _executed coverage floor (D-21-J):
    the 29 numbered self-test controls are now a second, independently-typed
    transcription cross-checked against what actually ran"
  - "check-high-confidence-bound.py's _EXCEPTIONS_ROSTER (D-21-J): HC-16's
    hardcoded EXCEPT-count literal is now len(_EXCEPTIONS_ROSTER), which is
    what makes the roster load-bearing rather than a parallel list"
  - "check-step0-emulator.py's SEMGATE02_OVERLAP_PAIRS (D-21-J): the 6
    documented semantic-overlap pairs, lifted from inline fixture ids"
  - "check-routing-battery.py's stdout-capture RR-* coverage cross-check
    (D-21-J): self_test() now asserts bidirectionally that every id in
    RR_SENTINEL_IDS fired and every fired RR-* id is in the roster"
  - "5 new consumes wirings in _gate_registry.py (HARN-01, HARN-02, HARN-03,
    HC-BOUND, REG-GUARD) plus 2 more (BATT-06, STEP0-08) — all against
    pre-existing DESCRIBE_FIELD_VOCABULARY members from batch A, no new
    vocabulary needed"
affects: [21-05, 21-06, 21-07, 21-11]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "describe() purity: reads module-level constants only, never disk I/O
      or subprocess — matching D-03's binding 'pure, no disk I/O' contract
      even where a live population count would have been more literal"
    - "coverage-floor roster lift (D-21-J): where a script had no existing
      enumerable roster backing its published count (check-act-limb.py's
      76 fixture labels, check-loop-closure.py's 37 N-ids, check-registration.py's
      29 numbered controls), the labels were lifted to a module-level
      constant and cross-checked against what the self-test actually ran —
      the same shape scripts/_gate_registry.py's own self_test() uses for
      _CONTROLS/_CONTROL_IDS"
    - "stdout-capture cross-check (check-routing-battery.py): where the
      RR-* sentinel assertions live 800+ lines deep inside
      self_test_boundary()/self_test_focused() with no roster to hang a
      limb on, self_test() captures their stdout (while still printing it,
      unchanged) and regex-scans it for line-leading RR-* ids, bidirectionally
      cross-checked against _battery_core.py's new RR_SENTINEL_IDS — this
      avoids touching the byte-frozen sentinel logic at all"
    - "derived-not-hardcoded distribution check: check-high-confidence-bound.py's
      HC-16 (EXCEPT: token distribution) now derives its expected total from
      len(_EXCEPTIONS_ROSTER) instead of a hardcoded '3' — this is what makes
      the roster load-bearing (shrinking it now fails HC-16 by name) rather
      than a parallel list the checking logic never reads"

key-files:
  created: []
  modified:
    - scripts/check-act-limb.py
    - scripts/check-loop-closure.py
    - scripts/check-focused-parity.py
    - scripts/check-high-confidence-bound.py
    - scripts/check-registration.py
    - scripts/check-routing-battery.py
    - scripts/check-step0-emulator.py
    - scripts/_battery_core.py
    - scripts/_gate_registry.py

key-decisions:
  - "check-act-limb.py's REQUIRED_BRANCHES (16 branches) was already a
    near-module-level literal (defined inside _run_self_test as a local) —
    lifted to true module scope with no behavior change. Its 76 fixture
    labels (a-bv, positive controls, module checks) had no roster at all;
    added _CONTROL_IDS as a hand-authored-once tuple plus a
    describe()-consistency self-test control, per the plan's own D-21-J
    'if no roster exists, lift it' instruction — scoped to the two
    mutation-proof arms the plan's acceptance criteria actually names
    (EXPECTED_STUB_COUNT, EXCEPT roster), not a fabricated third arm for
    this script."
  - "check-loop-closure.py's negative_controls table stays LOCAL (its
    thunks close over live file text describe() must never read); a
    module-level _CONTROL_ROSTER names the same 37 N-ids by source file,
    and a new self-test control asserts the ids the live table actually
    built match the roster by set equality."
  - "check-high-confidence-bound.py's HC-16 EXCEPT-distribution check was
    widened (not merely read) to derive its 'expect N' total from
    len(_EXCEPTIONS_ROSTER) rather than the literal 3 — this was necessary,
    not optional: without it, the mutation-proof arm's first attempt (roster
    shrunk, live gate still exits 0) demonstrated the roster was a parallel
    list. See Deviations below."
  - "check-routing-battery.py's RR-* coverage check is stdout-capture-based,
    not code-instrumented — self_test_boundary()/self_test_focused() are
    800+ lines of byte-sensitive sentinel logic (11 named RR-* assertions
    with frozen excerpt lineage) that the plan explicitly forbids touching
    ('sentinel logic and every frozen excerpt untouched'). The regex is
    line-start anchored (not a bare substring scan) to avoid false positives
    from supersession-chain PROVENANCE mentions inside other sentinels' own
    messages (e.g. 'Chain: RR-79-02 -> RR-92-01 -> ... -> RR-114-01') — see
    Deviations below. RR-108-03, a distinct frozen legacy sentinel for the
    retired decompose technique not listed in CLAUDE.md's 11-entry ownership
    map, is named and exempted rather than silently absorbed into the
    roster or silently masked by the scan."
  - "check-registration.py's 29 numbered self-test controls had no roster;
    inserted one _executed.append('cN') call per control block (mechanically
    derived from the existing '# Control N' comment positions) plus a
    module-level _CONTROL_IDS = tuple(f'c{n}' for n in range(1,30)) and an
    end-of-run coverage floor, matching _gate_registry.py's own
    self_test()/_CONTROL_IDS shape."

requirements-completed: [CONF-11]

# Metrics
duration: ~3h (across two turns; first turn ended at an API timeout with
  five scripts' work uncommitted but intact)
completed: 2026-09-06
---

# Phase 21 Plan 04: Batch B --describe Limbs (Harness/Registration/Measurement Gates) Summary

**All 7 batch-B gate scripts (HARN-01/02/03, HC-BOUND, REG-GUARD, BATT-06,
STEP0-08) gained a pure, vocabulary-conformant `--describe` JSON limb derived
live from module constants; three scripts (check-act-limb.py,
check-loop-closure.py, check-registration.py) had no existing roster backing
their published branch/control counts and gained one via D-21-J extraction;
check-high-confidence-bound.py's EXCEPT-distribution check was widened to
derive its total from the new roster rather than a hardcoded literal, which
is what makes that roster load-bearing; check-routing-battery.py's RR-*
sentinel coverage is proved via a stdout-capture cross-check that never
touches the byte-frozen sentinel logic underneath.**

## Performance

- **Duration:** ~3h across two turns (an API timeout ended the first turn
  with five scripts' `describe()` work complete but uncommitted; nothing
  was lost — verified and committed incrementally in the second turn)
- **Tasks:** 2 (Task 1: check-act-limb.py, check-loop-closure.py,
  check-focused-parity.py, check-high-confidence-bound.py; Task 2:
  check-registration.py, check-routing-battery.py, check-step0-emulator.py,
  plus `scripts/_battery_core.py`)
- **Files modified:** 9 (7 gate scripts + `scripts/_battery_core.py` +
  `scripts/_gate_registry.py`)

## Accomplishments

- All 7 batch-B scripts answer `--describe` with parseable JSON on stdout,
  exit 0.
- No new `DESCRIBE_FIELD_VOCABULARY` members were needed — all fields these
  7 limbs emit (`branch_roster`, `branch_count`, `control_ids`,
  `control_count`, `checked_files`, `disclosed_bounds_anchors`,
  `registered_surfaces`, `locked_constants`, `derived_counts`) were already
  declared by batch A (21-03).
- `scripts/_gate_registry.py`'s live D-04 floor (`d04-live-field-equality`)
  passes both directions for all 7 batch-B scripts — no `--self-test` edits
  to `_gate_registry.py` itself were required beyond wiring the 7 `consumes`
  tuples; the live floor derives its script set from `ENTRIES` itself.
- `bash scripts/check-firewall-battery.sh` reports **FIREWALL: GREEN
  (25/25)** after every change in this plan, confirmed by running the full
  battery (with `uv sync`'s `.venv` providing the pytest-capable interpreter
  VAL-03's third leg needs).
- `git diff --stat -- tests/` is empty throughout — no `_FROZEN_PATHS`
  member was touched.

## Roster lifts and their load-bearing proofs (D-21-J)

| Script | Roster added | Where it lives | Load-bearing proof |
|---|---|---|---|
| `check-act-limb.py` | `REQUIRED_BRANCHES` (16, moved from local to module scope), `_CONTROL_IDS` (76, new) | module-level | `--self-test`'s existing 16-branch anti-masking assertion is unchanged behavior; new `describe()`-consistency control cross-checks both against live state |
| `check-loop-closure.py` | `_CONTROL_ROSTER` (37 N-ids + source file, new) | module-level (the mutating `negative_controls` table stays local — its thunks close over live file text) | new self-test control asserts the roster's id set equals the ids the local table actually built and ran, by set equality |
| `check-focused-parity.py` | none needed — `EXPECTED_STUB_COUNT` and `_ANCHOR_CONTROL_EXEMPT` were already module constants | pre-existing | **Mutation arm run** (scratch copy): `EXPECTED_STUB_COUNT` 13→12 moves `--describe`'s `locked_constants.expected_stub_count` 13→12 |
| `check-high-confidence-bound.py` | `_EXCEPTIONS_ROSTER` (3, moved from a local inside `_check_exceptions_summary` to module scope); HC-16 widened to derive its total from `len(_EXCEPTIONS_ROSTER)` | module-level | **Mutation arm run** (scratch copy): removing entry `(c)` drops `--describe`'s `except_exception_count` 3→2 AND the live gate now fails: `HC-16: EXCEPT distribution incorrect: total=3 (expect 2)` for both rubric surfaces |
| `check-registration.py` | `_CONTROL_IDS` (29, `range(1,30)`-derived) + `_executed` coverage floor (new) | module-level | coverage floor: any control block skipped/deleted (no matching `_executed.append`) fails `--self-test` by name at the end-of-run set-equality check |
| `check-routing-battery.py` / `_battery_core.py` | `RR_SENTINEL_IDS` (11, new, in `_battery_core.py`) | module-level, sentinel logic untouched | **Mutation arm run** (scratch copy): removing `RR-77-08` from the roster drops `--describe`'s `rr_sentinel_count` 11→10 AND `--self-test` fails: `RR-* sentinel(s) fired in captured output but no longer covered by RR_SENTINEL_IDS: ['RR-77-08']` |
| `check-step0-emulator.py` | `SEMGATE02_OVERLAP_PAIRS` (6, new) | module-level | new `describe()`-consistency self-test control (no dedicated mutation arm required by this plan's acceptance criteria) |

## Self-test control counts (before -> after this plan)

| Script | Metric | Before | After |
|---|---|---|---|
| `check-act-limb.py` | named controls (a-bv + coh/cov/m) | 75 | 76 (`(describe)` added) |
| `check-loop-closure.py` | reported control lines | not asserted as a magic number (docstring's own stated policy) | +1 (`describe()`-consistency) |
| `check-focused-parity.py` | `_problems`-tracked controls | ~46 | ~47 (`(describe)` added) |
| `check-high-confidence-bound.py` | "Controls run: N" | 19 | 20 |
| `check-registration.py` | numbered controls | 29 (unenumerated before) | 29 (now a coverage-floored roster; describe consistency implicit in the floor itself) |
| `check-routing-battery.py` | fixture/named-assertion count | 20 fixtures + 14 named RR-*/SEMGATE assertions | +1 (`RR-* sentinel coverage: PASS`) |
| `check-step0-emulator.py` | "41 fixtures + ... named assertions" | 41 fixtures + 14 named | +1 (`describe()`-consistency) |

`_gate_registry.py --self-test` itself is unchanged at 16 controls (per
21-03's design: the live D-04 floor derives its script set from `ENTRIES`,
so later batches need no further self-test edits there).

## BATTERY_ONLY_GATE_IDS verbatim live value

`frozenset({"QUAL-01"})` — unchanged. Recorded here verbatim for plan 21-11,
which depends on knowing whether this set is still a single member.

## Task Commits

1. **`check-act-limb.py` (HARN-01)** — `c88821d` (feat)
2. **`check-loop-closure.py` (HARN-02)** — `0be3fb7` (feat)
3. **`check-focused-parity.py` (HARN-03)** — `273733b` (feat)
4. **`check-high-confidence-bound.py` (HC-BOUND)** — `65b62cd` (feat)
5. **`check-registration.py` (REG-GUARD)** — `bafedca` (feat)
6. **`_gate_registry.py` wiring (Task 1's 5 entries)** — `5a7b3aa` (feat)
7. **`check-routing-battery.py` + `_battery_core.py` (BATT-06)** — `69a7d7b` (feat)
8. **`check-step0-emulator.py` (STEP0-08)** — `33e4ff2` (feat)
9. **`_gate_registry.py` wiring (BATT-06/STEP0-08)** — `7ea5281` (feat)

**Plan metadata:** this commit (SUMMARY only — STATE/ROADMAP excluded per
worktree mode; the orchestrator owns those writes after the wave completes)

## Files Created/Modified

- `scripts/check-act-limb.py` — `REQUIRED_BRANCHES` (lifted to module
  scope), `_CONTROL_IDS`, `describe()`, `--describe` CLI flag,
  `(describe)`-consistency control
- `scripts/check-loop-closure.py` — `_CONTROL_ROSTER`, `describe()`,
  `--describe` CLI flag, `describe()`-consistency control
- `scripts/check-focused-parity.py` — `describe()`, `--describe` CLI flag,
  `(describe)`-consistency control
- `scripts/check-high-confidence-bound.py` — `_EXCEPTIONS_ROSTER` (lifted
  from a local), HC-16 widened to derive its total from the roster,
  `describe()`, `--describe` CLI flag, `(describe)`-consistency control
- `scripts/check-registration.py` — `_CONTROL_IDS`, `_executed` tracking +
  coverage floor threaded through the 29 numbered controls, `describe()`,
  `--describe` CLI flag
- `scripts/check-routing-battery.py` — `describe()`, `--describe` CLI flag,
  stdout-capture RR-* bidirectional coverage cross-check in `self_test()`
- `scripts/_battery_core.py` — `RR_SENTINEL_IDS` (new module-level roster;
  no sentinel logic or frozen excerpt touched)
- `scripts/check-step0-emulator.py` — `SEMGATE02_OVERLAP_PAIRS`,
  `describe()`, `--describe` CLI flag, `describe()`-consistency control
- `scripts/_gate_registry.py` — `consumes` wired on HARN-01, HARN-02,
  HARN-03, HC-BOUND, REG-GUARD, BATT-06, STEP0-08 (7 entries; no new
  `DESCRIBE_FIELD_VOCABULARY` members required)

## Decisions Made

See `key-decisions` in frontmatter — summarized: (1) roster lifts follow
D-21-J's "if no roster exists, lift enumeration to a module constant,
changing no verdict" instruction, scoped narrowly to what each script's
checking logic can actually be made to read; (2) check-high-confidence-bound.py's
HC-16 widening was necessary (not optional) to make the roster load-bearing,
discovered during the mutation-proof arm itself; (3) check-routing-battery.py's
RR-* coverage uses stdout capture + regex, not code instrumentation, because
the plan explicitly forbids touching the sentinel logic underneath; (4)
check-registration.py's 29-control coverage floor mirrors
`_gate_registry.py`'s own `_CONTROLS`/`_CONTROL_IDS` shape.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] check-routing-battery.py's naive RR-* regex scan produced false "extra" findings from supersession-chain provenance text**
- **Found during:** Task 2, first `--self-test` run after adding the
  bidirectional RR-* coverage check
- **Issue:** A bare `RR-\d+-\d+` substring scan over the captured self-test
  output also matched retired predecessor ids inside OTHER sentinels' own
  lineage prose (e.g. `RR-114-01`'s message states "Chain: RR-79-02 ->
  RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01"), which are not
  themselves assertions. This produced ten phantom "extra" ids and a false
  self-test failure on the unmutated tree.
- **Fix:** Anchored the regex to line-start (`^\s*(RR-\d+-\d+)\s`,
  MULTILINE) — every real sentinel assertion leads its own printed line
  (`  RR-80-01 PASS: ...`), so this excludes mid-sentence provenance
  mentions while still catching every genuine assertion.
- **Files modified:** `scripts/check-routing-battery.py`
- **Verification:** re-ran `--self-test` on the real tree: `RR-* sentinel
  coverage: PASS (11 sentinels agree)`.
- **Committed in:** `69a7d7b` (part of the BATT-06 commit; caught and fixed
  before the file was staged)

**2. [Rule 1 - Bug] RR-108-03 (a distinct, non-roster legacy sentinel) still triggered a false "extra" finding after the line-start fix**
- **Found during:** Task 2, same `--self-test` run, after fix #1
- **Issue:** `RR-108-03` (S-P09 decompose, frozen at v7.4 since the
  technique was retired at Phase 111) leads its own `PASS` line exactly
  like the 11 tracked sentinels, but CLAUDE.md's "Step 0 residual sentinels
  (RR-* ownership map)" — the source this plan derives `RR_SENTINEL_IDS`
  from — does not list it. It is a real, intentionally-different id, not a
  detection defect.
- **Fix:** Named `_RR_FIRED_EXEMPT = frozenset({"RR-108-03"})` with a
  comment explaining why, and excluded it from the "extra" comparison
  explicitly rather than silently widening the roster or the regex to
  absorb it.
- **Files modified:** `scripts/check-routing-battery.py`
- **Verification:** `--self-test` PASS with the exemption; the mutation-proof
  arm (removing `RR-77-08`) still correctly fails naming only `RR-77-08`,
  confirming the exemption doesn't mask a genuine roster gap.
- **Committed in:** `69a7d7b`

**3. [Rule 1 - Bug] check-high-confidence-bound.py's roster lift was initially not load-bearing**
- **Found during:** Task 1, running the required EXCEPT-roster mutation-proof
  arm (delete one entry, confirm the gate reports the loss)
- **Issue:** After lifting the three EXCEPT exceptions to
  `_EXCEPTIONS_ROSTER` and wiring `describe()` to read it, removing one
  entry on a scratch copy correctly dropped `--describe`'s emitted count
  (3→2), but the LIVE gate still exited 0 — HC-15 (which now iterates the
  roster) simply checked fewer entries against the unchanged rubric text
  and found all of them present. The roster was a parallel list: shrinking
  it silently reduced what the gate verified, with no failure signal.
- **Fix:** Widened HC-16 (the EXCEPT-distribution count check, a sibling
  assertion in the same file) to derive its expected total from
  `len(_EXCEPTIONS_ROSTER)` instead of the hardcoded literal `3`. Since
  each roster entry corresponds to exactly one `EXCEPT:` token in the live
  rubric text, a roster shrunk out of step with the actual text now fails
  HC-16 by name.
- **Files modified:** `scripts/check-high-confidence-bound.py`
- **Verification:** re-ran the mutation-proof arm on a fresh scratch copy:
  `--describe`'s count still drops 3→2, and the live gate now reports
  `HC-16: EXCEPT distribution incorrect: total=3 (expect 2), C3=1 (expect
  1), C5=2 (expect 2), Summary=0 (expect 0)` for both the canonical and
  emitted rubric surfaces.
- **Committed in:** `65b62cd` (part of the HC-BOUND commit; caught and
  fixed before the file was staged — the plan's own acceptance criterion
  is what surfaced this)

**Total deviations:** 3 auto-fixed (Rule 1 — bugs found and fixed during
this plan's own required mutation-proof verification, before the affected
files were staged).

## Assumption Drift (advisory)

**1. check-routing-battery.py's RR-* coverage mechanism is stdout-capture-based, not code-instrumented (unlike check-act-limb.py's/check-loop-closure.py's roster lifts).**
- **Found during:** Task 2, designing the BATT-06 limb
- **Planned:** the plan's `<action>` text for `check-routing-battery.py`
  reads "emit the RR-* sentinel roster derived from `_battery_core.py`'s
  own definitions (a `len()` and an id list, never a re-typed list of
  eleven ids) ... If `_battery_core.py` exposes no enumerable roster, add
  one there (D-21-J: enumeration lifted, sentinel logic and every frozen
  excerpt untouched)."
- **Actual:** the roster itself (`RR_SENTINEL_IDS`) was added exactly as
  planned. But making it PROVABLY load-bearing (the acceptance criteria's
  explicit removal-arm requirement) needed a second mechanism beyond the
  roster's mere existence, since nothing in `_battery_core.py`'s 800+ lines
  of sentinel logic reads a roster at all — each of the 11 assertions is
  independently coded inline. Rather than threading coverage-tracking
  through that byte-sensitive, frozen-excerpt-dependent code (which the
  plan's own "Frozen-evidence bound" explicitly warns against touching),
  `check-routing-battery.py`'s `self_test()` was changed to capture
  `self_test_boundary()`/`self_test_focused()`'s stdout and cross-check the
  RR-* ids it names against the roster, bidirectionally.
- **Why:** this keeps `_battery_core.py`'s sentinel logic and every frozen
  capture excerpt completely untouched (satisfying the plan's explicit
  bound) while still meeting the acceptance criteria's literal
  requirement — verified by the mutation-proof arm — that removing a
  roster entry makes `--self-test` report the loss.

## Next Phase Readiness

- All 20 script-backed gate rows (13 from batch A + 7 from batch B) now
  have working `--describe` limbs; `_gate_registry.py`'s live D-04 floor
  covers all of them with no further self-test edits needed as later
  batches (21-05) land.
- `DESCRIBE_FIELD_VOCABULARY` is unchanged at 16 members — every field this
  plan's 7 limbs emit was already declared by batch A.
- `BATTERY_ONLY_GATE_IDS` verbatim live value (`{"QUAL-01"}`) is recorded
  above for plan 21-11.
- No blockers. `git status --porcelain` in the real repo is clean after
  every commit; `git diff --stat -- tests/` is empty throughout.

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-06*

## Self-Check: PASSED

- FOUND: `scripts/check-act-limb.py` (modified)
- FOUND: `scripts/check-loop-closure.py` (modified)
- FOUND: `scripts/check-focused-parity.py` (modified)
- FOUND: `scripts/check-high-confidence-bound.py` (modified)
- FOUND: `scripts/check-registration.py` (modified)
- FOUND: `scripts/check-routing-battery.py` (modified)
- FOUND: `scripts/_battery_core.py` (modified)
- FOUND: `scripts/check-step0-emulator.py` (modified)
- FOUND: `scripts/_gate_registry.py` (modified)
- FOUND: commit `c88821d` (`git log --oneline --all`)
- FOUND: commit `0be3fb7` (`git log --oneline --all`)
- FOUND: commit `273733b` (`git log --oneline --all`)
- FOUND: commit `65b62cd` (`git log --oneline --all`)
- FOUND: commit `bafedca` (`git log --oneline --all`)
- FOUND: commit `5a7b3aa` (`git log --oneline --all`)
- FOUND: commit `69a7d7b` (`git log --oneline --all`)
- FOUND: commit `33e4ff2` (`git log --oneline --all`)
- FOUND: commit `7ea5281` (`git log --oneline --all`)
- FOUND: `bash scripts/check-firewall-battery.sh` reports FIREWALL: GREEN (25/25)
