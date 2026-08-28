---
phase: 02-loop-closure
plan: 02
subsystem: agent-methodology
tags: [markdown-prompt-spec, sync-content, gate-harness]

# Dependency graph
requires:
  - phase: 02-loop-closure
    plan: 01
    provides: The canonical "at most one re-perception pass" bound in SKILL-body.md's Turn discipline section and the Phase-1 re-entry route paragraph, both of which this plan cross-references without restating
provides:
  - A mid-run AskUserQuestion re-open clause in input-contract.md, scoped to a Self-Audit Gate Absent verdict traced to a missing input and bounded by the Turn discipline rule
  - A T-02-02 mitigation: mid-run answers re-enter through Phase 2's challenge-and-classify discipline instead of landing unchallenged in the Ground Truths list
  - The rubric's third (pre-existing) unbounded re-entry edge closed: "revise the analysis and re-score from the beginning" replaced with a bounded remedy carrying the same L8 token as SKILL-body.md
  - A Criterion 1 Absent-band route pointer in validation-rubric.md, cross-referencing the Phase-1 re-frame route and the Input Contract's missing-input variant
  - Regenerated first-principles/agents/first-principles.md and first-principles/agents/references/validation-rubric.md carrying every added literal
affects: [02-03-harn-02-gate]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Hard-wrap line-boundary avoidance for pinned literals: reflowed input-contract.md's first paragraph to one sentence per line (rather than the ~85-char wrap the file previously used) so no multi-word pinned literal is split across a newline that a raw substring-match verify script would otherwise treat as a break"
    - "Single canonical bound cross-referenced from a second, on-demand file by carrying the identical token (not restating the rule), turning the shared token into a drift detector between the two files"

key-files:
  created: []
  modified:
    - shared/agent/input-contract.md
    - shared/spine/references/validation-rubric.md
    - first-principles/agents/first-principles.md
    - first-principles/agents/references/validation-rubric.md

key-decisions:
  - "Reflowed the entirety of input-contract.md's edited first paragraph (not just the new sentences) to one-sentence-per-line, because the pre-existing wrap already split pinned literal L6 (`does not confirm framing on every delegation`) across a line boundary before this plan touched the file — confirmed via `git show HEAD:shared/agent/input-contract.md`, so this is a pre-existing condition this plan's own verify script exposed, not a regression it introduced"
  - "Placed the Criterion 1 Absent-band route pointer as a new indented continuation line inside the existing bullet, single unbroken line, rather than wrapping it at the file's normal width, for the same hard-wrap-avoidance reason"
  - "Rubric Edit A drops the phrase 'from the beginning' entirely rather than keeping 're-score from the beginning' and appending a bound afterward, so the literal X2 string cannot survive as an accidental substring of the new sentence"

patterns-established:
  - "When a plan's verify script pins a multi-word literal by raw substring match, check the *unedited* surrounding paragraph for pre-existing hard-wraps before authoring the edit, not just the new sentences being added — confirmed here to recur beyond the one instance flagged in 02-01's summary"

requirements-completed: [LOOP-02, LOOP-03]

# Metrics
duration: ~15min
completed: 2026-08-28
---

# Phase 2 Plan 02: Input Contract and Rubric Re-entry Summary

**Widened the Input Contract so a Self-Audit Gate Absent verdict traced to a missing input can re-open `AskUserQuestion` mid-run (bounded, routed through Phase 2's challenge discipline), and closed the rubric's own pre-existing unbounded re-score instruction — the third of LOOP-03's five re-entry edges — while adding a Criterion 1 Absent-band pointer back to the Phase-1 route, all verified present in both regenerated emitted surfaces.**

## Performance

- **Duration:** ~15 min
- **Completed:** 2026-08-28
- **Tasks:** 3 (all `type="auto"`, no checkpoints)
- **Files modified:** 4 (`shared/agent/input-contract.md`, `shared/spine/references/validation-rubric.md`, `first-principles/agents/first-principles.md`, `first-principles/agents/references/validation-rubric.md`)

## Accomplishments

- Appended a clause to `input-contract.md`'s first paragraph stating clarification is available again — literal L5, `not only before the analysis starts` — when the Self-Audit Gate scores a criterion Absent and the cause traces to a genuinely missing input (not framing the agent could have done itself), applying the same essentiality test used at the start of a run.
- Named the bound by cross-reference (not restatement): the mid-run re-open fires at most once per analysis, per the rule stated in `SKILL-body.md`'s Turn discipline section.
- Stated the T-02-02 mitigation explicitly: a mid-run answer re-enters through Phase 2 and is challenged and classified like any other input — it does not become a ground truth by virtue of arriving mid-analysis.
- Confirmed the second (fallback) paragraph of `input-contract.md` — the `AskUserQuestion`-unavailable case — is unscoped and left it byte-identical; it already generalizes to the mid-run trigger without modification.
- Replaced `validation-rubric.md`'s unbounded `revise the analysis and re-score from the beginning` (X2) with a bounded remedy carrying literal L8, `at most one re-perception pass`, byte-identical to the token in `SKILL-body.md`, plus the unresolved-gap-with-confidence-caveat degradation path and a plain-prose pointer (literal L9, `Turn discipline`) to where the rule is stated in full.
- Appended a route pointer to Criterion 1's `**Absent**` band descriptor: the verdict routes back to Phase 1 to re-frame the Essence Statement, or to re-opening input under the Input Contract when the cause is a missing input, rather than an in-place output-section-1 rewrite.
- Regenerated both emitted surfaces via `sync-content.py --write` and proved every literal reaches them: the Input Contract literals in `first-principles/agents/first-principles.md` (verbatim prepend path) and the rubric literals in `first-principles/agents/references/validation-rubric.md` (verbatim sibling-copy path) — deliberately not cross-checking L8 against `first-principles.md`, since the rubric is never inlined into the body.

## Task Commits

Each task was committed atomically:

1. **Task 1: Widen the Input Contract to permit a mid-run AskUserQuestion re-open** - `e22b835` (feat)
2. **Task 2: Bound the rubric's re-score instruction and point Criterion 1's Absent band at the Phase-1 route** - `5f9ab52` (feat)
3. **Task 3: Regenerate and prove both edits reach their (two different) emitted surfaces** - `82cb4d7` (feat)

## Exact Final Wording of Added Sentences

Recorded verbatim for plan 02-03's gate, which asserts these literals by exact substring match.

**Task 1 (appended to `input-contract.md`'s first paragraph, after "...it does not silently best-effort past a missing frame."):**

> Clarification is available again — not only before the analysis starts — when the Self-Audit Gate scores a criterion Absent and the cause traces to an input that was never supplied, such as a missing problem statement or a constraint whose presence or absence would change the entire analysis, rather than to framing this agent could have done itself: the same essentiality test applies. This mid-run re-open fires at most once per analysis, under the re-entry bound stated in the methodology's Turn discipline section. An answer received this way re-enters through Phase 2 and is challenged and classified like any other input — it does not become a ground truth by virtue of arriving from the user mid-analysis.

**Task 2, Edit A (replaced `validation-rubric.md` line 29):**

> If either condition is not met, revise the analysis and re-score — bounded to **at most one re-perception pass** per analysis, per the rule stated in full under `SKILL.md`'s Turn discipline section. If the same criterion still fails after that single pass, present it as an unresolved gap with a stated confidence caveat instead of re-scoring again.

**Task 2, Edit B (appended to Criterion 1's `**Absent**` band descriptor):**

> This verdict routes back to Phase 1 to re-frame the Essence Statement — or, when the cause is an input that was never supplied, to re-opening input under the Input Contract — rather than an in-place rewrite of output section 1; the route is bounded by the same rule described under `SKILL.md`'s "Before presenting conclusions" section.

No pinned literal required rewording. All of L5, L6, L7, L8, L9 were placed verbatim as specified, and X2 (`revise the analysis and re-score from the beginning`) was fully removed from `shared/spine/references/validation-rubric.md` (confirmed absent from both the source and the emitted rubric sibling).

**Confirmation: `input-contract.md`'s second (fallback) paragraph is unscoped.** Read in full during Task 1's `<read_first>` step. It reads: *"When clarification is needed, this agent uses `AskUserQuestion` to ask precisely what is missing. If `AskUserQuestion` is unavailable at runtime, this agent states the missing information it needs at the top of its response before proceeding with a best-effort analysis."* Neither sentence says "at start" or otherwise scopes the fallback to the beginning of a run — it names only the trigger ("when clarification is needed") and the tool-unavailable fallback, both of which apply identically whether the trigger fires at the start or mid-run. It was therefore left byte-identical, per the plan's instruction, and this is why Task 1's `<action>` did not touch it.

## Files Created/Modified

- `shared/agent/input-contract.md` - Widened first paragraph (mid-run `AskUserQuestion` re-open clause); reflowed to one sentence per line to avoid a pre-existing hard-wrap that split pinned literal L6 across a line boundary
- `shared/spine/references/validation-rubric.md` - Bounded the re-score instruction (line 29) and added the Criterion 1 Absent-band route pointer
- `first-principles/agents/first-principles.md` - Regenerated via `sync-content.py --write`; carries the widened Input Contract verbatim
- `first-principles/agents/references/validation-rubric.md` - Regenerated via `sync-content.py --write`; carries the bounded rubric text verbatim

## Decisions Made

- Followed the plan's constraint to reference `SKILL.md`'s sections in plain backtick prose, never a Markdown link, inside `validation-rubric.md` — matching the file's own header-block precedent and avoiding the unanchored-link failure mode `generate_agent_spine_references()`'s verbatim-copy (no absolutisation pass) would otherwise produce.
- Discovered mid-task-1 that the *pre-existing* wrap of `input-contract.md`'s first paragraph already split pinned literal L6 (`does not confirm framing on every delegation`) across lines 19-20 of the unedited file (confirmed via `git show HEAD:shared/agent/input-contract.md`), which is exactly the pitfall named in `02-01-SUMMARY.md`'s "patterns-established" note but occurring in text this plan did not itself author. Rule 1 (auto-fix bug) applies: the task's own `<verify>` block requires the literal to survive, and a pre-existing wrap silently defeating that check on an untouched sentence is a defect in the source file relative to what the plan needs, not a scope change. Fixed by reflowing the entire edited paragraph to one sentence per line — a formatting change only, no wording altered in the pre-existing sentences.
- Rubric Edit A was worded to drop "from the beginning" rather than keep it and append a qualifier, so the literal X2 string cannot survive as an accidental substring of the replacement sentence — verified directly by the task's own `<verify>` assertion.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Reflowed `input-contract.md`'s edited paragraph to avoid a pre-existing hard-wrap that would silently break pinned literal L6**
- **Found during:** Task 1, first verify run (`AssertionError: L6 lost - widening reintroduced per-delegation confirmation`)
- **Issue:** The paragraph's original ~85-char-wide word-wrap already placed a newline between "every" and "delegation" (confirmed present on the pre-Phase-2 base commit, not introduced by this plan), so the raw-text substring check for `does not confirm framing on every delegation` failed even though the words themselves were unchanged.
- **Fix:** Reflowed the whole first paragraph (both the pre-existing sentences and the newly appended ones) to one sentence per line, eliminating all internal hard-wraps in that paragraph so no multi-word literal can be split by a line boundary.
- **Files modified:** `shared/agent/input-contract.md`
- **Commit:** `e22b835`

Otherwise: plan executed exactly as written — no other deviations.

## Issues Encountered

- Task 1's first verify attempt failed with `AssertionError: L6 lost - widening reintroduced per-delegation confirmation`, traced via `grep -n "confirm framing"` to a pre-existing line break between "every" and "delegation" that predates this plan (confirmed via `git show HEAD:...`). Resolved by reflowing the paragraph (see Deviations above); re-ran the verify script, which then passed. No other tasks were affected by this issue.

## Next Phase Readiness

- All three of this plan's `<verify>` blocks pass, plus the plan's full `<verification>` checklist (10 items): `sync-content.py --check` exits 0; `input-contract.md` contains L5/L6/L7 with its second paragraph unchanged and no Markdown link; `validation-rubric.md` contains L8/L9, not X2, no Markdown link, and its two numbered pass conditions unchanged; L8 is byte-identical between the rubric and `SKILL-body.md`; both emitted surfaces (`first-principles/agents/first-principles.md`, `first-principles/agents/references/validation-rubric.md`) carry the expected literals; `sync-content.py --self-test` (GATE-02-v8.5), `check-agent.py --self-test`, `check-agent.py --file first-principles/agents/first-principles.md`, `check-links.py` (VAL-03), and `check-quality-harness.py --self-test` (QUAL-01) all exit 0; `git diff --name-only` against the pre-plan base (`5d7f3bc`) lists exactly the four files this plan's frontmatter names and no others.
- `markdownlint-cli2` on the regenerated tree (49 files under `first-principles/`): 0 issues.
- Not re-run in this plan (per its own instruction, matching 02-01's precedent): `bash scripts/check-firewall-battery.sh` was not used as the acceptance signal, since it reports `FIREWALL: RED (16/17)` on an unmodified tree for the pre-existing, unrelated reason that bare `python3 -m pytest` cannot find pytest outside `.venv` (VAL-03's third sub-command only). Not independently re-confirmed here; carried forward from the plan's own stated baseline and from `02-01-SUMMARY.md`'s prior confirmation.
- Plan 02-03 (wave 3, HARN-02 gate) can build its literal-presence assertions directly against the exact wording quoted above under "Exact Final Wording of Added Sentences" — none of it needs rewording, and none of it is stranded in `shared/` only: every literal was proven present in both regenerated emitted surfaces as well.
- LOOP-02 and LOOP-03 are both now fully closed across all five re-entry edges named in `SKILL-body.md`'s Turn discipline paragraph (second-order→Phase 2 was already bounded pre-milestone; Fix/Repeat and the new Phase-1 route were bounded in `02-01`; the rubric's re-score instruction and the new mid-run `AskUserQuestion` re-open are bounded by this plan).

---
*Phase: 02-loop-closure*
*Completed: 2026-08-28*
