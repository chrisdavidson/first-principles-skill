---
phase: 06
slug: final-skill-md-wiring-readme-and-validation
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-18
---

# Phase 06 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Three host-side gates — no unit-test framework (pure-Markdown skill) |
| **Config file** | `.markdownlint.jsonc` (created in Wave 0) |
| **Quick run command** | `agentskills validate ./first-principles-thinking` |
| **Full suite command** | `agentskills validate ./first-principles-thinking && npx markdownlint-cli2 "first-principles-thinking/**/*.md" --config .markdownlint.jsonc && bash dev/check-links.sh` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `agentskills validate ./first-principles-thinking`
- **After every plan wave:** Run the full suite command above
- **Before `/gsd:verify-work`:** All three gates (schema, markdownlint, link-resolution) must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 06-01-01 | 01 | 1 | PKG-02, PKG-03 | — | N/A | tooling | `.markdownlint.jsonc` exists; `dev/check-links.sh` exits 0 | ❌ W0 | ⬜ pending |
| 06-01-02 | 01 | 1 | — | — | N/A | lint | `npx markdownlint-cli2 "first-principles-thinking/**/*.md" --config .markdownlint.jsonc` exits 0 (5 MD040 fixed) | ❌ W0 | ⬜ pending |
| 06-02-01 | 02 | 2 | FOUND-04, TOOL-04 | — | N/A | schema+link | `agentskills validate ./first-principles-thinking` exits 0; `bash dev/check-links.sh` exits 0 | ✅ | ⬜ pending |
| 06-03-01 | 03 | 2 | PKG-01 | — | N/A | manual | Human review of `README.md` against D-01/D-02/D-03/D-10 | ✅ | ⬜ pending |
| 06-04-01 | 04 | 3 | FOUND-05, PKG-02, PKG-03 | — | N/A | schema+lint+link | Full suite command exits 0 | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*
*Task IDs are indicative; the planner sets the authoritative wave/task layout.*

---

## Wave 0 Requirements

- [ ] `.markdownlint.jsonc` — repo-root config: `default: false`, `MD003`/`MD040`/`MD041` on, `MD013` off
- [ ] `dev/check-links.sh` — host-side link-resolution script extracting every relative Markdown link from `first-principles-thinking/SKILL.md` + `references/` + `examples/` and asserting each target exists (committing it is discretionary per D-05; if committed it lives in `dev/`, never inside the skill directory)
- [ ] No unit-test framework needed — pure-Markdown skill; validation is the three host-side gates

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `README.md` covers skill, methodology summary, companion tools, worked examples, when-to-use, fork lineage, install | PKG-01 | Prose quality and completeness cannot be machine-checked | Read `README.md`; confirm every section in D-01 is present, methodology points to `SKILL.md` + `references/output-template.md` as canonical (D-02), "Relationship to the original" names the concrete v2.0 additions (D-03), install covers `cp` + `ln -s` into personal + project scope with the `first-principles-thinking` dirname requirement called out (D-10) |
| Installs by copy/symlink with no build step | FOUND-05 | No build artifact exists to assert against | Confirm the skill directory contains only Markdown (no `scripts/`, no generated files); confirm install is `cp -r`/`ln -s` only |
| `skills-ref`/`agentskills` install fallback | PKG-03 | Network/permission failure during install needs human judgement | If `agentskills` is unavailable, the validation task is flagged `autonomous: false`; fallback evidence is a documented manual conformance check against the CLAUDE.md frontmatter constraints (D-04 contingency) |

---

## Validation Sign-Off

- [ ] All tasks have an automated command or a Wave 0 dependency
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references (`.markdownlint.jsonc`, `dev/check-links.sh`)
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
