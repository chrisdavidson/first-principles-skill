---
phase: 20-live-conformance
plan: 02
subsystem: testing
tags: [conformance, live-capture, quality-harness, provenance]

# Dependency graph
requires:
  - phase: 20-live-conformance
    provides: "plan 20-01 confirmed tests/live-conformance-v9.0/ is not a _FROZEN_PATHS member and recorded the working-tree body sha the runs measure"
provides:
  - "8 committed live .jsonl captures + 8 .md analyses under tests/live-conformance-v9.0/, one per tests/live-conformance-catalog.md row"
  - "Per-run outcome, byte size, line count and sha256 for every produced file, resolved via classify_invocation_outcome"
  - "Operator authorisation record (proceed-8, 2026-09-06) and post-dispatch human-verify approval"
affects: [20-03, 20-04, 20-05, 20-06]

# Tech tracking
tech-stack:
  added: []
  patterns: ["commit-per-run evidence capture for non-reproducible live artifacts"]

key-files:
  created:
    - tests/live-conformance-v9.0/Q-P1.jsonl
    - tests/live-conformance-v9.0/Q-P1.md
    - tests/live-conformance-v9.0/Q-P2.jsonl
    - tests/live-conformance-v9.0/Q-P2.md
    - tests/live-conformance-v9.0/Q-P3.jsonl
    - tests/live-conformance-v9.0/Q-P3.md
    - tests/live-conformance-v9.0/PR-P1.jsonl
    - tests/live-conformance-v9.0/PR-P1.md
    - tests/live-conformance-v9.0/PR-P2.jsonl
    - tests/live-conformance-v9.0/PR-P2.md
    - tests/live-conformance-v9.0/PR-N1.jsonl
    - tests/live-conformance-v9.0/PR-N1.md
    - tests/live-conformance-v9.0/PR-N2.jsonl
    - tests/live-conformance-v9.0/PR-N2.md
    - tests/live-conformance-v9.0/PR-P1-R2.jsonl
    - tests/live-conformance-v9.0/PR-P1-R2.md
  modified: []

key-decisions:
  - "Operator authorised proceed-8 (all 8 rows) on 2026-09-06, re-dispatch policy D-20-A confirmed"
  - "All 8 runs completed on first dispatch; no re-dispatch, no superseded/ entry"
  - "Operator approved Task 3's human-verify checkpoint on 2026-09-06 after independent re-verification"

requirements-completed: [CONF-09]

# Metrics
duration: 1h15m
completed: 2026-09-06
---

# Phase 20 Plan 02: Live Conformance Dispatch Summary

**8 of 8 authorised live `claude -p` runs against the HEAD working-tree body landed, each committed individually with outcome resolved by `classify_invocation_outcome`, exceeding CONF-09's floor of 5 with no shortfall.**

## Performance

- **Duration:** ~1h15m (Task 2 dispatch window: 2026-09-06T00:08 -> 01:23 local; Task 1 authorisation and Task 3 verification bracket it)
- **Started:** 2026-09-06 (Task 1 authorisation)
- **Completed:** 2026-09-06 (Task 3 operator approval)
- **Tasks:** 3 (1 decision checkpoint, 1 auto dispatch task, 1 human-verify checkpoint)
- **Files modified:** 16 (8 `.jsonl` + 8 `.md`, all newly created; zero script edits)

## Accomplishments

- Authorised and dispatched all 8 catalog rows (`Q-P1`, `Q-P2`, `Q-P3`, `PR-P1`, `PR-P2`, `PR-N1`, `PR-N2`, `PR-P1-R2`) one at a time against the working-tree body, committing each capture immediately after its own run.
- Every run's terminal outcome resolved mechanically via `classify_invocation_outcome` on the raw `.jsonl` — never inferred from exit code or grep.
- Zero transport-layer stubs: all 8 runs completed cleanly on the first dispatch, so D-20-A's re-dispatch policy was never invoked and no `superseded/` directory exists.
- Verified `git status --porcelain tests/live-conformance-v9.0` is empty, one commit per run (8 commits), and `report-conformance.py --check` / `check-firewall-battery.sh` both green with no drift.

## Task 1: Authorisation Record

**Operator decision, verbatim:** `proceed-8` — "Dispatch all 8 rows now."
**Date:** 2026-09-06 UTC.
**Authorised id list:** `Q-P1`, `Q-P2`, `Q-P3`, `PR-P1`, `PR-P2`, `PR-N1`, `PR-N2`, `PR-P1-R2`.
**Re-dispatch policy confirmed:** D-20-A — one dispatch per row, at most one authorised re-dispatch for a transport-layer stub, superseded captures retained under `tests/live-conformance-v9.0/superseded/` and logged by sha256. No `.jsonl` existed under `tests/live-conformance-v9.0/` at authorisation time (confirmed by plan 20-01's `.gitkeep`-only state).

## Task 2: Per-Run Table

All values below were independently recomputed in this continuation session (sha256 via `sha256sum`, outcome via a fresh `classify_invocation_outcome` call, byte size and line count via `stat`/line-count on the files as committed) rather than copied from Task 2's own output.

| ID | Outcome | `.md` present | `.jsonl` bytes | `.jsonl` lines | `.jsonl` sha256 | `.md` sha256 |
|---|---|---|---|---|---|---|
| Q-P1 | completed | yes | 216898 | 61 | `6f0c94e01d0e7f7be9613443514bcf5dddaf4e0c67a5ea3ebe3c0e2c45a419a7` | `54a0140485c19a74eb62434b2aa2537db9bb63f340e9db24be14bc08fd1b3871` |
| Q-P2 | completed | yes | 189059 | 44 | `dc478c05788d6df5c31e2b3cbcff543002c3e8c35da6deb2685474b59a661c0b` | `f8a4fa7e234249feded17deb2683063337088a16f29435e5e7fae941c712dea2` |
| Q-P3 | completed | yes | 710590 | 94 | `433ec5a3ffeea5a09a690b150a8b3be18366c6891a5dcced90c2ad8fd0ab122c` | `8adfcc66ad1d445cf866974e1023b5f7ee03f62d7cf5a6878781c7320efc30a4` |
| PR-P1 | completed | yes | 241287 | 71 | `30cfeffda0476e04ad6eee88496e060ea78e1cd9842bc14bace1b38b463f2263` | `31ca943a45737d96e99794350549cfb40629af0145e3045c6be553d1823b473b` |
| PR-P2 | completed | yes | 241669 | 54 | `3c46807dcd32f4043f626f7c520c4ffd2de0e79bfd49c948299949352b6b2f03` | `e057d8adebb5cb53fd90842ffd7a7de8aaf39d0cef70449a2159a9da6206ec4e` |
| PR-N1 | completed | yes | 256671 | 82 | `0a5d6928a18b77c2396688730f0c77e48eb358754fc9d72825f8b81ce1766f7a` | `e90b82f139a426759965f597e87e4534b9a3b0c4aed6f049c4ff3a081bfe11b5` |
| PR-N2 | completed | yes | 239423 | 68 | `91ce6d8bd8b698904c4b8f29d8fb5b79dda0e8e67bd1693ab6ec258fcbbd4f1f` | `f0e9381843dc3929efc683d34e4819b58f34268ff4d20e46516f4ed7254ab6f8` |
| PR-P1-R2 | completed | yes | 258312 | 83 | `d53c721146ce2738ebf5cfce9b3ed896d8b387e62537e542ec00b91ca95dbc52` | `205678ffcaf4e45c1cf6410f7954276882131eea1fcb748527e34938117f5d32` |

**Superseded attempts:** none. No row produced a `rate_limit_stub`, `transport_error_stub`, or `no_terminal_result` outcome; `tests/live-conformance-v9.0/superseded/` does not exist.

**8 of 8 authorised runs landed** — exceeding CONF-09's floor of 5 by 3, with no shortfall to record.

## Task Commits

1. **Task 1: Authorise the live spend** — no file written (authorisation gate; recorded above).
2. **Task 2: Dispatch each authorised run** — 8 individual commits, one per run:
   - `c1ba57a` — `test(20-02): land live capture Q-P1 (completed)`
   - `ca71be6` — `test(20-02): land live capture Q-P2 (completed)`
   - `bb430a1` — `test(20-02): land live capture Q-P3 (completed)`
   - `d030f4b` — `test(20-02): land live capture PR-P1 (completed)`
   - `b8363a4` — `test(20-02): land live capture PR-P2 (completed)`
   - `7790a3e` — `test(20-02): land live capture PR-N1 (completed)`
   - `9ddffbc` — `test(20-02): land live capture PR-N2 (completed)`
   - `b264e50` — `test(20-02): land live capture PR-P1-R2 (completed)`
3. **Task 3: Confirm every capture landed** — no file written (verification gate; approved below).

**Plan metadata:** this commit (docs: complete plan).

## Task 3: Human-Verify Checkpoint — Operator Approval

**Operator response, verbatim: "approved"** — given 2026-09-06, after reviewing the verification table.

Every claim in the checkpoint was independently re-verified in this continuation session before recording approval, not merely re-stated:

- 8 `.jsonl` + 8 `.md` pairs present under `tests/live-conformance-v9.0/` — confirmed via `ls -la`.
- Roster is set-equal to the catalog's 8 ids — confirmed: `Q-P1, Q-P2, Q-P3, PR-P1, PR-P2, PR-N1, PR-N2, PR-P1-R2`, no row dropped, none added.
- All 8 outcomes independently re-derived through `classify_invocation_outcome` in this session -> all `completed` (see table above; not copied from Task 2's own report).
- `git status --porcelain tests/live-conformance-v9.0` -> empty, confirmed.
- One commit per run, 8 commits, confirmed via `git log --oneline -- tests/live-conformance-v9.0`.
- No `superseded/` directory — confirmed, D-20-A's re-dispatch path was never taken.
- `/usr/bin/grep -c 'live-conformance' scripts/check-firewall-battery.sh` -> `0`, correct per D-20-C (freezing is plan 20-06's job).
- `python3 scripts/report-conformance.py --check` -> `report-conformance: PASS — no drift`, exit 0.
- `bash scripts/check-firewall-battery.sh` -> `FIREWALL: GREEN (25/25)`.

## Operator Observation Raised at the Task 3 Gate (finding for plan 20-03/20-04, not a defect fixed here)

Five of the eight captures (all five `PR-*` rows — `PR-P1`, `PR-P2`, `PR-N1`, `PR-N2`, `PR-P1-R2`; none of the three `Q-*` rows) open by disclosing that `AskUserQuestion` was unavailable. Verified directly against the committed `.md` files in this session (`grep -i AskUserQuestion`): all 5 `PR-*` files hit, all 3 `Q-*` files do not.

This is the Input Contract's prescribed fallback (`shared/agent/input-contract.md` lines 23-30) firing under `_run_prompt_to`'s Plan-36-locked, non-interactive `claude -p` transport — **not a malfunction, and the transport must not be changed.**

Established at the gate:

- **Incidence is prompt-correlated:** 5/5 terse `PR-*` rows disclose; 0/3 figure-dense `Q-*` rows disclose.
- **No measured conformance penalty:** the worst run in the corpus by verdict-cell nonconformance is `Q-P2` (a non-disclosure row); `silent_untraced_claims` is 0 across all eight captures regardless of disclosure status.
- **Longitudinal comparability holds:** the prior committed live fixtures `tests/quality-provenance-v8.24/PR-P1.md` and `tests/quality-ledger-v8.26/PR-P1.md` carry the same disclosure, so the `PR-P1-R2` longitudinal comparison against them is like-for-like, not an artifact of this session's transport.

Plan 20-04 has been amended to publish this as a non-interactive-branch scope bound on the rate. **No capture was re-dispatched on account of this observation** — it is filed as a finding, not treated as a defect requiring rework.

## Structural Non-Uniformity Observed (input to plan 20-03's scoring/disposition work — not scored, dispositioned, or fixed here)

The eight analyses do not share one heading shape at the top level. Verified directly against all 8 committed `.md` files (`grep -n '^# '`):

- **Six rows** (`Q-P1`, `Q-P3`, `PR-P1`, `PR-P1-R2`, `PR-P2`, `PR-N1`) render a single top-level `# First-Principles Analysis: <title>` heading, with the six numbered sections nested one level down as `## 1. Problem Essence` … `## 6. Conclusion` (confirmed on `PR-N1`).
- **Two rows** (`Q-P2`, `PR-N2`) render the six numbered sections directly as top-level headings — `# 1. Problem Essence` … `# 6. Conclusion` — with no enclosing title heading at all.

Note: this diverges in one specific detail from the orchestrator's Task-3 pre-approval note, which characterised `PR-N2` as carrying "no numbered sections at all" — direct inspection shows `PR-N2` *does* carry numbered sections (`# 1.` through `# 6.`, top-level, same shape as `Q-P2`), it simply lacks the enclosing title heading the other six rows carry. The corrected, verified finding is recorded here per the definition of done (observed output, not paraphrase) and is unchanged in substance: the corpus does not share one heading shape, which is exactly the input plan 20-03 needs. This is not scored, dispositioned, or fixed in this plan.

## Files Created/Modified

- `tests/live-conformance-v9.0/Q-P1.jsonl` / `.md` — completed live capture, Q-P1 (gRPC migration commitment prompt)
- `tests/live-conformance-v9.0/Q-P2.jsonl` / `.md` — completed live capture, Q-P2 (subscription loyalty program prompt)
- `tests/live-conformance-v9.0/Q-P3.jsonl` / `.md` — completed live capture, Q-P3 (attic insulation vs. windows prompt)
- `tests/live-conformance-v9.0/PR-P1.jsonl` / `.md` — completed live capture, PR-P1 (AWS bill / serverless premise-rejection prompt)
- `tests/live-conformance-v9.0/PR-P2.jsonl` / `.md` — completed live capture, PR-P2 (database schema premise-rejection prompt)
- `tests/live-conformance-v9.0/PR-N1.jsonl` / `.md` — completed live capture, PR-N1 (TLS certificate renewal prompt)
- `tests/live-conformance-v9.0/PR-N2.jsonl` / `.md` — completed live capture, PR-N2 (image pipeline cost prompt)
- `tests/live-conformance-v9.0/PR-P1-R2.jsonl` / `.md` — completed live capture, PR-P1-R2 (PR-P1's prompt re-dispatched byte-for-byte for the D-02 longitudinal comparison)

No script, no `shared/` source file, and no other tracked file was modified by this plan.

## Decisions Made

- **Operator authorised `proceed-8`** (2026-09-06): dispatch all 8 catalog rows in one session rather than the 5-row minimum, buying the full topic spread plus the `PR-P1`/`PR-P1-R2` longitudinal pair.
- **No re-dispatch needed**: all 8 runs completed cleanly on first dispatch, so D-20-A's stub-handling branch was never exercised in practice.
- **Operator approved Task 3** (2026-09-06) after this session's independent re-verification of every checkpoint claim, rather than trusting the prior agent's report at face value.

## Deviations from Plan

None — plan executed exactly as written. Task 1 and Task 2 were completed and committed by a prior agent in this same session lineage (commits `c1ba57a` through `b264e50`); this continuation agent's role was limited to closing Task 3 and did not alter, add to, or remove any capture file.

## Issues Encountered

None. All 8 live dispatches completed on the first attempt; no transport-layer stub, no `MultipleAgentDispatchError`, no extraction failure.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- All 8 captures are committed, byte-verified, and outcome-verified — the irreplaceable evidence plan 20-03 through 20-06 depend on is durably in git.
- Plan 20-03 has two concrete inputs waiting from this plan: (1) the AskUserQuestion-disclosure finding, prompt-correlated and penalty-free, to fold into its disposition write-up; (2) the heading-shape non-uniformity across the 8 `.md` files, to account for in its scoring pass.
- Plan 20-04 is already amended (per the orchestrator's pre-approval note) to publish the non-interactive-branch disclosure rate as a documented scope bound.
- No blockers. Battery GREEN 25/25, `report-conformance.py --check` clean, zero script edits, three CONTRACT-06 pins untouched by this plan (no script was run through `--self-test` mutation in this session beyond the standard battery/report checks, both of which passed).

---
*Phase: 20-live-conformance*
*Completed: 2026-09-06*

## Self-Check: PASSED

All claimed files exist on disk and all claimed commits resolve in `git log --oneline --all`:

- `20-02-SUMMARY.md` — FOUND
- `c1ba57a`, `ca71be6`, `bb430a1`, `d030f4b`, `b8363a4`, `7790a3e`, `9ddffbc`, `b264e50` (Task 2 per-run commits) — FOUND
- `96703db` (this plan's metadata commit) — FOUND

No missing items.
