<!-- generated-by: gsd-doc-writer -->
# Testing

This document covers how to run every CI gate and the two pre-commit gates locally (including offline `--self-test` modes), the anti-masking measurement invariants, and what each pre-commit gate checks.

For the full at-a-glance gate inventory — every gate mapped to its owning script and job name — see [docs/ARCHITECTURE.md#ci-and-pre-commit-gate-inventory](ARCHITECTURE.md#ci-and-pre-commit-gate-inventory).

## CI gates — operational run-detail

All CI gates run in `.github/workflows/validation.yml` on push/PR to master. Run them locally before pushing.

### VAL-01 — plugin-validate

Validates the plugin schema. Requires the Claude Code CLI.

```sh
claude plugin validate ./first-principles
```

### VAL-02 — markdownlint

Checks Markdown style across `first-principles/**/*.md` using `.markdownlint.jsonc` rules.

```sh
# CI uses the markdownlint-cli2-action; run locally:
npx markdownlint-cli2 "first-principles/**/*.md"
```

### VAL-03 — check-links

Scans all relative Markdown links in the `first-principles/`, `shared/`, and `docs/` trees and verifies they resolve to existing files. For `docs/` links, anchor targets are also validated against the target heading's github-slugger slug (em-dash headings produce double-hyphen anchors). `docs/-prefixed` links inside `docs/` are flagged as CF-04 violations. `docs/history/**` is excluded (frozen archives).

```sh
python3 scripts/check-links.py
```

### VAL-04 / GATE-02 — check-trigger-collisions

Scans all skill `description` fields for 4-gram collisions (shared phrases that could cause ambiguous routing). In CI, the `--self-test` fixture runs first, then the live scan.

```sh
python3 scripts/check-trigger-collisions.py --self-test   # offline fixture
python3 scripts/check-trigger-collisions.py               # live scan
```

### VAL-05 — check-description-budget

Verifies that every skill listing (name + description combined) stays under the 2000-character cap.

```sh
python3 scripts/check-description-budget.py
```

### DUAL-04 — sync-check

Verifies that `shared/` and the generated `first-principles/` tree are in sync. Exit 1 on any drift. This is the pre-commit sync-drift gate run on every commit and also wired into CI.

```sh
python3 scripts/sync-content.py --check
# To fix drift:
python3 scripts/sync-content.py --write && git add -u
```

### GATE-01 — check-agent

Structural integrity check for the assembled agent: frontmatter schema, required fields, `disallowedTools`, version format, and description constraints. In CI, the `--self-test` fixture runs first, then the live file check.

```sh
python3 scripts/check-agent.py --self-test                                         # offline fixture
python3 scripts/check-agent.py --file first-principles/agents/first-principles.md  # live check
```

### BATT-06 — check-routing-battery

Merged dual-signal routing battery — captures each prompt in `tests/routing-battery-catalog.md` once and scores both the boundary-discipline signal and the focused-output signal. In CI only the offline `--self-test` runs; the full live battery is a developer tool.

```sh
# CI gate (offline, deterministic — no live Claude session):
python3 scripts/check-routing-battery.py --self-test

# Full live run (developer tool — requires a running Claude session):
python3 scripts/check-routing-battery.py --catalog tests/routing-battery-catalog.md --repeat 5 --min-pass 3
```

The `--self-test` mode exercises the boundary and focused-output fixture suites from `scripts/_battery_core.py`, including the anti-masking sentinels (see [Anti-masking measurement invariants](#anti-masking-measurement-invariants) below).

### STEP0-08 — check-step0-emulator

Offline Step 0 phrase-detection classifier. Reads the `**Phrase detection rules**` table from `shared/spine/SKILL-body.md`, compiles each trigger phrase into a deterministic regex classifier, and classifies a prompt to `MODE` (`focused-<technique>` or `full-composer`). No live Claude session required.

```sh
python3 scripts/check-step0-emulator.py --self-test
```

The `--self-test` mode runs two fixture categories: fault-injection fixtures (D-05 corruption modes) and the full `tests/step0-fixture-catalog.md` classification suite.

### STEP0-06 — check-step0-live

Live Step 0 harness. Forces invocation of the agent body via the approach-② bypass channel against a running `claude` session. Classifies each run's `MODE` from the captured stream.

```sh
# CI gate (offline deterministic self-test — no live Claude invoked):
python3 scripts/check-step0-live.py --self-test

# Full live run (manual only — 60 invocations, requires a live Claude session):
python3 scripts/check-step0-live.py --catalog tests/step0-fixture-catalog.md --repeat 5 --min-pass 3
```

The offline `--self-test` asserts the scoring and parsing logic without invoking Claude. The full live run against `tests/step0-fixture-catalog.md` is the canonical manual baseline (see `tests/step0-baseline-v6.4.md`).

### TRACE-03 — check-traceability

Traceability matrix gate. The `--self-test` mode runs in-process fixtures and named sentinels with no disk I/O beyond the script itself.

```sh
python3 scripts/check-traceability.py --self-test
```

To regenerate the capability → requirement → test matrix:

```sh
python3 scripts/check-traceability.py emit \
    --md-output docs/requirements-matrix.md \
    --json-output .planning/phases/82-traceability-matrix-and-gap-findings/matrix.json
```

## Routing battery (developer tools — not in CI)

Two developer tools let you run live routing batteries against a Claude session. Neither is wired into CI.

**Main-agent routing battery** — tests DELEGATE / NO-DELEGATE routing for the orchestrating agent:

```sh
python3 scripts/check-routing.py --catalog tests/routing-catalog.md --repeat 5 --min-pass 3
python3 scripts/check-routing.py --dry-run --catalog tests/routing-catalog.md   # parse-only, no live session
```

**Merged dual-signal battery (live run)** — see BATT-06 above for the `check-routing-battery.py` live invocation.

Routing outcomes vary between sessions, plugin sets, and Claude routing-model versions. Never attribute a single FAIL to one commit without a same-window control run. Each prompt gets a fresh `claude -p` session.

**Deprecated shims** (delegate to `check-routing-battery.py` — do not use for new invocations):

- `scripts/check-sub-skill-routing.py`
- `scripts/check-focused-output.py`

## Pre-commit gates

Two gates fire on every `git commit` when a hook mechanism is installed. For how to install the hooks, see [docs/DEVELOPMENT.md](DEVELOPMENT.md).

### Body-budget gate

**Owning script:** `scripts/check-body-budget.py`

Blocks the commit if `first-principles/agents/first-principles.md` exceeds 500 lines. The limit is a hard-coded constant (`MAX_LINES: int = 500` in the script) — changing it requires a code edit plus commit.

```sh
python3 scripts/check-body-budget.py           # check the live agent body
python3 scripts/check-body-budget.py --self-test  # run offline pass/fail fixtures
```

If the gate trips, reduce `shared/spine/SKILL-body.md` or the `shared/agent/` phase fragments before committing.

### Sync-drift gate

**Owning script:** `scripts/sync-content.py --check`

Blocks the commit if `shared/` and the generated `first-principles/` tree have diverged. This is the same check as CI gate DUAL-04 — it fires before the commit to catch drift locally.

```sh
python3 scripts/sync-content.py --check    # detect drift
python3 scripts/sync-content.py --write    # fix drift (regenerate)
```

**Bypass** for intentional in-progress work:

```sh
git commit --no-verify
```

## Anti-masking measurement invariants

The routing battery's focused-output scoring depends on two constants in `scripts/_battery_core.py`:

```
MIN_HEADER_HITS: int = 2       # scripts/_battery_core.py, line 1393
_COMPOSER_FOCUS_CEILING: int = 4   # scripts/_battery_core.py, line 1415
```

**`MIN_HEADER_HITS=2`** — the minimum number of distinct technique-category header hits required for the battery to classify an output as a focused single-technique response. An output must match at least two distinct headers from the technique's category set; a single incidental match does not trigger focused-mode classification. This prevents false-positive focused classifications from incidental prose matches.

**`_COMPOSER_FOCUS_CEILING=4`** — the threshold above which the battery classifies an output as full-composer rather than focused single-technique. An output scoring four or more composer-structure hits is classified `full-composer`; an output scoring fewer hits may still be classified as focused if the single-technique signal is strong enough. This ceiling distinguishes a focused output that touches a few structural elements from a full multi-technique composition.

Both constants are locked by the `self_test_boundary()` sentinels inside `scripts/_battery_core.py`, which run as part of the BATT-06 `--self-test` CI gate. Any edit to either constant will trip those sentinels. Do not change these values without understanding the full downstream impact on the battery classification logic.

## Quick reference

Run all offline gates locally in sequence:

```sh
python3 scripts/check-body-budget.py
python3 scripts/check-agent.py --self-test
python3 scripts/check-agent.py --file first-principles/agents/first-principles.md
python3 scripts/check-links.py
python3 scripts/check-trigger-collisions.py --self-test
python3 scripts/check-trigger-collisions.py
python3 scripts/check-description-budget.py
python3 scripts/sync-content.py --check
python3 scripts/check-routing-battery.py --self-test
python3 scripts/check-step0-emulator.py --self-test
python3 scripts/check-step0-live.py --self-test
python3 scripts/check-traceability.py --self-test
```

Or with `uv` (auto-resolves Python deps):

```sh
uv run scripts/sync-content.py --check
uv run scripts/check-agent.py --file first-principles/agents/first-principles.md
```

## See also

- [docs/ARCHITECTURE.md#ci-and-pre-commit-gate-inventory](ARCHITECTURE.md#ci-and-pre-commit-gate-inventory) — full gate inventory (canonical source)
- [docs/DEVELOPMENT.md](DEVELOPMENT.md) — pre-commit hook install paths and standard editing loop
- [docs/CONFIGURATION.md](CONFIGURATION.md) — frontmatter invariants and plugin configuration
- [docs/testing-agents-headlessly.md](testing-agents-headlessly.md) — methodology behind the routing battery (two-signal detection, `--permission-mode bypassPermissions`)
