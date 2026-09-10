<!-- generated-by: gsd-doc-writer -->
# Architecture

This document describes the source-of-truth layout, the generation pipeline, plugin registration, the five-phase agent methodology, the measurement subsystem (inventory), and the canonical CI and pre-commit gate inventory for the first-principles-skills plugin.

## Overview

The plugin ships a single orchestrating agent (`first-principles:first-principles`) plus thirteen slash-only companion skills. The entire deliverable is pure Markdown — no executable code ships inside the plugin tree. A Python generation script (`scripts/sync-content.py`) assembles the generated tree from canonical source files in `shared/`.

```
shared/           ← canonical source (edit here)
first-principles/ ← generated plugin (committed, never hand-edited)
scripts/          ← generation, validation, and measurement-battery scripts
tests/            ← routing catalog fixtures and step 0 capture files
```

## Source-of-truth vs. generated surface

**Edit `shared/` only. Never edit the generated tree directly.**

| Area | Path | Role |
|------|------|------|
| Agent body template | `shared/spine/SKILL-body.md` | Assembled agent body; contains `{{TOOL:slug}}` tokens |
| Agent frontmatter | `shared/spine/SKILL.meta.yml` | Frontmatter fields emitted to the generated agent |
| Token → name map | `shared/spine/tool-map.yml` | Slug → inline name mapping for `{{TOOL:slug}}` substitution |
| Output template | `shared/spine/references/output-template.md` | Emitted as an agent reference sibling; **not** inlined |
| Validation rubric | `shared/spine/references/validation-rubric.md` | Emitted as an agent reference sibling; **not** inlined |
| Phase procedures | `shared/agent/` | Phase fragments stitched into the agent body |
| Companion references | `shared/references/` | Five Whys, fishbone, inversion, pre-mortem, trade-off, second-order, estimate, theoretical-limit, identify-essence, challenge-assumptions, ground-truths, reason-upward, validate |
| Worked examples | `shared/examples/` | Fourteen domain-spread example files |
| Focused-mode skills | `shared/skills/<slug>/SKILL.md` | Source for each slash-only companion skill |

Generated output tree:

| Path | Role |
|------|------|
| `first-principles/agents/first-principles.md` | Assembled agent (sync-content.py output) |
| `first-principles/agents/references/` | Verbatim copies of `shared/references/` + spine refs |
| `first-principles/agents/references/examples/` | Verbatim copies of `shared/examples/` |
| `first-principles/skills/<slug>/SKILL.md` | Generated stubs from `shared/skills/<slug>/SKILL.md` |
| `first-principles/README.md` | Plugin README |
| `first-principles/LICENSE` | MIT license |

## Generation pipeline

`scripts/sync-content.py --write` reads `shared/` and regenerates the entire `first-principles/` tree. Every generated file is stamped with a `<!-- GENERATED — DO NOT EDIT -->` marker.

**Assembly steps:**

1. Read `shared/spine/SKILL.meta.yml` — emit frontmatter to `first-principles/agents/first-principles.md`
2. Read `shared/spine/SKILL-body.md` — resolve `{{TOOL:slug}}` tokens
3. For each `{{TOOL:slug}}`: substitute the phrase held under that slug's `agent` key in `shared/spine/tool-map.yml` (`_expand()`), e.g. `{{TOOL:fishbone}}` → "the inlined fishbone procedure"
4. Nothing from `shared/spine/references/` is inlined at this point. `output-template.md` and `validation-rubric.md` were inlined into the body until Phase 34-02 (Path B); they now ship as sibling reference files only, and the body reaches them through `${CLAUDE_PLUGIN_ROOT}/agents/references/…` links. Do not reintroduce an inlining step here — `sync-content.py` carries a standing NOTE against it.
5. Stitch phase fragments from `shared/agent/` in order
6. Copy `shared/references/*.md` and `shared/examples/*.md` verbatim to `first-principles/agents/references/`, and `shared/spine/references/*.md` to the same directory via `generate_agent_spine_references()`
7. For each `shared/skills/<slug>/SKILL.md`: resolve `{{PROCEDURE:slug}}` tokens (replaced by the full body of `shared/references/<slug>.md` from `## When to reach for this` onward) and write to `first-principles/skills/<slug>/SKILL.md`

**Drift detection:** `scripts/sync-content.py --check` verifies that `shared/` and the generated tree are in sync. Exit code 1 on any drift. This runs as a pre-commit gate and as CI gate DUAL-04.

## Token substitution

Two token types are used in source files. They do **different** things, and the difference is
easy to get backwards:

| Token | Used in | Replaced by | Kind |
|-------|---------|-------------|------|
| `{{TOOL:slug}}` | `shared/spine/SKILL-body.md` | The phrase under that slug's `agent` key in `shared/spine/tool-map.yml` — e.g. `{{TOOL:fishbone}}` → "the inlined fishbone procedure" | **naming**, not content |
| `{{PROCEDURE:slug}}` | `shared/skills/<slug>/SKILL.md` | Full body of `shared/references/<slug>.md` from `## When to reach for this` onward | **content** |

`{{TOOL:slug}}` substitutes a short human-readable *name*, nothing more. It appears twice over
in the spine body: inline in phase prose ("use `{{TOOL:fishbone}}` to brainstorm causes by
category") and as the bold label of that technique's entry in the agent's `## Companion tools`
summary. Those summaries are hand-written in `shared/spine/SKILL-body.md`; they are not
extracted from anything.

**The companion-technique procedures are therefore not inlined into the agent body.** They ship
as reference siblings under `first-principles/agents/references/<slug>.md` and are loaded on
demand. This is worth stating plainly because the substituted phrase itself says "the inlined
… procedure", which reads as though the procedure text is present in the body. It is not — a
search of the generated agent body for any technique's actual procedure steps returns nothing.

`shared/spine/tool-map.yml` holds one entry per companion-tool slug, keyed by surface (today the
only surface is `agent`). The eight registered slugs are `five-whys`, `fishbone`, `inversion`,
`pre-mortem`, `trade-off`, `second-order`, `estimate`, `theoretical-limit`. `_expand()`
distinguishes an unknown slug from a known slug missing the current surface key, so a
contributor sees which of the two mistakes they made.

## Plugin layout and registration

The plugin root is `first-principles/`. Install for development:

```bash
claude --plugin-dir ./first-principles
```

The agent is registered at `first-principles/agents/first-principles.md`. Fourteen skill directories live under `first-principles/skills/<slug>/SKILL.md` — the thirteen companion skills plus the `first-principles-analysis` launcher — all registered with `disable-model-invocation: true`; slash-only, the orchestrator never auto-routes to them. The launcher is why `shared/skills/*/SKILL.md` holds 14 version stamps rather than 13.

**Companion skill slugs:** `challenge-assumptions`, `estimate`, `fishbone`, `five-whys`, `ground-truths`, `identify-essence`, `inversion`, `pre-mortem`, `reason-upward`, `second-order`, `theoretical-limit`, `trade-off`, `validate`

## Five-phase methodology

The agent applies a five-phase procedure. Each phase produces a named artifact that is the entry condition for the next phase:

| Phase | Name | Artifact produced |
|-------|------|-------------------|
| 1 | Identify Essence | Essence Statement |
| 2 | Challenge Assumptions | Classified Assumptions Table |
| 3 | Establish Ground Truths | Ground Truths list (GT-N IDs) |
| 4 | Reason Upward | Derivation Chains (`GT-N + GT-M → conclusion`) |
| 5 | Validate | Signed-off analysis with a Self-Audit Gate pass |

Eight of these companion techniques (Five Whys, fishbone, inversion, pre-mortem, trade-off, second-order thinking, estimate, theoretical-limit) are *named* in the agent body via `{{TOOL:slug}}` tokens — each with a hand-written summary in the body's `## Companion tools` section — while their full procedures ship as on-demand reference siblings rather than in the body itself (see [Token substitution](#token-substitution)). All thirteen companion skills — these eight techniques plus the five phase skills (identify-essence, challenge-assumptions, ground-truths, reason-upward, validate) — are additionally registered as standalone, slash-only skills (`disable-model-invocation: true`).

## CI and pre-commit gate inventory

<!-- GENERATED — DO NOT EDIT. Source: scripts/_gate_registry.py. Regenerate via: scripts/gen-gate-docs.py --write. -->
Both surfaces render the same population and the same columns from `scripts/_gate_registry.py`, emitted by `scripts/gen-gate-docs.py --write`, so the two cannot diverge; `CLAUDE.md` keeps the full gate list visible without opening `docs/`, and per-gate detail lives in `docs/gates/<GATE-ID>.md`.

| Gate | Job / Mechanism | Script | What it checks |
|------|-----------------|--------|-----------------|
| VAL-01 | `plugin-validate` (CI) | `claude plugin validate` | Plugin manifest schema validity via the `claude` CLI. Spends zero model tokens. Does NOT validate the agent frontmatter — the CLI walks subdirectories of `agents/` and never inspects a flat `agents/*.md`, so GATE-01 is the sole validator of agent frontmatter. See [`docs/gates/VAL-01.md`](gates/VAL-01.md). |
| VAL-02 | `markdownlint` (CI) | `markdownlint-cli2` | MD style across `first-principles/**/*.md` via `markdownlint-cli2`. See [`docs/gates/VAL-02.md`](gates/VAL-02.md). |
| VAL-03 | `check-links` (CI) | `scripts/check-links.py --self-test` | Relative Markdown link validity across the plugin, `shared/`, and `docs/` trees; `docs/` anchors validated with a github-slugger rule. Three legs: self-test, a live scan, and a pytest run of `check-links_anchors_test.py`. The third leg needs a pytest-capable interpreter — when none is found the battery still runs legs 1-2 through `gate_prereq` and reports [PREREQ]/BLOCKED rather than [PASS]/GREEN. (scan_globs=3 entries; locked_constants=2 entries) See [`docs/gates/VAL-03.md`](gates/VAL-03.md). |
| VAL-04 / GATE-02 | `check-trigger-collisions` (CI) | `scripts/check-trigger-collisions.py --self-test` | No 4-gram collision across skill descriptions. Carries the pre-existing v3.0 GATE-02 id alongside VAL-04 — the battery registers this row under `VAL-04` only; `GATE-02` is a name the row also carries, not a second battery registration (see `extra_ids` on this entry, excluded from the D-01 battery-id equality floor by construction). (derived_counts=1 entries) See [`docs/gates/VAL-04.md`](gates/VAL-04.md). |
| VAL-05 | `check-description-budget` (CI) | `scripts/check-description-budget.py` | All skill listings stay under the 2000-character budget cap. (locked_constants=1 entries) See [`docs/gates/VAL-05.md`](gates/VAL-05.md). |
| VERSION-01 | `check-version-stamps` (CI) | `scripts/check-version-stamps.py --self-test` | Every hand-maintained version stamp carries the same value. Runs the live scan as well as the self-test — the invariant is a property of the working tree, not of the script's own fixtures. (derived_counts=1 entries; registered_surfaces=4) See [`docs/gates/VERSION-01.md`](gates/VERSION-01.md). |
| REG-GUARD | `check-registration` (CI) | `scripts/check-registration.py --self-test` | Registration completeness over two surfaces: (a) every skill directory and the main agent carry a frontmatter `name:` matching their own basename; (b) every gate this file's own battery registers has a matching `name: <job> (<GATE-ID>)` job in `.github/workflows/validation.yml`, QUAL-01 the one named battery-only exemption. This module's D-01 floor deliberately reuses `check-registration.py`'s `_BATTERY_GATE_RE` parsing semantics rather than inventing a second grammar over the same file. (control_ids=29; control_count=29; registered_surfaces=2; checked_files=4; locked_constants=1 entries) See [`docs/gates/REG-GUARD.md`](gates/REG-GUARD.md). |
| COLLIDE-01 | `check-install-collisions` (CI) | `scripts/check-install-collisions.py --self-test` | Dual-install name-collision scan: no skill/agent name collisions between the plugin and monolith install surfaces. (registered_surfaces=2; disclosed_bounds_anchors=1) See [`docs/gates/COLLIDE-01.md`](gates/COLLIDE-01.md). |
| DUAL-04 | `sync-check` (CI) | `scripts/sync-content.py --check` | `shared/` and the generated `first-principles/` tree are in sync. (derived_counts=1 entries; registered_surfaces=4; locked_constants=1 entries; control_ids=13; control_count=13) See [`docs/gates/DUAL-04.md`](gates/DUAL-04.md). |
| GATE-02-v8.5 | `GATE-02-v8.5` | `scripts/sync-content.py --self-test` | Pointer drift-guard: each of the four split core reference files' extracted Procedure slice carries exactly one well-formed link to its own `-detail.md` sibling. Proves the pointer exists and is well-formed, NOT that it is followed. Same script as DUAL-04, a different flag — the D-03 case for a flat `--describe` namespace rather than a per-gate id argument. See [`docs/gates/GATE-02-v8.5.md`](gates/GATE-02-v8.5.md). |
| GATE-01 | `check-agent` (CI) | `scripts/check-agent.py --self-test` | Agent structural checks — 8 frontmatter/body assertions on the shipped agent, including the exact `maxTurns` value (60), not merely its presence. The live leg targets the repo-anchored `AGENT_FILE` constant, so the gate is cwd-independent and cannot be silently re-pointed. (branch_roster=8; branch_count=8; scoped_branches=3; locked_constants=3 entries; checked_files=1; disclosed_bounds_anchors=1) See [`docs/gates/GATE-01.md`](gates/GATE-01.md). |
| BATT-06 | `check-routing-battery` (CI) | `scripts/check-routing-battery.py --self-test` | Offline merged dual-signal routing-battery self-test (boundary + focused-output); owns the honest-state and anti-masking sentinels. (locked_constants=4 entries; disclosed_bounds_anchors=11; derived_counts=1 entries; checked_files=1) See [`docs/gates/BATT-06.md`](gates/BATT-06.md). |
| STEP0-08 | `check-step0-emulator` (CI) | `scripts/check-step0-emulator.py --self-test` | Offline Step 0 phrase-detection classifier self-test. (locked_constants=1 entries; derived_counts=2 entries; disclosed_bounds_anchors=6; checked_files=2) See [`docs/gates/STEP0-08.md`](gates/STEP0-08.md). |
| STEP0-06 | `check-step0-live` (CI) | `scripts/check-step0-live.py --self-test` | Offline Step 0 live-harness scoring/parsing logic self-test. (locked_constants=2 entries; checked_files=2; control_ids=25; control_count=25) See [`docs/gates/STEP0-06.md`](gates/STEP0-06.md). |
| TRACE-03 | `check-traceability` (CI) | `scripts/check-traceability.py --self-test` | Offline traceability gate self-test — capability/tier schema, artifact resolution, plus the HEADLINE-LOCK sentinel asserting the published coverage headline against five named current-fact surfaces and both tracked matrix artifacts. (`docs/*.md`, `CLAUDE.md`, `CHANGELOG.md`, `README.md`; registered_surfaces=5; branch_roster=19; branch_count=19; locked_constants=4 entries; coverage_headline=2 entries) See [`docs/gates/TRACE-03.md`](gates/TRACE-03.md). |
| QUAL-01 | battery only — not a CI job | `scripts/check-quality-harness.py --self-test` | Offline blind A/B quality-measurement harness self-test — extraction guardrails, scoreline parsing, blinding, tabulation, baseline-fixture integrity, the mechanical defect detector, and the emission rendering contract's six legs. The single named battery-only CI exemption in REG-GUARD's `BATTERY_ONLY_GATE_IDS`. (control_ids=27; control_count=27; registered_surfaces=4; disclosed_bounds_anchors=30; derived_counts=4 entries; locked_constants=3 entries; contract_pins=3 entries) See [`docs/gates/QUAL-01.md`](gates/QUAL-01.md). |
| PROV-GUARD | `check-provenance` (CI) | `scripts/check-provenance.py --self-test` | Every `read-at-source` ground truth in an analysis's section 3 joins to a real WebFetch/Read of that source in the run's stored capture, and every literal it states appears verbatim in that source's retrieved text. Live leg reads `tests/quality-provenance-v8.24/` and reports 7/7 sources matched, 35/35 literals located. (control_ids=33; control_count=33; registered_surfaces=2; locked_constants=1 entries) See [`docs/gates/PROV-GUARD.md`](gates/PROV-GUARD.md). |
| HARN-01 | `check-act-limb` (CI) | `scripts/check-act-limb.py --self-test` | Offline Act-limb gate: the Phase 3 verification step and the Criterion 3 Fix note are present, correctly placed, and internally coherent in the emitted tree. (branch_roster=16; branch_count=16; control_ids=78; control_count=78; checked_files=2; disclosed_bounds_anchors=4) See [`docs/gates/HARN-01.md`](gates/HARN-01.md). |
| HARN-02 | `check-loop-closure` (CI) | `scripts/check-loop-closure.py --self-test` | Observe->Perceive re-entry edges: a Criterion 1 Absent verdict routes back to Phase 1, every re-entry edge is bounded to one re-perception pass, and a fired edge is recorded. (checked_files=4; control_ids=37; control_count=37) See [`docs/gates/HARN-02.md`](gates/HARN-02.md). |
| HARN-03 | `check-focused-parity` (CI) | `scripts/check-focused-parity.py --self-test` | Focused-mode parity: stub surface, agent surface and cross-surface parity-token set equality, with the D-12 anchor-control ratchet. (locked_constants=2 entries; registered_surfaces=3; disclosed_bounds_anchors=1) See [`docs/gates/HARN-03.md`](gates/HARN-03.md). |
| SCAN-GUARD | `check-selfaudit-scan` (CI) | `scripts/check-selfaudit-scan.py --self-test` | Self-audit scan structural gate: the Phase 15 self-audit scan prescription, its rubric verify block, and the Criterion-2-widened Verdict Block Format admission are present, correctly placed and internally coherent in the emitted tree, with one hundred clause-level named branches floored by an independent transcription (`_BRANCH_ROSTER_LOCK`). (branch_roster=100; branch_count=100; registered_surfaces=2; call_site_census=4 entries; control_ids=12; control_count=12; locked_constants=1 entries) See [`docs/gates/SCAN-GUARD.md`](gates/SCAN-GUARD.md). |
| HC-BOUND | `check-high-confidence-bound` (CI) | `scripts/check-high-confidence-bound.py --self-test` | Structural validation gate: Phase 5 tightening of Criterion 3 (Evidence) and Criterion 5 (Conclusion) HIGH-confidence bound is present and well-formed on both rubric surfaces, and all three documented EXCEPT exceptions are present. (registered_surfaces=2; derived_counts=1 entries; disclosed_bounds_anchors=3) See [`docs/gates/HC-BOUND.md`](gates/HC-BOUND.md). |
| CONF-GATE | `check-conf-gate` (CI) | `scripts/check-conf-gate.py --self-test` | Standing exemplar-conformance comparator: the four conformance counts on both gated example surfaces against source-literal targets, a 14-entry claim floor locked by equality to the live-discovered `shared-examples` ids, the D-03 prescribed-lead-in rule, and the marked-claim ratchet (may fall, never rise). (registered_surfaces=2; population_floors=2 entries; call_site_census=7 entries; control_ids=44; control_count=44; locked_constants=2 entries) See [`docs/gates/CONF-GATE.md`](gates/CONF-GATE.md). |
| INVARIANT-CHECK | battery only (inline) | — | Anti-masking constants still hold in `scripts/_battery_core.py`: pre-mortem=9 fishbone=7 inversion=13 trade-off=10 MIN_HEADER_HITS=2. A direct value-grep double-check of what BATT-06 and STEP0-08 already assert internally. See [`docs/gates/INVARIANT-CHECK.md`](gates/INVARIANT-CHECK.md). |
| FROZEN-EVIDENCE | battery only (inline) | — | Frozen baselines and captures are unmodified relative to HEAD, plus an untracked-files sweep over the same paths. `_FROZEN_PATHS` grows over time; this inline check increments the battery tally once regardless of array length. See [`docs/gates/FROZEN-EVIDENCE.md`](gates/FROZEN-EVIDENCE.md). |
| — | sync-drift gate (pre-commit) | `scripts/sync-content.py --check` | `shared/` and the generated tree are in sync — the same check as DUAL-04, fired before commit rather than in CI/battery. See [`docs/gates/PRECOMMIT-sync-drift-gate.md`](gates/PRECOMMIT-sync-drift-gate.md). |
| — | conformance generator self-test (pre-commit) | `scripts/report-conformance.py --self-test` | Blocks if `scripts/report-conformance.py --self-test` fails. Runs the generator's own falsifiability controls before its output is compared to anything (WR-05) — ordered before `--check` because a generator whose own controls are failing makes that comparison meaningless. See [`docs/gates/PRECOMMIT-conformance-generator-self-test.md`](gates/PRECOMMIT-conformance-generator-self-test.md). |
| — | conformance-baseline drift gate (pre-commit) | `scripts/report-conformance.py --check` | `docs/conformance-baseline.md` and `docs/data/conformance.json` reproduce byte-for-byte a fresh `report-conformance.py` run (D-06); fires before commit. Deliberately not registered in the battery or in CI. (registered_surfaces=5; checked_files=2; control_ids=102; control_count=102; locked_constants=1 entries) See [`docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md`](gates/PRECOMMIT-conformance-baseline-drift-gate.md). |
| — | claim-surface generator self-test (pre-commit) | `scripts/gen-gate-docs.py --self-test` | Blocks if `scripts/gen-gate-docs.py --self-test` fails. Same WR-05 ordering discipline as the conformance generator self-test — a broken generator's own controls must be caught before its comparison against committed output (the claim-surface drift gate) is even attempted. See [`docs/gates/PRECOMMIT-claim-surface-generator-self-test.md`](gates/PRECOMMIT-claim-surface-generator-self-test.md). |
| — | claim-surface drift gate (pre-commit) | `scripts/gen-gate-docs.py --check` | Blocks if `CLAUDE.md`'s/`docs/ARCHITECTURE.md`'s generated gate tables, `docs/TESTING.md`'s generated index, or any `docs/gates/<ID>.md` page no longer match a fresh `scripts/gen-gate-docs.py --write` run, or if CONF-13's standing literal scanner finds a non-exempt hand-maintained count literal — the same check as CONF-SURFACE, fired before commit rather than in CI/battery. See [`docs/gates/PRECOMMIT-claim-surface-drift-gate.md`](gates/PRECOMMIT-claim-surface-drift-gate.md). |
| CONF-SURFACE | `gen-gate-docs` (CI) | `scripts/gen-gate-docs.py --self-test` | The claim-surface drift gate itself: regenerates `CLAUDE.md`'s and docs/ARCHITECTURE.md's gate tables and docs/gates/<ID>.md pages from this registry's ENTRIES and every gate's --describe emission, and fails on drift. Registered in the battery, with a matching `gen-gate-docs (CONF-SURFACE)` CI job and both pre-commit hooks (plan 21-11, D-21-C). (registered_surfaces=40; checked_files=70; derived_counts=26 entries; disclosed_bounds_anchors=8; control_ids=93; control_count=93; locked_constants=2 entries) See [`docs/gates/CONF-SURFACE.md`](gates/CONF-SURFACE.md). |

Gates run on three surfaces: **23 in CI** (`.github/workflows/validation.yml`, on push/PR to master), **26 tallied in the offline battery** (`bash scripts/check-firewall-battery.sh`), and **5 pre-commit gates** (2 hook mechanisms run the identical set in the identical order). The battery is a strict superset of CI: all 23 CI gates plus 1 battery-only gate plus 2 inline checks. That is 23 + 1 + 2 = 26.
<!-- END GENERATED -->

HARN-01, HARN-02 and HARN-03 were registered under HARN-04 at v8.18.0 — each has a CI job plus a
single `--self-test`-only battery `gate` call, and each is counted in the battery total above. HC-BOUND
was registered at v8.19.0 under Phase 6 (HC-04) — it also has a CI job plus a single `--self-test`-only
battery `gate` call, and is counted in the battery total above. REG-GUARD was registered at v8.21.0
under Phase 3 (REG-03) — it has a CI job plus a battery `gate` call that runs both `--self-test` **and**
the live scan, matching VERSION-01, GATE-01 and COLLIDE-01, and is counted in the battery total above.
PROV-GUARD was registered at v8.24.0 under Phase 6 (GATE-02/GATE-03) — a CI job plus a battery `gate`
call running both `--self-test` **and** the live leg, matching VERSION-01, GATE-01, COLLIDE-01 and
REG-GUARD — and is counted in the battery total above. SCAN-GUARD was registered at v8.26.0 under
Phase 15 — a CI job plus a battery `gate` call running both `--self-test` **and** the live leg
(plan 15-09, closing `15-VERIFICATION.md` gap 2's WR-05 finding), matching PROV-GUARD's and
REG-GUARD's shape rather than HARN-01/02/03's and HC-BOUND's `--self-test`-only shape.
SCAN-GUARD is counted in the battery total above. CONF-GATE was registered at v9.0.0 under
Phase 18 — a CI job plus a battery `gate` call running both `--self-test` **and** the live
leg, matching PROV-GUARD's and SCAN-GUARD's shape, and is counted in the battery total above.
CONF-SURFACE was registered at v9.0.0 under Phase 21 (D-21-C, plan 21-11) — a CI job plus a
battery `gate` call running `gen-gate-docs.py --self-test` then `--check`, and both pre-commit
hooks (five gates each, up from three) — and is counted in the battery total above: this is the
`25 → 26` move produced by CONF-SURFACE itself, not hand-swept.

**Two gates are called GATE-02 and they are not the same gate.** `VAL-04 / GATE-02` is the v3.0
trigger-collision scanner (`check-trigger-collisions.py`), carried by a single job whose live name
is `check-trigger-collisions (VAL-04/GATE-02)`. `GATE-02-v8.5` is the v8.5 pointer drift-guard
(`sync-content.py --self-test`), a separate job. The `-v8.5` suffix is what distinguishes them;
dropping it conflates two unrelated checks.

The body-budget gate that used to appear in this table (blocking a commit that pushed the
agent body past 644 lines) was retired under TEARDOWN-01
(`docs/v8.7-constraint-teardown.md`, the standing record) — `scripts/check-body-budget.py`
is kept on disk and reports the body's current line count on every run, but it no longer
exits nonzero because of the body's size and no longer fires as a pre-commit gate at all; 644 survives only as a historical
reference figure inside the script. The battery still prints it as an untallied `[INFO]` line.

For operational run-detail — how to invoke each gate locally, `--self-test` modes, and what the pre-commit hook checks — see [docs/TESTING.md](TESTING.md).

## Measurement subsystem

The following scripts form the measurement subsystem. They sit alongside the validation scripts in `scripts/` and are named here at inventory altitude. For anti-masking invariants, constant values, and the full inter-layer wiring detail see [docs/TESTING.md](TESTING.md).

| Component | Script | Role |
|-----------|--------|------|
| Step 0 emulator | `scripts/check-step0-emulator.py` | Offline phrase-detection classifier; reads the `**Phrase detection rules**` table from `shared/spine/SKILL-body.md` and classifies a prompt to `MODE` (STEP0-08) |
| Step 0 live harness | `scripts/check-step0-live.py` | Live MODE classification via the approach-② bypass channel against a running `claude` session (STEP0-06 offline self-test) |
| Routing battery | `scripts/check-routing-battery.py` | Merged dual-signal battery: boundary-discipline + focused-output signals scored together (BATT-06 `--self-test`) |
| Routing battery (developer tool) | `scripts/check-routing.py` | Main-agent DELEGATE / NO-DELEGATE routing battery; developer tool, not wired into CI |
| Battery core | `scripts/_battery_core.py` | Shared battery logic; home of the anti-masking invariant constants and the `self_test_boundary()` sentinels |
| Traceability matrix | `scripts/check-traceability.py` | Capability → requirement → test traceability matrix; `emit` generates the matrix, `--self-test` is TRACE-03 |

The two deprecated shims that used to wrap this battery (`check-sub-skill-routing.py`, `check-focused-output.py`) and the unwired requirement-ID auditor `check-inventory.py` were retired at the 2026-08-16 audit; `check-routing-battery.py` is the only entry point, and its threshold flags are namespaced per signal.

## Key invariants

The canonical list — each invariant paired with the gate that would actually catch a violation —
is in [CONFIGURATION.md#key-invariants](CONFIGURATION.md#key-invariants).

Two are architectural rather than cosmetic, and are the ones this document's structure depends on:

- **Edit `shared/` only.** The generated tree is an output, and DUAL-04 fails any commit where
  the two disagree.
- **Reference file links are one level deep**, never nested `a.md → b.md → c.md`. The agent
  loads references on demand; a chain would make the depth of a load unbounded.
