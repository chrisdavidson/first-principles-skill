<!-- generated-by: gsd-doc-writer -->
# Contributing

Thank you for contributing to first-principles-skills. This project ships a Claude Code plugin as pure Markdown — no compiled artifacts, no build step. Contributions follow a `shared/` → sync → validate → PR loop.

## Before you start

- **Python ≥ 3.12 + PyYAML ≥ 6.0** are required to run sync and validation scripts.
- **Claude Code CLI** is required to run the routing battery and plugin validation.
- Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) to understand the source-of-truth vs. generated surface distinction — it is the single most important thing to know before making changes.

## The core rule

**Edit `shared/` only. Never edit `first-principles/` directly.**

The `first-principles/` tree is generated output. Every file in it carries a `<!-- GENERATED — DO NOT EDIT -->` marker. Direct edits will be overwritten on the next sync run and blocked by the pre-commit drift gate.

## Standard contribution loop

```sh
# 1. Edit files under shared/
# 2. Regenerate the plugin tree
python3 scripts/sync-content.py --write

# 3. Run local validation
python3 scripts/check-body-budget.py
python3 scripts/check-agent.py
python3 scripts/check-links.py
python3 scripts/check-trigger-collisions.py
python3 scripts/check-description-budget.py
python3 scripts/sync-content.py --check

# 4. Commit
git add -u
git commit -m "feat: <description>"
```

## Setting up pre-commit hooks (recommended)

Install the hooks so drift and body-budget issues are caught before you push:

```sh
./scripts/install-hooks.sh
```

This covers both the body-budget gate (blocks if the agent body exceeds 644 lines) and the sync-drift gate (blocks if `shared/` and the generated tree have drifted). See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for the alternative `core.hooksPath` opt-in.

## What you can contribute

| Area | Where to edit |
|------|--------------|
| Agent methodology (phases 1–5) | `shared/agent/` and `shared/spine/SKILL-body.md` |
| Agent frontmatter (description, version, tools) | `shared/spine/SKILL.meta.yml` |
| Companion technique reference (Five Whys, fishbone, etc.) | `shared/references/<slug>.md` |
| Focused-mode skill stubs | `shared/skills/<slug>/SKILL.md` |
| Worked examples | `shared/examples/` |
| Validation scripts | `scripts/` |
| Routing catalogs | `tests/routing-catalog.md`, `tests/sub-skill-routing-catalog.md` |
| Documentation | `docs/` — register new pages in the `docs/README.md` nav; intra-docs links use bare filenames (no `docs/` prefix) |

## Key invariants

All PRs must preserve these:

- Skill `name` in frontmatter must match the parent directory name exactly.
- Skill `description` must be third-person, ≤ 1,024 chars, no XML tags.
- `metadata.version` must be a double-quoted YAML string (e.g. `version: "3.8"`), not a bare number.
- Reserved words `anthropic` and `claude` are forbidden in skill `name` fields.
- All reference file links use forward slashes, one level deep — no nested `a.md → b.md → c.md` chains.
- The agent body (`first-principles/agents/first-principles.md`) must stay under 644 lines.

## CI gates

All PRs must pass the CI gates in `.github/workflows/validation.yml`. Before pushing, run the
whole offline set in one shot and check for a GREEN verdict:

```sh
bash scripts/check-firewall-battery.sh
```

The gate list itself is not repeated here — it changes, and a stale copy in a contributor-facing
file is worse than no copy. Two places carry it:

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#ci-and-pre-commit-gate-inventory) — the canonical
  inventory: every gate, its CI job, its script, and what it checks.
- [docs/TESTING.md](docs/TESTING.md) — how to run each one locally and interpret its output.

## Commit message format

Follow conventional commits:

```
feat: <description>
fix: <description>
refactor: <description>
docs: <description>
test: <description>
chore: <description>
```

## Submitting a PR

1. Fork the repository and create a branch from `master`.
2. Make your changes in `shared/`, run sync and all validation scripts locally.
3. Ensure all CI gates pass.
4. Open a PR against `master` with a clear description of what changed and why.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
