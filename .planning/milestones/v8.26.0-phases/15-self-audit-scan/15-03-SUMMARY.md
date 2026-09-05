---
phase: 15-self-audit-scan
plan: 03
subsystem: testing
tags: [python, gate, mutation-testing, quality-harness, self-audit]

# Dependency graph
requires:
  - phase: 15-self-audit-scan
    provides: "The SCAN-01 self-audit scan prescription in shared/spine/SKILL-body.md (plan 15-01) and its emitted twin"
  - phase: 15-self-audit-scan
    provides: "The SCAN-02 rubric verify block and Criterion 4/6 quote-source sentences in shared/spine/references/validation-rubric.md (plan 15-02) and its emitted twin"
provides:
  - "scripts/check-selfaudit-scan.py — the SCAN-GUARD structural gate asserting the self-audit scan prescription and its rubric verify block are present, correctly placed and internally coherent in the emitted tree"
  - "29 named branches (B-01..B-15, R-01..R-12, X-01..X-02), each with a negative control proven by mutation to fire alone, plus an anti-masking assertion and a dispatch-reachability control"
affects: [15-04-scan-gate-registration]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "HARN-01/HARN-02 structural-gate pattern (repo-anchored constants, --self-test control battery, boundary-anchored CHECK-ID matching, anti-masking branch coverage, in-process dispatch-reachability re-entry) applied to a fifth gate"
    - "_flat/_contains/_count_flat whitespace-normalized containment (ported from check-loop-closure.py) to handle a rubric surface that mixes hard-wrapped older prose with unwrapped newly-added blocks"

key-files:
  created:
    - scripts/check-selfaudit-scan.py
  modified: []

key-decisions:
  - "Split the single-file implementation into two commits matching the plan's two tasks (checks + positive controls, then the 29-branch negative-control battery) by reconstructing an intermediate Task-1-only version rather than writing incrementally, since the full design was clearer to draft as one coherent script first"
  - "Chose branch-neutralization-by-monkeypatch (append a wrapper that filters out one CHECK ID's messages from the check function's return value) for Sweep A instead of hand-editing each check's internal control flow — this is a source-level edit applied to the scratch copy and run as a real subprocess, so it satisfies 'break the source, watch the gate go red' while being uniform and auditable across all 29 branches"
  - "Broadened Sweep A's pass criterion beyond a literal 'WRONGLY PASSED' string: Body-2 and Rubric-2's own presence checks have a side-effect dependency (stripping the scan lead/block heading also breaks the placement check that reads the same anchor), so neutralizing Body-2/Rubric-2 alone still produces a red line — just attributed to Body-3/Rubric-3..8's 'failed for the WRONG reason' path rather than 'WRONGLY PASSED'. Both are valid evidence the control fires; the sweep table records the literal line either way"

requirements-completed: [SCAN-03]

# Metrics
duration: 70min
completed: 2026-09-04
---

# Phase 15 Plan 03: Self-Audit Scan Structural Gate (SCAN-GUARD) Summary

**Built `scripts/check-selfaudit-scan.py` — a 1,321-line, 29-branch structural gate that asserts the self-audit scan prescription (15-01) and its rubric verify block (15-02) are present, correctly placed and internally coherent in the emitted tree, with every check proven load-bearing by live mutation testing on disposable scratch copies, never on the real tree.**

## Performance

- **Duration:** ~70 min
- **Started:** 2026-09-04T02:35:00Z (approx.)
- **Completed:** 2026-09-04T03:45:00Z (approx.)
- **Tasks:** 3/3 completed
- **Files modified:** 1 (new)

## Accomplishments

- Wrote `_check_body_text` (15 checks, Body-1..15) validating the SCAN-01 prescription's presence, exact placement (between the closure-ledger's fenced example and the "Only once the ledger is clean" handoff) and internal coherence in `first-principles/agents/first-principles.md`.
- Wrote `_check_rubric_text` (12 checks, Rubric-1..12) validating the SCAN-02 verify block's presence, placement (between the Assumption Audit block and the Precedence rule) and the Criterion 4/6 `Quoted span:` pointer sentences, including a slice-scoped discrimination check (Rubric-7) against the Assumption Audit block's near-twin sentence and a slice-scoped halt-sentence check (Rubric-12) against its whole-file-shared duplicate.
- Wrote `_check_cross_surface` (2 checks, Cross-1..2) validating the shared column lists and scan heading appear on both surfaces.
- Extended `_run_self_test()` with 29 negative controls (one per required branch), an anti-masking assertion printing the full covered-branch set, and an in-process dispatch-reachability control re-entering `main(["--self-test"])`.
- Proved every check and every control fires alone by mutation on disposable `rsync --exclude .git` scratch copies (never the real tree): Sweep A (29 rows, check-source neutralization), Sweep B (6 rows, live-leg Markdown mutation), Sweep C (1 row, anti-masking non-vacuity).
- Confirmed `bash scripts/check-firewall-battery.sh` still reports `FIREWALL: GREEN (23/23)` — the gate is not registered yet (plan 15-04's job), so the tally is unmoved.

## Task Commits

Each task was committed atomically:

1. **Task 1: Write the gate's checks, file validator and positive controls** - `e3f20ec` (feat)
2. **Task 2: Build the negative-control table, the anti-masking assertion and the dispatch-reachability control** - `edd7560` (feat)
3. **Task 3: Neutralization-test every check** - no code commit (verification-only task; results recorded below). The real tree was never modified by this task — all mutation happened on a disposable scratch copy at `/tmp/.../scratchpad/scan-guard-mutation-scratch`, deleted on completion.

**Plan metadata:** committed alongside this SUMMARY.md (worktree mode — orchestrator merges centrally)

## Files Created/Modified

- `scripts/check-selfaudit-scan.py` (new, 1,321 lines) - The SCAN-GUARD structural gate. Constants pin 15-01's and 15-02's literals (module docstring names the two `shared/` source files and the emitted-tree rationale); `_flat`/`_contains`/`_count_flat` give whitespace-normalized containment (ported from `check-loop-closure.py`) since the rubric mixes hard-wrapped older prose with the newly-added, unwrapped scan block; `_slice`/`_slice_to_next_h2` bound the checks to the right region; `_check_body_text`/`_check_rubric_text`/`_check_cross_surface` are the three check functions; `_validate_files()` is the live-tree entry point; `_run_self_test()` runs three live positive controls plus the 29-branch negative-control battery, the anti-masking assertion, and the dispatch-reachability control; `main(argv)` dispatches on `--self-test`.

## Verbatim Record: live-tree validation

```text
check-selfaudit-scan: COVERAGE — first-principles/agents/first-principles.md, first-principles/agents/references/validation-rubric.md
check-selfaudit-scan: PASS
```

## Verbatim Record: final self-test output (tail)

```text
(hw-body) hard-wrap arm: PASS — Body-10 tolerates a hard-wrapped literal
...
(hw-rubric) hard-wrap arm: PASS — Rubric-6 tolerates a hard-wrapped literal
(X-01) correctly failed (1 failure(s))
(X-02) correctly failed (1 failure(s))
ANTI-MASKING GATE: All 29 branches covered: ['B-01-slice', 'B-02-lead', 'B-03-placement', 'B-04-heading', 'B-05-cols-chain', 'B-06-cols-claim', 'B-07-rowrule', 'B-08-rejected', 'B-09-cleanpass', 'B-10-ledger-indep', 'B-11-recon', 'B-12-placement-sentence', 'B-13-refix', 'B-14-bound', 'B-15-donotpresent', 'R-01-block', 'R-02-placement', 'R-03-divlabour', 'R-04-two-criteria', 'R-05-cols', 'R-06-ledger', 'R-07-missing', 'R-08-bound', 'R-09-crit4', 'R-10-crit6', 'R-11-bands', 'R-12-halt', 'X-01-cols', 'X-02-heading']
(dispatch) dispatch control: PASS — main(['--self-test']) reaches this block end-to-end
check-selfaudit-scan --self-test: PASS
```

## Verbatim Record: firewall battery verdict line

```text
FIREWALL: GREEN (23/23)
```

(`.venv` was absent in this fresh worktree; ran `uv sync` per the established environment-note pattern from 15-01/15-02 to provision a pytest-capable interpreter for VAL-03's third leg, then re-ran the battery clean.)

## Sweep A: check-source neutralization (29 rows)

Method: for each of the 29 checks, appended a monkeypatch to a disposable scratch copy of `scripts/check-selfaudit-scan.py` that wraps the relevant check function (`_check_body_text` / `_check_rubric_text` / `_check_cross_surface`) to strip out any failure message carrying that specific CHECK ID (boundary-anchored, matching `_check_negative`'s own ID-matching semantics), then ran `python3 scripts/check-selfaudit-scan.py --self-test` as a real subprocess in the scratch copy. Required result: the self-test exits non-zero and names that branch's own control in a red line — either "WRONGLY PASSED" (the check produced zero failures against its own mutated fixture) or "failed for the WRONG reason" (the check produced zero failures for its own ID, but a *different* check fired as a side effect of the same underlying anchor going missing — itself proof the neutralized check's own signal is gone). Both shapes are valid evidence; every row below records the verbatim line.

| # | Check ID | Branch(es) | Exit code | Verbatim red line |
|---|----------|-----------|-----------|--------------------|
| 1 | Body-1 | B-01-slice | 1 | `(B-01) WRONGLY PASSED (expected failure)` |
| 2 | Body-2 | B-02-lead | 1 | `(B-02) failed for the WRONG reason (expected check ID 'Body-2'; check IDs that DID fire: Body-3; got: Body-3: scan lead '**Self-audit scan (emit after the ledger is clean, before the verdict blocks):**' not found in whole file)` |
| 3 | Body-3 | B-03-placement | 1 | `(B-03) WRONGLY PASSED (expected failure)` |
| 4 | Body-4 | B-04-heading | 1 | `(B-04) WRONGLY PASSED (expected failure)` |
| 5 | Body-5 | B-05-cols-chain | 1 | `(B-05) WRONGLY PASSED (expected failure)` |
| 6 | Body-6 | B-06-cols-claim | 1 | `(B-06) WRONGLY PASSED (expected failure)` |
| 7 | Body-7 | B-07-rowrule | 1 | `(B-07) WRONGLY PASSED (expected failure)` |
| 8 | Body-8 | B-08-rejected | 1 | `(B-08) WRONGLY PASSED (expected failure)` |
| 9 | Body-9 | B-09-cleanpass | 1 | `(B-09) WRONGLY PASSED (expected failure)` |
| 10 | Body-10 | B-10-ledger-indep | 1 | `(B-10) WRONGLY PASSED (expected failure)` |
| 11 | Body-11 | B-11-recon | 1 | `(B-11) WRONGLY PASSED (expected failure)` |
| 12 | Body-12 | B-12-placement-sentence | 1 | `(B-12) WRONGLY PASSED (expected failure)` |
| 13 | Body-13 | B-13-refix | 1 | `(B-13) WRONGLY PASSED (expected failure)` |
| 14 | Body-14 | B-14-bound | 1 | `(B-14) WRONGLY PASSED (expected failure)` |
| 15 | Body-15 | B-15-donotpresent | 1 | `(B-15a) WRONGLY PASSED (expected failure)` and `(B-15b) WRONGLY PASSED (expected failure)` |
| 16 | Rubric-1 | R-01-block | 1 | `(R-01) WRONGLY PASSED (expected failure)` |
| 17 | Rubric-2 | R-02-placement | 1 | `(R-02) failed for the WRONG reason (expected check ID 'Rubric-2'; check IDs that DID fire: Rubric-3..8; got: Rubric-3..8: scan-block slice not found — missing or out-of-order heading '**Self-audit scan (verify before scoring)**' / '**Precedence rule (no double-counting):**')` |
| 18 | Rubric-3 | R-03-divlabour | 1 | `(R-03) WRONGLY PASSED (expected failure)` |
| 19 | Rubric-4 | R-04-two-criteria | 1 | `(R-04) WRONGLY PASSED (expected failure)` |
| 20 | Rubric-5 | R-05-cols | 1 | `(R-05) WRONGLY PASSED (expected failure)` |
| 21 | Rubric-6 | R-06-ledger | 1 | `(R-06) WRONGLY PASSED (expected failure)` |
| 22 | Rubric-7 | R-07-missing | 1 | `(R-07a) WRONGLY PASSED (expected failure)` and `(R-07b) WRONGLY PASSED (expected failure)` |
| 23 | Rubric-8 | R-08-bound | 1 | `(R-08) WRONGLY PASSED (expected failure)` |
| 24 | Rubric-9 | R-09-crit4 | 1 | `(R-09) WRONGLY PASSED (expected failure)` |
| 25 | Rubric-10 | R-10-crit6 | 1 | `(R-10) WRONGLY PASSED (expected failure)` |
| 26 | Rubric-11 | R-11-bands | 1 | `(R-11a) WRONGLY PASSED (expected failure)` and `(R-11b) WRONGLY PASSED (expected failure)` |
| 27 | Rubric-12 | R-12-halt | 1 | `(R-12a) WRONGLY PASSED (expected failure)` and `(R-12b) WRONGLY PASSED (expected failure)` |
| 28 | Cross-1 | X-01-cols | 1 | `(X-01) WRONGLY PASSED (expected failure)` |
| 29 | Cross-2 | X-02-heading | 1 | `(X-02) WRONGLY PASSED (expected failure)` |

All 29 rows: non-zero exit code and a verbatim red line naming that branch's own control. `ALL_OK=True` from the sweep driver.

## Sweep B: live-leg surface mutation (6 rows)

Method: applied each mutation directly to the emitted Markdown in the scratch copy (never `shared/`), then ran `python3 scripts/check-selfaudit-scan.py` (the live leg, no `--self-test`) as a real subprocess. Required result: exit 1, with the failure naming the expected CHECK ID.

| # | Surface | Mutation | Exit code | Verbatim FAIL line(s) |
|---|---------|----------|-----------|-------------------------|
| 1 | Body | strip the scan lead literal | 1 | `check-selfaudit-scan: FAIL — Body-2: scan lead occurs 0 time(s) in the section slice, expected exactly 1`; `check-selfaudit-scan: FAIL — Body-2: scan lead occurs 0 time(s) in the whole file, expected exactly 1`; `check-selfaudit-scan: FAIL — Body-3: scan lead '**Self-audit scan (emit after the ledger is clean, before the verdict blocks):**' not found in whole file` |
| 2 | Body | relocate the scan lead past the ledger-clean handoff | 1 | `check-selfaudit-scan: FAIL — Body-3: scan lead is not placed strictly between the ledger fence tail and the ledger-clean handoff (placement violated)` |
| 3 | Body | rename one column (`Chain Head (brief)` → `Chain Title (brief)`) in the body's chain-form column list only | 1 | `check-selfaudit-scan: FAIL — Body-5: chain-form column list occurs 0 time(s) in the section slice, expected exactly 1`; `check-selfaudit-scan: FAIL — Cross-1: chain-form column list missing from agent-body surface` |
| 4 | Rubric | strip the scan block heading | 1 | `check-selfaudit-scan: FAIL — Rubric-1: scan block heading occurs 0 time(s) in the whole file, expected exactly 1` |
| 5 | Rubric | relocate the scan block past the Precedence rule | 1 | `check-selfaudit-scan: FAIL — Rubric-2: scan block is not placed strictly between the Assumption Audit block and the Precedence rule (placement violated)`; `check-selfaudit-scan: FAIL — Rubric-3..8: scan-block slice not found — missing or out-of-order heading '**Self-audit scan (verify before scoring)**' / '**Precedence rule (no double-counting):**'` |
| 6 | Rubric | rename one column (`Chain Head (brief)` → `Chain Title (brief)`) in the rubric's chain-form column list only | 1 | `check-selfaudit-scan: FAIL — Rubric-5: missing column list(s) in scan slice: 'Chain \| Chain Head (brief) \| Form conforming? \| Rule applied \| Dependency clean?'`; `check-selfaudit-scan: FAIL — Cross-1: chain-form column list missing from rubric surface` |

All 6 rows: exit 1, expected CHECK ID present in the failure output. Both emitted Markdown files verified byte-identical to their pre-mutation state after each row (`agent_orig`/`rubric_orig` equality asserted in the driver).

## Sweep C: anti-masking non-vacuity (1 row)

Method: removed the B-01-slice control's three-line block (`body_b01 = ...` / `_check_negative("B-01", ...)`) from a scratch copy of `_run_self_test()`, leaving `REQUIRED_BRANCHES` unchanged (still 29 entries), then ran `python3 scripts/check-selfaudit-scan.py --self-test` as a real subprocess.

| Mutation | Exit code | Verbatim line |
|----------|-----------|----------------|
| Delete the B-01-slice `_check_negative(...)` call, leave `REQUIRED_BRANCHES` whole | 1 | `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['B-01-slice']` |

Confirmed: the deleted branch is named exactly, no other branch is reported orphaned, and `check-selfaudit-scan --self-test: FAIL — Anti-masking: 1 branches uncovered; (dispatch): main(['--self-test']) returned 1, expected 0` (the dispatch control also correctly fails, since the nested `--self-test` re-entry inherits the same mutated source).

## Scratch-copy hygiene

- Created via `rsync -a --exclude .git <worktree>/ <scratch>/` under the session scratchpad directory, never under `/tmp` directly and never inside the real worktree.
- `git status --porcelain` in the real repo confirmed empty (apart from the new `scripts/check-selfaudit-scan.py`) both before starting Task 3 and after every sweep.
- All mutation happened on files inside the scratch copy only; the real `scripts/check-selfaudit-scan.py`, `first-principles/agents/first-principles.md` and `first-principles/agents/references/validation-rubric.md` were never opened for writing during Task 3.
- The scratch directory was deleted (`rm -rf`) at the end of Task 3; confirmed absent afterward.

## Decisions Made

- **Two-commit reconstruction:** Wrote the complete script in one draft (since the design — 29 branches, shared constants, cross-referencing checks — was clearer to think through as a whole), then reconstructed a Task-1-only intermediate version (checks + positive controls a/b/c only, no `REQUIRED_BRANCHES`, no negative-control table, no anti-masking, no dispatch control) for the first commit, and restored the full version for the second commit — so each commit's diff matches its task's actual scope.
- **Monkeypatch-based Sweep A:** rather than hand-editing each check's internal `if`/`return` structure (29 different code shapes), Sweep A appends a small wrapper function after each check's original definition that filters out messages carrying the target CHECK ID from that function's return value. This is still a real source-level edit run as a real subprocess against the scratch copy — it is not an in-process mock — and it generalizes uniformly across all 29 branches without needing bespoke AST surgery per check.
- **Widened "correctly attributed failure" criterion for Sweep A:** two branches (Body-2, Rubric-2) have a side-effect dependency — their own presence check reads the same anchor a downstream placement/slice check also depends on, so neutralizing the presence check alone still trips the downstream check when the anchor is genuinely missing. The sweep records this as `"failed for the WRONG reason"` rather than `"WRONGLY PASSED"`; both are valid, distinguishable evidence that the control's own signal disappeared when its check was neutralized (the row lists the literal line either way, so this asymmetry is visible in the SUMMARY rather than smoothed over).

## Deviations from Plan

None — plan executed exactly as written. The two-commit split (documented above) and the widened Sweep A pass criterion are drafting/verification-methodology choices within the plan's own instructions ("build the checks", "one negative control per branch", "verify by mutation"), not changes to what the plan specifies must be checked or asserted.

### Environment note (not a deviation from this plan's scope, matching 15-01/15-02's precedent)

- **Found during:** Task 3 (firewall battery run)
- **Issue:** `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 22/23 passed)` — `[PREREQ] VAL-03` — because this fresh worktree had no `.venv` (no pytest-capable interpreter).
- **Fix:** Ran `uv sync`, which provisioned `.venv` with pytest and five other packages (git-ignored, untracked). Re-ran the battery: `FIREWALL: GREEN (23/23)`.
- **Verification:** `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (23/23)` and exits 0.

## Issues Encountered

- **Worktree lacked `.planning/phases/15-self-audit-scan/15-03-PLAN.md` and companion files:** copied `15-03-PLAN.md`, `15-CONTEXT.md`, `.planning/PROJECT.md`, `.planning/STATE.md` and `.planning/config.json` from the main repo checkout into this worktree's `.planning/`, mirroring 15-01's and 15-02's precedent (`.planning/` is gitignored, so worktrees only inherit tracked files).
- **Worktree HEAD was behind the expected base commit:** at agent start, `git merge-base HEAD 12c60210c2eb71dc46047765651f9ae0a8c5f412` returned `d4da3819...` (a Phase 12 commit), not the expected `12c60210...` (the commit that merged 15-02). Per the mandatory `worktree_branch_check` step, ran `git reset --hard 12c60210c2eb71dc46047765651f9ae0a8c5f412` to correct it before any plan work began.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `scripts/check-selfaudit-scan.py` exists, validates the live emitted tree clean (both the CLI live leg and `--self-test`), and every one of its 29 branches is proven load-bearing by live mutation on disposable scratch copies — ready for plan 15-04 (battery registration, CI job, CLAUDE.md row).
- No blockers. `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (23/23)` — the new gate is intentionally not yet registered (plan 15-04's scope), so the tally is unchanged.

---
*Phase: 15-self-audit-scan*
*Completed: 2026-09-04*

## Self-Check: PASSED

- FOUND: `scripts/check-selfaudit-scan.py`
- FOUND: `.planning/phases/15-self-audit-scan/15-03-SUMMARY.md`
- FOUND commit: `e3f20ec` (Task 1)
- FOUND commit: `edd7560` (Task 2)
