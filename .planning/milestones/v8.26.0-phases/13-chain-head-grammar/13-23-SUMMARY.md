---
phase: 13-chain-head-grammar
plan: 23
subsystem: testing
tags: [quality-harness, chain-head-grammar, QUAL-01, reason-upward, documentation-accuracy]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar
    provides: plan 13-22's fixes (round-6 CR-01 needle, prior residuals) and the four-surface
      QUAL-01 registry reason-upward.md was added to by plan 13-20
provides:
  - "shared/references/reason-upward.md's R8 discharge is a real fenced rendered head, not a
    fabricated sentence, on both the canonical source and the generated, slash-invocable
    first-principles/skills/reason-upward/SKILL.md"
  - "A rendered-example claim floor in scripts/check-quality-harness.py that fails by name on
    any registered rule surface (_RENDER_RULE_SURFACES) claiming its examples follow the head
    form without actually rendering that form in a fenced block"
affects: [13-chain-head-grammar closing plans, any future QUAL-01 registry additions]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Byte-recovered-not-retyped registry constant for a real historical defect wording
      (_RENDER_FABRICATED_EXAMPLE_WORDINGS), mirroring _RENDER_PRE_CONTRACT_WORDINGS's own
      discipline"
    - "Whitespace-normalized claim detection paired with a fenced-block containment check for
      the claimed literal, so a claim is only flagged when it is both present and untrue"

key-files:
  created: []
  modified:
    - shared/references/reason-upward.md
    - first-principles/skills/reason-upward/SKILL.md
    - scripts/check-quality-harness.py

key-decisions:
  - "R8's discharge on reason-upward.md is a fenced text block (matching output-template.md
    and SKILL-body.md's rendering), not an inline backtick span (the validation-rubric.md
    precedent) — chosen because the deleted sentence specifically claimed a rendered example
    exists, and only a fenced rendering makes that true."
  - "The rendered-example claim floor's non-vacuity control drives validation-rubric.md's real
    text, not output-template.md's or SKILL-body.md's — those two already carry a real fenced
    R8 head, so appending the fabricated wording to them would make the sentence TRUE, not
    fabricated; validation-rubric.md discharges R8 via an inline backtick span, so it is the
    one registered surface where the append is a genuine, detectable fabrication."
  - "first-principles/agents/references/reason-upward.md, listed in the plan's files_modified,
    does not exist and is not produced by sync-content.py — reason-upward.md is fed to the
    agent surface only via {{PROCEDURE:reason-upward}} substitution into the skill stub, not
    copied as an agent reference sibling (verified: it was absent before this plan's edits and
    absent after, byte-identically across the main repo and this worktree). The plan's third
    acceptance-criteria path for this file was not evaluated for that reason."

patterns-established:
  - "A claim-plus-payload floor: detect a sentence CLAIMING a rendered artifact exists, then
    require the artifact (the R8 literal, fenced) actually be present — reusable if a future
    surface makes an unbacked claim about any other rule literal."

requirements-completed: [CHAINHEAD-03]

# Metrics
duration: ~55min
completed: 2026-09-03
---

# Phase 13 Plan 23: Truthful R8 discharge on reason-upward.md plus a durable claim floor Summary

**Deleted the fabricated "Rendered examples follow the prescribed head form" sentence on
`shared/references/reason-upward.md` and its generated `/reason-upward` skill stub, replaced it
with a real fenced rendered head, and added `scripts/check-quality-harness.py`'s
`_render_example_claim_floor_problems` floor so the same defect class fails by name on any of
the four registered QUAL-01 rule surfaces.**

## Performance

- **Duration:** ~55 min
- **Tasks:** 3 completed (2 with commits; task 3 is pure mutation reproduction, no tracked-file
  changes)
- **Files modified:** 3 (`shared/references/reason-upward.md`,
  `first-principles/skills/reason-upward/SKILL.md`, `scripts/check-quality-harness.py`)

## Accomplishments

- `shared/references/reason-upward.md`'s R8 discharge is now a real fenced `text` block
  (`GT-1? ([brief fact label]) + C2 ([brief fact label])` plus two arrow-led hops), in its own
  labelled "Chain form:" subsection, matching `output-template.md`/`SKILL-body.md`'s layout.
  The fabricated sentence CR-02 (`13-VERIFICATION-round6.md`) flagged is gone from both the
  source and the generated, slash-invocable `first-principles/skills/reason-upward/SKILL.md`.
- Also fixed IN-02 (`13-REVIEW.md`): "ground truth IDs" → "its head inputs", matching
  `validation-rubric.md`'s wording, since a head may consist entirely of `Cn` inputs.
- Added `_RENDER_FABRICATED_EXAMPLE_WORDINGS` (byte-recovered from commit `8289490`, the exact
  plan-13-20 sentence, plus two natural re-introduction frames) and the pure helper
  `_render_example_claim_floor_problems`, wired into `self_test()` as control (i2), scanning
  every `_RENDER_RULE_SURFACES` entry unconditionally for a claim of rendered examples that
  isn't backed by a fenced rendering of the R8 literal.
- Registered the new wordings tuple as a sixteenth `_RenderRegistrySnapshot` field
  (`fabricated_example_wordings`), wired into `.live()`, `_RENDER_REGISTRY_FIELDS`, the by-value
  lock, and control (h2)'s negative-case table. Added non-vacuity controls (i3) — appends each
  wording to `validation-rubric.md`'s real text (the one registered surface with no fenced R8)
  and requires detection — and (i4) — an isolation arm over synthetic claiming files with and
  without a fenced head.
- Independently reproduced CR-02 by mutation on a disposable scratch copy (P1), confirmed the
  floor does not fire on a truthful claim (P2), and confirmed its scope is limited to claiming
  files (P3). See "Task 3 reproduction results" below for the actual observed output, which
  diverges from the plan's stated P1 expectation in one respect — recorded there, not silently
  smoothed over.
- Literal digest (`expected_literal_digest`) unchanged; `expected_literal_digest` and R6/R7/R9
  literal bytes confirmed unchanged against `git show HEAD:scripts/check-quality-harness.py`.
- `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (23/23)` after each task and
  at plan close.

## Task Commits

1. **Task 1: Make reason-upward.md's R8 discharge truthful, in its own subsection** -
   `389d425` (fix)
2. **Task 2: Add the rendered-example claim floor over every registered rule surface** -
   `8389309` (fix)
3. **Task 3: Reproduce CR-02 by mutation and confirm the floor fails by name** - no commit
   (pure mutation reproduction on disposable scratch copies; `git status --porcelain` on the
   real tree confirmed empty before and after, so there is nothing to commit for this task)

**Plan metadata:** committed separately after this SUMMARY (see final commit below)

## Files Created/Modified

- `shared/references/reason-upward.md` - fabricated R8 sentence deleted; real fenced rendered
  head added in a labelled "Chain form:" subsection; "ground truth IDs" → "its head inputs"
- `first-principles/skills/reason-upward/SKILL.md` - regenerated via `sync-content.py --write`,
  inherits the same fix
- `scripts/check-quality-harness.py` - `_RENDER_FABRICATED_EXAMPLE_WORDINGS`,
  `_RENDER_CLAIM_FLOOR_FENCE_RE`, `_render_example_claim_floor_problems`, control (i2)/(i3)/(i4)
  in `self_test()`, the `fabricated_example_wordings` `_RenderRegistrySnapshot` field and its
  lock/roster/negative-case wiring

## Decisions Made

- Chose the fenced-block rendering for R8 over an inline backtick span (see key-decisions in
  frontmatter) — the deleted sentence specifically claimed a rendered example exists, so only a
  fenced rendering discharges it truthfully.
- Scoped the new floor's non-vacuity control to `validation-rubric.md` specifically, not a loop
  over all four registered surfaces — see key-decisions in frontmatter for why looping over all
  four (mirroring control (l1) literally) would have produced false-failing expectations on the
  two surfaces that already carry a real fenced R8 head.

## Deviations from Plan

### Auto-fixed Issues

None — no Rule 1/2/3 auto-fixes were needed; the two tasks matched their `<action>` text
directly.

### Assumption Drift (advisory)

**1. `first-principles/agents/references/reason-upward.md` does not exist**
- **Found during:** Task 1, while running the acceptance-criteria grep commands
- **Planned:** The plan's frontmatter `files_modified` list and Task 1's acceptance criteria
  both name `first-principles/agents/references/reason-upward.md` as a third surface to check
  for the fabricated sentence and fenced-block count.
- **Actual:** `sync-content.py` does not produce this file. `shared/references/reason-upward.md`
  reaches the generated tree only through the `{{PROCEDURE:reason-upward}}` substitution into
  `first-principles/skills/reason-upward/SKILL.md`; unlike `five-whys.md`, `fishbone.md`,
  `estimate.md`, etc., it is not copied verbatim into `first-principles/agents/references/`
  (confirmed: `ls first-principles/agents/references/` lists the other reference files but not
  `reason-upward.md`, `challenge-assumptions.md`, `ground-truths.md`, `identify-essence.md`, or
  `validate.md`; same absence in the main repo's already-merged tree, so this is a pre-existing
  build-topology fact, not something this plan's edits changed).
- **Why:** `sync-content.py --check` exits 0 both before and after this plan's edits, confirming
  no drift was introduced; the acceptance-criteria grep commands were run against the two files
  that do exist (`shared/references/reason-upward.md`,
  `first-principles/skills/reason-upward/SKILL.md`) and both returned the expected `0`/`1`
  counts. The third path's checks were not evaluated because there is nothing at that path to
  check.

**2. Task 3's P1 mutation produces one failing problem, not the two the plan's acceptance
criteria describe**
- **Found during:** Task 3, running P1 on a disposable scratch copy
- **Planned:** "P1 on the scratch copy: `--self-test` exits non-zero; output contains
  `shared/references/reason-upward.md` in a claim-floor problem AND an R8 required-literal
  problem for the same relpath."
- **Actual:** `--self-test` exits non-zero (1) with exactly ONE problem naming the relpath: the
  new claim floor's `(i2) POSITIVE`. No R8 required-literal problem fires. This is a mechanical
  consequence of `_render_required_rule_problems`'s plain substring test
  (`if literal not in text`): plan 13-20's byte-recovered fabricated sentence itself quotes the
  R8 literal in backticks — `` Rendered examples follow the prescribed head form (`GT-1? ([brief
  fact label]) + C2 ([brief fact label])`). `` — so restoring that exact sentence (as P1's own
  instructions require, "restore plan 13-20's exact fabricated sentence") necessarily leaves the
  R8 literal present as a substring, and the required-literal check cannot see that its context
  is a false claim rather than a true rendering. This is exactly the mechanism
  `13-VERIFICATION-round6.md` itself names as the root cause CR-02 needed a NEW control for:
  "CR-02 is a true-per-grep, false-per-content sentence no literal-matching gate parses for
  factual accuracy" — the round-6 report never claims the required-literal check ever went red
  for this defect, only that no existing gate caught it, which the new claim floor now does.
- **Why not fixed:** Making R8's required-literal check ALSO fire here would mean teaching
  `_render_required_rule_problems` to distinguish "this literal is present as a genuine
  rendering" from "this literal is present only because a claim sentence quotes it" — a second,
  overlapping detector for the same defect class the new claim floor already exists to catch,
  and out of scope for a required-literal check whose entire contract (per its own docstring) is
  a plain substring test. The plan's own `<done>` criterion for Task 3 — "P1 turns the round-6
  defect into a named failure... proven by P1, not asserted" — is satisfied: P1 does turn a
  previously-green battery into a named, non-zero-exit failure identifying the exact relpath and
  the exact defect. P2 and P3 (below) matched the plan's stated expectations exactly, confirming
  the floor's scope and non-tautology.

---

**Total deviations:** 0 auto-fixed; 2 advisory (both concern plan-vs-reality mismatches
discovered during verification, not code defects — see above for full detail).
**Impact on plan:** No scope creep. Both items are disclosed observations about what the plan
predicted versus what the shipped mechanics actually produce; neither blocks any of the plan's
`<success_criteria>`, all of which are met (see below).

## Task 3 reproduction results (verbatim)

All three mutations ran on a disposable `rsync -a --exclude .git --exclude .venv --exclude
.planning` scratch copy; `git status --porcelain` on the real tracked tree was confirmed empty
before the first mutation and after the last, and after the closing full-battery run.

**P1** (restore the exact fabricated sentence, delete the fenced head added in Task 1):
```
self-test FAIL: render_contract (i2) POSITIVE: shared/references/reason-upward.md: claims its
examples follow the head form ('Rendered examples follow the prescribed head form (`GT-1?
([brief fact label]) + C2 ([brief fact label])`).') but does not render 'GT-1? ([brief fact
label]) + C2 ([brief fact label])' inside a fenced block
self-test: render_contract sub-check FAILED
```
Exit code: 1. (See "Assumption Drift" item 2 above: this is one problem, not the two the plan's
acceptance criteria describe; the required-literal arm does not additionally fire, for the
mechanical reason explained there.) Before this plan, this identical state was GREEN
(`13-VERIFICATION-round6.md`'s own finding). Restored.

**P2** (keep the fenced head, ALSO restore the fabricated sentence): `--self-test` exit code 0
— no problems reported. Confirms the floor does not fire on a claim that is true of the file
(the fenced head coexists with the sentence). Restored.

**P3** (delete the fenced head, leave no claiming sentence at all):
```
self-test FAIL: render_contract (i) POSITIVE: shared/references/reason-upward.md: rule R8 is
missing — deleted from this surface
self-test: render_contract sub-check FAILED
```
Exit code: 1, R8 required-literal problem only, no claim-floor problem — confirms the floor is
scoped to files that make the claim. Restored.

Real tree closing state: `python3 scripts/check-quality-harness.py --self-test` exit 0,
`python3 scripts/sync-content.py --check` exit 0, `bash scripts/check-firewall-battery.sh`
`FIREWALL: GREEN (23/23)`.

## Issues Encountered

- The worktree's local `.planning/` (gitignored, untracked, populated per-worktree) was missing
  `13-23-PLAN.md`, `PROJECT.md`, `STATE.md`, and `config.json` at spawn time — only prior plans'
  SUMMARY.md files were present. Copied the missing files from the main repo's `.planning/`
  (also gitignored/untracked, so this is a plain file copy, not a git operation) before reading
  them. This is worktree-setup housekeeping, not a plan deviation.
- The worktree's base commit at spawn time (`d4da381...`, phase-12 fixes) did not match the
  wave's expected base (`663423a...`, the phase-13-through-plan-13-22 merge); corrected per the
  `<worktree_branch_check>` step's own instructions (`git reset --hard 663423a...`) before any
  plan work began.
- `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED` (VAL-03's
  pytest-capable interpreter prerequisite unmet — no `.venv`). Ran `uv sync` (per `CLAUDE.md`'s
  own documented remedy) to create `.venv` with pytest; `.venv/` is gitignored, so this created
  no tracked-file changes. All subsequent battery runs reported `FIREWALL: GREEN (23/23)`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `reason-upward.md`'s R8 discharge is now truthful on both the canonical source and the
  generated skill stub, and the recurrence class (a claim of rendered examples with no fenced
  backing) fails by name on any of the four registered QUAL-01 surfaces going forward.
- `13-VERIFICATION-round6.md` also named three OTHER blocking gaps not in this plan's scope:
  CR-04 (`estimate-detail.md`/`theoretical-limit-detail.md` state the chain form and are
  unregistered), CR-05 (the detector's undisclosed over-rejection bound on a
  sentence-terminated intermediate hop), and CR-01's own fixture-needle gap (already closed by
  plan 13-22, this plan's dependency, per its file listing in `_RENDER_FIXTURE_SHAPE`'s
  `R-HEAD-GTHOP-LATE` entry observed already carrying the discriminating needle when this plan
  began — not verified further here since it was out of this plan's task list). Those remain for
  whichever later plan the phase's remaining wave assigns them to.
- Real tree closes `FIREWALL: GREEN (23/23)`, `sync-content.py --check` exit 0,
  `check-quality-harness.py --self-test` exit 0 — no blockers for the next plan in this wave.

---
*Phase: 13-chain-head-grammar*
*Completed: 2026-09-03*

## Self-Check: PASSED

- FOUND: `shared/references/reason-upward.md`
- FOUND: `first-principles/skills/reason-upward/SKILL.md`
- FOUND: `scripts/check-quality-harness.py`
- FOUND: `.planning/phases/13-chain-head-grammar/13-23-SUMMARY.md`
- FOUND commit: `389d425` (Task 1)
- FOUND commit: `8389309` (Task 2)
