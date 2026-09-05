---
phase: 13-chain-head-grammar
plan: 16
subsystem: quality-harness (QUAL-01 self-test)
tags: [gap-closure, falsifiability, chain-head-grammar]
dependency-graph:
  requires: ["13-15"]
  provides: ["ENTRY-SOURCE LOCK (control x)", "extended (t) SCORING RECORDER LOCK census"]
  affects: ["scripts/check-quality-harness.py"]
tech-stack:
  added: []
  patterns:
    - "pure problem-reporting helper + module-level registry + source-text call-site census"
key-files:
  created: []
  modified:
    - scripts/check-quality-harness.py
decisions: []
metrics:
  duration: "~2.5 hours (agent wall-clock)"
  completed: 2026-09-03
---

# Phase 13 Plan 16: Close both round-4 blocking gaps against criterion 3 / CHAINHEAD-05 Summary

Added `_render_entry_source_problems` (control (x)'s ENTRY-SOURCE LOCK, four synthetic isolation
arms x6-x9) to reject a coverage-floor registry entry whose `required` side is rebound to its own
`actual` side or to the wrong value (R4-CR-02), and extended control (t)'s source-text call-site
census with three re-derived counters covering the coverage-floor-registry, worked-example-
conformance, and entry-source helpers (R4-CR-01) — closing both round-4 forgeries the verifier
independently reproduced while `FIREWALL: GREEN (23/23)`.

## What Was Built

**Task 1 — ENTRY-SOURCE LOCK (R4-CR-02).** A new pure helper,
`_render_entry_source_problems(entries, expected_required_by_name)`, sited immediately after
`_render_coverage_floor_problems` in `scripts/check-quality-harness.py`. It reports four
independent problem shapes over a coverage-floor entry registry:

- UNREGISTERED — an entry name absent from the expectation map.
- WRONG SOURCE — an entry whose `required` side does not equal its registered expectation,
  reported with sorted MISSING/UNEXPECTED, matching `_render_coverage_floor_problems`'s own shape.
- ALIASED — an entry whose `required` side `is` the same object as its `actual` side. Kept
  independent of WRONG SOURCE deliberately: in the passing state every entry's two sides are equal
  by VALUE (that is what passing means), so only object identity can catch a rebind to the entry's
  own actual side.
- MISSING ENTRY — a name registered in the expectation map with no matching registry entry.

Control (x) now carries a new `(x) ENTRY-SOURCE LOCK` block, positioned after the existing
REGISTRY MEMBERSHIP LOCK and before THE FLOOR ITSELF, which builds the expectation map by
RE-DERIVING each required side from primary sources at lock time (a fresh call to
`_render_chain_family_ids` for arm 4a — not the local `render_chain_family_ids` variable, which is
exactly what MUTATION M2 exercises; the full locked-id set for arm 4b; and a second, independent
transcription of control (u)'s four locked dispatch anchors). Four synthetic isolation arms
(x6-x9) drive the new helper with literals only, mirroring the x1-x5 arms' discipline.

**Task 2 — extended call-site census (R4-CR-01).** Control (t)'s SCORING RECORDER LOCK gained
three new source-text call-site counters, built with the same concatenation idiom
(`"<name>" + "("`) as the two existing counters, counted over
`inspect.getsource(_selftest_render_contract)`:

- coverage-floor-registry helper (`_render_coverage_floor_problems`): expected **6**.
- worked-example-conformance helper (`_render_example_conformance_problems`): expected **6**.
- entry-source helper (`_render_entry_source_problems`, this plan's own Task 1 fix): expected **5**.

All three floored in the existing composite `if` condition, with the `_fail` message extended to
report each observed count against its expected value.

**Task 3 — closing evidence.** `_chain_block_well_formed` proven byte-unchanged across the whole
plan; the sha256 pin unaffected; coverage headline unmoved; sync clean; battery GREEN 23/23.

## Derived Census Enumeration (Task 2, hard constraint 3 — re-derived, not transcribed)

Enumerated with `grep -n "_render_coverage_floor_problems(\|_render_example_conformance_problems(\|_render_entry_source_problems(" scripts/check-quality-harness.py` and cross-checked against
`inspect.getsource(_selftest_render_contract)`'s own pattern count (verified live via a small
script importing the module and calling `inspect.getsource`):

| Helper | Real call(s) | Isolation call(s) | Total (observed == expected) |
|---|---|---|---|
| `_render_coverage_floor_problems` | 1 (THE FLOOR ITSELF) + 1 (leg 5's own reuse for the `(y)` NON-VACUITY floor) = 2 | x1, x2, x3, x4 = 4 | **6 == 6** |
| `_render_example_conformance_problems` | 1 (THE LEG ITSELF) | z5, z6, z7, z8, z9 = 5 | **6 == 6** |
| `_render_entry_source_problems` | 1 (the ENTRY-SOURCE LOCK) | x6, x7, x8, x9 = 4 | **5 == 5** |

The `def` lines (module level, outside `_selftest_render_contract`) are correctly excluded from
every count — verified by comparing the file-wide grep count (which includes the `def` line) against
the `inspect.getsource`-scoped count (which does not): coverage-floor-registry file-wide grep found
7 (1 def + 6 in-function); example-conformance file-wide grep found 7 (1 def + 6 in-function);
entry-source file-wide grep found 6 (1 def + 5 in-function). All three reconcile exactly.

## Mutations M1-M9 (verbatim, all on `rsync -a --exclude .git --exclude .venv --exclude .planning`
scratch copies — never the tracked tree)

| Mutation | Command / edit | Exit code | Failure line (arm named) |
|---|---|---|---|
| Baseline (post-Task-1 scratch, unmutated) | `python3 scripts/check-quality-harness.py --self-test` | 0 | `render_contract sub-check PASSED` |
| **M1** | arm 4a's registry `required` side changed to `frozenset(render_chain_verdict_expected)`; `render_chain_verdict_expected` narrowed 9→6 (deleted `R-HEAD-PROSE-MID`, `R-HEAD-GTHOP-BAD`, `R-HEAD-GTHOP-OK`) | **1** | `self-test FAIL: render_contract (x) ENTRY-SOURCE LOCK: arm 4a chain re-score table: WRONG SOURCE — required [...6 ids...] != expected [...9 ids...] — MISSING ['R-HEAD-GTHOP-BAD', 'R-HEAD-GTHOP-OK', 'R-HEAD-PROSE-MID'], UNEXPECTED []` |
| **M1 anti-masking** | ENTRY-SOURCE LOCK block, helper def, and x6-x9 isolation arms deleted from the scratch copy, M1 still applied | **0** | `render_contract sub-check PASSED` — proves the new arm, alone, catches M1 |
| **M2** | inserted `render_chain_family_ids = set(render_chain_verdict_expected)` immediately before `render_coverage_floor_entries` is constructed, plus the same 9→6 narrowing | **1** | `(x) ENTRY-SOURCE LOCK: arm 4a chain re-score table: WRONG SOURCE — ...` (identical shape to M1; no other arm fired — DERIVATION NON-VACUITY stayed silent because the rebound `render_chain_family_ids` is still a non-empty proper subset) |
| **M3** | one frozenset object (`render_m3_shared`) bound to BOTH the `actual` and `required` sides of the arm-4a entry, no narrowing anywhere | **1** | `(x) ENTRY-SOURCE LOCK: arm 4a chain re-score table: ALIASED — the required side is bound to the SAME OBJECT as the actual side, so this entry cannot report a coverage-floor problem` — WRONG SOURCE did **not** fire (values equal), proving the two shapes are independent |
| **M4** | added a fourth entry (`"m4 fourth entry"`) to `render_coverage_floor_entries` and its name to `render_x_expected_entry_names` so REGISTRY MEMBERSHIP LOCK passes | **1** | `(x) ENTRY-SOURCE LOCK: m4 fourth entry: UNREGISTERED — no entry-source expectation is registered for this arm name` |
| **M5** | deleted `"arm 4b recorded-verdict table"` from the lock's own expectation map, registry left whole | **1** | `(x) ENTRY-SOURCE LOCK: arm 4b recorded-verdict table: UNREGISTERED — no entry-source expectation is registered for this arm name` |
| **M6** | leg 5's real scoring block (`for render_y_problem in _render_example_conformance_problems(...): _fail(...)`) replaced with `pass`, examples on disk untouched | **1** | `(t) SCORING RECORDER LOCK: ... 5 worked-example-conformance helper call site(s) (expected 6) ...` |
| **M6 anti-masking** | the three new counters removed from control (t)'s condition and message, M6 still applied | **0** | `render_contract sub-check PASSED` |
| **M7** | M6 plus both `shared/examples/ishikawa-fishbone.md` and `shared/examples/composed-inversion-second-order.md` restored from commit `9ce0234` (the verifier's verbatim round-4 scenario) | **1** | same `(t) SCORING RECORDER LOCK` failure as M6 (`5 worked-example-conformance helper call site(s) (expected 6)`) — confirmed the identical scenario against the **pre-plan tree** (checked out at `df345acac900c819f9ab495e7260486baffbb919` via `git archive`) exits **0**, `render_contract sub-check PASSED` |
| **M8** | control (x)'s real `THE FLOOR ITSELF` call block replaced with `pass` | **1** | `(t) SCORING RECORDER LOCK: ... 5 coverage-floor-registry helper call site(s) (expected 6) ...` |
| **M8 anti-masking** | the three new counters removed from control (t)'s condition and message, M8 still applied | **0** | `render_contract sub-check PASSED` |
| **M9** | Task 1's ENTRY-SOURCE LOCK real call block replaced with `pass` | **1** | `(t) SCORING RECORDER LOCK: ... 4 entry-source helper call site(s) (expected 5) ...` |
| **M9 anti-masking** | the three new counters removed from control (t)'s condition and message, M9 still applied | **0** | `render_contract sub-check PASSED` |
| **CONTRAST** | the older, already-counted arm-4a re-score call (`_render_chain_verdict_floor_problems`) deleted, replaced with `pass` | **1** | `(t) SCORING RECORDER LOCK: ... 5 chain-verdict-floor-helper call site(s) (expected 6) ...` — unchanged from before this plan, confirming the census's pre-existing coverage is intact |

## x6-x9 Isolation Sweep (each neutralized alone, one new failure per arm)

| Arm | Neutralization | Exit code | Failure line |
|---|---|---|---|
| x6 CLEAN | `!=` inverted to `==` | 1 | `(x) ISOLATION x6 CLEAN: a matching entry wrongly reported a problem: []` |
| x7 WRONG SOURCE | condition inverted (`!=`/`or` → `==`/`and`) | 1 | `(x) ISOLATION x7 WRONG SOURCE: expected exactly one problem naming 'x7 WRONG SOURCE' and the differing id 'B', got [...]` |
| x8 UNREGISTERED | condition inverted | 1 | `(x) ISOLATION x8 UNREGISTERED: expected exactly one problem naming 'x8 UNREGISTERED', got [...]` |
| x9 ALIASED | condition inverted | 1 | `(x) ISOLATION x9 ALIASED: expected exactly one problem naming 'x9 ALIASED' and identifying the aliasing, got [...]` |

## `_chain_block_well_formed` Byte-Identity Evidence

- Function range at HEAD: lines **4277-4397** (`def _chain_block_well_formed` at 4277; next
  `def _chain_detector_source` at 4400) — unchanged from the plan's starting commit
  `df345acac900c819f9ab495e7260486baffbb919`, since every diff hunk in this plan starts at line
  6728 or later in the old file.
- `git diff df345acac900c819f9ab495e7260486baffbb919 HEAD -- scripts/check-quality-harness.py`
  hunk headers: `@@ -6728,...`, `@@ -10004,...`, `@@ -10027,...`, `@@ -10040,...`, `@@ -10050,...`,
  `@@ -10218,...`, `@@ -10315,...` — none overlaps 4277-4397, and `grep -c "_CHAIN_DETECTOR_PINNED_DIGEST"`
  over the same diff returns **0**.
- `_CHAIN_DETECTOR_PINNED_DIGEST` at line 4436, value `"sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3"` — unchanged.
- `python3 scripts/check-quality-harness.py --self-test`: `chain_detector_pin` sub-check PASSED.

## Verification Results (real tree, HEAD, no mutation)

1. `python3 scripts/check-quality-harness.py --self-test` — **EXIT 0**, `render_contract sub-check
   PASSED`, `chain_detector_pin sub-check PASSED`.
2. `python3 scripts/check-traceability.py --self-test` — **EXIT 0**; live headline via
   `_headline_literals()`: `('175/91/0/266', '175 reproducible / 91 audit-only / 0 gap / 266
   total')` — unchanged, no matrix row registered by this plan.
3. `python3 scripts/sync-content.py --check` — **EXIT 0**, no drift.
4. `bash scripts/check-firewall-battery.sh` — final line **`FIREWALL: GREEN (23/23)`**, EXIT 0.
   (First run reported `FIREWALL: BLOCKED` — exit 2, a prerequisite failure per CLAUDE.md's
   documented VAL-03 distinction, not a gate failure — because no pytest-capable interpreter
   existed yet. Ran `uv sync` to create `.venv` with pytest 9.1.1, then re-ran the battery to
   GREEN. `.venv` is already gitignored.)
5. `git status --porcelain` — empty before the first mutation, empty after the last (all mutation
   work ran on `rsync`-excluded scratch copies under the session scratchpad, all cleaned up
   afterward).

## Deviations from Plan

None — plan executed exactly as written. One environmental prerequisite gap was resolved per the
plan's own acceptance-criteria guidance (Task 3: "Exit 2 / `FIREWALL: BLOCKED` is a prerequisite
failure, not a pass — resolve the pytest interpreter (`uv sync`...) and re-run"), not a deviation
from the plan's scope.

## Self-Check: PASSED

- `scripts/check-quality-harness.py` — FOUND (modified, both task commits present).
- Commit `dc3f891` (Task 1) — FOUND in `git log --oneline`.
- Commit `fea3336` (Task 2) — FOUND in `git log --oneline`.
- `python3 scripts/check-quality-harness.py --self-test` — re-run at HEAD, EXIT 0, confirmed.
- `bash scripts/check-firewall-battery.sh` — re-run at HEAD, `FIREWALL: GREEN (23/23)`, confirmed.
- `git status --porcelain` on the real tree — empty, confirmed.
