---
phase: 03-validation-rubric
reviewed: 2026-05-17T00:00:00Z
depth: standard
files_reviewed: 1
files_reviewed_list:
  - first-principles-thinking/references/validation-rubric.md
findings:
  critical: 2
  warning: 6
  info: 3
  total: 11
status: issues_found
fix_status: all_resolved
fix_iteration: 2
fixed_findings:
  - CR-01
  - CR-02
  - WR-01
  - WR-02
  - WR-03
  - WR-04
  - WR-05
  - WR-06
  - IN-01
  - IN-02
  - IN-03
remaining_findings: []
---

# Phase 3: Code Review Report

**Reviewed:** 2026-05-17T00:00:00Z
**Depth:** standard
**Files Reviewed:** 1
**Status:** issues_found

## Summary

Reviewed `first-principles-thinking/references/validation-rubric.md`, the Layer-3
scoring instrument for the first-principles skill. It is a pure-Markdown reference
component — no runtime, no input handling — so the review targets internal
consistency, cross-reference correctness, and whether the rubric's own descriptors
are unambiguous and self-consistent.

The rubric is well-structured and largely coherent, but contains two BLOCKER-class
defects that make it self-contradicting or un-applicable as written: the pass
condition stated in the Scoring Model directly contradicts the gate defined in
"How to Apply This Rubric," and the rubric cites design-decision IDs (`D-01`, `D-08`)
that exist nowhere in `SKILL.md` or `output-template.md`. Six WARNING-class
consistency gaps and three INFO items follow. WR-05 and WR-06 were surfaced by an
adversarial cross-reference pass against the two sibling files and were not present
in the prior review.

No structural findings block was provided; all findings below are narrative.

## Critical Issues

### CR-01: Contradictory pass conditions — "Pass" definition conflicts with the gate [RESOLVED]

**Status:** Resolved in commit `04a7be1` — dropped the contradictory "Every criterion scores Sound or above" clause; the Pass definition now matches the gate (no Absent, at most one Hand-wavy).


**File:** `first-principles-thinking/references/validation-rubric.md:18-21` and `:60`
**Issue:** The "How to Apply This Rubric" section defines the pass condition as exactly
two clearing conditions:

> 1. **Gate cleared** — no criterion scores Absent.
> 2. **Hand-wavy cap cleared** — at most one criterion scores Hand-wavy.

This permits a passing analysis to contain criteria scored **Hand-wavy** (up to one).
But line 60 in the Scoring Model states:

> **Pass:** Every criterion scores Sound or above, with at most one criterion at Hand-wavy.

"Every criterion scores Sound or above" and "at most one criterion at Hand-wavy" are
mutually exclusive — a criterion at Hand-wavy is *not* "Sound or above" (the rank order
on line 49 is `Rigorous > Sound > Hand-wavy > Absent`). The first clause forbids any
Hand-wavy; the second clause permits one. A reviewer cannot tell whether an analysis
with one Hand-wavy criterion passes. This is a logic error that produces an
unresolvable verdict — the rubric's central output (pass/fail) is undefined for a
common case.
**Fix:** Drop the contradictory first clause so the definition matches the gate:
```markdown
**Pass:** No criterion scores Absent, and at most one criterion scores Hand-wavy.
(Equivalently: every criterion is Sound or above, except at most one may be Hand-wavy.)
```

### CR-02: Dangling design-decision references — `D-01` and `D-08` are undefined [RESOLVED]

**Status:** Resolved in commit `29f6112` — repo grep confirmed only `D-03` and `D-07` exist. `D-01` corrected to `D-07` (unverified-flag/`GT-N?` discipline, per `SKILL.md:71,81,97` and `output-template.md:44,83,114,150`); `D-08` corrected to `D-03` (Abandoned Reasoning escape valve, per `output-template.md:134`).


**File:** `first-principles-thinking/references/validation-rubric.md:139`, `:195`, `:196`
**Issue:** Criterion 2 (line 139) and Criterion 4 (lines 195-196) cite design-decision
identifiers as authority for what they fold in:

- Line 139: "Folds in: four-type classification quality and unverified-flag discipline (D-01)."
- Lines 195-196: "Folds in: dead-end honesty and the no-analogies-as-direct-evidence ban
  (D-01), and escape-valve policing for Abandoned Reasoning (D-08)."

A repo-wide grep of `SKILL.md`, `references/output-template.md`, and the other
reference/example files shows the only design-decision IDs defined are **D-03** and
**D-07**. `D-01` and `D-08` appear *only* in this file — they reference nothing. A
reviewer who tries to follow these citations to the source rule will find no rule. The
rubric is asserting traceability to design decisions that do not exist, which both
breaks the cross-reference and undermines the rubric's own auditability claim
(lines 92-96 argue the rubric must be auditable against quoted evidence).

Note the related symptom in Criterion 3 (line 168) and Criterion 5: the unverified-flag
behavior the rubric describes is the one `SKILL.md:65,71,81,97` and
`output-template.md:44,83,114,150` attribute to **D-07** — strongly suggesting `D-01`
was intended to be `D-07`. `D-08` is best matched by `D-03`, which
`output-template.md:134` ties directly to the required-Abandoned-Reasoning escape valve.
**Fix:** Either (a) correct the IDs to the design decisions that actually define these
rules — most likely `D-07` for the unverified-flag/`GT-N?` discipline and `D-03` for
the required-Abandoned-Reasoning-section / escape-valve rule — or (b) if a canonical
D-01..D-08 decision log exists outside the reviewed scope, add it to the repo and
confirm the IDs resolve. Do not ship dangling references.

## Warnings

### WR-01: Escape-valve scoring is undefined for four of six criteria [RESOLVED]

**Status:** Resolved in commit `26d37e2` — added a global "Escape-valve scoring" rule to the Scoring Model: a legitimate escape valve scores Rigorous (analysis-specific reason) or Hand-wavy (generic reason), never Absent solely for using it.


**File:** `first-principles-thinking/references/validation-rubric.md:111-275`
**Issue:** The skill's output format (`SKILL.md:128-132`, `output-template.md:12-16`)
permits any section to use the honest-depth escape valve (`Nothing material here — [reason]`).
The rubric only tells a reviewer how to score that escape valve for **Criterion 1**
(lines 118-119, 128-129) and **Criterion 4 / Abandoned Reasoning** (lines 204-206,
218-220). For Criteria 2, 3, 5, and 6, an escape-valve section is unaddressed: a
reviewer encountering `Nothing material here — [reason]` in, e.g., the Assumptions
Table cannot tell whether that scores Rigorous (justified omission), Hand-wavy (generic
reason), or Absent (the Absent descriptors on lines 131-133, 161-163, 246-249, 272-275
all read as if any empty-looking section is Absent). This is a genuine gap that will
produce inconsistent verdicts across reviewers.
**Fix:** Add a single global rule to the Scoring Model: "Any section legitimately using
the honest-depth escape valve is scored Rigorous if the stated reason is specific to
this analysis and Hand-wavy if the reason is generic/copy-pasteable; it is never scored
Absent solely for using the escape valve." Then the per-criterion Absent descriptors
should explicitly exclude a properly-used escape valve.

### WR-02: Criterion 4 vs. output-template disagree on "one chain per conclusion" [RESOLVED]

**Status:** Resolved in commit `0b34a55` — added the redundant-chain case ("a conclusion has more than one derivation chain") to the Criterion 4 Sound band.


**File:** `first-principles-thinking/references/validation-rubric.md:199` and `:223-224`
**Issue:** Criterion 4 Rigorous (line 199) requires "every conclusion stated anywhere
in the document (in section 4 or section 6) has exactly one derivation chain in
section 4." But the Absent descriptor (lines 223-224) treats "conclusions appear in
section 6 with no corresponding chains in section 4" as the Absent trigger. There is no
band defined for the in-between case the template explicitly warns about
(`output-template.md:95`: "no more (no redundant restatement)") — i.e., a conclusion
with *two or more* chains. Duplicate/redundant chains are a defect the template names,
yet Criterion 4's four bands have no slot for it; a reviewer would have to force-fit it
into Sound or Hand-wavy with no descriptor support.
**Fix:** Add the redundant-chain case to a band — most naturally Sound ("a conclusion
has more than one chain — redundant restatement rather than a missing chain") so
Criterion 4 covers the full failure space the template defines.

### WR-03: Criterion 5 Absent third clause overlaps and can conflict with the first two [RESOLVED]

**Status:** Resolved in commit `fa0876f` — rewrote the third Absent clause to be strictly additive ("covering the case the first two clauses miss — confidence ratings exist but no weak-link identification or chain inspection").


**File:** `first-principles-thinking/references/validation-rubric.md:246-249`
**Issue:** Criterion 5 Absent lists three OR'd conditions. The third — "there is no
evidence that Phase 5's stress-test operation was executed (no weak-link
identification, no chain inspection, no confidence rating of any kind)" — restates the
first ("no confidence ratings appear anywhere in the derivation chains") plus more. The
bands are meant to be mutually exclusive verdicts; an overlapping/encompassing clause
makes it ambiguous which clause a reviewer cites in the required Justification line
(line 75 demands the reviewer "name the specific structural property present or
absent"). Overlapping descriptors weaken the auditability the rubric claims for itself.
**Fix:** Make the third clause strictly additive, e.g., "OR — covering the case the
first two clauses miss — confidence ratings exist but no weak-link identification or
chain inspection was performed at all," or merge it into the first clause.

### WR-04: "load-bearing chain" used as a scoring term but never defined [RESOLVED]

**Status:** Resolved in commit `11fb53b` — added a "Load-bearing chain (definition)" entry to the Scoring Model: a chain is load-bearing if a Conclusion-section (section 6) claim depends on it.


**File:** `first-principles-thinking/references/validation-rubric.md:232`, `:247`
**Issue:** Criterion 5 Rigorous and Absent both hinge on whether a `GT-N?` input
"appears in a load-bearing chain" / is used "in load-bearing chains." The band a
reviewer assigns can flip on this judgment, but "load-bearing" is never defined in this
file. `SKILL.md:109` uses "load-bearing for a high-stakes conclusion" — a different,
narrower phrasing. Leaving the threshold undefined makes Criterion 5 scoring subjective
in exactly the place it must be precise (the rubric's stated purpose, lines 92-96, is
to be un-fudgeable).
**Fix:** Define the term once near the Scoring Model or at first use, e.g., "A chain is
*load-bearing* if a conclusion in section 6 depends on it." Align the wording with
`SKILL.md` or note the intentional difference.

### WR-05: Criterion 4 scope is ambiguous — title says "Derivation Chains," body also scores section 5 [RESOLVED]

**Status:** Resolved in commit `175a92b` — rewrote the Criterion 4 lead to state it scores **both** the Derivation Chains (output section 4) **and** the Abandoned Reasoning section (output section 5).


**File:** `first-principles-thinking/references/validation-rubric.md:190-220`
**Issue:** Criterion 4 is titled "Reason Upward" and its lead sentence says it "Scores
the **Derivation Chains** ... produced in Phase 4." But the band descriptors also score
the **Abandoned Reasoning** section, which `output-template.md:18-24,118` defines as a
*separate* output section — section 5, not section 4. A reviewer who reads the criterion
title and lead literally will score Criterion 4 on the chains alone (section 4) and
never inspect the escape-valve quality of section 5, because the criterion name and the
section it actually scores disagree. The "Folds in: ... escape-valve policing for
Abandoned Reasoning" note (line 196) is the only hint the section-5 content is in scope,
and it is buried in the same line as the broken D-08 reference. This produces
inconsistent verdicts: two reviewers will disagree on whether Abandoned Reasoning was
even meant to be scored here.
**Fix:** Make the section coverage explicit in the criterion lead, e.g. "Scores **both**
the Derivation Chains (output section 4) **and** the Abandoned Reasoning section (output
section 5)," so the scope cannot be read as section-4-only.

### WR-06: Double-jeopardy — the unflagged-`GT-N?`-in-a-chain defect is scoreable under three criteria [RESOLVED]

**Status:** Resolved in commit `cc783b5` — added a "Precedence rule (no double-counting)" to "How to Apply This Rubric": band a multi-criterion defect under the lowest-numbered criterion and only note the overlap elsewhere.


**File:** `first-principles-thinking/references/validation-rubric.md:152-154`, `:177-178`, `:182-183`, `:238-239`
**Issue:** A single observable defect — an unverified ground truth used in a chain
without the `?` suffix / "unverified — flagged" notation — is independently scoreable
under at least three criteria with no precedence rule:
- Criterion 2 Sound (line 152-154): an assumption used in a chain "lacks the
  'unverified — flagged' notation."
- Criterion 3 Sound / Hand-wavy (lines 177-178, 182-183): one / multiple unverified GTs
  "used in a derivation chain without the `?` suffix."
- Criterion 5 Sound (lines 238-239): "GT-N? inputs in chains are not mentioned in the
  chain's confidence line."

The rubric never says which criterion "owns" the defect. As written, one real flaw
drags down two or three criteria at once, and a pattern of them could trip the
Hand-wavy cap (CR-01 / lines 54-58) on the strength of a single underlying problem —
the gate/cap math double-counts. Scoring is therefore non-deterministic across
reviewers depending on how many criteria they choose to apply it to.
**Fix:** Add a precedence note to "How to Apply This Rubric": when one observable defect
maps to more than one criterion, score it under the lowest-numbered criterion whose
descriptor names it, and merely note (do not re-band) the overlap under the others.
Alternatively, narrow each descriptor so the `GT-N?`-flag rule lives in exactly one
criterion.

## Info

### IN-01: Heading levels make all six criteria siblings of "## Criteria" [RESOLVED]

**Status:** Resolved in commit `b1fb4c9` — demoted all six "## Criterion N" headings to `### Criterion N` so they nest under `## Criteria`.

**File:** `first-principles-thinking/references/validation-rubric.md:100`, `:106`, `:135`, `:165`, `:190`, `:226`, `:251`
**Issue:** "## Criteria" (line 100) is an H2, and each "## Criterion N" (lines 106,
135, 190, 226, 251) is also an H2 — so the six criteria are siblings of the section
that introduces them, not children. A document outline / table of contents will render
"Criteria" as an empty section followed by six peers. Cosmetic, but the skill's own
tech guidance (`CLAUDE.md`) keeps `MD003` consistent-heading discipline.
**Fix:** Demote the six criterion headings to `### Criterion N: ...` so they nest under
`## Criteria`.

### IN-02: "produced in Phase N" couples the rubric to methodology internals [RESOLVED]

**Status:** Resolved in commit `c35ca24` — criterion intros now reference the output-template section the artifact lives in (e.g., "Problem Essence section (output section 1)") rather than the producing phase, and the Criteria preamble was softened to "Criteria 1-5 follow the order of the six-section output format ... Criterion 6 is a whole-document cross-section check applied last."

**File:** `first-principles-thinking/references/validation-rubric.md:109`, `:136`, `:167`, `:194`, `:228`
**Issue:** Each criterion intro says the artifact is "produced in Phase 1/2/3/4/5." The
rubric's own scope note (lines 3-9) says it scores against the *six-section output
format*, not the methodology phases, and that the loop/procedure lives in `SKILL.md`.
Tying criterion descriptions to phase numbers means any renumbering of phases in
`SKILL.md` silently desyncs this file. Low risk today, but it is an unnecessary
coupling for a "score the artifact" instrument. Related: the "Criteria" preamble
(lines 102-104) claims "the criteria follow methodology-phase order," but Criterion 6
(lines 251-255) is a whole-document cross-section check that maps to no phase — the
blanket claim is not literally true for the sixth criterion.
**Fix:** Reference the output-template section the artifact lives in (e.g., "the
Essence Statement — output section 1") rather than the producing phase; and soften the
preamble to "Criteria 1-5 follow methodology-phase order; Criterion 6 is a
whole-document cross-section check applied last."

### IN-03: Section numbers cited bare, without naming the template they index [RESOLVED]

**Status:** Resolved in commit `9136ced` — the gap-citation example now names sections alongside numbers ("section 4 (Derivation Chains)", "section 6 (Conclusion)"), and the band names in the Verdict Block Format example are now bolded for uniformity with the rest of the file. The Criterion 4 and Criterion 6 leads already named their sections.

**File:** `first-principles-thinking/references/validation-rubric.md:73`, `:199-200`, `:222-224`, `:252-255`
**Issue:** Two minor consistency nits. (a) Criteria 4 and 6 cite "section 4" and
"section 6" as bare numbers; the numbering is defined in `output-template.md:18-24`, not
in this file, and the scope note says a reviewer may "come here only to score an
analysis" — i.e., possibly without the template loaded. (b) The Verdict Block Format
example (line 73) writes `Band: [Rigorous / Sound / Hand-wavy / Absent]` un-bolded,
while every other occurrence of the band names is bolded (`**Rigorous**`).
**Fix:** On first use, name the section alongside the number ("section 4 (Derivation
Chains)", "section 6 (Conclusion)"); optionally bold the band names in the example for
uniformity. No functional impact.

---

_Reviewed: 2026-05-17T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
