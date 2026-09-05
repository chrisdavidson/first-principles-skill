---
phase: 17-conformance-baseline
plan: 03
subsystem: tooling
tags: [pre-commit, git-hooks, documentation, mutation-testing]

# Dependency graph
requires:
  - phase: 17-02
    provides: "docs/conformance-baseline.md + docs/data/conformance.json committed and --check-clean; scripts/report-conformance.py --check/--self-test both exit 0"
provides:
  - "Both mirrored pre-commit hook files (.githooks/pre-commit, scripts/git-hooks/pre-commit) chain sync-drift + conformance-baseline drift checks"
  - "Six documentation surfaces (CLAUDE.md, docs/ARCHITECTURE.md, docs/DATA-FLOW.md, docs/CONFIGURATION.md, docs/TESTING.md, docs/DEVELOPMENT.md) state two pre-commit gates"
  - "Recorded proof that 17-VALIDATION.md mutation 7 fails by name on both install paths, with a regression half and a pass-through control"
affects: [18-conformance-remediation]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "sh -eu hook restructuring: non-terminal check propagates via '|| exit $?', only the final check keeps exec (no repo precedent existed for chaining two checks in one pre-commit hook)"
    - "Mutation battery executed on rsync --exclude .git --exclude .venv scratch copies, git init'd fresh so a real HEAD exists to commit against, under the session scratchpad, never the working tree"

key-files:
  created: []
  modified:
    - .githooks/pre-commit
    - scripts/git-hooks/pre-commit
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - docs/DATA-FLOW.md
    - docs/CONFIGURATION.md
    - docs/TESTING.md
    - docs/DEVELOPMENT.md

key-decisions:
  - "docs/DEVELOPMENT.md was edited even though it is not in the plan's files_modified frontmatter list -- the plan's Task 2 explicitly requires sweeping for surfaces the CONTEXT.md/RESEARCH.md file list missed, and the sweep found this sixth surface ('One gate fires on git commit: the sync-drift gate') before any edit was made"
  - "docs/ONBOARDING.md and docs/COMPONENT-DIAGRAM.md already stated 'the two pre-commit gates' -- both were stale before this phase (predating TEARDOWN-01's body-budget retirement) and are now accurate by coincidence; left unedited per the plan's instruction to confirm rather than silently re-touch"
  - "README.md's body-budget-hook prose (lines 135-145) was examined and left unchanged -- it describes the already-retired body-budget hook as if active, a pre-existing staleness class unrelated to this phase's gate-count axis and out of scope per the scope-boundary rule"

requirements-completed: [CONF-02]

# Metrics
duration: ~50min
completed: 2026-09-05
---

# Phase 17 Plan 03: Wire report-conformance.py --check into the pre-commit gate Summary

**Restructured both mirrored pre-commit hook files to chain `sync-content.py --check` then `report-conformance.py --check` (propagating the first's exit status explicitly rather than relying on `exec`'s process-replacement to mask the second), corrected six documentation surfaces stating a stale one-gate count, and proved by mutation on disposable scratch repos that the second check runs on both install paths, with a regression control and a pass-through control.**

## Performance

- **Duration:** ~50 min
- **Started:** 2026-09-05 (worktree base corrected to `18c729e` before start — see Deviations)
- **Completed:** 2026-09-05
- **Tasks:** 3/3 completed
- **Files modified:** 8 (2 hook files, 6 doc surfaces)

## Accomplishments

- Restructured `.githooks/pre-commit` and `scripts/git-hooks/pre-commit` so the sync-drift check runs first with its exit status explicitly propagated (`|| exit $?`), then `report-conformance.py --check` runs as the terminal `exec`'d statement — the first time this repo has chained two checks in one pre-commit hook (no prior precedent existed to copy).
- Preserved each file's pre-existing cosmetic asymmetry: `.githooks/pre-commit` keeps `echo`, `scripts/git-hooks/pre-commit` keeps `printf`; both still begin `#!/bin/sh`, contain `set -eu`, and `cd "$(git rev-parse --show-toplevel)"`; both remain executable.
- Swept the tracked Markdown tree for pre-commit gate-count statements: the five surfaces the plan named (`CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/DATA-FLOW.md`, `docs/CONFIGURATION.md`, `docs/TESTING.md`) plus a sixth found by the sweep itself (`docs/DEVELOPMENT.md`) all now state two pre-commit gates. `docs/ARCHITECTURE.md`'s gate-inventory table gained a second row with `—` in the gate-id column (no invented gate id). `docs/TESTING.md` gained a full "Conformance-baseline drift gate" subsection modelled on the existing "Sync-drift gate" subsection.
- Confirmed `docs/ONBOARDING.md` line 113 and `docs/COMPONENT-DIAGRAM.md` line 66 already said "the two pre-commit gates" (stale before this phase, coincidentally accurate afterward) and left both unedited, per the plan's instruction to record the observation rather than silently re-touch.
- Proved mutation 7 (17-VALIDATION.md) on both install paths — `core.hooksPath .githooks` and the `install-hooks.sh` symlink — with a regression half (sync-drift gate still fires on a desynced generated tree) and a pass-through control (an in-sync, unrelated commit succeeds).
- Confirmed the non-goal preservation battery: `FIREWALL: GREEN (24/24)`, no diff to `.github/workflows/validation.yml` / `scripts/check-firewall-battery.sh` / `scripts/check-quality-harness.py`, nothing under `shared/` or `first-principles/` touched, and both `report-conformance.py --check` and `--self-test` exit 0 on the real tree.

## Task Commits

1. **Task 1: Restructure both mirrored pre-commit hooks to chain two checks** - `032e920` (feat)
2. **Task 2: Sweep every doc surface stating the pre-commit gate count** - `e5bedd7` (docs)
3. **Task 3: Mutation 7 (prove the SECOND check runs) and the non-goal preservation battery** - no commit (verification-only task; the real tree was confirmed byte-unchanged before and after the mutation session, matching the shape of 17-02's Task 2)

**Plan metadata:** committed alongside this Summary.

## Final Hook Check-Invocation Blocks (both files, verbatim)

`.githooks/pre-commit`:
```sh
# --- Gate 1: sync-drift gate (preserved verbatim from prior version) --------
# Not exec'd -- a second gate follows, so its exit status is propagated
# explicitly with "|| exit $?" rather than replacing the shell process with
# it. A failing sync check must not be silently replaced by a passing
# conformance check, or the reverse.

$PY scripts/sync-content.py --check || exit $?

# --- Gate 2: conformance-baseline drift gate ---------------------------------
# Terminal check -- only this one may use exec, because nothing follows it.

exec $PY scripts/report-conformance.py --check
```

`scripts/git-hooks/pre-commit`'s equivalent block is byte-identical except for the header prose above it (which keeps `printf` instead of `echo` in the missing-interpreter branch, matching the pre-existing cosmetic asymmetry).

Both files' interpreter-resolution block was changed from a three-branch `if/elif/else` that `exec`'d directly to one that sets `PY="uv run"` or `PY="python3"` in a variable, so the two checks below can both invoke it.

## Doc-Sweep Disposition Table (every `pre-commit` hit examined)

| Surface | Hit | Disposition |
|---|---|---|
| `CLAUDE.md` § "Pre-commit gates" | "One gate fires..." | **Edited** — now "Two gates fire", names `report-conformance.py --check` and D-06's non-registration; `check-body-budget.py` paragraph and `--no-verify` line preserved unchanged |
| `docs/ARCHITECTURE.md` gate-inventory prose | `**1 pre-commit**` | **Edited** — now `**2 pre-commit**` |
| `docs/ARCHITECTURE.md` gate-inventory table | sync-drift row only | **Edited** — added a second row, `—` gate-id, naming `report-conformance.py --check` |
| `docs/DATA-FLOW.md` Stage 4 | "fires one pre-commit gate" | **Edited** — now "fires two pre-commit gates", added a second bullet |
| `docs/CONFIGURATION.md` "What the pre-commit hook gates" | "Both hook paths run one gate:" | **Edited** — now "run two gates:", added a second numbered item; body-budget/TEARDOWN-01 and `uv`/`--no-verify` paragraphs preserved |
| `docs/TESTING.md` "Pre-commit gates" | "One gate fires..." | **Edited** — now "Two gates fire...", added a full "Conformance-baseline drift gate" subsection with an `**Owning script:**` line and explicit no-CI-counterpart statement |
| `docs/DEVELOPMENT.md` "Pre-commit hooks" | "One gate fires on `git commit`: the **sync-drift gate**" | **Edited** — found by the sweep, not in the plan's five-file list; now names both gates |
| `docs/ONBOARDING.md` line 113 | "the two pre-commit gates" | **Left as-is** — already accurate (was stale relative to the pre-phase one-gate reality; now correct) |
| `docs/COMPONENT-DIAGRAM.md` line 66 | "the two pre-commit gates" | **Left as-is** — same situation as ONBOARDING.md |
| `README.md` lines 119-145 | body-budget hook described as active, sync-drift gate opt-in instructions | **Left as-is, out of scope** — this describes the already-retired (TEARDOWN-01) body-budget hook as if it still gates commits; a pre-existing staleness class on a different axis (hook *content*, not gate *count*) than this plan's D-06 scope; logged here rather than silently fixed, per the scope-boundary rule |
| `docs/DEVELOPMENT.md` line 19, `CONTRIBUTING.md` line 16, `docs/DATA-FLOW.md` line 7 | "caught by the pre-commit drift gate" | **Not a count statement** — no edit needed |
| `docs/ARCHITECTURE.md` line 58 | "This runs as a pre-commit gate and as CI gate DUAL-04" | **Not a count statement** — refers to the sync-drift gate specifically; no edit needed |
| `docs/v8.7-constraint-teardown.md`, `docs/audit-2026-08-16-duplication-staleness.md`, `CHANGELOG.md` | various historical mentions of hook paths / retired gates | **Left byte-unchanged** — historical documents, protected by the invariance rule; confirmed via `git diff --quiet` |
| `docs/requirements-matrix.md`, `docs/requirements-traceability.md` | historical requirement rows (META-Q4, HOOK-01..06) mentioning pre-commit hooks | **Not a current-fact count statement** — historical/generated requirement rows; no edit |
| `docs/v8.14-delivery-verification.md` | "pre-committed" (unrelated word: pre-registered success criteria) | **Not applicable** — different meaning entirely, not about git hooks |
| All other hits (MEASUREMENT-MAP.md, README.md's doc-index rows, testing-agents-headlessly.md, DEVELOPMENT.md's other cross-links) | links/pointers to the canonical gate table, no count restated | **Not a count statement** — no edit needed |

Re-run of the sweep pattern after all edits: `/usr/bin/grep -rn -i -E "1 pre-commit|run one gate|fires one pre-commit|One gate fires" CLAUDE.md README.md docs/*.md` produced **zero hits** — `SWEEP-CLEAN`.

## Mutation 7 — Four Verbatim Observed Outcomes

All four ran on `rsync -a --exclude .git --exclude .venv` scratch copies under the session scratchpad, each `git init`'d fresh with one baseline commit so a real HEAD existed to commit against. Both scratch repos were deleted after the session; `git status --porcelain` on the real tree was confirmed empty both before and after.

| # | Scenario | Command | Observed outcome | Verdict |
|---|---|---|---|---|
| 7a | `core.hooksPath .githooks`, only conformance baseline desynced (one-byte edit to the `Measurement date:` line) | `git commit` | Exit 1. Output: `DRIFT: docs/conformance-baseline.md` + unified diff + `Run: python3 scripts/report-conformance.py && git add -u`. **No** `sync-content` failure appeared. | PASS — refused by the new check's own message |
| 7b | `scripts/install-hooks.sh` path (confirmed `.git/hooks/pre-commit` is a symlink to `scripts/git-hooks/pre-commit` via `test -L`), same desync | `git commit` | Exit 1. Identical output to 7a: `DRIFT: docs/conformance-baseline.md` + diff + the same remediation line. | PASS — same refusal on the installer path |
| 7c | Baseline restored fresh (`git reset --hard HEAD`), instead desynced one byte of `first-principles/agents/first-principles.md` (`name: first-principles` → `name: first-principlesX`) | `git commit` | Exit 1. Output: `DRIFT: first-principles/agents/first-principles.md` + unified diff + `Run: python3 scripts/sync-content.py --write && git add -u` — the pre-existing sync-content remediation line, not report-conformance's. | PASS — the pre-existing gate did not regress |
| 7d | Both surfaces restored in sync (`git reset --hard HEAD`), unrelated trivial change (`echo "# trivial comment" >> README.md`) | `git commit` | Exit 0. Output: `report-conformance: PASS — no drift`, commit succeeded (`[master 99305d8] test 7d trivial pass-through`). | PASS — anti-masking control: the hook is not always-refusing |

## Non-Goal Preservation Battery (real tree)

- `bash scripts/check-firewall-battery.sh` — first run reported `FIREWALL: BLOCKED` (1 prerequisite unmet: no pytest-capable interpreter in this fresh worktree). Ran `uv sync` to provision `.venv` (gitignored, confirmed via `git check-ignore -v .venv`). Re-run: **`FIREWALL: GREEN (24/24)`** — battery count unmoved, matching D-06's explicit non-goal.
- `git diff --quiet -- .github/workflows/validation.yml scripts/check-firewall-battery.sh scripts/check-quality-harness.py` — exit 0 (`NON-GOALS-DIFF-CLEAN`). No CI job added, no battery registration added, `check-quality-harness.py` untouched.
- `git status --porcelain shared/ first-principles/` — printed nothing.
- `python3 scripts/report-conformance.py --check` — exit 0, `report-conformance: PASS — no drift`.
- `python3 scripts/report-conformance.py --self-test` — exit 0, `report-conformance: SELF-TEST PASS — 14 controls run` (an in-process control fixture printed its own expected `DRIFT:` diff to stderr as part of exercising the `check-detects-drift` control; this is the self-test proving its own drift-detection logic, not a live failure — overall exit status is 0).
- `git status --porcelain` on the real tree, bracketing the entire mutation-7 + battery session — empty both before and after.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking issue] Worktree HEAD was stale at plan start — reset to the correct wave-2 base commit**
- **Found during:** Startup HEAD-safety assertion (per the `<worktree_branch_check>` protocol in the executor prompt)
- **Issue:** `git merge-base HEAD 18c729e4990a75abcab22c7cfb4ab70484c6b437` returned `d4da381` (a Phase 12 commit), not the expected base — the worktree's initial HEAD predated the Phase 17 wave-1/wave-2 merges entirely.
- **Fix:** Ran `git reset --hard 18c729e4990a75abcab22c7cfb4ab70484c6b437` per the documented recovery path in the executor prompt's own startup instructions (the prompt itself warned this was expected, citing wave 2's prior experience of the same issue).
- **Files modified:** none (branch-pointer move only)
- **Commit:** N/A (pre-work repair, not a task deliverable)

**2. [Rule 3 - Blocking issue] Plan/context files absent from the worktree's gitignored `.planning/` tree**
- **Found during:** `files_to_read` step
- **Issue:** `.planning/` is project-gitignored; the worktree's copy only contained `17-01-SUMMARY.md` and `17-02-SUMMARY.md` (force-tracked per project convention). `17-03-PLAN.md`, `17-CONTEXT.md`, `17-VALIDATION.md`, `17-RESEARCH.md`, `17-PATTERNS.md`, `PROJECT.md`, `STATE.md`, `config.json` all existed only in the main repo checkout.
- **Fix:** Copied the required files from `/home/chrisdavidson/Projects/first-principles-skill/.planning/` into the worktree's `.planning/` tree (read-only reference copies; none of these are git-tracked or part of this plan's deliverables).
- **Files modified:** none tracked by git
- **Commit:** N/A (local reference copies only, never staged)

**3. [Rule 1 - Bug in the illustrative shape, corrected before implementing] Explicit exit-status propagation, not `set -eu`'s implicit abort**
- **Found during:** Task 1, first draft of the hook restructuring
- **Issue:** An initial draft ran `$PY scripts/sync-content.py --check; sync_status=$?; if [ "$sync_status" -ne 0 ]; then exit "$sync_status"; fi` — but with `set -eu` already in effect, an unguarded failing command aborts the script immediately, making the `sync_status=$?` line unreachable dead code in the failure case. This does not match the plan's explicit instruction to make propagation "explicit... so a reader can see which check owns which failure, and so a future third check cannot be appended into dead code."
- **Fix:** Adopted `17-PATTERNS.md`'s own illustrative shape verbatim: `$PY scripts/sync-content.py --check || exit $?` — this is genuinely explicit (the `||` suppresses `set -e`'s automatic abort for that one command, so the propagation is a real, readable branch rather than relying on the shell's implicit behavior).
- **Files modified:** `.githooks/pre-commit`, `scripts/git-hooks/pre-commit`
- **Commit:** `032e920` (implemented this way from the first commit; documented here as a deviation from an initial draft, not from the plan's own guidance, which this choice satisfies more literally)

### Auth gates
None encountered.

## Known Stubs
None. Both hook files are fully functional and proved by live mutation on both install paths; all six doc surfaces are fully edited, not partially stubbed.

## Threat Flags
None. All six threat-register mitigations for this plan (T-17-10 through T-17-14, T-17-SC) were followed exactly as specified — the interpreter-resolution `PATH` lookup is unchanged from the pre-existing behavior (T-17-10, accept), mutation 7c/7d cover T-17-11/T-17-12, the doc sweep with its disposition table covers T-17-13, and T-17-SC/T-17-14 are not applicable (no installs, no measurable latency concern). No new security-relevant surface was introduced.

## Self-Check: PASSED

- FOUND: `.githooks/pre-commit`
- FOUND: `scripts/git-hooks/pre-commit`
- FOUND: `CLAUDE.md`
- FOUND: `docs/ARCHITECTURE.md`
- FOUND: `docs/DATA-FLOW.md`
- FOUND: `docs/CONFIGURATION.md`
- FOUND: `docs/TESTING.md`
- FOUND: `docs/DEVELOPMENT.md`
- FOUND: `.planning/phases/17-conformance-baseline/17-03-SUMMARY.md`
- FOUND commit `032e920` (Task 1)
- FOUND commit `e5bedd7` (Task 2)
- FOUND commit `6482d69` (this Summary)
