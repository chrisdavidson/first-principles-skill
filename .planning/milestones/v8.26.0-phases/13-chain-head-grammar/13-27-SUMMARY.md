---
phase: 13-chain-head-grammar
plan: 27
subsystem: testing
tags: [python, regex, self-test, gate-hardening, check-traceability, check-quality-harness]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar
    provides: round-6 verification findings (13-VERIFICATION-round6.md) and independent code review (13-REVIEW.md)
provides:
  - "_DEF_CONSTRUCT_PREFIX: a real, shared whitespace-vocabulary constant both TRACE-03 patterns are built from"
  - "Corrected control (y) attribution, an independently transcribed arm-4b ENTRY-SOURCE LOCK entry, discriminating R-VERDICT-EXPIRY/-BAD needles, and a full prose-count sweep in check-quality-harness.py"
  - "A verify-and-record pass over every residual this batch does not change, each in a named CLOSED-ALREADY / FIXED HERE / HANDED-TO-13-28 state with evidence"
affects: [13-28]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Shared regex vocabulary hoisted to one module constant so two independently-written patterns derive from it rather than merely resembling it"
    - "ENTRY-SOURCE LOCK entries carry an independent, hand-transcribed second copy of their expectation rather than reusing the local the registry itself was built from"

key-files:
  created: []
  modified:
    - scripts/check-traceability.py
    - scripts/check-quality-harness.py

key-decisions:
  - "TRACE-03's 'cannot disagree by construction' claim: made true by deriving both patterns from one _DEF_CONSTRUCT_PREFIX constant, rather than weakening the four published surfaces."
  - "Round-6 WR-01 (dispatcher body can absorb a between-construct top-level statement): disclosed in code, not code-widened — the boundary alternation was left unextended because covering arbitrary top-level statements would need its own (h1) coverage this plan does not add."
  - "WR-04 prose-count sweep: fixed every live-claim occurrence found by direct computation against the current 18-id / 13-chain-family state, while leaving citations of a specific past plan's historical delta (the CR-03 'nine entries to one' reproduction) untouched as historical narrative."

requirements-completed: [CHAINHEAD-04]

# Metrics
duration: 30min
completed: 2026-09-03
---

# Phase 13 Plan 27: Sweep code-level residual findings round 6 and 13-REVIEW.md left open Summary

**Derived TRACE-03's "by construction" claim from a real shared constant, closed four `13-REVIEW.md` code defects in `check-quality-harness.py`, and recorded a named, evidenced disposition for every residual this batch does not touch.**

## Performance

- **Duration:** ~30 min
- **Completed:** 2026-09-03T12:29:00Z
- **Tasks:** 3 (2 with commits, 1 verification-only)
- **Files modified:** 2

## Accomplishments

- `scripts/check-traceability.py`'s `_SELFTEST_DISPATCHER_PAT` and `_next_top_level_pat` now both derive from one module constant, `_DEF_CONSTRUCT_PREFIX`, closing CR-03 (`13-REVIEW.md`) — the "cannot disagree on whitespace by construction" claim published in `CLAUDE.md`'s and `docs/ARCHITECTURE.md`'s TRACE-03 rows is now true of the code, proven by a scratch-copy mutation that fails exactly the two multi-space `(h1)` boundary arms when the shared constant is narrowed.
- Round-6 WR-01 (a top-level statement between the dispatcher and the next construct is absorbed into the dispatcher's body slice) is now disclosed in both docstring locations, alongside the pre-existing "last construct" disclosure it is distinct from.
- Round-6 WR-03 (`_resolve_artifact`'s docstring allegedly stale against the widened prefix set) was independently re-verified: it is already correct, closed by plan 13-21, not 13-17 as the plan's read_first guessed.
- Four `13-REVIEW.md` code-level defects in `scripts/check-quality-harness.py` are fixed: control (y)'s comment no longer restates the retracted `any()`-over-candidates attribution (WR-01); the ENTRY-SOURCE LOCK's arm-4b entry now carries an independent, hand-transcribed second copy of all eighteen locked fixture ids instead of reusing the registry's own local (WR-03); `R-VERDICT-EXPIRY` / `R-VERDICT-EXPIRY-BAD` now carry discriminating needles instead of the shared, undiscriminating `("expires at",)` (IN-03); and every live-claim stale prose count found in a full-file sweep is corrected against the current post-13-26 state (WR-04).
- Every residual this batch does not change (round-6 WR-02, WR-04, WR-05, WR-06) is recorded in a named state with quoted evidence, so plan 13-28 does not have to re-derive any of them.

## Task Commits

1. **Task 1: Make TRACE-03's "by construction" claim true by actually deriving it** - `4584d74` (fix)
2. **Task 2: Correct the four residual defects in check-quality-harness.py** - `5b34744` (fix)
3. **Task 3: Verify-and-record the residuals this batch does not change** - no commit (verification-only; every residual in scope was already closed, unchanged, or advisory — see below)

**Plan metadata:** this SUMMARY's own commit (docs: complete plan)

## Files Created/Modified

- `scripts/check-traceability.py` — `_DEF_CONSTRUCT_PREFIX` module constant; both `_SELFTEST_DISPATCHER_PAT` and `_next_top_level_pat` built from it; docstring/comment updates naming the constant; a new disclosure for round-6 WR-01's between-construct absorption case.
- `scripts/check-quality-harness.py` — control (y)'s comment corrected; ENTRY-SOURCE LOCK's arm-4b entry given an independent 18-id transcription; `R-VERDICT-EXPIRY`/`-BAD` needles made discriminating in both `_RENDER_FIXTURE_SHAPE` and the registry-lock copy; eleven stale prose-count occurrences corrected across the file.

## Decisions Made

- **TRACE-03 "by construction" (CR-03):** chose to make the claim true (derive both patterns from `_DEF_CONSTRUCT_PREFIX`) rather than downgrade the four published surfaces, per the plan's stated preference and `13-REVIEW.md`'s own fix sketch. `_SELFTEST_DISPATCHER_PAT` is built as `r"^" + _DEF_CONSTRUCT_PREFIX + r"+(" + names + r")\("` (preserving the original `def\s+` semantics via string-concatenation of the `+` onto the constant's trailing `\s`), and `_next_top_level_pat` as `r"^(?:" + _DEF_CONSTRUCT_PREFIX + r"|class\s|@)"` (preserving `def\s`).
- **Round-6 WR-01 outcome — DISCLOSED, not code-widened.** Chosen because extending the boundary alternation to also terminate at an arbitrary top-level statement (assignment, bare expression, `if`/`for`/`try`) would need its own dedicated `(h1)` coverage this plan does not add, and the underlying case is latent (no such statement exists between either file's dispatcher and its neighboring construct today, verified by inspection). The new disclosure sentence, added at `_selftest_dispatch_problems`'s own DISCLOSED LIMITATION paragraph and mirrored at the `(h)` comment block:

  > "A third, distinct case (round-6 WR-01, `13-VERIFICATION-round6.md`): the boundary pattern terminates only at `def`/`async def`/`class`/`@` — a top-level statement (an assignment, a bare expression, an `if`/`for`/`try`) sitting BETWEEN the dispatcher and the next such construct is not itself a boundary and is absorbed into the dispatcher's body slice too, the same absorption WR-02 discloses for trailing-after-last code, here mid-file rather than end-of-file. Also latent (no such statement sits between either file's dispatcher and its neighboring construct today, verified by inspection) and deliberately left open rather than widening the boundary alternation to recognise arbitrary top-level statements, which would need its own dedicated (h1) coverage this plan does not add."

- **Round-6 WR-03 — CLOSED-ALREADY, not 13-17 as the plan guessed.** `_resolve_artifact`'s docstring (lines 2000-2005) already reads:

  > "`.py` anchor starting with `_selftest_` OR `_self_test_` → additionally must be CALLED from a top-level `self_test()` or `_run_self_test()` (either optionally `async def`) in the same file, not merely defined (CR-02 / criterion 5, widened at 13-11/13-15/13-17; see `_selftest_dispatch_problems` for the disclosed resolution boundaries)"

  `git show 9ee844d` (`fix(13-21): close WR-05/WR-02/WR-03 residuals authored by this phase`) is the commit that made this correction — its diff shows exactly the "OR `_self_test_`" / "or `_run_self_test()`" widening landing at that plan, not 13-17. No edit made; recorded here instead, per the plan's own instruction.

- **WR-04 prose-count sweep scope — every live-claim occurrence, not just the three `13-REVIEW.md` named.** `13-REVIEW.md` named three locations (originally 6701/7465/10081); after plan 13-26 shifted the file, a full-file grep for the six numeric words (`nine`, `ten`, `fourteen`, `fifteen`, `sixteen`, `eighteen`) found eleven live-claim occurrences needing correction (see the full listing below), not three — the extra ones had drifted independently of the three `13-REVIEW.md` sampled. One occurrence (`nine entries to one`, line ~6787, describing the ORIGINAL CR-03 discovery at plan 13-12 when the family really did have nine members) was left unchanged as a historically-scoped incident description, matching how this project's frozen documents preserve historical figures — distinguished from the `nine chain-family fixtures` claim two paragraphs later (originally REVIEW's own WR-04 line), which is a live characterization of what a corrupted doc row COULD currently claim and was corrected to `thirteen`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] WR-04's prose-count sweep found eight additional stale occurrences beyond the three `13-REVIEW.md` named**

- **Found during:** Task 2
- **Issue:** `13-REVIEW.md`'s WR-04 named three locations (`check-quality-harness.py:6701`, `7465`, `10081` in its pre-13-26 line numbering). A full-file grep for the six numeric words the plan's acceptance criteria requires (`nine`, `ten`, `fourteen`, `fifteen`, `sixteen`, `eighteen`) found eight further live-claim occurrences that had also drifted against the current 18-id / 13-chain-family state: `_render_chain_family_ids`'s docstring ("sixteenth" → "fourteenth"), `_render_contract_fixtures`'s docstring ("fifteen" → "eighteen"), the id-count comment in `_render_registry_lock_problems` ("fifteen rows" → "eighteen rows"), the mode-2 shape-guard comment ("five of the fifteen" → "five of the eighteen"), `_selftest_render_contract`'s opening docstring line ("fifteen measured verdicts" → "eighteen"), the CONSUMPTION FLOOR docstring paragraph (two occurrences of "fifteen-id set" → "eighteen-id set"), two "ten chain-family fixtures" docstring/comment occurrences → "thirteen", and one "these ten ids" comment → "these thirteen ids" (this last one was internally inconsistent with the very next docstring line, which already correctly said "thirteen" — the clearest direct evidence of drift).
- **Fix:** Corrected all eleven occurrences (the three `13-REVIEW.md` named plus the eight additional ones found) against directly-computed live values (`render_locked_fixture_ids` has 18 members; its `R-CHAIN-*`/`R-HEAD-*` subset has 13), verified with a standalone script before editing.
- **Files modified:** scripts/check-quality-harness.py
- **Verification:** `python3 scripts/check-quality-harness.py --self-test` exits 0 after every edit; `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (23/23)`.
- **Committed in:** `5b34744` (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 — widened the WR-04 sweep beyond the three cited locations to satisfy the plan's own acceptance criteria, which asks for every numeric word in the file to be listed and verified, not just the three sampled by the review)
**Impact on plan:** Necessary for correctness — the acceptance criteria explicitly requires "No prose count in `scripts/check-quality-harness.py` disagrees with the live value it describes," which a three-location fix could not satisfy given the additional drift found. No scope creep beyond the file this task already had open.

## Numeric-word audit (Task 2 acceptance criterion)

Every occurrence of `nine`, `ten`, `fourteen`, `fifteen`, `sixteen`, `eighteen` in `scripts/check-quality-harness.py`, its live meaning, and its disposition:

| Line (post-fix) | Word | Meaning | Disposition |
|---|---|---|---|
| 76, 4770, 4772, 5028, 5103, 13296, 13301, 14436, 15053, 15248 | ten | defect-incidence TSV column count (unrelated concept — provenance/TSV schema, not fixture counts) | unchanged — not in scope, different subject |
| 4533, 13113 | ten | claims-mining reproduction counts (ledger rows mined as extra claims) | unchanged — not in scope, different subject |
| 4704 | ten | ledger rows counted as claims (same claims-mining subject) | unchanged — not in scope |
| 4778, 13255, 13284, 13350 | nine | provenance-columns count (unrelated concept) | unchanged — not in scope |
| 5117, 5420 | nine | defect-record numeric-field count (unrelated concept) | unchanged — not in scope |
| 6760 | sixteenth | `_render_chain_family_ids`'s docstring: ordinal of the next `R-CHAIN-*`/`R-HEAD-*` fixture if one were added | **fixed → fourteenth** (13 current members + 1) |
| 6787 | nine | `_render_coverage_floor_problems`'s docstring: the ORIGINAL CR-03 reproduction at plan 13-12, when arm 4a's table really did have nine entries | **unchanged — historical incident description**, not a live claim |
| 7157 | eighteen (was fifteen) | `_render_contract_fixtures`'s docstring: total fixtures read from `_RENDER_CONTRACT_EXTRACTION_TABLE` | **fixed → eighteen** (table has 18 rows, confirmed by direct count) |
| 7644-7645 | thirteen (was nine, twice) | doc-row token rationale: what a corrupted row could claim about the chain-family count | **fixed → thirteen** (13-REVIEW.md's own WR-04 finding) |
| 7781 | nineteen / eighteen | `_RenderRegistrySnapshot`'s own field count — a DIFFERENT registry (module-level rendering-contract registries, not worked-example fixtures); self-verifying via control (h2)'s anti-masking floor | unchanged — correct, unrelated concept |
| 7937 | eighteen (was fifteen) | extraction-table row-count comment (WR-03, `11-REVIEW-gap-closure.md` context) | **fixed → eighteen** |
| 8091 | eighteen (was fifteen) | mode-2 shape-guard comment: "five of the eighteen fixtures" | **fixed → eighteen** |
| 9758 | eighteen (was fifteen) | `_selftest_render_contract`'s docstring: "Controls (a)-(b) pin the eighteen measured verdicts" | **fixed → eighteen** |
| 9796 | eighteen (was fifteen) | CONSUMPTION FLOOR docstring: "a locked eighteen-id set written inline" | **fixed → eighteen** |
| 9823 | thirteen (was ten) | fifth-arm docstring: "re-scores the thirteen chain-family fixtures" | **fixed → thirteen** |
| 10402 | eighteen (was fifteen) | second CONSUMPTION FLOOR docstring occurrence: "The locked eighteen-id set below is written INLINE" | **fixed → eighteen** |
| 10441 | thirteen (was ten) | arm 4a comment: "re-scores the thirteen chain-family fixtures independently" | **fixed → thirteen** |
| 10444 | thirteen (was ten) | same paragraph: "can discharge those thirteen" | **fixed → thirteen** |
| 10498 | thirteen | CHAIN VERDICT FLOOR docstring: already said "thirteen" | unchanged — already correct |
| 10502 | thirteen (was ten) | same docstring, two lines later: "can discharge these thirteen ids" — was internally inconsistent with line 10498 above it | **fixed → thirteen** |
| 10527 | EIGHTEEN (was FOURTEEN) | EXPECTED-VERDICT FLOOR comment: "covers all EIGHTEEN locked ids" | **fixed → EIGHTEEN** |
| 10912 | eighteen (was fifteen) | ENTRY-SOURCE LOCK docstring: "arm 4b's recorded-verdict table (against all eighteen locked ids)" | **fixed → eighteen** |
| 11205 | fourteen | leg 5 DISCLOSED LIMITS: "not all fourteen `shared/examples/*.md` files" — the FILE count, must NOT move per the plan's own stated count-collision trap | unchanged — correct, deliberately unmoved |

## Residual disposition (Task 3 — every item ends in FIXED HERE, CLOSED-ALREADY, or HANDED TO 13-28)

### Round-6 findings

**Round-6 WR-01** — dispatcher body slice can absorb module-level code between the dispatcher and the next top-level construct.
**State: FIXED HERE (disclosed, not code-widened).** See Task 1 commit `4584d74`; new disclosure sentence quoted above under Decisions Made.

**Round-6 WR-02** — leg 5's failure message mislabels the `### Conclusion` heading as the chain "head".
**State: CLOSED-ALREADY**, by plan 13-21. Live evidence — `_render_example_conformance_problems`'s docstring (`scripts/check-quality-harness.py:7104-7115`):

> "WR-02 (`13-VERIFICATION-round5.md`): the malformed-block problem used to call `block_text.splitlines()[0]` "the head", but `block_text` always begins at the `### Conclusion` heading (`_render_example_chain_blocks` bounds the block starting at `heading.start()`), so that line is the heading, never the chain head [...] The heading is still reported (it is what locates the block) but is now named as a heading; the first line after it that matches `_CHAIN_HEAD_TOKEN_RE` is reported separately as the head candidate."

and the live message construction itself (`scripts/check-quality-harness.py:7136-7141`):

> `f"{relpath}:{line_number}: chain block scored malformed under the frozen detector — heading {heading_line[:60]!r}, head candidate {head_candidate[:60]!r}"`

Both correctly distinguish heading from head candidate. Round-6 itself recorded this residual as "Not independently re-derived (cosmetic message text)" — it was carried forward from round 5 without direct re-verification; direct verification now shows it was already fixed.

**Round-6 WR-03** — `_resolve_artifact`'s docstring stale against the widened prefix set.
**State: CLOSED-ALREADY**, by plan 13-21 (not 13-17 as the plan's read_first guessed). See Task 1 section above for the quoted docstring and the identifying commit (`9ee844d`).

**Round-6 WR-04** — the sha256 pin freezes `_chain_block_well_formed`'s ~120-line docstring too, so a doc-only fix inside it would need the milestone-amendment ceremony.
**State: CONFIRMED STANDING, unexercised.** No plan in this batch (13-22 through 13-27) touched `_chain_block_well_formed`. Evidence: `git diff 66e4cc4 HEAD -- scripts/check-quality-harness.py` (66e4cc4 = `docs(13-21): add plan summary`, the pre-batch commit) shows the first changed hunk at line 6521 — `_chain_block_well_formed` starts at line 4277 and is far outside every changed hunk. A direct line-range extraction (`sed -n '4277,4397p'`, 121 lines, matching `CLAUDE.md`'s documented size) diffed byte-for-byte identical between the pre-batch commit and the current tree (`diff` exit 0). The self-test's own `chain_detector_pin` sub-check, which asserts the live source's sha256 against the pinned `_CHAIN_DETECTOR_PINNED_DIGEST` (`sha256:d7d42d7a0bd781bd...`), reports PASSED on every run in this plan. The process constraint (a doc-only fix inside the docstring needs the milestone-amendment ceremony) remains standing and unexercised — no plan needed it this batch.

**Round-6 WR-05** — the 13-15/13-17 sentence in the TRACE-03 rows never restates what 13-15 itself closed.
**State: CLOSED-ALREADY**, by plan 13-21. Live sentence, byte-identical in `CLAUDE.md:163` and `docs/ARCHITECTURE.md:146` (confirmed by direct grep of both files):

> "13-15 (CR-02) closed a fourth, unguarded gap in the same body-slicing step, independent of these three: the body-boundary pattern did not recognise `async def`, so an `async def` construct following the dispatcher was absorbed into its body slice. 13-17 (WR-01) then derived the body-boundary pattern from the dispatcher pattern's own whitespace vocabulary, so a multi-space `async  def`, or a tab-separated `def` construct following the dispatcher is no longer absorbed into its body slice either."

This states 13-15's closure and 13-17's closure as two separate statements, exactly what round-6 WR-05 asked for. No edit made — 13-28 owns doc-row edits, and none was needed here.

**Round-6 WR-06** — zero of the fourteen shipped worked examples in `shared/examples/` use a `Cn`-as-head-input.
**State: HANDED TO 13-28 (advisory, deliberately not extended).** Confirmed unchanged: `shared/examples/*.md` still has exactly 14 files (`ls shared/examples/*.md | wc -l` = 14), and `git diff 66e4cc4 HEAD --stat -- shared/examples/` shows zero changes to that directory across the entire batch (13-22 through 13-27), so the count cannot have moved. `output-template.md`'s own `R-HEAD-ALLCHAIN` fixture (head: `C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold) + C4 (unconditional, zero code change) + C5 (~73% ceiling, no execution-model change)`, no `GT-N` identifier) still satisfies CHAINHEAD-06's literal requirement — confirmed scored `True` (well-formed) and passing in the live `render_contract` sub-check. Proposed wording for 13-28 to add to both `| QUAL-01 |` rows' DISCLOSED LIMITATIONS:

> "Separately, disclosed but not required: zero of the fourteen shipped worked examples in `shared/examples/` instantiate the `Cn`-as-head-input half of R7/R8 — `output-template.md`'s own `R-HEAD-ALLCHAIN` fixture does, which is what CHAINHEAD-06 literally requires; broadening `shared/examples/` to also exercise it is a deliberate, non-blocking extension, not a gap."

### `13-REVIEW.md` findings

**CR-03** — TRACE-03's "cannot disagree by construction" is a restated literal, not a derivation.
**State: FIXED HERE.** Task 1, commit `4584d74`. `_DEF_CONSTRUCT_PREFIX` module constant introduced; both `_SELFTEST_DISPATCHER_PAT` and `_next_top_level_pat` built from it. Verified by scratch-copy mutation: narrowing `_DEF_CONSTRUCT_PREFIX` to not match a two-space `async  def` fails exactly the two multi-space `(h1)` boundary arms (`multi-space async body-boundary case`, `multi-space dispatcher body-boundary case`), proving both patterns really consume the constant.

**WR-01** (`13-REVIEW.md`) — control (y)'s comment still carries the attribution 13-21 retracted in both doc rows.
**State: FIXED HERE.** Task 2, commit `5b34744`. Comment now states 13-21's measured attribution (the form check requires only two arrows in the truncated candidate) and cites the retraction directly instead of restating the retracted mechanism.

**WR-03** (`13-REVIEW.md`) — the ENTRY-SOURCE LOCK's "primary sources, never the local the registry was built from" is false for arm 4b.
**State: FIXED HERE.** Task 2, commit `5b34744`. Arm 4b's entry-source expectation is now an independent, hand-transcribed 18-id `frozenset` literal, matching the treatment the `(u)` entry already had. Verified by scratch-copy mutation: aliasing the registry entry's required side to the exact same object as its actual side (`render_x_arm4b_shared` bound once, used for both positions) now fails self-test with `(x) ENTRY-SOURCE LOCK: arm 4b recorded-verdict table: ALIASED — the required side is bound to the SAME OBJECT as the actual side, so this entry cannot report a coverage-floor problem`. (Note: the code's own vocabulary names this failure mode ALIASED, a sibling shape to WRONG SOURCE within the same `(x) ENTRY-SOURCE LOCK` check per `_render_entry_source_problems`'s docstring — both report through the same `"(x) ENTRY-SOURCE LOCK: {problem}"` failure path the plan's acceptance criteria describes.)

**WR-04** (`13-REVIEW.md`) — stale counts in three code comments.
**State: FIXED HERE**, and widened beyond the three named locations — see "Deviations from Plan" and the "Numeric-word audit" table above for the full accounting.

**IN-03** (`13-REVIEW.md`) — `R-VERDICT-EXPIRY` / `R-VERDICT-EXPIRY-BAD` share one undiscriminating needle.
**State: FIXED HERE.** Task 2, commit `5b34744`. Needles are now `"Accept — expires at"` (R-VERDICT-EXPIRY) and `"Current constraint (expires"` (R-VERDICT-EXPIRY-BAD), each verified unique by `grep -c` against the whole `output-template.md` (both return 1). Verified by scratch-copy mutation: swapping the two expiry blocks' bodies under each other's labels in `output-template.md` now fails self-test naming both ids (`R-VERDICT-EXPIRY: extracted text is missing required substring(s) ['Accept — expires at']` and `R-VERDICT-EXPIRY-BAD: extracted text is missing required substring(s) ['Current constraint (expires']`) — before this fix it was caught only by the opposed verdicts.

## Issues Encountered

None beyond the WR-04 scope widening documented above.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Both scripts pass `--self-test` individually and the full battery reports `FIREWALL: GREEN (23/23)`.
- Every residual named in this plan's must-haves is now in one of exactly three states (FIXED HERE, CLOSED-ALREADY, HANDED TO 13-28), each with recorded evidence — nothing is left silently open.
- `git diff --name-only` for this plan's two task commits shows only `scripts/check-traceability.py` and `scripts/check-quality-harness.py` — no `CLAUDE.md` or `docs/` file was touched, leaving all doc-row corrections for plan 13-28 to make exactly once against this plan's final code state.
- 13-28's proposed wording for round-6 WR-06 is provided verbatim above, ready to paste into both `| QUAL-01 |` rows.

---
*Phase: 13-chain-head-grammar*
*Completed: 2026-09-03*

## Self-Check: PASSED

- FOUND: `.planning/phases/13-chain-head-grammar/13-27-SUMMARY.md`
- FOUND: commit `4584d74` (Task 1)
- FOUND: commit `5b34744` (Task 2)
- `python3 scripts/check-traceability.py --self-test` exits 0 (verified this run)
- `python3 scripts/check-quality-harness.py --self-test` exits 0 (verified this run)
- `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (23/23)` (verified this run)
