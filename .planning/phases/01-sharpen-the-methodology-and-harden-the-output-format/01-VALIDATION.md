---
phase: 1
slug: sharpen-the-methodology-and-harden-the-output-format
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-16
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

This is a **pure-Markdown content-authoring phase** — there is no executable code
and no automated test runner applies. Validation is structured manual inspection
of authored Markdown against the 6 requirements and 5 success criteria, plus a
dogfooding run of the methodology itself as the phase gate.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Manual verification against success criteria (no automated test framework — pure-Markdown content authoring) |
| **Config file** | none |
| **Quick run command** | Re-read the authored file and check the success-criteria checklist for that task |
| **Full suite command** | Run the methodology on the test-run problem; verify every conclusion in `test-run-draft.md` traces to a named ground truth via a complete derivation chain |
| **Estimated runtime** | ~10 minutes (manual review of three Markdown deliverables) |

---

## Sampling Rate

- **After every task commit:** Re-read the authored file and check the success-criteria checklist for that task
- **After every plan wave:** Full manual review of all authored deliverables against all 6 requirements
- **Before `/gsd:verify-work`:** Run the test-run methodology in full and verify every conclusion in `test-run-draft.md` has a complete derivation chain
- **Max feedback latency:** ~600 seconds (manual content review)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 1-01-* | 01 | 1 | METH-01, METH-02, METH-03, METH-06 | — | N/A | manual inspection | n/a — content review | ❌ W0 (`methodology.md`) | ⬜ pending |
| 1-02-* | 02 | 1 | METH-04, METH-05 | — | N/A | manual inspection | n/a — content review | ❌ W0 (`output-template.md`) | ⬜ pending |
| 1-03-* | 03 | 2 | SC-4 (test-run dogfoods METH-01..06) | — | N/A | dogfooding run | n/a — produce and inspect the draft | ❌ W0 (`test-run-draft.md`) | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*
*Wave/plan assignment is indicative — the planner finalizes it; this map is updated to match the committed plans.*

---

## Wave 0 Requirements

- [ ] `methodology.md` — covers METH-01, METH-02, METH-03, METH-06, SC-5 — does not exist; an authoring task creates it
- [ ] `output-template.md` — covers METH-04, METH-05 — does not exist; an authoring task creates it
- [ ] `test-run-draft.md` — covers SC-4 — does not exist; created by running the methodology on a real design question

*No automated test framework is installed or required — the deliverables ARE the artifacts under validation.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Each of the 5 phases has an entry AND exit criterion | METH-01 | Prose content — no machine-checkable assertion | Read `methodology.md`; confirm all 5 phases state "this phase is done when X" and an entry condition |
| Each phase names a concrete output artifact | METH-02 | Prose content | Read `methodology.md`; confirm each phase names the artifact it produces |
| Challenge-Assumptions has the 4-type classification scheme with prescribed treatments | METH-03 | Prose content | Confirm physical law / current constraint / convention / untested belief each appear with a prescribed action + stakes-escalation rule |
| Output template is strict-shape with required sections incl. assumptions table | METH-04 | Prose content | Read `output-template.md`; confirm fixed section order and the assumptions table is mandatory |
| Output template requires per-conclusion derivation chains with stable GT-IDs | METH-05 | Prose content | Confirm the traceability map uses `GT-x + GT-y → … → conclusion` chains, not a flat linking table |
| Every phase instruction states a rationale, not a bare imperative | METH-06 | Prose content | Read each phase rule; confirm each is paired with a "because…" rationale |
| Test-run produces an analysis where every conclusion traces to a named ground truth | SC-4 | Dogfooding judgement | Run methodology on the chosen design question; trace each conclusion to a GT-ID |
| At least one phase (Reason Upward) is deliberately high-freedom | SC-5 | Design judgement | Confirm Reason Upward prescribes no sub-steps but mandates self-narration |

---

## Validation Sign-Off

- [ ] All tasks map to a manual-inspection or dogfooding verification
- [ ] Sampling continuity: every authored file is reviewed against its requirements before its wave closes
- [ ] Wave 0 covers all three MISSING deliverables (`methodology.md`, `output-template.md`, `test-run-draft.md`)
- [ ] No watch-mode flags (N/A — no test runner)
- [ ] Feedback latency < 600s
- [ ] `nyquist_compliant: true` set in frontmatter once the plans satisfy this contract

**Approval:** pending
