---
phase: 20-live-conformance
plan: 04
subsystem: testing
tags: [conformance, live-capture, quality-harness, report-generator, self-test]

# Dependency graph
requires:
  - phase: 20-live-conformance
    provides: "plan 20-03's 8 dispositioned catalog rows and the offline detect_defects reading (primary/secondary rate 5 of 8, all 8 completed) over the 8 landed captures"
provides:
  - "scripts/report-conformance.py: a fifth labelled surface (live-conformance) -- LIVE_CONFORMANCE_* constants, discover_artifacts widening, build_live_row, _live_row_clean, compute_live_headline, _render_live_conformance_section, the live_conformance JSON key, and 13 new --self-test controls (71 total)"
  - "docs/conformance-baseline.md's ## live-conformance section and docs/data/conformance.json's live_conformance key, publishing the 5-of-8 rate with its N, noise caveat, delegation-conditional bound, non-interactive-branch bound (with both foreclosed paths named as unmeasured, not measured-and-equal), false-negative backdrop, n/a-provenance departure and observation-not-a-gate clause"
affects: [20-05, 20-06]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "item-by-predicate headline as a sibling of the numeric-sum compute_headline (compute_live_headline mirrors compute_corpus_headline's shape, not compute_headline's)"
    - "four-value column vocabulary (number / n/a / unreadable / no-analysis) -- a run that never produced an analysis reads a distinct literal from a run whose analysis was unreadable"
    - "a live surface's rows excluded entirely from the flat JSON 'rows'/'artifact_count', unlike the adversarial-corpus precedent which keeps corpus rows in both the flat list and its own nested key"

key-files:
  created: []
  modified:
    - scripts/report-conformance.py
    - docs/conformance-baseline.md
    - docs/data/conformance.json

key-decisions:
  - "Live rows are excluded from render_json's flat top-level \"rows\" list and from \"artifact_count\" entirely (unlike adversarial-corpus rows, which stay in both the flat list and their own nested key) -- per Task 3's explicit acceptance criterion, this is the extra margin against a future consumer that iterates \"rows\" without filtering by surface, on top of _GATED_SURFACES already excluding the surface from CONF-GATE"
  - "The non-interactive-branch bound is published as unmeasured, not measured-and-equal, per the amendment: the pre-analysis clarification path and the mid-run Self-Audit-Gate re-open are structurally unreachable under the locked claude -p transport, and the section states this as a scope bound rather than implying the interactive branch would score the same"
  - "askuserquestion_disclosed (a new per-row bool, detected by scanning the persisted .md text for the literal substring \"AskUserQuestion\") backs the render section's interpolated disclosure count -- added because the hard rule forbids any hardcoded count/id inside _render_live_conformance_section's source, and the amendment requires stating how many runs opened with the disclosure"

requirements-completed: [CONF-09, CONF-10]

# Metrics
duration: "~1h"
completed: 2026-09-06
---

# Phase 20 Plan 04: Live-Conformance Surface and Publication Summary

**Added `live-conformance` as a fifth discovered/scored/rendered/JSON-published surface in `scripts/report-conformance.py`, and regenerated `docs/conformance-baseline.md` + `docs/data/conformance.json` to publish a primary and secondary rate of 5 of 8 (all 8 runs completed), reconciling exactly against plan 20-03's SUMMARY table, together with every disclosed bound the amendment requires.**

## Performance

- **Duration:** ~1h
- **Started:** continuation of same session lineage as 20-01/20-02/20-03
- **Completed:** 2026-09-06
- **Tasks:** 3 (all auto, each committed)
- **Files modified:** 3 (`scripts/report-conformance.py`, `docs/conformance-baseline.md`, `docs/data/conformance.json`)

## Accomplishments

- `live-conformance` discovered under a named count floor (`MIN_LIVE_CONFORMANCE_RUNS = 8`), scored via the unmodified, CONTRACT-06-frozen `detect_defects` (through `build_row`), and aggregated by an item-by-predicate headline (`compute_live_headline`) that is never folded into `compute_headline`'s numeric-sum shape.
- A four-value column vocabulary (`number` / `"n/a"` / `"unreadable"` / `"no-analysis"`) added specifically for this surface: a run that never produced a persisted analysis reads `"no-analysis"` in every measured field, never `0` and never conflated with the pre-existing `"unreadable"` state (a persisted-but-`_slice_sections`-rejected document).
- `## live-conformance` published in `docs/conformance-baseline.md`, positioned after `## adversarial-corpus` and before `## Source-vs-twin agreement (D-04)`, stating: the rate and its N, the secondary completion-conditional rate with an outcome breakdown, the K-of-5 noise-discipline caveat, the D-04 delegation-conditional bound, the non-interactive-branch bound (naming `AskUserQuestion`'s structural unavailability and both foreclosed paths — the pre-analysis clarification path and the mid-run re-open — as unmeasured, never measured-and-equal), the false-negative backdrop against `adversarial-corpus`'s own published rate, the `n/a`-provenance departure (D-06), and the observation-not-a-gate clause.
- `docs/data/conformance.json` carries the `live_conformance` top-level key (`headline` + `rows`), sibling to `adversarial_corpus`; `surface_counts["live-conformance"]` is populated; the flat top-level `"rows"` list and `"artifact_count"` deliberately exclude live rows (a stricter exclusion than the adversarial-corpus precedent, per Task 3's explicit acceptance criterion).
- 13 new offline `--self-test` controls registered in both `_CONTROLS` and `_CONTROL_IDS` (71 total, up from 58); none reads the real `tests/live-conformance-v9.0/` fixture.

## Task Commits

1. **Task 1: Constants, discovery, build_live_row and compute_live_headline** - `9056065` (feat)
2. **Task 2: The `## live-conformance` render section and the `live_conformance` JSON key** - `214ca9d` (feat)
3. **Task 3: Date and regenerate the two published artifacts, and prove byte-for-byte reproduction** - `a3847ac` (feat)

**Plan metadata:** (this commit, immediately following)

## Files Created/Modified

- `scripts/report-conformance.py` — fifth surface: `LIVE_CONFORMANCE_CAPTURE_GLOB`/`CATALOG`/`README`, `MIN_LIVE_CONFORMANCE_RUNS`, `_LIVE_FORM_FIELDS`, `_read_live_catalog`, `_live_row_clean`, `build_live_row`, `compute_live_headline`, `_LIVE_TABLE_FIELDS`, `_LIVE_NONINTERACTIVE_MARKERS`, `_render_live_conformance_section`, `render_json`/`render_markdown` wiring, `_make_minimum_tree` widened, 13 new `--self-test` controls
- `docs/conformance-baseline.md` — regenerated, new `## live-conformance` section, `MEASUREMENT_DATE` bumped to `2026-09-06`
- `docs/data/conformance.json` — regenerated, new `live_conformance` top-level key

## Decisions Made

- Live rows excluded from the flat `"rows"`/`"artifact_count"` JSON surface entirely (see key-decisions above) — a deliberate divergence from the adversarial-corpus precedent, driven by Task 3's own acceptance criterion text.
- The non-interactive-branch bound's incidence figure ("Of the 8 runs, N opened with this disclosure") is computed from a new per-row `askuserquestion_disclosed` field rather than hardcoded, satisfying the hard rule that no integer count may appear as a literal inside `_render_live_conformance_section`'s source; the prompt-correlation clause itself ("firing in the runs whose prompts were underspecified...") is stated as qualitative prose with no digit literal, since the amendment's specific 5-vs-3 PR/Q split is already recorded, with its own numbers, in the human-authored `tests/live-conformance-v9.0/README.md` (a static fixture document, not a code-generated surface the hard rule constrains).
- `compute_live_headline`'s `form_defects` field sums only over resolved (`section_resolution == "OK"`) rows, matching `compute_corpus_headline`'s own precedent exactly (the `_LIVE_FORM_FIELDS` constant's own comment about `heading_malformed_blocks` being counted unconditionally describes how `check-conf-gate.py`'s own separate, pre-existing aggregation works over its two gated surfaces — informational context for the reader, not a requirement this new per-surface headline replicates, since `check-conf-gate.py` does not read `live-conformance` at all).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] `_make_minimum_tree` and `_control_floor_passes_at_minimum` needed the new floor's minimum population, or every pre-existing floor control would fail**
- **Found during:** Task 1, before the first self-test run
- **Issue:** `discover_artifacts`'s new fifth count floor (`MIN_LIVE_CONFORMANCE_RUNS = 8`) applies unconditionally. The existing `--self-test` helper `_make_minimum_tree` (used by `_control_floor_shared_short`, `_control_floor_twin_short`, `_control_floor_contract_missing` and `_control_floor_passes_at_minimum`) did not populate any `tests/live-conformance-v9.0/*.jsonl` files, so every one of those four pre-existing controls would have started raising `DiscoveryFloorError` on the *new* floor before ever reaching the floor each control actually exercises.
- **Fix:** Widened `_make_minimum_tree` to also write `MIN_LIVE_CONFORMANCE_RUNS` placeholder `.jsonl` files, and widened `_control_floor_passes_at_minimum`'s expected artifact count to add `MIN_LIVE_CONFORMANCE_RUNS`.
- **Files modified:** `scripts/report-conformance.py`
- **Verification:** `python3 scripts/report-conformance.py --self-test` — all 4 pre-existing floor controls and the new `live-floor-short` control pass; full battery re-confirmed GREEN 25/25 in Task 3.
- **Committed in:** `9056065` (Task 1 commit)

**2. [Rule 1 - Bug] Task 1's live-conformance self-test controls initially embedded the real fixture path as a relpath literal, violating "none of them reading tests/live-conformance-v9.0/"**
- **Found during:** Task 1, self-review against the acceptance criterion "No new control reads `tests/live-conformance-v9.0/` — verified by the controls' source containing no reference to that path"
- **Issue:** Several new controls (in both Task 1 and Task 2) passed `"tests/live-conformance-v9.0/<name>"` as a synthetic `relpath`/`capture_relpath` string for tempdir-backed `Artifact`s. The controls never opened that real directory (all reads were against `tempfile.TemporaryDirectory()` paths), but the literal path string appeared in the controls' own source text, which the acceptance criterion reads literally.
- **Fix:** Replaced every such literal with a bare filename (e.g. `"stub.jsonl"`, `"x01.md"`), matching the adversarial-corpus controls' own precedent (`_control_corpus_render_no_hardcoded_stems` uses `"x01.md"`, not a `tests/adversarial-corpus-v9.0/` prefix).
- **Files modified:** `scripts/report-conformance.py`
- **Verification:** `sed -n '/live-conformance surface controls/,/^_CONTROLS: tuple/p' scripts/report-conformance.py | grep tests/live-conformance-v9.0` shows only the section's own comment line, no control body; `--self-test` re-run clean (66/71 controls at each respective stage).
- **Committed in:** `9056065` (Task 1 commit), `214ca9d` (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (1 blocking, 1 bug)
**Impact on plan:** Both fixes were necessary to keep the pre-existing self-test battery green and to satisfy an explicit acceptance criterion; no scope creep, no behavior change to any published figure.

## Assumption Drift (advisory)

None material. The amendment's five findings were published exactly as measured, with the non-interactive-branch bound stated as unmeasured (not measured-and-equal), matching the amendment's explicit instruction.

## Figure-by-Figure Reconciliation Against Plan 20-03's SUMMARY

Every figure below was read from the regenerated `docs/conformance-baseline.md` / `docs/data/conformance.json` and compared against plan `20-03-SUMMARY.md`'s Task 1 table.

| id | outcome | section_resolution | heading_malformed_blocks | nonconforming_verdict_cells | silent_untraced_claims | clean | 20-03 match |
|---|---|---|---|---|---|---|---|
| Q-P1 | completed | OK | 0 | 0 | 0 | True | yes |
| Q-P2 | completed | OK | 0 | 31 | 0 | False | yes |
| Q-P3 | completed | OK | 0 | 0 | 0 | True | yes |
| PR-P1 | completed | OK | 0 | 0 | 0 | True | yes |
| PR-P2 | completed | OK | 0 | 0 | 0 | True | yes |
| PR-N1 | completed | OK | 0 | 1 | 0 | False | yes |
| PR-N2 | completed | OK | 0 | 1 | 0 | False | yes |
| PR-P1-R2 | completed | OK | 0 | 0 | 0 | True | yes |

- **Primary rate (clean over runs attempted):** regenerated `5 of 8`; 20-03 reported `5 of 8`. **Match.**
- **Secondary rate (clean over runs completed):** regenerated `5 of 8` of `8 completed`; 20-03 reported `5 of 8` (identical since all 8 completed). **Match.**
- **Outcome breakdown:** regenerated `8 completed / 0 rate_limit_stub / 0 transport_error_stub / 0 no_terminal_result`; 20-03 reported the identical breakdown. **Match.**
- **`headline["form_defects"]` = 33** (31 + 1 + 1, summed over `_LIVE_FORM_FIELDS` on the three non-clean readable rows) — consistent with 20-03's per-row counts; no separate published total existed in 20-03 to compare against, so this is a derived-and-reconciled-by-construction figure, not an independently re-verified one.
- **False-negative backdrop cross-reference:** the rendered section's `10 of 13` corpus figure was read from `compute_corpus_headline`, computed in the same run as the live headline — not transcribed — so it cannot silently drift from `docs/conformance-baseline.md`'s own `## adversarial-corpus` section.

No figure differed. Nothing was adjusted to force a match; the code was written from the plan's specification and the reconciliation above confirms it computes what 20-03 already measured.

## Issues Encountered

None blocking beyond the two auto-fixed deviations above.

## User Setup Required

None.

## Next Phase Readiness

- `scripts/report-conformance.py` publishes a fifth, fully self-tested surface; `docs/conformance-baseline.md` and `docs/data/conformance.json` are regenerated and reproduce byte-for-byte under `--check`.
- Coverage headline (`192 reproducible / 94 audit-only / 0 gap / 286 total`) unchanged; `docs/requirements-traceability.md` unedited; `_GATED_SURFACES` still the 2-tuple `("shared-examples", "generated-twin")`; battery GREEN 25/25; all three CONTRACT-06 pins byte-unchanged throughout (`check-quality-harness.py --self-test` run and passed after every task).
- No blockers for plan 20-05 or 20-06.

---
*Phase: 20-live-conformance*
*Completed: 2026-09-06*

## Self-Check: PASSED

- `scripts/report-conformance.py` — FOUND
- `docs/conformance-baseline.md` — FOUND
- `docs/data/conformance.json` — FOUND
- `.planning/phases/20-live-conformance/20-04-SUMMARY.md` — FOUND
- `9056065` (Task 1 commit) — FOUND
- `214ca9d` (Task 2 commit) — FOUND
- `a3847ac` (Task 3 commit) — FOUND
- `11e9293` (SUMMARY commit) — FOUND

No missing items.
