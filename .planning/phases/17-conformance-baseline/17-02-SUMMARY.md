---
phase: 17-conformance-baseline
plan: 02
subsystem: testing
tags: [documentation, measurement-instrument, conformance-baseline, mutation-testing]

# Dependency graph
requires:
  - phase: 17-01
    provides: "scripts/report-conformance.py: discover_artifacts / build_row / build_rows / pair_agreement measurement core, render_markdown / render_json / cmd_write / cmd_check, --self-test"
provides:
  - "docs/conformance-baseline.md: the published L1 conformance reading of all 29 shipped surfaces, dated 2026-09-04"
  - "docs/data/conformance.json: structured 29-row sidecar, all 22 schema columns plus three report columns"
  - "Recorded proof that seven of the eight 17-VALIDATION.md anti-vacuity mutations each fail by name"
affects: [17-03-pre-commit-wiring, 18-conformance-remediation]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Mutation battery executed on rsync --exclude .git --exclude .venv scratch copies under the session scratchpad, never the working tree"
    - "git add before a second bare-run diff check, since git diff --quiet is vacuous against untracked files"

key-files:
  created:
    - docs/conformance-baseline.md
    - docs/data/conformance.json
  modified: []

key-decisions:
  - "No task-2 commit exists because task 2 is a verification-only task by design: every mutation ran on a disposable scratch copy, and the acceptance criteria require the real tree to be byte-unchanged before and after the session. Task 1's commit already carries the only file changes this plan makes."

requirements-completed: [CONF-01, CONF-02]

# Metrics
duration: ~55min
completed: 2026-09-05
---

# Phase 17 Plan 02: Generate, Verify and Prove the Conformance Baseline Summary

**Generated and committed `docs/conformance-baseline.md` + `docs/data/conformance.json` via `scripts/report-conformance.py`, confirmed all six headline figures against two independent witnesses, and proved seven of `17-VALIDATION.md`'s eight anti-vacuity mutations each fail by name on disposable scratch copies, leaving the real tree byte-unchanged throughout.**

## Performance

- **Duration:** ~55 min
- **Started:** 2026-09-05 (worktree base corrected to `21e8e61` before start — see Deviations)
- **Completed:** 2026-09-05T02:22:43Z
- **Tasks:** 2/2 completed
- **Files created:** 2 (`docs/conformance-baseline.md`, `docs/data/conformance.json`)

## Accomplishments

- Ran `scripts/report-conformance.py` (bare) to write both artifacts, confirmed a second write left them byte-identical (staged first so `git diff --quiet` was a real comparison, not a vacuous untracked-file check), and confirmed `--check` exits 0 on the committed tree.
- Verified all six headline figures against both `17-CONTEXT.md` § Specific Ideas and `17-RESEARCH.md` § Summary: 4/14 unreadable on each example surface (same four files by name), 58 §6 conclusion claims / 56 untraced, 69 §2 verdict cells / 69 non-conforming, 10 §4 chain blocks / 7 malformed, 28 heading-swept blocks / 19 malformed, 14/14 pairs agreeing. The contract surface read 3 claims/3 untraced, 1 verdict cell/1 non-conforming, 3 §4 chain blocks/1 malformed — all matching exactly, no adjustment needed on either side.
- Confirmed the criterion-4 prose properties: `MEASUREMENT_DATE` literal `2026-09-04` present, no target language (`grep -c -i -E` for target/should reach/must reach returns 0), no gate registered (`check-firewall-battery.sh` and `.github/workflows/validation.yml` byte-unchanged), and the read-only constraint held (`shared/`, `first-principles/`, `scripts/check-quality-harness.py` all untouched).
- Ran `bash scripts/check-firewall-battery.sh`: first attempt reported `FIREWALL: BLOCKED` (no pytest-capable interpreter in this fresh worktree); ran `uv sync` to provision `.venv`, then re-ran and observed `FIREWALL: GREEN (24/24)` — battery count unmoved, per D-06.
- Executed all seven scratch-copy mutations owned by this plan (M1-M6, M8; M7 belongs to 17-03) and recorded each verbatim observed message below. Every mutation fired the expected named failure; none produced a generic traceback or a silent clean pass.
- Confirmed `git status --porcelain` on the real tree was empty both before and after the entire mutation session, and confirmed `--check` and `--self-test` both remain clean on the real tree afterward.

## Task Commits

1. **Task 1: Generate, verify against the 2026-09-04 readings, and commit both artifacts** - `a2f190c` (feat)
2. **Task 2: Scratch-copy mutation battery — validation mutations 1-6 and 8** - no commit (verification-only task; see Deviations/key-decisions — the task's own acceptance criteria require the real tree to be byte-unchanged, and it was)

**Plan metadata:** committed alongside this Summary.

## Files Created

- `docs/conformance-baseline.md` (82 lines) - the published headline table, per-artifact tables for all three surfaces, and the D-04/D-05 reconciliation sections.
- `docs/data/conformance.json` - the structured 29-row JSON sidecar (`measurement_date`, `generator`, `artifact_count`, `surface_counts`, `headline`, `pair_agreement`, `rows`).

## Mutation Ledger (Task 2)

`git status --porcelain` on the real tree: **empty** before the session started and **empty** after it ended (both observed directly, not assumed). All seven mutations ran on `rsync -a --exclude .git --exclude .venv` scratch copies under the session scratchpad; a fresh copy was created per mutation (never stacked); every scratch directory was deleted after its mutation ran.

| Mutation | Command | Observed message | Verdict |
|---|---|---|---|
| M1 — D-02 shared-examples floor | Deleted `shared/examples/ishikawa-fishbone.md` in scratch copy, ran bare `report-conformance.py` | `report-conformance: COUNT FLOOR FAIL — expected >= 14 files matching shared/examples/*.md, found 13` (exit 1) | PASS — named floor fired, never a clean 13-row run |
| M2 — D-02 twin floor | Deleted `first-principles/agents/references/examples/ishikawa-fishbone.md` in scratch copy, ran bare | `report-conformance: COUNT FLOOR FAIL — expected >= 14 files matching first-principles/agents/references/examples/*.md, found 13` (exit 1) | PASS — twin floor named the twin glob |
| M3 — D-02 contract surface | Renamed `shared/spine/references/output-template.md` to `.md.bak` in scratch copy, ran bare | `report-conformance: COUNT FLOOR FAIL — expected shared/spine/references/output-template.md to exist at <scratch-path>/shared/spine/references/output-template.md, found missing` (exit 1) | PASS — named the expected path explicitly; no `found 0` count, no silent skip |
| M4 — D-02 mistyped glob | Edited `SHARED_EXAMPLES_GLOB` to `shared/example/*.md` (typo) in scratch copy's script, ran bare | `report-conformance: COUNT FLOOR FAIL — expected >= 14 files matching shared/example/*.md, found 0` (exit 1) | PASS — the "emptied or mistyped" case D-02 names, caught with `found 0` |
| M5 — D-03 partial row | Deleted the `## 1. Problem Essence` heading from `shared/examples/personal-general.md` (a readable file) in scratch copy, ran bare | Exit 0, 29 rows still emitted. Mutated row: `section_resolution` = `SectionResolutionError: expected sections 1-6 to resolve in order, resolved [2, 3, 4, 5, 6]`, `heading_chain_blocks=2`, `heading_malformed_blocks=0` (nonzero, real reading). Headline `Files unreadable by _slice_sections` moved `4 of 14` → `5 of 14` on shared-examples (twin stayed `4 of 14`, unaffected) | PASS — named partial row recorded, run did not crash, artifact not dropped from the table |
| M6 — CONF-02 drift detection (`.md`) | Hand-edited byte 7 of committed `docs/conformance-baseline.md` (`2026-09-04` → `2026-09-05`) in scratch copy, ran `--check`; then reverted and ran `--check` again | Mutated: `DRIFT: docs/conformance-baseline.md` + unified diff showing the reverted line + `Run: python3 scripts/report-conformance.py && git add -u` (exit 1). Reverted: `report-conformance: PASS — no drift` (exit 0) | PASS — both halves observed for the Markdown file |
| M6 — CONF-02 drift detection (`.json`) | Same byte-edit pattern on `docs/data/conformance.json`'s `measurement_date` field, `--check` before/after | Mutated: `DRIFT: docs/data/conformance.json` + unified diff + remediation line (exit 1). Reverted: `report-conformance: PASS — no drift` (exit 0) | PASS — both halves observed for the JSON file |
| M8 — D-04 agreement non-vacuity | Appended a new untraced bold claim (`**Additional consideration:** ...`, no citation) to the end of the twin `first-principles/agents/references/examples/personal-general.md` in scratch copy, ran bare | Headline `Source-vs-twin agreement (D-04)` dropped `14 of 14` → `13 of 14` pairs agree. D-04 section named the divergence: `- personal-general: conclusion_claims, untraced_claims` (both went 7→8 on the twin side; source stayed 7). No provenance column (`provenance_labels`, etc.) was touched by the mutation, and the headline moved anyway — this is the vacuity counter-check | PASS — pair-agreement is not vacuously matching `"n/a"` to `"n/a"`; it detects a real measured-field divergence |

Post-session: real tree `git status --porcelain` confirmed empty; `python3 scripts/report-conformance.py --check` exits 0 with `PASS — no drift`; `python3 scripts/report-conformance.py --self-test` exits 0 with `SELF-TEST PASS — 14 controls run`.

## Six Headline Figures As Rendered (`docs/conformance-baseline.md`)

| Reading | shared-examples | generated-twin | contract-surface |
|---|---|---|---|
| Files unreadable by `_slice_sections` | 4 of 14 | 4 of 14 | 0 of 1 |
| §6 conclusion claims (untraced) | 58 (56 untraced) | 58 (56 untraced) | 3 (3 untraced) |
| §2 verdict cells (non-conforming) | 69 (69 non-conforming) | 69 (69 non-conforming) | 1 (1 non-conforming) |
| §4 `chain_blocks` (malformed) | 10 (7 malformed) | 10 (7 malformed) | 3 (1 malformed) |
| `### Conclusion` heading-swept blocks (malformed) | 28 (19 malformed) | 28 (19 malformed) | 1 (0 malformed) |
| Source-vs-twin agreement (D-04) | 14 of 14 pairs agree | | |

The four unreadable files, confirmed by name on both surfaces: `composed-inversion-second-order.md`, `decompose-irreducibility.md`, `estimate-fermi.md`, `theoretical-limit-carnot.md`. Every figure matched both `17-CONTEXT.md` § Specific Ideas and `17-RESEARCH.md` § Summary exactly; no adjustment was made to either the artifact or the witnesses.

## Battery Tally

`bash scripts/check-firewall-battery.sh` reported `FIREWALL: GREEN (24/24)` after the artifacts landed — the count is unmoved from before this plan, matching D-06's explicit non-goal. The first run in this fresh worktree reported `FIREWALL: BLOCKED` (VAL-03's pytest-capable interpreter prerequisite unmet); `uv sync` provisioned `.venv` and the re-run was green. `.venv/` is gitignored and untracked; no source file changed by this remediation.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking issue] Worktree HEAD was stale at plan start — reset to the correct wave-1 base commit**
- **Found during:** Startup HEAD-safety assertion
- **Issue:** The worktree's initial HEAD (`d4da381`, a Phase 12 commit) predated the Phase 17 wave-1 merge entirely; `git merge-base HEAD <expected-base>` returned HEAD itself rather than the expected base, meaning the expected base commit (`21e8e617`, "chore: merge executor worktree" carrying plan 17-01's work) was a *descendant* of HEAD, not an ancestor.
- **Fix:** Per the worktree_branch_check protocol, ran `git reset --hard 21e8e617ce708c37e1248b475bbec2b5e933b8d9` and confirmed HEAD now matched. This is the documented recovery path in the plan's own startup instructions, not an improvised fix.
- **Files modified:** none (branch-pointer move only)
- **Commit:** N/A (pre-work repair, not a task deliverable)

**2. [Rule 3 - Blocking issue] Plan/context files absent from the worktree's gitignored `.planning/` tree**
- **Found during:** `files_to_read` step
- **Issue:** `.planning/` is project-gitignored; the worktree's copy only contained `17-01-SUMMARY.md` (force-tracked per project convention). `17-02-PLAN.md`, `17-CONTEXT.md`, `17-VALIDATION.md`, `17-RESEARCH.md`, `PROJECT.md`, `STATE.md`, `config.json` all existed only in the main repo checkout, not in this worktree.
- **Fix:** Copied the required files from `/home/chrisdavidson/Projects/first-principles-skill/.planning/` into the worktree's `.planning/` tree (read-only reference copies; none of these are git-tracked or part of this plan's deliverables).
- **Files modified:** none tracked by git (`.planning/` stays gitignored)
- **Commit:** N/A (local reference copies only, never staged)

**3. [Rule 1 - Bug in verification approach, not in the script] `git diff --quiet` against untracked files is vacuously true**
- **Found during:** Task 1, the "run bare command a second time, confirm `git diff --quiet` exits 0" step
- **Issue:** Immediately after the first bare run, the two artifacts were untracked (`??` in `git status`). `git diff` only compares tracked content against the index/working tree, so a `git diff --quiet` check at that point would pass regardless of whether the second write changed any bytes — a vacuous pass, not a real determinism proof.
- **Fix:** Staged both files with `git add` after the first write, then ran the bare command a second time, then ran `git diff --quiet` — now a real byte-for-byte comparison against the staged content. Confirmed exit 0.
- **Files modified:** none (verification methodology only; the script itself needed no change)
- **Commit:** folded into the verification record for `a2f190c`; no separate commit needed

### Auth gates
None encountered.

## Known Stubs
None. Both artifacts are fully generated, committed, and `--check`-clean.

## Threat Flags
None. All threat-register mitigations for this plan (T-17-06 scratch-copy containment, T-17-07 accepted public-disclosure risk, T-17-08 accepted tracked-drift risk, T-17-09 two-witness verification) were followed exactly as specified; no new security-relevant surface was introduced.

## Self-Check: PASSED

- FOUND: `docs/conformance-baseline.md`
- FOUND: `docs/data/conformance.json`
- FOUND: `.planning/phases/17-conformance-baseline/17-02-SUMMARY.md`
- FOUND commit `a2f190c` (Task 1)
