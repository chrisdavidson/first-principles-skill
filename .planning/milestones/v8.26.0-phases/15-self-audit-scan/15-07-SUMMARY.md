---
phase: 15-self-audit-scan
plan: 07
subsystem: testing
tags: [validation-gate, self-audit-scan, scan-guard, verdict-block-format, anti-masking, clause-level-branches]

# Dependency graph
requires:
  - phase: 15-self-audit-scan
    provides: SCAN-GUARD gate with fail-closed ordering arms, an equality-floored branch registry, and 58 clause-level branch ids (15-03, 15-04, 15-05, 15-06)
provides:
  - Verdict Block Format amended to admit the self-audit scan as a Quoted-span source for Criteria 4 and 6 only, with an admission sentence stating the §6→§4 closure ledger stays inadmissible everywhere
  - Criterion 4 and Criterion 6 quoted-span instructions split into a scan-half (scoped to the limbs each scan table's columns cover) and a direct-quotation half (for the limbs neither table carries a column for)
  - A byte-identical table-coverage-bound sentence on both the agent body and the rubric surface, replacing the agent body's prior overstated claim that the two scan columns close Criterion 4's reconciliation
  - SCAN-GUARD extended from 58 to 72 clause-level branch ids (Rubric-13 format-amendment check, Rubric-9/10 direct-half arms, Body-16, Cross-3), each with its own per-source negative control
  - Both 15-VERIFICATION.md blocking gaps re-reproduced and closed, with a disclosed residual bound recorded on the gate
affects: [Phase 16 (version stamps, matrix rows, coverage headline, CHANGELOG, REQUIREMENTS.md checkboxes, the battery-tally paragraph at CLAUDE.md:182)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A criterion's quoted-span instruction split into a scan-half (scoped to a mechanically-scanned limb) and a direct-quotation half (for a semantic limb no scan table reaches) — the same two-part shape now governs both Criterion 4 and Criterion 6"
    - "A format-level admission sentence stating precisely which criteria may quote process output and which artifact (the closure ledger) remains inadmissible everywhere, placed immediately after the template it amends so the exception is legible at the point of use"
    - "Unwrapping a hard-wrapped multi-line pinned literal into one continuous source line so exact-match fixture helpers (_strip_everywhere, _mutate_within_range, _duplicate_within_range) never need an embedded-newline literal to track"

key-files:
  created: []
  modified:
    - shared/spine/references/validation-rubric.md
    - shared/spine/SKILL-body.md
    - first-principles/agents/first-principles.md
    - first-principles/agents/references/validation-rubric.md
    - scripts/check-selfaudit-scan.py
    - scripts/check-firewall-battery.sh
    - CLAUDE.md
    - docs/ARCHITECTURE.md

key-decisions:
  - "Unwrapped the Verdict Block Format's Quoted-span template line and the new admission paragraph to single continuous lines in shared/ (not the hard-wrapped two/five-line form the surrounding prose uses) — this was not in the plan's literal action text but was needed so the new pinned literals in check-selfaudit-scan.py never require an embedded real newline to exact-match the raw-substring fixture helpers (_strip_everywhere/_mutate_within_range/_duplicate_within_range), matching how the rest of the file's raw-matched literals are already unwrapped in the live tree"
  - "The direct-quotation half of Rubric-9/Rubric-10 gets a count-exactly-once assertion only, no separate ordering assertion — task 2's acceptance criteria explicitly enumerate 'five arms under one check ID' for Rubric-9 (count-missing, count-dup, direct-missing, direct-dup, order), and the 'order' arm is the pre-existing scan-half ordering check, not a new direct-half one; adding an untested sixth arm would have violated the plan's rule against registering a branch id with no control behind it"
  - "R-13-format-order relocates the admission sentence into the Criterion 4 slice, which also drops it out of the Verdict Block Format section slice — this makes the fixture trip BOTH the admission-count-0 check and the ordering check in one run; _check_negative tolerates this because it only requires the expected_detail substring to appear in some matched message, not that it be the only one, so the extra failure does not weaken the control"

requirements-completed: [SCAN-02]

# Metrics
duration: 45min
completed: 2026-09-04
---

# Phase 15 Plan 07: Amend the Verdict Block Format and scope the Criterion 4/6 quoted-span instructions Summary

**Amended the Verdict Block Format to admit the self-audit scan as Criterion 4/6 evidence only, split each criterion's quoted-span instruction into a scan-half and a direct-quotation half covering the limbs no scan table reaches, and extended SCAN-GUARD from 58 to 72 clause-level branch ids pinning both halves plus the format amendment itself.**

## Performance

- **Duration:** ~45 min
- **Started:** 2026-09-04T07:50:00Z (approx, first edit)
- **Completed:** 2026-09-04T08:08:00Z (final commit)
- **Tasks:** 3 completed
- **Files modified:** 8 (`shared/spine/references/validation-rubric.md`, `shared/spine/SKILL-body.md`, `first-principles/agents/first-principles.md`, `first-principles/agents/references/validation-rubric.md`, `scripts/check-selfaudit-scan.py`, `scripts/check-firewall-battery.sh`, `CLAUDE.md`, `docs/ARCHITECTURE.md`)

## Accomplishments
- Amended the Verdict Block Format's standard-form `Quoted span:` template to admit the self-audit scan, for Criteria 4 and 6 only, as a source outside the six-section analysis — closing CR-02, where the prior redirect instructed quoting process output the format definition explicitly excluded.
- Added the admission-sentence pair immediately after the template, naming the scope of the exception and stating the §6→§4 closure ledger is admitted nowhere, so the amendment cannot be read as a general admission of process output (keeps D-03 intact).
- Split Criterion 4's and Criterion 6's quoted-span instruction into a scan-half (scoped to chain form/dependency, and to claim-tracing respectively) and a direct-quotation half naming the limbs each scan table carries no column for (Abandoned Reasoning, the analogy ban, `[Assumes: X]` for Criterion 4; Key-Insight non-obviousness for Criterion 6) — closing CR-03's unsatisfiability.
- Added a byte-identical table-coverage-bound sentence to both `SKILL-body.md`'s scan prescription and the rubric's pre-scoring verify block, and corrected `SKILL-body.md`'s prior claim that the two scan columns close "half of Criterion 4" to the accurate "half of that reconciliation."
- Extended SCAN-GUARD from 58 to 72 clause-level branch ids: Rubric-13 (six ids: the amended template and the admission sentence each split missing/dup, plus the single-direction pre-amendment-absence and ordering arms), Rubric-9/Rubric-10 direct-half count arms (four ids), Body-16 (two ids, the shared coverage-bound sentence inside the agent body's scan prescription), and Cross-3 (two ids, that same sentence cross-surface).
- Re-ran both of `15-VERIFICATION.md`'s blocking-gap reproductions end to end on disposable scratch copies and recorded a disclosed residual bound on the gate: the enumerated limbs are not asserted to be the *complete* set neither scan table reaches, because that completeness is a semantic property of the descriptor prose no mechanical check reads.

## Task Commits

Each task was committed atomically:

1. **Task 1: Amend the Verdict Block Format, scope both quoted-span instructions, state the coverage bound on both surfaces** - `d4e7f98` (fix)
2. **Task 2: Move SCAN-GUARD's pins onto the amended prose and add the format-amendment check** - `f94d8b5` (test)
3. **Task 3: Re-run both verifier reproductions end to end and record the residual bounds** - `58c9de5` (docs)

_No separate plan-metadata commit — SUMMARY.md is committed together with the self-check append per the worktree-parallel-executor protocol._

## Files Created/Modified
- `shared/spine/references/validation-rubric.md` - Amended Verdict Block Format template + admission sentence; two-sentence Criterion 4/6 quoted-span instructions; shared coverage-bound sentence in the Self-audit scan verify block; unwrapped the template/admission text to single continuous lines.
- `shared/spine/SKILL-body.md` - Added the shared coverage-bound sentence after Table 2's paragraph; corrected the overstated "leaves half of Criterion 4 unscanned" claim to "leaves half of that reconciliation unscanned."
- `first-principles/agents/first-principles.md`, `first-principles/agents/references/validation-rubric.md` - Regenerated via `sync-content.py --write`.
- `scripts/check-selfaudit-scan.py` - New/updated literals (`_RUBRIC_QUOTED_SPAN_C4/_C6` rewritten, `_RUBRIC_QUOTED_SPAN_C4/_C6_DIRECT`, `_RUBRIC_FORMAT_QUOTED_SPAN`, `_RUBRIC_FORMAT_PREAMENDMENT`, `_RUBRIC_FORMAT_ADMISSION`, `_TABLE_COVERAGE_BOUND`, `_RUBRIC_FORMAT_START`, `_RUBRIC_CRITERIA_START`); Rubric-9/Rubric-10 extended with direct-half count checks; new Rubric-13 check; Body-16 added to `_check_body_text`; Cross-3 added to `_check_cross_surface`; 14 new branch ids registered in `REQUIRED_BRANCHES`/`_BRANCH_ROSTER_LOCK` (58→72) with matching negative controls; new docstring entry (5) recording the disclosed residual bound.
- `scripts/check-firewall-battery.sh` - SCAN-GUARD registration comment updated 58→72 branches, naming the 15-07 additions.
- `CLAUDE.md`, `docs/ARCHITECTURE.md` - SCAN-GUARD row branch count 58→72, with the description extended to name the Verdict Block Format amendment, both quoted-span halves and the coverage-bound sentence as newly-pinned.

## Decisions Made
See `key-decisions` in the frontmatter above for the three substantive ones.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - blocking issue] Unwrapped the Quoted-span template and admission paragraph to single continuous lines**
- **Found during:** Task 1, while writing the new pinned literals for Task 2.
- **Issue:** My first draft of edit (1)/(2) preserved the original fenced block's hard-wrap (the template line broke across two physical lines, the admission paragraph across four). `_strip_everywhere`/`_mutate_within_range`/`_duplicate_within_range` in `check-selfaudit-scan.py` do raw exact-substring matching (not the `_flat`-normalized matching the count/order checks use), so pinning these two multi-line literals for Task 2's negative controls would have required embedding the exact real newline positions inside the Python string constants — fragile and inconsistent with how the file's other raw-matched literals are single physical lines in the live tree.
- **Fix:** Rewrote both spans as single continuous lines in `shared/spine/references/validation-rubric.md` (matching the style already used for edits (3)-(5), which were written as single lines from the start), then regenerated the emitted tree via `sync-content.py --write`.
- **Files modified:** `shared/spine/references/validation-rubric.md`, `first-principles/agents/references/validation-rubric.md`.
- **Verification:** `sync-content.py --check` exits 0; all six target sentences remain present verbatim and byte-identical across surfaces (re-verified after the rewrap); no `##`/`###` heading moved (heading-line diff empty).
- **Committed in:** `f94d8b5` (folded into Task 2's commit, since the rewrap was made in service of Task 2's literal-matching requirement, not a separate content change).

---

**Total deviations:** 1 auto-fixed (Rule 3).
**Impact on plan:** Mechanical formatting change only — no wording, meaning or byte-content of the six pinned sentences changed, only their line-wrap. All Task 1 acceptance criteria (exact sentence presence, heading immobility, byte-identical cross-surface occurrence) were re-verified after the rewrap and still pass.

## Issues Encountered
- `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED` (VAL-03's pytest-capable interpreter unavailable — this worktree's `.venv` did not exist). Ran `uv sync` (environment setup only, no new dependency added by this plan) to create `.venv`; the battery then reported `FIREWALL: GREEN (24/24)`.

## User Setup Required

None - no external service configuration required.

## Verifier Reproduction Table (Task 3)

Every row below was run on a disposable `rsync --exclude .git --exclude .venv` scratch copy, with `git status --porcelain` confirmed empty in the real tree before and after each mutation.

| Verifier `missing:` item | Command | Observed output |
|---|---|---|
| Gap 1, item 1 — format admits the scan tables for C4/C6 | Live leg on unmodified scratch copy, then reinstate the pre-amendment `Quoted span:` definition alongside the amended one | Unmodified: `exit 0`. Reinstated: `exit 1` — `Rubric-13: pre-amendment quoted-span template still present (1 occurrence(s)) in the whole file, expected 0` |
| Gap 1, item 2 — each redirect scoped, direct-quotation half covers the rest | Strip each of the four half-literals (C4-scan, C4-direct, C6-scan, C6-direct) one at a time, run the live leg | All four: `exit 1`, naming `Rubric-9`/`Rubric-10` with the correct half ("scan-half quoted-span sentence occurs 0 time(s)" / "direct-quotation half occurs 0 time(s)") |
| Gap 2, item 1 — ordering routed through `_find_flat`, fail-closed | Apply `if False:` to the Criterion 4 ordering arm's `failures.append(...)` guard (line 856 in the mutated copy), run `--self-test` | `exit 1` — `R-09c: no failures produced; Anti-masking: 1 branches uncovered` |
| Gap 2, item 2 — `REQUIRED_BRANCHES` floored by an independent transcription | Delete `"X-01-cols-chain-body",` and `"X-02-heading-body",` from `REQUIRED_BRANCHES` only (leaving `_BRANCH_ROSTER_LOCK` untouched), run `--self-test` | `exit 1` — `ROSTER LOCK: REQUIRED_BRANCHES drifted from _BRANCH_ROSTER_LOCK: missing=['X-01-cols-chain-body', 'X-02-heading-body'], extra=[]` |
| Gap 2, item 3 — clause-level branch granularity | `grep -c '_check_negative(' scripts/check-selfaudit-scan.py` (call sites) plus `REQUIRED_BRANCHES`/`_BRANCH_ROSTER_LOCK` length via import | 71 `_check_negative` call sites + 1 direct `R-01-no-mask` control (not routed through `_check_negative`, per 15-06's convention) = 72 controls, matching `len(REQUIRED_BRANCHES) == len(_BRANCH_ROSTER_LOCK) == 72`, equal by value. Extends plan 15-06's m1..m22 census (58 branches, 21/22 caught) — this plan's 14 new branches are additive, not a re-run of that census. |

## Next Phase Readiness
- Both `15-VERIFICATION.md` blocking gaps (SCAN-02, SCAN-03's clause-granularity residual) are closed and re-reproduced; `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)`.
- `python3 scripts/check-selfaudit-scan.py` and `--self-test` both exit 0; `python3 scripts/sync-content.py --check` exits 0; `python3 scripts/check-registration.py --self-test`/live and `python3 scripts/check-traceability.py --self-test` all exit 0.
- The disclosed residual bound (docstring entry 5) is now explicit: this gate does not assert the enumerated band-determining limbs are the *complete* set neither scan table reaches — a future descriptor edit that adds a new limb must land in the same plan as an enumeration edit, or the gate stays green while the enumeration goes stale. This mirrors the R7/R9/R10 disclosed-bound voice `check-quality-harness.py`'s QUAL-01 row already uses.
- Phase 16 still owns: version stamps, `docs/requirements-matrix.md` SCAN-01..04 rows, the coverage headline, CHANGELOG, `REQUIREMENTS.md` checkboxes, and `CLAUDE.md`'s battery-tally narrative paragraph at line 182 (untouched by this plan, per its own binding constraints).
- WR-03 (the live leg `_validate_files()` is not registered in CI or the battery — only `--self-test` runs) remains open, unchanged by this plan; out of scope per plan 15-06's binding constraints, carried forward.

---
*Phase: 15-self-audit-scan*
*Completed: 2026-09-04*

## Self-Check: PASSED

- FOUND: shared/spine/references/validation-rubric.md
- FOUND: shared/spine/SKILL-body.md
- FOUND: first-principles/agents/first-principles.md
- FOUND: first-principles/agents/references/validation-rubric.md
- FOUND: scripts/check-selfaudit-scan.py
- FOUND: scripts/check-firewall-battery.sh
- FOUND: CLAUDE.md
- FOUND: docs/ARCHITECTURE.md
- FOUND: .planning/phases/15-self-audit-scan/15-07-SUMMARY.md
- FOUND commit: d4e7f98
- FOUND commit: f94d8b5
- FOUND commit: 58c9de5
