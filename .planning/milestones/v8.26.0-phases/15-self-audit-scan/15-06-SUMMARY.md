---
phase: 15-self-audit-scan
plan: 06
subsystem: testing
tags: [validation-gate, self-audit-scan, scan-guard, anti-masking, clause-level-branches]

# Dependency graph
requires:
  - phase: 15-self-audit-scan
    provides: SCAN-GUARD gate with fail-closed ordering arms and an equality-floored branch registry (15-03, 15-04, 15-05)
provides:
  - SCAN-GUARD's REQUIRED_BRANCHES/_BRANCH_ROSTER_LOCK split from 31 check-level ids to 58 clause-level ids, one per independently-neutralizable assertion arm
  - Rubric-1's early return removed so a scan-block heading defect no longer suppresses the Criterion 4/6 findings (control R-01-no-mask)
  - Rubric-4's information-free two-criteria name loop deleted (WR-09)
  - A re-run 22-row neutralization census (15-REVIEW.md WR-01) with 21/22 now failing --self-test
affects: [15-07 (rubric/agent-body prose reconciliation, CR-02/CR-03), Phase 16 (version stamps, matrix rows, coverage headline)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "One branch id per independently-neutralizable assertion arm, matching HARN-01's clause-level naming convention (<check-id>-<clause>)"
    - "Two fixture-construction helpers added for the duplicate direction of a `!= 1` count guard: _duplicate_after (mirror image of _strip_everywhere, keeps the original occurrence and adds one more) and _duplicate_within_range (same, scoped to a slice)"
    - "A single mutated fixture can discharge two branch ids at once when its failures list contains two distinguishable messages (e.g. stripping the scan lead's only occurrence fires both the slice-scoped and whole-file Body-2 guards) — each _check_negative call targets its own message via expected_detail, so disabling either guard alone is independently caught"

key-files:
  created: []
  modified:
    - scripts/check-selfaudit-scan.py
    - scripts/check-firewall-battery.sh
    - CLAUDE.md
    - docs/ARCHITECTURE.md

key-decisions:
  - "Rubric-4's Criterion-name loop is DELETED, not scoped — WR-09 measured it as information-free (three sibling sentences in the same slice already name both criteria, so the loop could not independently fail) and the plan explicitly sanctioned deletion as the honest option over keeping an unfalsifiable arm"
  - "B-04's scan-heading duplicate fixture inserts INLINE (same physical line) rather than through the blank-line-separated _duplicate_within_range helper — the literal itself starts with '## ', and a bare standalone copy is mis-read by _slice_to_next_h2's _H2_RE as the section's own closing heading, truncating the slice and producing a wrong-reason failure across Body-5 through Body-14 (caught and fixed during self-test iteration, not shipped)"
  - "Cross-surface arms are split six ways (X-01-cols-chain-body/rubric, X-01-cols-claim-body/rubric, X-02-heading-body/rubric) rather than four, matching the plan's literal enumeration — each single-surface strip proves the OTHER surface's check does not silently cover for it"
  - "R-01-no-mask is implemented as a direct assert-both-check-ids control (not routed through _check_negative, which only asserts a single expected check id) — it duplicates the scan-block heading (Rubric-1 fires) and strips the Criterion 4 quoted-span sentence (Rubric-9 would fire) in the SAME fixture, then asserts both check ids are present in one _check_rubric_text call"
  - "Body-1's early return stays (everything after it genuinely depends on the section slice); only Rubric-1's early return was dropped (WR-10) — this asymmetry is now stated as an inline comment so a future reader does not 'fix' Body-1 by symmetry, per the plan's explicit instruction"
  - "Committed as 2 atomic commits (test: script split; docs: doc-surface count updates) rather than 3 commits mapped 1:1 to the plan's 3 tasks — see Deviations"

requirements-completed: [SCAN-03]

# Metrics
duration: 70min
completed: 2026-09-04
---

# Phase 15 Plan 06: Split SCAN-GUARD's branch ids to clause-level granularity Summary

**Split SCAN-GUARD's REQUIRED_BRANCHES/_BRANCH_ROSTER_LOCK from 31 check-level ids to 58 clause-level ids (one id per independently-neutralizable assertion arm), removed Rubric-1's masking early return and Rubric-4's unfalsifiable name loop, and re-ran 15-REVIEW.md's full 22-row neutralization census — 21 of 22 now fail `--self-test`, with the 22nd (WR-03's live-leg CI/battery registration gap) disclosed as out of scope.**

## Performance

- **Duration:** 70 min
- **Started:** 2026-09-04T11:05:00Z (approx, first edit)
- **Completed:** 2026-09-04T11:47:39Z
- **Tasks:** 3 completed
- **Files modified:** 4 (`scripts/check-selfaudit-scan.py`, `scripts/check-firewall-battery.sh`, `CLAUDE.md`, `docs/ARCHITECTURE.md`)

## Accomplishments
- Split `_check_body_text`'s branch ids from 15 check-level ids to 28 clause-level ids: every `!= 1` count guard now has a MISSING (0) and a DUPLICATE (2) arm, every multi-literal tuple has one arm per literal, and Body-3's combined placement predicate has one arm per half (tail-direction and clean-direction).
- Split `_check_rubric_text`'s branch ids from 15 check-level ids (including the two 15-05 already split, `R-09-crit4-order`/`R-10-crit6-order`) to 24 clause-level ids, plus a new `R-01-no-mask` control. Removed Rubric-1's early return (WR-10) — a fixture duplicating the scan-block heading AND stripping the Criterion 4 quoted-span sentence now surfaces BOTH `Rubric-1` and `Rubric-9` in one run, where before this plan the early return suppressed the second. Deleted Rubric-4's information-free `("Criterion 4", "Criterion 6")` name loop (WR-09) rather than keep it as an uncontrollable arm.
- Split `_check_cross_surface`'s branch ids from 2 check-level ids to 6 clause-level ids (`X-01-cols-chain-body/rubric`, `X-01-cols-claim-body/rubric`, `X-02-heading-body/rubric`), each with its own single-surface strip fixture.
- `_BRANCH_ROSTER_LOCK` re-transcribed by hand against the final 58-id split set (not derived from `REQUIRED_BRANCHES`), keeping plan 15-05's equality-plus-coverage-subset floor intact at the new count.
- Re-ran all 22 rows of `15-REVIEW.md`'s WR-01 mutation table on a disposable `rsync --exclude .git` scratch copy — see the table below. 21/22 now fail `--self-test`; `m22` still survives (disclosed, out of scope per this plan's binding constraints).
- Updated `scripts/check-firewall-battery.sh`, `CLAUDE.md` and `docs/ARCHITECTURE.md` to state the branch count as 58 (was 31), replacing the "clause-level control coverage ... lands in plan 15-06" residual note with the closure it describes.

## Task Commits

Tasks 1 and 2 (body split, rubric split + WR-10/WR-09 fixes) and the start of Task 3 (cross-surface split) were all made to the same functions in `scripts/check-selfaudit-scan.py` and are committed together, since each task's own `--self-test` boundary would otherwise require an intermediate `REQUIRED_BRANCHES` state referencing ids with no controls yet (see Deviations). Task 3's doc-surface count updates are a separate commit:

1. **Tasks 1+2+3 (script): split every branch id to clause-level granularity, add controls, remove Rubric-1's early return, delete Rubric-4's name loop** - `3ad5b0c` (test)
2. **Task 3 (docs): update SCAN-GUARD's branch count to 58 across battery/CLAUDE.md/ARCHITECTURE.md** - `613fa3b` (docs)

_No separate plan-metadata commit — SUMMARY.md is committed together with the self-check append per the worktree-parallel-executor protocol._

## Files Created/Modified
- `scripts/check-selfaudit-scan.py` - `REQUIRED_BRANCHES`/`_BRANCH_ROSTER_LOCK` rewritten to 58 clause-level ids; added `_duplicate_after` and `_duplicate_within_range` fixture helpers; rewrote the body branch negative controls block (28 controls, including an inline-insertion special case for the scan-heading duplicate to avoid a false H2-boundary match); rewrote the rubric branch negative controls block (24 controls plus `R-01-no-mask`); rewrote the cross-surface branch negative controls block (6 controls); removed Rubric-1's `return failures` and added an inline comment on the Body-1/Rubric-1 early-return asymmetry; deleted Rubric-4's `for crit_name in ("Criterion 4", "Criterion 6")` loop.
- `scripts/check-firewall-battery.sh` - SCAN-GUARD registration comment updated from "31 named branches" to "58 clause-level named branches ... plan 15-06 split every check-level branch into one id per independently neutralizable assertion arm".
- `CLAUDE.md` - SCAN-GUARD gate-table row updated: branch count 31 → 58, added the R-01-no-mask/Rubric-4-deletion closure description and the 21/22 re-run neutralization count with m22 named as the open residual.
- `docs/ARCHITECTURE.md` - SCAN-GUARD canonical-inventory row updated with the same count and residual note.

## Decisions Made
See `key-decisions` in the frontmatter above for the five substantive ones. In addition:
- Chose to test the m1-m22 census AND the four already-caught rows (m13-m16) rather than only the 16 the review listed as surviving, to confirm no regression from this plan's edits (all four still caught, unchanged).
- Kept the roster-lock, isolation-arm and call-site-census machinery plan 15-05 added completely unchanged in shape — only the id strings inside `REQUIRED_BRANCHES`/`_BRANCH_ROSTER_LOCK` moved, and the call-site census's expected count (4: 1 real `_roster_problems` call + 3 isolation arms) is untouched since that machinery is orthogonal to the branch split.

## Deviations from Plan

### Process deviation (Rule 1/3-shaped, mechanics only, no functional impact)

**1. Committed as 2 atomic commits instead of 3 (one per task)**
- **Found during:** Task 1, before the first commit.
- **Issue:** The plan's three tasks all rewrite the SAME `REQUIRED_BRANCHES`/`_BRANCH_ROSTER_LOCK` sets and the same `_run_self_test` function in `scripts/check-selfaudit-scan.py`. A true per-task commit boundary would require, after Task 1's commit, a `REQUIRED_BRANCHES` containing the new 28 body ids PLUS the OLD (pre-split) rubric/cross ids — which is exactly what I built incrementally during editing, but I ran the tasks' edits in one continuous sequence without pausing to commit and re-verify at each task boundary before starting the next.
- **Fix:** Committed the full script split (Tasks 1+2+3's code) as one `test(15-06): ...` commit once ALL of it was self-test-verified end to end (58/58 branches, exit 0), and the doc-surface count updates (the tail of Task 3) as a second `docs(15-06): ...` commit. Both commits are independently verifiable: `git show 3ad5b0c` is the complete, self-test-passing script; `git show 613fa3b` is the doc-only count-alignment follow-up.
- **Files modified:** `scripts/check-selfaudit-scan.py` (commit 1); `scripts/check-firewall-battery.sh`, `CLAUDE.md`, `docs/ARCHITECTURE.md` (commit 2).
- **Commits:** `3ad5b0c`, `613fa3b`.
- **Verification:** No functional difference from the plan's intended end state — `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)` after both commits, and the mutation-testing census below was re-run against the final committed state, not an intermediate one.

### Auto-fixed bug (Rule 1, found and fixed during self-test iteration, not shipped)

**2. B-04-heading-dup's first attempt broke the section slice**
- **Found during:** Task 1, running `--self-test` after adding the new controls.
- **Issue:** The first implementation of the `B-04-heading-dup` fixture used `_duplicate_within_range` (blank-line-separated insertion) to duplicate `_SCAN_HEADING` (`"## Self-audit scan (process output)"`) inside the section slice. Because that literal itself starts with `"## "`, the blank-line-separated duplicate became a bare standalone line matching `_H2_RE` (`^## `, MULTILINE) — `_slice_to_next_h2` read it as the section's own closing heading and truncated the slice there, producing a cascade of unrelated `Body-5` through `Body-14` "occurs 0 time(s)" failures instead of the intended `Body-4` "occurs 2 time(s)" failure (a wrong-reason failure caught immediately by `_check_negative`, never a silent pass).
- **Fix:** Replaced the fixture construction for this one arm with an inline insertion (same physical line, single-space separator) that cannot be mistaken for a new heading boundary. No other duplicate literal in the roster starts with `"## "`, so this is a one-off, not a pattern needing a general-purpose fix to the shared helper.
- **Verification:** `--self-test` now reports `(B-04b) correctly failed (1 failure(s))` with the `Body-4` "occurs 2 time(s)" message.
- **Committed in:** `3ad5b0c` (the fix, not the bug, is what shipped — the broken intermediate state was never committed).

## Mutation-Testing Verification (15-REVIEW.md WR-01, m1-m22)

Re-run on a disposable `rsync --exclude .git --exclude .venv` scratch copy of the worktree, one mutation applied and reverted at a time, `git status --porcelain` confirmed empty in the real worktree before and after. Baseline `--self-test` on the scratch copy: exit 0.

| # | Mutation | Result before this plan (15-REVIEW.md) | Result now |
|---|----------|------------------------------------------|------------|
| m1 | Rubric-9 ordering arm → `if False:` | SURVIVED | **CAUGHT** (closed in plan 15-05, re-confirmed here) |
| m2 | Rubric-10 ordering arm → `if False:` | SURVIVED | **CAUGHT** (closed in plan 15-05, re-confirmed here) |
| m3 | Cross-1 rubric arm → `if False:` | SURVIVED | **CAUGHT** (`X-01-cols-chain-rubric`) |
| m4 | Cross-2 body arm → `if False:` | SURVIVED | **CAUGHT** (`X-02-heading-body`) |
| m5 | Body-2 whole-file count arm → `if False:` | SURVIVED | **CAUGHT** (`B-02-lead-whole`) |
| m6 | Rubric-4 name loop → `if False:` | SURVIVED | **N/A — loop deleted** (WR-09; the presence check `R-04-two-criteria` is the falsifiable arm that remains) |
| m7 | drop `_BODY_ROWRULE_CLAIM` from Body-7's tuple | SURVIVED | **CAUGHT** (`B-07-rowrule-claim`) |
| m8 | drop `_BODY_PLACEMENT_2` from Body-12's tuple | SURVIVED | **CAUGHT** (`B-12-placement-2`) |
| m9 | drop `_BODY_LEDGER_INDEP_2` from Body-10's tuple | SURVIVED | **CAUGHT** (`B-10-ledger-indep-2`) |
| m10 | drop `_BODY_RECON_TEMPLATE` from Body-11's tuple | SURVIVED | **CAUGHT** (`B-11-recon-template`) |
| m11 | drop `_RUBRIC_DIVLABOUR_2` from Rubric-3's tuple | SURVIVED | **CAUGHT** (`R-03-divlabour-2`) |
| m12 | drop `_COLS_CLAIM` from Rubric-5's tuple | SURVIVED | **CAUGHT** (`R-05-cols-claim`) |
| m13 | Rubric-11 C6 loop → `if False:` | CAUGHT (pre-existing) | **CAUGHT** (re-confirmed, no regression) |
| m14 | Body-15 pre-amendment arm → `if False:` | CAUGHT (pre-existing) | **CAUGHT** (re-confirmed, no regression) |
| m15 | Rubric-7 near-twin arm → `if False:` | CAUGHT (pre-existing) | **CAUGHT** (re-confirmed, no regression) |
| m16 | Rubric-12 halt count → `if False:` | CAUGHT (pre-existing) | **CAUGHT** (re-confirmed, no regression) |
| m17 | drop `_COLS_CLAIM` from Cross-1's tuple | SURVIVED | **CAUGHT** (`X-01-cols-claim-body`/`X-01-cols-claim-rubric`) |
| m18 | delete `X-01-cols`/`X-02-heading` from `REQUIRED_BRANCHES` | SURVIVED | **CAUGHT** (roster-equality floor, re-confirmed at the new 58-id count with the renamed ids `X-01-cols-chain-body`/`X-02-heading-body`) |
| m19 | Body-3 `tail_idx < lead_idx < clean_idx` → `lead_idx < clean_idx` | SURVIVED | **CAUGHT** (`B-03-placement-tail`) |
| m20 | Rubric-9 `!= 1` → `< 1` | SURVIVED | **CAUGHT** (`R-09-crit4-count-dup`) |
| m21 | Body-4 `!= 1` → `< 1` | SURVIVED | **CAUGHT** (`B-04-heading-dup`) |
| m22 | delete `+ _check_cross_surface(...)` from `_validate_files` | SURVIVED | **SURVIVED — disclosed, out of scope** (WR-03: the live leg is not yet registered in CI/the battery; this plan's binding constraints explicitly exclude adding that registration) |

**21 of 22 rows now fail `--self-test`.** `m22` is the one open residual, matching the plan's stated acceptance bound exactly ("21 of 22 ... now fail the self-test; m22 disclosed as out of scope with its reason recorded").

## Known Stubs

None — this plan is test-infrastructure only; no UI, API, or data-flow surface was touched.

## Threat Flags

None — no new network endpoint, auth path, file-access pattern, or schema change was introduced. The threat model's three `mitigate` items (T-15-05 branch splitting, T-15-06 branch-count claims, T-15-07 Rubric-1 masking) are the work this plan performed, not a new surface it opened.

## Issues Encountered

- `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED` (VAL-03's pytest-capable interpreter unavailable — this worktree's `.venv` did not exist, matching plan 15-05's own recorded issue). Ran `uv sync` (environment setup only, no new dependency added by this plan) to create `.venv`; the battery then reported `FIREWALL: GREEN (24/24)`.
- The B-04-heading-dup fixture's inline-insertion fix (see Deviations item 2) was found and closed entirely within this plan's own iteration loop — no separate task or checkpoint needed.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness
- SCAN-GUARD's clause-level branch coverage now matches the HARN-01 pattern's ratio it was modelled on (58 controls over 58 ids here, vs. 73 over 16 in HARN-01 — HARN-01's ids each carry several controls where SCAN-GUARD's design gives each control its own id; both converge on "every independently-neutralizable arm has a control", which is the property WR-01 asked for).
- `_BRANCH_ROSTER_LOCK` is re-transcribed and the roster-equality floor holds at the new count; `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)`.
- Plan 15-07's scope (CR-02: amend the Verdict Block Format to admit the two scan tables as a Quoted-span source; CR-03: scope the Criterion 4/6 redirect sentences to only the limbs the tables actually cover) is untouched here — this plan's binding constraints explicitly excluded `shared/`/`first-principles/` edits.
- WR-03 (the live leg `_validate_files()` is not registered in CI or the battery — only `--self-test` runs) remains open; `m22`'s survival is the direct, re-measured evidence. Out of scope for this plan by its own binding constraints.
- Phase 16 still owns: version stamps, `docs/requirements-matrix.md` SCAN-01..04 rows, the coverage headline, CHANGELOG, and `CLAUDE.md:182`'s battery-tally narrative paragraph (untouched by this plan, as instructed).

---
*Phase: 15-self-audit-scan*
*Completed: 2026-09-04*

## Self-Check: PASSED

- FOUND: scripts/check-selfaudit-scan.py
- FOUND: scripts/check-firewall-battery.sh
- FOUND: CLAUDE.md
- FOUND: docs/ARCHITECTURE.md
- FOUND: .planning/phases/15-self-audit-scan/15-06-SUMMARY.md
- FOUND commit: 3ad5b0c
- FOUND commit: 613fa3b
