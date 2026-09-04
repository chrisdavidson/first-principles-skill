---
phase: 15-self-audit-scan
plan: 08
subsystem: testing
tags: [validation-gate, self-audit-scan, scan-guard, verdict-block-format, anti-masking, clause-level-branches]

# Dependency graph
requires:
  - phase: 15-self-audit-scan
    provides: Verdict Block Format admission scoped to Criteria 4/6 only, SCAN-GUARD's 72 clause-level branch ids (15-01..15-07)
provides:
  - Verdict Block Format admission widened to the artifacts the criteria actually band on — the self-audit scan for Criteria 4 and 6, AND the Assumption Audit scan for Criterion 2 — replacing a false absolute claim ("the sole place a verdict block may quote something outside the six-section analysis") that SCAN-GUARD's own Rubric-13 gate-locked as a passing invariant
  - SKILL-body.md's Phase-5 Validate step amended to state the same rule, byte-identical to the rubric's two clauses, closing the cross-surface disagreement about whether Criteria 4/6 may quote the scan at all
  - SCAN-GUARD extended from 72 to 86 clause-level branch ids: Rubric-13's per-clause count guards (C4/6 half, C2 half) and its superseded-clause count-0 guard, a new Rubric-14 pinning Criterion 2's Assumption-Audit-artifact descriptor sentence, a new Body-17 pinning the amended/pre-amendment Validate step, and Cross-4's four single-surface admission-clause arms
  - Two new whitespace-tolerant fixture helpers (_flat_pattern, _mutate_within_range_flat, _duplicate_within_range_flat) for constructing negative controls against a hard-wrapped literal that has not been unwrapped (Criterion 2's Rigorous descriptor, untouched by binding constraint)
  - Both remaining 15-VERIFICATION.md blocking gaps (SCAN-02's CR-01 contradiction, the cross-surface Validate-step drift) closed and reproduced live
affects: [Phase 16 (version stamps, matrix rows, coverage headline, CHANGELOG, REQUIREMENTS.md checkboxes, doc-surface branch-count/registration-shape claims deferred to plan 15-10)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A gate literal that pins a superseded/false absolute claim at whole-file count 0, so a revert to the old wording fails the gate by name rather than silently restoring a green state that hides the regression (mirrors _RUBRIC_FORMAT_PREAMENDMENT/_BODY_DONOTPRESENT_PREAMENDMENT's existing shape, extended to the admission sentence itself)"
    - "A whitespace-tolerant fixture-mutation helper pair (_mutate_within_range_flat/_duplicate_within_range_flat), built from a shared _flat_pattern regex, for constructing negative controls against source prose that is hard-wrapped and deliberately NOT unwrapped by binding constraint — the existing raw-substring fixture helpers (_mutate_within_range, _duplicate_within_range) silently find zero occurrences against such text, which would have produced an AssertionError rather than a usable fixture"
    - "A truth census over an entire rubric section (grep for 'process output', 'before scoring', 'Assumption Audit', 'self-audit scan', 'closure ledger', 'artifact produced') run BEFORE writing an admission/scoping sentence, to enumerate every criterion that bands on an artifact outside the scored document — the check whose absence produced the CR-01 gap in the first place"

key-files:
  created: []
  modified:
    - shared/spine/references/validation-rubric.md
    - shared/spine/SKILL-body.md
    - first-principles/agents/first-principles.md
    - first-principles/agents/references/validation-rubric.md
    - scripts/check-selfaudit-scan.py

key-decisions:
  - "Added _mutate_within_range_flat/_duplicate_within_range_flat/_flat_pattern rather than unwrapping Criterion 2's Rigorous descriptor to match the file's other pinned literals — the plan's binding constraint requires the descriptor sentence to stay exactly as it is (acceptance criterion: 'git diff shows no change inside the Criterion 2 section'), and the existing raw-substring fixture helpers (_mutate_within_range, _duplicate_within_range) assert `count == 1` via a raw `str.count`, which returns 0 against the descriptor's hard-wrapped real newlines — a plain reuse of the existing helpers would have raised an AssertionError rather than producing the R-14 fixtures. This was not spelled out in the plan's action text (which cites _mutate_within_range/_duplicate_within_range by name for R-14) but follows directly from the plan's own binding constraint plus its read_first instruction to transcribe every literal from the shipped file rather than the plan prose."
  - "R-13's two clause-split guards (C4/6, C2) and the superseded-clause guard, R-14's descriptor guard, and B-17's Validate-step guard each cover TWO branch ids (missing + dup) from ONE `!= N` count-guard code location, matching the file's established convention (e.g. the pre-existing R-13-format-amended-missing/-dup pair, R-09-crit4-count-missing/-dup) — a single mutation therefore neutralizes both ids of a pair simultaneously in the census, which the SUMMARY's neutralization table records as one mutation covering two rows rather than fabricating two independent mutations for a shared guard."

requirements-completed: [SCAN-02]

# Metrics
duration: 55min
completed: 2026-09-04
---

# Phase 15 Plan 08: Widen the Verdict Block Format admission to cover Criterion 2's Assumption Audit artifact Summary

**Replaced the false absolute claim that the self-audit scan is "the sole place a verdict block may quote something outside the six-section analysis" with a widened admission naming both process-output artifacts a verdict block may quote — the self-audit scan for Criteria 4/6, and the Assumption Audit scan for Criterion 2 — amended the agent body's Validate step to match byte-identically, and extended SCAN-GUARD from 72 to 86 clause-level branch ids pinning both halves.**

## Performance

- **Duration:** ~55 min
- **Started:** 2026-09-04T13:34:37Z (approx, first read)
- **Completed:** 2026-09-04T13:48:26Z (final commit)
- **Tasks:** 3 completed
- **Files modified:** 5 (`shared/spine/references/validation-rubric.md`, `shared/spine/SKILL-body.md`, `first-principles/agents/first-principles.md`, `first-principles/agents/references/validation-rubric.md`, `scripts/check-selfaudit-scan.py`)

## Accomplishments

- Replaced the Verdict Block Format's false absolute admission sentence — "this is the sole place a verdict block may quote something outside the six-section analysis... every other criterion quotes the analysis text itself" — with a widened sentence naming both admitted artifacts: the self-audit scan for Criteria 4 and 6, and the Assumption Audit scan for Criterion 2. The §6→§4 closure-ledger exclusion is retained unchanged (D-03 stays intact).
- Ran the required truth census over the whole `## Criteria` section (searched for `process output`, `before scoring`, `Assumption Audit`, `self-audit scan`, `closure ledger`, `artifact produced`) and confirmed the exact set of criteria banding on an artifact outside the six-section analysis is {Criterion 2, Criterion 4, Criterion 6} — matching the widened admission exactly, with no fourth criterion found.
- Amended `SKILL-body.md`'s Phase-5 Validate step (item 1 of the numbered feedback-loop list) to state the same rule, with both clause literals byte-identical to the rubric's — closing the cross-surface disagreement where the body still restricted quoting to "the specific span of your analysis" after the rubric was amended.
- Confirmed by census that Criterion 2's Rigorous descriptor is byte-unedited (`git diff` inside the `### Criterion 2: Challenge Assumptions` section is empty) — the admission moved to match the descriptor, never the reverse, per the binding constraint.
- Extended SCAN-GUARD from 72 to 86 clause-level branch ids: Rubric-13's admission split into per-clause count guards (Criteria-4/6 half, Criterion-2 half, each missing+dup) plus a whole-file count-0 guard on the superseded 15-07 clause; a new Rubric-14 pinning Criterion 2's Assumption-Audit-artifact descriptor sentence (the sentence the admission's C2 clause depends on); a new Body-17 pinning the amended Validate step and the pre-amendment restriction's absence; and Cross-4's four single-surface arms asserting both admission clauses on both surfaces.
- Built two new whitespace-tolerant fixture helpers (`_flat_pattern`, `_mutate_within_range_flat`, `_duplicate_within_range_flat`) to construct R-14's negative controls against Criterion 2's hard-wrapped descriptor sentence, which the existing raw-substring fixture helpers cannot locate.
- Proved all fourteen new branches by neutralization on a disposable `rsync --exclude .git --exclude .venv` scratch copy: ten underlying assertions (some shared by a missing/dup id pair, matching the file's existing convention), each disarmed one at a time, each making `--self-test` fail naming exactly its own branch id(s).
- Re-verified both remaining `15-VERIFICATION.md` gap-1 blocking findings (the CR-01 contradiction, the cross-surface Validate-step drift) end to end; `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)`.

## Task Commits

Each task was committed atomically:

1. **Task 1: Widen the Verdict Block Format admission, amend the body's Validate step, run the truth census, regenerate** - `a083cb5` (fix)
2. **Task 2: Move SCAN-GUARD's pins onto the widened admission and add the Rubric-13 clause arms, Rubric-14, Body-17 and Cross-4** - `912d410` (test)
3. **Task 3: Add one negative control per new branch and prove each fires alone by neutralization** - `02c0ee9` (docs)

## Files Created/Modified
- `shared/spine/references/validation-rubric.md` — Replaced the Verdict Block Format admission paragraph with the widened two-artifact sentence; Criterion 2's Rigorous descriptor left byte-unedited.
- `shared/spine/SKILL-body.md` — Amended the Phase-5 Validate step (numbered list item 1) to state the same widened rule, byte-identical clause literals.
- `first-principles/agents/first-principles.md`, `first-principles/agents/references/validation-rubric.md` — Regenerated via `sync-content.py --write`.
- `scripts/check-selfaudit-scan.py` — New constants (`_RUBRIC_FORMAT_ADMISSION` rewritten, `_RUBRIC_FORMAT_ADMISSION_SUPERSEDED`, `_ADMISSION_SCOPE_C46`, `_ADMISSION_SCOPE_C2`, `_RUBRIC_C2_AA_ARTIFACT`, `_BODY_VALIDATE_STEP`, `_BODY_VALIDATE_PREAMENDMENT`, `_CRIT2_START`, `_CRIT3_START`); Rubric-13 extended with per-clause count guards and the superseded-clause count-0 guard; new Rubric-14 check; new Body-17 check; Cross-4's four new arms in `_check_cross_surface`; three new fixture helpers (`_flat_pattern`, `_mutate_within_range_flat`, `_duplicate_within_range_flat`); fourteen new branch ids registered in `REQUIRED_BRANCHES`/`_BRANCH_ROSTER_LOCK` (72→86) with matching negative controls.

## Decisions Made
See `key-decisions` in the frontmatter above for the two substantive ones (the whitespace-tolerant fixture helpers, and the shared-guard branch-pair convention).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - blocking issue] Built whitespace-tolerant fixture helpers for R-14's controls instead of reusing `_mutate_within_range`/`_duplicate_within_range`**
- **Found during:** Task 3, while writing R-14's negative controls.
- **Issue:** The plan's task 3 action text names `_mutate_within_range`/`_duplicate_within_range` generically for all new controls, and cites the existing R-13 controls (which operate on unwrapped, single-line literals) as the template. Criterion 2's Rigorous descriptor sentence — the target of R-14's fixtures — is hard-wrapped across three physical lines in the shipped source (the file's older prose convention) and is explicitly required to stay byte-unedited by this plan's binding constraint. `_mutate_within_range`/`_duplicate_within_range` locate their target via a raw `str.count`/`str.find`, which returns 0 against the wrapped text (confirmed: raw count 0 vs. `_count_flat` normalized count 1) — calling them as written would have raised an `AssertionError` rather than producing a usable fixture.
- **Fix:** Added `_flat_pattern` (builds a whitespace-tolerant regex from a literal by escaping it and collapsing single-space token boundaries to `\s+`) plus `_mutate_within_range_flat`/`_duplicate_within_range_flat`, which locate the target via that regex instead of a raw substring, and used them for R-14's two fixtures only. R-13, Body-17 and Cross-4's fixtures all use the existing raw-substring helpers unchanged, since their targets are single-line literals in the shipped source.
- **Files modified:** `scripts/check-selfaudit-scan.py`.
- **Verification:** `python3 scripts/check-selfaudit-scan.py --self-test` reports all 86 branches covered including `R-14-c2-descriptor-missing`/`-dup`; the neutralization census (below) independently confirms both R-14 controls fire correctly and fail closed when their own guard is disarmed; `git diff` confirms Criterion 2's Rigorous descriptor section is still byte-unedited after this change.
- **Committed in:** `02c0ee9` (Task 3).

---

**Total deviations:** 1 auto-fixed (Rule 3).
**Impact on plan:** Additive only — two new fixture-construction helper functions, used exclusively for R-14's controls. No existing helper, check function or pinned literal was modified. All Task 2/3 acceptance criteria (86-branch registry equality, live-leg green, self-test all-covered, no new raw `str.find`/`.count` in the CHECK functions) independently re-verified after the addition.

## Truth Census (Task 1, required by plan)

Searched the whole `## Criteria` section (`shared/spine/references/validation-rubric.md` lines 208-490) for the terms `process output`, `before scoring`, `Assumption Audit`, `self-audit scan`, `closure ledger`, `artifact produced`. Five hits, all inside exactly three criteria:

| Line | Criterion | Text |
|---|---|---|
| 262-267 | Criterion 2 | "...the Assumption Audit artifact produced before scoring (per \"How to Apply This Rubric\") confirms this scan was exhaustive..." |
| 361 | Criterion 4 | "Quoted span: where the band is determined by chain form or chain dependency, it must be drawn from the self-audit scan's chain-form table row..." |
| 460 | Criterion 6 | "Quoted span: where the band is determined by whether a section-6 claim traces to a named section-4 chain, it must be drawn from the self-audit scan's claim-inventory table row..." |

**Set found = {Criterion 2, Criterion 4, Criterion 6} — matches the widened admission's enumeration exactly.** No fourth criterion was found; the widening was not escalated to a scope decision.

## Verifier Reproduction Table (Task 3, gap-1 `missing:` items)

| Verifier `missing:` item | Command | Observed output |
|---|---|---|
| Widen the admission sentence to cover the Assumption Audit artifact for Criterion 2 | `grep -c "the Assumption Audit scan for Criterion 2" shared/spine/references/validation-rubric.md` | `1` |
| Update `_RUBRIC_FORMAT_ADMISSION` and add a Rubric-13 arm asserting the Criterion-2 clause specifically | Import module, check `'R-13-format-admission-c2-missing' in REQUIRED_BRANCHES` and `'R-13-format-admission-c2-dup' in REQUIRED_BRANCHES` | `True True` |
| Amend `SKILL-body.md`'s Validate step and add a Body-*/Cross-* control tying the two surfaces together | `grep -c "per the Verdict Block Format's admission" shared/spine/SKILL-body.md`; check `'B-17-validate-missing'`, `'X-04-admission-c2-body'`, `'X-04-admission-c46-body'` all `in REQUIRED_BRANCHES` | `1`; `True True True` |

## Neutralization Census (Task 3)

Run on a disposable `rsync -a --exclude .git --exclude .venv` scratch copy at `/tmp/.../scan-scratch`. Baseline `--self-test` on the scratch copy: exit 0. One mutation applied and reverted at a time via a Python driver script (backs up the target file, mutates, runs `--self-test`, captures the result, restores from backup). `git status --porcelain` confirmed empty in the real tree before and after the whole census.

Ten underlying assertions were mutated (some cover two branch ids — the missing/dup pair sharing one `!= N` count guard, matching this file's established convention, e.g. the pre-existing `R-13-format-amended-missing`/`-dup` pair):

| Mutation (guard changed to `if False:`) | Branch id(s) covered | Observed `--self-test` result | Exit code |
|---|---|---|---|
| `if c46_count != 1:` (Rubric-13) | `R-13-format-admission-c46-missing`, `R-13-format-admission-c46-dup` | `ANTI-MASKING GATE FAILURE: 2 branch(es) not covered: ['R-13-format-admission-c46-dup', 'R-13-format-admission-c46-missing']` | 1 |
| `if c2_count != 1:` (Rubric-13) | `R-13-format-admission-c2-missing`, `R-13-format-admission-c2-dup` | `ANTI-MASKING GATE FAILURE: 2 branch(es) not covered: ['R-13-format-admission-c2-dup', 'R-13-format-admission-c2-missing']` | 1 |
| `if superseded_count != 0:` (Rubric-13) | `R-13-format-admission-superseded` | `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['R-13-format-admission-superseded']` | 1 |
| `if c2_descriptor_count != 1:` (Rubric-14) | `R-14-c2-descriptor-missing`, `R-14-c2-descriptor-dup` | `ANTI-MASKING GATE FAILURE: 2 branch(es) not covered: ['R-14-c2-descriptor-dup', 'R-14-c2-descriptor-missing']` | 1 |
| `if validate_count != 1:` (Body-17) | `B-17-validate-missing`, `B-17-validate-dup` | `ANTI-MASKING GATE FAILURE: 2 branch(es) not covered: ['B-17-validate-dup', 'B-17-validate-missing']` | 1 |
| `if validate_preamendment_count != 0:` (Body-17) | `B-17-validate-preamendment` | `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['B-17-validate-preamendment']` | 1 |
| `if not _contains(body_text, _ADMISSION_SCOPE_C46):` (Cross-4) | `X-04-admission-c46-body` | `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['X-04-admission-c46-body']` | 1 |
| `if not _contains(rubric_text, _ADMISSION_SCOPE_C46):` (Cross-4) | `X-04-admission-c46-rubric` | `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['X-04-admission-c46-rubric']` | 1 |
| `if not _contains(body_text, _ADMISSION_SCOPE_C2):` (Cross-4) | `X-04-admission-c2-body` | `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['X-04-admission-c2-body']` | 1 |
| `if not _contains(rubric_text, _ADMISSION_SCOPE_C2):` (Cross-4) | `X-04-admission-c2-rubric` | `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['X-04-admission-c2-rubric']` | 1 |

All fourteen branch ids were named as uncovered by exactly one of the ten mutations above, and no mutation's failure list named an id outside its own guard — no cross-masking observed. After the full census, the scratch copy's `check-selfaudit-scan.py` was byte-identical to its pre-mutation state (`diff` empty) and `--self-test` on the restored scratch copy exits 0.

## Issues Encountered

- `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED` (VAL-03's pytest-capable interpreter unavailable — this worktree's `.venv` did not exist, same environment-setup issue plan 15-07 recorded). Ran `uv sync` (environment setup only, no new dependency added by this plan) to create `.venv`; the battery then reported `FIREWALL: GREEN (24/24)`.
- The whole-tree `grep -c "sole place a verdict block may quote"` (the `<verification>` section's literal wording) reports 1, not 0, because `scripts/check-selfaudit-scan.py` itself necessarily retains the phrase as the `_RUBRIC_FORMAT_ADMISSION_SUPERSEDED` pinned-literal constant — the count-0 guard that detects the phrase's *reinstatement in prose* has to contain the phrase to check for it, exactly as the pre-existing `_RUBRIC_FORMAT_PREAMENDMENT` constant already does for the earlier superseded sentence. The plan's own acceptance criteria for Task 1 scope this check to the two shipped prose files (`shared/spine/references/validation-rubric.md` and `first-principles/agents/references/validation-rubric.md`), both of which report 0; this is the same shape, not a new gap.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Both remaining `15-VERIFICATION.md` gap-1 blocking findings (SCAN-02's CR-01 contradiction, the cross-surface Validate-step drift) are closed and re-reproduced; `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)`.
- `python3 scripts/check-selfaudit-scan.py` and `--self-test` both exit 0 (86/86 branches covered); `python3 scripts/sync-content.py --check` exits 0.
- Out of scope per this plan's own binding constraints, carried forward to plan 15-10: every doc-surface branch-count and registration-shape claim (`CLAUDE.md:169`, `CLAUDE.md:178`, `docs/ARCHITECTURE.md:150`, `docs/ARCHITECTURE.md:165-168`, the `scripts/check-firewall-battery.sh` SCAN-GUARD composition comment) and the gate docstring's residual-bound and cost paragraphs — none of these were touched by this plan and all still read "72 branches"/"58 to 72" today.
- `15-REVIEW.md`'s WR-01 (the coverage-bound sentence's enumeration of band-determining limbs is incomplete against the descriptors) remains explicitly out of scope for this plan, per its own binding constraint — it is in no gap's `missing[]` list in `15-VERIFICATION.md`.
- Phase 16 still owns: version stamps, `docs/requirements-matrix.md` SCAN-01..04 rows, the coverage headline, CHANGELOG, and `REQUIREMENTS.md` checkboxes.

---
*Phase: 15-self-audit-scan*
*Completed: 2026-09-04*

## Self-Check: PASSED

- FOUND: shared/spine/references/validation-rubric.md
- FOUND: shared/spine/SKILL-body.md
- FOUND: first-principles/agents/first-principles.md
- FOUND: first-principles/agents/references/validation-rubric.md
- FOUND: scripts/check-selfaudit-scan.py
- FOUND: .planning/phases/15-self-audit-scan/15-08-SUMMARY.md
- FOUND commit: a083cb5
- FOUND commit: 912d410
- FOUND commit: 02c0ee9
