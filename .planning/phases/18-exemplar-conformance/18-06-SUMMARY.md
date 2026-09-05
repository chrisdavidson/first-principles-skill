---
phase: 18-exemplar-conformance
plan: 06
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
    plan: 05
    provides: personal-general-2.md, product-business-2.md and software-systems-2.md at
      zero on all three remaining defect families, plus the fifth detector-reach finding
      (prose-joined "+"-chain heads) and the corpus-wide heading_malformed_blocks
      figure of 4 (science-engineering and science-engineering-2 only)
provides:
  - ishikawa-fishbone.md and product-business.md (already 0 malformed) now also read 0
    non-conforming verdict cells and 0 silently-untraced claims on both surfaces
  - science-engineering.md and science-engineering-2.md now read 0 malformed chain
    blocks, 0 non-conforming verdict cells and 0 silently-untraced claims on both surfaces
  - a sixth detector-reach finding: an arrow-led hop that itself starts with a GT
    identifier immediately after the arrow (`→ GT-1 (...) applied to ...`) can never be
    absorbed as a chain continuation — `_ARROW_LED_GT_RE` refuses it regardless of
    wording — fixed by moving the GT mention off the hop's first token (e.g. "→ Applying
    GT-1 (...) to ... yields ...")
  - ROADMAP criteria 2, 3, 4 (falsifiable zero) and 5 closed corpus-wide, both surfaces,
    all fourteen shipped examples
  - the marked-claim residual ratchet starting value (2, entirely in
    decompose-irreducibility.md, established by an earlier plan, unchanged by this one)
affects: [18-07, 18-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Arrow-led-GT hop landmine (sixth detector-reach finding, science-engineering.md
      Task 2): `_ARROW_LED_GT_RE` refuses ANY arrow-led continuation line that itself
      leads with a GT identifier immediately after the arrow — `→ GT-1 (...) applied to
      X: Y` is refused regardless of how well-formed the rest of the line is, because
      the detector treats a GT-led arrow line as the head of a NEW claim, not a
      continuation of the current one. This is distinct from the R9 disclosed bound
      (which describes a hop LEADING a fresh chain match, not a continuation refusal)
      but produces the same visible symptom — a chain that reads well-formed by eye
      scores malformed. Fix: reword the hop so the GT mention is not the first token
      after the arrow — \"GT-1 (5.5 PSH) applied to X: Y\" becomes \"Applying GT-1 (5.5
      PSH) to X yields Y\" — identical propositional content, pure connective
      restructuring, no new inference (D-02)."
    - "A hop's trailing punctuation only matters if the hop's LAST character (after
      markdown-closer stripping) is itself a sentence-terminal mark. A hop ending
      `...inefficiency.)` is NOT sentence-closed under `_segment_sentence_closed` — the
      final character is `)`, not `.`/`!`/`?` — so a parenthetical aside closing a
      non-final hop is safe from R10 even though the aside itself ends mid-parenthetical
      with a period. R10 only bites when the hop's very last character, unwrapped, is a
      bare terminal mark (`science-engineering-2.md`'s C1 hop 1 ending \"...would
      nucleate.\" and C2 hop 1 ending \"...causal chain.\" both needed the trailing
      period stripped; C1's hop 1 in the same file, ending \"...for battery
      inefficiency.)\", did not)."

key-files:
  created: []
  modified:
    - shared/examples/ishikawa-fishbone.md
    - shared/examples/product-business.md
    - shared/examples/science-engineering.md
    - shared/examples/science-engineering-2.md
    - first-principles/agents/references/examples/ishikawa-fishbone.md
    - first-principles/agents/references/examples/product-business.md
    - first-principles/agents/references/examples/science-engineering.md
    - first-principles/agents/references/examples/science-engineering-2.md
    - docs/conformance-baseline.md
    - docs/data/conformance.json

key-decisions:
  - "All resolvable §6 claims across the four files were CITED, not marked. Zero claims
    used the `no chain — flagged assumption only` marker and zero claims were cut; every
    one of the 13 claims (4 + 3 + 3 + 3) traces to at least one of its file's own chains
    via inline `(chain Cn)` / `(chains Cn and Cm)` citation. `marked_untraced_claims ==
    0` on all eight rows (shared-examples + generated-twin × 4 files) confirms this —
    including science-engineering.md and science-engineering-2.md, where the plan's
    <interfaces> section flagged the marker as ILLEGAL on all six of their claims (all
    open with a prescribed lead-in) — every one of those six was resolved by citation."
  - "ishikawa-fishbone.md's Confidence line (`**Confidence:** MEDIUM — Stage 1 is HIGH
    confidence (GT-1 through GT-4, all verified).`) IS extracted as a section-6 claim
    (the bold span's colon closes it, and the line ends in a period) and needed its own
    citation — the only one of this plan's four files where the closing Confidence line
    is a claim at all. product-business.md's, science-engineering.md's and
    science-engineering-2.md's Confidence lines either use the un-closed `**Confidence:
    MEDIUM**` form (colon inside the bold span — never matched, not a claim) or are too
    short (`**Confidence:** HIGH`, under the 40-character/no-terminal-punctuation
    assertiveness floor) — no citation needed."
  - "The sixth detector-reach finding (arrow-led-GT hop refusal) was found on
    science-engineering.md's Chain C1 hop 2 (`→ GT-1 (...) applied to ...`) and Chain C2
    hop 2 (`→ GT-3 (...): required ...`), then checked proactively on
    science-engineering-2.md's two chains before touching them — neither of that file's
    hops led with a GT identifier, so only the R10 trailing-punctuation fix was needed
    there, confirming (like plan 18-05's per-chain findings) that each detector-reach
    landmine is per-chain, not universal to every chain in the corpus."
  - "Verdict-cell compression (DEC-C) kept the Verification column's full existing prose
    unchanged in all 31 cells (8 + 7 + 8 + 8) across the four files; only the Verdict
    cell itself was rewritten to `<Token> — <justification>` with U+2014 EM DASH, and
    every justification is a compressed restatement of that same row's Verification
    text rather than new analysis."
  - "science-engineering-2.md's Assumption 8 (\"shaft-to-ground bonding ring...\") kept
    its original `Challenge` token even though its own Verification text confirms the
    degraded-conductance finding — DEC-C preserves the existing token unchanged
    regardless of whether the row reads, on its face, like a confirmed finding; no
    token was reclassified."
  - "ishikawa-fishbone.md's trailing `## Validation Rubric Verdict` appendix, sitting
    immediately after `## 6. Conclusion`, was left untouched and nothing was inserted
    between the two headings, per the plan's explicit T-18-10 mitigation instruction."

patterns-established:
  - "The arrow-led-GT hop landmine (this plan's sixth finding) should be checked
    proactively on any future chain de-wrap: if a hop's very first token after the arrow
    is a GT identifier, `_ARROW_LED_GT_RE` refuses the continuation regardless of the
    rest of the line's wording. Reword so the GT mention is not the hop's leading
    token."
  - "R10 (trailing sentence-terminal punctuation) only fires when a hop's raw last
    character is itself `.`/`!`/`?` — a hop ending in a closing parenthesis after an
    internal period (`...inefficiency.)`) is untouched by R10 and needs no fix. Check
    the literal last character before assuming a de-wrapped hop needs punctuation
    stripped."

requirements-completed: [CONF-04, CONF-05]

# Metrics
duration: ~75min (estimated; explicit start timestamp not captured)
completed: 2026-09-05
---

# Phase 18 Plan 06: Exemplar Conformance — Closing the Corpus Summary

**Closed the corpus: brought ishikawa-fishbone.md, product-business.md, science-engineering.md and science-engineering-2.md to zero on all three remaining defect families, discovering a sixth detector-reach landmine (an arrow-led hop that itself starts with a GT identifier is refused as a continuation regardless of wording), and drove ROADMAP criteria 2, 3, 4 and 5 to their falsifiable-zero targets across all fourteen shipped examples on both the shared-examples and generated-twin surfaces, with the corpus-wide marked-claim residual measured at 2 (unchanged, in decompose-irreducibility.md).**

## Performance

- **Duration:** ~75 min (estimated)
- **Completed:** 2026-09-05
- **Tasks:** 3 completed
- **Files modified:** 10 (4 shared examples, 4 generated twins, 2 conformance artifacts)

## Accomplishments

- `ishikawa-fishbone.md` and `product-business.md` (already 0 malformed, chains
  untouched): all 15 §2 Verdict cells (8 + 7) rewritten to `<Token> — <justification>`
  form with U+2014 EM DASH, Verification column kept intact; all 7 §6 claims (4 + 3)
  cited inline to their chain(s) — zero marked, zero cut.
- `science-engineering.md`: both chain blocks de-wrapped to one physical line per hop;
  found and fixed the sixth detector-reach landmine (an arrow-led hop starting `→ GT-1
  (...)` / `→ GT-3 (...)` is refused as a continuation, reworded to `→ Applying GT-N
  (...) ... yields ...`); all 8 Verdict cells conformed; all 3 §6 claims cited (all
  three are prescribed lead-ins, so the marker was illegal on every one — resolved by
  citation, none marked).
- `science-engineering-2.md`: both chain blocks de-wrapped to one physical line per hop
  with the trailing sentence-terminal period stripped from each chain's non-final hop
  (R10, reused directly from plans 18-04/18-05 without rediscovery); all 8 Verdict cells
  conformed; all 3 §6 claims cited (again all three prescribed lead-ins) — zero marked,
  zero cut.
- **Plan-scoped rollup, both surfaces, all four files:** `heading_malformed_blocks`,
  `nonconforming_verdict_cells`, and `silent_untraced_claims` each sum to exactly `0`
  across the eight rows (shared-examples + generated-twin × 4 files).
  `marked_untraced_claims` is `0` on every one of the eight rows, including the six
  claims where the marker was explicitly illegal.
- **Corpus-wide close (ROADMAP criteria 1-5):** across all fourteen shipped examples on
  BOTH the `shared-examples` and `generated-twin` surfaces, `section_resolution == "OK"`
  on every row, and `heading_malformed_blocks`, `nonconforming_verdict_cells`, and
  `silent_untraced_claims` each sum to exactly `0`. `pair_agreement.agreeing == 14` and
  `pair_agreement.total == 14`.
- The corpus-wide `marked_untraced_claims` sum (summed over the `shared-examples`
  surface) is **2**, entirely from `decompose-irreducibility.md` (established by an
  earlier phase-18 plan, not this one). This is the ratchet's starting value for plan
  18-07.
- `scripts/check-quality-harness.py` is byte-identical to its state at the plan's
  starting commit `f93835b` (`git diff --stat` — no output, zero diff). All three
  CONTRACT-06 sha256 pins are intact.
- `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (24/24)`.
- `git status --porcelain` is empty after the final commit.

## Per-file `conclusion_claims` values (for plan 18-07's `_CLAIM_FLOORS`)

| File | `conclusion_claims` (both surfaces) | `untraced_claims` | `marked_untraced_claims` | `silent_untraced_claims` | Claims cut |
|---|---|---|---|---|---|
| `ishikawa-fishbone` | 4 | 0 | 0 | 0 | none |
| `product-business` | 3 | 0 | 0 | 0 | none |
| `science-engineering` | 3 | 0 | 0 | 0 | none |
| `science-engineering-2` | 3 | 0 | 0 | 0 | none |

No claim was cut by name in this plan. All 13 claims (4 + 3 + 3 + 3) are cited to at
least one of their file's own chains.

## Corpus-wide marked-claim residual (ratchet starting value)

**2**, both instances in `decompose-irreducibility.md` (not a file this plan touched;
figure carried forward unchanged from an earlier plan's work). Plan 18-07 pins this as
the ratchet's starting value — it may fall but never rise.

## Task Commits

Each task was committed atomically:

1. **Task 1: ishikawa-fishbone.md and product-business.md — verdict cells and citations** - `f7be28b` (fix)
2. **Task 2: science-engineering.md — de-wrap two chains, verdict cells, citations** - `978105f` (fix)
3. **Task 3: science-engineering-2.md — de-wrap, verdict cells, citations, close the corpus** - `0eaa61e` (fix)

**Plan metadata:** committed together with this SUMMARY.md (worktree mode; STATE.md/ROADMAP.md
updates deferred to the orchestrator).

## Files Created/Modified

- `shared/examples/ishikawa-fishbone.md` — all 8 Verdict cells compressed to `<Token> —
  <justification>` form; all 4 §6 claims cited inline, including the Confidence line
- `shared/examples/product-business.md` — all 7 Verdict cells compressed; all 3 §6
  claims cited inline
- `shared/examples/science-engineering.md` — 2 chain blocks de-wrapped to one physical
  line per hop with the arrow-led-GT landmine fixed on each chain's second hop; all 8
  Verdict cells compressed; all 3 §6 claims cited inline
- `shared/examples/science-engineering-2.md` — 2 chain blocks de-wrapped to one physical
  line per hop with terminal punctuation stripped from each non-final hop; all 8 Verdict
  cells compressed; all 3 §6 claims cited inline
- `first-principles/agents/references/examples/{ishikawa-fishbone,product-business,science-engineering,science-engineering-2}.md`
  — regenerated twins via `python3 scripts/sync-content.py --write`
- `docs/conformance-baseline.md` / `docs/data/conformance.json` — regenerated after every
  task's edit

## Decisions Made

- **Arrow-led-GT hop landmine, found during Task 2.** After de-wrapping
  science-engineering.md's Chain C1 onto one physical line per hop, the chain still
  scored malformed. Direct inspection of `_chain_block_well_formed`'s absorption loop
  showed the cause: hop 2 (`→ GT-1 (5.5 PSH annual average) applied to 1,875 Wh/day:
  panel capacity = ... ≈ 341 W`) is an arrow-led line that itself leads with a GT
  identifier immediately after the arrow, which `_ARROW_LED_GT_RE` refuses as a
  continuation unconditionally — the detector treats it as the head of a new claim
  rather than a wrap of the current one, regardless of the fact that the sentence reads
  perfectly well as a continuation. Fixed by rewording to move the GT mention off the
  hop's leading token: `→ Applying GT-1 (5.5 PSH annual average) to 1,875 Wh/day yields
  panel capacity = ... ≈ 341 W`. Same fix applied to Chain C2's hop 2 (`GT-3` → `Applying
  GT-3 (...) yields ...`). This is a sixth detector-reach landmine, distinct from the
  five the phase's earlier plans found. Checked proactively on
  science-engineering-2.md's two chains before editing them; neither hop in that file
  led with a GT identifier, so this fix was not needed there.
- Reused plan 18-04/18-05's R10 disclosed-bound fix (strip trailing sentence-terminal
  punctuation from every non-final hop) on science-engineering-2.md's two chains,
  discovering along the way that a hop ending in a closing parenthesis after an internal
  period (`...battery inefficiency.)`) is NOT sentence-closed under
  `_segment_sentence_closed` — only a hop whose raw final character is itself
  `.`/`!`/`?` triggers R10. science-engineering.md's Chain C1 hop 1 has exactly this
  parenthetical-closing shape and needed no punctuation fix; science-engineering-2.md's
  two non-final hops both ended in a bare period and did.
- Chose to CITE every resolvable claim rather than marking any of them. All 13 claims
  across the four files (including all six of science-engineering.md's and
  science-engineering-2.md's prescribed-lead-in claims, where the marker was explicitly
  illegal per the plan's `<interfaces>` section) trace cleanly to at least one of their
  file's own chains — no cut was needed anywhere in this plan.
- Every citation was placed on the exact first physical line the extractor reads for
  that claim — the bold lead-in's own line for a `**Label:**` claim — per the
  per-physical-line finding plans 18-02 through 18-05 documented. ishikawa-fishbone.md's
  Confidence line required this treatment too, since (unlike the other three files in
  this plan) its Confidence line closes its bold span with a colon and ends in a period,
  making it an extracted claim.
- Left `ishikawa-fishbone.md`'s trailing `## Validation Rubric Verdict` appendix
  untouched and added nothing between `## 6. Conclusion` and it, per the plan's T-18-10
  mitigation — `selfaudit_disagreements == 2` on that file is a pre-existing, out-of-scope
  reading and was not touched.

## Deviations from Plan

None — plan executed exactly as written. The arrow-led-GT hop finding described above
was a file-side repair discovered while iterating toward the acceptance criteria (the
same class of detector-reach landmine the plan's own `<frozen_detector_non_goal>`
anticipated — "if the example resists conformance, the example changes"), not a
deviation from the plan's tasks or scope.

## Issues Encountered

- Diagnosing science-engineering.md's Chain C1 and C2 malformed readings required
  stepping outside `report-conformance.py`'s `detect_defects` wrapper and reading
  `_ARROW_LED_GT_RE`, `_chain_block_well_formed`'s absorption loop, and
  `_segment_sentence_closed` directly against the draft file to see exactly which
  continuation-refusal rule was firing — the wrapper only reports pass/fail per block,
  not which rule refused which line. This diagnostic technique (direct source read, no
  execution) surfaced the arrow-led-GT cause; the detector was never modified.
- Same environment finding recorded in every prior plan in this phase: `bash
  scripts/check-firewall-battery.sh` initially needed a pytest-capable interpreter for
  VAL-03; resolved by `uv sync`, which creates a local, gitignored `.venv`. No repo
  change.
- This worktree's `.git` HEAD was on an unrelated Phase-12-era commit (`d4da381`) at
  spawn time, behind the expected base (`f93835b`, which already includes 18-01 through
  18-05's merged work); corrected via `git reset --hard` to the expected base per the
  worktree branch-check protocol before any plan work began. Phase 18 planning artifacts
  (`18-06-PLAN.md`, `18-CONTEXT.md`, `18-RESEARCH.md`, `18-PATTERNS.md`, `PROJECT.md`,
  `STATE.md`, `config.json`) were copied in from the main repo checkout before reading,
  since `git worktree add` only checks out tracked files and `.planning/` is gitignored
  except for `NN-MM-SUMMARY.md` files.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- The corpus is closed: all fourteen shipped examples read zero on unreadable, malformed
  chain blocks, non-conforming verdict cells, and silently-untraced claims, on both the
  source and emitted-byte surfaces, with 14/14 pair agreement. ROADMAP criteria 1-5 are
  all met.
- Plan 18-07's `_CLAIM_FLOORS` should read this plan's four entries —
  `ishikawa-fishbone` 4, `product-business` 3, `science-engineering` 3,
  `science-engineering-2` 3 — alongside the entries plans 18-02 through 18-05 already
  produced, and should pin the corpus-wide `marked_untraced_claims` ratchet at its
  measured starting value of **2** (entirely in `decompose-irreducibility.md`).
- Future de-wrap work anywhere in the corpus should check proactively for the sixth
  detector-reach landmine (an arrow-led hop starting with a bare GT identifier is
  refused as a continuation) alongside the five already-documented landmines (nested
  parentheticals, per-physical-line citation, R10 over-rejection, citation-placement,
  prose-joined "+"-chain heads).
- No blockers. `scripts/check-quality-harness.py` remains untouched and all three
  sha256 CONTRACT-06 pins are intact (confirmed via `git diff --stat` against the
  plan's starting commit `f93835b`).

## Self-Check: PASSED

- FOUND: `shared/examples/ishikawa-fishbone.md`
- FOUND: `shared/examples/product-business.md`
- FOUND: `shared/examples/science-engineering.md`
- FOUND: `shared/examples/science-engineering-2.md`
- FOUND: `first-principles/agents/references/examples/ishikawa-fishbone.md`
- FOUND: `first-principles/agents/references/examples/product-business.md`
- FOUND: `first-principles/agents/references/examples/science-engineering.md`
- FOUND: `first-principles/agents/references/examples/science-engineering-2.md`
- FOUND: `docs/conformance-baseline.md`
- FOUND: `docs/data/conformance.json`
- FOUND commit: `f7be28b` (Task 1)
- FOUND commit: `978105f` (Task 2)
- FOUND commit: `0eaa61e` (Task 3)

---
*Phase: 18-exemplar-conformance*
*Completed: 2026-09-05*
