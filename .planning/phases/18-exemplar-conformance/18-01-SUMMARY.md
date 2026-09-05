---
phase: 18-exemplar-conformance
plan: 01
subsystem: testing
tags: [markdown, conformance-measurement, quality-harness, chain-headings]

# Dependency graph
requires:
  - phase: 17-conformance-baseline
    provides: report-conformance.py's discovery/measurement instrument, the committed
      docs/conformance-baseline.md and docs/data/conformance.json baseline, and the
      pre-commit conformance-drift gate
provides:
  - marked_untraced_claims / silent_untraced_claims derived columns on all 29 rows of both
    generated conformance artifacts, with the "unreadable" vocabulary preserved
  - a published "## Disclosed bounds" section stating the four written disclosures this
    phase owes (chain-form reach, marked-claim residual, output-template.md exclusion,
    closure-ledger zero-exemplar consequence)
  - Cn-numbered `### Conclusion` headings in all ten section-readable shared/examples
    files, so `_chain_ids` resolves and `(chain Cn)` citations can trace
  - the phase's true post-renumber starting figures for plans 18-04..18-06 (58
    silent-untraced, 0 marked, over shared-examples)
affects: [18-02, 18-03, 18-04, 18-05, 18-06, 18-07, 18-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Derived report columns computed from the same detect_defects record, never a second
      markdown parse (D-06a): marked_untraced_claims scans the existing
      _untraced_claims_text audit field for CAVEAT_MARKER."
    - "Self-test control that parses the rendered markdown string back into cells and
      asserts on the parsed value, with a negative arm proving a coercing renderer is
      caught -- the fix for Phase 17's CR-01 vacuous-control shape."

key-files:
  created: []
  modified:
    - scripts/report-conformance.py
    - docs/conformance-baseline.md
    - docs/data/conformance.json
    - shared/examples/ishikawa-fishbone.md
    - shared/examples/personal-general.md
    - shared/examples/personal-general-2.md
    - shared/examples/product-business.md
    - shared/examples/product-business-2.md
    - shared/examples/science-engineering.md
    - shared/examples/science-engineering-2.md
    - shared/examples/self-application.md
    - shared/examples/software-systems.md
    - shared/examples/software-systems-2.md
    - first-principles/agents/references/examples/*.md (ten generated twins)

key-decisions:
  - "CAVEAT_MARKER defined once as a module constant (`no chain — flagged assumption only`,
    U+2014 EM DASH, no trailing punctuation) and referenced from build_row's marker scan."
  - "REPORT_FIELDS widened from 3 to 5 entries; AGREEMENT_FIELDS (derived, never restated)
    widened automatically from 15 to 17 -- confirmed live via the widened
    agreement-field-scope self-test control rather than assumed."
  - "Renumbering used the mechanical `### Conclusion:` -> `### Conclusion Cn:` substitution
    only; no chains were authored or altered, matching CONTEXT D-02's form-vs-authorship
    line."

patterns-established:
  - "Three-way column vocabulary (number / \"n/a\" / \"unreadable\") extended to two new
    columns without exception -- the four unreadable files read the literal \"unreadable\",
    never 0, for marked_untraced_claims and silent_untraced_claims."
  - "Disclosed bounds are published in the generated baseline in the same voice R7/R9/R10
    use on the agent surface, with the marked-claim count computed from `rows` at render
    time rather than hardcoded, and proved so by in-memory mutation."

requirements-completed: [CONF-05, CONF-06]

# Metrics
duration: ~25min (estimated; explicit start timestamp not captured)
completed: 2026-09-05
---

# Phase 18 Plan 01: Exemplar Conformance Measurement Foundation Summary

**Extended `report-conformance.py` with marked/silent untraced-claim columns and a published Disclosed-bounds section, then C-numbered all 27 chain headings across the ten section-readable worked examples so `_chain_ids` resolves for the first time.**

## Performance

- **Duration:** ~25 min (estimated)
- **Completed:** 2026-09-05T04:28:49Z
- **Tasks:** 3 completed
- **Files modified:** 25 (1 script, 2 generated conformance artifacts, 10 shared examples, 10 generated twins, 2 doc regenerations counted above)

## Accomplishments

- `marked_untraced_claims` and `silent_untraced_claims` now appear on all 29 rows of both
  `docs/conformance-baseline.md` and `docs/data/conformance.json`, computed from the same
  `detect_defects` record `untraced_claims` already uses -- never a second parse -- and
  reading the literal `"unreadable"` (never `0`) on the eight rows `_slice_sections`
  rejects.
- A `## Disclosed bounds` section now publishes, in writing, the four disclosures this
  phase owes: the chain-form detector-reach bound, the marked-claim residual (derived from
  `rows` at render time, proved by in-memory mutation to actually be derived), the
  `output-template.md` scope exclusion and its reason, and the closure-ledger route's
  zero-shipped-exemplar consequence.
- All 27 `### Conclusion:` headings across the ten section-readable `shared/examples/`
  files now carry a `Cn` identifier in document order, resolving `_chain_ids` for every one
  of them (previously `[]` corpus-wide) -- the load-bearing prerequisite every citation-
  adding plan in this phase depends on.
- The heading-swept census (criterion 2's target) is confirmed unperturbed at 28 blocks /
  19 malformed before and after the renumber. `untraced_claims` moved 56 -> 58 exactly as
  RESEARCH.md Q4 predicted (+1 `ishikawa-fishbone`, +1 `product-business`), because
  `_claim_is_traced`'s GT-co-occurrence fallback now operates over per-conclusion blocks
  instead of one whole-section block.
- `scripts/check-quality-harness.py` is byte-identical to its state at plan start
  (confirmed via `git diff --stat` against the plan's starting commit).
- `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (24/24)` after creating
  a local `.venv` via `uv sync` to supply VAL-03's pytest prerequisite (gitignored,
  untracked, no repo change).

## Task Commits

Each task was committed atomically:

1. **Task 1: Add the marked-claim and silent-untraced derived columns (D-06a)** - `9584f18` (feat)
2. **Task 2: Publish this phase's four written disclosures in the generated baseline** - `767a4ad` (docs)
3. **Task 3: C-number every chain heading in the ten section-readable examples** - `cf77128` (fix)

**Plan metadata:** committed together with this SUMMARY.md (worktree mode; STATE.md/ROADMAP.md updates deferred to the orchestrator).

## Files Created/Modified

- `scripts/report-conformance.py` - `CAVEAT_MARKER` constant, widened `REPORT_FIELDS`/`AGREEMENT_FIELDS`, `build_row` marked/silent computation, `compute_headline`'s `untraced_breakdown`, the `## Disclosed bounds` renderer section, three new self-test controls (17 total, up from 14), `_synthetic_row` defaults for the two new fields
- `docs/conformance-baseline.md` / `docs/data/conformance.json` - regenerated twice (Task 1 columns, Task 3 renumber effects); `MEASUREMENT_DATE` bumped to 2026-09-05
- `shared/examples/{ishikawa-fishbone,personal-general,personal-general-2,product-business,product-business-2,science-engineering,science-engineering-2,self-application,software-systems,software-systems-2}.md` - `### Conclusion:` -> `### Conclusion Cn:`, text after the colon preserved verbatim, nothing else changed
- `first-principles/agents/references/examples/*.md` (same ten files) - regenerated via `python3 scripts/sync-content.py --write`

## Decisions Made

- `CAVEAT_MARKER` literal confirmed against `shared/spine/references/output-template.md:397,458` byte-for-byte, including the U+2014 em dash and the absence of trailing punctuation inside the marker itself.
- The new headline row in `render_markdown` shows `total untraced (N marked, M silent)` per surface, reusing the existing `conclusion_claims[s]['untraced']` total rather than restating it.
- Disclosure 2's marked-claim figure is scoped to `shared-examples` + `generated-twin` only (excluding `contract-surface`/`output-template.md`), consistent with CONF-03..06 naming the fourteen shipped analyses and Disclosure 3's stated exclusion of the contract surface from scope.
- `.venv` created via `uv sync` to unblock VAL-03 in the firewall battery; this is a local, gitignored environment fix, not a repo change, and was necessary to observe the plan's required `FIREWALL: GREEN (24/24)` verification line rather than accepting the `BLOCKED` state.

## Deviations from Plan

None — plan executed exactly as written. The two "expect two readings to move" and "post-renumber per-file figures" instructions in Task 3's `<action>` were followed and the actual measured deltas matched the plan's own prediction exactly (+1/+1, sum 56 -> 58).

## Issues Encountered

- The firewall battery initially reported `BLOCKED` (not `RED`) because no pytest-capable interpreter existed in this fresh worktree — VAL-03's third leg needs pytest. Resolved by running `uv sync`, which created a local, gitignored `.venv`. This is an environment prerequisite, not a plan defect, and required no code change.
- This worktree's `.git` HEAD was several commits behind the expected base commit at spawn time (`d4da381` vs. expected `4eff042`); corrected via `git reset --hard` to the expected base per the worktree branch-check protocol before any plan work began.
- Phase 18 planning artifacts (`18-CONTEXT.md`, `18-RESEARCH.md`, `18-PATTERNS.md`, `PROJECT.md`, `STATE.md`, `config.json`) are gitignored `.planning/` content that had not been copied into this worktree by the spawn process; they were copied in from the main repo checkout before reading, since `git worktree add` only checks out tracked files.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plans 18-04 through 18-06 (the citation-adding pass) should read their starting point as
  **58** silently-untraced claims (not the pre-renumber 56), broken down per file above —
  this is the corrected figure this plan's Task 3 explicitly produces for them.
- `_chain_ids` now resolves in all ten section-readable files, so `(chain C1)`-style inline
  citations (per RESEARCH.md Q4's drafting rule: the hyphenated `C`+digit token, not a
  spelled-out ordinal) will trace once added.
- The four unreadable drill files (`composed-inversion-second-order.md`,
  `decompose-irreducibility.md`, `estimate-fermi.md`, `theoretical-limit-carnot.md`) remain
  untouched by this plan — CONTEXT's `<decisions>` leaves their treatment (ishikawa-fishbone
  drill-preamble pattern vs. a thinner scaffold) to a later plan's discretion, as recorded.
- No blockers. `scripts/check-quality-harness.py` remains untouched and all three sha256
  CONTRACT-06 pins are intact.

## Self-Check: PASSED

- FOUND: `scripts/report-conformance.py`
- FOUND: `docs/conformance-baseline.md`
- FOUND: `docs/data/conformance.json`
- FOUND: `.planning/phases/18-exemplar-conformance/18-01-SUMMARY.md`
- FOUND commit: `9584f18` (Task 1)
- FOUND commit: `767a4ad` (Task 2)
- FOUND commit: `cf77128` (Task 3)
- FOUND commit: `94e2682` (this summary)

---
*Phase: 18-exemplar-conformance*
*Completed: 2026-09-05*
