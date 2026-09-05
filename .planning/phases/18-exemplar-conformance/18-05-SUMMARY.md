---
phase: 18-exemplar-conformance
plan: 05
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
    plan: 04
    provides: the R10 disclosed-bound fix (strip terminal punctuation from every
      non-final hop) proven on six chains across two files, and the
      per-physical-line claim-citation placement finding
provides:
  - personal-general-2.md, product-business-2.md and software-systems-2.md now
    read 0 malformed chain blocks, 0 non-conforming verdict cells and 0
    silently-untraced claims on both shared-examples and generated-twin surfaces
  - a fifth detector-reach finding: a chain head that joins a GT token with
    non-GT prose clauses via "+" (e.g. "GT-5 (...) + the diagnostic-flagged
    drawdown-tolerance assumption (...)") can never match
    `_CHAIN_FORM_LINE_RE`, because every "+"-joined item must itself be a
    GT-/C-token — fixed by flattening the non-GT clauses into a single
    parenthetical attached to the sole true GT-token
  - per-file conclusion_claims values for plan 18-07's _CLAIM_FLOORS:
    personal-general-2 7, product-business-2 4, software-systems-2 10 (all
    zero cut)
  - corpus-wide heading_malformed_blocks down to 4 (science-engineering and
    science-engineering-2 only, owned by plan 18-06)
affects: [18-06, 18-07, 18-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Prose-joined chain head repair: `_CHAIN_FORM_LINE_RE`'s head grammar is
      `GT/C-token(parens)? (+ GT/C-token(parens)?)*` — every \"+\"-joined
      item after the first must itself be a bare GT-N or Cn token, never a
      prose description of an assumption-table row. A head like `GT-5 (...) +
      the diagnostic-flagged drawdown-tolerance assumption (...) + the
      convention-challenged expected-utility assumption (...)` cannot match
      at any position because the non-GT items break the required
      alternation, regardless of arrow count or trailing punctuation. Fix:
      fold the non-GT clauses into ONE parenthetical on the sole real GT
      token, joined internally with semicolons — same propositional content,
      pure reformatting, no new inference."
    - "Non-final-hop terminal-punctuation removal (from plan 18-04, reused
      here without rediscovery): after de-wrapping a chain onto one physical
      line per hop, every hop before the LAST one must end without
      sentence-terminal punctuation, or `_chain_block_well_formed`'s
      `_segment_sentence_closed` check truncates the join before the next
      arrow is absorbed. Applied here to hop 1 of all three chains in
      personal-general-2.md (already single-line, no wrapping needed) and to
      hop 1 of all three chains in software-systems-2.md (which also needed
      full de-wrapping first)."
    - "product-business-2.md's three chains needed de-wrapping only — no
      chain in this file had a non-final-hop trailing-punctuation problem,
      confirming the R10 landmine is per-chain, not universal to every
      multi-hop chain."

key-files:
  created: []
  modified:
    - shared/examples/personal-general-2.md
    - shared/examples/product-business-2.md
    - shared/examples/software-systems-2.md
    - first-principles/agents/references/examples/personal-general-2.md
    - first-principles/agents/references/examples/product-business-2.md
    - first-principles/agents/references/examples/software-systems-2.md
    - docs/conformance-baseline.md
    - docs/data/conformance.json

key-decisions:
  - "All resolvable §6 claims across the three files were CITED, not marked.
    Zero claims used the `no chain — flagged assumption only` marker and
    zero claims were cut; every one of the 21 claims (7 + 4 + 10) traces to
    at least one of its file's own chains via inline `(chain Cn)` / `(chains
    Cn and Cm)` / `(chains Cn, Cm and Co)` citation.
    `marked_untraced_claims == 0` on all six rows (shared-examples +
    generated-twin × 3 files) confirms this — including
    `product-business-2.md`, the file the plan flagged as highest-risk for
    a forced cut (3 of its 4 claims open with a prescribed lead-in), where
    every claim was resolved by citation to Chain 1 and/or Chain 3."
  - "Chain 3's head restructuring in personal-general-2.md preserves the
    exact same propositional content as the original three-clause '+'-join:
    GT-5's own justification, the diagnostic-flagged drawdown-tolerance
    assumption, and the convention-challenged expected-utility assumption
    are now three semicolon-joined clauses inside GT-5's single
    parenthetical rather than three separate '+'-joined items. No new
    ground truth or inference was authored (D-02); the citation form
    changed, not the claim."
  - "Verdict-cell compression (DEC-C) kept the Verification column's full
    existing prose unchanged in all 21 cells (8 + 7 + 6) across the three
    files; only the Verdict cell itself was rewritten to `<Token> —
    <justification>` with U+2014 EM DASH, and every justification is a
    compressed restatement of that same row's Verification text rather
    than new analysis."
  - "Two prose 'Chain N' mentions in personal-general-2.md's Chain 3 hop 1
    (\"the central-estimate chain (Chain 1) governs\") were rewritten to
    the citable `chain C1` token form during the de-wrap pass, matching
    plan 18-04's established pattern — a pure terminology substitution with
    no change to the stated reasoning."

patterns-established:
  - "The prose-joined-head repair (fold non-GT '+' clauses into the sole
    real GT token's own parenthetical) should be checked proactively on any
    remaining chain head in plans 18-06/18-08 that reads as `GT-N (...) +
    <prose description> (...)` rather than `GT-N (...) + GT-M (...)` — the
    shape is invisible to a purely-arrow-counting read of the chain and was
    only found by tracing `_chain_block_well_formed`'s per-line candidacy
    loop directly against the file."

requirements-completed: [CONF-04, CONF-05]

# Metrics
duration: ~65min (estimated; explicit start timestamp not captured)
completed: 2026-09-05
---

# Phase 18 Plan 05: Exemplar Conformance — Chain De-Wrap, Verdict Cells, and Claim Citations for the Second Group of Three Worked Examples Summary

**Drove `personal-general-2.md`, `product-business-2.md` and `software-systems-2.md` to zero on all three remaining defect families, discovering a fifth detector-reach landmine — a chain head that "+"-joins a GT token with non-GT prose clauses can never match the frozen grammar, regardless of arrow count — and reusing plan 18-04's R10 trailing-punctuation fix on the two files that needed it, closing 9 malformed chain blocks, 21 non-conforming verdict cells and 21 untraced claims with zero claims marked or cut.**

## Performance

- **Duration:** ~65 min (estimated)
- **Completed:** 2026-09-05
- **Tasks:** 3 completed
- **Files modified:** 8 (3 shared examples, 3 generated twins, 2 conformance artifacts)

## Accomplishments

- `personal-general-2.md`: all 3 chain blocks were already de-wrapped (single physical
  line per hop) but scored malformed because each chain's hop 1 closed its own
  sentence before the second arrow (R10) and Chain 3's head "+"-joined a GT token
  with two non-GT prose clauses (a new detector-reach shape, fixed by flattening
  into a single parenthetical); fixed both, then conformed all 8 Verdict cells and
  cited all 7 §6 claims — zero marked, zero cut.
- `product-business-2.md`: all 3 chain blocks de-wrapped to one physical line per
  hop (no trailing-punctuation issue in this file); all 7 Verdict cells conformed;
  all 4 §6 claims cited, including all 3 that open with a prescribed lead-in
  (`**Recommended approach:**`, `**Key insight:**`, `**Trade-offs acknowledged:**`)
  — zero marked, zero cut, despite this being the plan's flagged highest-risk file.
- `software-systems-2.md`: all 3 chain blocks de-wrapped to one physical line per
  hop, with terminal punctuation stripped from each chain's non-final hop (R10);
  all 6 Verdict cells conformed; all 10 §6 claims cited (the largest claim count
  in the corpus) — zero marked, zero cut.
- **Plan-scoped rollup, both surfaces, all three files:** `heading_malformed_blocks`,
  `nonconforming_verdict_cells`, and `silent_untraced_claims` each sum to exactly
  `0` across the six rows (shared-examples + generated-twin × 3 files). No marked
  claim opens with a prescribed lead-in — D-03 holds trivially since zero claims
  were marked at all.
- **Corpus-wide progress check:** `shared-examples` sum of `heading_malformed_blocks`
  is now exactly `4` (`science-engineering` 2 + `science-engineering-2` 2), matching
  the acceptance ceiling and leaving only plan 18-06's two files.
- `scripts/check-quality-harness.py` is byte-identical to its state at the plan's
  starting commit `468ee98` (`git diff --stat` — no output, zero diff). All three
  CONTRACT-06 sha256 pins are intact.
- `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (24/24)`.
- `git status --porcelain` is empty after the final commit.

## Per-file `conclusion_claims` values (for plan 18-07's `_CLAIM_FLOORS`)

| File | `conclusion_claims` (both surfaces) | `untraced_claims` | `marked_untraced_claims` | `silent_untraced_claims` | Claims cut |
|---|---|---|---|---|---|
| `personal-general-2` | 7 | 0 | 0 | 0 | none |
| `product-business-2` | 4 | 0 | 0 | 0 | none |
| `software-systems-2` | 10 | 0 | 0 | 0 | none |

No claim was cut by name in this plan. All 21 claims (7 + 4 + 10) are cited to at
least one of their file's own chains.

## Task Commits

Each task was committed atomically:

1. **Task 1: personal-general-2.md — fix trailing-punctuation chain truncation, conform verdict cells, cite claims** - `9905768` (fix)
2. **Task 2: product-business-2.md — de-wrap three chains, conform verdict cells, cite claims** - `5b976d9` (fix)
3. **Task 3: software-systems-2.md — de-wrap three chains, conform verdict cells, cite claims** - `d3d1f75` (fix)

**Plan metadata:** committed together with this SUMMARY.md (worktree mode; STATE.md/ROADMAP.md
updates deferred to the orchestrator).

## Files Created/Modified

- `shared/examples/personal-general-2.md` — non-final hop trailing punctuation
  stripped from all 3 chains; Chain 3's head flattened from a 3-clause "+"-join
  (one GT token, two non-GT prose clauses) into a single GT-5 parenthetical; all
  8 Verdict cells compressed to `<Token> — <justification>` form; all 7 §6 claims
  cited inline
- `shared/examples/product-business-2.md` — 3 chain blocks de-wrapped to one
  physical line per hop; 7 Verdict cells conformed; 4 §6 claims cited inline
- `shared/examples/software-systems-2.md` — 3 chain blocks de-wrapped to one
  physical line per hop with terminal punctuation stripped from each non-final
  hop; 6 Verdict cells conformed; 10 §6 claims cited inline
- `first-principles/agents/references/examples/{personal-general-2,product-business-2,software-systems-2}.md`
  — regenerated twins via `python3 scripts/sync-content.py --write`
- `docs/conformance-baseline.md` / `docs/data/conformance.json` — regenerated
  after every task's edit

## Decisions Made

- **Prose-joined chain-head finding, found during Task 1.** After stripping the
  trailing-period from Chain 3's hop 1 in `personal-general-2.md`, the chain
  still scored malformed. Tracing `_chain_block_well_formed`'s per-line
  candidacy loop directly showed the cause: the head line
  `GT-5 (...) + the diagnostic-flagged drawdown-tolerance assumption (...) +
  the convention-challenged expected-utility assumption (...)` cannot match
  `_CHAIN_FORM_LINE_RE` at any starting position, because the grammar requires
  every "+"-joined item to itself be a `GT-N`/`Cn` token — a prose description
  breaks the alternation regardless of how many arrows follow. Fixed by folding
  the two non-GT clauses into GT-5's own single parenthetical, joined
  internally with semicolons — identical propositional content, pure
  reformatting (D-02: no new ground truth or inference authored). This is a
  fifth detector-reach landmine, distinct from the four the phase's earlier
  plans found (nested parentheticals, per-physical-line citation, R10
  over-rejection, citation-placement).
- Reused plan 18-04's R10 disclosed-bound fix (strip terminal punctuation from
  every non-final hop) directly on `personal-general-2.md`'s three
  already-single-line chains and on `software-systems-2.md`'s three chains
  after de-wrapping, without re-discovering it by trial.
- `product-business-2.md` needed only de-wrapping — none of its three chains'
  non-final hops carried trailing sentence-terminal punctuation — confirming
  the R10 landmine is per-chain rather than universal to every multi-hop
  chain in the corpus.
- Chose to CITE every resolvable claim rather than marking any of them, even
  in `product-business-2.md` where the plan flagged the highest risk of a
  forced cut (3 of 4 claims open with a prescribed lead-in). All four claims
  trace cleanly to Chain 1 and/or Chain 3, so no cut was needed.
- Every citation was placed on the exact first physical line the extractor
  reads for that claim — the bold lead-in's own line for a `**Label:**`
  claim, the list marker's own line for a numbered/bulleted claim — per the
  per-physical-line finding plans 18-02/18-03/18-04 documented.

## Deviations from Plan

None — plan executed exactly as written. The prose-joined chain-head finding
described above was a file-side repair discovered while iterating toward the
acceptance criteria (the same class of detector-reach landmine the plan's own
`<frozen_detector_non_goal>` anticipated — "if the example resists conformance,
the example changes"), not a deviation from the plan's tasks or scope.

## Issues Encountered

- Diagnosing `personal-general-2.md`'s Chain 3 required stepping outside
  `report-conformance.py`'s `detect_defects` wrapper and reading
  `_CHAIN_FORM_LINE_RE` / `_CHAIN_HEAD_TOKEN` / `_chain_block_well_formed`
  directly to see exactly why a two-arrow, correctly-punctuated chain still
  failed to match — the wrapper only reports pass/fail per block, not which
  grammar clause a candidate fails on. This diagnostic technique (direct
  source read, no execution) surfaced the prose-joined-head cause; the
  detector was never modified.
- This worktree's `.git` HEAD was on an unrelated Phase-12-era commit
  (`d4da381`) at spawn time, several commits behind the expected base
  (`468ee98`, which already includes 18-01 through 18-04's merged work);
  corrected via `git reset --hard` to the expected base per the worktree
  branch-check protocol before any plan work began. Phase 18 planning
  artifacts (`18-05-PLAN.md`, `18-04-SUMMARY.md`, `18-01-SUMMARY.md`,
  `18-CONTEXT.md`, `18-RESEARCH.md`, `18-PATTERNS.md`, `PROJECT.md`,
  `STATE.md`, `config.json`) were copied in from the main repo checkout
  before reading, since `git worktree add` only checks out tracked files
  and `.planning/` is gitignored except for `NN-MM-SUMMARY.md` files.
- Same environment finding recorded in plans 18-01 through 18-04: `bash
  scripts/check-firewall-battery.sh` initially needed a pytest-capable
  interpreter for VAL-03; resolved by `uv sync`, which creates a local,
  gitignored `.venv`. No repo change.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Plan 18-06 (the remaining exemplar-conformance pass, `science-engineering.md`
  and `science-engineering-2.md`) should check proactively for the
  prose-joined chain-head shape found here (a "+"-joined chain head where any
  item after the first is not a bare `GT-N`/`Cn` token) alongside the
  already-documented nested-parenthetical, per-physical-line-citation, and
  R10 trailing-punctuation landmines.
- Plan 18-07's `_CLAIM_FLOORS` should read this plan's three entries —
  `personal-general-2` 7, `product-business-2` 4, `software-systems-2` 10 —
  alongside the entries plans 18-02, 18-03, and 18-04 already produced.
- No blockers. `scripts/check-quality-harness.py` remains untouched and all
  three sha256 CONTRACT-06 pins are intact (confirmed via `git diff --stat`
  against the plan's starting commit `468ee98`).

## Self-Check: PASSED

- FOUND: `shared/examples/personal-general-2.md`
- FOUND: `shared/examples/product-business-2.md`
- FOUND: `shared/examples/software-systems-2.md`
- FOUND: `first-principles/agents/references/examples/personal-general-2.md`
- FOUND: `first-principles/agents/references/examples/product-business-2.md`
- FOUND: `first-principles/agents/references/examples/software-systems-2.md`
- FOUND: `docs/conformance-baseline.md`
- FOUND: `docs/data/conformance.json`
- FOUND commit: `9905768` (Task 1)
- FOUND commit: `5b976d9` (Task 2)
- FOUND commit: `d3d1f75` (Task 3)

---
*Phase: 18-exemplar-conformance*
*Completed: 2026-09-05*
