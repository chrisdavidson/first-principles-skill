---
phase: 13-chain-head-grammar
plan: 09
subsystem: quality-harness
tags: [chain-head-grammar, rendering-contract, gap-closure, BL-02]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar (plans 01-08)
    provides: the chain-head grammar (R7/R8), R7's disclosed positional
      bound (13-08, BL-01), the scored-not-extracted consumption floor
      (13-05, CR-01), and the dispatch-reachability leg (13-06, CR-02)
provides:
  - R9, the head-only scope note rewritten with the GT-leading-hop
    refusal `_ARROW_LED_GT_RE` actually enforces, and the prescribed
    rewrite, byte-identical on all three canonical surfaces
    (output-template.md, SKILL-body.md, validation-rubric.md) and in the
    generated tree
  - two new chain-head worked examples, `R-HEAD-GTHOP-BAD` and
    `R-HEAD-GTHOP-OK`, pinning both directions of the refusal (malformed)
    and its remedy (well-formed) in tracked bytes, extracted and scored
    at self-test time by the unmodified `_chain_block_well_formed`
  - a fourteen-fixture consumption floor (up from twelve) with two new
    `(b)` verdict controls and discriminating needles proven to
    discriminate in both directions
  - both published `| QUAL-01 |` doc rows (CLAUDE.md, docs/ARCHITECTURE.md)
    stating nine literals and fourteen worked examples, with a registered
    remedy token (`R-HEAD-GTHOP-OK`) and an updated NEGATIVE-CASE COUNT
    FLOOR (12, up from 10)
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A published contract note must be scoped to exactly what its pinned
      mechanical detector enforces, not to what would be ideal — when the
      two diverge, the fix is disclosure in the note (this plan), never
      widening or anchoring the frozen detector (CONTRACT-06)."
    - "A minimal-pair fixture (same hop, one clause reordered) scored in
      opposite directions by the same unmodified detector is the
      load-bearing way to pin both a refusal and its prescribed remedy in
      tracked, falsifiable bytes rather than prose assertion alone."

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
  - "A-01 (BL-02 fork), as pre-decided by the plan: scoped the published
    scope note to what `_ARROW_LED_GT_RE` enforces rather than relaxing
    the detector. `_chain_block_well_formed`, `_CHAIN_FORM_LINE_RE` and
    `_ARROW_LED_GT_RE` are byte-unchanged; every edit in this plan's
    `git diff` against the pre-plan base lands at or beyond line 6502 in
    `scripts/check-quality-harness.py`, well clear of
    `_chain_block_well_formed` (~line 4276) and both regexes
    (~lines 4104-4200)."
  - "A-02 (registration as R9): the scope note is now a registered
    literal in `_RENDER_RULE_LITERALS`, required on all three surfaces
    via `_RENDER_SURFACE_REQUIRED_RULES`, with its own required clause
    and a recomputed `expected_literal_digest`. This widens the literal
    registry from eight to nine entries and moved control (k)'s
    CASE-COUNT FLOOR from 20 (8+8+4) to 23 (9+9+5) in both its constant
    and its comment."
  - "A-03 confirmed by direct re-measurement before any edit, against the
    live unmutated module, using the exact bytes this plan ships: the
    GT-leading hop (`→ GT-4's stated duty cycle is the binding term in
    both estimates`) scores False (malformed); the prescribed rewrite
    (`→ the duty cycle stated in GT-4 is the binding term in both
    estimates`) scores True (well-formed) — matching the plan's
    `<measured_facts>` table exactly."

metrics:
  duration: ~1.5h
  files_modified: 9
  tasks_completed: 3
  completed: 2026-09-02
---

# Phase 13 Plan 09: GT-leading-hop refusal (BL-02) Summary

The head-only scope note now states, on all three canonical surfaces and in
the generated tree, that a hop must not begin with a `GT-N` identifier —
closing the gap where the published note unconditionally licensed a
possessive-hop pattern (`GT-4's stated duty cycle`) that the frozen
`_ARROW_LED_GT_RE` refuses because it reads any GT-N-leading hop as the head
of a new chain.

## What was built

**Task 1 — R9: the scope note's GT-leading-hop refusal.** Appended one new
sentence to the existing scope note — "One exception: a hop must not begin
with a `GT-N` identifier, which the form check reads as the head of a new
chain and which therefore ends this one — write `→ the duty cycle stated in
GT-4 is the binding term`, not `→ GT-4's stated duty cycle is the binding
term`." — byte-identical across `shared/spine/references/output-template.md`,
`shared/spine/SKILL-body.md`, and inline on one physical line in
`shared/spine/references/validation-rubric.md`. Registered it as `R9` in
`_RENDER_RULE_LITERALS`, added `R9` to all three `_RENDER_SURFACE_REQUIRED_RULES`
tuples, added `"R9": "a hop must not begin with a \`GT-N\` identifier"` to
`expected_literal_clauses`, and recomputed `expected_literal_digest` from the
edited registry:
`sha256:199469956b572956ff2b09cbd82e48389d989c6eecff5382d0b96ab34bd2894b`.
Moved control (k)'s CASE-COUNT FLOOR constant and comment from `20`
(8 + 8 + 4) to `23` (9 + 9 + 5).

**Task 2 — `R-HEAD-GTHOP-BAD` / `R-HEAD-GTHOP-OK` minimal pair.** Added two
worked-example blocks to `output-template.md` §4, immediately after 13-08's
`R-HEAD-PROSE-MID` block: `**Non-conforming — a hop beginning with a GT-N
identifier:**` (the possessive GT-4-leading hop, scored malformed) and
`**Conforming — the same hop with the identifier moved off the front:**`
(the identical hop with the clause reordered, scored well-formed). Registered
both across `_RENDER_CONTRACT_EXTRACTION_TABLE`, `_RENDER_FIXTURE_SHAPE` (with
discriminating first needles `"→ GT-4's stated duty cycle"` /
`"→ the duty cycle stated in GT-4"` and a shared head needle
`"2.20× at full duty"`), `expected_ids` (twelve → fourteen, sorted),
`expected_extraction_rows`, `expected_fixture_shape`, the `_get` bindings, two
new `(b)` verdict controls routed through the existing `_score_chain` wrapper
(no fifth recorder site — control (t)'s lock at exactly 4 sites stayed
green), and `render_locked_fixture_ids` (twelve → fourteen). Updated every
current-set "twelve" prose mention to "fourteen": `_render_contract_fixtures`'s
docstring, the `expected_fixture_shape` comment's denominator,
`_selftest_render_contract`'s "measured verdicts" and "…-id set" sentences
(plus a new sentence naming plan 13-09/BL-02), and control (p)'s comment.
Left the WR-03 historical "eleven was the table's size at Phase 11…"
qualification byte-unchanged, per the plan's explicit instruction.

**Task 3 — Both `| QUAL-01 |` doc rows.** Updated CLAUDE.md:165 and
docs/ARCHITECTURE.md:146 (kept byte-identical to each other) to state
"fourteen worked examples", extend the chain-head enumeration to name the new
pair, bound leg (2) to "nine hand-transcribed rule literals (R1-R9)… the
rubric declares R1, R6, R7, R8 and R9; the two contract surfaces declare all
nine", and add a DISCLOSED LIMITATIONS sentence naming R9's exception and
that `R-HEAD-GTHOP-BAD`/`R-HEAD-GTHOP-OK` pin both directions as measured, not
prescribed. Registered `R-HEAD-GTHOP-OK` (deliberately the `-OK` id, not
`-BAD`) as a sixth `_QUAL01_DOC_ROW_TOKENS` entry and moved the (m)
NEGATIVE-CASE COUNT FLOOR's four hardcoded sites (comment, `if` condition,
f-string message, docstring) from 10 (2×5) to 12 (2×6).

## Verification (run in order, on the tracked tree, after all three tasks)

1. `python3 scripts/check-quality-harness.py --self-test` → exit 0, all
   sub-checks PASSED including `render_contract` and `chain_detector_pin`.
2. `python3 scripts/sync-content.py --check` → exit 0.
3. `python3 scripts/check-traceability.py --self-test` → exit 0.
4. `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (23/23)`,
   exit 0. (VAL-03 initially reported `[PREREQ]`/BLOCKED — no `.venv` existed
   in this worktree — ran `uv sync` to create it, then re-ran to GREEN, same
   remedy 13-08 documented.)
5. `grep -c 'sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3' scripts/check-quality-harness.py` → `1`.
6. `git diff 78613b5043755f3ad9503d6c9eb3362930fddcff HEAD -- scripts/check-quality-harness.py` reviewed by eye:
   every hunk starts at line 6502 or later, well clear of
   `def _chain_block_well_formed` (~line 4276) and both frozen regexes
   (~lines 4104-4200). `_CHAIN_DETECTOR_PINNED_DIGEST` confirmed unchanged
   at `sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3`.

## Pre/post values of both hardcoded count floors

| Floor | Pre-plan | Post-plan |
|---|---|---|
| control (k) CASE-COUNT FLOOR (`expected_missing_case_count`) | `20` (8+8+4) | `23` (9+9+5) |
| control (m) NEGATIVE-CASE COUNT FLOOR (`qual01_negative_case_count` expectation) | `10` (2×5) | `12` (2×6) |

## Mutations (all ten reproduced on disposable `rsync -a --exclude .git
--exclude .venv` scratch copies under the session scratchpad; `git status
--porcelain` on the tracked tree confirmed empty of any mutation leakage
before the first mutation and after every mutation cycle in each task)

**Task 1, MUTATION 1** — delete R9's `One exception:` sentence from
`shared/spine/references/validation-rubric.md` alone:
```
self-test FAIL: render_contract (i) POSITIVE: shared/spine/references/validation-rubric.md: rule R9 is missing — deleted from this surface
```
Exit 1, naming both R9 and the surface, as required.

**Task 1, MUTATION 2** — restore, then remove `"R9"` from
`_RENDER_SURFACE_REQUIRED_RULES`'s rubric tuple only, leaving
`expected_required_rules` alone:
```
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: required_rules: {'shared/spine/references/output-template.md': ('R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9'), 'shared/spine/SKILL-body.md': ('R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9'), 'shared/spine/references/validation-rubric.md': ('R1', 'R6', 'R7', 'R8')} != expected {'shared/spine/references/output-template.md': ('R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9'), 'shared/spine/SKILL-body.md': ('R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9'), 'shared/spine/references/validation-rubric.md': ('R1', 'R6', 'R7', 'R8', 'R9')}
self-test FAIL: render_contract (k) CASE-COUNT FLOOR: expected 23 cases (derived sum 22), ran 22
```
Exit 1 on the `required_rules` registry-lock arm as required, plus the
CASE-COUNT FLOOR independently. Proves R9 cannot be quietly de-scoped from
the rubric.

**Task 1, MUTATION K-FLOOR** — restore, then revert
`expected_missing_case_count` alone from `23` back to `20`, leaving
`_RENDER_SURFACE_REQUIRED_RULES` at nine/nine/five:
```
self-test FAIL: render_contract (k) CASE-COUNT FLOOR: expected 20 cases (derived sum 23), ran 23
```
Exact match to the plan's specified message, byte for byte.

**Task 2, MUTATION 3** — delete the `R-HEAD-GTHOP-OK` `(b)` verdict block
entirely:
```
self-test FAIL: render_contract (p) CONSUMPTION FLOOR: fixture id(s) ['R-HEAD-GTHOP-OK'] are never scored by any control and not named in a reported problem
```
Exact match to the plan's specified message.

**Task 2, MUTATION 4** — restore, then flip `R-HEAD-GTHOP-BAD`'s control
direction (assert it scores malformed):
```
self-test FAIL: render_contract (b) R-HEAD-GTHOP-BAD (doc label 'Non-conforming — a hop beginning with a GT-N identifier:') scored malformed, expected well-formed
```
Exit 1 naming `R-HEAD-GTHOP-BAD` from control (b) — the non-vacuity proof for
the refusal half.

**Task 2, MUTATION 5** — restore, then flip `R-HEAD-GTHOP-OK`'s control
direction:
```
self-test FAIL: render_contract (b) R-HEAD-GTHOP-OK (doc label 'Conforming — the same hop with the identifier moved off the front:') scored well-formed, expected malformed
```
Exit 1 naming `R-HEAD-GTHOP-OK` from control (b) — the non-vacuity proof for
the remedy half.

**Task 2, MUTATION 6** — restore, then swap the two new fixtures' extraction
anchors:
```
self-test FAIL: render_contract (a) extraction [mode 2: shape mismatch] R-HEAD-GTHOP-BAD: extracted text is missing required substring(s) ["→ GT-4's stated duty cycle"]
self-test FAIL: render_contract (a) extraction [mode 2: shape mismatch] R-HEAD-GTHOP-OK: extracted text is missing required substring(s) ['→ the duty cycle stated in GT-4']
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: extraction_rows: row 12 (R-HEAD-GTHOP-BAD) (...) != expected (...)
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: extraction_rows: row 13 (R-HEAD-GTHOP-OK) (...) != expected (...)
```
Both fixtures' shape guards fired independently on their own first needle —
proving the needles discriminate in both directions.

**Task 3, MUTATION 7** — delete the `R-HEAD-GTHOP-OK` mention from
`CLAUDE.md`'s QUAL-01 row only:
```
self-test FAIL: render_contract (m) POSITIVE: CLAUDE.md: the '| QUAL-01 |' row is missing required token 'R-HEAD-GTHOP-OK'
```
Exit 1, naming both the token and the file.

**Task 3, MUTATION 8** — restore, then delete the sixth entry from
`_QUAL01_DOC_ROW_TOKENS` alone:
```
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: qual01_doc_row_tokens: ('emission rendering contract', 'validation-rubric.md', 'scored by a control, not merely extracted', 'dispatch reachability', 'R-HEAD-PROSE-MID') != expected ('emission rendering contract', 'validation-rubric.md', 'scored by a control, not merely extracted', 'dispatch reachability', 'R-HEAD-PROSE-MID', 'R-HEAD-GTHOP-OK')
self-test FAIL: render_contract (m) NEGATIVE-CASE COUNT FLOOR: derived 10 (file, token) case(s) from 2 doc row(s) x 5 token(s) != expected 12
```
Exit 1 on the `qual01_doc_row_tokens` registry-lock arm as required, plus the
count floor independently.

**Task 3, MUTATION M-FLOOR** — restore, then revert the (m) NEGATIVE-CASE
COUNT FLOOR's `if` condition and f-string message tail alone (from 12 back
to 10), leaving `_QUAL01_DOC_ROW_TOKENS` at its six entries:
```
self-test FAIL: render_contract (m) NEGATIVE-CASE COUNT FLOOR: derived 12 (file, token) case(s) from 2 doc row(s) x 6 token(s) != expected 10
```
Exact match to the plan's specified message, byte for byte.

## Deviations from Plan

None — plan executed exactly as written. All measured facts (the malformed
verdict for the GT-leading hop and the well-formed verdict for the
prescribed rewrite) were re-confirmed against the live unmutated module
before any edit, and matched the plan's `<measured_facts>` table exactly.

## Self-Check: PASSED

- `shared/spine/references/output-template.md` — FOUND, contains R9's
  refusal sentence (1) and both `R-HEAD-GTHOP-BAD`/`R-HEAD-GTHOP-OK` worked
  examples.
- `shared/spine/SKILL-body.md` — FOUND, contains R9's refusal sentence (1).
- `shared/spine/references/validation-rubric.md` — FOUND, contains R9's
  refusal sentence (1) inline on one physical line.
- `scripts/check-quality-harness.py` — FOUND, contains `R-HEAD-GTHOP-BAD`
  and `R-HEAD-GTHOP-OK` (extraction row, fixture shape, `expected_ids`,
  `expected_extraction_rows`, `expected_fixture_shape`, `_get` bindings,
  `(b)` control blocks, `render_locked_fixture_ids`, doc-row token registry).
- `CLAUDE.md` — FOUND, contains `R-HEAD-GTHOP-OK` and `R1-R9`.
- `docs/ARCHITECTURE.md` — FOUND, contains `R-HEAD-GTHOP-OK` and `R1-R9`.
- Commit `65cf89e` — FOUND in `git log --oneline`.
- Commit `3444579` — FOUND in `git log --oneline`.
- Commit `16d1854` — FOUND in `git log --oneline`.
- `_CHAIN_DETECTOR_PINNED_DIGEST` — confirmed unchanged
  (`sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3`,
  count 1).
- `bash scripts/check-firewall-battery.sh` — re-run after all three commits
  landed: `FIREWALL: GREEN (23/23)`, exit 0.
