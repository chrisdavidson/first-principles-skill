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

**This table is the canonical gate inventory.** Every other document links here rather than
restating it — `CONTRIBUTING.md`, `CONFIGURATION.md`, `DATA-FLOW.md`, `TESTING.md`, and the
measurement docs all point at this anchor. `CLAUDE.md` keeps its own operational copy by
design, because a working session must be able to see the gate list without opening `docs/`.

Gates run on three surfaces, and the distinction matters: **20 in CI**
(`.github/workflows/validation.yml`, on push/PR to master), **23 tallied in the offline battery**
(`bash scripts/check-firewall-battery.sh`), and **1 pre-commit** hook. The battery is a
strict superset of CI: all 20 CI gates — VAL-01 included, so it runs on both surfaces and
needs the `claude` CLI in both — plus QUAL-01, which is battery-only by design and is the
one registered gate with no CI job, plus the two inline checks INVARIANT-CHECK and
FROZEN-EVIDENCE. That is 20 + 1 + 2 = 23.

| Gate | Job / Mechanism | Script | What it checks |
|------|----------------|--------|----------------|
| VAL-01 | `plugin-validate` (CI) | `claude plugin validate` | Plugin schema validity |
| VAL-02 | `markdownlint` (CI) | `markdownlint-cli2` | MD style across `first-principles/**/*.md` |
| VAL-03 | `check-links` (CI) | `scripts/check-links.py` | Relative MD links resolve in plugin, shared, and docs trees; `docs/` anchors validated with github-slugger rule |
| VAL-04 / GATE-02 | `check-trigger-collisions` (CI) | `scripts/check-trigger-collisions.py` | No 4-gram collision across skill descriptions |
| VAL-05 | `check-description-budget` (CI) | `scripts/check-description-budget.py` | All skill listings under 2000-char cap |
| VERSION-01 | `check-version-stamps` (CI) | `scripts/check-version-stamps.py` | All 17 hand-maintained version stamps carry the same value (self-test **and** live scan) |
| REG-GUARD | `check-registration` (CI) | `scripts/check-registration.py` | Offline registration completeness gate over two surfaces. (a) Plugin axis: every skill directory and the main agent carry a frontmatter `name:` matching their own basename; manifest-declared additional paths resolve inside the plugin. (b) CI-job axis (WR-02, v8.24): every gate `scripts/check-firewall-battery.sh` registers has a matching `name: <job> (<GATE-ID>)` job in `.github/workflows/validation.yml` (QUAL-01 is the single named battery-only exemption); this is the assertion the v8.24 `GATE-02` matrix row's `artifact_link` binds to by symbol anchor. Self-test **and** live scan on both surfaces, matching VERSION-01, GATE-01 and COLLIDE-01: the self-test fixtures are isolated from the shipped tree, so only the live leg asserts either invariant on the shipped surfaces. |
| COLLIDE-01 | `check-install-collisions` (CI) | `scripts/check-install-collisions.py` | Dual-install name-collision self-test + live-tree scan (no skill/agent name collisions between plugin and monolith install surfaces) |
| DUAL-04 | `sync-check` (CI) | `scripts/sync-content.py --check` | `shared/` and generated tree are in sync |
| GATE-02-v8.5 | `pointer-drift-guard` (CI) | `scripts/sync-content.py --self-test` | Offline pointer drift-guard: each split core reference file's Procedure slice carries exactly one well-formed link to its own `-detail.md` sibling |
| GATE-01 | `check-agent` (CI) | `scripts/check-agent.py` | Agent structural checks |
| BATT-06 | `check-routing-battery` (CI) | `scripts/check-routing-battery.py --self-test` | Merged dual-signal battery self-test (boundary + focused-output); anti-masking sentinels |
| STEP0-08 | `check-step0-emulator` (CI) | `scripts/check-step0-emulator.py --self-test` | Offline Step 0 phrase-detection classifier self-test |
| STEP0-06 | `check-step0-live` (CI) | `scripts/check-step0-live.py --self-test` | Step 0 live-harness scoring/parsing logic self-test |
| TRACE-03 | `check-traceability` (CI) | `scripts/check-traceability.py --self-test` | Traceability gate self-test (capability/tier schema + artifact resolution), plus the `HEADLINE-LOCK` sentinel: asserts the published headline (both prose and compact-slash renderings) against five current-fact surfaces — `docs/requirements-traceability.md`, `CLAUDE.md`, `docs/README.md`, `docs/MEASUREMENT-MAP.md`, `docs/COMPONENT-DIAGRAM.md` (slash form only) — plus both tracked matrix artifacts, all derived live from `build_matrix_rows()` with no hardcoded figure. A two-layer historical/delta exemption — whole-file, then a figure-adjacent arrow anchored to the headline literal itself (one of three recognised renderings — `→`, `->`, or the HTML comment closer `-->` — must sit adjacent to the literal, delimiting it from a digit run; a mermaid edge, a bare HTML comment terminator, or an unrelated numeric arrow elsewhere on the line no longer exempts it, control `(i2)`) — lets `docs/v8.0-final-closure.md` and `CHANGELOG.md` state the same figure: control `(h)` attributes this on synthetic lines built at each surface's real relpath, independent of whether the live file still contains today's literal, and `(h2)` asserts that verdict is invariant under a perturbed figure, so a headline move never forces an edit to either frozen document. A tree-wide scan over `HEADLINE_SCAN_GLOBS` (`docs/*.md`, `CLAUDE.md`, `CHANGELOG.md`, `README.md`, non-recursive — unreachable: `CONTRIBUTING.md`, `scripts/`, `shared/`, `first-principles/`, `.github/`, any future `docs/<subdir>/`, `tests/`, and the git-ignored `docs/history/`) fails, naming the file and line, on any surface those globs reach that states the headline as current fact while unregistered; every declined candidate is a named INFO line, never a silent skip. Every surface carries its own named non-vacuity control; the scan carries two floors derived from `read_relpaths` (what the read loop itself actually opened, not a separate glob sweep — the floor helper takes the `_HeadlineScanRead` record itself, so a glob-derived `set[str]` cannot be passed at any call site; `(m)` locks the helper's own semantics, not block (j)'s wiring) — a coverage floor over the union of `COVERED_HEADLINE_SURFACES` and `HISTORICAL_EXEMPT_FILES`, and a per-surface accounted-hit floor over `COVERED_HEADLINE_SURFACES` alone — plus block `(l)`, which drives the real glob-expansion/collection path with alternative glob lists. Block `(n)` locks this row's own `HEADLINE_SCAN_GLOBS` transcription against the constant (glob list only; the rest of this row's prose is unasserted). Does not assert the figure is *correct*; does not scan `tests/` or the git-ignored `docs/history/`; detection is line-scoped, so a headline hard-wrapped across two physical lines escapes the scan; nor does it catch a mermaid edge whose target label happens to begin with the headline text (unreachable in this tree today, not structurally excluded). |
| QUAL-01 | battery only — **not a CI job** | `scripts/check-quality-harness.py --self-test` | Offline blind A/B quality-measurement harness self-test — extraction guardrails, scoreline parsing, blinding, tabulation, baseline-fixture integrity, and the mechanical defect detector (chain form and heading parsing, chain-dependency acyclicity/grounding, Self-Audit-Gate reconciliation against the measured record, defect-incidence schema compatibility) |
| HARN-01 | `check-act-limb` (CI) | `scripts/check-act-limb.py` | Offline Act-limb gate: the Phase 3 verification step and the Criterion 3 Fix note are present, correctly placed, and internally coherent in the emitted tree. Self-test carries isolation control fixtures for all 16 neutralizable branches (58 controls); an anti-masking assertion fails the gate unless every branch is covered. |
| HARN-02 | `check-loop-closure` (CI) | `scripts/check-loop-closure.py` | Offline Observe→Perceive re-entry-edge gate: a Criterion 1 Absent verdict routes back to Phase 1, every re-entry edge is bounded to one re-perception pass, and a fired edge is recorded |
| HARN-03 | `check-focused-parity` (CI) | `scripts/check-focused-parity.py` | Offline focused-mode parity gate: stub surface, agent surface and cross-surface parity-token set equality, with the D-12 anchor-control ratchet |
| HC-BOUND | `check-high-confidence-bound` (CI) | `scripts/check-high-confidence-bound.py --self-test` | Offline structural validation gate: asserts Phase 5 tightening of Criterion 3 (Evidence) and Criterion 5 (Conclusion) HIGH-confidence bound is present and well-formed in both rubric surfaces (canonical and emitted), and all three documented EXCEPT exceptions are present. Structural only; does not measure agent behavior (MEAS-01/MEAS-02, deferred to v8.20+). |
| PROV-GUARD | `check-provenance` (CI) | `scripts/check-provenance.py` | Offline gate: every `*Provenance: read-at-source*` GT in an analysis's section 3 joins to a real `WebFetch`/`Read` of that source in the run's stored `.jsonl` capture, and every literal it states appears verbatim in that source's retrieved text; live leg reads `tests/quality-provenance-v8.24/` and reports `7/7 sources matched, 35/35 literals located`. Records fact, not form — every other column `detect_defects` emits scores the analysis's form. Does not assert that a stated number means what the analysis says (backlog 999.4), treats identifier digit-tails like `x86` → `86` as expected (not a bug), does not use whole-span bold/quoted matching (measured and rejected, 4/11 and 4/8), and its no-network control blocks `socket` but not a `subprocess` shell-out. Self-test **and** live leg on both surfaces, matching VERSION-01, GATE-01, COLLIDE-01 and REG-GUARD. |
| INVARIANT-CHECK | battery only (inline) | — | Anti-masking constants still hold: `pre-mortem=9 fishbone=7 inversion=13 trade-off=10 MIN_HEADER_HITS=2` |
| FROZEN-EVIDENCE | battery only (inline) | `git diff --quiet` | Frozen baselines and captures are unmodified |
| — | sync-drift gate (pre-commit) | `scripts/sync-content.py --check` | `shared/` and generated tree are in sync (same check as DUAL-04, fires before commit) |

HARN-01, HARN-02 and HARN-03 were registered under HARN-04 at v8.18.0 — each has a CI job plus a
single `--self-test`-only battery `gate` call, and each is counted in the battery total above. HC-BOUND
was registered at v8.19.0 under Phase 6 (HC-04) — it also has a CI job plus a single `--self-test`-only
battery `gate` call, and is counted in the battery total above. REG-GUARD was registered at v8.21.0
under Phase 3 (REG-03) — it has a CI job plus a battery `gate` call that runs both `--self-test` **and**
the live scan, matching VERSION-01, GATE-01 and COLLIDE-01, and is counted in the battery total above.
PROV-GUARD was registered at v8.24.0 under Phase 6 (GATE-02/GATE-03) — a CI job plus a battery `gate`
call running both `--self-test` **and** the live leg, matching VERSION-01, GATE-01, COLLIDE-01 and
REG-GUARD — and is counted in the battery total above.

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
