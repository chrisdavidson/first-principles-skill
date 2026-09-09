---
phase: 24-diagnosis-name-the-mechanism-not-the-instance
plan: 03
subsystem: docs
tags: [claim-containment, prose-02, census, adjudication, gen-gate-docs]

# Dependency graph
requires:
  - phase: 24-diagnosis-name-the-mechanism-not-the-instance/01
    provides: "scripts/census-delta-vectors.py and its four captured rung enumerations"
  - phase: 24-diagnosis-name-the-mechanism-not-the-instance/02
    provides: "docs/v9.1-claim-containment-diagnosis.md's banner, self-discipline, method, section skeleton and section 1"
provides:
  - "docs/v9.1-claim-containment-diagnosis.md Appendix A — the adjudicated per-vector census, 671 rows, grounds partitioned by equality"
  - "The G3 (stale-terminus) set: docs/gates/CONF-SURFACE.md:219 (CR-01) and tests/premise-rejection-catalog.md:687 (newly-found sibling), handed to Phase 25 as CONTAIN-02's demonstration targets"
  - "A fixed bug in the page's own section 1.2 (a false claim about the measured-transition regex's matching behavior on a compressed inline chain), found and corrected while re-deriving the mechanism this task adjudicates against"
affects: ["25 (claim-containment mechanism, CONTAIN-02's fail-before/pass-after demonstration)"]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Scratchpad Python join script assembling the appendix mechanically from the census tool's own TSV output, never by hand-transcription (docs/PROCESS.md §1.2's own worked example is the failure mode this avoids)"
    - "Shared-argument ids (A1..A25) referenced from a compact per-vector table, rather than repeating the same file-level/chain-level argument prose on all 671 rows — satisfies 'one row per vector, one ground per row' while keeping the argument text auditable and non-duplicated"
    - "Terminal-vs-non-terminal hop adjudication within one growth-history sentence: a chain's own final hop gets individual G2/G3 checking against a live source; earlier hops in the same already-adjudicated chain get G5 with a pointer to the terminus row"

key-files:
  created: []
  modified:
    - docs/v9.1-claim-containment-diagnosis.md

key-decisions:
  - "Re-ran the census at write time per the plan's own instruction rather than trusting plan 24-01's capture; found the tree had moved twice (665 -> 671 -> 671-post-fix) and disclosed both moves on the page instead of silently adjudicating a stale snapshot"
  - "Fixed a bug in section 1.2 (Rule 1 — not one of the census's own adjudicated vectors, a separate factual error in the mechanism's own description) discovered while verifying the mechanism by direct invocation before adjudicating against it"
  - "Adopted a same-sentence/disclaimed-elsewhere test to decide G1 (whole passage, dated/closed or explicitly disclaimed) vs. individual G2/G3 terminus checking: a passage gets G1 if it explicitly disclaims live/current authority (an 'already discharged' historical ledger, a 'Historical terminal record' label, a 'not a gate' K-of-5 disclaimer) or is a citation footnote physically separated from any 'current' claim; a passage's terminus gets individual G2/G3 checking if it sits in the same sentence as, or is directly cited by, an unambiguous 'currently X' assertion (CLAUDE.md's battery-total sentence, docs/ARCHITECTURE.md's cross-reference to 'the battery total above', CONF-SURFACE.md's ongoing re-pin guarantee)"
  - "Disclosed, rather than tried to eliminate, the appendix's own self-reference: once committed, Appendix A's own match column becomes new population for a later census run (observed live: 671 -> 1349 after insertion), which is disclosed on the page itself as an expected consequence, not chased to a fixed point"

patterns-established:
  - "Adjudication-economics pattern: file-level G1 argument stated once per category (8 categories covering 123 files), chain-level G1/G5 argument stated once per growth-history passage, individual G2/G3 argument stated once per corroborated/stale terminus — 671 rows collapse to 25 distinct shared arguments, each independently disputable by a reader"

requirements-completed: [PROSE-02]

# Metrics
duration_minutes: 26
completed: 2026-09-09
---

# Phase 24 Plan 03: Adjudicated per-vector census (Appendix A) Summary

**Hand-adjudicated all 671 mechanically enumerated `N -> M` delta vectors into Appendix A, one row per vector reconciled by equality across five grounds, surfacing a second, previously-unknown stale-terminus site (`tests/premise-rejection-catalog.md`) alongside CR-01's own — and fixed a factual bug in the page's own mechanism description while re-deriving it.**

## Performance

- **Duration:** ~26 min
- **Started:** 2026-09-09T12:51:17Z
- **Completed:** 2026-09-09T13:17:39Z
- **Tasks:** 2 (both auto)
- **Files modified:** 1 (`docs/v9.1-claim-containment-diagnosis.md`)

## Accomplishments

- Re-ran `scripts/census-delta-vectors.py --rung all` at write time (per the plan's own
  instruction not to trust plan 24-01's capture without re-checking): found the tree had moved
  from 665 to 671 vectors because plan 24-02 had, in the interim, created this very page and its
  own two force-tracked `24-01-SUMMARY.md`/`24-02-SUMMARY.md` companions — each newly contributing
  narrative-prose delta vectors. Both the delta and its cause are disclosed on the page.
- While re-deriving the mechanism (required reading before adjudicating against it), found and
  fixed a bug in section 1.2: the page's own claim that a compressed inline chain
  `152 → 182 → 184` "matches the pattern twice" is **false** — verified by direct invocation
  (`re.finditer` on the live pattern object returns exactly one match, `152 → 182`, because
  non-overlapping substitution cannot re-anchor a second match on the shared middle value).
  Replaced with an accurate, live-verified worked example built from `docs/gates/CONF-SURFACE.md`'s
  actual multi-sentence text (three separate hops, each independently matched, all stripped —
  confirmed by running `_strip_citation_shaped_numbers` against the real passage).
- Assigned exactly one ground (G1..G5) to every one of the 671 enumerated vectors via a scratchpad
  join script (`/tmp/.../scratchpad/build_appendix.py`) reading the census tool's own TSV output —
  never hand-transcribed. Grounds partition the population by equality:
  **G1=609, G2=8, G3=3, G4=27, G5=24, sum=671=TOTAL.**
- Every G2/G3 row's terminus was checked against a named live source with a recorded command:
  the battery total (`bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)`), the
  requirements coverage headline (`docs/data/matrix.json` → 192 reproducible / 94 audit-only / 286
  total), the quality-harness pinned fixtures (`check-quality-harness.py --self-test` → PASS), and
  the provenance-verifier control count (`check-provenance.py --self-test` → 33 controls).
- **Two G3 (stale-terminus) rows found**, both handed to Phase 25 as CONTAIN-02's demonstration
  targets, neither corrected (D-10 forbids the fix in this phase):
  1. `docs/gates/CONF-SURFACE.md:219` — CR-01 itself, re-found independently by the mechanical
     census: `_DEFERRED_LEDGER_MAX` narrated `182 → 184`; live constant is `181`.
  2. `tests/premise-rejection-catalog.md:687` — a **newly-discovered sibling**, not named in
     `22-REVIEW.md` or `23-CONTEXT.md`: PROV-GUARD's control count narrated `24 → 32`; the live
     self-test reports 33 controls. This sits on a `tests/` fixture file, a surface CONTAIN-01's
     three named `docs/`-tree surfaces do not reach — a finding about the mechanism's own reach,
     found by the census D-09/D-10 exists to run.
- Published the pre-registered widening ladder's outcome rung by rung, including the zero
  (`py-docstrings`, per D-12's binding proviso that a zero is published, not searched around):
  md-narrow 59, md-all 611, py-docstrings 0, shared-text 1.
- Disclosed the appendix's own self-reference rather than trying to eliminate it: once committed,
  Appendix A's own `match` column is itself new population for a subsequent census run — observed
  live, a post-commit re-run reads 1349 vectors, not 671. This growth is explained on the page
  itself (Appendix A's own preamble) as expected, continuing section 1.5's "class's own recursion"
  theme, rather than as an unexplained discrepancy.

## Task Commits

Each task was committed atomically:

1. **Task 1: Adjudicate every enumerated vector against the five grounds** — `664abe1` (feat)
2. **Task 2: Record the ladder outcome and hand the stale set to Phase 25** — `1be8ac4` (feat)

**Plan metadata:** captured in this SUMMARY commit (docs: complete plan)

## Files Created/Modified

- `docs/v9.1-claim-containment-diagnosis.md` — appended `## Appendix A`: regeneration
  command/date, the population-delta disclosure, the self-reference disclosure, the G1-G5 ground
  legend, the ground-count reconciliation table, 25 shared arguments, the 671-row per-vector
  table, the four-rung ladder-outcome table, and the G3-set-as-Phase-25-target statement. Also
  fixed a pre-existing factual bug in section 1.2 (written by plan 24-02) about the
  measured-transition regex's own matching behavior.

## Decisions Made

- **Re-ran the census at write time** rather than trusting plan 24-01's capture (per the plan's
  own `<action>` text): found and disclosed a real population delta (665 → 671) caused by plan
  24-02's own commits, and a second delta (671, unchanged in count but changed in content) caused
  by this task's own section-1.2 bugfix. The 671-row enumeration adjudicated is the one captured
  immediately after that fix, before Appendix A itself existed.
- **Fixed section 1.2's regex-matching bug** (Rule 1 — a factual error in the mechanism's own
  description, not one of the census's adjudicated vectors) rather than adjudicating around it,
  because letting a demonstrably false claim about the very mechanism PROSE-01 diagnoses stand
  in the page I was appending Appendix A to would have undermined the appendix's own credibility.
  Verified by direct invocation both before and after the fix.
- **G1-vs-G2/G3 test for growth-history passages:** rather than blanket-classify every "N → M"
  growth narrative the same way, each passage was checked for whether it explicitly disclaims
  live/current authority (an "already discharged" ledger, a "Historical terminal record" label, a
  "not a gate" K-of-5 disclaimer) — G1 — or whether its terminus sits in the same sentence as, or
  is directly cross-referenced by, an unambiguous "currently X" statement — individual G2/G3
  checking. This is what let CLAUDE.md's/docs/ARCHITECTURE.md's battery-growth terminus be
  corroborated as G2 while the same numbers' restatement in a "Historical terminal record"
  blockquote on `docs/README.md` was correctly read as G1 — a real, falsifiable distinction (a
  reader can check the disclaiming label or the sentence boundary), not an arbitrary split.
- **Adjudication economics:** 671 rows collapse to 25 distinct shared arguments (8 file-level
  categories covering 123 closed/frozen files, plus per-line/per-chain arguments for the 17 "live"
  files' 155 rows), each row still carrying its own ground and a reference to the argument that
  grounds it — satisfying "one row per vector, one ground per row, disputable individually"
  without retyping the same paragraph hundreds of times.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed a factually incorrect claim about the measured-transition regex's matching behavior in section 1.2**
- **Found during:** Task 1's required re-derivation of the mechanism before adjudicating against it
- **Issue:** Section 1.2 (written by plan 24-02) claimed a compressed inline chain
  `` `152 → 182 → 184` `` "matches the pattern twice, consuming `152 → 182` as one hop and
  `182 → 184` as the next." Verified false by direct invocation: `re.finditer` on the live
  `_CITATION_SHAPE_RES` arrow pattern returns exactly **one** match on that literal string
  (`152 → 182`), because non-overlapping regex substitution cannot re-anchor a second match on the
  shared middle value (`182`) once the first match has consumed it. Standalone, `184` would
  actually survive stripping and be retained as a live count claim — the opposite of what the
  sentence asserted.
- **Fix:** Replaced the illustrative example with one verified against the real live text: ran
  `_strip_citation_shaped_numbers` against `docs/gates/CONF-SURFACE.md`'s actual three-sentence
  passage (each hop written in its own sentence, not chained inline) and confirmed all three hops,
  including the terminus `184`, strip cleanly — matching what section 1.4's own direct-invocation
  demonstration already showed. New text states both the compressed-chain counterexample and the
  real multi-sentence mechanism, each backed by a `python` code block showing the actual command
  and output.
- **Files modified:** `docs/v9.1-claim-containment-diagnosis.md` (section 1.2 only)
- **Verification:** `python3 -c "..."` invocations shown in the commit; `python3
  scripts/gen-gate-docs.py --check` and `python3 scripts/check-links.py` both exit 0 after the fix.
- **Committed in:** `664abe1` (Task 1 commit)

**2. [Rule 3 - Blocking] Ran `uv sync` to obtain a pytest-capable interpreter for VAL-03**
- **Found during:** first full-battery run, which reported `FIREWALL: BLOCKED (25/26)` — the
  worktree had no `.venv` and `python3` could not `import pytest`, matching plan 24-01's own
  documented finding of the same pre-existing, environment-only condition.
- **Issue:** The plan's acceptance criteria require reading a live `FIREWALL: GREEN` verdict.
- **Fix:** `uv sync` (creates `.venv`, gitignored, installs pytest per `pyproject.toml`/`uv.lock`).
  No product code changed.
- **Files modified:** none tracked (`.venv/` is gitignored).
- **Verification:** re-ran the battery; `FIREWALL: GREEN (26/26)`.
- **Committed in:** not applicable (no tracked files changed)

**3. [Rule 3 - Blocking] Fixed one MD040 (fenced-code-language) issue introduced by this plan's own Task 2 content**
- **Found during:** a markdownlint-cli2 pass run before committing (not itself a battery gate, but
  VAL-02 is a CI gate on this file)
- **Issue:** Task 2's quoted ladder docstring used a bare ` ``` ` fence with no language tag.
- **Fix:** added `` ```text `` to that one fence.
- **Files modified:** `docs/v9.1-claim-containment-diagnosis.md`
- **Verification:** re-ran `markdownlint-cli2 docs/v9.1-claim-containment-diagnosis.md`; the
  introduced issue is gone.
- **Committed in:** `1be8ac4` (Task 2 commit)

---

**Total deviations:** 3 auto-fixed (1 Rule 1, 2 Rule 3)
**Impact on plan:** The Rule 1 fix is scoped entirely to section 1.2's own illustrative example
and does not touch any adjudicated vector or any file outside the diagnosis page; verified by
direct invocation before and after. Both Rule 3 fixes are mechanical prerequisites (an environment
dependency, a lint-tag addition) with zero effect on the census's population, grounds, or counts.
No scope creep.

## Out-of-Scope Findings (logged, not fixed)

Three pre-existing MD040 issues at lines 44, 94, 159 of
`docs/v9.1-claim-containment-diagnosis.md` (introduced by plan 24-02, not touched by this plan's
edits) are logged in
`.planning/phases/24-diagnosis-name-the-mechanism-not-the-instance/deferred-items.md` per the
scope-boundary rule, rather than fixed here.

## Issues Encountered

None beyond the three auto-fixed items above.

## Assumption Drift (advisory)

- **Planned:** the plan's `<action>` text frames Appendix A as adjudicating "the mechanically
  enumerated population from plan 24-01" (objective) and separately instructs re-running at write
  time if the tree has moved (task 1 action) — read together, a reader could expect the 665-row
  count from plan 24-01's own SUMMARY to be the number actually adjudicated.
- **Actual:** the number actually adjudicated is 671, not 665, because the tree measurably moved
  twice between plan 24-01's capture and this plan's write-time run (plan 24-02's own commits,
  then this plan's own section-1.2 bugfix). Both moves and their causes are stated explicitly on
  the page (Appendix A's own preamble) rather than left as an unexplained deviation from plan
  24-01's headline number.
- **Why it matters:** a reader comparing plan 24-01's SUMMARY ("665") against Appendix A's
  published count ("671") without reading Appendix A's own disclosure paragraph could mistake the
  difference for an error rather than the disclosed, expected consequence of re-running at write
  time exactly as the plan instructs.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Appendix A hands Phase 25 (`claim-containment mechanism`) an explicit, non-empty G3 target list
  (2 rows: `docs/gates/CONF-SURFACE.md:219` and `tests/premise-rejection-catalog.md:687`) that
  `CONTAIN-02` must demonstrate failing-before/passing-after. Neither is corrected here.
- `docs/gates/CONF-SURFACE.md:219`'s narrated `182 → 184` remains live-stale against the real
  `_DEFERRED_LEDGER_MAX = 181` — unchanged by this plan, exactly as D-10 requires.
- The G1..G5 ground assignments and the 25 shared arguments are on the page and open to dispute by
  a later reader or reviewer, per D-10's own falsifiability requirement — this plan does not close
  that door.
- No blockers for 24-04, 24-05 or 24-06, which append into the same file's remaining fixed
  sections (§2, §3, §§4-6) without touching Appendix A.

---
*Phase: 24-diagnosis-name-the-mechanism-not-the-instance*
*Completed: 2026-09-09*

## Self-Check: PASSED

- FOUND: `docs/v9.1-claim-containment-diagnosis.md`
- FOUND: commit `664abe1` (Task 1)
- FOUND: commit `1be8ac4` (Task 2)
- FOUND: `.planning/phases/24-diagnosis-name-the-mechanism-not-the-instance/24-03-SUMMARY.md`
- Post-commit deletion check (`git diff --diff-filter=D --name-only`) — no deletions on either
  commit.
- `git status --short` — clean after both commits.
