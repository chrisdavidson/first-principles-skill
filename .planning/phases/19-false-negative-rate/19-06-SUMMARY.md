---
phase: 19-false-negative-rate
plan: 06
subsystem: testing
tags: [adversarial-corpus, conformance, quality-harness, anti-vacuity, report-conformance]

# Dependency graph
requires:
  - phase: 19-false-negative-rate (plans 01-05, waves 1-3)
    provides: "the 13-item corpus on disk, catalog.md, README.md, and report-conformance.py's
      fourth adversarial-corpus surface with the published 9-of-13 false-negative rate"
provides:
  - "scripts/report-conformance.py: four new falsifiability floors over the corpus reading
    (D-04 roster equality, CONF-08 disposition, CONF-07 population, D-03 per-item in-memory
    perturbation) wired into cmd_check(), each anti-vacuity controlled and neutralization-tested"
affects: [19-07]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Position-based (not string-count-based) structural mutation sites: check-conf-gate.py's
       D-08 arm needs exact-string-count == 1 for its one long needle; a 13-item corpus with
       naturally-repeating short citations ('(chain C2)' 2-3x per item) cannot use that test, so
       sites are located as absolute [start, end) character spans via the frozen detector's own
       section-slicing/cell/chain/citation vocabulary, then mutated by precise slice replacement."
    - "Per-family absence disposition decided and documented in the function's own docstring:
       families (a)/(c) are expected on every item and a missing site is a reported problem;
       family (b) is genuinely absent on 5/13 items (single-line chain form) and its absence is
       an expected condition, never reported on its own -- only a zero-families-fired item
       triggers D-03 NO MUTATION APPLIED."
    - "check-conf-gate.py's collect-then-report / call-site-census / BL-01 comment-stripping /
       BL-02 roster-lock shapes copied verbatim into report-conformance.py's own cmd_check()."

key-files:
  created: []
  modified:
    - scripts/report-conformance.py

key-decisions:
  - "Split the plan's two tasks into two atomic commits (7cfbb50 Task 1, f809311 Task 2) rather
     than landing them together -- unlike plan 19-05's forced coupling (the pre-commit
     conformance-drift gate), nothing here required the two tasks to land in one commit, since
     neither task touches a rendered artifact."
  - "Family (b)'s absence on 5/13 corpus items (single-line chain form, no separate arrow-led
     continuation line) is treated as an expected condition, not a reported problem -- decided
     and documented in _corpus_perturbation_problems' own docstring, matching the plan's
     'decide per family, state the decision' instruction."
  - "Mutation sites are located by absolute character position, not by CONF-GATE's exact-string-
     count-== 1 test -- verified live that no single corpus citation instance is textually unique
     (e.g. t01's '(chain C2)' occurs 3 times), so string-count uniqueness cannot be the 'site
     found' signal for this corpus the way it is for CONF-GATE's one long needle."

requirements-completed: [CONF-07, CONF-08]

# Metrics
duration: ~2h
completed: 2026-09-05
---

# Phase 19 Plan 06: Corpus Falsifiability Floors Summary

**Four new floors in `scripts/report-conformance.py` (D-04 roster equality, CONF-08 disposition,
CONF-07 population, D-03 per-item in-memory perturbation) make the published 9-of-13
false-negative rate falsifiable rather than merely reported, with all 25 new/changed controls
each neutralization-tested to fire on a real, isolated mutation.**

## Performance

- **Duration:** ~2h
- **Started:** 2026-09-05
- **Completed:** 2026-09-05T17:41:39Z
- **Tasks:** 2 completed
- **Files modified:** 1 (`scripts/report-conformance.py`)

## Accomplishments

- `_corpus_roster_problems` — D-04 equality floor (never subset) between `catalog.md`'s `File`
  stems and the discovered `adversarial-corpus` stem set, folding in `parse_corpus_catalog`'s own
  parse problems.
- `_corpus_disposition_problems` — CONF-08's zero-silent-passes clause made mechanical: every
  fully-clean corpus item must carry a disposition beginning `fix` / `accept-with-reason` /
  `defer-with-owner`.
- `_corpus_population_problems` — per-item `conclusion_claims >= 1` / `chain_blocks >= 1`, plus
  three corpus-wide denominator floors (`_CORPUS_POPULATION_FLOORS`, re-derived source literals,
  never read back from the regenerated artifact).
- `_corpus_perturbation_problems` — the D-03 anti-vacuity backbone: for every corpus row, reads
  shipped bytes fresh from disk, takes a `detect_defects` baseline, then runs three
  structurally-located, position-based, in-memory-only mutation families (verdict-cell separator,
  chain-hop re-wrap, citation removal) and asserts each firing family moves its target field by
  exactly the expected amount.
- `_CORPUS_CALL_SITES` / `_CORPUS_CALL_FORMS` / `_CORPUS_CALL_SITES_LOCK` — a comment-stripping
  source-text census over `cmd_check()`'s four enforcement call sites, floored by set equality
  against a second, independently transcribed roster (CONF-GATE's BL-01/BL-02 shape).
- All four floors wired into `cmd_check()` in the collect-then-report shape, after the existing
  drift check, so a stale baseline and a corpus floor breach are both reported in one run.
- 25 new `--self-test` controls (18 → 43), each with a positive and (where applicable) an
  isolated negative case.

## Task Commits

Each task was committed atomically:

1. **Task 1: Add the roster, disposition and population floors and wire them into cmd_check** —
   `7cfbb50` (feat)
2. **Task 2: Add the D-03 per-item in-memory perturbation floor with structural mutation sites** —
   `f809311` (feat)

**Plan metadata:** this SUMMARY.md (docs commit follows).

## Control count, before and after each task

- Before this plan: **18 controls** (`report-conformance: SELF-TEST PASS — 18 controls run`, per
  `19-05-SUMMARY.md`).
- After Task 1 (`7cfbb50`): **29 controls** (`report-conformance: SELF-TEST PASS — 29 controls
  run`), +11 for the roster/disposition/population floors.
- After Task 2 (`f809311`): **43 controls** (`report-conformance: SELF-TEST PASS — 43 controls
  run`), +14 for the perturbation floor and its call-site census.

## Re-derived population floor values (18-D-05 source-literal discipline)

Derivation command, run against the committed `docs/data/conformance.json` (never modified by
this plan), verbatim output:

```
$ python3 -c "
import json
data = json.load(open('docs/data/conformance.json'))
rows = data['adversarial_corpus']['rows']
totals = {}
for field in ('conclusion_claims','verdict_cells','chain_blocks'):
    totals[field] = sum(r[field] for r in rows if r['section_resolution']=='OK')
print(totals)
"
{'conclusion_claims': 49, 'verdict_cells': 66, 'chain_blocks': 32}
```

Pinned in `_CORPUS_POPULATION_FLOORS` exactly as printed: `conclusion_claims: 49`,
`verdict_cells: 66`, `chain_blocks: 32`. Asserted equal to this inline literal by the
`corpus-population-floor-values-locked` control.

## Files Created/Modified

- `scripts/report-conformance.py` — the four floors, their wiring into `cmd_check()`, the
  call-site census/roster-lock machinery, and 25 new `--self-test` controls. No other file
  touched.

## Verification performed (all commands actually run, outputs recorded)

- `python3 scripts/report-conformance.py --self-test` (final state): `SELF-TEST PASS — 43
  controls run`.
- `python3 scripts/report-conformance.py --check` (final state): `PASS — no drift`.
- `git diff --quiet docs/conformance-baseline.md docs/data/conformance.json` → succeeds
  (**ARTIFACTS BYTE-UNCHANGED**) — this plan changes no rendered byte, at both the Task 1 and
  Task 2 checkpoints.
- `git status --porcelain tests/adversarial-corpus-v9.0/` → empty after a full `--check` run.
- `sha256sum tests/adversarial-corpus-v9.0/*.md` compared programmatically against the 14-row
  table in `tests/adversarial-corpus-v9.0/README.md` (13 items + `catalog.md`, `README.md`
  itself correctly excluded from the table): `missing from table: set()`, `extra in table:
  set()`, `mismatches: []`.
- `bash scripts/check-firewall-battery.sh` (after `uv sync` to install the already-locked pytest
  dev dependency into this fresh worktree's `.venv`, the documented VAL-03 remedy): `FIREWALL:
  GREEN (25/25)`.
- `git diff --stat scripts/check-quality-harness.py scripts/check-conf-gate.py
  .github/workflows/validation.yml` → no output on both commits; neither frozen detector file nor
  the CI workflow was touched.
- `git status --porcelain` after each commit: exactly `scripts/report-conformance.py`, then clean.
- Post-commit deletion check (`git diff --diff-filter=D --name-only HEAD~1 HEAD`) on both
  commits: no output, no files deleted.

## Neutralization ledger (N01-N11), each applied ALONE to a disposable scratch copy

All eleven neutralizations were applied to an `rsync -a --exclude .git` scratch copy under the
scratchpad directory. `git status --porcelain` in the real worktree was confirmed empty before
and after every round; the scratch copy was deleted at the end. Each command's stderr is recorded
verbatim below (trimmed to the load-bearing line where the full diff output is not itself the
point).

**N01 — delete one row (`T-01`) from `catalog.md`:**
```
$ python3 scripts/report-conformance.py --check
report-conformance: FAIL — D-04 CORPUS ROSTER DRIFT: missing=['t01-ledger-arbitrary-chain'] extra=[]
```
Exit 1. Fires by name, naming the orphaned stem in `missing=[...]`.

**N02 — add a catalog row naming a stem with no file (`T-99` / `t99-nonexistent-item`):**
```
$ python3 scripts/report-conformance.py --check
report-conformance: FAIL — D-04 CORPUS ROSTER DRIFT: missing=[] extra=['t99-nonexistent-item']
```
Exit 1. Fires by name, naming the stem in `extra=[...]`.

**N03 — blank `T-01`'s `Disposition` cell:**
```
$ python3 scripts/report-conformance.py --check
report-conformance: FAIL — SILENT PASS [t01-ledger-arbitrary-chain]: scores fully clean, no disposition recorded
```
Exit 1.

**N04 — change `T-01`'s `Disposition` cell to `looks fine`:**
```
$ python3 scripts/report-conformance.py --check
report-conformance: FAIL — DISPOSITION FORM [t01-ledger-arbitrary-chain]: 'looks fine' does not begin with fix / accept-with-reason / defer-with-owner
```
Exit 1.

**N05 — delete every `## 6. Conclusion` claim from `t01-ledger-arbitrary-chain.md`** (section 6
body replaced with a single non-assertive `n/a` line):
```
$ python3 scripts/report-conformance.py --check
report-conformance: FAIL — CORPUS POPULATION [t01-ledger-arbitrary-chain] conclusion_claims: 0 — a form-clean reading over an empty population is not a probe
report-conformance: FAIL — CORPUS POPULATION FLOOR BREACH conclusion_claims: 41 < floor 49 — a zero defect count against a shrunken population is not conformance
```
Exit 1. Both the per-item and the corpus-wide denominator floor fired.

**N06 — delete the `## 2. Assumptions Table` data rows from `t01-ledger-arbitrary-chain.md`**
(header/separator retained, zero data rows):
```
$ python3 scripts/report-conformance.py --check
report-conformance: FAIL — CORPUS POPULATION FLOOR BREACH verdict_cells: 61 < floor 66 — a zero defect count against a shrunken population is not conformance
report-conformance: FAIL — D-03(a) mutation site not found (or not unique) in tests/adversarial-corpus-v9.0/t01-ledger-arbitrary-chain.md
```
Exit 1. The corpus-wide denominator floor fired as named by the plan; D-03(a) also correctly
reports "not found" for the same item since it no longer has any verdict cell to mutate.

**N07 — neuter mutation family (a)** (changed the script's own replacement character from `"-"` to
`"—"`, i.e. the mutation becomes a no-op):
```
$ python3 scripts/report-conformance.py --check
report-conformance: FAIL — D-03(a) verdict-cell separator mutation on tests/adversarial-corpus-v9.0/t01-ledger-arbitrary-chain.md did not increment nonconforming_verdict_cells by exactly 1 (baseline 0, mutated 0)
[... one such FAIL line per corpus item, all 13 ...]
```
Exit 1. Fires by name, naming the item and both baseline/mutated values, for every corpus item.

**N08 — delete `problems += _corpus_perturbation_problems(rows, REPO_ROOT)` from `cmd_check()`:**
```
$ python3 scripts/report-conformance.py --self-test
report-conformance: SELF-TEST FAIL [corpus-call-site-census-positive] — ["CALL-SITE CENSUS: _corpus_perturbation_problems occurs 0 time(s) in cmd_check's source, expected 1", "CALL-FORM LOCK: _corpus_perturbation_problems's expected call form not found in cmd_check's source: 'problems += _corpus_perturbation_problems(rows, REPO_ROOT)'"]
```
Exit 1. Fires by name, naming the call-site census and the deleted symbol.

**N09 — comment that same line out with a leading `#`:**
```
$ python3 scripts/report-conformance.py --self-test
report-conformance: SELF-TEST FAIL [corpus-call-site-census-positive] — ["CALL-SITE CENSUS: _corpus_perturbation_problems occurs 0 time(s) in cmd_check's source, expected 1", "CALL-FORM LOCK: _corpus_perturbation_problems's expected call form not found in cmd_check's source: 'problems += _corpus_perturbation_problems(rows, REPO_ROOT)'"]
```
Exit 1. The same census, this time via the comment-stripped source path — confirms the BL-01
case: a census that read un-stripped source would have passed here, and did not.

**N10 — delete `"_corpus_perturbation_problems"` from `_CORPUS_CALL_SITES_LOCK` only:**
```
$ python3 scripts/report-conformance.py --self-test
report-conformance: SELF-TEST FAIL [corpus-call-sites-roster-lock-positive] —
report-conformance: SELF-TEST FAIL [corpus-call-sites-roster-lock-narrowed] — ["ROSTER LOCK: _CORPUS_CALL_FORMS diverges from lock: ['_corpus_perturbation_problems']"]
```
Exit 1. Fires by name, naming the roster lock and the symbol.

**N11 — strip the U+2014 from `t01-ledger-arbitrary-chain.md`'s FIRST verdict cell (the one
`_corpus_verdict_mutation_site` would itself target):**
```
$ python3 scripts/report-conformance.py --check
report-conformance: FAIL — DRIFT: docs/conformance-baseline.md, docs/data/conformance.json
[... rendered diff showing t01's "clean": 7 -> 6, "nonconforming_verdict_cells": 0 -> 1,
     "verdict_flag": 0 -> 1, "form_defects": 0 -> 1, "fully_clean": true -> false ...]
```
Exit 1. **Recorded verbatim, as N11 instructs:** no `D-03(a)` problem fired. `t01` has five
verdict cells; `_corpus_verdict_mutation_site` tries conforming cells in document order and,
finding the first one's em dash already gone, moves on to the SECOND conforming cell (still
intact) and mutates that one successfully instead — the search-next-candidate behavior documented
in the function's own docstring. The observed failure is the second of the plan's two named
disjuncts: **"the item now fails CONF-07's form precondition"** — `nonconforming_verdict_cells`
now reads 1 at baseline (not 0), so `t01` no longer scores `fully_clean`, and the published
headline (`"clean": 7` → `6` for stratum B2) would move on a fresh render. `--check` reports this
as `DRIFT` because the committed `docs/conformance-baseline.md` still shows the pre-mutation
reading — exactly the D-07 disclosed bound already published in that file ("the drift gate fails
on staleness ... never when a count read here ... is high").

A neutralization that did not fire would have been a defect in this plan's floors; all eleven
fired as named.

## Decisions Made

- Split Task 1 and Task 2 into two separate atomic commits (unlike plan 19-05's forced single
  commit, which was required by the drift gate). Neither task here touches a rendered artifact,
  so nothing forced coupling; splitting them follows the standard task-commit protocol.
- Family (b)'s per-item absence (5 of 13 items use a single-line chain form with no separate
  arrow-led continuation line) is documented as an EXPECTED CONDITION in
  `_corpus_perturbation_problems`'s own docstring, never reported as its own problem — matching
  the plan's explicit "decide per family, state the decision" instruction. Families (a) and (c)
  are expected to find a site on every item (verified live); a missing site there is a genuine
  problem.
- Mutation sites are located by absolute character position (via `_corpus_section_offsets` plus
  each family's own structural locator), not by CONF-GATE's exact-string-count-== 1 test —
  verified empirically that no single corpus citation instance is textually unique in this
  13-item corpus (e.g. `t01`'s `(chain C2)` occurs 3 times, `(chains C1 and C2)` occurs 2 times),
  so string-count uniqueness cannot be the "site found" signal here the way it is for CONF-GATE's
  one long, naturally-unique needle. This is the trade RESEARCH.md's Q4 flags explicitly.

## Deviations from Plan

### Auto-fixed Issues

None — no bug, missing-critical-functionality, or blocking-issue auto-fix was required.

### Assumption Drift (advisory)

**1. Position-based mutation instead of string-count-based "uniqueness".** The plan's
`<interfaces>` block frames the mutation-site search in CONF-GATE's own vocabulary ("A site that
is not found, or that is found more than once where uniqueness is required..."), which reads as
an exact-string-count test. Empirically, on the real 13-item corpus, no single citation instance
is textually unique (verified before writing any mutation code — see the "Decisions Made"
section above), so a literal string-count approach would report "not unique" on nearly every item
and the floor would never pass. RESEARCH.md's own Q4 anticipates and names this exact trade
("the site precision CONF-GATE gets from an exact-string match... is lost"). The implementation
therefore uses absolute-position slicing instead of string-count uniqueness — functionally
equivalent precision (each mutation targets one exact, unambiguous character span) delivered by a
different mechanism than the prose literally describes. Documented here per the assumption-drift
advisory rather than silently substituted.

## Issues Encountered

None beyond the mechanical work of locating mutation sites, described above.

## User Setup Required

None — no external service configuration required. This worktree needed `uv sync` (gitignored
`.venv`) to satisfy the VAL-03 pytest prerequisite for the firewall battery, the same
already-documented remedy every prior plan in this phase applied independently in its own
worktree.

## Next Phase Readiness

- `scripts/report-conformance.py` now enforces four falsifiability floors over the
  adversarial-corpus reading; `docs/conformance-baseline.md` and `docs/data/conformance.json`
  remain byte-identical to plan 19-05's committed state.
- `tests/adversarial-corpus-v9.0/` is unchanged on disk (verified sha256-for-sha256 against the
  README's chain-of-custody table) and still **not registered** in `_FROZEN_PATHS` — that
  registration is deliberately deferred to plan 19-07 (wave 5), per decision (f) in
  `19-01-PLAN.md` and restated in plan 19-04's README.
- `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (25/25)` in this worktree as
  of the final commit; `python3 scripts/report-conformance.py --check` reports `PASS — no drift`;
  `git status --porcelain` is clean.
- Plan 19-07 can now register the corpus (and this script's own new floor machinery, which lives
  entirely inside `scripts/report-conformance.py` and needs no separate freezing) under
  `_FROZEN_PATHS` against a corpus whose reading is falsifiable rather than merely reported.

---
*Phase: 19-false-negative-rate*
*Completed: 2026-09-05*

## Self-Check

- FOUND: `scripts/report-conformance.py` (modified, present)
- FOUND: commit `7cfbb50` (Task 1)
- FOUND: commit `f809311` (Task 2)

## Self-Check: PASSED
