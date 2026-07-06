<!-- generated-by: gsd-doc-writer -->
# Development

This guide covers the full contributor workflow: editing canonical source files, running the sync pipeline, passing validation gates, and submitting changes.

## Prerequisites

- **Python ≥ 3.12** with **PyYAML ≥ 6.0** — required for all scripts
  ```sh
  pip install --user 'pyyaml>=6.0'
  # Or use uv (resolves deps automatically):
  uv run scripts/sync-content.py --check
  ```
- **Claude Code CLI** — required to run the routing battery and plugin validation
- **Git** — standard contributor requirement

## Core rule: edit `shared/` only

The `first-principles/` tree is **generated output**. Every file in it carries a `<!-- GENERATED — DO NOT EDIT -->` marker. Edits made directly to the generated tree will be overwritten on the next sync run and will be caught by the pre-commit drift gate.

**All canonical content lives in `shared/`.**

## Standard editing loop

```
1. Edit files under shared/
2. python3 scripts/sync-content.py --write   # regenerate first-principles/
3. python3 scripts/check-agent.py            # GATE-01 structural checks
4. python3 scripts/sync-content.py --check   # verify no drift
5. git add -u && git commit
```

Or with `uv`:

```sh
uv run scripts/sync-content.py --write
```

## What lives where in `shared/`

| Path | What to edit |
|------|-------------|
| `shared/spine/SKILL-body.md` | Agent body template (uses `{{TOOL:slug}}` tokens) |
| `shared/spine/SKILL.meta.yml` | Agent frontmatter (name, description, version, disallowedTools, maxTurns) |
| `shared/spine/tool-map.yml` | Slug → inline name mapping for token substitution |
| `shared/spine/references/output-template.md` | Output document template inlined into the agent |
| `shared/spine/references/validation-rubric.md` | Validation rubric inlined into the agent |
| `shared/agent/` | Phase procedure fragments stitched into the agent body |
| `shared/references/<slug>.md` | Companion technique reference files (sourced by `{{TOOL:slug}}` and `{{PROCEDURE:slug}}`) |
| `shared/examples/` | Worked example files |
| `shared/skills/<slug>/SKILL.md` | Focused-mode skill stubs (use `{{PROCEDURE:slug}}` tokens) |

## Validation scripts

Run these locally before pushing. For the full CI gate inventory (every gate mapped to its owning script), see [ARCHITECTURE.md](ARCHITECTURE.md). For how to run each gate and interpret results, see [TESTING.md](TESTING.md).

### Sync pipeline

| Script | Gate | Command |
|--------|------|---------|
| `sync-content.py` | DUAL-04 | `python3 scripts/sync-content.py --write` (regenerate) / `python3 scripts/sync-content.py --check` (verify no drift) |

### Static validation gates

| Script | Gate | Command | What it checks |
|--------|------|---------|----------------|
| `check-agent.py` | GATE-01 | `python3 scripts/check-agent.py` | Agent structural integrity |
| `check-links.py` | VAL-03 | `python3 scripts/check-links.py` | Relative MD links resolve (scans `first-principles/`, `shared/`, and `docs/`; `docs/` anchors validated) |
| `check-trigger-collisions.py` | VAL-04 / GATE-02 | `python3 scripts/check-trigger-collisions.py` | No 4-gram collision across skills |
| `check-description-budget.py` | VAL-05 | `python3 scripts/check-description-budget.py` | Skill listings ≤ 2000 chars |
| `check-body-budget.py` | pre-commit | `python3 scripts/check-body-budget.py` | Agent body ≤ 644 lines |
| `check-inventory.py` | AUDIT-01..AUDIT-04 | `python3 scripts/check-inventory.py` | Requirement-ID audit: enumerates and classifies IDs across milestone REQUIREMENTS files. **Not wired into CI** — manual audit tool. |

### Measurement and routing gates

| Script | Gate | Command | Notes |
|--------|------|---------|-------|
| `check-routing.py` | (developer tool) | `python3 scripts/check-routing.py --catalog tests/routing-catalog.md --repeat 5 --min-pass 3` | Main-agent DELEGATE / NO-DELEGATE routing battery. **Not wired into CI** — developer tool only. |
| `check-routing-battery.py` | BATT-06 | `python3 scripts/check-routing-battery.py --repeat 5 --min-pass 3` / `python3 scripts/check-routing-battery.py --self-test` | Merged dual-signal battery (boundary + focused-output). `--self-test` is the BATT-06 CI gate (offline, deterministic). |
| `check-step0-emulator.py` | STEP0-08 | `python3 scripts/check-step0-emulator.py --self-test` | Offline Step 0 phrase-detection classifier (no live Claude session). STEP0-08 CI gate. |
| `check-step0-live.py` | STEP0-06 | `python3 scripts/check-step0-live.py --self-test` (CI) / `python3 scripts/check-step0-live.py --repeat 5 --min-pass 3` (full manual, 60 invocations) | Live Step 0 harness via approach-② bypass channel. `--self-test` is STEP0-06 CI gate. Full manual run requires a live Claude session. |
| `check-traceability.py` | TRACE-03 | `python3 scripts/check-traceability.py --self-test` | Traceability matrix gate. `emit` subcommand regenerates `docs/requirements-matrix.md`. |

**Deprecated shims** (backward compatibility only — do not use for new invocations):

| Script | Delegates to |
|--------|-------------|
| `check-sub-skill-routing.py` | `check-routing-battery.py` (boundary signal) |
| `check-focused-output.py` | `check-routing-battery.py` (focused-output signal) |

**Internal helpers** (underscore-prefixed, not directly invoked):

- `_battery_core.py` — battery core logic; home of `MIN_HEADER_HITS=2` and `_COMPOSER_FOCUS_CEILING=4` constants and the `self_test_boundary()` sentinels
- `_skill_io.py` — shared I/O utilities for skill validation scripts

## Pre-commit hooks

Two gates fire on `git commit`: the **body-budget gate** (blocks if the agent body exceeds 644 lines) and the **sync-drift gate** (blocks if `shared/` and the generated tree have diverged).

Install one of the following mechanisms. **Do not enable both — they are mutually exclusive at the Git level.**

**Option A — `install-hooks.sh` (recommended):**

```sh
./scripts/install-hooks.sh
```

This symlinks `scripts/git-hooks/pre-commit` into `.git/hooks/pre-commit`, running both gates on every commit.

**Option B — `core.hooksPath`:**

```sh
git config core.hooksPath .githooks
```

This points Git at the `.githooks/pre-commit` entry point, which also runs both gates.

**Bypass** for intentional in-progress work:

```sh
git commit --no-verify
```

For what each gate checks in detail, see [TESTING.md](TESTING.md).

## Editing focused-mode skills

Each of the thirteen companion skills has a source file at `shared/skills/<slug>/SKILL.md`. These use `{{PROCEDURE:slug}}` tokens, which are replaced by the full body of `shared/references/<slug>.md` (from `## When to reach for this` onward) when sync-content.py runs.

After editing a skill stub:

```sh
python3 scripts/sync-content.py --write
```

The generated output lands at `first-principles/skills/<slug>/SKILL.md`.

## Key invariants

Keep these invariants intact when authoring or editing:

- Skill `name` in frontmatter must match the parent directory name exactly.
- Skill `description` must be third-person, ≤ 1,024 chars, no XML tags.
- `metadata.version` must be a double-quoted YAML string (e.g. `version: "3.8"`), not a bare number.
- Reserved words `anthropic` and `claude` are forbidden in skill `name` fields.
- All reference file links use forward slashes, one level deep — no `a.md → b.md → c.md` chains.
- The agent body (`first-principles/agents/first-principles.md`) must stay under 644 lines.

## CI gates

All gates run on push/PR to master in `.github/workflows/validation.yml`. A PR cannot merge if any gate fails. For the full gate inventory, see [ARCHITECTURE.md](ARCHITECTURE.md). For how to run each gate locally and interpret results, see [TESTING.md](TESTING.md).

## Commit conventions

Follow the conventional commits format:

```
feat: <description>
fix: <description>
refactor: <description>
docs: <description>
test: <description>
chore: <description>
```

## See also

- [ARCHITECTURE.md](ARCHITECTURE.md) — full CI gate inventory, source-of-truth vs. generated surface layout
- [TESTING.md](TESTING.md) — validation script run-detail, routing battery reference, pre-commit gate behavior
- [CONFIGURATION.md](CONFIGURATION.md) — frontmatter fields and invariants
