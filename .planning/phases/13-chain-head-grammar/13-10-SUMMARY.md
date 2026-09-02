---
phase: 13-chain-head-grammar
plan: 10
subsystem: quality-harness
tags: [chain-head-grammar, rendering-contract, consumption-floor, gap-closure, BL-03]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar (plans 01-09)
    provides: the chain-head grammar (R7/R8/R9), R7's disclosed positional
      bound (13-08, BL-01), R9's GT-leading-hop refusal and remedy (13-09,
      BL-02), and the scored-not-extracted consumption floor this plan
      strengthens (13-05, CR-01)
provides:
  - a `scored_verdicts: dict[str, list[bool]]` recorder replacing the
    `scored_ids: set[str]` membership recorder; no separately writable
    `scored_ids` name exists any more
  - two pure floor helpers, `_render_verdict_floor_problems` (recorded
    verdict must equal an inline expectation over all fourteen locked
    fixtures) and `_render_chain_verdict_floor_problems` (independently
    re-scores the nine chain-family fixtures from `fixtures` with the
    frozen `_chain_block_well_formed`, consulting no recorder)
  - control (v), a recorder-delegation probe proving each of the four
    scoring wrappers actually delegates to its raw scorer
  - control (w), proving both new floor helpers falsifiable in-process
    with synthetic inputs, mirroring control (s)
  - a rewritten control (t) locking the new recorder/helper call-site
    counts and forbidding the two reproduced forgery idioms, with an
    honest DISCLOSED LIMITATION replacing the false "closes exactly that"
    claim
  - both `| QUAL-01 |` doc rows (CLAUDE.md, docs/ARCHITECTURE.md) stating
    the strengthened guarantee and its disclosed A-02 asymmetry, with
    `expected-verdict floor` registered as a seventh doc-row token
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A membership set is not evidence that scoring occurred — the
      recorder must hold the VERDICT a scorer produced, compared against
      an inline expectation, not merely the fact that some code touched
      the fixture id."
    - "Where a scorer is a pure single-argument predicate, layer an
      independent re-derivation arm that reads the raw text and calls the
      frozen function directly, bypassing the recorder entirely — no
      forgery of the recorder, of any shape, can then discharge that
      fixture. Where the scorer needs extra context arguments the floor
      would have to restate, disclose the narrower guarantee rather than
      duplicating the wiring."
    - "A source-level comment describing a search pattern must never spell
      out the exact substring it counts, or the comment itself inflates
      the count it takes over the function it lives inside — the same
      concatenation discipline the counted patterns themselves must use."

key-files:
  created: []
  modified:
    - scripts/check-quality-harness.py
    - CLAUDE.md
    - docs/ARCHITECTURE.md

key-decisions:
  - "A-01 confirmed as designed: bypass 2 (wrapper called, verdict
    discarded) leaves the gate green on its own — the wrappers still run
    and the recorder still holds the real verdicts, so no behavioural
    content is removed. A real contract regression applied on top of the
    same mutated copy is required to prove the floor can still fail, and
    it does — see Bypass 2 stage 2 below, though the specific control that
    fires there differs from what the plan predicted (recorded as a
    finding, not silently forced to match)."
  - "A-02 disclosed asymmetry: independent re-derivation (arm 4a) applies
    only to the nine chain-family fixtures, whose scorer
    (`_chain_block_well_formed`) is a single-argument pure function. The
    five `R-CITE-*` / `R-VERDICT-*` fixtures need extra arguments (chain
    ids, chain text, ledger fragments) arm 4a would otherwise have to
    restate, duplicating control (f)'s wiring — for those five the
    guarantee stays recorded-verdict (arm 4b) plus control (v)'s
    delegation probe plus control (t)'s source-level lock. Published in
    both `| QUAL-01 |` doc rows verbatim."
  - "A-03 measured facts re-confirmed by direct call against the live,
    unmutated module before any edit — all nine chain-family verdicts and
    all five non-chain-family sequences (including R-CITE-NONE's
    two-call [False, True] flip) matched the plan's `<measured_facts>`
    table exactly; no table was edited to match a different measurement."
  - "Control (t) rewritten to lock six independent counts derived from
    `_selftest_render_contract`'s own source: four `.setdefault(` recorder
    sites, four `_score_*` definitions, six call sites for
    `_render_verdict_floor_problems` (one real arm-4b call plus five of
    control (w)'s isolation-driving calls), five call sites for
    `_render_chain_verdict_floor_problems` (one real arm-4a call plus four
    of control (w)'s isolation calls), and zero occurrences of the two
    reproduced forgery idioms (`.update(` on the recorder, and a
    bare-subscript assignment into it). Every comment describing these
    patterns deliberately avoids spelling out the literal counted
    substring contiguously — an early draft that did so inflated the
    counts it was itself asserting, caught by re-running the self-test
    before committing."
  - "Deviation from the plan's stage-2 prediction for bypass 2 (recorded
    as a finding, not corrected by editing code or the fixture registry):
    the plan expected the contract-regression re-run to trigger a
    `(p) CHAIN VERDICT FLOOR` problem naming R-HEAD-PROSE-BAD. The literal
    prescribed edit (`C2's threshold` -> `C2 (threshold)`) also deletes
    two of R-HEAD-PROSE-BAD's three required extraction-shape needles
    (`_RENDER_FIXTURE_SHAPE`), because the possessive phrase IS the
    needle text. The extraction guard's own '(a) extraction [mode 2:
    shape mismatch]' problem fires first, and — per Task 1's own
    literal spec for `_render_chain_verdict_floor_problems` ('skipping
    ids discharged by `_render_fixture_id_accounted`... reporting an id
    expected but absent from fixtures') — that pre-existing problem
    discharges R-HEAD-PROSE-BAD from arm 4a's own report, since the id
    IS already accounted for. The overall required proof (bypass 2 stays
    green on its own; a real regression on the same mutated copy goes
    red) is still achieved — exit 1, gate catches the regression — just
    via a different named control. No shape-needle or detector change was
    made to force the plan's predicted control to fire, since doing so
    would weaken a legitimate anti-cross-contamination guard for a
    cosmetic match to a plan author's guess."

metrics:
  duration: ~2h
  files_modified: 3
  tasks_completed: 3
  completed: 2026-09-02
---

# Phase 13 Plan 10: Expected-verdict consumption floor (BL-03) Summary

The `scored_ids` membership-set consumption floor — itself Plan 13-05's fix
for the original CR-01 — is replaced by a verdict-sequence recorder compared
against an inline expected-verdict table, with the nine chain-family
fixtures additionally re-scored independently by the frozen detector. Both
bypasses `13-VERIFICATION.md` reproduced against the old floor (a bare
`.update({...})` with no scorer called, and a wrapper called with its
return discarded) are closed: the first now fails control (t) and arm 4b by
value; the second leaves the gate green on its own (the designed A-01
outcome) but goes red the moment a real contract regression is layered on
top of the same mutated copy.

## What was built

**Task 1 — Replace the membership recorder with a verdict recorder, add
two pure floor helpers.** `scored_ids: set[str] = set()` became
`scored_verdicts: dict[str, list[bool]] = {}`; each of the four wrappers
(`_score_chain`, `_score_verdict`, `_score_traced`, `_score_ledger`) now
calls its scorer FIRST, then appends the boolean summary via exactly one
`scored_verdicts.setdefault(fixture_id, []).append(...)` site, then returns
what it returned before, unchanged (`_score_ledger` still returns the
fragment list; it records `bool(fragments)`). Added
`_render_verdict_floor_problems(expected, scored_verdicts, problems)` and
`_render_chain_verdict_floor_problems(expected, fixtures, scorer, problems)`
immediately after `_render_unscored_fixture_ids`, both pure (all inputs as
parameters, no module constant read), both discharging via
`_render_fixture_id_accounted` exactly like the existing floor. Arm 3's own
derivation now reads `_render_unscored_fixture_ids(render_locked_fixture_ids,
set(scored_verdicts), problems)` — `scored_ids` no longer exists as a
writable name anywhere (renamed the pure helper's own parameter to
`scored_id_set` to satisfy the literal zero-occurrences criterion). Rewrote
the false in-code claim that control (t) "closes exactly that" fail-OPEN
shape, replacing it with an accurate account naming both reproduced
bypasses and pointing at arms 4a/4b and control (v) as the actual fix.

**Task 2 — Wire the two floor arms, add controls (v) and (w), rewrite
control (t).** Arm 4a (`(p) CHAIN VERDICT FLOOR`) re-scores all nine
chain-family fixtures from `fixtures` with the unmodified
`_chain_block_well_formed`, reading no recorder. Arm 4b
(`(p) EXPECTED-VERDICT FLOOR`) compares all fourteen locked ids' recorded
sequences against an inline table, including `R-CITE-NONE`'s two-call
`[False, True]` flip. An anti-masking assertion requires the union of both
tables' keys to equal the locked fourteen-id set. Control (v) (RECORDER
DELEGATION PROBE) calls each wrapper with a probe id outside the locked set
(`PROBE-SCORE-CHAIN`/`-VERDICT`/`-TRACED`/`-LEDGER`), asserting the
wrapper's return equals the raw scorer's return and the recorder holds that
same value; for `_score_chain` it probes both directions (the shipped
one-hop `False` base case and a two-hop `True` case) and asserts the two
results differ. Control (w) (FLOOR HELPER ISOLATION) drives both new
helpers with synthetic literals only (clean, wrong-verdict, missing/absent,
accounted, and — for the verdict helper — a proper-prefix anti-masking
case), mirroring control (s). Control (t) was rewritten to lock: exactly 4
`.setdefault(` recorder sites, exactly 4 `_score_*` definitions, exactly 6
call sites for the verdict-floor helper and exactly 5 for the
chain-verdict-floor helper (one real arm call each, plus control (w)'s
isolation-driving calls), and zero occurrences of the two reproduced
forgery idioms (a bare `.update(` on the recorder; a bare-subscript
assignment into it, detected as a same-line textual heuristic). Every
comment describing these patterns avoids spelling out the literal counted
substring contiguously — an early draft did not, and its own prose
inflated four of the six counts it was asserting; caught immediately by
re-running the self-test.

**Task 3 — Reproduce both original bypasses, correct the doc rows, close
green.** Both `| QUAL-01 |` rows now state the strengthened guarantee
after the existing consumption-floor sentence, and disclose A-02's
asymmetry in DISCLOSED LIMITATIONS. `expected-verdict floor` is a seventh
`_QUAL01_DOC_ROW_TOKENS` entry; the (m) NEGATIVE-CASE COUNT FLOOR moved
from 12 (2x6) to 14 (2x7) across all four hardcoded sites (comment, `if`
condition, f-string, and `_selftest_render_contract`'s own docstring).
Both original bypasses were reproduced on disposable scratch copies (see
Mutations below).

## Verification (run in order, on the tracked tree, after all three tasks)

1. `python3 scripts/check-quality-harness.py --self-test` → exit 0, all
   sub-checks PASSED including `render_contract` and `chain_detector_pin`.
2. `python3 scripts/sync-content.py --check` → exit 0.
3. `python3 scripts/check-traceability.py --self-test` → exit 0 (`PASS`).
4. `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (23/23)`,
   exit 0. (VAL-03 initially reported `[PREREQ]`/`BLOCKED` — no `.venv`
   existed in this worktree — ran `uv sync` to create it, then re-ran to
   GREEN, same remedy 13-08/13-09 documented.)
5. `grep -c 'sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3' scripts/check-quality-harness.py` → `1`.
6. `git diff -U0 3d0f3e2aa1fcacefa4171794a69db39efcb0ec4b -- scripts/check-quality-harness.py` reviewed
   by eye: every hunk lands at line 124 (one new import) or line 6641 or
   later — well clear of `_chain_block_well_formed` (~line 4277-4463).
   `_CHAIN_DETECTOR_PINNED_DIGEST` confirmed unchanged.

## Expected-verdict tables as landed

**Chain family** (arm 4a, `dict[str, bool]`, re-scored independently from
`fixtures` by `_chain_block_well_formed`) — all nine re-measured against
the live unmutated module before any edit, matching `<measured_facts>`
exactly:

| Fixture id | Verdict |
|---|---|
| `R-CHAIN-CONFORMING` | `True` |
| `R-CHAIN-WRAPPED` | `False` |
| `R-CHAIN-NUMBERED` | `False` |
| `R-HEAD-PROSE-BAD` | `False` |
| `R-HEAD-CHAINREF` | `True` |
| `R-HEAD-ALLCHAIN` | `True` |
| `R-HEAD-PROSE-MID` | `True` |
| `R-HEAD-GTHOP-BAD` | `False` |
| `R-HEAD-GTHOP-OK` | `True` |

**All fourteen locked ids** (arm 4b, `dict[str, list[bool]]`, compared
against `scored_verdicts`) — the nine above wrapped as single-element
lists, plus the five non-chain sequences, all re-measured against the live
unmutated module:

| Fixture id | Recorded sequence |
|---|---|
| `R-VERDICT-EXPIRY` | `[True]` |
| `R-VERDICT-EXPIRY-BAD` | `[False]` |
| `R-CITE-INLINE` | `[True]` |
| `R-CITE-LEDGER` | `[True]` |
| `R-CITE-NONE` | `[False, True]` |

## Pre/post value of the (m) NEGATIVE-CASE COUNT FLOOR

| Floor | Pre-plan | Post-plan |
|---|---|---|
| control (m) NEGATIVE-CASE COUNT FLOOR (`qual01_negative_case_count` expectation) | `12` (2x6) | `14` (2x7) |

## Mutations (all ten reproduced on disposable `rsync -a --exclude .git
--exclude .venv` scratch copies under the session scratchpad; `git status
--porcelain` on the tracked tree confirmed empty before the first mutation
and after every mutation cycle)

**MUTATION A** — in the arm-4b inline table, change `R-HEAD-CHAINREF` from
`[True]` to `[False]`:
```
self-test FAIL: render_contract (p) EXPECTED-VERDICT FLOOR: [EXPECTED-VERDICT MISMATCH] R-HEAD-CHAINREF: recorded verdict sequence [True] != expected sequence [False]
```
Exit 1, naming `R-HEAD-CHAINREF` and both sequences, as required.

**MUTATION B** — in the arm-4a inline table, change `R-HEAD-GTHOP-BAD` from
`False` to `True`:
```
self-test FAIL: render_contract (p) CHAIN VERDICT FLOOR: [CHAIN VERDICT FLOOR] R-HEAD-GTHOP-BAD: scored False != expected True
```
Exit 1, naming it, as required.

**MUTATION C** — make `_render_chain_verdict_floor_problems` return `[]`
unconditionally (injected right after its docstring):
```
self-test FAIL: render_contract (w) FLOOR HELPER ISOLATION chain WRONG-VERDICT: expected exactly one problem naming 'X', got []
self-test FAIL: render_contract (w) FLOOR HELPER ISOLATION chain FIXTURE-ABSENT: expected exactly one problem REPORTING (not skipping) 'X', got []
```
Exit 1, naming control (w) and its wrong-verdict/fixture-absent arms —
proves the helper cannot be silently neutered.

**MUTATION D** — make `_render_verdict_floor_problems` return `[]`
unconditionally:
```
self-test FAIL: render_contract (w) FLOOR HELPER ISOLATION verdict WRONG-VERDICT: expected exactly one problem naming 'X', got []
self-test FAIL: render_contract (w) FLOOR HELPER ISOLATION verdict MISSING: expected exactly one problem naming 'X', got []
self-test FAIL: render_contract (w) FLOOR HELPER ISOLATION verdict ANTI-MASKING: expected exactly one problem naming the proper prefix 'X' (not 'X-BAD'), got [] — a helper reverted to bare `in` containment would let a problem naming only 'X-BAD' wrongly discharge 'X' too
```
Exit 1, naming control (w).

**MUTATION E** — make `_score_chain` return `True` without calling
`_chain_block_well_formed` (recording `True` as well) — the "record
without scoring" fail-OPEN shape, now closed behaviourally:
```
self-test FAIL: render_contract (b) R-CHAIN-WRAPPED (doc label 'Non-conforming — a hop broken across physical lines:') scored well-formed, expected malformed
self-test FAIL: render_contract (b) R-CHAIN-NUMBERED (doc label 'Non-conforming — the same hops rendered as a numbered list:') scored well-formed, expected malformed
self-test FAIL: render_contract (b) R-HEAD-PROSE-BAD (doc label 'Non-conforming — an input carrying unparenthesized prose:') scored well-formed, expected malformed
self-test FAIL: render_contract (b) R-HEAD-GTHOP-BAD (doc label 'Non-conforming — a hop beginning with a GT-N identifier:') scored well-formed, expected malformed
self-test FAIL: render_contract (p) EXPECTED-VERDICT FLOOR: [EXPECTED-VERDICT MISMATCH] R-CHAIN-NUMBERED: recorded verdict sequence [True] != expected sequence [False]
self-test FAIL: render_contract (p) EXPECTED-VERDICT FLOOR: [EXPECTED-VERDICT MISMATCH] R-CHAIN-WRAPPED: recorded verdict sequence [True] != expected sequence [False]
self-test FAIL: render_contract (p) EXPECTED-VERDICT FLOOR: [EXPECTED-VERDICT MISMATCH] R-HEAD-GTHOP-BAD: recorded verdict sequence [True] != expected sequence [False]
self-test FAIL: render_contract (p) EXPECTED-VERDICT FLOOR: [EXPECTED-VERDICT MISMATCH] R-HEAD-PROSE-BAD: recorded verdict sequence [True] != expected sequence [False]
self-test FAIL: render_contract (v) RECORDER DELEGATION PROBE: _score_chain false-direction probe returned True, raw _chain_block_well_formed returned False
self-test FAIL: render_contract (v) RECORDER DELEGATION PROBE: _score_chain's two probe results did not differ (True == True) — a wrapper returning a constant would otherwise satisfy the equality arms above against a constant raw comparison
self-test FAIL: render_contract (v) RECORDER DELEGATION PROBE: recorder holds [True, True] for 'PROBE-SCORE-CHAIN', expected [False, True]
```
Exit 1, naming control (v) (both the differing-results arm and the
equality arm) as required — plus controls (b) and arm 4b independently,
since the fabrication also affects the live chain-family fixtures, not
just the probes.

**MUTATION F** — delete the arm-4a call to
`_render_chain_verdict_floor_problems`:
```
self-test FAIL: render_contract (t) SCORING RECORDER LOCK: observed 4 recorder-mutation site(s) (expected 4), 4 scoring-wrapper definition(s) (expected 4), 6 verdict-floor-helper call site(s) (expected 6), 4 chain-verdict-floor-helper call site(s) (expected 5), 0 forbidden recorder dict-update occurrence(s) (expected 0), and 0 forbidden bare-subscript assignment occurrence(s) (expected 0)
```
Exit 1, naming control (t)'s call-site lock (the chain-verdict-floor-helper
count dropped from 5 to 4), as required.

**Bypass 1 reproduction** — replace the three `(b)` chain-head verdict
blocks (`R-HEAD-PROSE-BAD`/`R-HEAD-CHAINREF`/`R-HEAD-ALLCHAIN`) with a
single `scored_verdicts.update({"R-HEAD-PROSE-BAD": False,
"R-HEAD-CHAINREF": True, "R-HEAD-ALLCHAIN": True})` line (bare booleans,
not the required single-element-list shape, to faithfully carry forward
the original bypass's "no scorer called" intent into the new dict-of-lists
schema):
```
self-test FAIL: render_contract (p) EXPECTED-VERDICT FLOOR: [EXPECTED-VERDICT MISMATCH] R-HEAD-ALLCHAIN: recorded verdict sequence True != expected sequence [True]
self-test FAIL: render_contract (p) EXPECTED-VERDICT FLOOR: [EXPECTED-VERDICT MISMATCH] R-HEAD-CHAINREF: recorded verdict sequence True != expected sequence [True]
self-test FAIL: render_contract (p) EXPECTED-VERDICT FLOOR: [EXPECTED-VERDICT MISMATCH] R-HEAD-PROSE-BAD: recorded verdict sequence False != expected sequence [False]
self-test FAIL: render_contract (t) SCORING RECORDER LOCK: observed 4 recorder-mutation site(s) (expected 4), 4 scoring-wrapper definition(s) (expected 4), 6 verdict-floor-helper call site(s) (expected 6), 5 chain-verdict-floor-helper call site(s) (expected 5), 1 forbidden recorder dict-update occurrence(s) (expected 0), and 0 forbidden bare-subscript assignment occurrence(s) (expected 0)
```
Exit 1 — both control (t)'s forbidden-`.update(` arm AND arm 4b's
value-shape mismatch fire independently, exactly as the plan predicted
("Control (t)'s forbidden-idiom arm fires on `.update(`; independently,
arm 4b sees an unexpected value shape").

**Bypass 2 reproduction, stage 1** — replace the same three blocks with
bare `_score_chain("R-HEAD-PROSE-BAD", head_prose_bad or "")` /
`_score_chain("R-HEAD-CHAINREF", head_chainref or "")` /
`_score_chain("R-HEAD-ALLCHAIN", head_allchain or "")` calls whose returns
are discarded:
```
exit=0 (all sub-checks PASSED, including render_contract and chain_detector_pin)
```
Exit 0, the DESIGNED outcome (A-01): the wrappers still run and the
recorder still holds the real verdicts (arm 4b sees correct values), arm
4a still independently re-scores the same text from `fixtures`, so the
mutation removes no behavioural content.

**Bypass 2 reproduction, stage 2 (real contract regression on top of the
same mutated copy)** — edited `shared/spine/references/output-template.md`
so R-HEAD-PROSE-BAD's block head reads `C2 (threshold)` instead of `C2's
threshold`, then re-ran on the same scratch copy:
```
self-test FAIL: render_contract (a) extraction [mode 2: shape mismatch] R-HEAD-PROSE-BAD: extracted text is missing required substring(s) ["C2's threshold", "+ C2's threshold\n→"]
```
Exit 1 — the required outcome (the gate goes red once a real regression is
introduced) is achieved, but via a DIFFERENT named control than the plan
predicted. See "Deviation from the plan's stage-2 prediction" in
key-decisions above: the prescribed literal edit necessarily deletes two
of `R-HEAD-PROSE-BAD`'s three `_RENDER_FIXTURE_SHAPE` needles (the
possessive phrase IS the needle text), so the extraction-integrity guard
fires and, via `_render_fixture_id_accounted`, discharges the fixture from
arm 4a's own report — this is Task 1's literal discharge-semantics spec
working as designed, not a defect. Both runs' verbatim output are recorded
above in full, per the plan's own instruction to report the disagreement
rather than force a match.

**MUTATION G** — delete the `expected-verdict floor` phrase from
`CLAUDE.md`'s QUAL-01 row only:
```
self-test FAIL: render_contract (m) POSITIVE: CLAUDE.md: the '| QUAL-01 |' row is missing required token 'expected-verdict floor'
```
Exit 1, naming both the token and the file.

**MUTATION H** — revert the (m) NEGATIVE-CASE COUNT FLOOR's `if` condition
AND f-string message tail together (both carry the same literal number)
from `14` back to `12`, leaving `_QUAL01_DOC_ROW_TOKENS` at its seven
entries:
```
self-test FAIL: render_contract (m) NEGATIVE-CASE COUNT FLOOR: derived 14 (file, token) case(s) from 2 doc row(s) x 7 token(s) != expected 12
```
Exact match to the plan's specified message, byte for byte.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 — self-inflicted bug] Control (t)'s own comments inflated the
counts they were asserting**
- **Found during:** Task 2, first self-test run after wiring the rewritten
  control (t).
- **Issue:** Comments describing the new source-level counts spelled out
  the literal counted substrings contiguously (e.g. `` `scored_verdicts.update(` ``,
  `` `_render_verdict_floor_problems(` ``) inside backtick-quoted code
  spans. `inspect.getsource()` captures comments as plain text, so these
  literal mentions inflated `render_t_setdefault_count`,
  `render_t_verdict_call_count`, `render_t_chain_call_count`,
  `render_t_update_count`, and `render_t_subscript_assign_count` above
  their true code-only values, causing the self-test to fail immediately
  after the rewrite (observed counts 5/7/6/2/1 against expected 4/6/5/0/0).
- **Fix:** Rewrote every such comment to describe the pattern
  conceptually (by control-letter or role) rather than spelling out the
  literal contiguous substring, mirroring the pre-existing discipline
  already used for the `.setdefault(`/`def _score_` counts inherited from
  Plan 13-05.
- **Files modified:** `scripts/check-quality-harness.py`.
- **Commit:** `1059097`.

**2. [Rule 1 — acceptance-criteria bug] Task 1's literal `'closes exactly
that'` acceptance criterion was violated by the historical quotation of
the original false claim**
- **Found during:** Re-checking Task 1's own acceptance-criteria greps
  after Task 3's docstring pass; the very first Task-1-time check of
  `grep -c 'closes exactly that'` had returned `1`, not the required `0`,
  and had gone unnoticed at the time it was run.
- **Issue:** Both the (p) CONSUMPTION FLOOR comment and control (t)'s own
  rewritten comment quoted the discredited original sentence verbatim
  ("... control (t) below closes exactly that ...") as historical record,
  which satisfies the SUBSTANCE of "corrected" but violates the literal
  zero-occurrence grep the plan's acceptance criteria specify.
- **Fix:** Paraphrased both historical references to describe the false
  claim's content ("asserted that control (t) below ... fully closed the
  fail-OPEN shape") without reproducing the exact four-word phrase
  contiguously, preserving the historical accuracy without the literal
  substring match.
- **Files modified:** `scripts/check-quality-harness.py`.
- **Commit:** `bb6e483`.

**3. [Rule 3 — blocking prerequisite] VAL-03 blocked on a missing `.venv`**
- **Found during:** Task 3's closing verification, first `bash
  scripts/check-firewall-battery.sh` run.
- **Issue:** This worktree had no `.venv`, so no pytest-capable
  interpreter was found; VAL-03 reported `[PREREQ]` and the battery
  printed `FIREWALL: BLOCKED` (exit 2), not a gate failure — the same
  remedy 13-08/13-09 documented.
- **Fix:** Ran `uv sync` to create `.venv`, then re-ran the battery to
  `FIREWALL: GREEN (23/23)`.
- **Files modified:** none (`.venv/` is gitignored, not committed).

### Findings (not fixed — a measured disagreement with the plan's own
prediction, per A-03's discipline)

**4. Bypass 2 stage-2's regression fires a different named control than
the plan predicted**
- **Found during:** Task 3, reproducing the stage-2 contract regression
  exactly as specified.
- **Detail:** See "Bypass 2 reproduction, stage 2" above and the matching
  key-decisions entry. The plan expected a `(p) CHAIN VERDICT FLOOR`
  problem naming `R-HEAD-PROSE-BAD`; the measured behavior is an
  `(a) extraction [mode 2: shape mismatch]` problem on the same fixture,
  because the prescribed literal edit deletes the extraction-shape
  needles that are the possessive phrase itself. The overall required
  proof (regression caught, exit 1, on the same mutated copy that stayed
  green at stage 1) is satisfied.
- **Disposition:** Left as measured. No shape-needle or fixture change was
  made to force the plan's predicted control to fire; doing so would
  weaken the extraction-integrity guard for a cosmetic match.

## Self-Check: PASSED

- `scripts/check-quality-harness.py` — FOUND, contains
  `scored_verdicts`, `_render_verdict_floor_problems`,
  `_render_chain_verdict_floor_problems`, `PROBE-SCORE-CHAIN`, and the
  rewritten control (t).
- `CLAUDE.md` — FOUND, contains `expected-verdict floor`.
- `docs/ARCHITECTURE.md` — FOUND, contains `expected-verdict floor`.
- Commit `cc3c7b3` — FOUND in `git log --oneline`.
- Commit `1059097` — FOUND in `git log --oneline`.
- Commit `bb6e483` — FOUND in `git log --oneline`.
- `grep -c 'scored_ids' outside comments` — `0` (parameter renamed to
  `scored_id_set`; all remaining non-comment mentions eliminated).
- `_CHAIN_DETECTOR_PINNED_DIGEST` — confirmed unchanged
  (`sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3`,
  count 1); `git diff -U0` against the pre-plan base shows no hunk inside
  or near `_chain_block_well_formed`.
- `bash scripts/check-firewall-battery.sh` — re-run after all three
  commits landed: `FIREWALL: GREEN (23/23)`, exit 0.
- `python3 scripts/sync-content.py --check` — exit 0.
- `python3 scripts/check-traceability.py --self-test` — exit 0 (`PASS`).
- `git status --porcelain` — empty, confirmed after all ten mutations and
  both bypass reproductions (all run on disposable scratch copies).
