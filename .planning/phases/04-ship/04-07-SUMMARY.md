---
phase: 04-ship
plan: 07
subsystem: docs
tags: [requirements-traceability, honesty-note, doc-hygiene, gap-closure]

# Dependency graph
requires:
  - phase: 04-ship (04-06)
    provides: the 04-VERIFICATION.md gap findings this plan closes
provides:
  - "docs/requirements-traceability.md with a single consistent audit-only figure (90) across the headline, the D-07 Honesty note, and the bold audit-only-rows heading"
  - "260728-wdi correction note re-scoped as dated history rather than an expired present-tense claim"
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Append-and-rescope dated-history correction shape for prose notes whose present-tense claim has been superseded by a later headline move, rather than deleting/rewriting the original record"

key-files:
  created: []
  modified:
    - docs/requirements-traceability.md

key-decisions:
  - "Re-scoped the 260728-wdi note as dated history (append 5 new lines, keep the first four lines byte-identical) instead of deleting or rewriting it, preserving the audit trail of what that quick task did"
  - "Left the two genuinely-historical 88 occurrences (docs/v8.0-final-closure.md:16, docs/v8.18-praor-loop-closure.md:175) byte-unchanged — both describe 88 as a superseded figure inside a named, dated transition, not a live claim"

patterns-established: []

requirements-completed: [SHIP-05]

# Metrics
duration: 15min
completed: 2026-08-29
---

# Phase 04-ship Plan 07: Close GAP 1 — audit-only count contradiction Summary

**Fixed a self-contradiction in `docs/requirements-traceability.md` where the coverage headline and bold heading correctly read 90 audit-only requirements but the D-07 Honesty note and a stale correction note still asserted 88.**

## Performance

- **Duration:** ~15 min
- **Started:** 2026-08-29T16:53:00Z (approx.)
- **Completed:** 2026-08-29T17:08:47Z
- **Tasks:** 2 completed
- **Files modified:** 1

## Accomplishments
- Corrected the D-07 Honesty note's audit-only count from 88 to 90, agreeing with the headline six lines above and the bold heading further down the file
- Re-scoped the `260728-wdi` correction note's final sentence as explicitly dated history (2026-07-28), pointing forward to headline-history row 8 for the later 147/90/0/237 move, while keeping the note's attribution and first four lines byte-identical
- Swept the whole tracked tree for `"88 audit-only\|88 requirements"` and confirmed exactly two surviving hits, both correctly classified `historical` and both untouched
- Re-confirmed sync-content, version-stamp, traceability, and link gates all pass; ran the full firewall battery

## Task Commits

Each task was committed atomically:

1. **Task 1: Correct the D-07 Honesty note count and re-scope the 260728-wdi correction note** - `369b209` (docs)
2. **Task 2: Sweep and classify every surviving 88-figure occurrence, then re-confirm the whole tree** - verification-only, no file changes; no commit (nothing to stage)

**Plan metadata:** (this SUMMARY commit)

## Files Created/Modified
- `docs/requirements-traceability.md` - D-07 Honesty note count corrected (88 → 90); `260728-wdi` correction note's final sentence re-scoped as dated history pointing to headline-history row 8

## Decisions Made
- Used the append-and-rescope shape (keep first four lines of the `260728-wdi` block quote byte-identical, replace only the final two lines with five new lines) rather than deleting or rewriting the note, per the plan's explicit instruction and the repo's established "append to records of past decisions rather than rewrite them" convention (D-08 addendum, DETECT-05 correction blocks in `docs/README.md`)

## Task 2: Sweep Classification Table

Sweep command: `command grep -rn "88 audit-only\|88 requirements" docs/ CHANGELOG.md scripts/ CLAUDE.md`

Result: exactly 2 hits.

| # | Location | Excerpt | Classification | Justification |
|---|----------|---------|-----------------|----------------|
| 1 | `docs/v8.0-final-closure.md:16` | "→ 126 reproducible / 88 audit-only / 0 gap / 214 total when 15 builder requirements were retired, → **147/90/0/237** when the 23 v8.18 requirements were registered" | `historical` | Sits inside a block quote explicitly headed "Superseded. Every count." and states 88 as one step in a documented three-move transition sequence ending at the current 147/90/0/237 figure. `CLAUDE.md`'s Requirements-surface section names this file "historical record, not current state." Not a live claim. |
| 2 | `docs/v8.18-praor-loop-closure.md:175` | "moving the coverage headline from **126 reproducible / 88 audit-only / 0 gap / 214 total** to **147 reproducible / 90 audit-only / 0 gap / 237 total**" | `historical` | The before/after of this milestone's own headline move, presented as a named, dated transition (v8.18 Phase 4 loop-closure record), not a present-tense assertion of the current count. |

`live-claim` bucket: **empty** (as required). Both hits are the two expected genuinely-historical occurrences named in the plan's `<interfaces>` block; no new/unexpected hit surfaced.

## Whole-tree gate re-confirmation

Run in order, each gated on the previous passing:

1. `python3 scripts/sync-content.py --check` — exit 0, no output. PASS.
2. `python3 scripts/check-version-stamps.py` — `check-version-stamps: 17 stamps, all '8.18.0'` / `check-version-stamps: PASS`, exit 0. PASS.
3. `python3 scripts/check-traceability.py --self-test` — exit 0, `V818-ROWS PASS` lines present (row count == 23, tier partition pinned, etc.). PASS.
4. `python3 scripts/check-links.py --self-test && python3 scripts/check-links.py` — both exit 0 (`check-links: PASS (244 markdown links + 6 namespace refs across 127 files)`). PASS.
5. `bash scripts/check-firewall-battery.sh` — **verbatim final line:**

```
FIREWALL: BLOCKED (1 prerequisite(s) unmet; 19/20 passed)
```

Exit code: 2.

**This is the documented BLOCKED outcome, not a gate failure.** The single unmet item is `[PREREQ] VAL-03`: no pytest-capable interpreter is available in this worktree (`.venv/bin/python3` does not exist in this worktree checkout, and the bare `python3` on `PATH` has no `pytest` module installed). Confirmed this is a worktree-environment artifact, not a repo-wide or plan-introduced defect: the main repository checkout at `/home/chrisdavidson/Projects/first-principles-skill/.venv` has a populated `.venv` with pytest available, while this worktree — created fresh for this agent — never received its own `.venv`. All 19 other gates in the battery printed `[PASS]`, including `DUAL-04`, `GATE-02-v8.5`, `VAL-01`, `VAL-02`, `VAL-04`, `VAL-05`, `VERSION-01`, `GATE-01`, `BATT-06`, `STEP0-06`, `STEP0-08`, `TRACE-03`, `COLLIDE-01`, `QUAL-01`, `HARN-01`, `HARN-02`, `HARN-03`, plus the `INVARIANT-CHECK` and `FROZEN-EVIDENCE` inline checks. Per the plan's own instruction ("If it prints `FIREWALL: BLOCKED` / exit 2, that is an unmet pytest prerequisite in the environment, not a gate failure — report it as such rather than treating it as a defect introduced by this plan"), this is reported as-is and not auto-fixed by installing a fresh `.venv`, since doing so is outside this plan's `files_modified` scope (`docs/requirements-traceability.md` only) and outside Task 2's read-only verification action.

## Deviations from Plan

None - plan executed exactly as written. The two edits landed exactly as specified (Task 1), and the sweep returned exactly the two expected historical hits with an empty `live-claim` bucket (Task 2). The `FIREWALL: BLOCKED` outcome on the battery run is explicitly anticipated and pre-classified by the plan itself as an environment prerequisite gap, not a deviation requiring a fix.

## Issues Encountered
- `bash scripts/check-firewall-battery.sh` reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 19/20 passed)` because this worktree checkout has no `.venv` with `pytest` installed (VAL-03's third leg requires a pytest-capable interpreter). The plan explicitly instructs treating this outcome as an unmet environment prerequisite, not a gate failure introduced by this plan; confirmed by comparison against the main repo checkout, which does have a working `.venv`. Not fixed in-scope: creating a `.venv` (`uv sync`) is outside this plan's `files_modified` (`docs/requirements-traceability.md`) and outside Task 2's verification-only action.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- GAP 1 from `04-VERIFICATION.md` is closed: `docs/requirements-traceability.md` is internally consistent, stating exactly one live audit-only figure (90) across all three places that make a live claim.
- The battery's `FIREWALL: BLOCKED` outcome (pytest prerequisite absent in this worktree) may resurface for any other plan in this wave running its own firewall-battery verification inside this same worktree; it is an environment condition, not something this plan's edit caused or can fix within its own scope.

---
*Phase: 04-ship*
*Completed: 2026-08-29*
