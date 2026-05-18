---
phase: 2
slug: skill-md-skeleton-and-frontmatter
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-16
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

This is a **content-authoring phase** — it produces Markdown files, not executable
code. There is no automated test framework. Validation is **structural inspection**:
line counts, character counts, YAML parse checks, and link-resolution checks. These
are deterministic shell commands run after each task.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None — structural verification by shell command |
| **Config file** | none — no test config needed |
| **Quick run command** | `wc -l first-principles-thinking/SKILL.md` |
| **Full suite command** | `wc -l first-principles-thinking/SKILL.md && python3 -c "import yaml,sys; yaml.safe_load(open('first-principles-thinking/SKILL.md').read().split('---')[1])"` |
| **Estimated runtime** | ~1 second |

---

## Sampling Rate

- **After every task commit:** Run the relevant structural check (`wc -l`, `wc -c`, YAML parse, or link check)
- **After every plan wave:** Run the full suite command — line count + YAML parse
- **Before `/gsd:verify-work`:** SKILL.md body < 500 lines, description ≤ 1,024 chars, all nav-map links resolve
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-xx | 01 | 1 | FOUND-01 | — | N/A | structural | `python3 -c "import yaml; d=yaml.safe_load(open('first-principles-thinking/SKILL.md').read().split('---')[1]); assert d['name']=='first-principles-thinking'; assert d['metadata']['version']=='2.0'"` | ✅ | ⬜ pending |
| 02-01-xx | 01 | 1 | FOUND-02 | — | N/A | structural | `python3 -c "import yaml; d=yaml.safe_load(open('first-principles-thinking/SKILL.md').read().split('---')[1]); assert len(d['description'])<=1024" && grep -c 'Use when' first-principles-thinking/SKILL.md` | ✅ | ⬜ pending |
| 02-01-xx | 01 | 1 | FOUND-03 | — | N/A | structural | `test $(wc -l < first-principles-thinking/SKILL.md) -lt 500` | ✅ | ⬜ pending |
| 02-01-xx | 01 | 1 | VALID-05 | — | N/A | structural | `grep -q 'references/validation-rubric.md' first-principles-thinking/SKILL.md && test -f first-principles-thinking/references/validation-rubric.md` | ✅ | ⬜ pending |

*Task IDs are placeholders — the planner assigns final IDs. Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements.* No test files or framework
install needed — this phase's verification is structural inspection via shell
commands (`wc`, `grep`, `python3 -c yaml`). The planner must include these checks
as `<acceptance_criteria>` and verification tasks within the implementation wave,
not as separate test files.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Description triggers reliably in practice | FOUND-02 | Discoverability is behavioral — only confirmable by live skill loading in Claude Code | After install, type a trigger phrase ("challenge assumptions", "is this the right approach") and confirm the skill auto-loads. Deferred to Phase 6 live-validation; Phase 2 verifies the description structurally only. |
| Methodology embedded verbatim with rigor preserved | FOUND-03 | Faithfulness to Phase 1 `methodology.md` is a content-diff judgement, not a count | Diff the resident methodology block against `01/methodology.md`; confirm entry/exit criteria, named artifacts, the 4-type assumption scheme, and rationale statements all survive. |

---

## Validation Sign-Off

- [ ] All tasks have a deterministic structural-check command or Wave 0 coverage
- [ ] Sampling continuity: every task has an automated structural check (no 3 consecutive unverified tasks)
- [ ] Wave 0 covers all MISSING references — N/A, no test files needed
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
