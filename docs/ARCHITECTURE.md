<!-- generated-by: gsd-doc-writer -->
# Architecture

This document describes the source-of-truth layout, the generation pipeline, plugin registration, the five-phase agent methodology, the measurement subsystem (inventory), and the canonical CI and pre-commit gate inventory for the first-principles-skills plugin.

## Overview

The plugin ships a single orchestrating agent (`first-principles:first-principles`) plus eleven slash-only companion skills. The entire deliverable is pure Markdown — no executable code ships inside the plugin tree. A Python generation script (`scripts/sync-content.py`) assembles the generated tree from canonical source files in `shared/`.

```
shared/           ← canonical source (edit here)
first-principles/ ← generated plugin (committed, never hand-edited)
scripts/          ← generation, validation, and measurement-battery scripts
tests/            ← routing catalog fixtures and step 0 capture files
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

Six of these companion techniques (Five Whys, fishbone, inversion, pre-mortem, trade-off, second-order thinking) are inlined into the agent body via `{{TOOL:slug}}` tokens and are also available as on-demand reference siblings. All eleven companion skills — these six techniques plus the five phase skills (identify-essence, challenge-assumptions, ground-truths, reason-upward, validate) — are additionally registered as standalone, slash-only skills (`disable-model-invocation: true`).

## CI and pre-commit gate inventory

All CI gates run in `.github/workflows/validation.yml` on push/PR to master. The two pre-commit gates fire on `git commit` via the project hook mechanism.

| Gate | Job / Mechanism | Script | What it checks |
|------|----------------|--------|----------------|
| VAL-01 | `plugin-validate` (CI) | `claude plugin validate` | Plugin schema validity |
| VAL-02 | `markdownlint` (CI) | `markdownlint-cli2` | MD style across `first-principles/**/*.md` |
| VAL-03 | `check-links` (CI) | `scripts/check-links.py` | Relative MD links resolve in plugin, shared, and docs trees; `docs/` anchors validated with github-slugger rule |
| VAL-04 / GATE-02 | `check-trigger-collisions` (CI) | `scripts/check-trigger-collisions.py` | No 4-gram collision across skill descriptions |
| VAL-05 | `check-description-budget` (CI) | `scripts/check-description-budget.py` | All skill listings under 2000-char cap |
| DUAL-04 | `sync-check` (CI) | `scripts/sync-content.py --check` | `shared/` and generated tree are in sync |
| GATE-01 | `check-agent` (CI) | `scripts/check-agent.py` | Agent structural checks |
| BATT-06 | `check-routing-battery` (CI) | `scripts/check-routing-battery.py --self-test` | Merged dual-signal battery self-test (boundary + focused-output); anti-masking sentinels |
| STEP0-08 | `check-step0-emulator` (CI) | `scripts/check-step0-emulator.py --self-test` | Offline Step 0 phrase-detection classifier self-test |
| STEP0-06 | `check-step0-live` (CI) | `scripts/check-step0-live.py --self-test` | Step 0 live-harness scoring/parsing logic self-test |
| TRACE-03 | `check-traceability` (CI) | `scripts/check-traceability.py --self-test` | Traceability gate self-test (capability/tier schema + artifact resolution) |
| — | body-budget gate (pre-commit) | `scripts/check-body-budget.py` | Agent body (`first-principles/agents/first-principles.md`) stays under 500 lines |
| — | sync-drift gate (pre-commit) | `scripts/sync-content.py --check` | `shared/` and generated tree are in sync (same check as DUAL-04, fires before commit) |

Note: VAL-04 and GATE-02 are both carried by the single `check-trigger-collisions` job (matching the live job's `name: check-trigger-collisions (VAL-04/GATE-02)`).

For operational run-detail — how to invoke each gate locally, `--self-test` modes, and what the pre-commit hook checks — see [docs/TESTING.md](TESTING.md).

## Measurement subsystem

The following scripts form the measurement subsystem. They sit alongside the validation scripts in `scripts/` and are named here at inventory altitude. For anti-masking invariants, constant values, and the full inter-layer wiring detail see [docs/TESTING.md](TESTING.md).

| Component | Script | Role |
|-----------|--------|------|
| Step 0 emulator | `scripts/check-step0-emulator.py` | Offline phrase-detection classifier; reads the `**Phrase detection rules**` table from `shared/spine/SKILL-body.md` and classifies a prompt to `MODE` (STEP0-08) |
| Step 0 live harness | `scripts/check-step0-live.py` | Live MODE classification via the approach-② bypass channel against a running `claude` session (STEP0-06 offline self-test) |
| Routing battery | `scripts/check-routing-battery.py` | Merged dual-signal battery: boundary-discipline + focused-output signals scored together (BATT-06 `--self-test`) |
| Routing battery (developer tool) | `scripts/check-routing.py` | Main-agent DELEGATE / NO-DELEGATE routing battery; developer tool, not wired into CI |
| Battery core | `scripts/_battery_core.py` | Shared battery logic; home of the anti-masking invariant constants and the `self_test_boundary()` sentinels |
| Traceability matrix | `scripts/check-traceability.py` | Capability → requirement → test traceability matrix; `emit` generates the matrix, `--self-test` is TRACE-03 |

Two deprecated thin shims (`scripts/check-sub-skill-routing.py`, `scripts/check-focused-output.py`) delegate to `check-routing-battery.py` for backward compatibility; new callers should invoke `check-routing-battery.py` directly.

## Key invariants

- All reference file links use forward slashes, one level deep (no nested `a.md → b.md → c.md`).
- Skill `name` in frontmatter must match the parent directory name exactly.
- Skill `description` fields must be third-person, ≤ 1,024 chars, no XML tags.
- `metadata.version` must be a double-quoted YAML string (e.g. `version: "3.8"`), not a bare number.
- Reserved words `anthropic` and `claude` are forbidden in skill `name` fields.
- The agent body (`first-principles/agents/first-principles.md`) must stay under 500 lines.
