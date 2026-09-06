---
phase: 21-generate-the-claim-surface
plan: 07
subsystem: tooling
tags: [gate-registry, generator, render-layer, region-replacement, ci-gates, drift-gate, containment-rule]

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    plan: 06
    provides: "scripts/gen-gate-docs.py's compute layer — harvest(),
      frozen_pathspecs()/frozen_path_write_problems(),
      all_floor_problems(), _replace_region()/RegionMarkerError,
      cmd_write()/cmd_check(), describe(), self_test() (20 controls),
      main() — with generate_all() stubbed (returns {}) for this plan to
      implement"
provides:
  - "render_gate_table(rows) -> str: the single 4-column row renderer
    (Gate | Job / Mechanism | Script | What it checks), called on the SAME
    rows value for both CLAUDE.md and docs/ARCHITECTURE.md, proving
    byte-identical output by construction (D-02)"
  - "render_table_region(rows, surface) -> str: wraps render_gate_table
    with a surface-appropriate lead-in (replacing both superseded framing
    sentences with a shared post-unification statement) and a derived
    population-arithmetic paragraph (_population_counts/
    _population_arithmetic_sentence — no hand-typed 22/25/2 literals)"
  - "_replace_or_bootstrap_region(): a first-migration-safe wrapper around
    _replace_region — CLAUDE.md and docs/ARCHITECTURE.md carry no GENERATED
    markers yet, so this bootstraps the region between two stable,
    pre-existing anchor lines (the section heading and the first line of
    the hand-written registration-history paragraph) on the first call,
    then delegates straight to _replace_region once the markers exist"
  - "render_detail_page(entry, blob, existing_text) -> str: emits
    docs/gates/<GATE-ID>.md — fully generated for thin (non-NARRATIVE_ENTRIES)
    entries (D-08), fenced-split (Facts / How-to-run, via _replace_region)
    with byte-preserved hand-written narrative for the four
    NARRATIVE_ENTRIES (QUAL-01, SCAN-GUARD, TRACE-03, CONF-GATE) when
    existing_text is supplied (D-05)"
  - "detail_page_containment_problems(): D-06's containment floor — every
    number stated outside a generated fence on a docs/gates/*.md page must
    also appear inside one, with spelled-out number normalisation
    (one..twenty, the tens, hundred, hyphenated compounds) and the page's
    own H1 (a gate-id identifier, not a count claim) excluded from the
    'outside' scan; wired into cmd_check() as a page-level floor"
  - "generate_all() fully implemented: returns CLAUDE.md, docs/ARCHITECTURE.md,
    and one docs/gates/<slug>.md page per registry entry (including the
    anticipatory CONF-SURFACE entry) — 30 targets total against the live
    28-entry registry. Nothing is written to disk by this plan; --check
    correctly reports all 30 as drifted (exit 1), which is the expected,
    proving state 21-08 builds on"
affects: [21-08, 21-09, 21-10, 21-11]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "bootstrap-then-delegate region replacement: _replace_or_bootstrap_region
      reuses _replace_region's exact whole-line-anchored, fence-aware
      matching for the steady state, and only special-cases the very first
      migration (markers absent) by locating two STABLE pre-existing prose
      anchors instead — the heading and the hand-written paragraph that
      follows the table today. Both anchors survive OUTSIDE the generated
      region on every subsequent call, so the same anchors keep working
      forever without ever being consulted again once the real GENERATED
      markers exist."
    - "one-renderer-two-surfaces by construction, not by comparison:
      generate_all() computes `rows` ONCE from ENTRIES + the harvested
      blob and calls render_gate_table(rows) for both surfaces — the
      byte-identical-table-body property cannot regress to 'two renderers
      that happen to agree' because there is structurally only one call
      site producing the row data."
    - "H1-exclusion for D-06 containment: a docs/gates/<ID>.md page's own
      title line names the gate id (e.g. `GATE-02-v8.5`), which trips the
      digit regex on its own suffix (`-8.5`) despite being an identifier,
      not a count claim — excluded from the containment scan by line
      index (0), not by an identifier-shaped-token carve-out (which
      21-CONTEXT.md's D-06 rejected as a broader alternative rule)."

key-files:
  created: []
  modified:
    - scripts/gen-gate-docs.py

key-decisions:
  - "CLAUDE_REGION_MARKERS and ARCHITECTURE_REGION_MARKERS reuse the
    IDENTICAL literal GENERATED_MARKER/GENERATED_END_MARKER text across
    both files — _replace_region operates per-file (occurrence count is
    scoped to the text it's given), so there is no collision in reusing
    the same HTML-comment marker text in two separate documents."
  - "The bootstrap anchors are the section heading (`### CI gates` /
    `## CI and pre-commit gate inventory`) and the FIRST LINE of the
    hand-written registration-history paragraph that follows the table
    today (`HARN-01, HARN-02 and HARN-03 were registered...`, worded
    slightly differently per surface — 'each is a CI job' in CLAUDE.md vs
    'each has a CI job' in docs/ARCHITECTURE.md, both transcribed
    verbatim as separate constants). This keeps the registration-history,
    two-gates-named-GATE-02 disambiguation, and retired body-budget
    paragraphs entirely OUTSIDE the generated region as hand-written
    prose, per the plan's explicit instruction — proved by
    region-preserves-surrounding-prose against the LIVE CLAUDE.md."
  - "The population-arithmetic sentence is a NEW, freshly generated
    sentence placed inside the generated region (after the table),
    distinct from the pre-existing hand-written registration-history
    paragraph that ALSO happens to mention similar figures as historical
    narrative outside the region. This is a deliberate, disclosed
    redundancy rather than an attempt to surgically excise every
    number-bearing clause from five paragraphs of irreducibly narrative
    prose — the plan requires the arithmetic to be GENERATED and the
    narrative to be PRESERVED; it does not require deduplicating the two."
  - "_script_cell's derivation is best-effort, not a byte-for-byte
    reproduction of the pre-existing hand-maintained Script column: two
    entries backing the SAME script (DUAL-04 / GATE-02-v8.5, both
    scripts/sync-content.py) are disambiguated by extracting the first
    invocation's flag from run_command, since a bare script path alone
    would render both rows identically. No acceptance criterion requires
    literal preservation of the old Script cell text, only that the
    render be derived and consistent."
  - "D-06's containment rule is scoped to docs/gates/*.md pages only, per
    Task 2's own action text ('Implement D-06's containment rule as a
    page-level check') — it is NOT applied to CLAUDE.md/ARCHITECTURE.md's
    own generated regions, whose hand-written surrounding prose (outside
    this plan's markers) is explicitly out of scope for this phase's
    CONF-13 literal-count work (a later phase's or plan's concern)."

requirements-completed: [CONF-12]

# Metrics
duration: ~35min (single session)
completed: 2026-09-06
---

# Phase 21 Plan 07: Render Layer (unified gate table + detail pages) Summary

**`scripts/gen-gate-docs.py`'s `generate_all()` now fully implemented: one `render_gate_table()` call produces a byte-identical 27-row x 4-column table for both `CLAUDE.md` and `docs/ARCHITECTURE.md`, with the `TRACE-03` glob substring and the population arithmetic both derived from the harvested `--describe` blob; `render_detail_page()` emits all 28 `docs/gates/<GATE-ID>.md` pages (fully generated for 24 thin entries, fenced-split with byte-preserved narrative for the four fat ones), and D-06's spelled-out-number-aware containment rule is wired into `--check`.**

## Performance

- **Duration:** ~35 min, single session
- **Tasks:** 2 (Task 1: shared row renderer + two table regions; Task 2: detail-page renderer, D-05 fenced split, D-06 containment)
- **Files modified:** 1 (`scripts/gen-gate-docs.py`)

## Accomplishments

- `render_gate_table(rows)` renders the unified `Gate | Job / Mechanism | Script | What it checks` table; `generate_all()` computes `rows` once from `ENTRIES` + the harvested blob and calls it for both surfaces, making byte-identical table bodies a structural fact rather than an observed coincidence — verified by the `one-renderer-two-surfaces` control.
- The live-rendered `| TRACE-03 |` row is exactly one physical line (543 characters) and contains `` `docs/*.md`, `CLAUDE.md`, `CHANGELOG.md`, `README.md` `` byte-for-byte — the exact substring `check-traceability.py`'s block `(n)` currently requires — derived via `_glob_prose()` applied to the harvested `scan_globs` field, never re-typed.
- The population-arithmetic sentence (`_population_counts`/`_population_arithmetic_sentence`) carries zero hand-typed `22`/`25`/`2` literals; a synthetic entry added to a copy of `ENTRIES` moves `ci_count` and `tallied_count` by exactly 1 while leaving `precommit_count`/`inline_count` unchanged, proving each number's derivation independently.
- Both superseded framing sentences (`CLAUDE.md`'s "keeps its own operational copy by design", `docs/ARCHITECTURE.md`'s "Every other document links here rather than restating it") are replaced on both surfaces with a shared `_POST_UNIFICATION_STATEMENT`; `framing-sentences-replaced` asserts both absence and presence, both surfaces.
- `_replace_or_bootstrap_region()` migrates `CLAUDE.md`/`docs/ARCHITECTURE.md` from "no GENERATED markers exist yet" to a generated region using two stable pre-existing prose anchors (the section heading, and the first line of the hand-written registration-history paragraph that follows the table) — `region-preserves-surrounding-prose` proves, against the LIVE `CLAUDE.md` in memory, that everything from that paragraph onward survives byte-identically.
- `render_detail_page()` emits `docs/gates/<GATE-ID>.md` for all 28 registry entries (including the anticipatory `CONF-SURFACE` entry, per the `page-per-entry` control's set-equality floor): 24 thin pages are fully generated with no hand-written region at all (`thin-page-fully-generated`), and the four `NARRATIVE_ENTRIES` (`QUAL-01`, `SCAN-GUARD`, `TRACE-03`, `CONF-GATE`) preserve a hand-written narrative paragraph byte-identically across a blob change and a second regeneration pass (`narrative-preserved-across-regeneration` proves both the preservation and the idempotency).
- D-06's containment rule (`detail_page_containment_problems`) is wired into `cmd_check()` as a page-level floor over every generated `docs/gates/*.md` page; it normalises spelled-out number words (`one`..`twenty`, the tens, `hundred`, hyphenated compounds) to their digit form before comparing, proved by paired fire/pass controls in both digit and spelled-out form (`containment-violation-fires`, `containment-satisfied-passes`, `containment-spelled-out-normalised`).
- `python3 scripts/gen-gate-docs.py --check` exits **1**, reporting **30 drifted targets** (`len(ENTRIES) + 2` = 28 + 2) — every `docs/gates/*.md` page plus both surface files — confirmed by direct count of `DRIFT:` lines in the live run. A `0` here would mean the renderer reproduced the pre-existing hand-maintained text, which D-02 makes impossible; `_control_check_dispatch_wired` was updated in place (from plan 21-06's `rc == 0` expectation) to assert `rc == 1` for this exact reason.
- Both required anti-vacuity neutralizations were performed on scratch copies (never touching the real tree) and each failed exactly the arm(s) the mechanism they disabled backs:
  - Spelled-out normalisation disabled (`_spelled_number_value` short-circuited to always return `None`): `containment-spelled-out-normalised` FAILED with `SELF-TEST FAIL [containment-spelled-out-normalised] — []` (the "should fire" arm reported zero problems instead of one, since "forty-seven" was no longer recognised at all). No other control failed.
  - Outside-fence extraction disabled (`outside_lines` hard-coded to `[]`): `containment-violation-fires` FAILED with `SELF-TEST FAIL [containment-violation-fires] — []` (as required). `containment-spelled-out-normalised` also failed as an expected, non-masking side effect — both controls share the same `outside_lines` extraction step, so disabling it collapses both to zero findings; this is a legitimate consequence of removing the shared mechanism, not a masking failure of either control against its own target.
- `bash scripts/check-firewall-battery.sh` reports **FIREWALL: GREEN (25/25)** after the commit. `git diff --stat` over `scripts/check-quality-harness.py` across this plan's range is empty, so all three CONTRACT-06 pins are provably byte-unchanged.

## Task 1: The shared 27x4 row renderer and the two table regions

| Verification | Result |
|---|---|
| `python3 scripts/gen-gate-docs.py --self-test` | exits 0, `SELF-TEST PASS — 34 controls run` (strictly greater than 21-06's 20) |
| `python3 scripts/gen-gate-docs.py --check` | exits 1, `harvested 21/21 script-backed entries`, 30 `DRIFT:` blocks |
| Table body identity | `render_gate_table(rows)` called on the same `rows` twice: byte-identical (verified both via the `one-renderer-two-surfaces` control and by extracting each surface's rendered table and comparing directly — `IDENTICAL: True`, 27 rows) |
| Live TRACE-03 row | one physical line, 543 characters, contains `` `docs/*.md`, `CLAUDE.md`, `CHANGELOG.md`, `README.md` `` byte-for-byte |
| `git status --porcelain` (pre-commit) | `scripts/gen-gate-docs.py` only |

Named isolation arms implemented and passing: `one-renderer-two-surfaces`, `row-count-equals-entries`, `no-row-wrapped`, `trace03-glob-substring-derived` (synthetic + live arms), `population-arithmetic-derived`, `framing-sentences-replaced`, `region-preserves-surrounding-prose`.

## Task 2: The `docs/gates/<GATE-ID>.md` detail-page renderer

| Verification | Result |
|---|---|
| `python3 scripts/gen-gate-docs.py --self-test` | exits 0, 34 controls (Task 2 added 8 to Task 1's 26 running total, itself 6 above 21-06's 20) |
| `python3 scripts/gen-gate-docs.py --check` | exits 1, drifted-target count = 30 = `len(ENTRIES)` (28) `+ 2` |
| `docs/gates/` on disk | absent throughout — nothing written by this plan |
| `git status --porcelain` | `scripts/gen-gate-docs.py` only |

Named isolation arms implemented and passing: `page-per-entry`, `narrative-preserved-across-regeneration`, `thin-page-fully-generated`, `containment-violation-fires`, `containment-satisfied-passes`, `containment-spelled-out-normalised`, `check-reports-full-drift-count`. Plan 21-06's `check-dispatch-wired` control was amended in place (documented above) to match the new, correct `rc == 1` expectation.

## Task Commits

1. **Task 1 + Task 2: render layer implementation** — `7a86bc9` (feat) — both tasks landed in one commit; see Deviations below.

**Plan metadata:** this commit (SUMMARY only — STATE/ROADMAP excluded per worktree mode; the orchestrator owns those writes after the wave completes)

## Files Created/Modified

- `scripts/gen-gate-docs.py` (modified, +802/-10 lines) — `render_gate_table()`, `render_table_region()`, `_replace_or_bootstrap_region()`, `render_detail_page()`, `detail_page_containment_problems()` and supporting helpers (`_page_slug`, `_glob_prose`, `_script_cell`, `_checks_cell`, `_gate_table_rows`, `_population_counts`, `_population_arithmetic_sentence`, `_facts_block`, `_how_to_run_block`, `_normalise_numbers`, `_generated_line_flags`), `generate_all()` fully wired, `cmd_check()` extended with the D-06 containment floor, 14 new self-test controls (26 to 34 net across both tasks, plus the `check-dispatch-wired` amendment)

## Decisions Made

See `key-decisions` in frontmatter — summarized: (1) both surfaces' GENERATED markers reuse identical literal text since `_replace_region` scopes occurrence counts per-file; (2) the bootstrap anchors for the first migration are two stable, pre-existing prose lines (the section heading and the hand-written registration-history paragraph's first line), keeping all downstream hand-written narrative outside the generated region; (3) the population-arithmetic sentence is a new generated sentence, deliberately not a surgical rewrite of the pre-existing hand-written paragraph that also mentions similar figures as historical narrative; (4) `_script_cell`'s rendering is a fresh, derived design, not a byte-for-byte reproduction of the legacy hand-maintained Script column; (5) D-06's containment rule is scoped to `docs/gates/*.md` pages only, per Task 2's own action text.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `_control_check_dispatch_wired` (plan 21-06) asserted the wrong exit code for the now-implemented render layer**
- **Found during:** Task 1, first `--self-test` run after wiring `generate_all()`
- **Issue:** Plan 21-06's `check-dispatch-wired` control asserted `main(["--check"])` returns `0` against the live tree — correct while `generate_all()` was a stub returning `{}`, but now that it returns real generated content that necessarily differs from the pre-existing hand-maintained `CLAUDE.md`/`docs/ARCHITECTURE.md`/absent `docs/gates/` pages, `0` would mean the renderer reproduced the pre-existing text, which is impossible under D-02 (exactly the plan's own stated acceptance criterion: "Exit 0 here would mean the renderer produced the pre-existing text ... treat a 0 as a defect").
- **Fix:** Updated the control's assertion to `rc == 1` with an expanded docstring explaining why, and added a distinct `check-reports-full-drift-count` control that additionally asserts the drifted-target count equals `len(ENTRIES) + 2` and that no `docs/gates/*.md` page exists on disk yet.
- **Files modified:** `scripts/gen-gate-docs.py`
- **Verification:** `--self-test` passes with both controls green; `--check` confirmed to exit 1 with exactly 30 `DRIFT:` blocks.
- **Committed in:** `7a86bc9`

**2. [Rule 1 - Bug] Initial containment-rule wiring flagged false positives from digits inside identifiers/hand-written comments**
- **Found during:** Task 2, first live `--check` run after wiring `detail_page_containment_problems` into `cmd_check()`
- **Issue:** The containment scan's first cut matched `05` inside the hand-written `(D-05)` parenthetical in `_DISCLOSED_BOUNDS_HAND_WRITTEN_COMMENT`, firing on three `NARRATIVE_ENTRIES` pages (`TRACE-03`, `QUAL-01`, `CONF-GATE`) even though nothing was actually wrong — the digits belonged to a plan-decision label, not a count claim.
- **Fix:** Removed the `(D-05)` reference from the hand-written comment text (reworded without digits) rather than special-casing the scanner for this one string, keeping the containment mechanism itself general.
- **Files modified:** `scripts/gen-gate-docs.py`
- **Verification:** `python3 scripts/gen-gate-docs.py --check` reports zero containment problems on all 28 generated pages; the two required containment controls (`containment-violation-fires`/`containment-satisfied-passes`) still discriminate correctly.
- **Committed in:** `7a86bc9`

**Commit-granularity note (not a Rule 1-4 deviation, disclosed for transparency, matching plan 21-06's precedent):** Both tasks landed in a single commit (`7a86bc9`). The render layer's constants, row/table renderers, detail-page renderer, and D-06 containment rule are mutually dependent (the detail-page renderer reuses the same marker/fence-scanning primitives the table-region bootstrap uses; the containment floor is wired into the same `cmd_check()` the table renderer's drift-count criterion depends on), so the file was authored and verified as one cohesive unit rather than incrementally per task — the same shape plan 21-06 recorded for the same underlying reason.

**Total deviations:** 2 auto-fixed (both Rule 1) + 1 disclosed commit-granularity note.
**Impact on plan:** Both auto-fixes are correctness fixes surfaced by the plan's own required verification steps (running `--self-test`/`--check` after wiring), not scope creep. The commit-granularity note does not affect the plan's success criteria; every task's specific deliverables and verifications are present and independently confirmed above.

## Issues Encountered

None beyond the deviations above.

## Next Phase Readiness

- `scripts/gen-gate-docs.py`'s `generate_all()` is fully implemented and returns real content for all 30 targets (`CLAUDE.md`, `docs/ARCHITECTURE.md`, 28 `docs/gates/*.md` pages).
- `python3 scripts/gen-gate-docs.py --write` is ready for plan 21-08 to land: `--check` currently reports the expected drift (all 30 targets), proving the machinery is correct and nothing has been written yet.
- `bash scripts/check-firewall-battery.sh` reports GREEN 25/25; `git status --porcelain` in the real repo is clean after the commit; `scripts/check-quality-harness.py` is untouched (`git diff --stat` empty over this plan's range), so all three CONTRACT-06 pins are provably byte-unchanged.
- No blockers.

## Known Stubs

None — `generate_all()` is the plan's own deliverable and is no longer a stub; `--write` has simply not been RUN yet (that is plan 21-08's explicit job, not a gap in this plan).

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-06*

## Self-Check: PASSED

- FOUND: `scripts/gen-gate-docs.py` modified (render layer implemented)
- FOUND: commit `7a86bc9` (`git log --oneline --all`)
- FOUND: `bash scripts/check-firewall-battery.sh` reports FIREWALL: GREEN (25/25)
- FOUND: `python3 scripts/gen-gate-docs.py --self-test` exits 0 (34 controls)
- FOUND: `python3 scripts/gen-gate-docs.py --check` exits 1 (30 drifted targets = len(ENTRIES)+2)
