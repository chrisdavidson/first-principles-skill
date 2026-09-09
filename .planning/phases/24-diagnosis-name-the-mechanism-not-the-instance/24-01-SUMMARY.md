---
phase: 24-diagnosis-name-the-mechanism-not-the-instance
plan: 01
subsystem: apparatus
tags: [python, ast, regex, importlib, census, containment]

# Dependency graph
requires: []
provides:
  - "scripts/census-delta-vectors.py — unregistered, stdlib-only reporter enumerating every N -> M delta vector in narrative prose outside a generated fence"
  - "Four captured rung enumerations (md-narrow=59, md-all=598, py-docstrings=0, shared-text=1) for plan 24-03's hand-adjudication pass"
  - "Mechanical proof the census tool is registered nowhere (battery, CI workflow, both pre-commit hooks)"
affects: ["24-02", "24-03"]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "importlib.util.spec_from_file_location + sys.modules registration to load a sibling gate script and select live regex objects by exact .pattern match, rather than retyping a grammar (matches check-provenance.py / check-conf-gate.py / check-step0-live.py precedent)"
    - "Pre-registered widening ladder recorded in the tool's own module docstring before any search runs (D-12)"

key-files:
  created: [scripts/census-delta-vectors.py]
  modified: [CLAUDE.md, docs/ARCHITECTURE.md, docs/gates/CONF-SURFACE.md]

key-decisions:
  - "Census script committed under scripts/ (D-11's third option), following scripts/trace-tests-usage.py's standing 'manual tool, not a CI gate' shape"
  - "Regenerated CLAUDE.md/docs/ARCHITECTURE.md/docs/gates/CONF-SURFACE.md via gen-gate-docs.py --write after the new file joined CONF-13's scripts/ population — a mechanical population-count sync, not a ledger change (_DEFERRED_LEDGER_MAX stayed 181, literal_scan_non_exempt stayed 0)"

patterns-established:
  - "Pattern: fidelity-floor pattern selection — select delta-vector regexes from the live _CITATION_SHAPE_RES tuple by exact .pattern string match, exit 1 naming the missing pattern rather than falling back to a locally-defined regex if the source tuple moves"

requirements-completed: [PROSE-02]

# Metrics
duration: ~12min
completed: 2026-09-09
---

# Phase 24 Plan 01: Sibling-Site Census Reporter Summary

**Built `scripts/census-delta-vectors.py`, an unregistered reporter that enumerates every `N → M` delta vector in narrative prose by selecting its two patterns live from `_CITATION_SHAPE_RES`, and ran its four pre-registered widening-ladder rungs (59 / 598 / 0 / 1 vectors) to feed plan 24-03's hand adjudication.**

## Performance

- **Duration:** ~12 min
- **Started:** 2026-09-09T12:34:18Z (approximate, per STATE.md's phase-execution-start timestamp; this agent did not capture a precise start-of-plan timestamp)
- **Completed:** 2026-09-09T12:46:38Z
- **Tasks:** 2 (both auto)
- **Files modified:** 4 (1 created, 3 regenerated)

## Accomplishments
- `scripts/census-delta-vectors.py` exists, loads `scripts/gen-gate-docs.py` via `importlib` and selects the arrow/English delta-vector patterns by exact `.pattern` match against `_CITATION_SHAPE_RES`, refusing to run (exit 1, named error) if either pattern is no longer a live member of that tuple — verified by mutation on a disposable `rsync --exclude .git` scratch copy.
- All four pre-registered rungs of the widening ladder ran and were captured to the session scratchpad for plan 24-03's adjudication, each with its command, measurement timestamp, and exit code recorded: `md-narrow` (59 vectors), `md-all` (598 vectors), `py-docstrings` (0 vectors, published honestly per D-12), `shared-text` (1 vector).
- Mechanically proved the tool is registered in `scripts/check-firewall-battery.sh`, `.github/workflows/validation.yml`, `.githooks/pre-commit` and `scripts/git-hooks/pre-commit` exactly nowhere (four zero-hit greps).
- `python3 scripts/gen-gate-docs.py --check` exits 0 and `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (26/26)`, both read live after the commit — the battery total is unchanged from its value before this plan ran (also 26; confirmed by grepping `CLAUDE.md`'s generated CI-gate arithmetic sentence, unmoved).
- Committed the script through all five pre-commit gates (`sh .githooks/pre-commit` exits 0 with the script staged).

## Task Commits

Each task was committed atomically. Tasks 1 and 2 shared one file (`scripts/census-delta-vectors.py`); per the plan's own text ("Commit the script" appears only in Task 2's action, after the four-rung run and the non-registration proofs), the single commit for both tasks landed at the end of Task 2:

1. **Task 1: Write the unregistered delta-vector census reporter** — verified inline (`--help`, `--rung md-narrow`, all module-docstring/grep acceptance criteria, the fidelity-floor mutation test on a scratch copy) but not committed standalone, since Task 2 owns the commit for this same file.
2. **Task 2: Run all four rungs, capture the enumerations, and prove non-registration** — `fdd10fa` (feat)

**Plan metadata:** captured in this SUMMARY commit (docs: complete plan)

## Files Created/Modified
- `scripts/census-delta-vectors.py` — new. Stdlib-only, `argparse` + `main() -> int` reporter; `--rung {md-narrow,md-all,py-docstrings,shared-text,all}` (default `all`), `--format {markdown,tsv}` (default `markdown`); no offline gate-check flag, no file-mutating flag, mutates nothing it reads.
- `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/gates/CONF-SURFACE.md` — regenerated via `scripts/gen-gate-docs.py --write` because the new `.py` file under `scripts/` joined CONF-13's live-derived `_py_docstring_scan_scripts()` population (`literal_scan_py_population` 29→30, `literal_scan_surfaces`/`registered_surfaces`/`checked_files` each +1). No ledger entry changed (`_DEFERRED_LEDGER_MAX` stayed 181, `literal_scan_non_exempt` stayed 0 both before and after) and no battery/CI gate count moved.

## Decisions Made
- Followed D-11's third disposition option (committed, unregistered `scripts/` tool) rather than a scratchpad throwaway or a `.planning/`-evidence artifact, matching the plan's explicit `scripts/trace-tests-usage.py` analog.
- Reworded two docstring sentences ("No `--self-test`. No `--write`.") to avoid literally containing the substrings `self-test`/`--write`, which the plan's own acceptance-criterion grep (`grep -c "self-test\|--write"` must return 0) would otherwise have matched against the docstring's own disclosure of that fact — resolved by describing the absence without naming the flag strings verbatim.
- Reworded "Exit status is 0" / "returns 1" to "Exit status is clean" / "exits non-zero" to satisfy the no-digit-literal requirement on the module docstring (CONF-13's own scanner would otherwise flag these as hand-typed count literals).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Ran `gen-gate-docs.py --write` to resync three generated surfaces before the pre-commit gate would pass**
- **Found during:** Task 2 (after landing the script, `python3 scripts/gen-gate-docs.py --check` reported DRIFT on `CLAUDE.md`, `docs/ARCHITECTURE.md` and `docs/gates/CONF-SURFACE.md` — their generated Facts fences still showed the pre-census `registered_surfaces`/`checked_files`/`literal_scan_*` population counts)
- **Issue:** The plan's own `<action>` text anticipated this exact hazard ("this file lands in `_py_docstring_scan_scripts()`'s live glob, so its module docstring is scanned by CONF-13 at commit time") but only names the ledger/`_DEFERRED_LEDGER_MAX` path as out-of-scope; it does not separately name the population-count regeneration path, which is a distinct, in-scope mechanical step (the same `gen-gate-docs.py --write && re-gate` step Phase 21/22 plans routinely end with).
- **Fix:** Ran `python3 scripts/gen-gate-docs.py --write` (regenerated 34 files; 31 of them — the unaffected `docs/gates/*.md` thin pages — round-tripped byte-identical and register no diff, leaving 3 files with real content changes: `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/gates/CONF-SURFACE.md`). Confirmed `_DEFERRED_LEDGER_MAX` unchanged at 181 and `literal_scan_non_exempt` unchanged at 0 both before and after — this was a population-count sync, not a ledger change or a fix to a defect.
- **Files modified:** `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/gates/CONF-SURFACE.md`
- **Verification:** `python3 scripts/gen-gate-docs.py --check` exits 0 after the write; `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (26/26)`; battery-total arithmetic sentence in `CLAUDE.md` unchanged (still `23 + 1 + 2 = 26`).
- **Committed in:** `fdd10fa` (Task 2 commit)

**2. [Rule 3 - Blocking] Ran `uv sync` to create a pytest-capable `.venv`**
- **Found during:** Task 2's first `bash scripts/check-firewall-battery.sh` run, which reported `FIREWALL: BLOCKED (25/26)` because VAL-03's third leg needs a pytest-capable interpreter and neither `.venv/bin/python3` nor `python3` could import pytest — an unmet external prerequisite (CLAUDE.md's documented BLOCKED/exit-2 outcome, distinct from a genuine gate failure), pre-existing in this worktree and unrelated to this plan's file changes.
- **Issue:** The plan's acceptance criteria require reading a live `FIREWALL: GREEN` verdict, which is not obtainable while VAL-03 is BLOCKED.
- **Fix:** Ran `uv sync` (creates `.venv`, gitignored, installs pytest and five other packages per `pyproject.toml`/`uv.lock`, per CLAUDE.md's own documented remedy). No product code changed.
- **Files modified:** none tracked (`.venv/` is gitignored).
- **Verification:** Re-ran the battery; VAL-03 now reports `[PASS]`; full battery reports `FIREWALL: GREEN (26/26)`.
- **Committed in:** not applicable (no tracked files changed)

---

**Total deviations:** 2 auto-fixed (both Rule 3 - Blocking)
**Impact on plan:** Both were mechanical prerequisites for reading the plan's own required live verdicts (a clean `gen-gate-docs.py --check` and a `FIREWALL: GREEN` reading); neither touched the census tool's logic, its non-registration, or any ledger/battery/CI count. No scope creep.

## Issues Encountered
None beyond the two auto-fixed items above.

## Assumption Drift (advisory)

- **Planned:** the plan's `<action>` text implies landing the script and proving non-registration should be sufficient for `gen-gate-docs.py --check` to "still exit 0" with no further step named.
- **Actual:** an intermediate `--write` regeneration was required first, because CONF-13's `.py` population is live-derived and any new file under `scripts/` moves several generated population counts even when it introduces zero non-exempt literals.
- **Why it matters:** a reader following the plan's action text literally might expect `--check` to pass immediately after `git add` with no intervening `--write`; it does not, and the reason (population-count drift, not a ledger or literal defect) is worth naming explicitly rather than leaving as an unexplained extra command in the task's own read of its `<action>`.

## User Setup Required
None — no external service configuration required.

## Next Phase Readiness
- The four captured rung enumerations (`census-md-narrow.md`, `census-md-all.md`, `census-py-docstrings.md`, `census-shared-text.md`, each with its command, measurement timestamp and exit code) are in the session scratchpad, ready for plan 24-03's hand-adjudication pass per D-10.
- `scripts/census-delta-vectors.py` is available for any later plan (this phase or Phase 25) to re-run against the live tree; it remains unregistered by design and must stay that way per D-D/D-11 unless a later phase explicitly decides otherwise.
- No blockers for 24-02 or 24-03.

---
*Phase: 24-diagnosis-name-the-mechanism-not-the-instance*
*Completed: 2026-09-09*

## Self-Check: PASSED

- FOUND: `scripts/census-delta-vectors.py`
- FOUND: commit `fdd10fa`
- FOUND: `.planning/phases/24-diagnosis-name-the-mechanism-not-the-instance/24-01-SUMMARY.md`
