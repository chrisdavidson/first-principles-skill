---
phase: 15-self-audit-scan
plan: 12
subsystem: testing
tags: [self-test, anti-masking-floor, entry-source-lock, parameterized-controls, scan-guard]

# Dependency graph
requires:
  - phase: 15-self-audit-scan
    provides: "plan 15-11's region-split Rubric-13 clause guards and corrected SCAN-GUARD docstring bound, closing 15-VERIFICATION.md gap 1 (SCAN-02); the 94-branch tree this plan's Step A reproductions are measured against"
provides:
  - "Rubric-11's controls parameterized over every _BAND_BULLETS literal (8 new branch ids, 2 superseded removed, net +6, 94 -> 100), closing the WR-01 hole where narrowing the tuple to one literal left --self-test green"
  - "A falsifiable ENTRY-SOURCE LOCK over the roster floor's covered argument, closing the WR-04 hole where aliasing it to REQUIRED_BRANCHES left the surplus check structurally incapable of failing"
  - "A full census of every multi-literal construct in check-selfaudit-scan.py (nine found), establishing the 'every multi-literal tuple has one arm per literal' claim as measured TRUE file-wide with no exceptions"
  - "Corrected docstring residual ledger (new bounds 11/12, amended IN-04) reconciling what tasks 1 and 2 make true, without disturbing bounds (7)/(8)'s own still-open WR-01/WR-04 findings from an earlier, unrelated review round"
affects: [15-13, 16-ship-hardening]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Parameterize self-test controls from the same tuple the check logic iterates, via zip(bullets, names) — deliberately NOT strict=True, because strict=True turns the narrowing mutation the control exists to catch into an uncaught exception instead of a clean, named anti-masking failure"
    - "ENTRY-SOURCE LOCK: assert a real call site's own argument text (not just call-pattern occurrence count) against an expected literal built by string concatenation — never as one contiguous literal declared inside the same function inspect.getsource() reads, which would make the check vacuously self-match its own declaration"

key-files:
  created: []
  modified:
    - scripts/check-selfaudit-scan.py

key-decisions:
  - "Dropped the plan's suggested zip(_BAND_BULLETS, _BAND_NAMES, strict=True) in favor of plain zip() — strict=True raises an uncaught ValueError on the exact _BAND_BULLETS-narrowing mutation the control exists to catch, which fails the task's own acceptance criteria (clean exit 1 naming six uncovered ids); plain zip truncates to the shorter sequence, satisfying it. Disclosed bound: this makes the LENGTHENING direction fail-open, guarded procedurally rather than mechanically, matching the file's existing bound (5) shape."
  - "Built the ENTRY-SOURCE LOCK's expected argument-triple literal via string concatenation rather than one contiguous string — a contiguous literal declared inside _run_self_test is part of what inspect.getsource(_run_self_test) returns, so a naive whole-source containment check found its OWN declaration and passed vacuously regardless of the real call site's actual text. Caught during verification-before-commit (never landed in a commit); fixed to match the file's existing 'build search patterns by concatenation' convention."
  - "Added bounds (11) and (12) to the docstring's residual ledger rather than editing bounds (7)/(8) — 15-REVIEW.md's round-1 WR-01 (band-determining limbs) and round-2 WR-01 (_BAND_BULLETS) are different findings that happen to share a label because two independent review rounds both restarted their own WR numbering from WR-01; same collision for WR-04. Bounds (7)/(8) describe the round-1 findings, which this plan does not touch."

requirements-completed: [SCAN-03]

# Metrics
duration: ~35min
completed: 2026-09-04
---

# Phase 15 Plan 12: `_BAND_BULLETS` parameterization and roster floor's entry-source lock Summary

**Parameterized Rubric-11's self-test controls over every `_BAND_BULLETS` literal (8 new branch ids, 94→100) and installed a falsifiable ENTRY-SOURCE LOCK over the roster floor's `covered` argument, closing both of `15-VERIFICATION.md` gap 2's `missing:` items and reconciling the gate's own residual ledger — `bash scripts/check-firewall-battery.sh` closes at `FIREWALL: GREEN (24/24)`.**

## Performance

- **Duration:** ~35 min
- **Started:** 2026-09-04T16:20:00Z (approx., worktree base-correction time)
- **Completed:** 2026-09-04T16:39:25Z
- **Tasks:** 3/3 completed
- **Files modified:** 1

## Accomplishments

- `Rubric-11`'s controls in `_run_self_test` are now driven from `zip(_BAND_BULLETS, _BAND_NAMES)` — one strip-arm (Criterion 4) and one dup-arm (Criterion 6) per literal, eight controls total — rather than the two hand-written controls that only ever exercised `_BAND_SOUND`.
- Reproduced live, independently, both holes `15-VERIFICATION.md`'s minor gap named: (1) narrowing `_BAND_BULLETS` to `(_BAND_SOUND,)` left `--self-test` at rc 0 reporting "All 94 branches covered"; (2) aliasing the real `_roster_problems(...)` call's third argument to `frozenset(REQUIRED_BRANCHES)` left `--self-test` at rc 0 with `ROSTER LOCK: PASS`, because the roster-x1/x2/x3 isolation arms and the `(roster-census)` call-site census only ever drive the pure helper with synthetic sets and count call-pattern occurrences, never argument text.
- After the fix, both mutations now fail `--self-test` by name: the narrowing mutation exits 1 naming the six now-uncovered branch ids; the aliasing mutation exits 1 naming `(roster-entry-source)`.
- A full census of every construct in the file where a check iterates over more than one literal found nine total (not the two the plan's `read_first` section named) — `_BAND_BULLETS` was the file's only exception before this plan; the other eight (four inline body/rubric tuples, the Rubric-13 region×clause double loop, and the cross-surface column-list loop) already carried one hand-written arm per literal. The published "every multi-literal tuple has one arm per literal" claim is now measured TRUE of the whole file, with no named exceptions.
- Found and fixed, before landing, a self-referential masking bug in my own first draft of the ENTRY-SOURCE LOCK: the expected argument-triple literal was declared as one contiguous string inside `_run_self_test`, so a whole-source containment check always found its own declaration regardless of what the real call site actually read. Rebuilt via string concatenation, matching the file's existing convention; re-verified the aliasing reproduction is caught after the fix.
- `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)` with `[PASS] SCAN-GUARD` (ran `uv sync` first to resolve the VAL-03 pytest prerequisite in this worktree, per CLAUDE.md's documented remedy).
- Measured `len(REQUIRED_BRANCHES) == len(_BRANCH_ROSTER_LOCK) == 100` (94 + 6 net). No external doc surface (`CLAUDE.md`, `docs/ARCHITECTURE.md`, `scripts/check-firewall-battery.sh`) was edited — reconciling those against 100 is plan 15-13's, per the binding constraints.

## Task Commits

Each task was committed atomically:

1. **Task 1: Parameterize Rubric-11's controls over every `_BAND_BULLETS` literal, and census every other multi-literal loop in the gate** - `2224dd9` (fix)
2. **Task 2: Install a falsifiable ENTRY-SOURCE LOCK over the roster floor's covered argument** - `35ebe35` (fix)
3. **Task 3: Record the residual and close green** - `83cd39b` (docs)

**Plan metadata:** committed alongside this SUMMARY (worktree mode — orchestrator finalizes on merge)

_Note: this plan carried no TDD tasks._

## Files Created/Modified

- `scripts/check-selfaudit-scan.py` — added `_BAND_NAMES`; replaced `R-11a`/`R-11b` with an 8-control `zip`-driven loop; registered 8 new branch ids and removed 2 superseded ones in `REQUIRED_BRANCHES`/`_BRANCH_ROSTER_LOCK`; added `_entry_source_problems` (pure helper), the `(roster-entry-source)` real lock, three `roster-es-x1/x2/x3` isolation arms, and a `(roster-es-census)` call-site census; added docstring bounds (11)/(12), amended IN-04, added a plan-15-12 sentence to the module summary paragraph

## Task 1: Step A reproduction (measured baseline)

Mutation: `_BAND_BULLETS = (_BAND_RIGOROUS, _BAND_SOUND, _BAND_HANDWAVY, _BAND_ABSENT)` → `_BAND_BULLETS = (_BAND_SOUND,)`, on a disposable `rsync -a --exclude .git` scratch copy.

```
$ python3 scripts/check-selfaudit-scan.py --self-test
...
ANTI-MASKING GATE: All 94 branches covered: [...]
check-selfaudit-scan --self-test: PASS
$ echo $?
0
```

Exactly as `15-VERIFICATION.md` predicted: rc 0, "All 94 branches covered" — three of four band literals had no arm in either criterion slice. Restored; real tree confirmed clean (`git status --porcelain` empty) before and after.

## Task 1: fix and re-verification

After parameterizing the controls (`zip(_BAND_BULLETS, _BAND_NAMES)`, no `strict=True` — see Deviations), the real tree:

```
$ python3 scripts/check-selfaudit-scan.py --self-test
...
ANTI-MASKING GATE: All 100 branches covered: [..., 'R-11-bands-crit4-absent', 'R-11-bands-crit4-handwavy',
'R-11-bands-crit4-rigorous', 'R-11-bands-crit4-sound', 'R-11-bands-crit6-absent', 'R-11-bands-crit6-handwavy',
'R-11-bands-crit6-rigorous', 'R-11-bands-crit6-sound', ...]
check-selfaudit-scan --self-test: PASS
$ echo $?
0
$ python3 scripts/check-selfaudit-scan.py
check-selfaudit-scan: COVERAGE — .../first-principles.md, .../validation-rubric.md
check-selfaudit-scan: PASS
$ echo $?
0
```

Re-applying the Step A narrowing mutation against the FIXED file (fresh scratch copy):

```
$ python3 scripts/check-selfaudit-scan.py --self-test
...
ANTI-MASKING GATE FAILURE: 6 branch(es) not covered: ['R-11-bands-crit4-absent', 'R-11-bands-crit4-handwavy',
'R-11-bands-crit4-sound', 'R-11-bands-crit6-absent', 'R-11-bands-crit6-handwavy', 'R-11-bands-crit6-sound']
$ echo $?
1
```

Clean exit 1 naming exactly six uncovered ids (no traceback) — the acceptance criteria's required behavior. (The specific six named reflect `zip`'s positional truncation when `_BAND_BULLETS` is narrowed to one element that lands at index 0, paired with `_BAND_NAMES[0]` = "rigorous"; the count and the clean-exit behavior are what the criteria requires, not a specific label-to-content mapping under this artificial single-element mutation — the real, unmutated tuple is correctly 1:1 by position.)

`/usr/bin/grep -c '"R-11-bands-crit4"' scripts/check-selfaudit-scan.py` → **0**; `/usr/bin/grep -c '"R-11-bands-crit6"' scripts/check-selfaudit-scan.py` → **0** (superseded ids gone).

## Task 1: neutralization evidence (all 8 new branch ids)

Extracted from the real tree's own `--self-test` run (each control mutates an in-memory copy of the real rubric and asserts the check fails for its own named reason):

| Branch id | Mutation | Observed `--self-test` arm result |
|---|---|---|
| `R-11-bands-crit4-rigorous` | strip `_BAND_RIGOROUS` from Criterion 4 slice | `(R-11-rigorous-crit4) correctly failed (2 failure(s))` — also fires `Rubric-9`'s ordering guard, which anchors on `_BAND_RIGOROUS`; documented, tolerated sibling failure per `_check_negative`'s design |
| `R-11-bands-crit4-sound` | strip `_BAND_SOUND` from Criterion 4 slice | `(R-11-sound-crit4) correctly failed (1 failure(s))` |
| `R-11-bands-crit4-handwavy` | strip `_BAND_HANDWAVY` from Criterion 4 slice | `(R-11-handwavy-crit4) correctly failed (1 failure(s))` |
| `R-11-bands-crit4-absent` | strip `_BAND_ABSENT` from Criterion 4 slice | `(R-11-absent-crit4) correctly failed (1 failure(s))` |
| `R-11-bands-crit6-rigorous` | duplicate `_BAND_RIGOROUS` in Criterion 6 slice | `(R-11-rigorous-crit6) correctly failed (1 failure(s))` |
| `R-11-bands-crit6-sound` | duplicate `_BAND_SOUND` in Criterion 6 slice | `(R-11-sound-crit6) correctly failed (1 failure(s))` |
| `R-11-bands-crit6-handwavy` | duplicate `_BAND_HANDWAVY` in Criterion 6 slice | `(R-11-handwavy-crit6) correctly failed (1 failure(s))` |
| `R-11-bands-crit6-absent` | duplicate `_BAND_ABSENT` in Criterion 6 slice | `(R-11-absent-crit6) correctly failed (1 failure(s))` |

All eight fire before the ANTI-MASKING GATE, whose "All 100 branches covered" line confirms none went silently uncovered.

**Spot-check against the live emitted file** (two representative mutations, disposable scratch copy, direct edit of `first-principles/agents/references/validation-rubric.md`, bare live leg — not `--self-test`'s in-memory fixture):

1. Stripped `- **Hand-wavy**` from the `[_CRIT4_START, _CRIT5_START)` range only:
   ```
   check-selfaudit-scan: FAIL — Rubric-11: band bullet '- **Hand-wavy**' occurs 0 time(s) in Criterion 4 slice, expected exactly 1
   ```
   rc=1. Restored; live leg confirmed rc=0.

2. Duplicated `- **Absent**` within the `[_CRIT6_START, _USAGE_NOTE)` range only:
   ```
   check-selfaudit-scan: FAIL — Rubric-11: band bullet '- **Absent**' occurs 2 time(s) in Criterion 6 slice, expected exactly 1
   ```
   rc=1. Restored; live leg confirmed rc=0. Real tree `git status --porcelain` confirmed empty (only the intentional `scripts/check-selfaudit-scan.py` change) throughout.

## Task 1: multi-literal construct census (Step D)

`/usr/bin/grep -nE "^_[A-Z_0-9]+ = \(_[A-Z]" scripts/check-selfaudit-scan.py` → exactly one line (`_BAND_BULLETS`, line 502), confirming the plan's prediction that it is the file's only *named tuple-of-constants*.

However, a broader `/usr/bin/grep -n "for .* in (" scripts/check-selfaudit-scan.py` sweep — run because the plan's own `read_first` section named only ONE inline multi-literal loop (the cross-surface column-list loop) — found **eight** inline `for X in (...)` / nested-loop constructs, not one. Reporting this as the "third construct" (and beyond) the census turned up, per the plan's own instruction:

| Construct | Location | Literals | Controlled arms (pre-plan) | Verdict |
|---|---|---|---|---|
| `_BAND_BULLETS` loop (Rubric-11, both slices) | lines ~1160/1168 (check logic, unchanged) | 4 × 2 slices = 8 | 2 (combined, `_BAND_SOUND` only) | **EXCEPTION → COVERED** (closed by Task 1) |
| Body row-rule tuple | line 873 | 2 | 2 (`B-07-rowrule-chain/claim`) | COVERED |
| Body ledger-independence tuple | line 892 | 2 | 2 (`B-10-ledger-indep-1/2`) | COVERED |
| Body reconciliation tuple | line 903 | 2 | 2 (`B-11-recon-lead/template`) | COVERED |
| Body placement tuple | line 913 | 2 | 2 (`B-12-placement-1/2`) | COVERED |
| Rubric division-of-labour tuple | line 1041 | 2 | 2 (`R-03-divlabour-1/2`) | COVERED |
| Rubric cols-in-scan-slice tuple | line 1063 | 2 | 2 (`R-05-cols-chain/claim`) | COVERED |
| `Rubric-13` region×clause double loop | lines 1255-1270 | 2 regions × 2 clauses = 4 combos | 8 (missing+dup per combo) | COVERED |
| Cross-surface column-list loop | line 1343 | 2 literals × 2 surfaces = 4 combos | 4 (`X-01-*`) | COVERED |

**Verdict: `_BAND_BULLETS` was the file's ONLY exception before this plan; the other eight multi-literal constructs already carried one hand-written arm per literal.** After Task 1's fix, the published "clause-level ids cover every multi-literal tuple, one arm per literal" claim is TRUE of the whole file, with no named exceptions — this narrows the plan's own `read_first` undercount (it named only the cross-surface loop) into a complete, measured inventory.

## Task 2: Step A re-reproduction (measured, not taken on faith)

`15-VERIFICATION.md` explicitly noted this hole was NOT independently re-reproduced in that verification round (it was taken from `15-REVIEW.md`'s measured claim). Reproduced here against the plan-15-11 tree, disposable scratch copy:

Mutation: `_roster_problems(REQUIRED_BRANCHES, _BRANCH_ROSTER_LOCK, frozenset(covered_branches))` → third argument changed to `frozenset(REQUIRED_BRANCHES)`.

```
$ python3 scripts/check-selfaudit-scan.py --self-test
...
(roster-lock) ROSTER LOCK: PASS — REQUIRED_BRANCHES == _BRANCH_ROSTER_LOCK and covered_branches has no unregistered branch id(s)
...
$ echo $?
0
```

Confirmed exactly as `15-REVIEW.md` predicted: rc 0, `ROSTER LOCK: PASS` — `surplus = covered - required` became `REQUIRED_BRANCHES - REQUIRED_BRANCHES` (empty by construction), and neither the roster-x1/x2/x3 isolation arms nor the `(roster-census)` call-site census caught it, because both only ever drive the pure helper with synthetic id sets or count call-pattern occurrences — never argument text. Restored; real tree confirmed clean before and after.

## Task 2: fix and re-verification

After installing `_entry_source_problems` and wiring `(roster-entry-source)`:

```
$ python3 scripts/check-selfaudit-scan.py --self-test
...
(roster-entry-source) ENTRY-SOURCE LOCK: PASS
(roster-es-x1) ISOLATION CLEAN: PASS
(roster-es-x2) ISOLATION ALIASED: PASS (real call's argument-triple text 'A, B, frozenset(C)' not found in source (rewritten, aliased, or missing call site))
(roster-es-x3) ISOLATION MISSING: PASS (real call's argument-triple text 'A, B, frozenset(C)' not found in source (rewritten, aliased, or missing call site))
(roster-es-census) CALL-SITE CENSUS: PASS (4 call sites)
...
ANTI-MASKING GATE: All 100 branches covered: [...]
check-selfaudit-scan --self-test: PASS
$ echo $?
0
```

Branch count unchanged at 100 — task 2 adds named controls, not registered branch ids, matching the plan's requirement.

Re-applying the Step A aliasing mutation against the FIXED file (fresh scratch copy):

```
$ python3 scripts/check-selfaudit-scan.py --self-test
check-selfaudit-scan --self-test: FAIL — (roster-entry-source): real call's argument-triple text
'REQUIRED_BRANCHES, _BRANCH_ROSTER_LOCK, frozenset(covered_branches)' not found in source (rewritten,
aliased, or missing call site); (dispatch): main(['--self-test']) returned 1, expected 0
...
(roster-lock) ROSTER LOCK: PASS — ...   <- the OLD guard still says PASS, exactly the pre-fix defect
(roster-entry-source) real call's argument-triple text '...' not found in source (rewritten, aliased, or missing call site)
$ echo $?
1
```

Now caught: exit 1, naming `(roster-entry-source)` by name, while `(roster-lock)` alone still reads `PASS` — direct evidence the NEW lock is what closes the hole the OLD floor could not see.

**Deleting the lock's own real call** (replacing the wiring with `roster_entry_source_problems = []` / `if False:`), fresh scratch copy:

```
$ python3 scripts/check-selfaudit-scan.py --self-test
check-selfaudit-scan --self-test: FAIL — (roster-es-census): observed 3 _entry_source_problems call
site(s), expected 4; (dispatch): main(['--self-test']) returned 1, expected 0
$ echo $?
1
```

Confirms the R4-CR-01 lesson applied to this task's own new floor: deleting the real call fails the census by name rather than leaving the battery silently green.

**Neutralizing both isolation arms at once** (replacing `_entry_source_problems`'s body with `return []` unconditionally), fresh scratch copy:

```
$ python3 scripts/check-selfaudit-scan.py --self-test
check-selfaudit-scan --self-test: FAIL — (roster-es-x2): aliased case did not report as expected: [];
(roster-es-x3): missing-call case did not report as expected: []; (dispatch): main(['--self-test']) returned 1, expected 0
(roster-es-x2) ISOLATION ALIASED: expected one problem naming the missing expected text, got []
(roster-es-x3) ISOLATION MISSING: expected one problem naming the missing call site, got []
$ echo $?
1
```

Both arms fail loudly when the helper's own detection logic is neutralized (the clean-case `roster-es-x1` arm, which expects `[]`, is unaffected — correctly discriminating). All scratch-copy work used disposable `rsync -a --exclude .git` copies; `git status --porcelain` in the real tree confirmed empty (or showing only the intentional `scripts/check-selfaudit-scan.py` edit) before and after every mutation.

## Task 3: closing sequence

- `python3 scripts/check-selfaudit-scan.py --self-test` → exit 0.
- `python3 scripts/check-selfaudit-scan.py` (bare live leg) → exit 0.
- `python3 scripts/sync-content.py --check` → exit 0.
- Ran `uv sync` first (installed pytest 9.1.1 and its locked transitive deps into this worktree's own `.venv` — CLAUDE.md's documented remedy for VAL-03's pytest prerequisite, not an ad hoc install).
- `bash scripts/check-firewall-battery.sh` → **`FIREWALL: GREEN (24/24)`**, with `[PASS] SCAN-GUARD check-selfaudit-scan.py --self-test + live`.
- `python3 scripts/check-registration.py --self-test` → exit 0 (29 controls, PASS).
- `python3 scripts/check-registration.py` (live) → exit 0 (`PASS (discovered 14 skills, agent present, manifest parsed, 14/14 names verified, 21/22 battery gates CI-registered + 1 battery-only by design)`).
- Measured `len(REQUIRED_BRANCHES) == len(_BRANCH_ROSTER_LOCK) == 100`.

### `15-VERIFICATION.md` gap 2 closure table

| Gap 2 `missing:` item | Closed by | Evidence |
|---|---|---|
| "Parameterize Rubric-11's arms over all four `_BAND_BULLETS` literals, registering new ids in `REQUIRED_BRANCHES` and `_BRANCH_ROSTER_LOCK`" | Task 1 (`2224dd9`) | 8 new ids registered (`R-11-bands-crit{4,6}-{rigorous,sound,handwavy,absent}`); narrowing `_BAND_BULLETS` now fails `--self-test` naming the uncovered ids (Task 1 fix-verification above), where before it was rc 0 (Step A reproduction above) |
| "Add an ENTRY-SOURCE LOCK for the roster floor's `covered` argument, matching `check-quality-harness.py`'s R4-CR-02 shape" | Task 2 (`35ebe35`) | `_entry_source_problems` + `(roster-entry-source)` wired; aliasing the real call's third argument now fails `--self-test` naming `(roster-entry-source)` (Task 2 fix-verification above), where before it was rc 0 with `ROSTER LOCK: PASS` (Step A re-reproduction above) |

### Residual ledger, confirmed by direct read after edit

- `/usr/bin/grep -n "^(7)" scripts/check-selfaudit-scan.py` → line 156, text unchanged: `` (7) **`15-REVIEW.md` WR-01 remains open**: the shared table-coverage-bound ``, still naming the band-determining-limbs gap as open — this plan does not touch it (it is a DIFFERENT WR-01, from an earlier review round, than the `_BAND_BULLETS` WR-01 this plan closes — the two rounds' independent WR numbering happened to collide).
- `/usr/bin/grep -n "IN-04:" scripts/check-selfaudit-scan.py` → amended to name the one new meta-guard task 2 added (`(roster-es-census)`), while stating the four other top-level assertions IN-04 originally named are still unguarded.
- `/usr/bin/grep -n "^(11)\|^(12)" scripts/check-selfaudit-scan.py` → both present: bound (11) records Task 1's outcome and the multi-literal census verdict; bound (12) records the ENTRY-SOURCE LOCK's disclosed bounds.

No external doc surface (`CLAUDE.md`, `docs/ARCHITECTURE.md`, `scripts/check-firewall-battery.sh`) was edited by this plan, per the binding constraints — plan 15-13 reconciles all four against the measured `100`.

## Decisions Made

- Dropped the plan's suggested `zip(..., strict=True)` in favor of plain `zip()` — see key-decisions above and the Deviations section below.
- Built the ENTRY-SOURCE LOCK's expected literal via string concatenation rather than one contiguous string, to avoid a self-referential vacuous match — see key-decisions above and the Deviations section below.
- Added new docstring bounds (11)/(12) rather than editing bounds (7)/(8), after confirming via direct read of both `15-REVIEW.md`'s round-1 disposition table and its round-2 findings section that "WR-01" and "WR-04" are each used for two unrelated findings across the two review rounds.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] The plan's suggested `zip(..., strict=True)` turns the exact mutation the control exists to catch into an uncaught crash**
- **Found during:** Task 1, verifying the fix against the Step A narrowing mutation
- **Issue:** `zip(_BAND_BULLETS, _BAND_NAMES, strict=True)` raises `ValueError: zip() argument 2 is longer than argument 1` when `_BAND_BULLETS` is narrowed to fewer elements than `_BAND_NAMES` — an uncaught traceback, not the clean `ANTI-MASKING GATE FAILURE` naming six uncovered ids the task's own acceptance criteria requires.
- **Fix:** Dropped `strict=True`; plain `zip()` truncates to the shorter sequence, so narrowing produces fewer controls and the anti-masking floor reports the resulting uncovered ids by name.
- **Files modified:** `scripts/check-selfaudit-scan.py`
- **Verification:** Re-ran the Step A mutation against the fixed file: exit 1, `ANTI-MASKING GATE FAILURE: 6 branch(es) not covered: [...]`, no traceback.
- **Committed in:** `2224dd9` (task 1 commit)

**2. [Rule 1 - Bug] Self-referential masking bug in the ENTRY-SOURCE LOCK's first draft**
- **Found during:** Task 2, verifying the fix against the Step A re-reproduction mutation (before this task's commit)
- **Issue:** The expected argument-triple literal was first declared as one contiguous string (`"REQUIRED_BRANCHES, _BRANCH_ROSTER_LOCK, frozenset(covered_branches)"`) assigned to a local variable inside `_run_self_test`. Since `inspect.getsource(_run_self_test)` returns that variable's own declaration as part of the function's source, a whole-source containment check trivially found its own declaration and reported `ENTRY-SOURCE LOCK: PASS` even against the aliased real call site — the exact defect this lock exists to catch, reinstated by the lock's own construction.
- **Fix:** Rebuilt the expected literal via string concatenation (`"REQUIRED_BRANCHES" + ", " + "_BRANCH_ROSTER_LOCK" + ", " + "frozenset(covered_branches)"`), matching the file's existing "build search patterns by concatenation" convention (e.g. `roster_call_pattern = "_roster_problems" + "("`), so the assembled literal never appears contiguous anywhere except at the real call site's own written-out text.
- **Files modified:** `scripts/check-selfaudit-scan.py`
- **Verification:** Re-ran the aliasing mutation against the fixed helper: exit 1, naming `(roster-entry-source)`. This defect was found and fixed before this task's commit — the committed code (`35ebe35`) never shipped the vacuous version; confirmed via `git show 35ebe35:scripts/check-selfaudit-scan.py`.
- **Committed in:** `35ebe35` (task 2 commit — the fix landed in the same commit as the feature, since it was caught before committing)

---

**Total deviations:** 2 auto-fixed (both Rule 1 — bugs found while satisfying the plan's own acceptance criteria and the binding constraint that every new control be neutralization-tested, not by inspection)
**Impact on plan:** Both fixes were necessary for the new controls to actually deliver the falsifiability the plan requires. No scope creep — both stay within `scripts/check-selfaudit-scan.py`, do not touch `shared/`, and do not weaken any existing guard.

## Issues Encountered

None beyond the two deviations above.

## User Setup Required

None — no external service configuration required. `uv sync` was run to satisfy VAL-03's pytest prerequisite in this worktree's own `.venv` (a locked dev-dependency install per CLAUDE.md, not an external service).

## Next Phase Readiness

`15-VERIFICATION.md` gap 2's two `missing:` items (both minor-severity holes in SCAN-GUARD's anti-masking floor) are closed, reproduced live before and after the fix in both directions. The tree closes green at 24/24.

Left open by design, owned by later plans in this wave chain per the binding constraints:
- Plan 15-13: reconciling the branch count (measured 100, up from 94) and any other census arithmetic on `CLAUDE.md`, `docs/ARCHITECTURE.md` and `scripts/check-firewall-battery.sh` — all deliberately left stale by this plan.
- `15-REVIEW.md`'s round-1 WR-01 (band-determining limbs, docstring bound (7)) and round-1 WR-04 (`_find_flat` normalization not independently load-bearing, docstring bound (8)) remain open, unrelated to and unchanged by this plan.

---
*Phase: 15-self-audit-scan*
*Completed: 2026-09-04*

## Self-Check: PASSED

All modified/created files found on disk (`scripts/check-selfaudit-scan.py`, this SUMMARY); all
three task commits (`2224dd9`, `35ebe35`, `83cd39b`) confirmed present in `git log`.
