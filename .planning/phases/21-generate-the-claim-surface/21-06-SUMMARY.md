---
phase: 21-generate-the-claim-surface
plan: 06
subsystem: tooling
tags: [gate-registry, generator, describe-harvest, region-replacement, ci-gates, drift-gate]

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    plan: 05
    provides: "All 27 script-backed gate rows (batch A + B + C) now expose a
      working --describe JSON limb; scripts/_gate_registry.py's ENTRIES,
      DESCRIBE_FIELD_VOCABULARY, field_resolution_problems()/
      vocabulary_problems() (D-04), registry_id_problems()/
      battery_gate_ids() (D-01), _registry_entry_ids()/
      _registry_precommit_ids()/_requested_fields_by_script()/
      _ANTICIPATORY_KEYS — all consumed directly by this plan's generator"
provides:
  - "scripts/gen-gate-docs.py (NEW, 859 lines): the generator's compute
    layer — harvest() subprocess-invokes every non-anticipatory
    script-backed registry entry's --describe leg, never aborting on a
    crashing or malformed-JSON script; frozen_pathspecs()/
    frozen_path_write_problems() derive check-firewall-battery.sh's own
    _FROZEN_PATHS array by regex (copied grammar from
    check-quality-harness.py's read_frozen_pathspecs, never imported) and
    floor the generator's own write set against it (19-D-08);
    all_floor_problems() runs D-01 + D-04 + vocabulary + frozen-path in one
    pass so no floor masks another"
  - "_replace_region(text, start_marker, end_marker, new_content) -> str:
    the region-replacement primitive plan 21-07/21-08 will drive CLAUDE.md's
    and docs/ARCHITECTURE.md's generated regions and docs/gates/<ID>.md's
    fenced blocks through — whole-line-anchored marker matching, a
    reimplemented (not imported) CommonMark fenced-code-block scanner
    (_fenced_line_flags) so a marker string inside a documented fenced
    example is never mistaken for a real marker, and RegionMarkerError
    named failures for all five malformed-marker shapes"
  - "generate_all() -> dict[Path, str]: the compute+render entry point,
    STUBBED in this plan (returns {}) — plan 21-07 implements the render
    half. cmd_write()/cmd_check() are implemented fully against the stub,
    including cmd_check()'s pass-1/pass-2 non-determinism check (exit 2,
    distinct from drift's exit 1) and the harvested-script vacuity floor
    (T-21-06-05)"
  - "main(argv) -> int: --write/--check/--self-test/--describe CLI dispatch
    via a mutually-exclusive group (sync-content.py's exact shape);
    gen-gate-docs.py answers its OWN --describe (D-21-C: 'a generator that
    cannot describe itself would be the first exception to D-08's
    uniformity')"
affects: [21-07, 21-08, 21-09, 21-11]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "copied-grammar-not-code-dependency: frozen_pathspecs()'s
      _FROZEN_PATHS_ARRAY_RE/_FROZEN_PATHS_ENTRY_RE are a byte-for-byte
      copy of check-quality-harness.py's read_frozen_pathspecs regexes —
      same boundary _gate_registry.py's own _BATTERY_GATE_RE documents for
      its D-01 extraction: reading another script's parsing grammar and
      re-typing it is not importing that script's checking logic"
    - "reimplemented-not-imported fence scanner: _fenced_line_flags()
      reproduces check-quality-harness.py's _fenced_code_flags CommonMark
      closing-rule discipline (same delimiter character, at least the
      opening length, no info string on the closer) from scratch in the
      new file, so this module never imports or edits the file carrying
      the three CONTRACT-06 sha256 pins"
    - "all-floors-in-one-pass: all_floor_problems() concatenates D-01 +
      D-04 + vocabulary + frozen-path-disjointness unconditionally, proven
      by a floors-run-together control that both a D-01 and a D-04 problem
      surface in the same run rather than one masking the other"
    - "monkeypatch-and-restore for CLI-level self-test controls: the
      nondeterminism-exit-2 control rebinds _this_module.generate_all to a
      flaky closure inside a try/finally, mirroring sync-content.py's own
      control (l) idiom for GENERATED_TARGET_COUNT"

key-files:
  created:
    - scripts/gen-gate-docs.py
  modified: []

key-decisions:
  - "Task 1's commit (05e7193) ended up carrying Task 2's _replace_region
    primitive and its self-test controls as well, because the file was
    authored as one cohesive unit rather than incrementally. This is a
    commit-granularity deviation from strict per-task atomicity, not a
    scope or correctness issue — recorded under Deviations below. Task 2's
    commit (a00d104) captures the one real code change discovered while
    performing Task 2's own required verification: a fixture-hardening fix
    to region-marker-in-fence-ignored."
  - "The T-21-06-05 harvested-script vacuity floor is computed over
    _expected_harvest_scripts(), which excludes the CONF-SURFACE
    anticipatory entry's own script (scripts/gen-gate-docs.py itself) —
    mirroring _registry_entry_ids()'s exclusion so cmd_check() reports
    '21/21', matching the plan's literal acceptance-criteria wording,
    rather than '22/22' (which would include this file harvesting
    itself, a coupling D-21-C reserves for plan 21-11)."
  - "harvest() and cmd_check() both call _gate_registry's ENTRIES with the
    anticipatory (CONF-SURFACE) member filtered out before harvesting, so
    this plan's own new file is never subprocess-invoked by its own
    --check run — self-invocation is deliberately deferred to when
    CONF-SURFACE is wired into the battery (plan 21-11)."
  - "_replace_region's inserted span always uses this repo's LF convention
    for the marker-separator newlines; only the END marker's own original
    line terminator (or its absence, at end-of-file) is preserved verbatim,
    so a CRLF- or no-final-newline file keeps that property exactly at the
    file's tail while the freshly-generated span inside stays LF-normalized
    (CLAUDE.md's newline='\\n' mandate)."

requirements-completed: [CONF-12]

# Metrics
duration: ~20min (single session)
completed: 2026-09-06
---

# Phase 21 Plan 06: Generator Core (describe-harvest, floors, region-replacement) Summary

**`scripts/gen-gate-docs.py` (859 lines, new): a working `--write`/`--check`/`--self-test`/`--describe` CLI that harvests all 21 non-anticipatory script-backed gate entries' `--describe` JSON, applies four floors (D-01 battery-id equality, D-04 bidirectional field resolution, closed vocabulary, and a new frozen-path disjointness floor) in one pass, and ships `_replace_region` — a CommonMark-fence-aware, whole-line-anchored region-rewrite primitive with no existing in-tree analog — proved against the live `CLAUDE.md` in memory with a render layer still stubbed for plan 21-07.**

## Performance

- **Duration:** ~20 min, single session
- **Tasks:** 2 (Task 1: CLI skeleton + describe-harvest + live D-04 floor; Task 2: `_replace_region` + boundary controls)
- **Files modified:** 1 (`scripts/gen-gate-docs.py`, new)

## Accomplishments

- `scripts/gen-gate-docs.py` harvests all 21 non-anticipatory script-backed `_gate_registry.ENTRIES` via subprocess `--describe`, reporting `harvested 21/21 script-backed entries` on both `--check` and the self-test's live `check-dispatch-wired` control — matching the number of script-backed entries in `ENTRIES` exactly, per the plan's own acceptance criterion.
- Four floors (D-01, D-04, vocabulary, frozen-path disjointness) are applied together in every `--check` run via `all_floor_problems()`, proven never to mask one another by the `floors-run-together` control (one D-01 problem + one D-04 problem in a single fixture → exactly two problems reported).
- `_replace_region` implements the plan's five malformed-marker failure shapes (zero start, zero end, duplicate start, duplicate end, end-before-start) as named `RegionMarkerError`s, whole-line-anchored matching outside CommonMark-fenced code blocks (reimplemented fence scanner, not imported, so the three CONTRACT-06 pins in `check-quality-harness.py` are never touched), and preserves every byte outside the replaced span — proved against the **live `CLAUDE.md`**'s own `### CI gates` subsection in memory, with no write to disk.
- Both required anti-vacuity neutralizations were performed on scratch copies and each failed **exactly** the arm the plan names, with no other arm affected:
  - Whole-line anchoring → substring search: `region-marker-in-fence-ignored` FAILED with `RegionMarkerError: start marker 'START': found 2 occurrence(s) outside fenced code blocks (expected exactly 1)`.
  - CommonMark closing rules → naive parity toggle: `region-tilde-fence-quoting-backticks` FAILED with `RegionMarkerError: start marker 'START': found 2 occurrence(s) outside fenced code blocks (expected exactly 1)`.
- A scratch-copy mutation deleting `check-links.py`'s `--describe` dispatch branch was named correctly by `gen-gate-docs.py --check` (`harvest: ... emitted malformed JSON`, both D-04 directions, and the T-21-06-05 vacuity floor: `missing: ['scripts/check-links.py']`), exit 1 — never a crash, never a silent pass. Real tree `git status --porcelain` was empty before and after every scratch-copy operation in this plan.
- `bash scripts/check-firewall-battery.sh` reports **FIREWALL: GREEN (25/25)** after both commits. `CONF-SURFACE` is intentionally not yet registered (plan 21-11); `scripts/check-quality-harness.py` was never touched by this plan (`git diff --stat` over its full range is empty), so all three CONTRACT-06 pins are provably byte-unchanged by construction.

## Task 1: CLI skeleton, describe-harvest, live D-04 floor

| Verification | Result |
|---|---|
| `python3 scripts/gen-gate-docs.py --self-test` | exits 0, `SELF-TEST PASS — 20 controls run` |
| `python3 scripts/gen-gate-docs.py --check` | exits 0, `harvested 21/21 script-backed entries` |
| `python3 scripts/gen-gate-docs.py --describe \| python3 -m json.tool` | exits 0 |
| `python3 scripts/_gate_registry.py --self-test` | exits 0, `SELF-TEST PASS — 16 controls run` (unchanged — no edits needed) |
| Scratch-copy mutation: delete `check-links.py`'s `--describe` branch | `--check` names `scripts/check-links.py` in the harvest problem, both D-04 directions, and the vacuity floor; exit 1 |
| `bash scripts/check-firewall-battery.sh` | `FIREWALL: GREEN (25/25)` |

Named isolation arms implemented and passing: `harvest-nonzero-exit-named`, `harvest-malformed-json-named`, `harvest-one-bad-does-not-abort`, `floors-run-together`, `frozen-path-write-fires`, `frozen-paths-derived-not-typed`, `check-dispatch-wired` (drives `main(["--check"])` in-process against the live tree), `nondeterminism-exit-2`.

## Task 2: `_replace_region` and its boundary controls

Named isolation arms implemented and passing: `region-happy-path`, `region-zero-start-raises`, `region-zero-end-raises`, `region-duplicate-start-raises`, `region-duplicate-end-raises`, `region-end-before-start-raises`, `region-marker-in-fence-ignored`, `region-tilde-fence-quoting-backticks`, `region-preserves-final-newline`, `region-preserves-crlf`, `region-real-file-claude-md` (the live-file control), plus `describe-emits-parseable-json`.

**Neutralization observations (both required by acceptance criteria, both performed on `/tmp` scratch copies via `rsync -a --exclude='.git'`, never touching the real tree):**

1. Whole-line anchoring reverted to `marker in bare` (substring search): the `region-marker-in-fence-ignored` fixture was strengthened during this task specifically because the original fixture (a bare "START" line inside vs. outside a fence) did not actually exercise whole-line anchoring — only fence exclusion — so the neutralization would have passed undetected. The fixed fixture adds a non-fenced line that *contains* "START" as a substring without *equaling* it ("See the START region below for an example."). Under the neutralization: `SELF-TEST FAIL [region-marker-in-fence-ignored] — RegionMarkerError: start marker 'START': found 2 occurrence(s) outside fenced code blocks (expected exactly 1)`. No other control failed.
2. CommonMark closing rules reverted to a naive open/close parity toggle in `_fenced_line_flags`: `SELF-TEST FAIL [region-tilde-fence-quoting-backticks] — RegionMarkerError: start marker 'START': found 2 occurrence(s) outside fenced code blocks (expected exactly 1)`. No other control failed.

## Task Commits

1. **Task 1: CLI skeleton, describe-harvest, and the live D-04 floor** — `05e7193` (feat) — this commit also carries Task 2's `_replace_region` primitive and its original self-test controls; see Deviations below.
2. **Task 2: fixture-hardening fix found during required neutralization verification** — `a00d104` (test)

**Plan metadata:** this commit (SUMMARY only — STATE/ROADMAP excluded per worktree mode; the orchestrator owns those writes after the wave completes)

## Files Created/Modified

- `scripts/gen-gate-docs.py` (NEW, 859 lines) — `harvest()`, `frozen_pathspecs()`/`frozen_path_write_problems()`, `all_floor_problems()`, `generate_all()` (stub), `_replace_region()`/`RegionMarkerError`, `cmd_write()`/`cmd_check()`, `describe()`, `self_test()`, `main()`

## Decisions Made

See `key-decisions` in frontmatter — summarized: (1) the harvest vacuity floor and `cmd_check()`'s reported count both exclude the `CONF-SURFACE` anticipatory entry's own script so the live count reads `21/21`, matching the plan's literal wording, with self-description of `gen-gate-docs.py` deferred to plan 21-11's wiring; (2) `_replace_region`'s freshly-emitted span always uses LF, with only the end marker's own original terminator (or absence of one) preserved, matching CLAUDE.md's `newline='\n'` mandate while still proving byte-exact preservation *outside* the span.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `region-marker-in-fence-ignored`'s original fixture did not actually exercise whole-line anchoring**
- **Found during:** Task 2's required anti-vacuity-by-neutralization verification (reverting whole-line anchoring to a substring search)
- **Issue:** The original fixture only placed an exact "START" line both inside and outside a fenced block, so fence exclusion alone was sufficient to pass it — reverting whole-line anchoring to `marker in bare` left the control green, meaning the anchoring invariant it claimed to cover was not actually falsifiable by it.
- **Fix:** Added a non-fenced line containing "START" as a substring without equaling it ("See the START region below for an example."), which only whole-line anchoring correctly excludes. Re-ran the neutralization: the control now fails by name as required.
- **Files modified:** `scripts/gen-gate-docs.py`
- **Verification:** Both required neutralizations (substring search, parity toggle) each fail exactly their own named arm with no other arm affected; `--self-test` and `--check` both pass on the un-mutated tree; `bash scripts/check-firewall-battery.sh` GREEN 25/25.
- **Committed in:** `a00d104`

**Commit-granularity note (not a Rule 1-4 deviation, disclosed for transparency):** `scripts/gen-gate-docs.py` was authored as one cohesive file rather than incrementally per task, so Task 1's commit (`05e7193`) also contains Task 2's `_replace_region` primitive and its original self-test controls. Task 2's own commit (`a00d104`) captures the one real code change made while performing Task 2's specific required verification work (the fixture-hardening fix above), keeping that work separately attributable even though the bulk of Task 2's deliverable landed a commit early.

**Total deviations:** 1 auto-fixed (Rule 1) + 1 disclosed commit-granularity note.
**Impact on plan:** The auto-fix strengthened a self-test control that would otherwise have silently under-covered its stated invariant — a correctness improvement, no scope creep. The commit-granularity note does not affect the plan's success criteria; every task's specific deliverables and verifications are present and independently confirmed.

## Issues Encountered

None beyond the deviation above.

## Next Phase Readiness

- `scripts/gen-gate-docs.py` exists with a fully working `--write`/`--check`/`--self-test`/`--describe` CLI, ready for plan 21-07 to implement `generate_all()`'s render half (currently a documented stub returning `{}`).
- `_replace_region` is proved correct against the live `CLAUDE.md` in memory and is ready for plan 21-07/21-08 to drive `CLAUDE.md`'s and `docs/ARCHITECTURE.md`'s generated table regions and `docs/gates/<ID>.md`'s fenced blocks.
- The frozen-path disjointness floor and `_FROZEN_PATHS` extraction are in place and proven against the live battery script, ready to guard plan 21-08's `docs/gates/` write set.
- `bash scripts/check-firewall-battery.sh` reports GREEN 25/25; `git status --porcelain` in the real repo is clean after both commits; all three CONTRACT-06 pins untouched (this plan never modified `scripts/check-quality-harness.py`).
- No blockers.

## Known Stubs

- `generate_all()` in `scripts/gen-gate-docs.py` returns `{}` unconditionally. This is the plan's own explicitly documented deliverable shape ("Output: a generator that can harvest, floor, replace regions and diff — with a render layer that is still a stub"), not an unintentional gap — plan 21-07 implements the render half. `cmd_write()`/`cmd_check()` are fully implemented against this stub and are proved correct (including the non-determinism/drift distinction) via synthetic monkeypatched fixtures in `--self-test`.

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-06*

## Self-Check: PASSED

- FOUND: `scripts/gen-gate-docs.py` (created)
- FOUND: commit `05e7193` (`git log --oneline --all`)
- FOUND: commit `a00d104` (`git log --oneline --all`)
- FOUND: `bash scripts/check-firewall-battery.sh` reports FIREWALL: GREEN (25/25)
- FOUND: `python3 scripts/gen-gate-docs.py --self-test` exits 0 (20 controls)
- FOUND: `python3 scripts/gen-gate-docs.py --check` exits 0 (`harvested 21/21 script-backed entries`)
