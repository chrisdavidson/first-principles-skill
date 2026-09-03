---
phase: 13-chain-head-grammar
plan: 18
subsystem: quality-harness
tags: [chain-head-grammar, rendering-contract, positional-bound, gap-closure, CR-02]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar (plan 08, BL-01)
    provides: the R7 positional-bound disclosure pattern this plan mirrors onto R9 —
      appended disclosure sentence, re-pointed pinned clause, recomputed digest
  - phase: 13-chain-head-grammar (plan 09, BL-02)
    provides: R9's original unconditional-refusal literal, mirrored on three
      canonical surfaces, that this plan amends
provides:
  - R9's literal now carries a measured positional-bound disclosure sentence,
    byte-identical on all three canonical surfaces (output-template.md,
    SKILL-body.md, validation-rubric.md) and in the generated tree
  - expected_literal_clauses["R9"] re-pointed from the negative-refusal half to
    the disclosure half, mirroring plan 13-08's identical re-point for R7
  - expected_literal_digest recomputed from the live, edited
    _RENDER_RULE_LITERALS
  - the four-row positional measurement (0/1/2/3 preceding hops ->
    False/False/True/True) re-run directly against the live, unmutated
    _chain_block_well_formed and recorded verbatim below
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A rule's published prose must be scoped to exactly what its pinned
      mechanical detector enforces — when a sibling rule (R7) already
      received this exact disclosure treatment, the fix is to reproduce the
      measurement independently rather than transcribe the review's prose,
      then apply the same shape (append, don't rewrite; re-point the clause
      arm at the disclosure half; recompute the digest)."

key-files:
  created: []
  modified:
    - scripts/check-quality-harness.py
    - shared/spine/references/output-template.md
    - shared/spine/SKILL-body.md
    - shared/spine/references/validation-rubric.md
    - first-principles/agents/first-principles.md
    - first-principles/agents/references/output-template.md
    - first-principles/agents/references/validation-rubric.md

key-decisions:
  - "Re-measured the four-row positional table directly against the live,
    unmutated _chain_block_well_formed before writing any prose, per hard
    constraint and the plan's own fail-fast instruction. Result matched the
    planner's prediction exactly: False/False/True/True at 0/1/2/3 preceding
    hops — recorded verbatim below with the exact block text used."
  - "Used 13-REVIEW.md CR-02's fix-sketch wording verbatim for the appended
    disclosure sentence so the published bound matches what the reviewer
    reproduced, per the plan's action text."
  - "Ran the M1/M2/M3 mutation sweep against the Task-1+Task-2 complete state
    (both the module literal and the three surfaces amended) rather than
    against the Task-1-only intermediate state, because M3's clause-arm
    behavior cannot be isolated while the surfaces still report the literal
    entirely missing — confirmed empirically: running M3(a) against the
    Task-1-only state produces the same three missing-surface failures
    regardless of the clause mutation, masking the arm under test."

requirements-completed: [CHAINHEAD-01, CHAINHEAD-02, CHAINHEAD-03, CHAINHEAD-04]

# Metrics
duration: ~15min
completed: 2026-09-03
---

# Phase 13 Plan 18: R9 positional-bound disclosure (CR-02 literal half) Summary

R9's GT-leading-hop refusal no longer states an enforcement claim its instrument does not honour: the literal now carries the same measured positional-bound disclosure sentence R7 already carries, byte-identically on all three canonical surfaces, with its pinned clause re-pointed at the disclosure half and its digest recomputed.

## Performance

- **Duration:** ~15 min
- **Completed:** 2026-09-03
- **Tasks:** 3/3 completed
- **Files modified:** 7

## Accomplishments

- Re-measured R9's real positional bound directly against the live, unmutated `_chain_block_well_formed` (not transcribed from review prose) and confirmed the planner's predicted False/False/True/True transition.
- Amended `_RENDER_RULE_LITERALS["R9"]` by appending the disclosure sentence, re-pointed `expected_literal_clauses["R9"]` at the disclosure half, and recomputed `expected_literal_digest`.
- Mirrored the amended R9 text byte-identically onto all three canonical surfaces and regenerated the tree; `validation-rubric.md`'s running paragraph kept the trailing "Hops rendered as an ordered list" sentence and R1/R7's literals intact as contiguous substrings.
- Proved `_chain_block_well_formed` and `_CHAIN_DETECTOR_PINNED_DIGEST` byte-unchanged (no diff hunk overlaps the function's 4277-4397 line range), the coverage headline unmoved at `175/91/0/266`, and the battery `FIREWALL: GREEN (23/23)`.

## Task Commits

1. **Task 1: Measure R9's real positional bound, then amend the R9 literal and its pinned clause and recompute the literal digest** - `d8cfccb` (fix)
2. **Task 2: Mirror the amended R9 text byte-identically onto the three canonical surfaces and regenerate** - `a9821df` (fix)
3. **Task 3: Prove the frozen detector untouched, the headline unmoved, and the battery green** - no file changes (evidence-only task; all gates passed on the first run after Task 2's commit, so nothing required editing)

**Plan metadata:** (this commit, following SUMMARY creation)

## Files Created/Modified

- `scripts/check-quality-harness.py` - R9's literal gains the disclosure sentence; `expected_literal_clauses["R9"]` re-pointed; `expected_literal_digest` recomputed
- `shared/spine/references/output-template.md` - R9's §4 scope-note paragraph gains the disclosure sentence, byte-identical to the module literal
- `shared/spine/SKILL-body.md` - same amendment, byte-identical
- `shared/spine/references/validation-rubric.md` - same amendment inserted in place inside Criterion 4's running paragraph, ahead of the trailing "Hops rendered as an ordered list" sentence
- `first-principles/agents/first-principles.md` - regenerated via `sync-content.py --write`
- `first-principles/agents/references/output-template.md` - regenerated
- `first-principles/agents/references/validation-rubric.md` - regenerated

## Measurement Record (Task 1, pre-write)

Driven directly against the live, unmutated `_chain_block_well_formed` (pure-function call via `importlib.util.spec_from_file_location`, no scratch copy, no tree mutation). Head and offending hop match the shipped `R-HEAD-GTHOP-BAD` fixture bytes exactly:

- Head: `C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)`
- Offending hop: `→ GT-4's stated duty cycle is the binding term in both estimates`
- Filler hops (ordinary, non-offending): `→ the bracket straddles zero, so its two ends recommend opposite actions`; `→ the second reading is the binding one`

| Preceding ordinary hops | Block text | Verdict |
|---|---|---|
| 0 | `C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)`<br>`→ GT-4's stated duty cycle is the binding term in both estimates` | `False` |
| 1 | `C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)`<br>`→ the bracket straddles zero, so its two ends recommend opposite actions`<br>`→ GT-4's stated duty cycle is the binding term in both estimates` | `False` |
| 2 | `C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)`<br>`→ the bracket straddles zero, so its two ends recommend opposite actions`<br>`→ the second reading is the binding one`<br>`→ GT-4's stated duty cycle is the binding term in both estimates` | `True` |
| 3 | `C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)`<br>`→ the bracket straddles zero, so its two ends recommend opposite actions`<br>`→ the second reading is the binding one`<br>`→ a third filler hop that states one ordinary inference`<br>`→ GT-4's stated duty cycle is the binding term in both estimates` | `True` |

Result: `False/False/True/True` — matches the planner's prediction exactly. The published sentence's threshold ("fewer than two hops precede it") matches this measured transition point (transition between 1 preceding hop, detected, and 2 preceding hops, not detected).

## Digest Derivation

- **Pre-plan `expected_literal_digest`:** `sha256:199469956b572956ff2b09cbd82e48389d989c6eecff5382d0b96ab34bd2894b`
- **Post-plan `expected_literal_digest`:** `sha256:1990944390d22d07dcace92290262159bdfa8c09a2686534c6e300f621aebe00`
- **Derivation command** (run against the live, edited module):

```python
import sys, hashlib, importlib.util
spec = importlib.util.spec_from_file_location("cqh", "scripts/check-quality-harness.py")
cqh = importlib.util.module_from_spec(spec)
sys.modules["cqh"] = cqh
spec.loader.exec_module(cqh)
literals = cqh._RENDER_RULE_LITERALS
digest = "sha256:" + hashlib.sha256(
    "\x00".join(f"{k}={v}" for k, v in sorted(literals.items())).encode("utf-8")
).hexdigest()
print(digest)
```

Output: `sha256:1990944390d22d07dcace92290262159bdfa8c09a2686534c6e300f621aebe00` — matches the value pasted into `expected_literal_digest` and the mismatch the self-test reported before the digest was updated.

## Intermediate Self-Test Failure (between Task 1 and Task 2)

Immediately after Task 1's literal/clause/digest edit, before Task 2 mirrored the text onto the three surfaces, `python3 scripts/check-quality-harness.py --self-test` failed as expected, naming exactly the three surfaces (positive evidence control (i) reaches all three):

```
self-test FAIL: render_contract (i) POSITIVE: shared/spine/references/output-template.md: rule R9 is missing — deleted from this surface
self-test FAIL: render_contract (i) POSITIVE: shared/spine/SKILL-body.md: rule R9 is missing — deleted from this surface
self-test FAIL: render_contract (i) POSITIVE: shared/spine/references/validation-rubric.md: rule R9 is missing — deleted from this surface
self-test: render_contract sub-check FAILED
```

(The digest mismatch that would otherwise also fire here was already resolved in the same Task-1 edit, since the digest was recomputed from the live post-edit literals in the same commit.)

## Byte-Identity Extraction Comparisons (Task 2)

Extracted `_RENDER_RULE_LITERALS["R9"]` (629 bytes) from the live module and compared by substring containment against each surface's live text:

```python
r9 = cqh._RENDER_RULE_LITERALS["R9"]
for path in [
    "shared/spine/references/output-template.md",
    "shared/spine/SKILL-body.md",
    "shared/spine/references/validation-rubric.md",
]:
    text = open(path, encoding="utf-8").read()
    print(path, "contains literal:", r9 in text)
```

Output:
```
shared/spine/references/output-template.md contains literal: True
shared/spine/SKILL-body.md contains literal: True
shared/spine/references/validation-rubric.md contains literal: True
```

All three: `True`. `grep -c "only while fewer than two hops precede it"` on each of the three surfaces also returned `1` (present exactly once, no duplicate transcription). On `validation-rubric.md`, `grep -c "Hops rendered as an ordered list"` returned `1` (trailing sentence intact) and `_RENDER_RULE_LITERALS["R1"]`/`["R6"]`/`["R7"]`/`["R8"]`/`["R9"]` were all independently confirmed as contiguous substrings of the live paragraph text (all `True`).

## Mutations

All mutations run on disposable `rsync -a --exclude .git --exclude .venv --exclude .planning ./ /tmp/.../scratch<N>/` copies; `git status --porcelain` on the real tracked tree confirmed empty (no unexpected changes) before the first mutation and after every mutation cycle.

**MUTATION M1, case 1** — delete the R9 disclosure sentence from `shared/spine/references/output-template.md` alone (run against the Task-1+Task-2 complete state):
```
self-test FAIL: render_contract (i) POSITIVE: shared/spine/references/output-template.md: rule R9 is missing — deleted from this surface
```
Exit 1.

**MUTATION M1, case 2** — same deletion from `shared/spine/SKILL-body.md` alone:
```
self-test FAIL: render_contract (i) POSITIVE: shared/spine/SKILL-body.md: rule R9 is missing — deleted from this surface
```
Exit 1.

**MUTATION M1, case 3** — same deletion from `shared/spine/references/validation-rubric.md` alone:
```
self-test FAIL: render_contract (i) POSITIVE: shared/spine/references/validation-rubric.md: rule R9 is missing — deleted from this surface
```
Exit 1.

**MUTATION M2** — restore `expected_literal_digest` to its pre-plan value (`sha256:199469956b572956ff2b09cbd82e48389d989c6eecff5382d0b96ab34bd2894b`) while the new literal stays in place (run against the Task-1+Task-2 complete state):
```
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: literals: digest 'sha256:1990944390d22d07dcace92290262159bdfa8c09a2686534c6e300f621aebe00' != pinned 'sha256:199469956b572956ff2b09cbd82e48389d989c6eecff5382d0b96ab34bd2894b'
```
Exit 1.

**MUTATION M3, direction (a)** — revert `expected_literal_clauses["R9"]` to the pre-plan refusal substring (`a hop must not begin with a \`GT-N\` identifier`) while the literal carries the new disclosure text:
```
(no render_contract FAIL lines; self-test exit 0, all sub-checks including render_contract and chain_detector_pin PASSED)
```
Exit 0 — confirms the re-point is a judgement call, not gate-forced: the pre-plan refusal substring is still present inside the amended literal, so the clause arm alone cannot distinguish it.

**MUTATION M3, direction (b)** — perturb the new disclosure clause by one token (`two` → `three`):
```
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: literals: R9 is missing its required clause 'detects that violation only while fewer than three hops precede it'
```
Exit 1.

Both M3 directions confirmed on the Task-1+Task-2 complete state (running M3(a) against the Task-1-only intermediate state instead produces the same three missing-surface failures regardless of the clause mutation, which would mask the arm under test — recorded as the reason for deferring the mutation sweep to after Task 2, see Decisions above).

## `_chain_block_well_formed` Byte-Identity Evidence (Task 3)

`_chain_block_well_formed` spans lines 4277-4397 of `scripts/check-quality-harness.py` (confirmed by locating the function's `def` line and the next top-level `def _chain_detector_source` at line 4401). `_CHAIN_DETECTOR_PINNED_DIGEST` sits at line 4436.

`git diff c35444aa374ac802e486d91eac714bb9394a2d1f HEAD -- scripts/check-quality-harness.py` hunk ranges (measured):
```
@@ -7241,7 +7241,14 @@
@@ -7249,7 +7256,11 @@
@@ -7917,9 +7928,13 @@
@@ -7952,7 +7967,7 @@
```
All four hunks land at line 7241 or later — none overlap the function's 4277-4397 range. `grep -c "_CHAIN_DETECTOR_PINNED_DIGEST"` against the same diff returned `0` — the pin is absent from the diff entirely. `chain_detector_pin` sub-check: `self-test: chain_detector_pin sub-check PASSED`.

## Gate Verdicts (Task 3, final)

1. `python3 scripts/check-quality-harness.py --self-test` → exit 0, all sub-checks (including `render_contract` and `chain_detector_pin`) PASSED.
2. `python3 scripts/check-traceability.py --self-test` → exit 0; headline line: `HEADLINE-LOCK PASS: published headline == 175 reproducible / 91 audit-only / 0 gap / 266 total` — unmoved, confirmed by running the gate.
3. `python3 scripts/sync-content.py --check` → exit 0, no output (no drift).
4. `bash scripts/check-firewall-battery.sh` → final line `FIREWALL: GREEN (23/23)`, exit 0.
   - First run hit `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 22/23 passed)` on VAL-03 (`[PREREQ] VAL-03 — no pytest-capable interpreter found`), the same prerequisite gap plan 13-08 documented for this same worktree. Ran `uv sync` (documented CLAUDE.md remedy) to create `.venv`; re-ran to `FIREWALL: GREEN (23/23)`. See Deviations below.
5. `git status --porcelain` on the real tree: empty immediately before the first scratch mutation and empty (aside from the untracked, gitignored `.venv/` created by `uv sync`) after all scratch work and after the final battery run.

## Decisions Made

- Reproduced the four-row positional measurement independently against the live detector rather than transcribing the review's prose, per the plan's fail-fast instruction — the measurement matched the planner's prediction, so no deviation was needed.
- Deferred the M1/M2/M3 mutation sweep to after Task 2 landed (see key-decisions above) so the clause/digest arms could be isolated from the still-missing-surface failures that dominate the Task-1-only intermediate state.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - blocking prerequisite] VAL-03 blocked on a missing `.venv`**
- **Found during:** Task 3's closing verification, first `bash scripts/check-firewall-battery.sh` run.
- **Issue:** This worktree had no `.venv`, so no pytest-capable interpreter was found; VAL-03 reported `[PREREQ]` and the battery printed `FIREWALL: BLOCKED` (exit 2), not a gate failure. Identical to the prerequisite gap plan 13-08 documented for the same worktree lineage.
- **Fix:** Ran `uv sync` (documented remedy in CLAUDE.md's own VAL-03 note) to create `.venv`, then re-ran the battery to `FIREWALL: GREEN (23/23)`.
- **Files modified:** none (`.venv/` is gitignored, not committed).

---

**Total deviations:** 1 auto-fixed (1 blocking prerequisite)
**Impact on plan:** No scope creep; the prerequisite fix is a one-time worktree setup step documented as the standard remedy, not a code change.

## Issues Encountered

None beyond the documented VAL-03 prerequisite gap above.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- R9's positional bound is now disclosed exactly as R7's is; both head-grammar sub-rules whose enforcement instrument is the frozen `_chain_block_well_formed` now state accurate, measured enforcement claims.
- This plan closes only the literal half of gap 1 (`13-VERIFICATION.md` criterion 1, CR-02). Per the plan's explicit scope note: the fixture pinning the non-detected position (R9's analogue of R7's `R-HEAD-PROSE-MID`) is plan 13-19's deliverable, not this plan's; both `| QUAL-01 |` doc-row corrections are plan 13-21's, deferred so they are corrected once against the final code state.
- Gap 2 (`shared/references/reason-upward.md` unregistered as a fourth canonical surface, CR-03) and the CR-01 two-arrow-floor doc-row misattribution remain open, tracked by other plans in this wave — not addressed here per hard constraints 5 and 6.

## Self-Check: PASSED

- `scripts/check-quality-harness.py` — FOUND
- `shared/spine/references/output-template.md` — FOUND
- `shared/spine/SKILL-body.md` — FOUND
- `shared/spine/references/validation-rubric.md` — FOUND
- `first-principles/agents/first-principles.md` — FOUND
- `first-principles/agents/references/output-template.md` — FOUND
- `first-principles/agents/references/validation-rubric.md` — FOUND
- `.planning/phases/13-chain-head-grammar/13-18-SUMMARY.md` — FOUND
- Commit `d8cfccb` — FOUND in `git log --oneline --all`.
- Commit `a9821df` — FOUND in `git log --oneline --all`.
- Commit `08902c4` — FOUND in `git log --oneline --all`.

---
*Phase: 13-chain-head-grammar*
*Completed: 2026-09-03*
