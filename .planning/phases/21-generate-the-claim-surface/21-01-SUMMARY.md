---
phase: 21-generate-the-claim-surface
plan: 01
subsystem: infra
tags: [documentation-generation, gate-registry, conf-13, measurement-harness]

# Dependency graph
requires: []
provides:
  - "21-CONF13-BASELINE.md: reproducible sweep + classification of CONF-13's hand-maintained
    branch-count literals, with the aggregate driveable target (79 scanner-target -> 0) and a
    per-surface breakdown"
  - "The phase's DECISIONS OF RECORD (D-21-A through D-21-K), written once in this plan's own
    <decisions_of_record> block and referenced by every other plan in Phase 21"
affects: [21-04, 21-07, 21-08, 21-09, 21-10, 21-12]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Direction-based ordinal-vs-count disambiguation: a labeling noun (Criterion, Phase, Item,
      Plan, Step, ...) immediately BEFORE a number identifies which instance, not how many;
      number-before-noun is the count-claim direction. Generalizes cleanly and closed the
      dominant false-positive source without hand-listing individual phrases."
    - "Sweep-then-classify split: a deterministic hit-detector (never mutates the tree) feeds a
      separate classifier that assigns exactly one of four dispositions per hit, with per-surface
      arithmetic asserted (not just aggregate) so two offsetting per-surface errors can't hide."

key-files:
  created:
    - .planning/phases/21-generate-the-claim-surface/21-CONF13-BASELINE.md
  modified: []

key-decisions:
  - "CONF-13's real driveable target is 79 (scanner-target -> 0), not 9 (roadmap's
    admitted-partial figure), not 1,015, and not 76 (the two unfiltered readings this document
    supersedes) — derived from a raw sweep of 250 hits: 150 structural (eliminated for free once
    plans 21-04/21-07/21-08/21-10's generated-doc split lands), 79 scanner-target (must be
    hand-driven to 0 then held there by plan 21-09's standing scanner), 15 exempt (legitimate
    non-branch-count numbers the scanner must keep permitting), 6 false-positive."
  - "The sweep pattern itself was tightened twice (not just the classifier) after the first run
    exceeded the 25% per-surface false-positive ceiling on several small .py-docstring surfaces:
    an exit-code line/prose exclusion and a direction-based ordinal/label exclusion, both
    structural properties of the text rather than per-hit exceptions."
  - "Headline-provenance deltas (the coverage headline's historical row-count narrative,
    229 -> 214 -> 237 -> 252 -> 266 -> 286) are classified exempt, extending CONF-13's own named
    coverage-headline exemption (owned by HEADLINE-LOCK) to the intermediate deltas that document
    how that same figure arrived at its current value."

patterns-established:
  - "Reproducibility proven end-to-end, not just claimed: the two Python scripts are embedded
    verbatim in the baseline document; extracting them back out and re-running against the
    working tree reproduces both the raw counts and the full classification byte-for-byte."

requirements-completed: [CONF-13]

# Metrics
duration: 45min
completed: 2026-09-06
---

# Phase 21 Plan 01: CONF-13 Baseline Summary

**Measured CONF-13's real branch-count-literal figure via a two-pass-tightened sweep (250 raw
hits) and a four-way classifier, publishing an aggregate target of 79 `scanner-target → 0` hits
(150 structural, 15 exempt, 6 false-positive) — replacing the roadmap's admitted-wrong `9` and
`21-RESEARCH.md`'s two unfiltered readings (`1,015` / `76`).**

## Performance

- **Duration:** ~45 min
- **Started:** 2026-09-06T (session start)
- **Completed:** 2026-09-06T17:24:34Z
- **Tasks:** 2/2 completed
- **Files modified:** 1 (`21-CONF13-BASELINE.md`, created)

## Accomplishments

- Built a deterministic, read-only Python sweep detecting count-bearing literals (digit form,
  spelled-out form, range/delta form) adjacent to a curated 23-entry count-noun vocabulary across
  all 27 D-21-E candidate surfaces (7 Markdown files + `docs/gates/*.md` glob + 20 script module
  docstrings via `ast.get_docstring()`).
- Tightened the sweep pattern twice after the first run measured false-positive rates above the
  25% per-surface ceiling — an exit-code-line/prose exclusion and a direction-based ordinal/label
  exclusion (`Criterion 4`, `Phase 3`, `Step 0` identify which instance, not how many) — bringing
  every surface under the ceiling without a third pass.
- Classified all 250 raw hits into exactly one of four dispositions (structural / scanner-target
  / exempt / false-positive) with per-surface arithmetic verified to sum to each row's raw count,
  not just the aggregate.
- Published the exemption taxonomy (`version-stamp-count`, `headline-provenance-delta`,
  `plan-number-identifier`, `retired-body-budget`) each with a written reason and hit count.
- Published the driveable target: **79 aggregate `scanner-target → 0`**, with a per-surface
  breakdown table, and **15 exempt hits** the standing scanner (plan `21-09`) must continue to
  permit.
- Proved reproducibility end-to-end: extracted the two embedded scripts back out of the finished
  document into a fresh directory and re-ran them against the working tree — raw counts and full
  classification matched the published tables byte-for-byte.

## Task Commits

Each task was committed atomically:

1. **Task 1: Design and run the CONF-13 sweep; record raw per-surface counts** - `b9fc9a4` (feat)
2. **Task 2: Classify every hit; publish the exemption taxonomy and the driveable target** - `6c95bed` (feat)

## Files Created/Modified

- `.planning/phases/21-generate-the-claim-surface/21-CONF13-BASELINE.md` — the measured baseline:
  sweep method (vocabulary, adjacency window, two tightening passes, verbatim re-runnable
  scripts), raw counts (250 hits / 27 surfaces), classification (per-surface 4-way breakdown),
  exemption taxonomy, target (79 scanner-target aggregate + per-surface table), disclosed bounds,
  and the full 250-line classified hit list.

## Decisions Made

See `21-01-PLAN.md`'s `<decisions_of_record>` block (D-21-A through D-21-K) — the phase's binding
decisions, written once and referenced by every other plan in Phase 21. This plan did not add new
architectural decisions beyond what that block already records; its own decisions are the sweep
methodology and classification choices listed in this summary's frontmatter `key-decisions`.

## Deviations from Plan

None (Rule 1-3) — the plan anticipated the false-positive-ceiling tightening loop explicitly
("If this class exceeds ~25% of raw hits on any surface, tighten the pattern and re-run Task 1's
sweep rather than absorbing the noise into the taxonomy") and this execution followed that
instruction as written, not as an unplanned deviation.

One executor discretion call, documented rather than treated as a deviation: the plan's
`files_modified` frontmatter lists `21-CONF13-BASELINE.md` alongside `21-01-SUMMARY.md`, and
`.planning/` is blanket-gitignored in this repo except for force-tracked `SUMMARY.md` files (see
project memory `planning-summaries-force-tracked.md`). Since plans `21-09`/`21-10`/`21-12`
explicitly depend on this baseline document surviving past this session, and the worktree is
force-removed after merge, `21-CONF13-BASELINE.md` was force-added (`git add -f`) the same way
`SUMMARY.md` files already are — extending an established project pattern to a new
must-persist artifact rather than introducing a new one.

## Issues Encountered

The sweep's first (untightened) run measured false-positive rates above 25% on several small
`.py`-docstring surfaces (driven by `Exit codes:` docstring blocks and `Criterion N`/`Phase
N`-style ordinal references being misdetected as counts). Resolved per the plan's own instruction
by tightening the sweep pattern itself (not the classifier) with two structural, direction-based
exclusions, verified by re-running the sweep's `--selftest` falsifiability checks (both still
pass) and confirming every surface's false-positive share is now ≤10.7%.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

**Ready for plan `21-09`** (the standing scanner deliverable) to build from this baseline's
method and target: reuse `HEADLINE-LOCK`'s shape (glob-scoped read loop, per-surface non-vacuity,
coverage floor derived from the read loop's own `read_relpaths`) per D-21-D, host inside
`scripts/gen-gate-docs.py` per D-21-D, and derive `PY_DOCSTRING_SURFACES` programmatically from
`check-firewall-battery.sh`'s live `gate` registrations rather than hand-listing the 20 scripts a
second time (flagged as a disclosed bound in this baseline's own "Disclosed bounds" section).

**Ready for plans `21-04`/`21-07`/`21-08`/`21-10`** to drive the 79 scanner-target hits to 0 by
hand, with the per-surface table telling each plan exactly how many hits its surface carries and
`21-CONF13-BASELINE.md`'s full classified hit list telling them exactly which lines.

**No blockers.** `git status --porcelain` after both commits shows no change outside
`.planning/phases/21-generate-the-claim-surface/21-CONF13-BASELINE.md` — no shipped artifact
(`scripts/`, `docs/`, `CLAUDE.md`) was touched by this plan, consistent with its
measurement-only, read-only scope.

## Self-Check: PASSED

- FOUND: `.planning/phases/21-generate-the-claim-surface/21-01-SUMMARY.md`
- FOUND: `.planning/phases/21-generate-the-claim-surface/21-CONF13-BASELINE.md`
- FOUND: commit `b9fc9a4` (Task 1)
- FOUND: commit `6c95bed` (Task 2)

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-06*
