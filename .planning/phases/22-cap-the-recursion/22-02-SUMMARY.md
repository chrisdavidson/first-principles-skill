---
phase: 22-cap-the-recursion
plan: 02
subsystem: docs
tags: [process-contract, depth-rule, review-protocol, pre-commit-gates]

requires:
  - phase: 22-cap-the-recursion (plan 01)
    provides: "docs/PROCESS.md — canonical process contract (depth rule, product/apparatus split, rework cap, exception ledger)"
provides:
  - "CLAUDE.md — depth-rule paragraph + Key-invariants bullet, both outside the generated fence, both linking docs/PROCESS.md"
  - "CLAUDE.md — ### Review protocol section naming docs/PROCESS.md §2, D-08's REVIEW.md frontmatter shape, and the product-blocks/apparatus-files rule"
  - "CONTRIBUTING.md — true five-gate pre-commit count (replacing the false 'One gate fires' claim) + depth-rule sentence and link"
affects:
  - "22-04 (restores CR-05's 17 docs/README.md figures; independent surface, no ordering dependency on this plan)"
  - "22-07 (widens LITERAL_SCAN_MD_GLOBS to include docs/PROCESS.md and CONTRIBUTING.md; must land after this plan's CONTRIBUTING.md edits are committed)"

tech-stack:
  added: []
  patterns:
    - "sentence-plus-link citation of a canonical page, never a restatement (D-04)"
    - "review-protocol-as-instruction with a disclosed no-repo-side-binding limitation (D-08)"

key-files:
  created: []
  modified:
    - CLAUDE.md
    - CONTRIBUTING.md

key-decisions:
  - "Reworded the Key-invariants convention bullet to avoid the word 'one' immediately after 'gate enforces' — CONF-13's literal scanner flagged 'gate enforces this one.' as an unattributed count-shaped literal; the fix was a wording change, not a ledger entry, because the phrase carried no actual count"
  - "Avoided writing the literal filename of the rejected classify-findings post-processor in CLAUDE.md's Review protocol section — the acceptance criteria treat that string's mere presence as evidence an enforcement script was invented, so the D-08 rejection is described generically instead"
  - "scripts/gen-gate-docs.py left byte-unchanged — Tasks 1-3's new CLAUDE.md and CONTRIBUTING.md prose produced zero literal-scan hits after the Task-1 rewording, so no ledger entry, no _DEFERRED_LEDGER_MAX repin, and no _DEFERRED_LEDGER_KEYS_DIGEST repin were needed"

requirements-completed: [CONF-14, CONF-15]

duration: "~35 minutes"
completed: 2026-09-08
---

# Phase 22 Plan 02: State the Depth Rule on CLAUDE.md and CONTRIBUTING.md Summary

`CLAUDE.md` now states the depth rule twice outside its generated fence (once as a standalone
paragraph, once as a Key-invariants bullet) and carries a new `### Review protocol` section
naming D-08's `REVIEW.md` frontmatter shape; `CONTRIBUTING.md` states the depth rule once and no
longer claims a single pre-commit gate fires on `git commit` — it states the true count of five
and points at the enumerating surfaces instead of transcribing them. No literal-scan ledger entry
was required: the new prose produced zero non-exempt hits once one bullet was reworded.

## Performance

- **Duration:** ~35 minutes
- **Completed:** 2026-09-08T12:30:50Z
- **Tasks:** 3
- **Files modified:** 2 (`CLAUDE.md`, `CONTRIBUTING.md`)

## Accomplishments

- The depth rule (`a guard guards the product; a guard is not itself guarded`) is now stated
  verbatim on all three named surfaces — `docs/PROCESS.md` (plan 22-01), `CLAUDE.md`,
  `CONTRIBUTING.md` — each of the latter two carrying a link to `docs/PROCESS.md` rather than
  restating its rules (D-04).
- `CLAUDE.md` gained a `### Review protocol` section instructing any reviewer (the vendored
  `bm:gsd-code-reviewer`, a fork, or a human) to tier findings against `docs/PROCESS.md` §2,
  carry the tier in `REVIEW.md` frontmatter in D-08's exact shape, and block only on product
  findings — with the vendored-agent no-repo-side-binding limitation stated plainly.
- `CONTRIBUTING.md`'s false "One gate fires on `git commit`" claim is corrected to the true count
  of five, without deleting the digit (CR-04's own defect shape), pointing at `CLAUDE.md`'s
  `### Pre-commit gates` section and `docs/CONFIGURATION.md#pre-commit-hooks` for the enumeration.

## Task Commits

Each task was committed atomically:

1. **Task 1: State the depth rule in CLAUDE.md, outside the generated fence** - `d40efa4` (docs)
2. **Task 2: Add the review-protocol block to CLAUDE.md** - `d305845` (docs)
3. **Task 3: Fix CONTRIBUTING.md's false gate count, add the depth-rule sentence and link** - `823fbd1` (fix)

_No plan-metadata commit yet — this SUMMARY.md and its commit are the metadata step, per the
worktree-mode git_commit_metadata convention (STATE.md/ROADMAP.md excluded; orchestrator owns
those after the wave merges)._

## Files Created/Modified

- `CLAUDE.md` — depth-rule paragraph after `<!-- END GENERATED -->` (line 184), a matching
  Key-invariants bullet (line ~410), and a new `### Review protocol` section between
  `### Pre-commit gates` and `### Routing battery` (line 247)
- `CONTRIBUTING.md` — the pre-commit-gate-count paragraph rewritten to state five gates truthfully
  (lines ~40-45), and a depth-rule sentence plus link appended to `## Key invariants` (lines ~73-77)

## Decisions Made

- **Wording fix over ledger entry.** The Key-invariants bullet's first draft ("Convention — no
  gate enforces this one.") tripped CONF-13's literal scanner (`gen-gate-docs.py --check` reported
  a non-exempt hit on `'gate enforces this one.'`). Since "this one" carries no actual count — it
  is an anaphor, not a number — the fix was rewording ("Convention — no gate enforces it.") rather
  than adding a `_DEFERRED_LITERAL_HITS` entry. Re-ran `--check`: exit 0, no hit.
- **No literal filename for the rejected post-processor.** The plan's `<action>` names
  `scripts/classify-findings.py` as the concrete thing D-08 rejected, for the executor's own
  context. Writing that literal string into `CLAUDE.md` would satisfy the acceptance criteria's
  letter but trips its intent — `/usr/bin/grep -c "classify-findings" CLAUDE.md` must be `0`
  precisely so no reader can read the file and conclude such a script exists or was proposed by
  name. `CLAUDE.md` now says "a findings-classifier post-processor" instead.
- **No `gen-gate-docs.py` edit.** Both `--check` runs (after Tasks 1-2, and again after Task 3)
  exited 0 with `literal_scan_non_exempt: 0` — confirmed via `--describe`'s `derived_counts` block,
  since that field is nested there, not top-level. `literal_scan_ledger_entries` (135) still equals
  `literal_scan_ledger_max` (135), unchanged. Per the plan's own instruction, this is recorded so
  the next plan's (22-07) repin arithmetic starts from a known, unmoved state.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Reworded a Key-invariants bullet that tripped the literal scanner**
- **Found during:** Task 1 (depth-rule statement in `CLAUDE.md`)
- **Issue:** The first-draft bullet phrase "gate enforces this one." was flagged by
  `gen-gate-docs.py --check` as an unattributed count-shaped literal, even though "this one" is an
  anaphor referring to the invariant, not a count.
- **Fix:** Reworded to "Convention — no gate enforces it." — same meaning, no false-positive
  literal shape.
- **Files modified:** `CLAUDE.md`
- **Verification:** `python3 scripts/gen-gate-docs.py --check` → exit 0, no non-exempt hit.
- **Committed in:** `d40efa4` (Task 1 commit; the rewording landed before the task's own commit,
  so no separate fix commit was needed)

**2. [Rule 1 - Bug] Removed the literal rejected-script filename from CLAUDE.md's prose**
- **Found during:** Task 2 (review-protocol block)
- **Issue:** First-draft prose named `scripts/classify-findings.py` verbatim when describing D-08's
  rejection of that idea. The task's own acceptance criteria (`grep -c "classify-findings"` == 0)
  treat that string's presence as evidence a script was invented, contradicting the plan's own
  "no script was invented" claim.
- **Fix:** Reworded to "a findings-classifier post-processor" — same substance, no literal filename.
- **Files modified:** `CLAUDE.md`
- **Verification:** `/usr/bin/grep -c "classify-findings" CLAUDE.md` → `0`.
- **Committed in:** `d305845` (Task 2 commit; rewording landed before the task's own commit)

---

**Total deviations:** 2 auto-fixed (both Rule 1 — wording bugs against the task's own acceptance
criteria, found and fixed before either task's commit landed)
**Impact on plan:** Both fixes are wording-only; no scope creep, no new files touched beyond the
two named in the plan.

### Known Pre-Existing Discrepancy (not a deviation — out of scope, not caused by this plan)

**Acceptance criterion 5 of Task 1 / verification item 6 of the plan** requires
`/usr/bin/grep -c "GENERATED — DO NOT EDIT" CLAUDE.md` to print exactly `1`. The measured value is
`2`, both before and after this plan's commits — confirmed via `git show HEAD:CLAUDE.md` at the
plan's starting commit (`5bbadc4`, before any Task 1-3 edit), which already showed count `2`. The
second hit is `CLAUDE.md:126`, inside the pre-existing "Source-of-truth vs. generated surface"
prose describing the `<!-- GENERATED — DO NOT EDIT -->` marker convention in general terms — it is
not a second real fence, has no matching `END GENERATED`, and predates this plan entirely. The
criterion this literal count was meant to stand in for — "the fence markers are still exactly one
pair" — is independently confirmed true by two narrower checks that are not confounded by that
line: `/usr/bin/grep -c "GENERATED — DO NOT EDIT. Source: scripts/_gate_registry.py" CLAUDE.md` → 1
(the one true fence opener), and `/usr/bin/grep -c "END GENERATED" CLAUDE.md` → 1 (its one
closer). Per the SCOPE BOUNDARY rule, a pre-existing condition in an unrelated line, unrelated to
this task's edits, is logged here rather than fixed. No `deferred-items.md` entry was filed
separately since it is fully recorded here.

## Issues Encountered

None beyond the two literal-scan wording fixes recorded above as deviations.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- The depth rule now stands on all three of its named surfaces (`docs/PROCESS.md`, `CLAUDE.md`,
  `CONTRIBUTING.md`), each verified with `/usr/bin/grep -l ... | wc -l` → `3`.
- `CLAUDE.md`'s `### Review protocol` section is written and ready for its first live test —
  `/bm:code-review 22`, named in the block itself as the accepted limitation's first check.
- `scripts/gen-gate-docs.py` is untouched (135/135 ledger, `literal_scan_non_exempt: 0`), so plan
  22-07's widening of `LITERAL_SCAN_MD_GLOBS` to include `docs/PROCESS.md` and `CONTRIBUTING.md`
  starts from a clean, unmoved baseline.
- Battery confirmed `FIREWALL: GREEN (26/26)` on the full tree with this plan's commits applied;
  both `.githooks/pre-commit` and `scripts/git-hooks/pre-commit` exit 0.
- No blockers for downstream plans in this phase.

## Self-Check: PASSED

- `[ -f CLAUDE.md ]` → FOUND
- `[ -f CONTRIBUTING.md ]` → FOUND
- `[ -f .planning/phases/22-cap-the-recursion/22-02-SUMMARY.md ]` → FOUND
- `git log --oneline --all | grep -q d40efa4` → FOUND (Task 1 commit)
- `git log --oneline --all | grep -q d305845` → FOUND (Task 2 commit)
- `git log --oneline --all | grep -q 823fbd1` → FOUND (Task 3 commit)
- `git log --oneline --all | grep -q 8bda048` → FOUND (SUMMARY.md commit)
- All plan-level `<verification>` commands re-run above with observed (not assumed) output,
  including `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)`.

---
*Phase: 22-cap-the-recursion*
*Completed: 2026-09-08*
