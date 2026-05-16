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

### Active

<!-- Current scope. Building toward these. v1 = enhanced single skill, pure Markdown. -->

- [ ] Expand worked examples to cover software/systems, product/business, personal/general, and science/engineering domains
- [ ] Add a Markdown validation rubric — a scoring/self-check the model applies to verify an analysis followed first-principles rigor
- [ ] Build out the companion thinking tools (5-Whys, pre-mortem, trade-off analysis) as fully usable reference components inside the single skill
- [ ] Keep the skill installable the same way as the original (copy or symlink into a Claude Code skills directory)

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

## Constraints

- **Tech stack**: Pure Markdown for v1 — no executable code in the skill. Validation tooling is a rubric the model applies.
- **Format**: Must remain a valid Claude Code skill — `SKILL.md` with correct YAML frontmatter (`name`, `description` with trigger phrases, `version`), plus supporting `references/` and `examples/` directories.
- **Compatibility**: Installable by copy or symlink into a Claude Code skills directory, matching the original repo's installation model.
- **Scope discipline**: v1 is a single skill. Resist splitting into multiple skills or adding code — those are explicitly later milestones.

## Key Decisions

<!-- Decisions that constrain future work. Add throughout project lifecycle. -->

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| v1 is the enhanced single skill only | Keeps the first milestone focused and shippable; collection and Python builder are separable later work | — Pending |
| Validation tooling is a Markdown rubric, not a script | Honors "pure Markdown v1"; a self-check the model applies needs no executable code | — Pending |
| Companion tools (5-Whys, pre-mortem, trade-off) live as reference files inside the single skill | v1 is one skill, not a collection — they become usable components, not separate skills | — Pending |
| Keep `uv` scaffold untouched in v1 | It is foundation for the milestone-3 Python builder; removing or using it now would be premature | — Pending |
| Use first-principles analysis to drive the project's own design decisions | The user's explicit "build itself" goal — dogfooding the methodology as planning philosophy | — Pending |

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
*Last updated: 2026-05-16 after Phase 1 completion*
