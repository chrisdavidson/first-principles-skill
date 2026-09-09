---
phase: 24-diagnosis-name-the-mechanism-not-the-instance
plan: 06
subsystem: docs
tags: [claim-containment, prose-03, self-referential-tests, ratchet, docs-index]

# Dependency graph
requires:
  - phase: 24-diagnosis-name-the-mechanism-not-the-instance/05
    provides: "docs/v9.1-claim-containment-diagnosis.md sections 1-3 and Appendix A, plus 999.54/999.55"
provides:
  - "docs/v9.1-claim-containment-diagnosis.md section 4 — the consistency-shaped class declared out of scope, 999.50/999.51/999.55 named as its answer, with a falsifiable class-property reason"
  - "docs/v9.1-claim-containment-diagnosis.md section 5 — all four self-referential tests answered in two labelled subsections (forward, and honestly about this phase)"
  - "docs/v9.1-claim-containment-diagnosis.md section 6 — keep/keep/drop verdicts on RATCHET-01/02/03 with written REACH-or-LEVEL arguments, rendered before any is built"
  - "docs/README.md — new v9.1 milestone-scoped index section registering the diagnosis page"
  - "A recorded self-instance sweep of sections 4-6 against the page's own quantity-claim discipline"
affects: ["25 (mechanism design — sections 4-6 name what the mechanism must NOT try to reach, and what test 2/3 already require of it)", "26 (RATCHET-01/02/03 verdicts land on Phase 26 success criterion 5's keep/drop slot)", "27 (REL-08's product-recurrence verification criterion is cited, not claimed, in section 5b)"]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "REACH-or-LEVEL verdicts written and recorded before the mechanism they classify exists (D-14/RATCHET-04's ordering requirement), rather than deferred to the phase that builds it"

key-files:
  created: []
  modified:
    - docs/v9.1-claim-containment-diagnosis.md
    - docs/README.md

key-decisions:
  - "RATCHET-03 (the hedge-word diff-review scan) verdicted DROP, not KEEP: its trigger condition — a removed literal replaced by a hedge word with no compensating precision — cannot be told apart from a legitimate docs/PROCESS.md §2 frozen-historical-count paraphrase without referencing CONF-13's own state at the moment of the edit, which is a LEVEL-shaped check (a guard whose subject is another guard's own correctness) per docs/PROCESS.md §1.1. This confirms rather than undercuts the standing risk note's own flagged doubt about RATCHET-03 being the same meta-guard regress it warns about."
  - "RATCHET-01 (cog --check pre-commit) and RATCHET-02 (ledger non-increase assertion) verdicted KEEP, both REACH: RATCHET-01 extends the exact compare-generated-region-to-source pattern the sync-drift gate and conformance-baseline drift gate already run unregistered on every commit; RATCHET-02 tightens the scope of the already-live _DEFERRED_LEDGER_MAX non-increase assertion (the same constant section 3's CR-01 disposition cites) rather than adding a new guard."
  - "Section 4's falsification test is stated as a direct challenge in the reader's hands (name a consistency-shaped defect a value-comparison would catch), rather than as a bare assertion, per D-15's binding proviso that the reason must be a falsifiable class property, not a surface-reach claim"
  - "Found and corrected, during task 3's self-instance sweep, a restatement of Appendix A's own '609 of 671' ground-count figure inside the RATCHET-03 argument — reworded to point at Appendix A's own table instead of retyping a count that is itself subject to Appendix A's own disclosed self-reference growth"
  - "docs/README.md registered the page under a new '## v9.1 — Claim containment diagnosis' milestone-scoped section rather than the counted 'Standing of the nine milestone documents' table, per the plan's explicit constraint; git diff shows zero deletion lines in docs/README.md across the whole phase, confirming CR-03's own row and the counted table are byte-unchanged"

patterns-established: []

requirements-completed: [PROSE-01, PROSE-02, PROSE-03, PROSE-04]

# Metrics
duration_minutes: 48
completed: 2026-09-09
---

# Phase 24 Plan 06: Out-of-scope declaration, self-referential tests, and RATCHET verdicts Summary

**Declared the consistency-shaped class out of scope with a falsifiable class-property reason (999.50/999.51/999.55 named), answered all four self-referential tests in two labelled registers, rendered keep/keep/drop verdicts on RATCHET-01/02/03 with written REACH-or-LEVEL arguments before any is built, registered the diagnosis page in the docs index, and verified the phase-level invariants live: FIREWALL GREEN 26/26 (matching the pre-phase reading), zero gate-infrastructure hunks, no fix written.**

## Performance

- **Duration:** ~48 min (including a stale-worktree correction: `git reset --hard` from a Phase-12-era HEAD to the directed base commit before any file was read)
- **Started:** 2026-09-09T13:55:31Z
- **Completed:** 2026-09-09T14:43Z (approx.)
- **Tasks:** 3 (all auto)
- **Files modified:** 2 (`docs/v9.1-claim-containment-diagnosis.md`, `docs/README.md`)

## Accomplishments

- **Wrote `## 4. Out of scope: the consistency-shaped class`.** States the milestone's D-E scope
  limit (quantity-shaped claims only) in writing; names `999.50`, `999.51` and CR-02's own
  `999.55` by number as the class's answer, re-derived live via a grep for their `ROADMAP.md`
  headers rather than copied from memory. States the reason as a two-layer falsifiable class
  property (primary: no corroborating value exists, with an explicit falsification test in the
  reader's hands; secondary: the semantic-judge route named as a direction, `999.4`, and
  explicitly not opened, per D-D's gate budget). Rules out "the surface is out of reach" by citing
  section 3's own CR-02 disposition: `CLAUDE.md` is a `CONTAIN-01`-reached surface and CR-02 still
  escapes every quantity mechanism, because the escape is a property of the class, not the surface.
- **Wrote `## 5. The four self-referential tests, answered`**, in two labelled subsections per
  D-13. 5a answers each test forward, against `CONTAIN-01/02/03`, `NARR-01/02` and
  `RATCHET-01/02/03` — the mechanisms Phase 25/26 will build. 5b answers each test honestly about
  this phase's own work: test 1 and test 3 are N/A (this phase writes no fix and builds no
  mechanism to classify), each with its reason stated; test 2 is answered positively and directly,
  pointing at section 2's `docs/gates/SCAN-GUARD.md:65` sibling site, named before any fix exists;
  test 4 states what product-recurrence verification would mean for a diagnosis and names Phase
  27's `REL-08` as where it is deferred, quoted in full, rather than claimed here.
- **Wrote `## 6. Verdicts on RATCHET-01, RATCHET-02, RATCHET-03`**, discharging D-14/RATCHET-04's
  ordering requirement (the determination written *before* the mechanism is built). Quoted the
  standing risk note in full ("less mechanism, not more"; RATCHET-03 "the weakest of the three on
  its own evidence"). Rendered:
  - **RATCHET-01 (`cog --check` pre-commit): KEEP, REACH** — extends the exact
    compare-generated-region-to-source pattern the sync-drift gate and conformance-baseline drift
    gate already run, unregistered, on every commit.
  - **RATCHET-02 (ledger non-increase assertion): KEEP, REACH** — tightens the scope of the
    already-live `_DEFERRED_LEDGER_MAX` assertion (the same constant section 3's CR-01 disposition
    cites) rather than adding a new guard.
  - **RATCHET-03 (hedge-word diff-review scan): DROP, LEVEL** — its trigger condition cannot be
    told apart from a legitimate `docs/PROCESS.md` §2 paraphrase without referencing `CONF-13`'s
    own state at the moment of the edit, confirming rather than undercutting the standing risk
    note's flagged doubt.
  - Recorded that the two kept mechanisms (both REACH) do not together constitute the meta-guard
    regress `docs/PROCESS.md` §1 caps, and named Phase 26 as where all three verdicts land.
- **Registered the page in `docs/README.md`** under a new `## v9.1 — Claim containment diagnosis`
  milestone-scoped section, without touching the counted `## Standing of the nine milestone
  documents` table or CR-03's own nav row (`git diff` shows zero deletion lines in `docs/README.md`
  across the whole phase).
- **Swept sections 4-6 for fresh instances of the class this page diagnoses**, recorded in a new
  closing subsection on the page. Every digit-shaped token was enumerated by hand and falls into
  one of the page's own four disciplined grounds (requirement/backlog id, phase/section number,
  file-plus-line citation, or marked quotation), except two arrow-shaped matches the mechanical
  census tool reports on a `docs/PROCESS.md` §1 phase-chain citation (`999.27 → 999.28 → 999.30`)
  — the identical already-adjudicated G4 false-positive shape Appendix A's own `A1` argument names
  for the structurally identical match on `CLAUDE.md:185`. One genuine restatement was found and
  corrected before commit: an earlier draft of the RATCHET-03 argument retyped Appendix A's own
  `609 of 671` ground-count figure directly; reworded to point at Appendix A's table instead.
- **Verified every phase-level invariant live, each with its command:**
  - `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)`, identical to the
    pre-plan-24-01 reading (`24-01-SUMMARY.md` records the same `26/26` before this phase began).
    This worktree had no `.venv`; `uv sync` was run first (Rule 3, see Deviations) to obtain the
    pytest-capable interpreter VAL-03's live leg needs.
  - `git diff --stat b937b3c -- scripts/check-firewall-battery.sh .github/workflows/validation.yml
    .githooks/pre-commit scripts/git-hooks/pre-commit scripts/gen-gate-docs.py
    scripts/_gate_registry.py` (where `b937b3c` is the commit immediately before plan 24-01 began)
    → empty output. Zero hunks in any gate-infrastructure file across the whole phase.
  - `git diff --name-only b937b3c | grep -E "^shared/|^first-principles/"` → no match (exit 1).
    No path under `shared/` or `first-principles/` touched by the whole phase.
  - `python3 scripts/gen-gate-docs.py --check` → exit 0, unchanged.
  - `python3 scripts/report-conformance.py --check` → `PASS — no drift`; adding the `docs/README.md`
    index row required no `--write` regeneration.
  - `python3 scripts/check-links.py` → `PASS (317 markdown links + 6 namespace refs across 161
    files)`, exit 0.
  - `sh .githooks/pre-commit` with everything staged → exit 0 (all 5 pre-commit gates pass; the
    printed `DRIFT: /tmp/...` line is the conformance generator's own self-test fixture, not a
    real failure).
  - **"The battery is green" is evidence only about gate registration, stated in the page's own
    Method section and in the acceptance criteria this plan carries forward — it is never
    evidence about the truth of any hand-written sentence on this page or any other. This SUMMARY
    presents it under that same limit.**

## Task Commits

Each task was committed atomically:

1. **Task 1: Write section 4 — the consistency-shaped class, out of scope** — `a1a7abb` (feat)
2. **Task 2: Write sections 5 and 6 — self-referential tests and RATCHET verdicts** — `c199185` (feat)
3. **Task 3: Register the page in the docs index and verify the phase invariants** — `54f422a` (feat)

**Plan metadata:** captured in this SUMMARY commit (docs: complete plan)

## Files Created/Modified

- `docs/v9.1-claim-containment-diagnosis.md` — appended section 4, section 5 (5a/5b), section 6,
  and a closing "Self-instance sweep" subsection. Sections 1-3 and Appendix A (plans 24-02/03/05)
  are untouched.
- `docs/README.md` — appended a new `## v9.1 — Claim containment diagnosis` milestone-scoped
  section with a one-row document table. No other line in the file was touched.

## Decisions Made

- **RATCHET-03 verdicted DROP, not KEEP** — see key-decisions above. This is the one place this
  plan takes a substantive position rather than a purely descriptive one: the diagnosis's own
  section 1/2 finding (the arrow/English-transition exemption is broad *because it must be*, to
  narrate legitimate history) is what makes RATCHET-03's trigger condition genuinely ambiguous
  between gaming and paraphrase, which is itself the argument for LEVEL classification and the
  standing risk note's own flagged doubt confirmed rather than waved away.
- **RATCHET-01 and RATCHET-02 verdicted KEEP, both REACH** — each argued from an existing,
  already-live analogue already cited elsewhere on this page (the pre-commit compare-to-source
  pattern; `_DEFERRED_LEDGER_MAX`), rather than treated as novel mechanism.
- **Reworded a restated Appendix A figure to a pointer**, found during task 3's own self-instance
  sweep before commit — see key-decisions above.
- **Used `b937b3c` (the commit immediately preceding plan 24-01's first commit) as the whole-phase
  diff baseline**, re-derived by walking `git log --reverse` for the earliest `24-01`/`24-02`
  commits in this milestone's own numbering and excluding an unrelated same-numbered `124-01`
  phase from a much earlier point in this repository's history — this repo's phase numbers have
  been reused across major-version milestones, and a naive `grep "(24-01)"` match would have
  picked the wrong ancestor.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Ran `uv sync` to restore this fresh worktree's missing pytest-capable `.venv`**
- **Found during:** Task 3's first full-battery verification run, which reported
  `FIREWALL: BLOCKED (25/26)` — `[PREREQ] VAL-03` — because this worktree had no `.venv` and
  neither `.venv/bin/python3` nor `python3` could `import pytest`.
- **Issue:** The plan's own `<verification>` block requires a live `FIREWALL: GREEN` reading with
  a total identical to the pre-phase reading.
- **Fix:** `uv sync` (creates `.venv`, gitignored, installs the six packages already pinned in the
  committed `pyproject.toml`/`uv.lock` — no new or unvetted package name; the identical fix plans
  24-03, 24-04 and 24-05 each already applied once, in their own worktrees). No product code
  changed.
- **Files modified:** none tracked (`.venv/` is gitignored).
- **Verification:** re-ran the battery; `FIREWALL: GREEN (26/26)`.

---

**Total deviations:** 1 auto-fixed (Rule 3, environment prerequisite only)
**Impact on plan:** The fix is a mechanical prerequisite for reading the plan's own required live
verdict; it touched no tracked file and no product code, ledger, or gate/CI registration. No scope
creep.

## Out-of-Scope Findings (logged, not fixed)

None newly found. The three pre-existing MD040 (fenced-code-language) issues at lines 44, 94, 159
of `docs/v9.1-claim-containment-diagnosis.md` (introduced by plan 24-02, already logged in this
phase's `deferred-items.md`) remain unchanged — confirmed via `markdownlint-cli2` after task 2's
commit: same 3 issues, same 3 line numbers. This plan's own new content introduces no new MD040
findings (every new fenced block carries an explicit language tag).

## Issues Encountered

**Worktree base-commit drift, corrected before any planning work started.** This worktree's HEAD
was stale at a Phase-12-era commit (`d4da381`, no `.planning/` directory present at all) when this
plan began. The `worktree_branch_check` step's merge-base assertion caught this and `git reset
--hard` to the directed base commit (`e23ce601d9bc63b31c950dc24ce3d732994b5818`) corrected it
before any file was read or edited — the identical pattern plan 24-05 encountered and recorded.

**The plan's own task 3 acceptance criteria list `docs/gates/CONF-SURFACE.md` and `CLAUDE.md` as
files that must not appear in "the whole-phase diff," but they do** — both were legitimately
touched by plan 24-01 (a `gen-gate-docs.py --write` resync when `scripts/census-delta-vectors.py`
joined `CONF-13`'s scanned population, `registered_surfaces=39→40`, `checked_files=69→70`),
already merged into this worktree's base commit before this plan started. This plan's own prompt
context (the `<phase_invariants>` block) explicitly names this exact situation as expected and
legitimate, and instructs verifying that *this plan's own* work does not add to it rather than
that the whole-phase diff is empty on those two files. Verified accordingly: `git diff --stat
e23ce601d9bc63b31c950dc24ce3d732994b5818 -- docs/README.md
docs/v9.1-claim-containment-diagnosis.md` shows only those two intended files changed by this
plan's own commits, and `gen-gate-docs.py --check` / `report-conformance.py --check` both report
no drift after this plan's `docs/README.md` addition — no further regeneration was needed or run.
Recorded here rather than silently reconciled, since the plan text and the actual phase-invariants
guidance genuinely diverge and a future reader should see why this SUMMARY reads the criterion the
way it does.

## Assumption Drift (advisory)

None beyond what plan 24-05's own SUMMARY already recorded (the `check_spelled_out=False`
parameter finding), which this plan did not re-invoke.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `docs/v9.1-claim-containment-diagnosis.md` is now complete: sections 1-6 plus Appendix A, closing
  with a recorded self-instance sweep. This is the last plan in Phase 24.
- Phase 25's planner should read section 4 before proposing any widening of `CONTAIN-01`/`02`
  toward the consistency-shaped class (out of scope, `999.50`/`999.51`/`999.55` are its answer),
  and should read section 2's sibling-site finding (`docs/gates/SCAN-GUARD.md:65`) and Appendix A's
  second G3 site (`tests/premise-rejection-catalog.md:687`) before scoping `CONTAIN-02`'s
  demonstration fixtures.
- Phase 26's planner should read section 6 before building any of RATCHET-01/02/03: RATCHET-01 and
  RATCHET-02 carry KEEP verdicts with REACH arguments already written; RATCHET-03 carries a DROP
  verdict for success criterion 5's own drop slot, with the argument stated in full — this
  discharges RATCHET-04's ordering requirement, it does not require re-litigating the call.
- Phase 27's `REL-08` inherits the product-recurrence framing section 5b names but explicitly does
  not attempt.
- No blockers. All three CR sites and both G3 sites remain live and uncorrected, per D-05/D-10 —
  this phase's own goal.

---
*Phase: 24-diagnosis-name-the-mechanism-not-the-instance*
*Completed: 2026-09-09*

## Self-Check: PASSED

- FOUND: `docs/v9.1-claim-containment-diagnosis.md`
- FOUND: `docs/README.md`
- FOUND: commit `a1a7abb` (Task 1)
- FOUND: commit `c199185` (Task 2)
- FOUND: commit `54f422a` (Task 3)
- Post-commit deletion check (`git diff --diff-filter=D --name-only HEAD~1 HEAD`) on each of the
  three commits — no deletions on any.
- `git status --short` — clean after all three commits.
- `python3 scripts/gen-gate-docs.py --check` — exit 0.
- `python3 scripts/report-conformance.py --check` — `PASS — no drift`.
- `python3 scripts/check-links.py` — `PASS (317 markdown links + 6 namespace refs across 161
  files)`, exit 0.
- `bash scripts/check-firewall-battery.sh` — `FIREWALL: GREEN (26/26)`.
- `sh .githooks/pre-commit` with everything staged — exit 0.
- `markdownlint-cli2 docs/v9.1-claim-containment-diagnosis.md` — 3 issues, all pre-existing
  (lines 44, 94, 159), none newly introduced.
