<!-- generated-by: gsd-doc-writer -->
# Configuration

This document covers all configurable fields, invariants, and environment options for the
first-principles-skills plugin — from the orchestrating agent's frontmatter through the
focused-mode skill stubs, the sync pipeline, and the pre-commit and CI gates.

## Agent frontmatter fields

The orchestrating agent is defined at `first-principles/agents/first-principles.md`.
Its frontmatter is generated from `shared/spine/SKILL.meta.yml`. The canonical values are:

| Field | Value | Description |
|-------|-------|-------------|
| `name` | `first-principles` | Plugin-internal agent identifier; must match the directory name |
| `description` | (see SKILL.meta.yml) | Third-person routing description; ≤ 1,024 chars, no XML tags |
| `license` | `MIT` | License field emitted verbatim |
| `metadata.version` | `"3.0.0"` | Version string; must be a double-quoted YAML string, not a bare number |
| `disallowedTools` | `[Write, Edit]` | Tools the agent is forbidden from invoking |
| `maxTurns` | `30` | Maximum conversation turns before the agent halts |
| `AskUserQuestion` | `permitted` | Allows the agent to pause and request clarification |

**To change agent frontmatter:** Edit `shared/spine/SKILL.meta.yml`, then run
`python3 scripts/sync-content.py --write` to regenerate `first-principles/agents/first-principles.md`.
Never hand-edit the generated file.

## Focused-mode skill stub frontmatter fields

Each focused-mode skill stub lives at `first-principles/skills/<slug>/SKILL.md` and is
generated from `shared/skills/<slug>/SKILL.md`. The eleven registered slugs are:
`pre-mortem`, `inversion`, `fishbone`, `five-whys`, `trade-off`, `second-order`,
`identify-essence`, `challenge-assumptions`, `ground-truths`, `reason-upward`, `validate`.

| Field | Required | Example | Description |
|-------|----------|---------|-------------|
| `name` | Yes | `pre-mortem` | Must match the parent directory name exactly; `anthropic` and `claude` are reserved words and forbidden |
| `description` | Yes | `Runs a focused pre-mortem only…` | Third-person, ≤ 1,024 chars, no XML tags |
| `disable-model-invocation` | Yes | `true` | Must be `true`; prevents orchestrator auto-routing — only explicit `/first-principles:<slug>` slash invocation loads the skill |
| `metadata.version` | Yes | `"3.8.0"` | Double-quoted YAML string; required for sync-drift detection |
| `license` | No | `MIT` | License field; passed through verbatim if present |

**To change a skill stub's frontmatter or body:** Edit the source at
`shared/skills/<slug>/SKILL.md`, then run `python3 scripts/sync-content.py --write`.
The `{{PROCEDURE:<slug>}}` token in the source body is replaced at generation time with
the `## When to reach for this` section through EOF of `shared/references/<slug>.md`.

## Token substitution

The sync pipeline performs two token substitutions:

| Token | Location | Replaced with |
|-------|----------|---------------|
| `{{TOOL:<slug>}}` | `shared/spine/SKILL-body.md` | The value keyed by `<slug>` and the current surface (`agent`) in `shared/spine/tool-map.yml` |
| `{{PROCEDURE:<slug>}}` | `shared/skills/<slug>/SKILL.md` body | Full body of `shared/references/<slug>.md` from `## When to reach for this` onward |

`shared/spine/tool-map.yml` maps each companion-tool slug to its inline text for each
surface. The six registered slugs in the tool map are: `five-whys`, `fishbone`,
`inversion`, `pre-mortem`, `trade-off`, `second-order`.

## Version string invariant

`metadata.version` in all frontmatter files must be emitted as a **double-quoted YAML
string** (e.g. `version: "3.0.0"`), never as a bare number. The sync script enforces
this via a custom `_QuotedStr` representer on `shared/spine/SKILL.meta.yml`. Skill stub
frontmatter is passed through verbatim — the source author must use quoted strings in
`shared/skills/<slug>/SKILL.md`.

## Body line budget

The generated agent body at `first-principles/agents/first-principles.md` must not
exceed **500 lines** (`MAX_LINES = 500` in `scripts/check-body-budget.py`). This limit
is a hard-coded constant — changing it requires a code edit and a reviewed commit.

Check the current count without committing:

```bash
python3 scripts/check-body-budget.py
```

The gate runs automatically on commit (see Pre-commit hooks below) and can be bypassed
with `git commit --no-verify` for intentional in-progress work.

## Markdownlint configuration

Markdownlint rules are configured in `.markdownlint.jsonc` at the repo root:

| Rule | Enabled | Description |
|------|---------|-------------|
| `default` | `false` | All default rules disabled; only the three below are active |
| `MD003` | `true` | Heading style consistency |
| `MD040` | `true` | Fenced code blocks must have a language tag |
| `MD041` | `true` | First line must be a top-level heading |

The linter runs in CI (VAL-02) against `first-principles/**/*.md`.

## Sync pipeline

`scripts/sync-content.py` reads `shared/` and regenerates the entire generated surface.
It requires Python >= 3.12 and PyYAML >= 6.0.

| Command | Effect |
|---------|--------|
| `python3 scripts/sync-content.py --write` | Regenerate all target files |
| `python3 scripts/sync-content.py --check` | Verify no drift; exit 1 if any generated file differs from its source |
| `uv run scripts/sync-content.py --write` | Equivalent using uv (auto-resolves PyYAML) |

**Exit codes for `--check`:**

| Code | Meaning |
|------|---------|
| `0` | No drift |
| `1` | Drift detected — run `--write` and `git add -u` to fix |
| `2` | Environment error (Python < 3.12, missing PyYAML, or non-deterministic generation) |

Generated files are stamped with `<!-- GENERATED — DO NOT EDIT. Source: shared/... -->`.
Skill stub bodies are stamped with `<!-- DO NOT EDIT — generated from shared/skills/<slug>/SKILL.md by sync-content.py -->`.
Both markers appear immediately after the closing `---` frontmatter delimiter.

## Pre-commit hooks

Two hook mechanisms are available. **Use only one at a time** — they are mutually exclusive.

### Option A: install-hooks.sh (symlink into .git/hooks/)

```bash
./scripts/install-hooks.sh
```

Creates `.git/hooks/pre-commit` as a symlink to `scripts/git-hooks/pre-commit`.
Preserves any existing hook as `.git/hooks/pre-commit.bak` on first install; refuses
to overwrite if a `.bak` file already exists.

### Option B: core.hooksPath (.githooks/ directory)

```bash
git config core.hooksPath .githooks
```

Uses `.githooks/pre-commit` directly. This is the alternative approach — do not activate
both mechanisms simultaneously.

### What the pre-commit hook gates

Both hook paths run identical gates:

1. **Body-budget gate** — fires only when one of the seven body-affecting paths is staged
   (`first-principles/agents/first-principles.md`, `shared/spine/SKILL-body.md`,
   `shared/spine/input-contract.md`, `shared/spine/SKILL.meta.yml`,
   `shared/spine/references/output-template.md`,
   `shared/spine/references/validation-rubric.md`, `scripts/sync-content.py`).
   Invokes `scripts/check-body-budget.py`; blocks the commit if the body exceeds 500 lines.

2. **Sync-drift gate** — always runs; invokes `scripts/sync-content.py --check`.
   Blocks the commit if `shared/` and the generated tree have diverged.

Both gates prefer `uv` when available and fall back to `python3`. Bypass both gates
with `git commit --no-verify` for intentional in-progress work.

## CI gates

All gates run in `.github/workflows/validation.yml` on push and pull request to `master`.
Each job has a 10-minute timeout and runs on `ubuntu-latest`.

| Gate ID | Job name | Script | What it checks |
|---------|----------|--------|----------------|
| VAL-01 | `plugin-validate` | `claude plugin validate ./first-principles` | Plugin schema validity (requires `@anthropic-ai/claude-code` installed via npm) |
| VAL-02 | `markdownlint` | `markdownlint-cli2-action@v23` | MD003, MD040, MD041 across `first-principles/**/*.md` |
| VAL-03 | `check-links` | `scripts/check-links.py` | Relative Markdown links resolve |
| VAL-04 / GATE-02 | `check-trigger-collisions` | `scripts/check-trigger-collisions.py` | No 4-gram collision across skill descriptions |
| VAL-05 | `check-description-budget` | `scripts/check-description-budget.py` | All skill listings under 2,000-character cap |
| DUAL-04 | `sync-check` | `scripts/sync-content.py --check` | `shared/` and generated tree are in sync |
| GATE-01 | `check-agent` | `scripts/check-agent.py` | Agent structural checks |

Python-based gates all require Python 3.12 and `pyyaml>=6.0` (installed with
`pip install 'pyyaml>=6.0'` in each job).

## Key invariants

- `name` in frontmatter must match the parent directory name exactly.
- `metadata.version` must be a double-quoted YAML string — never a bare number.
- `description` fields must be third-person, ≤ 1,024 chars, no XML tags.
- `disable-model-invocation: true` must be present on every focused-mode skill stub.
- Reserved words `anthropic` and `claude` are forbidden in skill `name` fields.
- All reference file links use forward slashes and are one level deep from the referencing file.
- The generated agent body must not exceed 500 lines.
- Edit `shared/` only. Never edit the generated tree (`first-principles/`) directly.
