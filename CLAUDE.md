# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Claude Code **plugin** that ships a first-principles analysis agent (`first-principles:first-principles`) plus eleven standalone slash-invocable companion skills (pre-mortem, inversion, fishbone, five-whys, trade-off, second-order, identify-essence, challenge-assumptions, ground-truths, reason-upward, validate). The entire deliverable is pure Markdown — no executable code ships inside the plugin.

## Commands

### Sync generated files from canonical source

```sh
python3 scripts/sync-content.py --write   # regenerate all target files
python3 scripts/sync-content.py --check   # verify no drift (exit 1 on drift)
uv run scripts/sync-content.py --write    # uv alternative (auto-resolves deps)
```

### Validation scripts (all need Python ≥ 3.12 + PyYAML)

```sh
python3 scripts/check-agent.py            # GATE-01: agent structural checks
python3 scripts/check-links.py            # VAL-03: broken relative MD links
python3 scripts/check-trigger-collisions.py  # VAL-04: 4-gram collision scan across skills
python3 scripts/check-description-budget.py  # VAL-05: skill listing under 2000-char ceiling
python3 scripts/check-body-budget.py      # pre-commit body budget (500-line limit)
```

### Routing battery (requires a running Claude Code session)

```sh
python3 scripts/check-routing-battery.py --catalog tests/routing-battery-catalog.md --repeat 5 --min-pass 3
python3 scripts/check-routing-battery.py --self-test   # offline deterministic gate
# Deprecated shims (delegate to check-routing-battery.py):
python3 scripts/check-sub-skill-routing.py --catalog tests/routing-battery-catalog.md --repeat 5 --min-pass 3
python3 scripts/check-focused-output.py --catalog tests/routing-battery-catalog.md --repeat 5 --min-pass 3 --p-threshold 4 --n-threshold 1
python3 scripts/check-routing.py --catalog tests/routing-catalog.md
python3 scripts/check-routing.py --dry-run --catalog tests/routing-catalog.md  # parse only
```

### Step 0 measurement harness (commands)

```sh
# Live manual full run — 60 live claude invocations (manual only, not run in CI).
# Run from the repo root so the relative --catalog path resolves. Baseline: tests/step0-baseline-v5.0.md
python3 scripts/check-step0-live.py --catalog tests/step0-fixture-catalog.md --repeat 5 --min-pass 3

# Live harness offline self-test — STEP0-06 CI gate (no live claude session)
python3 scripts/check-step0-live.py --self-test

# Offline emulator self-test — STEP0-08 CI gate (no live claude session; no heavy manual run)
python3 scripts/check-step0-emulator.py --self-test
```

### Plugin validation (CI equivalent, requires `claude` CLI)

```sh
claude plugin validate ./first-principles
```

### Install pre-commit hooks

```sh
./scripts/install-hooks.sh        # body-budget + sync-drift gates in .git/hooks/pre-commit
# OR:
git config core.hooksPath .githooks   # same gates via .githooks/pre-commit
# (do not use both — they are mutually exclusive at the Git level)
```

## Architecture

### Source-of-truth vs. generated surface

**Edit `shared/` only. Never edit the generated tree directly.**

```
shared/                         ← canonical source (edit here)
  spine/
    SKILL-body.md               ← assembled agent body template; {{TOOL:slug}} tokens
    SKILL.meta.yml              ← frontmatter for the agent
    tool-map.yml                ← slug → inline name mapping for token substitution
    references/
      output-template.md        ← inlined into agent body by sync-content.py
      validation-rubric.md      ← inlined into agent body by sync-content.py
  agent/                        ← phase-procedure fragments stitched into the agent body
  references/                   ← companion tool reference files (five-whys.md, etc.)
  examples/                     ← worked-example source files
  skills/<slug>/SKILL.md        ← source for each focused-mode slash skill

first-principles/               ← generated plugin (committed, never hand-edited)
  agents/first-principles.md    ← assembled agent (sync-content.py output)
  agents/references/            ← verbatim copies of shared/references/ + spine refs
  agents/references/examples/   ← verbatim copies of shared/examples/
  skills/<slug>/SKILL.md        ← generated stubs from shared/skills/<slug>/SKILL.md
  README.md
  LICENSE
```

`scripts/sync-content.py --write` reads `shared/` and regenerates the entire `first-principles/agents/` tree and all `first-principles/skills/*/SKILL.md` files. It stamps every generated file with a `<!-- GENERATED — DO NOT EDIT -->` marker.

### Token substitution in SKILL-body.md

`{{TOOL:slug}}` tokens in `shared/spine/SKILL-body.md` are replaced by the `## Procedure` section extracted from `shared/references/<slug>.md`. This inlines the companion technique procedures directly into the agent body at generation time.

`{{PROCEDURE:slug}}` tokens in `shared/skills/<slug>/SKILL.md` are replaced by the full body of `shared/references/<slug>.md` (from `## When to reach for this` onward) when generating the focused-mode skill stubs.

### Plugin layout and skill registration

The plugin root is `first-principles/`. The agent is registered at `first-principles/agents/first-principles.md`. The eleven companion skills live under `first-principles/skills/<slug>/SKILL.md` and are registered with `disable-model-invocation: true` (slash-only; the orchestrator never auto-routes to them).

Install for development: `claude --plugin-dir ./first-principles`

### CI gates

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
| STEP0-08 | `check-step0-emulator.py --self-test` | Offline Step 0 phrase-detection classifier self-test (deterministic, no live session) |
| STEP0-06 | `check-step0-live.py --self-test` | Offline Step 0 live-harness self-test — scoring/parsing logic asserted with no live `claude` session (deterministic, mirrors STEP0-08 pattern) |

### Pre-commit gates

Two gates fire on `git commit` (whichever hook mechanism is active):
1. **Body-budget gate** — blocks if `first-principles/agents/first-principles.md` would exceed 500 lines
2. **Sync-drift gate** — blocks if `shared/` and the generated tree have diverged

Bypass for intentional in-progress work: `git commit --no-verify`

### Routing battery

Two verifiers cover different layers of routing correctness. All issue prompts from a catalog file against a live `claude -p` session (one fresh session per prompt, sequential) and score verdicts from the `stream-json` event stream. Routing is non-deterministic — threshold K-of-N counts are the criterion, not per-run pass/fail.

**`check-routing.py`** — main agent routing battery. Scores DELEGATE / NO-DELEGATE. Pass thresholds: P-cases ≥ 8/10 DELEGATE **and** N-cases ≥ 15/17 NO-DELEGATE.

**`check-routing-battery.py`** — merged dual-signal battery. Captures each prompt once from `tests/routing-battery-catalog.md` and scores BOTH the boundary-discipline signal AND the focused-output signal (FU-21 gate, FOCUS-01) from the same stream, with a both-match per-prompt verdict. Namespaced thresholds default: boundary `--p-threshold 2`; focused-output `--p-threshold 4 --n-threshold 1`. Supports `--self-test` for an offline, deterministic self-check with no live claude session (BATT-06 CI gate).

`check-sub-skill-routing.py` and `check-focused-output.py` are **deprecated thin shims** that translate the old per-script flags onto the merged battery and forward to `check-routing-battery.py`. They exist for backward compatibility only; new callers should invoke `check-routing-battery.py` directly.

Catalog fixtures: `tests/routing-catalog.md` (main agent routing battery), `tests/routing-battery-catalog.md` (merged boundary + focused-output battery).

See also: [Step 0 measurement harness](#step-0-measurement-harness) for the two-layer Step 0 classifier measurement tools that sit below the routing layer.

## Step 0 measurement harness

Two tools measure the agent body's Step 0 technique-selection logic, at different layers. They complement the routing battery (see [Routing battery](#routing-battery)) and each other.

**`scripts/check-step0-emulator.py`** — offline Step 0 phrase-detection emulator. Reads the `**Phrase detection rules**` table from `shared/spine/SKILL-body.md`, compiles each trigger phrase into a deterministic regex classifier, and classifies an input prompt to `MODE` (`focused-<technique>` or `full-composer`). No live `claude` session required. `--self-test` runs fault-injection fixtures (D-05 corruption modes) and the full `tests/step0-fixture-catalog.md` classification suite; it is the **STEP0-08 CI gate**. There is no heavy manual run — `--self-test` is the only supported batch mode.

**`scripts/check-step0-live.py`** — live Step 0 agent-body harness. Forces invocation of the agent body against the verbatim oblique prompt via the approach-② `_wrap_for_bypass` bypass channel, over the Plan-36-locked `claude -p --output-format stream-json --verbose` transport. Classifies each run's `MODE` from the captured `.jsonl` stream using `_classify_mode` (with the harness-side `none`→`full-composer` inference fix — D-01/D-02). Scores K-of-N results across the 12-row `tests/step0-fixture-catalog.md`. The full manual run uses `--repeat 5 --min-pass 3` (60 live `claude` invocations — manual only, not run in CI); the canonical baseline is `tests/step0-baseline-v5.0.md`. Its offline `--self-test` (no `claude` invocation) is the **STEP0-06 CI gate**.

### Measurement comparison

| Tool | Measured layer | Run command | CI gate |
|------|---------------|-------------|---------|
| `check-routing.py` | Main-agent DELEGATE / NO-DELEGATE routing boundary | `--catalog tests/routing-catalog.md --repeat 5 --min-pass 3` | None — developer tool, not wired into `validation.yml` |
| `check-routing-battery.py` | Merged dual-signal: boundary + focused-output (FU-21 gate, FOCUS-01) | `--repeat 5 --min-pass 3` / offline `--self-test` | BATT-06 |
| `check-step0-emulator.py` | Offline Step 0 phrase-detection classifier (deterministic, no live session) | `--self-test` | STEP0-08 |
| `check-step0-live.py` | Live Step 0 MODE classification via approach-② bypass channel | Manual `--repeat 5 --min-pass 3` (60 invocations) / offline `--self-test` | STEP0-06 |

### Key invariants

- All reference file links use forward slashes and are one level deep from the file that references them (never nested `a.md → b.md → c.md`).
- Skill `name` in frontmatter must match the parent directory name exactly.
- Skill `description` fields must be third-person, ≤ 1,024 chars, no XML tags.
- `metadata.version` must be a double-quoted YAML string (e.g. `version: "3.8"`), not a bare number.
- Reserved words `anthropic` and `claude` are forbidden in skill `name` fields.
