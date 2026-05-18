---
phase: 5
slug: domain-spread-worked-examples
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-17
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | none — pure-Markdown content phase, no executable code |
| **Config file** | none |
| **Quick run command** | none — validation is manual rubric application |
| **Full suite command** | none — validation is manual rubric application |
| **Estimated runtime** | n/a |

---

## Sampling Rate

- **After every task commit:** Re-read the just-authored example section against `references/output-template.md` (correct section present, in order).
- **After every plan wave:** Score each completed example file against all 6 criteria in `references/validation-rubric.md`.
- **Before `/gsd:verify-work`:** All four example files must clear the rubric gate (no criterion Absent; at most one Hand-wavy).
- **Max feedback latency:** n/a (synchronous review)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 05-01-* | 01 | 1 | EX-01 | — | N/A | manual rubric | none — apply `validation-rubric.md` to `examples/software-systems.md` | ✅ stub exists | ⬜ pending |
| 05-02-* | 02 | 1 | EX-02 | — | N/A | manual rubric | none — apply `validation-rubric.md` to `examples/product-business.md` | ✅ stub exists | ⬜ pending |
| 05-03-* | 03 | 1 | EX-03 | — | N/A | manual rubric | none — apply `validation-rubric.md` to `examples/personal-general.md` | ✅ stub exists | ⬜ pending |
| 05-04-* | 04 | 1 | EX-04 | — | N/A | manual rubric | none — apply `validation-rubric.md` to `examples/science-engineering.md` | ✅ stub exists | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements.* The four `examples/*.md` stub files already exist; `references/output-template.md` and `references/validation-rubric.md` are the authoring contract and the validator. No framework install, no test scaffolding.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Example follows the six-section output format | EX-01..EX-04 | No executable code; format conformance is a document-structure review | Open the example file; confirm all six sections from `output-template.md` are present in fixed order |
| Example shows ≥1 abandoned/dead-end reasoning step | EX-01..EX-04 | Semantic judgement, not machine-checkable | Confirm the Abandoned Reasoning section records a genuine dead-end the analysis nearly took |
| Example clears the validation rubric gate | EX-01..EX-04 | Rubric is applied by human or model review, not a command | Apply all 6 criteria in `references/validation-rubric.md`; gate clears = no Absent, ≤1 Hand-wavy |
| The four examples are structurally distinct (not one skeleton with nouns swapped) | EX-01..EX-04 | Cross-file comparison, judgement-based | Compare deepest sections, chain counts, and dead-end depth across all four per CONTEXT.md D-03 |

---

## Validation Sign-Off

- [ ] Each example file conforms to `references/output-template.md` (six sections, fixed order)
- [ ] Each example records ≥1 genuine abandoned reasoning step
- [ ] Each example clears the `references/validation-rubric.md` gate (no Absent, ≤1 Hand-wavy)
- [ ] The four examples are structurally distinct per CONTEXT.md D-03
- [ ] `nyquist_compliant: true` set in frontmatter once all four pass

**Approval:** pending
