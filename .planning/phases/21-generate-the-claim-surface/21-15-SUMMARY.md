---
phase: 21-generate-the-claim-surface
plan: 15
subsystem: infra
tags: [gate-registry, claim-surface, self-test, executed-vs-registered-floor, gap-closure]

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    provides: "plan 21-14's executed-vs-registered floor pattern (sync-content.py, check-version-stamps.py) and the CONF-SURFACE claim-surface generator/drift gate"
provides:
  - "check-agent.py's _EXECUTED_CHECK_INDICES floor: GATE-01's published branch_roster/branch_count equal what _check_agent_text() actually reaches, both unconditionally and under --skip-name-check, with _SKIP_NAME_CHECK_SCOPED_INDICES made load-bearing"
  - "check-act-limb.py's executed-list floor: HARN-01's published control_ids/control_count (78, was 76) equal what _run_self_test() actually runs, via _control_roster_problems()"
  - "check-step0-live.py's executed-list floor: STEP0-06's published control_ids/control_count (25, was 23) equal what self_test() actually runs, via _step0_control_roster_problems(); declared _CONTROL_IDS order verified against real run order (no drift found)"
  - "check-selfaudit-scan.py's executed-list floor: SCAN-GUARD's published control_ids/control_count (12, was 10) equal what _run_self_test() actually runs, via _selfaudit_meta_floor_problems(); describe-consistency now compares against the executed set instead of _META_CONTROL_IDS compared to itself"
  - "check-step0-emulator.py's executed-pairs floor: STEP0-08's SEMGATE-02 pair count/disclosed_bounds_anchors equal what Category 7's six pair blocks actually run, via _semgate02_pair_problems()"
  - "Regenerated claim surface (CLAUDE.md, docs/ARCHITECTURE.md, docs/gates/HARN-01.md, docs/gates/SCAN-GUARD.md, docs/gates/STEP0-06.md) with every moved figure asserted against its live --describe"
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Executed-vs-registered floor as a first-statement-of-block append (executed.append(id) before any condition/assertion, so a raising/failing control still counts as executed) — applied across five scripts with different block shapes: simple if-gated blocks (check-agent.py), a shared _check_negative() helper (check-act-limb.py, 71 fixture labels via one call site), 23 standalone inline blocks with no shared helper (check-step0-live.py), 10 named meta-control blocks (check-selfaudit-scan.py), and 6 pair blocks (3 hand-written + 3 table-driven, check-step0-emulator.py)."
    - "Reentrancy-guarded dispatch controls ((m) in check-act-limb.py, (dispatch) in check-selfaudit-scan.py) append their id BEFORE the reentrancy check, so both the outer invocation and any nested (skipped) invocation count the control as executed — avoiding a false missing= on the nested self-test's own floor."
    - "Negative-arm placement depends on whether the roster constant is pure ids or also carries published content: check-agent.py/check-act-limb.py/check-step0-live.py/check-selfaudit-scan.py add two negative-arm ids into their own id-only roster constant (a permanent addition is harmless); check-step0-emulator.py's SEMGATE02_OVERLAP_PAIRS is (id, description) tuples that feed a real published disclosed_bounds_anchors list, so its negative arm is a self-contained synthetic-set control that never touches the real constant."
    - "describe()-consistency tautology fix (check-selfaudit-scan.py): the pre-existing block compared describe()'s control_ids/control_count against _META_CONTROL_IDS — the SAME constant describe() itself reads, a comparison that can never fail regardless of what actually ran. Fixed by comparing against the local `executed` list instead, which required moving the negative-arm block's appends to run BEFORE the describe block (not after, as textually convenient) so `executed` is complete by the time describe()'s constant-derived control_count is compared against it."

key-files:
  created: []
  modified:
    - scripts/check-agent.py
    - scripts/check-act-limb.py
    - scripts/check-step0-live.py
    - scripts/check-selfaudit-scan.py
    - scripts/check-step0-emulator.py
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - docs/gates/HARN-01.md
    - docs/gates/SCAN-GUARD.md
    - docs/gates/STEP0-06.md

key-decisions:
  - "check-agent.py's Check 5 (maxTurns) index (4) is recorded as executed exactly when the skip_name_check-scoped VALUE clause is in play (gated purely on `not skip_name_check`, mirroring Checks 2/8), NOT when the block is merely entered — the key-presence half of Check 5 always runs regardless of skip_name_check and is not itself scoped, so gating the append on block-entry would have made index 4 always-executed and broken the --skip-name-check floor arm's equality with _SKIP_NAME_CHECK_SCOPED_INDICES. Discovered via a genuine self-test failure (missing=[] extra=[4]) before landing, not assumed."
  - "check-selfaudit-scan.py's original helper name (_selfaudit_control_roster_problems) was renamed to _selfaudit_meta_floor_problems after its own self-test broke: the substring '_roster_problems(' is contained inside 'control_roster_problems(', which inflated the PRE-EXISTING (roster-census) call-site census from 4 to 7 (it greps `inspect.getsource(_run_self_test)` for that literal substring). Renaming to a string that does not contain '_roster_problems(' fixed it without touching the census's own logic or expected count."
  - "check-selfaudit-scan.py's negative-arm block (roster-floor-missing/roster-floor-extra) runs BEFORE the (describe) block, not after — the textually natural position — because describe()'s control_count reads the _META_CONTROL_IDS constant (12, after this plan), and the describe-consistency comparison now checks it against len(executed); if the negative-arm appends happened after describe(), executed would only have 10 items at describe-check time and the (describe) control would wrongly fail 10 != 12 on every clean run."
  - "check-step0-emulator.py's negative arm for the SEMGATE-02 floor drives the shared _semgate02_pair_problems() helper with a synthetic pair-id set (not registered anywhere), rather than adding a permanent roster-floor-missing/roster-floor-extra pair into SEMGATE02_OVERLAP_PAIRS as the other four scripts do — because that constant's entries are (id, description) tuples that feed the REAL published disclosed_bounds_anchors list on STEP0-08's docs page; a fabricated permanent entry there would publish a fictitious 'documented semantic-overlap pair', which is exactly the over-claim defect this plan closes."

requirements-completed: [CONF-11]

# Metrics
duration: ~100min
completed: 2026-09-07
---

# Phase 21 Plan 15: Close the remaining CONF-11 rosters — check-agent, check-act-limb, check-step0-live, check-selfaudit-scan, check-step0-emulator

**Floored the five remaining CR-05 `--describe` rosters (check-agent.py, check-act-limb.py, check-step0-live.py, check-selfaudit-scan.py, check-step0-emulator.py) against what their own `--self-test` actually executes, in both directions, each with permanent negative-arm controls, and regenerated the claim surface — closing GAP 2 in full alongside plan 21-14's two scripts.**

## Performance

- **Duration:** ~100 min
- **Started:** 2026-09-07 (worktree setup + first Read)
- **Completed:** 2026-09-07
- **Tasks:** 3
- **Files modified:** 10 (5 scripts, CLAUDE.md, docs/ARCHITECTURE.md, 3 docs/gates/*.md pages)

## Accomplishments

- `scripts/check-agent.py`: added `_EXECUTED_CHECK_INDICES` (module-level set, cleared per call) and `_index_roster_problems()`. Each of the 8 gated checks in `_check_agent_text()` now records its own index as executed (Checks 4 and 6 were restructured from a combined `if GATE and CONDITION:` to a separate gate-then-condition so the append happens regardless of pass/fail). `_run_self_test()` gained two floor arms (unconditional and `--skip-name-check`, the latter proving `_SKIP_NAME_CHECK_SCOPED_INDICES` is load-bearing) plus a permanent synthetic negative arm — 13 controls total reported (was 10 fixtures). `branch_count` itself stayed at 8 (no fabricated `_CHECK_DESCRIPTIONS` entry was added).
- `scripts/check-act-limb.py`: added an `executed: list[str]` collector — `_check_negative()`'s single call site covers the 71 fixture-label controls in one place; explicit appends cover `a`, `b`, `coh`, `cov` and `m` (the reentrancy-guarded dispatch control, appended before its guard check so a nested self-test run still counts it). `_control_roster_problems()` floors `executed` against `_CONTROL_IDS`, which gained two permanent negative-arm ids (`roster-floor-missing`, `roster-floor-extra`) — 78 controls now reported (was 76).
- `scripts/check-step0-live.py`: verified `_CONTROL_IDS`' declared order against `self_test()`'s real run order by reading every one of the 23 blocks top to bottom — **no drift found**, the order matches exactly. Added `executed: list[str]`, one append per block (four fixture-loop entries plus 19 standalone blocks with no shared helper), `_step0_control_roster_problems()`, and two permanent negative-arm ids — 25 controls now reported (was 23).
- `scripts/check-selfaudit-scan.py`: added `executed: list[str]` covering the 10 pre-existing meta-controls (`roster-census`, `roster-lock`, `roster-entry-source`, `roster-es-census`, `validate-census`, `live-census`, `dispatch`, `live-dispatch`, `live-dispatch-census`, `describe`) plus two new negative-arm ids, floored via `_selfaudit_meta_floor_problems()`. Replaced the describe-consistency block's tautological `describe() vs _META_CONTROL_IDS` comparison with `describe() vs executed` — verified in a scratch copy that this assertion now fires independently of the separate roster floor. `REQUIRED_BRANCHES`/`_BRANCH_ROSTER_LOCK` (the 100-branch fixture battery's own floor) were read-only throughout, confirmed by diff review. 12 controls now reported (was 10).
- `scripts/check-step0-emulator.py`: each of Category 7's six SEMGATE-02 pair blocks (S-A01/S-A03/S-A05 hand-written, S-A07/S-A09/S-A11 table-driven) now appends its own id to `executed_pairs`. `_semgate02_pair_problems()` floors it against `SEMGATE02_OVERLAP_PAIRS`, with a synthetic-set negative arm (deliberately not a permanent addition to `SEMGATE02_OVERLAP_PAIRS`, since that constant's entries are `(id, description)` pairs feeding STEP0-08's real published `disclosed_bounds_anchors`). `semgate02_pair_count` stayed at 6 (no fabricated pair added).
- Regenerated the claim surface (`gen-gate-docs.py --write`): `CLAUDE.md`'s/`docs/ARCHITECTURE.md`'s STEP0-06 row moved `control_count` 23→25, HARN-01 row moved 76→78, SCAN-GUARD row moved 10→12; `docs/gates/STEP0-06.md`, `docs/gates/HARN-01.md`, `docs/gates/SCAN-GUARD.md` Facts fences moved identically. GATE-01 and STEP0-08 rows/pages are **unchanged** — deliberate, since neither script's roster constant gained a fabricated permanent entry.

## Task Commits

1. **Task 1: Floor check-agent.py's check roster and check-act-limb.py's control roster** - `b3cefc3` (feat)
2. **Task 2: Floor check-step0-live.py's and check-selfaudit-scan.py's control rosters** - `f1d38ac` (feat)
3. **Task 3: Floor the SEMGATE-02 pair roster, then regenerate and re-gate the claim surface** - `f1c08ff` (feat)

_No plan-metadata commit in this worktree run — orchestrator handles STATE.md/ROADMAP.md centrally after merge._

## Files Created/Modified

- `scripts/check-agent.py` — `_EXECUTED_CHECK_INDICES` set + `_index_roster_problems()` pure helper; every gated check appends its own index (Checks 4/6 restructured to separate gate from condition, no behavior change); `_FIXTURE_VALID_CANONICAL` fixture added for the floor arms; two floor arms + one permanent synthetic negative arm in `_run_self_test()`; rewrote the comment above `_CHECK_DESCRIPTIONS`
- `scripts/check-act-limb.py` — `executed: list[str]` collector; `_check_negative()` appends `label` as its first statement; explicit appends at `a`, `b`, `coh`, `cov`, `m`; `_control_roster_problems()` pure helper; `_CONTROL_IDS` gained `roster-floor-missing`/`roster-floor-extra` (76→78); floor evaluation + negative-arm block before the verdict
- `scripts/check-step0-live.py` — `executed: list[str]` collector, one append per of the 23 blocks (order-verified against real run order); `_step0_control_roster_problems()` pure helper; `_CONTROL_IDS` gained two negative-arm ids (23→25); floor evaluation + negative-arm block before the verdict
- `scripts/check-selfaudit-scan.py` — `executed: list[str]` collector across the 10 meta-controls; `_selfaudit_meta_floor_problems()` pure helper (renamed from an initial name that collided with the `(roster-census)` call-site census's substring scan); `_META_CONTROL_IDS` gained two negative-arm ids (10→12); negative-arm block relocated to run BEFORE the (describe) block so `executed` is complete when describe()'s constant-derived count is compared; describe-consistency comparison rewritten to check against `executed` instead of `_META_CONTROL_IDS`
- `scripts/check-step0-emulator.py` — `executed_pairs: list[str]` collector across Category 7's six pair blocks; `_semgate02_pair_problems()` pure helper; synthetic-set negative arm (SEMGATE02_OVERLAP_PAIRS itself untouched, stays at 6 pairs); describe-consistency comparison for `semgate02_pair_count`/`disclosed_bounds_anchors` rewritten to check against `executed_pairs`
- `CLAUDE.md`, `docs/ARCHITECTURE.md` — regenerated gate table (STEP0-06, HARN-01, SCAN-GUARD rows moved; GATE-01, STEP0-08 unmoved; generated region only)
- `docs/gates/HARN-01.md`, `docs/gates/SCAN-GUARD.md`, `docs/gates/STEP0-06.md` — regenerated Facts fences (control_ids/control_count moved as above)

## Decisions Made

See `key-decisions` in frontmatter above: Check 5's append semantics (block-entry vs. skip_name_check-gated), the helper rename forced by a call-site-census substring collision, the negative-arm block reordering forced by the describe-consistency tautology fix, and the SEMGATE-02 negative arm's deliberate use of a synthetic set instead of a permanent roster addition.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] check-selfaudit-scan.py's helper name collided with the pre-existing `(roster-census)` call-site census**
- **Found during:** Task 2, first self-test run after adding the floor helper
- **Issue:** Named the new pure helper `_selfaudit_control_roster_problems`. The pre-existing `(roster-census)` control counts occurrences of the literal substring `_roster_problems(` in `inspect.getsource(_run_self_test)`, expecting exactly 4 (1 real call + 3 isolation arms). Because `_selfaudit_control_roster_problems(` contains `_roster_problems(` as a substring, the census jumped from 4 to 7 and the self-test failed with an unrelated-looking error.
- **Fix:** Renamed the helper to `_selfaudit_meta_floor_problems` (7 occurrences renamed), which does not contain the colliding substring.
- **Files modified:** `scripts/check-selfaudit-scan.py`
- **Commit:** `f1d38ac`

**2. [Rule 1 - Bug] check-selfaudit-scan.py's describe-consistency comparison would have wrongly failed on every clean run**
- **Found during:** Task 2, designing the describe-consistency rewrite
- **Issue:** The plan directs comparing `describe()`'s `control_ids`/`control_count` against `executed` instead of `_META_CONTROL_IDS`. `describe()`'s `control_count` reads the module-level `_META_CONTROL_IDS` constant (12, after this plan's two new ids), but the textually natural position for the negative-arm block (after `(describe)`, before the final floor) would have left `executed` at only 10 items when the describe check ran — a permanent, wrong `10 != 12` failure on a clean tree.
- **Fix:** Moved the negative-arm append-and-assert block to run BEFORE `(describe)`, so all 12 ids are in `executed` by the time `describe()`'s comparison runs. Verified this ordering with a full `--self-test` PASS before committing.
- **Files modified:** `scripts/check-selfaudit-scan.py`
- **Commit:** `f1d38ac`

Neither issue reached a commit in its broken state — both were caught by running `--self-test` before committing, per the plan's own verification discipline.

### Plan-text discrepancy (recorded, not a code defect)

Plan 21-15's Task 2 acceptance criteria state, for `check-step0-live.py`: *"adding a fabricated id to `_CONTROL_IDS` fails naming it under `extra=`."* The actual, verified behavior — confirmed twice, once for `check-step0-live.py` and independently for all four other scripts in this plan that use the same `missing=`/`extra=` polarity (`_index_roster_problems`/`_control_roster_problems`/`_selfaudit_meta_floor_problems`/`_semgate02_pair_problems` all share the same convention: `missing = registered - executed`, `extra = executed - registered`) — is that a fabricated id added ONLY to the registered roster (never executed) is named under `missing=`, not `extra=`. `extra=` only fires when something executes that is NOT in the registered roster (demonstrated by the permanent synthetic negative arms in every script, e.g. `missing=['synthetic-b'] extra=['synthetic-c']`). This is the SAME polarity plan 21-14 documented for `check-agent.py`'s own over-claim scenario ("missing=[8]"), so the plan's `extra=` wording for `check-step0-live.py` specifically appears to be a copy-paste inconsistency, not a description of different intended behavior. The check itself correctly fires and correctly names the offending id in both directions across all five scripts — only the plan's own polarity label for this one arm does not match the mechanically consistent, cross-script-verified result. Recorded here rather than silently "corrected" in the SUMMARY's wording.

## Falsification Arms Recorded (verbatim failure text, scratch copies via `rsync -a --exclude .git`, real tree `git status --porcelain` empty before and after every run)

**check-agent.py, over-claim (fabricated 9th `_CHECK_DESCRIPTIONS` entry):**
```
check-agent --self-test: index-floor (unconditional) FAIL — executed/registered check-index mismatch: missing=[8] extra=[]
check-agent --self-test: index-floor (skip-name-check) FAIL — executed/registered check-index mismatch: missing=[8] extra=[]
```
Exit 1. Before this task: `branch_count` 9 and a fictitious assertion description published on GATE-01's row with rc 0.

**check-agent.py, under-claim (deleted Check 6's `_EXECUTED_CHECK_INDICES.add(5)`):**
```
check-agent --self-test: index-floor (unconditional) FAIL — executed/registered check-index mismatch: missing=[5] extra=[]
check-agent --self-test: index-floor (skip-name-check) FAIL — executed/registered check-index mismatch: missing=[5] extra=[]
```
Exit 1.

**check-agent.py, scoped-branch arm (`_SKIP_NAME_CHECK_SCOPED_INDICES` changed to `(1, 4)`):**
```
check-agent --self-test: index-floor (skip-name-check) FAIL — executed/registered check-index mismatch: missing=[7] extra=[]
```
Exit 1 (the unconditional arm still PASSes, correctly — only the scoped arm is affected).

**check-act-limb.py, under-claim (deleted the `_check_negative("c", ...)` call site):**
```
control roster/executed floor: FAIL — control roster/executed mismatch: missing=['c'] extra=[]
```
Exit 1. (Side effect: the reentrant `(m)` dispatch control also reports WRONGLY FAILED, because its nested self-test invocation hits the same missing-'c' floor — the same defect caught twice, not a masking issue.)

**check-act-limb.py, over-claim (fabricated `"fabricated-id"` appended to `_CONTROL_IDS`):**
```
control roster/executed floor: FAIL — control roster/executed mismatch: missing=['fabricated-id'] extra=[]
```
Exit 1.

**check-act-limb.py, permanent negative arm (synthetic pair, runs on every `--self-test`):**
```
(roster-floor-missing/extra) negative arms: PASS — fires and names both directions: ["control roster/executed mismatch: missing=['synthetic-b'] extra=['synthetic-c']"]
```

**check-step0-live.py, under-claim (deleted `executed.append("kn-rejection")`):**
```
self-test FAIL: control roster/executed floor — control roster/executed mismatch: missing=['kn-rejection'] extra=[]
```
Exit 1.

**check-step0-live.py, over-claim (fabricated `"fabricated-id"` appended to `_CONTROL_IDS`):**
```
self-test FAIL: control roster/executed floor — control roster/executed mismatch: missing=['fabricated-id'] extra=[]
```
Exit 1. (See "Plan-text discrepancy" above — plan text predicted `extra=`, actual is `missing=`.)

**check-selfaudit-scan.py, under-claim (deleted `executed.append("roster-lock")`):**
```
check-selfaudit-scan --self-test: FAIL — (dispatch): main(['--self-test']) returned 1, expected 0; (describe): control_ids disagrees with executed controls; control roster/executed mismatch: missing=['roster-lock'] extra=[]
```
Exit 1. Both the `(describe)` control AND the separate roster floor report the discrepancy independently — confirmed by reading the code and by this live mutation.

**check-selfaudit-scan.py, over-claim (fabricated `"fabricated-id"` appended to `_META_CONTROL_IDS`):**
```
check-selfaudit-scan --self-test: FAIL — (dispatch): main(['--self-test']) returned 1, expected 0; (describe): control_ids disagrees with executed controls; control roster/executed mismatch: missing=['fabricated-id'] extra=[]
```
Exit 1.

**check-step0-emulator.py, over-claim (fabricated `("S-A13", "fabricated")` appended to `SEMGATE02_OVERLAP_PAIRS`):**
```
check-step0-emulator --self-test: FAIL — (describe): semgate02_pair_count disagrees with executed pairs: {...'semgate02_pair_count': 7...}, SEMGATE-02 pair roster/executed mismatch: missing=['S-A13'] extra=[]
```
Exit 1. Before this task: a fabricated pair would have published a 7th `disclosed_bounds_anchors` entry on STEP0-08's page with everything green.

**check-step0-emulator.py, under-claim (deleted `executed_pairs.append("S-A03")`):**
```
check-step0-emulator --self-test: FAIL — (describe): semgate02_pair_count disagrees with executed pairs: {...'semgate02_pair_count': 6...}, SEMGATE-02 pair roster/executed mismatch: missing=['S-A03'] extra=[]
```
Exit 1.

## Before/After `--describe` Figures Moved Onto the Generated Surface

| Field | Script | Before | After | Producing command |
|---|---|---|---|---|
| `branch_count` / `branch_roster` | `check-agent.py --describe` | 8 | 8 (**unmoved**) | `python3 scripts/check-agent.py --describe` |
| `control_ids` / `control_count` | `check-act-limb.py --describe` | 76 | 78 | `python3 scripts/check-act-limb.py --describe` |
| `control_ids` / `control_count` | `check-step0-live.py --describe` | 23 | 25 | `python3 scripts/check-step0-live.py --describe` |
| `control_ids` / `control_count` | `check-selfaudit-scan.py --describe` | 10 | 12 | `python3 scripts/check-selfaudit-scan.py --describe` |
| `derived_counts.semgate02_pair_count` | `check-step0-emulator.py --describe` | 6 | 6 (**unmoved**) | `python3 scripts/check-step0-emulator.py --describe` |

`CLAUDE.md`'s/`docs/ARCHITECTURE.md`'s HARN-01, STEP0-06 and SCAN-GUARD rows, and their `docs/gates/*.md` Facts fences, all confirmed mechanically equal to their live `--describe` figures (see Verification Evidence). GATE-01's and STEP0-08's rows/pages are confirmed byte-identical (no diff) — stated deliberately, per the plan's instruction that an unmoved figure after a roster change is itself a claim worth recording.

## Verification Evidence

- `python3 scripts/check-agent.py --self-test` → `check-agent --self-test: PASS (10 fixtures, 13 controls total)`
- `python3 scripts/check-agent.py` (live leg, shipped agent) → `check-agent: PASS`
- `python3 scripts/check-act-limb.py --self-test` → `check-act-limb --self-test: PASS` (78 controls executed, matches `len(_CONTROL_IDS)`)
- `python3 scripts/check-step0-live.py --self-test` → `self-test PASS (...)`, `control roster/executed floor PASS — 25 controls executed`
- `python3 scripts/check-step0-live.py --describe` → `control_count`: 25
- `python3 scripts/check-selfaudit-scan.py --self-test` → `check-selfaudit-scan --self-test: PASS`, `control roster/executed floor: PASS — 12 meta-controls executed`
- `python3 scripts/check-selfaudit-scan.py` (live leg) → `check-selfaudit-scan: PASS`
- `python3 scripts/check-step0-emulator.py --self-test` → `check-step0-emulator --self-test: PASS — 41 fixtures + ...`, `SEMGATE02-floor PASS — 6 pairs executed`
- `python3 scripts/gen-gate-docs.py --self-test` → `gen-gate-docs: SELF-TEST PASS — 53 controls run` (unchanged from plan 21-14 — this plan adds controls inside the five edited scripts, never a `gen-gate-docs.py` registry entry)
- `python3 scripts/gen-gate-docs.py --check` → exit 0, `harvested 22/22 expected script-backed entries (22 total)`
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)` (total unchanged)
- `python3 scripts/check-registration.py` → `PASS (... 23/24 battery gates CI-registered + 1 battery-only by design)` — no new battery gates, no new REG-GUARD exemptions
- `sh .githooks/pre-commit` → exit 0
- `git diff -- scripts/check-agent.py scripts/check-act-limb.py scripts/check-step0-live.py scripts/check-step0-emulator.py` reviewed: every removed line is either a pure gate-restructuring (check-agent.py Checks 4/6, no assertion-text change) or absent entirely (the other three files' diffs are purely additive)
- `git diff -- scripts/check-selfaudit-scan.py` reviewed: the only removed lines are the describe-consistency block's `_META_CONTROL_IDS`-vs-itself comparison, replaced per the plan's explicit instruction; `REQUIRED_BRANCHES`/`_BRANCH_ROSTER_LOCK` untouched (confirmed no hunk touches either name)

## Issues Encountered

- This worktree checkout had no `.planning/` plan/state files and no `.venv` (matching the note left by plans 21-13's and 21-14's executors) — copied `21-15-PLAN.md`, `21-14-SUMMARY.md`, `21-VERIFICATION.md`, `21-CONTEXT.md`, `21-PATTERNS.md`, `PROJECT.md`, `STATE.md`, `config.json` from the main repo working tree, and ran `uv sync` to create `.venv` so VAL-03's pytest leg could resolve.
- The worktree's HEAD was on an OLDER commit (`d4da381`) than the expected base (`adbd12a4a02411df63bd3cb2f73849d2251eac0b`, itself an ancestor check that failed — `d4da381` was not an ancestor of the expected base at all) at agent start; corrected via `git reset --hard adbd12a4a02411df63bd3cb2f73849d2251eac0b` per the mandatory branch-check protocol before any work began.
- Two self-inflicted bugs were caught and fixed before any commit landed — see "Deviations from Plan" above (the `_roster_problems(` substring collision, and the describe-consistency ordering issue).

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- CR-05 (the six `--describe` rosters CONF-11's GAP 2 named as unfloored against execution) is now closed for all six names: `check-version-stamps.py` closed in plan 21-14; `check-agent.py`, `check-act-limb.py`, `check-step0-live.py`, `check-selfaudit-scan.py` and `check-step0-emulator.py` closed in this plan.
- GAP 2 (CONF-11's "live constants" promise) is closed in full across both plans 21-14 and 21-15.
- The plan-text discrepancy on `check-step0-live.py`'s over-claim polarity label (documented above) is a wording note only — no code change is implied or needed; flagging it here in case a future documentation pass wants to correct the plan's own prose.

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-07*

## Self-Check: PASSED

All 10 modified files confirmed present on disk; all 3 task commit hashes (`b3cefc3`, `f1d38ac`, `f1c08ff`) confirmed present in `git log --oneline --all`.
