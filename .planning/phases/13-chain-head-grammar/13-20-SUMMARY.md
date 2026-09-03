---
phase: 13-chain-head-grammar
plan: 20
subsystem: quality-harness
tags: [chain-head-grammar, rendering-contract, surface-registration, gap-closure, CR-03]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar (plan 19, CR-02 fixture half)
    provides: the R-HEAD-GTHOP-LATE fixture and the fifteen/ten derived
      counts this plan inherits unchanged in `_selftest_render_contract`
provides:
  - `shared/references/reason-upward.md` registered as the fourth
    `_RENDER_RULE_SURFACES` entry, carrying R6 (unwrapped to byte-identity),
    R7, R8 and R9 byte-identically
  - the shipped, slash-invocable `first-principles/skills/reason-upward/
    SKILL.md` carrying the same four literals via `{{PROCEDURE:reason-
    upward}}` — closing the gap where `/reason-upward` prescribed the chain
    form with no head-input rule at all
  - `_RENDER_SURFACE_REQUIRED_RULES["shared/references/reason-upward.md"]`
    = `("R6", "R7", "R8", "R9")`, the registry-lock's extended inline
    expectations, and control (k)'s case-count floor moved 23 -> 27
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Registering a fourth canonical surface follows the same fork plan
      11-07 (CR-01) took for the rubric: register rather than delete the
      chain form, because a slash-invoked stub has no companion surface to
      carry the rule for it — the register-side argument is strictly
      stronger here than it was for the rubric."
    - "Verify-by-mutation surfaced a genuine mismatch between the plan's
      predicted failure arm and the measured one (MUTATION Q2): the plan
      named control (j) as the second firing arm, but (j) derives its
      expected set from the same live `_RENDER_RULE_SURFACES` tuple being
      mutated, so it cannot independently catch a shrink of that tuple.
      The measured second arm was (k) CASE-COUNT FLOOR, not (j) — the
      property (\"de-registration fails on two independent arms\") still
      held, just not the two arms predicted."

key-files:
  created: []
  modified:
    - shared/references/reason-upward.md
    - scripts/check-quality-harness.py
    - first-principles/skills/reason-upward/SKILL.md

key-decisions:
  - "Option A (register the surface) chosen over Option B (delete the chain
    form and point at the output template), per the must_haves' own
    argument: this phase's 11-07/CR-01 precedent registered rather than
    deleted, and the register-side case is stronger here because a
    slash-invoked skill stub has no agent body beside it to carry the
    missing rule. Option B rejected concretely: a stub cannot follow a
    pointer into `shared/spine/` (not shipped), and pointing into the
    plugin's agent reference tree would recreate the exact coupling
    `LAUNCHER_SKILLS`'s own comment names as the reason the launcher
    pattern exists."
  - "Gave `shared/references/reason-upward.md` the same four required keys
    as the rubric (R6-R9, not R1-R5) — it is a focused-mode procedure
    reference, not the output spec, so it has no business stating the
    citation rule (R4), the brevity TELL (R3) or R1/R2/R5. It still gets
    the unscoped contradiction scan regardless of this narrower required
    set, which is half the point of registering it."
  - "Swept `check-quality-harness.py`'s own stale 'three canonical
    surfaces' / 'both surfaces' prose per-occurrence rather than by
    blanket replace. Two categories left deliberately unchanged: the
    'BOTH canonical surfaces' phrase describing the two FULL-rule-set
    surfaces (output-template.md, SKILL-body.md) — accurate before and
    after this plan, since only two surfaces ever require all nine keys —
    and the two 'three surfaces restate one number' occurrences in the
    `_QUAL01_DOC_ROW_TOKENS` count-drift narrative, an unrelated concern
    (doc-row token count, not surface registration) explicitly deferred to
    plan 13-21 per hard constraint 5."
  - "Recorded MUTATION Q2's measured discrepancy against the plan's
    prediction rather than silently reporting the predicted line: removing
    only the fourth `_RENDER_RULE_SURFACES` entry fires (h) MEMBERSHIP LOCK
    and (k) CASE-COUNT FLOOR, not (j) COVERAGE FLOOR as predicted — (j)
    derives its expected set from the same tuple being mutated, so it is
    structurally blind to a shrink of that tuple itself. Verified by
    running the mutation, not assumed from reading the code."

requirements-completed: [CHAINHEAD-03, CHAINHEAD-04]

# Metrics
duration: ~55min
completed: 2026-09-03
---

# Phase 13 Plan 20: Register reason-upward.md as the fourth QUAL-01 canonical surface Summary

`shared/references/reason-upward.md` — the sole source of the shipped, slash-invocable `first-principles/skills/reason-upward/SKILL.md` — now carries R6 (unwrapped to byte-identity), R7, R8 and R9 byte-identically, and is registered in `_RENDER_RULE_SURFACES` with a scoped required-rule set, closing the gap where `/reason-upward` prescribed the chain form with no head-input admissibility rule at all and a wrap-permitting phrasing there was invisible to QUAL-01's contradiction scan.

## Performance

- **Duration:** ~55 min
- **Completed:** 2026-09-03
- **Tasks:** 3/3 completed
- **Files modified:** 3 (2 canonical `shared/` + 1 generated sibling)

## Option A/B Decision (recorded before editing, per Task 1's instruction)

**Chosen: Option A — register the surface.**

- **Argument 1 (this phase's own precedent).** Plan 11-07 (CR-01) registered `shared/spine/references/validation-rubric.md` as a third canonical surface rather than deleting the chain form from it, on the reasoning that a surface the model reads at decision time must carry the rule, not a pointer to it.
- **Argument 2 (stronger here than for the rubric).** The rubric is read alongside the full agent body at Phase 5 self-audit; `shared/references/reason-upward.md` IS the entire body of a slash-invoked skill — there is no agent body beside it to supply the missing rule. A user who runs `/reason-upward` sees only this file's text.
- **Why Option B (delete the chain form, point at the output template) is rejected, concretely:** a skill stub cannot follow a pointer into `shared/spine/`, which is not shipped inside the plugin (verified: `shared/spine/references/output-template.md` is emitted as an agent reference sibling, never copied into `first-principles/skills/`). Pointing into the plugin's own agent reference tree instead would make a focused-mode skill depend on the composer agent's tree — exactly the coupling `LAUNCHER_SKILLS`'s own comment in `scripts/sync-content.py` names as the reason the launcher pattern (a self-contained stub, no cross-tree dependency) exists in the first place.

## Task Commits

1. **Task 1: Record the decision, then give `shared/references/reason-upward.md` the four rule literals byte-identically** — `8289490` (fix)
2. **Task 2: Register the surface in `_RENDER_RULE_SURFACES`, move every floor that counts surfaces or literals, prove each new guard falsifiable** — `2a6d40f` (fix)
3. **Task 3: Close at a green battery with the literals, the detector and the headline all proven unmoved** — no file changes beyond the one-time `uv sync` prerequisite fix (`.venv/` gitignored, not committed); all gates passed once the prerequisite was resolved.

**Plan metadata:** (this commit, following SUMMARY creation)

## Files Created/Modified

- `shared/references/reason-upward.md` — R6 unwrapped onto one physical line (byte-identical to `_RENDER_RULE_LITERALS["R6"]`), R7 added verbatim, R8 inline-backticked in a carrier sentence following `validation-rubric.md`'s rendering convention, R9 added verbatim — all inserted between the existing R6 restatement and the unchanged `Each chain must include...` sentence
- `scripts/check-quality-harness.py` — fourth `_RENDER_RULE_SURFACES` entry with its rationale comment, fourth `_RENDER_SURFACE_REQUIRED_RULES` entry (`R6`-`R9`), extended registry-lock `expected_surfaces`/`expected_required_rules`, control (j)'s comment moved to "four-element set", control (k)'s `expected_missing_case_count` moved 23 → 27 with updated arithmetic comment, and a per-occurrence sweep of stale "three canonical surfaces" prose (four occurrences changed, four left unchanged with recorded reasons)
- `first-principles/skills/reason-upward/SKILL.md` — regenerated via `sync-content.py --write`; carries all four literals byte-identically

## Byte-Identity Evidence (Task 1)

Extracted directly from the live `_RENDER_RULE_LITERALS` module constant against the edited file's real text (not by eye):

| Literal | In `shared/references/reason-upward.md` | In `first-principles/skills/reason-upward/SKILL.md` |
|---|---|---|
| R6 | `True` | `True` |
| R7 | `True` | `True` |
| R8 | `True` | `True` |
| R9 | `True` | `True` |

Eight booleans, all `True`.

**Contradiction phrases (five zero counts):** none of `_RENDER_CONTRADICTION_PHRASES` — `'wraps with arrow-led continuation'`, `'wrap with arrow-led continuation'`, `'too long for one line wraps'`, `'a hop may be broken'`, `'may wrap across physical lines'` — appears in the edited file. All five checked `False` (absent).

**`python3 scripts/sync-content.py --check`** → exit 0, no drift.

**`git status --porcelain`** after Task 1's edit + regeneration listed exactly `shared/references/reason-upward.md` and `first-principles/skills/reason-upward/SKILL.md` — nothing else, confirming `first-principles/agents/first-principles.md` was unaffected (`reason-upward` is in `SKILLS` but not `TOOLS`, per `scripts/sync-content.py`).

## Plugin-Surface Gate Results (Task 1)

| Gate | Command | Result |
|---|---|---|
| VAL-05 | `python3 scripts/check-description-budget.py` | PASS — total 1985/2000 chars, `reason-upward` slug at 82 chars |
| VAL-02 | `markdownlint-cli2 "first-principles/**/*.md"` | 0 issues in 0 files (49 files linted) |
| HARN-03 | `python3 scripts/check-focused-parity.py` | PASS |
| body-budget (report-only) | `python3 scripts/check-body-budget.py` | REPORT — body is 743 lines (historical reference figure 644; **does not gate**, per TEARDOWN-01) |

## Registration (Task 2)

`_RENDER_RULE_SURFACES` grew from three to four entries: `output-template.md`, `SKILL-body.md`, `validation-rubric.md`, `shared/references/reason-upward.md`. `_RENDER_SURFACE_REQUIRED_RULES["shared/references/reason-upward.md"] = ("R6", "R7", "R8", "R9")` — the same scoped set as the rubric, for the same reason (procedure reference, not output spec). The registry-lock's inline `expected_surfaces` and `expected_required_rules` were both extended independently (typed inline, not read from the module constants).

Control (k)'s derived case-count floor: `sum(len(keys) for keys in _RENDER_SURFACE_REQUIRED_RULES.values())` = 9 (output-template.md) + 9 (SKILL-body.md) + 5 (validation-rubric.md) + 4 (reason-upward.md) = **27**. `expected_missing_case_count` moved from 23 to 27 to match; both the derived sum and the inline expectation agree at 27, confirmed by the self-test run.

Control (l1)'s case count, confirmed DERIVED and self-adjusting: `len(render_reads) * len(_RENDER_PRE_CONTRACT_WORDINGS)` = 4 surfaces × 3 wordings = **12** cases (measured directly, not read from source).

`python3 scripts/check-quality-harness.py --self-test` → exit 0, `render_contract` and `chain_detector_pin` sub-checks both PASSED.

## Prose Sweep (Task 2, item 6)

**Changed (four occurrences, all describing the surface count and now stale at "three"):**

| Location | Before | After |
|---|---|---|
| CHAINHEAD-07 pin rationale comment (~line 4429) | "R7 and R8 ... now state on three canonical surfaces" | "...now state on four canonical surfaces" |
| `_RENDER_RULE_SURFACES` preceding comment block | ended at plan 11-07's third-surface rationale | extended with a new paragraph naming plan 13-20/CR-03's fourth-surface rationale |
| `_RENDER_RULE_LITERALS` preceding comment | "present byte for byte in BOTH `_RENDER_RULE_SURFACES` entries ... on both surfaces specifically" | "present byte for byte on every `_RENDER_RULE_SURFACES` entry that requires it (per `_RENDER_SURFACE_REQUIRED_RULES`) ... across every surface that requires it" — this comment was already stale before this plan (written when only two surfaces existed, never updated when 11-07 added the third); corrected to the general, surface-agnostic form rather than restating a number that will drift again |
| `_selftest_render_contract` docstring, controls (h)-(l) intro | "pin the reconciled multi-hop head form (CONTRACT-05) across THREE canonical surfaces" | "...across FOUR canonical surfaces", with a new sentence naming plan 13-20/CR-03 alongside the existing plan 11-07/CR-01 sentence |
| control (i) POSITIVE comment | "if a REQUIRED rule is deleted from any of the three canonical surfaces today" | "...four canonical surfaces today" |
| control (j) COVERAGE FLOOR comment | "Compares a three-element set as of plan 11-07's rubric surface" | "Compares a four-element set as of plan 13-20's reason-upward surface (previously a three-element set as of plan 11-07's rubric surface)" |

(Six rows shown; several land on the same "three → four" defect and are grouped above by location for readability — every literal occurrence of "three canonical surfaces" / "THREE canonical surfaces" / "three-element set" that referred to `_RENDER_RULE_SURFACES` was changed.)

**Deliberately left unchanged, with reason:**

| Location | Text | Reason |
|---|---|---|
| `_RENDER_RULE_SURFACES` preceding comment, "on BOTH canonical surfaces below" (~line 7179) | "must each be stated, byte for byte, on BOTH canonical surfaces below" | Correctly refers to the TWO surfaces requiring the FULL rule set (`output-template.md`, `SKILL-body.md`) — a distinct, smaller group than all registered surfaces. Both before and after this plan, exactly two surfaces require all nine keys; this phrase is accurate and unaffected by adding a fourth partially-scoped surface. |
| `_selftest_render_contract` docstring, NEGATIVE-CASE COUNT FLOOR narrative (~line 9513, two occurrences at ~9513/~12001 after edits) | "the count has now drifted stale in two consecutive plans ... because three surfaces restate one number and nothing compared them" | Refers to the `_QUAL01_DOC_ROW_TOKENS` doc-row token-count drift channel (a different mechanism entirely — CLAUDE.md's `\| QUAL-01 \|` doc rows), not `_RENDER_RULE_SURFACES`. Out of scope: hard constraint 5 reserves both `\| QUAL-01 \|` doc-row corrections for plan 13-21. |
| R9 comment (~line 7280 after edits): "unregistered prose, byte-identical on three surfaces by discipline alone, until plan 13-09" | historical narrative | Describes the pre-registration state as of a specific past plan (13-09), not a live "current state" claim — correctly left as a dated historical statement, matching the treatment 13-19's SUMMARY applied to similar historical narratives. |

`grep -n "three canonical\|THREE canonical\|three-element" scripts/check-quality-harness.py` after the sweep returns zero hits referring to `_RENDER_RULE_SURFACES`; the two remaining "three surfaces" hits (doc-row narrative) are the deliberately-unchanged rows above.

## Mutations (Task 2, all on disposable `rsync -a --exclude .git --exclude .venv --exclude .planning` scratch copies; `git status --porcelain` on the tracked tree confirmed empty before the first mutation and after every cycle)

**MUTATION Q1 — four cases, strip R6, then R7, then R8, then R9 from `shared/references/reason-upward.md` one at a time:**

```
self-test FAIL: render_contract (i) POSITIVE: shared/references/reason-upward.md: rule R6 is missing — deleted from this surface
self-test FAIL: render_contract (i) POSITIVE: shared/references/reason-upward.md: rule R7 is missing — deleted from this surface
self-test FAIL: render_contract (i) POSITIVE: shared/references/reason-upward.md: rule R8 is missing — deleted from this surface
self-test FAIL: render_contract (i) POSITIVE: shared/references/reason-upward.md: rule R9 is missing — deleted from this surface
```

Each case run independently (scratch file restored between cases); exit 1 each time, naming `shared/references/reason-upward.md` and the specific key.

**MUTATION Q2 — remove the fourth entry from `_RENDER_RULE_SURFACES` only (measured, not assumed):**

```
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: surfaces: ('shared/spine/references/output-template.md', 'shared/spine/SKILL-body.md', 'shared/spine/references/validation-rubric.md') != expected ('shared/spine/references/output-template.md', 'shared/spine/SKILL-body.md', 'shared/spine/references/validation-rubric.md', 'shared/references/reason-upward.md')
self-test FAIL: render_contract (k) CASE-COUNT FLOOR: expected 27 cases (derived sum 27), ran 23
```

Exit 1, naming the `surfaces` registry-lock field (as required) — **but the second firing arm was (k) CASE-COUNT FLOOR, not (j) COVERAGE FLOOR** as the plan's acceptance criteria predicted. Verified by running the mutation, not by reading: `(j)`'s expected set is `set(_RENDER_RULE_SURFACES)` — the SAME live tuple this mutation shrinks — so `read_relpaths` (derived from reading whatever the shrunk tuple names) and `(j)`'s expected set are both computed from the post-mutation three-element tuple and trivially agree; `(j)` cannot independently detect a shrink of its own source of truth. `(k)` catches it instead because `_RENDER_SURFACE_REQUIRED_RULES` (left unmutated, still four entries) diverges from what `_RENDER_RULE_SURFACES` (mutated, three entries) now names. The property the threat model states — "de-registration fails on two independent arms" — still holds in substance (two arms fired: (h) and (k)), just not the exact two predicted. Recorded as an assumption-drift advisory below rather than silently matched to the plan's prediction.

**MUTATION Q3 — append the first of three `_RENDER_PRE_CONTRACT_WORDINGS` historical wrap-permitting wordings to `shared/references/reason-upward.md`:**

Wording used: `'**A chain too long for one line wraps with arrow-led continuation lines — never numbered steps.**'`

Post-plan tree (registered):
```
self-test FAIL: render_contract (i) POSITIVE: shared/references/reason-upward.md: contradicts the no-wrap rule with the phrase 'wraps with arrow-led continuation'
self-test FAIL: render_contract (i) POSITIVE: shared/references/reason-upward.md: contradicts the no-wrap rule with the phrase 'too long for one line wraps'
self-test FAIL: render_contract (l3) NEGATIVE-of-the-negative: appending R1's own correct literal wrongly triggered a contradiction problem for ['shared/references/reason-upward.md']
```
Exit 1, naming the relpath and "contradicts the no-wrap rule" (control (i), not (l1) as predicted — (i) reads the real shipped bytes directly and catches the on-disk mutation before (l1)'s in-memory reproduction runs; (l1) itself does not separately fail since the phrase is already present in `read.text`, so appending it again is trivially still detected — a **pass**, not a fail, for that specific control). Collateral (l3) fires as an expected consequence of the file genuinely containing a contradiction on disk (that control appends R1's own correct literal and expects no contradiction; since the file already contains one, it correctly reports the pre-existing violation).

Pre-plan counterfactual, same wording appended to the tree exported from commit `615e179` (before this plan's registration): **exit 0** — no problem reported, confirming the "invisible to QUAL-01" claim: before registration, a wrap-permitting phrasing landing in this file went completely undetected.

**MUTATION Q4 — leave `expected_missing_case_count` at 23 with the fourth surface registered:**

```
self-test FAIL: render_contract (k) CASE-COUNT FLOOR: expected 23 cases (derived sum 27), ran 27
```

Exit 1, naming `(k) CASE-COUNT FLOOR` and both counts.

## Byte-Identity Evidence (Task 3)

`_chain_block_well_formed` spans lines 4277-4399 of `scripts/check-quality-harness.py` (`def _chain_block_well_formed` at 4277; next top-level `def _chain_detector_source` at 4400) — unchanged from plan 13-19's measurement.

`git diff -U0 615e179bb85e49dabbe8ab8272d1e487ebc127ce HEAD -- scripts/check-quality-harness.py` hunk `@@` ranges (this plan's full diff, both tasks combined): all begin at line 4429 or later. None fall between 4277 and 4399. `git diff <base> HEAD -- scripts/check-quality-harness.py | grep -E "^[+-]" | grep -c "_CHAIN_DETECTOR_PINNED_DIGEST\|expected_literal_digest"` returned `0` — neither frozen name appears in any actually-added-or-removed line. `_RENDER_RULE_LITERALS` (the identifier) appears in the diff only as unchanged context lines and inside two edited comments referencing the name; the dict's own key/value pairs are byte-unchanged (confirmed by inspection of the diff body — no `R1`-`R9` value line is touched).

## Gate Verdicts (Task 3, final)

1. `python3 scripts/check-quality-harness.py --self-test` → exit 0, `render_contract` and `chain_detector_pin` sub-checks PASSED.
2. `python3 scripts/check-traceability.py --self-test` → exit 0; `HEADLINE-LOCK PASS: published headline == 175 reproducible / 91 audit-only / 0 gap / 266 total` — unmoved, confirmed by running the gate (a surface registration adds no matrix row and changes no tier, so `build_matrix_rows()`'s live-derived headline is untouched by construction).
3. `python3 scripts/sync-content.py --check` → exit 0, no drift.
4. `bash scripts/check-firewall-battery.sh` → final line `FIREWALL: GREEN (23/23)`, exit 0.
   - First run hit `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 22/23 passed)` on VAL-03 (`[PREREQ] VAL-03 — no pytest-capable interpreter found`), the same prerequisite gap plans 13-08/13-18/13-19 documented for this worktree lineage. Ran `uv sync` (documented CLAUDE.md remedy) to create `.venv`; re-ran to `FIREWALL: GREEN (23/23)`. See Deviations below.
   - Named lines: `[PASS] VAL-02 markdownlint-cli2 first-principles/**/*.md`; `[PASS] VAL-05 check-description-budget.py`; `[PASS] HARN-03 check-focused-parity.py --self-test`; `[PASS] REG-GUARD check-registration.py --self-test + live`.
5. `git status --porcelain` on the real tree: empty before the first scratch mutation, empty after every mutation cycle, and empty at Task 3's close (aside from the untracked, gitignored `.venv/` created by `uv sync`, confirmed via `git check-ignore -v .venv`).

## Assumption Drift (advisory)

- **Found during:** Task 2, MUTATION Q2.
- **Planned assumption:** the acceptance criteria stated that removing only the fourth `_RENDER_RULE_SURFACES` entry would fire both `(h) MEMBERSHIP LOCK` (naming the `surfaces` field) and `control (j)'s coverage floor`.
- **Actual (measured):** the mutation fires `(h) MEMBERSHIP LOCK` and `(k) CASE-COUNT FLOOR`; `(j)` does not fire for this specific mutation shape, because `(j)` compares `read_relpaths` against `set(_RENDER_RULE_SURFACES)` — the same live tuple being mutated — so a shrink of that tuple is invisible to `(j)` by construction (its expected set shrinks in lockstep with the actual set).
- **Why:** `(j)`'s documented job is proving "no registered surface silently dropped OUT of the RETURNED records" — i.e., that the READ step didn't drop something the (possibly-already-wrong) registry asked for. It was never designed to independently re-validate the registry's own membership against a locked expectation; that is `(h)`'s job, which did fire correctly. The threat model's stated property ("de-registration fails on two independent arms") still holds — two arms fired — just not the exact two named. No code change made in response; this is reported as measured fact per the project's verify-by-mutation discipline, not silently reconciled with the prediction.

## Decisions Made

- Recorded the Option A/B decision in writing before editing `shared/references/reason-upward.md`, per Task 1's fail-fast instruction — both named arguments (11-07/CR-01 precedent; the stub-has-no-companion-surface case being strictly stronger here) held up, so no re-authoring was needed.
- Gave the new surface the same scoped required-rule set as the rubric (R6-R9) rather than the full nine, for the same "procedure reference, not output spec" reasoning already established for the rubric.
- Applied the per-occurrence prose sweep rather than a blanket replace across "three"/"both surfaces" text, and additionally corrected one comment (`_RENDER_RULE_LITERALS`'s preceding block) that was already stale before this plan (written for two surfaces, never updated at 11-07's third-surface addition) — judged in-scope because it directly describes the mechanism this plan edits and because leaving a doubly-stale comment beside a freshly-registered fourth surface would compound the exact drift this project's through-line names.
- Reported MUTATION Q2's measured arm mismatch honestly rather than silently matching the plan's prediction, per the standing "verify by mutation, not by reading" discipline (STATE.md, carried across rounds 1-5).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — blocking prerequisite] VAL-03 blocked on a missing `.venv`**
- **Found during:** Task 3's closing verification, first `bash scripts/check-firewall-battery.sh` run.
- **Issue:** This worktree had no `.venv`, so no pytest-capable interpreter was found; VAL-03 reported `[PREREQ]` and the battery printed `FIREWALL: BLOCKED` (exit 2), not a gate failure. Identical to the prerequisite gap plans 13-08/13-18/13-19 documented for the same worktree lineage.
- **Fix:** Ran `uv sync` (documented remedy in CLAUDE.md's own VAL-03 note) to create `.venv`, then re-ran the battery to `FIREWALL: GREEN (23/23)`.
- **Files modified:** none (`.venv/` is gitignored, not committed).

---

**Total deviations:** 1 auto-fixed (1 blocking prerequisite)
**Impact on plan:** No scope creep; the prerequisite fix is a one-time worktree setup step documented as the standard remedy, not a code change. The MUTATION Q2 discrepancy above is recorded as an advisory, not a deviation — no code was changed in response to it.

## Issues Encountered

None beyond the documented VAL-03 prerequisite gap and the MUTATION Q2 measured-vs-predicted discrepancy, both recorded above.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Gap 2 (`13-VERIFICATION.md` criterion 2, CR-03) is now closed: the set of surfaces QUAL-01 registers equals the set of canonical surfaces that state the chain form, and a `/reason-upward` user is shown the head-input rule, its negative, its positional bounds and its head-only scope note — the same bytes the other three surfaces carry.
- Both `| QUAL-01 |` doc-row corrections remain plan 13-21's, once, against the final code state — this plan deliberately did not touch `CLAUDE.md` or `docs/ARCHITECTURE.md`, per hard constraint 5.
- Wave 14 (13-21) inherits a rendering-contract surface count of four (was three) and a per-surface literal-case floor of 27 (was 23), both derived rather than hand-typed, ready for its own doc-row and residue corrections plus the phase-close battery re-proof.

## Self-Check: PASSED

- `shared/references/reason-upward.md` — FOUND (verified via `test -f`).
- `scripts/check-quality-harness.py` — FOUND (verified via `test -f`).
- `first-principles/skills/reason-upward/SKILL.md` — FOUND (verified via `test -f`).
- Commit `8289490` — FOUND in `git log --oneline --all`.
- Commit `2a6d40f` — FOUND in `git log --oneline --all`.
- `bash scripts/check-firewall-battery.sh` — re-run after both commits landed: `FIREWALL: GREEN (23/23)`, exit 0.

---
*Phase: 13-chain-head-grammar*
*Completed: 2026-09-03*
