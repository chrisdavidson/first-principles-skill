---
phase: 19-false-negative-rate
plan: 01
subsystem: testing
tags: [adversarial-corpus, ledger-01, quality-harness, conformance, corpus-fixture]

# Dependency graph
requires:
  - phase: 18-exemplar-conformance
    provides: the 14 shipped worked examples under shared/examples/ that already measure 0/0/0
      on the three form counts (untraced_claims, nonconforming_verdict_cells,
      malformed_chain_blocks) — the derivation substrate for this plan's items
provides:
  - "tests/adversarial-corpus-v9.0/t01-ledger-arbitrary-chain.md — the 999.2 seed case named by CONF-07"
  - "tests/adversarial-corpus-v9.0/t07-non-sequitur-between-hops.md"
  - "tests/adversarial-corpus-v9.0/t09-arithmetic-does-not-follow.md"
  - "tests/adversarial-corpus-v9.0/t12-inline-citation-wrong-chain.md"
affects: [19-02, 19-03, 19-04, 19-05, 19-06, 19-07]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Derived-fixture authoring: copy a shipped shared/examples/*.md exemplar verbatim, then
       apply a surgical single-passage edit inside section 4 and/or 6 so the three frozen form
       counts (untraced_claims, nonconforming_verdict_cells, malformed_chain_blocks) are
       inherited from the substrate rather than re-earned."
    - "Structural closure-ledger row (_STRUCTURAL_LEDGER_ROW_RE) as the mechanism for a
       form-clean, content-false claim: quote the claim verbatim, cite a real-but-wrong chain id."

key-files:
  created:
    - tests/adversarial-corpus-v9.0/t01-ledger-arbitrary-chain.md
    - tests/adversarial-corpus-v9.0/t07-non-sequitur-between-hops.md
    - tests/adversarial-corpus-v9.0/t09-arithmetic-does-not-follow.md
    - tests/adversarial-corpus-v9.0/t12-inline-citation-wrong-chain.md
  modified: []

key-decisions:
  - "t01's Closure ledger row quotes only item 3's first sentence (matching the VERIFIED PROTOTYPE
     in the plan's <interfaces> block), not the full two-sentence claim — this is what the
     regex-anchored structural row form and the 0.7 overlap threshold both require."
  - "t07's non-sequitur required touching more than the single named hop to stay internally
     consistent: the C2 heading and the full 'Recommended approach' paragraph (not just its
     lead sentence) were reworded from pilot-language to launch-language so the document does
     not visibly contradict its own new conclusion; C1 and C3 were left byte-identical."
  - "t09's wrong arithmetic (multiply by the derating factor instead of dividing by it) was
     carried through seven locations — the C1 heading, all three hops, the C1 confidence
     paragraph, and two section-6 sentences (Recommended approach, Trade-offs acknowledged) —
     so the false 250 W figure reads as a coherent, internally consistent recommendation rather
     than a document that argues with itself. C2 was left byte-identical."

requirements-completed: [CONF-07]

# Metrics
duration: 25min
completed: 2026-09-05
---

# Phase 19 Plan 01: Adversarial Corpus — First Four Items Summary

**Four form-clean, factually-wrong adversarial-corpus fixtures derived by surgical edits from three Phase-18 exemplars, including the 999.2 seed case CONF-07 names by name.**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-09-05T12:49:00-04:00 (approx, worktree base-correction)
- **Completed:** 2026-09-05T12:59:52-04:00
- **Tasks:** 2
- **Files modified:** 4 (all new)

## Accomplishments
- `t01-ledger-arbitrary-chain.md` — the 999.2 seed case named by CONF-07: a closure-ledger row
  citing chain C2 while quoting a claim that chain C1 actually derives. Measures
  `conclusion_claims 8, untraced_claims 0, verdict_cells 5, nonconforming_verdict_cells 0,
  chain_blocks 2, malformed_chain_blocks 0, dependency_cycles 0, ungrounded_chains 0,
  selfaudit_disagreements 0` — byte-identical to the plan's VERIFIED PROTOTYPE reading.
- `t12-inline-citation-wrong-chain.md` — the same LEDGER-01 falsehood via the inline `(chain Cn)`
  form rather than a ledger row, demonstrating the flaw is form-independent. Measures
  `conclusion_claims 3, untraced_claims 0, verdict_cells 7, nonconforming_verdict_cells 0,
  chain_blocks 3, malformed_chain_blocks 0, dependency_cycles 0, ungrounded_chains 0,
  selfaudit_disagreements 0` — identical to its `product-business.md` substrate.
- `t07-non-sequitur-between-hops.md` — chain C2's second hop now inverts the force of the first
  hop (an unmeasured, high-sensitivity variable is used to argue for *immediate* adoption rather
  than for gathering data first) while remaining perfectly shaped. Measures
  `conclusion_claims 3, untraced_claims 0, verdict_cells 7, nonconforming_verdict_cells 0,
  chain_blocks 3, malformed_chain_blocks 0, dependency_cycles 0, ungrounded_chains 0,
  selfaudit_disagreements 0` — matching its `product-business.md` substrate's shape counts.
- `t09-arithmetic-does-not-follow.md` — chain C1's panel-sizing arithmetic multiplies by the
  0.80 derating factor where the energy path requires dividing by it, producing a wrong 250 W
  panel-array recommendation carried consistently through the heading and section 6. Measures
  `conclusion_claims 3, untraced_claims 0, verdict_cells 8, nonconforming_verdict_cells 0,
  chain_blocks 2, malformed_chain_blocks 0, dependency_cycles 0, ungrounded_chains 0,
  selfaudit_disagreements 0` — matching its `science-engineering.md` substrate's shape counts.

## Task Commits

Each task was committed atomically:

1. **Task 1: Author t01 (999.2 seed case) and t12 (inline-form twin)** - `3420117` (test)
2. **Task 2: Author t07 (non-sequitur between hops) and t09 (arithmetic does not follow)** - `a227ee1` (test)

**Plan metadata:** commit pending (this SUMMARY + STATE update)

_Note: no TDD tasks in this plan — pure fixture authoring, no code path exercised._

## Files Created/Modified
- `tests/adversarial-corpus-v9.0/t01-ledger-arbitrary-chain.md` - `personal-general.md` copy with
  item 3's inline `(chain C1)` citation stripped and a structural closure-ledger row inserted
  citing the wrong chain (C2)
- `tests/adversarial-corpus-v9.0/t12-inline-citation-wrong-chain.md` - `product-business.md` copy
  with the `**Key insight:**` line's citation changed from `(chain C1)` to `(chain C2)`
- `tests/adversarial-corpus-v9.0/t07-non-sequitur-between-hops.md` - `product-business.md` copy
  with C2's second hop, heading, and Recommended-approach paragraph rewritten to a shaped but
  invalid inference
- `tests/adversarial-corpus-v9.0/t09-arithmetic-does-not-follow.md` - `science-engineering.md`
  copy with C1's derivation arithmetic (heading, all three hops, confidence paragraph, and two
  section-6 sentences) rewritten with an invalid operation (multiply instead of divide by the
  derating factor)

## Decisions Made
- t01's ledger row quotes item 3's first sentence only (not the full two-sentence claim), per
  the plan's own VERIFIED PROTOTYPE — reproduced exactly (`conclusion_claims` 7→8, all zeros).
- For t07 and t09, "surgical single-passage edit" was interpreted to include every location
  needed for the document to read as internally consistent with its new false conclusion (the
  chain heading and the section-6 sentence(s) that cite it), while leaving the untouched chains
  (C1/C3 for t07, C2 for t09) byte-identical — confirmed by `diff` against the substrate for each
  untouched block.

## Deviations from Plan

### Auto-fixed Issues

None — no code, gate, or blocking issue required a fix. This plan touches only new files under
`tests/adversarial-corpus-v9.0/`.

**Total deviations:** 0
**Impact on plan:** None.

## Issues Encountered

Two acceptance-criteria checks in the plan produced results that differ from the plan's stated
expectation, both investigated and both traced to the check itself rather than to the corpus
items. Recorded here per the "definition of done" rule (report the observed result, not the
expected one):

1. **Task 2's two-arrow grep criterion does not hold, and cannot hold under the plan's own
   formatting rule.** The acceptance criterion states:
   `/usr/bin/grep -c '^[^#].*→.*→' tests/adversarial-corpus-v9.0/t07-non-sequitur-between-hops.md`
   returns at least 3. The observed result is `0` (confirmed via the literal command). Every
   chain block in every one of the 14 `shared/examples/*.md` exemplars (verified by grepping all
   14 files) renders each hop on its own physical line with exactly one leading arrow — the
   "head-plus-arrow-led form" `output-template.md` §4 describes, and the form Task 1 and Task 2's
   own action text explicitly require preserving ("keep every line after the head beginning with
   the arrow, and keep the hop on one physical line"). Two arrows on a single raw line only occurs
   in the *degenerate one-line* chain form (`GT-N + GT-M → [intermediate] → [conclusion]` on one
   line), which no shipped exemplar uses and which the plan does not ask for. This appears to be
   a plan-authoring imprecision, not a defect in the corpus item: the authoritative, mechanically
   verified property — `chain_blocks == 3`, `malformed_chain_blocks == 0` via `detect_defects`,
   confirmed above — establishes the two-arrow-per-*block* form actually did survive the rewrite,
   just not on a single physical line. Not auto-fixed (nothing to fix; the target file is correct
   and the grep expectation is what's miscalibrated) and not escalated as a Rule 4 architectural
   question — it doesn't block the task's `<done>` criterion, which is the `detect_defects`
   reading, not the grep line.
2. **`bash scripts/check-firewall-battery.sh` reports `FIREWALL: BLOCKED` (24/25), not
   `FIREWALL: GREEN (25/25)`** as the plan's `<verification>` section states. The single unmet
   item is `[PREREQ] VAL-03 — no pytest-capable interpreter found` (neither
   `.venv/bin/python3` nor `python3` in this worktree can `import pytest`). This is a documented,
   distinct-from-failure outcome (`CLAUDE.md`: "BLOCKED, exit 2, is a third outcome for an unmet
   external prerequisite ... distinct from a genuine gate failure, RED, exit 1"), caused by this
   git worktree not carrying its own `.venv` (the main repo's `.venv` at
   `/home/chrisdavidson/Projects/first-principles-skill/.venv` is not shared with worktrees).
   Not auto-fixed: installing pytest via `uv sync` is a package-manager operation, excluded from
   Rule 3 auto-fixing per the deviation rules. This plan touches zero files under `scripts/`,
   `shared/`, or `first-principles/`, so it cannot be the cause of this gap, and
   `report-conformance.py --check` (the actual pre-commit-relevant gate) passes clean both before
   and after each commit in this plan.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Nine of the phase's thirteen planned corpus items remain (plan 19-02 authors the remaining
  stratum-B1/B2 items on route (b); plan 19-03 authors the five stratum-A hand-authored items).
- `tests/adversarial-corpus-v9.0/` exists with exactly these four `.md` files; it is
  deliberately NOT yet registered in `_FROZEN_PATHS` (plan 19-07 owns that, per the phase's
  decision record (f)/(T-19-01)).
- To fully green the firewall battery in this worktree, a future session should run `uv sync`
  from the repo root (not auto-run here per the package-install exclusion) — this is an
  environment-setup item, not a phase blocker.

---
*Phase: 19-false-negative-rate*
*Completed: 2026-09-05*

## Self-Check: PASSED

- FOUND: tests/adversarial-corpus-v9.0/t01-ledger-arbitrary-chain.md
- FOUND: tests/adversarial-corpus-v9.0/t07-non-sequitur-between-hops.md
- FOUND: tests/adversarial-corpus-v9.0/t09-arithmetic-does-not-follow.md
- FOUND: tests/adversarial-corpus-v9.0/t12-inline-citation-wrong-chain.md
- FOUND: commit 3420117 (Task 1)
- FOUND: commit a227ee1 (Task 2)
- FOUND: commit fdace20 (this SUMMARY)
