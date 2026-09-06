---
phase: 21-generate-the-claim-surface
plan: 05
subsystem: tooling
tags: [gate-registry, describe, self-test, ci-gates, batch-c, contract-06, headline-lock]

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    plan: 04
    provides: "scripts/_gate_registry.py's GateEntry/ENTRIES,
      DESCRIBE_FIELD_VOCABULARY, field_resolution_problems()/
      vocabulary_problems() (D-04), registry_id_problems() (D-01), the live
      D-04 floor control (d04-live-field-equality) that derives its script
      set from ENTRIES itself; 20 of 27 script-backed gate rows already
      carrying a working --describe limb (13 batch A + 7 batch B)"
provides:
  - "7 working --describe limbs for batch C, the heaviest and most
    registry-rich scripts in the tree: check-step0-live.py (STEP0-06),
    check-provenance.py (PROV-GUARD), check-conf-gate.py (CONF-GATE),
    check-selfaudit-scan.py (SCAN-GUARD), check-traceability.py
    (TRACE-03), check-quality-harness.py (QUAL-01), report-conformance.py
    (the conformance-baseline pre-commit row) — all 27 script-backed gate
    rows now describe themselves"
  - "_battery_core.py's LOCKED_TRANSPORT_ARGV_TEMPLATE: the Plan-36-locked
    claude -p invocation's argv, lifted from an inline list literal inside
    _run_prompt_to to a module constant that function now builds its argv
    from, so STEP0-06's --describe limb documents the transport it
    actually invokes rather than a hand-retyped copy"
  - "check-selfaudit-scan.py's _VALIDATE_LEG_SYMBOLS and _META_CONTROL_IDS:
    a call-site-census roster lifted from a local tuple, and a new
    10-entry roster naming the self-test's infrastructure-level controls
    that sit outside REQUIRED_BRANCHES/_BRANCH_ROSTER_LOCK — both roster
    constants explicitly untouched per the plan's hard bound"
  - "check-traceability.py's coverage_headline field: the one deliberate
    exception to the describe() pure/no-I/O contract in this plan — it
    calls _headline_literals() live on every invocation, matching that
    function's own deliberate non-memoization, backed by a new
    coverage_headline vocabulary member in _gate_registry.py"
  - "check-quality-harness.py's contract_pins field: the three CONTRACT-06
    pinned functions' digest+line_count identity, exposed without
    touching any pinned function body — backed by a new contract_pins
    vocabulary member"
  - "2 new DESCRIBE_FIELD_VOCABULARY members (coverage_headline,
    contract_pins) plus 7 new consumes wirings in _gate_registry.py"
affects: [21-06, 21-07, 21-08, 21-11]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "argv-template lift: a Plan-36-locked inline argv list, previously
      hand-typed at its only call site, moved to a module constant the
      call site now BUILDS FROM via placeholder substitution — the same
      shape D-21-J's roster lifts use, applied to a command-line template
      rather than an id roster"
    - "meta-control roster, distinct from the structural branch roster:
      check-selfaudit-scan.py's self-test carries two independent kinds
      of named check — REQUIRED_BRANCHES (100 structural assertion
      branches, explicitly frozen this plan) and _META_CONTROL_IDS (10
      infrastructure-level checks: roster equality, call-site censuses,
      in-process dispatch controls, and this plan's new describe check) —
      kept as two separate rosters rather than merging them into one,
      because merging would have required touching the frozen roster"
    - "deliberate I/O exception, disclosed in the function docstring:
      describe()'s otherwise-pure contract is broken exactly once
      (check-traceability.py's coverage_headline), for the same reason
      _headline_literals() itself refuses to cache — memoizing here would
      let the published figure go stale the moment a matrix row moves"
    - "pin state is read, never recomputed: check-quality-harness.py's
      describe() reuses the three PRE-EXISTING single-call-site source
      wrapper functions (_chain_detector_source/_conclusion_claims_source/
      _slice_sections_source) to derive line counts, rather than adding a
      second inspect.getsource() call site against any pinned function —
      preserving each wrapper's own documented single-call-site invariant"
    - "typing.get_type_hints for a Literal roster: report-conformance.py's
      five-surface identity was never restated by hand — it derives from
      Artifact's own `surface: Literal[...]` field annotation via
      get_type_hints()/get_args(), so a sixth surface added there is
      picked up automatically"

key-files:
  created: []
  modified:
    - scripts/check-step0-live.py
    - scripts/_battery_core.py
    - scripts/check-provenance.py
    - scripts/check-conf-gate.py
    - scripts/check-selfaudit-scan.py
    - scripts/check-traceability.py
    - scripts/check-quality-harness.py
    - scripts/report-conformance.py
    - scripts/_gate_registry.py

key-decisions:
  - "check-step0-live.py had no existing control roster at all (unlike
    check-provenance.py/check-conf-gate.py's pre-existing _CONTROL_IDS
    shape) — a hand-authored-once _CONTROL_IDS tuple (23 entries) was
    added naming every existing self_test() check by a short id, matching
    batch B's check-act-limb.py precedent (D-21-J: 'if no roster exists,
    lift it'). One roster entry ('decompose-absence') had to be renamed
    to 'scrubbed-slug-absence' after it tripped the file's own
    fragment-concatenation scrubbed-slug guard by containing the literal
    substring the guard scans for."
  - "check-selfaudit-scan.py's branch_roster/branch_count read
    REQUIRED_BRANCHES directly and read-only, per the plan's explicit
    hard bound. The plan's own 'control_ids' requirement was satisfied by
    a SEPARATE, new _META_CONTROL_IDS roster (10 entries) naming the
    self-test's non-branch infrastructure controls (roster-census,
    dispatch, live-dispatch, ..., describe) — not by adding a 101st entry
    to REQUIRED_BRANCHES, which the plan forbids touching."
  - "check-traceability.py's coverage_headline field is the only field
    across all three tasks that performs live disk I/O inside describe()
    — a deliberate, disclosed exception to the D-03 pure contract,
    required by the plan text itself ('the coverage headline as derived
    from build_matrix_rows() ... never as a literal') and justified by
    _headline_literals()'s own pre-existing refusal to memoize."
  - "check-quality-harness.py's describe() and its --describe branch are
    physically located OUTSIDE all three CONTRACT-06 pinned functions
    (inserted after _slice_sections_pin_problems, well clear of any
    pinned body); verified by git diff -U0 showing ZERO deletion lines
    anywhere in the file for this task's commit — a pure-addition diff
    cannot have touched a pinned function's bytes."
  - "report-conformance.py's five-surface identity is derived via
    typing.get_type_hints(Artifact)['surface'] + get_args(), not a
    hand-retyped list — Artifact.__annotations__['surface'] alone returns
    an unresolved string under this file's typing usage, so
    get_type_hints() (which resolves it) was required, not merely
    stylistic."

requirements-completed: [CONF-11]

# Metrics
duration: ~2.5h (single session)
completed: 2026-09-06
---

# Phase 21 Plan 05: Batch C --describe Limbs (Heaviest/Most Registry-Rich Gates) Summary

**All 7 batch-C gate scripts — the highest-risk batch in Phase 21, including the file carrying
the three CONTRACT-06 sha256 pins and the file carrying `HEADLINE_SCAN_GLOBS` that plan 21-07's
generated TRACE-03 row will be built from — gained a pure, vocabulary-conformant `--describe`
JSON limb; all three CONTRACT-06 pins verified byte-unchanged by direct digest recomputation, no
gate verdict moved, battery held at 25/25 throughout.**

## Performance

- **Duration:** ~2.5h, single session, three atomic task commits
- **Tasks:** 3 (Task 1: check-step0-live.py, check-provenance.py, check-conf-gate.py; Task 2:
  check-selfaudit-scan.py, check-traceability.py; Task 3: check-quality-harness.py,
  report-conformance.py)
- **Files modified:** 9 (7 gate scripts + `scripts/_battery_core.py` + `scripts/_gate_registry.py`)

## Accomplishments

- All 7 batch-C scripts answer `--describe` with parseable JSON on stdout, exit 0. All 27
  script-backed gate rows in the entire registry (13 batch A + 7 batch B + 7 batch C) now expose
  a working `--describe` limb.
- 2 new `DESCRIBE_FIELD_VOCABULARY` members added (`coverage_headline`, `contract_pins`), each
  with a written meaning comment, both consumed by exactly the entries that emit them.
- `scripts/_gate_registry.py`'s live D-04 floor (`d04-live-field-equality`) passes both
  directions for all 7 batch-C scripts.
- `bash scripts/check-firewall-battery.sh` reports **FIREWALL: GREEN (25/25)** after every task
  in this plan.
- `git diff --stat -- tests/` is empty throughout — no `_FROZEN_PATHS` member was touched.
- All three CONTRACT-06 pins verified byte-unchanged: `git diff -U0 -- scripts/check-quality-harness.py`
  for this plan's commits shows **zero deletion lines** in the entire file — a pure-addition diff
  cannot have touched any pinned function body or digest literal.

## Task 1: STEP0-06, PROV-GUARD, CONF-GATE

| Script | Field(s) added | Before -> After self-test count | Mutation-proof arm |
|---|---|---|---|
| `check-step0-live.py` | `locked_constants.transport_command` (derived from new `_battery_core.LOCKED_TRANSPORT_ARGV_TEMPLATE`, which `_run_prompt_to` now builds its argv from), `checked_files`, `control_ids`/`control_count` (new 23-entry `_CONTROL_IDS`, hand-authored-once) | 0 (no prior roster) -> 23 controls | Removed `"describe"` from `_CONTROL_IDS` on a scratch copy: `--describe`'s `control_count` dropped 23 -> 22 |
| `check-provenance.py` | `control_ids`/`control_count` (reused pre-existing `REQUIRED_CONTROLS`), `registered_surfaces` (live fixture's own two relpaths, never the published `7/7` measurement) | 32 -> 33 controls | Removed `"describe"` from `REQUIRED_CONTROLS` on a scratch copy: `--describe`'s `control_count` dropped 33 -> 32 AND `--self-test`'s own anti-masking gate failed by name (`describe` ran but is not registered) |
| `check-conf-gate.py` | `registered_surfaces` (=`_GATED_SURFACES` verbatim, **in order**, never sorted), `population_floors` (=`_POPULATION_FLOORS`), `call_site_census` (=`_LIVE_CALL_SITES`), `control_ids`/`control_count`, `locked_constants` (marked-claim ratchet value + prescribed lead-ins, joined) | 42 -> 43 controls (measured; the plan's "90 before this plan" figure belongs to `report-conformance.py` per 20-05-SUMMARY, not this script — confirmed by running both) | (a) `_POPULATION_FLOORS["verdict_cells"]` 77->999 on a scratch copy: emitted value moved AND `--self-test` failed `population-floor-passes-at-floor` by name. (b) `_GATED_SURFACES` 2-tuple -> 3-tuple (`"bogus-fourth"` appended): emitted array grew to 3 elements in order AND `--self-test` failed `population-floor-fires`/`population-floor-passes-at-floor` by name (population floors breached for the new surface) |

`check-conf-gate.py --describe`'s `registered_surfaces` verified equal to exactly
`["shared-examples", "generated-twin"]` (the ordered 2-tuple, not alphabetized).

## Task 2: SCAN-GUARD, TRACE-03

| Script | Field(s) added | Before -> After self-test count | Mutation-proof arm |
|---|---|---|---|
| `check-selfaudit-scan.py` | `branch_roster`/`branch_count` (=`REQUIRED_BRANCHES`, read-only — **byte-unchanged**, confirmed by `git diff -U0` showing no hunk inside either `REQUIRED_BRANCHES` or `_BRANCH_ROSTER_LOCK`), `registered_surfaces` (AGENT_FILE/RUBRIC_FILE), `call_site_census` (new module-level `_VALIDATE_LEG_SYMBOLS`, lifted from a local tuple `_run_self_test` now reads instead of a parallel copy), `control_ids`/`control_count` (new 10-entry `_META_CONTROL_IDS`, the self-test's infrastructure-level controls outside the branch roster), `locked_constants` (`_BAND_BULLETS`, joined) | 100 branches unchanged (explicitly frozen) + new `(describe)` meta-control added to the self-test's non-branch check set (10 meta-controls total, `(describe)` being the 10th) | N/A — SCAN-GUARD's mutation-proof arms are `_gate_registry.py`'s D-04 floor plus the direct `REQUIRED_BRANCHES` byte-freeze verification (no separate scratch-copy mutation required by this task's acceptance criteria) |
| `check-traceability.py` | `scan_globs` (=`HEADLINE_SCAN_GLOBS` verbatim, **ordered array**, never sorted/pre-joined), `registered_surfaces` (=`COVERED_HEADLINE_SURFACES`), `branch_roster`/`branch_count` (=`_HEADLINE_LOCK_BLOCKS`, 19 blocks), `locked_constants` (`_TRACE03_DOC_ROWS`, `HISTORICAL_EXEMPT_FILES`, `_HEADLINE_LOCK_STAGES` names, `_SELFTEST_ANCHOR_PREFIXES`, each joined), `coverage_headline` (live `_headline_literals()` call — the one deliberate exception to the pure-describe contract) | New `(describe)` sentinel added to `_run_self_test`'s dispatch chain (19 blocks unchanged; `describe()`-consistency now asserted every run) | Appended `"bogus/*.md"` to `HEADLINE_SCAN_GLOBS` on a scratch copy: `--describe`'s `scan_globs` array grew to 5 elements in order AND `--self-test` failed block **(n)** by name on **both** `CLAUDE.md` and `docs/ARCHITECTURE.md` ("does not transcribe HEADLINE_SCAN_GLOBS") |

`check-traceability.py --describe`'s `scan_globs`, joined with `", ".join(f"\`{g}\`" for g in scan_globs)`,
reproduces exactly `` `docs/*.md`, `CLAUDE.md`, `CHANGELOG.md`, `README.md` `` — verified present
verbatim on the single `| TRACE-03 ` line in both `CLAUDE.md` and `docs/ARCHITECTURE.md`.
`coverage_headline` verified equal to a fresh, independent call to `_headline_literals()`:
`{"slash": "192/94/0/286", "prose": "192 reproducible / 94 audit-only / 0 gap / 286 total"}`.

## Task 3: QUAL-01, conformance-baseline row

**CONTRACT-06 pin verification (recomputed as verification, never to make a test pass):**

| Function | Pinned digest | Recomputed digest | Line count |
|---|---|---|---|
| `_chain_block_well_formed` | `sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3` | **matches** | 121 |
| `_conclusion_claims` | `sha256:8b0cc1f1d2d32215e284f0276afbdbd63e761bcef573ec3723f6e6205405d394` | **matches** | **63** (matches `15-04-SUMMARY.md`) |
| `_slice_sections` | `sha256:485ffe356a6782657709bc55ffaa1b474b1af2024398bcc00d2c799eb41c848e` | **matches** | **149** (matches `15-04-SUMMARY.md`) |

All three recomputed by calling the three pre-existing, single-call-site source wrapper functions
(`_chain_detector_source()`, `_conclusion_claims_source()`, `_slice_sections_source()`) —
`describe()` never calls `inspect.getsource()` a second time against any pinned function directly.
`git diff -U0 -- scripts/check-quality-harness.py` for this task's commit shows **zero deletion
lines** in the entire file.

| Script | Field(s) added | Before -> After self-test count |
|---|---|---|
| `check-quality-harness.py` | `control_ids`/`control_count` (27 locked fixture ids from `_RENDER_CONTRACT_EXTRACTION_TABLE`), `registered_surfaces` (=`_RENDER_RULE_SURFACES`), `disclosed_bounds_anchors` (all 30 `_QUAL01_DOC_ROW_TOKENS` entries — asserted as an array whose length equals `len(_QUAL01_DOC_ROW_TOKENS)`, never the literal 30), `derived_counts` (rule/surface/doc-row counts), `locked_constants` (R1-R12 ids, surface->required-rules map, `_QUAL01_DOC_ROWS`, all joined), `contract_pins` (new field: the three pinned functions' `{digest, line_count}`, both read/derived, never recomputed against the pin) | 27 -> 28 "sub-check PASSED" lines (this file's own printed per-run metric; its docstring's stale "exactly twenty-one" claim predates several later additions and was not touched — out of scope, matching the file's own disclosed-staleness convention) |
| `report-conformance.py` | `registered_surfaces` (5 surface pathspecs — 4 globs + `CONTRACT_SURFACE_RELPATH` — derived via `typing.get_type_hints(Artifact)['surface']` + `get_args()`, never hand-retyped), `checked_files` (`docs/conformance-baseline.md`, `docs/data/conformance.json`), `control_ids`/`control_count` (reused pre-existing `_CONTROL_IDS`) | 100 -> 101 controls |

`python3 scripts/report-conformance.py --check` reported `PASS — no drift` both before and after
this task's edit — the limb did not perturb the committed conformance baseline.

## Task Commits

1. **STEP0-06, PROV-GUARD, CONF-GATE `--describe` + `_gate_registry.py` wiring** — `82cb12e` (feat)
2. **SCAN-GUARD, TRACE-03 `--describe` + `_gate_registry.py` wiring** — `cffb209` (feat)
3. **QUAL-01, conformance-baseline row `--describe` + `_gate_registry.py` wiring** — `89f22b0` (feat)

**Plan metadata:** this commit (SUMMARY only — STATE/ROADMAP excluded per worktree mode; the
orchestrator owns those writes after the wave completes)

## Files Created/Modified

- `scripts/check-step0-live.py` — `_CONTROL_IDS` (23, new hand-authored roster), `describe()`,
  `--describe` CLI flag, `(describe)`-consistency control
- `scripts/_battery_core.py` — `LOCKED_TRANSPORT_ARGV_TEMPLATE` (new module constant;
  `_run_prompt_to` now builds its argv from it instead of a hand-typed inline list)
- `scripts/check-provenance.py` — `describe()`, `_control_describe_consistency()` (registered in
  `REQUIRED_CONTROLS`), `--describe` CLI flag
- `scripts/check-conf-gate.py` — `describe()`, `_control_describe_consistency()` (registered in
  `_CONTROLS`/`_CONTROL_IDS`), `--describe` CLI flag
- `scripts/check-selfaudit-scan.py` — `_VALIDATE_LEG_SYMBOLS` (lifted from a local tuple),
  `_META_CONTROL_IDS` (10, new), `describe()`, `--describe` CLI flag, `(describe)`-consistency
  control (outside `REQUIRED_BRANCHES`)
- `scripts/check-traceability.py` — `describe()` (including the live `coverage_headline` call),
  `_self_test_describe_consistency()`, `--describe` CLI flag (top-level, checked before subcommand
  dispatch)
- `scripts/check-quality-harness.py` — `describe()` (outside all three pinned functions),
  `_selftest_describe_consistency()`, `--describe` CLI flag
- `scripts/report-conformance.py` — `typing.get_args`/`get_type_hints` import, `describe()`,
  `_control_describe_consistency()` (registered in `_CONTROLS`/`_CONTROL_IDS`), `--describe` CLI
  flag
- `scripts/_gate_registry.py` — 2 new `DESCRIBE_FIELD_VOCABULARY` members (`coverage_headline`,
  `contract_pins`), `consumes` wired on all 7 batch-C entries plus the
  `PRECOMMIT:conformance-baseline-drift-gate` entry (8 entries total)

## Decisions Made

See `key-decisions` in frontmatter — summarized: (1) STEP0-06 needed a from-scratch roster lift
(D-21-J), the others reused pre-existing rosters; (2) SCAN-GUARD's `control_ids` requirement was
satisfied by a new, separate meta-control roster rather than touching the frozen branch roster;
(3) TRACE-03's `coverage_headline` is the plan's one sanctioned exception to describe()'s pure
contract; (4) QUAL-01's `describe()` and its CLI branch sit physically and provably outside all
three pinned functions; (5) report-conformance.py's five-surface identity is derived from the
`Artifact` dataclass's own type annotation, not restated.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] `_CONTROLS`/`describe()` function-definition ordering in check-conf-gate.py**
- **Found during:** Task 1, first `--describe` run after wiring `check-conf-gate.py`
- **Issue:** `_CONTROLS: tuple[...] = (...)` is a module-level statement evaluated immediately at
  import time. Placing `describe()`/`_control_describe_consistency()` AFTER `_CONTROLS` (as
  initially drafted, mirroring where `self_test()` sits) raised `NameError: name
  '_control_describe_consistency' is not defined` at import, since the tuple literal referenced
  the function object before it existed.
- **Fix:** Moved both function definitions to immediately before the `_CONTROLS` tuple literal.
  Internal references to `_CONTROL_IDS` (defined even later) remain safe because they are
  late-bound inside a function body, not evaluated at definition time.
- **Files modified:** `scripts/check-conf-gate.py`
- **Verification:** re-ran `--describe` and `--self-test`; both passed.
- **Committed in:** `82cb12e`

**2. [Rule 1 - Bug] check-step0-live.py's new roster entry name collided with the file's own
scrubbed-slug guard**
- **Found during:** Task 1, first `--self-test` run after adding `_CONTROL_IDS`
- **Issue:** The roster entry `"decompose-absence"` (naming the pre-existing scrubbed-slug-absence
  check) contained the literal substring the file's own fragment-concatenation guard scans for and
  scrubs (`"de" + "com" + "pose"`), tripping a false self-test failure on the unmutated tree
  (`self-test FAIL: decompose-absence drift — 'decompose' reappeared in check-step0-live.py`).
- **Fix:** Renamed the roster entry to `"scrubbed-slug-absence"`, which describes the same check
  without containing the scrubbed literal.
- **Files modified:** `scripts/check-step0-live.py`
- **Verification:** re-ran `--self-test`: clean pass, no false positive.
- **Committed in:** `82cb12e`

**Total deviations:** 2 auto-fixed (Rule 1/Rule 3 — both caught and fixed during this plan's own
required verification, before the affected files were staged).

## Next Phase Readiness

- All 27 script-backed gate rows in the entire registry (batch A + B + C) now have working
  `--describe` limbs. `_gate_registry.py`'s live D-04 floor covers all of them.
- `DESCRIBE_FIELD_VOCABULARY` grew from 16 to 18 members (`coverage_headline`, `contract_pins`),
  each with a written meaning comment and a wired consumer.
- Plan 21-06/21-07 can now build the generator against a complete `--describe` surface: no
  script-backed row remains undescribed.
- Plan 21-08's `docs/gates/QUAL-01.md` repoint has its full 30-token `disclosed_bounds_anchors`
  source ready to consume.
- No blockers. `git status --porcelain` in the real repo is clean after every commit;
  `git diff --stat -- tests/` is empty throughout; all three CONTRACT-06 pins byte-unchanged.

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-06*

## Self-Check: PASSED

- FOUND: `scripts/check-step0-live.py` (modified)
- FOUND: `scripts/_battery_core.py` (modified)
- FOUND: `scripts/check-provenance.py` (modified)
- FOUND: `scripts/check-conf-gate.py` (modified)
- FOUND: `scripts/check-selfaudit-scan.py` (modified)
- FOUND: `scripts/check-traceability.py` (modified)
- FOUND: `scripts/check-quality-harness.py` (modified)
- FOUND: `scripts/report-conformance.py` (modified)
- FOUND: `scripts/_gate_registry.py` (modified)
- FOUND: commit `82cb12e` (`git log --oneline --all`)
- FOUND: commit `cffb209` (`git log --oneline --all`)
- FOUND: commit `89f22b0` (`git log --oneline --all`)
- FOUND: `bash scripts/check-firewall-battery.sh` reports FIREWALL: GREEN (25/25)
