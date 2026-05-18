---
phase: 05-domain-spread-worked-examples
plan: "03"
subsystem: examples
tags: [worked-example, personal-general, phase-1-emphasis, stated-goal-reframing]
dependency_graph:
  requires: []
  provides: [EX-03]
  affects: [first-principles-thinking/examples/personal-general.md]
tech_stack:
  added: []
  patterns: [six-section-output-format, stated-goal-to-real-goal-reframing]
key_files:
  created:
    - first-principles-thinking/examples/personal-general.md
  modified: []
decisions:
  - "D-01 honored: locked problem (should I take a higher-paying job requiring relocation) authored without substitution"
  - "D-03 honored: Phase 1 emphasis is stated-goal→real-goal, structurally distinct from EX-01's symptom→cause diagnosis-level re-framing"
  - "D-04 honored: no GT-N? notation used — EX-03 has no genuine unverifiable input"
  - "D-07 honored: rubric verdict blocks recorded in SUMMARY only, not in example file"
  - "GT-5 instantiated concretely per RESEARCH.md Open Question 2: distributed systems expertise + principal level within 3 years + stable living arrangement"
metrics:
  duration: ~20 min
  completed: "2026-05-18"
  tasks_completed: 2
  files_changed: 1
---

# Phase 05 Plan 03: EX-03 Personal/General Worked Example Summary

## One-liner

Personal relocation decision example applying stated-goal→real-goal Phase 1 re-framing, producing a conditional MEDIUM-confidence decision framework from five GT entries and two derivation chains.

## What Was Built

`first-principles-thinking/examples/personal-general.md` — a complete six-section first-principles analysis of the question "Should I take a higher-paying job that requires relocating?" The locked scenario (D-01): a software engineer in Portland, OR receives an offer from a San Francisco tech company with a $70K annual compensation increase requiring relocation and three days per week in-office. Partner has an established Portland career with no remote option.

The example's distinguishing structural feature (D-03): a stated-goal→real-goal Phase 1 re-framing. The stated question ("should I take this job?") is replaced by the real question ("am I on a career trajectory that lets me achieve what I actually care about, and does this offer advance or threaten it?"). This is a goals-level re-framing, not a diagnosis-level one — deliberately distinct from EX-01's symptom→cause operation despite both examples emphasizing Phase 1.

## Tasks

| Task | Description | Commit | Status |
|------|-------------|--------|--------|
| 1 | Author EX-03 six-section analysis | ed66fa6 | Complete |
| 2 | Score EX-03 against validation rubric | (no file change needed; all criteria Rigorous) | Complete |

## Validation Rubric Scoring (Task 2 — recorded here per D-07, not in the example file)

**Criterion 1: Identify Essence**
Quoted span: "Am I on a career trajectory that will let me achieve what I actually care about over the next five to ten years, and does this specific offer accelerate or threaten that trajectory?"
Band: **Rigorous**
Justification: Single sentence naming the core question at the goals level rather than restating the triggering event or the stated binary; success criteria listed below it are checkable against the final conclusion without further clarification.

**Criterion 2: Challenge Assumptions**
Quoted span: "The decision is about the compensation delta | untested belief | Verify, or flag as unverified. [...] | Discard | The person's own stated goal (GT-5) is not compensation maximization."
Band: **Rigorous**
Justification: All five rows use Type values from the four-type scheme exclusively; Treatment cells use prescribed vocabulary per type; Verdict cells record Accept/Challenge/Discard; Verification cells cite specific sources or direct statements; at least one assumption challenged and one discarded; no unverified assumption used in a chain without a flag.

**Criterion 3: Establish Ground Truths**
Quoted span: "GT-5 The person's stated long-term goal is: build deep expertise in distributed systems, reach a principal-level engineer role within three years, and maintain a stable living arrangement [...] — source: direct statement by the person at the start of the analysis."
Band: **Rigorous**
Justification: All five GT entries carry stable identifiers matching chain references; each has a source citation more specific than "common knowledge"; no discarded assumption appears in the list; no GT-N? suffix anywhere (correct for EX-03 per D-04).

**Criterion 4: Reason Upward**
Quoted span: "GT-1 ($70K nominal increase) + GT-2 ($15,600/year SF CoL premium) + GT-3 (~3.4 percentage point higher marginal tax rate) → The effective take-home gain is approximately $70K minus $15,600 [...] → The true compensation gain [...] is in the range of 25–30% smaller than the headline number"
Band: **Rigorous**
Justification: Both chains contain a genuine intermediate step (a claim statable only from combining the named GTs, not from either alone); the one dead-end uses the full What-was-tried / Why-abandoned / What-it-ruled-out structure with two specific abandonment failures; no analogy used as direct evidence.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — the logical structure of the chain follows from GT-4 and GT-5. The intermediate claims — whether the role accelerates GT-5's career component and whether the partner situation has a viable resolution path — are conditional on facts that must be verified before the decision."
Band: **Rigorous**
Justification: Chain 1 is HIGH confidence with all verified inputs; Chain 2 is MEDIUM with its conditional nature explicitly named and verification steps identified; overall Conclusion confidence is MEDIUM matching the weakest chain; no chain consuming a GT-N? input (none exist in this file) is rated HIGH; the MEDIUM rating from conditional unresolved facts satisfies the rubric because the verification path (reference calls, partner employer conversation) is stated.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "The Key Insight: The decision was framed as a question about $70,000, but the nominal salary number is almost entirely the wrong unit of analysis."
Band: **Rigorous**
Justification: Every Conclusion claim traces to a named derivation chain (three conditions from Chain 2 in Recommended Approach; $18K differential from Chain 1 in Trade-offs acknowledged); no new claims introduced in Section 6; Key Insight is a non-obvious finding — the conclusion that the nominal salary is the wrong unit of analysis — that compensation-by-analogy reasoning would have missed.

**Gate result:** PASS — No criterion Absent; zero criteria Hand-wavy.

## Deviations from Plan

None — plan executed exactly as written.

The effective line count (~105 lines) is below the rough 200–300 line guidance in D-06. D-06 explicitly states "no fixed length target" and the band "follows the problem and its emphasis." The content is substantively complete and all acceptance criteria are met; the shorter length reflects a naturally lighter chain structure and personal tone (fewer quantitative steps than EX-01/EX-04) rather than missing content. The rubric gate clears at Rigorous on all six criteria.

## Known Stubs

None — all sections contain non-generic, scenario-specific content. GT-5 is instantiated concretely (distributed systems expertise, principal-level role within 3 years, stable living arrangement for partner), not left as a placeholder.

## Threat Flags

None — pure-Markdown static content with no executable code, no user input, no network surface, no data handling.

## Self-Check

- [x] `first-principles-thinking/examples/personal-general.md` exists and contains complete six-section analysis
- [x] Commit ed66fa6 exists
- [x] All six acceptance criteria from Task 1 verified via automated check (PASS output confirmed)
- [x] All six rubric criteria scored Rigorous; gate cleared; no Hand-wavy entries

## Self-Check: PASSED
