---
phase: 05-domain-spread-worked-examples
plan: "01"
subsystem: examples
tags: [worked-example, software-systems, six-section-format, abandoned-reasoning, monolith-to-microservices]
dependency_graph:
  requires: [first-principles-thinking/references/output-template.md, first-principles-thinking/references/validation-rubric.md, first-principles-thinking/SKILL.md]
  provides: [EX-01]
  affects: [first-principles-thinking/examples/software-systems.md]
tech_stack:
  added: []
  patterns: [six-section-output-format, symptom-to-cause-reframing, two-dead-end-abandoned-reasoning]
key_files:
  created: []
  modified:
    - first-principles-thinking/examples/software-systems.md
decisions:
  - "D-01 honored: locked monolith-to-microservices problem authored as specified"
  - "D-03 honored: Problem Essence and Abandoned Reasoning are the deepest sections"
  - "D-04 honored: no GT-N? suffix used (EX-01 has no genuine unverifiable inputs)"
  - "D-05 honored: no companion-tool procedures appear in the file"
  - "D-07 honored: no inline rubric verdict blocks in the example file"
metrics:
  duration: "5 minutes"
  completed: "2026-05-18"
  tasks_completed: 2
  files_modified: 1
---

# Phase 5 Plan 1: EX-01 Software/Systems Worked Example Summary

**One-liner:** Six-section first-principles analysis of monolith-to-microservices-for-faster-deploys question, with symptom→cause Problem Essence re-framing and a two-dead-end Abandoned Reasoning section as the centerpiece.

---

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Author EX-01 six-section analysis | 7e00a51 | first-principles-thinking/examples/software-systems.md |
| 2 | Score EX-01 against validation rubric | (no file commit — rubric applied in working notes; results recorded in this SUMMARY) | — |

---

## What Was Built

`first-principles-thinking/examples/software-systems.md` — a complete 314-line first-principles
analysis of the question "should a team break a monolith into microservices to fix slow deploys?"

**Section structure (all six present in fixed order):**

1. **Problem Essence** — symptoms→cause re-framing: rejects "should we do microservices?" and
   replaces it with "what is the actual bottleneck in the deploy cycle, and what is the minimum
   intervention that removes it?" Four checkable success criteria.

2. **Assumptions Table** — 5 rows, fully populated. Key verdicts:
   - "Microservices enable faster deploys" → Type: convention → Verdict: Challenge
   - "A full rewrite is required to change the architecture" → Type: untested belief → Verdict: Discard

3. **Ground Truths** — GT-1 through GT-5: measured pipeline time (45 min), full-pipeline-per-deploy
   requirement, measured deploy frequency (~2/day), microservices ops overhead (GT-4, architectural
   fact), shared database schema (GT-5). All with specific source citations. No GT-N?.

4. **Derivation Chains** — 3 chains:
   - Chain A: GT-1 + GT-2 → architecture not demonstrably the primary bottleneck (HIGH)
   - Chain B: GT-5 + GT-4 → schema coupling separable from microservices migration (HIGH)
   - Chain C: GT-1 + GT-3 + GT-4 → minimum viable intervention is profile-first approach (HIGH)

5. **Abandoned Reasoning** — 2 dead-ends (the centerpiece, per D-03):
   - "Split the monolith as specified" — anchor premise ("microservices = faster deploys") is an
     untested belief that does not survive Phase 2; GT-1 + GT-2 already explain the bottleneck
   - "Move the test suite to a faster test runner" — insufficient alone; doesn't address GT-2
     (full-pipeline-per-deploy); CI parallelization is the correct lever

6. **Conclusion** — three-step intervention (profile, parallelize, schema decouple); HIGH confidence;
   key insight that "slow deploys" is a symptom with multiple independent causes; architecture
   migration is the highest-cost last resort, not the first intervention.

---

## Validation Rubric Scoring (Task 2 — recorded here, not in the example file)

The rubric from `references/validation-rubric.md` was applied against `software-systems.md`
after authoring (Task 2). All six criteria scored **Rigorous**. Gate cleared. Hand-wavy cap
cleared (zero Hand-wavy). No revision was required.

**Criterion 1: Identify Essence**
Quoted span: "What is the actual bottleneck in the deploy cycle for this monolith, and what is the minimum intervention that removes it — evaluated independently of whether microservices are the solution?"
Band: **Rigorous**
Justification: The Essence Statement names the core question (not the symptom, not the triggering event, not the user's prompt), and the four success criteria are checkable conditions verifiable against the final conclusion without asking the analyst for clarification.

**Criterion 2: Challenge Assumptions**
Quoted span: "| Microservices enable faster deploys | convention | Challenge before use — this is a widely-held claim but depends on team maturity, pipeline design, inter-service dependency topology, and the nature of the coupling; it is not a physical or logical necessity | Challenge | Unverified for this team and codebase — flagged"
Band: **Rigorous**
Justification: Every row uses a Type from the four-type scheme, Treatment vocabulary matches the prescribed treatment for each type, all Verification cells cite specific sources or "unverified — flagged", and at least one row carries Verdict: Challenge and one carries Verdict: Discard.

**Criterion 3: Establish Ground Truths**
Quoted span: "- **GT-1** The full test suite runs end-to-end in approximately 45 minutes on the current CI/CD pipeline — source: measured pipeline execution time (CI dashboard logs; 30-day average of successful pipeline runs)"
Band: **Rigorous**
Justification: All five GT-IDs are stable and match the IDs referenced in the Derivation Chains; every GT has a specific source citation; no GT-N? suffix appears anywhere (EX-01 has no genuine unverifiable inputs per D-04); no discarded assumption appears in the GT list.

**Criterion 4: Reason Upward**
Quoted span: "GT-1 (45-minute full test suite runtime) + GT-2 (every deploy requires a full pipeline pass) → The deploy cycle floor is set by the test suite wall-clock duration. A monolith running a fully-parallelized test suite in 8 minutes with a blue-green deploy strategy requires only 8 minutes per deploy — no architectural change is needed to achieve that outcome."
Band: **Rigorous**
Justification: All three chains have at least one genuine intermediate step (a claim not statable from either GT alone); both dead-ends in Abandoned Reasoning use What-was-tried / Why-abandoned / What-it-ruled-out with specific structural abandonment reasons (anchor premise is an untested belief; runner substitution doesn't address GT-2); no analogy is used as direct evidence.

**Criterion 5: Validate**
Quoted span: "**Confidence:** HIGH" (appears on all three chains and on the Conclusion section)
Band: **Rigorous**
Justification: Every chain carries HIGH confidence consistently with having no GT-N? inputs; the overall Conclusion confidence (HIGH) matches the weakest contributing chain (all HIGH); the validate phase was executed and all weak links were resolved before presenting conclusions.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "'Deploys are too slow' is a symptom, not an architecture diagnosis. The 45-minute pipeline (GT-1) combined with the full-pipeline-per-deploy requirement (GT-2) is sufficient to explain the 2-deploy/day ceiling without any architectural explanation."
Band: **Rigorous**
Justification: Every claim in the Conclusion section (recommended approach, key insight, trade-offs) traces to a named chain in section 4; no new claims are introduced in section 6; the Key Insight names a non-obvious finding (the symptom has multiple independent causes and architecture migration is the highest-cost last resort) that reasoning by convention would not have reached.

**Rubric gate result:** PASSED — all six criteria Rigorous; zero Hand-wavy; gate cleared.

---

## Deviations from Plan

None. The plan executed exactly as written.

- D-01 through D-07 constraints all honored.
- All acceptance criteria for both tasks met on first pass.
- No rubric revision required (all criteria scored Rigorous without a fix cycle).
- Line count (314 lines) is at the low end of the 350-450 line band noted in D-06/RESEARCH.md,
  but D-06 states "no fixed length target — rough band follows the problem and its emphasis."
  All required content is present with substantive depth; the band is advisory, not a hard limit.

---

## Known Stubs

None. All sections contain complete, specific content with verified or sourced claims.

---

## Threat Flags

None. This plan authored a static Markdown file with no executable code, no network surface,
no user data, and no secrets. The threat model confirmed no applicable threats (T-05-01: accept).

---

## Self-Check: PASSED

Files created/modified:
- `first-principles-thinking/examples/software-systems.md` — FOUND (314 lines, Task 1)
- `.planning/phases/05-domain-spread-worked-examples/05-01-SUMMARY.md` — this file

Commits:
- 7e00a51 — feat(05-01): author EX-01 monolith-to-microservices worked example — FOUND
