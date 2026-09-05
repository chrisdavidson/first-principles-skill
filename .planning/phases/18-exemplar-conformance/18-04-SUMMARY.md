---
phase: 18-exemplar-conformance
plan: 04
subsystem: testing
tags: [markdown, conformance-measurement, quality-harness, worked-examples]

# Dependency graph
requires:
  - phase: 18-exemplar-conformance
    plan: 01
    provides: marked/silent untraced-claim columns on report-conformance.py, the published
      Disclosed-bounds section, and Cn-numbered chain headings across the ten
      section-readable shared/examples files
  - phase: 18-exemplar-conformance
    plan: 02
    provides: the nested-parenthetical chain-head landmine finding and the
      per-physical-line claim citation finding
  - phase: 18-exemplar-conformance
    plan: 03
    provides: SectionResolutionError == 0 corpus-wide on both surfaces (ROADMAP
      criterion 1 closed), and the citation-placement-on-first-physical-line finding
provides:
  - self-application.md, software-systems.md and personal-general.md now read
    0 malformed chain blocks, 0 non-conforming verdict cells and 0
    silently-untraced claims on both shared-examples and generated-twin surfaces
  - a fourth detector-reach finding (R10's disclosed bound, already published by
    output-template.md): a chain whose head or first (non-final) hop closes its
    own sentence before the second arrow is scored malformed even though it
    violates none of R1-R9 — fixed file-side by stripping terminal punctuation
    from every non-final hop after de-wrapping
  - per-file conclusion_claims values for plan 18-07's _CLAIM_FLOORS:
    self-application 9, software-systems 8, personal-general 7 (all zero cut)
affects: [18-05, 18-06, 18-07, 18-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Non-final-hop terminal-punctuation removal: after de-wrapping a chain
      onto one physical line per hop, `_chain_block_well_formed`'s
      `_segment_sentence_closed` check treats ANY hop ending in `.`/`!`/`?` as
      the end of the candidate segment, so a following arrow-led hop is never
      absorbed and the joined candidate falls one arrow short. Every hop
      before the LAST one in a chain must end without sentence-terminal
      punctuation (comma, semicolon, or no punctuation) — exactly what
      output-template.md §4 states in prose (\"intermediate hops carry no
      terminal punctuation in this project's worked examples\") but which
      plans 18-02/18-03 had not yet needed to apply, since their fixes were to
      single-hop or already-short chains."
    - "Chain and confidence-line citations must use the literal `Cn` token
      immediately adjacent (no intervening space) to trace: `chain C1` traces
      (`_cites_chain`'s normalized form `c1` is a substring of `chain c1`),
      but the spelled-out `Chain 1` (digit only, no `C`) does NOT — there is a
      space between `n` and `1` so no `c1` substring exists. Confidence lines
      that narrate per-chain confidence in prose (\"Chain 1 is HIGH...\") must
      be rewritten to the `chain C1` token form to trace."

key-files:
  created: []
  modified:
    - shared/examples/personal-general.md
    - shared/examples/software-systems.md
    - shared/examples/self-application.md
    - first-principles/agents/references/examples/personal-general.md
    - first-principles/agents/references/examples/software-systems.md
    - first-principles/agents/references/examples/self-application.md
    - docs/conformance-baseline.md
    - docs/data/conformance.json

key-decisions:
  - "All resolvable §6 claims across the three files were CITED, not marked.
    Zero claims used the `no chain — flagged assumption only` marker and zero
    claims were cut; every one of the 24 claims (7 + 8 + 9) traces to at
    least one of its file's own chains via inline `(chain Cn)` / `(chains Cn
    and Cm)` citation. `marked_untraced_claims == 0` on all six rows
    (shared-examples + generated-twin x 3 files) confirms this."
  - "Verdict-cell compression (DEC-C) kept the Verification column's full
    existing prose unchanged in all 17 cells (5 + 6 + 6) across the three
    files; only the Verdict cell itself was rewritten to `<Token> —
    <justification>` with U+2014 EM DASH, and every justification is a
    compressed restatement of that same row's Verification text rather than
    new analysis."
  - "software-systems.md's and self-application.md's confidence lines,
    which previously narrated per-chain confidence with spelled-out ordinals
    (\"Chain 1 is HIGH confidence\", \"Chain 2 ... is HIGH confidence\"), were
    rewritten to the citable `chain C1`/`chain C2`/`chain C3` token form —
    a pure terminology substitution with no change to the stated confidence
    levels or reasoning."

patterns-established:
  - "The R10 disclosed-bound fix (strip terminal punctuation from every
    non-final hop) is now proven on six chains across two files
    (software-systems.md's three, self-application.md's three) and should be
    applied proactively — not discovered by trial — to any remaining
    multi-hop chain de-wrap in plans 18-05/18-06."

requirements-completed: [CONF-04, CONF-05]

# Metrics
duration: ~70min (estimated; explicit start timestamp not captured)
completed: 2026-09-05
---

# Phase 18 Plan 04: Exemplar Conformance — Chain De-Wrap, Verdict Cells, and Claim Citations for Three Worked Examples Summary

**De-wrapped six multi-hop chains (three in software-systems.md, three in self-application.md) onto one physical line per hop, discovering and fixing a fourth detector-reach landmine — a non-final hop's terminal punctuation truncates chain absorption before the second arrow (R10's disclosed bound) — then brought all 17 verdict cells and 24 section-6 claims across all three of this plan's files to zero defects by citation, with zero claims marked or cut.**

## Performance

- **Duration:** ~70 min (estimated)
- **Completed:** 2026-09-05
- **Tasks:** 3 completed
- **Files modified:** 8 (3 shared examples, 3 generated twins, 2 conformance artifacts)

## Accomplishments

- `personal-general.md` (already 0 malformed blocks): all 5 Verdict cells rewritten to
  `<Token> — <justification>` form with U+2014 EM DASH, Verification column kept intact;
  all 7 §6 claims cited inline to chain C1 and/or C2 — zero marked, zero cut.
- `software-systems.md`: all 3 chain blocks de-wrapped to one physical line per hop
  (`heading_chain_blocks == 3`, `heading_malformed_blocks == 0`); all 6 Verdict cells
  conformed; all 8 §6 claims cited — zero marked, zero cut.
- `self-application.md`: all 3 chain blocks de-wrapped to one physical line per hop
  (`heading_chain_blocks == 3`, `heading_malformed_blocks == 0`); all 6 Verdict cells
  conformed; all 9 §6 claims cited (including rewriting the spelled-out "Chain 1"/"Chain
  2"/"Chain 3" confidence narration to the citable `chain C1`/`C2`/`C3` token form) —
  zero marked, zero cut.
- **Plan-scoped rollup, both surfaces, all three files:** `heading_malformed_blocks`,
  `nonconforming_verdict_cells`, and `silent_untraced_claims` each sum to exactly `0`
  across the six rows (shared-examples + generated-twin × 3 files). No marked claim opens
  with a prescribed lead-in (`**Recommended approach:**`, `**Key insight:**`,
  `**Trade-offs acknowledged:**`) — D-03 holds trivially since zero claims were marked at
  all.
- `scripts/check-quality-harness.py` is byte-identical to its state at the plan's starting
  commit `4f15951` (`git diff --stat` — no output, zero diff). All three CONTRACT-06 sha256
  pins are intact.
- `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (24/24)`.
- `git status --porcelain` is empty after the final commit.

## Per-file `conclusion_claims` values (for plan 18-07's `_CLAIM_FLOORS`)

| File | `conclusion_claims` (both surfaces) | `untraced_claims` | `marked_untraced_claims` | `silent_untraced_claims` | Claims cut |
|---|---|---|---|---|---|
| `personal-general` | 7 | 0 | 0 | 0 | none |
| `software-systems` | 8 | 0 | 0 | 0 | none |
| `self-application` | 9 | 0 | 0 | 0 | none |

No claim was cut by name in this plan. All 24 claims (7 + 8 + 9) are cited to at least one
of their file's own chains.

## Task Commits

Each task was committed atomically:

1. **Task 1: personal-general.md — verdict cells and claim citations** - `a2c85e1` (fix)
2. **Task 2: software-systems.md — de-wrap three chains, then verdict cells and citations** - `4b76ba8` (fix)
3. **Task 3: self-application.md — de-wrap three chains, then verdict cells and citations** - `c20d953` (fix)

**Plan metadata:** committed together with this SUMMARY.md (worktree mode; STATE.md/ROADMAP.md
updates deferred to the orchestrator).

## Files Created/Modified

- `shared/examples/personal-general.md` — 5 Verdict cells compressed to `<Token> —
  <justification>` form; 7 §6 claims cited inline (`(chain C1)` / `(chain C2)` /
  `(chains C1 and C2)`); Confidence line's spelled-out "Chain 1"/"Chain 2" rewritten to
  `chain C1`/`chain C2`
- `shared/examples/software-systems.md` — 3 chain blocks de-wrapped to one physical line
  per hop, with terminal punctuation stripped from every non-final hop; 6 Verdict cells
  conformed; 8 §6 claims cited inline
- `shared/examples/self-application.md` — 3 chain blocks de-wrapped to one physical line
  per hop, with terminal punctuation stripped from every non-final hop; 6 Verdict cells
  conformed; 9 §6 claims cited inline, including the Confidence line's per-chain narration
- `first-principles/agents/references/examples/{personal-general,software-systems,self-application}.md`
  — regenerated twins via `python3 scripts/sync-content.py --write`
- `docs/conformance-baseline.md` / `docs/data/conformance.json` — regenerated after every
  task's edit

## Decisions Made

- **R10 disclosed-bound fix, found during Task 2.** After de-wrapping software-systems.md's
  Chain 1 onto one physical line per hop, the chain still scored malformed. Tracing through
  `_chain_block_well_formed` directly showed the cause: hop 1 ended with a period, which
  `_segment_sentence_closed` reads as the end of the candidate segment, so hop 2's arrow
  is never absorbed and the joined candidate contains only one arrow (fails the two-arrow
  requirement). This is exactly `output-template.md`'s own published R10 bound ("a chain
  whose head or first hop closes its own sentence before the next `→` ... is scored
  malformed for that reason alone ... intermediate hops carry no terminal punctuation in
  this project's worked examples"). Fixed by removing the trailing period from every
  non-final hop in all six chains (three in software-systems.md, three in
  self-application.md), joining internal sentence breaks with semicolons instead where
  needed to preserve readability. This is a formatting-only fix (DEC-B): no wording,
  number, or inference was changed, only trailing punctuation.
- Every citation was placed on the exact first physical line the extractor reads for that
  claim — the bold lead-in's own line for a `**Label:**` claim, the list marker's own line
  for a numbered/bulleted claim — per the per-physical-line finding plans 18-02 and 18-03
  documented. All three files in this plan use hard-wrapped prose (unlike personal-general.md's
  single-line paragraphs), so this placement rule was load-bearing for every multi-line
  claim in software-systems.md and self-application.md.
- Chose to CITE every resolvable claim rather than marking any of them, even where marking
  was legally available (i.e., the claim did not open with a prescribed lead-in). This
  produces a stronger conformance signal (`marked_untraced_claims == 0`) than the plan's
  floor required and leaves no ambiguity about which claims are genuinely unestablished
  versus merely uncited.
- self-application.md's and software-systems.md's Confidence lines previously narrated
  confidence per chain using spelled-out ordinals ("Chain 1 is HIGH confidence"), which do
  not trace under `_cites_chain` (no `C1`-shaped token, just a digit separated from the word
  "Chain" by a space). Rewrote these to the citable `chain C1`/`chain C2`/`chain C3` token
  form without changing the stated confidence levels.

## Deviations from Plan

None — plan executed exactly as written. The R10 disclosed-bound fix described above was a
file-side repair discovered while iterating toward the acceptance criteria (the plan's own
`<interfaces>` section had already documented the general shape of this landmine via
`_CHAIN_FORM_LINE_RE`'s nested-parenthetical note and DEC-B's residual note; this plan found
and closed the sibling terminal-punctuation shape of the same detector-reach class), not a
deviation from the plan's tasks or scope.

## Issues Encountered

- Chasing software-systems.md's Chain 1 malformed reading after de-wrapping required
  stepping outside `report-conformance.py`'s `detect_defects` wrapper and calling
  `_slice_sections` / `_chain_blocks` / `_chain_block_well_formed` directly against the
  draft file to see which candidate segment the detector was actually building — the
  wrapper only reports pass/fail per block, not the intermediate segment-absorption state.
  This diagnostic technique (direct import of `check-quality-harness.py` and manual
  function calls) is what surfaced the terminal-punctuation cause; it is not itself a code
  change and the detector was never modified.
- Same environment finding recorded in plans 18-01/18-02/18-03: `bash
  scripts/check-firewall-battery.sh` initially needs a pytest-capable interpreter for VAL-03;
  resolved by `uv sync`, which creates a local, gitignored `.venv`. No repo change.
- This worktree's `.git` HEAD was on an unrelated Phase-12-era commit (`d4da381`) at spawn
  time, several commits behind the expected base (`4f15951`, which already includes
  18-01/18-02/18-03's merged work); corrected via `git reset --hard` to the expected base
  per the worktree branch-check protocol before any plan work began. Phase 18 planning
  artifacts (`18-04-PLAN.md`, `18-CONTEXT.md`, `18-RESEARCH.md`, `18-PATTERNS.md`,
  `PROJECT.md`, `STATE.md`, `config.json`) were copied in from the main repo checkout
  before reading, since `git worktree add` only checks out tracked files and `.planning/`
  is gitignored except for `NN-MM-SUMMARY.md` files.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Plans 18-05/18-06 (the remaining exemplar-conformance passes) can reuse this plan's R10
  disclosed-bound fix (strip terminal punctuation from every non-final hop after
  de-wrapping) directly, without re-discovering it by trial — apply proactively to any
  multi-hop chain de-wrap.
- Plan 18-07's `_CLAIM_FLOORS` should read this plan's three entries — `self-application`
  9, `software-systems` 8, `personal-general` 7 — alongside the entries plans 18-02 and
  18-03 already produced for the four previously-unreadable drill files.
- No blockers. `scripts/check-quality-harness.py` remains untouched and all three sha256
  CONTRACT-06 pins are intact (confirmed via `git diff --stat` against the plan's starting
  commit `4f15951`).

## Self-Check: PASSED

- FOUND: `shared/examples/personal-general.md`
- FOUND: `shared/examples/software-systems.md`
- FOUND: `shared/examples/self-application.md`
- FOUND: `first-principles/agents/references/examples/personal-general.md`
- FOUND: `first-principles/agents/references/examples/software-systems.md`
- FOUND: `first-principles/agents/references/examples/self-application.md`
- FOUND: `docs/conformance-baseline.md`
- FOUND: `docs/data/conformance.json`
- FOUND commit: `a2c85e1` (Task 1)
- FOUND commit: `4b76ba8` (Task 2)
- FOUND commit: `c20d953` (Task 3)

---
*Phase: 18-exemplar-conformance*
*Completed: 2026-09-05*
