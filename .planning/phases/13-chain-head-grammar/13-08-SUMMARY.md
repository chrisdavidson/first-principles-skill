---
phase: 13-chain-head-grammar
plan: 08
subsystem: quality-harness
tags: [chain-head-grammar, rendering-contract, positional-bound, gap-closure, BL-01]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar (plans 01-07)
    provides: the chain-head grammar (R7/R8), the scored-not-extracted consumption
      floor (13-05, CR-01), the dispatch-reachability leg (13-06, CR-02), and the
      reconciled GT-presuming chain-completeness prose (13-07)
provides:
  - R7's own disclosed positional bound, byte-identical on all three canonical
    surfaces (output-template.md, SKILL-body.md, validation-rubric.md) and in the
    generated tree: the prose-input rule binds in every head position, but the
    frozen `_chain_block_well_formed` detects the violation only when the offending
    input is the last one before the first arrow
  - a fourth chain-head worked example, `R-HEAD-PROSE-MID`, pinning the measured
    non-final-position behavior in tracked bytes, extracted and scored at
    self-test time by the unmodified detector
  - a twelve-fixture consumption floor (up from eleven) with a new `(b)` verdict
    control and a discriminating third needle on `R-HEAD-PROSE-BAD` so the two
    possessive-prose fixtures discriminate in both directions
  - both published `| QUAL-01 |` doc rows (CLAUDE.md, docs/ARCHITECTURE.md)
    stating the positional bound instead of the unconditional claim, with a
    registered token (`R-HEAD-PROSE-MID`) and an updated NEGATIVE-CASE COUNT
    FLOOR (10, up from 8)
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A rule's published prose must be scoped to exactly what its pinned mechanical
      detector enforces, not what the rule conceptually means — when the two diverge,
      the fix is disclosure in the prose (this plan), never widening or anchoring the
      frozen detector (CONTRACT-06)."
    - "A minimal-pair fixture (same bytes, one token's position moved) scored in
      opposite directions by the same unmodified detector is the load-bearing way to
      pin a measured positional bound in tracked, falsifiable bytes rather than
      prose assertion alone."

key-files:
  created: []
  modified:
    - shared/spine/references/output-template.md
    - shared/spine/SKILL-body.md
    - shared/spine/references/validation-rubric.md
    - first-principles/agents/references/output-template.md
    - first-principles/agents/references/validation-rubric.md
    - first-principles/agents/first-principles.md
    - scripts/check-quality-harness.py
    - CLAUDE.md
    - docs/ARCHITECTURE.md

key-decisions:
  - "A-01 (BL-01 fork), as pre-decided by the plan: scoped the published prose to
    what the detector enforces rather than anchoring `_CHAIN_FORM_LINE_RE`.
    `_chain_block_well_formed` is byte-unchanged; `git diff` against the pre-plan
    base shows no hunk between `def _chain_block_well_formed` (line 4276, untouched
    across this plan) and its closing `return False` — every edit lands at or
    beyond line 6498."
  - "A-02 confirmed by direct re-measurement before any edit, against the live
    unmutated module: the middle-position head (`GT-13? (bill composition
    unknown) + C2's threshold + GT-12? (duty cycle unknown)`) scores `True`
    (well-formed); the shipped trailing-position `R-HEAD-PROSE-BAD` scores `False`
    (malformed); the first-position variant also scores `True`, confirming A-03's
    reasoning that shipping only the middle-position fixture is sufficient."
  - "Fixed a self-inflicted line-wrap in the WR-03 historical-count qualification
    (\"eleven was the table's size at Phase 11...\") that split the required
    single-line grep target across two physical comment lines — the exact failure
    mode 13-07's own lesson (recorded in this plan's read_first) warned about.
    Caught by re-running the acceptance-criteria grep before moving on, not by the
    self-test (which does not check comment prose)."
  - "Left two pre-existing, unrelated `eleven` mentions untouched despite the plan's
    literal acceptance criterion reading `grep -vn '^\\s*#' ... | grep -ci eleven`
    reports `0`: `_RENDER_REGISTRY_FIELDS` (eleven today, ten registries — a
    dataclass FIELD count, unchanged by this plan, which added registry ENTRIES not
    a new FIELD) and the `--run`/`--rejudge` scoreline TSV's eleven-column
    docstring (an unrelated column count). Both predate this plan and are outside
    its five enumerated fix locations (task 2's read_first list); renumbering
    either to twelve would be a false statement, not a fix. The literal grep
    therefore reports 2, not 0 — recorded here as a finding per the plan's own
    A-02 discipline (\"a disagreement is a finding, not a table to fix\") rather
    than mechanically forcing incorrect text."
  - "Simplified Mutation 5's reproduction to match what control (m)'s real code
    does: `_QUAL01_DOC_ROW_TOKENS`'s new fifth token, `R-HEAD-PROSE-MID`, appears
    TWICE in each doc row (once in the chain-head-grammar quartet enumeration, once
    in the corrected overclaiming sentence) because the plan's own action text
    specifies both mentions verbatim. Stripping only the first occurrence left the
    second standing and the self-test correctly stayed green (0, not 1) — not a
    bug, but a signal that the mutation must replicate control (m)'s own
    `line.replace(token, \"\")` (which strips every occurrence on the row), not a
    single manual substring removal. Redone accordingly; recorded as a deviation
    below."

metrics:
  duration: ~2h
  files_modified: 9
  tasks_completed: 3
  completed: 2026-09-02
---

# Phase 13 Plan 08: Chain-head positional-bound disclosure (BL-01) Summary

R7's head-input rule now states, on all three canonical surfaces and in the
generated tree, that the frozen mechanical form check enforces the possessive-prose
prohibition only when the offending input is the last one before the first arrow —
closing the gap where the published rule claimed unconditional coverage the pinned
detector never delivered.

## What was built

**Task 1 — R7's positional-bound sentence.** Replaced R7's closing clause
(`write \`C2 (threshold)\`.`) with `write \`C2 (threshold)\` in every position. The
mechanical form check detects that violation only when the prose input is the last
one before the first \`→\`; in an earlier position the check matches the
well-formed remainder and scores the head conforming, so the rule binds in
positions the check does not reach.` — byte-identical (663 bytes, confirmed by
direct string comparison) across `shared/spine/references/output-template.md`,
`shared/spine/SKILL-body.md`, and inline on one physical line in
`shared/spine/references/validation-rubric.md`. Re-pinned
`_RENDER_RULE_LITERALS["R7"]` to the same bytes (verified `r7 in
open('shared/spine/SKILL-body.md').read()` is `True`), re-pointed
`expected_literal_clauses["R7"]` at the disclosure clause, and recomputed
`expected_literal_digest` from the edited registry:
`sha256:ce68aff83ff55e6286cf98cfbc60468c2f99ead880bdd8718a1826c233e206a7`.

**Task 2 — `R-HEAD-PROSE-MID` worked example.** Added a fourth chain-head block to
`output-template.md` §4 — `**Measured limitation — the same prose input in a
non-final position:**` — showing the same violation as the shipped
`R-HEAD-PROSE-BAD` fixture but with the offending input moved to the middle
position. Registered it across `_RENDER_CONTRACT_EXTRACTION_TABLE`,
`_RENDER_FIXTURE_SHAPE` (with a new third discriminating needle,
`"+ C2's threshold\n→"`, added to `R-HEAD-PROSE-BAD` so the pair discriminates in
both directions), `expected_ids`, `expected_extraction_rows`,
`expected_fixture_shape`, the `_get` binding, `render_locked_fixture_ids`, and a
new `(b)` verdict control routed through the existing `_score_chain` wrapper (no
fifth recorder site — control (t)'s lock at exactly 4 sites stayed green).
Corrected the five current-set "eleven" → "twelve" prose mentions and qualified
(without renumbering) the sixth, historical WR-03 mention.

**Task 3 — Both `| QUAL-01 |` doc rows.** Updated CLAUDE.md:165 and
docs/ARCHITECTURE.md:146 to state "twelve worked examples", name the fourth
chain-head example (`R-HEAD-PROSE-MID`) in the quartet enumeration, and bound the
overclaiming sentence: "the pair discriminates the possessive form in trailing
head position; `R-HEAD-PROSE-MID` pins the measured bound that the same violation
in an earlier position is scored well-formed, so R7 as published states the bound
rather than an unconditional claim." Added a sentence to DISCLOSED LIMITATIONS in
both rows naming the R7/detector asymmetry. Registered `R-HEAD-PROSE-MID` as a
fifth `_QUAL01_DOC_ROW_TOKENS` entry and moved the NEGATIVE-CASE COUNT FLOOR's
four hardcoded sites (comment, `if` condition, f-string message, docstring) from
8 to 10 (2 doc rows x 5 tokens).

## Verification (run in order, on the tracked tree, after all three tasks)

1. `python3 scripts/check-quality-harness.py --self-test` → exit 0, all sub-checks
   PASSED including `render_contract` and `chain_detector_pin`.
2. `python3 scripts/sync-content.py --check` → exit 0.
3. `python3 scripts/check-traceability.py --self-test` → exit 0.
4. `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (23/23)`, exit 0.
   (VAL-03 initially reported `[PREREQ]`/BLOCKED because no `.venv` existed in this
   worktree; ran `uv sync` to create it — a prerequisite setup step, not a gate
   fix — then re-ran to GREEN.)
5. `grep -c 'sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3' scripts/check-quality-harness.py` → `1`.
6. `git diff -U0 <pre-plan-base> HEAD -- scripts/check-quality-harness.py` reviewed
   by eye: every hunk lands at or beyond line 6498; none fall between
   `def _chain_block_well_formed` (line 4276) and its closing `return False`.

## Mutations (all nine reproduced on disposable `rsync -a --exclude .git --exclude
.venv` scratch copies under the session scratchpad; `git status --porcelain` on
the tracked tree confirmed empty before the first and after every mutation cycle)

**Task 1, mutation 1** — delete the new final sentence of R7 from
`shared/spine/SKILL-body.md` alone:
```
self-test FAIL: render_contract (i) POSITIVE: shared/spine/SKILL-body.md: rule R7 is missing — deleted from this surface
```
Exit 1, naming both R7 and the surface, as required.

**Task 1, mutation 2** — revert `expected_literal_digest` to the pre-plan value
(`sha256:4ccfd10ed7577c46dd8cd0ea9c76e666d84d3c193e15c6bcc485ea24df83f7a6`):
```
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: literals: digest 'sha256:ce68aff83ff55e6286cf98cfbc60468c2f99ead880bdd8718a1826c233e206a7' != pinned 'sha256:4ccfd10ed7577c46dd8cd0ea9c76e666d84d3c193e15c6bcc485ea24df83f7a6'
```
Exit 1, matching the required "digest … != pinned …" substring.

**Task 2, mutation 1** — delete the new `(b)` verdict block entirely:
```
self-test FAIL: render_contract (p) CONSUMPTION FLOOR: fixture id(s) ['R-HEAD-PROSE-MID'] are never scored by any control and not named in a reported problem
```
Exact match to the plan's specified message.

**Task 2, mutation 2** — flip the control's direction (remove the `not`):
```
self-test FAIL: render_contract (b) R-HEAD-PROSE-MID (doc label 'Measured limitation — the same prose input in a non-final position:') scored malformed, expected well-formed (measured bound)
```
Non-vacuity proven: the control observes a real verdict.

**Task 2, mutation 3** — replace `R-HEAD-PROSE-MID`'s extraction anchor with
`R-HEAD-PROSE-BAD`'s anchor:
```
self-test FAIL: render_contract (a) extraction [mode 2: shape mismatch] R-HEAD-PROSE-MID: extracted text is missing required substring(s) ["+ C2's threshold + GT-12?"]
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: extraction_rows: row 11 (R-HEAD-PROSE-MID) (...) != expected (...)
```
The `"+ C2's threshold + GT-12?"` needle is the one that fires, rejecting the
mis-anchored extraction.

**Task 2, mutation 4** — restore, then remove `R-HEAD-PROSE-BAD`'s third needle
and re-point its anchor at the middle-position block:
```
self-test FAIL: render_contract (b) R-HEAD-PROSE-BAD (doc label 'Non-conforming — an input carrying unparenthesized prose:') scored well-formed, expected malformed
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: extraction_rows: row 8 (R-HEAD-PROSE-BAD) (...) != expected (...)
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: fixture_shape: R-HEAD-PROSE-BAD shape ("C2's threshold", 'bill composition unknown') != expected discriminating shape ("C2's threshold", 'bill composition unknown', "+ C2's threshold\n→")
```
Exit 1 as required. Without the third needle the shape guard alone would have
passed the mis-anchored extraction vacuously; here the reused middle-position
bytes also fail control (b)'s own verdict assertion for `R-HEAD-PROSE-BAD`
(expects malformed, gets well-formed), and the registry-lock arms independently
catch the anchor/shape drift — three independent detections of the same
regression, not one.

**Task 3, mutation 5** — delete the `R-HEAD-PROSE-MID` mention from
`docs/ARCHITECTURE.md`'s QUAL-01 row: the token appears TWICE in the row (per the
plan's own action text — once in the quartet enumeration, once in the corrected
overclaiming sentence), so the reproduction strips every occurrence on the row
(matching control (m)'s own `line.replace(token, "")`), not a single substring:
```
self-test FAIL: render_contract (m) POSITIVE: docs/ARCHITECTURE.md: the '| QUAL-01 |' row is missing required token 'R-HEAD-PROSE-MID'
```
Exit 1, naming both the token and the file.

**Task 3, mutation 6** — delete the fifth entry from `_QUAL01_DOC_ROW_TOKENS`
alone:
```
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: qual01_doc_row_tokens: (...4 entries...) != expected (...5 entries...)
self-test FAIL: render_contract (m) NEGATIVE-CASE COUNT FLOOR: derived 8 (file, token) case(s) from 2 doc row(s) x 4 token(s) != expected 10
```
Exit 1 on the registry-lock arm as required, plus the count floor independently.

**Task 3, mutation M-FLOOR** — revert the `(m)` NEGATIVE-CASE COUNT FLOOR's `if`
condition and f-string message tail alone (from 10 back to 8), leaving
`_QUAL01_DOC_ROW_TOKENS` at its five entries:
```
self-test FAIL: render_contract (m) NEGATIVE-CASE COUNT FLOOR: derived 10 (file, token) case(s) from 2 doc row(s) x 5 token(s) != expected 8
```
Exact match to the plan's specified message, byte for byte.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 — self-inflicted bug] Line-wrap broke the WR-03 qualification's
required single-line grep**
- **Found during:** Task 2, immediately after the edit, running the acceptance
  criteria's own grep commands.
- **Issue:** The parenthetical "(eleven was the table's size at Phase 11, when
  this was found; the table has grown since)" was split across two `#`-comment
  lines, so `grep -c "eleven was the table's size at Phase 11"` reported `0`
  instead of the required `1` — the exact failure class 13-07 documented in this
  plan's own read_first section.
- **Fix:** Rewrapped the parenthetical onto the same physical line as the
  sentence it qualifies.
- **Files modified:** `scripts/check-quality-harness.py`.
- **Commit:** `aa217a5`.

**2. [Rule 3 — blocking prerequisite] VAL-03 blocked on a missing `.venv`**
- **Found during:** Task 3's closing verification, first `bash
  scripts/check-firewall-battery.sh` run.
- **Issue:** This worktree had no `.venv`, so no pytest-capable interpreter was
  found; VAL-03 reported `[PREREQ]` and the battery printed `FIREWALL: BLOCKED`
  (exit 2), not a gate failure.
- **Fix:** Ran `uv sync` (documented remedy in CLAUDE.md's own VAL-03 note) to
  create `.venv`, then re-ran the battery to `FIREWALL: GREEN (23/23)`.
- **Files modified:** none (`.venv/` is gitignored, not committed).

### Findings (not fixed — pre-existing, out of this plan's scope)

**3. Two unrelated pre-existing "eleven" mentions make the literal acceptance-
criteria grep report 2, not 0**
- **Found during:** Task 2, re-running `grep -vn '^\s*#' scripts/check-quality-harness.py | grep -ci eleven` after making all five prescribed fixes.
- **Detail:** `_RENDER_REGISTRY_FIELDS` ("eleven today, ten registries") counts
  dataclass fields, not fixtures — unchanged by this plan, which added registry
  entries, not a new field. The `--run`/`--rejudge` scoreline TSV docstring
  ("eleven-column") counts an unrelated TSV column count. Neither is among the
  plan's six enumerated fix locations; renumbering either to "twelve" would be a
  false statement about a quantity this plan did not change.
- **Disposition:** Left unchanged. Recorded here per the plan's own A-02
  discipline treating a disagreement as a finding, not something to force-fix.

## Self-Check: PASSED

- `shared/spine/references/output-template.md` — FOUND, contains R7's disclosure
  sentence (1) and the `R-HEAD-PROSE-MID` worked example (1).
- `shared/spine/SKILL-body.md` — FOUND, contains R7's disclosure sentence (1).
- `shared/spine/references/validation-rubric.md` — FOUND, contains R7's
  disclosure sentence (1) inline on one physical line.
- `scripts/check-quality-harness.py` — FOUND, contains `R-HEAD-PROSE-MID` (13
  occurrences: extraction row, fixture shape, `expected_ids`,
  `expected_extraction_rows`, `expected_fixture_shape`, `_get` binding, `(b)`
  control x2 (comment + code), `render_locked_fixture_ids`, doc-row token
  registry x2, doc-row expected-tokens x1).
- `CLAUDE.md` — FOUND, contains `R-HEAD-PROSE-MID`.
- `docs/ARCHITECTURE.md` — FOUND, contains `R-HEAD-PROSE-MID`.
- Commit `5806b7b` — FOUND in `git log --oneline`.
- Commit `aa217a5` — FOUND in `git log --oneline`.
- Commit `492c3a5` — FOUND in `git log --oneline`.
- `_CHAIN_DETECTOR_PINNED_DIGEST` — confirmed unchanged
  (`sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3`,
  count 1).
- `bash scripts/check-firewall-battery.sh` — re-run after all three commits
  landed: `FIREWALL: GREEN (23/23)`, exit 0.
