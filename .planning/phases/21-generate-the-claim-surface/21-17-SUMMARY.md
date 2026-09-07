---
phase: 21-generate-the-claim-surface
plan: 17
subsystem: testing
tags: [self-test, verification-gate, python, ci-gate, version-stamps]

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    provides: "plan 21-14's VERSION-01 kind-roster floor and plan 21-16's ledger ratchet, both landed earlier in this phase"
provides:
  - "check-version-stamps.py's _stamp_roster_problems aligned to the repo-wide missing/extra polarity"
  - "_roster_arm_clauses(), a reusable clause-split-with-shape-guard helper other scripts can port"
  - "a permanent registered control for the genuine roster under-claim direction"
  - "a derived (not hand-typed) self-test PASS line for check-version-stamps.py"
affects: [21-18, 21-19]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "missing/extra roster-floor polarity: missing=registered-walked (over-claim), extra=walked-registered (under-claim) — now uniform across check-version-stamps.py and its six siblings"
    - "clause-split negative arm with message-shape guard (_roster_arm_clauses) ported from check-agent.py's idiom"
    - "counting wrapper + statement-anchored source census for deriving a self-test's published fixture/assertion figures instead of hand-typing them"

key-files:
  created: []
  modified:
    - scripts/check-version-stamps.py

key-decisions:
  - "Overrode plan 21-14's recorded key decision to keep _stamp_roster_problems' inverted polarity. Aligned instead with the six sibling floors (check-agent.py, check-act-limb.py, check-selfaudit-scan.py, check-step0-live.py, check-step0-emulator.py, sync-content.py) so one missing/extra vocabulary holds across seven floors, per this plan's decision of record."
  - "The fixture-count census matches statement-start tokens (stripped line startswith build_fixture( / _build_fixture() rather than a bare substring search, because a bare regex over the self-test's own source text counted the census's own comments and string literals as false-positive call sites — discovered live while proving falsification 8."
  - "The census counts bypass calls to the underlying _build_fixture( (excluding the wrapper's own internal delegation line) so a call that routes around the counting wrapper inflates the census and is caught as a mismatch, rather than silently matching the (also un-incremented) counter."

requirements-completed: [CONF-11]

# Metrics
duration: ~35min
completed: 2026-09-07
---

# Phase 21 Plan 17: Align VERSION-01's roster polarity and derive its self-test figures Summary

**Inverted `_stamp_roster_problems` polarity fixed to match six sibling floors, a genuine under-claim control added where none existed, and the self-test's "8 fixture trees, 16 named assertions" hand-typed literals replaced with figures derived from what actually ran.**

## Performance

- **Duration:** ~35 min
- **Started:** 2026-09-07T18:27Z (approx.)
- **Completed:** 2026-09-07T19:02:51Z
- **Tasks:** 2 completed
- **Files modified:** 1 (`scripts/check-version-stamps.py`)

## Accomplishments

- `_stamp_roster_problems` now computes `missing = registered_set - walked_set` (over-claim) and `extra = walked_set - registered_set` (under-claim), matching `check-agent.py`, `check-act-limb.py`, `check-selfaudit-scan.py`, `check-step0-live.py`, `check-step0-emulator.py` and `sync-content.py` — this file previously computed the reverse of every sibling.
- Added `_roster_arm_clauses(text) -> tuple[str, str]`, a pure clause-split helper (ported idiom from `check-agent.py`) that raises `ValueError` naming the offending text if either the `missing=` or ` extra=` marker is absent, rather than silently treating the whole message as both clauses.
- Renamed the two over-claim arms to `kind-roster-overclaim-fabricated` and `kind-roster-overclaim-fixture` (the latter was previously misnamed `kind-roster-underclaim-detected` while actually testing an over-claim), and both now assert which specific clause their target id landed in.
- Added a genuinely new `kind-roster-underclaim-detected` control that shrinks the roster while walking the real repo tree — the one direction that had no permanent registered control before this plan (the prior demonstration was a one-off scratch-copy run recorded only in `21-14-SUMMARY.md`).
- Added `kind-roster-arm-shape-guard`, proving `_roster_arm_clauses`' message-shape guard is live.
- Replaced the self-test's two hand-typed count literals (`"8 fixture trees, 16 named assertions"`) with derived figures: a counting `build_fixture` wrapper around `_build_fixture`, and `len(executed)` from an `expect()`-populated list. Live run now reports `PASS (6 fixture trees, 21 named assertions)`.
- Added `expect-names-unique` (a duplicated control id would otherwise silently understate the published assertion figure) and `fixture-count-matches-call-sites` (a source census that also catches a call bypassing the counting wrapper).

## Task Commits

Each task was committed atomically:

1. **Task 1: Align the roster polarity, split the clauses, and add the genuine under-claim control** - `8f3c7b4` (fix)
2. **Task 2: Derive the self-test's two published figures instead of hand-typing them** - `fad7b80` (fix)

**Plan metadata:** committed by the worktree-mode `commit-to-subrepo`/orchestrator flow (SUMMARY.md commit follows this file)

## Files Created/Modified

- `scripts/check-version-stamps.py` - Polarity-aligned roster floor, `_roster_arm_clauses` helper, four roster arms (two renamed, one new, one shape-guard), counting fixture wrapper, and a derived self-test PASS line with two new anti-drift controls.

## Decisions Made

- **Overrode plan 21-14's polarity decision**, in writing, per this plan's explicit mandate. `21-14-SUMMARY.md` recorded the inversion as deliberate, justified by that plan's own acceptance-criteria wording ("over-claim -> extra="). This plan judges a uniform missing/extra vocabulary across seven floors worth more than one plan's phrasing — and it is what makes plan 21-19's cross-script census possible at all.
- **Census matches statement-start tokens, not a bare substring search.** A first implementation using `re.search(r"\bbuild_fixture\(", line)` over the self-test's own source text (via `inspect.getsource`) counted its own explanatory comments and a code line's string literal (`elif "_build_fixture(" in line`) as false-positive call sites, inflating the census to 7-9 against a true count of 6. Fixed by requiring `stripped.startswith(_FIXTURE_WRAPPER_CALL)` / `stripped.startswith(_FIXTURE_BUILDER_CALL)` (the call must be the first token on its line), and by moving the token constants (`_FIXTURE_WRAPPER_CALL`, `_FIXTURE_BUILDER_CALL`, `_FIXTURE_DELEGATION_ARGS`) to module level outside `self_test()` so they never appear in the text the census itself reads.
- **The census also catches a bypass call to the underlying `_build_fixture(` directly** (excluding only the wrapper's own internal delegation line), so a call that routes around the counting wrapper inflates the census without inflating the counter — surfacing the mismatch rather than hiding it (both sides would otherwise stay in accidental agreement, since neither counted the bypass). This was discovered and fixed while reproducing falsification 8, which originally passed when it should have failed.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixture-count census had false positives from its own comments/string literals**
- **Found during:** Task 2, while running falsification 8 (bypass-call detection) for the first time — it passed when the plan requires it to fail, revealing the census was blind to the exact defect it exists to catch, and a second run of the *unmodified* real tree showed `call_sites=9` against `fixture_count=6` (extra false-positive matches from the census's own explanatory comments and a code line containing the search string as a literal).
- **Issue:** `re.search(r"\bbuild_fixture\(", line)` is a bare substring test over the self-test function's own source (via `inspect.getsource`), so it matched the census implementation's own comments (which name `` `build_fixture(` `` in prose) and a code line (`elif "_build_fixture(" in line ...`) that contains the search token as a Python string literal, not as a call.
- **Fix:** Anchored the match to the start of each stripped line (`stripped.startswith(_FIXTURE_WRAPPER_CALL)` / `stripped.startswith(_FIXTURE_BUILDER_CALL)`), which only actual call statements satisfy, and moved the three token constants to module level so the census's own source (which necessarily contains those tokens) is never re-scanned by itself.
- **Files modified:** `scripts/check-version-stamps.py`
- **Verification:** Re-ran the unmodified self-test (`fixture_count=6, call_sites=6`, PASS) and all three Task-2 falsification arms (6, 7, 8) on a fresh `rsync` scratch copy; falsification 8 (bypass call) now correctly fails naming `fixture-count-matches-call-sites`.
- **Committed in:** `fad7b80` (part of Task 2 commit — fixed before commit, not a follow-up)

---

**Total deviations:** 1 auto-fixed (1 bug, caught and fixed by the plan's own falsification requirement before commit)
**Impact on plan:** The fix was required to meet the plan's own falsification-8 acceptance criterion; no scope creep beyond what Task 2 already specified.

## Issues Encountered

- The worktree lacked a local `.venv`, so `scripts/check-firewall-battery.sh` initially reported `BLOCKED` (VAL-03's pytest leg unavailable) rather than `GREEN`. Ran `uv sync` to create `.venv` (ships pytest 9.1.1) per `CLAUDE.md`'s documented remedy; the battery then reported `FIREWALL: GREEN (26/26)`.

## Falsification Arms — Exact Failure Text

All eight falsification arms specified in the plan were reproduced on `rsync -a --exclude .git` scratch copies (never in the real tree — `git status --porcelain` confirmed empty before and after every scratch-copy run):

1. **Polarity swap** (the verifier's exact reproduction): swapping the two subtractions back to the pre-plan inversion —
   `check-version-stamps --self-test: FAIL (3 fixture(s): kind-roster-overclaim-fabricated, kind-roster-overclaim-fixture, kind-roster-underclaim-detected)`, exit 1. (Before this plan, the identical mutation left it 16/16 PASS, exit 0.)
2. **`extra` suppressed** (`extra = set()`): `check-version-stamps --self-test: FAIL (1 fixture(s): kind-roster-underclaim-detected)`, exit 1; specifically `kind-roster-underclaim-detected FAIL ([])`.
3. **`missing` suppressed** (`missing = set()`): `check-version-stamps --self-test: FAIL (2 fixture(s): kind-roster-overclaim-fabricated, kind-roster-overclaim-fixture)`, exit 1; both `FAIL ([])`.
4. **Message-shape marker deleted** (removed the `" extra="` half of the format string): unhandled `ValueError: _roster_arm_clauses: message lacks 'missing=' or ' extra=' marker: "stamp-source-kind roster/walked mismatch: missing=['fixture-fabricated-kind']"`, process exits 1 (non-zero) rather than silently passing with both clauses equal to the whole message.
5. **Walk-record deleted** (removed `walked.append(spine_kind)` in `collect_stamps()`): `check-version-stamps --self-test: FAIL (2 fixture(s): kind-roster-matches-walked, kind-roster-underclaim-detected)`, exit 1; `kind-roster-matches-walked FAIL (["stamp-source-kind roster/walked mismatch: missing=['shared/spine/SKILL.meta.yml'] extra=[]"])`.
6. **Derived-assertion-figure probe** (added one extra `expect("scratch-probe", True)` inside `self_test()`, no literal edited): terminal line rose from `PASS (6 fixture trees, 21 named assertions)` to `PASS (6 fixture trees, 22 named assertions)`.
7. **Duplicate control id** (duplicated the `expect("clean-agrees", ...)` call): `check-version-stamps --self-test: FAIL (1 fixture(s): expect-names-unique)`, exit 1; `expect-names-unique FAIL (duplicated: ['clean-agrees'])`.
8. **Fixture-counter drift** (added a call to `_build_fixture(...)` directly, bypassing the `build_fixture` counting wrapper): `check-version-stamps --self-test: FAIL (1 fixture(s): fixture-count-matches-call-sites)`, exit 1; `fixture-count-matches-call-sites FAIL (fixture_count=6, call_sites=7)`.

## Before/After `--self-test` Terminal Line

- **Before this plan:** `check-version-stamps --self-test: PASS (8 fixture trees, 16 named assertions)` (hand-typed literals).
- **After this plan:** `check-version-stamps --self-test: PASS (6 fixture trees, 21 named assertions)` (both figures derived — `6` from the counting wrapper, `21` from `len(executed)`; per-control PASS line count independently verified via `out.count(' PASS')` = 22, which includes the terminal summary line itself).

## Verification Performed

- `python3 scripts/check-version-stamps.py --self-test` — exits 0, all 21 controls PASS.
- `python3 scripts/check-version-stamps.py` (live leg) — exits 0, stdout unchanged (17 stamps, all `'8.26.0'`) before and after both tasks.
- `python3 scripts/check-version-stamps.py --describe` — byte-identical JSON before and after both tasks (`stamp_source_kind_count: 4`, same four `registered_surfaces`).
- `python3 scripts/gen-gate-docs.py --check` — exits 0, `harvested 22/22 expected script-backed entries`, no `DRIFT:` lines.
- `bash scripts/check-firewall-battery.sh` — `FIREWALL: GREEN (26/26)` after provisioning a local `.venv` via `uv sync` (see Issues Encountered).
- `sh .githooks/pre-commit` — exits 0 (the `DRIFT:`/`NON-DETERMINISTIC:` lines in its output are the generators' own self-test fixtures exercising their falsifiability controls, not real drift on this tree).
- `git status --porcelain` — empty except the one intentionally modified file, both before and after every scratch-copy falsification run.
- Acceptance-criteria greps: `missing = registered_set - walked_set` count=1, `extra = walked_set - registered_set` count=1, whole-message-arm substring count=0, all four new/renamed control ids appear as `expect(` first arguments, `kind-roster-overclaim-detected` (old misnamed id) appears nowhere.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `_roster_arm_clauses` is now available at the module level with the exact name plan 21-18 requires (ports the identical helper into five more scripts) and plan 21-19 requires (registers a cross-script census keyed on that token).
- `docs/gates/VERSION-01.md`'s claim that the roster is "floored ... in both directions by `self_test()`" is now actually true of the code, but the doc itself is not yet updated to describe it accurately post-plan — that correction is explicitly scoped to plan 21-19, per this plan's objective.
- No blockers identified for 21-18 or 21-19.

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-07*
