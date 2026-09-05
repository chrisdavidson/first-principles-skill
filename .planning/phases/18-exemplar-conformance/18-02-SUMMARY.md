---
phase: 18-exemplar-conformance
plan: 02
subsystem: testing
tags: [markdown, conformance-measurement, quality-harness, worked-examples]

# Dependency graph
requires:
  - phase: 18-exemplar-conformance
    plan: 01
    provides: marked/silent untraced-claim columns on report-conformance.py, the published
      Disclosed-bounds section, and Cn-numbered chain headings across the ten
      section-readable shared/examples files (the 58-silent/0-marked starting point)
provides:
  - three of the four detector-unreadable drill files (composed-inversion-second-order.md,
    estimate-fermi.md, theoretical-limit-carnot.md) now resolve into six numbered sections
    under the unmodified _slice_sections, each carrying at least one well-formed
    C1-numbered chain and zero silently-untraced §6 claims
  - shared-examples SectionResolutionError count reduced from 4 to 1
    (decompose-irreducibility, owned by plan 18-03)
  - per-file conclusion_claims floors for plan 18-07's _CLAIM_FLOORS:
    composed-inversion-second-order 2, estimate-fermi 5, theoretical-limit-carnot 5
affects: [18-03, 18-07, 18-08]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Drill-preamble pattern (precedent: ishikawa-fishbone.md) applied to two
      single-technique drills: the existing Step-by-step drill stays unnumbered and above
      the body; a numbered six-section wrapper below it reuses the drill's own prose for
      Problem Essence, Ground Truths and Conclusion, and uses the honest-depth escape
      valve (`Nothing material here — [reason]`) for Assumptions Table and Abandoned
      Reasoning, whose content genuinely does not exist in a single-technique drill."
    - "Chain-head parenthetical must not nest parens: _CHAIN_FORM_LINE_RE's parenthetical
      group is `\\([^)\\n]*\\)` (no nested `)` tolerance), so a head clause like
      `GT-4 (... established in the five-whys (reduce-to-primitives) example)` truncates
      at the inner `)` and can score the block malformed. Fix: flatten the nested
      parenthetical to plain prose inside the outer one."
    - "The claim extractor reads one physical line at a time — a citation added on a later
      wrapped line of a multi-line paragraph is invisible to `_cites_chain`. Any
      `(chain Cn)` citation must land on the SAME physical line as the bold lead-in or
      list-item text `_conclusion_claims` actually extracts."
    - "Verdict cells with no separate Verification column compress the justification
      directly into the Verdict cell: `Challenge — unverified; requires <the treatment's
      own verification step>`, preserving the row's existing meaning rather than dropping
      information."

key-files:
  created: []
  modified:
    - shared/examples/composed-inversion-second-order.md
    - shared/examples/estimate-fermi.md
    - shared/examples/theoretical-limit-carnot.md
    - first-principles/agents/references/examples/composed-inversion-second-order.md
    - first-principles/agents/references/examples/estimate-fermi.md
    - first-principles/agents/references/examples/theoretical-limit-carnot.md
    - docs/conformance-baseline.md
    - docs/data/conformance.json

key-decisions:
  - "No derivation chain was authored in this plan. composed-inversion-second-order.md's
    chain is its pre-existing `### Conclusion:` block, renumbered to `### Conclusion C1:`
    verbatim. estimate-fermi.md's and theoretical-limit-carnot.md's chains are
    transcriptions of the chain-shaped content that sat inside an invisible fenced/indented
    block under each file's `## Phase 4 Handoff` heading — every number, factor and
    inference in the finished chain traces to that pre-existing block; nothing new was
    inferred."
  - "Zero claims were cut. All claims that existed after the heading/colon fixes
    (composed-inversion-second-order: 2, estimate-fermi: 5, theoretical-limit-carnot: 5)
    were retained and traced by inline `(chain C1)` citation — none needed the
    no-chain-marker route and none needed cutting."
  - "estimate-fermi.md and theoretical-limit-carnot.md's Assumptions Table and Abandoned
    Reasoning sections use the template's honest-depth escape valve
    (`Nothing material here — [reason]`) with a stated reason naming the drill's
    single-technique scope, per the plan's D-05-adjacent guidance in 18-CONTEXT and the
    task's own instruction. This is a recorded, intended consequence, not a shortcut: both
    files' `verdict_cells` reads 0, published as-is in the baseline rather than hidden."

patterns-established:
  - "Two of the three unreadable-drill fixes (estimate-fermi.md,
    theoretical-limit-carnot.md) now share one structural shape: unnumbered drill preamble
    -> numbered six-section wrapper reusing the drill's own prose, escape valve for the two
    sections with no genuine content in a single-technique drill. Any future single-
    technique drill exemplar should copy this shape rather than re-deriving it."

requirements-completed: [CONF-03, CONF-04, CONF-05]

# Metrics
duration: ~90min (estimated; explicit start timestamp not captured)
completed: 2026-09-05
---

# Phase 18 Plan 02: Exemplar Conformance — Three Drill-File Fixes Summary

**Numbered the six canonical sections into three of the four detector-unreadable drill files (composed-inversion-second-order.md, estimate-fermi.md, theoretical-limit-carnot.md), unfencing/transcribing each file's pre-existing chain into a C1-numbered form and citing every resulting §6 claim inline — zero chains authored, zero claims cut.**

## Performance

- **Duration:** ~90 min (estimated)
- **Completed:** 2026-09-05
- **Tasks:** 3 completed
- **Files modified:** 8 (3 shared examples, 3 generated twins, 2 conformance artifacts)

## Accomplishments

- `composed-inversion-second-order.md` now resolves into six numbered sections
  (`## 1.` … `## 6.`), its lone `### Conclusion:` chain heading is now `### Conclusion C1:`,
  all five non-conforming `unverified — flagged` Verdict cells now read
  `Challenge — unverified; requires <specific verification step>`, the
  `**Recommended approach.**` period-form lead-in (invisible to the claim extractor) is now
  `**Recommended approach:**`, and both resulting §6 claims cite `(chain C1)` inline.
- `estimate-fermi.md` and `theoretical-limit-carnot.md` both now wrap their existing
  single-technique drill (left unnumbered, above the body) in a numbered six-section body,
  reusing the drill's own target-quantity/GT prose for §1 and §3, transcribing each file's
  chain out of an invisible fenced/indented block into an unfenced, `### Conclusion C1:`
  heading with one physical line per hop, and using the honest-depth escape valve
  (`Nothing material here — [reason]`) for §2 and §5, whose content genuinely does not
  exist in a single-technique drill.
- shared-examples `SectionResolutionError` count: **4 → 1** (only
  `decompose-irreducibility` remains, owned by plan 18-03).
- All three files read `heading_malformed_blocks == 0`, `nonconforming_verdict_cells == 0`,
  and `silent_untraced_claims == 0` on both the `shared-examples` and `generated-twin`
  surfaces.
- `scripts/check-quality-harness.py` is byte-identical to its state at plan start (confirmed
  via `git diff --stat` against the plan's starting commit — no output, zero diff).
- `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (24/24)` after running
  `uv sync` to supply VAL-03's pytest prerequisite in this fresh worktree (gitignored,
  untracked, no repo change).

## Per-file `conclusion_claims` values (for plan 18-07's `_CLAIM_FLOORS`)

| File | `conclusion_claims` (both surfaces) | `untraced_claims` | Claims cut |
|---|---|---|---|
| `composed-inversion-second-order` | 2 | 0 | none |
| `estimate-fermi` | 5 | 0 | none |
| `theoretical-limit-carnot` | 5 | 0 | none |

No claim was cut by name in this plan — every claim present after the heading/colon repairs
was retained and traced by an inline `(chain C1)` citation.

## Task Commits

Each task was committed atomically:

1. **Task 1: composed-inversion-second-order.md — number the headings it already has** -
   `759a84e` (fix)
2. **Task 2: estimate-fermi.md — wrap the drill in six sections and unfence its chain** -
   `8df7920` (fix)
3. **Task 3: theoretical-limit-carnot.md — same treatment, same shape** - `11729c8` (fix)

**Plan metadata:** committed together with this SUMMARY.md (worktree mode; STATE.md/ROADMAP.md
updates deferred to the orchestrator).

## Files Created/Modified

- `shared/examples/composed-inversion-second-order.md` — six numbered canonical headings,
  `### Conclusion C1:` renumber, five Verdict-cell repairs, one colon fix, two inline chain
  citations
- `shared/examples/estimate-fermi.md` — numbered six-section wrapper added below the
  unchanged, unnumbered Estimate Drill; chain unfenced into `### Conclusion C1:`; escape
  valve in §2/§5; four §6 claims citing chain C1 on their first physical line
- `shared/examples/theoretical-limit-carnot.md` — same treatment as estimate-fermi.md;
  chain unfenced from its indented block into `### Conclusion C1:`; escape valve in §2/§5;
  four §6 claims citing chain C1
- `first-principles/agents/references/examples/{composed-inversion-second-order,estimate-fermi,theoretical-limit-carnot}.md`
  — regenerated twins via `python3 scripts/sync-content.py --write`
- `docs/conformance-baseline.md` / `docs/data/conformance.json` — regenerated after every
  task's edit

## Decisions Made

- The `_CHAIN_FORM_LINE_RE` parenthetical group does not tolerate a nested `)` inside a
  head clause's parenthetical — a head reading
  `GT-4 (... established in the five-whys (reduce-to-primitives) example)` truncated at the
  inner `)` and scored `theoretical-limit-carnot`'s chain malformed on first draft. Fixed by
  flattening the nested parenthetical to plain prose (`five-whys reduce-to-primitives
  example`, no inner parens) rather than escaping or restructuring further — this is a
  detector-reach finding, not a detector defect requiring the frozen-detector-non-goal
  escalation, since the fix is entirely on the file side.
- `_conclusion_claims` extracts claim text per PHYSICAL LINE, not per paragraph — a citation
  placed on a later wrapped line of a hard-wrapped bold-lead-in paragraph is invisible to
  `_cites_chain`. Every `(chain C1)` citation in this plan's edits was verified to land on
  the exact physical line the extractor reads, using an ad-hoc harness-import script
  (mirroring `report-conformance.py`'s own import pattern) run against each draft before
  committing, rather than inferred from reading the rendered markdown.
- estimate-fermi.md's and theoretical-limit-carnot.md's Ground Truths sections restate
  GT-4/5/6 already cited throughout each drill (in the target-quantity intro, Step 3
  sourcing notes, and the original fenced chain) in the canonical `- **GT-N** ... —
  source: ...` bullet form. This is judged a formatting transcription, not new-fact
  authorship, per the scope fence's form-vs-authorship line: no fact, number, or source
  attribution appears that was not already stated elsewhere in the same file.

## Deviations from Plan

None — plan executed exactly as written. The only in-flight correction was the nested-paren
chain-head fix recorded above, which is a file-side repair discovered while iterating toward
the acceptance criteria, not a deviation from the plan's tasks or scope fence.

## Issues Encountered

- `bash scripts/check-firewall-battery.sh` initially reported `BLOCKED` (not `RED`) because
  this worktree had no pytest-capable interpreter — VAL-03's third leg needs pytest.
  Resolved by running `uv sync`, which created a local, gitignored `.venv`. This is an
  environment prerequisite, not a plan defect, and required no code change (same finding
  plan 18-01 recorded for its own worktree).
- The chain-head nested-parenthetical malformation (theoretical-limit-carnot.md, described
  above) was caught by running the frozen detector against the draft before committing,
  not by reading the rendered markdown — the malformed reading would not have been visible
  by inspection alone.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Plan 18-03 should read its starting point as shared-examples `SectionResolutionError == 1`
  (`decompose-irreducibility` only) — the corrected figure this plan's Task 3 explicitly
  produces.
- Plan 18-07 should use this plan's per-file `conclusion_claims` readings — 2 / 5 / 5 for
  `composed-inversion-second-order` / `estimate-fermi` / `theoretical-limit-carnot` — as the
  `_CLAIM_FLOORS` entries for these three files, once `decompose-irreducibility` also
  resolves under plan 18-03 and can be added.
- No blockers. `scripts/check-quality-harness.py` remains untouched and all three sha256
  CONTRACT-06 pins are intact (confirmed via `git diff --stat` against the plan's starting
  commit `6989a48`).

## Self-Check: PASSED

- FOUND: `shared/examples/composed-inversion-second-order.md`
- FOUND: `shared/examples/estimate-fermi.md`
- FOUND: `shared/examples/theoretical-limit-carnot.md`
- FOUND: `first-principles/agents/references/examples/composed-inversion-second-order.md`
- FOUND: `first-principles/agents/references/examples/estimate-fermi.md`
- FOUND: `first-principles/agents/references/examples/theoretical-limit-carnot.md`
- FOUND: `docs/conformance-baseline.md`
- FOUND: `docs/data/conformance.json`
- FOUND commit: `759a84e` (Task 1)
- FOUND commit: `8df7920` (Task 2)
- FOUND commit: `11729c8` (Task 3)

---
*Phase: 18-exemplar-conformance*
*Completed: 2026-09-05*
