---
gsd_state_version: 1.0
milestone: v3.13
milestone_name: Routing Catalog v3.2 Content Coverage
status: archived
last_updated: 2026-06-03T23:30:00.000Z
last_activity: 2026-06-03
progress:
  total_phases: 3
  completed_phases: 3
  total_plans: 5
  completed_plans: 5
  percent: 100
stopped_at: Milestone archived — v3.13 shipped and tagged
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-06-03 after v3.13 milestone)

**Core value:** Every conclusion traces back to a verified ground truth and every assumption is explicitly challenged — reasoning a skeptic cannot dismiss as hand-waving.
**Current focus:** Planning next milestone

## Current Position

Phase: 57 (complete)
Plan: All plans complete
Status: v3.13 archived — planning next milestone
Last activity: 2026-06-03

## Milestone History

| Milestone | Phases | Plans | Shipped |
|-----------|--------|-------|---------|
| v1.0 Enhanced Skill | 1-6 | 22 | 2026-05-18 |
| v1.1 Ishikawa (Fishbone) Diagram Tool | 7-10 | 8 | 2026-05-19 |
| v1.2 Forward Consequence-Tracing Tools | 11-14 | 6 | 2026-05-20 |
| v2.0 Collection-of-Skills Plugin | 15-21 | 27 | 2026-05-22 |
| v3.0 First-Principles Orchestrating Agent | 22-29 | 22 | 2026-05-23 |
| v3.1 Routing Quality | 30 | 4 | 2026-05-23 |
| v3.2 META Depth | 31-34 | 21 | 2026-05-24 |
| v3.3 Body-Budget Pre-Commit Hook | 35 | 3 | 2026-05-25 |
| v3.4 Routing-Battery Noise Reduction | 36 | 3 | 2026-05-25 |
| v3.5 Routing Fragility Analysis — P3 & P7 | 37-38 | 7 | 2026-05-25 |
| v3.6 Routing Catalog Expansion (P9/P10) | 39-41 | 8 | 2026-05-26 |
| v3.7 Validation Rigor | 42-44 | 6 | 2026-05-27 |
| v3.8 Sub-Skill Routing Hardening | 45-46 | 8 | 2026-05-28 |
| v3.9 P8 Routing Fix + Phase 45 Convention Restoration | 47-48 | 4 | 2026-05-29 |
| v3.10 Phase 46 Convention Closure | 49 | 1 | 2026-05-29 |
| v3.11 P8 Routing Forward Monitoring | 50-51 | 2 | 2026-05-30 |
| v3.12 Phase-Level Slash Commands | 52-54 | 6 | 2026-05-30 |
| v3.13 Routing Catalog v3.2 Content Coverage | 55-57 | 5 | 2026-06-03 |

Full per-milestone records: `.planning/MILESTONES.md`. Retrospective: `.planning/RETROSPECTIVE.md`.

## Accumulated Context

### Roadmap Evolution

- Phase 26.1 inserted after Phase 26: Migrate monolith and plugin skills into the agent (URGENT) — v3.0
- No phase insertions in v3.1 (single-phase milestone)
- v3.2: 4-phase dependency-ordered roadmap (taxonomy → self-application → per-domain examples → regression gates)
- v3.3: 1-phase milestone (single deliverable, pre-commit hook)
- v3.4: 1-phase milestone (rerun-to-stability extension to check-routing.py)
- v3.5: 2-phase roadmap — Phase 37 (diagnosis + fixes, FRAG-01..06) → Phase 38 (validation, FRAG-07..09). Natural dependency: fixes must precede validation.
- v3.6: 2-phase roadmap mirrors v3.5 structure — Phase 39 (catalog authoring + threshold update, CAT-01..07) → Phase 40 (mini-battery gate + full battery + baseline commit, CAT-08..10). Mini-battery gate pattern (v3.5 retrospective insight) baked in from the start.
- Phase 41 added: Nyquist sign-off for phases 39 and 40
- v3.10: 1-phase milestone (Phase 49) — pure documentation, no code changes, no battery runs. Evidence already exists in 46-01 through 46-04 SUMMARYs.
- v3.11: 2-phase roadmap — Phase 50 (run mini-battery + diagnose if failing, MON-01/02) → Phase 51 (fix if confirmed defect + verify rerun + commit baseline, MON-03/04/05). Conditional branching: MON-02/03/04 only execute if P8 pass rate is below threshold; Phase 51 always executes (baseline committed regardless of outcome).
- v3.12: 3-phase roadmap — Phase 52 (reference file extraction + sync-content.py extension, PHASE-06/07) → Phase 53 (stub authoring + emission + manifest update, PHASE-01..05/08) → Phase 54 (static checks + routing regression battery, PHASE-09/10). Dependency chain: generation infrastructure must exist before stubs can be authored and emitted; all deliverables must exist before gates can be run.
- v3.13: 3-phase roadmap mirrors v3.6 — Phase 55 (catalog authoring + threshold update, TAX-01/02 + META-01/02 + WKEX-01/02 + INFRA-01/02/06) → Phase 56 (mini-battery gate + full battery + baseline commit, INFRA-03/04/05) → Phase 57 (Nyquist sign-off). Dependency chain: new prompts and threshold changes must exist before any battery run; mini-battery must pass before full battery.

### v3.13 scoping notes

- Phase 55 authors all six new catalog rows (P11/P12/P13/N18/N19/N20), updates check-routing.py default thresholds (P ≥ 11/13, N ≥ 18/20) and self-test fixtures, updates the catalog header pass-thresholds line, and adds the v3.13 Catalog History entry. No battery runs in this phase.
- Phase 56 runs the mini-battery gate on new P-prompts first (`tests/routing-mini-catalog-v3.13.md`, `--repeat 5 --min-pass 3`). If all three new P-prompts pass, the full 33-prompt battery runs. The canonical baseline `tests/routing-baseline-v3.13.md` is committed with attribution and coexistence notes.
- Phase 57 is documentation-only: Nyquist sign-off for Phases 55 and 56 (VALIDATION.md files filed, `nyquist_compliant: true`). Mirrors Phase 41 from v3.6.
- Description budget constraint is hard: 1977/2000 chars of slack on the description — no description edits allowed. All trigger phrases for new P-prompts must be drawn from the existing description vocabulary in `shared/spine/SKILL.meta.yml`.
- Mini-battery gate pattern (proven in v3.5, baked in since v3.6): the gate runs before the full battery to catch prompt-embedding failures early (~15-20 min) without paying the full battery cost (~70+ min) on a failed prompt.
- `commit_docs: false` applies — all .planning/ artifacts remain gitignored and are not committed.

### Decisions

Decisions are logged in the PROJECT.md Key Decisions table. Recent decisions added in v3.1:

- Routing battery thresholds tolerate single-prompt non-determinism (P ≥ 6/8, N ≥ 14/15) — verdict survives stochastic flips.
- `check-routing.py` ships as developer tool + non-blocking CI job, not blocking gate — LLM non-determinism makes a strict gate flaky.
- Stream-json + jq subagent-capture methodology documented in-repo (`docs/testing-agents-headlessly.md`), no longer load-bearing in tribal knowledge.

v3.5 roadmapping notes:

- P3 and P7 have distinct root causes (structural embedding defect vs. vocabulary gap) — Phase 37 applies independent, targeted fixes rather than a single undifferentiated change.
- Catalog fix (P3) and description fix (P7) are co-located in Phase 37 because the root-cause documentation directly informs what to change in each case.
- Mini-battery (FRAG-07) precedes full battery (FRAG-08) as a fast-iteration confirmation step — avoids the ~45-70 min full run if a fix is wrong.
- N-case stability (15/15 NO-DELEGATE) is a hard success criterion for Phase 38 — success is not P 8/8 but P3+P7 fixed without degrading N-side behavior.
- [Phase ?]: v3.7 routing battery: P 10/10, N 17/17, BATTERY: PASS — no regressions from v3.6; P2 and P3 improved to PASS
- [Phase ?]: All P11/P12/P13 trigger phrases drawn from existing description vocabulary (budget 1977/2000 chars) — no description edits required
- [Phase ?]: P-threshold default raised from 8 to 11 to match 13P catalog shape
- [Phase ?]: N-threshold default raised from 15 to 18 to match 20N catalog shape
- [Phase ?]: P1-P10 and N1-N17 K/N scores carried forward verbatim from routing-baseline-v3.12.md per D-04; only P11/P12/P13 and N18/N19/N20 freshly measured in v3.13 baseline

### v3.12 scoping notes

- Phase 52 is pure infrastructure: extract the 5 phase procedure descriptions from `shared/spine/SKILL-body.md` into dedicated `shared/references/` files (identify-essence, challenge-assumptions, ground-truths, reason-upward, validate), and extend `sync-content.py` SKILLS tuple + `generate_skill_stubs()` to recognize the new slugs. No user-visible files change.
- Phase 53 authors all 5 `shared/skills/<slug>/SKILL.md` stubs using the `{{PROCEDURE:<slug>}}` token pattern, runs `sync-content.py --write` to emit `first-principles/skills/<slug>/SKILL.md`, and updates `first-principles/.claude-plugin/plugin.json` to declare all 11 skills.
- Phase 54 runs every static gate (`check-links.py`, `check-description-budget.py`, `check-trigger-collisions.py`, `sync-content.py --check`) and the orchestrator routing battery (`--repeat 3 --min-pass 2`, P ≥ 8/10, N ≥ 15/17). The new stubs carry `disable-model-invocation: true` so they cannot cause orchestrator over-triggering; routing regression risk is low but must be verified.
- REQUIREMENTS.md Out of Scope: do NOT modify `shared/spine/SKILL-body.md` to use `{{PHASE:N}}` tokens — the extracted reference files serve as source of truth; SKILL-body.md retains its inline content. This milestone is additive only; the 6 existing companion-tool stubs are not touched.
- `commit_docs: false` applies — all .planning/ artifacts remain gitignored and are not committed.

### v3.11 scoping notes

- MON-01 runs the P8-scoped mini-battery (`tests/routing-mini-catalog-p8.md`, `--repeat 5 --min-pass 3`). This is the entry gate for the milestone.
- MON-02/03/04 are conditional: they only apply if MON-01 finds the pass rate below threshold. If the v3.9 fix held, Phase 51 goes straight to baseline commit (MON-05).
- Root-cause taxonomy for diagnosis (MON-02): vocabulary gap | catalog embedding defect | stochastic boundary. Classification must be supported by evidence, not asserted.
- Fix scope is strictly P8 (MON-03) — no full battery runs, no changes to other catalog prompts.
- N-side spot checks at the P8 boundary (MON-04) confirm no regression from any fix applied.
- `tests/routing-baseline-v3.11.md` (MON-05) is committed regardless of whether a fix was applied; it records the final disposition (held / fixed / stochastic).
- Full routing battery refresh is explicitly out of scope — deferred to a future milestone that makes broader changes.
- `commit_docs: false` applies — all .planning/ artifacts remain gitignored and are not committed.

### v3.10 scoping notes

- Phase 46 has no VERIFICATION.md or VALIDATION.md — this was accepted tech-debt at v3.8 close and deferred past v3.9.
- Evidence is fully captured in per-plan SUMMARYs: 46-04-SUMMARY has Tasks 2 + 3 K/N evidence tables for VERIFY-01 (focused-output baseline) and VERIFY-02 (routing regression); other SUMMARYs cover individual tasks.
- Convention reference: 45-VERIFICATION.md (requirements coverage table) and 45-VALIDATION.md (nyquist_compliant + per-task map + retroactive note) — filed Phase 48.
- No code changes, no routing battery runs, no shared/ edits. Phase 49 is documentation-only.
- `commit_docs: false` applies — all .planning/ artifacts remain gitignored and are not committed.

### Pending Todos

- None.

### Blockers/Concerns

- None.

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260528-vsk | Reword sibling-shared boilerplate to clear check-trigger-collisions gate (6 technique skills carried verbatim "Slash-only; orchestrator uses the main agent." in description → 60 false-positive 4-gram collisions blocking CI on push) | 2026-05-29 | 4380d47 | _inline_ |
| 260528-x9w | Audit opportunities to reduce code-review context across three streams (this-repo cost / skill redesign / repo surface). Investigation only; produced FINDINGS.md (304 lines) recommending 2 cheap follow-ups, not a milestone | 2026-05-29 | _no commit (research)_ | [260528-x9w-audit-code-review-context](./quick/260528-x9w-audit-code-review-context/) |
| 260528-gm | Stamp GENERATED marker on every byte-identical agent-surface emission in sync-content.py so code reviewers can shortcut the shared/↔first-principles/ mirror (~80K tokens duplication on full-repo review) | 2026-05-29 | 15afb18 | _inline_ |
| 260528-ri | Add inert `.reviewignore` at repo root declaring the generated mirror as review-skippable. Forward-compatible — no current reviewer reads it. Pairs with the GENERATED marker for dual-signal shortcut | 2026-05-29 | 3fce97e | _inline_ |
| 260603-ljj | Add automatic resume capability to check-routing.py — skips prompts whose run files are already complete on disk, so interrupted battery runs continue from where they left off rather than restarting from scratch | 2026-06-03 | e92fc7e | [260603-ljj-add-resume-functionality-to-check-routin](./quick/260603-ljj-add-resume-functionality-to-check-routin/) |
| 260528-cr | `/gsd-code-review --files scripts/sync-content.py .reviewignore` → 0 CRITICAL / 2 WARNING / 4 INFO. REVIEW.md alongside FINDINGS.md | 2026-05-29 | _no commit (review)_ | [260528-x9w-audit-code-review-context](./quick/260528-x9w-audit-code-review-context/) |
| 260528-w1 | REVIEW WR-01: correct docstrings on three verbatim-copy generators (generate_agent_references / generate_agent_spine_references / generate_agent_examples) — they still claimed "NO marker expansion, NO edits" after the GENERATED marker prepend | 2026-05-29 | 1fc2949 | _inline_ |
| 260528-w2 | REVIEW WR-02: name agent marker's primary canonical source as a navigable path (`shared/spine/SKILL-body.md`) instead of a freeform prose triple — matches the source_rel shape used by every other call site | 2026-05-29 | 54d15f1 | _inline_ |
| 260529-auo | Review the README.md and update the file to reflect the current state of the project | 2026-05-29 | 42c2ced | [260529-auo-review-the-readme-md-and-update-the-file](./quick/260529-auo-review-the-readme-md-and-update-the-file/) |

Note: "_inline_" rows indicate quick-style tasks executed without the full /gsd-quick ceremony (no per-task PLAN.md / SUMMARY.md / dedicated dir). The audit and the code-review output share dir `260528-x9w-audit-code-review-context/` (FINDINGS.md + REVIEW.md).

Open backlog (skill-side, NOT this repo): teach `gsd-code-reviewer` to parse `.reviewignore` before file discovery — see `.reviewignore` header for rationale and estimated saving (~80K tokens on a full-repo review of this project).

### v3.7 scoping notes

- Core problem: validation rubric criteria are too vague — easy to claim compliance without actually being rigorous. "Could withstand inspection by a skeptic" is itself hand-wavy.
- Success criterion: a skeptic reading any output produced by the agent cannot find an unchallenged assumption.
- Approach: rewrite criteria AND enforce structured application (not either/or).
- Key deliverable is a mandatory Assumption Audit protocol — exhaustive enumeration of assumptions by scanning each derivation chain step, not opportunistic listing.
- Routing regression gate applies: rubric changes live in `shared/spine/references/validation-rubric.md` which propagates via sync-content.py; agent body budget check remains in force.
- v3.7 does NOT expand the routing catalog — that is separate work. Scope is purely the validation/rubric layer.

## Deferred Items

Items acknowledged and deferred:

| Category | Item | Status |
|----------|------|--------|
| verification_gap | Phase 45: 45-VERIFICATION.md | resolved — 45-VERIFICATION.md created 2026-05-29 (Phase 48 Plan 01) |
| nyquist_gap | Phase 45: 45-VALIDATION.md frontmatter never closed | resolved — 45-VALIDATION.md frontmatter closed 2026-05-29 (Phase 48 Plan 01) |
| verification_gap | Phase 46: 46-VERIFICATION.md | resolved — 46-VERIFICATION.md created 2026-05-29 (Phase 49) |
| nyquist_gap | Phase 46: 46-VALIDATION.md | resolved — 46-VALIDATION.md created 2026-05-29 (Phase 49) |
| forward_monitoring | P8 (`decompose this problem`) routing | resolved — P8 HELD at 3/5 (Phase 50); v3.11 baseline (tests/routing-baseline-v3.11.md) closes the watch obligation (Phase 51) |

## v3.13 Requirement Traceability

| REQ-ID | Phase | Notes |
|--------|-------|-------|
| TAX-01 | Phase 55 | P11 assumption-taxonomy P-prompt authoring |
| TAX-02 | Phase 55 | N18 assumption-taxonomy N-prompt authoring |
| META-01 | Phase 55 | P12 self-application P-prompt authoring |
| META-02 | Phase 55 | N19 self-application N-prompt authoring |
| WKEX-01 | Phase 55 | P13 worked-examples-domain P-prompt authoring |
| WKEX-02 | Phase 55 | N20 worked-examples-domain N-prompt authoring |
| INFRA-01 | Phase 55 | check-routing.py threshold + self-test update |
| INFRA-02 | Phase 55 | Catalog header threshold line update |
| INFRA-03 | Phase 56 | Mini-battery gate on new P-prompts |
| INFRA-04 | Phase 56 | Full battery PASS at new thresholds |
| INFRA-05 | Phase 56 | Canonical baseline committed |
| INFRA-06 | Phase 55 | Catalog History entry for v3.13 |

## Session Continuity

Last session: 2026-06-03T22:00:00.000Z
Stopped at: Phase 57 planned (57-01-PLAN.md — 1 plan, 3 tasks)

## Operator Next Steps

- Run `/gsd-new-milestone` to start the next milestone cycle (questioning → research → requirements → roadmap)

## Performance Metrics

| Phase | Plan | Duration | Notes |
|-------|------|----------|-------|
| Phase 29 P01 | 25 min | 5 tasks | 4 files |
| Phase 30 (v3.1) | ~2h 20m | 4 plans / 8 tasks | 7 files, +1006/-2 LOC |
| Phase 33 P01 | 12 min | 2 tasks | 2 files |
| Phase 34 P02 | ~5 min | 1 tasks | 2 files |
| Phase 36 (v3.4) | 1 day | 3 plans | check-routing.py extended; baseline + docs appended |
| Phase 44 P01 | ~70min | 3 tasks | 2 files |
| Phase 44 P02 | ~10min | 2 tasks | 1 file | tests/routing-baseline-v3.7.md committed |
| Phase 54 P01 | 35s | 1 tasks | 0 files |
| Phase 55 P55-01 | 5m | 5 tasks | 1 files |
| Phase 55 P02 | 5m | 2 tasks | 2 files |
| Phase 56 P01 | ~15m | 2 tasks | 1 file | tests/routing-mini-catalog-v3.13.md; INFRA-03 BATTERY: PASS |
| Phase 56 P02 | 10min | 2 tasks | 1 files |
