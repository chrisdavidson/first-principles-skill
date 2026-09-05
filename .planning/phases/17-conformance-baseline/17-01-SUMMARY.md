---
phase: 17-conformance-baseline
plan: 01
subsystem: testing
tags: [python, measurement-instrument, quality-harness, conformance]

# Dependency graph
requires:
  - phase: null
    provides: "CONTRACT-06-frozen scripts/check-quality-harness.py (detect_defects, SectionResolutionError, _render_example_chain_blocks, _chain_block_well_formed, _DEFECT_RECORD_FIELDS) -- imported read-only"
provides:
  - "scripts/report-conformance.py: discover_artifacts / build_row / build_rows / pair_agreement measurement core"
  - "render_markdown / render_json / generate_all / cmd_write / cmd_check drift-checked dual-surface renderer"
  - "--self-test with 14 named, floored anti-vacuity controls"
affects: [17-02-generate-and-commit-baseline, 17-03-pre-commit-wiring, 18-conformance-remediation]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "importlib.util harness import with sys.modules pre-registration (copied from check-provenance.py)"
    - "one row-builder, two renderers (render_markdown/render_json share one build_rows()/pair_agreement() call)"
    - "in-memory-regenerate-then-diff --check (copied from sync-content.py's cmd_check shape)"
    - "hardcoded MEASUREMENT_DATE module constant reconciling dated output with byte-for-byte --check reproduction (new pattern, no prior precedent in this repo)"
    - "second, independently-transcribed _CONTROL_IDS tuple floors _CONTROLS by equality (SCAN-GUARD's _BRANCH_ROSTER_LOCK shape)"

key-files:
  created:
    - scripts/report-conformance.py
  modified: []

key-decisions:
  - "Provenance columns render 'n/a' unconditionally, even on SectionResolutionError partial rows -- the twelve measured schema fields render 'unreadable' in that case, but the nine provenance columns stay 'n/a' because no .jsonl capture exists regardless of whether detect_defects ran (sharpens the plan's 'every OTHER field' wording to satisfy the every-row provenance-n/a acceptance criterion)"
  - "cmd_check()'s drift comparison was factored into a path-agnostic _diff_against_disk() helper so --self-test's check-detects-drift control could exercise real drift detection against a tempdir fixture without ever writing into docs/, keeping cmd_check() itself hardcoded to the real module-constant paths per settled decision (d)"

requirements-completed: [CONF-01, CONF-02]

# Metrics
duration: 45min
completed: 2026-09-05
---

# Phase 17 Plan 01: report-conformance.py Measurement Core Summary

**Built `scripts/report-conformance.py` -- a stdlib-only measurement instrument that imports the CONTRACT-06-frozen quality harness read-only, discovers 29 artifacts under three named count floors, computes a 15-field source-vs-twin agreement reading, and renders two deterministic, drift-checked surfaces, all reproducing every figure in `17-CONTEXT.md` exactly.**

## Performance

- **Duration:** ~45 min
- **Started:** 2026-09-04 (session), executed 2026-09-05
- **Completed:** 2026-09-05T02:15:14Z
- **Tasks:** 3/3 completed
- **Files modified:** 1 (`scripts/report-conformance.py`, created)

## Accomplishments
- `discover_artifacts()` globs the two example directories plus the contract surface under three named count floors (D-02); `build_row()`/`build_rows()` implement D-03's partial-row reporting for the four artifacts `_slice_sections` rejects; `pair_agreement()` computes D-04's 15-field source-vs-twin comparison.
- `render_markdown()`/`render_json()` share one row set so the two surfaces cannot disagree; `cmd_check()` regenerates in memory and diffs against disk with a pass1/pass2 non-determinism guard, matching `sync-content.py`'s shape.
- `--self-test` carries 14 named, floored anti-vacuity controls; all four required neutralizations were run on an `rsync --exclude .git` scratch copy and observed to fail by the expected control id(s).
- `bash scripts/check-firewall-battery.sh` still reports `FIREWALL: GREEN (24/24)` -- the battery is unmoved, as D-06 requires.

## Task Commits

Each task was committed atomically:

1. **Task 1: Measurement core -- harness import, glob discovery with named count floors, per-artifact rows** - `ace8277` (feat)
2. **Task 2: Renderers, MEASUREMENT_DATE, write path, and --check drift detection** - `0aae632` (feat)
3. **Task 3: Inline --self-test with named anti-vacuity controls** - `9d8f079` (test)

**Plan metadata:** committed alongside this Summary.

## Files Created/Modified
- `scripts/report-conformance.py` (932 lines) - the whole Phase 17 measurement instrument: harness import, discovery/count-floor enforcement, partial-row builder, agreement computation, dual renderers, `--check` drift detection, and inline `--self-test`.

## Settled Discretion Items, As Implemented

The plan's `<settled_decisions>` (a)-(e) were implemented exactly as written, with one sharpening noted below:

- **(a) Report shape:** all 22 `_DEFECT_RECORD_FIELDS` columns are emitted on both rendered surfaces. The nine provenance columns render the literal `"n/a"` on every one of the 29 rows -- including the four `SectionResolutionError` partial rows, where the plan's literal "every OTHER field -> 'unreadable'" wording is sharpened: only the twelve *measured* schema fields (indices 1-12) render `"unreadable"`; the nine provenance fields (indices 13-21) stay `"n/a"` unconditionally, because no `.jsonl` capture exists for an artifact regardless of whether `detect_defects` ran. This sharpening is what makes the acceptance criterion `all(r["provenance_labels"]=="n/a" for r in rows)` hold across all 29 rows, including the 4 unreadable ones.
- **(b) Snapshot, not append-only:** `render_markdown`/`render_json` fully overwrite both surfaces on every `cmd_write()` call; no history is retained inside the artifact itself.
- **(c) `MEASUREMENT_DATE = "2026-09-04"`** is a hardcoded module constant, documented in the module docstring as a new pattern with no existing precedent in this repo (`docs/requirements-matrix.md` carries no date at all).
- **(d) CLI surface:** `MD_PATH`/`JSON_PATH` are hardcoded module constants; no `--md-output`/`--json-output` override exists. The CLI is exactly `--check` / `--self-test` / bare-run (write).
- **(e) D-05 reconciliation note:** lives in the rendered `docs/conformance-baseline.md` itself (a `## Two chain-block censuses (D-05)` section), with a one-line pointer in the module docstring.

## Count-Floor Failure Message Literals (for later plans/verifier to grep)

- Shared-examples short: `report-conformance: COUNT FLOOR FAIL — expected >= 14 files matching shared/examples/*.md, found 13`
- Twin short: `report-conformance: COUNT FLOOR FAIL — expected >= 14 files matching first-principles/agents/references/examples/*.md, found 13`
- Contract surface missing (named path, never a bare zero): `report-conformance: COUNT FLOOR FAIL — expected shared/spine/references/output-template.md to exist at <path>, found missing`
- `--check` remediation line (verbatim): `Run: python3 scripts/report-conformance.py && git add -u`

## Registered Control-Id Roster (14, `--self-test`)

`floor-shared-short`, `floor-twin-short`, `floor-contract-missing`, `floor-glob-empty`, `floor-passes-at-minimum`, `partial-row-records-heading-census`, `partial-row-not-dropped`, `agreement-field-scope`, `agreement-detects-measured-divergence`, `agreement-vacuity-guard`, `agreement-unpaired-is-divergence`, `render-determinism`, `render-provenance-sentinel`, `check-detects-drift`. Floored by equality against a second, independently-transcribed `_CONTROL_IDS` tuple (SCAN-GUARD's `_BRANCH_ROSTER_LOCK` shape).

## Observed Neutralization Output (all four run on an `rsync --exclude .git` scratch copy, never the real tree; `git status --porcelain` confirmed empty on the real tree before and after each)

1. **Deleting the `expected >= {MIN_SHARED_EXAMPLES}` comparison from `discover_artifacts`:**
   ```
   report-conformance: SELF-TEST FAIL [floor-shared-short] — discover_artifacts did not raise on a 13-file shared glob
   report-conformance: SELF-TEST FAIL [floor-glob-empty] — report-conformance: COUNT FLOOR FAIL — expected >= 14 files matching first-principles/agents/references/examples/*.md, found 0
   report-conformance: COUNT FLOOR FAIL — expected shared/spine/references/output-template.md to exist at <tmp>/shared/spine/references/output-template.md, found missing
   ```
   Exit 1, naming both `floor-shared-short` AND `floor-glob-empty` as required.

2. **Widening `AGREEMENT_FIELDS` to `_DEFECT_RECORD_FIELDS + REPORT_FIELDS`:**
   ```
   report-conformance: SELF-TEST FAIL [agreement-field-scope] — 25
   report-conformance: SELF-TEST FAIL [agreement-vacuity-guard] — (0, [('synth', ['provenance_labels'])])
   ```
   Exit 1, naming `agreement-field-scope` as required (plus a bonus catch on `agreement-vacuity-guard`, since a provenance-only difference now counts as a real divergence once the field is in scope).

3. **Making `build_row` re-raise `SectionResolutionError` instead of emitting a partial row:**
   ```
   report-conformance: SELF-TEST FAIL [partial-row-records-heading-census] — SectionResolutionError: expected sections 1-6 to resolve in order, resolved []
   report-conformance: SELF-TEST FAIL [partial-row-not-dropped] — SectionResolutionError: expected sections 1-6 to resolve in order, resolved []
   ```
   Exit 1, naming both `partial-row-records-heading-census` AND `partial-row-not-dropped` as required.

4. **Removing one control id's registration from `_CONTROLS` (its call site) while leaving it in `_CONTROL_IDS`:**
   ```
   report-conformance: SELF-TEST FAIL [coverage-floor] — registered/executed control-id mismatch: missing=['floor-shared-short'] extra=[]
   ```
   Exit 1, naming the coverage floor and the missing id as required.

All four scratch copies were deleted after each neutralization run; `git status --porcelain` on the real working tree was confirmed empty both before the mutation-testing session began and after it completed (the only change in the real tree across the whole plan is `scripts/report-conformance.py` itself, task-by-task).

## Verification (observed, not assumed)

- `python3 scripts/report-conformance.py --self-test` — **exit 0**, `report-conformance: SELF-TEST PASS — 14 controls run`.
- `python3 scripts/report-conformance.py --check` — **exit 1** (artifacts not committed yet; that lands in plan 17-02), with two named `DRIFT:` lines (`docs/conformance-baseline.md`, `docs/data/conformance.json`) and the literal remediation line `Run: python3 scripts/report-conformance.py && git add -u`.
- `git diff --quiet -- scripts/check-quality-harness.py shared/ first-principles/` — **exit 0** after every task and after the mutation-testing session (frozen/generated trees untouched throughout).
- `bash scripts/check-firewall-battery.sh` — **`FIREWALL: GREEN (24/24)`**, battery count unmoved (required `uv sync` first to provision a pytest-capable `.venv` for VAL-03's third leg in this sandbox; `.venv/` is gitignored and untouched by the plan's own diff).
- Row-level figures independently re-derived via `build_rows(REPO_ROOT)` and confirmed to match `17-CONTEXT.md` § Specific Ideas exactly: 29 rows (14/14/1 surface split); 4 unreadable shared-examples rows by name (`composed-inversion-second-order`, `decompose-irreducibility`, `estimate-fermi`, `theoretical-limit-carnot`); `composed-inversion-second-order` carries `heading_chain_blocks=1`, `heading_malformed_blocks=0`, `conclusion_claims="unreadable"`; all 29 rows read `provenance_labels=="n/a"` and `provenance_flag=="n/a"`; readable shared-examples sums are 58/56/69/69/10/7 (claims/untraced/verdict/nonconforming/chain_blocks/malformed); all-14 heading-swept sums are 28/19; contract surface reads 3/3/1/1/3/1; `pair_agreement` returns `(14, 14, [])`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed a missing `|` table-cell separator in four `render_markdown` headline rows**
- **Found during:** Task 2, first `--check` run
- **Issue:** The four headline-table row builders (`§6 conclusion claims`, `§2 verdict cells`, `§4 chain_blocks`, `### Conclusion heading-swept blocks`) concatenated the row label directly onto the first joined value with no intervening `| `, producing a 3-column row under a 4-column header (`Reading | shared-examples | generated-twin | contract-surface`).
- **Fix:** Inserted the missing `| ` between the label and the `" | ".join(...)` call in all four row builders.
- **Files modified:** `scripts/report-conformance.py`
- **Commit:** folded into `0aae632` (caught and fixed before that commit was made; no separate commit needed).

**2. [Rule 1 - Bug, clarification] Provenance columns stay `"n/a"` on partial (unreadable) rows, not `"unreadable"`**
- **Found during:** Task 1, running the acceptance-criteria check `all(r["provenance_labels"]=="n/a" for r in rows)`
- **Issue:** A literal reading of the plan's `<action>` text ("set every OTHER `_DEFECT_RECORD_FIELDS` entry to the string `'unreadable'`") would set the nine provenance columns to `"unreadable"` on the four `SectionResolutionError` rows, contradicting the plan's own acceptance criterion that every one of the 29 rows reads `provenance_labels == "n/a"`.
- **Fix:** `build_row`'s `except SectionResolutionError` branch checks `field in PROVENANCE_FIELDS` and keeps those nine fields `"n/a"` unconditionally; only the twelve measured schema fields (and `section_resolution` itself) become `"unreadable"`. This matches settled decision (a)'s framing that the nine provenance columns are `"n/a"` for *any* artifact with no `.jsonl` capture — true of all 29 artifacts regardless of readability.
- **Files modified:** `scripts/report-conformance.py`
- **Commit:** `ace8277` (implemented this way from the first commit; documented here as a deviation from a literal reading of the action text, not from the settled decisions or acceptance criteria, which this choice satisfies).

### Auth gates
None encountered.

## Known Stubs
None. The script is fully functional; `docs/conformance-baseline.md` / `docs/data/conformance.json` are intentionally NOT generated or committed by this plan (that is plan 17-02's scope, per the plan's own `<objective>`).

## Threat Flags
None. All three threat-register mitigations (T-17-02 hardcoded output paths, T-17-03 audit-only field exclusion, T-17-05 anti-vacuity floors) were implemented exactly as specified in the plan's `<threat_model>`; no new security-relevant surface was introduced beyond what that register already names.
