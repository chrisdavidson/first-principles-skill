---
phase: 16-integration-ship
plan: 01
subsystem: traceability-matrix
tags: [check-traceability, matrix-rows, self-test-sentinel, v8.26]
dependency-graph:
  requires: []
  provides:
    - "_rows_v826() (20 MatrixRow objects, 17 reproducible + 3 audit-only)"
    - "_self_test_v826_rows_sentinel() (V826-ROWS, dispatched inside TRACE-03)"
    - "new live headline: 192/94/0/286 (derived, not yet swept onto prose surfaces)"
  affects:
    - "docs/requirements-traceability.md (16-02 will sweep the new headline onto it)"
    - "CLAUDE.md, docs/README.md, docs/MEASUREMENT-MAP.md, docs/COMPONENT-DIAGRAM.md (16-02)"
    - "docs/requirements-matrix.md, docs/data/matrix.json (16-02 regenerates via emit)"
tech-stack:
  added: []
  patterns:
    - "_rows_v8NN() + _self_test_v8NN_rows_sentinel() milestone-registration pattern (4th iteration)"
key-files:
  created: []
  modified:
    - scripts/check-traceability.py
decisions:
  - "CHAINHEAD-07 gets its own v8.26 row distinct from the existing v8.25/CONTRACT-06 row (judgment call A3, independently reversible)"
  - "SCAN-04, SHIP-04, SHIP-05 tiered audit-only; the other 17 v8.26 rows are reproducible"
metrics:
  duration: "~35 minutes"
  completed: "2026-09-04"
---

# Phase 16 Plan 01: Register v8.26 matrix rows Summary

Registered this milestone's 20 requirements (CHAINHEAD-01..07, LEDGER-01..04, SCAN-01..04,
SHIP-01..05) as `v8.26` rows in `scripts/check-traceability.py`'s `build_matrix_rows()` oracle,
via a new `_rows_v826()` (17 reproducible + 3 audit-only) and a `V826-ROWS` self-test sentinel
built to the `_self_test_v825_rows_sentinel()` shape, dispatched inside `_run_self_test()`
immediately before `_self_test_headline_lock()`.

## What was built

**Task 1** — `_rows_v826() -> list[MatrixRow]`, inserted between `_rows_v825()` and
`build_matrix_rows()`. Returns exactly 20 rows, all `milestone="v8.26"`, keyed
`"v8.26/<bare_id>"`:

| bare_id | capability | tier | artifact_link |
|---|---|---|---|
| CHAINHEAD-01/02/03/05 | Methodology | reproducible | `check-quality-harness.py#_selftest_render_contract` |
| CHAINHEAD-04/06 | Test-Network | reproducible | `check-quality-harness.py#_selftest_render_contract` |
| CHAINHEAD-07 | Test-Network | reproducible | `check-quality-harness.py#_selftest_chain_detector_pin` |
| LEDGER-01/02 | Methodology | reproducible | `check-quality-harness.py#_selftest_render_contract` |
| LEDGER-03 | Methodology | reproducible | `check-quality-harness.py#_selftest_render_contract` |
| LEDGER-04 | Test-Network | reproducible | `check-quality-harness.py#_selftest_ledger_traceability` |
| SCAN-01 | Methodology | reproducible | `check-selfaudit-scan.py#_check_body_text` |
| SCAN-02 | Methodology | reproducible | `check-selfaudit-scan.py#_check_rubric_text` |
| SCAN-03 | Test-Network | reproducible | `check-selfaudit-scan.py#_check_cross_surface` |
| SCAN-04 | Test-Network | **audit-only** | `""` |
| SHIP-01 | Test-Network | reproducible | `check-version-stamps.py` |
| SHIP-02 | Test-Network | reproducible | `check-firewall-battery.sh` |
| SHIP-03 | Test-Network | reproducible | `check-traceability.py#_self_test_headline_lock` |
| SHIP-04/05 | Methodology | **audit-only** | `""` |

`build_matrix_rows()` now wires `rows.extend(_rows_v826())` as the last (eighth) inclusion
path, with its docstring updated ("Seven inclusion paths" → "Eight inclusion paths", plus a
new `(h)` paragraph).

**Task 2** — `_self_test_v826_rows_sentinel()`, inserted immediately after
`_self_test_v825_rows_sentinel()`. Blocks (a)-(g) mirror the V825-ROWS shape (row-count drift
guard, bare_id set, tier partition pinned BY ID, deep-resolved artifact_links, a SHIP-03
positive counter-check, milestone/key lock, capability lock). Two v8.26-specific blocks:
- **(h) LIVE ANCHOR FLOOR** — derives the set of `_selftest_*`/`_self_test_*` anchors from the
  live rows and asserts equality against exactly `{_selftest_render_contract,
  _selftest_chain_detector_pin, _selftest_ledger_traceability, _self_test_headline_lock}`, plus
  live positives for CHAINHEAD-07 and SHIP-03.
- **(h4) CALL-SITE CENSUS** — for the three non-`_selftest_`-prefixed SCAN anchors
  (`_check_body_text`, `_check_rubric_text`, `_check_cross_surface`), derived from the live
  rows' own artifact_link anchors, counts call sites in `check-selfaudit-scan.py`'s source text
  (excluding each symbol's own `def` line) and requires ≥2 total with ≥1 inside `_validate_files`
  and ≥1 inside `_run_self_test`.

Dispatched via `_self_test_v826_rows_sentinel(wrong_results)` in `_run_self_test()`, positioned
between `_self_test_v825_rows_sentinel(wrong_results)` and `_self_test_headline_lock(wrong_results)`
per the plan's ordering requirement.

**Task 3** — Recorded the derived headline (below) and confirmed the resulting red is confined
to HEADLINE-LOCK; no prose surface was edited (that is plan 16-02's job).

## Verification performed (observed, not assumed)

- `python3 -c "..."` (Task 1's exact verify command) — **exit 0**, printed:
  `OK ('192/94/0/286', '192 reproducible / 94 audit-only / 0 gap / 286 total')`
- `/usr/bin/grep -c "rows.extend(_rows_v826())" scripts/check-traceability.py` → `1`
- `/usr/bin/grep -n "Eight inclusion paths" scripts/check-traceability.py` → exactly one line
  (1871)
- `_rows_v826()`'s docstring contains `DISCLOSED BOUNDARY` and names `_check_body_text`,
  `_check_rubric_text`, `_check_cross_surface` — confirmed via a Python regex extraction, not
  by reading.
- `python3 scripts/check-traceability.py --self-test` — **exit 1** (expected). Output contains
  **11 `V826-ROWS PASS`** lines and **0 `V826-ROWS FAIL`** lines. All 9 `FAIL` lines present are
  `HEADLINE-LOCK` findings (confirmed by `grep "FAIL" | grep -cv "HEADLINE-LOCK"` → `0`).
- `python3 scripts/sync-content.py --check` — **exit 0**.
- `python3 scripts/check-version-stamps.py` — **exit 0**, reports `17 stamps, all '8.25.0'`.
- `git status --porcelain` after both task commits — **empty** (clean tree; both tasks
  committed). `git diff --stat` against the plan's base commit
  (`a19bf1c197275d746f22a7d8cdf3172af532762f`) confirms `scripts/check-traceability.py` is the
  **only** file touched across the whole plan (446 insertions, 2 deletions).

### Required mutation proofs (Task 2 acceptance criteria — performed, not reasoned about)

Both run on a disposable `rsync -a --exclude .git` scratch copy in the scratchpad directory,
confirmed via `git status --porcelain` on the real worktree before and after that the real tree
was never touched by the scratch mutations.

**Mutation 1** — flipped `SCAN-04`'s tier to `reproducible` and `CHAINHEAD-06`'s tier to
`audit-only` (holds the 17/3 counts constant). `--self-test` on the scratch copy reported:
```
V826-ROWS FAIL: audit-only bare_id set mismatch — expected=['SCAN-04', 'SHIP-04', 'SHIP-05'], got=['CHAINHEAD-06', 'SHIP-04', 'SHIP-05']
```

**Mutation 2** — deleted the `_check_cross_surface(` call inside `_validate_files`
(`scripts/check-selfaudit-scan.py:1493`) and the one inside `_run_self_test`'s positive control
(`:1836`). `--self-test` on the scratch copy reported:
```
V826-ROWS FAIL: (h4) CALL-SITE CENSUS — _check_cross_surface has 14 call site(s) (in _validate_files=0, in _run_self_test=14), expected >=2 with >=1 in each
```
(`_run_self_test` still calls `_check_cross_surface` from its many negative-control fixtures,
so the total stayed above the floor of 2 — the census correctly caught the deletion via the
`in _validate_files=0` sub-condition, exactly the disclosed shape: it counts source text, not
behavior.)

## New headline (for plan 16-02 to sweep onto the 5 `COVERED_HEADLINE_SURFACES` + 2 generated artifacts)

- Slash rendering: `192/94/0/286`
- Prose rendering: `192 reproducible / 94 audit-only / 0 gap / 286 total`
- `len(build_matrix_rows())`: `286`

## HEADLINE-LOCK findings checklist for plan 16-02

Every `FAIL` line from `python3 scripts/check-traceability.py --self-test` after this plan's
commits, all `HEADLINE-LOCK` (0 non-HEADLINE-LOCK failures confirmed above). File:line is the
current (stale, `175/91/0/266`-era) occurrence 16-02 must edit; the finding's own text is
copied verbatim from the self-test:

| # | File : line | Current stale text | Self-test finding |
|---|---|---|---|
| 1 | `docs/requirements-traceability.md:7` | `**Coverage headline:** 175 reproducible / 91 audit-only / 0 gap / 266 total` | `docs/requirements-traceability.md does not state '192 reproducible / 94 audit-only / 0 gap / 286 total' — build_matrix_rows() and the published headline disagree` |
| 2 | `docs/requirements-matrix.md` (generated) | stale row/count set | `docs/requirements-matrix.md is stale — re-run the emit subcommand` |
| 3 | `docs/data/matrix.json` (generated) | stale row/count set | `docs/data/matrix.json is stale — re-run the emit subcommand` |
| 4 | `CLAUDE.md:227` | `(**175 reproducible / 91 audit-only / 0 gap / 266 total**)` | `(f) CLAUDE.md does not state '192 reproducible / 94 audit-only / 0 gap / 286 total' as a non-historical occurrence` |
| 5 | `docs/COMPONENT-DIAGRAM.md:97` | `(active residuals; 175/91/0/266)` | `(f) docs/COMPONENT-DIAGRAM.md does not state '192 reproducible / 94 audit-only / 0 gap / 286 total' as a non-historical occurrence` |
| 6 | `docs/MEASUREMENT-MAP.md:52` | `(175 reproducible / 91 audit-only / 0 gap / 266 total)` | `(f) docs/MEASUREMENT-MAP.md does not state '192 reproducible / 94 audit-only / 0 gap / 286 total' as a non-historical occurrence` |
| 7 | `docs/README.md:20` | `> headline of **175 reproducible / 91 audit-only / 0 gap / 266 total**.` | `(f) docs/README.md does not state '192 reproducible / 94 audit-only / 0 gap / 286 total' as a non-historical occurrence` |
| 8 | `docs/requirements-traceability.md:7` (same statement as #1, different check layer) | see #1 | `(f) docs/requirements-traceability.md does not state '192 reproducible / 94 audit-only / 0 gap / 286 total' as a non-historical occurrence` |
| 9 | (derived) | — | `(j) accounted-hit floor unmet: ['CLAUDE.md', 'docs/COMPONENT-DIAGRAM.md', 'docs/MEASUREMENT-MAP.md', 'docs/README.md', 'docs/requirements-traceability.md']` — resolves automatically once #4-#8 are fixed |
| — | (self-resolving) | — | `(m) arm 2 precondition violated — the constructed total (0) does not meet or exceed the old running-total threshold (5)` — a self-test-internal control precondition tied to the same stale/current gap; resolves once the above are fixed |

Also flagged by 16-RESEARCH.md but out of this plan's scope (16-02's prose sweep, not a
`HEADLINE-LOCK` finding): `docs/requirements-traceability.md`'s "v8.26 CHAINHEAD
deferred-registration note" (line ~18-29) still says "nineteen requirements" and "Phase 16's
SHIP-01..04" — both stale now that SHIP-05 exists — plus headline-history row 12 needs adding
and the stale CHAINHEAD-06/07 "Pending" status in `.planning/REQUIREMENTS.md` may need
correcting (recorded as a hygiene item in 16-RESEARCH.md, not blocking).

## Deviations from Plan

### Auto-fixed Issues

None — plan executed exactly as written for the code changes.

### Noted acceptance-criterion discrepancy (documented, not silently ignored)

**Task 2's acceptance criterion** states:
`/usr/bin/grep -c "_self_test_v826_rows_sentinel(wrong_results)" scripts/check-traceability.py`
returns exactly `2` (one def, one dispatch).

**Observed:** this literal grep returns `1`, not `2`. Reason: every existing sentinel in this
file (`_self_test_v818_rows_sentinel`, `_self_test_v824_rows_sentinel`,
`_self_test_v825_rows_sentinel`) is defined as
`def _self_test_v8NN_rows_sentinel(wrong_results: list[str]) -> None:` — the type annotation
`: list[str]` between the parameter name and the closing paren means the `def` line does NOT
match the literal substring `_self_test_v8NN_rows_sentinel(wrong_results)` (no closing paren
immediately after `wrong_results`). Verified this is not new: the identical grep against the
pre-existing `_self_test_v825_rows_sentinel(wrong_results)` also returns `1`, not `2`, on the
unmodified tree. The plan's criterion appears to assume an un-annotated signature that does not
match this codebase's established convention.

**Resolution:** kept the annotated signature (`wrong_results: list[str]) -> None:`) for
consistency with `_self_test_v818/v824/v825_rows_sentinel`, and verified the underlying intent
— exactly one `def` and exactly one dispatch call — independently:
`/usr/bin/grep -c "^def _self_test_v826_rows_sentinel"` → `1`;
`/usr/bin/grep -n "_self_test_v826_rows_sentinel(wrong_results)"` shows exactly one call site
(inside `_run_self_test()`, immediately after `_self_test_v825_rows_sentinel(wrong_results)` and
before `_self_test_headline_lock(wrong_results)`). Not treated as a Rule 1-3 deviation since no
code was wrong — the plan's literal acceptance-criterion string just doesn't fit this codebase's
own signature style, the same way it wouldn't fit any of the three prior sentinels either.

## Known Stubs

None. This plan adds only data-returning functions and a self-test sentinel; no UI or
data-flow component receives empty/mock data as a result of this work.

## Threat Flags

None. Per the plan's own threat model, this phase edits one Python file mapping requirement
IDs to already-existing gates — no new input-handling, auth, network, or schema surface.

## Self-Check: PASSED

- `scripts/check-traceability.py` — FOUND (modified, both commits present)
- Commit `f2e9f45` (Task 1) — FOUND in `git log --oneline`
- Commit `e67b639` (Task 2) — FOUND in `git log --oneline`
- `python3 scripts/check-traceability.py --self-test` re-run at summary time — confirmed 11
  `V826-ROWS PASS`, 0 `V826-ROWS FAIL`, all other FAILs are `HEADLINE-LOCK`
