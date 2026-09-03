---
phase: 14-closure-ledger-claim-inventory
plan: 03
subsystem: testing
tags: [quality-harness, render-contract, registry, self-test, ledger, claim-inventory]

# Dependency graph
requires:
  - phase: 14-closure-ledger-claim-inventory (plan 02)
    provides: "R11, R12 and the amended R4 as byte-identical literals shipped on output-template.md, SKILL-body.md and (R11/R12 only) validation-rubric.md"
provides:
  - "_RENDER_RULE_LITERALS carrying R11/R12 and the amended R4, byte-identical to the shipped surfaces"
  - "_RENDER_SURFACE_REQUIRED_RULES (and its second inline transcription) requiring R11/R12 on the three D-06 surfaces, not on reason-upward.md"
  - "expected_literal_clauses pinning R4's disclosure half, R11's bound-1 hinge, and R12's non-discharge half"
  - "control (k) running 37 negative cases; expected_literal_digest recomputed over the final twelve-literal state"
affects: [15-scan]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Reconstruct a registered literal's Python source by extracting the surface's bare text programmatically and verifying the wrapped string-concatenation literal reconstructs byte-identically, rather than hand-transcribing long unicode-bearing prose"

key-files:
  created: []
  modified:
    - scripts/check-quality-harness.py

key-decisions:
  - "R4's clause pin repointed from the rule half ('A claim doing neither is cut, not softened') to D-01's disclosure half ('detected only when the row sits inside section 6'), following R7/R9/R10's own stated rationale (plans 13-08, 13-18, 13-25): the clause arm should pin the half a future edit is likeliest to quietly drop, which after this plan is the new disclosure, not the rule half that was already covered and is in no more danger than before"
  - "R11's clause pin targets bound 1 (the whole-line, uncited section-intro label) rather than the positive extraction rule, per CONTEXT.md D-07's naming of it as 'the hinge of detectable-from-the-emission-alone'"
  - "R12's clause pin targets D-09's non-discharge half ('the marker discloses the gap, it does not discharge the claim') rather than the marker's own bytes, since an author reading the marker as a discharge is the exact failure this phase exists to prevent"

patterns-established:
  - "Registered-literal insertion verified by round-tripping the Python string-concatenation source through exec() and asserting equality with the extracted surface text, before the Edit tool ever touches the file — catches transcription errors in long unicode prose (em dash, section sign, arrows) that eyeballing would miss"

requirements-completed: [LEDGER-01, LEDGER-02, LEDGER-03, LEDGER-04]

# Metrics
duration: ~25min
completed: 2026-09-03
---

# Phase 14 Plan 03: Register R11/R12 and Amended R4 in the Render Registry Summary

**Wired the R11 (claim-extraction), R12 (caveat) and amended R4 (citation) rule literals plan 14-02 shipped as prose into `_RENDER_RULE_LITERALS`, `_RENDER_SURFACE_REQUIRED_RULES` (both transcriptions), `expected_literal_clauses` and `expected_literal_digest`, so LEDGER-04's control half now holds — verified by mutation on disposable scratch copies, not by reading.**

## Performance

- **Duration:** ~25 min
- **Tasks:** 2 completed
- **Files modified:** 1 (`scripts/check-quality-harness.py`)

## Accomplishments

- `_RENDER_RULE_LITERALS["R4"]` amended with D-01's section-6-visibility disclosure and D-03's structural-row residual; `["R11"]` and `["R12"]` added as new registered literals — all three verified byte-identical to their shipped surface text by direct substring assertion against the live `shared/spine/**` files (not by reading).
- `_RENDER_SURFACE_REQUIRED_RULES` and its second inline transcription inside `_render_registry_lock_problems` both gained `"R11", "R12"` on `output-template.md`, `SKILL-body.md` and `validation-rubric.md`; `reason-upward.md`'s tuple is untouched. Required-rule case count is now 37 (12 + 12 + 8 + 5).
- `expected_literal_clauses["R4"]` repointed to the disclosure half; `["R11"]` and `["R12"]` added, each following R7/R9/R10's precedent of pinning the half most at risk of quiet softening.
- Control (k)'s `expected_missing_case_count` raised from 31 to 37; `expected_literal_digest` recomputed last, over the final twelve-literal state, from `sha256:301ef5ff8ebe97b8163800e9f9cc2b0daec1ac1b48a97a64ac1adc23ccf6e8f3` to `sha256:7834b5c5b51136e2403d41ad94bb126eaec785eddb2df4e0950f69654edbdd49`.
- `python3 scripts/check-quality-harness.py --self-test` exits 0 (all sub-checks, including `render_contract` and `ledger_traceability`, PASSED). `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (23/23)` (required `uv sync` to create a local `.venv` in this worktree first — VAL-03's pytest-capable-interpreter prerequisite was unmet, same one-time environment setup plans 14-01 and 14-02 documented).
- `_chain_block_well_formed` and its sha256 pin are byte-unchanged: `git diff HEAD -- scripts/check-quality-harness.py` across both commits shows no hunk naming that function.

## Task Commits

Each task was committed atomically:

1. **Task 1: Register the literals and their required surfaces** - `d0e5d73` (feat)
2. **Task 2: Repoint R4's clause pin, add R11/R12 clause pins, raise control (k)'s case count, and recompute the digest** - `23edd5f` (fix)

_No TDD tasks in this plan._

## Files Created/Modified

- `scripts/check-quality-harness.py` — R4 amended, R11/R12 added to `_RENDER_RULE_LITERALS`; `_RENDER_SURFACE_REQUIRED_RULES` and its second transcription extended to 37 required-rule cases; `expected_literal_clauses` repointed/extended; control (k)'s case-count floor raised to 37; `expected_literal_digest` recomputed

## Decisions Made

- Constructed the three registered-literal Python string-concatenation blocks programmatically — extracting the bare surface text (stripping the bold-label prefix) from `shared/spine/references/output-template.md`, wrapping it into implicit-concatenated string literals, and round-tripping through `exec()` to assert the reconstructed value equals the extracted surface text exactly — before inserting via Edit. This is not in the plan's action text but follows the plan's own instruction to "check the joined value programmatically rather than by eye," given the literals' length (up to ~1,180 bytes) and unicode content (em dash, section sign `§`, arrows `→`).
- Comments preceding each new/amended entry name plan 14-03, the requirement IDs (R11 → LEDGER-01/LEDGER-02; R12 → LEDGER-03; R4 → D-01/D-03) and the decision IDs, per the plan's explicit instruction.
- Recorded the rubric's declination of R4 with an inline comment above the `validation-rubric.md` tuple in `_RENDER_SURFACE_REQUIRED_RULES`, so a later reader does not read the absence as an oversight (plan's explicit instruction).

## Deviations from Plan

None — plan executed exactly as written. Both call-site orderings (literals → required-rules → second transcription → clauses → case-count → digest) were followed in the sequence the plan specifies, and the intermediate red state after Task 1 was observed and is recorded below as expected, not worked around.

## Intermediate Red State (Task 1, expected and observed)

Immediately after Task 1's commit and before Task 2's, `python3 scripts/check-quality-harness.py --self-test` failed with exactly the two problems the plan predicts:

```
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: literals: key set ['R1', 'R10', 'R11', 'R12', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9'] != expected ['R1', 'R10', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9']
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: literals: digest 'sha256:7834b5c5b51136e2403d41ad94bb126eaec785eddb2df4e0950f69654edbdd49' != pinned 'sha256:301ef5ff8ebe97b8163800e9f9cc2b0daec1ac1b48a97a64ac1adc23ccf6e8f3'
```

A third, related failure also appeared — control (h2)'s R1-gutted isolation case reported the key-set/digest mismatches instead of its own targeted "missing its required clause" message, because `expected_literal_clauses` had not yet gained R11/R12 keys. This is a direct, expected consequence of the same intermediate state (the clause key set is a subset check that now unconditionally disagrees with the literal key set) and resolved automatically once Task 2 added the R11/R12 clause entries — no separate fix was needed.

## Digest Change (old -> new, recorded per plan's explicit instruction)

- **Old:** `sha256:301ef5ff8ebe97b8163800e9f9cc2b0daec1ac1b48a97a64ac1adc23ccf6e8f3`
- **New:** `sha256:7834b5c5b51136e2403d41ad94bb126eaec785eddb2df4e0950f69654edbdd49`

## Mutation Verdicts (verbatim, per Task 2's acceptance criteria)

All mutations were performed on disposable `rsync -a --exclude .git` scratch copies under the scratchpad directory; `git status --porcelain` on the real worktree was confirmed empty before and after every mutation (the scratch copies themselves are not git repositories, since `.git` was excluded from the rsync).

**Mutation 1 — deleting R11's physical line from `shared/spine/references/validation-rubric.md`:**
```
self-test FAIL: render_contract (i) POSITIVE: shared/spine/references/validation-rubric.md: rule R11 is missing — deleted from this surface
```
Names both `validation-rubric.md` and `R11`, as required.

**Mutation 2 — changing one character inside `_RENDER_RULE_LITERALS["R12"]`** (lowercased the "C" in "Conclusion-section" at the start of the literal):
```
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: literals: digest 'sha256:d38b095234cb410dbf2a9014698fb2031ca3abacd422194ad911fee61ec8abab' != pinned 'sha256:7834b5c5b51136e2403d41ad94bb126eaec785eddb2df4e0950f69654edbdd49'
```
Digest mismatch fires, as required.

**Mutation 3 — deleting the `"R11"` entry from `expected_literal_clauses`:**
```
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: literals: key set ['R1', 'R10', 'R11', 'R12', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9'] != expected ['R1', 'R10', 'R12', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9']
self-test FAIL: render_contract (h2) LOCK NEGATIVE: case 'literals clause arm: R1 gutted (WR-01 reproduction)' produced no problem naming field 'literals' AND matching this case's arm 'is missing its required clause' — [...]
```
`literals: key set` mismatch fires, as required (plus the same cascading (h2) effect noted above, expected for the same structural reason).

## Measured Readings (verified by execution)

- `python3 scripts/check-quality-harness.py --self-test` — exit 0, all sub-checks PASSED (including `render_contract` and `ledger_traceability`)
- `bash scripts/check-firewall-battery.sh` — `FIREWALL: GREEN (23/23)`
- `grep -c 'sha256:301ef5ff8ebe97b8163800e9f9cc2b0daec1ac1b48a97a64ac1adc23ccf6e8f3' scripts/check-quality-harness.py` — 0 (old digest fully gone)
- `grep -c 'expected_missing_case_count = 37' scripts/check-quality-harness.py` — 1
- `grep -c 'expected_missing_case_count = 31' scripts/check-quality-harness.py` — 0
- `grep -c 'expected_required_rules' scripts/check-quality-harness.py` — 3
- `sum(len(v) for v in _RENDER_SURFACE_REQUIRED_RULES.values())` — 37
- `git diff HEAD -- scripts/check-quality-harness.py` (across both commits) — no hunk names `_chain_block_well_formed`

## Issues Encountered

- Same as plans 14-01 and 14-02: this worktree had no pytest-capable interpreter, so `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 22/23 passed)` naming `[PREREQ] VAL-03`. Resolved via `uv sync` (creates `.venv`, ships pytest 9.1.1); battery then reported `FIREWALL: GREEN (23/23)`. `.venv` is gitignored and was not committed.
- The `.planning/phases/14-closure-ledger-claim-inventory/` directory (containing this plan and the prior two plans' summaries) is not synced into a fresh worktree because `.planning/` is gitignored repo-wide. Copied `14-03-PLAN.md`, `14-CONTEXT.md`, `14-PATTERNS.md`, `PROJECT.md`, `STATE.md` and `config.json` from the main working tree into this worktree at the start of execution so the plan and its context could be read — a local-only, uncommitted copy of already-committed-elsewhere planning artifacts, not a tracked-tree change. This mirrors plan 14-01's identical note about the `.planning/captures/` fixture.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- LEDGER-04's control half now holds: dropping R11 or R12 from any of its three required surfaces fails `--self-test` naming the surface and the key (proven above by mutation).
- Plan 14-04 (out of scope for this plan) can now build `_RENDER_FIXTURE_SHAPE` entries and self-test controls scoring the nine worked-example blocks plan 14-02 rendered, against the R11/R12 literals this plan registered.
- Phase 15's claim-inventory scan can rely on R11/R12 being registered-and-checked, not merely stated.
- No blockers.

---
*Phase: 14-closure-ledger-claim-inventory*
*Completed: 2026-09-03*

## Self-Check: PASSED

- FOUND: scripts/check-quality-harness.py
- FOUND: .planning/phases/14-closure-ledger-claim-inventory/14-03-SUMMARY.md
- FOUND commit: d0e5d73 (Task 1)
- FOUND commit: 23edd5f (Task 2)
- CONFIRMED: `python3 scripts/check-quality-harness.py --self-test` exit 0
- CONFIRMED: `bash scripts/check-firewall-battery.sh` — FIREWALL: GREEN (23/23)
