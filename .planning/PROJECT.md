# First Principles Thinking Skill (Enhanced)

## What This Is

An enhanced, extended version of the First Principles Thinking skill for Claude Code —
a pure-Markdown skill (`SKILL.md` + `references/` + `examples/`) forked from
[chrisdavidson/first-principles-skill](https://github.com/chrisdavidson/first-principles-skill).
It gives Claude a systematic methodology for decomposing problems into fundamental truths
and reasoning up from there, for anyone using Claude Code to evaluate designs, challenge
assumptions, and avoid reasoning by analogy.

## Core Value

When Claude applies this skill, the analysis is *rigorous* — every conclusion traces back to
a verified ground truth, and every assumption is explicitly challenged. If everything else
fails, the methodology must still produce reasoning a skeptic cannot dismiss as hand-waving.

## Requirements

### Validated

<!-- Shipped and confirmed valuable. -->

- [x] Sharpen the 5-phase methodology — tighten the process, output format, and rigor where the original is loose — *Validated in Phase 1: Sharpen the Methodology and Harden the Output Format (5/5 success criteria verified)*
- [x] Build out the companion thinking tools (5-Whys, pre-mortem, trade-off analysis) as fully usable reference components inside the single skill — *Validated in Phase 4: Companion Tool References (4/4 success criteria verified)*
- [x] Expand worked examples to cover software/systems, product/business, personal/general, and science/engineering domains — *Validated in Phase 5: Domain-Spread Worked Examples (4/4 must-haves verified, after GAP-01/02/03 gap closure and code-review fixes WR-01–WR-05)*
- [x] Add a Markdown validation rubric — a scoring/self-check the model applies to verify an analysis followed first-principles rigor — *Validated in Phase 3: Validation Rubric*
- [x] Keep the skill installable the same way as the original (copy or symlink into a Claude Code skills directory) — *Validated in Phase 6: Final SKILL.md Wiring, README, and Validation (5/5 success criteria verified — copy/symlink install confirmed, no build step, schema validation passes)*

### Active

<!-- Current scope. Building toward these. v1 = enhanced single skill, pure Markdown. -->

- v1.0 shipped (2026-05-18) — all 27 v1 requirements validated; the enhanced
  single-skill milestone is complete and tagged. No active milestone scope until
  the next one is defined via `/gsd:new-milestone`.

### Next Milestone Candidates

<!-- Carried-forward intent for v1.1+. Not committed scope. -->

- **Milestone 2 — collection of related thinking skills:** split the companion
  tools (5-Whys, pre-mortem, trade-off analysis) into a Claude Code plugin that
  distributes them with a `plugin-name:skill-name` namespace.
- **Milestone 3 — programmatic skill builder:** a Python program (the reserved
  `uv` scaffold) that generates `SKILL.md` + reference files.
- **v1.x polish:** close the two carried-forward tech-debt items (Five Whys
  Phase 3 handback line; `trade-off-analysis.md` length), and the v2 `META-01/02/03`
  depth requirements (self-application reference, expanded taxonomy, extra examples).

### Out of Scope

<!-- Explicit boundaries. Includes reasoning to prevent re-adding. -->

- Splitting into multiple separate skills — deferred to milestone 2 ("collection of skills"); v1 stays a single skill
- A Python program to programmatically build/assemble skills — deferred to milestone 3; the `uv` scaffold stays as that foundation but is untouched in v1
- Executable validation scripts — v1 validation is a Markdown rubric only; scripted scoring is a possible later milestone
- Rewriting or replacing the original methodology wholesale — this enhances and extends, it does not start from scratch

## Context

- **Source repo:** Forked in spirit from `github.com/chrisdavidson/first-principles-skill` (MIT, authored by the same user). The original is a complete, working skill: a 5-phase methodology (Identify Essence → Challenge Assumptions → Establish Ground Truths → Reason Upward → Validate), a standardized output format, multilingual triggers (English + Chinese), a `references/` directory (SpaceX/Tesla examples, software examples), and an `examples/` directory (microservices architecture review).
- **Working directory:** `first-principles-skills` (plural) currently holds only a `uv init` Python scaffold (`main.py`, empty `README.md`, no dependencies). The plural name and `uv` scaffold are deliberate — they reserve room for future milestones (a collection of skills, then a programmatic builder). v1 does not touch the Python side.
- **Three-milestone vision:** (1) enhanced/extended single skill — *this milestone*; (2) collection of related thinking skills; (3) potential Python program that programmatically builds skills.
- **Self-referential goal:** the project's own design decisions are to be made *using* first-principles analysis — the methodology is the planning philosophy, not just the deliverable.
- **Current state (post-v1.0):** the skill ships as `first-principles-thinking/` —
  ~1,700 lines of pure Markdown across `SKILL.md`, 5 `references/` files, and 4
  `examples/` files, plus a human-facing `README.md`. Built in 6 phases / 22 plans
  over 3 days (175 commits). All three validation gates pass (Agent Skills schema,
  markdownlint, link resolution). Installs by copy or symlink with no build step.
  Two minor tech-debt items carried forward; Nyquist coverage is advisory-partial.

## Constraints

- **Tech stack**: Pure Markdown for v1 — no executable code in the skill. Validation tooling is a rubric the model applies.
- **Format**: Must remain a valid Claude Code skill — `SKILL.md` with correct YAML frontmatter (`name`, `description` with trigger phrases, `version`), plus supporting `references/` and `examples/` directories.
- **Compatibility**: Installable by copy or symlink into a Claude Code skills directory, matching the original repo's installation model.
- **Scope discipline**: v1 is a single skill. Resist splitting into multiple skills or adding code — those are explicitly later milestones.

## Key Decisions

<!-- Decisions that constrain future work. Add throughout project lifecycle. -->

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| v1 is the enhanced single skill only | Keeps the first milestone focused and shippable; collection and Python builder are separable later work | ✓ Good — v1.0 shipped focused and on scope, no creep |
| Validation tooling is a Markdown rubric, not a script | Honors "pure Markdown v1"; a self-check the model applies needs no executable code | ✓ Good — rubric proven to FAIL a deliberately weak analysis (Phase 3) |
| Companion tools (5-Whys, pre-mortem, trade-off) live as reference files inside the single skill | v1 is one skill, not a collection — they become usable components, not separate skills | ✓ Good — three self-contained `references/` components, promotion-ready for milestone 2 |
| Keep `uv` scaffold untouched in v1 | It is foundation for the milestone-3 Python builder; removing or using it now would be premature | ✓ Good — scaffold untouched; reserved for milestone 3 |
| Use first-principles analysis to drive the project's own design decisions | The user's explicit "build itself" goal — dogfooding the methodology as planning philosophy | ✓ Good — methodology dogfooded in the Phase 1 test-run draft |
| Build order is dependency-driven: methodology → SKILL.md → rubric → tools → examples → wiring | A content-build chain — the rubric must exist before examples so examples are authored to pass it | ✓ Good — each phase produced a verifiable artifact that unblocked the next |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-18 after v1.0 milestone — full evolution review. All 27 v1 requirements moved to Validated; Key Decisions outcomes resolved to ✓ Good; Context updated with shipped state; next-milestone candidates recorded. v1.0 Enhanced Skill is shipped and tagged.*
