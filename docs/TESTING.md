<!-- generated-by: gsd-doc-writer -->
# Testing

This document covers all validation scripts, the routing battery, pre-commit gates, and CI gates for the first-principles-skills plugin.

## Quick reference

Run all local checks in sequence:

```sh
python3 scripts/check-body-budget.py
python3 scripts/check-agent.py
python3 scripts/check-links.py
python3 scripts/check-trigger-collisions.py
python3 scripts/check-description-budget.py
python3 scripts/sync-content.py --check
```

Or with `uv`:

```sh
uv run scripts/check-agent.py
uv run scripts/sync-content.py --check
```

## Validation scripts

### `check-body-budget.py` (pre-commit)

Verifies that `first-principles/agents/first-principles.md` does not exceed the 500-line body budget.

```sh
python3 scripts/check-body-budget.py
# Exit 0: within budget
# Exit 1: over budget — reduce shared/spine/SKILL-body.md or agent/ fragments
```

### `check-agent.py` (GATE-01)

Structural integrity check for the assembled agent: frontmatter schema, required fields, disallowedTools, version format, and description constraints.

```sh
python3 scripts/check-agent.py
```

### `check-links.py` (VAL-03)

Scans all relative Markdown links in the `first-principles/` tree and verifies they resolve to existing files.

```sh
python3 scripts/check-links.py
```

### `check-trigger-collisions.py` (VAL-04)

Scans all skill `description` fields for 4-gram collisions — phrases shared between skills that could cause ambiguous routing.

```sh
python3 scripts/check-trigger-collisions.py
```

### `check-description-budget.py` (VAL-05)

Verifies that every skill listing (name + description combined) stays under the 2000-character cap.

```sh
python3 scripts/check-description-budget.py
```

### `sync-content.py --check` (DUAL-04)

Verifies that `shared/` and the generated `first-principles/` tree are in sync. Exits 1 if any file has drifted.

```sh
python3 scripts/sync-content.py --check
# To fix drift:
python3 scripts/sync-content.py --write && git add -u
```

## Routing battery

The routing battery tests whether the agent auto-delegates correctly for a set of prompts. It requires a running `claude` CLI session.

### Catalogs

| File | What it tests |
|------|--------------|
| `tests/routing-catalog.md` | Agent routing — when `first-principles:first-principles` should and should not delegate |
| `tests/sub-skill-routing-catalog.md` | Companion skill routing — when focused-mode skills should trigger |

### Running the battery

```sh
python3 scripts/check-routing.py --catalog tests/routing-catalog.md
python3 scripts/check-routing.py --catalog tests/sub-skill-routing-catalog.md

# Parse-only (no live session needed):
python3 scripts/check-routing.py --dry-run --catalog tests/routing-catalog.md
```

Each prompt gets a fresh `claude -p` session. The script scores DELEGATE / NO-DELEGATE from the `stream-json` event stream.

### Pass thresholds

| Case type | Pass criterion |
|-----------|---------------|
| P-cases (expect DELEGATE) | ≥ 8/10 |
| N-cases (expect NO-DELEGATE) | ≥ 15/17 |

Both thresholds must be met. A single mis-route does not fail the battery — the threshold counts are the criterion.

### Non-determinism note

Routing outcomes vary between sessions, plugin sets, and Claude routing-model versions. Never attribute a single FAIL to one commit without a same-window control run. See `docs/testing-agents-headlessly.md` for the underlying methodology (two-signal detection rule, `--permission-mode bypassPermissions` requirement, jq extraction strategies).

## Pre-commit gates

Two gates fire on every `git commit` when either hook mechanism is active:

1. **Body-budget gate** — blocks if `first-principles/agents/first-principles.md` exceeds 500 lines
2. **Sync-drift gate** — blocks if `shared/` and the generated tree have drifted

Install with `./scripts/install-hooks.sh` (recommended) or `git config core.hooksPath .githooks`. See [DEVELOPMENT.md](DEVELOPMENT.md) for setup details.

Bypass: `git commit --no-verify`

## CI gates

All gates run in `.github/workflows/validation.yml` on push/PR to master:

| Gate ID | Job | Script | What it checks |
|---------|-----|--------|----------------|
| VAL-01 | plugin-validate | `claude plugin validate` | Plugin schema validity |
| VAL-02 | markdownlint | `markdownlint-cli2` | MD style across `first-principles/**/*.md` |
| VAL-03 | check-links | `check-links.py` | Relative MD links resolve |
| VAL-04 | check-trigger-collisions | `check-trigger-collisions.py` | No 4-gram collision across skills |
| VAL-05 | check-description-budget | `check-description-budget.py` | All skill listings under 2000-char cap |
| DUAL-04 | sync-check | `sync-content.py --check` | `shared/` and generated tree in sync |
| GATE-01 | check-agent | `check-agent.py` | Agent structural checks |

All gates must pass before a PR can merge.

## See also

- [docs/testing-agents-headlessly.md](testing-agents-headlessly.md) — methodology behind the routing battery
- [DEVELOPMENT.md](DEVELOPMENT.md) — standard editing loop and contributor workflow
- [CONFIGURATION.md](CONFIGURATION.md) — gate configuration options
