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

### Validation scripts (Python ≥ 3.12; those that parse frontmatter also need PyYAML — `check-body-budget.py`, `check-install-collisions.py` and `check-quality-harness.py` are stdlib-only)

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
```

This list is a convenience, not the authority — a hand-maintained list of gates goes stale by
construction. `bash scripts/check-firewall-battery.sh` runs the set that actually exists.

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

Every gate below except QUAL-01 runs in `.github/workflows/validation.yml` on push/PR to master.
QUAL-01 is battery-only — it has no CI job, and `bash scripts/check-firewall-battery.sh` is the
only thing that runs it. This table is kept here on purpose so a working session can see the
gate list without opening `docs/`; the canonical inventory, with CI job names and the
battery-only inline checks, is [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md#ci-and-pre-commit-gate-inventory).

| Gate | Script | What it checks |
|------|--------|----------------|
| VAL-01 | `claude plugin validate` | Plugin schema validity |
| VAL-02 | `markdownlint-cli2` | MD style across `first-principles/**/*.md` |
| VAL-03 | `check-links.py --self-test` + `check-links.py` | Relative MD links resolve, now including `first-principles/skills/*/references/*.md` (full-check, D-01) and `first-principles/skills/*/SKILL.md` (namespace-ref-only, D-05); both new axes currently match zero live findings (v8.5 GATE-01, D-06) — the `--self-test` fixture is what makes them load-bearing until real content lands (Phase 154) |
| VAL-04 | `check-trigger-collisions.py` | No 4-gram collision across skill descriptions |
| VAL-05 | `check-description-budget.py` | All skill listings under 2000-char cap |
| VERSION-01 | `check-version-stamps.py --self-test` + `check-version-stamps.py` | Every hand-maintained version stamp carries the same value (14 `shared/skills/*/SKILL.md` + `shared/spine/SKILL.meta.yml` + both manifests). Installs are version-gated, not content-gated, so one missed stamp ships an inert update with every other gate green — the v8.14 failure mode. The stamp count is reported, never asserted: a new skill is discovered by glob, and one missing its stamp fails on presence rather than on a magic number. The generated tree is out of scope — DUAL-04 already ties it to `shared/`. |
| DUAL-04 | `sync-content.py --check` | `shared/` and generated tree are in sync |
| GATE-02-v8.5 | `sync-content.py --self-test` | Offline pointer drift-guard (v8.5 Phase 154): asserts each of the four split core reference files' extracted Procedure slice contains exactly one well-formed link to its own detail sibling, carries per-file strip (missing) and duplicate negative controls plus a `main()` dispatch control, and proves the pointer exists and is well-formed — explicitly NOT that it is followed (Phase 156's live question). The label is milestone-qualified to distinguish it from the pre-existing v3.0 `GATE-02` bound to the trigger-collision scanner (`check-trigger-collisions.py`, D-12). |
| GATE-01 | `check-agent.py` | Agent structural checks |
| BATT-06 | `check-routing-battery.py --self-test` | Offline merged dual-signal routing-battery self-test (boundary + focused-output; deterministic, no live session) — owns the honest-state and anti-masking sentinels detailed in the [Routing battery](#routing-battery) section |
| STEP0-08 | `check-step0-emulator.py --self-test` | Offline Step 0 phrase-detection classifier self-test (deterministic, no live session); owns RR-80-01 emulator-layer assertion (S-N04 → full-composer, no trigger phrase fires); owns Category 7 SEMGATE named assertions (SEMGATE-02 — semantic-ambiguity co-fire / boundary disambiguation over the documented overlap pairs). **All six documented pairs are now locked** — the original three (S-A01/A03/A05) plus fishbone↔five-whys, theoretical-limit↔estimate and pre-mortem↔trade-off (S-A07/A09/A11, added by the 2026-08-16 audit's stream 6, finding CAP-1), each with a full-composer boundary control. Every pair is locked by a hardcoded literal *and* a catalog row, so the catalog can be deleted without the assertion going vacuous. VAL-04 is structurally blind to this axis — it scans skill descriptions, never the Step 0 phrase table — so this gate is the only thing standing between a phrase-table row reorder and a silent routing flip. |
| STEP0-06 | `check-step0-live.py --self-test` | Offline Step 0 live-harness self-test — scoring/parsing logic asserted with no live `claude` session (deterministic, mirrors STEP0-08 pattern) |
| TRACE-03 | `check-traceability.py --self-test` | Offline traceability gate self-test — capability/tier schema + artifact resolution fixtures (deterministic, no live session; only --self-test runs in CI — the `emit` subcommand is a manual regeneration step. `docs/data/matrix.json` is tracked as of TEARDOWN-03, docs/v8.7-constraint-teardown.md.) |
| COLLIDE-01 | `check-install-collisions.py --self-test` | Offline dual-install name-collision self-test — detects skill/agent name collisions between plugin (`first-principles/`) and monolith (`first-principles-thinking/`) install surfaces (D-02: relaxes VAL-04's monolith exclusion for the NAME axis only; VAL-04 owns the trigger 4-gram axis, this gate owns the name-collision axis — orthogonal concerns; absent monolith dir is vacuously clean; deterministic, no live session) |
| QUAL-01 | `check-quality-harness.py --self-test` | Offline blind A/B quality-measurement harness self-test (deterministic, no live session) — extraction guardrails A/B, scoreline parser, blinding integrity, tabulation arithmetic, baseline-fixture integrity, and the mechanical defect detector; the promoted instrument behind the pre/post-fix quality baseline (HARNESS-01, `docs/v8.7-quality-baseline-freeze.md`) |
| HARN-01 | `scripts/check-act-limb.py` | **not registered** — neither CI nor battery. Offline Act-limb gate: the Phase 3 verification step and the Criterion 3 Fix note are present, correctly placed, and internally coherent in the emitted tree |

HARN-01 is listed for discoverability only. It is **not registered** — neither CI nor battery — is **not** counted in any surface total on this page, and runs only when it is invoked directly. Phase 4 / HARN-04 owns registering it in `scripts/check-firewall-battery.sh` and moving the tally.

`bash scripts/check-firewall-battery.sh` runs the full offline gate set — currently **17/17** — in one shot and prints a FIREWALL: GREEN/RED verdict. QUAL-01 (added at v8.7 Phase 164, HARNESS-01) moved the battery from 15 to 16; VERSION-01 (added by the 2026-08-16 audit, [`docs/audit-2026-08-16-duplication-staleness.md`](docs/audit-2026-08-16-duplication-staleness.md)) moved it from 16 to 17. The tally is 15 `gate` registrations plus two inline checks (INVARIANT-CHECK, FROZEN-EVIDENCE); the body-size `[INFO]` line is deliberately untallied. See [`docs/v8.7-quality-baseline-freeze.md`](docs/v8.7-quality-baseline-freeze.md) and [`docs/v8.7-constraint-teardown.md`](docs/v8.7-constraint-teardown.md) for the milestone's full gate-composition and retired-constraint record.

### Pre-commit gates

One gate fires on `git commit` (whichever hook mechanism is active): the **sync-drift gate** —
blocks if `shared/` and the generated tree have diverged.

The agent body's line count (`first-principles/agents/first-principles.md`) is still reported by
`scripts/check-body-budget.py` on every run, but it no longer blocks a commit — the 644-line gate
was retired under TEARDOWN-01. See `docs/v8.7-constraint-teardown.md` for the evidence and the
standing record.

Bypass for intentional in-progress work: `git commit --no-verify`

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
  (**126 reproducible / 88 audit-only / 0 gap / 214 total**), compact historical ledger, and gap
  findings. (Derived from regenerated matrix Phase 138 Plan 03; META-Q4 re-tiered
  reproducible→audit-only in the v8.8 post-close TEARDOWN-01 cleanup, 133/96 → 132/97; 15
  v4.0/v4.1 builder requirements retired at quick task `260728-vxn`, 132/97 → 126/88,
  229 → 214 rows.)
- **`docs/v8.0-final-closure.md`** — **historical record, not current state.** Accepted
  limitations (RR-114-01 1/5, RR-108-04 0/5, RR-108-05 0/5) and deferred-ledger disposition as of
  v8.0 (Phase 142). It calls 133/96/0/229 the "final" coverage headline because v8.0 was meant to
  wrap the project; work continued and that figure has been superseded twice — see the bullet
  above. Do not quote its headline as current.
- **`docs/requirements-matrix.md`** — generated 214-row capability→requirement→test
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
