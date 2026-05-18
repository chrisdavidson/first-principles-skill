---
phase: 05-domain-spread-worked-examples
plan: "02"
subsystem: examples
tags: [worked-example, product-business, assumptions-table, analogy-ban]
dependency_graph:
  requires: [first-principles-thinking/references/output-template.md, first-principles-thinking/references/validation-rubric.md, first-principles-thinking/SKILL.md]
  provides: [EX-02]
  affects: [first-principles-thinking/examples/product-business.md]
tech_stack:
  added: []
  patterns: [six-section-output-format, classified-assumptions-table, no-analogies-as-direct-evidence]
key_files:
  created: [first-principles-thinking/examples/product-business.md]
  modified: []
decisions:
  - "D-03: Section 2 (Assumptions Table) is the deepest section — 7 rows carrying the analysis"
  - "D-04: No GT-N? suffix used — EX-02 has no genuine unverifiable input; GT-4 is a verified absence"
  - "D-07: Rubric scoring recorded in SUMMARY only, not embedded in the example file"
  - "Conclusion confidence is HIGH because the pilot recommendation follows from the verified data gap; no chain depends on an unverified GT-N? input"
metrics:
  duration: "3 minutes"
  completed: "2026-05-18T03:15:51Z"
  tasks: 2
  files: 1
---

# Phase 05 Plan 02: EX-02 Product/Business Worked Example Summary

## One-Liner

Six-section first-principles analysis of the SaaS free-tier adoption question, with a 7-row Classified Assumptions Table as the centerpiece and the competitor-parity analogy as the documented dead end.

## What Was Built

`first-principles-thinking/examples/product-business.md` — a complete first-principles analysis of the locked EX-02 problem: "Should a SaaS product add a free tier to grow adoption?" Scenario: a 3-year-old B2B SaaS project-management tool, $2.4M ARR, 240 paying teams at approximately $10K/year, primarily outbound sales acquisition, no existing free tier.

The file follows the strict six-section output format from `references/output-template.md`:

1. **Problem Essence** — re-frames the question from "add a free tier?" to "does this product's economics support one?", with four checkable success criteria.
2. **Assumptions Table** — 7 rows; the competitor-parity row is classified as `convention` with Verdict: Discard (analogy-as-evidence); two rows carry "unverified — flagged"; no assumption type is outside the four-type scheme.
3. **Ground Truths** — GT-1 through GT-4 with specific source citations; GT-4 is the verified absence of conversion data (not a GT-N? — it is a known gap, not an unverified belief used in a chain).
4. **Derivation Chains** — 3 chains, each with a genuine intermediate step; all rated HIGH confidence; no GT-N? input consumed anywhere.
5. **Abandoned Reasoning** — 1 dead end: competitor-parity analogy abandoned because it is an analogy-as-evidence move with no named GT grounding competitor economics.
6. **Conclusion** — pilot-first recommendation with pre-specified threshold; key insight that "competitors do it" fails the no-analogies rule; trade-offs acknowledged; all claims trace to named chains.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Author EX-02 six-section analysis | b1f5b90 | first-principles-thinking/examples/product-business.md |
| 2 | Score EX-02 against validation rubric | (in this SUMMARY) | — |

## Rubric Scoring (Task 2 — Scratch Check)

Applied all 6 criteria from `references/validation-rubric.md` to `product-business.md`. No inline verdict blocks appear in the example file (D-07).

**Criterion 1: Identify Essence**
Quoted span: "Does this B2B SaaS product's own economics support adding a free tier, or is the case for one resting entirely on unverified beliefs and competitor analogy?"
Band: **Rigorous**
Justification: The Essence Statement names the core question (economics vs. unverified beliefs), not the triggering event ("add a free tier"); the four success criteria are checkable conditions a reader can verify against the final conclusion without asking for clarification.

**Criterion 2: Challenge Assumptions**
Quoted span: "| All our competitors have a free tier, so we need one | convention | Explicitly challenge before use... | Discard | Analogy-as-evidence move. Competitor adoption of a pricing model is not evidence that the same model is economically viable for this product in this ICP segment at this ARR stage."
Band: **Rigorous**
Justification: All 7 rows use Types drawn from the four-type scheme (no freeform labels), Treatments use the prescribed vocabulary for each type, Verdicts use Accept/Challenge/Discard, two rows carry "unverified — flagged" notation, and the competitor-parity assumption is explicitly challenged and discarded with a specific structural reason.

**Criterion 3: Establish Ground Truths**
Quoted span: "**GT-4** The free-to-paid conversion rate for this product in this ICP segment is unknown and has not been measured; no historical pilot or freemium experiment has been run. — source: verified gap (product and sales teams confirm no conversion data exists)"
Band: **Rigorous**
Justification: GT-1 through GT-4 carry stable IDs used consistently throughout the document, every entry has a source citation more specific than "common knowledge," no discarded assumptions appear in the list, and GT-4 correctly represents a verified absence without the GT-N? suffix (which is correct per D-04: the gap is known, not an unverified belief used in a chain).

**Criterion 4: Reason Upward**
Quoted span: "GT-1 (240 teams at $10K/year average contract; outbound acquisition model) + GT-4 (conversion rate unknown and unverified) → At $10K/year average contract, even a modest conversion rate (1–2%) on a free-tier cohort could justify the investment; but at near-zero conversion the free tier generates support and infrastructure cost with no revenue offset — the outcome is highly sensitive to a variable that has never been measured for this product → Deciding to add or reject a free tier without conversion data is a decision under ignorance, not a decision under uncertainty"
Band: **Rigorous**
Justification: All three chains name GT-IDs and contain a genuine intermediate claim statable from neither GT alone; the dead end documents the competitor-parity argument with specific structural abandonment reason (analogy-as-evidence move, no named GT grounding competitor economics); no analogy is used as direct evidence in any live chain.

**Criterion 5: Validate**
Quoted span: "**Confidence:** HIGH" (repeated for all three chains and the Conclusion)
Band: **Rigorous**
Justification: All chains are explicitly rated HIGH confidence, which is correct since no GT-N? input appears in any chain; the Conclusion confidence (HIGH) matches the weakest contributing chain (all HIGH); no chain that would require a caveat exists.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "The free-tier question is an empirical question about this product's conversion economics, not a convention the product team is obligated to follow. An outbound-led SaaS product with $10K/year average contracts and no existing self-serve channel is structurally different from the consumer tools and developer utilities where free-tier models consistently generate positive unit economics."
Band: **Rigorous**
Justification: Every Conclusion claim traces to a named chain (Recommended approach to Chain 2, Key Insight to dead end + Chain 1, Trade-offs to Chain 3); no new claims are introduced in the Conclusion; the Key Insight is a non-obvious structural finding that reasoning by analogy would have missed.

**Gate result:** No criterion Absent. Hand-wavy cap: zero criteria Hand-wavy. **All six criteria: Rigorous. Gate cleared.**

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

None — all sections contain live analysis; no placeholder text or hardcoded empty values.

## Threat Flags

None — static Markdown file with no executable code, no user input, no network surface, no secrets.

## Self-Check

Files created:
- `first-principles-thinking/examples/product-business.md` — present

Commits:
- `b1f5b90` — feat(05-02): author EX-02 product/business worked example (SaaS free tier)

## Self-Check: PASSED
