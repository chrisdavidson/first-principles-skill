# Data Flow: From Source Edit to Shipped, Gated Artifact

This guide traces the full lifecycle of a change through the system — from editing a file in `shared/` to a verified, gate-passing artifact in the generated `first-principles/` plugin. Each stage summarises the connection and links to the canonical home for detail; it does not re-derive facts those documents own.

## Stage 1 — Canonical source (`shared/`)

Everything you edit lives under `shared/`. The generated `first-principles/` tree carries a `<!-- GENERATED — DO NOT EDIT -->` marker on every file; edits made there are overwritten on the next sync run and caught by the pre-commit drift gate.

- For the full inventory of what lives where in `shared/` (spine, references, skills, examples), see [DEVELOPMENT.md#what-lives-where-in-shared](DEVELOPMENT.md#what-lives-where-in-shared).
- For the authoritative source-of-truth vs. generated surface layout, see [ARCHITECTURE.md#source-of-truth-vs-generated-surface](ARCHITECTURE.md#source-of-truth-vs-generated-surface).
- For the core rule and standard editing loop, see [DEVELOPMENT.md#core-rule-edit-shared-only](DEVELOPMENT.md#core-rule-edit-shared-only) and [DEVELOPMENT.md#standard-editing-loop](DEVELOPMENT.md#standard-editing-loop).

## Stage 2 — Generation (`scripts/sync-content.py`)

Running `python3 scripts/sync-content.py --write` reads `shared/` and regenerates the entire `first-principles/agents/` tree (the agent body, its `references/` siblings, and the worked examples) and all `first-principles/skills/*/SKILL.md` stubs. Running `--check` instead performs a dry-run comparison and exits with code 1 on any drift.

The non-obvious wiring this stage introduces is **token substitution** — two token types expand inline content from `shared/references/` at generation time:

| Token | Source file | Replaced by |
|-------|-------------|-------------|
| `{{TOOL:slug}}` | `shared/spine/SKILL-body.md` | `## Procedure` section from `shared/references/<slug>.md` |
| `{{PROCEDURE:slug}}` | `shared/skills/<slug>/SKILL.md` | Full body of `shared/references/<slug>.md` from `## When to reach for this` onward |

These token-substitution edges mean that editing a companion reference file (e.g. `shared/references/inversion.md`) propagates its content into both the assembled agent body (via `{{TOOL:inversion}}` in `SKILL-body.md`) and the focused-mode skill stub (via `{{PROCEDURE:inversion}}` in the skill source file). A reader inspecting the generated files alone will not see the composition seams — they exist only in `shared/`.

For the canonical description of the assembly steps and token types, see [ARCHITECTURE.md#generation-pipeline](ARCHITECTURE.md#generation-pipeline) and [ARCHITECTURE.md#token-substitution](ARCHITECTURE.md#token-substitution).

## Stage 3 — Generated plugin (`first-principles/`)

After `--write` completes, the generated plugin tree is ready for installation and use:

- **Orchestrating agent:** `first-principles/agents/first-principles.md` — the fully assembled agent body, including all inlined technique procedures and the output template.
- **Reference siblings:** `first-principles/agents/references/` — verbatim copies of `shared/references/` and the spine reference files.
- **Focused-mode skills:** `first-principles/skills/<slug>/SKILL.md` — generated stubs for all thirteen companion skills, each with its `{{PROCEDURE:slug}}` token already expanded.

Install the plugin for development with:

```sh
claude --plugin-dir ./first-principles
```

For the plugin registration details and the full companion skill slug list, see [ARCHITECTURE.md#plugin-layout-and-registration](ARCHITECTURE.md#plugin-layout-and-registration).

## Stage 4 — Gates (CI + pre-commit)

Every `git commit` fires one pre-commit gate locally before the commit lands:

- **Sync-drift gate** — runs `scripts/sync-content.py --check` and blocks if `shared/` and the generated tree have diverged.

A body-budget gate used to run alongside it, blocking a commit that grew the agent body
(`first-principles/agents/first-principles.md`) past 644 lines. It was retired under
TEARDOWN-01 (`docs/v8.7-constraint-teardown.md`, the standing record) —
`scripts/check-body-budget.py` still reports the body's current line count on request, but
it no longer exits nonzero because of the body's size and no longer fires as part of the pre-commit hook; 644 survives only as a
historical reference figure inside the script.

The sync-drift gate is also the CI gate **DUAL-04** (`sync-check`), which closes the loop on Stage 2: it is the mechanism that enforces the `--write`/`--check` contract at both commit time and on every push or PR. If a developer edits `shared/` and skips the `--write` step, DUAL-04 fails.

On push or PR to master, the full CI suite runs in `.github/workflows/validation.yml`:

| Gate | What it guards |
|------|---------------|
| VAL-01 | Plugin schema validity |
| VAL-02 | Markdown style |
| VAL-03 | Relative link resolution (plugin + shared trees) |
| VAL-04 / GATE-02 | No 4-gram collision across skill descriptions |
| COLLIDE-01 | No skill/agent name collisions between plugin and monolith install surfaces |
| VAL-05 | Skill listings under 2000-char cap |
| DUAL-04 | `shared/` and generated tree in sync |
| GATE-01 | Agent structural integrity |
| STEP0-06 | Step 0 live-harness scoring/parsing self-test |
| STEP0-08 | Offline Step 0 phrase-detection classifier self-test |
| BATT-06 | Merged dual-signal routing battery self-test (anti-masking sentinels) |
| TRACE-03 | Traceability matrix gate self-test |

For the full canonical gate inventory (script names, job IDs, what each checks), see [ARCHITECTURE.md#ci-and-pre-commit-gate-inventory](ARCHITECTURE.md#ci-and-pre-commit-gate-inventory). For how to run each gate locally and interpret results, see [TESTING.md#ci-gates--operational-run-detail](TESTING.md#ci-gates--operational-run-detail) and [TESTING.md#pre-commit-gates](TESTING.md#pre-commit-gates).

## Stage 5 — Measurement harness

Once the agent body is shipped (generated and gate-passing), the measurement harness operates on it. The routing battery, two-layer Step 0 harness, and traceability matrix all measure the shipped artifact — they do not change it.

- **Routing battery** (`scripts/check-routing-battery.py`) — merged dual-signal battery scoring DELEGATE/NO-DELEGATE boundary and focused-output signal; BATT-06 CI gate runs its `--self-test`.
- **Step 0 emulator** (`scripts/check-step0-emulator.py`) — offline phrase-detection classifier; reads the `**Phrase detection rules**` table from `shared/spine/SKILL-body.md` and classifies a prompt to `MODE` without a live Claude session (STEP0-08).
- **Step 0 live harness** (`scripts/check-step0-live.py`) — live MODE classification via the approach-② bypass channel against a running `claude` session (STEP0-06 offline self-test).
- **Traceability matrix** (`scripts/check-traceability.py`) — capability → requirement → test matrix; TRACE-03 CI gate.

For the measurement subsystem inventory, see [ARCHITECTURE.md#measurement-subsystem](ARCHITECTURE.md#measurement-subsystem). For the layer-by-layer ownership map — which gate owns which residual, and how the measurement layers relate to each other — see [MEASUREMENT-MAP.md](MEASUREMENT-MAP.md).

## Summary

A single source edit propagates as follows:

```
shared/                     ← edit here (Stage 1)
    ↓  scripts/sync-content.py --write
first-principles/            ← generated plugin (Stage 3)
    ↑  scripts/sync-content.py --check  [DUAL-04 closes this loop]
    ↓  git commit → CI push/PR
Gates (pre-commit + CI)      ← validation suite (Stage 4)
    ↓
Measurement harness          ← routing battery + Step 0 + traceability (Stage 5)
```

Token substitution (Stage 2) is the invisible join: `{{TOOL:slug}}` and `{{PROCEDURE:slug}}` tokens in `shared/` expand to content from `shared/references/<slug>.md` at generation time, so the generated plugin carries the composed output without exposing the composition seams.
