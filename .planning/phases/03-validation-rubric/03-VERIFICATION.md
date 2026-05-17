---
phase: 03-validation-rubric
verified: 2026-05-17T12:00:00Z
status: gaps_found
score: 5/7 must-haves verified
overrides_applied: 0
gaps:
  - truth: "The rubric states a gate rule (any Absent fails) and a hand-wavy cap (two or more Hand-wavy fails)"
    status: partial
    reason: "The gate and cap are defined correctly in the 'How to Apply This Rubric' section (lines 18-19). However, the Scoring Model summary at line 60 contains a contradictory Pass condition: 'Every criterion scores Sound or above, with at most one criterion at Hand-wavy.' The first clause ('Sound or above') excludes Hand-wavy by the rubric's own rank order (Rigorous > Sound > Hand-wavy > Absent), while the second clause ('at most one Hand-wavy') permits it. A reviewer scoring an analysis with exactly one Hand-wavy criterion cannot determine whether it passes from the Scoring Model section alone. The REVIEW (CR-01) flags this as a BLOCKER."
    artifacts:
      - path: "first-principles-thinking/references/validation-rubric.md"
        issue: "Line 60: contradictory Pass definition — 'Every criterion scores Sound or above, with at most one criterion at Hand-wavy' is self-contradicting because Hand-wavy is below Sound per the rank order stated on line 49."
    missing:
      - "Replace the contradictory Pass line with a self-consistent definition matching lines 18-19, e.g.: '**Pass:** No criterion scores Absent, and at most one criterion scores Hand-wavy.'"
  - truth: "Honors CONTEXT.md decisions D-01: exactly 6 criteria with rigor sub-features folded per-phase; D-02: gate plus hand-wavy cap; D-03: one shared 4-level scale; D-05: hand-wavy cap set at 2 of 6; D-06: band labels Rigorous/Sound/Hand-wavy/Absent chosen by the planner; D-07: per-criterion verdict blocks; D-08: escape-valve policing in Criteria 1 and 4; D-09: explicit gap citation on a gate-fail verdict"
    status: failed
    reason: "The rubric cites design-decision identifiers D-01 and D-08 at lines 139, 195, and 196 (Criterion 2 and Criterion 4 'Folds in:' lines). These IDs exist only in 03-CONTEXT.md — a non-shipped planning artifact — and resolve to nothing in any shipped file (SKILL.md and output-template.md reference only D-03 and D-07). A reviewer following the rubric's D-01 and D-08 citations will find no target document. The rubric claims auditability (lines 92-96) while containing unresolvable cross-references. REVIEW CR-02 flags this as a BLOCKER."
    artifacts:
      - path: "first-principles-thinking/references/validation-rubric.md"
        issue: "Lines 139, 195-196: 'D-01' and 'D-08' are cited as authority for what each criterion folds in, but neither ID is defined in any shipped file. SKILL.md defines D-07; output-template.md references D-07 and D-03. D-01 and D-08 are internal CONTEXT.md planning IDs that were not supposed to appear in the shipped rubric."
    missing:
      - "Either (a) replace D-01 with D-07 (the unverified-flag/GT-N? discipline) and replace D-08 with D-03 (the Abandoned Reasoning / escape-valve rule per output-template.md:134), which are the shipped IDs that describe the same behaviors; or (b) remove the ID citations entirely and leave the fold-in descriptions as prose — the design intent is clear without IDs that cannot be resolved from a shipped file."
---

# Phase 3: Validation Rubric — Verification Report

**Phase Goal:** `references/validation-rubric.md` exists as a falsifiable self-check — analytic criteria with named, observable levels and gate scoring — that demonstrably catches hand-waving rather than certifying it.
**Verified:** 2026-05-17T12:00:00Z
**Status:** gaps_found (2 blockers from code review CR-01 and CR-02)
**Re-verification:** No — initial verification

## Step 0: Previous Verification

No previous VERIFICATION.md exists. Initial verification mode.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | validation-rubric.md defines exactly 6 analytic criteria, one per methodology phase plus traceability | VERIFIED | 6 `## Criterion` H2 headings at lines 106, 135, 165, 190, 226, 251; names match PLAN spec exactly |
| 2 | Each criterion carries the same 4-level scale, each level with a concrete observable descriptor (no adjectives) | VERIFIED | Rigorous/Sound/Hand-wavy/Absent appear 7-8 times each; adjective-test passes — no "adequate," "sufficient," or "thorough" found; descriptors are structural and countable |
| 3 | The rubric states a gate rule (any Absent fails) and a hand-wavy cap (two or more Hand-wavy fails) | PARTIAL — BLOCKER | Gate and cap are correctly defined in "How to Apply This Rubric" (lines 18-19) and restated in Scoring Model (lines 51-58). However, the Scoring Model's Pass: line (line 60) contradicts itself: "Every criterion scores Sound or above, with at most one criterion at Hand-wavy" — the first clause excludes Hand-wavy per the rank order on line 49, while the second clause permits one. Unresolvable verdict for the one-Hand-wavy case. |
| 4 | The rubric prescribes a per-criterion verdict-block format with a quoted span or explicit gap citation | VERIFIED | Lines 64-97 prescribe both the standard form (Quoted span / Band / Justification) and the gap-citation form (Gap / Band / Justification) in two fenced code blocks without language tags |
| 5 | Honors CONTEXT.md decisions including D-01, D-02, D-03, D-05, D-06, D-07, D-08, D-09 | FAILED — BLOCKER | The rubric cites D-01 (lines 139, 195) and D-08 (lines 195-196) as authority for what Criteria 2 and 4 fold in. Neither ID is defined in any shipped file. SKILL.md and output-template.md define only D-07 and D-03. These are internal planning IDs from CONTEXT.md that leaked into the shipped rubric. The other decision points (D-02, D-03, D-05, D-06, D-07, D-09) are correctly honored. |
| 6 | A deliberately-weak analysis exists as a non-shipped .planning/ verification artifact that produces an overall FAIL | VERIFIED | 03-weak-sample.md exists at 325 lines; contains all 6 section headings, 3 named injections, 6 verdict blocks, Overall Verdict = FAIL fired by the gate (Criterion 2 = Absent) |
| 7 | Applying the authored rubric to the weak sample produces an overall fail with per-criterion evidence-quoting verdicts | VERIFIED | Criterion 2 scores Absent (every Type cell reads "general assumption"), gate fires, FAIL correctly stated; verdict blocks all contain quoted spans or gap citations matching rubric format |

**Score:** 5/7 truths verified (2 blockers: CR-01 contradictory Pass definition, CR-02 dangling D-01/D-08 references)

### Deferred Items

None. No gaps are addressed by later phases — both failures are defects in the shipped rubric that affect it as-is.

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `first-principles-thinking/references/validation-rubric.md` | Full analytic rubric replacing stub | VERIFIED (with defects) | 285 lines, no YAML frontmatter, opens with `# Validation Rubric` H1, block-quote scope note, correct structure — but contains CR-01 and CR-02 defects |
| `.planning/phases/03-validation-rubric/03-weak-sample.md` | Deliberately-weak analysis + rubric scoring run | VERIFIED | 325 lines, non-shipped .planning/ artifact, six-section format, three injections, 6 verdict blocks, FAIL verdict |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `first-principles-thinking/references/validation-rubric.md` | `first-principles-thinking/SKILL.md` | Link in "Before presenting conclusions" section | VERIFIED | SKILL.md line 151 contains `[references/validation-rubric.md](references/validation-rubric.md)` |
| `03-weak-sample.md` scoring run | `validation-rubric.md` | 6 `### Criterion N` blocks applying the rubric | VERIFIED | All 6 verdict blocks present; band vocabulary matches rubric (Rigorous/Sound/Hand-wavy/Absent); format matches prescribed structure |
| `validation-rubric.md criterion descriptors` | `output-template.md` section structure | Descriptors observable against 6-section output format | VERIFIED | Criterion descriptors reference GT-IDs, GT-N? suffix, Assumptions Table columns, derivation chain format, Conclusion section — all observable against output-template.md |

### Data-Flow Trace (Level 4)

Not applicable. This is a pure-Markdown skill with no runtime, no state, no data fetching. "Data flow" is the conceptual chain from rubric descriptors to the weak-sample scoring run. That chain is verified under Key Links above.

### Behavioral Spot-Checks

Step 7b: SKIPPED — no runnable entry points. This is a pure-Markdown skill. The equivalent behavioral check is the scoring-run in 03-weak-sample.md, which constitutes a manual execution of the rubric against a known-weak input.

**Manual spot-check — the rubric actually catches the injected failures:**

| Injection | Criterion | Expected band | Actual band | Status |
|-----------|-----------|---------------|-------------|--------|
| Flattened derivation chains (no intermediate step) | 4: Reason Upward | Hand-wavy | Hand-wavy | PASS |
| Stripped four-type classification (all Type cells = "general assumption") | 2: Challenge Assumptions | Absent | Absent | PASS |
| Generic escape-valve in Abandoned Reasoning | 4: Reason Upward (folded) | Hand-wavy | Hand-wavy (folded into same C4 verdict) | PASS |
| Gate fires on Criterion 2 Absent | Overall | FAIL | FAIL | PASS |

The rubric produced the right verdict. The phase goal — "demonstrably catches hand-waving rather than certifying it" — is satisfied by the weak-sample run.

**Important nuance from 03-02-SUMMARY.md deviation:** The plan predicted Criterion 4 would score Absent; honest application of the rubric scored it Hand-wavy (chains are present but flattened; the Absent descriptor requires chains to be fully missing). The deviation strengthens confidence in the rubric's precision — it does not overfire.

### Probe Execution

Step 7c: SKIPPED — no probe scripts exist or are applicable. This is a pure-Markdown phase with no `scripts/tests/probe-*.sh` files.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| VALID-01 | 03-01-PLAN.md | `validation-rubric.md` defines 6-8 analytic criteria covering the 5 phases and traceability | SATISFIED | Exactly 6 criteria verified; covers Identify Essence, Challenge Assumptions, Establish Ground Truths, Reason Upward, Validate, Conclusion-to-GT Traceability |
| VALID-02 | 03-01-PLAN.md | Each rubric criterion has 3-4 named levels, each with a concrete observable descriptor | SATISFIED | 4 levels per criterion (Rigorous/Sound/Hand-wavy/Absent); descriptors are structural and countable; adjective-test passes |
| VALID-03 | 03-01-PLAN.md, 03-02-PLAN.md | The rubric uses a gate scoring model — any criterion at the lowest band fails the analysis and forces revision | SATISFIED (with noted defect) | Gate correctly defined (lines 51-53); demonstrated in weak-sample FAIL. The CR-01 contradiction in the Pass: line (line 60) weakens the Scoring Model section but does not negate the gate itself, which is clearly stated in two locations. |
| VALID-04 | 03-01-PLAN.md, 03-02-PLAN.md | The rubric requires Claude to quote the specific span of its analysis that satisfies or fails each criterion | SATISFIED | Verdict Block Format section (lines 64-97) prescribes quoted-span and gap-citation forms; demonstrated in weak-sample verdict blocks |
| VALID-05 | Not in Phase 3 | `SKILL.md` instructs Claude to apply the rubric as a validator → fix → repeat feedback loop | OUT OF SCOPE | REQUIREMENTS.md maps VALID-05 to Phase 2; SKILL.md already links to validation-rubric.md — this requirement is Phase 2's responsibility |

**Orphaned requirements check:** REQUIREMENTS.md maps VALID-01, VALID-02, VALID-03, VALID-04 to Phase 3. VALID-05 is mapped to Phase 2. No Phase 3 requirements are orphaned.

**REQUIREMENTS.md checkbox status note:** VALID-01 and VALID-02 remain unchecked (`[ ]`) in REQUIREMENTS.md despite being satisfied by the authored rubric. This is a tracking discrepancy in the requirements file, not a defect in the delivered artifact. Both are substantively met.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `first-principles-thinking/references/validation-rubric.md` | 60 | Self-contradictory Pass: definition — "Every criterion scores Sound or above, with at most one criterion at Hand-wavy" | BLOCKER | Makes the rubric's central output (pass/fail) undefined for the one-Hand-wavy case; a reviewer cannot reliably apply it |
| `first-principles-thinking/references/validation-rubric.md` | 139, 195-196 | Dangling design-decision references: D-01 and D-08 cited as authority; neither defined in any shipped file | BLOCKER | A reviewer following these citations reaches no target; the rubric claims auditability while containing unresolvable references |
| `first-principles-thinking/references/validation-rubric.md` | 100-106 | `## Criteria` (H2) followed by `## Criterion N` (also H2) — criteria are siblings of their intro section, not children | WARNING | Document outline renders "Criteria" as an empty section; no functional impact on rubric application |
| `first-principles-thinking/references/validation-rubric.md` | 246-249 | Criterion 5 Absent third clause overlaps with first clause | WARNING | Ambiguous which clause to cite in required Justification; weakens auditability for this criterion |
| `first-principles-thinking/references/validation-rubric.md` | 232, 247 | "load-bearing chain" used as a scoring term but never defined | WARNING | Makes Criterion 5 scoring subjective at the point where precision is most needed |
| `first-principles-thinking/references/validation-rubric.md` | 111-275 | Escape-valve scoring undefined for Criteria 2, 3, 5, 6 | WARNING | Reviewers encounter `Nothing material here` in these sections with no rubric guidance; inconsistent verdicts across reviewers |

**Debt marker check:** No TBD, FIXME, XXX, or TODO markers found in any modified file.

### Human Verification Required

No items require human verification. This is a pure-Markdown artifact; all structural properties are programmatically verifiable. The weak-sample scoring run constitutes the behavioral demonstration.

## Gaps Summary

Two BLOCKER defects prevent the phase goal from being fully achieved as a shipped, usable instrument:

**Blocker 1 — CR-01: Contradictory Pass definition (validation-rubric.md line 60)**

The "How to Apply This Rubric" section correctly defines the pass condition. The Scoring Model's summary Pass: line contradicts it by writing a clause that excludes the band it then permits. A reviewer applying the rubric to an analysis with exactly one Hand-wavy criterion cannot determine whether it passes from the Scoring Model section alone — they must resolve a contradiction. This makes the rubric's central function (pass/fail determination) unreliable for a common scoring outcome.

Fix: `**Pass:** No criterion scores Absent, and at most one criterion scores Hand-wavy.` (This matches lines 18-19 and the stated gate + cap rules.)

**Blocker 2 — CR-02: Dangling D-01 and D-08 references (lines 139, 195-196)**

Criterion 2 cites "D-01" and Criterion 4 cites "D-01" and "D-08" as the authority for what they fold in. These identifiers exist only in 03-CONTEXT.md — an internal, non-shipped planning document. No shipped file defines D-01 or D-08. SKILL.md and output-template.md use D-07 (unverified-flag/GT-N? discipline) and D-03 (Abandoned Reasoning / escape-valve rule) for the behaviors the rubric attributes to D-01 and D-08 respectively. A user following the rubric's citations will reach no target and cannot verify the authority being claimed.

Fix: Replace D-01 with D-07 and D-08 with D-03 (the shipped IDs for the same behaviors), or remove the ID citations and leave the fold-in descriptions as plain prose.

**Effect on phase goal:** The rubric's core function — catching hand-waving — is demonstrated by the weak-sample FAIL (5 of 7 truths verified, including the falsification demonstration). The two blockers affect the rubric's reliability and auditability as a precise instrument, not its basic structure. They are correctness defects that a motivated reviewer would trip on in the one-Hand-wavy edge case (CR-01) and when following citations (CR-02). The phase goal is partially achieved; the rubric needs two targeted fixes before it is fully operative.

---

_Verified: 2026-05-17T12:00:00Z_
_Verifier: Claude (gsd-verifier)_
