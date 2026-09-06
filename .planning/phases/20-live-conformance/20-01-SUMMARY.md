---
phase: 20-live-conformance
plan: 01
subsystem: test-fixtures
tags: [conformance, live-measurement, catalog, CONF-09, CONF-10]
dependency-graph:
  requires: []
  provides:
    - "tests/live-conformance-catalog.md (8-row run inventory, parses under _read_quality_catalog)"
    - "tests/live-conformance-v9.0/ (durable, unfrozen capture destination)"
    - "written decision record for D-20-A, D-20-B, D-20-C"
  affects:
    - "plan 20-02 (dispatch, reads this catalog via --probe --catalog)"
    - "plan 20-03 (fixture README, fills disposition: placeholders)"
    - "plan 20-04/20-05 (report-conformance.py's fifth surface and roster equality floor)"
    - "plan 20-06 (registers both paths in _FROZEN_PATHS after captures land)"
tech-stack:
  added: []
  patterns:
    - "one-row/N-row header-compatibility adapter catalog, following tests/quality-provenance-v8.24/catalog.md"
    - "decision record transcribed into the committed artifact itself, not left in planning docs only"
key-files:
  created:
    - tests/live-conformance-catalog.md
    - tests/live-conformance-v9.0/.gitkeep
  modified: []
decisions:
  - "D-20-A/D-20-B/D-20-C transcribed verbatim from 20-01-PLAN.md into the committed catalog file"
  - "Rendered the decision record's outcome classification and all structured facts as prose/bulleted lists rather than markdown pipe tables, because _read_quality_catalog treats every line starting with `|` as a table row and raises ValueError on the first one that isn't the exact `| ID | Prompt | Notes |` header"
metrics:
  duration: "~35 minutes"
  completed: "2026-09-06"
---

# Phase 20 Plan 01: Live Conformance Run Inventory Summary

Authored the 8-row `| ID | Prompt | Notes |` catalog that is both the prompt source for Phase
20's live `--probe` dispatches and the run inventory `report-conformance.py`'s roster floor will
read by equality, plus the phase's written decision record for D-20-A/D-20-B/D-20-C, landing the
decision before any capture or surface code exists.

## What Was Built

- **`tests/live-conformance-catalog.md`** — one new file, 158 lines. Prose header (`## Purpose`,
  `## Decision record`, `## Run command`, `## Provenance`) followed by exactly one markdown table
  with the literal header `| ID | Prompt | Notes |` and 8 data rows: `Q-P1`, `Q-P2`, `Q-P3`
  (copied byte-for-byte from `tests/quality-catalog-v8.7.md`), `PR-P1`, `PR-P2`, `PR-N1`, `PR-N2`
  (copied byte-for-byte from the `Prompt` column of `tests/premise-rejection-catalog.md`), and
  `PR-P1-R2` (PR-P1's prompt text repeated under a distinct id per D-02's within-body-variance /
  cross-body-longitudinal second run). Every row's `Notes` cell carries an origin sentence naming
  its source file and row id, followed by the literal marker `disposition: MISSING` — plan 20-03
  fills in the real disposition once each run's reading is known.
- **`tests/live-conformance-v9.0/.gitkeep`** — reserves the durable, in-repo capture destination
  before any live dispatch. Confirmed offline (no live run performed) that this path is not
  registered in `_FROZEN_PATHS`, so `is_frozen_destination` returns `False` and `--probe` will be
  able to write into it once plan 20-02 moves scratch captures in.

## Decision Record (transcribed into the committed file)

- **D-20-A** — "zero form defects" is CONF-GATE's exact four counts (`unreadable`,
  `heading_malformed_blocks`, `nonconforming_verdict_cells`, `silent_untraced_claims`), never the
  wider 13-column or 3-column alternatives. Denominator = all 8 catalog rows; a transport stub
  counts in the denominator but never the numerator; a stub's superseded capture is never
  deleted, only moved to `superseded/` and logged.
- **D-20-B** — the 8 runs measure HEAD, not the `v8.26.0` tag, because `git diff --name-only
  v8.26.0..HEAD -- shared/ first-principles/` returns only `shared/examples/*` and
  `first-principles/agents/references/examples/*` (28 files) — confirmed live in Task 2, matching
  the plan's expectation exactly, so no halt was needed. Fix discipline is file-only: agent
  output is never edited; a defect is filed against the artifact or the prescription and never
  closed by widening a detector.
- **D-20-C** — both `tests/live-conformance-v9.0/` and `tests/live-conformance-catalog.md` are
  registered in `_FROZEN_PATHS` only in plan 20-06, strictly after captures and catalog are
  committed. Confirmed today that neither path appears in `_FROZEN_PATHS` yet (still 20 entries).

## Verification Performed

- Task 1's automated verify command (`_read_quality_catalog` over the new file): exits 0, prints
  all 8 ids, `['Q-P1', 'Q-P2', 'Q-P3', 'PR-P1', 'PR-P2', 'PR-N1', 'PR-N2', 'PR-P1-R2']`.
- Byte-identity checks (extraction + comparison, not eyeballing): Q-P1/Q-P2/Q-P3 against
  `tests/quality-catalog-v8.7.md`, and PR-P1/PR-P2/PR-N1/PR-N2 against the `Prompt` column of
  `tests/premise-rejection-catalog.md`, plus PR-P1 == PR-P1-R2 — all confirmed identical by
  running the harness's own `_split_row`/`_read_quality_catalog` against both files and comparing
  extracted cell text.
- `git status --short tests/quality-catalog-v8.7.md tests/premise-rejection-catalog.md` — both
  empty; neither source file was modified.
- Literal-string presence, checked with `/usr/bin/grep -c` per literal (all counts >= 1):
  `silent_untraced_claims`, `heading_malformed_blocks`, `nonconforming_verdict_cells`,
  `runs attempted`, `classify_invocation_outcome`, `unreadable` (3 occurrences), and the sentence
  "The runs measure HEAD, not the `v8.26.0` tag" plus the fix-discipline sentence ending
  "widening a detector."
- Task 2's automated verify command: exits 0, prints `DEFAULT_PLUGIN_DIR` ending in
  `first-principles` (confirmed it resolves to the working tree, not the plugin cache) and
  confirms `is_frozen_destination` is `False` for the fixture path.
- `/usr/bin/grep -c 'live-conformance' scripts/check-firewall-battery.sh` → 0 (grep's own exit
  code 1 on a zero count is expected grep behavior, not a command failure).
- `/usr/bin/find tests/live-conformance-v9.0 -name "*.jsonl"` → empty; no live run was dispatched
  in this plan.
- `git rev-parse HEAD` → `41696efda42c29bb3f26f20143023411d9eb7ae6` (recorded as the body sha
  these 8 runs will measure).
- `python3 scripts/report-conformance.py --check` → `PASS — no drift`.
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (25/25)`. First run reported
  `FIREWALL: BLOCKED (1 prerequisite unmet; 24/25 passed)` because no pytest-capable interpreter
  existed in this worktree (`.venv` absent, `python3` had no pytest) — this is VAL-03's documented
  third outcome (SHIP-06, distinct from a genuine gate failure), not a defect in this plan's
  changes. Ran `uv sync` to create `.venv` (installs pytest 9.1.1 among 6 packages), which is
  gitignored and produced no untracked files, then re-ran the battery to GREEN 25/25.
- `python3 scripts/check-quality-harness.py --self-test` → exit 0, all sub-checks PASSED
  including `chain_detector_pin`, `conclusion_claims_pin`, and `slice_sections_pin` — the three
  CONTRACT-06 sha256 pins are byte-unchanged.
- `_FROZEN_PATHS` array in `scripts/check-firewall-battery.sh` — still 20 entries (counted
  programmatically), confirming no premature registration under D-20-C.
- `git status --short` at the end of the plan — empty; `git log --oneline -5` shows both task
  commits directly on top of the phase-start commit, nothing else pending.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking issue] Rendered the decision record's structured tables as prose/lists, not markdown pipe tables**
- **Found during:** Task 1, while drafting the `## Decision record` section
- **Issue:** `_read_quality_catalog` (scripts/check-quality-harness.py:228) treats every line in
  the file that starts with `|` as a table row unconditionally — it does not scope its check to
  a specific section. Any pipe-table anywhere else in the file (e.g. D-20-A's four-row outcome
  table, rendered as an actual markdown table) would hit a line that isn't in a recognized table
  yet and isn't the literal `| ID | Prompt | Notes |` header, raising `ValueError` before the
  real catalog table is ever reached.
- **Fix:** Rendered D-20-A's outcome classification as a four-item bulleted list (outcome →
  `.md` written? → denominator? → numerator?, one bullet per state) instead of a pipe table, and
  kept every other structured fact in the decision record as prose or bullets. Added an explicit
  "Parser note" paragraph at the top of the file stating this constraint so a future editor does
  not reintroduce a stray pipe table.
- **Verified:** Task 1's verify command (`_read_quality_catalog` parsing the file into exactly 8
  rows) passes; the file's only `|`-prefixed lines are the 10 lines of the actual Catalog table
  (header, separator, 8 data rows), confirmed by inspection during authoring.
- **Files modified:** `tests/live-conformance-catalog.md` (the only file this affects; no other
  file needed a corresponding change).
- **Commit:** `e63c0ba`

### Environment fix (not a code deviation)

**Battery prerequisite: created `.venv` via `uv sync`.** The worktree had no pytest-capable
interpreter, which is VAL-03's documented `BLOCKED` (not `RED`) outcome for an unmet external
prerequisite. Running `uv sync` (creates a gitignored `.venv`, installs `pytest==9.1.1` and five
dependencies) is the CLAUDE.md-documented remedy and is not a change to any tracked file — no
commit was needed for it, and `git status --short` was empty immediately afterward.

## Self-Check

- `tests/live-conformance-catalog.md` — FOUND
- `tests/live-conformance-v9.0/.gitkeep` — FOUND
- Commit `e63c0ba` — FOUND in `git log --oneline --all`
- Commit `309828e` — FOUND in `git log --oneline --all`

## Self-Check: PASSED
