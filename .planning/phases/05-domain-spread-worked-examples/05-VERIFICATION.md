---
phase: 05-domain-spread-worked-examples
verified: 2026-05-17T00:00:00Z
status: gaps_found
score: 2/4 truths fully verified — truths 1 and 2 pass; truths 3 (rubric gate) and 4 (structural variety) have open gaps reported by human verification
overrides_applied: 0
gaps:
  - id: GAP-01
    truth: 3
    title: "Rubric-rigor defects in the worked examples"
    summary: "Human review of the rubric gate found content-rigor defects that drop affected criteria below Rigorous. Resolve so every criterion verifiably scores Sound or above with no Absent and at most one Hand-wavy per file."
    detail: "Concrete defects from 05-REVIEW.md: WR-03 — software-systems.md Conclusion A chain header declares inputs GT-1 + GT-2 but the conclusion relies on the unnamed GT-3 (2-deploys/day ceiling); the chain must name every GT it uses. WR-04 — software-systems.md Section 6 introduces new reasoning (specific time estimates, a pipeline-stage taxonomy) absent from any chain, violating the synthesis-only rule for the Conclusion section. WR-05 — product-business.md cites a named/numbered 'Phase 4 no-analogies-as-direct-evidence rule' that SKILL.md does not name or number; the example must not invent authoritative terminology. WR-06 — science-engineering.md panel-sizing chain applies only the 0.80 derating factor (scoped by GT-2 to temperature/wiring/MPPT/inverter losses) and omits battery round-trip efficiency, despite nearly all energy flowing through the battery in a 3-day-autonomy system — incomplete loss accounting against the example's own 'no number without an antecedent' criterion."
  - id: GAP-02
    truth: 4
    title: "Cross-example inconsistency undermines the calibration set"
    summary: "Human review of the structural-variety check found the four examples are internally inconsistent in ways that weaken their role as a calibration set teaching one consistent output format."
    detail: "Concrete defects from 05-REVIEW.md: WR-01 / WR-02 — software-systems.md uses lettered 'Conclusion A/B/C' labels while product-business.md, personal-general.md and science-engineering.md use unlabelled '### Conclusion:'. Standardise the Conclusion labelling across all four files. The lettered scheme also blurs the template's one-chain-per-conclusion rule, since A/B/C are intermediate findings feeding a single synthesised recommendation — reconcile against the template. Then confirm the depth-of-emphasis variety remains genuine after the fix."
  - id: GAP-03
    truth: 3
    title: "Remaining code review advisory items"
    summary: "Resolve the Info-level findings from 05-REVIEW.md so the worked-example set is internally clean and consistent."
    detail: "Address the 7 Info findings in 05-REVIEW.md: preamble inconsistency across the four files, the unused 'Nothing material here' escape valve (no example demonstrates it), and the absolute 'no architectural change is needed' phrasing in software-systems.md that reads in tension with its own later schema-decomposition recommendation. Reviewer's full report: 05-REVIEW.md."
human_verification:
  - test: "Confirm each example passes the validation rubric gate (no criterion Absent, at most one Hand-wavy)"
    expected: "All six criteria score Sound or above for each of the four files; no example has two or more criteria at Hand-wavy"
    why_human: "Rubric scoring requires reading and evaluating the quality of prose, reasoning chains, and the specificity of abandonment reasons — grep cannot distinguish Rigorous from Sound or Hand-wavy"
  - test: "Confirm the four examples are structurally distinct (not the same skeleton with domain nouns swapped)"
    expected: "EX-01 centerpiece is Problem Essence (symptom→cause) + two dead-ends; EX-02 centerpiece is the dense Assumptions Table; EX-03 centerpiece is Problem Essence (stated-goal→real-goal) with MEDIUM conclusion; EX-04 centerpiece is quantitative Ground Truths + Derivation Chains with GT-5? and MEDIUM confidence chains"
    why_human: "Structural distinctiveness is a qualitative judgment about depth and emphasis, not a binary presence/absence check"
---

# Phase 5: Domain-Spread Worked Examples Verification Report

**Phase Goal:** Four worked examples exist in `examples/`, one per domain, each applying the methodology in the standardized output format, each exercising the method differently, and each showing at least one abandoned or dead-end reasoning step.
**Verified:** 2026-05-17
**Status:** gaps_found
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | `examples/` contains four worked examples covering software/systems, product/business, personal/general, and science/engineering, each following the standardized six-section output format | VERIFIED | All four files exist at the expected paths; all have exactly six `##` sections in the prescribed order (1. Problem Essence through 6. Conclusion) confirmed by grep; each file has exactly one H1 verbatim heading |
| 2 | Each example shows at least one abandoned or dead-end reasoning step (not a clean march to the answer) | VERIFIED | EX-01 has 2 dead-ends (`### Dead End:` × 2); EX-02, EX-03, EX-04 each have exactly 1 dead-end; all use the What-was-tried / Why-abandoned / What-it-ruled-out structure |
| 3 | Each example, when scored against the validation rubric, passes the gate (no criterion at the lowest band) | UNCERTAIN — needs human | SUMMARYs record all six criteria Rigorous for all four examples; files contain no rubric verdict blocks (correct per D-07); structural checks confirm no section is empty or stub-level; but rubric scoring at Rigorous vs Sound vs Hand-wavy is a qualitative judgment that cannot be verified by grep alone |
| 4 | The four examples differ in structure and methodology emphasis — no two are the same skeleton with domain nouns swapped | VERIFIED (automated) / UNCERTAIN (qualitative) | Structurally measurable differences: EX-01 has 2 dead-ends (unique), EX-04 has GT-5? notation (unique), EX-03 has MEDIUM confidence conclusion (unique), EX-04 has quantitative unit-arithmetic chains (unique), EX-02 has a 7-row Assumptions Table as the densest section; whether these differences constitute sufficient depth-of-emphasis variation is a qualitative judgment |

**Score:** 4/4 truths verified at the structural/automated level. Two truths have qualitative components requiring human confirmation.

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `first-principles-thinking/examples/software-systems.md` | EX-01 software/systems worked example — six-section analysis | VERIFIED | 314 lines; H1 matches spec verbatim; six sections in order; 5 GTs with citations; 3 chains; 2 dead-ends; no GT-N? suffix; no rubric blocks; HIGH confidence on all chains |
| `first-principles-thinking/examples/product-business.md` | EX-02 product/business worked example — six-section analysis | VERIFIED | H1 matches spec verbatim; six sections in order; 7-row Assumptions Table (9 rows including header/separator); 4 GTs with citations; 3 chains; 1 dead-end; no GT-N? suffix; no rubric blocks; HIGH confidence |
| `first-principles-thinking/examples/personal-general.md` | EX-03 personal/general worked example — six-section analysis | VERIFIED | H1 matches spec verbatim; six sections in order; 5 GTs with citations; 2 chains; 1 dead-end; no GT-N? suffix; no rubric blocks; MEDIUM confidence on Chain 2 and Conclusion (correct per plan) |
| `first-principles-thinking/examples/science-engineering.md` | EX-04 science/engineering worked example — six-section analysis | VERIFIED | H1 matches spec verbatim; six sections in order; GT-5? present with literal `?` suffix; per-appliance load breakdown table in Section 3; 2 quantitative chains both consuming GT-5?; both chains end MEDIUM confidence naming GT-5? and verification path; 1 dead-end; no rubric blocks; no HIGH confidence on GT-5?-consuming chains |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| EX-01 section 4 chains | EX-01 section 3 Ground Truths | GT-1 through GT-5 referenced by name in every chain | VERIFIED | All three chains (A, B, C) name GT-IDs matching the five GTs defined in section 3 |
| EX-01 section 6 Conclusion | EX-01 section 4 chains | Every Conclusion claim traces to a named chain | VERIFIED | Section 6 references GT-1, GT-2, GT-3, GT-4 explicitly; three-step intervention maps to chains A/B/C |
| EX-02 section 4 chains | EX-02 section 3 Ground Truths | GT-1 through GT-4 referenced in every chain | VERIFIED | Three chains all name GT-IDs matching the four GTs in section 3; GT-4 (verified gap) is used correctly without GT-N? suffix |
| EX-02 section 6 Conclusion | EX-02 section 4 chains | Conclusion traces to named chains | VERIFIED | Pilot recommendation traces to Chain 2; threshold pre-specification traces to Chain 3; key insight references dead-end + Chain 1 |
| EX-03 section 4 chains | EX-03 section 3 Ground Truths | GT-1 through GT-5 referenced in both chains | VERIFIED | Chain 1 uses GT-1 + GT-2 + GT-3; Chain 2 uses GT-4 + GT-5; all GT-IDs match section 3 definitions |
| EX-03 section 6 Conclusion | EX-03 section 4 chains | Three conditions in recommended approach trace to Chain 2 | VERIFIED | $18K effective differential from Chain 1 appears in Trade-offs; three decision conditions are the Chain 2 intermediate claims |
| EX-04 section 4 chains | EX-04 section 3 Ground Truths | GT-1 through GT-5? referenced in both chains | VERIFIED | Panel chain: GT-2 + GT-5? + GT-1; Battery chain: GT-5? + GT-4 + GT-3; all IDs match section 3 |
| EX-04 section 6 Conclusion | EX-04 section 4 chains | Section 6 names all five GT-IDs (GT-1 through GT-5?) explicitly | VERIFIED | "These sizes are derived from the site's 5.5 PSH annual average (GT-1), the 0.80 system derating factor (GT-2), the 80% DoD limit of LiFePO4 chemistry (GT-3), the 3-day autonomy target (GT-4), and the estimated 1.5 kWh/day daily load (GT-5?)." |

### Behavioral Spot-Checks

Step 7b: SKIPPED — pure-Markdown skill content with no runnable entry points.

### Probe Execution

Step 7c: SKIPPED — no probe scripts exist or are declared for this phase.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|---------|
| EX-01 | 05-01-PLAN.md | `examples/` contains a software/systems worked example that follows the output format and shows at least one abandoned reasoning step | SATISFIED | `software-systems.md` exists with six sections, 2 dead-ends, specific scenario content |
| EX-02 | 05-02-PLAN.md | `examples/` contains a product/business worked example that follows the output format and shows a dead-end | SATISFIED | `product-business.md` exists with six sections, 1 dead-end (competitor-parity analogy), dense Assumptions Table |
| EX-03 | 05-03-PLAN.md | `examples/` contains a personal/general worked example that follows the output format and shows a dead-end | SATISFIED | `personal-general.md` exists with six sections, 1 dead-end (pure-compensation framing), MEDIUM-confidence conclusion |
| EX-04 | 05-04-PLAN.md | `examples/` contains a science/engineering worked example that follows the output format and shows a dead-end | SATISFIED | `science-engineering.md` exists with six sections, 1 dead-end (peak-load sizing), GT-5? notation, MEDIUM-confidence chains |

Note: REQUIREMENTS.md shows EX-01 through EX-04 as "Pending" (not marked Complete). This is expected — the REQUIREMENTS.md traceability table is updated during Phase 6 packaging. The deliverables exist; the tracking status is a Phase 6 concern.

### Anti-Patterns Found

| File | Pattern | Severity | Impact |
|------|---------|----------|--------|
| (none found) | — | — | — |

No TBD, FIXME, XXX, placeholder, or stub patterns found in any of the four example files. No empty implementations, no hardcoded empty data.

### Structural Distinctiveness Evidence

The four examples are verifiably distinct at the structural/mechanical level:

| Property | EX-01 | EX-02 | EX-03 | EX-04 |
|----------|-------|-------|-------|-------|
| Dead-ends | 2 (unique) | 1 | 1 | 1 |
| GT-N? notation | absent | absent | absent | present (unique) |
| Conclusion confidence | HIGH | HIGH | MEDIUM (unique) | MEDIUM (unique) |
| Derivation chains | 3 | 3 | 2 (unique) | 2 (unique) |
| Assumption rows | 5 | 7 (densest) | 5 | 8 |
| Phase 1 re-framing type | symptom→cause | economics question | stated-goal→real-goal | sizing question |
| Quantitative arithmetic | none | none | compensation delta | unit-conversion chains (unique) |

Whether these differences constitute sufficient depth-of-emphasis variation beyond mechanical metrics is a qualitative judgment requiring human review.

### Human Verification Required

#### 1. Rubric Gate Confirmation (EX-01 through EX-04)

**Test:** Apply the six criteria from `first-principles-thinking/references/validation-rubric.md` to each of the four example files and confirm no criterion scores Absent, and at most one criterion scores Hand-wavy per file.

**Expected:** All criteria score Sound or Rigorous on every file. Gate cleared (no Absent). Hand-wavy cap cleared (0 or 1 Hand-wavy per file).

**Why human:** Rubric scoring requires evaluating the quality and specificity of prose content. The boundary between Rigorous, Sound, and Hand-wavy cannot be determined by structural presence checks alone — it requires reading and judging whether entries are "specific to this analysis" (Rigorous), "generic or vague" (Sound/Hand-wavy), or "missing" (Absent). Grep can confirm sections exist and are populated; it cannot assess whether the content meets the Rigorous descriptor.

Key areas to focus on for each file:
- EX-01, Criterion 4 (Reason Upward): whether the second dead-end ("Move the test suite to a faster test runner") gives a genuinely specific abandonment reason or a generic one
- EX-03, Criterion 5 (Validate): whether the MEDIUM confidence from conditional reasoning (not from GT-N?) satisfies the rubric's confidence-caveat requirement
- EX-02, Criterion 3 (Ground Truths): whether GT-4 (a verified absence / data gap) correctly avoids needing GT-N? notation — confirmed correct by plan D-04, but worth human review
- EX-04, Criterion 4 (Reason Upward): whether the quantitative intermediate steps are genuine intermediates (claims not statable from any single GT alone) — the files show the intermediate computation explicitly labeled as such

#### 2. Structural Variety Depth Check

**Test:** Read all four examples and confirm the depth-of-emphasis differences are substantive — that EX-01's Problem Essence is genuinely deeper/longer than EX-02/03/04's, EX-02's Assumptions Table is genuinely the densest section, EX-03's Phase 1 re-framing is qualitatively distinct from EX-01's despite both emphasizing Phase 1, and EX-04's Derivation Chains contain genuinely substantive unit arithmetic.

**Expected:** Each example's designated "deepest section" is visibly more developed than the same section in the other three examples.

**Why human:** Depth and emphasis are qualitative properties. Mechanical line counts (EX-01 is 314 lines, EX-04 is ~190 lines) can indicate relative weight but do not confirm that the right sections carry the emphasis. A reader must confirm that the variety is genuine rather than superficial.

---

## Gaps Summary

Structural and automated checks pass (truths 1 and 2 fully verified). Human verification of the two qualitative items reported issues, so truths 3 and 4 carry open gaps. Status is `gaps_found`.

| Gap | Truth | What's missing |
|-----|-------|----------------|
| GAP-01 | 3 | Rubric-rigor defects: undeclared ground truth in a chain header (WR-03), Section 6 synthesis-only violation (WR-04), invented "Phase 4 rule" terminology (WR-05), incomplete loss accounting in the solar panel chain (WR-06). |
| GAP-02 | 4 | Cross-example inconsistency: lettered vs unlabelled Conclusion headings across the four files (WR-01/WR-02), which also blurs the one-chain-per-conclusion rule. |
| GAP-03 | 3 | Remaining advisory items: preamble inconsistency, undemonstrated escape valve, and an over-absolute phrasing in software-systems.md (the 7 Info findings in 05-REVIEW.md). |

See the `gaps:` frontmatter block above for full per-gap detail. Close via `/gsd:plan-phase 5 --gaps` → `/gsd:execute-phase 5 --gaps-only`, then this verification re-runs.

---

_Verified: 2026-05-17_
_Verifier: Claude (gsd-verifier)_
