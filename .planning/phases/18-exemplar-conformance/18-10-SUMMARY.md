---
phase: 18-exemplar-conformance
plan: 10
subsystem: testing
tags: [python, bash, docs, self-test, ratchet, battery-header, conf-gate]

# Dependency graph
requires:
  - phase: 18-exemplar-conformance (plan 18-09)
    provides: run_live() call-site census, call-form lock, and independent literal locks for _CLAIM_FLOORS/_MARKED_RATCHET/_PRESCRIBED_LEAD_INS; control battery 18 -> 31
provides:
  - _MARKED_RATCHET widened to 4, summed over both gated surfaces (shared-examples + generated-twin), reconciled with docs/conformance-baseline.md's already-published figure
  - ratchet-fires-across-both-surfaces, a discriminating control that only passes under the widened filter
  - scripts/check-firewall-battery.sh's header restored to self-documenting (25 gates, CONF-GATE in roster, CONF-GATE Composition-change paragraph)
  - CLAUDE.md and docs/ARCHITECTURE.md CONF-GATE rows updated to the shipped 32-control count and the reconciled ratchet scope
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Two-place edit discipline exercised for the first time: _MARKED_RATCHET and its ratchet-value-locked control moved together in one commit"
    - "Discriminating control construction: a fixture chosen so it fires under the NEW filter but not the OLD one, so narrowing the filter back fails the control by name"

key-files:
  created: []
  modified:
    - scripts/check-conf-gate.py
    - scripts/check-firewall-battery.sh
    - CLAUDE.md
    - docs/ARCHITECTURE.md

key-decisions:
  - "Widened _MARKED_RATCHET to 4 (corpus-wide over both gated surfaces) rather than narrowing the published baseline sentence to shared-examples only, per the plan's pre-recorded decision — matches _targets_problems' existing both-surfaces shape and requires no docs/conformance-baseline.md regeneration"
  - "The wide-pattern sweep (\\b24\\b across CLAUDE.md/README.md/CONTRIBUTING.md/CHANGELOG.md/docs/) found no third current-fact battery-count hit beyond the one 18-VERIFICATION.md already named (CLAUDE.md:196); the two dated-history mentions (CLAUDE.md:161, CHANGELOG.md:30) are confirmed present and left byte-unchanged"

patterns-established:
  - "A ratchet control fixture must be DISCRIMINATING between the old and new enforcement scope, not merely a positive case, so narrowing the scope back fails the control by name rather than passing vacuously"

requirements-completed: [CONF-05, CONF-06]

# Metrics
duration: 55min
completed: 2026-09-05
---

# Phase 18 Plan 10: CONF-GATE Self-Documentation Reconciliation Summary

**Widened `_MARKED_RATCHET` from 2 to 4 (corpus-wide over both gated surfaces) to match the already-published baseline figure, repaired `check-firewall-battery.sh`'s stale header (24→25, CONF-GATE added to roster and Composition-change ledger), and fixed the one stale battery-count sentence and both CONF-GATE doc rows' control count — closing all three MINOR / non-blocking gaps `18-VERIFICATION.md` recorded.**

## Performance

- **Duration:** 55 min
- **Started:** 2026-09-05T11:05:00Z
- **Completed:** 2026-09-05T12:00:24Z
- **Tasks:** 3 completed
- **Files modified:** 4 (`scripts/check-conf-gate.py`, `scripts/check-firewall-battery.sh`, `CLAUDE.md`, `docs/ARCHITECTURE.md`)

## Accomplishments

- `_MARKED_RATCHET` moved 2 → 4, summed over `_GATED_SURFACES` (both `shared-examples` and `generated-twin`), matching `docs/conformance-baseline.md`'s "Disclosed bounds" §2 sentence exactly — code, comment, and published doc now state the same quantity over the same row set.
- Three inline ratchet fixtures retuned around the new pin (5/4/3); `ratchet-value-locked`'s two-place lock moved 2 → 4 in the same commit as the constant; a new discriminating control `ratchet-fires-across-both-surfaces` proves the surface widening is load-bearing. Control count 31 → 32.
- `scripts/check-firewall-battery.sh`'s header repaired: "24" → "25" in four places, CONF-GATE inserted into the 25-name roster, "21 of the 22" → "22 of the 23" non-inline arithmetic, and a CONF-GATE Composition-change paragraph added in the file's established house form (the eighth such addition; ends "Battery composition moved 24 -> 25").
- `CLAUDE.md`'s pre-commit-gate sentence ("the battery stays at 24") and both CONF-GATE doc rows (CLAUDE.md, docs/ARCHITECTURE.md) refreshed to the shipped `32-control` count and the reconciled corpus-wide-pinned-at-4 ratchet scope.
- Full N1-N3 neutralization ledger run on disposable scratch copies (`git status --porcelain` on the real tree confirmed empty before and after every scratch operation).

## Task Commits

Each task was committed atomically:

1. **Task 1: Widen the marked-claim ratchet to the corpus-wide quantity and reconcile it with its own comment and the published baseline sentence (WR-02)** - `c02113f` (feat)
2. **Task 2: Repair scripts/check-firewall-battery.sh's self-documenting header and add CONF-GATE's Composition-change paragraph** - `862d61d` (docs)
3. **Task 3: Fix the stale current-fact battery count in CLAUDE.md, refresh both CONF-GATE doc rows' control count, and re-sweep with a wider pattern than 18-08's** - `3d6b5c9` (docs)

**Plan metadata:** (this commit — SUMMARY.md, staged next)

## Files Created/Modified

- `scripts/check-conf-gate.py` - `_MARKED_RATCHET` 2 → 4, `_ratchet_problems` filter widened to `_GATED_SURFACES`, three fixtures retuned, `ratchet-value-locked` moved to 4, `ratchet-fires-across-both-surfaces` added. Control count 31 → 32.
- `scripts/check-firewall-battery.sh` - Header count corrections (24 → 25 in four places), CONF-GATE added to the 25-name roster, CONF-GATE Composition-change paragraph added. Comment-only edit; no executable line changed.
- `CLAUDE.md` - Pre-commit-gate parenthetical 24 → 25; CONF-GATE row's control count 18 → 32 plus the reconciled ratchet scope and a census/call-form-lock disclosed-bound clause.
- `docs/ARCHITECTURE.md` - CONF-GATE row's control count 18 → 32 plus the reconciled ratchet scope, targeted substitution only.

## Decisions Made

- **WR-02 fork:** widened `_MARKED_RATCHET` to the corpus-wide quantity (4) rather than narrowing the published baseline sentence to shared-examples only. Reasons recorded in the plan and confirmed live: narrowing would leave `generated-twin` a declared gated surface with no ratchet (the scope hole WR-02 names); the baseline sentence is rendered from `rows` at run time, so narrowing it means editing generated prose to under-state a derived reading; and widening needed no `docs/conformance-baseline.md` or `docs/data/conformance.json` regeneration, confirmed by `report-conformance.py --check` staying green with zero diff.
- The wide-pattern sweep used a deliberately broader regex (`\b24\b` across `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `docs/`) than 18-08's narrow `24/24|24 tallied|all 24 battery`, which is what let `CLAUDE.md:196` through undetected. The wider sweep found no third current-fact hit.

## Deviations from Plan

None — plan executed exactly as written. All three tasks landed at their specified targets (control count 32; battery header 25/25 with CONF-GATE Composition-change paragraph; both doc rows reconciled).

One recorded observation, not a deviation: the plan's Task 2 `<read_first>` section states "the seven existing `Composition change (...)` paragraphs are at lines 56, 63, 71, 85, 117, 128, 140 and 153" — that list is eight line numbers, not seven, and the live tree confirms eight prior paragraphs (HARNESS-01, TEARDOWN-01, the 2026-08-16 audit stream 0, HARN-04, HC-BOUND, REG-GUARD, PROV-GUARD, SCAN-GUARD). Task 2's acceptance criterion ("`grep -c \"Composition change (\"` returns `8`") inherits the same off-by-one and is measured to return `9` (eight prior + CONF-GATE) on the live tree — verified by listing all nine matched lines below. This is an arithmetic slip in the plan text, not a defect in the shipped header; the header itself is internally consistent (25 gates, 9 Composition-change paragraphs tracking 9 gate additions across the file's history, since the file started counting from a non-zero baseline before any paragraph existed).

## Neutralization Ledger (verbatim, N1-N3 per the phase's verify-by-mutation discipline)

All mutations below were applied on disposable `rsync -a --exclude .git` scratch copies under the session scratchpad. `git status --porcelain` on the real tree was confirmed empty (aside from this plan's own staged/committed edits) before and after every scratch-copy operation.

**Before Task 1:** `check-conf-gate: SELF-TEST PASS — 31 controls run`
**After Task 1:** `check-conf-gate: SELF-TEST PASS — 32 controls run`

**N1 — revert `_MARKED_RATCHET` to `2`, leaving the lock at `4`:**
```
check-conf-gate: SELF-TEST FAIL [ratchet-passes-at-pin] —
check-conf-gate: SELF-TEST FAIL [ratchet-passes-below] —
check-conf-gate: SELF-TEST FAIL [ratchet-value-locked] — 2
check-conf-gate: SELF-TEST FAIL [ratchet-fires-across-both-surfaces] — ['MARKED-CLAIM RATCHET VIOLATION: 5 > pinned 2']
RC=1
```
`[ratchet-value-locked]` fires as required — proves the two-place edit is enforced. (The other three failures are a side effect of reverting only the constant while the surrounding fixtures stay calibrated to 4; `[ratchet-value-locked]` is the acceptance-criterion-named failure.)

**N2 — revert `_ratchet_problems`' filter to `r["surface"] == "shared-examples"`:**
```
check-conf-gate: SELF-TEST FAIL [ratchet-fires-across-both-surfaces] — []
RC=1
```
Fails exactly the discriminating control by name — proves the surface widening is load-bearing, not cosmetic.

**N3 — raise a real reading on the corpus.** On a scratch copy, converted a currently-cited claim in `shared/examples/personal-general.md` (item 1 under `## 6. Conclusion`, `1. (chain C2) Verify, through direct conversations...`) into an uncited, marked claim by replacing its `(chain C2)` citation with `(no chain — flagged assumption only)`, ran `python3 scripts/sync-content.py --write`, then `python3 scripts/check-conf-gate.py`:
```
check-conf-gate: FAIL — MARKED-CLAIM RATCHET VIOLATION: 6 > pinned 4
RC=1
```
Exact match to the plan's specified acceptance output. (Note: simply *appending* the marker phrase to an already-cited claim's text, without removing its citation, was tried first and did NOT raise the marked count — `_claim_is_traced` traces on the chain citation regardless of marker presence, and `marked_untraced_claims` is a subset of already-untraced claims. The reproduction above removes the citation, which is what actually converts a traced claim into a marked-untraced one; this is the live proof the widened ratchet fires on the real corpus, not only on synthetic rows.)

`git status --porcelain` on the real tree: empty before and after every scratch operation in all three neutralizations.

## Three-Way Agreement (verbatim, as required by Task 1's acceptance criteria)

- **Code:** `_MARKED_RATCHET: int = 4` — `_ratchet_problems` sums `marked_untraced_claims` `for r in rows if r["surface"] in _GATED_SURFACES and r["section_resolution"] == "OK"`.
- **Constant's comment:** "The marked_untraced_claims sum over BOTH gated surfaces (_GATED_SURFACES): shared-examples 2 + generated-twin 2 = 4 ... This is exactly the figure docs/conformance-baseline.md's 'Disclosed bounds' §2 already publishes and names as pinned by this constant, so the code and the published sentence now state the same quantity over the same row set."
- **`docs/conformance-baseline.md:37`:** "**2. Marked-claim residual (derived) — a ratchet as of Phase 18 (CONF-GATE).** 4 claim(s) across shared-examples and generated-twin carry the `no chain — flagged assumption only` marker (shared-examples: 2, generated-twin: 2) ... it is now pinned by `scripts/check-conf-gate.py`'s `_MARKED_RATCHET`: the reading may fall, never rise."

All three state 4, over the same row set (shared-examples + generated-twin), unchanged by this plan (docs/conformance-baseline.md was not edited, confirmed by `report-conformance.py --check` reporting no drift).

## Battery Roster Name Count

The line 19-23 roster after Task 2's edit contains exactly **25** whitespace-separated gate names:
```
DUAL-04, GATE-02-v8.5, STEP0-06, STEP0-08, VAL-01,
VAL-02, VAL-03, VAL-04, VAL-05, VERSION-01,
GATE-01, BATT-06, TRACE-03, COLLIDE-01, QUAL-01,
HARN-01, HARN-02, HARN-03, HC-BOUND, REG-GUARD,
PROV-GUARD, SCAN-GUARD, CONF-GATE, INVARIANT-CHECK, FROZEN-EVIDENCE
```
Verified by tokenizing the five roster lines and counting non-`#` tokens: 25.

## Wide-Pattern Sweep (full hit list and disposition)

Command run: `/usr/bin/grep -rn -E "\b24\b" --include=*.md CLAUDE.md README.md CONTRIBUTING.md CHANGELOG.md docs/`

70 raw hits across `CLAUDE.md`, `CHANGELOG.md`, `docs/audit-2026-08-16-duplication-staleness.md`, `docs/use-journal.md`, `docs/v8.7-constraint-teardown.md`, `docs/README.md`, `docs/conformance-baseline.md`, `docs/requirements-matrix.md`, `docs/requirements-traceability.md`, `docs/v8.0-final-closure.md`, `docs/ARCHITECTURE.md`. `README.md` and `CONTRIBUTING.md` had zero hits.

Filtered by hand for any hit whose sentence is a CURRENT-FACT statement about the firewall battery's gate count or composition:

| File:Line | Sentence (excerpt) | Disposition |
|---|---|---|
| `CLAUDE.md:196` | "the battery ... stays at 24" (pre-commit conformance-baseline gate note) | **FIXED** in Task 3 → "stays at 25" |
| `CLAUDE.md:161` | GATE-01 row: "a `60 → 20` edit previously passed all 24 battery gates undetected" | **Left as dated history** — a Phase-15-era measurement, true as written; `git diff CLAUDE.md \| grep -c "60 → 20"` returns 0 |
| `CHANGELOG.md:30` | `[8.26.0]` entry: "the firewall battery tally stays **24/24**" | **Left as dated history** — a frozen release entry; `git diff CHANGELOG.md` is empty |
| `CHANGELOG.md:31` | "SCAN-GUARD ... already moved it 23 to 24" | **Left as dated history** — same `[8.26.0]` entry as above, not a current-fact statement |

Every other hit among the 70 is either: a `v8.24`/`v8.24.0` milestone-version stamp (`CLAUDE.md:37-38,173,179,240`; `docs/requirements-matrix.md`, `docs/requirements-traceability.md`, `docs/v8.0-final-closure.md`, `docs/README.md`); a control count unrelated to the battery gate count (PROV-GUARD's "24 controls" at `CLAUDE.md:37,173`; `CHANGELOG.md:308`; `docs/audit-2026-08-16-duplication-staleness.md:441,469-470`); a row/date/hour figure with no battery meaning (`CHANGELOG.md:109,778,896,1025-1027,1043,1161`; `docs/audit-2026-08-16-duplication-staleness.md:88,531`; `docs/use-journal.md:6,131`; `docs/v8.7-constraint-teardown.md:153`; `docs/README.md:28,38,46,56`); or `CLAUDE.md:158,167,186` and `docs/ARCHITECTURE.md:137,146,152` naming v8.24-registered gates or the already-correct "moved it 22 to 23"/"currently 25/25" current-fact statements. No third current-fact battery-count hit was found — the sweep confirms `18-VERIFICATION.md`'s minor gap 2 named the only residual.

## Overall Verification (plan `<verification>` block, run in order after all three tasks)

```
1. python3 scripts/check-conf-gate.py --self-test
   -> check-conf-gate: SELF-TEST PASS — 32 controls run

2. python3 scripts/check-conf-gate.py
   -> check-conf-gate: COVERAGE — measured 28 artifacts across shared-examples, generated-twin
      D-08(a)/(b)/(c) arms all fire correctly
      check-conf-gate: PASS (live marked sum 4, at the pin of 4)

3. python3 scripts/report-conformance.py --check
   -> report-conformance: PASS — no drift (rc 0)

4. python3 scripts/check-registration.py --self-test && python3 scripts/check-registration.py
   -> both PASS, rc 0

5. python3 scripts/check-quality-harness.py --self-test
   -> rc 0; chain_detector_pin / conclusion_claims_pin / slice_sections_pin all PASSED

6. git diff --stat scripts/check-quality-harness.py
   -> (empty — CONTRACT-06 untouched)

7. python3 scripts/sync-content.py --check
   -> rc 0 (no shared/ edit; no-op pass)

8. bash scripts/check-firewall-battery.sh
   -> FIREWALL: GREEN (25/25)

9. git status --porcelain
   -> (empty; all changes committed across the three task commits)
```

**Environment note (not a deviation):** `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 24/25 passed)` because this worktree had no `.venv` with pytest for VAL-03's third leg (a fresh worktree per `18-CONTEXT.md`'s prior-wave note). Ran `uv sync` (the CLAUDE.md-documented remedy) to create `.venv`, after which the battery reported `FIREWALL: GREEN (25/25)`. No code or gate behavior was changed.

## Issues Encountered

None beyond the plan-arithmetic observation recorded above (Task 2's "seven"/"8" off-by-one, which does not affect the shipped header's correctness) and the environment note above.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- All three MINOR / non-blocking gaps `18-VERIFICATION.md` recorded are closed: the marked-claim ratchet is reconciled at 4 across code/comment/baseline; the battery header is self-documenting at 25 gates with CONF-GATE's Composition-change paragraph; no current-fact battery-count statement in the tracked tree reads 24.
- Battery GREEN 25/25; `check-quality-harness.py` byte-unchanged (CONTRACT-06 intact); `report-conformance.py --check` and `sync-content.py --check` both rc 0 with no regeneration; `git status --porcelain` clean.
- No blockers. This was the second of the milestone's rework-cap-limited gap-closure plans (ROADMAP guardrail 2); no further gap-closure plans are authorized without new verification findings.

## Self-Check: PASSED

- FOUND: `scripts/check-conf-gate.py`
- FOUND: `scripts/check-firewall-battery.sh`
- FOUND: `CLAUDE.md`
- FOUND: `docs/ARCHITECTURE.md`
- FOUND: `.planning/phases/18-exemplar-conformance/18-10-SUMMARY.md`
- FOUND: `c02113f` (Task 1 commit)
- FOUND: `862d61d` (Task 2 commit)
- FOUND: `3d6b5c9` (Task 3 commit)

All claimed files and commits verified present via direct filesystem check and `git log`.

---
*Phase: 18-exemplar-conformance*
*Completed: 2026-09-05*
