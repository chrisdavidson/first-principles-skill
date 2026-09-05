---
phase: 16-integration-ship
plan: 04
subsystem: firewall-battery
tags: [ship-02, qual-01, dispatch-reachability, gate-count-reconciliation]
dependency-graph:
  requires:
    - "17 hand-maintained version stamps at 8.26.0 and zero-drift regenerated tree (16-03)"
    - "20 new v8.26 matrix rows registered at Phase 16 (16-01), including LEDGER-04's artifact_link into check-quality-harness.py#_selftest_ledger_traceability"
  provides:
    - "bash scripts/check-firewall-battery.sh reports FIREWALL: GREEN (24/24), exit 0, on the fully integrated tree"
    - "QUAL-01's dispatch-reachability anchor set (control (u)) widened from four to five anchors, matching what LEDGER-04's artifact_link legitimately added"
    - "SHIP-02 confirmed: every surface stating the battery's gate count (script roster, CLAUDE.md, docs/ARCHITECTURE.md, docs/README.md) reconciles to the 22 gate/gate_prereq ids + 2 inline checks = 24 the script actually runs"
  affects:
    - "scripts/check-quality-harness.py"
tech-stack:
  added: []
  patterns:
    - "uv sync to provision a pytest-capable .venv when VAL-03's third leg reports [PREREQ] BLOCKED rather than a gate FAIL"
key-files:
  created: []
  modified:
    - scripts/check-quality-harness.py
decisions:
  - "Widened render_u_required and its ENTRY-SOURCE LOCK restatement from four to five locked anchors (adding _selftest_ledger_traceability) rather than weakening the EQUALITY floor to a subset test — WR-04 exists precisely so a narrowing anchor set cannot hide behind a subset check, and this file's own docstring frames restating the set (not deriving it) as the deliberate, loud-on-narrow design."
metrics:
  duration: "~20 minutes"
  completed: "2026-09-04"
---

# Phase 16 Plan 04: Confirm SHIP-02 — full battery GREEN on the integrated tree Summary

Diagnosed and fixed the QUAL-01 regression 16-03 deferred (a stale four-anchor dispatch-reachability
lock in `check-quality-harness.py` that predated wave 1's legitimate fifth anchor), confirmed
`bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)` on the fully integrated
tree, and reconciled the battery's gate-count claim across all four surfaces that state it — finding
all four already correct, requiring no prose edits.

## What was built

**Task 1** — Ran the full offline battery on the tree as merged from waves 1-3. Initial run reported
`FIREWALL: RED (1 gate(s) failed, 1 prerequisite(s) unmet; 22/24 passed)`: `[PREREQ] VAL-03` (no
pytest-capable interpreter in this worktree) and `[FAIL] QUAL-01`
(`check-quality-harness.py --self-test`).

- **VAL-03 PREREQ**: fixed per the plan's own remedy and the environment notes — ran `uv sync`,
  which created `.venv` with pytest 9.1.1 (gitignored, confirmed via `.gitignore:11`, `git status`
  clean before and after).
- **QUAL-01 FAIL**: reproduced the exact failure the orchestrator diagnosed and 16-03 deferred —
  `(x) COVERAGE FLOOR: (u) dispatch-reachability symbol set: actual [...5 anchors...] != required
  [...4 anchors...] — UNEXPECTED ['_selftest_ledger_traceability']`. Confirmed independently, before
  acting, each fact the scoped-deviation grant asserted: `LEDGER-04`'s `artifact_link` at
  `scripts/check-traceability.py:1833` really does name
  `check-quality-harness.py#_selftest_ledger_traceability`; that symbol really exists
  (`check-quality-harness.py:14266`) and really is dispatched from `self_test()`
  (`check-quality-harness.py:16663`); and `check-traceability.py`'s own dispatch-reachability leg
  passes, meaning this is a real, legitimate fifth anchor rather than a hidden deletion the floor
  should have caught. Widened both locked transcriptions of the anchor set — `render_u_required`
  (control (u)'s primary lock) and its independent second transcription inside the ENTRY-SOURCE LOCK
  registry (`render_x_entry_source_expected["(u) dispatch-reachability symbol set"]`) — from four to
  five, keeping the assertion an EQUALITY floor (not weakened to a subset test, per WR-04's own
  rationale), and corrected the three co-located comments that stated "four anchors"/"four locked
  anchors" as a count. This is the scoped deviation authorized by this plan's own execution prompt:
  `scripts/check-quality-harness.py` is outside `16-04-PLAN.md`'s declared `files_modified`
  (`CLAUDE.md`, `docs/ARCHITECTURE.md`, `scripts/check-firewall-battery.sh`), but the plan's own
  Task 1 action text directs fixing exactly this class of regression, and 16-03's own deferred-items
  entry named this as 16-04 Task 1's job.
- Re-ran the full battery: `FIREWALL: GREEN (24/24)`, exit 0, zero `[FAIL]` lines, zero `[PREREQ]`
  lines, 24 `[PASS]` lines.

Verbatim lines confirming the two named controls, from `/tmp/16-04-battery-final.txt`:
```
[PASS] QUAL-01         check-quality-harness.py --self-test
[PASS] SCAN-GUARD      check-selfaudit-scan.py --self-test + live
```

**Task 2** — Derived ground truth from the script itself: `22` distinct `gate`/`gate_prereq` ids
(23 call sites, one tally slot shared by VAL-03's either/or branch, matching the plan's own disclosed
shape) plus 2 inline checks (`INVARIANT-CHECK`, `FROZEN-EVIDENCE`) = 24. Checked all three counting
surfaces the plan names, plus the two adjacent claims it calls out, against that derived number:

1. `scripts/check-firewall-battery.sh:18` — `# Gates (24):` roster header present.
2. `CLAUDE.md` — `currently **24/24**` present; the composition-history sentence already ends
   "SCAN-GUARD (added under Phase 15, v8.26.0) moved it from 23 to 24"; the "22 `gate`/`gate_prereq`
   registrations plus two inline checks" tally sentence immediately follows it undisturbed.
3. `docs/ARCHITECTURE.md` — `**24 tallied in the offline battery**` and `21 + 1 + 2 = 24` both
   present.
4. `docs/README.md` — `battery 15/15 → 24/24` delta present (the arrow renders as `→`, matching the
   grep, which the shell here matches as a literal via the `/usr/bin/grep -c` count returning `1`).

All four surfaces were already correct — no drift found, no prose edit made. Per the plan's own
instruction ("Change nothing that is already right — a gratuitous edit to a correct sentence is
churn"), `CLAUDE.md`, `docs/ARCHITECTURE.md` and `scripts/check-firewall-battery.sh` were read and
verified but not modified in this task.

## Verification performed (observed, not assumed)

- `bash scripts/check-firewall-battery.sh > /tmp/16-04-battery-final.txt 2>&1; echo $?` → `0`;
  last line `FIREWALL: GREEN (24/24)`.
- `/usr/bin/grep -c "^\[FAIL\]" /tmp/16-04-battery-final.txt` → `0`.
- `/usr/bin/grep -c "^\[PREREQ\]" /tmp/16-04-battery-final.txt` → `0`.
- `/usr/bin/grep -c "^\[PASS\]" /tmp/16-04-battery-final.txt` → `24`.
- `python3 scripts/check-quality-harness.py --self-test; echo $?` → `0` (was `1` before the fix,
  with the exact `render_contract sub-check FAILED` line reproduced above).
- `/usr/bin/grep -oE '^[[:space:]]*(gate|gate_prereq) "[^"]+"' scripts/check-firewall-battery.sh |
  /usr/bin/grep -oE '"[^"]+"' | sort -u | wc -l` → `22`.
- `/usr/bin/grep -q "# Gates (24):" scripts/check-firewall-battery.sh` → match (exit 0).
- `/usr/bin/grep -q "currently \*\*24/24\*\*" CLAUDE.md` → match (exit 0).
- `/usr/bin/grep -q "21 + 1 + 2 = 24" docs/ARCHITECTURE.md` → match (exit 0).
- `/usr/bin/grep -c "battery 15/15 → 24/24" docs/README.md` → `1`.
- `git status --short` after the commit → clean (no untracked or uncommitted files besides this
  SUMMARY).
- `git diff --diff-filter=D --name-only HEAD~1 HEAD` after the fix commit → empty (no unexpected
  deletions).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1/Rule 3 - Bug, scope-authorized] Widened QUAL-01's stale four-anchor dispatch-reachability lock to five**
- **Found during:** Task 1, running the full battery per the plan's own `<action>`.
- **Issue:** `scripts/check-quality-harness.py`'s `render_u_required` set (control (u)) and its
  independent ENTRY-SOURCE LOCK restatement still hardcoded four `_selftest_*` anchor names. Wave 1
  (16-01) registered a new `LEDGER-04` matrix row whose `artifact_link` legitimately names a fifth,
  real, dispatched anchor (`_selftest_ledger_traceability`, a Phase-14 sub-check never previously
  named by any matrix row), which the derived symbol set (`_matrix_named_selftest_symbols()`) then
  picked up — failing the EQUALITY floor against the stale four-anchor lock.
- **Fix:** Added `_selftest_ledger_traceability` to both `render_u_required` and
  `render_x_entry_source_expected["(u) dispatch-reachability symbol set"]`, keeping the assertion an
  EQUALITY floor (not weakened to a subset test), and corrected three co-located comments that stated
  the anchor count as "four."
- **Files modified:** `scripts/check-quality-harness.py`.
- **Commit:** `d7a504b`.
- **Authorization:** explicitly scoped and pre-authorized by this plan's execution prompt (see
  `<scoped_deviation_authorized>`), which confirmed the cause and directed the exact fix; also
  anticipated by 16-04-PLAN.md's own Task 1 action text ("If any gate reports FAIL, fix the cause
  rather than the symptom") and named in `16-03-SUMMARY.md`/`deferred-items.md` as this plan's job.

### Environment fixes (not a code deviation)

**2. VAL-03 `[PREREQ] BLOCKED`** — this worktree's Python environment had no pytest-capable
interpreter. Ran `uv sync` per the plan's own interfaces section and the environment notes, creating
a gitignored `.venv` with pytest 9.1.1. No tracked files changed; `git status --short` was clean
before and after.

Task 2 found no drift on any of the four counting surfaces — nothing to fix, nothing committed for
that task.

## Known Stubs

None. This plan's only code change widens a hardcoded anchor-set lock in a validation script; no UI
or data-flow component is touched.

## Threat Flags

None. Per the plan's own threat model, T-16-12 (a BLOCKED run reported as satisfying SHIP-02) was
avoided by fixing the prerequisite rather than reclassifying it; T-16-13 (a stale gate-count claim)
was checked and found not to apply — no surface had drifted; T-16-14 (FROZEN-EVIDENCE) passed inside
the GREEN battery run; T-16-15 and T-16-SC are accepted with no applicable surface, unchanged by this
plan's edit (a validation-script fix, not a new dependency or executable surface in the shipped
plugin).

## Self-Check: PASSED

- `scripts/check-quality-harness.py` — FOUND (modified, commit `d7a504b`), contains
  `_selftest_ledger_traceability` in both `render_u_required` and the ENTRY-SOURCE LOCK registry.
- Commit `d7a504b` — FOUND in `git log --oneline`.
- `python3 scripts/check-quality-harness.py --self-test` re-run at summary time → confirmed exit 0.
- `bash scripts/check-firewall-battery.sh` re-run at summary time → confirmed `FIREWALL: GREEN
  (24/24)`, exit 0.
- `/tmp/16-04-battery-final.txt` — confirmed present, last line `FIREWALL: GREEN (24/24)`.
