---
phase: 18-exemplar-conformance
plan: 12
subsystem: check-conf-gate.py (CONF-GATE)
tags: [gap-closure, self-test, neutralization, CONF-GATE, BL-03, WR-07]
dependency-graph:
  requires: [18-11]
  provides: [BL-03-closed, WR-07-closed]
  affects: [scripts/check-conf-gate.py]
tech-stack:
  added: []
  patterns:
    - "per-surface denominator floor as a seventh census/form-lock/roster-covered enforcement call site"
    - "inline-literal fixtures never derived from the constant they protect (CR-02(a) discipline, extended to _POPULATION_FLOORS)"
decisions:
  - "Pinned _POPULATION_FLOORS at the re-derived live reading (verdict_cells=77, heading_chain_blocks=31 per gated surface), matching 18-VERIFICATION.md's measured figure rather than 18-REVIEW.md's proposed 76/30."
  - "uv sync was run to materialize .venv/pytest so VAL-03's third leg could execute, resolving FIREWALL: BLOCKED to FIREWALL: GREEN (25/25); an environment setup action, not a code change — .venv stays gitignored."
metrics:
  duration: "~50 minutes"
  completed: "2026-09-05"
---

# Phase 18 Plan 12: Close BL-03 — per-surface denominator floors for verdict_cells/heading_chain_blocks Summary

Closed BL-03 from `18-VERIFICATION.md`: two of `_TARGETS`' four zero counts
(`nonconforming_verdict_cells`, `heading_malformed_blocks`) were numerator-only, so
zero-by-conformance and zero-by-deletion were indistinguishable. `scripts/check-conf-gate.py`
gains `_POPULATION_FLOORS` (per-surface denominator floors over `verdict_cells` and
`heading_chain_blocks`) and `_population_floor_problems`, wired as a seventh enforcement call
site covered by the existing census, form lock and roster equality lock. Also folded in WR-07
(18-REVIEW.md): the `heading_malformed_blocks` sum's readable-vs-all-rows scope decision is now
controlled, not just documented. `--self-test` grew from 34 to 38 controls.

## What Was Built

**Task 1 (BL-03):** Re-derived the floor values live from `docs/data/conformance.json` (command
and output below) and pinned `_POPULATION_FLOORS = {"verdict_cells": 77, "heading_chain_blocks":
31}` immediately after `_CLAIM_FLOORS_LOCK`, with a comment stating the DENOMINATOR-not-target
distinction, the D-05 source-literal discipline, and the DISCLOSED BOUND (shrinkage-only, not
substitution-detecting). Added `_population_floor_problems(rows)`, mirroring
`_targets_problems`' two scopes exactly (`verdict_cells` over readable rows,
`heading_chain_blocks` over all rows of the surface, per surface in `_GATED_SURFACES` order).
Wired `problems += _population_floor_problems(rows)` into `run_live()` immediately after the
existing claim-floor call. Widened the seven-symbol enforcement-call machinery from plans
18-09/18-11 to include the new symbol: `_LIVE_CALL_SITES`, `_LIVE_CALL_FORMS`,
`_LIVE_CALL_SITES_LOCK`, and all four synthetic census fixtures
(`_CENSUS_X1_CLEAN_SOURCE`, `_CENSUS_X2_MISSING_SOURCE`, `_CENSUS_X3_DUPLICATED_SOURCE`,
`_FORM_LOCK_X2_REWRITTEN_SOURCE`; `_CENSUS_X4_COMMENTED_SOURCE` derives from X1 by `.replace()`
and needed no direct edit). Amended the module docstring's Exit-codes enumeration and the
"six enforcement call sites" sentence (now seven).

**Task 2 (BL-03, WR-07):** Added four controls, every expected value an INLINE literal never
read from `_POPULATION_FLOORS` or `_TARGETS`:
- `population-floor-passes-at-floor` — two synthetic rows (one per gated surface) at exactly
  `verdict_cells=77, heading_chain_blocks=31`; asserts `_population_floor_problems([...]) == []`.
- `population-floor-fires` — the same two rows one below floor (`76`/`30`); asserts all four
  named problems (both keys, both surfaces).
- `population-floor-values-locked` — asserts `_POPULATION_FLOORS == {"verdict_cells": 77,
  "heading_chain_blocks": 31}` (an inline dict literal), the `ratchet-value-locked` shape.
- `target-heading-malformed-counted-when-unreadable` (WR-07) — a synthetic unreadable
  `shared-examples` row carrying `heading_malformed_blocks=1`; asserts `_targets_problems`
  still reports it, pinning the scope decision that this sum runs over ALL rows, not just
  readable ones.

## Floor re-derivation (verbatim)

```
$ python3 -c "import json;h=json.load(open('docs/data/conformance.json'))['headline'];print(h['verdict_cells'],h['heading_swept_blocks'])"
{'shared-examples': {'total': 77, 'nonconforming': 0}, 'generated-twin': {'total': 77, 'nonconforming': 0}, 'contract-surface': {'total': 1, 'nonconforming': 1}} {'shared-examples': {'total': 31, 'malformed': 0}, 'generated-twin': {'total': 31, 'malformed': 0}, 'contract-surface': {'total': 1, 'malformed': 0}}
```

Matches the plan's `<interfaces>` note: shared-examples and generated-twin both read 77
(`verdict_cells.total`) and 31 (`heading_swept_blocks.total`). Pinned the LIVE reading — no
adoption of 18-REVIEW.md's proposed 76/30 was needed since the two figures agreed.

## Control count before/after

| Point | Controls |
|-------|----------|
| Before this plan (end of 18-11) | 34 |
| After Task 1 (wiring only, no new controls) | 34 |
| After Task 2 | 38 |

## Neutralization Ledger

Every mutation below was applied ALONE to a scratch copy under the scratchpad directory
(`rsync -a --exclude .git` from the worktree), never to the real tree. `git status --porcelain`
on the real tree was confirmed to show only this plan's own in-progress edit to
`scripts/check-conf-gate.py` before and after each run.

### N10 — delete `problems += _population_floor_problems(rows)` from `run_live()` (Task 1 acceptance)

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [live-call-site-census] — ["CALL-SITE CENSUS: _population_floor_problems occurs 0 time(s) in run_live's source, expected 1"]
check-conf-gate: SELF-TEST FAIL [live-call-form-lock] — ["CALL-SITE CENSUS: _population_floor_problems occurs 0 time(s) in run_live's source, expected 1", "CALL-FORM LOCK: _population_floor_problems's expected call form not found in run_live's source: 'problems += _population_floor_problems(rows)'"]
rc=1
```

### N11 — delete `"_population_floor_problems"` from `_LIVE_CALL_SITES_LOCK` only

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [live-call-site-roster-locked] — CALL-SITE ROSTER DRIFT: ['_population_floor_problems']
rc=1
```

### N12 — the verifier's BL-03 reproduction, replayed (Task 1 acceptance)

Deleted all six data rows of `## 2. Assumptions Table` from
`shared/examples/software-systems.md` AND its byte-identical generated twin
`first-principles/agents/references/examples/software-systems.md` (confirmed 6 rows found and
removed on both surfaces).

```
$ python3 scripts/check-conf-gate.py
check-conf-gate: FAIL — POPULATION FLOOR BREACH [shared-examples] verdict_cells: 71 < floor 77 — a zero defect count against a shrunken population is not conformance
check-conf-gate: FAIL — POPULATION FLOOR BREACH [generated-twin] verdict_cells: 71 < floor 77 — a zero defect count against a shrunken population is not conformance
rc=1
```

Exit code **1**, naming both `POPULATION FLOOR BREACH [shared-examples] verdict_cells` AND
`POPULATION FLOOR BREACH [generated-twin] verdict_cells` (18-VERIFICATION.md measured `PASS`,
rc 0, for this exact pair of edits).

### N13 — 18-REVIEW.md's C3, replayed (Task 1 acceptance)

Renamed `### Conclusion C1: Architecture is not demonstrably the primary bottleneck` to
`### Renamed C1: ...` in both `shared/examples/software-systems.md` and its generated twin (a
fresh scratch copy, independent of N12's deletion).

```
$ python3 scripts/check-conf-gate.py
check-conf-gate: FAIL — POPULATION FLOOR BREACH [shared-examples] heading_chain_blocks: 30 < floor 31 — a zero defect count against a shrunken population is not conformance
check-conf-gate: FAIL — POPULATION FLOOR BREACH [generated-twin] heading_chain_blocks: 30 < floor 31 — a zero defect count against a shrunken population is not conformance
rc=1
```

Exit code **1**, naming `POPULATION FLOOR BREACH [shared-examples] heading_chain_blocks` as the
acceptance criterion requires (also names `generated-twin`, since the twin was edited too — a
strictly stronger result than the single-surface requirement).

After N12/N13, the real tree's `python3 scripts/sync-content.py --check` was confirmed rc 0 and
`git status --porcelain` showed only `scripts/check-conf-gate.py` as modified.

### N14 — change `_POPULATION_FLOORS["verdict_cells"]` from 77 to 1

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [population-floor-fires] — ['POPULATION FLOOR BREACH [shared-examples] heading_chain_blocks: 30 < floor 31 — a zero defect count against a shrunken population is not conformance', 'POPULATION FLOOR BREACH [generated-twin] heading_chain_blocks: 30 < floor 31 — a zero defect count against a shrunken population is not conformance']
check-conf-gate: SELF-TEST FAIL [population-floor-values-locked] — POPULATION FLOOR VALUE MISMATCH: {'verdict_cells': 1, 'heading_chain_blocks': 31} != {'verdict_cells': 77, 'heading_chain_blocks': 31}
rc=1
```

Both `[population-floor-values-locked]` (the direct value-lock arm) AND `[population-floor-fires]`
(the inline fixture's `verdict_cells=76` no longer breaches a floor of 1, so the fixture's
expected four-problem count drops to two, failing its own assertion) fire — the direct proof the
control is not self-referential.

### N15 — change `_POPULATION_FLOORS["heading_chain_blocks"]` from 31 to 32

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [population-floor-passes-at-floor] — 
check-conf-gate: SELF-TEST FAIL [population-floor-values-locked] — POPULATION FLOOR VALUE MISMATCH: {'verdict_cells': 77, 'heading_chain_blocks': 32} != {'verdict_cells': 77, 'heading_chain_blocks': 31}
rc=1
```

Both `[population-floor-values-locked]` AND `[population-floor-passes-at-floor]` fire (the
inline fixture's `heading_chain_blocks=31` no longer passes at a raised floor of 32).

**N14/N15 in one sentence:** each produced TWO named failures where BL-03's own hazard class (a
fixture derived from the constant it protects) would have produced one or zero — proof neither
inline-literal control is self-referential to `_POPULATION_FLOORS`.

### N16 — narrow the surface loop in `_population_floor_problems` to `("shared-examples",)`

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [population-floor-fires] — ['POPULATION FLOOR BREACH [shared-examples] verdict_cells: 76 < floor 77 — a zero defect count against a shrunken population is not conformance', 'POPULATION FLOOR BREACH [shared-examples] heading_chain_blocks: 30 < floor 31 — a zero defect count against a shrunken population is not conformance']
rc=1
```

`[population-floor-fires]` fires — the generated-twin arm no longer reports (only two of the
expected four problems returned).

### N17 — narrow `_targets_problems`' `heading_malformed_blocks` sum from `surf_rows` to `readable`

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST FAIL [target-heading-malformed-counted-when-unreadable] — ['TARGET EXCEEDED [shared-examples] unreadable: 1 > target 0']
rc=1
```

Exit code 1, naming `[target-heading-malformed-counted-when-unreadable]` — with the sum scoped
to `readable`, the synthetic unreadable row's `heading_malformed_blocks=1` no longer contributes
to any reading, so the control's assertion (expecting a `heading_malformed_blocks`-named
problem) fails and only the unrelated `unreadable` target problem survives (18-REVIEW.md M12
measured both legs PASS for this exact edit).

After every N10-N17 run, the scratch copy was discarded and the real tree's
`git status --porcelain` was confirmed to show only this plan's own in-progress edit to
`scripts/check-conf-gate.py`.

## Verification (run in order, from the repo root)

1. `python3 scripts/check-conf-gate.py --self-test` → `check-conf-gate: SELF-TEST PASS — 38 controls run`, rc 0
2. `python3 scripts/check-conf-gate.py` → `COVERAGE — measured 28 artifacts across shared-examples, generated-twin`, three `D-08(a)/(b)/(c) ... 0 -> 1` lines, `check-conf-gate: PASS`, rc 0
3. `python3 scripts/check-quality-harness.py --self-test` → rc 0, 27 sub-checks PASSED (including `chain_detector_pin`, `conclusion_claims_pin`, `slice_sections_pin`)
4. `git diff --stat scripts/check-quality-harness.py` → empty (CONTRACT-06 intact)
5. `python3 scripts/sync-content.py --check` → rc 0
6. `python3 scripts/report-conformance.py --check` → `report-conformance: PASS — no drift`, rc 0
7. `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (25/25)`, rc 0 (initially reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 24/25 passed)` because no interpreter in this fresh worktree could import pytest for VAL-03's third leg; ran `uv sync` to materialize `.venv`, resolving the prerequisite — `.venv` stays gitignored, an environment setup step, not a code change)
8. `git status --porcelain` → `M scripts/check-conf-gate.py` only

## Source Assertions

- `/usr/bin/grep -v '^ *#' scripts/check-conf-gate.py | /usr/bin/grep -n "_population_floor_problems"`
  shows the symbol in: `_LIVE_CALL_SITES`, `_LIVE_CALL_FORMS`, `_LIVE_CALL_SITES_LOCK`, the
  function definition, the `run_live()` call site, and all four synthetic census fixtures
  (`_CENSUS_X1_CLEAN_SOURCE`, `_CENSUS_X2_MISSING_SOURCE`, `_CENSUS_X3_DUPLICATED_SOURCE`,
  `_FORM_LOCK_X2_REWRITTEN_SOURCE`) — 9 non-comment hits total.
- `/usr/bin/grep -n "_POPULATION_FLOORS" scripts/check-conf-gate.py` shows it only in its own
  declaration/comment, inside `_population_floor_problems`, and as the left-hand side of the
  `population-floor-values-locked` equality assertion — no fixture derives a value from it.

## Deviations from Plan

None — plan executed exactly as written. The re-derived floor figures (77/31) matched the plan's
`<interfaces>` block's own live reading exactly, so no divergence from 18-REVIEW.md's proposed
76/30 needed further judgment beyond pinning the live figure as instructed.

## Assumption Drift (advisory)

None material.

## Self-Check: PASSED

- `scripts/check-conf-gate.py` exists and contains `_POPULATION_FLOORS`, `_population_floor_problems`: FOUND
- Commit `1dc4e9e` (Task 1) exists in `git log`: FOUND
- Commit `5a5f41d` (Task 2) exists in `git log`: FOUND
- `python3 scripts/check-conf-gate.py --self-test` → 38 controls, rc 0: FOUND
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (25/25)`: FOUND
