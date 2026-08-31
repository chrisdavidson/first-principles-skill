---
phase: 06-integration-and-ship
plan: 02
subsystem: testing
tags: [traceability, matrix, provenance, self-test, docs]

# Dependency graph
requires:
  - phase: 06-integration-and-ship (plan 01)
    provides: scripts/check-provenance.py (PROV-GUARD), CI/battery registration
provides:
  - "_rows_v824() registering the 15 v8.24 requirements as matrix rows (14 reproducible + 1 audit-only)"
  - "V824-ROWS self-test sentinel wired into check-traceability.py's self_test() dispatch"
  - "Regenerated docs/requirements-matrix.md and docs/data/matrix.json (237 -> 252 rows)"
  - "docs/requirements-traceability.md headline, history row 9, and every ungated prose tally brought to the post-phase truth"
  - "docs/requirements-traceability.md PROV-GUARD addendum stating what the gate asserts and its four documented limits"
affects: [06-03, 06-04, 06-05]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Milestone matrix-row registration follows the _rows_vNNN() + _self_test_vNNN_rows_sentinel() pair, tier-partition pinned by ID not by count (V818-ROWS precedent)"

key-files:
  created: []
  modified:
    - scripts/check-traceability.py
    - docs/requirements-matrix.md
    - docs/data/matrix.json
    - docs/requirements-traceability.md

key-decisions:
  - "All 14 reproducible v8.24 rows are Test-Network (departs from 06-RESEARCH.md's Open Questions item 1, which recommended CAP-*/PROV-* -> Methodology): none of the 15 requirements change agent methodology prose, they are verification apparatus or release bookkeeping"
  - "VAL-04 is Methodology + audit-only, following the SHIP-04/SHIP-05 carve-out so _SEVERITY_LABEL reads MEDIUM rather than HIGH"
  - "GATE-02's artifact_link points at scripts/check-firewall-battery.sh, not .github/workflows/validation.yml, since no offline gate re-reads the CI YAML"

patterns-established:
  - "V824-ROWS sentinel: exactly-15 drift guard, bare_id set lock, tier partition pinned by ID, deep-resolve over reproducible rows only, GATE-03 positive counter-check, milestone/key lock, capability lock -- mirrors V818-ROWS's (a)-(g) shape"

requirements-completed: [VAL-04]

# Metrics
duration: ~20min
completed: 2026-08-31
---

# Phase 06 Plan 02: Register the v8.24 milestone as traceability-matrix rows Summary

**Registered the 15 v8.24 requirements as matrix rows (14 reproducible + 1 audit-only), locked them with a V824-ROWS self-test sentinel, regenerated both tracked artifacts (237 -> 252 rows), and brought every count in `docs/requirements-traceability.md` to the post-phase truth, including a new PROV-GUARD addendum documenting what the gate asserts and does not.**

## Performance

- **Duration:** ~20 min
- **Tasks:** 2/2 completed
- **Files modified:** 4 (`scripts/check-traceability.py`, `docs/requirements-matrix.md`, `docs/data/matrix.json`, `docs/requirements-traceability.md`)

## Accomplishments

- `_rows_v824()` added to `scripts/check-traceability.py`, wired into `build_matrix_rows()` as inclusion path (f), registering CAP-01..03, PROV-01..05, GATE-01..03, VAL-01..04 as milestone-qualified `v8.24/<bare_id>` rows.
- `_self_test_v824_rows_sentinel()` added and registered in `self_test()`'s dispatch list (between V818-ROWS and HEADLINE-LOCK), mirroring V818-ROWS's (a)-(g) assertions: exactly 15 rows, canonical bare_id set, tier partition pinned by ID (`{"VAL-04"}` audit-only), deep-resolved artifact_links over the 14 reproducible rows, a GATE-03 positive counter-check, milestone/key lock, and capability lock.
- Both tracked artifacts regenerated via `emit`: `docs/requirements-matrix.md` and `docs/data/matrix.json` now hold 252 rows, byte-identical to `render_matrix_markdown()`/`emit_matrix()` output.
- Every count in `docs/requirements-traceability.md` updated to the post-phase truth: headline `161 reproducible / 91 audit-only / 0 gap / 252 total`, the `252-row` matrix reference, `91 requirements are validated`, `moved seven times`, headline-history row 9, `**91 audit-only rows**`, `MEDIUM audit-only items (53,` / `91-row audit-only total`, `Generated matrix (252 rows)`, and one appended sentence on the "Pre-existing drift corrected" blockquote (left byte-intact otherwise).
- A dated PROV-GUARD addendum appended to the Status section recording the gate id, its CI-job/battery registration, the verbatim live result (`7/7 sources matched, 35/35 literals located`), all four documented "does not assert" limits, and why VAL-04 is the milestone's one audit-only row.

## Task Commits

Each task was committed atomically:

1. **Task 1: Register the 15 v8.24 rows, lock them with V824-ROWS, regenerate both artifacts, and reconcile every count** - `1d0000e` (feat)
2. **Task 2: Record PROV-GUARD and its four stated limits in docs/requirements-traceability.md** - `3d3f146` (docs)

_Note: this plan's git-tracked commits above are the two task commits; the SUMMARY/metadata commit follows separately per the parallel-executor protocol._

## Files Created/Modified

- `scripts/check-traceability.py` - Added `_rows_v824()`, wired it into `build_matrix_rows()` (inclusion path f), added `_self_test_v824_rows_sentinel()`, registered it in `self_test()`'s dispatch and docstring
- `docs/requirements-matrix.md` - Regenerated, 237 -> 252 rows
- `docs/data/matrix.json` - Regenerated, 237 -> 252 rows
- `docs/requirements-traceability.md` - Headline/history/prose counts reconciled to 252 rows; PROV-GUARD addendum appended

## Decisions Made

- Capability assignment departs from `06-RESEARCH.md`'s "Open Questions" item 1 recommendation: all 14 reproducible v8.24 rows are Test-Network (not Methodology), because none of the 15 requirements change agent methodology prose — they are properties of gate scripts and a test fixture. This is documented explicitly in `_rows_v824()`'s docstring.
- VAL-04 is Methodology + audit-only (SHIP-04/SHIP-05 carve-out), giving it MEDIUM severity under `_SEVERITY_LABEL` rather than HIGH, matching the project's stated judgment that a missing docs record is not a verification-system gap.
- GATE-02's `artifact_link` is `scripts/check-firewall-battery.sh` rather than `.github/workflows/validation.yml`, stated as an explicit honesty note in the docstring: no offline gate re-reads the CI YAML file itself.

## Deviations from Plan

None - plan executed exactly as written. The plan's own `<verify>` automated block used `T=$(mktemp -d)` (a `/tmp` path) to re-run `emit` for a byte-diff check; `check-traceability.py`'s pre-existing `_resolve_confined_output()` guard (T-82-01) rejects output paths outside `.planning/` or `docs/`, so that literal command as written fails with exit 2 before reaching the byte-diff. This is a pre-existing security guard unrelated to this plan's changes (not modified here — `git diff` confirms `_resolve_confined_output`/`ALLOWED_OUTPUT_ROOTS` are untouched). The equivalent verification was run instead using a gitignored `.planning/tmp-verify/` scratch directory (removed after use), which is allowed by the guard and produced the same result: `diff -q` against both tracked artifacts exits 0. All other verify-block assertions (self-test PASS, the Python row/count assertions, `docs/requirements-traceability.md` literal checks, and the no-`MatrixRow(` Pitfall-4 check on the sentinel body) ran and passed exactly as written.

## Issues Encountered

- `bash scripts/check-firewall-battery.sh` reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 21/22 passed)` — the sole blocker is `[PREREQ] VAL-03`, because this worktree has no `.venv` and the system `python3` cannot `import pytest`. This is the documented BLOCKED outcome (distinct from RED) described in `CLAUDE.md`'s battery section, is an environment-setup gap pre-existing in this worktree, and is out of scope for this plan's `<files>` (`scripts/check-traceability.py`, the two matrix artifacts, and `docs/requirements-traceability.md`) — installing pytest is excluded from Rule 3 auto-fix (package-manager installs require a checkpoint, and this package is a well-known, already-referenced dev dependency, not a new/unverified one, so no checkpoint was raised; it is simply noted here as unresolved). TRACE-03 itself (this plan's own gate) reports PASS within the battery run. All other 21 registered gates in the battery passed.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `docs/requirements-traceability.md`, `docs/requirements-matrix.md`, and `docs/data/matrix.json` are all consistent with `build_matrix_rows()` and ready for any later phase that reads the traceability surface.
- The `PROV-GUARD` addendum is in place, closing D-14's third surface (CLAUDE.md and `check-provenance.py`'s own docstring being the other two, both handled in a separate plan).
- No blockers for 06-03/06-04/06-05.

---
*Phase: 06-integration-and-ship*
*Completed: 2026-08-31*
