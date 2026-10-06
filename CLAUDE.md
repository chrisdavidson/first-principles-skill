# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Current shipped version: see `.claude-plugin/marketplace.json` (every hand-maintained version
stamp moves in lockstep — VERSION-01 enforces it). For what changed in any milestone, read the tag table and
entries in [`CHANGELOG.md`](CHANGELOG.md). This file describes the repo as it stands and does
not track release history — where it names a milestone below, that is a current-state fact
carrying its provenance, not a changelog entry.

A Claude Code **plugin** that ships a first-principles analysis agent (`first-principles:first-principles`) plus the thirteen companion skills (pre-mortem, inversion, fishbone, five-whys, trade-off, second-order, estimate, theoretical-limit, identify-essence, challenge-assumptions, ground-truths, reason-upward, validate), the `first-principles-analysis` launcher, and the `persona` reader-view companion. The entire deliverable is pure Markdown — no executable code ships inside the plugin.

## Commands

### Sync generated files from canonical source

```sh
python3 scripts/sync-content.py --write   # regenerate all target files
python3 scripts/sync-content.py --check   # verify no drift (exit 1 on drift)
uv run scripts/sync-content.py --write    # uv alternative (auto-resolves deps)
```

### Validation scripts (Python ≥ 3.12; PyYAML required for frontmatter parsing)

```sh
python3 scripts/check-agent.py                # GATE-01
python3 scripts/check-links.py                # VAL-03
python3 scripts/check-version-stamps.py       # VERSION-01
python3 scripts/check-quality-harness.py --self-test  # QUAL-01
python3 scripts/check-provenance.py --self-test       # PROV-GUARD
python3 scripts/check-conf-gate.py --self-test        # CONF-GATE
python3 scripts/check-report-figures.py --self-test   # FIG-GATE (needs typst)
python3 scripts/check-persona-view.py --self-test     # PERSONA-GATE
```

Authority: `bash scripts/check-firewall-battery.sh` (runs all gates). pytest is required only by VAL-03's anchor-check leg. Run `uv sync` to install dependencies in `.venv`.

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
# Run from the repo root so the relative --catalog path resolves. Baseline: tests/step0-baseline-v8.5.md
python3 scripts/check-step0-live.py --catalog tests/step0-fixture-catalog.md --repeat 5 --min-pass 3

# Live harness offline self-test — STEP0-06 CI gate (no live claude session)
python3 scripts/check-step0-live.py --self-test

# Offline emulator self-test — STEP0-08 CI gate (no live claude session; no heavy manual run)
python3 scripts/check-step0-emulator.py --self-test
```

### Lint and format (Ruff)

```sh
uv run ruff check              # lint, Ruff defaults
uv run ruff format             # format .py files
uv run ruff format --check     # verify formatting without writing
```

A local convention, not a gate: Ruff is not registered in CI or the battery. The version is pinned in
`pyproject.toml`'s dev group. Frozen and recorded `tests/<run-dir>/` scripts are excluded, and
sha256-pinned functions are fenced with `# fmt: off` / `# fmt: on`. To hide the mass reformat from
blame: `git config blame.ignoreRevsFile .git-blame-ignore-revs`.

### Plugin validation and installation

```sh
claude plugin validate ./first-principles          # validate plugin manifest
claude --plugin-dir ./first-principles             # install for local development
```

### Install pre-commit hooks

```sh
./scripts/install-hooks.sh        # every pre-commit gate (### Pre-commit gates, below) in .git/hooks/pre-commit (body-budget retired under TEARDOWN-01, docs/v8.7-constraint-teardown.md)
# OR:
git config core.hooksPath .githooks   # the same gates via .githooks/pre-commit
# (do not use both — they are mutually exclusive at the Git level)
```

### Fast-path: SKIP_DRIFT_CHECK for generators

Skip pre-commit drift checks when intentionally regenerating outputs:

```sh
SKIP_DRIFT_CHECK=1 git commit
```

Skips only the pre-commit sync-drift gate; both generator self-tests still run. It does not skip claim-surface drift: the `gen-gate-docs.py --self-test` the hooks run in both modes compares the generated surfaces against the working tree, so regenerate with `python3 scripts/gen-gate-docs.py --write` before committing. CI verifies sync-drift (DUAL-04) and claim-surface drift (CONF-SURFACE) on PR; conformance-baseline drift (CONF-DRIFT) runs only in the offline battery, which no CI job runs, so run `bash scripts/check-firewall-battery.sh` before pushing.

### Bypass patterns

`git commit --no-verify` bypasses all pre-commit gates. Sync-drift runs pre-commit and in CI (DUAL-04) — never bypass it for PR commits. Recommended: use `SKIP_DRIFT_CHECK=1` for generator runs, `git commit` for normal work, `bash scripts/check-firewall-battery.sh` before pushing.

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
      report-layout.md          ← PDF reader report's pandoc/typst page template, emitted as a reference sibling, extracted by awk at render time, never Read
      report-figures.md         ← typst figure library (evidence trace, assumption verdict matrix), emitted as a reference sibling, extracted by awk, NOT inlined
      how-to-read.md            ← static business-reading guide, emitted as a reference sibling, copied beside the reports by awk at delivery, never Read
      persona-views.md          ← reader-persona contract, emitted as an agent reference sibling, read by the persona skill and PERSONA-GATE, NOT inlined
  agent/                        ← phase-procedure fragments stitched into the agent body
  references/                   ← companion tool reference files (five-whys.md, etc.)
  references/<slug>-detail.md   ← v8.5 on-demand appendix siblings (SLUGS_WITH_DETAIL only)
  examples/                     ← worked-example source files
  persona-examples/              ← persona views derived from worked examples by real persona-skill runs; outside the examples/ glob
  skills/<slug>/SKILL.md        ← source for each focused-mode slash skill

first-principles/               ← generated plugin (committed, never hand-edited)
  agents/first-principles.md    ← assembled agent (sync-content.py output)
  references/                   ← verbatim copies of shared/references/ + spine refs
  references/<slug>-detail.md   ← generated on-demand detail sibling (agent surface)
  references/examples/          ← verbatim copies of shared/examples/
  references/persona-examples/  ← verbatim copies of shared/persona-examples/
  skills/<slug>/SKILL.md        ← generated stubs from shared/skills/<slug>/SKILL.md
  skills/<slug>/references/<slug>-detail.md  ← generated on-demand detail sibling (skill-stub surface)
  README.md
  LICENSE
```

The reference tree lives at plugin root, not under `agents/` (Claude Code registers every file in `agents/` subdirectories as a selectable agent type). `scripts/sync-content.py --check` enforces this: any stray file under `first-principles/agents/` other than `first-principles.md` fails the gate. 

`scripts/sync-content.py --write` regenerates from `shared/`: the assembled agent, all reference trees, skill files, and detail siblings. Every generated file carries `<!-- GENERATED — DO NOT EDIT -->`.

### Token substitution

- `{{TOOL:slug}}` → phrase from `tool-map.yml` (agent key)
- `{{PROCEDURE:slug}}` → full body from `shared/references/<slug>.md`
- `-detail.md` pointers use `references/<slug>-detail.md` in agent/skill surfaces; bare paths in `shared/references/`

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md#token-substitution) for full detail.

### Plugin layout

The plugin root is `first-principles/` with the agent at `first-principles/agents/first-principles.md`. Fifteen skills (thirteen companions, launcher, persona) live under `first-principles/skills/<slug>/SKILL.md` — all slash-only (`disable-model-invocation: true`).

### CI gates

<!-- GENERATED — DO NOT EDIT. Source: scripts/_gate_registry.py. Regenerate via: scripts/gen-gate-docs.py --write. -->
Both surfaces render the same population and the same columns from `scripts/_gate_registry.py`, emitted by `scripts/gen-gate-docs.py --write`, so the two cannot diverge; a working session still sees the full gate list here without opening `docs/`, and per-gate detail lives in `docs/gates/<GATE-ID>.md`. Every gate below except PROV-GUARD and QUAL-01 runs in `.github/workflows/validation.yml` on push/PR to master; PROV-GUARD and QUAL-01 are battery-only — they have no CI job, and `bash scripts/check-firewall-battery.sh` is the only thing that runs them.

| Gate | Job / Mechanism | Script | What it checks |
|------|-----------------|--------|-----------------|
| VAL-01 | `plugin-validate` (CI) | `claude plugin validate` | Plugin manifest schema validity via `claude plugin validate`. Spends zero model tokens. Does NOT validate the agent frontmatter — the CLI walks subdirectories of `agents/` and never inspects a flat `agents/*.md`, so GATE-01 is the sole validator of agent frontmatter. That same walk is a runtime fact, not just a validator quirk: at session start Claude Code registers every Markdown file it finds in a subdirectory of a plugin's `agents/` tree as its own selectable agent type, which is why the reference tree ships at `first-principles/references/` rather than nested under `agents/`, and why `sync-content.py --check` fails on any stray file reappearing under `first-principles/agents/`. See [`docs/gates/VAL-01.md`](docs/gates/VAL-01.md). |
| VAL-02 | `markdownlint` (CI) | `markdownlint-cli2` | MD style across `first-principles/**/*.md` via `markdownlint-cli2`. See [`docs/gates/VAL-02.md`](docs/gates/VAL-02.md). |
| VAL-03 | `check-links` (CI) | `scripts/check-links.py --self-test` | Relative Markdown link validity across the plugin, `shared/`, and `docs/` trees; `docs/` anchors validated with a github-slugger rule. Three legs: self-test, a live scan, and a pytest run of `check-links_anchors_test.py`. The third leg needs a pytest-capable interpreter — when none is found the battery still runs legs 1-2 through `gate_prereq` and reports [PREREQ]/BLOCKED rather than [PASS]/GREEN. (scan_globs=3 entries; locked_constants=2 entries) See [`docs/gates/VAL-03.md`](docs/gates/VAL-03.md). |
| VERSION-01 | `check-version-stamps` (CI) | `scripts/check-version-stamps.py --self-test` | Every hand-maintained version stamp carries the same value. Runs the live scan as well as the self-test — the invariant is a property of the working tree, not of the script's own fixtures. (derived_counts=1 entries; registered_surfaces=4) See [`docs/gates/VERSION-01.md`](docs/gates/VERSION-01.md). |
| REG-GUARD | `check-registration` (CI) | `scripts/check-registration.py --self-test` | Registration completeness over two surfaces: (a) every skill directory and the main agent carry a frontmatter `name:` matching their own basename, and every skill stub's `disable-model-invocation` is `true` -- the property VAL-04's 4-gram collision scan was a proxy for (999.104); (b) every gate this file's own battery registers has a matching `name: <job> (<GATE-ID>)` job in `.github/workflows/validation.yml`, the gates named in `BATTERY_ONLY_GATE_IDS` exempt. This module's D-01 floor deliberately reuses `check-registration.py`'s `_BATTERY_GATE_RE` parsing semantics rather than inventing a second grammar over the same file. (control_ids=32; control_count=32; registered_surfaces=2; checked_files=4; locked_constants=2 entries) See [`docs/gates/REG-GUARD.md`](docs/gates/REG-GUARD.md). |
| DUAL-04 | `sync-check` (CI) | `scripts/sync-content.py --check` | `shared/` and the generated `first-principles/` tree are in sync. (derived_counts=1 entries; registered_surfaces=4; locked_constants=1 entries; control_ids=14; control_count=14) See [`docs/gates/DUAL-04.md`](docs/gates/DUAL-04.md). |
| GATE-02-v8.5 | `GATE-02-v8.5` | `scripts/sync-content.py --self-test` | Pointer drift-guard: each of the four split core reference files' extracted Procedure slice carries exactly one well-formed link to its own `-detail.md` sibling. Proves the pointer exists and is well-formed, NOT that it is followed. Same script as DUAL-04, a different flag — the D-03 case for a flat `--describe` namespace rather than a per-gate id argument. See [`docs/gates/GATE-02-v8.5.md`](docs/gates/GATE-02-v8.5.md). |
| GATE-01 | `check-agent` (CI) | `scripts/check-agent.py --self-test` | Agent structural checks — 8 frontmatter/body assertions on the shipped agent, including the exact `maxTurns` value (60) and the exact `disallowedTools` list, not merely their presence. The live leg targets the repo-anchored `AGENT_FILE` constant, so the gate is cwd-independent and cannot be silently re-pointed. (branch_roster=8; branch_count=8; scoped_branches=4; locked_constants=4 entries; checked_files=1; disclosed_bounds_anchors=1) See [`docs/gates/GATE-01.md`](docs/gates/GATE-01.md). |
| BATT-06 | `check-routing-battery` (CI) | `scripts/check-routing-battery.py --self-test` | Offline merged dual-signal routing-battery self-test (boundary + focused-output); owns the honest-state and anti-masking sentinels. (locked_constants=4 entries; disclosed_bounds_anchors=11; derived_counts=1 entries; checked_files=1) See [`docs/gates/BATT-06.md`](docs/gates/BATT-06.md). |
| STEP0-08 | `check-step0-emulator` (CI) | `scripts/check-step0-emulator.py --self-test` | Offline Step 0 phrase-detection classifier self-test. (locked_constants=1 entries; derived_counts=2 entries; disclosed_bounds_anchors=6; checked_files=2) See [`docs/gates/STEP0-08.md`](docs/gates/STEP0-08.md). |
| STEP0-06 | `check-step0-live` (CI) | `scripts/check-step0-live.py --self-test` | Offline Step 0 live-harness scoring/parsing logic self-test. (locked_constants=2 entries; checked_files=2; control_ids=25; control_count=25) See [`docs/gates/STEP0-06.md`](docs/gates/STEP0-06.md). |
| TRACE-03 | `check-traceability` (CI) | `scripts/check-traceability.py --self-test` | Offline traceability gate self-test — capability/tier schema, artifact resolution, a live row-field leg checking every matrix row's surfaces value against the shipped-skill vocabulary and every row's statement for presence and marker/citation form, every row's re-run field (`rerun_by`) for vocabulary, tier consistency and, for `ci`, a CI-job registry entry (`battery-only`, `pre-commit-only` and `live-manual` are checked for vocabulary and tier consistency only, never against a registry, so a row can overstate one of those runners and stay green; archive-era wording is not re-read in CI or by any tracked tool), re-reading any tracked-surface citation, plus the HEADLINE-LOCK sentinel asserting the published coverage headline against five named current-fact surfaces and both tracked matrix artifacts. (`docs/*.md`, `CLAUDE.md`, `CHANGELOG.md`, `README.md`; registered_surfaces=5; branch_roster=19; branch_count=19; locked_constants=4 entries; coverage_headline=2 entries) See [`docs/gates/TRACE-03.md`](docs/gates/TRACE-03.md). |
| CONF-DRIFT | battery only (inline) | `scripts/report-conformance.py --check` | `docs/conformance-baseline.md` and `docs/data/conformance.json` reproduce byte-for-byte a fresh `report-conformance.py` run. Regardless of regeneration it also fails when the caught adversarial-corpus set moves against `_CORPUS_TARGET_CAUGHT_LOCK` (`TARGET CAUGHT-SET DRIFT`) or when a corpus or live-conformance floor fails, so regenerating the two artifacts does not clear it. Run inline by the offline battery — no CI job, and no pre-commit hook since Phase 89 D-01; registered in the battery at Phase 90 (backlog 999.38), after a stretch in which it ran nowhere. (registered_surfaces=5; checked_files=2; locked_constants=1 entries) See [`docs/gates/CONF-DRIFT.md`](docs/gates/CONF-DRIFT.md). |
| QUAL-01 | battery only — not a CI job | `scripts/check-quality-harness.py --self-test` | Offline blind A/B quality-measurement harness self-test — extraction guardrails, scoreline parsing, blinding, tabulation, baseline-fixture integrity, the mechanical defect detector, and the emission rendering contract's six legs. One of the named battery-only CI exemptions in REG-GUARD's `BATTERY_ONLY_GATE_IDS`. (control_ids=27; control_count=27; registered_surfaces=4; disclosed_bounds_anchors=30; derived_counts=4 entries; locked_constants=3 entries; contract_pins=3 entries) See [`docs/gates/QUAL-01.md`](docs/gates/QUAL-01.md). |
| PROV-GUARD | battery only — not a CI job | `scripts/check-provenance.py --self-test` | The self-test is an offline regression test of the verifier's own parsing, join and literal-location logic (D-16 positive/negative/anti-masking controls), not a product guard. Its only live input was the frozen `tests/quality-provenance-v8.24/` fixture (7/7 sources matched, 35/35 literals located), now outside the battery and CI — relaxed to battery-only under 999.107 option B (`docs/v9.4-gate-retirement.md` §2.4). One of the named battery-only CI exemptions in REG-GUARD's `BATTERY_ONLY_GATE_IDS`. (control_ids=33; control_count=33; registered_surfaces=2; locked_constants=1 entries) See [`docs/gates/PROV-GUARD.md`](docs/gates/PROV-GUARD.md). |
| HARN-01 | `check-act-limb` (CI) | `scripts/check-act-limb.py --self-test` | Offline Act-limb gate: the Phase 3 verification step and the Criterion 3 Fix note are present, correctly placed, and internally coherent in the emitted tree. (branch_roster=17; branch_count=17; control_ids=87; control_count=87; checked_files=2; disclosed_bounds_anchors=4) See [`docs/gates/HARN-01.md`](docs/gates/HARN-01.md). |
| HARN-02 | `check-loop-closure` (CI) | `scripts/check-loop-closure.py --self-test` | Observe->Perceive re-entry edges: a Criterion 1 Absent verdict routes back to Phase 1, every re-entry edge is bounded to one re-perception pass, and a fired edge is recorded. (checked_files=3; control_ids=38; control_count=38) See [`docs/gates/HARN-02.md`](docs/gates/HARN-02.md). |
| HARN-03 | `check-focused-parity` (CI) | `scripts/check-focused-parity.py --self-test` | Focused-mode parity: stub surface, agent surface and cross-surface parity-token set equality, with the D-12 anchor-control ratchet. A named non-technique exemption set (`NON_TECHNIQUE_SLUGS`) excludes non-technique skills from the technique checks, and its must-fail control fails if any technique slug is added to it. (locked_constants=3 entries; registered_surfaces=3; disclosed_bounds_anchors=1) See [`docs/gates/HARN-03.md`](docs/gates/HARN-03.md). |
| SCAN-GUARD | `check-selfaudit-scan` (CI) | `scripts/check-selfaudit-scan.py --self-test` | Self-audit scan structural gate: the Phase 15 self-audit scan prescription, its rubric verify block, and the Criterion-2-widened Verdict Block Format admission are present, correctly placed and internally coherent in the emitted tree, with one hundred clause-level named branches floored by an independent transcription (`_BRANCH_ROSTER_LOCK`). (branch_roster=100; branch_count=100; registered_surfaces=2; call_site_census=4 entries; control_ids=12; control_count=12; locked_constants=1 entries) See [`docs/gates/SCAN-GUARD.md`](docs/gates/SCAN-GUARD.md). |
| HC-BOUND | `check-high-confidence-bound` (CI) | `scripts/check-high-confidence-bound.py --self-test` | Structural validation gate: Phase 5 tightening of Criterion 3 (Evidence) and Criterion 5 (Conclusion) HIGH-confidence bound is present and well-formed on both rubric surfaces, and all three documented EXCEPT exceptions are present. (registered_surfaces=2; derived_counts=1 entries; disclosed_bounds_anchors=3) See [`docs/gates/HC-BOUND.md`](docs/gates/HC-BOUND.md). |
| CONF-GATE | `check-conf-gate` (CI) | `scripts/check-conf-gate.py --self-test` | Standing exemplar-conformance comparator: the four conformance counts on both gated example surfaces against source-literal targets, a 14-entry claim floor locked by equality to the live-discovered `shared-examples` ids, the D-03 prescribed-lead-in rule, and the marked-claim ratchet (may fall, never rise). (registered_surfaces=2; population_floors=2 entries; call_site_census=7 entries; control_ids=45; control_count=45; locked_constants=2 entries) See [`docs/gates/CONF-GATE.md`](docs/gates/CONF-GATE.md). |
| INVARIANT-CHECK | battery only (inline) | — | Anti-masking constants still hold in `scripts/_battery_core.py`: pre-mortem=9 fishbone=7 inversion=13 trade-off=10 MIN_HEADER_HITS=2. A direct value-grep double-check of what BATT-06 and STEP0-08 already assert internally. See [`docs/gates/INVARIANT-CHECK.md`](docs/gates/INVARIANT-CHECK.md). |
| FROZEN-EVIDENCE | battery only (inline) | — | Frozen baselines and captures are unmodified relative to HEAD, plus an untracked-files sweep over the same paths. `_FROZEN_PATHS` grows over time; this inline check increments the battery tally once regardless of array length. See [`docs/gates/FROZEN-EVIDENCE.md`](docs/gates/FROZEN-EVIDENCE.md). |
| — | sync-drift gate (pre-commit) | `scripts/sync-content.py --check` | `shared/` and the generated tree are in sync — the same check as DUAL-04, fired before commit rather than in CI/battery. See [`docs/gates/PRECOMMIT-sync-drift-gate.md`](docs/gates/PRECOMMIT-sync-drift-gate.md). |
| — | conformance generator self-test (pre-commit) | `scripts/report-conformance.py --self-test` | Blocks if `scripts/report-conformance.py --self-test` fails: runs the generator's own falsifiability controls at commit time (WR-05). It does not compare the committed baseline against a fresh run; that comparison (`report-conformance.py --check`) no longer runs in the hooks and runs in the offline battery as inline check CONF-DRIFT. (control_ids=111; control_count=111) See [`docs/gates/PRECOMMIT-conformance-generator-self-test.md`](docs/gates/PRECOMMIT-conformance-generator-self-test.md). |
| — | claim-surface generator self-test (pre-commit) | `scripts/gen-gate-docs.py --self-test` | Blocks if `scripts/gen-gate-docs.py --self-test` fails: runs the generator's own controls at commit time (WR-05). Two of them (`check-dispatch-wired`, `nondeterminism-exit-2`) drive `main(["--check"])` against the working tree, so the claim-surface drift comparison runs inside this self-test, not after it, and stale generated surfaces block a commit even under the `SKIP_DRIFT_CHECK` fast path. The standalone `--check` runs in the battery and CI as CONF-SURFACE. See [`docs/gates/PRECOMMIT-claim-surface-generator-self-test.md`](docs/gates/PRECOMMIT-claim-surface-generator-self-test.md). |
| CONF-SURFACE | `gen-gate-docs` (CI) | `scripts/gen-gate-docs.py --self-test` | The claim-surface drift gate itself: regenerates `CLAUDE.md`'s and docs/ARCHITECTURE.md's gate tables and docs/gates/<ID>.md pages from this registry's ENTRIES and every gate's --describe emission, and fails on drift. Registered in the battery, with a matching `gen-gate-docs (CONF-SURFACE)` CI job and both pre-commit hooks (plan 21-11, D-21-C). (registered_surfaces=46; checked_files=81; derived_counts=38 entries; disclosed_bounds_anchors=14; control_ids=111; control_count=111; locked_constants=2 entries) See [`docs/gates/CONF-SURFACE.md`](docs/gates/CONF-SURFACE.md). |
| RETRACT-01 | `check-retracted-claims` (CI) | `scripts/check-retracted-claims.py --self-test` | A claim a code review found false may never reappear on a published surface. Literal, not semantic: it bars the registered literals, never a reworded restatement, and a retracted claim nobody registers is invisible to it. Exemptions are (path, exact count) and fire in both directions — above the count a new occurrence crept in, below it the erratum that justified the exemption was deleted. `scripts/check-retracted-claims.py` is the sole excluded path, since the registry necessarily contains every literal it bars; control C10 pins that exclusion to a population of one. Added after v9.7.0 shipped seven blocking product defects, two of which were the same claim shipping twice: 55-CR-01 retracted the one-phase-per-technique premise and 58-CR-01 found it again three phases later in the requirements matrix, because the requirement statement generating that row was never updated alongside the fix. (registered_surfaces=9; derived_counts=2 entries; control_ids=14; control_count=14) See [`docs/gates/RETRACT-01.md`](docs/gates/RETRACT-01.md). |
| PROV-ROLLUP | `check-provenance-rollup` (CI) | `scripts/check-provenance-rollup.py --self-test` | The provenance roll-up's enumeration must agree with the section 3 it summarises. Not a presence check: the enumerated ids are compared against the document's own ground-truth population, so an emitted label cannot satisfy it, and the template's enumeration-governs rule — *where a count and its enumeration disagree, the enumeration governs* — is what makes the comparison decidable. A present roll-up over an empty section 3 is a FAILURE, never a pass: every enumeration agrees vacuously with an empty set, so that guard is what stops check 2 passing on everything. Line-format presence (check 1) and read-at-source coverage (check 3) are report-only by design and cannot fail — on live documents the line-format rate is a K-of-N live reading, barred from gating by `docs/v8.7-constraint-teardown.md` §2 item 3, and check 3 was downgraded on measurement because 17 of 19 observations named their location in the ground truth's own section-3 entry rather than on the roll-up line, which is a question the template does not settle. The locator reads only the template's line format, never the agent body's backticked prescription of the same content, so its presence count is a lower bound on content emission, not a measure of it. The self-test separately pins that line-format reading capture by capture on ten frozen corpora, as a regression pin of the locator on unchanged bytes, not a gate on any live rate. Whether a run opened the template is read directly from its transcript (the harness's reference-reads census, pinned capture by capture on two frozen corpora) rather than inferred from the roll-up's scarcity; the tripwire that keeps the template's line format — a line-anchored `?-marked:` — out of the agent body and the companion references stays. That tripwire reads line form only: the agent body already prescribes the roll-up's content, at its Phase 3 exit criterion, as a mid-line quotation the tripwire does not match. The shipped worked exemplars are fixed files rather than a live reading, so the self-test requires every one to carry a roll-up that passes check 2; live documents stay report-only. Added at backlog 999.173's registration residual: the checker shipped registered nowhere, so its reading gated nothing and 999.176's fourteen non-conforming exemplars shipped with the battery green. (registered_surfaces=2; `shared/references/*.md`; locked_constants=3 entries; derived_counts=10 entries; disclosed_bounds_anchors=14; control_ids=22; control_count=22) See [`docs/gates/PROV-ROLLUP.md`](docs/gates/PROV-ROLLUP.md). |
| CHAIN-JUDGE | `check-claim-chain-judge` (CI) | `scripts/check-claim-chain-judge.py --self-test` | The offline control suite of the only instrument in this tree that judges whether a conclusion's claim is SEMANTICALLY supported by the chain it cites, rather than merely citing it. Control groups plus anti-masking injections (counts in the table above are derived, never typed here), a scripted judge, no `claude` call. **What is registered is the `--self-test` only, and the distinction is the point.** The live semantic reading stays a manual measurement and is deliberately NOT gated: two passes over byte-identical input agreed on 7 of 13 documents and each reached 6 of 10 catalogued targets but not the same 6, and no precision figure exists by design (blocked on 999.118, whose exemplars must be re-derived first because the obvious negative class is not clean). Gating a reading that disagrees with itself would manufacture exactly the false confidence this instrument exists to detect. Registered at W2 2026-09-27 because it had shipped in no battery entry, no CI job and no registry record — the same state 999.173's residual was in when 999.176's fourteen non-conforming exemplars shipped with the battery green. (control_ids=7; control_count=7; registered_surfaces=1; disclosed_bounds_anchors=5) See [`docs/gates/CHAIN-JUDGE.md`](docs/gates/CHAIN-JUDGE.md). |
| EMIT-STAGE-A | `check-emission-stage-a` (CI) | `scripts/check-emission-stage-a.py --self-test` | Offline controls for the capture protocol that reads the AGENT'S OWN document rather than the main session's summary of it. C18/C19's sibling on the capture side: under `--plugin-dir`, `claude -p` stdout is the orchestrator's summary, and all ten arm-T captures of the v9.13 run were summaries carrying 0 of 6 contract sections and 0 ground-truth identifiers (`docs/trackb-transport-erratum.md`). Controls cover subagent extraction, multi-block joins, re-emitted documents, hand-back de-framing, and the delivery-route reading. Two of them exist because they caught real bugs in this script before it was trusted: C11 (keeping only the last text block lost 3 of 6 sections) and C12 (concatenating a re-emission double-counted every reading). C07 fails if the derivation detector is silently improved, because its published 1-of-2 sensitivity would then be stale. Offline and deterministic; the live capture run is manual and separate. (control_ids=21; control_count=21; registered_surfaces=2; checked_files=2; locked_constants=4 entries; disclosed_bounds_anchors=2) See [`docs/gates/EMIT-STAGE-A.md`](docs/gates/EMIT-STAGE-A.md). |
| EVIDENCE-01 | `gen-evidence-card` (CI) | `scripts/gen-evidence-card.py --self-test` | Every figure published on `docs/EVIDENCE.md` — the project's public, general-audience measurement record — is re-read from its cited source at generation time, and the committed page must reproduce a fresh render byte-for-byte. The pinned-literal mechanism is what makes the page falsifiable rather than merely typed: edit a source so it no longer says what the card claims and generation FAILS instead of publishing a stale number (verified by mutation, not assumed). This is a product-surface guard by `docs/PROCESS.md` §2's claim-audience cut — the card asserts measured facts to a reader outside the build loop — so a stale figure there is a product defect, not an apparatus one. The card publishes no composite quality score by construction (control C11 asserts it), because `docs/v8.7-correctness-spot-check.md` measured that rubric conformance does not predict correctness; a score assembled from conformance readings would look like quality and demonstrably is not. The comparative Track B section renders only on a `cleared` pre-registered result (C06/C07): a null or inconclusive run publishes nothing, enforced mechanically so it cannot be relitigated against a disappointing number afterwards. (registered_surfaces=1; checked_files=5; population_floors=1 entries; control_ids=13; control_count=13) See [`docs/gates/EVIDENCE-01.md`](docs/gates/EVIDENCE-01.md). |
| TRACKB-01 | `check-trackb-comparative` (CI) | `scripts/check-trackb-comparative.py --self-test` | Offline controls for the pre-registered agent-vs-unaided comparative harness — the project's first measurement against NOT using its own agent, every prior 'A/B' here having contrasted two versions of the same agent body. Two controls carry the integrity of the whole design. C01 fails if `docs/trackb-neutral-rubric.md` ever acquires a format token: scoring against the agent's own output contract would mark the control arm `Absent` for not being in the agent's format, producing a large and meaningless result, so rubric neutrality is the comparison's integrity rather than a stylistic preference. C13 asserts this script's pinned protocol constants still agree with the pre-registration's own stated text — a pre-registration whose executable form has drifted from it is not a pre-registration, and no other gate in this tree can see that drift. C08/C09/C10 are the threshold's own falsifiability set: a noise-sized effect must NOT clear, a run with no drift-control arm must NOT clear, and a real effect MUST clear, so the bar is reachable in both directions. Offline and deterministic; it never invokes `claude` and the live run is manual and separate. (registered_surfaces=4; control_ids=27; control_count=27) See [`docs/gates/TRACKB-01.md`](docs/gates/TRACKB-01.md). |
| SUMM-BLOCK | `check-summary-block` (CI) | `scripts/check-summary-block.py --self-test` | Finds exactly one structured-summary block at the end of a report's appendix, validates it against `shared/spine/references/summary-schema.json` with a stdlib validator driven by that file, and cross-checks every id and value against the report's own prose. Its must-fail controls are the parser failures agent-router's worked-example rerun recorded — a re-entry read from a Derivation Chains sentence, a Fix/Repeat disclosure missed, a rewritten first scoring pass, and a recommendation cut at the colon that introduces its list — rebuilt in-tree from the real reports, each required to fail for its own finding code while the same report with a correct block passes. Re-entry is read only from the Self-Audit Gate's fixed lines and the top-of-file disclosure. Also runs in exemplar mode over both worked-example surfaces, the source tree and its generated twin, so a later edit drifting an example's prose from its block does not stay silent — a field a legacy example cannot source is null exactly when its own section is absent. Reading live agent reports stays a recorded measurement, never a gate, and a live shortfall is reported, never absorbed by loosening the checker. It also compares the **Pre-check:** line directly above each section 4 Confidence line with that chain's head line, the bands it cites and the ceiling those imply, and section 6's with `conclusion.rests_on`, with section 4 for the bands it cites and with the ceiling those imply; it does not check that section 6's head names every chain the Conclusion rests on. A pre-check line anywhere else is never field-compared: in exemplar mode it fails, as does a Confidence line with no pre-check directly above it, and in live mode neither the misplacement nor the absence is reported. A band raised to its ceiling stays invisible to it. (control_ids=52; control_count=52; registered_surfaces=4; checked_files=4; locked_constants=3 entries; derived_counts=2 entries; disclosed_bounds_anchors=14) See [`docs/gates/SUMM-BLOCK.md`](docs/gates/SUMM-BLOCK.md). |
| FIG-GATE | `check-report-figures` (CI) | `scripts/check-report-figures.py --self-test` | Renders both figures of the typst library in `shared/spine/references/report-figures.md` (the shipped source) against the real-analysis fixture, a two-digit-id worst-case fixture and every worked example's structured-summary block, and asserts through `typst eval 'query(...)'` that drawn edges equal the total of every chain `rests_on` entry, conclusion edges equal `conclusion.rests_on`, the matrix total equals the assumption count, no label overflows its box and every SVG fits the text column. Must-fail controls — a dropped edge, a miscounted cell, a shrunk node, an edge dropped from a fixture — each fail for their own finding code alone. Counts come from the library's own metadata, not SVG geometry; legibility is checked by inspection, not by this gate. It also compiles the PDF page template in `shared/spine/references/report-layout.md` through the agent's own pandoc and typst pipeline over a worked example and the reading guide, and requires a real PDF from each; the template frozen from commit 45f6244a, which typst 0.15 cannot compile and which broke every reader-report PDF while the battery stayed green, must fail, as must a content-valued `document(author:)`. That proves the template compiles, not that the page looks right. typst or pandoc absent means BLOCKED, never PASS. (control_ids=16; control_count=16; registered_surfaces=4; checked_files=5; locked_constants=3 entries; derived_counts=3 entries; disclosed_bounds_anchors=8) See [`docs/gates/FIG-GATE.md`](docs/gates/FIG-GATE.md). |
| PERSONA-GATE | `check-persona-view` (CI) | `scripts/check-persona-view.py --self-test` | Checks a reader-persona view against the analysis it was derived from and the contract in `shared/spine/references/persona-views.md` — the memo header (To, Re, Basis, Band) and provenance sentence, the band against section 6, the role's word band, that every sentence carries a citation, that every cited chain, ground-truth (with matching `?` marking), assumption and dead-end id resolves in the source, that every number appears in the source, that the body is a memo — an In brief paragraph, then one paragraph per fixed question with no bullet, no label and no printed question (it counts paragraphs and cannot prove each answers its question), and that a lexical voice check (PV-DIRECTIVE) flags a denylisted imperative opener, second-person address, a verdict on the reader, or a six-word run of §6's recommended approach, over-reporting by design and never judging meaning. Must-fail controls — an invented id, an invented number, an uncited sentence, a wrong band, a missing header, an over-length body, among others — each fail for their own finding code alone, and stubbing id resolution turns the self-test red. It also checks the reading guide's names against the output template and its word ceiling. It proves a citation resolves, never that it supports its sentence, and its fixtures are hand-written memo views of shipped worked examples plus one frozen pre-87 example. (control_ids=40; control_count=40; registered_surfaces=3; checked_files=13; locked_constants=9 entries; derived_counts=4 entries; disclosed_bounds_anchors=9) See [`docs/gates/PERSONA-GATE.md`](docs/gates/PERSONA-GATE.md). |

Gates run on three surfaces: **28 in CI** (`.github/workflows/validation.yml`, on push/PR to master), **33 tallied in the offline battery** (`bash scripts/check-firewall-battery.sh`), and **3 pre-commit gates** (2 hook mechanisms run the identical set in the identical order). The battery is a strict superset of CI: all 28 CI gates plus 2 battery-only gates plus 3 inline checks. That is 28 + 2 + 3 = 33.
<!-- END GENERATED -->

HARN-01, HARN-02 and HARN-03 were registered under HARN-04 at v8.18.0 — each is a CI job plus a
single `--self-test`-only battery `gate` call, and each is counted in the battery total above.

**a guard guards the product; a guard is not itself guarded.** See [docs/PROCESS.md](docs/PROCESS.md) and the gate definition files in `docs/gates/` for full detail. The `bash scripts/check-firewall-battery.sh` runs the full offline gate set and prints a FIREWALL: GREEN / RED / BLOCKED verdict.

### Pre-commit gates

These gates fire on `git commit` (the count is in the generated sentence above), in this order, in both hook mechanisms:

1. **Sync-drift** — `shared/` ↔ generated tree are in sync (DUAL-04)
2. **Conformance generator self-test** — `scripts/report-conformance.py --self-test`
3. **Claim-surface generator self-test** — `scripts/gen-gate-docs.py --self-test`

With `SKIP_DRIFT_CHECK=1` the sync-drift gate is skipped and only the two self-tests run. The conformance-baseline drift check (`scripts/report-conformance.py --check`) does not run at commit time: the hooks never call it, and it runs in the offline battery as inline check CONF-DRIFT. The claim-surface drift comparison does run at commit time, in both modes: the claim-surface generator self-test's controls `check-dispatch-wired` and `nondeterminism-exit-2` drive `main(["--check"])` against the working tree, so stale generated surfaces block the commit even under `SKIP_DRIFT_CHECK=1`. Its standalone form (`scripts/gen-gate-docs.py --check`) also runs in the battery and in CI as CONF-SURFACE.

Bypass: `git commit --no-verify`

### Claims and falsifiers

**Key rule:** A factual claim requires a falsifier — a command that exits non-zero if the claim is false. Never rely on presence checks alone.

- Pair claims with falsifiers that test *truth*, not presence
- Plan-checker must re-derive falsifiers independently (never reuse planner's)
- Derive falsifiers from observed text, not model assumptions
- On claim retraction: add literal to `REGISTRY` in `scripts/check-retracted-claims.py` (RETRACT-01)
- **Literal counts:** Some gates pin literal counts (INVARIANT-CHECK: `pre-mortem=9 fishbone=7 inversion=13 trade-off=10 MIN_HEADER_HITS=2`). These are locked because they measure intrinsic agent design (technique marker counts, detection parameters), not generated output. Other counts (coverage headlines, control counts) should be auto-derived from source when safe to reduce cascading edits. See `scripts/_battery_core.py` for locked-count justification and `scripts/check-firewall-battery.sh` for validation.

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
binding, and this repository cannot pin which tools it holds. As installed when last checked
(`bm` plugin 4.9.0, read 2026-09-23 — the `tools:` line is unchanged from 4.5.5, checked in
both) it holds `Read`, `Write`, `Bash`, `Grep` and `Glob`;
re-derive that set from the installed agent definition's own `tools:` line before relying on
it. It reads this file, which is the only reach this repository has into its behaviour. The
first live test of whether this block is honoured was the `/bm:code-review` run of the phase that added it.

**The derived check a reviewer's output must satisfy**, stated as prose rather than as a gate:
every finding in a `REVIEW.md` carries a `product` or `apparatus` tier, and a finding carrying
neither is itself a defect in the review.

No script, control or CI job enforces any of this. D-08 rejected a findings-classifier
post-processor by name, and D-01 made the cut a judgement a path glob cannot decide — CR-05 is
the counterexample: an edit made entirely in `docs/` prose (`docs/README.md`,
`docs/MEASUREMENT-MAP.md` and `docs/COMPONENT-DIAGRAM.md`, the three files its own `File:` field
names) that produced a product-tier defect, which the rejected
`shared/`-plus-`first-principles/` glob would have tiered apparatus.


## Requirements surface

- **`docs/requirements-traceability.md`** — authoritative source. Current coverage:
  <!-- GENERATED:CLAUDE-COVERAGE-HEADLINE -->
  Active residuals, the current coverage headline
  (**277 reproducible / 269 audit-only / 0 gap / 546 total**), compact historical ledger, and gap
  findings.
  <!-- END GENERATED:CLAUDE-COVERAGE-HEADLINE -->

- **`docs/requirements-matrix.md`** — generated from:
  ```sh
  python3 scripts/check-traceability.py emit \
      --md-output docs/requirements-matrix.md \
      --json-output docs/data/matrix.json
  ```

- **`docs/v8.0-final-closure.md`** — historical record (Phase 142); not current.
- **`docs/history/`** — local-only per-milestone snapshots (git-ignored).
- **`docs/data/matrix.json`** — git-tracked structured sidecar to matrix.

## Step 0 measurement harness

- `scripts/check-step0-emulator.py` — offline phrase-detection (STEP0-08)
- `scripts/check-step0-live.py` — live agent-body harness (STEP0-06); baseline: `tests/step0-baseline-v8.5.md`

K-of-5 is recorded observation, not gated. See `docs/TESTING.md` and `docs/MEASUREMENT-MAP.md`.

### Measurement comparison

See [`docs/MEASUREMENT-MAP.md`](docs/MEASUREMENT-MAP.md#measurement-layers) for layer architecture.

| Tool | Measured | CI gate |
|------|----------|---------|
| `check-routing.py` | DELEGATE / NO-DELEGATE boundary | None |
| `check-routing-battery.py` | Dual-signal: boundary + focused-output (FU-21 gate) | BATT-06 |
| `check-step0-emulator.py` | Offline phrase-detection classifier | STEP0-08 |
| `check-step0-live.py` | Live MODE classification | STEP0-06 |

### Step 0 residual sentinels

BATT-06 and STEP0-08 own sentinels (RR-80-01, RR-79-01, RR-114-01, RR-117-01, RR-117-02, RR-119-01, RR-119-02, RR-108-02, RR-108-04, RR-108-05, RR-77-08) asserting documented honest counts against frozen captures. Do not edit without first reading:

- `docs/requirements-traceability.md` — active residuals, dispositions
- `docs/v8.0-final-closure.md` — terminal ACCEPTED-FINAL dispositions  
- `scripts/_battery_core.py` — sentinel source with lineage comments

### Key invariants

**Link resolution:** Agent-body links use `${CLAUDE_PLUGIN_ROOT}/references/` (session WD, not plugin dir). Skill stubs: file-relative for detail siblings, `${CLAUDE_PLUGIN_ROOT}/skills/<slug>/SKILL.md` for cross-technique peers. Reference tree at plugin root, never under `agents/`. VAL-03 full-checks all links.

**Skill structure:** `name:` matches parent directory exactly. `description:` third-person, ≤1,024 chars, no XML. `metadata.version:` double-quoted string. Reserved: `anthropic`, `claude` in names.

**Versioning:** Every hand-maintained version stamp carries the same value (VERSION-01). A bump touches all stamps or none.

See [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md#key-invariants) for gate enforcement.
