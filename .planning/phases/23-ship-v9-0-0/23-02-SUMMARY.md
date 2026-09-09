---
phase: 23-ship-v9-0-0
plan: 02
subsystem: traceability-matrix
tags: [matrix-rows, headline-lock, self-test-sentinel, conformance-milestone]

# Dependency graph
requires:
  - phase: 23-ship-v9-0-0
    plan: 01
    provides: "Nine re-derived v9.0.0 requirement boxes and PHASE_BASE_SHA (40064ee); no commit of its own (`.planning/` gitignored)"
provides:
  - "_rows_v9() and _self_test_v9_rows_sentinel() in scripts/check-traceability.py, registering the 19 v9.0.0 requirements (CONF-01..15, REL-01..04) as matrix rows"
  - "Coverage headline moved 192/94/0/286 -> 208/97/0/305 across all five COVERED_HEADLINE_SURFACES plus docs/gates/CONF-SURFACE.md/TRACE-03.md, produced by regenerating the matrix rather than a hand edit"
  - "docs/requirements-matrix.md and docs/data/matrix.json regenerated, confirmed byte-reproducible from a fresh emit"
  - "docs/requirements-traceability.md headline-history row 13, plus a correction to a pre-existing miscount in its own preamble sentence"
  - "REL-03 ticked in .planning/REQUIREMENTS.md with inline evidence"
affects: ["23-03", "23-04", "23-05"]

tech-stack:
  added: []
  patterns: ["positional MatrixRow construction (established convention)", "set-equality floors over named constants, never subset/count tests", "falsification by scratch-copy mutation, never by reading"]

key-files:
  created: []
  modified:
    - "scripts/check-traceability.py"
    - "docs/requirements-matrix.md"
    - "docs/data/matrix.json"
    - "docs/requirements-traceability.md"
    - "CLAUDE.md"
    - "docs/README.md"
    - "docs/MEASUREMENT-MAP.md"
    - "docs/COMPONENT-DIAGRAM.md"
    - "docs/gates/CONF-SURFACE.md"
    - "docs/gates/TRACE-03.md"
    - ".planning/REQUIREMENTS.md"
    - ".planning/STATE.md"
    - ".planning/ROADMAP.md"

key-decisions:
  - "Capability/tier assignment for all 19 rows follows the _rows_v826() discriminator verbatim (agent-read prose -> Methodology, apparatus/gate code -> Test-Network), with no departure needed for any row."
  - "Only REL-03 carries a #_self_test_* anchor (_self_test_headline_lock); the other 15 reproducible rows carry a bare script path because none of report-conformance.py/check-conf-gate.py/check-firewall-battery.sh/gen-gate-docs.py/check-version-stamps.py defines a _selftest_/_self_test_-prefixed symbol -- stated as a DISCLOSED BOUNDARY in both _rows_v9()'s and the sentinel's docstrings, and carried into headline-history row 13's Cause cell."
  - "docs/gates/CONF-SURFACE.md and docs/gates/TRACE-03.md required regeneration via gen-gate-docs.py --write (not originally named in the plan's files_modified list) because the headline move changed live-derived facts (coverage_headline, literal_scan_exempt_headline-provenance-delta) those generated pages embed."

requirements-completed: [REL-03]

# Metrics
duration: ~65min
completed: 2026-09-09
---

# Phase 23 Plan 02: Register v9.0.0 Matrix Rows and Sweep the Coverage Headline Summary

**`_rows_v9()` registers all 19 v9.0.0 requirements as traceability-matrix rows (16 reproducible
+ 3 audit-only), pinned by an 8-control `V9-ROWS` sentinel proven non-vacuous by four scratch-copy
mutations, and the resulting coverage-headline move (`192/94/0/286` → `208/97/0/305`) is swept
across all five `COVERED_HEADLINE_SURFACES` plus two generated gate-doc pages, landing in one
commit (`ed73189`).**

## Performance

- **Duration:** ~65 min
- **Completed:** 2026-09-09
- **Tasks:** 3 completed (landed as one commit, per plan design)
- **Files modified:** 10 tracked files in the commit, plus 3 gitignored `.planning/` files

## Accomplishments

- Added `_rows_v9()` immediately before `build_matrix_rows()`, registering 19 rows
  (CONF-01..15, REL-01..04) with milestone `"v9.0"` and keys prefixed `"v9.0/"`; wired as
  inclusion path `(i)` via `rows.extend(_rows_v9())`.
- Added `_self_test_v9_rows_sentinel()` reproducing the established 8-lettered-control shape
  (drift guard, set-equality ID/tier/anchor floors, deep artifact resolution, positive
  counter-check, milestone/key lock, capability lock, live anchor floor + live positive),
  registered in the self-test dispatcher immediately after `_self_test_v826_rows_sentinel`.
- Regenerated `docs/requirements-matrix.md` and `docs/data/matrix.json` via the documented
  `emit` command; confirmed byte-reproducible from a fresh run after all edits.
- Swept the derived headline (`208 reproducible / 97 audit-only / 0 gap / 305 total`, slash
  `208/97/0/305`) onto all five `COVERED_HEADLINE_SURFACES`, both prose and slash renderings
  where each surface uses them.
- Added headline-history row 13 to `docs/requirements-traceability.md`, corrected a pre-existing
  miscount in the same file's own preamble sentence, and updated the audit-only-rows heading.
- Regenerated `docs/gates/CONF-SURFACE.md` and `docs/gates/TRACE-03.md` via
  `gen-gate-docs.py --write` (their embedded `coverage_headline` and
  `literal_scan_exempt_headline-provenance-delta` facts had moved with the new rows).
- Confirmed by section-scoped diff against `HEAD` (`c02a065`) that CLAUDE.md's "Review protocol"
  and docs/README.md's "Standing of the nine milestone documents" sections are byte-unchanged.
- Ticked REL-03 in `.planning/REQUIREMENTS.md` with inline evidence; updated
  `.planning/STATE.md` and `.planning/ROADMAP.md`.

## Headline Move (before/after)

| | Before | After |
|---|---|---|
| Prose | `192 reproducible / 94 audit-only / 0 gap / 286 total` | `208 reproducible / 97 audit-only / 0 gap / 305 total` |
| Slash | `192/94/0/286` | `208/97/0/305` |
| Rows | 286 | 305 (+19) |

Derived live via `_headline_literals()` off `build_matrix_rows()` after `_rows_v9()` was wired
in — never pre-computed or carried over from a planning document. Verified: `python3
scripts/check-traceability.py --self-test` → `check-traceability --self-test: PASS`, with
`HEADLINE-LOCK PASS` on every stage and zero `HEADLINE-LOCK FAIL` / `V9-ROWS FAIL` lines.

## Audit-only ID set (by name, set-equality pinned)

`CONF-14`, `CONF-15`, `REL-04` — the same three named in `_rows_v9()`'s docstring and asserted
by `_self_test_v9_rows_sentinel()` control (c) against `_EXPECTED_V9_AUDIT_ONLY_IDS`. The
remaining 16 (`CONF-01..13` minus `CONF-14`/`CONF-15`, plus `REL-01..03`) are reproducible.

## Falsification Table (V9-ROWS non-vacuity, four scratch-copy mutations)

All four mutations applied only to a disposable `rsync -a --exclude .git` scratch copy at the
session scratchpad directory, never to the real tree. `git status --porcelain` in the real
repository showed the same single line (`M scripts/check-traceability.py` — the in-progress,
not-yet-committed task 1/2 diff, expected per the plan's own "land tasks 1-3 as one commit"
design) both immediately before the first mutation and immediately after the last; no new
diff was introduced by the mutation exercise itself.

| # | Mutation | Command | Verbatim result | CAUGHT? |
|---|---|---|---|---|
| 1 | Delete CONF-01's `MatrixRow` block (3 lines) | `python3 scripts/check-traceability.py --self-test` | `V9-ROWS FAIL: expected exactly 19 rows in _rows_v9(), got 18 — drift guard failed.` / `V9-ROWS FAIL: bare_id set mismatch — missing=['CONF-01'], extra=[]` / `V9-ROWS FAIL: reproducible bare_id set mismatch — ...` | YES — (a), (b), (c) |
| 2 | Flip REL-04 audit-only→reproducible **and** CONF-01 reproducible→audit-only (counts unchanged: 3 audit-only / 16 reproducible before and after) | same | `V9-ROWS FAIL: audit-only bare_id set mismatch — expected=['CONF-14', 'CONF-15', 'REL-04'], got=['CONF-01', 'CONF-14', 'CONF-15']` | YES — (c), proving the partition is pinned by name, not count |
| 3 | Change CONF-06's key prefix `"v9.0/CONF-06"` → `"v8.26/CONF-06"` (milestone field left `"v9.0"`) | same | `V9-ROWS FAIL: milestone/key drift — ['v8.26/CONF-06']` | YES — (f) |
| 4 | Repoint REL-03's `artifact_link` anchor to `_self_test_nonexistent_anchor` | same | `V9-ROWS FAIL: artifact_link issue — REL-03: anchor '_self_test_nonexistent_anchor' is not a def/class/module-level symbol in 'scripts/check-traceability.py'` / `V9-ROWS FAIL: (h) LIVE ANCHOR FLOOR — expected anchor set ['_self_test_headline_lock'], observed ['_self_test_nonexistent_anchor']` / `V9-ROWS FAIL: (h) LIVE POSITIVE — REL-03 did not resolve cleanly: [...]` | YES — (d), (h) anchor floor, (h) live positive |

Each mutation reverted before the next; `md5sum` of the scratch file confirmed byte-identical
to a saved pre-mutation copy after every revert.

## Tree-wide Grep — Superseded Literal Disposition

`git grep -n "192 reproducible"` and `git grep -n "192/94/0/286"` across the tracked tree, every
surviving hit disposed:

| File | Disposition |
|---|---|
| `.planning/milestones/v8.26.0-phases/16-integration-ship/16-0*-SUMMARY.md` (10 hits) | Historical plan-execution records of the prior (v8.26.0) headline move — dated, past-tense, force-tracked SUMMARY.md files; not current-fact claims |
| `.planning/phases/20-live-conformance/20-04-SUMMARY.md`, `20-06-SUMMARY.md` | Historical — records what the headline read *during* Phase 20's own execution |
| `.planning/phases/21-generate-the-claim-surface/21-05-SUMMARY.md`, `21-12-SUMMARY.md`, `21-CONF13-BASELINE.md` | Historical — records of Phase 21's own measurements at the time |
| `.planning/phases/22-cap-the-recursion/22-07-SUMMARY.md` | Historical |
| `.planning/phases/24-diagnosis-name-the-mechanism-not-the-instance/24-03-SUMMARY.md` | Historical |
| `CHANGELOG.md` (2 hits) | `HISTORICAL_EXEMPT_FILES` member — describes the `[8.26.0]` entry's own past move, correctly frozen |
| `docs/README.md:106` | Inside "Standing of the nine milestone documents" — the CR-03-fenced section; confirmed byte-unchanged (see CR-02/CR-03 fence below); also carries an explicit arrow, so it is historical regardless |
| `docs/gates/TRACE-03.md`, `docs/gates/CONF-SURFACE.md` | **Regenerated** this plan (`gen-gate-docs.py --write`) — now state the current `208/97/0/305` figure; the grep no longer finds a current-fact `192/94` hit here after regeneration |
| `docs/requirements-traceability.md` (rows 12, historical-note lines 35/136) | Historical — each carries an explicit arrow (`→`) marking it as a past transition, per `HEADLINE-LOCK`'s own arrow-adjacency exemption |
| `CLAUDE.md:322-323` | Historical — arrow chain in the "Requirements surface" section's provenance parenthetical |

No hit anywhere in the tracked tree states the superseded figure as an unqualified current fact.
`docs/COMPONENT-DIAGRAM.md` slash-form check (`192/94/0/286`) returns nothing after the sweep.

## CR-02 / CR-03 No-Fix Fence (section-scoped diff)

Base: `HEAD` at plan start = `c02a065c192e2c337a53aaf53ea317e96b603d99` (plan 23-01's metadata
commit). This is the correct base because `.planning/` is gitignored (`commit_docs: false`, so
plan 23-01 made no commit of its own to `CLAUDE.md`/`docs/README.md`), and this plan's own
tasks 1-2 touched only `scripts/check-traceability.py` before either fenced file was edited.

```
git show HEAD:CLAUDE.md | awk -v h='### Review protocol' 'index($0,h)==1{f=1;print;next} f&&/^#+ /{exit} f{print}'
git show HEAD:docs/README.md | awk -v h='## Standing of the nine milestone documents' 'index($0,h)==1{f=1;print;next} f&&/^#+ /{exit} f{print}'
```
— same `awk` applied to the working-tree file after all edits (including the
`gen-gate-docs.py --write` regeneration, which touched CLAUDE.md's generated gate table but not
this hand-written section).

| Section | Pre-edit line count | Diff against working tree |
|---|---|---|
| `CLAUDE.md` § "Review protocol" | 37 | **empty** |
| `docs/README.md` § "Standing of the nine milestone documents" | 42 | **empty** |

Both extractions non-vacuous (37 and 42 lines respectively — the heading was not accidentally
deleted), and both diffs empty. No fix was written for CR-02 or CR-03 in this plan.

## Verification Results

```
$ python3 scripts/check-traceability.py --self-test
... (many PASS lines, including 9× "V9-ROWS PASS", 56× "HEADLINE-LOCK PASS")
check-traceability --self-test: (describe) describe()-consistency PASS (19 blocks, 4 scan globs)
check-traceability --self-test: PASS
$ echo $?
0
```

```
$ python3 scripts/check-traceability.py emit --md-output .planning/tmp-verify/m.md --json-output .planning/tmp-verify/m.json
check-traceability emit: PASS — 305 rows written to .planning/tmp-verify/m.md + .planning/tmp-verify/m.json
$ diff -q .planning/tmp-verify/m.md docs/requirements-matrix.md && echo MD MATCH
MD MATCH
$ diff -q .planning/tmp-verify/m.json docs/data/matrix.json && echo JSON MATCH
JSON MATCH
```

```
$ python3 scripts/gen-gate-docs.py --self-test
gen-gate-docs: SELF-TEST PASS — 74 controls run
$ python3 scripts/gen-gate-docs.py --check
harvested 22/22 expected script-backed entries (22 total)
$ echo $?
0
$ sh .githooks/pre-commit
... (report-conformance self-test's own mutated-fixture diff line, expected internal noise)
report-conformance: SELF-TEST PASS — 102 controls run
report-conformance: PASS — no drift
gen-gate-docs: SELF-TEST PASS — 74 controls run
harvested 22/22 expected script-backed entries (22 total)
$ echo $?
0
```

```
$ /usr/bin/grep -c "rows.extend(_rows_v9())" scripts/check-traceability.py
1
$ /usr/bin/grep -c "_self_test_v9_rows_sentinel(wrong_results)" scripts/check-traceability.py
1
$ git log --oneline -1
ed73189 feat(23-02): register v9.0.0's 19 requirements as matrix rows, sweep headline
$ git show --stat HEAD | tail -3
10 files changed, 589 insertions(+), 28 deletions(-)
```

- `FIREWALL: GREEN 26/26` was not used anywhere in this plan to discharge REL-03; every
  criterion above is evidenced by a specific command's observed output.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Pre-existing miscount in `docs/requirements-traceability.md`'s own
headline-history preamble**
- **Found during:** Task 3, deriving the "moved N times" count from the table's own rows to
  write the new sentence.
- **Issue:** The preamble read "The coverage headline has moved nine times", but the table (12
  rows before this plan's row 13) marks only rows 4 and 5 as zero-drift, leaving 10 non-zero-drift
  rows — the sentence already disagreed with its own table before this plan touched it.
- **Fix:** Corrected to "eleven times" (10 pre-existing + row 13), with an explicit
  "**Correction, dated 2026-09-09**" note stating the prior figure, why it was wrong, and that it
  was found while deriving the new count rather than introduced by it.
- **Files modified:** `docs/requirements-traceability.md`
- **Verification:** Recomputed by counting table rows 1-13 minus the two explicitly-marked
  zero-drift rows = 11; matches the corrected sentence.
- **Committed in:** `ed73189`

**2. [Rule 3 - Blocking] `docs/gates/CONF-SURFACE.md` and `docs/gates/TRACE-03.md` went stale
after the headline move, blocking `gen-gate-docs.py --check`**
- **Found during:** Task 3, running `gen-gate-docs.py --check` before the closing commit (per
  the plan's own WR-05 ordering instruction).
- **Issue:** Both pages embed live-derived facts (`coverage_headline`, and
  `literal_scan_exempt_headline-provenance-delta`, which grew 11→13 because row 13's own headline
  move added more `N,M,...` digit-adjacent-to-`row` literals to that exempt class) that moved
  with `_rows_v9()`'s registration but were not yet regenerated.
- **Fix:** Ran `python3 scripts/gen-gate-docs.py --write`, which regenerated all 34 tracked
  generated pages; only these two had content changes. Re-ran `--self-test` then `--check`,
  both clean.
- **Files modified:** `docs/gates/CONF-SURFACE.md`, `docs/gates/TRACE-03.md` (added to the
  commit; not originally in the plan's `files_modified` frontmatter, but required for the
  commit's own pre-commit gates to pass)
- **Verification:** `python3 scripts/gen-gate-docs.py --check` → `harvested 22/22 ... EXIT 0`;
  section-scoped CR-02/CR-03 diff re-confirmed empty after the regeneration (CLAUDE.md's
  generated gate table changed elsewhere in the same file, not inside the fenced section).
- **Committed in:** `ed73189`

**3. [Rule 1 - Bug] `bm-sdk query state.record-session --resume-file "None"` clobbered the
byte-verbatim-protected Phase 22 halt record inside `.planning/STATE.md`**
- **Found during:** State-update step, immediately after the tool call, while spot-checking
  what it had changed.
- **Issue:** This repository's `STATE.md` carries exactly one field named `Resume file:`, and it
  sits inside the "Phase 22 halt record, verbatim" block that D-07 requires stay byte-unchanged.
  The generic `state.record-session` handler's blind field-replace matched that one occurrence
  and overwrote it from
  `.planning/phases/24-diagnosis-name-the-mechanism-not-the-instance/24-CONTEXT.md` to `None`.
- **Fix:** Reverted the line to its original text immediately, before any further edits.
  Recorded here rather than silently absorbed; no further `state.record-session` calls with a
  `--resume-file` argument were made this plan.
- **Files modified:** `.planning/STATE.md` (gitignored; no commit)
- **Verification:** `/usr/bin/grep -n -i resume .planning/STATE.md` → single hit, restored to
  `.planning/phases/24-diagnosis-name-the-mechanism-not-the-instance/24-CONTEXT.md`.
- **Committed in:** n/a (`.planning/STATE.md` is gitignored)

## Known Stubs

None. Every artifact this plan touches is either a data-registration function with a live
self-test sentinel, or a regenerated/hand-swept documentation surface — no UI, no mock data path.

## Threat Flags

None. Per the plan's own threat model (T-23-02/T-23-03/T-23-04, all `mitigate`): the sentinel's
eight controls plus four mutation arms mitigate T-23-02; the DISCLOSED BOUNDARY paragraphs in
both `_rows_v9()` and its sentinel mitigate T-23-03; the section-scoped CR-02/CR-03 diff
mitigates T-23-04. No new network, auth, or trust-boundary surface is introduced.

## Next Steps

- Plan 23-03 (Wave 3): REL-01 — bump all 17 hand-maintained version stamps to `9.0.0` in
  lockstep, propagate through `sync-content.py`, prove VERSION-01 and DUAL-04 fail by mutation.
- REL-02 (23-04) and REL-04 (23-05) remain; REL-03 is the only Phase 23 requirement this plan
  discharges.

## Self-Check: PASSED

- `test -f scripts/check-traceability.py` → FOUND
- `test -f docs/requirements-matrix.md` → FOUND
- `test -f docs/data/matrix.json` → FOUND
- `test -f docs/gates/TRACE-03.md` → FOUND
- `test -f docs/gates/CONF-SURFACE.md` → FOUND
- `git log --oneline --all | grep -q ed73189 && echo FOUND` → FOUND
- `/usr/bin/grep -c "rows.extend(_rows_v9())" scripts/check-traceability.py` → `1` → FOUND
- `/usr/bin/grep -c "_self_test_v9_rows_sentinel(wrong_results)" scripts/check-traceability.py` → `1` → FOUND
- `/usr/bin/grep -n "\[x\] \*\*REL-03\*\*" .planning/REQUIREMENTS.md` → FOUND
