# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Claude Code **plugin** that ships a first-principles analysis agent (`first-principles:first-principles`) plus thirteen standalone slash-invocable companion skills (pre-mortem, inversion, fishbone, five-whys, trade-off, second-order, estimate, theoretical-limit, identify-essence, challenge-assumptions, ground-truths, reason-upward, validate). The entire deliverable is pure Markdown — no executable code ships inside the plugin.

## Commands

### Sync generated files from canonical source

```sh
python3 scripts/sync-content.py --write   # regenerate all target files
python3 scripts/sync-content.py --check   # verify no drift (exit 1 on drift)
uv run scripts/sync-content.py --write    # uv alternative (auto-resolves deps)
```

### Validation scripts (most need Python ≥ 3.12 + PyYAML; check-install-collisions.py is stdlib-only)

```sh
python3 scripts/check-agent.py            # GATE-01: agent structural checks
python3 scripts/check-links.py            # VAL-03: broken relative MD links
python3 scripts/check-trigger-collisions.py  # VAL-04: 4-gram collision scan across skills
python3 scripts/check-description-budget.py  # VAL-05: skill listing under 2000-char ceiling
python3 scripts/check-body-budget.py      # report-only line-count reporter; gate retired under TEARDOWN-01, see docs/v8.7-constraint-teardown.md
python3 scripts/check-install-collisions.py --self-test  # COLLIDE-01: dual-install name-collision self-test
python3 scripts/check-install-collisions.py              # COLLIDE-01: live-tree scan (vacuous if monolith absent)
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
      output-template.md        ← inlined into agent body by sync-content.py
      validation-rubric.md      ← inlined into agent body by sync-content.py
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

`{{TOOL:slug}}` tokens in `shared/spine/SKILL-body.md` are replaced by the `## Procedure` section extracted from `shared/references/<slug>.md`. This inlines the companion technique procedures directly into the agent body at generation time.

`{{PROCEDURE:slug}}` tokens in `shared/skills/<slug>/SKILL.md` are replaced by the full body of `shared/references/<slug>.md` (from `## When to reach for this` onward) when generating the focused-mode skill stubs.

**On-demand `-detail.md` load convention (v8.5 Phase 154):** `SLUGS_WITH_DETAIL` in `scripts/sync-content.py` is the single set of slugs authorised to carry a split `shared/references/<slug>-detail.md` appendix — every core-file `## Procedure` section ends with a named-trigger pointer block that directs the reader to the detail sibling on demand, rather than inlining that content into every emission. The pointer must appear exactly once per core file; the `GATE-02-v8.5` pointer drift-guard gate (see CI gates below) asserts this. Because the assembled agent body and the skill stub each sit one directory level above their own detail sibling, `_rewrite_detail_link()` adapts the pointer's link target to `references/<slug>-detail.md` on those two assembly surfaces, while the agent reference sibling (which lands alongside its own `<slug>-detail.md`) keeps the bare, unrewritten form.

### Plugin layout and skill registration

The plugin root is `first-principles/`. The agent is registered at `first-principles/agents/first-principles.md`. The thirteen companion skills live under `first-principles/skills/<slug>/SKILL.md` and are registered with `disable-model-invocation: true` (slash-only; the orchestrator never auto-routes to them).

Install for development: `claude --plugin-dir ./first-principles`

### CI gates

All gates run in `.github/workflows/validation.yml` on push/PR to master:

| Gate | Script | What it checks |
|------|--------|----------------|
| VAL-01 | `claude plugin validate` | Plugin schema validity |
| VAL-02 | `markdownlint-cli2` | MD style across `first-principles/**/*.md` |
| VAL-03 | `check-links.py --self-test` + `check-links.py` | Relative MD links resolve, now including `first-principles/skills/*/references/*.md` (full-check, D-01) and `first-principles/skills/*/SKILL.md` (namespace-ref-only, D-05); both new axes currently match zero live findings (v8.5 GATE-01, D-06) — the `--self-test` fixture is what makes them load-bearing until real content lands (Phase 154) |
| VAL-04 | `check-trigger-collisions.py` | No 4-gram collision across skill descriptions |
| VAL-05 | `check-description-budget.py` | All skill listings under 2000-char cap |
| DUAL-04 | `sync-content.py --check` | `shared/` and generated tree are in sync |
| GATE-02-v8.5 | `sync-content.py --self-test` | Offline pointer drift-guard (v8.5 Phase 154): asserts each of the four split core reference files' extracted Procedure slice contains exactly one well-formed link to its own detail sibling, carries per-file strip (missing) and duplicate negative controls plus a `main()` dispatch control, and proves the pointer exists and is well-formed — explicitly NOT that it is followed (Phase 156's live question). The label is milestone-qualified to distinguish it from the pre-existing v3.0 `GATE-02` bound to the trigger-collision scanner (`check-trigger-collisions.py`, D-12). |
| GATE-01 | `check-agent.py` | Agent structural checks |
| BATT-06 | `check-routing-battery.py --self-test` | Offline merged dual-signal routing-battery self-test (boundary + focused-output; deterministic, no live session) — owns the honest-state and anti-masking sentinels detailed in the [Routing battery](#routing-battery) section |
| STEP0-08 | `check-step0-emulator.py --self-test` | Offline Step 0 phrase-detection classifier self-test (deterministic, no live session); owns RR-80-01 emulator-layer assertion (S-N04 → full-composer, no trigger phrase fires); owns Category 7 SEMGATE named assertions (SEMGATE-02 — semantic-ambiguity co-fire / boundary disambiguation over the documented overlap pairs) |
| STEP0-06 | `check-step0-live.py --self-test` | Offline Step 0 live-harness self-test — scoring/parsing logic asserted with no live `claude` session (deterministic, mirrors STEP0-08 pattern) |
| TRACE-03 | `check-traceability.py --self-test` | Offline traceability gate self-test — capability/tier schema + artifact resolution fixtures (deterministic, no live session; only --self-test runs in CI — the `emit` subcommand is a manual regeneration step. `matrix.json` is tracked as of TEARDOWN-03, docs/v8.7-constraint-teardown.md.) |
| COLLIDE-01 | `check-install-collisions.py --self-test` | Offline dual-install name-collision self-test — detects skill/agent name collisions between plugin (`first-principles/`) and monolith (`first-principles-thinking/`) install surfaces (D-02: relaxes VAL-04's monolith exclusion for the NAME axis only; VAL-04 owns the trigger 4-gram axis, this gate owns the name-collision axis — orthogonal concerns; absent monolith dir is vacuously clean; deterministic, no live session) |
| QUAL-01 | `check-quality-harness.py --self-test` | Offline blind A/B quality-measurement harness self-test (deterministic, no live session) — extraction guardrails A/B, scoreline parser, blinding integrity, tabulation arithmetic, baseline-fixture integrity, and the mechanical defect detector; the promoted instrument behind the pre/post-fix quality baseline (HARNESS-01, `docs/v8.7-quality-baseline-freeze.md`) |

`bash scripts/check-firewall-battery.sh` runs the full offline gate set — currently **16/16** — in one shot and prints a FIREWALL: GREEN/RED verdict; QUAL-01 (added at v8.7 Phase 164, HARNESS-01) is what moved the battery from 15 to 16. See [`docs/v8.7-quality-baseline-freeze.md`](docs/v8.7-quality-baseline-freeze.md) and [`docs/v8.7-constraint-teardown.md`](docs/v8.7-constraint-teardown.md) for the milestone's full gate-composition and retired-constraint record.

### Pre-commit gates

One gate fires on `git commit` (whichever hook mechanism is active): the **sync-drift gate** —
blocks if `shared/` and the generated tree have diverged.

The agent body's line count (`first-principles/agents/first-principles.md`) is still reported by
`scripts/check-body-budget.py` on every run, but it no longer blocks a commit — the 644-line gate
was retired under TEARDOWN-01. See `docs/v8.7-constraint-teardown.md` for the evidence and the
standing record.

Bypass for intentional in-progress work: `git commit --no-verify`

### Routing battery

Two verifiers cover different layers of routing correctness. All issue prompts from a catalog file against a live `claude -p` session (one fresh session per prompt, sequential) and score verdicts from the `stream-json` event stream. Routing is non-deterministic — threshold K-of-N counts are the criterion, not per-run pass/fail.

**`check-routing.py`** — main agent routing battery. Scores DELEGATE / NO-DELEGATE. Pass thresholds: P-cases ≥ 11/13 DELEGATE **and** N-cases ≥ 18/20 NO-DELEGATE.

**`check-routing-battery.py`** — merged dual-signal battery. Captures each prompt once from `tests/routing-battery-catalog.md` and scores BOTH the boundary-discipline signal AND the focused-output signal (FU-21 gate, FOCUS-01) from the same stream, with a both-match per-prompt verdict. Namespaced thresholds default: boundary `--p-threshold 2`; focused-output `--p-threshold 4 --n-threshold 1`. Supports `--self-test` for an offline, deterministic self-check with no live claude session (BATT-06 CI gate); the BATT-06 `--self-test` (`_battery_core.self_test_boundary()`) owns the RR-80-01 marker-counting assertion (one bare pre-mortem hit < MIN_HEADER_HITS → classify() returns "none", not "focused-pre-mortem"), the RR-79-01 / RR-114-01 (supersedes RR-108-01; RESOLVED-STRUCTURALLY-OFFLINE Phase 121 OCH-02) / RR-108-02 honest-state sentinels (S-P01 pre-mortem v7.8 vector [1,2,3,0,2]; S-P02 inversion **re-pointed v7.11→v7.13 (Phase 138-02) → v8.5 (Phase 156)** via `_load_excerpt_v85`, v8.5 vector [0,0,0,0,0], CARRIED 0/5 live, inversion 13 markers post Phase 121; S-P05 trade-off v7.6 vector [2,2,2,2,1], CLOSED at 4/5, trade-off 10 markers post Phase 121), the RR-108-04 (S-P10 estimate) / RR-108-05 (S-P14 theoretical-limit) sentinels **re-pointed v7.11→v7.13 (Phase 138-02) → v8.5 (Phase 156)** via `_load_excerpt_v85` (v8.5 composer vectors both [0,0,0,0,0], tech-hit sums both [0,0,0,1,0]; both CARRIED 0/5 live, SUSTAINED at floor), the RR-117-01 fishbone sentinel **re-pointed to v8.6 (Phase 160)** via `_load_excerpt_v86` (v8.6 vector [2,2,2,3,4], 4/5 PASS CLOSE), and the RR-77-08 lock-only anti-masking boundary sentinel (the relative check `_rr7708_composer == _COMPOSER_FOCUS_CEILING - 1` asserted via adversarial fixture, no production code change — the literal `== 4` drift guard was retired under TEARDOWN-02, `docs/v8.7-constraint-teardown.md`). Detector marker counts (pre-mortem 9 / fishbone 7 / inversion 13 / trade-off 10) are byte-unchanged after Phase 156; RR-114-01/RR-108-04/RR-108-05 read the v8.5 captures while RR-117-01 reads the v8.6 captures (Phase 160 re-point) and all non-residual sentinels stay on v7.8/v7.11 evidence.

`check-sub-skill-routing.py` and `check-focused-output.py` are **deprecated thin shims** that translate the old per-script flags onto the merged battery and forward to `check-routing-battery.py`. They exist for backward compatibility only; new callers should invoke `check-routing-battery.py` directly.

Catalog fixtures: `tests/routing-catalog.md` (main agent routing battery), `tests/routing-battery-catalog.md` (merged boundary + focused-output battery).

See also: [Step 0 measurement harness](#step-0-measurement-harness) for the two-layer Step 0 classifier measurement tools that sit below the routing layer.

## Requirements surface

The canonical requirements and traceability surface lives in the git-tracked tree:

- **`docs/v8.0-final-closure.md`** — terminal state entry point: final baselines, accepted
  limitations (RR-114-01 1/5, RR-108-04 0/5, RR-108-05 0/5), final coverage headline
  (133 reproducible / 96 audit-only / 0 gap / 229 total), and deferred-ledger disposition
  summary. Start here for the v8.0 end-state. (Phase 142 terminal record.)
- **`docs/requirements-traceability.md`** — authoritative source of truth: active
  residuals, coverage headline (133 reproducible / 96 audit-only / 0 gap / 229 total),
  compact historical ledger, and gap findings. Start here. (Derived from regenerated matrix Phase 138 Plan 03.)
- **`docs/requirements-matrix.md`** — generated 229-row capability→requirement→test
  matrix. Regenerate with:
  ```sh
  python3 scripts/check-traceability.py emit \
      --md-output docs/requirements-matrix.md \
      --json-output .planning/phases/82-traceability-matrix-and-gap-findings/matrix.json
  ```
- **`docs/history/`** — frozen per-milestone REQUIREMENTS.md / ROADMAP.md /
  MILESTONE-AUDIT.md snapshots (26 milestones, v1.0 through v5.3).

`.planning/phases/82-traceability-matrix-and-gap-findings/matrix.json` is git-tracked as of
TEARDOWN-03 (`docs/v8.7-constraint-teardown.md`) rather than gitignored, so regenerating the
matrix via the `emit` subcommand above now dirties a tracked file, not an ignored one.

## Step 0 measurement harness

Two tools measure the agent body's Step 0 technique-selection logic, at different layers. They complement the routing battery (see [Routing battery](#routing-battery)) and each other.

**`scripts/check-step0-emulator.py`** — offline Step 0 phrase-detection emulator. Reads the `**Phrase detection rules**` table from `shared/spine/SKILL-body.md`, compiles each trigger phrase into a deterministic regex classifier, and classifies an input prompt to `MODE` (`focused-<technique>` or `full-composer`). No live `claude` session required. `--self-test` runs fault-injection fixtures (D-05 corruption modes) and the full `tests/step0-fixture-catalog.md` classification suite; it is the **STEP0-08 CI gate**. There is no heavy manual run — `--self-test` is the only supported batch mode.

**`scripts/check-step0-live.py`** — live Step 0 agent-body harness. Forces invocation of the agent body against the verbatim oblique prompt via the approach-② `_wrap_for_bypass` bypass channel, over the Plan-36-locked `claude -p --output-format stream-json --verbose` transport. Classifies each run's `MODE` from the captured `.jsonl` stream using `_classify_mode` (with the harness-side `none`→`full-composer` inference fix — D-01/D-02). Scores K-of-N results across the 12-row `tests/step0-fixture-catalog.md`. The full manual run uses `--repeat 5 --min-pass 3` (60 live `claude` invocations — manual only, not run in CI); the canonical baseline is `tests/step0-baseline-v7.8.md` (Phase 119 v7.8 CONF-03; prior baselines are frozen in `tests/step0-baseline-v*.md`). Its offline `--self-test` (no `claude` invocation) is the **STEP0-06 CI gate**.

**K-of-5 is a recorded observation, not a gate (governing record §2 item 3, `docs/v8.7-constraint-teardown.md`).** A K-of-5 result from this harness is demoted to an observation that a phase records — it may not gate a phase. The evidence: the S-P04 (five-whys) vector swung 2/5 → 0/5 → 2/5 across v7.11, v8.5, and v8.6 with no source change to the five-whys technique between those measurements. At N=5, noise equals effect. The tool itself is untouched — its pass-threshold flag and its verdict line survive byte-unchanged, because every frozen baseline from v7.4 through v8.6 depends on that comparability staying intact; what changed is the authority a phase gives the verdict, not the verdict itself.

### Measurement comparison

| Tool | Measured layer | Run command | CI gate |
|------|---------------|-------------|---------|
| `check-routing.py` | Main-agent DELEGATE / NO-DELEGATE routing boundary | `--catalog tests/routing-catalog.md --repeat 5 --min-pass 3` | None — developer tool, not wired into `validation.yml` |
| `check-routing-battery.py` | Merged dual-signal: boundary + focused-output (FU-21 gate, FOCUS-01) | `--repeat 5 --min-pass 3` / offline `--self-test` | BATT-06 |
| `check-step0-emulator.py` | Offline Step 0 phrase-detection classifier (deterministic, no live session) | `--self-test` | STEP0-08 |
| `check-step0-live.py` | Live Step 0 MODE classification via approach-② bypass channel | Manual `--repeat 5 --min-pass 3` (60 invocations) / offline `--self-test` | STEP0-06 |

### RR-80-01 dual-layer ownership (S-N04 confirming gate)

**RR-80-01** (the S-N04 semantically-pre-mortem over-routing residual; NON_BLOCKING per `NON_BLOCKING_NEGATIVE_IDS`, D-16) is owned by a dual-layer offline confirming gate:

- **STEP0-08** (`check-step0-emulator.py --self-test`): a hardcoded named S-N04 assertion proving the phrase-detection emulator fires no trigger phrase on the S-N04 prompt and classifies it `full-composer` (catalog-independent inline literal).
- **BATT-06** (`check-routing-battery.py --self-test` → `_battery_core.self_test_boundary()`): a hardcoded named marker-counting assertion proving one bare pre-mortem header hit (count=1) is below `MIN_HEADER_HITS` (2), so `pre-mortem` does NOT enter the `fired` set and `classify()` returns `"none"` (not `"focused-pre-mortem"`).

RR-80-01 (S-N04) re-pointed through v6.4 → v7.4 (Phase 108) → v7.6 (Phase 114) → v7.7 (Phase 117 CONF-02) → **v7.8 (Phase 119 CONF-04)**: at the v7.8 CONF-03 re-baseline S-N04 is **5/5** (non-blocking; Phase-118 FIX-03/FIX-04 prose fix moved over bar; run5 is_error:true 74-char anomaly, count=0). The v7.8 vector is `[1, 1, 1, 1, 0]` over `tests/step0-captures-v7.8/S-N04-run{1..5}.txt`. The offline gate asserts the **documented count vector, not the live pass rate** (honesty-not-score). Both assertions are hardcoded (catalog-independent) per D-04.

### RR-79-01 (CLOSED v7.7; SUSTAINED v7.8) / RR-114-01 (supersedes RR-108-01) / RR-117-01 fishbone / RR-117-02 precision / RR-119-01 / RR-119-02 sentinels (Phase 85 → Phase 119 → Phase 138)

**v8.0 terminal disposition (Phase 142):** RR-114-01 (S-P02 inversion, true K/N 1/5 v7.13 live), RR-108-04 (S-P10 estimate, true K/N 0/5 v7.13 live), and RR-108-05 (S-P14 theoretical-limit, true K/N 0/5 v7.13 live) are ACCEPTED-FINAL documented known limitations. BATT-06 sentinels retained as regression guards (`_load_excerpt_v713`); no successor minted; no further live re-measure. The per-run vectors below record the honest frozen-capture measured state (honesty-not-score, D-01 global). **Superseded in part at Phase 156 (v8.5):** the byte-freeze relaxation (docs/v8.5-byte-freeze-relaxation.md) re-opened exactly RR-108-04 (S-P10) and RR-108-05 (S-P14) for one bounded live re-measure, and RR-114-01 (S-P02) was re-measured as the unsplit control; all three re-pointed to v8.5 via `_load_excerpt_v85` (S-P02 [0,0,0,0,0] 0/5, S-P10/S-P14 both 0/5 SUSTAINED at floor). No successor was minted, the IDs are kept, and the ACCEPTED-FINAL disposition stands — the v8.5 evidence confirms rather than overturns it.

**RR-79-01**, **RR-114-01**, **RR-117-01**, **RR-117-02**, **RR-119-01**, and **RR-119-02** are owned by **BATT-06** (`check-routing-battery.py --self-test` → `_battery_core.self_test_boundary()`). The `_load_excerpt_v78` helper (added Phase 119 CONF-04, Plan 03) reads `tests/step0-captures-v7.8/<id>-run<n>.txt`; `_load_excerpt_v77` retained for lineage (Phase 117 CONF-02 era; v7.7 captures byte-frozen); `_load_excerpt_v76` retained for lineage (RR-108-02 still reads v7.6); `_load_excerpt_v711` retained for lineage (RR-79-01/RR-117-02/RR-119-01/RR-119-02 read v7.8; non-residual sentinels byte-frozen); `_load_excerpt_v713` added Phase 138-02 — reads `tests/step0-captures-v7.13/<id>-run<n>.txt`, now retained for lineage after its three sentinels re-pointed onward to v8.5; `_load_excerpt_v85` added Phase 156 MEASURE-03 SC-4 — reads `tests/step0-captures-v8.5/<id>-run<n>.txt` for the three still-v8.5 sentinels (RR-114-01 S-P02 inversion 0/5 FAIL CARRIED, RR-108-04 S-P10 estimate 0/5 CARRIED, RR-108-05 S-P14 theoretical-limit 0/5 CARRIED); a new `_load_excerpt_v86` helper (Phase 160) reads `tests/step0-captures-v8.6/<id>-run<n>.txt`, and RR-117-01 (S-P03 fishbone) re-pointed onward from v8.5 to v8.6 via this helper (4/5 PASS CLOSE); `_load_excerpt_v85` is retained for lineage and still serves RR-114-01/RR-108-04/RR-108-05; prior generation helpers all stay defined and byte-frozen for lineage.

- **RR-79-01** (**CLOSED at Phase 117 v7.7 CONF-01** — S-P01 pre-mortem 3/5 ≥ min-pass; FIX-01 confirmed out-of-sample; **CLOSE SUSTAINED at Phase 119 v7.8 CONF-03** — S-P01 3/5 = v7.4 floor): re-pointed to v7.8 captures (Phase 119 CONF-04, D-04 step two). Asserts the S-P01 per-run pre-mortem distinct-marker count vector == [1, 2, 3, 0, 2] over the 5 v7.8 live CONF-03 excerpts in `tests/step0-captures-v7.8/S-P01-run{1..5}.txt`. Drift guard: `len(_TECHNIQUE_CATEGORIES["pre-mortem"]) == 9`. Positive counter-checks: run2=2 and run3=3 each >= `MIN_HEADER_HITS=2`. CLOSE keeps the RR-79-01 ID (RR-108-02 CLOSE precedent per D-09); sentinel retained as regression guard.
- **RR-114-01** (supersedes RR-108-01; S-P02 inversion CARRIED 1/5 at the Phase 114 v7.6 re-baseline; **RESOLVED-STRUCTURALLY-OFFLINE Phase 121 OCH-02**; **re-pointed v7.11→v7.13 Phase 138-02, D-03**): now asserts the per-run inversion composite-marker count vector == [5, 4, 5, 5, 4] over the 5 v7.13 excerpts in `tests/step0-captures-v7.13/S-P02-run{1..5}.txt` via `_load_excerpt_v713`. Drift guard: `len(_TECHNIQUE_CATEGORIES["inversion"]) == 13` (Phase 121 OCH-02 extended inversion 9→13 by adding 4 heading-anchored output-contract markers: ## Inverted Claim / ## Failure-Guaranteeing Conditions / ## Necessary Preconditions / ## Stress-Test Verdict). Positive counter-checks: all v7.13 runs >= MIN_HEADER_HITS (detector reachable on every run); synthetic 2-marker text confirms detector fires. Disposition: detector reads the headers on every run; live S-P02 1/5 CARRIED (all 5 runs detected inversion output, but 4 runs also had significant composer structure → CEILING suppressed — see v7.13 verdict). Frozen v7.13 composite vector [5,4,5,5,4] asserted (honesty-not-score, D-01). Prior v7.6 vector [2,0,1,1,1] on frozen captures; retained for lineage. ID kept; no successor minted (D-04 step 3). **Re-pointed v7.13 → v8.5 at Phase 156 MEASURE-03 SC-4 (D-03)** via `_load_excerpt_v85` over tests/step0-captures-v8.5/S-P02-run{1..5}.txt: the v8.5 vector is [0, 0, 0, 0, 0] (S-P02 0/5 FAIL CARRIED, down from the v7.13 1/5 floor). S-P02 is the unsplit inversion control, so the drop is not a split artifact; the v8.5 excerpts are orchestrator-summary prose that discusses the inversion without echoing the structural output-contract headers, so the detector counts 0 on every run. Because no real-excerpt run clears the bar, the per-run positive counter-check can no longer fire (recorded as a finding in the sentinel, not deleted); the synthetic 2-marker reachability check is retained as the sole non-vacuous proof. Prior v7.13/v7.6 vectors retained for lineage; drift guard inversion == 13 unchanged.
- **RR-117-01** (**CLOSED at Phase 117 v7.7 CONF-01** — S-P03 fishbone 5/5; first fishbone vector sentinel; RR-75-03 lineage; **CLOSE SUSTAINED at Phase 119 v7.8 CONF-03** — S-P03 4/5 ≥ v7.4 floor, D-1b softening): re-pointed to v7.8 captures (Phase 119 CONF-04, D-04 step two). Asserts the S-P03 per-run fishbone distinct-marker count vector == [1, 4, 2, 2, 3] over the 5 v7.8 live CONF-03 excerpts in `tests/step0-captures-v7.8/S-P03-run{1..5}.txt`. Drift guard: `len(_TECHNIQUE_CATEGORIES["fishbone"]) == 7`. Positive counter-checks: run2=4 and run5=3 each >= MIN_HEADER_HITS. Retained as regression guard. **Re-pointed v7.11 → v8.5 at Phase 156 MEASURE-03 SC-4 (D-03)** via `_load_excerpt_v85` over tests/step0-captures-v8.5/S-P03-run{1..5}.txt: the v8.5 vector is [2, 2, 1, 1, 2] (S-P03 3/5 PASS — CLOSE SUSTAINED per DEC-02's K/N >= 3/5 rule, down one from the v7.11 4/5 floor). The run2/run5 counter-check indices still clear the bar at v8.5 and are retained. D-05 fired-set finding (verdict §2): the drop is not a split artifact — the markers that dropped (cause_category, sub_causes, preset_6M_8P_4S) have source text still in the always-inlined core fishbone.md, and the structural anchor fishbone_or_ishikawa fired 5/5 on every run in both generations; what narrowed is procedural-vocabulary echo depth. The CORR-03 stale-prose inconsistency in the sentinel block (prose claimed v7.8 while the code read v7.11) was corrected as part of this re-point. Prior v7.8/v7.11 vectors retained for lineage. **Re-pointed v8.5 → v8.6 at Phase 160 (D-03)** via `_load_excerpt_v86` over tests/step0-captures-v8.6/S-P03-run{1..5}.txt: the v8.6 vector is [2, 2, 2, 3, 4] (S-P03 4/5 PASS — CLOSE SUSTAINED, up one from the v8.5 3/5 floor), drift guard `len(_TECHNIQUE_CATEGORIES["fishbone"]) == 7` retained unchanged; prior v8.5/v7.x vectors retained for lineage.
- **RR-117-02** (Phase 117 CONF-02 — S-N03 precision sentinel; **re-pointed to v7.8 Phase 119 CONF-04**): proves FIX-01+FIX-03/FIX-04 did NOT hurt routing on genuinely-oblique prompts. Asserts S-N03 per-run pre-mortem count vector == [1, 0, 0, 0, 0] over `tests/step0-captures-v7.8/S-N03-run{1..5}.txt` (9-marker post-fix detector; debugging prompt; all 5 runs stay below MIN_HEADER_HITS=2 → full-composer 5/5). D-17 precision finding sustained.
- **RR-119-01** (**NEW, Phase 119 CONF-04** — S-N01 over-routing resolved-over-bar): minted Phase 119 CONF-04, Plan 03. At v7.7: S-N01 0/5 (all-over-route). At v7.8 CONF-03: S-N01 3/5 PASS (Phase-118 FIX-03/FIX-04 prose fix). Asserts the S-N01 per-run pre-mortem distinct-marker count vector == [0, 2, 1, 1, 3] over `tests/step0-captures-v7.8/S-N01-run{1..5}.txt`. Positive counter-check: run2=2 >= MIN_HEADER_HITS (over-routes on that run — non-vacuous). Disposition: RESOLVED-OVER-BAR with under-count caveat (negative passes are a MIX of genuine clarification-holds and detector under-counts, D-01). NOT a reclassification (D-4).
- **RR-119-02** (**NEW, Phase 119 CONF-04** — S-N02 over-routing resolved-over-bar): minted Phase 119 CONF-04, Plan 03. At v7.7: S-N02 2/5 (over-routes on 3 of 5 runs). At v7.8 CONF-03: S-N02 3/5 PASS (Phase-118 FIX-03/FIX-04 prose fix). Asserts the S-N02 per-run pre-mortem distinct-marker count vector == [0, 3, 3, 1, 1] over `tests/step0-captures-v7.8/S-N02-run{1..5}.txt`. Positive counter-check: run2=3 >= MIN_HEADER_HITS (over-routes on that run — non-vacuous). Disposition: RESOLVED-OVER-BAR with under-count caveat (runs 2,3 are detector under-counts where agent still ran a pre-mortem, D-01). NOT a reclassification (D-4).

All sentinels assert the **documented honest state, not the live pass rate** (honesty-not-score, C-02). Excerpts are frozen read-only evidence; they are git-tracked so any tampering is visible in diff/PR review.

### RR-108-02 (CLOSED at v7.6) / RR-77-08 sentinels (Phase 85 → Phase 114)

**RR-108-02** (chain: RR-79-03 -> RR-92-02 -> RR-95-02 -> RR-108-02; **CLOSED at the Phase 114 v7.6 re-baseline**) and **RR-77-08** are owned by **BATT-06** (`check-routing-battery.py --self-test` → `_battery_core.self_test_boundary()`):

- **RR-108-02** (S-P05 trade-off, **CLOSED at 4/5 PASS** at the Phase 114 v7.6 re-baseline — improved from v7.4's 2/5; CLOSE keeps the RR-108-02 ID, no successor minted per D-04; **structurally extended Phase 121 OCH-02**): asserts the per-run trade-off distinct-marker count vector == [2, 2, 2, 2, 1] over the 5 v7.6 excerpts in `tests/step0-captures-v7.6/S-P05-run{1..5}.txt`. Drift guard: `len(_TECHNIQUE_CATEGORIES["trade-off"]) == 10` (Phase 121 OCH-02 extended trade-off 6→10 by adding 4 heading-anchored output-contract markers: ## Options / ## Criteria & Weights / ## Scoring / ## Recommendation). Positive counter-checks: run1=2 and run2=2 each >= MIN_HEADER_HITS (barrier cleared on runs 1-4 in v7.6, coherent with the live 4/5 PASS). Frozen v7.6 vector [2,2,2,2,1] UNCHANGED (captures predate the headers). Live trade-off emission re-measure terminally accepted as not-to-be-run at v8.0 (project wrapped; honesty-not-score, D-01 — see docs/v8.0-final-closure.md).
- **RR-77-08**: a lock-only anti-masking boundary sentinel. Its literal drift guard asserting the constant equals 4 was retired under TEARDOWN-02 (the freeze on retuning the constant is released — see `docs/v8.7-constraint-teardown.md`); what survives is the **relative** load-bearing assertion `_rr7708_composer == _COMPOSER_FOCUS_CEILING - 1`, proved via a synthetic adversarial fixture (a focused pre-mortem output containing Ground Truths + Derivation Chains + Verdict headers → `composer_hits=3`). At `CEILING=4`: `3 < 4` → `n==1` branch fires → `focused-pre-mortem` (correct). At a hypothetical `CEILING=3`: `3 >= 3` → `n==1` suppressed → `full-composer` (regression). Honest caveat: because the fixture's own `composer_hits` count is fixed at 3 in the sentinel's source, this relative check still binds the constant's value to 4 in practice — a future retune is a two-part edit (the constant itself and the fixture that proves it load-bearing), not a one-line change. No production code change beyond the drift-guard removal (D-05/D-06; research confirmed no current misclassification).

**RR-108-02** is an honest CLOSE (per `tests/step0-baseline-v7.6.md`) whose offline sentinel asserts the documented v7.6 count vector, not the live pass rate (honesty-not-score). The RR-108-04 (S-P10 estimate) and RR-108-05 (S-P14 theoretical-limit) sentinels were **re-pointed v7.11→v7.13 at Phase 138-02** (D-03): they asserted honest v7.13 composite count vectors ([0,5,4,0,3] for S-P10, [3,8,3,5,2] for S-P14) over `tests/step0-captures-v7.13/S-P{10,14}-run{1..5}.txt` via `_load_excerpt_v713`; both CARRIED 0/5 live (honesty-not-score, D-01). **Both were re-pointed v7.13 → v8.5 at Phase 156 MEASURE-03 SC-4 (D-03)** via `_load_excerpt_v85` over tests/step0-captures-v8.5/S-P{10,14}-run{1..5}.txt — authorized by the byte-freeze relaxation (docs/v8.5-byte-freeze-relaxation.md, which re-opened exactly these two residuals' re-measure): the v8.5 composer vectors are both [0, 0, 0, 0, 0] and the technique-hit sums both [0, 0, 0, 1, 0] (a single incidental run4 keyword match each); both remain 0/5 CARRIED — SUSTAINED at their own 0/5 v7.13 floor per DEC-02's adjacency rule. RR-108-03 (S-P09 decompose) stays byte-frozen on v7.4; prior v7.13 vectors retained for lineage. RR-108-03 (S-P09 decompose) remains byte-frozen on v7.4 evidence (RESOLVED-BY-MERGE v7.5). **RR-77-08** is a lock-only boundary sentinel: `_COMPOSER_FOCUS_CEILING` is already correctly set to 4 (Phase 77); this sentinel prevents silent regression. The Phase-118 fix is at the trigger layer (guard column + tiebreaker in `shared/spine/SKILL-body.md`); the detector markers (pre-mortem == 9, fishbone == 7) are byte-unchanged through Phase 138. The inversion and trade-off marker sets were extended in Phase 121 OCH-02 (9→13 and 6→10 respectively) by adding heading-anchored output-contract markers; this does not affect pre-mortem or fishbone counts.

### Key invariants

- All reference file links use forward slashes and are one level deep from the file that references them (never nested `a.md → b.md → c.md`).
- Skill `name` in frontmatter must match the parent directory name exactly.
- Skill `description` fields must be third-person, ≤ 1,024 chars, no XML tags.
- `metadata.version` must be a double-quoted YAML string (e.g. `version: "3.8"`), not a bare number.
- Reserved words `anthropic` and `claude` are forbidden in skill `name` fields.
