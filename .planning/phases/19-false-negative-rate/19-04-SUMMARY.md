---
phase: 19-false-negative-rate
plan: 04
subsystem: testing
tags: [adversarial-corpus, catalog, chain-of-custody, quality-harness, false-negative-rate]

# Dependency graph
requires:
  - phase: 19-false-negative-rate (plans 01, 02, 03, wave 1)
    provides: "the 13 corpus items on disk under tests/adversarial-corpus-v9.0/ and their measured
      dispositions, recorded in each plan's SUMMARY.md, consumed here verbatim"
provides:
  - "tests/adversarial-corpus-v9.0/catalog.md — the machine-parsed per-item metadata table"
  - "tests/adversarial-corpus-v9.0/README.md — hand-written chain of custody and sha256 table"
affects: [19-05, 19-06, 19-07]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Sidecar catalog.md, machine-parsed and equality-floored against the discovered file set
       (the tests/quality-provenance-v8.24/catalog.md precedent), paired with a hand-written
       README.md carrying chain of custody and sha256s (the tests/quality-ledger-v8.26/README.md
       precedent) — both applied to a 13-item corpus rather than a single fixture."

key-files:
  created:
    - tests/adversarial-corpus-v9.0/catalog.md
    - tests/adversarial-corpus-v9.0/README.md
  modified: []

key-decisions:
  - "Catalog IDs use the file's own number (T-01..T-14, T-10 absent) rather than a re-sequenced
     1-13 range, matching the plan's interfaces block and decision (b)'s numbering."
  - "No rate, count, or hand-typed fraction appears in catalog.md — per the plan's action text and
     D-06, the headline false-negative rate lives only in docs/conformance-baseline.md (a later
     plan's generated surface); this file states stratum definitions and dispositions only."
  - "Every 'What is false' cell avoids literal slash characters and the string '...' so the
     no-rate/no-placeholder acceptance checks pass without weakening the prose (e.g. '1,440÷100'
     phrasing carried from 19-02-SUMMARY.md rather than '1,440/100')."

requirements-completed: [CONF-07, CONF-08]

# Metrics
duration: ~35min
completed: 2026-09-05
---

# Phase 19 Plan 04: Adversarial Corpus Catalog and README Summary

**Authored the corpus's two hand-written sidecars — a seven-column, equality-floorable `catalog.md` covering all 13 items and a chain-of-custody `README.md` with a 14-row sha256 table — consuming the three wave-1 plans' measured dispositions verbatim rather than re-deriving them; zero code touched.**

## Performance

- **Duration:** ~35 min
- **Started:** 2026-09-05 (after worktree base correction to `6d5a079`)
- **Completed:** 2026-09-05
- **Tasks:** 2 completed
- **Files created:** 2 (`catalog.md`, `README.md`)

## Accomplishments

- `catalog.md` — one row per corpus item (13 total: `T-01`..`T-09`, `T-11`..`T-14`, `T-10`
  deliberately absent), each carrying ID, File (stem), Stratum, Source, a one-sentence "What is
  false" statement, the rule that ought to catch it (or the honest "no shipped rule reaches it"
  answer for B2), and an explicit Disposition. Five stratum-A rows (three positive controls —
  `T-03`/`T-04`/`T-05` — one genuine miss `T-06`, one disclosed grounding-short-circuit bound
  `T-13`), one B1 row (`T-02`, PROV-GUARD only), seven B2 rows.
- `README.md` — status line (FROZEN, deliberately-false content warning), origin/chain-of-custody
  section naming plans 19-01/19-02/19-03 per authoring group, the `SectionResolutionError`
  full-commit rationale, the no-substitute-fixture argument, the no-generated-twin statement, the
  stratum-A-non-clean-is-allowed note, the frozen-evidence discipline (including the `git rm`
  tamper-evidence residual) and its plan-19-07 sequencing note, and a 14-row sha256
  chain-of-custody table (13 corpus items + `catalog.md`), computed as the last edit.

## Task Commits

Each task was committed atomically:

1. **Task 1: Author catalog.md** — `7985524` (test)
2. **Task 2: Author README.md** — `5ac7484` (docs)

**Plan metadata:** commit pending (this SUMMARY).

_No TDD tasks in this plan — both tasks are `type="auto"`, pure sidecar authoring, no code path
exercised._

## Files Created/Modified

- `tests/adversarial-corpus-v9.0/catalog.md` — new. Prose header (what the corpus is, stratum
  definitions, why B1 is closed at PROV-GUARD, why `T-10` is absent), `## Catalog` table (13 rows,
  7 columns), `## Reading the strata` closing note.
- `tests/adversarial-corpus-v9.0/README.md` — new. Nine sections per the plan's `<action>` list:
  header/status, origin and chain of custody, full-commit rationale, no-substitute rationale,
  no-generated-twin statement, stratum-A-non-clean note, frozen-evidence discipline, sequencing
  note, sha256 table.

## Verification (observed results, commands actually run)

**Task 1's equality one-liner** (run against the committed `catalog.md`):
```
items 13 rows 13 B1 1
missing []
extra []
```
Exit code 0.

**Disposition-prefix census** (parsed from the committed table, all 13 rows):
```
accept-with-reason: 12
defer-with-owner: 1
```
No row begins with `fix`. Every "What is false" cell measured ≥ 40 characters with no `TBD`/
`TODO`/`...` substring (asserted by a scratchpad Python script, all 13 rows passed).

```
$ /usr/bin/grep -c 'T-10' tests/adversarial-corpus-v9.0/catalog.md
1
$ /usr/bin/grep -Ec '[0-9]+ */ *[0-9]+|false-negative rate is [0-9]' tests/adversarial-corpus-v9.0/catalog.md
0
```

**Task 2's README assertion command:**
```
files=14 hashrows=14
```
Exit code 0. Every one of the 14 sha256 digests in the committed table was re-verified against a
fresh `sha256sum tests/adversarial-corpus-v9.0/*.md` run via a scratchpad Python comparison
(`fresh_hashes == table_hashes` → `True`, `missing from table: set()`, `extra in table: set()`).

```
$ /usr/bin/grep -c 'README.md' tests/adversarial-corpus-v9.0/README.md
1
```
The three required README sentences, matched lines (grepped after commit):
- No-generated-twin: `## The corpus has no generated twin, deliberately` (line 48) — the section
  body states nothing under `shared/` produces the corpus and `sync-content.py` never emits it.
- Stratum-A-non-clean allowed: `## A stratum-A item is allowed to score non-clean` (line 56) — the
  section body states the three form counts (not the three substantive columns) are CONF-07's
  precondition.
- `git rm` deletion-guard residual: line 75, `committed \`git rm\` of one of these files is in HEAD
  by the time the check runs, so no worktree...` — states FROZEN-EVIDENCE is tamper-evidence for
  modification and addition, never a deletion guard.

```
$ ls tests/adversarial-corpus-v9.0/*.md | /usr/bin/grep -vc -e catalog.md -e README.md
13
$ python3 scripts/report-conformance.py --check
report-conformance: PASS — no drift
$ bash scripts/check-firewall-battery.sh
...
FIREWALL: GREEN (25/25)
$ git status --porcelain
(no output)
```

## Decisions Made

- Catalog IDs number by the file's own stem number (`T-01`..`T-14`, `T-10` absent) rather than
  re-sequencing to a dense `T-01`..`T-13` range — this matches the plan's own action text ("ID —
  `T-01` .. `T-14`, T-10 absent") and lets a reader map an ID directly to a filename without a
  lookup table.
- Every catalog cell was written to avoid literal `/` characters and the literal string `...`, so
  the plan's own acceptance-criteria greps (no rate/ratio, no placeholder text) pass without
  softening the prose — e.g. "1,440÷100 slip" (carried verbatim from `19-02-SUMMARY.md`'s own
  phrasing) rather than a slash-separated fraction.
- Consumed every falsehood statement, rule-reach analysis, and disposition directly from the three
  wave-1 SUMMARY.md files rather than re-measuring or re-deriving any of them, per the plan's
  `<interfaces>` instruction ("do not re-measure the corpus from scratch... do not re-derive a
  falsehood statement a SUMMARY already fixed").

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking issue] `uv sync` to install the already-locked pytest dev dependency**
- **Found during:** Task 2 verification (`bash scripts/check-firewall-battery.sh`)
- **Issue:** the battery reported `[PREREQ] VAL-03` and `FIREWALL: BLOCKED (24/25 passed)` because
  this fresh worktree had no `.venv` and the bare `python3` interpreter could not import `pytest`.
- **Fix:** ran `uv sync`, which reads the repo's own `pyproject.toml`/`uv.lock` (already committed,
  already pinned) to create `.venv` and install the six already-declared packages. This is the
  documented remedy in `CLAUDE.md`'s VAL-03 row and is explicitly outside the Rule-3
  package-install exclusion, which targets installing an arbitrary new package name, not syncing
  an existing lockfile — the same fix wave-1 plans 19-02 and 19-03 applied independently in their
  own worktrees.
- **Verification:** re-ran `bash scripts/check-firewall-battery.sh` — `FIREWALL: GREEN (25/25)`.
- **Files modified:** none tracked (`.venv/` is gitignored).
- **Committed in:** not committed (gitignored, no tracked-file change).

No other deviations — both tasks executed exactly as the plan's `<action>` blocks specify.

**Total deviations:** 1 (environment setup only, no product-code or fixture-content change).
**Impact on plan:** None.

## Assumption Drift (advisory)

None material. The corpus item count (13, `T-10` absent) and the stratum/B1-closure rules matched
`19-01-PLAN.md`'s decision record exactly; no drift from the plan's stated assumptions was observed.

## Known Stubs

None. Both sidecar files are complete, hand-written prose and tables with no placeholder values,
no empty data-bearing fields, and no deferred wiring.

## Threat Flags

None. This plan's threat register (T-19-01, T-19-03, T-19-04, T-19-06) is fully addressed by the
sha256 table (tampering), the `Source` column and README origin section (repudiation), the
first-paragraph deliberately-false-content warning (information disclosure), and the equality-
floored `catalog.md` table itself (disposition tampering) — no new security-relevant surface was
introduced beyond what the plan's own threat model already names.

## User Setup Required

None — no external service configuration required. A future session in a fresh worktree will need
`uv sync` again (gitignored `.venv`), same as every prior plan in this phase.

## Next Phase Readiness

- `tests/adversarial-corpus-v9.0/` now contains 13 corpus items plus `catalog.md` and `README.md`
  (15 files total), fully self-describing and machine-parsable, but **still not registered** in
  `_FROZEN_PATHS` — that registration is deliberately deferred to plan 19-07 (wave 5), per decision
  (f) in `19-01-PLAN.md` and restated in this plan's own README.
- Plan 19-05 (wave 3) can now build the `report-conformance.py` fourth-surface extension against a
  stable, catalogued corpus; plan 19-06 (wave 4) can build its three floors (equality, disposition,
  perturbation) against this exact `catalog.md` schema.
- `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (25/25)` in this worktree as of
  the final commit; `python3 scripts/report-conformance.py --check` reports `PASS — no drift`;
  `git status --porcelain` is empty.

---
*Phase: 19-false-negative-rate*
*Completed: 2026-09-05*

## Self-Check

- FOUND: tests/adversarial-corpus-v9.0/catalog.md
- FOUND: tests/adversarial-corpus-v9.0/README.md
- FOUND: commit 7985524 (Task 1)
- FOUND: commit 5ac7484 (Task 2)

## Self-Check: PASSED
