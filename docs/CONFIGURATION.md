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
| `metadata.version` | `"8.0.0"` | Version string; must be a double-quoted YAML string, not a bare number |
| `disallowedTools` | `[Write, Edit]` | Tools the agent is forbidden from invoking |
| `maxTurns` | `30` | Maximum conversation turns before the agent halts |
| `AskUserQuestion` | `permitted` | Allows the agent to pause and request clarification |

**To change agent frontmatter:** Edit `shared/spine/SKILL.meta.yml`, then run
`python3 scripts/sync-content.py --write` to regenerate `first-principles/agents/first-principles.md`.
Never hand-edit the generated file.

## Focused-mode skill stub frontmatter fields

Each focused-mode skill stub lives at `first-principles/skills/<slug>/SKILL.md` and is
generated from `shared/skills/<slug>/SKILL.md`. The thirteen registered slugs are:
`pre-mortem`, `inversion`, `fishbone`, `five-whys`, `trade-off`, `second-order`,
`identify-essence`, `challenge-assumptions`, `ground-truths`, `reason-upward`, `validate`,
`estimate`, `theoretical-limit`.

| Field | Required | Example | Description |
|-------|----------|---------|-------------|
| `name` | Yes | `pre-mortem` | Must match the parent directory name exactly; `anthropic` and `claude` are reserved words and forbidden |
| `description` | Yes | `Runs a focused pre-mortem only…` | Third-person, ≤ 1,024 chars, no XML tags |
| `disable-model-invocation` | Yes | `true` | Must be `true`; prevents orchestrator auto-routing — only explicit `/first-principles:<slug>` slash invocation loads the skill |
| `metadata.version` | Yes | `"8.0.0"` | Double-quoted YAML string; required for sync-drift detection |
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
surface. The eight registered slugs in the tool map are: `five-whys`, `fishbone`,
`inversion`, `pre-mortem`, `trade-off`, `second-order`, `estimate`, `theoretical-limit`.

## Version string invariant

`metadata.version` in all frontmatter files must be emitted as a **double-quoted YAML
string** (e.g. `version: "3.0.0"`), never as a bare number. The sync script enforces
this via a custom `_QuotedStr` representer on `shared/spine/SKILL.meta.yml`. Skill stub
frontmatter is passed through verbatim — the source author must use quoted strings in
`shared/skills/<slug>/SKILL.md`.

## Body line budget (report-only, gate retired)

`scripts/check-body-budget.py` reports the generated agent body's line count
(`first-principles/agents/first-principles.md`) on every run. `MAX_LINES = 644` survives in
the script as a historical reference figure only — the number was recalibrated whenever it
bound (500 → 580 → 644) rather than derived from any measured quality requirement, and the
script no longer exits nonzero because of the body's size (it can still fail on a
missing body file or a self-test bug — just never on the line count itself). **The gate that used to block a
commit over this count was retired under TEARDOWN-01** (`docs/v8.7-constraint-teardown.md`,
the standing record) — it no longer runs as part of the pre-commit hooks (see Pre-commit
hooks below) and cannot fail a commit.

Check the current reported count:

```bash
python3 scripts/check-body-budget.py
```

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

Both hook paths run one gate:

1. **Sync-drift gate** — always runs; invokes `scripts/sync-content.py --check`.
   Blocks the commit if `shared/` and the generated tree have diverged.

A body-budget gate used to run alongside this one, blocking a commit that grew the
generated agent body past 644 lines. It was retired under TEARDOWN-01
(`docs/v8.7-constraint-teardown.md`) — `scripts/check-body-budget.py` no longer exits nonzero
because of the body's size, so gating a commit on it would be dead weight, and neither `scripts/git-hooks/pre-commit` nor
`.githooks/pre-commit` invokes it any longer. The reporter is still runnable on demand (see
Body line budget above) for visibility into the current count.

The gate prefers `uv` when available and falls back to `python3`. Bypass it with
`git commit --no-verify` for intentional in-progress work.

## CI gates

All gates run in `.github/workflows/validation.yml` on push and pull request to `master`.
The full gate inventory — all 12 CI gates plus the sync-drift pre-commit gate, with their
owning scripts — is maintained
canonically in [docs/ARCHITECTURE.md](ARCHITECTURE.md#ci-and-pre-commit-gate-inventory). Refer there for the
authoritative gate table.

## Key invariants

- `name` in frontmatter must match the parent directory name exactly.
- `metadata.version` must be a double-quoted YAML string — never a bare number.
- `description` fields must be third-person, ≤ 1,024 chars, no XML tags.
- `disable-model-invocation: true` must be present on every focused-mode skill stub.
- Reserved words `anthropic` and `claude` are forbidden in skill `name` fields.
- All reference file links use forward slashes and are one level deep from the referencing file.
- The generated agent body's line count is reported by `scripts/check-body-budget.py`, not
  enforced — the 644-line figure is a retired, report-only regression-guard figure (gate
  retired under TEARDOWN-01).
- Edit `shared/` only. Never edit the generated tree (`first-principles/`) directly.

## Anti-masking measurement invariants

The routing battery enforces two anti-masking constants defined in
`scripts/_battery_core.py`: `MIN_HEADER_HITS=2` and `_COMPOSER_FOCUS_CEILING=4`. These
constants govern how the battery distinguishes a focused-technique output from a
full-composer output. Their definitions, rationale, and the sentinel tests that lock them
are documented canonically in
[docs/TESTING.md#anti-masking-measurement-invariants](TESTING.md#anti-masking-measurement-invariants).
