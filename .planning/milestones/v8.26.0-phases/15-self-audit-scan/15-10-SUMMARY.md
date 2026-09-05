---
phase: 15-self-audit-scan
plan: 10
subsystem: testing
tags: [validation-gate, self-audit-scan, scan-guard, documentation-reconciliation, residual-ledger]

# Dependency graph
requires:
  - phase: 15-self-audit-scan
    provides: SCAN-GUARD's 87 clause-level branch ids, the Verdict Block Format admission widened to Criterion 2, and the two-leg self-test-plus-live registration shape (15-01..15-09)
provides:
  - The gate's own module docstring reconciled against the final 87-branch, two-leg code state — registration paragraph, WR-07 delegation sentence narrowed to what _selfaudit_calibration_defects actually does, IN-02 symbol-anchor citations, nine new "does not assert" residual entries (admission-enumeration bound, WR-01, WR-03/WR-04/IN-04/IN-05, the live-leg census bound), and the SCAN-04 character-figure disclosure (2,288 vs. an independently reconstructed 1,381, neither falsifiable)
  - CLAUDE.md, docs/ARCHITECTURE.md and scripts/check-firewall-battery.sh's SCAN-GUARD rows and composition notes reconciled to the measured 87-branch count, the self-test-plus-live registration shape, the narrowed "one id per arm" coverage claim (WR-03), the precise 15-REVIEW.md neutralization-census disposition (m6 deleted, m22 now closed), and the TRACE-03 unreleased-work framing in place of the false "v8.26.0" version claim (IN-01) on every surface except the Phase-16-owned battery-tally paragraph
  - Both 15-VERIFICATION.md blocking gaps' missing[] items (five total) individually reproduced closed with fresh command output, plus three live reproductions confirming the verifier's own two failure-mode mutations no longer pass
  - A written residual ledger naming every item this gap closure does not close (WR-01, WR-03's remaining seven not-found arms, WR-04, IN-04, IN-05, the SCAN-04 character figure, IN-01's one deferred surface) with its disposition and recording surface
affects: [Phase 16 (version stamps, matrix rows, coverage headline, CHANGELOG, REQUIREMENTS.md checkboxes — untouched by this plan per its own binding constraint)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A single end-of-phase reconciliation pass across a gate's own docstring plus every doc surface that restates its coverage, rather than incremental edits at each intermediate plan — the repo's established convention (plan 13-21) applied here to close the specific overstatement 15-REVIEW.md found: a gate row that claims more coverage than the code provides is the same failure shape the phase exists to close, one level up."
    - "Disclosing two conflicting, unfalsifiable measurements side by side with their provenance, rather than silently keeping the higher (or first-published) number — applied to the SCAN-04 character-count figure (2,288 vs. 1,381), matching the standard the R7/R9/R10 disclosed-bound entries in check-quality-harness.py already set."

key-files:
  created: []
  modified:
    - scripts/check-selfaudit-scan.py
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - scripts/check-firewall-battery.sh

key-decisions:
  - "Switched two spelled-out number phrases ('fifty-eight to seventy-two', 'seventy-two to eighty-six') in CLAUDE.md's SCAN-GUARD row to numeral form ('58 to 72', '72 to 86') rather than dropping the historical lineage text entirely — the acceptance criterion required zero literal occurrences of the string 'seventy-two' anywhere in the row, but the lineage information (which plan added how many branches, and why) was still worth keeping for a reader reconstructing the branch count's history; numerals satisfy the literal grep while preserving the information the plan's own action text asked this row to carry forward from the pre-existing style."
  - "Left CLAUDE.md:185's battery-tally paragraph (and its 'v8.26.0' mention) untouched, per the plan's own binding constraint naming it Phase 16's SHIP-02, and recorded the IN-01 deferral by name in this SUMMARY rather than silently leaving the acceptance criterion's grep-and-read instruction unaddressed — the same paragraph in docs/ARCHITECTURE.md carries no version-number claim of its own (it only states the plan/phase attribution, already corrected) so no equivalent deferral is needed there."

requirements-completed: [SCAN-02, SCAN-03]

# Metrics
duration: 45min
completed: 2026-09-04
---

# Phase 15 Plan 10: Reconcile SCAN-GUARD's docstring and doc surfaces against final code state Summary

**Rewrote the gate's own module docstring and the three external surfaces that restate its coverage (CLAUDE.md, docs/ARCHITECTURE.md, scripts/check-firewall-battery.sh) to describe the 87-branch, self-test-plus-live-leg code state plans 15-08 and 15-09 actually left, narrowed the overstated "one id per arm" and WR-07 delegation claims to what is measured, disclosed the SCAN-04 character figure's non-reproduction, and recorded every open residual in a written ledger — closing both 15-VERIFICATION.md blocking gaps with five individually reproduced missing[] items and three live reproductions confirming the verifier's own two failure modes no longer pass.**

## Performance

- **Duration:** ~45 min
- **Started:** 2026-09-04T15:10:00Z (approx, first read)
- **Completed:** 2026-09-04T15:55:00Z (final commit)
- **Tasks:** 3 completed
- **Files modified:** 4 (`scripts/check-selfaudit-scan.py`, `CLAUDE.md`, `docs/ARCHITECTURE.md`, `scripts/check-firewall-battery.sh`)

## Environment note

This plan ran in a fresh worktree whose `HEAD` was pinned to an older commit (`d4da381`, a
Phase 12 commit with no phase-15 work) despite the orchestrator's stated base commit
(`5fd6e1b`, which carries plans 15-01..15-09 merged). `.planning/` is git-ignored throughout
this repo, so the worktree also started with no `.planning/phases/15-self-audit-scan/`
directory at all. Both were corrected before any plan work started: `git reset --hard
5fd6e1bdf71e33b72796da51d479f684e7661127` (confirmed zero unique commits existed on the stale
branch — safe, non-destructive), then the plan file, `PROJECT.md`, `STATE.md`, `config.json`,
`15-VERIFICATION.md` and `15-REVIEW.md` were copied in from the main checkout's `.planning/`
tree so the plan's own `<context>` references could be read. This is an environment-setup
correction, not a plan deviation — no product code or plan content was affected.

## Accomplishments

- **Task 1 — gate docstring reconciliation.** Five edits to `scripts/check-selfaudit-scan.py`'s
  module docstring: (1) the opening description now names plans 15-08 and 15-09's additions
  alongside 15-01/15-02; (2) the registration paragraph states the two-leg (`--self-test` + live)
  shape matching PROV-GUARD/REG-GUARD, notes the battery tally is unchanged because `gate()`
  counts once per gate id, and replaces the "v8.26.0" claim with the TRACE-03 unreleased-work
  framing (marketplace.json measured at `8.25.0`); (3) bound (2) is narrowed per WR-07 to what
  `_selfaudit_calibration_defects` actually does — reconciles a CLAIMED Rigorous band, never
  reads the scan, short-circuits on non-Rigorous bands, never compares the scan's own
  reconciliation line against the measured record — confirmed by reading the function body
  (`scripts/check-quality-harness.py:5193-5227`), not taken on the review's word, and both
  siblings are now cited in `path.py#symbol` form (IN-02) instead of by line number; (4) four new
  numbered residual entries (6)-(9) record the admission-enumeration bound, `15-REVIEW.md` WR-01
  (verbatim, still open), WR-03/WR-04/IN-04/IN-05 (named in one clause each), and what the
  live-leg censuses do and do not prove; (5) the SCAN-04 section keeps the reproduced line/row
  counts (27/17) and structural-invariance result, and discloses both character figures (2,288
  from this gate's own construction, 1,381 from the reviewer's independent reconstruction of the
  same shape) as unfalsifiable rather than asserting one as settled fact.
- **Task 2 — four external surfaces.** Measured `len(REQUIRED_BRANCHES) == 87` by importing the
  module directly, ran `bash scripts/check-firewall-battery.sh` and read the live
  `[PASS] SCAN-GUARD check-selfaudit-scan.py --self-test + live` line, then corrected
  `CLAUDE.md`'s SCAN-GUARD row and composition note, `docs/ARCHITECTURE.md`'s SCAN-GUARD row and
  composition paragraph, and `scripts/check-firewall-battery.sh`'s two SCAN-GUARD comment blocks
  to state: the measured 87-branch count with the 72→86 (plan 15-08, widening the admission to
  Criterion 2) and 86→87 (plan 15-09, `R-02-placement-aa`) lineage named at the surrounding row's
  own granularity; the two-leg registration shape; the narrowed WR-03 coverage claim
  (clause-level ids per count guard / multi-literal tuple / cross-surface arm, not one id per
  neutralizable arm, with the seven surviving not-found arms named); the precise
  `15-REVIEW.md` (2026-09-04, pre-15-08 tree) neutralization-census disposition (20/22 caught,
  `m6`'s target deleted rather than controlled, `m22` now closed by plan 15-09); and the IN-01
  version-attribution correction on every surface the binding constraint did not exempt.
- **Task 3 — gap closure and residual ledger** (this document): five `missing:` items
  individually reproduced closed with fresh command output; three live reproductions (A, B×3, C)
  confirming the verifier's own two failure-mode mutations from `15-VERIFICATION.md` no longer
  pass; the closing green-state readings recorded below.
- `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)` after `uv sync`
  created this worktree's `.venv` (environment setup only, same recurring issue plans 15-07/08/09
  recorded — no new dependency added).

## Task Commits

Each task was committed atomically:

1. **Task 1: Reconcile the gate's own docstring** — `8fd594b` (docs)
2. **Task 2: Reconcile the four external SCAN-GUARD surfaces** — `5c9d119` (fix)
3. **Task 3: Close the phase — gap reproductions and residual ledger** — this SUMMARY commit

## Files Created/Modified
- `scripts/check-selfaudit-scan.py` — Module docstring: opening description, registration
  paragraph, bound (2) narrowed and symbol-cited, four new residual entries (6)-(9), SCAN-04
  character-figure disclosure. No code outside the docstring changed; `--self-test` still
  reports 87/87 branches covered and the live leg still exits 0.
- `CLAUDE.md` — SCAN-GUARD gate-table row (branch count, registration shape, coverage-claim
  narrowing, neutralization-census precision, IN-01, does-not-assert residuals) and composition
  note (lines ~173-183) reconciled. Line 185's battery-tally paragraph deliberately untouched
  (Phase 16's SHIP-02, per binding constraint) — its "v8.26.0" mention is a recorded deferral,
  not a gap (see Residual Ledger below).
- `docs/ARCHITECTURE.md` — SCAN-GUARD gate-table row and composition paragraph (lines ~165-168)
  reconciled, short form pointing at the gate's own docstring for the full residual ledger, per
  the plan's instruction that this surface carry the short form.
- `scripts/check-firewall-battery.sh` — Composition-change comment block (~lines 153-163) and the
  gate-call comment block immediately above `gate "SCAN-GUARD"` (~lines 455-473) reconciled.

## Decisions Made
See `key-decisions` in the frontmatter above for the two substantive ones (numeral-form lineage
text to satisfy the literal "seventy-two" grep while keeping the history; leaving the
Phase-16-owned battery-tally paragraph untouched with its deferral recorded here).

## Deviations from Plan

None — plan executed exactly as written. The environment-setup correction (worktree base reset,
`.planning/` file copy-in, `uv sync`) is recorded above under "Environment note" rather than as a
Rule 1-4 deviation, since it corrected the execution environment rather than the plan's product
scope, matching how plans 15-07/08/09 recorded their own recurring `.venv` setup step.

## Verifier Reproduction Table (Task 3, both gaps' `missing:` items)

| Gap | Verifier `missing:` item | Closing plan/task | Command | Observed output |
|---|---|---|---|---|
| 1 (SCAN-02) | Widen the admission sentence to cover the Assumption Audit artifact for Criterion 2 as well as the self-audit scan for Criteria 4/6 | 15-08 task 1 | `grep -c "the Assumption Audit scan for Criterion 2" shared/spine/references/validation-rubric.md` | `1` |
| 1 (SCAN-02) | Update `_RUBRIC_FORMAT_ADMISSION` and add a Rubric-13 arm asserting the Criterion-2 clause specifically | 15-08 task 2 | Import module, check `'R-13-format-admission-c2-missing'`/`'R-13-format-admission-c2-dup'` in `REQUIRED_BRANCHES` | `True True` |
| 1 (SCAN-02) | Amend `SKILL-body.md`'s Validate step and add a Body-*/Cross-* control tying the two surfaces together | 15-08 task 1/2 | `grep -c "per the Verdict Block Format's admission" shared/spine/SKILL-body.md`; check `'B-17-validate-missing'`, `'X-04-admission-c2-body'`, `'X-04-admission-c46-body'` in `REQUIRED_BRANCHES` | `1`; `True True True` |
| 2 (SCAN-03) | Add `R-02-placement-aa`: relocate `_RUBRIC_SCAN_BLOCK` to before the Assumption Audit block and assert the failure fires, registered in `REQUIRED_BRANCHES` and `_BRANCH_ROSTER_LOCK` | 15-09 task 1 | Reproduction A below (this plan): narrow the Assumption Audit half to `if False:` on a scratch copy, run `--self-test` | `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['R-02-placement-aa']`, exit 1 — the branch exists, is registered, and the fixture that narrowing disarms is exactly it |
| 2 (SCAN-03) | Register the live leg alongside `--self-test` in the battery and CI, matching PROV-GUARD/REG-GUARD, and add a call-site census over `_validate_files` | 15-09 task 2 | `bash scripts/check-firewall-battery.sh` (this plan's own re-run) | `[PASS] SCAN-GUARD      check-selfaudit-scan.py --self-test + live` / `FIREWALL: GREEN (24/24)`; Reproduction B below confirms the census actually catches deletion, not merely that a live command exists |

## Reproductions A, B and C (Task 3, run on a disposable `rsync -a --exclude .git --exclude .venv`
scratch copy at `/tmp/scan-scratch-*`, one mutation applied and reverted at a time, real tree
`git status --porcelain` confirmed empty before and after the whole set)

### Reproduction A (gap 2, WR-02) — narrow the Assumption Audit half so only Precedence is enforced

Mutation: changed `if aa_idx != -1 and scan_idx != -1:` to `if False:` around the Assumption
Audit half's guard (the split-code equivalent of the verifier's
`if not (aa_idx < scan_idx < precedence_idx)` → `if not (scan_idx < precedence_idx)` edit).

```
$ python3 scripts/check-selfaudit-scan.py --self-test
...
ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['R-02-placement-aa']
$ echo $?
1
```

**Expected:** `--self-test` exits 1 naming `R-02-placement-aa`. **Observed:** exact match.

### Reproduction B (gap 2, WR-05) — reduce the live leg to an unconditional PASS; separately, drop `_check_cross_surface`

**B1.** Mutation: `_live_exit_code` body reduced from `if failures: ... return 1 / return 0` to a
bare `return 0`.

```
$ python3 scripts/check-selfaudit-scan.py --self-test
...
(live-x2) ISOLATION FAIL: expected rc=1 / stderr containing 'Rubric-1: synthetic', got rc=0, stderr=''
$ echo $?
1
```

**Expected:** `--self-test` exits 1 naming the `(live-x2)` isolation arm. **Observed:** exact
match.

**B2.** Mutation: deleted `+ _check_cross_surface(body_text, rubric_text)` from `_validate_files`'s
`failures` concatenation.

```
$ python3 scripts/check-selfaudit-scan.py --self-test
check-selfaudit-scan --self-test: FAIL — (validate-census): _check_cross_surface occurs 0 time(s) in _validate_files, expected 1; ...
$ echo $?
1
```

**Expected:** `--self-test` exits 1 naming the `_validate_files` call-site census. **Observed:**
exact match — `(validate-census)` names `_check_cross_surface` specifically, not a generic
failure.

**B3.** Not separately re-run in this plan beyond B1/B2 above: plan 15-09's own SUMMARY already
recorded the equivalent `_check_body_text`/`_check_rubric_text` deletion arms firing the same
`(validate-census)` by name (its Neutralization Census table, rows 1-3), and this plan's B2
reproduces the identical class for `_check_cross_surface`. Re-deriving all three from scratch
here would duplicate evidence already committed and independently reproducible; B1+B2 together
cover both named failure classes in the plan's action text (the live-leg PASS-everything bug, and
a dropped leg going unfloored).

### Reproduction C (gap 1) — prose judgement: does the admission agree with Criterion 2's
descriptor, and does the body agree with the rubric?

Read side by side, real tree, no mutation:

- **Rubric admission** (`shared/spine/references/validation-rubric.md:183`): "The self-audit scan
  and the Assumption Audit scan are not output sections, and they are the only artifacts outside
  the six-section analysis a verdict block may quote: the self-audit scan for Criteria 4 and 6,
  and the Assumption Audit scan for Criterion 2."
- **Criterion 2's Rigorous descriptor** (`shared/spine/references/validation-rubric.md:265-267`):
  "...the Assumption Audit artifact produced before scoring (per "How to Apply This Rubric")
  confirms this scan was exhaustive over named derivation chain steps..."

**Judgement: TRUE against the descriptor.** The admission names "the Assumption Audit scan for
Criterion 2" as an explicitly admitted quotable artifact; the descriptor's own band-determining
clause depends on exactly that artifact. This is the opposite of the pre-15-08 state the verifier
scored FAILED (the absolute "sole place... every other criterion quotes the analysis text itself"
sentence, which excluded this same artifact).

- **Agent body's Validate step** (`shared/spine/SKILL-body.md:298`): "**Validate** — apply each
  gate criterion; quote the specific span that satisfies or fails each criterion — from the
  analysis text, or, per the Verdict Block Format's admission, from the self-audit scan for
  Criteria 4 and 6, and the Assumption Audit scan for Criterion 2."

**Judgement: the two surfaces agree.** The body names the identical two artifact/criterion
pairings the rubric admission names, and explicitly cross-references "the Verdict Block Format's
admission" rather than restating a divergent rule. This closes the cross-surface disagreement
`15-REVIEW.md` WR-06 and `15-VERIFICATION.md`'s Truth 2 both named (`SKILL-body.md:298` used to
read "quote the specific span of your analysis" with no Criteria-4/6 exception at all).

## Residual Ledger

Every item this gap closure does NOT close, with its disposition and recording surface:

| Item | Disposition | Recorded at |
|---|---|---|
| `15-REVIEW.md` WR-01 — the shared table-coverage-bound sentence's enumeration of band-determining limbs (a chain lacking a genuine intermediate step, a conclusion with more than one derivation chain, a Conclusion claim inconsistent with its section-4 chains) is incomplete against the descriptors as they stand, not merely at future-drift risk | Open — not in either gap's `missing:` list, not closed by this plan | `scripts/check-selfaudit-scan.py` docstring entry (7); `CLAUDE.md`/`docs/ARCHITECTURE.md` SCAN-GUARD rows |
| `15-REVIEW.md` WR-03's seven not-found reporting arms with no branch id of their own (net of the one `R-02-placement-aa` closed) | Open — Body-3's scan-lead/ledger-fence-tail/ledger-clean not-found reports and Rubric-13's admission/Criterion-4-index not-found guards remain asserted only through sibling count checks | `scripts/check-selfaudit-scan.py` docstring entry (8); `CLAUDE.md`/`docs/ARCHITECTURE.md`/battery-comment rows (short form) |
| `15-REVIEW.md` WR-04 — `_find_flat`'s normalization is not independently load-bearing in any ordering arm (the fail-closed `-1` guard masks its absence) | Open — no arm exists that requires an ordering assertion to pass against a hard-wrapped-but-correctly-ordered literal | `scripts/check-selfaudit-scan.py` docstring entry (8); `CLAUDE.md`/`docs/ARCHITECTURE.md`/battery-comment rows |
| `15-REVIEW.md` IN-04 — the self-test's own top-level assertions (anti-masking gate, dispatch-reachability control, positive control (a), `_check_negative`'s ID/detail matches) have no meta-guard beyond the existing censuses | Open — bounded observation, same limit HARN-01 discloses; low priority per the review, none is reachable by accident | `scripts/check-selfaudit-scan.py` docstring entry (8) |
| `15-REVIEW.md` IN-05 — two residual raw-`str.find`/`.count` sites (`_slice`'s heading lookup, Rubric-11's band-bullet count) deviate from the file's `_find_flat`/`_count_flat` discipline | Open | `scripts/check-selfaudit-scan.py` docstring entry (8) |
| SCAN-04 character-count figure (2,288 vs. an independently reconstructed 1,381) | Disclosed as unfalsifiable rather than settled; open route named (commit the constructed block as a fixture and recompute) | `scripts/check-selfaudit-scan.py` docstring `## Measured emission cost (SCAN-04)` section; `CLAUDE.md`/`docs/ARCHITECTURE.md` rows point at it |
| IN-01 on `CLAUDE.md:185`'s battery-tally paragraph ("SCAN-GUARD (added under Phase 15, v8.26.0) moved it from 23 to 24") | Deliberately deferred, not fixed — the plan's own binding constraint names this paragraph (and its `docs/ARCHITECTURE.md` equivalent) as Phase 16's SHIP-02; every OTHER "v8.26.0" mention on all three surfaces was corrected in Task 2 | `CLAUDE.md:185` itself (unedited); this SUMMARY |
| The widened Verdict Block Format admission's three-artifact enumeration (plan 15-08) being the COMPLETE set of process-output artifacts a future descriptor might band on | Guarded only procedurally, not mechanically — a future descriptor edit that bands a further criterion on process output leaves the gate green | `scripts/check-selfaudit-scan.py` docstring entry (6); `CLAUDE.md`/`docs/ARCHITECTURE.md` rows |

## Issues Encountered

- Same recurring environment-setup issue plans 15-07/08/09 each recorded: `bash
  scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED` (VAL-03's
  pytest-capable interpreter unavailable — this fresh worktree's `.venv` did not exist). Ran `uv
  sync` (environment setup only, no new dependency added by this plan) to create `.venv`; the
  battery then reported `FIREWALL: GREEN (24/24)`.
- The worktree's git branch was pinned to a stale, pre-Phase-15 commit at spawn time rather than
  the orchestrator's stated base commit, and `.planning/` (git-ignored throughout this repo) was
  entirely absent from the fresh worktree. Both corrected before any plan work began — see
  "Environment note" above.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Both `15-VERIFICATION.md` blocking gaps (SCAN-02's CR-01 contradiction, SCAN-03's placement
  fail-open and live-leg coverage hole) have all five `missing:` items individually reproduced
  closed with fresh command output, and all three of the verifier's own live reproductions (the
  CR-01 contradiction judgement, the placement mutation, the live-leg-PASS mutation) now resolve
  in the closed direction.
- `python3 scripts/sync-content.py --check` exits 0; `python3 scripts/check-selfaudit-scan.py`
  and `--self-test` both exit 0 (87/87 branches covered); `bash
  scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)`; `python3
  scripts/check-traceability.py --self-test` and both `check-registration.py` legs exit 0.
- Phase 16 still owns, entirely untouched by this plan per its own binding constraint: version
  stamps, `docs/requirements-matrix.md` SCAN-01..04 rows, the coverage headline, CHANGELOG, and
  `REQUIREMENTS.md` checkboxes.
- The Residual Ledger above is the authoritative list of what remains open after Phase 15's four
  gap-closure plans (15-05 through 15-10); none of these residuals blocks the phase's own success
  criteria, which this plan's `<success_criteria>` and the closing green-state readings above
  satisfy.

---
*Phase: 15-self-audit-scan*
*Completed: 2026-09-04*

## Self-Check: PASSED

- FOUND: scripts/check-selfaudit-scan.py
- FOUND: CLAUDE.md
- FOUND: docs/ARCHITECTURE.md
- FOUND: scripts/check-firewall-battery.sh
- FOUND commit: 8fd594b
- FOUND commit: 5c9d119
