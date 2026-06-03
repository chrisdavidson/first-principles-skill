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

Run these locally before pushing:

| Script | Gate | Command | What it checks |
|--------|------|---------|----------------|
| `check-body-budget.py` | pre-commit | `python3 scripts/check-body-budget.py` | Agent body ≤ 500 lines |
| `check-agent.py` | GATE-01 | `python3 scripts/check-agent.py` | Agent structural integrity |
| `check-links.py` | VAL-03 | `python3 scripts/check-links.py` | Relative MD links resolve |
| `check-trigger-collisions.py` | VAL-04 | `python3 scripts/check-trigger-collisions.py` | No 4-gram collision across skills |
| `check-description-budget.py` | VAL-05 | `python3 scripts/check-description-budget.py` | Skill listings ≤ 2000 chars |
| `sync-content.py --check` | DUAL-04 | `python3 scripts/sync-content.py --check` | `shared/` and generated tree in sync |

## Pre-commit hooks

Install one of the following mechanisms (not both — they are mutually exclusive at the Git level):

**Option A — install-hooks.sh (recommended):**

```sh
./scripts/install-hooks.sh
```

This symlinks `scripts/git-hooks/pre-commit` into `.git/hooks/pre-commit` and covers both the body-budget gate and the sync-drift gate.

**Option B — core.hooksPath:**

```sh
git config core.hooksPath .githooks
```

`.githooks/pre-commit` also runs both gates.

**Bypass** for intentional in-progress work:

```sh
git commit --no-verify
```

## Editing focused-mode skills

Each of the eleven companion skills has a source file at `shared/skills/<slug>/SKILL.md`. These use `{{PROCEDURE:slug}}` tokens, which are replaced by the full body of `shared/references/<slug>.md` (from `## When to reach for this` onward) when sync-content.py runs.

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
- The agent body (`first-principles/agents/first-principles.md`) must stay under 500 lines.

## CI gates

All gates run on push/PR to master in `.github/workflows/validation.yml`. A PR cannot merge if any gate fails. See [TESTING.md](TESTING.md) for how to run each gate locally.

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

- [ARCHITECTURE.md](ARCHITECTURE.md) — source-of-truth vs. generated surface layout
- [TESTING.md](TESTING.md) — full validation script and routing battery reference
- [CONFIGURATION.md](CONFIGURATION.md) — frontmatter fields and gate configuration
