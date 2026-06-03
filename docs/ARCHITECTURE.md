<!-- generated-by: gsd-doc-writer -->
# Architecture

This document describes the source-of-truth layout, the generation pipeline, plugin registration, the five-phase agent methodology, and the CI and pre-commit gate system for the first-principles-skills plugin.

## Overview

The plugin ships a single orchestrating agent (`first-principles:first-principles`) plus eleven slash-only companion skills. The entire deliverable is pure Markdown — no executable code ships inside the plugin tree. A Python generation script (`scripts/sync-content.py`) assembles the generated tree from canonical source files in `shared/`.

```
shared/          ← canonical source (edit here)
first-principles/ ← generated plugin (committed, never hand-edited)
scripts/          ← generation, validation, and routing-battery scripts
tests/            ← routing catalog fixtures
```

## Source-of-truth vs. generated surface

**Edit `shared/` only. Never edit the generated tree directly.**

| Area | Path | Role |
|------|------|------|
| Agent body template | `shared/spine/SKILL-body.md` | Assembled agent body; contains `{{TOOL:slug}}` tokens |
| Agent frontmatter | `shared/spine/SKILL.meta.yml` | Frontmatter fields emitted to the generated agent |
| Token → name map | `shared/spine/tool-map.yml` | Slug → inline name mapping for `{{TOOL:slug}}` substitution |
| Output template | `shared/spine/references/output-template.md` | Inlined into agent body |
| Validation rubric | `shared/spine/references/validation-rubric.md` | Inlined into agent body |
| Phase procedures | `shared/agent/` | Phase fragments stitched into the agent body |
| Companion references | `shared/references/` | Five Whys, fishbone, inversion, pre-mortem, trade-off, second-order, identify-essence, challenge-assumptions, ground-truths, reason-upward, validate |
| Worked examples | `shared/examples/` | Eleven domain-spread example files |
| Focused-mode skills | `shared/skills/<slug>/SKILL.md` | Source for each slash-only companion skill |

Generated output tree:

| Path | Role |
|------|------|
| `first-principles/agents/first-principles.md` | Assembled agent (sync-content.py output) |
| `first-principles/agents/references/` | Verbatim copies of `shared/references/` + spine refs |
| `first-principles/agents/references/examples/` | Verbatim copies of `shared/examples/` |
| `first-principles/skills/<slug>/SKILL.md` | Generated stubs from `shared/skills/<slug>/SKILL.md` |
| `first-principles/README.md` | Plugin README |
| `first-principles/LICENSE` | MIT license |

## Generation pipeline

`scripts/sync-content.py --write` reads `shared/` and regenerates the entire `first-principles/` tree. Every generated file is stamped with a `<!-- GENERATED — DO NOT EDIT -->` marker.

**Assembly steps:**

1. Read `shared/spine/SKILL.meta.yml` — emit frontmatter to `first-principles/agents/first-principles.md`
2. Read `shared/spine/SKILL-body.md` — resolve `{{TOOL:slug}}` tokens
3. For each `{{TOOL:slug}}`: extract the `## Procedure` section from `shared/references/<slug>.md` and inline it
4. Inline `shared/spine/references/output-template.md` and `shared/spine/references/validation-rubric.md` at their respective insertion points
5. Stitch phase fragments from `shared/agent/` in order
6. Copy `shared/references/*.md` and `shared/examples/*.md` verbatim to `first-principles/agents/references/`
7. For each `shared/skills/<slug>/SKILL.md`: resolve `{{PROCEDURE:slug}}` tokens (replaced by the full body of `shared/references/<slug>.md` from `## When to reach for this` onward) and write to `first-principles/skills/<slug>/SKILL.md`

**Drift detection:** `scripts/sync-content.py --check` verifies that `shared/` and the generated tree are in sync. Exit code 1 on any drift. This runs as a pre-commit gate and as CI gate DUAL-04.

## Token substitution

Two token types are used in source files:

| Token | Used in | Replaced by |
|-------|---------|-------------|
| `{{TOOL:slug}}` | `shared/spine/SKILL-body.md` | `## Procedure` section from `shared/references/<slug>.md` |
| `{{PROCEDURE:slug}}` | `shared/skills/<slug>/SKILL.md` | Full body of `shared/references/<slug>.md` from `## When to reach for this` onward |

## Plugin layout and registration

The plugin root is `first-principles/`. Install for development:

```bash
claude --plugin-dir ./first-principles
```

The agent is registered at `first-principles/agents/first-principles.md`. The eleven companion skills live under `first-principles/skills/<slug>/SKILL.md` and are registered with `disable-model-invocation: true` — slash-only; the orchestrator never auto-routes to them.

**Companion skill slugs:** `challenge-assumptions`, `fishbone`, `five-whys`, `ground-truths`, `identify-essence`, `inversion`, `pre-mortem`, `reason-upward`, `second-order`, `trade-off`, `validate`

## Five-phase methodology

The agent applies a five-phase procedure. Each phase produces a named artifact that is the entry condition for the next phase:

| Phase | Name | Artifact produced |
|-------|------|-------------------|
| 1 | Identify Essence | Essence Statement |
| 2 | Challenge Assumptions | Classified Assumptions Table |
| 3 | Establish Ground Truths | Ground Truths list (GT-N IDs) |
| 4 | Reason Upward | Derivation Chains (`GT-N + GT-M → conclusion`) |
| 5 | Validate | Signed-off analysis with validation rubric pass |

Six companion techniques (Five Whys, fishbone, inversion, pre-mortem, trade-off, second-order thinking) are available as on-demand reference siblings of the agent and as standalone slash skills.

## CI gates

All gates run in `.github/workflows/validation.yml` on push/PR to master:

| Gate | Script | What it checks |
|------|--------|----------------|
| VAL-01 | `claude plugin validate` | Plugin schema validity |
| VAL-02 | `markdownlint-cli2` | MD style across `first-principles/**/*.md` |
| VAL-03 | `check-links.py` | Relative MD links resolve |
| VAL-04 | `check-trigger-collisions.py` | No 4-gram collision across skill descriptions |
| VAL-05 | `check-description-budget.py` | All skill listings under 2000-char cap |
| DUAL-04 | `sync-content.py --check` | `shared/` and generated tree are in sync |
| GATE-01 | `check-agent.py` | Agent structural checks |

## Pre-commit gates

Two gates fire on `git commit`. Either hook mechanism below provides full coverage — do not use both simultaneously:

| Mechanism | How to activate |
|-----------|----------------|
| `install-hooks.sh` (recommended) | `./scripts/install-hooks.sh` |
| `core.hooksPath` | `git config core.hooksPath .githooks` |

Both gates in the hook:
1. **Body-budget gate** — blocks if `first-principles/agents/first-principles.md` exceeds 500 lines
2. **Sync-drift gate** — blocks if `shared/` and the generated tree have diverged

Bypass for intentional in-progress work: `git commit --no-verify`

## Key invariants

- All reference file links use forward slashes, one level deep (no nested `a.md → b.md → c.md`).
- Skill `name` in frontmatter must match the parent directory name exactly.
- Skill `description` fields must be third-person, ≤ 1,024 chars, no XML tags.
- `metadata.version` must be a double-quoted YAML string (e.g. `version: "3.8"`), not a bare number.
- Reserved words `anthropic` and `claude` are forbidden in skill `name` fields.
- The agent body (`first-principles/agents/first-principles.md`) must stay under 500 lines.
