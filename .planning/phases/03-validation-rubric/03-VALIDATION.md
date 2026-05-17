---
phase: 3
slug: validation-rubric
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-16
---

# Phase 3 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | none — pure-Markdown skill, no executable code (PROJECT.md v1 constraint) |
| **Config file** | none |
| **Quick run command** | none — verification is behavioral (apply the rubric, observe the verdict) |
| **Full suite command** | none |
| **Estimated runtime** | n/a |

This phase produces Markdown content, not code. Formal test infrastructure
(pytest/jest/etc.) does not apply. Validation is **behavioral**: apply the
authored rubric to the deliberately-weak sample analysis and verify it
produces a fail with per-criterion evidence-quoting verdicts.

---

## Sampling Rate

- **After every task commit:** Re-read the modified Markdown file; confirm the
  task's `<acceptance_criteria>` source assertions hold (criterion count,
  level count, observable-descriptor wording).
- **After the rubric is authored:** Apply it to `03-weak-sample.md` and confirm
  the gate fires.
- **Before `/gsd:verify-work`:** The weak-sample fail run must be complete and
  every Success Criterion observable.
- **Max feedback latency:** immediate (manual inspection of Markdown).

---

## Per-Task Verification Map

Task IDs are assigned by the planner. The requirement-level validation map
below is the contract every plan must satisfy.

| Req ID | Wave | Behavior | Test Type | Verification |
|--------|------|----------|-----------|--------------|
| VALID-01 | — | `validation-rubric.md` defines exactly 6 analytic criteria covering the 5 phases + conclusion-to-ground-truth traceability | Manual count | Count criteria headings in the shipped file = 6; each maps to a named phase or traceability |
| VALID-02 | — | Each criterion has 4 named levels, each with a concrete observable descriptor (no adjectives) | Manual audit | Apply the adjective-test to every level descriptor — remainder must still be verifiable |
| VALID-03 | — | Gate model: any criterion scored at the lowest band fails the whole analysis and forces revision; hand-wavy cap (2/6 at second-lowest) also fails | Manual scoring | Score the weak sample; verify any lowest-band criterion produces a fail verdict |
| VALID-04 | — | Evidence-quoting: each verdict block contains a quoted span (or explicit gap citation), the band, and a one-line justification | Manual scoring | Apply the rubric to the weak sample; verify every verdict block has the required parts |
| SC-4 | — | Applying the rubric to the deliberately-weak sample produces a fail, each verdict quoting the specific span | Behavioral | Apply the rubric to `.planning/phases/03-validation-rubric/03-weak-sample.md`; verify ≥2 criteria fail with named, quoted spans |

*Status tracked per-task once the planner assigns task IDs.*

---

## Wave 0 Requirements

*None — this phase creates new Markdown files; no test infrastructure is needed.*
Existing project structure covers all phase requirements.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Criterion count, level count, observable-descriptor wording | VALID-01, VALID-02 | Markdown content audit — no executable assertion possible | Read `references/validation-rubric.md`; count criteria (=6) and levels per criterion (=4); apply the adjective-test to each descriptor |
| Gate + hand-wavy cap fire correctly | VALID-03 | The gate is a scoring rule applied by the model | Apply the rubric to `03-weak-sample.md`; confirm a lowest-band score and/or 2 second-lowest scores produce an overall fail |
| Weak-sample fail run with quoted spans | VALID-04, SC-4 | Behavioral demonstration, not an automatable test | Run the rubric against `03-weak-sample.md`; confirm each verdict block quotes the analysis span (or cites the gap) it scores |

*All Phase 3 verification is manual by nature — the deliverable is a Markdown
rubric and its fail demonstration, not code.*

---

## Validation Sign-Off

- [ ] Every task has `<acceptance_criteria>` with source/behavior assertions on the Markdown
- [ ] The weak-sample fail run is authored and demonstrably produces a fail
- [ ] All 4 Success Criteria are observable in the shipped rubric + weak-sample artifact
- [ ] No executable code introduced (pure-Markdown v1 constraint honored)
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
