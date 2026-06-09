---
gsd_state_version: 1.0
milestone: v4.1
milestone_name: Builder Auto-Install Flag
status: archived
stopped_at: Milestone archived (Phase 64.1 tech debt closure complete)
last_updated: "2026-06-09T00:00:00.000Z"
last_activity: 2026-06-09
progress:
  total_phases: 5
  completed_phases: 5
  total_plans: 5
  completed_plans: 5
  percent: 100
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-06-09 after v4.1 milestone fully closed)

**Core value:** Every conclusion traces back to a verified ground truth and every assumption is explicitly challenged — reasoning a skeptic cannot dismiss as hand-waving.
**Current focus:** Planning next milestone (run `/gsd-new-milestone`)

## Current Position

Phase: v4.1 archived
Plan: —
Status: Milestone complete
Last activity: 2026-06-09

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
| v4.0 Programmatic Skill/Agent Builder | 58-60 + 60.1 | 7 | 2026-06-04 |
| v4.1 Builder Auto-Install Flag | 61-64 + 64.1 | 5 | 2026-06-08 |

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
- v4.0: 3-phase roadmap — Phase 58 (CLI scaffold + template rendering, CLI-01/02/03/07) → Phase 59 (post-generation validation wiring, CLI-04/05/06) → Phase 60 (documentation, CLI-08). Dependency chain: interactive entry point and templates must exist before validators can be wired; all behavior must be settled before documentation is written.
- Phase 60.1 inserted after Phase 60: Fix CLI-06 semantic gap — check-agent.py `_EXPECTED_NAME` lock and trigger-phrase checks cause every builder-generated agent to always fail regardless of structural correctness (URGENT) — v4.0
- v4.1: 4-phase roadmap — Phase 61 (argparse + flow wiring, no-op stubs) → Phase 62 (_install() + conflict guard + validation gate, INST-01/02/03/05) → Phase 63 (_sync_content() + rollback, INST-04) → Phase 64 (tests + README, INST-06/07). Dependency chain: argparse must exist before any filesystem logic is added; conflict guard must be stable before integration tests; rollback depends on knowing the exact install path.
- Phase 64.1 inserted after Phase 64: Address tech debt: v4.1 debt items — stale D-03 note (Ph62), missing no-flag test (Ph64), stdout-before-stderr output order (Ph63) (INSERTED, URGENT) — v4.1

### v4.1 scoping notes

- Phase 61 introduces argparse without touching install logic — makes `--install` recognizable and stubs `_install()` and `_sync_content()` as no-ops. Zero filesystem writes. This isolates any wiring failures from install logic failures.
- Phase 62 implements both artifact_type branches of `_install()`: skill path (`shared/skills/<slug>/SKILL.md`, requires mkdir) and agent path (`shared/agent/<slug>.md`, flat file). Conflict guard on `shared/` destination is independent of the existing overwrite guard in `_render_and_write()` which protects `generated/`. INST-05 (validation gate) lands here because it is part of the install flow, not documentation.
- Phase 63 implements `_sync_content()` via subprocess invocation of `sync-content.py --write` using a `REPO_ROOT`-anchored absolute path and `sys.executable`. On non-zero exit: forward stderr verbatim, call `target.unlink()` (rollback), `sys.exit(1)`. Resolved in favor of PITFALLS.md (rollback) over FEATURES.md (keep file) — drift gate argument is load-bearing.
- Phase 64 is tests + README only. Tests use `TemporaryDirectory` + module-level constant patching to avoid real `shared/` writes. Post-suite assertion: `git status --porcelain shared/` must be empty. README documents `--install` behavior, conflict policy, rollback semantics, and agent-manifest caveat (new agents in `shared/agent/` are not automatically declared in `plugin.json`).
- `commit_docs: false` applies — all .planning/ artifacts remain gitignored and are not committed.
- Phase 61 satisfies no INST- requirements on its own; it is a prerequisite. Requirements map: INST-01/02/03/05 → Phase 62; INST-04 → Phase 63; INST-06/07 → Phase 64.
- Copy idiom: `target.write_text(candidate_path.read_text(encoding="utf-8"), encoding="utf-8")` — avoids introducing `shutil` import per ARCHITECTURE.md anti-pattern 5.

### v4.0 scoping notes

- Phase 58 owns the complete interactive experience: `main.py` entry point, prompt loop, and both template renderers (skill and agent). This is the core delivery — a user can generate a valid candidate file from this phase alone.
- Phase 59 wires the three existing check-* scripts as a post-generation validation step. No new validation logic is written; only subprocess integration and pass/fail reporting.
- Phase 60 is documentation-only: README "Builder" section with usage, prompts, and output locations.
- Output is candidate-only (no auto-install into shared/ or first-principles/) — this is an explicit v4.0 Out of Scope boundary in REQUIREMENTS.md.
- The uv scaffold already exists (main.py in the project root). Phase 58 replaces/extends it in-place; no new files outside main.py and a possible templates/ directory are expected.
- check-description-budget.py and check-trigger-collisions.py apply to skill output; check-agent.py applies to agent output. They run in-process via subprocess on the generated candidate file path.
- `commit_docs: false` applies — all .planning/ artifacts remain gitignored and are not committed.

### Decisions

Decisions are logged in the PROJECT.md Key Decisions table. Recent decisions added in v3.1:

- Routing battery thresholds tolerate single-prompt non-determinism (P ≥ 6/8, N ≥ 14/15) — verdict survives stochastic flips.
- `check-routing.py` ships as developer tool + non-blocking CI job, not blocking gate — LLM non-determinism makes a strict gate flaky.
- Stream-json + jq subagent-capture methodology documented in-repo (`docs/testing-agents-headlessly.md`), no longer load-bearing in tribal knowledge.

v4.1 roadmapping decisions:

- Rollback on sync failure (PITFALLS.md wins over FEATURES.md) — drift gate is a repository-wide blocker; orphaned `shared/` file is harder to diagnose than a clean rollback with verbatim error output.
- `Path.write_text` for the copy step, not `shutil.copy2` — avoids introducing a new import, consistent with sync-content.py line 739 idiom.
- Validation gate (INST-05) is part of Phase 62 (install flow), not Phase 64 (documentation) — it is a behavioral change to `_run_validation()` semantics, not a docs artifact.
- Phase 61 does not satisfy any INST- requirement independently; it is a prerequisite that isolates argparse changes from filesystem changes.

### v3.13 scoping notes

- Phase 55 authors all six new catalog rows (P11/P12/P13/N18/N19/N20), updates check-routing.py default thresholds (P ≥ 11/13, N ≥ 18/20) and self-test fixtures, updates the catalog header pass-thresholds line, and adds the v3.13 Catalog History entry. No battery runs in this phase.
- Phase 56 runs the mini-battery gate on new P-prompts first (`tests/routing-mini-catalog-v3.13.md`, `--repeat 5 --min-pass 3`). If all three new P-prompts pass, the full 33-prompt battery runs. The canonical baseline `tests/routing-baseline-v3.13.md` is committed with attribution and coexistence notes.
- Phase 57 is documentation-only: Nyquist sign-off for Phases 55 and 56 (VALIDATION.md files filed, `nyquist_compliant: true`). Mirrors Phase 41 from v3.6.
- Description budget constraint is hard: 1977/2000 chars of slack on the description — no description edits allowed. All trigger phrases for new P-prompts must be drawn from the existing description vocabulary in `shared/spine/SKILL.meta.yml`.
- Mini-battery gate pattern (proven in v3.5, baked in since v3.6): the gate runs before the full battery to catch prompt-embedding failures early (~15-20 min) without paying the full battery cost (~70+ min) on a failed prompt.
- `commit_docs: false` applies — all .planning/ artifacts remain gitignored and are not committed.

### Decisions

Decisions are logged in the PROJECT.md Key Decisions table.

v3.5 roadmapping notes:

- P3 and P7 have distinct root causes (structural embedding defect vs. vocabulary gap) — Phase 37 applies independent, targeted fixes rather than a single undifferentiated change.
- Catalog fix (P3) and description fix (P7) are co-located in Phase 37 because the root-cause documentation directly informs what to change in each case.
- Mini-battery (FRAG-07) precedes full battery (FRAG-08) as a fast-iteration confirmation step — avoids the ~45-70 min full run if a fix is wrong.
- N-case stability (15/15 NO-DELEGATE) is a hard success criterion for Phase 38 — success is not P 8/8 but P3+P7 fixed without degrading N-side behavior.

### v3.12 scoping notes

- Phase 52 is pure infrastructure: extract the 5 phase procedure descriptions from `shared/spine/SKILL-body.md` into dedicated `shared/references/` files (identify-essence, challenge-assumptions, ground-truths, reason-upward, validate), and extend `sync-content.py` SKILLS tuple + `generate_skill_stubs()` to recognize the new slugs. No user-visible files change.
- Phase 53 authors all 5 `shared/skills/<slug>/SKILL.md` stubs using the `{{PROCEDURE:<slug>}}` token pattern, runs `sync-content.py --write` to emit `first-principles/skills/<slug>/SKILL.md`, and updates `first-principles/.claude-plugin/plugin.json` to declare all 11 skills.
- Phase 54 runs every static gate (`check-links.py`, `check-description-budget.py`, `check-trigger-collisions.py`, `sync-content.py --check`) and the orchestrator routing battery (`--repeat 3 --min-pass 2`, P ≥ 8/10, N ≥ 15/17). The new stubs carry `disable-model-invocation: true` so they cannot cause orchestrator over-triggering; routing regression risk is low but must be verified.
- REQUIREMENTS.md Out of Scope: do NOT modify `shared/spine/SKILL-body.md` to use `{{PHASE:N}}` tokens — the extracted reference files serve as source of truth; SKILL-body.md retains its inline content. This milestone is additive only; the 6 existing companion-tool stubs are not touched.
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

## Deferred Items

Items acknowledged and deferred:

| Category | Item | Status |
|----------|------|--------|
| verification_gap | Phase 45: 45-VERIFICATION.md | resolved — 45-VERIFICATION.md created 2026-05-29 (Phase 48 Plan 01) |
| nyquist_gap | Phase 45: 45-VALIDATION.md frontmatter never closed | resolved — 45-VALIDATION.md frontmatter closed 2026-05-29 (Phase 48 Plan 01) |
| verification_gap | Phase 46: 46-VERIFICATION.md | resolved — 46-VERIFICATION.md created 2026-05-29 (Phase 49) |
| nyquist_gap | Phase 46: 46-VALIDATION.md | resolved — 46-VALIDATION.md created 2026-05-29 (Phase 49) |
| forward_monitoring | P8 (`decompose this problem`) routing | resolved — P8 HELD at 3/5 (Phase 50); v3.11 baseline (tests/routing-baseline-v3.11.md) closes the watch obligation (Phase 51) |

## v4.1 Requirement Traceability

| REQ-ID | Phase | Notes |
|--------|-------|-------|
| INST-01 | Phase 62 | Skill install copy: shared/skills/<slug>/SKILL.md |
| INST-02 | Phase 62 | Agent install copy: shared/agent/<slug>.md |
| INST-03 | Phase 62 | Conflict guard: abort + exit 1 if target exists |
| INST-04 | Phase 63 | sync-content.py --write + rollback on failure |
| INST-05 | Phase 62 | Validation FAIL becomes hard block when --install active |
| INST-06 | Phase 64 | README ## Builder section update |
| INST-07 | Phase 64 | Tests (TemporaryDirectory, all failure modes) |

## v4.0 Requirement Traceability

| REQ-ID | Phase | Notes |
|--------|-------|-------|
| CLI-01 | Phase 58 | Interactive session + prompt loop |
| CLI-02 | Phase 58 | Skill template rendering |
| CLI-03 | Phase 58 | Agent template rendering |
| CLI-04 | Phase 59 | check-description-budget.py integration |
| CLI-05 | Phase 59 | check-trigger-collisions.py integration |
| CLI-06 | Phase 59 | check-agent.py integration |
| CLI-07 | Phase 58 | main.py entry point constraint |
| CLI-08 | Phase 60 | README Builder section |

## Session Continuity

Last session: 2026-06-09T00:00:00.000Z
Stopped at: v4.1 milestone fully archived

## Operator Next Steps

- Run `/gsd-new-milestone` to define and plan the next milestone

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
| Phase 59 P01 | 5m | 2 tasks | 2 files |
| Phase 59 P02 | 5m | 2 tasks | 2 files |
| Phase 63 P01 | 3 minutes | 1 tasks | 1 files |
