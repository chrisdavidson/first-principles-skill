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

This is the canonical loop; `CONTRIBUTING.md` points here rather than keeping its own copy.

```sh
# 1. Edit files under shared/ — never first-principles/
# 2. Regenerate the plugin tree
python3 scripts/sync-content.py --write     # or: uv run scripts/sync-content.py --write

# 3. Run every offline gate in one shot; expect FIREWALL: GREEN
bash scripts/check-firewall-battery.sh

# 4. Commit
git add -u && git commit
```

Step 3 replaces the habit of running a hand-picked list of scripts. A hand-picked list goes
stale — it silently omits gates added later, and keeps naming ones that were retired — whereas
the battery is the set that actually runs. When you need a single gate rather than all of them,
[TESTING.md](TESTING.md) has each one's invocation.

For a faster inner loop while iterating, the two that catch most mistakes are:

```sh
python3 scripts/sync-content.py --check     # DUAL-04: no drift
python3 scripts/check-agent.py              # GATE-01: agent structure
```

## How your edit reaches a session — and how it silently fails to

Regenerating `first-principles/` does **not** mean a Claude Code session will load what you just
wrote. Getting this wrong is invisible: sessions keep running months-old code and report success.

### The trap: the plugin cache is version-pinned, not content-tracked

`claude plugin install` copies the plugin into
`~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` as a **snapshot** — including when the
marketplace source is a local filesystem path. Both refresh commands are **version-gated, not
content-gated**:

| Command | What it reports | Does it resync the cache? |
|---|---|---|
| `claude plugin marketplace update <mkt>` | "Successfully updated" | **No** |
| `claude plugin update <plugin>@<mkt>` | "already at the latest version" | **No** |

Verified 2026-07-27 by appending a marker to a file in the working tree and running both: each
reported success and neither changed the cached copy.

**So an edit to `shared/`, synced and committed, never reaches a session unless you also bump
`version` in both `first-principles/.claude-plugin/plugin.json` and
`.claude-plugin/marketplace.json`.** This is not theoretical — it is how an install sat on **3.8.0
from 2026-06-08 while the working tree was at 8.6.0**: eleven skills instead of thirteen, missing
`/estimate` and `/theoretical-limit`, and an agent description two generations stale. Both refresh
commands had been reporting success throughout.

### The supported development install

Symlink the plugin root into the skills directory. It loads as `first-principles@skills-dir` with
no cache copy, no version pin, and nothing to refresh — every session reads the working tree:

```sh
ln -s "$PWD/first-principles" ~/.claude/skills/first-principles
claude plugin list        # expect: first-principles@skills-dir ... Status: loaded
```

Restart the session to pick it up. Two cautions:

- **Do not symlink inside the plugin cache.** The cache has a garbage collector (it marks
  directories with `.in_use` and `.orphaned_at`) that reaps a symlink placed there, leaving the
  install record pointing at a path that no longer exists.
- **A later `claude plugin update` that does find a newer version replaces the symlink with a real
  directory.** Re-create it if that happens.

For a one-off session without installing anything:

```sh
claude --plugin-dir ./first-principles
```

### Record the loaded version in live-measurement artifacts

Any record of a live run — routing battery, Step 0 harness, quality harness — should state the
plugin version and install surface the session actually loaded. A stale surface is otherwise
indistinguishable from a real result, and supplies a plausible wrong explanation that costs time
to rule out. This happened during the investigation in
`dispatch-attribution-findings.md`: the stale install had to be
eliminated as a confound before the real finding could be trusted.

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
| `check-version-stamps.py` | VERSION-01 | `python3 scripts/check-version-stamps.py` | Every hand-maintained version stamp carries the same value; run `--self-test` for the fault-injection fixtures |
| `check-body-budget.py` | report-only | `python3 scripts/check-body-budget.py` | Reports the agent body's current line count; gate retired under TEARDOWN-01 (`docs/v8.7-constraint-teardown.md`) |

### Measurement and routing gates

| Script | Gate | Command | Notes |
|--------|------|---------|-------|
| `check-routing.py` | (developer tool) | `python3 scripts/check-routing.py --catalog tests/routing-catalog.md --repeat 5 --min-pass 3` | Main-agent DELEGATE / NO-DELEGATE routing battery. **Not wired into CI** — developer tool only. |
| `check-routing-battery.py` | BATT-06 | `python3 scripts/check-routing-battery.py --repeat 5 --min-pass 3` / `python3 scripts/check-routing-battery.py --self-test` | Merged dual-signal battery (boundary + focused-output). `--self-test` is the BATT-06 CI gate (offline, deterministic). |
| `check-step0-emulator.py` | STEP0-08 | `python3 scripts/check-step0-emulator.py --self-test` | Offline Step 0 phrase-detection classifier (no live Claude session). STEP0-08 CI gate. |
| `check-step0-live.py` | STEP0-06 | `python3 scripts/check-step0-live.py --self-test` (CI) / `python3 scripts/check-step0-live.py --repeat 5 --min-pass 3` (full manual, 60 invocations) | Live Step 0 harness via approach-② bypass channel. `--self-test` is STEP0-06 CI gate. Full manual run requires a live Claude session. |
| `check-traceability.py` | TRACE-03 | `python3 scripts/check-traceability.py --self-test` | Traceability matrix gate. `emit` subcommand regenerates `docs/requirements-matrix.md`. |

**Retired shims.** Retired at the 2026-08-16 audit ([`audit-2026-08-16-duplication-staleness.md`](audit-2026-08-16-duplication-staleness.md)): the two deprecated shims `check-sub-skill-routing.py` and `check-focused-output.py`, plus `check-inventory.py`. Call `check-routing-battery.py` directly, with its namespaced `--boundary-*` / `--focused-*` threshold flags.

**Internal helpers** (underscore-prefixed, not directly invoked):

- `_battery_core.py` — battery core logic; home of `MIN_HEADER_HITS=2` and `_COMPOSER_FOCUS_CEILING=4` constants and the `self_test_boundary()` sentinels. The ceiling's freeze on retuning was released under TEARDOWN-02 (`docs/v8.7-constraint-teardown.md`); its value stays 4.
- `_skill_io.py` — shared I/O utilities for skill validation scripts

## Pre-commit hooks

One gate fires on `git commit`: the **sync-drift gate**, which blocks if `shared/` and the
generated tree have diverged. Install it with either mechanism — **never both**, they are
mutually exclusive at the Git level:

```sh
./scripts/install-hooks.sh          # Option A (recommended)
git config core.hooksPath .githooks # Option B
git commit --no-verify              # bypass, for intentional in-progress work
```

What each mechanism does to an existing hook, and why the body-budget gate no longer runs
alongside the sync-drift gate, is in
[CONFIGURATION.md#pre-commit-hooks](CONFIGURATION.md#pre-commit-hooks). For what each CI gate
checks, see [TESTING.md](TESTING.md).

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
- The agent body (`first-principles/agents/first-principles.md`)'s line count is reported (not enforced) by `scripts/check-body-budget.py` — the 644-line gate was retired under TEARDOWN-01; see [`docs/v8.7-constraint-teardown.md`](v8.7-constraint-teardown.md).

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
