---
phase: 14-closure-ledger-claim-inventory
plan: 04
subsystem: testing
tags: [quality-harness, render-contract, claim-inventory, fixtures, self-test]

# Dependency graph
requires:
  - phase: 14-closure-ledger-claim-inventory (plan 02)
    provides: "R11's three disclosed bounds and R12's caveat-marker rule as byte-identical literals, plus nine worked-example blocks in output-template.md §6"
  - phase: 14-closure-ledger-claim-inventory (plan 03)
    provides: "R11/R12 and the amended R4 registered in _RENDER_RULE_LITERALS, _RENDER_SURFACE_REQUIRED_RULES and expected_literal_clauses"
provides:
  - "Nine claim-bound fixtures (R-CLAIM-LABEL-BARE/INLINE/CITED, R-CLAIM-COLON-MID/END, R-CLAIM-TERSE-DROP/KEEP, R-CLAIM-CAVEAT-MARKED/CITED) registered in _RENDER_CONTRACT_EXTRACTION_TABLE, _RENDER_FIXTURE_SHAPE and _RENDER_FIXTURE_FORBIDDEN, plus every registry lock mirror"
  - "_render_claim_bound_problems, a parameterised helper scoring R11's three bounds and R12's marker via the unmodified _conclusion_claims/_claim_is_traced"
  - "Every fixture-population floor (render_locked_fixture_ids, render_verdict_expected arm 4b, control (x)'s entry-source transcription, control (t)'s recorder-mutation census) moved from eighteen to twenty-seven ids"
affects: [15-scan]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A parameterised scoring helper (_render_claim_bound_problems) that derives its per-id dispatch (single-call vs two-call-with-punctuation-toggle) from the shape of its own *expected* parameter, and its scorer-family dispatch (claim vs traced) from a function-local literal id set — never a module-level constant — so a call site wiring the wrong table or the wrong scorer becomes unexpressible"
    - "A fixture pair scored twice with a mutated variant, in memory, when the needle-uniqueness discipline forces two blocks to be worded differently rather than as a true minimal pair — recovers the minimal-pair property mechanically instead of at the fixture-text level"

key-files:
  created: []
  modified:
    - scripts/check-quality-harness.py

key-decisions:
  - "Q2 (planner decision, carried forward): extended _selftest_render_contract in place for the wiring (locked-id sets, expected-verdict tables, control (t)'s census) while extracting the new scoring logic into a module-scope helper (_render_claim_bound_problems) — not a wholesale split of the 3,200+ line function, which no LEDGER requirement authorizes"
  - "The helper's own 'problems' list and arm 4b's pre-existing _render_verdict_floor_problems both independently compare recorded verdicts against expected — deliberate defense-in-depth matching the existing R-CITE-*/R-VERDICT-* precedent, not redundancy to be trimmed"
  - "Chain ids C1 (LABEL/COLON/TERSE family) and C5 (CAVEAT pair) are derived inside the helper from a single function-local traced_ids set, not passed as a separate parameter — keeps the helper's signature at exactly the four parameters the plan specifies"

patterns-established:
  - "A fixture-population helper's *expected* dict[str, list[bool]] parameter is read for two purposes at once — which ids to process, and (via list length) how many times to score each — rather than only for post-hoc comparison"

requirements-completed: [LEDGER-03, LEDGER-04]

# Metrics
duration: ~55min
completed: 2026-09-03
---

# Phase 14 Plan 04: Wire the Claim-Extraction Fixtures Into Every Floor Summary

**Registered nine worked-example fixtures pinning R11's three claim-extraction bounds and R12's caveat-marker rule, scored them through a new parameterised helper (`_render_claim_bound_problems`) that calls the unmodified `_conclusion_claims`/`_claim_is_traced` directly, and moved every accounting floor in `_selftest_render_contract` from eighteen to twenty-seven registered ids — verified by execution (firewall battery GREEN 23/23) and by seven scratch-copy mutation probes, not by reading.**

## Performance

- **Duration:** ~55 min
- **Tasks:** 2 completed (2 commits, one per task)
- **Files modified:** 1 (`scripts/check-quality-harness.py`)

## Accomplishments

- `_RENDER_CONTRACT_EXTRACTION_TABLE` gained nine rows (all `shared/spine/references/output-template.md`, `fenced-block`) for `R-CLAIM-LABEL-BARE/INLINE/CITED`, `R-CLAIM-COLON-MID/END`, `R-CLAIM-TERSE-DROP/KEEP` and `R-CLAIM-CAVEAT-MARKED/CITED`, mirrored into `_RENDER_FIXTURE_SHAPE` (each with a uniqueness-verified discriminating needle — confirmed by direct per-needle count against the live template, all exactly 1) and `_RENDER_FIXTURE_FORBIDDEN` (two new guards: `R-CLAIM-LABEL-BARE` forbids `"C1"`, `R-CLAIM-CAVEAT-MARKED` forbids `"C5"`).
- `_render_registry_lock_problems`'s `expected_ids`, the authoritative four-column `expected_extraction_rows`, `expected_fixture_shape` (every new id gets a full-value needle tuple from the start, never a `()` tier) and `expected_forbidden` all extended to match — `_render_contract_fixtures()` now reads and shape-validates all 27 fixtures cleanly (confirmed by direct execution, zero problems).
- New module-scope helper `_render_claim_bound_problems(expected, fixtures, claim_scorer, traced_scorer)`, placed beside `_render_fixture_accounting_problems`, copying its "inputs as parameters, no module constant read" purity discipline. It dispatches each of the nine ids to either `claim_scorer` (R11's three bounds, against chain id `"C1"`) or, for the two caveat ids, `claim_scorer` then `traced_scorer` (against chain id `"C5"`) — with the TERSE pair scored TWICE, once as extracted and once with the trailing period toggled in memory, mechanically proving the assertiveness axis is punctuation rather than the wording difference Task 1's needle-uniqueness discipline forced the pair to give up at the text level. Verified standalone against all nine real fixtures (exact match to expected verdicts) and against four synthetic isolation scenarios (missing fixture, verdict mismatch, anti-masking, empty table) before wiring it in.
- Wired into `_selftest_render_contract` as a new control `(aa)`, placed with the other fixture-scoring controls (after (g), before (p)): nine new `_get()` calls (satisfying the consumption floor's `requested_ids` arm), the helper call, a merge of its returned verdicts into `scored_verdicts` via `.setdefault(...).extend(...)`, and `_fail` messages naming both the fixture id and its doc label for any returned problem.
- Every accounting floor moved from eighteen to twenty-seven: `render_locked_fixture_ids`, `render_verdict_expected` (arm 4b, all nine new verdict lists including the two-call `[False, True]`/`[True, False]` pair), control (x)'s independent second transcription (arm 4b entry-source expectation), and control (t)'s recorder-mutation census (four wrapper `.setdefault` sites plus the new merge call = five). `render_chain_verdict_expected` (arm 4a, thirteen) is unchanged — the new ids carry the `R-CLAIM-` prefix specifically so they stay out of the chain family, whose single-argument scorer cannot score them.
- `python3 scripts/check-quality-harness.py --self-test` exits 0, all sub-checks PASSED including `render_contract`. `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (23/23)` (required `uv sync` to create a local `.venv` — same one-time VAL-03 pytest-interpreter setup plans 14-01/14-02/14-03 documented). `python3 scripts/sync-content.py --check` exits 0 (no drift; this plan touches only `scripts/`, no `shared/` or generated-tree files).
- `_conclusion_claims`, `_claim_is_traced` and `_chain_block_well_formed` (plus its sha256 pin) are byte-unchanged — confirmed by `git diff` naming no hunk inside any of the three across both commits.

## Task Commits

Each task was committed atomically:

1. **Task 1: Register the nine fixtures in the extraction table, shape lock and forbidden map** - `ad517a0` (feat)
2. **Task 2: Score the nine fixtures through a parameterised helper, and wire every floor** - `30286a4` (feat)

_No TDD tasks in this plan._

## Files Created/Modified

- `scripts/check-quality-harness.py` — nine `R-CLAIM-*` fixtures registered across the extraction table, shape lock and forbidden map (Task 1); `_render_claim_bound_problems` added, control `(aa)` wired into `_selftest_render_contract`, and every accounting floor (`render_locked_fixture_ids`, arm 4b, control (x)'s entry-source transcription, control (t)'s census) moved from eighteen to twenty-seven (Task 2)

## Decisions Made

- Q2 (carried forward from the plan's own objective): extended `_selftest_render_contract` in place for wiring, extracted only the new scoring logic into `_render_claim_bound_problems`. Net measured growth of `_selftest_render_contract` itself is +109 lines (3201 -> 3310, measured against the base commit, not the ~3,203 the plan's Q2 text estimated from an earlier reading) — more than the "roughly twenty lines" Q2 predicted for the wiring alone, because the wiring includes two full dict literals (doc labels, expected verdicts) and a fixtures-assembly dict, not just the helper call itself. Still far short of the "two hundred" an inline (non-extracted) implementation would have added; the new scoring logic itself lives entirely in the separately-measured 109-line helper, outside the function. Recorded here as an observed correction to the plan's estimate, not a defect — nothing in the acceptance criteria gates on an exact line count.
- The helper computes verdicts AND compares them to `expected` internally (emitting its own `claim-bound: verdict mismatch` problems), rather than delegating verdict-correctness solely to the pre-existing arm-4b floor. This was required by Task 2's own acceptance criterion (ii): "a table whose expected verdict disagrees with what the supplied scorer returns must produce a NAMED problem" — an isolation requirement the helper itself must satisfy, independent of arm 4b. The resulting duplication (both the helper's own comparison and arm 4b's separate comparison against `scored_verdicts`) mirrors the existing precedent for `R-CITE-*`/`R-VERDICT-*` fixtures, where control (f)'s inline assertions and arm 4b's floor already check the same thing twice.
- Chain ids `"C1"`/`"C5"` and the caveat/non-caveat dispatch are derived inside the helper from one function-local `traced_ids = {"R-CLAIM-CAVEAT-MARKED", "R-CLAIM-CAVEAT-CITED"}` set (not a module-level constant, and not a fifth parameter) — satisfies the acceptance criterion that the helper's body reference no module-level name while keeping its signature at exactly the four parameters (`expected`, `fixtures`, `claim_scorer`, `traced_scorer`) the plan specifies.
- The two-call TERSE mutation (period append/strip) is derived generically from `len(expected_verdicts) == 2` inside the helper, rather than hardcoded per fixture id — only the caveat/non-caveat family split and the C1/C5 chain-id choice are id-literal-based. This keeps the helper closer to a general two-scorer dispatcher than a hardcoded nine-branch table, while still satisfying every stated acceptance criterion (verified against the real fixtures and against four synthetic isolation cases with no real ids at all).

## Eighteen -> Twenty-Seven Sweep (per-occurrence, as required by the plan)

Thirteen total case-insensitive occurrences of "eighteen" existed in the file before this plan. Seven were fixture-table-total claims and were moved to "twenty-seven"; six were left unchanged, each for a stated reason:

| Line (pre-edit) | Text (excerpt) | Decision | Reason |
|---|---|---|---|
| `_render_contract_fixtures` docstring | "Read all eighteen Phase 11/13 ... fixtures" | **MOVED** -> "twenty-seven Phase 11/13/14" | Direct fixture-table-total claim; explicitly named in the plan's interfaces item 4 |
| `_render_registry_lock_problems` comment | "(...the table now carries eighteen rows.)" | **MOVED** -> "twenty-seven rows" | Present-tense claim about `_RENDER_CONTRACT_EXTRACTION_TABLE`'s current row count |
| `_selftest_render_contract` comment (consumption floor, first mention) | "that set against a locked eighteen-id set written inline" | **MOVED** -> "twenty-seven-id set" | Describes `render_locked_fixture_ids`'s current size; explicitly named in interfaces item 6 |
| `_selftest_render_contract` comment (consumption floor, second mention) | "The locked eighteen-id set below is written INLINE" | **MOVED** -> "twenty-seven-id set" | Same referent as above, restated near the dict literal |
| `(p) EXPECTED-VERDICT FLOOR — arm 4b` comment | "covers all EIGHTEEN locked ids" | **MOVED** -> "TWENTY-SEVEN locked ids" | Direct description of `render_verdict_expected`'s current id count; explicitly named in interfaces item 6 |
| `(x) COVERAGE FLOOR REGISTRY` comment | "arm 4b's recorded-verdict table (against all eighteen locked ids)" | **MOVED** -> "twenty-seven locked" | Describes the same arm-4b total from the coverage-floor registry's perspective |
| `(x) ENTRY-SOURCE LOCK` comment | "is a SECOND, independent transcription of the eighteen locked fixture ids" | **MOVED** -> "twenty-seven locked" | Describes `render_x_entry_source_expected`'s arm-4b entry, which this plan extends; explicitly named in interfaces item 6 |
| `_RenderRegistrySnapshot` docstring | "(nineteen today, eighteen registries: the extraction table contributes both...)" | **left unchanged** | Counts `_RENDER_REGISTRY_FIELDS` (registries the whole render-contract mechanism tracks: surfaces, literals, chain-form signature, etc.) — unrelated to the fixture-table id count this plan changes; no registry was added or removed |
| `_render_registry_lock_problems` comment (WR-01 narrative) | "...that silently disables the mode-2 shape guard for five of the eighteen fixtures..." | **left unchanged** | Entirely retrospective prose about the WR-01 historical finding, describing the table's size AT THAT PAST MOMENT (18) — not a claim about the current total, the same treatment the adjacent "Eleven was the table's size at Phase 11" sentence already receives |
| `_selftest_render_contract` docstring | "Controls (a)-(b) pin the eighteen measured verdicts." | **left unchanged** | Out of scope: controls (a)/(b) together actually pin 13 chain-family verdicts (extraction + the chain-block scoring family), not 18 — this sentence's literal referent was already imprecise before this plan and is not one of the sites the plan's `<interfaces>` section names; changing it would not make it accurate (it would need to say "thirteen", not "twenty-seven"), so it is flagged here rather than silently "fixed" outside this plan's stated scope |
| `run_layer`/rejudge-harness region (x3) | "re-dispatch all eighteen successful invocations", "the eighteen live invocations auditable", "must print a total of eighteen planned invocations" | **left unchanged** | Live `claude` invocation counts in the routing/rejudge harness — unrelated axis, explicitly named in the plan's own text as one that must NOT move |

## Mutation Verdicts (verbatim, per Task 2's acceptance criteria)

All seven mutations were performed on disposable `rsync -a --exclude .git` scratch copies under the scratchpad directory; `git status --porcelain` on the real worktree was confirmed empty before and after every mutation (the scratch copies themselves are not git repositories, since `.git` was excluded from the rsync).

**1 — changing `R-CLAIM-CAVEAT-MARKED`'s expected verdict in `render_verdict_expected` from `[False]` to `[True]`:**
```
self-test FAIL: render_contract (p) EXPECTED-VERDICT FLOOR: [EXPECTED-VERDICT MISMATCH] R-CLAIM-CAVEAT-MARKED: recorded verdict sequence [False] != expected sequence [True]
```
Names the id; proves the marker really scores untraced under the unmodified `_claim_is_traced` (D-09's teeth).

**2 — deleting `R-CLAIM-CAVEAT-MARKED` from `render_verdict_expected`:**
```
self-test FAIL: render_contract (x) COVERAGE FLOOR: arm 4b recorded-verdict table: actual [...26 ids...] != required [...27 ids...] — MISSING ['R-CLAIM-CAVEAT-MARKED'], UNEXPECTED []
```
A coverage-floor failure naming the id, per the acceptance criterion's "EXPECTED-VERDICT FLOOR or coverage-floor failure" disjunction.

**3 — deleting the `- Measure duty cycle first` block from `output-template.md`:**
```
self-test FAIL: render_contract (a) extraction [mode 1: anchor unresolved] R-CLAIM-TERSE-DROP: anchor '...' did not resolve (label matched 0 times (need exactly 1))
self-test FAIL: render_contract (aa) [claim-bound: fixture missing] R-CLAIM-TERSE-DROP: expected but absent from the extracted fixtures mapping (doc label 'Not a claim — a short list item with no sentence-ending punctuation:')
```
A NAMED extraction problem, with doc label, not a silent skip.

**4 — narrowing control (x)'s arm-4b second transcription back to the old eighteen ids while `render_locked_fixture_ids` stays at twenty-seven:**
```
self-test FAIL: render_contract (x) ENTRY-SOURCE LOCK: arm 4b recorded-verdict table: WRONG SOURCE — required [...27 ids...] != expected [...18 ids...] — MISSING [], UNEXPECTED ['R-CLAIM-CAVEAT-CITED', 'R-CLAIM-CAVEAT-MARKED', 'R-CLAIM-COLON-END', 'R-CLAIM-COLON-MID', 'R-CLAIM-LABEL-BARE', 'R-CLAIM-LABEL-CITED', 'R-CLAIM-LABEL-INLINE', 'R-CLAIM-TERSE-DROP', 'R-CLAIM-TERSE-KEEP']
```
The two-place-edit property holds — narrowing the independent transcription alone is caught.

**5 — deleting the single real call site of `_render_claim_bound_problems`:**
```
self-test FAIL: render_contract (p) CONSUMPTION FLOOR: fixture id(s) ['R-CLAIM-CAVEAT-CITED', 'R-CLAIM-CAVEAT-MARKED', 'R-CLAIM-COLON-END', 'R-CLAIM-COLON-MID', 'R-CLAIM-LABEL-BARE', 'R-CLAIM-LABEL-CITED', 'R-CLAIM-LABEL-INLINE', 'R-CLAIM-TERSE-DROP', 'R-CLAIM-TERSE-KEEP'] are never scored by any control and not named in a reported problem
self-test FAIL: render_contract (p) EXPECTED-VERDICT FLOOR: [nine more mismatches, "recorded verdict sequence None != expected sequence [...]"]
```
The consumption floor sees all nine ids go unscored, exactly as the acceptance criterion requires.

**6 — standalone helper isolation (missing fixture, verdict mismatch, anti-masking, empty table), run directly against `_render_claim_bound_problems` before wiring, on synthetic ids never touching the real registry:**
```
OK (i): missing fixture -> named problem ['[claim-bound: fixture missing] SYNTH-MISSING: expected but absent from the extracted fixtures mapping']
OK (ii): mismatch -> named problem ['[claim-bound: verdict mismatch] SYNTH-A: got [False], expected [True]']
OK (iii): anti-masking -> ['[claim-bound: verdict mismatch] SYNTH-B: got [False], expected [True]'] (SYNTH-A, whose stub matched, produced no problem)
OK (iv): empty table -> named problem ['NON-VACUITY: the claim-bound expectation table is empty — an empty table cannot pin anything and must not pass']
```

**7 — the real nine-fixture run, standalone, before wiring:**
```
problems: []
verdicts: {'R-CLAIM-LABEL-BARE': [False], 'R-CLAIM-LABEL-INLINE': [True], 'R-CLAIM-LABEL-CITED': [True], 'R-CLAIM-COLON-MID': [False], 'R-CLAIM-COLON-END': [True], 'R-CLAIM-TERSE-DROP': [False, True], 'R-CLAIM-TERSE-KEEP': [True, False], 'R-CLAIM-CAVEAT-MARKED': [False], 'R-CLAIM-CAVEAT-CITED': [True]}
```
Exact match to the plan's specified expected-verdict table.

## Measured Readings (verified by execution)

- `python3 scripts/check-quality-harness.py --self-test` — exit 0, all sub-checks PASSED (including `render_contract`)
- `bash scripts/check-firewall-battery.sh` — `FIREWALL: GREEN (23/23)`
- `python3 scripts/sync-content.py --check` — exit 0
- `git diff 4b09201..HEAD --stat -- scripts/check-quality-harness.py` — 1 file changed, 411 insertions(+), 19 deletions(-)
- `git diff -- scripts/check-quality-harness.py` (across both commits) — no hunk inside `_conclusion_claims`, `_claim_is_traced`, `_chain_block_well_formed` or the sha256 pin
- `_selftest_render_contract` line count: 3201 (base commit `4b09201`) -> 3310 (this plan's HEAD), +109 lines
- `_render_claim_bound_problems` line count (new helper, outside the function): 109 lines

## Issues Encountered

- Same as plans 14-01/14-02/14-03: this worktree had no pytest-capable interpreter, so `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED` naming `[PREREQ] VAL-03`. Resolved via `uv sync` (creates `.venv`, ships pytest 9.1.1); battery then reported `FIREWALL: GREEN (23/23)`. `.venv` is gitignored and was not committed.
- The `.planning/phases/14-closure-ledger-claim-inventory/` directory (this plan, `14-CONTEXT.md`, `14-PATTERNS.md`) and `PROJECT.md`/`STATE.md`/`config.json` are not synced into a fresh worktree because `.planning/` is gitignored repo-wide. Copied them from the main working tree into this worktree at the start of execution — a local-only, uncommitted copy of already-committed-elsewhere planning artifacts, matching plans 14-01/14-02/14-03's identical note.
- The plan's own Task 1 `<verify>` script asserts an unconditional pairwise prefix check across all 27 `_RENDER_FIXTURE_SHAPE` keys ("no id is a prefix of another"). Run literally, it fails even on a correctly completed Task 1, because the PRE-EXISTING pair `("R-VERDICT-EXPIRY", "R-VERDICT-EXPIRY-BAD")` already violates that property — the exact case `_render_fixture_id_token`'s own docstring names as the reason the delimiter-scoped accounting matcher exists (WR-07). This is unrelated to this plan's additions. Ran a corrected verification instead, scoped exactly to Task 1's own action text ("no NEW id is a prefix of any existing or other new id"), which is the property Task 1 actually needs and the one the acceptance criteria's remaining checks (27 keys, non-empty needle tuples, clean extraction, forbidden guards) depend on. Did not alter the pre-existing `R-VERDICT-EXPIRY`/`R-VERDICT-EXPIRY-BAD` pair or its accepted exception.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- LEDGER-04's control half is now extended to the claim axis: dropping any of the nine `R-CLAIM-*` ids from any floor, changing an expected verdict, or narrowing control (x)'s independent transcription all fail by name (proven above by mutation).
- Phase 15's claim-inventory scan can rely on R11/R12 being registered, scored and floored — not merely stated (14-02) or registered as literals (14-03).
- No blockers.

---
*Phase: 14-closure-ledger-claim-inventory*
*Completed: 2026-09-03*

## Self-Check: PASSED

- FOUND: scripts/check-quality-harness.py
- FOUND: .planning/phases/14-closure-ledger-claim-inventory/14-04-SUMMARY.md
- FOUND commit: ad517a0 (Task 1)
- FOUND commit: 30286a4 (Task 2)
- CONFIRMED: `python3 scripts/check-quality-harness.py --self-test` exit 0
- CONFIRMED: `bash scripts/check-firewall-battery.sh` — FIREWALL: GREEN (23/23)
- CONFIRMED: `python3 scripts/sync-content.py --check` exit 0
