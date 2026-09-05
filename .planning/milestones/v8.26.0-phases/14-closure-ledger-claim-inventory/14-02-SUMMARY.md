---
phase: 14-closure-ledger-claim-inventory
plan: 02
subsystem: contract-prose
tags: [output-template, skill-body, validation-rubric, claim-extraction, closure-ledger, caveat-rule]

# Dependency graph
requires:
  - phase: 14-closure-ledger-claim-inventory (plan 01)
    provides: "_slice_sections' section-6 boundary fix (D-02) and _closure_ledger_fragments' structural-row narrowing (D-03), which R11's and R4's wording describe"
provides:
  - "R11 (claim-extraction rule), amended R4 (D-01/D-03 disclosure clauses) and R12 (caveat rule) as byte-identical literals on output-template.md, SKILL-body.md and validation-rubric.md (R4 on its original two surfaces only)"
  - "nine worked-example blocks in output-template.md §6 pinning R11's three disclosed bounds and R12's marker, ready for plan 14-04 to wire into _RENDER_FIXTURE_SHAPE"
affects: [14-03, 14-04, 14-05, 15-scan]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Registered rule literal = single physical sentence, byte-contained (not full-line-identical) across surfaces — a surface-specific bold label prefix, or lead-in prose, may precede the same literal on different surfaces without breaking reconciliation (confirmed against the pre-existing R6 precedent, which already carries different prefixes on different surfaces)"

key-files:
  created: []
  modified:
    - shared/spine/references/output-template.md
    - shared/spine/SKILL-body.md
    - shared/spine/references/validation-rubric.md
    - first-principles/agents/first-principles.md
    - first-principles/agents/references/output-template.md
    - first-principles/agents/references/validation-rubric.md

key-decisions:
  - "R11's bound-2 illustration uses a portable, self-contained `**Label:** text` / `**Label: text**` contrast instead of the capture-derived `**Overall confidence: HIGH.**` example, so the same literal can be copied byte-for-byte onto SKILL-body.md and validation-rubric.md without colliding with Task 2's fixture needles"
  - "R11 and R12 land on SKILL-body.md as bare sentences with no bold label prefix, matching the pre-existing R4/R6 convention on that surface, rather than carrying the '**Claim inventory.**'/'**Caveats.**' label verbatim"
  - "Bounds 2 and 3 get discriminating PAIRS, not BAD/OK/LATE trios, because both are categorical (a colon-placement regex test, a length/punctuation floor) with no positional axis a third fixture could discriminate — only bound 1 (the whole-line uncited label) has that axis"

patterns-established:
  - "A bold-label lead-in and its rule sentence can share one physical line on the surface that renders worked examples (output-template.md), while the same sentence stands alone on surfaces that don't (SKILL-body.md, validation-rubric.md) — reconciliation is byte containment against file text, not full-line equality"

requirements-completed: [LEDGER-01, LEDGER-02, LEDGER-03]

# Metrics
duration: ~25min
completed: 2026-09-03
---

# Phase 14 Plan 02: Claim-Extraction Rule (R11), Amended Citation Rule (R4) and Caveat Rule (R12) Summary

**Wrote the §6→§4 closure ledger's claim-extraction rule (R11), the caveat rule (R12), and an amended citation rule (R4) onto all three canonical contract surfaces in byte-identical words, plus nine worked-example blocks pinning R11's three measured bounds and R12's marker — all verified by execution (firewall battery GREEN 23/23), not by reading.**

## Performance

- **Duration:** ~25 min
- **Tasks:** 3 completed (4 commits — one mid-plan fix)
- **Files modified:** 6 (3 canonical `shared/spine/**` surfaces + 3 regenerated `first-principles/` targets)

## Accomplishments

- `output-template.md` §6 now states, in this order: `**Claim inventory.**` (R11 — the positive extraction rule, the rule-level fenced-block/restatement/prose exclusions, and three measured bounds), the existing `**Citation form.**` block (R4, amended with the D-03 structural-row residual and the D-01 section-6-visibility bound) with its three original fenced examples and closing paragraph untouched, and `**Caveats.**` (R12 — the `no chain — flagged assumption only` marker, registered with fixed bytes, and the rule that a marked caveat still scores untraced).
- Nine worked-example blocks appended to §6: a BAD/OK/(citation-added) trio for bound 1 (the whole-line uncited section-intro label), a discriminating pair for bound 2 (colon-placement), a discriminating pair for bound 3 (the assertiveness floor), and a discriminating pair for R12's marker (untraced-with-marker vs. traced-by-citation). Each doc label and each discriminating substring occurs exactly once in the file, verified by direct count, not visual inspection.
- R11 and R12 (and the amended R4, on its original two surfaces) copied byte-for-byte onto `SKILL-body.md`'s `## Before presenting conclusions` block and `validation-rubric.md`'s Criterion 6 — as bare sentences with no bold-label prefix on those two surfaces, matching the pre-existing R4/R6 convention already shipped there. R4 was deliberately NOT added to `validation-rubric.md` (planner's declined D-06 extension).
- `python3 scripts/sync-content.py --write` / `--check` clean; cumulative diff since the plan's base commit touches exactly the six expected files, none under `first-principles/skills/`.
- `python3 scripts/check-agent.py`, `python3 scripts/check-links.py`, and `python3 scripts/check-quality-harness.py --self-test` all exit 0 (`render_contract` and `ledger_traceability` sub-checks both PASSED). `npx markdownlint-cli2 'first-principles/**/*.md'` reports 0 issues in 49 files.
- `bash scripts/check-firewall-battery.sh` reports **`FIREWALL: GREEN (23/23)`** (required `uv sync` to create a local `.venv` in this worktree first, since VAL-03's pytest-capable-interpreter prerequisite was unmet — a one-time environment setup, not a code change; same remedy plan 14-01 documented).

## Task Commits

Each task was committed atomically (one additional mid-plan fix commit between Task 1 and Task 2's verification):

1. **Task 1: Write R11, the amended R4 and R12 into output-template.md §6** - `bb4daf0` (feat)
2. **Fix: give R11's bound-2 illustration a self-contained example** - `e1cd0d9` (fix) — discovered while verifying Task 2, see Deviations
3. **Task 2: Render the nine worked-example blocks pinning R11's bounds and R12's marker** - `93a70cb` (feat)
4. **Task 3: Carry R11, amended R4 and R12 onto SKILL-body.md and validation-rubric.md, then regenerate** - `0b1b422` (feat)

_No TDD tasks in this plan._

## Files Created/Modified

- `shared/spine/references/output-template.md` - `**Claim inventory.**` (R11), amended `**Citation form.**` (R4), `**Caveats.**` (R12), and nine worked-example blocks in §6
- `shared/spine/SKILL-body.md` - R11, amended R4 and R12 as bare sentences inside `## Before presenting conclusions`
- `shared/spine/references/validation-rubric.md` - R11 and R12 (not R4) added after Criterion 6's band list, with a lead-in sentence
- `first-principles/agents/first-principles.md`, `first-principles/agents/references/output-template.md`, `first-principles/agents/references/validation-rubric.md` - regenerated via `sync-content.py --write`

## Decisions Made

- **R11's bound-2 illustration was rewritten mid-plan to be self-contained.** The plan's action text for Task 1 specified the exact contrast `**Overall confidence:** HIGH.` vs. `**Overall confidence: HIGH.**`; Task 2 independently specifies that same capture-derived string as fixture block 4/5's content. Embedding the literal example directly in R11 (rather than pointing at "the worked examples below," my first draft) would have duplicated the identical substring in a way that broke Task 2's own needle-uniqueness requirement (each discriminating substring must occur exactly once in the file) once R11 and blocks 4/5 both existed. Resolved by giving R11 a generic, portable `**Label:** text` / `**Label: text**` pair instead — matching the self-contained inline-example style R7/R9 already use elsewhere in the same file (e.g. "write `C2 (threshold)` in every position") rather than a cross-reference to specific worked examples that only resolve on one of the three surfaces this literal must also live on.
- **R11 and R12 land on SKILL-body.md and validation-rubric.md without their bold-label prefix.** Verified against the pre-existing, shipped convention: `SKILL-body.md`'s current R4 sentence already omits `**Citation form.**`, and R6's registered literal appears bare in `output-template.md`/`SKILL-body.md` but mid-sentence after a different prefix (`"Reasoning (D-03). "`) in `validation-rubric.md` — confirming the reconciliation mechanism is byte *containment* against file text, not full-line equality across surfaces. R11/R12 follow the same shape: the identical sentence, with each surface allowed its own (or no) lead-in.
- **Kept the whole-line-copy verify script from the plan text as an aspirational check, but ran a corrected version instead** — see Deviations below; both are shown to make the discrepancy auditable rather than silently swapping one for the other.
- Bound 2 and bound 3 take discriminating **pairs**, not BAD/OK/LATE trios, per CONTEXT.md's explicit clarification (D-07): both are categorical (a regex colon-placement test and a length/punctuation floor) with no positional axis a third fixture could discriminate — manufacturing a third would pin nothing real. Only bound 1 (the whole-line, uncited section-intro label) has a positional axis, so it alone gets a genuine trio (BAD / OK-same-line / OK-with-citation).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] R11's bound-2 clause referenced content that doesn't exist on two of its three surfaces, and collided with Task 2's own fixture needle**
- **Found during:** Task 2's verification (needle-uniqueness check)
- **Issue:** My first draft of R11's bound-2 clause read "...is not matched at all — the worked examples below give the minimal contrasting pair..." This has two problems: (a) "the worked examples below" only resolves inside `output-template.md` §6 — the identical literal also lands on `SKILL-body.md` and `validation-rubric.md` (Task 3), neither of which has worked examples following it; (b) an earlier draft embedded the literal capture-derived string `**Overall confidence: HIGH.**` directly in R11's prose, which is also Task 2 block 4/5's exact fixture content, so the file-wide count of the needle `"confidence: HIGH.**"` became 2 instead of 1, failing Task 2's own `assert t.count(n) == 1` check.
- **Fix:** Rewrote the clause to a generic, portable, self-contained example — `**Label:** text` / `**Label: text**` — matching the inline-example style R7/R9 already use in the same file, with no cross-reference to other content and no collision with any fixture's discriminating substring.
- **Files modified:** `shared/spine/references/output-template.md`
- **Verification:** Re-ran both Task 1's and Task 2's `<verify>` scripts after the fix; both pass. `grep -c` confirms `"confidence: HIGH.**"` and `"confidence:** HIGH —"` each occur exactly once file-wide (in blocks 4 and 5 respectively).
- **Commit:** `e1cd0d9`

**2. [Rule 1 - Bug] Task 3's provided `<verify>` script assumes whole-line equality across surfaces; the actual reconciliation mechanism (and the pre-existing R4/R6 convention) is byte containment, not full-line copy**
- **Found during:** Task 3, running the plan's own verify script
- **Issue:** The plan's Task 3 verify script extracts the *entire physical line* containing each rule's probe substring from `output-template.md` (which, for R4/R11/R12, includes a leading bold label like `**Citation form.**`) and asserts that whole line is byte-identical (as a substring) inside `SKILL-body.md` and `validation-rubric.md`. Running it as written: `AssertionError: R4 missing byte-identically from SKILL-body.md`. But the pre-existing, shipped convention (confirmed by reading `SKILL-body.md`'s current R4 sentence, and R6's registered literal, which appears bare in two files but mid-sentence after a *different* prefix in `validation-rubric.md`) is that only the bare rule sentence — not any surface-specific label — needs to be byte-contained. The `<interfaces>` section of this same plan states the mechanism explicitly: "`_render_rule_report` tests byte containment against the file text," not full-line equality.
- **Fix:** Wrote a corrected verification (see `## Self-Check` below and the plan's own acceptance criteria, all independently satisfied) that extracts each rule's bare sentence (stripping the surface-specific label from `output-template.md`'s copy) and checks byte containment in each target surface — matching the actual, already-shipped precedent rather than the plan script's stricter, non-precedented assumption. Did not alter any canonical prose to satisfy the flawed script; the content is correct and precedent-consistent as written.
- **Files modified:** none (verification-only; recorded here per the "Auto-fix" discipline since it affects how "done" was established for this task)
- **Verification:** Corrected script prints `surface parity OK`; independently confirmed via `grep -c` that each of R4/R11/R12's probe substrings occurs exactly once per file, on exactly the surfaces required by `_RENDER_SURFACE_REQUIRED_RULES`'s D-06 mapping (R4 absent from `validation-rubric.md`, all three absent from `reason-upward.md`).
- **Commit:** `0b1b422` (verification discrepancy; no separate fix commit needed since no source bytes changed)

## Registered-Literal Text (verbatim — plan 14-03 copies these exact bytes)

**R4 (amended)**, as it appears on `output-template.md` and `SKILL-body.md` (bare sentence, no bold-label prefix on either surface's registered-literal text; `output-template.md`'s copy carries a `**Citation form.**` label immediately before it):

> Every Conclusion-section claim either names the chain that established it inline — `(chain C1)` — or is discharged by a §6→§4 closure ledger row that quotes the claim and names its chain. A claim doing neither is cut, not softened. Ledger discharge requires the structural row form the closure-ledger example below shows — a list marker, then the quoted claim, then an arrow, then the chain id — and a prose sentence that merely quotes something and names a chain is not a ledger row. This is detected only when the row sits inside section 6: the ledger emitted as process output before the analysis is not visible to the check, and inline citation is therefore the mechanically checkable form.

**R11 (new)**, as it appears on all three surfaces (bare sentence; `output-template.md`'s copy carries a `**Claim inventory.**` label immediately before it):

> A Conclusion-section claim is a bold lead-in whose colon closes the bold span, or a numbered or bulleted list item, and the three lead-ins this template prescribes — `**Recommended approach:**`, `**Key insight:**`, `**Trade-offs acknowledged:**` — are always claims and each must cite a chain; nothing inside a fenced block is ever a claim whatever its shape, a near-paraphrase restatement or direct entailment of an already-cited claim earlier in the same section is not a second claim, and prose carrying neither a bold colon lead-in nor a list marker is not a claim at all. Three bounds are measured, not assumed: a bold lead-in whose colon-terminated span is the entire physical line and carries no citation of its own is a section-intro label, and the citation obligation then falls to the list items beneath it; a bold span whose closing `**` is not immediately preceded by the colon is not matched at all — write `**Label:** text` to match, not `**Label: text**`; and a list item counts only when it closes its own sentence or runs past forty characters. Enumerate by this rule, not by recollection — the rule is the contract and the extractor is a partial instrument for it.

**R12 (new)**, as it appears on all three surfaces (bare sentence; `output-template.md`'s copy carries a `**Caveats.**` label immediately before it):

> A caveat qualifying an existing Conclusion-section claim either names the chain it qualifies inline or carries the marker `no chain — flagged assumption only` (em dash, lower case, no trailing punctuation inside the marker), and a marked caveat still scores untraced: the marker discloses the gap, it does not discharge the claim, because it is honest labelling rather than a citation and the extractor is deliberately not taught to recognise it. A caveat doing neither is cut, not softened.

## Fixture Population (nine worked-example blocks, output-template.md §6, after `**Caveats.**`)

| # | Doc label | Bound/rule pinned | Shape |
|---|-----------|--------------------|-------|
| 1 | `**Not a claim — a bold lead-in alone on its line, carrying no citation:**` | Bound 1 (section-intro label), BAD member | trio |
| 2 | `**A claim — the same lead-in carrying its assertion on the same line:**` | Bound 1, OK member (same line) | trio |
| 3 | `**A claim — the lead-in alone on its line, but carrying its own citation:**` | Bound 1, OK member (own citation) | trio |
| 4 | `**Not matched at all — a bold span whose colon sits inside it:**` | Bound 2 (colon-termination), BAD | pair |
| 5 | `**A claim — the same statement with the colon closing the bold span:**` | Bound 2, OK | pair |
| 6 | `**Not a claim — a short list item with no sentence-ending punctuation:**` | Bound 3 (assertiveness floor), BAD | pair |
| 7 | `**A claim — a short list item closing its own sentence:**` | Bound 3, OK | pair |
| 8 | `**Conformant but still untraced — a caveat carrying the flagged-assumption marker:**` | R12 marker, still-untraced | pair |
| 9 | `**Conformant and traced — the same caveat citing the chain it qualifies:**` | R12 marker, discharged-by-citation | pair |

**Why bounds 2 and 3 get pairs, not trios (recorded per the plan's explicit instruction, so a verifier does not read it as a missing trio):** Bound 1 has a positional axis — the *same* violation (a whole-line, uncited bold lead-in) can sit in a position the check reaches or, in principle, be rewritten in two different ways that both fix it (same-line assertion, or citation added to the label itself), which is why it alone gets three members. Bounds 2 and 3 are purely categorical: bound 2 is a single regex test (does the bold span's closing `**` immediately follow a colon, yes/no); bound 3 is a single length/punctuation floor (over 40 chars, or ends in terminal punctuation, yes/no). Neither has a "detected here but not there" positional dimension for a third fixture to discriminate — manufacturing one would pin nothing real, which CONTEXT.md's D-07 clarification names explicitly as the vacuous-fixture defect to avoid.

## Assumption Drift (advisory)

- **Planned:** Task 3's verify script implies R4/R11/R12 should be copied as identical whole lines (including any bold label) across all three surfaces.
- **Actual:** Copied as bare sentences (label-free) on `SKILL-body.md`/`validation-rubric.md`, matching the pre-existing R4/R6 convention; `output-template.md` alone carries the bold label on the same physical line.
- **Why:** The reconciliation mechanism (`_render_rule_report`, per this plan's own `<interfaces>` section) tests byte containment against file text, not full-line equality — confirmed against R6's already-shipped literal, which carries a different prefix on `validation-rubric.md` than on `output-template.md`/`SKILL-body.md`. Following the plan script literally would have required inventing a new, unprecedented convention (duplicating output-template.md's bold labels onto the other two surfaces) that the actual detector does not require and that plan 14-03 (which owns the real `_RENDER_RULE_LITERALS` registration) is better positioned to confirm or correct once it registers R11/R12 for real.

## Issues Encountered

- Same as plan 14-01: this worktree had no pytest-capable interpreter, so `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 22/23 passed)` naming `[PREREQ] VAL-03`. Resolved via `uv sync` (creates `.venv`, ships pytest 9.1.1); battery then reported `FIREWALL: GREEN (23/23)`. `.venv` is gitignored and was not committed.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 14-03 (matrix rows / registration) can now copy the exact R4/R11/R12 bytes recorded above verbatim into `_RENDER_RULE_LITERALS`, recompute `expected_literal_digest`, and extend `_RENDER_SURFACE_REQUIRED_RULES` for the three D-06 surfaces.
- Plan 14-04 can wire the nine worked-example blocks (table above) into `_RENDER_FIXTURE_SHAPE` and score them via `_conclusion_claims`/`_claim_is_traced`/`_closure_ledger_fragments` (control (f)'s shape, per PATTERNS.md).
- `reason-upward.md` remains untouched and out of scope (D-06), confirmed by empty `git diff`.
- No blockers.

---
*Phase: 14-closure-ledger-claim-inventory*
*Completed: 2026-09-03*

## Self-Check: PASSED

- FOUND: shared/spine/references/output-template.md (R11/R4/R12 + nine worked-example blocks)
- FOUND: shared/spine/SKILL-body.md (R11/R4/R12)
- FOUND: shared/spine/references/validation-rubric.md (R11/R12, R4 absent as required)
- FOUND: first-principles/agents/first-principles.md (regenerated)
- FOUND: first-principles/agents/references/output-template.md (regenerated)
- FOUND: first-principles/agents/references/validation-rubric.md (regenerated)
- FOUND commit: bb4daf0 (Task 1)
- FOUND commit: e1cd0d9 (fix)
- FOUND commit: 93a70cb (Task 2)
- FOUND commit: 0b1b422 (Task 3)
- CONFIRMED: `python3 scripts/sync-content.py --check` exit 0
- CONFIRMED: `python3 scripts/check-agent.py` exit 0
- CONFIRMED: `python3 scripts/check-links.py` exit 0
- CONFIRMED: `python3 scripts/check-quality-harness.py --self-test` exit 0
- CONFIRMED: `npx markdownlint-cli2 'first-principles/**/*.md'` — 0 issues in 49 files
- CONFIRMED: `bash scripts/check-firewall-battery.sh` — FIREWALL: GREEN (23/23)
