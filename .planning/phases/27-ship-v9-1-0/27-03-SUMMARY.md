---
phase: 27-ship-v9-1-0
plan: 03
subsystem: testing
tags: [conformance-baseline, recurrence-reading, report-conformance, gen-gate-docs, REL-08]

# Dependency graph
requires:
  - phase: 27-ship-v9-1-0 (plan 01)
    provides: "tests/recurrence-reading-v9.1/protocol.md and README.md (the sweep protocol and frozen-evidence discipline this plan's reader parses)"
provides:
  - "scripts/report-conformance.py: the sixth labelled surface (recurrence-reading) -- schema, floor, reader, row builder, headline, render section, JSON sibling key, 8 self-test controls (102 -> 110)"
  - "docs/conformance-baseline.md / docs/data/conformance.json: the rendered ## recurrence-reading section and recurrence_reading JSON key, publishing an explicit not-yet-recorded state with no digit"
affects:
  - "plan 27-04 (pre-arm reading, fills the six record files' pending chain-of-custody rows and gives the reader real data to parse)"
  - "plan 27-09 (post-arm reading, second timing)"

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "closed-column-vocabulary reader with a self-checked totals line (RecurrenceRecordParseError), mirroring _parse_corpus_target's closed-vocabulary discipline"
    - "headline computation that never sums across instruments or averages across readers, enforced by a source-level AST control (CONTEXT.md D-01/D-05/D-08 made mechanical)"
    - "digit-free render prose while a reading is absent, verified by direct grep extraction rather than assumed"

key-files:
  created: []
  modified:
    - scripts/report-conformance.py
    - docs/conformance-baseline.md
    - docs/data/conformance.json
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - docs/gates/CONF-SURFACE.md
    - docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md

key-decisions:
  - "Both plan tasks landed in one commit, not two, because pre-commit gate 3 is unconditional and Task 1 alone already moves discovered_artifact_count"
  - "Reworded 'Two instruments...Two readers...' prose to avoid spelled-out number words after detail_page_containment_problems flagged 'Two' as a claim of 2"
  - "Widened the pre-existing 'Column vocabulary' non_live filter to also exclude recurrence-reading rows (Rule 1: the new surface has no provenance-field schema at all)"

requirements-completed: []

# Metrics
duration: ~90min
completed: 2026-09-11
---

# Phase 27 Plan 03: Recurrence-Reading Surface (Inert) Summary

Landed the sixth labelled surface, `recurrence-reading`, in `scripts/report-conformance.py`: a closed-vocabulary reader over `tests/recurrence-reading-v9.1/`'s six declared (timing x arm) record files, a headline computation that never sums across instruments or averages across readers, a `## recurrence-reading` render section publishing an explicit not-yet-recorded state with no digit (verified by direct extraction and grep, not assumed), and 8 new self-test controls (102 -> 110), each proven non-vacuous by induced failure this session.

## Performance

- **Duration:** ~90 min
- **Completed:** 2026-09-11T00:43:36Z
- **Tasks:** 2 (both landed in a single commit — see Deviations)
- **Files modified:** 7

## Accomplishments

- `RECURRENCE_READING_DIR`/`RECURRENCE_SUPPORT_FILES`/`RECURRENCE_RECORD_FILES` constants, a sixth `Artifact.surface` Literal value, `discover_artifacts()`'s support-file floor, and unconditional appending of all six declared record-slot artifacts (present or absent, never silently dropped)
- `_read_recurrence_records()`: parses the eight-column Markdown table, re-derives sites/claims from the parsed rows, and raises `RecurrenceRecordParseError` on a totals-line mismatch or an out-of-vocabulary `tier`/`fence class` cell (T-27-08)
- `build_recurrence_row()`: derives timing/arm/reader from the filename, never calls the document-defect detector (there is no document to score)
- `compute_recurrence_headline()`: per-(timing, arm, reader) sites/claims pairs, the instrument gap (prose-vs-scanner, per timing), and the timing delta (pre-vs-post, per arm/reader, joined on file+claimed-value so a shifted line number is not mistaken for a new site) — its own docstring states the D-01/D-05 no-sum/no-average prohibition
- `_render_recurrence_reading_section()`: renders the section into `render_markdown()`; `render_json()` gained a `recurrence_reading` sibling key (headline + full row list) and a `recurrence-reading` `surface_counts` entry, excluded from the flat `rows` list on the same grounds as `live-conformance`
- 8 new self-test controls (`recurrence-support-floor`, `recurrence-totals-line-must-match-rows`, `recurrence-closed-column-vocabulary`, `recurrence-absent-record-emits-no-digit`, `recurrence-arms-never-summed`, `recurrence-readers-never-averaged`, `recurrence-timing-delta-joins-on-content`, `recurrence-no-exit-code-conditioned-on-count`), dual-registered in `_CONTROLS`/`_CONTROL_IDS`
- Regenerated `docs/conformance-baseline.md` + `docs/data/conformance.json`, then `CLAUDE.md`/`docs/ARCHITECTURE.md`/`docs/gates/CONF-SURFACE.md`/`docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md` via `gen-gate-docs.py --write`

## Task Commits

Both tasks landed in one commit (see Deviations for why the two-commit split was not possible):

1. **Task 1 (register the surface) + Task 2 (render, controls, regenerate)** — `90f28ee` (feat)

**Plan metadata:** this file's own commit (`docs(27-03): add plan summary`, applied after this file is written)

## Files Created/Modified

- `scripts/report-conformance.py` — the sixth surface: constants, `Artifact.surface` extension, `discover_artifacts()` floor + append loop, `RecurrenceRecordParseError`, `_read_recurrence_records`, `build_recurrence_row`, `build_rows()` dispatch, `compute_recurrence_headline`, `_render_recurrence_reading_section`, `render_markdown`/`render_json` wiring, 8 self-test controls, plus a Rule 1 fix to the pre-existing "Column vocabulary" paragraph's surface filter and a `_control_json_count_scopes_agree` fixture update
- `docs/conformance-baseline.md` — new `## recurrence-reading` section
- `docs/data/conformance.json` — new `recurrence_reading` top-level key, `surface_counts.recurrence-reading`
- `CLAUDE.md` / `docs/ARCHITECTURE.md` / `docs/gates/CONF-SURFACE.md` / `docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md` — generated regions moved `control_ids`/`control_count` 102 -> 110 and `literal_scan_nonmodule_docstring_hits` 398 -> 401 (measured, non-gating) via `gen-gate-docs.py --write`

## Decisions Made

- **Both tasks in one commit.** Pre-commit gate 3 (`report-conformance.py --check`) is unconditional on every commit. Registering the surface alone (Task 1) already changes `discover_artifacts()`'s/`build_rows()`'s output (six new artifacts), which moves `discovered_artifact_count` in `docs/data/conformance.json` regardless of whether the render section exists yet. A Task-1-only commit therefore cannot pass the mandatory hook without `--no-verify`, which is forbidden. Completing both tasks' code before either commit lands keeps the regenerated baseline pair internally consistent (a real `## recurrence-reading` section, not orphan JSON rows with no section to explain them).
- **Digit-free render prose required rewording decision-ID citations out of the section.** The plan's acceptance criterion is a literal "no Arabic digit other than the frozen path" grep test over the rendered section — stricter than the semantic literal-scanner most other pages satisfy. Draft prose citing `CONTEXT.md D-01`/`D-03`/`D-05`/`D-08`, "Phase 26", and "plan 27-09" was reworded to plain prose with no decision-ID digits, since those citations would have failed the literal grep even though they would not have tripped `_scan_text_for_literal_hits()`.
- **`detail_page_containment_problems()` flagged "Two" as a claim of `2`.** The spelled-out-number matcher (`check_spelled_out=True`, the default) treats "Two instruments... Two readers..." as stating the value 2. Reworded to "Instruments never summed; readers never reconciled" and "prose readers A and B" — `docs/conformance-baseline.md` is not actually a registered containment or literal-scan surface (confirmed by reading `LITERAL_SCAN_MD_GLOBS` and `_CONTAINMENT_SURFACES` directly), so this was a courtesy fix per the plan's own instruction ("Reword any hit; do not exempt one"), not a gate requirement.
- **Widened the pre-existing "Column vocabulary" paragraph's surface filter (Rule 1).** `non_live = [r for r in rows if r["surface"] != "live-conformance"]` silently counted the new recurrence-reading rows into "artifacts on the four surfaces above" (a sentence specifically about provenance-field semantics those rows do not have), inflating the stated count from 42 to 48. Widened the exclusion to also drop `recurrence-reading`, restoring the correct count.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed "Column vocabulary" paragraph's surface-count inflation**
- **Found during:** Task 2 (`--check` drift review before regenerating)
- **Issue:** `non_live = [r for r in rows if r["surface"] != "live-conformance"]` counted the six new recurrence-reading rows into a sentence describing "artifacts on the four surfaces above" (shared-examples, generated-twin, contract-surface, adversarial-corpus) — a count those rows do not belong to, since they carry no provenance-field schema at all.
- **Fix:** Widened the exclusion to `r["surface"] not in ("live-conformance", "recurrence-reading")`.
- **Files modified:** `scripts/report-conformance.py`
- **Verification:** `--check` shows zero drift on the "Column vocabulary" paragraph (count stays 42, matching the on-disk baseline).
- **Committed in:** `90f28ee`

**2. [Rule 3 - Blocking] `_control_json_count_scopes_agree`'s driven-with-a-row-on-every-surface fixture needed a sixth surface**
- **Found during:** Task 2 (`--self-test` after wiring `render_json`'s new sibling key)
- **Issue:** The pre-existing control asserted `set(counts) == {...five surfaces...}` and drove its fixture with a row on every surface except the new one — both would have silently passed even if `recurrence-reading` were missing from `surface_counts`.
- **Fix:** Added a synthetic `recurrence-reading` row to the fixture and widened the asserted surface set to six.
- **Files modified:** `scripts/report-conformance.py`
- **Verification:** `--self-test` passes (110 controls); re-running with the fix reverted reproduces the original failure (`{'shared-examples': 1, ..., 'recurrence-reading': 0}` mismatch).
- **Committed in:** `90f28ee`

**3. [Rule 1 - Bug] `compute_recurrence_headline`'s timing-delta join used the full `file:line` string, not `file` alone**
- **Found during:** Task 1 (writing `compute_recurrence_headline` against the action's own spec, before any control existed)
- **Issue:** The action requires joining on "`file` plus `claimed value` rather than on line number", but the first draft's `_claimed_ids` used the raw `file:line` string as half the key, which would treat a line-number shift as a different site.
- **Fix:** Split `file:line` on its trailing `:` and use only the file portion in the join key.
- **Files modified:** `scripts/report-conformance.py`
- **Verification:** `recurrence-timing-delta-joins-on-content` control passes and was proven non-vacuous (see below).
- **Committed in:** `90f28ee`

---

**Total deviations:** 3 auto-fixed (2 Rule 1 bugs, 1 Rule 3 blocking-test-gap fix). All within scope of making the new surface correct; no scope creep.

## Issues Encountered

- **Task boundary vs. mandatory pre-commit gate.** See "Both tasks in one commit" above. Documented as a deviation rather than a blocker since the resolution (complete both tasks' code, land one commit) satisfies every one of the plan's stated acceptance criteria for both tasks except the literal "two separate commits" framing, which was never itself an acceptance criterion.
- **`docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md` moved but was not named in the plan's file list.** `gen-gate-docs.py --write` regenerates this page too (it renders `report-conformance.py --describe`'s own `control_ids`/`control_count`, the same fields CLAUDE.md's/ARCHITECTURE.md's gate-table row cites). Included in the commit since omitting it would have failed `gen-gate-docs.py --check` (pre-commit gate 5) and the firewall battery's CONF-SURFACE gate.

## Verification (observed this session)

- `python3 scripts/report-conformance.py --self-test` → `SELF-TEST PASS — 110 controls run` (was 102 before this plan; each of the 8 new controls individually proven non-vacuous by induced failure, transcribed below).
- `python3 scripts/report-conformance.py --check` → `PASS — no drift`.
- `python3 scripts/gen-gate-docs.py --self-test` → `SELF-TEST PASS — 112 controls run` (unchanged — no gen-gate-docs.py gate control was added).
- `python3 scripts/gen-gate-docs.py --check` → exit 0, `harvested 22/22 expected script-backed entries`.
- `/usr/bin/grep -n "^## recurrence-reading" docs/conformance-baseline.md` → `158:## recurrence-reading`.
- `/usr/bin/grep -c "recurrence_reading" docs/data/conformance.json` → `1`.
- `sh .githooks/pre-commit` → exit 0 (all five pre-commit gates green).
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)` (battery total unchanged, no new gate registered — D-D holds).
- `.github/workflows/validation.yml` and `scripts/check-firewall-battery.sh` are byte-unchanged from before this plan (`git diff --stat` empty on both).
- `git diff --diff-filter=D --name-only HEAD~1 HEAD` → empty (no unexpected deletions).
- `git diff --name-only f189c99` (phase base) → exactly the plan's six `files_modified` entries, plus `tests/recurrence-reading-v9.1/{README.md,protocol.md}` and `scripts/check-firewall-battery.sh` from plan 27-01, plus the two prior plans' SUMMARY.md files, plus `docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md` (see Issues Encountered).

### `control_count` before/after (acceptance criterion)

- Before: `102`
- After: `110` (`python3 scripts/report-conformance.py --describe` → `control_count: 110`, equal to `len(_CONTROL_IDS)`)

### Digit-free section extraction (acceptance criterion)

Command:
```
awk '/^## recurrence-reading$/{flag=1; print; next} /^## /{if(flag) exit} flag' docs/conformance-baseline.md > /tmp/recurrence-section.txt
sed 's#tests/recurrence-reading-v9\.1##g' /tmp/recurrence-section.txt | grep -o '[0-9]' | sort -u
```
Output: (empty — no digits found outside the frozen directory path).

### Ledger readings before/after (acceptance criterion)

- `literal_scan_ledger_max` / `_DEFERRED_LITERAL_HITS`: `180 / 180` before, `180 / 180` after (unmoved).
- `containment_ledger_max` / `_DEFERRED_CONTAINMENT_HITS`: `20 / 20` before, `20 / 20` after (unmoved).
- No coincidental corroboration occurred (the value that did move, `literal_scan_nonmodule_docstring_hits` 398 -> 401, is not a ledgered key and matches no frozen-historical figure on any page checked).

### Non-vacuity transcripts for the 8 new controls (each induced-failure, then restored-and-passing)

1. **recurrence-support-floor** — with `MIN_RECURRENCE_SUPPORT_FILES` monkeypatched to `0` (floor disabled): `AssertionError: discover_artifacts did not raise when protocol.md is missing`. Restored: passes.
2. **recurrence-totals-line-must-match-rows** — with `_read_recurrence_records` monkeypatched to skip the totals comparison: `AssertionError: mismatched totals line did not raise`. Restored: passes.
3. **recurrence-closed-column-vocabulary** — with `_RECURRENCE_VALID_TIERS`/`_RECURRENCE_VALID_FENCE_CLASSES` widened to admit the bad values: `AssertionError: out-of-vocabulary tier did not raise`. Restored: passes.
4. **recurrence-absent-record-emits-no-digit** — with `_render_recurrence_reading_section` monkeypatched to append a stray digit-bearing line: assertion fails on the leaked digit. Restored: passes.
5. **recurrence-arms-never-summed** — with the renderer monkeypatched to append a "Combined total: N sites" line: assertion fails (`"7 sites" not in rendered` trips). Restored: passes.
6. **recurrence-readers-never-averaged** — with the renderer monkeypatched to append an "Average across readers: N sites" line: assertion fails (`"4 sites" not in rendered` trips). Restored: passes.
7. **recurrence-timing-delta-joins-on-content** — with `compute_recurrence_headline` monkeypatched to a naive full-`file:line` join: the shifted-line site is misclassified as `pre_only`/`post_only` instead of `both`; assertion fails. Restored: passes.
8. **recurrence-no-exit-code-conditioned-on-count** — with `_recurrence_exit_conditioning_violations` monkeypatched to always return `[]`: `AssertionError: control failed to catch its own synthetic violation`. Restored: passes.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- The recurrence-reading surface exists, is inert (all six record files legitimately absent), and reproduces byte-for-byte under `--check`.
- Plan 27-04 can now author `tests/recurrence-reading-v9.1/pre-arm-*.md` and expect this plan's reader/render/headline code to pick them up without further code changes — `build_recurrence_row`/`compute_recurrence_headline`/`_render_recurrence_reading_section` were exercised against synthetic present-row fixtures in this plan's own control non-vacuity proofs (see transcripts above), not only the all-absent state.
- No blockers.

---
*Phase: 27-ship-v9-1-0*
*Completed: 2026-09-11*
