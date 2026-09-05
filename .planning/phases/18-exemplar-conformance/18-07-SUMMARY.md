---
phase: 18-exemplar-conformance
plan: 07
subsystem: testing
tags: [markdown, conformance-measurement, quality-harness, standing-gate]

# Dependency graph
requires:
  - phase: 18-exemplar-conformance
    plan: 01
    provides: report-conformance.py's discover_artifacts/build_row/build_rows/
      pair_agreement/compute_headline public surface, the CAVEAT_MARKER constant, and
      the published Disclosed-bounds section this plan amends
  - phase: 18-exemplar-conformance
    plan: 06
    provides: the closed corpus (all four target counts at zero on both gated
      surfaces) and the corpus-wide marked-claim residual (2, entirely in
      decompose-irreducibility.md) this plan pins as a ratchet
provides:
  - scripts/check-conf-gate.py — CONF-GATE, a live comparator against source-literal
    targets, a 14-entry claim floor locked by equality to the discovered
    shared-examples ids, the D-03 prescribed-lead-in rule, the marked-claim ratchet, a
    D-08 live anti-vacuity arm (three in-memory mutations of personal-general.md), and
    an 18-control --self-test roster floored by equality against a second transcribed
    id lock
  - docs/conformance-baseline.md's Disclosed-bounds §2 now states the marked-claim
    residual as a ratchet ("may fall, never rise") pinned by the gate's own
    _MARKED_RATCHET literal, reconciled equal (2) to the derived reading
affects: [18-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "One-way importlib import of a script that itself performs a one-way importlib
      import: check-conf-gate.py imports report-conformance.py under the sys.modules
      key `_report_conformance` and reads every detector function off that
      already-imported module (`_rc.detect_defects`, `_rc.build_rows`,
      `_rc._synthetic_row`, `_rc._render_example_chain_blocks`,
      `_rc._chain_block_well_formed`, `_rc.CAVEAT_MARKER`) rather than re-registering
      the harness under `_quality_harness` a second time, which would re-execute the
      harness module body inside a process that already has it loaded."
    - "Equality-floor pattern (SCAN-GUARD's _BRANCH_ROSTER_LOCK / _roster_problems
      shape) applied twice in this file: once for the 14-entry _CLAIM_FLOORS roster
      against the live-discovered shared-examples ids (D-07), and once for the
      --self-test control-id roster against a second, independently transcribed lock
      (_CONTROL_IDS) — a control added to one and not the other fails self_test() by
      name."
    - "D-08 live anti-vacuity arm: mutate the exact string content the live leg has
      just measured (never write to disk), re-run the same frozen detector against the
      mutated string, and require the specific expected count to increment by exactly
      1. This is the only thing a --self-test tempdir fixture cannot prove — that the
      live leg is wired to the shipped artifacts, not to nothing."

key-files:
  created:
    - scripts/check-conf-gate.py
  modified:
    - scripts/report-conformance.py
    - docs/conformance-baseline.md

key-decisions:
  - "_CLAIM_FLOORS' 14 entries were transcribed from this phase's own summaries
    (18-02 through 18-06) and then independently re-confirmed live against
    docs/data/conformance.json before being pinned as source literals — every value
    equals the current baseline reading exactly, so zero entries carry a CUT-marker
    comment (no claim was cut anywhere in this phase)."
  - "The D-08 arm targets personal-general.md specifically (not a random or
    alphabetically-first file) because it is the tree's plainest exemplar of conforming
    chain form — two chains, no drill-preamble scaffolding — making each of the three
    mutation sites (a hop line, a Verdict cell, a citation) easy to locate and reason
    about by direct inspection, and each was confirmed unique (str.count == 1) in the
    live file before being pinned as a needle literal."
  - "The three D-08 mutations are applied as sequential string replacements against ONE
    read of the live file text (not three independent reads), and each is verified
    against the frozen detector before the next proceeds — if a later mutation's needle
    ever collides with an earlier mutation's replacement text, the count check would
    catch it rather than silently mismeasuring."
  - "Task 3 reused the existing Disclosed-bounds §2 paragraph in
    scripts/report-conformance.py's render_markdown rather than adding a new section:
    the marked-claim figure was already derived from `rows` at render time (D-06a),
    so only the prose needed amending to state the ratchet framing and name the pinning
    location (`check-conf-gate.py`'s `_MARKED_RATCHET`)."

patterns-established:
  - "A standing conformance gate built by wrapping an existing reporter's discovery/
    measurement surface (one-way import, zero re-implementation) rather than
    duplicating it — the accepted-cost trade-off (a shared bug affects both, but two
    independent implementations would diverge more often) is stated in the gate's own
    module docstring, not left implicit."

requirements-completed: [CONF-06]

# Metrics
duration: ~85min (estimated; explicit start timestamp not captured)
completed: 2026-09-05
---

# Phase 18 Plan 07: Exemplar Conformance — The Standing CONF-GATE Comparator Summary

**Built `scripts/check-conf-gate.py`: a live gate that measures the fourteen shipped worked examples through `report-conformance.py`'s discovery and measurement surface and compares the readings against source-literal targets, a 14-entry claim floor, the D-03 prescribed-lead-in rule and the marked-claim ratchet — never against the regenerated baseline — backed by a D-08 live anti-vacuity arm (three in-memory mutations of `personal-general.md`) and an 18-control offline `--self-test` battery.**

## Performance

- **Duration:** ~85 min (estimated)
- **Completed:** 2026-09-05
- **Tasks:** 3 completed
- **Files modified:** 3 (1 script created, 1 script amended, 1 generated doc amended)

## Accomplishments

- `scripts/check-conf-gate.py` created (704 lines): imports `scripts/report-conformance.py`
  exactly once under the `sys.modules` key `_report_conformance`, and reads every detector
  function off that already-imported module — `sys.modules["_quality_harness"]` appears
  zero times in this file (`/usr/bin/grep -c` confirms).
- `_GATED_SURFACES = ("shared-examples", "generated-twin")`, a named constant with a
  written reason for excluding `contract-surface` (the specification document whose §4
  worked examples deliberately include non-conforming teaching contrasts).
- `_TARGETS`: four zero-valued source literals (`unreadable`, `heading_malformed_blocks`,
  `nonconforming_verdict_cells`, `silent_untraced_claims`), compared against readings
  re-derived live from `build_rows(REPO_ROOT)` on every run — never read back from
  `docs/data/conformance.json`.
- `_CLAIM_FLOORS`: 14 entries, one per shipped shared-examples analysis, each confirmed
  live against `docs/data/conformance.json` before being pinned. Locked by EQUALITY (never
  subset) against the live-discovered shared-examples ids (D-07), reporting `missing` and
  `extra` by name on drift.
- The D-03 rule: a marked claim (carrying `no chain — flagged assumption only`) that opens
  with one of the three prescribed lead-ins (`**Recommended approach:**`, `**Key
  insight:**`, `**Trade-offs acknowledged:**`) fails the gate by name.
- The marked-claim ratchet (`_MARKED_RATCHET = 2`): the shared-examples sum of
  `marked_untraced_claims` may fall, never rise.
- The D-08 live anti-vacuity arm: three in-memory mutations of `shared/examples/personal-general.md`'s live text — (a) a hop re-wrapped across two physical lines
  (arrow removed, continuation indented) increments `heading_malformed_blocks` by exactly
  1; (b) a Verdict cell's em dash and justification stripped increments
  `nonconforming_verdict_cells` by exactly 1; (c) a `(chain C1)` citation removed
  increments `silent_untraced_claims` by exactly 1. All three confirmed live (see Task 2
  below) and never written to disk.
- An 18-control offline `--self-test` battery (exceeds the ≥12 floor), floored by equality
  against a second, independently transcribed `_CONTROL_IDS` lock, covering: each of the
  four `_TARGETS` firing/passing (7 controls including a generated-twin-specific fire), the
  D-07 roster floor's missing/extra/equal cases (3 controls), the D-04 claim floor's
  fire/pass cases (2 controls), the D-03 rule's fire/pass cases (2 controls), the ratchet's
  fire/pass-at-pin/pass-below cases (3 controls), and the contract-surface exclusion's
  reachability (1 control).
- Task 3 amended `scripts/report-conformance.py`'s existing Disclosed-bounds §2 paragraph
  to state the marked-claim residual as a ratchet ("may fall, never rise") pinned by
  `check-conf-gate.py`'s `_MARKED_RATCHET`, and mechanically reconciled the gate's literal
  (2) against the baseline's derived reading (2) — equal, confirmed by the verify command.
- `python3 scripts/check-conf-gate.py` exits 0 live, printing a `COVERAGE —` line naming 28
  measured artifacts and three D-08 mutation lines. `python3 scripts/check-conf-gate.py
  --self-test` exits 0, printing `SELF-TEST PASS — 18 controls run`.
- `git status --porcelain` is empty immediately after a live run (mechanically asserted,
  not assumed) — the D-08 arm never writes to `shared/` or `first-principles/`.
- `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (24/24)` — the tally is
  unchanged, confirming the gate is not yet registered (that is plan 18-08's job).
- `git diff --stat` against this plan's starting commit for `scripts/check-quality-harness.py`
  produces no output — the frozen harness (all three CONTRACT-06 sha256 pins) is untouched.

## Task Commits

Each task was committed atomically:

1. **Task 1: Build the CONF-GATE comparator and its live leg** - `1be3341` (feat)
2. **Task 2: Add the D-08 live anti-vacuity arm and the --self-test control roster** - `10c9f1e` (feat)
3. **Task 3: Publish the marked-claim ratchet in the baseline and reconcile gate against report** - `0a81275` (docs)

**Plan metadata:** committed together with this SUMMARY.md (worktree mode; STATE.md/ROADMAP.md
updates deferred to the orchestrator).

## Files Created/Modified

- `scripts/check-conf-gate.py` (created, 704 lines) — the standing CONF-GATE comparator:
  imports, `_GATED_SURFACES`, `_TARGETS`, `_CLAIM_FLOORS`, `_MARKED_RATCHET`,
  `_PRESCRIBED_LEAD_INS`, the five pure comparator functions, the D-08 live arm, `run_live()`,
  the 18-control `--self-test` battery, and `main()`.
- `scripts/report-conformance.py` — Disclosed-bounds §2 paragraph amended to state the
  marked-claim residual as a ratchet, naming `check-conf-gate.py`'s `_MARKED_RATCHET` as the
  pin location.
- `docs/conformance-baseline.md` — regenerated after the Task 3 amendment
  (`docs/data/conformance.json` unchanged — the amendment is markdown prose only, no
  measured figure moved).

## Decisions Made

- **D-08 target selection.** `personal-general.md` was chosen over a random or
  alphabetically-first file because it is the corpus's plainest exemplar of conforming
  chain form (two chains, no drill-preamble scaffolding) — every mutation site (a specific
  hop line, a specific Verdict cell, a specific citation) could be located and reasoned
  about by direct inspection rather than by trial. Each of the three needle literals was
  confirmed unique (`str.count == 1`) in the live file before being pinned as a module
  constant.
- **Mutation verification methodology.** Before writing the D-08 arm's assertions, each of
  the three mutations was tested standalone against the real, unmodified
  `report-conformance.py` and `check-quality-harness.py` modules (via an ad-hoc script
  mirroring the production import idiom) to confirm the exact expected count delta (+1, not
  +0 or +2) before being encoded as a hard assertion in the gate itself — this is the same
  "verify by mutation, not by reading" discipline earlier plans in this phase established.
- **`_CLAIM_FLOORS` zero cuts.** All 14 entries equal their 2026-09-04 baseline reading
  exactly (independently reconfirmed live against `docs/data/conformance.json` before being
  pinned), so the file carries zero `# CUT:`-style inline comments — `/usr/bin/grep -c '# CUT:'`
  returns 0, matching the plan's acceptance criterion that this count equal the number of
  floors below baseline (also 0).
- **Task-boundary split.** Task 1's commit intentionally omits the D-08 arm and
  `--self-test` battery (deferred to Task 2's commit) so each task's own `<verify>` command
  exercises only the functionality that task actually added — Task 1's live leg prints
  `COVERAGE —` and `PASS` with no mutation lines; Task 2's commit is what first makes those
  lines appear.

## Deviations from Plan

None — plan executed exactly as written. All three tasks' acceptance criteria and `<verify>`
commands pass against the finished file.

## Assumption Drift (advisory)

None material. The plan's `<interfaces>` section anticipated `_rc._render_example_chain_blocks`
and `_rc._chain_block_well_formed` would be needed for the D-08(a) mutation's re-measurement;
this was confirmed correct on first attempt (both symbols are bound at `report-conformance.py`'s
own module scope and therefore accessible as `_rc.<name>`).

## Issues Encountered

- `bash scripts/check-firewall-battery.sh` initially reported `BLOCKED` (not `RED`) because this
  worktree had no pytest-capable interpreter for VAL-03's third leg. Resolved by running `uv
  sync`, which creates a local, gitignored `.venv`. Same finding every prior plan in this phase
  recorded; no repo change.
- This worktree's `.git` HEAD was on the pre-18-06-merge commit at spawn time (behind the
  expected base `017bb5dd`, which already includes plan 18-06's merged work); corrected via `git
  reset --hard` to the expected base per the worktree branch-check protocol before any plan work
  began. Phase 18 planning artifacts (`18-07-PLAN.md`, `18-CONTEXT.md`, `18-RESEARCH.md`,
  `18-PATTERNS.md`, prior plans' `SUMMARY.md` files, `PROJECT.md`, `STATE.md`, `config.json`)
  were copied in from the main repo checkout before reading, since `git worktree add` only
  checks out tracked files and `.planning/` is gitignored except for `NN-MM-SUMMARY.md` files.

## Neutralization Observation (D-08 arm's disclosed scope, required by Task 2's acceptance)

Performed on a disposable `rsync -a --exclude .git` copy under the scratch directory (never
the real repo, per the acceptance criterion's explicit instruction): the D-08 arm's own call
site (`mutation_lines = _run_d08_arm(rows)` inside `run_live()`) was deleted and replaced with
`mutation_lines = []`. Result:

- `python3 scripts/check-conf-gate.py --self-test` in the mutated copy **still exited 0**,
  printing `SELF-TEST PASS — 18 controls run` — unchanged, because none of the 18 self-test
  controls exercises `run_live()` or the D-08 arm at all.
- `python3 scripts/check-conf-gate.py` (the live leg) in the mutated copy exited 0 but **lost
  all three D-08 mutation lines** from its output, printing only the `COVERAGE —` line and
  `PASS`.

This is the arm's disclosed scope, exactly as `<depth_rule>` requires stating rather than
silently assuming: D-08 proves the live leg IS wired to the shipped artifacts when its call
site is present — it does NOT prove its own call site cannot be removed, and it carries no
control of its own (per `<depth_rule>`, "a guard guards the product; a guard is not itself
guarded"). A reviewer inspecting the live leg's output (or its absence) is what catches this
specific removal in practice; no code change was made in the real worktree to produce this
observation, and the scratch copy was deleted afterward.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Plan 18-08 owns: registering `check-conf-gate.py` in `scripts/check-firewall-battery.sh` and
  `.github/workflows/validation.yml`, the doc sweep (CLAUDE.md's CI gate table, etc.), and the
  mutation rounds. This plan deliberately left the battery tally at 24/24 unchanged, confirmed
  by the final `FIREWALL: GREEN (24/24)` reading above.
- `scripts/check-quality-harness.py` remains untouched and all three sha256 CONTRACT-06 pins
  are intact (confirmed via `git diff --stat` against this plan's starting commit `017bb5dd`).
- No blockers.

## Self-Check: PASSED

- FOUND: `scripts/check-conf-gate.py`
- FOUND: `scripts/report-conformance.py`
- FOUND: `docs/conformance-baseline.md`
- FOUND commit: `1be3341` (Task 1)
- FOUND commit: `10c9f1e` (Task 2)
- FOUND commit: `0a81275` (Task 3)

---
*Phase: 18-exemplar-conformance*
*Completed: 2026-09-05*
