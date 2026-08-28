---
phase: 02-loop-closure
plan: 01
subsystem: agent-methodology
tags: [markdown-prompt-spec, sync-content, gate-harness]

# Dependency graph
requires:
  - phase: 01-evidence-acquisition
    provides: The Phase 3 verification step and rewritten Exit-criterion line (Act limb) that this plan's Task 3 edit builds on without colliding
provides:
  - A canonical, single-location bound ("at most one re-perception pass") naming all five re-entry edges in the agent body's Turn discipline section
  - A re-entry disclosure rule (name which edge fired, what triggered it, what changed) extending the existing regenerate-the-analysis revision-tracking sentence
  - A bounded Fix/Repeat loop (Repeat item no longer instructs an unbounded re-score)
  - A new Criterion-1-Absent -> Phase 1 re-entry route, plus a pointer to the AskUserQuestion route for missing-input cases
  - A Phase 3 exit-criterion exception clause naming the bounded re-entry edges without weakening the original completeness claim
  - Regenerated first-principles/agents/first-principles.md carrying every added literal
affects: [02-02-input-contract-and-rubric-reentry, 02-03-harn-02-gate]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Site-of-trigger feedback-edge idiom (state trigger, then destination, in one sentence at the mechanism that produces the trigger) reused for the new Phase-1 route, matching the existing second-order->Phase 2 sentence"
    - "Single canonical bound statement cross-referenced from each specific edge, rather than the bound restated at every site"

key-files:
  created: []
  modified:
    - shared/spine/SKILL-body.md
    - first-principles/agents/first-principles.md

key-decisions:
  - "Placed the canonical re-entry bound inside the existing Turn discipline section as a new paragraph, per the plan's Pattern: single global bound statement, rather than repeating the bound at all five edge sites"
  - "Extended the existing regenerate-the-analysis sentence for LOOP-05's disclosure requirement instead of authoring a new table artifact, per the plan's Pattern: extend an existing artifact"
  - "Wrapped pinned literals L3 (returns to Phase 1 to re-frame the Essence Statement) onto a single unbroken line rather than the surrounding paragraph's normal ~100-char wrap width, because the plan's substring-match verification treats a mid-phrase newline as a break in the literal"

patterns-established:
  - "Pinned multi-word literal strings destined for substring-match gates must not be split across a hard-wrapped line boundary in the source Markdown"

requirements-completed: [LOOP-01, LOOP-03, LOOP-04, LOOP-05]

# Metrics
duration: ~20min
completed: 2026-08-28
---

# Phase 2 Plan 01: Observe->Perceive Loop Closure (body-side edits) Summary

**Four prose edits to `shared/spine/SKILL-body.md` close the Observe->Perceive edge on the emitted agent body: a single canonical re-entry bound naming all five feedback edges, a re-entry disclosure rule, a bounded Fix/Repeat loop, and a new Phase-1 re-entry route for Criterion 1 Absent verdicts — all verified present in the regenerated `first-principles/agents/first-principles.md`, not just the source.**

## Performance

- **Duration:** ~20 min
- **Completed:** 2026-08-28
- **Tasks:** 3 (all `type="auto"`, no checkpoints)
- **Files modified:** 2 (`shared/spine/SKILL-body.md`, `first-principles/agents/first-principles.md`)

## Accomplishments

- Added a single canonical **"Re-entry edges are bounded."** paragraph to `### Turn discipline` naming all five re-entry edges (second-order->Phase 2, Fix/Repeat, rubric re-score, the new Criterion-1->Phase-1 route, and the mid-run `AskUserQuestion` re-open), stating the one-pass bound and the unresolved-gap-with-confidence-caveat degradation path, and the `maxTurns: 60` rationale.
- Extended the existing "If you regenerate the analysis" revision-tracking sentence to require naming which re-entry edge fired, what triggered it, and what changed — surfaced at the top of the response, reusing the "Before presenting conclusions" section's recoverable-vs-silent framing, explicitly not a seventh output section.
- Rewrote the Fix/Repeat list's item 3 to re-score once, then report an unresolved gap with a confidence caveat instead of fixing again — removing the unbounded `until every criterion clears the gate` instruction (X1) from the file entirely.
- Added a new paragraph routing a Criterion 1 Absent verdict back to Phase 1 to re-frame the Essence Statement (not an in-place output-section-1 patch), bounded by the Turn discipline rule, with a pointer to `AskUserQuestion` for the missing-input variant (authored fully in plan 02-02).
- Appended an exception clause to the Phase 3 `**Exit criterion:**` line preserving the original completeness claim verbatim while naming the bounded re-entry edges as the sanctioned exception.
- Regenerated `first-principles/agents/first-principles.md` via `sync-content.py --write` and proved every added literal (L1-L4, L10a/L10b) and the removed X1 phrase reach the emitted surface, not only `shared/`.

## Task Commits

Each task was committed atomically:

1. **Task 1: State the global re-entry bound and the re-entry firing record in Turn discipline** - `367ce07` (feat)
2. **Task 2: Add the Phase-1 re-entry route and bound the Fix/Repeat loop** - `78f0e38` (feat)
3. **Task 3: Fix Phase 3's contradicting exit criterion, regenerate, and prove the edits reach the emitted body** - `b8a4886` (feat)

## Exact Final Wording of Added Sentences

Recorded verbatim for plan 02-03's gate, which asserts these literals by exact substring match.

**Task 1, Edit A (new paragraph in `### Turn discipline`, after the "Never poll" paragraph):**

> **Re-entry edges are bounded.** Five re-entry edges exist in this methodology: the second-order pass's return to Phase 2 for re-challenging, the Self-Audit Gate's Fix/Repeat loop, the Self-Audit Gate rubric's re-score instruction, the Criterion 1 Absent verdict's return to Phase 1 to re-frame the Essence Statement (below), and the mid-run `AskUserQuestion` re-open (Input Contract). Each edge fires **at most one re-perception pass** per analysis. A second failure of the same criterion after one pass is reported as an **unresolved gap with a confidence caveat**, not a second pass. This bound holds because the turn budget is `maxTurns: 60` and the Self-Audit Gate runs last: an unbounded loop spends the gate's own budget, and the gate is what gets dropped.

**Task 1, Edit B (appended to the "If you regenerate the analysis" paragraph):**

> ... indistinguishable from one that was never produced. When a re-entry edge fires, disclose it the same way: **name which re-entry edge fired**, what triggered it — which criterion scored Absent, or which input was missing — and what changed as a result, stated at the top of the response alongside the omission disclosures required under "Before presenting conclusions": a disclosed re-entry is recoverable, a silent one is not. This disclosure is process output, not a seventh output section.

**Task 2, Edit A (rewritten Repeat item, single line):**

> 3. **Repeat** — re-score once after fixing. If a criterion still fails after that single re-perception pass, report it as an unresolved gap with a confidence caveat instead of fixing it again — see Turn discipline for the bound governing every re-entry edge.

**Task 2, Edit B (new paragraph after the numbered list, before "The Self-Audit Gate scores THIS analysis's own structure..."):**

> **A Criterion 1 Absent verdict returns to Phase 1.** When the Self-Audit Gate scores Criterion 1 Absent — the Essence Statement is missing, or the Problem Essence section holds only a restatement of the prompt with no analytical distillation — the analysis **returns to Phase 1 to re-frame the Essence Statement** and re-enters the phase chain from there. This is not an in-place rewrite of output section 1: an Essence Statement patched in place does not re-derive the artifacts downstream of it. This return is bounded by the Turn discipline rule (one re-perception pass) and is a revision like any other — artifacts carried forward or explicitly retired, and the firing recorded, per that same section. When the Absent verdict instead traces to an input the user never supplied — rather than to framing the analysis could have done itself — the route is to re-open input via `AskUserQuestion` under the Input Contract instead.

**Task 3 (appended exception clause to the Phase 3 `**Exit criterion:**` line, final sentence only):**

> The list is complete enough that Phase 4 can reason upward without needing to return to Phase 2 for new facts, except through the bounded re-entry edges named under Turn discipline: when a Criterion 1 return or a mid-run `AskUserQuestion` brings new facts into this list, that is the methodology working as specified, not a failure of this exit criterion.

No pinned literal required rewording. All of L1, L2, L3, L4, L10a, L10b were placed verbatim as specified, and X1 (`until every criterion clears the gate`) was fully removed from `shared/spine/SKILL-body.md` (confirmed absent from both the source and the emitted body).

## Files Created/Modified

- `shared/spine/SKILL-body.md` - Turn discipline re-entry bound + disclosure rule, bounded Fix/Repeat item, new Phase-1 re-entry route, Phase 3 exit-criterion exception clause
- `first-principles/agents/first-principles.md` - Regenerated via `sync-content.py --write`; carries every added literal byte-identically

## Decisions Made

- Followed the plan's two named research patterns exactly: one canonical bound statement (not five repeated ones) and extension of an existing artifact for the disclosure rule (not a new table) — both patterns were pre-selected in the plan's context, no independent architectural choice was needed here.
- A markdown mid-line hard-wrap in `SKILL-body.md`'s normal ~100-char style broke the pinned literal `returns to Phase 1 to re-frame the Essence Statement` across a line boundary (newline where the literal expects a space). Fixed by moving the wrap point earlier in that sentence so the full literal is contiguous on one line, since the literal is asserted by exact Python substring match against the raw file text (newlines are not whitespace-normalized before the check runs, either in this plan's own verify block or in plan 02-03's HARN-02 gate as described). This is a mechanical formatting fix, not a content change — flagged as its own pattern above since it will recur for plan 02-02's literals if the same wrap-width habit is followed there.

## Deviations from Plan

None — plan executed exactly as written. The line-wrap fix above is a formatting correction within Task 2's own scope (the literal had to land intact per the task's own `<verify>` block), not an unplanned addition; it did not touch any file, section, or literal outside what Task 2 already specified.

## Issues Encountered

- Initial attempt at Task 2 Edit B split the pinned literal `returns to Phase 1 to re-frame the Essence Statement` across a line break during authoring, causing the task's own `<verify>` script to fail with `AssertionError: L3 missing`. Diagnosed via `grep -n "re-frame the Essence Statement"` showing the phrase started mid-line 240 rather than being contiguous with the preceding "returns to Phase 1 to" on line 239. Resolved by re-wrapping the paragraph so the full literal sits on one line; re-ran the verify script, which then passed. No other tasks were affected.

## Next Phase Readiness

- All three of this plan's `<verify>` blocks pass, plus the plan's full `<verification>` checklist (8 items): `sync-content.py --check` exits 0; `SKILL-body.md` contains L1/L2/L3/L4 and not X1; the Phase 3 exit line contains L10a and L10b; the emitted body contains L1-L4 and not X1; `check-agent.py --self-test` and `--file first-principles/agents/first-principles.md` both PASS; `check-links.py` PASS (237 links + 6 namespace refs, 125 files); `git diff --name-only` against the pre-plan base lists exactly the two files this plan's frontmatter names and no others.
- `markdownlint-cli2` on the regenerated agent body: 0 issues. `sync-content.py --self-test` (GATE-02-v8.5 pointer drift-guard): ALL PASS.
- Plan 02-02 (wave 2) can proceed: it authors the `AskUserQuestion` side of the Input Contract re-entry route and the rubric's own re-score bound in `validation-rubric.md`, both of which this plan's body-side text already points to by name (`AskUserQuestion` under the Input Contract; "Turn discipline" for the bound) without restating their content.
- Plan 02-03 (wave 3, HARN-02 gate) can build its literal-presence assertions directly against the exact wording quoted above — none of it needs rewording, and none of it is stranded in `shared/` only: every literal was proven present in the emitted `first-principles/agents/first-principles.md` as well.
- Not run in this plan (deliberately, per the plan's own instruction): `bash scripts/check-firewall-battery.sh` was not used to judge this plan, since it reports `FIREWALL: RED (16/17)` on the unmodified tree for a pre-existing, unrelated reason (bare `python3 -m pytest` cannot find pytest outside `.venv`). Not independently re-confirmed in this plan's execution; carried forward from the plan's own stated baseline.

---
*Phase: 02-loop-closure*
*Completed: 2026-08-28*

## Self-Check: PASSED

- FOUND: shared/spine/SKILL-body.md
- FOUND: first-principles/agents/first-principles.md
- FOUND: .planning/phases/02-loop-closure/02-01-SUMMARY.md
- FOUND commits: 367ce07, 78f0e38, b8a4886, 5219d08
