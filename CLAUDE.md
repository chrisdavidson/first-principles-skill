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
python3 scripts/check-provenance.py --self-test           # PROV-GUARD: provenance-verifier self-test (24 controls)
python3 scripts/check-provenance.py                        # PROV-GUARD: live coverage check against tests/quality-provenance-v8.24/
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

Every gate below except QUAL-01 runs in `.github/workflows/validation.yml` on push/PR to master.
QUAL-01 is battery-only — it has no CI job, and `bash scripts/check-firewall-battery.sh` is the
only thing that runs it. This table is kept here on purpose so a working session can see the
gate list without opening `docs/`; the canonical inventory, with CI job names and the
battery-only inline checks, is [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md#ci-and-pre-commit-gate-inventory).

| Gate | Script | What it checks |
|------|--------|----------------|
| VAL-01 | `claude plugin validate` | Plugin manifest schema validity — **and nothing else that matters.** It does *not* validate the agent: the CLI walks *subdirectories* of `agents/` and never inspects a flat `agents/*.md`, so it validates the 29 reference siblings under `agents/references/` (which are not agents) and skips `agents/first-principles.md` (which is). Verified 2026-08-30 against a minimal probe plugin: a flat `agents/solo.md` alone produces no `Validating agent:` line at all. Consequence: **GATE-01 is the sole validator of the agent frontmatter.** The 29 `No frontmatter block found` warnings are that same misclassification and are expected — do not "fix" them by adding frontmatter, which would make 29 inert content files look like agent definitions. `claude plugin details` confirms the *loader* is correct where the validator is not: `Agents (1)`. |
| VAL-02 | `markdownlint-cli2` | MD style across `first-principles/**/*.md` |
| VAL-03 | `check-links.py --self-test` + `check-links.py` | Relative MD links resolve, now including `first-principles/skills/*/references/*.md` (full-check, D-01) and `first-principles/skills/*/SKILL.md` (namespace-ref-only, D-05); both new axes currently match zero live findings (v8.5 GATE-01, D-06) — the `--self-test` fixture is what makes them load-bearing until real content lands (Phase 154) |
| VAL-04 | `check-trigger-collisions.py` | No 4-gram collision across skill descriptions |
| VAL-05 | `check-description-budget.py` | All skill listings under 2000-char cap |
| VERSION-01 | `check-version-stamps.py --self-test` + `check-version-stamps.py` | Every hand-maintained version stamp carries the same value (14 `shared/skills/*/SKILL.md` + `shared/spine/SKILL.meta.yml` + both manifests). Installs are version-gated, not content-gated, so one missed stamp ships an inert update with every other gate green — the v8.14 failure mode. The stamp count is reported, never asserted: a new skill is discovered by glob, and one missing its stamp fails on presence rather than on a magic number. The generated tree is out of scope — DUAL-04 already ties it to `shared/`. |
| REG-GUARD | `scripts/check-registration.py` | Registered — CI job `check-registration (REG-GUARD)` plus battery registration, both running `--self-test` **and** the live scan, matching VERSION-01, GATE-01 and COLLIDE-01. Offline registration completeness gate over **two** surfaces. (a) Plugin axis: every skill directory under `first-principles/skills/` and the main agent carry a frontmatter `name:` matching their own directory/file basename, and any manifest-declared additional paths resolve inside the plugin. (b) CI-job axis (WR-02, v8.24): every gate `scripts/check-firewall-battery.sh` registers has a matching `name: <job> (<GATE-ID>)` job in `.github/workflows/validation.yml`, with QUAL-01 the single named battery-only exemption — deleting a CI job used to leave every offline gate green, and is what made the v8.24 `GATE-02` matrix row's `reproducible` tier unfalsifiable. Self-test carries 29 isolated control fixtures with positive and anti-masking negative controls; because those fixtures are tempdir/in-memory and never read the shipped tree, only the live leg asserts either invariant on the shipped surfaces. |
| DUAL-04 | `sync-content.py --check` | `shared/` and generated tree are in sync |
| GATE-02-v8.5 | `sync-content.py --self-test` | Offline pointer drift-guard (v8.5 Phase 154): asserts each of the four split core reference files' extracted Procedure slice contains exactly one well-formed link to its own detail sibling, carries per-file strip (missing) and duplicate negative controls plus a `main()` dispatch control, and proves the pointer exists and is well-formed — explicitly NOT that it is followed (Phase 156's live question). The label is milestone-qualified to distinguish it from the pre-existing v3.0 `GATE-02` bound to the trigger-collision scanner (`check-trigger-collisions.py`, D-12). |
| GATE-01 | `check-agent.py` | Agent structural checks — 8 frontmatter/body assertions on the shipped agent. **Load-bearing alone: VAL-01 does not reach this file** (see the VAL-01 row). The live leg takes no `--file`; it targets the repo-anchored `AGENT_FILE` constant, so the gate is cwd-independent and its target cannot be silently re-pointed, and it prints a `COVERAGE —` line naming the file it validated. That PASS is backed by an anti-vacuity control (`_assert_live_coverage`): the frontmatter this run actually read is mutated to strip `name:`, and the gate fails unless the checker reports that specific defect — so a vacuous checker cannot report green. Unlike REG-GUARD's tempdir fixtures, this control runs on the **live** leg by design: the `--self-test` fixtures are in-memory and never read the shipped tree. |
| BATT-06 | `check-routing-battery.py --self-test` | Offline merged dual-signal routing-battery self-test (boundary + focused-output; deterministic, no live session) — owns the honest-state and anti-masking sentinels detailed in the [Routing battery](#routing-battery) section |
| STEP0-08 | `check-step0-emulator.py --self-test` | Offline Step 0 phrase-detection classifier self-test (deterministic, no live session); owns RR-80-01 emulator-layer assertion (S-N04 → full-composer, no trigger phrase fires); owns Category 7 SEMGATE named assertions (SEMGATE-02 — semantic-ambiguity co-fire / boundary disambiguation over the documented overlap pairs). **All six documented pairs are now locked** — the original three (S-A01/A03/A05) plus fishbone↔five-whys, theoretical-limit↔estimate and pre-mortem↔trade-off (S-A07/A09/A11, added by the 2026-08-16 audit's stream 6, finding CAP-1), each with a full-composer boundary control. Every pair is locked by a hardcoded literal *and* a catalog row, so the catalog can be deleted without the assertion going vacuous. VAL-04 is structurally blind to this axis — it scans skill descriptions, never the Step 0 phrase table — so this gate is the only thing standing between a phrase-table row reorder and a silent routing flip. |
| STEP0-06 | `check-step0-live.py --self-test` | Offline Step 0 live-harness self-test — scoring/parsing logic asserted with no live `claude` session (deterministic, mirrors STEP0-08 pattern) |
| TRACE-03 | `check-traceability.py --self-test` | Offline traceability gate self-test — capability/tier schema + artifact resolution fixtures, plus the `HEADLINE-LOCK` sentinel (WR-08, widened v8.25.0 Phase 10; arrow-anchoring and read-loop soundness fixes landed Phase 10 plans 08-09, structural-residual closures landed plan 10). Asserts the published coverage headline, recognizing both the prose and compact-slash renderings, against five named current-fact surfaces — `docs/requirements-traceability.md`, `CLAUDE.md`, `docs/README.md`, `docs/MEASUREMENT-MAP.md`, `docs/COMPONENT-DIAGRAM.md` (the last states only the compact-slash form, never the prose form, which is why two-rendering support is load-bearing rather than decorative) — plus the two tracked generated artifacts (`docs/requirements-matrix.md`, `docs/data/matrix.json`), all tied back to `build_matrix_rows()` with the figure appearing as a literal nowhere in the gate. A two-layer historical/delta exemption — whole-file membership, then a figure-adjacent arrow layer anchored to the headline literal itself: one of three recognised arrow renderings (`→`, `->`, or the HTML comment closer `-->` reused as an ASCII long arrow) must sit immediately adjacent to THIS line's headline mention, delimiting it from a digit run on one side or the other, so a mermaid edge, a bare HTML comment terminator, or an unrelated numeric arrow elsewhere on the same line (a battery-count delta, a K-of-5 vector) no longer exempts a current-fact statement — a complete `<!-- ... -->` comment is stripped before the arrow test runs so its own terminator can never supply an arrow, while a genuine delta written with the same three bytes keeps its arrow; complete comments are also stripped from whole file text before hits are collected, line count preserved so findings stay citable, so a headline commented out across several lines is not reported as a current-fact statement at all (control `(i3)`) (all `(i2)`, six named arms, each verified by neutralization to fail alone when its own fix is reverted) — lets `docs/v8.0-final-closure.md` and `CHANGELOG.md` state the same figure as a frozen or dated fact: control `(h)` asserts layer attribution on synthetic lines carrying the current literal at each surface's real relpath, so the verdict is independent of whether the live file still contains that literal, and the `(h2)` invariance control asserts that same verdict is unchanged under a perturbed figure, over four cases each pinned to the layer it must land on — the two whole-file cases are invariant by MEMBERSHIP (the classifier short-circuits before the perturbed literals reach the arrow layer, so they cannot fail while the membership lock holds) and the property itself is carried by the two ARROW arms, one at a live relpath and one at a synthetic non-exempt path — together guaranteeing a headline move never forces an edit to either frozen document. A tree-wide scan over `HEADLINE_SCAN_GLOBS` (live value: `docs/*.md`, `CLAUDE.md`, `CHANGELOG.md`, `README.md`, non-recursive — it does not reach `CONTRIBUTING.md`, `scripts/`, `shared/`, `first-principles/`, `.github/`, any future `docs/<subdir>/`, `tests/`, or the git-ignored `docs/history/`) fails, naming the file and line, on any tracked surface matched by those globs that states the headline as current fact while absent from the registered set; every candidate the scan's own read loop declines to open is a named INFO line, never a silent skip. Each surface carries its own named non-vacuity control (`(g)`), and the scan carries two floors evaluated before its PASS branch, both derived from `read_relpaths` — the set the read loop itself actually opened, never a separate glob-based sweep, which the floor helper's signature is what enforces: it takes the `_HeadlineScanRead` record itself, so a glob-derived `set[str]` cannot be handed to it at any call site (`(m)`'s three arms lock the helper's own semantics; they do not observe block (j)'s wiring, which is why that wiring is made unexpressible rather than merely asserted): a coverage floor requiring every path in the union of `COVERED_HEADLINE_SURFACES` and `HISTORICAL_EXEMPT_FILES` to have been READ, and a per-surface accounted-hit floor requiring each `COVERED_HEADLINE_SURFACES` member individually to account for at least one non-historical hit, so one surface's extra hits can no longer mask another surface's zero (`(j-floor)`/`(l)`/`(m)`) — plus block `(l)`, which drives the real glob-expansion and file-collection path with alternative glob lists rather than a hand-built simulation: narrowing or emptying `HEADLINE_SCAN_GLOBS` now fails the gate naming the surfaces it can no longer reach. Block `(n)` asserts this row's own transcription of `HEADLINE_SCAN_GLOBS` against the constant in both this file and `docs/ARCHITECTURE.md` — covering the glob list's transcription only; the rest of either row's prose remains unasserted. CI still does not run the `emit` subcommand — that stays a manual regeneration step. **Does not assert** that the coverage figure is *correct* (`build_matrix_rows()` is the oracle; this sentinel only ties the published surfaces to it); does not scan `tests/` or the git-ignored `docs/history/`; detection is line-scoped, so a headline hard-wrapped across two physical lines is not detected; and a line of the form `<digits> --> <current literal>` is treated as a delta even when it is a mermaid edge whose target label happens to begin with the headline text (measured unreachable in this tree today, not structurally excluded). `docs/data/matrix.json` is tracked as of TEARDOWN-03, docs/v8.7-constraint-teardown.md. Deterministic, no live session. |
| COLLIDE-01 | `check-install-collisions.py --self-test` | Offline dual-install name-collision self-test — detects skill/agent name collisions between plugin (`first-principles/`) and monolith (`first-principles-thinking/`) install surfaces (D-02: relaxes VAL-04's monolith exclusion for the NAME axis only; VAL-04 owns the trigger 4-gram axis, this gate owns the name-collision axis — orthogonal concerns; absent monolith dir is vacuously clean; deterministic, no live session) |
| QUAL-01 | `check-quality-harness.py --self-test` | Offline blind A/B quality-measurement harness self-test (deterministic, no live session) — extraction guardrails A/B, scoreline parser, blinding integrity, tabulation arithmetic, baseline-fixture integrity, the mechanical defect detector (including chain-heading parsing, chain-dependency acyclicity/grounding, and Self-Audit-Gate reconciliation against the measured record), and defect-incidence schema compatibility; the promoted instrument behind the pre/post-fix quality baseline (HARNESS-01, `docs/v8.7-quality-baseline-freeze.md`) |
| HARN-01 | `scripts/check-act-limb.py` | Registered — CI job `check-act-limb (HARN-01)` plus battery registration. Offline Act-limb gate: the Phase 3 verification step and the Criterion 3 Fix note are present, correctly placed, and internally coherent in the emitted tree. Self-test carries isolation control fixtures for all 16 neutralizable branches (58 controls); an anti-masking assertion fails the gate unless every branch is covered. |
| HARN-02 | `scripts/check-loop-closure.py` | Registered — CI job `check-loop-closure (HARN-02)` plus battery registration. The Observe→Perceive re-entry edges are present in the agent body and in `shared/agent/input-contract.md`, with per-source negative controls |
| HARN-03 | `scripts/check-focused-parity.py` | Registered — CI job `check-focused-parity (HARN-03)` plus battery registration. Stub surface, agent surface and cross-surface parity-token set equality, with the D-12 anchor-control ratchet |
| HC-BOUND | `check-high-confidence-bound.py --self-test` | Registered — CI job `check-high-confidence-bound (HC-BOUND)` plus battery registration. Structural validation gate: asserts Phase 5 tightening of Criterion 3 (Evidence) and Criterion 5 (Conclusion) HIGH-confidence bound is present and well-formed in both rubric surfaces (canonical and emitted), and all three documented EXCEPT exceptions are present. Does not measure agent behavior (MEAS-01/MEAS-02, deferred to v8.20+). |
| PROV-GUARD | `scripts/check-provenance.py` | Registered — CI job `check-provenance (PROV-GUARD)` plus battery registration, both running `--self-test` **and** the live leg, matching VERSION-01, GATE-01, COLLIDE-01 and REG-GUARD. Asserts every `*Provenance: read-at-source*` ground truth in an analysis's section 3 joins to a real `WebFetch`/`Read` of that source in the run's stored `.jsonl` capture, and every literal it states appears verbatim in that source's retrieved text; the live leg reads the committed fixture at `tests/quality-provenance-v8.24/` and reports `7/7 sources matched, 35/35 literals located`. Every other column `detect_defects` emits scores the *form* of an analysis; this is the first check in the stack that can falsify a `read-at-source` label against what the run actually fetched — it records fact, not form. **What it does not assert:** that a stated number means what the analysis says it means, nor that the citing chain is valid inference (backlog 999.4); the literal regex also matches digit tails of identifiers such as `x86` → `86` (expected, not a bug); whole-span bold/quoted matching was measured and rejected (4/11 bold spans, 4/8 quoted spans located); PROV-04's no-network control blocks `socket` but not a `subprocess` shell-out. The self-test's 24 controls are tempdir/in-memory and therefore assert nothing about the committed fixture, which is why the live leg runs on both surfaces. |

HARN-01, HARN-02 and HARN-03 were registered under HARN-04 at v8.18.0 — each is a CI job plus a
single `--self-test`-only battery `gate` call, and each is counted in the battery total below. HC-BOUND
was registered at v8.19.0 under Phase 6 (HC-04). REG-GUARD was registered at v8.21.0 under Phase 3 (REG-03).
PROV-GUARD was registered at v8.24.0 under Phase 6 (GATE-02/GATE-03) — a CI job plus a battery `gate`
call running both `--self-test` and the live leg — and is counted in the battery total below.

`bash scripts/check-firewall-battery.sh` runs the full offline gate set — currently **23/23** — in one shot and prints a FIREWALL: GREEN / RED / BLOCKED verdict (SHIP-06: BLOCKED, exit 2, is a third outcome for an unmet external prerequisite — currently only VAL-03's pytest interpreter — and is distinct from a genuine gate failure, RED, exit 1). QUAL-01 (added at v8.7 Phase 164, HARNESS-01) moved the battery from 15 to 16; VERSION-01 (added by the 2026-08-16 audit, [`docs/audit-2026-08-16-duplication-staleness.md`](docs/audit-2026-08-16-duplication-staleness.md)) moved it from 16 to 17; HARN-01/02/03 (added under HARN-04, Phase 4, v8.18.0) moved it from 17 to 20; HC-BOUND (added under HC-04, Phase 6, v8.19.0) moved it from 20 to 21; REG-GUARD (added under REG-03, Phase 3, v8.21.0) moved it from 21 to 22; PROV-GUARD (added under Phase 6, v8.24.0) moved it from 22 to 23. The tally is 21 `gate`/`gate_prereq` registrations plus two inline checks (INVARIANT-CHECK, FROZEN-EVIDENCE); the body-size `[INFO]` line is deliberately untallied. See [`docs/v8.7-quality-baseline-freeze.md`](docs/v8.7-quality-baseline-freeze.md) and [`docs/v8.7-constraint-teardown.md`](docs/v8.7-constraint-teardown.md) for the milestone's full gate-composition and retired-constraint record.

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
  (**161 reproducible / 91 audit-only / 0 gap / 252 total**), compact historical ledger, and gap
  findings. (Derived from regenerated matrix Phase 138 Plan 03; META-Q4 re-tiered
  reproducible→audit-only in the v8.8 post-close TEARDOWN-01 cleanup, 133/96 → 132/97; 15
  v4.0/v4.1 builder requirements retired at quick task `260728-vxn`, 132/97 → 126/88,
  229 → 214 rows; the 23 v8.18 milestone requirements registered as matrix rows at Phase 4 / D-05,
  126/88 → 147/90, 214 → 237 rows; the 15 v8.24 milestone requirements registered as matrix rows
  at Phase 6 / D-06, 147/90 → 161/91, 237 → 252 rows.)
- **`docs/v8.0-final-closure.md`** — **historical record, not current state.** Accepted
  limitations (RR-114-01 1/5, RR-108-04 0/5, RR-108-05 0/5) and deferred-ledger disposition as of
  v8.0 (Phase 142). It calls 133/96/0/229 the "final" coverage headline because v8.0 was meant to
  wrap the project; work continued and that figure has been superseded four times — see the
  bullet above. Do not quote its headline as current.
- **`docs/requirements-matrix.md`** — generated 252-row capability→requirement→test
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
