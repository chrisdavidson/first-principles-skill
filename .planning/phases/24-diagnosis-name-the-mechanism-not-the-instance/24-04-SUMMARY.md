---
phase: 24-diagnosis-name-the-mechanism-not-the-instance
plan: 04
subsystem: docs
tags: [claim-containment, prose-02, sibling-site, narrative-entries, gen-gate-docs]

# Dependency graph
requires:
  - phase: 24-diagnosis-name-the-mechanism-not-the-instance/03
    provides: "docs/v9.1-claim-containment-diagnosis.md's Appendix A — the adjudicated per-vector census (671 vectors, G1..G5 grounds)"
provides:
  - "docs/v9.1-claim-containment-diagnosis.md section 2 — the sibling census: definition of \"sibling site\", the primary named site (docs/gates/SCAN-GUARD.md, confirmed live via detail_page_containment_problems), the three published counts (671 / 11 / 3), and the alternatives considered"
  - "A live-confirmed second escape route beyond CR-01's arrow exemption: NARRATIVE_ENTRIES pages' include_spelled_out=False path, which excludes a chain's spelled-out terminus from consideration independently of the arrow/English-transition regex"
affects: ["25 (claim-containment mechanism design — the primary site and the two independent escape routes it demonstrates bear on REACH-vs-LEVEL scoping)"]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Split a two-task plan's page edit into two sequential Edit-then-commit passes (revert, reapply task 1's block alone, commit, then insert task 2's block, commit) rather than one combined edit, to keep each task's commit atomic and independently verifiable per the task_commit_protocol"

key-files:
  created: []
  modified:
    - docs/v9.1-claim-containment-diagnosis.md

key-decisions:
  - "Confirmed research's SCAN-GUARD.md nomination rather than superseding it: evaluated it against every docs/gates/*.md-resident alternative Appendix A surfaces (QUAL-01.md's single-hop G2 pair, CONF-SURFACE.md:219 itself) and every out-of-reach alternative (tests/premise-rejection-catalog.md, the CLAUDE.md/docs/ARCHITECTURE.md battery-total chain), and SCAN-GUARD wins on all three of the plan's stated preferences (corroborable terminus, reached by containment today, multi-hop chain) simultaneously"
  - "Disclosed rather than smoothed over a population-boundary finding: the primary named site's true terminus (\"one hundred\", spelled out) falls outside Appendix A's own digit-only census population (D-09), so it is confirmed live by direct invocation in this plan but is NOT one of the G2/G3 rows the published counts sum — the published counts stay strictly reconciled to Appendix A's own tallies, and the gap is named as a finding in its own right rather than folded into the count"
  - "Named two independent escape routes for the primary site rather than one: digit-form hops (58 to 72, 72 to 86) are stripped by _CITATION_SHAPE_RES's English-prose transition pattern (CR-01's own mechanism); the chain's true terminus escapes by a second, unrelated route — NARRATIVE_ENTRIES pages' include_spelled_out=False parameter excludes spelled-out numbers from consideration before the arrow/English-transition exemption is ever reached"
  - "Published \"sibling sites found\" (11) and \"stale terminus\" (3) as Appendix A's own G2+G3 row sums, explicitly disclosing that this is a row count, not a distinct-location count — 11 rows resolve to 4 distinct G2 sites and 2 distinct G3 sites, because the md-narrow and md-all census rungs both scan overlapping tracked Markdown and therefore double-count sites that fall in both"
  - "Ran uv sync to restore this fresh worktree's missing .venv/pytest before the full battery could pass — a Rule 3 blocking fix (syncing the existing committed lockfile, not installing a new/unvetted package), matching the identical fix plan 24-03 already applied once in its own worktree"

patterns-established: []

requirements-completed: [PROSE-02]

# Metrics
duration_minutes: 24
completed: 2026-09-09
---

# Phase 24 Plan 04: The sibling census (section 2) Summary

**Named and live-confirmed `docs/gates/SCAN-GUARD.md`'s branch-roster growth-history narrative as PROSE-02's currently-unflagged sibling site — a chain escaping containment by two independent routes, one of which (NARRATIVE_ENTRIES's spelled-out-number exclusion) is a second mechanism beyond CR-01's own — and published the census's three required counts (671 / 11 / 3) reconciled against Appendix A.**

## Performance

- **Duration:** ~24 min
- **Started:** 2026-09-09T13:22Z (worktree base-commit correction and file discovery)
- **Completed:** 2026-09-09T13:34Z
- **Tasks:** 2 (both auto)
- **Files modified:** 1 (`docs/v9.1-claim-containment-diagnosis.md`)

## Accomplishments

- Evaluated `24-RESEARCH.md`'s candidate (`docs/gates/SCAN-GUARD.md`'s branch-roster growth chain)
  against every alternative Appendix A's fuller, mechanically-enumerated population surfaces, per
  the plan's stated preference order (terminus corroborable against a named live source; site on a
  surface containment already reaches today; multi-hop chain). SCAN-GUARD wins on all three
  simultaneously — the only candidate that does — so research's nomination is **confirmed, not
  superseded**.
- Confirmed the site live, in this plan's own session, all three ways task 1 requires:
  1. **Currently unflagged** — `detail_page_containment_problems` invoked on `docs/gates/SCAN-GUARD.md`'s
     live text with `check_spelled_out=False` (the real value `cmd_check()` derives, since
     `"SCAN-GUARD"` is a `NARRATIVE_ENTRIES` member) returns `[]`.
  2. **File and line, re-derived now** — `docs/gates/SCAN-GUARD.md:65`, located by
     `/usr/bin/grep -n "ninety-four to one hundred" docs/gates/SCAN-GUARD.md`, with that command
     recorded as the durable anchor rather than the line number.
  3. **Identical shape, two independent escape routes** — digit-form hops (`58 to 72`, `72 to 86`)
     are stripped by `_CITATION_SHAPE_RES`'s English-prose transition pattern (line 1167,
     `\d{1,4}\s+to\s+\d{1,4}`), the same mechanism section 1 names for CR-01; the chain's true
     terminus (`ninety-four to one hundred`) escapes by a second, unrelated route — it contains no
     digits for that pattern to match at all, and is excluded upstream because
     `detail_page_containment_problems` passes `include_spelled_out=check_spelled_out=False` for
     every `NARRATIVE_ENTRIES` page, so a spelled-out number is never extracted as a candidate claim
     regardless of context. Confirmed by direct invocation: `_normalise_numbers(..., include_spelled_out=True)`
     returns `{'6', '94', '100'}` for the terminus sentence; `include_spelled_out=False` returns
     `set()`. A single-route fix (widening only the arrow/English-transition exemption) would not
     close this site.
- Stated the chain is **currently accurate, not a fourth live defect**: the terminus (100) matches
  `docs/gates/SCAN-GUARD.md`'s own `<!-- GENERATED:FACTS -->` fence (`branch_roster` (100),
  `branch_count`: `100`), checked live 2026-09-09 — exactly the "could recur" shape PROSE-02 asks
  for, not an overstated finding.
- Disclosed a population-boundary nuance rather than hiding it: the primary site's two
  census-population hops (lines 39, 46) are graded **G5** in Appendix A because the chain's true
  terminus is spelled out in words and therefore falls outside D-09's digit-only population — so the
  primary named site is confirmed live in this section but is **not** one of the G2/G3 rows the
  published counts sum. The counts were not widened to include it (D-12 forbids widening the
  population after finding a site outside it); the gap itself is named as a finding.
- Defined "sibling site" on the page before publishing any count: the union of Appendix A's G2 and
  G3 rows, with G1/G4/G5 each excluded by a stated reason.
- Published the three required counts, each dated, commanded, and reconciled against Appendix A's
  own ground tallies: **671** vectors enumerated (D-09's population); **11** sibling sites found
  (G2 + G3 = 8 + 3); **3** carrying a stale terminus (G3). Disclosed that "11" and "3" are row
  counts, not distinct-location counts — the `md-narrow`/`md-all` census rungs both scan overlapping
  tracked Markdown, so `docs/gates/CONF-SURFACE.md:219` is counted twice, leaving 4 distinct G2
  sites and 2 distinct G3 sites.
- Recorded the alternatives considered — CR-01 itself (the instance already found),
  `tests/premise-rejection-catalog.md:687` (a genuine G3 sibling, but on a surface containment
  cannot reach at all today — a reach-gap candidate, not an exemption candidate), `docs/gates/QUAL-01.md:167`
  (reached and corroborated, but a single flat pair with no growth history), and the
  `CLAUDE.md`/`docs/ARCHITECTURE.md` battery-total chain (a real growth chain, but on surfaces
  containment's sole call site does not reach today) — with a reason for each, and stated in the
  page's own voice that "strongest candidate" is a judgement over a surveyed population, not a
  verified fact.
- Closed section 2 pointing forward to Phase 25's CONTAIN-02 demonstration target (the G3 set),
  already recorded in Appendix A and not corrected here.

## Task Commits

Each task was committed atomically:

1. **Task 1: Nominate the sibling site and confirm it live** — `a8cd5c1` (feat)
2. **Task 2: Publish the census counts and the alternatives considered** — `af24046` (feat)

**Plan metadata:** captured in this SUMMARY commit (docs: complete plan)

## Files Created/Modified

- `docs/v9.1-claim-containment-diagnosis.md` — filled in `## 2. The sibling census`: the primary
  named site with its three-part live confirmation and two-independent-route escape analysis, the
  "sibling site" definition, the three published counts, and the alternatives-considered list.

## Decisions Made

- **Confirmed rather than superseded research's SCAN-GUARD.md nomination**, after evaluating it
  against the fuller Appendix A population as the plan's `<interfaces>` section instructed, because
  it uniquely satisfies all three of the plan's stated preferences (corroborable terminus, reached
  by containment today, multi-hop chain) where every other candidate fails at least one.
- **Disclosed the primary site's population-boundary status** rather than either omitting the
  nuance or silently widening the published counts to include it — the site is confirmed live and
  named per ROADMAP criterion 2's own text ("at least one currently-unflagged site"), but the
  published "sibling sites found" / "stale terminus" counts stay strictly reconciled to Appendix A's
  G2+G3 rows, per D-12's binding proviso against widening a pre-registered population after seeing
  what lies outside it.
- **Named two independent escape routes** for the primary site (the arrow/English-transition
  exemption for digit-form hops; the separate `include_spelled_out=False` exclusion for the
  spelled-out terminus) rather than treating it as one instance of CR-01's own mechanism — the
  second route is verified by direct invocation to be structurally unrelated to the first, so a fix
  scoped only to `_CITATION_SHAPE_RES` would not close this site.
- **Split the plan's two tasks into two sequential edit-then-commit passes** on the same file
  section (reverting the combined draft and reapplying Task 1's content alone first, committing,
  then inserting Task 2's content, committing) so each task lands as its own atomic, independently
  verifiable commit per the task_commit_protocol, rather than one combined commit for both tasks.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Ran `uv sync` to restore this fresh worktree's missing pytest-capable `.venv`**
- **Found during:** the first full-battery run for Task 2's verification, which reported
  `FIREWALL: BLOCKED (25/26)` — `[PREREQ] VAL-03` — because this worktree had no `.venv` and neither
  `.venv/bin/python3` nor `python3` could `import pytest`.
- **Issue:** Task 2's acceptance criteria require a live `FIREWALL: GREEN` reading with an unchanged
  total.
- **Fix:** `uv sync` (creates `.venv`, gitignored, installs the six packages already pinned in the
  committed `pyproject.toml`/`uv.lock` — no new or unvetted package name, matching the identical fix
  plan 24-03 already applied once). No product code changed.
- **Files modified:** none tracked (`.venv/` is gitignored).
- **Verification:** re-ran the battery; `FIREWALL: GREEN (26/26)`.
- **Committed in:** noted in the Task 2 commit message; no tracked files changed by this fix itself.

## Out-of-Scope Findings (logged, not fixed)

None newly found. The three pre-existing MD040 (fenced-code-language) issues at lines 44, 94, 159
of `docs/v9.1-claim-containment-diagnosis.md` (introduced by plan 24-02, already logged by plan
24-03's own `deferred-items.md`) remain unchanged by this plan's edits — confirmed via
`markdownlint-cli2` before and after both commits: same 3 issues, same 3 line numbers, both times.

## Issues Encountered

**Worktree base-commit drift, corrected before any planning work started.** This worktree's HEAD
was stale at a Phase 12-era commit (`d4da381`) with no `.planning/` directory at all — the
`worktree_branch_check` step's merge-base assertion caught this and `git reset --hard` to the
directed base commit (`7906a46`) corrected it before any file was read or edited. The gitignored
`.planning/phases/24-diagnosis-name-the-mechanism-not-the-instance/24-04-PLAN.md` and
`24-CONTEXT.md` were also absent from the worktree after the reset (expected — `.planning/` is
gitignored and only force-tracked `*-SUMMARY.md` files travel with the tree); both were read
directly from the main repository checkout at their canonical `.planning/` path instead.

## Assumption Drift (advisory)

None material. The plan's own `<interfaces>` section already flagged the SCAN-GUARD-vs-census
tension this plan resolved ("Research's candidate, to be evaluated rather than assumed... The
adjudicated census from plan 24-03 is the fuller population; use it"), so confirming rather than
superseding it, and disclosing the population-boundary nuance the evaluation surfaced, is the plan's
own instruction carried out rather than a drift from it.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Section 2 is complete; sections 3-6 remain placeholders for plans 24-05 and 24-06, which append
  into the same file without touching section 2 or Appendix A.
- The primary named site (`docs/gates/SCAN-GUARD.md:65`) and its two independent escape routes are
  now on the page for Phase 25's mechanism design to read: the second route (NARRATIVE_ENTRIES's
  `include_spelled_out=False` exclusion) is a distinct closable target from CR-01's own
  arrow/English-transition exemption, and Phase 25's REACH-or-LEVEL determination should account for
  both rather than assuming one fix closes both.
- The G3 set (`docs/gates/CONF-SURFACE.md:219`, `tests/premise-rejection-catalog.md:687`) is
  unchanged from plan 24-03's hand-off and remains Phase 25's CONTAIN-02 demonstration target; this
  plan corrects neither, per D-10.
- No blockers for 24-05 or 24-06.

---
*Phase: 24-diagnosis-name-the-mechanism-not-the-instance*
*Completed: 2026-09-09*

## Self-Check: PASSED

- FOUND: `docs/v9.1-claim-containment-diagnosis.md`
- FOUND: commit `a8cd5c1` (Task 1)
- FOUND: commit `af24046` (Task 2)
- Post-commit deletion check (`git diff --diff-filter=D --name-only`) — no deletions on either
  commit.
- `git status --short` — clean after both commits (`.venv/` untracked and gitignored, not a
  deletion or drift).
- `python3 scripts/gen-gate-docs.py --check` — exit 0.
- `python3 scripts/check-links.py` — `PASS (314 markdown links + 6 namespace refs across 161
  files)`, exit 0.
- `bash scripts/check-firewall-battery.sh` — `FIREWALL: GREEN (26/26)`.
- `markdownlint-cli2 docs/v9.1-claim-containment-diagnosis.md` — 3 issues, all pre-existing
  (lines 44, 94, 159), none newly introduced.
