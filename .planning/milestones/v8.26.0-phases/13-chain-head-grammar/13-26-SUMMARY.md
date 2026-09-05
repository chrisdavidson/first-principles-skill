---
phase: 13-chain-head-grammar
plan: 26
subsystem: quality-harness
tags: [chain-head-grammar, render-contract, quality-harness, worked-examples, disclosure]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar
    provides: "plan 13-25 registered R10, the disclosed over-rejection bound (a chain whose head or first hop closes its own sentence is scored malformed even though it violates none of R1-R9), with no fixture behind it"
provides:
  - "R-HEAD-PERIOD-BAD / R-HEAD-PERIOD-OK / R-HEAD-PERIOD-LATE — three worked-example blocks in output-template.md pinning R10's bound in all three measured directions (rejecting, conforming, undetected), extracted at QUAL-01 self-test time and scored by the unmodified `_chain_block_well_formed`"
  - "all three fixtures wired through the extraction table, the fixture-shape guard (with discriminating needles proven bidirectional by mutation), both registry-lock copies, the consumption/chain-verdict/expected-verdict floors, and the chain-family coverage floor (auto-derived via the `R-HEAD-` prefix)"
  - "mutation proof (S1-S5) that each fixture fails by name when its own violation is removed, moved, or swapped, including the LATE fixture's non-vacuity proof round 6 found missing for its GTHOP analogue"
affects: [13-27, 13-28]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Three-hop LATE fixture design: when a BAD/OK minimal pair differs by a single trailing character, the LATE (undetected-position) variant must NOT be built by moving that character to the pair's own last hop — doing so makes OK's text a literal string prefix of LATE's, which makes it structurally impossible for OK's shape guard to carry a needle absent from LATE. Insert a differently-worded intermediate hop instead, so all three fixtures in the triple carry a needle absent from both siblings, verified by direct extraction-table testing before wiring."

key-files:
  created: []
  modified:
    - shared/spine/references/output-template.md
    - first-principles/agents/references/output-template.md
    - scripts/check-quality-harness.py

key-decisions:
  - "Redesigned R-HEAD-PERIOD-LATE mid-task from a two-hop chain (period moved to the pair's own final hop) to a three-hop chain (an inserted, differently-worded second hop ahead of the closing one). The two-hop version scored correctly (False/True/True) but made R-HEAD-PERIOD-OK's extracted text a literal prefix of R-HEAD-PERIOD-LATE's, so no substring needle could ever discriminate OK from LATE — exactly the CR-01 vacuity class this phase exists to close. Caught before wiring, by testing needle collisions directly against the unmodified extraction pipeline rather than by inspection."
  - "R-HEAD-PERIOD-BAD and R-HEAD-PERIOD-OK are a strict minimal pair (exactly one character apart, the terminal period), per the plan's explicit requirement — verified by a character-level diff, not by eye."
  - "Left the pre-existing '(p) EXPECTED-VERDICT FLOOR ... covers all FOURTEEN locked ids' comment (line ~10480) untouched: it was already stale before this plan (the live count was fifteen, not fourteen) and is not a count this plan's own move invalidates — out of scope per the deviation rules' scope boundary, not fixed here."

patterns-established:
  - "Before wiring a new fixture triple's needles into `_RENDER_FIXTURE_SHAPE`, test every needle against every sibling fixture's extracted text (not just the fixture it belongs to) — a needle that only looks unique against the pre-existing corpus can still collide with its own new siblings."

requirements-completed: [CHAINHEAD-01, CHAINHEAD-05]

# Metrics
duration: ~65min
completed: 2026-09-03
---

# Phase 13 Plan 26: Ship the R10 fixture triple (R-HEAD-PERIOD-BAD/OK/LATE) Summary

**Added three worked-example chain blocks to `output-template.md` — a minimal-pair BAD/OK differing by exactly one character (a terminal period on the first hop) and an undetected-position LATE variant — pinning R10's disclosed over-rejection bound in all three measured directions, wired through every QUAL-01 floor, and proven by five separate mutations (S1-S5) to fail by name when the violation each fixture exists to pin is removed, relocated, or swapped.**

## Performance

- **Duration:** ~65 min
- **Completed:** 2026-09-03
- **Tasks:** 3/3 completed
- **Files modified:** 3 (2 canonical/generated `shared/`+`first-principles/` template surfaces, 1 script)

## Accomplishments

- Shipped `R-HEAD-PERIOD-BAD` (malformed — first hop closes its own sentence, though the chain violates none of R1-R9), `R-HEAD-PERIOD-OK` (well-formed — the identical chain with the period removed, one character apart from BAD), and `R-HEAD-PERIOD-LATE` (well-formed but non-conforming — the identical violation moved past the point where the check's two-arrow requirement is already satisfied), each scored directly against the unmodified `_chain_block_well_formed` before wiring (`False`, `True`, `True`).
- Wired all three through `_RENDER_CONTRACT_EXTRACTION_TABLE`, `_RENDER_FIXTURE_SHAPE` (with position-pinning needles for BAD and LATE per the CR-01 lesson), both registry-lock copies (`expected_ids`, `expected_extraction_rows`, `expected_fixture_shape`), `render_locked_fixture_ids` (15 → 18), `render_chain_verdict_expected` and `render_verdict_expected` (`False`/`True`/`True`), and a new `(b)` scoring-control block.
- The chain-family coverage floor and its ENTRY-SOURCE LOCK both re-derive from `render_locked_fixture_ids` at lock time (no separate hand-edit needed) — confirmed the `R-HEAD-` prefix picks up all three automatically, moving the chain-family count from ten to thirteen.
- Discovered and fixed a structural discrimination gap in the original two-hop LATE design before it was wired: redesigned to a three-hop chain so every fixture in the triple carries a needle absent from both of its siblings, not just from the pre-existing 15.
- Proved by mutation (on a disposable `rsync --exclude .git --exclude .venv --exclude .planning` scratch copy, `git status --porcelain` on the real tree confirmed empty before and after every single mutation) that: removing BAD's period fails on the shape guard naming BAD (S1); moving LATE's period to the first hop fails naming LATE (S2); removing LATE's period entirely fails specifically on LATE's own mode-2 shape guard, not only a verdict problem, proving the LATE fixture is not vacuous (S3); swapping BAD's and OK's bodies fails naming both ids (S4); and emptying each of the three needle tuples in turn fails the registry-lock `fixture_shape` arm by name (S5, ×3).
- `_chain_block_well_formed` and `_CHAIN_DETECTOR_PINNED_DIGEST` confirmed byte-identical to `git show HEAD:` — this plan adds no literal and touches no detector code.
- Closes GREEN: `python3 scripts/check-quality-harness.py --self-test` exit 0, `python3 scripts/sync-content.py --check` exit 0, `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (23/23)`.

## Task Commits

1. **Task 1: Ship the three R10 worked-example blocks in output-template.md** - `14bf89d` (feat)
2. **Task 2: Wire the three fixtures through the extraction table and every floor** - `c880162` (feat) — this commit also carries the Task-1 LATE redesign fix (see Deviations), since the collision was found while building Task 2's needles and fixing it required re-editing the same `output-template.md` blocks.
3. **Task 3: Prove each new fixture discriminates, by mutation** - no commit (pure verification on a disposable scratch copy; the real tree was never modified — confirmed by `git status --porcelain` before and after each of S1-S5, and by `diff` against the real tree after every restore).

**Plan metadata:** (this commit, once created)

## Files Created/Modified

- `shared/spine/references/output-template.md` - canonical §4 grammar section: three new fenced worked-example blocks (`R-HEAD-PERIOD-BAD`/`OK`/`LATE`) plus their bold labels and explanatory prose, immediately after the existing GTHOP triple
- `first-principles/agents/references/output-template.md` - generated mirror, regenerated via `sync-content.py --write`
- `scripts/check-quality-harness.py` - extraction table, fixture-shape needles, registry-lock copies, consumption/chain-verdict/expected-verdict floors, a new `(b)` scoring-control block, and two swept prose-count occurrences (chain-family docstring ordinal; nothing touching the unrelated "fourteen `shared/examples/*.md` files" count)

## Decisions Made

- Redesigned `R-HEAD-PERIOD-LATE` from a two-hop chain to a three-hop chain mid-task, after discovering the two-hop version made `R-HEAD-PERIOD-OK`'s text a literal prefix of `R-HEAD-PERIOD-LATE`'s (see key-decisions above for full rationale). Verified the fix directly against the live extraction table (`_extract_contract_example`) and `_chain_block_well_formed` before wiring, not by inspection.
- Kept BAD/OK as a strict one-character minimal pair per the plan's explicit instruction, and gave LATE its own distinct middle hop rather than trying to preserve "identical chain, period relocated" literally — the GTHOP-LATE precedent this triple follows made the same trade (added a third hop rather than staying byte-identical to its BAD/OK siblings).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] R-HEAD-PERIOD-LATE's original two-hop design made R-HEAD-PERIOD-OK's text a literal prefix of it, making bidirectional needle discrimination structurally impossible**
- **Found during:** Task 2 (designing the discriminating needle tuples the plan requires)
- **Issue:** The plan's literal wording ("the identical chain with the terminal period moved from the first hop to a later hop") was initially implemented as a two-hop chain with the period moved to the second (and only remaining) hop. This scored correctly (`False`/`True`/`True`) but meant `R-HEAD-PERIOD-OK`'s full extracted text was a strict string prefix of `R-HEAD-PERIOD-LATE`'s (LATE = OK + one trailing period). Since any substring of a prefix is necessarily a substring of the longer string, OK's shape guard could never carry a needle proven absent from LATE — a mis-anchored extraction returning LATE's body under OK's label would satisfy OK's guard undetected, the exact CR-01 vacuity class (round 6) this phase exists to close.
- **Fix:** Redesigned LATE as a three-hop chain: the same head and first hop as OK, a new differently-worded intermediate hop ("the migration case does not rest on C1 alone"), and the closing hop (with the period) as the third line. This breaks the prefix relationship — OK's needle (spanning the hop1→hop2 transition) is no longer a substring of LATE's text, since LATE's second hop is different prose. Verified directly: extracted all three fixtures via the live `_RENDER_CONTRACT_EXTRACTION_TABLE` and confirmed each fixture's own shape needle is absent from both siblings' text, and each fixture still scores `False`/`True`/`True` under the unmodified `_chain_block_well_formed`.
- **Files modified:** shared/spine/references/output-template.md, first-principles/agents/references/output-template.md (regenerated), scripts/check-quality-harness.py (bold label and needle tuple text updated to match)
- **Verification:** Programmatic cross-block containment check (each fixture's needle present in its own text, absent from both siblings') before wiring; `_chain_block_well_formed` scoring re-run after the redesign; `--self-test` exit 0 with `render_contract` and `chain_detector_pin` PASSED; mutation S4 (swap test) independently confirms bidirectional BAD/OK discrimination.
- **Committed in:** c880162 (Task 2 commit — the redesigned blocks and the wiring landed together since the collision was found while building the wiring)

---

**Total deviations:** 1 auto-fixed (1 bug — a fixture-discrimination gap found before it could ship, not after)
**Impact on plan:** The fix stays entirely within the plan's own stated intent (a minimal pair plus an undetected-position variant, each carrying a discriminating needle) — no scope creep, no change to plan objective or acceptance criteria, all of which are met by the final design.

## Issues Encountered

None beyond the deviation above, which was caught and fixed before any commit landed with the vulnerable design.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- R10's disclosed bound now has fixture evidence in all three measured directions, matching the treatment R7 and R9 already received — no published-claim/fixture gap remains for R10.
- `_chain_block_well_formed` and `_CHAIN_DETECTOR_PINNED_DIGEST` remain untouched and byte-identical to `git show HEAD:` — no milestone-amendment ceremony was triggered.
- Firewall battery closes GREEN (23/23) with no open blockers for the next plans in this wave.

## Self-Check: PASSED

- FOUND: shared/spine/references/output-template.md
- FOUND: first-principles/agents/references/output-template.md
- FOUND: scripts/check-quality-harness.py
- FOUND commit: 14bf89d
- FOUND commit: c880162

---
*Phase: 13-chain-head-grammar*
*Completed: 2026-09-03*
