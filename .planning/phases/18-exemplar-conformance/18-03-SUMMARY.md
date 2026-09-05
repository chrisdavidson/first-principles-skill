---
phase: 18-exemplar-conformance
plan: 03
subsystem: testing
tags: [markdown, conformance-measurement, quality-harness, worked-examples]

# Dependency graph
requires:
  - phase: 18-exemplar-conformance
    plan: 02
    provides: the drill-preamble wrapper pattern (ishikawa-fishbone.md precedent), the
      nested-parenthetical chain-head landmine finding, and the per-physical-line claim
      citation finding; shared-examples SectionResolutionError reduced from 4 to 1
      (decompose-irreducibility the sole remainder)
provides:
  - the last detector-unreadable drill file (decompose-irreducibility.md) now resolves
    into six numbered sections under the unmodified _slice_sections, carrying exactly one
    well-formed C1-numbered chain and zero silently-untraced §6 claims
  - shared-examples AND generated-twin SectionResolutionError count reduced to 0 —
    ROADMAP Phase 18 criterion 1 met corpus-wide
  - decompose-irreducibility's conclusion_claims floor for plan 18-07's _CLAIM_FLOORS: 7
affects: [18-07, 18-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Same drill-preamble shape as plan 18-02's estimate-fermi.md/theoretical-limit-carnot.md
      fixes: unnumbered drill preamble (including its own '## Summary of Drill Results'
      table) stays above and untouched; a numbered six-section wrapper below it reuses the
      drill's own prose for Problem Essence, Ground Truths (a straight lift of the GT-1..GT-8
      list including the GT-7?/GT-8? unverified markers) and the chain; escape valve for
      Assumptions Table and Abandoned Reasoning."
    - "Citation placement: '(chain C1)' must land on the FIRST physical line of a hard-wrapped
      bold-lead-in claim, not merely anywhere in the paragraph — placing the citation directly
      after the bold lead-in's colon (rather than at the end of a multi-line paragraph) keeps
      it on the extractor's first physical line even when the rest of the sentence wraps.
      Confirmed live: an earlier draft with '(chain C1)' at the tail of a three-line paragraph
      scored 5/7 claims untraced; moving the citation to the first line dropped untraced to 2
      (the two intentionally marked claims)."

key-files:
  created: []
  modified:
    - shared/examples/decompose-irreducibility.md
    - first-principles/agents/references/examples/decompose-irreducibility.md
    - docs/conformance-baseline.md
    - docs/data/conformance.json

key-decisions:
  - "No new analysis was authored. The one chain (### Conclusion C1) is a transcription of
    two passages the file already contained: the '#### Verdict on C1' computation
    (Round-trip = C1a x C1b x C1c ~= 0.97 x 0.99 x 0.40 ~= 38%, originally at lines ~119-121)
    and the '**Phase 3 consequence:**' paragraph (GT-3 refutes the 85% claim, originally at
    lines ~242-244). Every number and inference in the chain traces to those two passages;
    nothing was inferred or added."
  - "GT-1 through GT-8 were lifted verbatim into the new section 3, including the GT-7?/GT-8?
    unverified markers — neither unverified ground truth was silently promoted to verified
    during transcription (T-18-07 mitigation)."
  - "Zero claims were cut. All 7 conclusion_claims (3 prescribed lead-ins + 2 bullets + the
    Confidence line, matching the pattern QUAL-01/estimate-fermi.md already counts the
    Confidence line under) are either cited to chain C1 inline or carry the
    'no chain — flagged assumption only' marker. The two marked claims are the
    heat-in/heat-out clarification and the two-unverified-LCOS-inputs caveat — the two
    natural marker candidates the plan's <action> named."
  - "heading_chain_blocks == 1 on both surfaces, satisfying the plan's hard scope fence — no
    second chain was authored for C2 or C3, and no re-analysis of the decomposition was
    introduced."

patterns-established:
  - "All three of the four originally-unreadable drill files (composed-inversion-second-order,
    estimate-fermi, theoretical-limit-carnot from 18-02, plus decompose-irreducibility here)
    now share the identical drill-preamble -> numbered-six-section-wrapper shape. Any future
    single-technique drill exemplar should copy this shape."

requirements-completed: [CONF-03, CONF-04, CONF-05]

# Metrics
duration: ~40min (estimated; explicit start timestamp not captured)
completed: 2026-09-05
---

# Phase 18 Plan 03: Exemplar Conformance — decompose-irreducibility.md Section Resolution Summary

**Wrapped the last detector-unreadable drill file in six numbered sections, transcribing its own pre-existing Verdict-on-C1 computation and Phase 3 consequence paragraph into one C1-numbered chain — closing ROADMAP Phase 18 criterion 1 (SectionResolutionError: 1 -> 0) corpus-wide on both surfaces.**

## Performance

- **Duration:** ~40 min (estimated)
- **Completed:** 2026-09-05
- **Tasks:** 1 completed
- **Files modified:** 4 (1 shared example, 1 generated twin, 2 conformance artifacts)

## Accomplishments

- `decompose-irreducibility.md` now resolves into six numbered sections (`## 1.` … `## 6.`)
  under the unmodified `_slice_sections`, with the original `## Reduce-to-Primitives Drill`
  preamble (including its `## Summary of Drill Results` table) left untouched above the
  numbered body.
- Exactly one chain, `### Conclusion C1: The 85% round-trip electricity efficiency claim is
  refuted by the Carnot limit`, transcribed from the file's own prior prose (see Chain
  Provenance below). `heading_chain_blocks == 1` on both surfaces, satisfying the plan's hard
  scope fence.
- `heading_malformed_blocks == 0`, `nonconforming_verdict_cells == 0`, and
  `silent_untraced_claims == 0` on both `shared-examples` and `generated-twin` surfaces.
  `conclusion_claims == 7`, `untraced_claims == 2` (both carrying the caveat marker, per
  `marked_untraced_claims == 2`).
- **shared-examples `SectionResolutionError`: 1 -> 0. generated-twin `SectionResolutionError`:
  1 -> 0.** ROADMAP Phase 18 criterion 1 ("SectionResolutionError count is 0 over
  `shared-examples` AND `generated-twin`") is now met corpus-wide — all 14 shipped worked
  examples resolve into six sections on both surfaces.
- `scripts/check-quality-harness.py` is byte-identical to its state at the plan's starting
  commit `8dd1f2e` (confirmed via `git diff --stat` — no output, zero diff). All three
  CONTRACT-06 sha256 pins are intact.
- `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (24/24)` after running
  `uv sync` to supply VAL-03's pytest prerequisite in this fresh worktree (gitignored,
  untracked, no repo change).

## Chain Provenance (for the SUMMARY's required record)

The one chain in `### Conclusion C1` is a transcription, not new analysis, of two passages
the file already contained before this plan:

1. **The `#### Verdict on C1` computation** (originally lines ~119-121 of the pre-edit file):
   `Round-trip = C1a × C1b × C1c ≈ 0.97 × 0.99 × 0.40 ≈ 38%` — carried into the chain's first
   arrow-led hop verbatim.
2. **The `**Phase 3 consequence:**` paragraph** (originally lines ~242-244 of the pre-edit
   file): "GT-3 (Carnot / second-law anchor) immediately refutes the 85% round-trip
   electricity efficiency claim in C1" — carried into the chain's second arrow-led hop and
   the chain's heading text.

The chain's head inputs (GT-1, GT-2, GT-3) and their figures (~97%, ~99%, ~40%) are the same
three ground truths and figures the drill's own `#### Verdict on C1` section already computes
the product from — no new fact, number, or source attribution was introduced.

## `conclusion_claims` value (for plan 18-07's `_CLAIM_FLOORS`)

| File | `conclusion_claims` (both surfaces) | `untraced_claims` | `marked_untraced_claims` | `silent_untraced_claims` | Claims cut |
|---|---|---|---|---|---|
| `decompose-irreducibility` | 7 | 2 | 2 | 0 | none |

No claim was cut by name in this plan. All 7 claims (the three prescribed lead-ins, two
bullet items, and the closing `**Confidence:**` line) are either cited to chain C1 inline or
carry the `no chain — flagged assumption only` marker.

## Task Commits

Each task was committed atomically:

1. **Task 1: Wrap the drill in six numbered sections and transcribe the one chain** -
   `d8e1386` (fix)

**Plan metadata:** committed together with this SUMMARY.md (worktree mode; STATE.md/ROADMAP.md
updates deferred to the orchestrator).

## Files Created/Modified

- `shared/examples/decompose-irreducibility.md` — added a numbered six-section body below
  the unchanged, unnumbered drill preamble; §1 and §3 reuse the drill's own prose and its
  GT-1..GT-8 list verbatim (including the GT-7?/GT-8? unverified markers); §2 and §5 use the
  honest-depth escape valve; §4 carries the one transcribed `### Conclusion C1:` chain; §6
  states the drill's finding as 7 claims, each citing `(chain C1)` inline or carrying the
  caveat marker
- `first-principles/agents/references/examples/decompose-irreducibility.md` — regenerated
  twin via `python3 scripts/sync-content.py --write`
- `docs/conformance-baseline.md` / `docs/data/conformance.json` — regenerated after the edit

## Decisions Made

- **Citation placement fix, found during first draft.** The initial draft placed
  `(chain C1)` at the end of each hard-wrapped, multi-line bold-lead-in paragraph. Running
  the frozen detector against the draft (per the "verify by mutation, not by reading"
  discipline both prior plans establish) showed 5 of 7 claims scoring untraced — the
  extractor reads claim text per PHYSICAL LINE (18-02's documented finding), so a citation on
  a later wrapped line is invisible to it. Fixed by moving `(chain C1)` to land on the same
  physical line as the bold lead-in's colon in every case (`**Recommended approach:** Treat
  ... as refuted (chain C1) and ...`), which dropped untraced to 2 — exactly the two
  intentionally marked claims. This is a file-side fix, not a detector-reach finding
  requiring escalation, since 18-02 had already documented the general shape of the pitfall;
  this plan confirms it recurs and records the specific placement fix (citation directly
  after the colon, not at the paragraph's tail) that keeps a citation visible regardless of
  how the rest of the sentence wraps.
- The chain head's three parenthetical glosses (`GT-1 (Joule heating law anchors ... —
  physical law)`, etc.) were kept flat with no nested `(` or `)`, applying 18-02's documented
  `_CHAIN_FORM_LINE_RE` nested-parenthetical landmine finding proactively rather than
  discovering it by trial.
- GT-1, GT-2 and GT-3 (not GT-4/5/6, which belong to C2/C3) were selected as the chain's head
  inputs because they are exactly the three ground truths the drill's own Verdict-on-C1
  section already multiplies together; no other ground truth is load-bearing for the C1
  refutation.

## Deviations from Plan

None — plan executed exactly as written, within the single hard scope fence
(`heading_chain_blocks == 1`, no new analysis, no chain for C2 or C3). The citation-placement
correction described above was an in-flight fix discovered while iterating toward the
acceptance criteria, not a deviation from the plan's task or scope.

## Issues Encountered

- `bash scripts/check-firewall-battery.sh` initially reported `BLOCKED` (not `RED`) because
  this worktree had no pytest-capable interpreter — VAL-03's third leg needs pytest.
  Resolved by running `uv sync`, which created a local, gitignored `.venv`. Same finding
  plans 18-01 and 18-02 recorded for their own worktrees; no code change required.
- This worktree's `.git` HEAD was several commits behind the expected base commit at spawn
  time (`d4da381`, a Phase-12-era commit, vs. the expected `8dd1f2e`, which already includes
  18-01 and 18-02's merged work); corrected via `git reset --hard` to the expected base per
  the worktree branch-check protocol before any plan work began.
- Phase 18 planning artifacts (`18-03-PLAN.md`, `18-CONTEXT.md`, `18-RESEARCH.md`,
  `18-PATTERNS.md`, `PROJECT.md`, `STATE.md`, `config.json`) are gitignored `.planning/`
  content that had not been copied into this worktree by the spawn process; they were copied
  in from the main repo checkout before reading, since `git worktree add` only checks out
  tracked files. Same finding plans 18-01 and 18-02 recorded.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- **ROADMAP Phase 18 criterion 1 is fully closed**: `SectionResolutionError` is 0 over both
  `shared-examples` and `generated-twin`, corpus-wide. All 14 shipped worked examples resolve
  into six sections on both surfaces. No file remains for a future plan to fix under this
  criterion.
- Plan 18-07 should use this plan's `conclusion_claims` reading — **7** — as
  `decompose-irreducibility`'s `_CLAIM_FLOORS` entry, alongside the entries plan 18-02
  already produced for the other three previously-unreadable files (2 / 5 / 5 for
  composed-inversion-second-order / estimate-fermi / theoretical-limit-carnot).
- No blockers. `scripts/check-quality-harness.py` remains untouched and all three sha256
  CONTRACT-06 pins are intact (confirmed via `git diff --stat` against the plan's starting
  commit `8dd1f2e`).

## Self-Check: PASSED

- FOUND: `shared/examples/decompose-irreducibility.md`
- FOUND: `first-principles/agents/references/examples/decompose-irreducibility.md`
- FOUND: `docs/conformance-baseline.md`
- FOUND: `docs/data/conformance.json`
- FOUND commit: `d8e1386` (Task 1)

---
*Phase: 18-exemplar-conformance*
*Completed: 2026-09-05*
