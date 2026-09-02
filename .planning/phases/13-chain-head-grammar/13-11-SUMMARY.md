---
phase: 13-chain-head-grammar
plan: 11
subsystem: traceability, docs
tags: [dispatch-reachability, gap-closure, phase-close, WR-01, WR-02, WR-03, WR-09]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar (plans 01-10)
    provides: the chain-head grammar (R7/R8/R9) and its positional/scope disclosures
      (13-08, 13-09), the expected-verdict consumption floor (13-10), and the
      CR-02 dispatch-reachability leg this plan widens (13-06)
provides:
  - a dispatch-reachability leg in `scripts/check-traceability.py` that accepts
    BOTH self-test-anchor conventions in this repository (`_selftest_`/`self_test()`
    and `_self_test_`/`_run_self_test()`), including an `async def` dispatcher,
    proven by mutation to catch a deleted dispatch of `check-traceability.py`'s
    OWN `reproducible` row (SHIP-03's `_self_test_headline_lock`)
  - a widened `(h2)` live non-vacuity floor naming the three-member expected
    anchor set explicitly, and a second `(h3)` live positive for SHIP-03
  - two worked examples (`ishikawa-fishbone.md`, `composed-inversion-second-order.md`)
    speaking the input-inclusive Criterion 4 vocabulary R7 defines, instead of
    the pre-13-07 GT-presuming wording
  - both TRACE-03 doc rows (`CLAUDE.md`, `docs/ARCHITECTURE.md`) stating the
    widened leg's real reach, the A-02 QUAL-01 scope asymmetry, and the WR-02
    deferral with its reason
  - the phase's closing evidence: `_chain_block_well_formed` proven
    byte-identical across the whole 13-08..13-11 batch by two independent
    checks, the matrix artifacts proven unmoved by regenerate-and-diff, and
    `FIREWALL: GREEN (23/23)`
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A gate that checks another file's dispatch discipline while exempting
      its own hosting file's identical convention is not a hypothetical risk —
      it is exactly what happened here: `check-traceability.py` checked
      `_selftest_*`/`self_test()` reachability everywhere except in its own
      `_self_test_*`/`_run_self_test()` sub-checks, because the leg was
      authored against one file's naming convention and never re-examined
      against the file that hosts it."
    - "When two independent regex alternatives can each legitimately match a
      dispatcher, resolve ambiguity by construction (leftmost match via
      `.search()` over a single combined pattern) rather than by picking one
      arbitrarily, and record that the choice is deliberate and disclosed,
      verified against the live tree rather than assumed."

key-files:
  created: []
  modified:
    - scripts/check-traceability.py
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - shared/examples/ishikawa-fishbone.md
    - shared/examples/composed-inversion-second-order.md
    - first-principles/agents/references/examples/ishikawa-fishbone.md
    - first-principles/agents/references/examples/composed-inversion-second-order.md

key-decisions:
  - "A-01 confirmed by direct read before editing: `_self_test_headline_lock`
    IS dispatched from `_run_self_test()` at `scripts/check-traceability.py:5644`
    (pre-edit line numbers), and the next top-level construct after
    `def _run_self_test()` (`:5582`) is `def _run_emit(` at `:5658`, so the
    call sits inside the sliced body — widening the leg could not turn a
    currently-passing SHIP-03 row red for an unrelated reason."
  - "A-02 preserved exactly as scoped: `check-quality-harness.py`'s own
    `_MATRIX_SELFTEST_ANCHOR_RE`/`_matrix_named_selftest_symbols` twin was left
    untouched, reading only `_selftest_*` anchors from `check-traceability.py`'s
    source. The two-scripts independence property this pair provides therefore
    covers only `check-traceability.py`'s `_selftest_*`-prefixed matrix rows,
    not `check-traceability.py`'s own `_self_test_*` anchors (SHIP-03) — now
    covered by one detector (the widened leg itself), not two. Published as a
    new clause in leg (4) of both `| QUAL-01 |` doc rows."
  - "First-match-wins for a file with multiple dispatcher definitions is
    resolved by construction (`.search()` over one combined regex finds the
    leftmost match in the file) rather than by an explicit tie-break rule, and
    verified — not assumed — that neither file in this repository defines more
    than one of `self_test`/`_run_self_test` today (each has exactly one)."
  - "MUTATION 3 (async def _run_self_test) exit-0 finding recorded honestly
    rather than silently accepted at face value: when `_run_self_test` itself
    becomes `async def` in the scratch copy, the CLI's own un-awaited call site
    (`_run_self_test()` with no `await`, unchanged production code) produces an
    unawaited coroutine and a `RuntimeWarning`, so NONE of the self-test's
    internal checks execute — the observed `exit 0` is real but vacuous for
    that specific full-CLI run, not evidence the widened regex was exercised.
    The regex's actual async-recognition is independently and meaningfully
    proven by the (h1) synthetic case that calls `_selftest_dispatch_problems`
    directly with an in-memory `async def self_test():` string (no CLI
    execution path involved) — that case passes for the correct reason. Both
    facts are recorded below rather than picking the more flattering one."

requirements-completed: [CHAINHEAD-01, CHAINHEAD-07]

duration: ~1h40min
completed: 2026-09-02
---

# Phase 13 Plan 11: Widen the Dispatch-Reachability Leg and Close the Phase Summary

**Widened `check-traceability.py`'s CR-02 dispatch-reachability leg to accept both
self-test-anchor conventions this repository actually uses (closing WR-01 and WR-03),
reconciled the last two worked examples still quoting the pre-13-07 GT-presuming
Criterion 4 wording (closing WR-09), and closed the phase with the frozen chain
detector proven byte-identical across the entire four-plan gap-closure batch, the
matrix artifacts proven unmoved, and `FIREWALL: GREEN (23/23)`.**

## Performance

- **Duration:** ~1h40min
- **Tasks:** 3 completed (Task 3 produced no code change — see below)
- **Files modified:** 7 across two code commits

## Accomplishments

**Task 1 (WR-01, WR-03).** `_selftest_dispatch_problems` previously accepted only the
`_selftest_` anchor prefix and a hardcoded `^def self_test\(` dispatcher pattern —
`check-quality-harness.py`'s own conventions. `check-traceability.py` uses
`_self_test_*`/`_run_self_test()` for its own sub-checks (e.g. SHIP-03's
`_self_test_headline_lock`, a `reproducible` matrix row), so every one of them was
silently exempt from the exact CR-02 defect class (defined but never dispatched) this
leg exists to catch. Widened acceptance to a module-level `_SELFTEST_ANCHOR_PREFIXES =
("_selftest_", "_self_test_")` tuple and a `_SELFTEST_DISPATCHER_NAMES = ("self_test",
"_run_self_test")` tuple, combined into one regex alternation that also tolerates
`async def` (folding in WR-03, which the same file's own `_def_class_pat` two functions
up already carries an explicit `async\s+def` alternation to avoid — the two patterns no
longer disagree). Verified live before editing (A-01) that `_self_test_headline_lock`
really is dispatched from `_run_self_test()`, and that neither file in the repository
defines more than one dispatcher name today, so the "slice from the first match"
disclosed choice is currently inert. Added three new `(h1)` synthetic cases (a
`_self_test_*` anchor called from `_run_self_test()`, the same anchor defined but
uncalled, and an `async def self_test()` dispatcher calling its `_selftest_*` anchor),
widened `(h2)`'s non-vacuity floor from a two-member to a three-member expected anchor
set (adding `_self_test_headline_lock`), and added a second `(h3)` live positive
resolving SHIP-03's own artifact_link. Updated both TRACE-03 doc rows (`CLAUDE.md`,
`docs/ARCHITECTURE.md`) to state the widened reach and the still-open WR-02 false
negatives, and added a new clause to leg (4) of both QUAL-01 doc rows recording A-02:
`check-quality-harness.py`'s own independent detector stays scoped to
`check-traceability.py`'s `_selftest_*`-prefixed rows only, so the two-scripts
independence property does not extend to `check-traceability.py`'s own `_self_test_*`
anchors, which are now covered by one detector instead of two.

**Task 2 (WR-09).** Reworded the Criterion 4 justification in both
`shared/examples/ishikawa-fishbone.md` (`:329-330`) and
`shared/examples/composed-inversion-second-order.md` (`:312-313`) from "names the
GT-IDs consumed" / "names the GT-IDs it consumes" to "names the inputs it consumes —
here, ground truths — in the prescribed head form," matching the vocabulary R7 already
defines on all three canonical surfaces (`output-template.md`, `SKILL-body.md`,
`validation-rubric.md`). Both analyses' chains consume ground truths only, so the new
wording states that as a fact about these specific analyses (A-03) rather than
generalizing to composed upstream conclusions the analyses don't actually have. Also
updated "not from either GT alone" → "not from any single named input alone" to match
the reflow 13-07 made on the rubric. Regenerated via `sync-content.py --write`; the two
generated copies under `first-principles/agents/references/examples/` carry the same
correction. `git diff --stat shared/examples/` shows exactly 2 files changed, 8
insertions / 6 deletions — a vocabulary reconciliation, not a rewrite.

**Task 3 (phase close).** Produced no code change: every check in (a)-(c) passed and
(d)'s WR-02 deferral sentence was already landed by Task 1, exactly as the plan's own
"modifies no file" branch anticipates. See closing evidence below.

## Task Commits

1. **Task 1: Widen the dispatch-reachability leg** — `5aa8a21` (fix)
2. **Task 2: Reconcile the two worked examples** — `69a87ad` (fix)
3. **Task 3: Close the phase** — no code commit; SUMMARY.md only (`.planning/` is
   gitignored in this repository, same mechanical note every prior 13-0N-SUMMARY.md in
   this phase records)

## Mutation Reproductions (Task 1, all on a disposable `rsync -a --exclude .git
--exclude .venv` scratch copy under the session scratchpad; `git status --porcelain`
on the tracked tree confirmed empty — aside from this plan's own pending, uncommitted
edits at the time — before the first mutation and unchanged after every mutation cycle)

**MUTATION 1** — delete the `_self_test_headline_lock(wrong_results)` dispatch line
(WR-01's closure proof: before this task the same mutation left the gate green):
```
check-traceability --self-test: FAIL — V825-ROWS: 1 artifact_link issue(s), V825-ROWS: (h3) SHIP-03 live positive failed
  V825-ROWS FAIL: artifact_link issue — SHIP-03: anchor '_self_test_headline_lock' is defined in 'scripts/check-traceability.py' but is never called from _run_self_test() — a 'reproducible' tier pointing at a defined-but-never-dispatched sub-check is unenforced
  V825-ROWS FAIL: (h3) LIVE POSITIVE — SHIP-03 did not resolve cleanly: ["anchor '_self_test_headline_lock' is defined in 'scripts/check-traceability.py' but is never called from _run_self_test() — a 'reproducible' tier pointing at a defined-but-never-dispatched sub-check is unenforced"]
```
Exit 1, naming `_self_test_headline_lock` and `never called from`, as required.

**MUTATION 2** — revert `_SELFTEST_ANCHOR_PREFIXES` to `("_selftest_",)` alone:
```
check-traceability --self-test: FAIL — V825-ROWS: (h1) _self_test_ uncalled case failed, V825-ROWS: (h2) non-vacuity floor failed
  V825-ROWS FAIL: (h2) NON-VACUITY FLOOR — expected anchor set ['_self_test_headline_lock', '_selftest_chain_detector_pin', '_selftest_render_contract'], observed ['_selftest_chain_detector_pin', '_selftest_render_contract']
```
Exit 1, `(h2)`'s non-vacuity floor fires by name, naming the missing anchor, as
required. (The new `(h1)` `_self_test_` uncalled-case also fails as an expected
side-effect of narrowing the prefix set — not a separate defect.)

**MUTATION 3** — rename `def _run_self_test(` to `async def _run_self_test(`:
```
exit=0
scripts/check-traceability.py:5850: RuntimeWarning: coroutine '_run_self_test' was never awaited
  _run_self_test()
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
```
Exit 0, as the plan's acceptance criterion requires — WR-03's case. **Recorded finding
(not a defect, not fixed):** this specific full-CLI run's `exit 0` is real but for a
different reason than the widened regex being exercised. The production call site
`_run_self_test()` (unchanged, no `await`) now creates an unawaited coroutine when the
target function is `async def`, so the entire self-test body — every check, including
the (h1)/(h2)/(h3) blocks this plan added — never runs at all in this exact mutation;
Python emits `RuntimeWarning: coroutine '_run_self_test' was never awaited` and the
process exits 0 with no assertions evaluated. The widened regex's actual acceptance of
`async def self_test(...)` is independently and meaningfully proven by the (h1)
synthetic case added in this same task, which calls `_selftest_dispatch_problems`
directly with the in-memory literal `"async def self_test():\n    _selftest_x()\n"` —
no CLI dispatch path involved — and correctly reports no problem (see Task 1's
acceptance-criteria run above: `V825-ROWS PASS: (h1) an async def self_test() dispatcher
calling its anchor reports no problem — WR-03 closed`). Both observations are recorded
rather than presenting only the flattering one.

**MUTATION 4** — neutralize the new `(h1)` `_run_self_test`-uncalled case's assertion
(the condition's expected-substring literal was corrupted to a string that can never
appear in the real message, proving the assertion is wired to `wrong_results.append`
and not vacuous):
```
check-traceability --self-test: FAIL — V825-ROWS: (h1) _self_test_ uncalled case failed
  V825-ROWS FAIL: (h1) _self_test_/_run_self_test() uncalled case produced ["anchor '_self_test_x' is defined in 'f.py' but is never called from _run_self_test() — a 'reproducible' tier pointing at a defined-but-never-dispatched sub-check is unenforced"]
```
Exit 1, naming that `(h1)` case, as required.

`git status --porcelain` on the tracked tree: confirmed showing only this plan's own
pending edits (never a mutation artifact) before the first mutation and after the last;
all four mutations were applied to and reverted on the disposable scratch copy only.

## Frozen-Detector Proof (Task 3, batch-wide)

Baseline commit re-derived rather than trusted from the plan's transcription:
```
$ git log --oneline | grep '13-07' | head -1
b6ecc27 fix(13-07): sweep the whole-file-exempt v8.0-final-closure supersession record to 175/91/0/266
```
Matches the plan's stated baseline exactly.

`git diff b6ecc27..HEAD -- scripts/check-quality-harness.py` produces 27 hunks; every
hunk's starting line is either `122` (a single new import) or `6496` and later — well
clear of `_chain_block_well_formed`'s range (`4277`-`4397`, confirmed by locating its
`def` line and its terminal `return False`). No hunk falls inside the function.

Live digest recompute:
```
$ python3 -c "
import sys, importlib.util, hashlib
spec = importlib.util.spec_from_file_location('qh', 'scripts/check-quality-harness.py')
m = importlib.util.module_from_spec(spec); sys.modules['qh'] = m; spec.loader.exec_module(m)
print('sha256:' + hashlib.sha256(m._chain_detector_source().rstrip('\n').encode('utf-8')).hexdigest())
"
sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3
```
Matches `_CHAIN_DETECTOR_PINNED_DIGEST` exactly — no recompute was needed, the digest
just confirms what the pin already states.

## Matrix Artifacts (Task 3)

Regenerated into a confined `.planning/scratch-emit/` location (per
`_resolve_confined_output`'s `.planning/`-or-`docs/` rule), diffed byte-for-byte against
the committed artifacts, then deleted:
```
$ python3 scripts/check-traceability.py emit --md-output .planning/scratch-emit/requirements-matrix.md --json-output .planning/scratch-emit/matrix.json
check-traceability emit: PASS — 266 rows written
$ diff .planning/scratch-emit/requirements-matrix.md docs/requirements-matrix.md ; echo $?
0
$ diff .planning/scratch-emit/matrix.json docs/data/matrix.json ; echo $?
0
```
Both byte-identical. No row was added, removed, or re-tiered across the whole batch —
coverage headline confirmed unchanged: `grep -c '175 reproducible / 91 audit-only / 0
gap / 266 total' CLAUDE.md` → `1`. `git status --porcelain docs/` empty after the check.

## Battery and Sync (Task 3)

- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (23/23)`, exit 0.
  (Same remedy 13-07/13-08/13-09/13-10 all documented: this worktree had no `.venv`;
  `uv sync` created it from the committed lockfile, then the battery went green. No new
  dependency.)
- `python3 scripts/sync-content.py --check` → exit 0.
- `python3 scripts/check-traceability.py --self-test` → exit 0 (`PASS`).
- `python3 scripts/check-quality-harness.py --self-test` → exit 0, all sub-checks
  PASSED including `render_contract` and `chain_detector_pin`.
- Registration count check against 13-07's recorded pre-gap-closure baseline:
  `grep -c '23/23' CLAUDE.md` → `1` (matches); `grep -c 'gate ' scripts/check-firewall-battery.sh` → `52`
  (matches) — no gate registered, no CI job added across the whole four-plan batch.

## WR-02 Deferral (recorded, not fixed)

Both dispatch detectors (`check-traceability.py`'s `_selftest_dispatch_problems` and
`check-quality-harness.py`'s `_dispatch_reachability_problems`) count a mention of the
anchor inside a string literal or docstring as a dispatch, and the body slice runs to
the next top-level construct OR end of file — so when the dispatcher is the LAST
top-level construct in its file, trailing module-level code counts as dispatcher body.

**Reason for deferring rather than fixing in this plan:** it is latent — no such
mention exists in either file today, verified by grep before this plan and unchanged by
it — and the fix changes the slicing/matching semantics of a leg two gates (TRACE-03
and QUAL-01) now depend on. That wants its own falsifiability battery (new synthetic
cases proving a string-literal mention is correctly rejected and that trailing
module-level code is correctly excluded from the body), not a rider on a gap-closure
plan whose scope is WR-01/WR-03/WR-09. Published in both TRACE-03 doc rows
(`CLAUDE.md`, `docs/ARCHITECTURE.md`) as an explicit, named, open item rather than left
to inference — this is a recorded decision, not an omission, and should be picked up as
a milestone backlog item before either detector's slicing logic is next touched.

## Verification Findings Map

| Finding | Severity | Closed by | Evidence |
|---|---|---|---|
| BL-01 — R7's negative rule enforced only in trailing head position | Blocking | 13-08 (`5806b7b`, `aa217a5`, `492c3a5`) | Positional bound scoped on all three canonical surfaces, `R-HEAD-PROSE-MID` fixture pins the measured non-final-position bound |
| BL-02 — head-only scope note silent on GT-N-leading hops | Blocking | 13-09 (`65cf89e`, `3444579`, `16d1854`) | R9 registered on all three surfaces; `R-HEAD-GTHOP-BAD`/`R-HEAD-GTHOP-OK` pin both directions |
| BL-03 — consumption floor forgeable (membership set, not verdict) | Blocking | 13-10 (`cc3c7b3`, `1059097`, `bb6e483`) | `scored_verdicts` verdict-sequence recorder + expected-verdict floor + independent chain re-score (arm 4a) + control (v) delegation probe; both original bypasses reproduced closed in 13-10's own SUMMARY |
| WR-01 — dispatch-reachability leg exempt for `check-traceability.py`'s own `_self_test_*` anchors | Warning | 13-11 Task 1 (`5aa8a21`) | Widened `_SELFTEST_ANCHOR_PREFIXES`; MUTATION 1 above proves SHIP-03's dispatch is now genuinely checked |
| WR-02 — string-literal / trailing-module-level-code false negatives in the dispatch leg | Warning | **Deferred, not fixed** — recorded in both TRACE-03 doc rows with reason (this plan, `5aa8a21`) | See "WR-02 Deferral" above |
| WR-03 — dispatcher pattern does not recognise `async def` | Warning | 13-11 Task 1 (`5aa8a21`), folded in per the plan's own instruction | `_SELFTEST_DISPATCHER_PAT`'s `(?:async\s+)?` prefix; (h1) synthetic case and MUTATION 3's isolated proof above |
| WR-04 — sha256 pin hashes the ~150-line docstring, gating an editorial-only fix behind an amendment process | Info (procedural friction, not a defect) | Not in this plan's scope; documented in `13-VERIFICATION.md` as a WARNING affecting future edits to the pinned function, not a closable finding of this batch | No action taken — out of scope |
| WR-09 — two worked examples still quote pre-13-07 GT-presuming Criterion 4 wording | Warning | 13-11 Task 2 (`69a87ad`) | Both examples reworded to input-inclusive vocabulary; `grep -rn 'GT-IDs consumed\|GT-IDs it consumes' shared/ first-principles/` → no matches |

(WR-04 is listed for completeness since it appears in `13-VERIFICATION.md`'s Anti-Patterns
table; it was not one of this plan's `closes_gaps` and required no action here.)

## Deviations from Plan

### Auto-fixed Issues

None — no bug, missing functionality, or blocking issue was found that required
deviation from the plan's literal instructions. All three tasks landed as specified.

### Findings (not fixed — measured, not corrected to match a prediction)

**1. MUTATION 3's `exit 0` is real but vacuous for a reason the plan did not name**
- **Found during:** Task 1's acceptance-criteria verification, MUTATION 3.
- **Detail:** See "MUTATION 3" under Mutation Reproductions above. The plan's acceptance
  criterion ("The self-test MUST still exit 0 — WR-03's case") is satisfied literally,
  but the mechanism is an unawaited-coroutine no-op (the CLI's own unchanged, non-`await`
  call site), not a genuine end-to-end exercise of the widened async-recognizing regex.
  The regex itself IS correctly proven via the (h1) synthetic case added in the same
  task, which calls the pure function directly.
- **Disposition:** Recorded as measured, not corrected. No code or fixture change was
  made to force the full-CLI mutation to exercise the internals — doing so would mean
  either awaiting a coroutine in a codepath that must stay synchronous in production, or
  fabricating a scenario the real tree can never encounter (the actual `_run_self_test`
  is never `async def`). The (h1) case already provides the meaningful proof.

## Self-Check: PASSED

- `scripts/check-traceability.py` — FOUND, contains `_SELFTEST_ANCHOR_PREFIXES`,
  `_SELFTEST_DISPATCHER_NAMES`, `_SELFTEST_DISPATCHER_PAT`, and the widened `(h1)`/`(h2)`/`(h3)` blocks.
- `CLAUDE.md` — FOUND, TRACE-03 row states the widened reach and WR-02 deferral; QUAL-01
  row's leg (4) states the A-02 clause.
- `docs/ARCHITECTURE.md` — FOUND, same two rows updated identically.
- `shared/examples/ishikawa-fishbone.md` — FOUND, contains "the inputs it consumes".
- `shared/examples/composed-inversion-second-order.md` — FOUND, contains "the inputs it consumes".
- `first-principles/agents/references/examples/ishikawa-fishbone.md` — FOUND, regenerated copy matches.
- `first-principles/agents/references/examples/composed-inversion-second-order.md` — FOUND, regenerated copy matches.
- Commit `5aa8a21` — FOUND in `git log --oneline`.
- Commit `69a87ad` — FOUND in `git log --oneline`.
- `grep -c '_SELFTEST_ANCHOR_PREFIXES' scripts/check-traceability.py` → `4` (≥ 2, required).
- `grep -c '_SELFTEST_DISPATCHER_NAMES' scripts/check-traceability.py` → `4` (≥ 2, required).
- `grep -c '_self_test_headline_lock' scripts/check-traceability.py` → `20`, up from a
  pre-task value of `13` (increase of `7`, ≥ 2 required).
- `grep -rn 'GT-IDs consumed\|GT-IDs it consumes' shared/ first-principles/` → no matches.
- `_CHAIN_DETECTOR_PINNED_DIGEST` — confirmed unchanged
  (`sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3`); live
  recompute matches; `git diff b6ecc27..HEAD` shows no hunk inside
  `_chain_block_well_formed`'s line range.
- `docs/requirements-matrix.md`, `docs/data/matrix.json` — regenerate-and-diff both
  byte-identical; `git status --porcelain docs/` empty.
- `bash scripts/check-firewall-battery.sh` — re-run after both commits landed:
  `FIREWALL: GREEN (23/23)`, exit 0.
- `python3 scripts/sync-content.py --check` — exit 0.
- `python3 scripts/check-traceability.py --self-test` — exit 0 (`PASS`).
- `python3 scripts/check-quality-harness.py --self-test` — exit 0, all sub-checks PASSED.
- `git status --porcelain` — empty, confirmed after all four mutations (all run on a
  disposable scratch copy, never the tracked tree).
