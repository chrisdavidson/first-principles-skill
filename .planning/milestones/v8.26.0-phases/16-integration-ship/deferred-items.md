# Phase 16 Deferred Items

## QUAL-01 self-test regression from wave 1 (16-01), out of scope for 16-03

**Found during:** 16-03's plan-level sanity re-run of `bash scripts/check-firewall-battery.sh`
after all three tasks landed (that command is not part of 16-03's own `<verification>` block,
which only requires `check-version-stamps.py` (both legs), `sync-content.py --check`,
`check-agent.py`, and `check-traceability.py --self-test` — all of which pass).

**Observed:**
```
[FAIL] QUAL-01         check-quality-harness.py --self-test
FIREWALL: RED (1 gate(s) failed, 1 prerequisite(s) unmet; 22/24 passed)
```
`python3 scripts/check-quality-harness.py --self-test` fails with:
```
self-test FAIL: render_contract (x) COVERAGE FLOOR: (u) dispatch-reachability symbol set:
actual ['_selftest_analysis_persistence', '_selftest_capture_tool_reader',
'_selftest_chain_detector_pin', '_selftest_ledger_traceability', '_selftest_render_contract']
!= required ['_selftest_analysis_persistence', '_selftest_capture_tool_reader',
'_selftest_chain_detector_pin', '_selftest_render_contract']
— MISSING [], UNEXPECTED ['_selftest_ledger_traceability']
```
(One `[PREREQ] VAL-03` line also appears — a missing pytest interpreter in this worktree's
Python environment, an unrelated, pre-existing environment gap, not a gate failure per
CLAUDE.md's SHIP-06 three-state verdict semantics.)

**Root cause:** `scripts/check-quality-harness.py` carries its own internal hardcoded
locked anchor set (`render_u_required`, restated in the `(u) dispatch-reachability symbol set`
coverage-floor entry) used to assert exactly which `_selftest_*` symbols
`check-traceability.py`'s matrix `artifact_link`s are allowed to name inside this file. Wave 1
(16-01) registered `v8.26/LEDGER-04` with `artifact_link =
"check-quality-harness.py#_selftest_ledger_traceability"` — a fifth anchor into this file that
predates Phase 16 (added at Phase 14, plan 14-05) but was never previously named by any
`check-traceability.py` matrix row, so this locked set was never exercised against it. Wave 1's
own summary (`16-01-SUMMARY.md`) confirms `scripts/check-traceability.py` was the only file it
touched — it never had reason to know `check-quality-harness.py` carries a second, independent
lock on the same symbol set.

**Why this is out of scope for 16-03:** Plan 16-03's task list is scoped to version-stamp
bumps, generated-tree propagation, and retiring three time-qualified release-status sentences
(scope addition L-2) — `scripts/check-quality-harness.py` is not in its `files_modified` list
and none of its three tasks touch matrix-row registration. The regression was introduced by
wave 1 (16-01), not by any 16-03 edit; SCOPE BOUNDARY (deviation rules) requires only
in-scope auto-fixing. 16-03's own `<verification>` block does not require the full battery to
pass — only version-stamps/sync-content/check-agent/traceability, all of which pass.

**Confirmed to belong to 16-04, not 16-03:** `16-04-PLAN.md` Task 1's own `<action>` explicitly
anticipates and directs this exact fix: "the tree now differs from the plan-time baseline in
exactly four ways — the 20 new matrix rows (16-01) ... If any gate reports FAIL, fix the cause
rather than the symptom." Fixing `render_u_required` (and its `(x)` coverage-floor-entry
restatement) to include `_selftest_ledger_traceability` is 16-04 Task 1's job, since that is
where `bash scripts/check-firewall-battery.sh` is required to report `FIREWALL: GREEN (24/24)`.

**Action taken:** none — deferred to 16-04 per its own plan text, as designed.
