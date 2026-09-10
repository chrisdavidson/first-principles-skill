# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Current shipped version: see `.claude-plugin/marketplace.json` (all 17 version stamps move in
lockstep — VERSION-01 enforces it). For what changed in any milestone, read the tag table and
entries in [`CHANGELOG.md`](CHANGELOG.md). This file describes the repo as it stands and does
not track release history — where it names a milestone below, that is a current-state fact
carrying its provenance, not a changelog entry.

A Claude Code **plugin** that ships a first-principles analysis agent (`first-principles:first-principles`) plus fourteen slash-invocable skills: the thirteen companion skills (pre-mortem, inversion, fishbone, five-whys, trade-off, second-order, estimate, theoretical-limit, identify-essence, challenge-assumptions, ground-truths, reason-upward, validate) and the `first-principles-analysis` launcher. The entire deliverable is pure Markdown — no executable code ships inside the plugin.

## Commands

### Sync generated files from canonical source

```sh
python3 scripts/sync-content.py --write   # regenerate all target files
python3 scripts/sync-content.py --check   # verify no drift (exit 1 on drift)
uv run scripts/sync-content.py --write    # uv alternative (auto-resolves deps)
```

### Validation scripts (Python ≥ 3.12; those that parse frontmatter also need PyYAML — `check-body-budget.py`, `check-install-collisions.py`, `check-quality-harness.py` and `check-provenance.py` are stdlib-only)

```sh
python3 scripts/check-agent.py            # GATE-01: agent structural checks
python3 scripts/check-links.py            # VAL-03: broken relative MD links
python3 scripts/check-trigger-collisions.py  # VAL-04: 4-gram collision scan across skills
python3 scripts/check-description-budget.py  # VAL-05: skill listing under 2000-char ceiling
python3 scripts/check-version-stamps.py   # VERSION-01: all hand-maintained version stamps agree
python3 scripts/check-body-budget.py      # report-only line-count reporter; gate retired under TEARDOWN-01, see docs/v8.7-constraint-teardown.md
python3 scripts/check-install-collisions.py --self-test  # COLLIDE-01: dual-install name-collision self-test
python3 scripts/check-install-collisions.py              # COLLIDE-01: live-tree scan (vacuous if monolith absent)
python3 scripts/check-quality-harness.py --self-test     # QUAL-01: offline blind A/B quality-harness self-test
python3 scripts/check-provenance.py --self-test           # PROV-GUARD: provenance-verifier self-test (33 controls)
python3 scripts/check-provenance.py                        # PROV-GUARD: live coverage check against tests/quality-provenance-v8.24/
python3 scripts/check-conf-gate.py --self-test              # CONF-GATE: exemplar-conformance comparator self-test (43 controls)
python3 scripts/check-conf-gate.py                           # CONF-GATE: live comparator against source-literal conformance targets
```

This list is a convenience, not the authority — a hand-maintained list of gates goes stale by
construction. `bash scripts/check-firewall-battery.sh` runs the set that actually exists.

**pytest is a prerequisite for the full battery, not for any script above.** None of the
scripts listed here need it — it is needed only by VAL-03's third leg, which runs
`scripts/check-links_anchors_test.py` under pytest (`check-links.py` itself has no such
dependency). `scripts/check-firewall-battery.sh` resolves a pytest-capable interpreter itself:
`.venv/bin/python3` first, then `python3`, each confirmed by an `import pytest` preflight.
Run `uv sync` to create `.venv` (it ships pytest), or install pytest for whichever interpreter
`python3` resolves to. If neither interpreter can import pytest, the battery prints
`[PREREQ] VAL-03` and `FIREWALL: BLOCKED`, exiting 2 — distinct from `FIREWALL: RED` / exit 1,
which still means a gate genuinely failed.

### Routing battery (requires a running Claude Code session)

```sh
python3 scripts/check-routing-battery.py --catalog tests/routing-battery-catalog.md --repeat 5 --min-pass 3
python3 scripts/check-routing-battery.py --self-test   # offline deterministic gate
python3 scripts/check-routing.py --catalog tests/routing-catalog.md
python3 scripts/check-routing.py --dry-run --catalog tests/routing-catalog.md  # parse only
```

### Step 0 measurement harness (commands)

```sh
# Live manual full run — 60 live claude invocations (manual only, not run in CI).
# Run from the repo root so the relative --catalog path resolves. Baseline: tests/step0-baseline-v7.8.md
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
./scripts/install-hooks.sh        # sync-drift gate in .git/hooks/pre-commit (body-budget retired under TEARDOWN-01, docs/v8.7-constraint-teardown.md)
# OR:
git config core.hooksPath .githooks   # same sync-drift gate via .githooks/pre-commit
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
      output-template.md        ← emitted as an agent reference sibling, NOT inlined
      validation-rubric.md      ← emitted as an agent reference sibling, NOT inlined
  agent/                        ← phase-procedure fragments stitched into the agent body
  references/                   ← companion tool reference files (five-whys.md, etc.)
  references/<slug>-detail.md   ← v8.5 on-demand appendix siblings (SLUGS_WITH_DETAIL only)
  examples/                     ← worked-example source files
  skills/<slug>/SKILL.md        ← source for each focused-mode slash skill

first-principles/               ← generated plugin (committed, never hand-edited)
  agents/first-principles.md    ← assembled agent (sync-content.py output)
  agents/references/            ← verbatim copies of shared/references/ + spine refs
  agents/references/<slug>-detail.md      ← generated on-demand detail sibling (agent surface)
  agents/references/examples/   ← verbatim copies of shared/examples/
  skills/<slug>/SKILL.md        ← generated stubs from shared/skills/<slug>/SKILL.md
  skills/<slug>/references/<slug>-detail.md  ← generated on-demand detail sibling (skill-stub surface)
  README.md
  LICENSE
```

`scripts/sync-content.py --write` reads `shared/` and regenerates the entire `first-principles/agents/` tree (including the `agents/references/<slug>-detail.md` on-demand siblings) and all `first-principles/skills/*/SKILL.md` files (including each split skill's own `skills/<slug>/references/<slug>-detail.md` sibling). It stamps every generated file with a `<!-- GENERATED — DO NOT EDIT -->` marker.

### Token substitution in SKILL-body.md

`{{TOOL:slug}}` tokens in `shared/spine/SKILL-body.md` are replaced by the phrase held under that slug's `agent` key in `shared/spine/tool-map.yml` — e.g. `{{TOOL:fishbone}}` → "the inlined fishbone procedure". **This substitutes a name, not content.** The companion-technique procedures are *not* inlined into the agent body; they ship as on-demand reference siblings under `first-principles/agents/references/<slug>.md`, and the body's `## Companion tools` summaries are hand-written in `SKILL-body.md`. The substituted phrase says "inlined", which invites the opposite conclusion — read [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md#token-substitution) before reasoning about what the body contains.

`{{PROCEDURE:slug}}` tokens in `shared/skills/<slug>/SKILL.md` are replaced by the full body of `shared/references/<slug>.md` (from `## When to reach for this` onward) when generating the focused-mode skill stubs.

**On-demand `-detail.md` load convention (v8.5 Phase 154):** `SLUGS_WITH_DETAIL` in `scripts/sync-content.py` is the single set of slugs authorised to carry a split `shared/references/<slug>-detail.md` appendix — every core-file `## Procedure` section ends with a named-trigger pointer block that directs the reader to the detail sibling on demand, rather than inlining that content into every emission. The pointer must appear exactly once per core file; the `GATE-02-v8.5` pointer drift-guard gate (see CI gates below) asserts this. Because the assembled agent body and the skill stub each sit one directory level above their own detail sibling, `_rewrite_detail_link()` adapts the pointer's link target to `references/<slug>-detail.md` on those two assembly surfaces, while the agent reference sibling (which lands alongside its own `<slug>-detail.md`) keeps the bare, unrewritten form.

### Plugin layout and skill registration

The plugin root is `first-principles/`. The agent is registered at `first-principles/agents/first-principles.md`. Fourteen skill directories live under `first-principles/skills/<slug>/SKILL.md` — the thirteen companion skills plus the `first-principles-analysis` launcher — all registered with `disable-model-invocation: true` (slash-only; the orchestrator never auto-routes to them).

Install for development: `claude --plugin-dir ./first-principles`

### CI gates

<!-- GENERATED — DO NOT EDIT. Source: scripts/_gate_registry.py. Regenerate via: scripts/gen-gate-docs.py --write. -->
Both surfaces render the same population and the same columns from `scripts/_gate_registry.py`, emitted by `scripts/gen-gate-docs.py --write`, so the two cannot diverge; a working session still sees the full gate list here without opening `docs/`, and per-gate detail lives in `docs/gates/<GATE-ID>.md`. Every gate below except QUAL-01 runs in `.github/workflows/validation.yml` on push/PR to master; QUAL-01 is battery-only — it has no CI job, and `bash scripts/check-firewall-battery.sh` is the only thing that runs it.

| Gate | Job / Mechanism | Script | What it checks |
|------|-----------------|--------|-----------------|
| VAL-01 | `plugin-validate` (CI) | `claude plugin validate` | Plugin manifest schema validity via the `claude` CLI. Spends zero model tokens. Does NOT validate the agent frontmatter — the CLI walks subdirectories of `agents/` and never inspects a flat `agents/*.md`, so GATE-01 is the sole validator of agent frontmatter. See [`docs/gates/VAL-01.md`](docs/gates/VAL-01.md). |
| VAL-02 | `markdownlint` (CI) | `markdownlint-cli2` | MD style across `first-principles/**/*.md` via `markdownlint-cli2`. See [`docs/gates/VAL-02.md`](docs/gates/VAL-02.md). |
| VAL-03 | `check-links` (CI) | `scripts/check-links.py --self-test` | Relative Markdown link validity across the plugin, `shared/`, and `docs/` trees; `docs/` anchors validated with a github-slugger rule. Three legs: self-test, a live scan, and a pytest run of `check-links_anchors_test.py`. The third leg needs a pytest-capable interpreter — when none is found the battery still runs legs 1-2 through `gate_prereq` and reports [PREREQ]/BLOCKED rather than [PASS]/GREEN. (scan_globs=3 entries; locked_constants=2 entries) See [`docs/gates/VAL-03.md`](docs/gates/VAL-03.md). |
| VAL-04 / GATE-02 | `check-trigger-collisions` (CI) | `scripts/check-trigger-collisions.py --self-test` | No 4-gram collision across skill descriptions. Carries the pre-existing v3.0 GATE-02 id alongside VAL-04 — the battery registers this row under `VAL-04` only; `GATE-02` is a name the row also carries, not a second battery registration (see `extra_ids` on this entry, excluded from the D-01 battery-id equality floor by construction). (derived_counts=1 entries) See [`docs/gates/VAL-04.md`](docs/gates/VAL-04.md). |
| VAL-05 | `check-description-budget` (CI) | `scripts/check-description-budget.py` | All skill listings stay under the 2000-character budget cap. (locked_constants=1 entries) See [`docs/gates/VAL-05.md`](docs/gates/VAL-05.md). |
| VERSION-01 | `check-version-stamps` (CI) | `scripts/check-version-stamps.py --self-test` | Every hand-maintained version stamp carries the same value. Runs the live scan as well as the self-test — the invariant is a property of the working tree, not of the script's own fixtures. (derived_counts=1 entries; registered_surfaces=4) See [`docs/gates/VERSION-01.md`](docs/gates/VERSION-01.md). |
| REG-GUARD | `check-registration` (CI) | `scripts/check-registration.py --self-test` | Registration completeness over two surfaces: (a) every skill directory and the main agent carry a frontmatter `name:` matching their own basename; (b) every gate this file's own battery registers has a matching `name: <job> (<GATE-ID>)` job in `.github/workflows/validation.yml`, QUAL-01 the one named battery-only exemption. This module's D-01 floor deliberately reuses `check-registration.py`'s `_BATTERY_GATE_RE` parsing semantics rather than inventing a second grammar over the same file. (control_ids=29; control_count=29; registered_surfaces=2; checked_files=4; locked_constants=1 entries) See [`docs/gates/REG-GUARD.md`](docs/gates/REG-GUARD.md). |
| COLLIDE-01 | `check-install-collisions` (CI) | `scripts/check-install-collisions.py --self-test` | Dual-install name-collision scan: no skill/agent name collisions between the plugin and monolith install surfaces. (registered_surfaces=2; disclosed_bounds_anchors=1) See [`docs/gates/COLLIDE-01.md`](docs/gates/COLLIDE-01.md). |
| DUAL-04 | `sync-check` (CI) | `scripts/sync-content.py --check` | `shared/` and the generated `first-principles/` tree are in sync. (derived_counts=1 entries; registered_surfaces=4; locked_constants=1 entries; control_ids=13; control_count=13) See [`docs/gates/DUAL-04.md`](docs/gates/DUAL-04.md). |
| GATE-02-v8.5 | `GATE-02-v8.5` | `scripts/sync-content.py --self-test` | Pointer drift-guard: each of the four split core reference files' extracted Procedure slice carries exactly one well-formed link to its own `-detail.md` sibling. Proves the pointer exists and is well-formed, NOT that it is followed. Same script as DUAL-04, a different flag — the D-03 case for a flat `--describe` namespace rather than a per-gate id argument. See [`docs/gates/GATE-02-v8.5.md`](docs/gates/GATE-02-v8.5.md). |
| GATE-01 | `check-agent` (CI) | `scripts/check-agent.py --self-test` | Agent structural checks — 8 frontmatter/body assertions on the shipped agent, including the exact `maxTurns` value (60), not merely its presence. The live leg targets the repo-anchored `AGENT_FILE` constant, so the gate is cwd-independent and cannot be silently re-pointed. (branch_roster=8; branch_count=8; scoped_branches=3; locked_constants=3 entries; checked_files=1; disclosed_bounds_anchors=1) See [`docs/gates/GATE-01.md`](docs/gates/GATE-01.md). |
| BATT-06 | `check-routing-battery` (CI) | `scripts/check-routing-battery.py --self-test` | Offline merged dual-signal routing-battery self-test (boundary + focused-output); owns the honest-state and anti-masking sentinels. (locked_constants=4 entries; disclosed_bounds_anchors=11; derived_counts=1 entries; checked_files=1) See [`docs/gates/BATT-06.md`](docs/gates/BATT-06.md). |
| STEP0-08 | `check-step0-emulator` (CI) | `scripts/check-step0-emulator.py --self-test` | Offline Step 0 phrase-detection classifier self-test. (locked_constants=1 entries; derived_counts=2 entries; disclosed_bounds_anchors=6; checked_files=2) See [`docs/gates/STEP0-08.md`](docs/gates/STEP0-08.md). |
| STEP0-06 | `check-step0-live` (CI) | `scripts/check-step0-live.py --self-test` | Offline Step 0 live-harness scoring/parsing logic self-test. (locked_constants=2 entries; checked_files=2; control_ids=25; control_count=25) See [`docs/gates/STEP0-06.md`](docs/gates/STEP0-06.md). |
| TRACE-03 | `check-traceability` (CI) | `scripts/check-traceability.py --self-test` | Offline traceability gate self-test — capability/tier schema, artifact resolution, plus the HEADLINE-LOCK sentinel asserting the published coverage headline against five named current-fact surfaces and both tracked matrix artifacts. (`docs/*.md`, `CLAUDE.md`, `CHANGELOG.md`, `README.md`; registered_surfaces=5; branch_roster=19; branch_count=19; locked_constants=4 entries; coverage_headline=2 entries) See [`docs/gates/TRACE-03.md`](docs/gates/TRACE-03.md). |
| QUAL-01 | battery only — not a CI job | `scripts/check-quality-harness.py --self-test` | Offline blind A/B quality-measurement harness self-test — extraction guardrails, scoreline parsing, blinding, tabulation, baseline-fixture integrity, the mechanical defect detector, and the emission rendering contract's six legs. The single named battery-only CI exemption in REG-GUARD's `BATTERY_ONLY_GATE_IDS`. (control_ids=27; control_count=27; registered_surfaces=4; disclosed_bounds_anchors=30; derived_counts=4 entries; locked_constants=3 entries; contract_pins=3 entries) See [`docs/gates/QUAL-01.md`](docs/gates/QUAL-01.md). |
| PROV-GUARD | `check-provenance` (CI) | `scripts/check-provenance.py --self-test` | Every `read-at-source` ground truth in an analysis's section 3 joins to a real WebFetch/Read of that source in the run's stored capture, and every literal it states appears verbatim in that source's retrieved text. Live leg reads `tests/quality-provenance-v8.24/` and reports 7/7 sources matched, 35/35 literals located. (control_ids=33; control_count=33; registered_surfaces=2; locked_constants=1 entries) See [`docs/gates/PROV-GUARD.md`](docs/gates/PROV-GUARD.md). |
| HARN-01 | `check-act-limb` (CI) | `scripts/check-act-limb.py --self-test` | Offline Act-limb gate: the Phase 3 verification step and the Criterion 3 Fix note are present, correctly placed, and internally coherent in the emitted tree. (branch_roster=16; branch_count=16; control_ids=78; control_count=78; checked_files=2; disclosed_bounds_anchors=4) See [`docs/gates/HARN-01.md`](docs/gates/HARN-01.md). |
| HARN-02 | `check-loop-closure` (CI) | `scripts/check-loop-closure.py --self-test` | Observe->Perceive re-entry edges: a Criterion 1 Absent verdict routes back to Phase 1, every re-entry edge is bounded to one re-perception pass, and a fired edge is recorded. (checked_files=4; control_ids=37; control_count=37) See [`docs/gates/HARN-02.md`](docs/gates/HARN-02.md). |
| HARN-03 | `check-focused-parity` (CI) | `scripts/check-focused-parity.py --self-test` | Focused-mode parity: stub surface, agent surface and cross-surface parity-token set equality, with the D-12 anchor-control ratchet. (locked_constants=2 entries; registered_surfaces=3; disclosed_bounds_anchors=1) See [`docs/gates/HARN-03.md`](docs/gates/HARN-03.md). |
| SCAN-GUARD | `check-selfaudit-scan` (CI) | `scripts/check-selfaudit-scan.py --self-test` | Self-audit scan structural gate: the Phase 15 self-audit scan prescription, its rubric verify block, and the Criterion-2-widened Verdict Block Format admission are present, correctly placed and internally coherent in the emitted tree, with one hundred clause-level named branches floored by an independent transcription (`_BRANCH_ROSTER_LOCK`). (branch_roster=100; branch_count=100; registered_surfaces=2; call_site_census=4 entries; control_ids=12; control_count=12; locked_constants=1 entries) See [`docs/gates/SCAN-GUARD.md`](docs/gates/SCAN-GUARD.md). |
| HC-BOUND | `check-high-confidence-bound` (CI) | `scripts/check-high-confidence-bound.py --self-test` | Structural validation gate: Phase 5 tightening of Criterion 3 (Evidence) and Criterion 5 (Conclusion) HIGH-confidence bound is present and well-formed on both rubric surfaces, and all three documented EXCEPT exceptions are present. (registered_surfaces=2; derived_counts=1 entries; disclosed_bounds_anchors=3) See [`docs/gates/HC-BOUND.md`](docs/gates/HC-BOUND.md). |
| CONF-GATE | `check-conf-gate` (CI) | `scripts/check-conf-gate.py --self-test` | Standing exemplar-conformance comparator: the four conformance counts on both gated example surfaces against source-literal targets, a 14-entry claim floor locked by equality to the live-discovered `shared-examples` ids, the D-03 prescribed-lead-in rule, and the marked-claim ratchet (may fall, never rise). (registered_surfaces=2; population_floors=2 entries; call_site_census=7 entries; control_ids=44; control_count=44; locked_constants=2 entries) See [`docs/gates/CONF-GATE.md`](docs/gates/CONF-GATE.md). |
| INVARIANT-CHECK | battery only (inline) | — | Anti-masking constants still hold in `scripts/_battery_core.py`: pre-mortem=9 fishbone=7 inversion=13 trade-off=10 MIN_HEADER_HITS=2. A direct value-grep double-check of what BATT-06 and STEP0-08 already assert internally. See [`docs/gates/INVARIANT-CHECK.md`](docs/gates/INVARIANT-CHECK.md). |
| FROZEN-EVIDENCE | battery only (inline) | — | Frozen baselines and captures are unmodified relative to HEAD, plus an untracked-files sweep over the same paths. `_FROZEN_PATHS` grows over time; this inline check increments the battery tally once regardless of array length. See [`docs/gates/FROZEN-EVIDENCE.md`](docs/gates/FROZEN-EVIDENCE.md). |
| — | sync-drift gate (pre-commit) | `scripts/sync-content.py --check` | `shared/` and the generated tree are in sync — the same check as DUAL-04, fired before commit rather than in CI/battery. See [`docs/gates/PRECOMMIT-sync-drift-gate.md`](docs/gates/PRECOMMIT-sync-drift-gate.md). |
| — | conformance generator self-test (pre-commit) | `scripts/report-conformance.py --self-test` | Blocks if `scripts/report-conformance.py --self-test` fails. Runs the generator's own falsifiability controls before its output is compared to anything (WR-05) — ordered before `--check` because a generator whose own controls are failing makes that comparison meaningless. See [`docs/gates/PRECOMMIT-conformance-generator-self-test.md`](docs/gates/PRECOMMIT-conformance-generator-self-test.md). |
| — | conformance-baseline drift gate (pre-commit) | `scripts/report-conformance.py --check` | `docs/conformance-baseline.md` and `docs/data/conformance.json` reproduce byte-for-byte a fresh `report-conformance.py` run (D-06); fires before commit. Deliberately not registered in the battery or in CI. (registered_surfaces=5; checked_files=2; control_ids=102; control_count=102; locked_constants=1 entries) See [`docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md`](docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md). |
| — | claim-surface generator self-test (pre-commit) | `scripts/gen-gate-docs.py --self-test` | Blocks if `scripts/gen-gate-docs.py --self-test` fails. Same WR-05 ordering discipline as the conformance generator self-test — a broken generator's own controls must be caught before its comparison against committed output (the claim-surface drift gate) is even attempted. See [`docs/gates/PRECOMMIT-claim-surface-generator-self-test.md`](docs/gates/PRECOMMIT-claim-surface-generator-self-test.md). |
| — | claim-surface drift gate (pre-commit) | `scripts/gen-gate-docs.py --check` | Blocks if `CLAUDE.md`'s/`docs/ARCHITECTURE.md`'s generated gate tables, `docs/TESTING.md`'s generated index, or any `docs/gates/<ID>.md` page no longer match a fresh `scripts/gen-gate-docs.py --write` run, or if CONF-13's standing literal scanner finds a non-exempt hand-maintained count literal — the same check as CONF-SURFACE, fired before commit rather than in CI/battery. See [`docs/gates/PRECOMMIT-claim-surface-drift-gate.md`](docs/gates/PRECOMMIT-claim-surface-drift-gate.md). |
| CONF-SURFACE | `gen-gate-docs` (CI) | `scripts/gen-gate-docs.py --self-test` | The claim-surface drift gate itself: regenerates `CLAUDE.md`'s and docs/ARCHITECTURE.md's gate tables and docs/gates/<ID>.md pages from this registry's ENTRIES and every gate's --describe emission, and fails on drift. Registered in the battery, with a matching `gen-gate-docs (CONF-SURFACE)` CI job and both pre-commit hooks (plan 21-11, D-21-C). (registered_surfaces=40; checked_files=70; derived_counts=29 entries; disclosed_bounds_anchors=8; control_ids=96; control_count=96; locked_constants=2 entries) See [`docs/gates/CONF-SURFACE.md`](docs/gates/CONF-SURFACE.md). |

Gates run on three surfaces: **23 in CI** (`.github/workflows/validation.yml`, on push/PR to master), **26 tallied in the offline battery** (`bash scripts/check-firewall-battery.sh`), and **5 pre-commit gates** (2 hook mechanisms run the identical set in the identical order). The battery is a strict superset of CI: all 23 CI gates plus 1 battery-only gate plus 2 inline checks. That is 23 + 1 + 2 = 26.
<!-- END GENERATED -->

**a guard guards the product; a guard is not itself guarded** — measured justification: the
chain `999.27 → 999.28 → 999.30`. [docs/PROCESS.md](docs/PROCESS.md) holds the full depth rule,
the product/apparatus review split, and the rework cap; cite it, do not restate its rules here.

HARN-01, HARN-02 and HARN-03 were registered under HARN-04 at v8.18.0 — each is a CI job plus a
single `--self-test`-only battery `gate` call, and each is counted in the battery total below. HC-BOUND
was registered at v8.19.0 under Phase 6 (HC-04). REG-GUARD was registered at v8.21.0 under Phase 3 (REG-03).
PROV-GUARD was registered at v8.24.0 under Phase 6 (GATE-02/GATE-03) — a CI job plus a battery `gate`
call running both `--self-test` and the live leg — and is counted in the battery total below.
SCAN-GUARD was registered at v8.26.0 under Phase 15 — a CI job plus a battery `gate` call running
both `--self-test` and the live leg (plan 15-09, closing `15-VERIFICATION.md` gap 2's WR-05
finding), matching PROV-GUARD's and REG-GUARD's shape rather than HARN-01/02/03's and HC-BOUND's
`--self-test`-only shape — and is counted in the battery total below. CONF-SURFACE was registered
at v9.0.0 under Phase 21 (D-21-C, plan 21-11) — a CI job plus a battery `gate` call running
`gen-gate-docs.py --self-test` then `--check` — and is counted in the battery total below.

`bash scripts/check-firewall-battery.sh` runs the full offline gate set — currently **26/26** — in one shot and prints a FIREWALL: GREEN / RED / BLOCKED verdict (SHIP-06: BLOCKED, exit 2, is a third outcome for an unmet external prerequisite — currently only VAL-03's pytest interpreter — and is distinct from a genuine gate failure, RED, exit 1). QUAL-01 (added at v8.7 Phase 164, HARNESS-01) moved the battery from 15 to 16; VERSION-01 (added by the 2026-08-16 audit, [`docs/audit-2026-08-16-duplication-staleness.md`](docs/audit-2026-08-16-duplication-staleness.md)) moved it from 16 to 17; HARN-01/02/03 (added under HARN-04, Phase 4, v8.18.0) moved it from 17 to 20; HC-BOUND (added under HC-04, Phase 6, v8.19.0) moved it from 20 to 21; REG-GUARD (added under REG-03, Phase 3, v8.21.0) moved it from 21 to 22; PROV-GUARD (added under Phase 6, v8.24.0) moved it from 22 to 23; SCAN-GUARD (added under Phase 15, v8.26.0) moved it from 23 to 24. CONF-GATE (added under Phase 18, v9.0.0) moved it from 24 to 25. CONF-SURFACE (added under Phase 21, v9.0.0, D-21-C) moved it from 25 to 26 — generated by this same gate rather than hand-swept, the phase's own demonstration. The tally is 24 `gate`/`gate_prereq` registrations plus two inline checks (INVARIANT-CHECK, FROZEN-EVIDENCE); the body-size `[INFO]` line is deliberately untallied. See [`docs/v8.7-quality-baseline-freeze.md`](docs/v8.7-quality-baseline-freeze.md) and [`docs/v8.7-constraint-teardown.md`](docs/v8.7-constraint-teardown.md) for the milestone's full gate-composition and retired-constraint record.

### Pre-commit gates

Five gates fire on `git commit` (whichever hook mechanism is active) — both `.githooks/pre-commit`
and `scripts/git-hooks/pre-commit` run the same five, in the same order:

1. The **sync-drift gate** — blocks if `shared/` and the generated tree have diverged.
2. The **conformance generator self-test** — `scripts/report-conformance.py --self-test` — blocks
   if the generator's own falsifiability controls fail, ahead of gate 3's comparison against
   committed output (WR-05 ordering).
3. The **conformance-baseline drift gate** — `scripts/report-conformance.py --check` — blocks if
   `docs/conformance-baseline.md` or `docs/data/conformance.json` no longer match a fresh run.
   This check is deliberately NOT registered a second time in `scripts/check-firewall-battery.sh`
   and adds no CI job (REG-GUARD's CI-job axis is unaffected) — it fails on staleness of the
   committed baseline only, never on a conformance count being too high (D-06,
   `.planning/phases/17-conformance-baseline/17-CONTEXT.md`). `docs/conformance-baseline.md`
   carries the pre-existing labelled surface `adversarial-corpus`, measuring
   `tests/adversarial-corpus-v9.0/`'s deliberately-wrong probes under the unmodified, frozen
   `detect_defects` — a clean probe reading there is a MEASUREMENT of detector reach, never a
   statement that an artifact conforms — and now carries a fifth labelled surface,
   `live-conformance`, measuring the agent's own live-invoked output, captured under
   `tests/live-conformance-v9.0/`, through that same unmodified `detect_defects`. Its rate is a
   recorded observation, stated with its N, never a gate — conditional on delegation having
   occurred (D-04) — and subject to the same K-of-5 noise discipline as every other live reading
   in this file. `tests/live-conformance-v9.0` and `tests/live-conformance-catalog.md` are now
   registered `_FROZEN_PATHS` entries (Phase 20) alongside `tests/adversarial-corpus-v9.0`,
   `tests/quality-provenance-v8.24` and `tests/quality-ledger-v8.26`, and the battery total (26,
   see above) is unaffected by either registered-vs-unregistered pre-commit gate because
   FROZEN-EVIDENCE is an inline check that increments once regardless of array length.
4. The **claim-surface generator self-test** — `scripts/gen-gate-docs.py --self-test` — same
   WR-05 ordering discipline as gate 2, ahead of gate 5's comparison.
5. The **claim-surface drift gate** — `scripts/gen-gate-docs.py --check` (CONF-SURFACE, D-21-C,
   plan 21-11) — blocks if this file's, `docs/ARCHITECTURE.md`'s, `docs/TESTING.md`'s or any
   `docs/gates/<ID>.md` page's generated region no longer matches a fresh `--write` run, or if
   CONF-13's standing literal scanner finds a non-exempt hand-maintained count literal. Unlike
   gates 2-3's generator, CONF-SURFACE is *also* registered in `scripts/check-firewall-battery.sh`
   with a matching `gen-gate-docs (CONF-SURFACE)` CI job (see the gate table above) — it runs on
   all three surfaces, not pre-commit only.

The agent body's line count (`first-principles/agents/first-principles.md`) is still reported by
`scripts/check-body-budget.py` on every run, but it no longer blocks a commit — the 644-line gate
was retired under TEARDOWN-01. See `docs/v8.7-constraint-teardown.md` for the evidence and the
standing record.

Bypass for intentional in-progress work: `git commit --no-verify`

### Review protocol

Any reviewer of this repository — the vendored `bm:gsd-code-reviewer` agent, a fork of it, or a
human — tiers every finding, carries the tier in `REVIEW.md` frontmatter, and blocks only on
product findings.

1. **Tier every finding** as `product` or `apparatus` against
   [docs/PROCESS.md](docs/PROCESS.md) section 2. The cut is by claim-audience, not by directory
   and not by subject — see section 2 for the full rule; it is not re-transcribed here.
2. **Carry the tier in `REVIEW.md` frontmatter**, in this exact shape:

   ```yaml
   findings:
     product:   {critical: N, warning: N, info: N}
     apparatus: {critical: N, warning: N, info: N}
     total: N
   blocking: N        # product only
   status: issues_found
   ```

3. **Block only on product findings.** Apparatus findings auto-file to the
   `.planning/ROADMAP.md` backlog and never block a phase.

**Accepted limitation, stated plainly.** `bm:gsd-code-reviewer` is vendored outside this
repository, under the plugin cache, and is replaced on plugin update — there is no repo-side
binding. The agent holds `Read`, `Grep` and `Glob` and reads this file, which is the only reach
this repository has into its behaviour. The first live test of whether this block is honoured is
this phase's own `/bm:code-review 22`.

**The derived check a reviewer's output must satisfy**, stated as prose rather than as a gate:
every finding in a `REVIEW.md` carries a `product` or `apparatus` tier, and a finding carrying
neither is itself a defect in the review.

No script, control or CI job enforces any of this. D-08 rejected a findings-classifier
post-processor by name, and D-01 made the cut a judgement a path glob cannot decide — CR-05 is
the counterexample, an edit made in `scripts/` that produced a product-tier defect.

### Routing battery

Two verifiers cover different layers of routing correctness (`check-routing.py` for the
main-agent DELEGATE / NO-DELEGATE boundary; `check-routing-battery.py` for the merged
boundary + focused-output signal (FU-21 gate, FOCUS-01), whose offline `--self-test` is the
BATT-06 CI gate). Live catalog runs are developer tools, not CI gates, and are read by
aggregate K-of-N across repeats — never a single run's verdict.

Namespaced threshold defaults for the merged battery, one flag per signal:
`--boundary-p-threshold 2`, `--boundary-n-threshold 2`, `--focused-p-threshold 4`,
`--focused-n-threshold 1`. The un-namespaced `--p-threshold` / `--n-threshold` flags belonged
to the two pre-merge batteries and no longer exist.

The two deprecated shims that used to wrap this battery (`check-sub-skill-routing.py`,
`check-focused-output.py`) were **retired at the 2026-08-16 audit**, together with
`check-inventory.py`; their thresholds and self-test guards moved onto
`check-routing-battery.py`. See
[`docs/audit-2026-08-16-duplication-staleness.md`](docs/audit-2026-08-16-duplication-staleness.md).

Full detail — thresholds, catalog fixtures, and the per-sentinel ownership map — lives in
`docs/TESTING.md` and `docs/MEASUREMENT-MAP.md`. Read those before touching the batteries.

## Requirements surface

The canonical requirements and traceability surface lives in the git-tracked tree:

- **`docs/requirements-traceability.md`** — **the authoritative source of truth; start here.**
  Active residuals, the current coverage headline
  (**208 reproducible / 97 audit-only / 0 gap / 305 total**), compact historical ledger, and gap
  findings. (Derived from regenerated matrix Phase 138 Plan 03; META-Q4 re-tiered
  reproducible→audit-only in the v8.8 post-close TEARDOWN-01 cleanup, 133/96 → 132/97; 15
  v4.0/v4.1 builder requirements retired at quick task `260728-vxn`, 132/97 → 126/88,
  229 → 214 rows; the 23 v8.18 milestone requirements registered as matrix rows at Phase 4 / D-05,
  126/88 → 147/90, 214 → 237 rows; the 15 v8.24 milestone requirements registered as matrix rows
  at Phase 6 / D-06, 147/90 → 161/91, 237 → 252 rows; the 14 v8.25 milestone requirements
  registered as matrix rows at Phase 12 / 12-01, 161/91 → 174/92 (row count 252 → 266);
  CONTRACT-06 re-tiered reproducible at Phase 13 / CHAINHEAD-07, 174/92 → 175/91, row count
  unchanged at 266; the 20 v8.26 milestone requirements registered as matrix rows at Phase 16 /
  SHIP-03, 175/91 → 192/94, row count 266 → 286; the 19 v9.0 milestone requirements registered as
  matrix rows at Phase 23 / REL-03, 192/94 → 208/97, row count 286 → 305.)
- **`docs/v8.0-final-closure.md`** — **historical record, not current state.** Accepted
  limitations (RR-114-01 1/5, RR-108-04 0/5, RR-108-05 0/5) and deferred-ledger disposition as of
  v8.0 (Phase 142). It calls 133/96/0/229 the "final" coverage headline because v8.0 was meant to
  wrap the project; work continued and that figure has been superseded seven times — see the
  bullet above. Do not quote its headline as current.
- **`docs/requirements-matrix.md`** — generated 305-row capability→requirement→test
  matrix. Regenerate with:
  ```sh
  python3 scripts/check-traceability.py emit \
      --md-output docs/requirements-matrix.md \
      --json-output docs/data/matrix.json
  ```
- **`docs/data/matrix.json`** — the structured JSON sidecar behind
  `docs/requirements-matrix.md`, written by the same `emit` run.
- **`docs/history/`** — frozen per-milestone REQUIREMENTS.md / ROADMAP.md /
  MILESTONE-AUDIT.md snapshots (26 milestones, v1.0 through v5.3). **Local-only:
  git-ignored and untracked, so it is absent from a fresh clone.** Nothing in the
  tracked tree may link into it (`docs/requirements-traceability.md` names the
  files as plain text, not links) — a link would break the VAL-03 gate in CI.

`docs/data/matrix.json` is git-tracked (TEARDOWN-03, `docs/v8.7-constraint-teardown.md`), so
regenerating the matrix via the `emit` subcommand above dirties a tracked file, not an ignored
one. It lived at `.planning/phases/82-traceability-matrix-and-gap-findings/matrix.json` until it
was relocated under `docs/` so that `.planning/` could return to a blanket gitignore — no
planning artifacts are published to the public repo.

## Step 0 measurement harness

Two tools measure the agent body's Step 0 technique-selection logic, at different layers. They complement the routing battery (see [Routing battery](#routing-battery)) and each other.

**`scripts/check-step0-emulator.py`** — offline phrase-detection emulator (STEP0-08 CI gate
via `--self-test`, the only supported batch mode; no live session, no heavy manual run).

**`scripts/check-step0-live.py`** — live agent-body harness over the Plan-36-locked
`claude -p --output-format stream-json --verbose` transport; offline `--self-test` is the
STEP0-06 CI gate. Canonical baseline: `tests/step0-baseline-v7.8.md` (priors frozen in
`tests/step0-baseline-v*.md`).

Mechanism detail for both — bypass channel, MODE classification, fault-injection fixtures —
is in `docs/TESTING.md` and `docs/MEASUREMENT-MAP.md`.

**K-of-5 is a recorded observation, not a gate (governing record §2 item 3, `docs/v8.7-constraint-teardown.md`).** A K-of-5 result from this harness is demoted to an observation that a phase records — it may not gate a phase. The evidence: the S-P04 (five-whys) vector swung 2/5 → 0/5 → 2/5 across v7.11, v8.5, and v8.6 with no source change to the five-whys technique between those measurements. At N=5, noise equals effect. The tool itself is untouched — its pass-threshold flag and its verdict line survive byte-unchanged, because every frozen baseline from v7.4 through v8.6 depends on that comparability staying intact; what changed is the authority a phase gives the verdict, not the verdict itself.

### Measurement comparison

The four Step-0/routing tools, for orientation. The canonical layer map — which adds the
traceability, quality-harness and sentinel layers — is
[`docs/MEASUREMENT-MAP.md`](docs/MEASUREMENT-MAP.md#measurement-layers).

| Tool | Measured layer | Run command | CI gate |
|------|---------------|-------------|---------|
| `check-routing.py` | Main-agent DELEGATE / NO-DELEGATE routing boundary | `--catalog tests/routing-catalog.md --repeat 5 --min-pass 3` | None — developer tool, not wired into `validation.yml` |
| `check-routing-battery.py` | Merged dual-signal: boundary + focused-output (FU-21 gate, FOCUS-01) | `--repeat 5 --min-pass 3` / offline `--self-test` | BATT-06 |
| `check-step0-emulator.py` | Offline Step 0 phrase-detection classifier (deterministic, no live session) | `--self-test` | STEP0-08 |
| `check-step0-live.py` | Live Step 0 MODE classification via approach-② bypass channel | Manual `--repeat 5 --min-pass 3` (60 invocations) / offline `--self-test` | STEP0-06 |

### Step 0 residual sentinels (RR-* ownership map)

The BATT-06 and STEP0-08 offline self-tests own a set of named per-residual sentinels
(RR-80-01, RR-79-01, RR-114-01, RR-117-01, RR-117-02, RR-119-01, RR-119-02, RR-108-02,
RR-108-04, RR-108-05, RR-77-08). Each asserts a **documented honest count vector, not a
live pass rate** (honesty-not-score, D-01) against git-tracked frozen capture excerpts, so
tampering is visible in diff review.

Do not edit a sentinel, its drift guard, or its capture generation without reading the
authoritative record first:

- `docs/requirements-traceability.md` — active residuals, dispositions, coverage headline.
- `docs/v8.0-final-closure.md` — terminal ACCEPTED-FINAL dispositions.
- `scripts/_battery_core.py` — the sentinel source, with per-RR lineage comments and the
  `_load_excerpt_v*` generation helpers (all prior generations retained byte-frozen).

### Key invariants

- All reference file links use forward slashes and are one level deep from the file that references them (never nested `a.md → b.md → c.md`).
- **Agent-body reference links are plugin-root-anchored, not file-relative.** Every `references/…` link in `shared/spine/SKILL-body.md` — and the four `-detail.md` pointers the agent surface emits — carries the `${CLAUDE_PLUGIN_ROOT}/agents/references/` prefix (`AGENT_REF_PREFIX` in `scripts/sync-content.py`). An agent body is read with the *session* working directory in force, not the plugin directory, so a file-relative target resolves against the user's project and the read fails — observed live at v8.14.0, where the Phase 5 Self-Audit Gate never fired. `${CLAUDE_PLUGIN_ROOT}` is substituted in agent and skill content wherever it appears. **Skill stubs deliberately keep the file-relative form** — a slash-invoked skill is resolved against its own directory. VAL-03 *resolves* the token onto `first-principles/` rather than skipping it, so the agent body stays fully link-checked.
- **Agent reference siblings are anchored too, as of v8.17.4 — this overturns DEC-A.** The 16 links *between* files in `first-principles/agents/references/` (4 `-detail.md` pointers + 12 cross-technique) were bare filenames. DEC-A left them bare on the reasoning that they land in the same directory as their target — true of the filesystem, false of the reader, since a model opens them with the session working directory in force. `_absolutise_agent_ref_links()` anchors them at emission; `shared/references/*.md` deliberately keeps the bare form because it also feeds the skill stubs, whose correct target is a different path. GATE-02-v8.5's (g) assertion was inverted to match (anchored once, bare zero) and gained a directory-wide bare-target sweep, because the per-slug loop never reached the 12 cross-technique links. An unrecognised bare `.md` target now **raises** rather than passing through.
- **Scope the claim on the sibling surface narrowly.** The documented substitution table covers "Skill and agent content" — registered components the harness loads. Reference siblings are *not* registered components; they are plain files the model opens with Read, and the docs are **silent** on substitution inside them (checked 2026-08-17). The token is used there because it is **self-describing and inference-resolvable** — the model arrived via an already-expanded absolute path — not because substitution is guaranteed. Do not restate the body's guarantee for that surface.
- **Skill stubs: cross-technique links target the peer stub, as of v8.17.5 — this closes D-02.** The 12 links (`](five-whys.md)` in `skills/fishbone/SKILL.md`) broke for a *different* reason than the agent surface's: a wrong path inside a resolution mechanism that works, since the harness does resolve a slash-invoked skill against its own directory but `skills/fishbone/five-whys.md` does not exist. They now target `${CLAUDE_PLUGIN_ROOT}/skills/<slug>/SKILL.md` (`SKILL_PEER_PREFIX`), chosen over a backticked namespace ref and over pointing into the agent's reference tree because it leaves the prose byte-identical and resolves on disk. **The four `references/<slug>-detail.md` pointers stay file-relative** — they resolve against the stub's own directory, which is how the harness loads a skill.
- **`_absolutise_skill_peer_links()` must run AFTER `_rewrite_detail_link()`.** The detail rewrite gives its target a `/`, taking it out of `_BARE_MD_TARGET_RE`'s reach; the reverse order would mis-target the detail sibling as a peer skill.
- **VAL-03 full-checks skill stubs as of v8.17.5, retiring D-05's deferral.** `first-principles/skills/*/SKILL.md` was namely namespace-only *because* those 12 links did not resolve; with that fixed it was promoted into `FULL_CHECK_GLOBS` (it stays in `NAMESPACE_ONLY_GLOBS` too — `_collect_files` dedups, and the surface wants both axes). The self-test's old *disjointness* assertion became an intended-overlap-plus-dedup assertion, and D-06's "both surfaces match zero live findings" note is superseded: this surface now contributes 16 real links.
- Skill `name` in frontmatter must match the parent directory name exactly.
- Skill `description` fields must be third-person, ≤ 1,024 chars, no XML tags.
- `metadata.version` must be a double-quoted YAML string (e.g. `version: "3.8"`), not a bare number.
- Every hand-maintained version stamp must carry the *same* value — see VERSION-01 above. A bump touches all 17 or none.
- Reserved words `anthropic` and `claude` are forbidden in skill `name` fields.
- The agent body's line count is **not** an invariant: the 644-line gate was retired under TEARDOWN-01 and is report-only.

Each invariant is paired with the gate that enforces it in [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md#key-invariants) — including the two that are conventions with no gate behind them.
