---
phase: 13-chain-head-grammar
plan: 19
subsystem: quality-harness
tags: [chain-head-grammar, rendering-contract, positional-bound, gap-closure, CR-02, fixture-half]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar (plan 18, CR-02 literal half)
    provides: R9's positional-bound disclosure sentence, byte-identical on all
      three canonical surfaces, and the re-pointed `expected_literal_clauses["R9"]`
      this plan's fixture makes falsifiable rather than merely stated
  - phase: 13-chain-head-grammar (plan 08, BL-01)
    provides: the R-HEAD-PROSE-MID precedent — the exact shape (worked block,
      extraction row, discriminating third needle on its twin, arm 4a/4b
      registration) this plan reproduces for R9
provides:
  - `R-HEAD-GTHOP-LATE`, a fifteenth rendering-contract fixture pinning the
    measured non-detected position of R9's GT-leading-hop rule, extracted and
    independently re-scored WELL-FORMED by the unmodified
    `_chain_block_well_formed` every self-test run
  - a discriminating third needle on `R-HEAD-GTHOP-BAD` so the pair
    discriminates in both directions (mirrors 13-08's fix for the PROSE pair)
  - the chain-family coverage floor's derived family grown from nine to ten ids
    with no hand-typed count, verified by direct call to
    `_render_chain_family_ids`
  - the fourteen/nine fixture-population and chain-family prose counts swept
    per-occurrence, with the historical-narrative and unrelated-count
    occurrences left untouched and enumerated
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A positional-bound disclosure sentence (13-18) is incomplete without a
      fixture pinning the non-detected side (this plan) — the sentence alone
      is a claim; the fixture is what makes a future anchoring of the
      detector's regex fail a control by name instead of silently
      invalidating a published bound. Same shape both times: 13-08 shipped
      both halves for R7 in one plan; this phase split R9's two halves across
      13-18 and 13-19 by explicit scope note."
    - "A minimal-pair fixture's needle tuple must discriminate in BOTH
      directions once a new sibling lands beside it — the needle spanning the
      exact structural transition unique to the older fixture (here, the
      head's trailing `threshold)` immediately followed by the offending
      hop) is what a mis-anchored extraction cannot satisfy."

key-files:
  created: []
  modified:
    - shared/spine/references/output-template.md
    - scripts/check-quality-harness.py
    - first-principles/agents/references/output-template.md

key-decisions:
  - "Measured the LATE block's verdict directly against the live, unmutated
    `_chain_block_well_formed` before registering it anywhere (Task 1's
    fail-fast instruction) — confirmed True with two ordinary hops preceding
    the offending hop, and False when the same hop is moved to first
    position, both matching 13-18's four-row positional measurement exactly."
  - "Chose the needle `\"threshold)\\n→ GT-4's stated duty cycle\"` for
    R-HEAD-GTHOP-BAD's third needle because it spans the exact structural
    fact that discriminates BAD from LATE: in BAD the offending hop
    immediately follows the head; in LATE it does not. Verified by extraction
    (needle present in BAD, absent from LATE), not by eye."
  - "Swept the fourteen/nine prose counts per-occurrence rather than by
    blanket replace, per the plan's explicit trap warning. Two categories of
    occurrence were deliberately left untouched: (a) two CR-03 historical-
    finding narratives (line ~6728's \"shrunk from nine entries to one\" and
    the `_QUAL01_DOC_ROW_TOKENS` eighth-token comment's \"nine chain-family
    fixtures ... narrowed to one\") describing the specific historical
    reproduction and the doc row's own (unchanged, plan 13-21's) current
    wording; (b) two unrelated counts (`_RENDER_REGISTRY_FIELDS`'s \"fifteen
    today, fourteen registries\" dataclass-field count, and leg 5's \"not all
    fourteen shared/examples/*.md files\" count) that the plan explicitly
    named as must-not-move."

requirements-completed: [CHAINHEAD-01, CHAINHEAD-02, CHAINHEAD-04, CHAINHEAD-05]

# Metrics
duration: ~40min
completed: 2026-09-03
---

# Phase 13 Plan 19: R-HEAD-GTHOP-LATE, R9's fixture-half positional-bound proof Summary

R9's positional bound — the frozen form check detects a GT-leading hop only while fewer than two ordinary hops precede it — is now pinned by a fixture, not merely stated: `R-HEAD-GTHOP-LATE` ships in `output-template.md` §4, is extracted and independently re-scored well-formed by the unmodified `_chain_block_well_formed` every self-test run, is covered by the chain-family equality floor (nine ids grown to ten, no hand-typed count), and discriminates against its shipped twin `R-HEAD-GTHOP-BAD` in both directions via a new third needle.

## Performance

- **Duration:** ~40 min
- **Completed:** 2026-09-03
- **Tasks:** 3/3 completed
- **Files modified:** 3 (2 canonical `shared/` + 1 generated sibling)

## Accomplishments

- Authored the `R-HEAD-GTHOP-LATE` worked block in `output-template.md` §4, measured its verdict directly against the live detector (`True`) before registering it anywhere, and measured the positional-discrimination control (moved to first position: `False`).
- Registered the fixture end to end: fifteenth extraction row, fixture-shape needle tuple, sorted `expected_ids` entry, positional `expected_extraction_rows` entry, `expected_fixture_shape` entry, a `_get` retrieval, a `(b)` verdict control, and entries in arm 4a (`render_chain_verdict_expected`) and arm 4b (`render_verdict_expected`).
- Gave `R-HEAD-GTHOP-BAD` a discriminating third needle (`"threshold)\n→ GT-4's stated duty cycle"`) so the pair discriminates in both directions, verified by extraction rather than by eye.
- Confirmed the chain-family coverage floor's derived family grows from nine to ten ids with zero hand-typed count changes (`_render_chain_family_ids` re-derives it from `_RENDER_CHAIN_FAMILY_PREFIXES` over the now-fifteen-member `render_locked_fixture_ids`).
- Swept every `fourteen`/`nine` prose occurrence that refers to the fixture population or the chain-family subset, leaving four occurrences deliberately unchanged with reasons recorded below.
- Closed at `FIREWALL: GREEN (23/23)`, coverage headline unmoved at `175/91/0/266`, `_chain_block_well_formed` byte-identity proven by diff-hunk-range inspection.

## Task Commits

1. **Task 1: Author the `R-HEAD-GTHOP-LATE` worked block in `output-template.md` §4 and verify its measured verdict before registering it** — `535275b` (fix)
2. **Task 2: Register `R-HEAD-GTHOP-LATE` through every floor that covers the fixture population, and give `R-HEAD-GTHOP-BAD` a discriminating third needle** — `268e083` (fix)
3. **Task 3: Close at a green battery with the frozen detector and the headline both proven unmoved** — no file changes beyond the one-time `uv sync` prerequisite fix (`.venv/` gitignored, not committed); all gates passed once the prerequisite was resolved.

**Plan metadata:** (this commit, following SUMMARY creation)

## Files Created/Modified

- `shared/spine/references/output-template.md` — the `R-HEAD-GTHOP-LATE` worked block and its explanatory paragraph, placed immediately after the `R-HEAD-GTHOP-OK` block
- `scripts/check-quality-harness.py` — fifteenth extraction row, fixture shape (with `R-HEAD-GTHOP-BAD`'s new third needle), inline registry-lock expectations, `_get` retrieval, `(b)` control, arm 4a/4b entries, prose-count sweep
- `first-principles/agents/references/output-template.md` — regenerated via `sync-content.py --write`

## Measurement Record (Task 1, pre-registration)

Driven directly against the live, unmutated `_chain_block_well_formed`:

- **LATE block** (head + two ordinary hops + the offending hop in final position):
  ```text
  C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)
  → the bracket straddles zero, so its two ends recommend opposite actions
  → the second reading is the binding one
  → GT-4's stated duty cycle is the binding term in both estimates
  ```
  Verdict: `True` — matches 13-18's "2 preceding hops" row exactly.

- **Same block, offending hop moved to first position** (positional-discrimination control, P3's in-memory form):
  ```text
  C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)
  → GT-4's stated duty cycle is the binding term in both estimates
  → the bracket straddles zero, so its two ends recommend opposite actions
  → the second reading is the binding one
  ```
  Verdict: `False`.

Anchor `**Non-conforming, and undetected by the form check — the GT-led hop in a later position:**` appears exactly once in `shared/spine/references/output-template.md` and exactly once in `first-principles/agents/references/output-template.md`. The unique second hop, `"the second reading is the binding one"`, was confirmed absent everywhere in the repo before shipping (`grep -rn` across `shared/`, `scripts/`, `first-principles/` returned zero hits) and appears exactly once in `output-template.md` after shipping.

## Needle Discrimination (Task 2, extraction-verified)

```
BAD shape:  ("→ GT-4's stated duty cycle", "2.20× at full duty", "threshold)\n→ GT-4's stated duty cycle")
LATE shape: ("the second reading is the binding one", "2.20× at full duty")

BAD needle tuple satisfied by BAD block:   True
BAD needle tuple satisfied by LATE block:  False
LATE needle tuple satisfied by LATE block: True
LATE needle tuple satisfied by BAD block:  False
```

All four booleans as required — the pair discriminates in both directions.

## Chain-Family Derivation (Task 2)

```
render_locked_fixture_ids (15 members) -> _render_chain_family_ids(..., _RENDER_CHAIN_FAMILY_PREFIXES)
family size: 10
['R-CHAIN-CONFORMING', 'R-CHAIN-NUMBERED', 'R-CHAIN-WRAPPED', 'R-HEAD-ALLCHAIN',
 'R-HEAD-CHAINREF', 'R-HEAD-GTHOP-BAD', 'R-HEAD-GTHOP-LATE', 'R-HEAD-GTHOP-OK',
 'R-HEAD-PROSE-BAD', 'R-HEAD-PROSE-MID']
```

No literal `10` was added to the source — confirmed by grepping the diff for a standalone `10` token (zero matches).

## Mutations (Task 2, all on disposable `rsync -a --exclude .git --exclude .venv --exclude .planning` scratch copies; `git status --porcelain` on the tracked tree confirmed empty before the first mutation and after every cycle)

**MUTATION P1** — delete `R-HEAD-GTHOP-LATE` from `render_chain_verdict_expected` only (leave it in `render_locked_fixture_ids`):
```
self-test FAIL: render_contract (x) COVERAGE FLOOR: arm 4a chain re-score table: actual [...9 ids, GTHOP-LATE absent...] != required [...10 ids...] — MISSING ['R-HEAD-GTHOP-LATE'], UNEXPECTED []
self-test: render_contract sub-check FAILED
```
Exit 1, naming `arm 4a chain re-score table` and the dropped id, exactly as required.

**MUTATION P3** — move the LATE block's offending hop to first position in `shared/spine/references/output-template.md`:
```
self-test FAIL: render_contract (b) R-HEAD-GTHOP-LATE (doc label 'Non-conforming, and undetected by the form check — the GT-led hop in a later position:') scored malformed, expected well-formed (measured bound)
self-test FAIL: render_contract (p) CHAIN VERDICT FLOOR: [CHAIN VERDICT FLOOR] R-HEAD-GTHOP-LATE: scored False != expected True
self-test FAIL: render_contract (p) EXPECTED-VERDICT FLOOR: [EXPECTED-VERDICT MISMATCH] R-HEAD-GTHOP-LATE: recorded verdict sequence [False] != expected sequence [True]
self-test: render_contract sub-check FAILED
```
Exit 1, arm 4a re-scores the mutated block independently and fires by name.

**MUTATION P4** — repoint `R-HEAD-GTHOP-BAD`'s extraction anchor at the LATE block's anchor (third needle present):
```
self-test FAIL: render_contract (a) extraction [mode 2: shape mismatch] R-HEAD-GTHOP-BAD: extracted text is missing required substring(s) ["threshold)\n→ GT-4's stated duty cycle"]
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: extraction_rows: row 12 (R-HEAD-GTHOP-BAD) (...) != expected (...)
self-test: render_contract sub-check FAILED
```
Exit 1, fails on the shape guard naming `R-HEAD-GTHOP-BAD` — NOT a verdict mismatch, exactly the mis-anchoring case the third needle exists to catch.

**MUTATION P4, anti-vacuity (same anchor repoint, third needle removed)**:
```
self-test FAIL: render_contract (b) R-HEAD-GTHOP-BAD (doc label 'Non-conforming — a hop beginning with a GT-N identifier:') scored well-formed, expected malformed
self-test FAIL: render_contract (p) CHAIN VERDICT FLOOR: [CHAIN VERDICT FLOOR] R-HEAD-GTHOP-BAD: scored True != expected False
self-test FAIL: render_contract (p) EXPECTED-VERDICT FLOOR: [EXPECTED-VERDICT MISMATCH] R-HEAD-GTHOP-BAD: recorded verdict sequence [True] != expected sequence [False]
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: extraction_rows: row 12 (R-HEAD-GTHOP-BAD) (...) != expected (...)
```
Exit 1, but the `[mode 2: shape mismatch]` line is **absent** — the mutation is now only caught by the verdict-mismatch arms (for the wrong reason), proving the removed needle was what caught the mis-anchoring specifically.

**MUTATION P2** (recorded as a measured NON-failure, in-memory pure-function call — no scratch copy needed): applying the GTHOP-OK rewrite (`"→ the duty cycle stated in GT-4 is the binding term in both estimates"`) to the LATE block's final hop:
```python
_chain_block_well_formed(
    "C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)\n"
    "→ the bracket straddles zero, so its two ends recommend opposite actions\n"
    "→ the second reading is the binding one\n"
    "→ the duty cycle stated in GT-4 is the binding term in both estimates"
)
# -> True
```
Leaves the block well-formed, so arm 4a does not fire. Disclosed bound, not omitted: a conforming-direction fixture cannot detect a change that keeps it conforming.

## Prose Count Sweep (Task 2, item 7)

**Changed (fixture population, `fourteen` → `fifteen`):**

| Location | Before | After |
|---|---|---|
| `_render_contract_fixtures` docstring | "Read all fourteen ... fixtures" | "Read all fifteen ... fixtures" |
| `_render_registry_lock_problems` WR-03 comment | "the table now carries fourteen rows" | "the table now carries fifteen rows" |
| shape-guard promotion comment | "five of the fourteen fixtures" | "five of the fifteen fixtures" |
| `_selftest_render_contract` docstring | "Controls (a)-(b) pin the fourteen measured verdicts" | "...pin the fifteen measured verdicts" |
| `_selftest_render_contract` docstring (control (p) intro) | "a locked fourteen-id set written inline" | "a locked fifteen-id set written inline" |
| control (p) CONSUMPTION FLOOR comment | "The locked fourteen-id set below is written INLINE" | "The locked fifteen-id set below is written INLINE" |
| control (x) three-sets comment | "arm 4b's recorded-verdict table (against all fourteen locked ids)" | "...against all fifteen locked ids" |

**Changed (chain-family subset, `nine` → `ten`):**

| Location | Before | After |
|---|---|---|
| `_selftest_render_contract` docstring (fifth arm) | "re-scores the nine chain-family fixtures" | "re-scores the ten chain-family fixtures" |
| control (p) EXPECTED-VERDICT FLOOR comment | "re-scores the nine chain-family fixtures independently" / "discharge those nine" | "...ten chain-family fixtures..." / "discharge those ten" |
| control (p) CHAIN VERDICT FLOOR — arm 4a comment | "directly on the nine chain-family fixtures' extracted text" / "discharge these nine ids" | "...ten chain-family fixtures'..." / "discharge these ten ids" |

**Deliberately left unchanged, with reason:**

| Location | Text | Reason |
|---|---|---|
| `_render_coverage_floor_problems` docstring (~line 6728) | "arm 4a's own coverage table could be shrunk from nine entries to one" | Historical narrative of the specific CR-03 reproduction (13-12), which measured a shrink from the family's then-actual size (nine) to one. Renumbering would misstate what was actually reproduced at that time. |
| `_QUAL01_DOC_ROW_TOKENS` eighth-token comment (~line 7414) | "a row can keep stating that the nine chain-family fixtures are independently re-scored while the arm deciding WHICH nine is narrowed to one" | Explains what the (unchanged, plan 13-21's) `| QUAL-01 |` doc rows currently claim — those rows still literally say "nine" until 13-21 corrects them per hard constraint 5, so this explanatory comment stays consistent with the doc rows' present wording rather than the code's new internal count. |
| `_RenderRegistrySnapshot` docstring | "`_RENDER_REGISTRY_FIELDS` (fifteen today, fourteen registries...)" | Unrelated count — dataclass field count, not fixture population. Plan explicitly named this as a must-not-move. |
| leg 5 conformance-leg docstring | "not all fourteen `shared/examples/*.md` files" | Unrelated count — the number of `shared/examples/*.md` files (exactly 14, unaffected by this plan). Plan explicitly named this as the collision trap to avoid. |

`grep -n "\bnine\b\|\bfourteen\b" scripts/check-quality-harness.py` after the sweep returns eleven lines: the four deliberately-unchanged lines above plus seven pre-existing, unrelated occurrences (`_DEFECT_RECORD_FIELDS`'s nine provenance columns, three occurrences; the nine numeric-field defect-record comments, two occurrences) — all outside the render-contract fixture population/chain-family scope entirely and untouched by this plan.

## Byte-Identity Evidence (Task 3)

`_chain_block_well_formed` spans lines 4277-4399 of `scripts/check-quality-harness.py` (`def _chain_block_well_formed` at 4277; next top-level `def _chain_detector_source` at 4400).

`git diff -U0 -- scripts/check-quality-harness.py` hunk `@@` ranges (this plan's full diff, both tasks combined): all begin at line 6517 or later. None fall between 4277 and 4399. `grep -c "_CHAIN_DETECTOR_PINNED_DIGEST\|_RENDER_RULE_LITERALS\|expected_literal_digest"` against the diff returned `0` — none of the three frozen names appear anywhere in this plan's diff.

## Gate Verdicts (Task 3, final)

1. `python3 scripts/check-quality-harness.py --self-test` → exit 0, `render_contract` and `chain_detector_pin` sub-checks PASSED.
2. `python3 scripts/check-traceability.py --self-test` → exit 0; `HEADLINE-LOCK PASS: published headline == 175 reproducible / 91 audit-only / 0 gap / 266 total` — unmoved, confirmed by running the gate.
3. `python3 scripts/sync-content.py --check` → exit 0, no drift.
4. `bash scripts/check-firewall-battery.sh` → final line `FIREWALL: GREEN (23/23)`, exit 0.
   - First run hit `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 22/23 passed)` on VAL-03 (`[PREREQ] VAL-03 — no pytest-capable interpreter found`), the same prerequisite gap plans 13-08 and 13-18 documented for this worktree lineage. Ran `uv sync` (documented CLAUDE.md remedy) to create `.venv`; re-ran to `FIREWALL: GREEN (23/23)`. See Deviations below.
5. `git status --porcelain` on the real tree: empty before the first scratch mutation, empty after every mutation cycle, and empty at Task 3's close (aside from the untracked, gitignored `.venv/` created by `uv sync`).

## Decisions Made

- Reproduced the LATE block's verdict and its positional-discrimination control directly against the live detector before registering the fixture anywhere, per Task 1's fail-fast instruction — both matched the planner's prediction (and 13-18's independently-measured four-row table) exactly, so no re-authoring was needed.
- Chose the third needle for `R-HEAD-GTHOP-BAD` by verifying, through extraction rather than by eye, that it is present in BAD and absent from LATE — the same discipline 13-08 applied to the PROSE pair.
- Applied the per-occurrence prose-count sweep rather than a blanket replace, and recorded each deliberate non-move with its reason (two historical-narrative occurrences, two unrelated-count occurrences).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — blocking prerequisite] VAL-03 blocked on a missing `.venv`**
- **Found during:** Task 3's closing verification, first `bash scripts/check-firewall-battery.sh` run.
- **Issue:** This worktree had no `.venv`, so no pytest-capable interpreter was found; VAL-03 reported `[PREREQ]` and the battery printed `FIREWALL: BLOCKED` (exit 2), not a gate failure. Identical to the prerequisite gap plans 13-08 and 13-18 documented for the same worktree lineage.
- **Fix:** Ran `uv sync` (documented remedy in CLAUDE.md's own VAL-03 note) to create `.venv`, then re-ran the battery to `FIREWALL: GREEN (23/23)`.
- **Files modified:** none (`.venv/` is gitignored, not committed).

---

**Total deviations:** 1 auto-fixed (1 blocking prerequisite)
**Impact on plan:** No scope creep; the prerequisite fix is a one-time worktree setup step documented as the standard remedy, not a code change.

## Issues Encountered

None beyond the documented VAL-03 prerequisite gap above.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Gap 1 (`13-VERIFICATION.md` criterion 1, CR-02) is now fully closed across both its literal half (13-18) and its fixture half (this plan): R9's positional bound is both disclosed in prose and pinned by a falsifiable fixture, matching R7's treatment exactly.
- Both `| QUAL-01 |` doc-row corrections remain plan 13-21's, once, against the final code state — this plan deliberately did not touch `CLAUDE.md` or `docs/ARCHITECTURE.md`, per hard constraint 5.
- Gap 2 (`shared/references/reason-upward.md` unregistered as a fourth canonical surface, CR-03) remains open for plan 13-20.
- Wave 14 (13-21) inherits a fixture-population count of fifteen and a chain-family count of ten, both derived rather than hand-typed, ready for its own doc-row and count corrections.

## Self-Check: PASSED

- `shared/spine/references/output-template.md` — FOUND (verified via `test -f`).
- `scripts/check-quality-harness.py` — FOUND (verified via `test -f`).
- `first-principles/agents/references/output-template.md` — FOUND (verified via `test -f`).
- Commit `535275b` — FOUND in `git log --oneline --all`.
- Commit `268e083` — FOUND in `git log --oneline --all`.
- `_CHAIN_DETECTOR_PINNED_DIGEST` — 6 occurrences in `scripts/check-quality-harness.py` (the pinned constant and its comparisons), confirmed absent from this plan's diff by `git diff | grep -c` returning `0`.
- `bash scripts/check-firewall-battery.sh` — re-run after both commits landed: `FIREWALL: GREEN (23/23)`, exit 0.

---
*Phase: 13-chain-head-grammar*
*Completed: 2026-09-03*
