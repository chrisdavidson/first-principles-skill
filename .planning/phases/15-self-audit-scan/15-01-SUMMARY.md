---
phase: 15-self-audit-scan
plan: 01
subsystem: agent-body
tags: [markdown, prompt-engineering, sync-content, quality-harness]

# Dependency graph
requires: []
provides:
  - "The SCAN-01 self-audit scan prescription in shared/spine/SKILL-body.md's 'Before presenting conclusions' section"
  - "The emitted twin of that prescription in first-principles/agents/first-principles.md"
affects: [15-02-scan-wiring, 15-03-scan-gate]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Process-output scan tables (Assumption Audit precedent) extended to a second scan: chain-form + claim-inventory tables emitted after the closure ledger and before the Self-Audit Gate verdict blocks"

key-files:
  created: []
  modified:
    - shared/spine/SKILL-body.md
    - first-principles/agents/first-principles.md

key-decisions:
  - "Wrote the new prose as unwrapped single-line paragraphs (matching this file's existing convention) rather than hard-wrapped text, after the first verify attempt showed the pinned literals count(t) check fails across an embedded newline"
  - "Rephrased two of the seventeen pinned literals ('derive both tables...' and 'close the block...') as mid-sentence lowercase clauses introduced by 'Both tables are independent of the ledger above:' and 'Then', since the plan requires the literals verbatim but lower-case at a clause boundary, not as sentence-initial capitalized text"

requirements-completed: [SCAN-01]

# Metrics
duration: 25min
completed: 2026-09-04
---

# Phase 15 Plan 01: Self-Audit Scan Prescription Summary

**Added a `## Self-audit scan (process output)` prescription to the canonical agent body — two tables (chain form, then claim inventory) emitted after the §6→§4 closure ledger is clean and before the Self-Audit Gate's verdict blocks, with a single reconciliation line, ledger-independent derivation, and a disclosed enforcement bound.**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-09-04T01:30:00Z (approx.)
- **Completed:** 2026-09-04T01:54:52Z
- **Tasks:** 2/2 completed
- **Files modified:** 2

## Accomplishments
- Inserted the SCAN-01 scan prescription into `shared/spine/SKILL-body.md`, positioned exactly between the closure-ledger's fenced example block and the "Only once the ledger is clean" handoff paragraph, with all 17 pinned literals present exactly once and in the required order.
- Amended the existing "Do not present conclusions until..." sentence to add the self-audit scan as a required gate condition, leaving the two following sentences byte-identical.
- Regenerated `first-principles/agents/first-principles.md` via `sync-content.py --write`; confirmed zero drift with `--check`.
- Ran the full offline firewall battery after resolving a VAL-03 pytest-prerequisite gap (`uv sync`); confirmed `FIREWALL: GREEN (23/23)`.

## Task Commits

Each task was committed atomically:

1. **Task 1: Write the SCAN-01 scan prescription into shared/spine/SKILL-body.md** - `67746ec` (feat)
2. **Task 2: Regenerate the emitted tree and prove the full offline battery is green** - `2ae6ad5` (chore)

**Plan metadata:** committed alongside this SUMMARY.md (worktree mode — orchestrator merges centrally)

## Files Created/Modified
- `shared/spine/SKILL-body.md` - Added the SCAN-01 self-audit scan prescription block (22 new lines) between the closure-ledger fenced example and the Self-Audit Gate handoff; amended the "Do not present conclusions until..." sentence to require the scan.
- `first-principles/agents/first-principles.md` - Regenerated via `sync-content.py --write`; carries the emitted twin of the same prescription, verbatim.

## Verbatim Record: final text of the new block

(as it now reads in `shared/spine/SKILL-body.md`, immediately after the closure-ledger fenced block and immediately before "Only once the ledger is clean")

````text
**Self-audit scan (emit after the ledger is clean, before the verdict blocks):** Once the ledger above is clean, and before the Self-Audit Gate's verdict blocks, emit `` `## Self-audit scan (process output)` `` as one top-level heading holding two tables, chain form first, claim inventory second.

Table 1 covers section 4 with the column list `` `Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean?` ``, one row per section-4 chain block, in order. `Form conforming?` is `yes` or `no`; `Rule applied` names the rule the block violated (R7, R8, R9 or R10 by name plus a short clause, e.g. a hop beginning with a `GT-N` identifier) and is `n/a` on a conforming block; `Dependency clean?` is `yes`, or names the dependency defect — a cycle among chain ids, or an input the chain names that resolves to no ground truth or upstream chain. The dependency column exists because Criterion 4 is reconciled against BOTH the per-block form check and chain dependency, so a table covering form alone leaves half of Criterion 4 unscanned.

Table 2 covers section 6 with the column list `` `§6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited` ``, one row per section-6 construct, in order. `Construct` is `bold lead-in`, `list item` or `prose`; `Claim under R11?` is `yes` or `no`; `R11 clause applied` names the clause of the claim-inventory rule that included or excluded that span (for example: a bold lead-in whose colon closes the bold span; a section-intro label whose colon-terminated span is the whole line and which carries no citation of its own; a bold span whose closing marker is not immediately preceded by the colon; a list item under the forty-character floor that closes no sentence; content inside a fenced block; a near-paraphrase or direct entailment of an already-cited claim earlier in the same section); `Chain cited` is the chain id, or `none — untraced`, or `n/a` for an excluded construct. Every section-6 construct gets a row, non-claims included, each naming the R11 clause that included or excluded it.

A chain that conforms and a construct that is not a claim each still get a row — a clean pass, not a suppressed row.

Both tables are independent of the ledger above: derive both tables from the emitted text of sections 4 and 6 without consulting the §6→§4 closure ledger, and the closure ledger is not admissible as Criterion 4 or Criterion 6 evidence — Criteria 4 and 6 quote this scan, never the ledger. The ledger runs before the Fix/Repeat loop and describes claims that may have been cut, so it describes a document other than the one being scored.

Then close the block with a single reconciliation line a reader can recount against sections 4 and 6:

```text
Scan complete: N chain rows, one per section-4 chain block in order; M section-6 rows, one per construct in order — K claims under R11, J excluded. P chains malformed, Q claims untraced.
```

This scan is included in the response as process output before the Phase 5 verdict blocks, immediately after the Assumption Audit scan and before the Self-Audit Gate's verdict blocks, under its own top-level heading. This scan is the artifact the Phase-5 rubric's Self-audit scan check verifies is present, and the source Criteria 4 and 6 draw their quoted span from.

If any Fix step adds, removes, renames or re-renders a §4 chain, or edits a §6 span, re-run the affected rows of this scan against the current text before re-scoring.

This prescription binds the emission; no gate in this tree checks that a given run complied with it — a gate can assert the prescription is present and well-formed, never that a run obeyed it.
````

And the amended handoff sentence:

```text
Do not present conclusions until the closure ledger is clean, the self-audit scan has been emitted, AND the Self-Audit Gate is cleared.
```

## Verbatim Record: `git diff --stat`

Task 1 (`67746ec`):
```text
 shared/spine/SKILL-body.md | 24 +++++++++++++++++++++++-
 1 file changed, 23 insertions(+), 1 deletion(-)
```

Task 2 (`2ae6ad5`):
```text
 first-principles/agents/first-principles.md | 24 +++++++++++++++++++++++-
 1 file changed, 23 insertions(+), 1 deletion(-)
```

Combined:
```text
 first-principles/agents/first-principles.md | 24 +++++++++++++++++++++++-
 shared/spine/SKILL-body.md                  | 24 +++++++++++++++++++++++-
 2 files changed, 46 insertions(+), 2 deletions(-)
```

## Verbatim Record: battery verdict line

```text
FIREWALL: GREEN (23/23)
```

(Full run output: DUAL-04, GATE-02-v8.5, STEP0-06, STEP0-08, VAL-01, VAL-02, VAL-03, VAL-04, VAL-05, VERSION-01, REG-GUARD, GATE-01, BATT-06, TRACE-03, COLLIDE-01, QUAL-01, PROV-GUARD, HARN-01, HARN-02, HARN-03, HC-BOUND all `[PASS]`; `[INFO] body-size` report-only at 771 lines; `[PASS] INVARIANT-CHECK`; `[PASS] FROZEN-EVIDENCE`.)

## Decisions Made
- **Unwrapped single-line paragraphs:** The plan's automated verify script does an exact-substring `str.count()` check against 17 pinned literals. `shared/spine/SKILL-body.md`'s existing paragraphs are each stored as one long physical line (soft-wrapped for display only, no embedded `\n`). My first draft hard-wrapped the new prose at ~100 columns, which broke several literals across a newline and failed the verify script (12 of 17 literals reported missing). Rewrote the block as unwrapped single-line paragraphs to match the file's actual on-disk convention, after which all 17 literals matched.
- **Lowercase mid-sentence literal placement:** Two of the 17 pinned literals are lowercase clause fragments (`derive both tables...`, `close the block...`) that cannot stand as capitalized sentence-initial text without breaking the exact-match check. Introduced them as mid-sentence clauses (`Both tables are independent of the ledger above: derive both tables...` and `Then close the block...`) to satisfy both the literal-verbatim requirement and normal English sentence capitalization elsewhere in the block.

## Deviations from Plan

None - plan executed exactly as written, with two in-scope wording adjustments (documented above under Decisions Made) needed to satisfy the plan's own automated verify script; no rule-1/2/3/4 auto-fix was required since these were drafting corrections to my own first attempt, not defects in the plan or in unrelated code.

### Environment note (not a deviation from this plan's scope)

- **Found during:** Task 2 (battery run)
- **Issue:** `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 22/23 passed)` because no pytest-capable interpreter existed in this worktree (`.venv` was absent).
- **Fix:** Ran `uv sync` per the plan's own Task 2 action text ("run `uv sync` to create `.venv`... and re-run the battery until it reports GREEN or RED"), which installed pytest and five other packages into a git-ignored `.venv/`. Re-ran the battery: `FIREWALL: GREEN (23/23)`.
- **Files modified:** none tracked (`.venv/` is gitignored).
- **Verification:** `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (23/23)` and exits 0.
- This was an explicitly anticipated step in the plan's own Task 2 action text, not an unplanned deviation.

## Issues Encountered

- **Worktree lacked `.planning/phases/15-self-audit-scan/`:** `.planning/` is gitignored (blanket rule per CLAUDE.md), so the plan files that exist in the main repo checkout were not present in this git worktree (worktrees only inherit tracked files). Copied `15-01-PLAN.md`, `15-CONTEXT.md`, `15-RESEARCH.md`, and `15-PATTERNS.md` from the main repo's `.planning/phases/15-self-audit-scan/` into the worktree's `.planning/phases/15-self-audit-scan/` before starting, so the plan's own `<context>` references resolve. This mirrors the established pattern of force-adding `.planning/` SUMMARY.md files into git despite the blanket ignore (confirmed via `git log -- .planning/phases/14-closure-ledger-claim-inventory/14-06-SUMMARY.md`).
- **Worktree HEAD was behind the expected base commit:** at agent start, `git merge-base HEAD 77bf3c70...` returned `d4da3819...` (a Phase 12 commit), not the expected `77bf3c70...` (a Phase 14 commit). Per the mandatory worktree_branch_check step, ran `git reset --hard 77bf3c70bd9ac35f7cf353c5186eeccee881d493` to correct it before any plan work began.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- `shared/spine/SKILL-body.md` and its emitted twin now carry the SCAN-01 prescription with all 17 required literals, ready for plan 15-02 (SCAN-02, wiring Criteria 4 and 6 to quote this scan) and plan 15-03 (SCAN-03, gating on its presence).
- No blockers. The offline battery is GREEN at 23/23 with no Phase-16 ship surface (version stamps, matrix, CHANGELOG, `.claude-plugin`) touched, matching the plan's out-of-scope boundary.

---
*Phase: 15-self-audit-scan*
*Completed: 2026-09-04*
