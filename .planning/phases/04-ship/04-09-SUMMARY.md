---
phase: 04-ship
plan: 09
subsystem: docs
tags: [doc-hygiene, gap-closure, optional]

# Dependency graph
requires:
  - phase: 04-ship (04-08)
    provides: "docs/v8.18-praor-loop-closure.md and docs/README.md already in their post-04-08 state (the 'since v7.9' primacy-claim fix), which this plan's edits build on top of"
provides:
  - "docs/v8.18-praor-loop-closure.md's FIREWALL: RED literal with the invisible U+00AD soft hyphen removed — now byte-identical to the battery's actual printed string and greppable"
  - "docs/README.md's v8.18 index row citing the CHANGELOG correction note by its containing `## [8.17.2]` entry instead of a line number that had already rotted once"
  - "docs/ARCHITECTURE.md's canonical gate-surface paragraph stating a true strict-superset relation with an arithmetic (17 + 1 + 2 = 20) that closes at the number the battery actually prints"
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Assert-then-remove single-character edit for an invisible-character defect (assert exactly one chr(0xAD) present, then remove it) rather than a bulk transliteration pass, so the edit fails loudly if the byte count assumption is wrong"
    - "Citing a rotting target (a CHANGELOG line number) by its stable containing structure (the entry heading) instead of re-pointing at the current line, so the citation cannot rot again on the next insertion above it"

key-files:
  created: []
  modified:
    - docs/v8.18-praor-loop-closure.md
    - docs/README.md
    - docs/ARCHITECTURE.md

key-decisions:
  - "Independently re-derived all three ARCHITECTURE.md facts from live files rather than trusting the plan's stated numbers: counted 17 job keys in .github/workflows/validation.yml (grep on top-level `  <name>:` keys, catching pointer-drift-guard's bare-named job), counted 18 distinct gate/gate_prereq registrations in scripts/check-firewall-battery.sh (VAL-03's gate/gate_prereq branches are mutually exclusive and counted as one slot) plus 2 inline checks (INVARIANT-CHECK, FROZEN-EVIDENCE) = 20, and confirmed `gate \"VAL-01\"` is registered in the battery script by direct grep. All three matched the planner's derivation (17, 20, yes)."
  - "Reflowed the plan's suggested replacement sentence for docs/ARCHITECTURE.md onto different line breaks than first drafted, after the first draft's line wrap split the required literal 'strict superset of CI' across two source lines and defeated its own single-line grep acceptance criterion — same defect class 04-08 hit and fixed the same way (reflow, not reword)."

patterns-established: []

requirements-completed: [SHIP-05]

# Metrics
duration: 25min
completed: 2026-08-29
---

# Phase 04-ship Plan 09: Close three backlog-triaged documentation defects (soft hyphen, stale citation, gate-arithmetic) Summary

**Removed an invisible U+00AD soft hyphen that silently defeated grep on the `FIREWALL: RED` literal, re-pointed a CHANGELOG citation from a line number that had already rotted once to its stable containing entry, and corrected `docs/ARCHITECTURE.md`'s gate-surface paragraph from a false "CI additionally runs VAL-01" claim with arithmetic that summed to 19 to a true strict-superset statement that closes at the battery's actual 20.**

## Performance

- **Duration:** ~25 min
- **Tasks:** 2 completed, both committed
- **Files modified:** 3

## Accomplishments

- Confirmed the soft-hyphen defect live: `grep -c "FIREWALL: RED" docs/v8.18-praor-loop-closure.md` returned 0 before the edit (the fragment read `FIRE<U+00AD>WALL: RED` with an invisible U+00AD between `FIRE` and `WALL`, rendered here as an escape per the plan's own convention rather than pasting the literal byte), matching the plan's claim that the defect is invisible in review and breaks the exact search a person would run
- Removed the single U+00AD via an assert-then-remove Python script (`assert count == 1` before removing), not a bulk strip — `git diff --numstat` confirms exactly 1 added / 1 deleted line
- Repo-wide swept all tracked `.md`/`.py`/`.sh`/`.yml`/`.yaml`/`.json` files (via `git ls-files`) for `chr(0xAD)`: **0 hits** anywhere in the tracked tree after the edit
- Repo-wide scanned for `CHANGELOG.md:355`: found exactly **one** occurrence (`docs/README.md:192`), matching the planner's scan; replaced it with a citation naming the containing `## [8.17.2]` entry, which the CHANGELOG's own text confirms exists and contains the `Correction (v8.18.0, 2026-08-29)` note
- Independently re-derived (not inherited) the three facts behind `docs/ARCHITECTURE.md`'s gate-surface paragraph — see Deviations/Decisions below — and corrected the paragraph's final sentence to state a true strict-superset relation whose arithmetic closes at 20
- Re-ran the full whole-tree verification chain after the ARCHITECTURE.md edit: `sync-content.py --check` (exit 0, no drift), `check-version-stamps.py` (17 stamps, all `8.18.0`, PASS), `check-traceability.py --self-test` (`V818-ROWS PASS` x6), `check-links.py --self-test` and live (both PASS), and the full firewall battery

## Task Commits

Each task was committed atomically:

1. **Task 1: Remove the invisible soft hyphen and repair the stale CHANGELOG citation** — `64e64a4` (fix)
2. **Task 2: Correct the gate-surface paragraph in docs/ARCHITECTURE.md and re-confirm the whole tree** — `f370393` (docs)

**Plan metadata:** (this SUMMARY commit)

## Files Created/Modified

- `docs/v8.18-praor-loop-closure.md` — removed the single U+00AD soft hyphen inside the `FIREWALL: RED` backticked literal (SHIP-06 paragraph); no other character changed
- `docs/README.md` — v8.18 milestone-index row's CHANGELOG citation changed from `the \`CHANGELOG.md:355\` correction note` to `the correction note inside the \`## [8.17.2]\` CHANGELOG entry`
- `docs/ARCHITECTURE.md` — the canonical gate-surface paragraph's final sentence replaced: the false "CI additionally runs VAL-01" claim (which implied the battery does not run it) and the arithmetic that only summed to 19 are both fixed; the already-correct opening clause (`**17 in CI**` / `**20 tallied in the offline battery**` / `**1 pre-commit**`) was left byte-unchanged

## Independently derived facts (Task 2)

Per the plan's instruction to re-derive rather than trust the planner's own numbers, and to record method + result for each:

| Fact | Method | Result | Matches planner? |
|------|--------|--------|-------------------|
| CI job count in `.github/workflows/validation.yml` | `grep -n "^  [a-zA-Z0-9_-]*:$"` over the file, filtering out the `on:` trigger keys (`push:`, `pull_request:`) — lists every top-level job key including `pointer-drift-guard`, whose `name:` is the bare `GATE-02-v8.5` with no parenthesised id (confirmed this would be undercounted by a naive `grep -c "name:.*("`) | **17** jobs (`plugin-validate`, `markdownlint`, `check-links`, `check-trigger-collisions`, `check-version-stamps`, `check-install-collisions`, `check-description-budget`, `sync-check`, `pointer-drift-guard`, `check-agent`, `check-routing-battery`, `check-step0-emulator`, `check-step0-live`, `check-traceability`, `check-act-limb`, `check-loop-closure`, `check-focused-parity`) | Yes |
| Battery's tallied total | `grep -n '^gate "'` and `grep -n '^gate_prereq "'` (and the indented mutually-exclusive VAL-03 pair) over `scripts/check-firewall-battery.sh`, counting distinct gate IDs (VAL-03's `gate`/`gate_prereq` branches are mutually exclusive at runtime and counted as one slot, not two) plus a direct grep for `INVARIANT-CHECK`/`FROZEN-EVIDENCE` inline-check print sites | **18** distinct `gate`/`gate_prereq` registrations + **2** inline checks = **20** | Yes |
| Is VAL-01 registered in the battery? | `grep -c 'gate "VAL-01"' scripts/check-firewall-battery.sh` | **1** (yes, registered — the fact the old sentence denied) | Yes |

All three figures matched the planner's stated derivation (17, 20, yes), so the replacement text was applied as suggested (after a line-wrap reflow — see Deviations).

## Repo-wide U+00AD scan (Task 1)

Scanned every file returned by `git ls-files` ending in `.md`/`.py`/`.sh`/`.yml`/`.yaml`/`.json`, decoded as UTF-8, checked line-by-line for `chr(0xAD)`. **Total hits after the edit: 0.** (Before the edit, the one occurrence was `docs/v8.18-praor-loop-closure.md:140`, matching the plan's own repo-wide scan.)

## `CHANGELOG.md:355` disposition table

| # | File | Disposition | Justification |
|---|------|-------------|----------------|
| 1 | `docs/README.md:192` | Fixed | The only surviving hit; replaced with a citation naming the containing `## [8.17.2]` entry instead of a line number |

No other occurrences were found repo-wide (`docs/`, `CLAUDE.md`, `scripts/`, `CHANGELOG.md` all scanned; `grep -rn "CHANGELOG.md:355" ... | wc -l` returns `0` after the fix). No `historical` classification was needed — the single hit was a live, active claim, not a dated record quoting a past decision's own wording.

## Whole-tree gate re-confirmation (Task 2)

Run in order, each passing before the next:

1. `python3 scripts/sync-content.py --check` — exit 0, no output. PASS.
2. `python3 scripts/check-version-stamps.py` — `check-version-stamps: 17 stamps, all '8.18.0'`, `check-version-stamps: PASS`, exit 0. PASS.
3. `python3 scripts/check-traceability.py --self-test` — exit 0, `V818-ROWS PASS` present (6 sub-assertions). PASS.
4. `python3 scripts/check-links.py --self-test && python3 scripts/check-links.py` — both exit 0; live check reports `PASS (244 markdown links + 6 namespace refs across 127 files)`. PASS.
5. `bash scripts/check-firewall-battery.sh` — **verbatim final line:**

```
FIREWALL: BLOCKED (1 prerequisite(s) unmet; 19/20 passed)
```

Exit code: 2.

**This is the same documented `BLOCKED` outcome plans 04-07 and 04-08 reported for this worktree, not a gate failure and not a regression introduced by this plan.** The single unmet item is `[PREREQ] VAL-03`: no pytest-capable interpreter is available in this worktree checkout (`.venv/bin/python3` absent; bare `python3` on `PATH` has no `pytest` module). All 19 other gates printed `[PASS]`: `DUAL-04`, `GATE-02-v8.5`, `STEP0-06`, `STEP0-08`, `VAL-01`, `VAL-02`, `VAL-04`, `VAL-05`, `VERSION-01`, `GATE-01`, `BATT-06`, `TRACE-03`, `COLLIDE-01`, `QUAL-01`, `HARN-01`, `HARN-02`, `HARN-03`, plus the `INVARIANT-CHECK` and `FROZEN-EVIDENCE` inline checks. `VAL-01` in particular — the very gate this plan's Task 2 edit is about — printed `[PASS]` live, directly confirming the corrected paragraph's claim that it runs on both surfaces.

The `20` the corrected `docs/ARCHITECTURE.md` paragraph now claims matches the `19/20` denominator the battery itself prints (numerator withheld only by the unmet pytest prerequisite in this worktree, not by a wrong total).

`git diff --name-only HEAD~2 HEAD` lists exactly `docs/ARCHITECTURE.md`, `docs/README.md`, `docs/v8.18-praor-loop-closure.md` — matching the plan's `files_modified` list exactly, no more, no less.

## Deviations from Plan

1. **[Rule 1 - Formatting fix] Reflowed the plan's suggested replacement sentence for `docs/ARCHITECTURE.md` onto different line breaks than the first draft.** Found during Task 2. The plan's suggested prose, applied with a line break after "The battery is a strict", split the required literal `strict superset of CI` across two source lines (`...a strict\nsuperset of CI:...`), which made `grep -c "strict superset of CI"` return `0` instead of the acceptance criterion's required `1` — a single-line-source phrase does not match a phrase split across a newline. Fix: reflowed the same wording onto lines that keep `strict superset of CI` on one physical line. Verified: `grep -c "strict superset of CI"` now returns `1`; `grep -c "17 + 1 + 2 = 20"` (also line-break-sensitive) confirmed `1` on the first attempt since that phrase was not split. No wording was changed, only which words land on which line — the same defect class (and the same fix) plan 04-08 hit and recorded for two other sites. Files: `docs/ARCHITECTURE.md`. Commit: `f370393`.

No architectural deviations, no Rule 4 escalations, no auth gates, no stubs introduced.

## Issues Encountered

- `bash scripts/check-firewall-battery.sh` reports `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 19/20 passed)` for the same reason plans 04-07 and 04-08 documented: this worktree checkout has no `.venv` with `pytest` installed, and the bare `python3` on `PATH` cannot import it. Not fixed in-scope — this plan's `files_modified` is three documentation files only, and the fix (VAL-03's interpreter resolution) is out of scope and already shipped in Phase 3 (plan 03-08). The orchestrator's merge onto the main tree (which has a populated `.venv`) is expected to resolve it, matching the note both prior plans in this wave recorded.
- The plan's acceptance criterion for Task 2's final line ("`bash scripts/check-firewall-battery.sh` final line is exactly `FIREWALL: GREEN (20/20)`") could not be met in this environment for the reason above; the actual printed line (`FIREWALL: BLOCKED (1 prerequisite(s) unmet; 19/20 passed)`) is recorded verbatim above instead, per the executor's mandate to report the observed result rather than the expected one.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- All three backlog-triaged documentation defects from `04-VERIFICATION.md` are closed: the `FIREWALL: RED` literal is now greppable and copyable with no invisible character; `docs/README.md`'s CHANGELOG citation is stable under future insertions; and `docs/ARCHITECTURE.md`'s canonical gate-surface paragraph states a true superset relation with arithmetic that closes at the battery's actual 20.
- This plan is optional and droppable by design (its own frontmatter: `optional: true`, `gap_closure: true`); it did not touch any file plans 04-07 or 04-08 opened, and neither of `04-VERIFICATION.md`'s two failed verification truths depended on it.
- No version stamp moved (still `8.18.0`, 17/17). The `FIREWALL: BLOCKED` outcome is an environment condition affecting this worktree, not something this plan caused or can fix within its own scope.

---
*Phase: 04-ship*
*Completed: 2026-08-29*

## Self-Check: PASSED

- FOUND: `docs/v8.18-praor-loop-closure.md`
- FOUND: `docs/README.md`
- FOUND: `docs/ARCHITECTURE.md`
- FOUND: `.planning/phases/04-ship/04-09-SUMMARY.md`
- FOUND: commit `64e64a4` (Task 1)
- FOUND: commit `f370393` (Task 2)
