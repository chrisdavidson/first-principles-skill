---
phase: 4
slug: companion-tool-references
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-17
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Manual review against ROADMAP success criteria (pure-Markdown skill; no automated test runner) |
| **Config file** | none |
| **Quick run command** | Read the authored file; check against its SC (SC-1 / SC-2 / SC-3) and SC-4 |
| **Full suite command** | `grep -n "^---" first-principles-thinking/references/five-whys.md first-principles-thinking/references/pre-mortem.md first-principles-thinking/references/trade-off-analysis.md` (SC-4) + apply `references/validation-rubric.md` quality bar; verify all five ROADMAP components (D-03) in each file |
| **Estimated runtime** | ~60 seconds |

---

## Sampling Rate

- **After every task commit:** Read the authored file; verify against its ROADMAP success criterion.
- **After every plan wave:** Read all three files; run the SC-4 frontmatter grep; verify all five ROADMAP components (when-to-use, procedure, mini-example, failure modes, handoff) appear in each.
- **Before `/gsd:verify-work`:** All three files present, no frontmatter, all five components in each, SC-1/SC-2/SC-3 disciplines encoded.
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 04-01-XX | 01 | 1 | TOOL-01 | — | N/A | manual | Read `five-whys.md`; verify branching procedure + test-based stop criterion (not count-based); all 5 components present; no `^---` frontmatter | ❌ W0 | ⬜ pending |
| 04-02-XX | 02 | 1 | TOOL-02 | — | N/A | manual | Read `pre-mortem.md`; verify prospective-hindsight framing as a mandatory first step; all 5 components present; no `^---` frontmatter | ❌ W0 | ⬜ pending |
| 04-03-XX | 03 | 1 | TOOL-03 | — | N/A | manual | Read `trade-off-analysis.md`; verify weights-locked-before-scoring as a discrete step; all 5 components present; no `^---` frontmatter | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

*Note: this pure-Markdown phase has no automated test runner. Verification is gate-checked by `/gsd:verify-work` reading each file against the ROADMAP success criteria. Task IDs above are placeholders — the planner assigns concrete IDs.*

---

## Wave 0 Requirements

All three target files are stubs and must be authored in Wave 1 — no test infrastructure setup precedes them:

- [ ] `first-principles-thinking/references/five-whys.md` — covers TOOL-01, SC-1
- [ ] `first-principles-thinking/references/pre-mortem.md` — covers TOOL-02, SC-2
- [ ] `first-principles-thinking/references/trade-off-analysis.md` — covers TOOL-03, SC-3

No test framework install needed. No shared fixtures. No config files.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `five-whys.md` reads as a usable sub-procedure with a test-based stop criterion | TOOL-01 / SC-1 | Pure-Markdown content quality is not machine-checkable | Read the file; confirm a reader could run the drill-down from the file alone; confirm the stop criterion is test-based (corrective-action test), not "ask why five times" |
| `pre-mortem.md` framing assumes the failure has already happened | TOOL-02 / SC-2 | Framing quality is a judgment, not a grep | Read the file; confirm the first procedure step instructs the reader to assume the plan has already failed and work backward |
| `trade-off-analysis.md` fixes weighted criteria before scoring | TOOL-03 / SC-3 | Ordering discipline is structural, judged by reading | Read the file; confirm "lock weights before scoring any option" appears as a discrete, ordered step |
| All five ROADMAP components present in each file | TOOL-01/02/03, D-03 | Component presence + adequacy is a content review | Read each file; confirm when-to-use, procedure, mini-example, failure modes, and handoff each appear and are substantive |
| No YAML frontmatter on any file | SC-4 | — (this one IS automatable) | `grep -n "^---" first-principles-thinking/references/{five-whys,pre-mortem,trade-off-analysis}.md` returns no matches |

---

## Validation Sign-Off

- [ ] All tasks have a manual verification mapped (no automated runner for a pure-Markdown phase)
- [ ] Sampling continuity: each authored file is reviewed at its commit
- [ ] Wave 0 covers all MISSING references (the three stubs)
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
