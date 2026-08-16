# Changelog

All notable changes to this project are documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Version stamps move in lockstep.** Plugin installs are version-gated, not content-gated,
so every release bumps all 17 stamps together — the 14 `shared/skills/*/SKILL.md` sources
(13 companion skills plus the `first-principles-analysis` launcher),
`shared/spine/SKILL.meta.yml`, `.claude-plugin/marketplace.json`, and
`first-principles/.claude-plugin/plugin.json`. A body edit without a bump never reaches an
installed session.

## [Unreleased]

### Known defect — the `?`-count exit criterion is satisfied in form and fails in substance

v8.16.0's Phase 3 exit criterion requires the count of `?`-marked ground truths to be stated
explicitly. **Across every draft observed in post-release testing, a count was stated and none
was correct.** Three runs against the same prompt — two turn budgets, both agent versions:

| Draft | Stated | Actual |
|---|---|---|
| full-composer, `maxTurns: 60`, base | 24 of 41 | **31 of 41** |
| same run, consolidated after revision | 17 of 45 *(while enumerating 20 IDs)* | **21 of 57** |
| full-composer, `maxTurns: 30` | 17 of 22 *("the unsuffixed five")* | **15 of 22** *(seven unsuffixed)* |

The consolidated draft is the sharpest case: it reports the same quantity **three different ways
inside one document** — a header figure, an enumeration of a different length, and an actual
suffix count that matches neither.

**Self-Audit Gate Criterion 3 passes all three.** It quotes the stated count as its satisfying
span rather than recomputing it, so the gate verifies *that a count was stated*, not *that it is
correct*. In the `maxTurns: 30` draft the Gate quotes `"Count of ?-marked ground truths: 17 of
22"` verbatim and bands the criterion **Sound**.

**Why this one is worth fixing before the others.** Every other Gate criterion is a judgement
call — whether an essence statement is specific enough, whether a chain has a genuine
intermediate. This one is arithmetic over a document the agent has already written, and it is
the criterion the provenance discipline leans on hardest: the count is the summary statistic a
reader uses to calibrate the whole analysis. A wrong count understates unverified inputs by up
to seven ground truths, in the direction that flatters the analysis.

**Proposed fix, not yet implemented:** derive the count rather than assert it — require the
`?`-marked IDs to be *enumerated*, and make the Gate check the enumeration against the Phase 3
list rather than against the stated number. An enumeration is checkable by inspection; a bare
integer is not.

*Not a regression: the criterion is new in 8.16.0 and has never reported a correct figure.
Recorded here so it is not rediscovered as a fresh finding.*

## [8.16.0] - 2026-08-16

Source-provenance discipline for ground truths. Both changes come from the same observed
failure: a fabricated figure carried a well-formed citation to a real paper that did not
contain it, propagated into a HIGH-confidence derivation chain, and reached the conclusion.
A citation being *present* passed every check the agent had.

### Added

- **Source-provenance labels on every ground truth** (Phase 3, `shared/spine/SKILL-body.md`).
  One test decides the label: *did this analysis read the asserted figure or wording in the
  cited source?* Three values — `read-at-source` (no suffix), `reported-by-delegate` (`?`
  required), `unverified` (`?` required). Provenance is scored on what the analysis did, never
  on who supplied the claim: a well-formed citation from a capable sub-agent is
  `reported-by-delegate` until someone opens the source.
- **Delegate-reported ground-truth form** in `shared/spine/references/output-template.md` §3,
  alongside the existing verified and unverified forms, plus a required provenance summary.
- **Provenance check** prepended to Criterion 3 of the Self-Audit Gate, applied before banding.

### Changed

- **The `?` suffix is now the default rather than the exception.** It is dropped only when a
  read-at-source location can be named. A delegate report counts as read-at-source only when it
  quotes the source's own wording and that quote was checked.
- **Phase 3 exit criterion** now requires the count of `?`-marked ground truths to be stated
  *and* every unsuffixed ground truth feeding a HIGH-confidence chain to name where its figure
  was read. A bare count of zero no longer satisfies the criterion — the named read-locations
  are the auditable part.
- **Self-Audit Gate Criterion 3 band ladder retightened.** An unsuffixed, unread ground truth
  feeding a HIGH-confidence chain now bands at **Hand-wavy**; it previously banded at **Sound**,
  which is precisely the defect above passing at a tolerated level. The MEDIUM/LOW-confidence
  case stays at Sound, so the ladder still discriminates.

### Note

The binary `GT-N` / `GT-N?` notation is deliberately unchanged. Provenance layers on top of it
rather than introducing a third symbol, so D-07, the exact-tie tiebreak, the MEDIUM/LOW
confidence rule, and all four Criterion 3 bands keep working without re-verification.

## [8.15.0] - 2026-08-16

Findings from the first real-world audit of the shipped agent — a full-composer run against a
Medium article, reconstructed from the raw subagent transcript rather than from the written
output.

### Added

- **"Turn discipline" section** in the agent body, placed before Step 0. Prescriptive rather
  than prohibitive on purpose: the observed run reached for `Monitor` first and fell back to
  `sleep` loops anyway, so the text names the alternative — dispatched work notifies on
  completion, so stop and wait for the notification rather than polling.
- **Carry-forward rule for regenerated analyses.** The observed run emitted three complete
  full-length analyses and each rewrite silently lost artifacts: the Essence Statement was
  present in drafts 1 and 2 and absent from the deliverable, and `GT-N?` marks decayed 13 → 2 →
  0 while a fabricated figure's usage rose 0 → 6 → 8. A rewrite is now a revision — confirm
  every named artifact survives or is explicitly retired.
- **Honest-failure clause.** If the closure ledger or the gate could not run, say so at the top
  of the response, naming which. A stated omission is recoverable; a silent one is not.

### Changed

- **`maxTurns` raised 30 → 60.** The observed run used 32 assistant turns against a cap of 30,
  with roughly 9 spent on tool-schema fetches and seven consecutive busy-wait loops polling for
  dispatched sub-agents. The Fix/Repeat loop runs last and is therefore what gets dropped when
  the budget runs out — and it was.
- **The Validation Rubric is renamed the Self-Audit Gate.** The request asked for "a validation
  rubric scoring the article's argument"; the agent produced one and let it stand in for its own
  gate, which never ran. Two different instruments shared a name. The disambiguation lives in
  `SKILL-body.md`, not only in the reference file, because the whole failure was that the linked
  file never got opened: the gate scores *this analysis's* structure, a subject-matter rubric is
  a separate deliverable, and both must appear.
- `docs/CONFIGURATION.md` and `docs/FIVE-PHASE-FLOW.md` updated in the same commit so no tracked
  prose asserts the old value or the old name. `docs/CONFIGURATION.md` also carried a
  pre-existing stale `metadata.version` of `"8.0.0"`.

### Note

The file path `references/validation-rubric.md` is deliberately unchanged despite the rename —
`check-quality-harness.py` copies it *by name* into the QUAL-01 frozen packet and asserts on the
entry list, `check-traceability.py` pins it as a `deliverable_path`, and `sync-content.py` keys
its INLINE list on the slug. The frozen quality baseline records the rubric by path only, so
retitling does not affect pre/post comparability.

## Earlier releases (1.0 – 8.14)

This changelog was not maintained between 3.8.0 and 8.15.0. The entries below are
**reconstructed from the annotated git tags** and carry only each release's headline — no
Added/Changed/Fixed decomposition, because that detail was never recorded here and inventing it
would misrepresent the record. **For any release below, the annotated tag body is the
authoritative account** (`git show <tag>`). Releases **3.0.0 through 3.8.0 are omitted from this
table** — they already carry full hand-written entries further down.

Note also that the repository history was rewritten on 2026-07-28 (removal of `docs/history/`
and 237 raw test captures), so commit SHAs referenced in material predating that date are stale;
tag names remain valid.

| Tag | Date | Headline |
|---|---|---|
| `v8.14-greenmean` | 2026-07-29 | v8.14 GREENMEAN-01 — the milestone that stopped itself |
| `v8.14` | 2026-07-29 | Builder Retirement & Traceability Reconciliation |
| `v8.13` | 2026-07-28 | DETECTFIX-01 — Correct the Inverted D-18 Defect Checks |
| `v8.12` | 2026-07-26 | REALREAD-01 — First Read of Real Work Output |
| `v8.11` | 2026-07-24 | DEFROBUST-01 — D-03 Definition-Robustness Test |
| `v8.10` | 2026-07-24 | CORRECTGATE-01 — A Correctness Instrument for the DIVERGE Class |
| `v8.9` | 2026-07-24 | DIAGNOSE-01 — Diagnose the Failed §6→§4 Contract Fix |
| `v8.8` | 2026-07-23 | Technical-Debt Clean-Up & Framing Correction |
| `v8.7` | 2026-07-23 | Analysis Correctness, Constraint Teardown & Output-Contract Integrity |
| `v8.6` | 2026-07-21 | Agent-Body Procedure Compression |
| `v8.5` | 2026-07-20 | Context Optimization: Execute the Reference-File Split |
| `v8.4` | 2026-07-19 | Implementation-Readiness Evaluation |
| `v8.3` | 2026-07-18 | Technique & Context-Length Optimization Evaluation |
| `v8.2` | 2026-07-18 | Deep Investigation of the 19 Not-Approved Grok Items |
| `v8.1` | 2026-07-16 | Grok Recommendations Review & Selective Implementation |
| `v8.0` | 2026-07-06 | Final Release (project wrapped) |
| `v7.13` | 2026-07-02 | Live Re-Measure — RR-130-01 Fix + Step 0 Residuals |
| `v7.12` | 2026-06-30 | Diagnose & Fix RR-130-01 (Main-Routing Inline-Answering Regression) |
| `v7.11` | 2026-06-30 | Live Re-Measure of the Whole System |
| `v7.10` | 2026-06-28 | Evaluate Gaps & Technical Debt Misaligning Agent Goals |
| `v7.9` | 2026-06-27 | Close the 5-Fix Over-Routing Fishbone (Fix #3 / Fix #4 / Fix #5) |
| `v7.8` | 2026-06-25 | Step 0 Over-Routing Precision — Negative-Match Guard & Stay-in-Composer Default |
| `v7.7` | 2026-06-24 | Fix the S-P01/S-P03 Step 0 Under-Routing Regressions |
| `v7.6` | 2026-06-23 | Validate the Merge — Live 8-Technique Step 0 Re-Baseline |
| `v7.5` | 2026-06-21 | Execute the decompose→five-whys Merge |
| `v7.4` | 2026-06-20 | Measure the Expansion — Live 9-Technique Step 0 Re-Baseline |
| `v7.3` | 2026-06-20 | Introduce Tier-1 Rigor — the theoretical-limit Skill |
| `v7.2` | 2026-06-19 | Introduce Tier-1 Rigor — the estimate Skill |
| `v7.1` | 2026-06-19 | Introduce Tier-1 Rigor — the decompose Skill |
| `v7.0` | 2026-06-18 | Documentation Refresh & System-Connection Docs |
| `v6.4` | 2026-06-17 | Resolve v6.3 Carry-Forward Residuals (RR-92-01 / RR-92-02) |
| `v6.3` | 2026-06-16 | GEN-01 Step 0 Classifier Rearchitecture |
| `v6.2` | 2026-06-15 | Close the Last Two Documented Gaps |
| `v6.1` | 2026-06-15 | Close Actionable Traceability Gaps |
| `v6.0` | 2026-06-14 | Requirements & Traceability Alignment |
| `v5.3` | 2026-06-14 | Live S-P Routing — Close Remaining Detector Residuals |
| `v5.2` | 2026-06-13 | Live S-P Routing Fix |
| `v5.1` | 2026-06-12 | Step 0 Live Detector Closure |
| `v5.0` | 2026-06-12 | Step 0 Measurement Harness |
| `v4.3` | 2026-06-11 | Unified Routing/Output Battery |
| `v4.2` | 2026-06-10 | Sub-Skill Battery Fixture Correction |
| `v4.1` | 2026-06-06 | Builder Auto-Install Flag |
| `v4.0` | 2026-06-04 | Programmatic Skill/Agent Builder |
| `v3.13` | 2026-06-03 | Routing Catalog v3.2 Content Coverage |
| `v3.12` | 2026-05-30 | Phase-Level Slash Commands |
| `v3.11` | 2026-05-29 | P8 Routing Forward Monitoring |
| `v3.10` | 2026-05-29 | Phase 46 Convention Closure |
| `v3.9` | 2026-05-29 | P8 Routing Fix + Phase 45 Convention Restoration |
| `v2.0` | 2026-05-22 | Collection-of-Skills Plugin |
| `v2.0.0` | 2026-05-21 | Collection-of-Skills Plugin (dual-publish) |
| `v1.2` | 2026-05-20 | Forward Consequence-Tracing Tools (Inversion + Second-Order Thinking) |
| `v1.1` | 2026-05-19 | Ishikawa (Fishbone) Diagram Tool |
| `v1.0` | 2026-05-18 | Enhanced Skill |

---

The 3.0.0 – 3.8.0 entries below are the original hand-written records, kept verbatim.

## [3.8.0] - 2026-05-28

### Added

- `scripts/check-focused-output.py` — verifies that agent analysis outputs stay focused on first-principles methodology (not off-topic delegation); includes `--self-test` fixture battery and a LOAD-BEARING Probe 3 sanity feed.
- `scripts/check-sub-skill-routing.py` — verifies that companion-tool invocations (`/first-principles:fishbone` etc.) are correctly routed to the named sub-skill rather than delegated to the main agent.
- Sub-skill routing catalog at `tests/sub-skill-routing-catalog.md` (P12, P24, N1, N2 prompts).
- Sub-skill routing baseline at `tests/sub-skill-routing-baseline-v3.8.md`.
- Focused-output baseline at `tests/focused-output-baseline-v3.8.md`.
- Six namespaced companion-tool skills under `first-principles/skills/{five-whys,fishbone,inversion,pre-mortem,trade-off,second-order}/` — standalone slash-only skills (`/first-principles:<name>`) for direct invocation of individual techniques without triggering the full agent. Each has `disable-model-invocation: true`.
- `generate_skill_stub` in `scripts/sync-content.py` with six corresponding `shared/skills/` sources; skill stubs are now generated alongside the agent surface.
- `GENERATED` marker prepended to every byte-identical emission in the generated agent tree so code reviewers can skip the `shared/`↔`first-principles/` mirror.
- `.reviewignore` at repo root declaring the generated mirror as review-skippable.

### Fixed

- Signal A routing-envelope override now takes priority over composer-structure cardinality classifier, fixing false sub-skill delegation on routing prompts that carry both signals.
- `_extract_assistant_text` tightened to top-level assistant entries only, preventing nested tool-result text from inflating detection scores.
- Sibling-shared boilerplate in six technique-skill descriptions reworded to eliminate ~60 false-positive 4-gram collisions that blocked `check-trigger-collisions.py` on CI push.
- `sync-content.py` docstrings on three verbatim-copy generators corrected — they previously claimed "NO marker expansion, NO edits" after the GENERATED marker prepend was added.
- Agent marker's primary canonical source now named as a navigable path (`shared/spine/SKILL-body.md`) instead of freeform prose.

## [3.7.0] - 2026-05-27

### Added

- Mandatory Assumption Audit protocol in the validation rubric (`shared/spine/references/validation-rubric.md`): exhaustive enumeration of assumptions by scanning each derivation-chain step, replacing the prior opportunistic-listing approach.
- `[Assumes: X]` annotations on derivation-chain steps in `science-engineering-2.md` worked example.
- Assumption Audit section in `software-systems.md` worked example.
- Routing baseline v3.7 at `tests/routing-baseline-v3.7.md` — BATTERY PASS: P 10/10, N 17/17.

### Changed

- Validation rubric Criteria 1, 2, and 4 Rigorous descriptors rewritten with structural/observable tests instead of subjective phrases ("withstand inspection by a skeptic").
- Validation rubric Criteria 5 and 6 Rigorous descriptors: modal verbs removed; compliance is now detectable from output structure alone.

## [3.6.0] - 2026-05-26

### Added

- Two new routing catalog prompts: P9 (chemistry/first-principles of reaction kinetics) and P10 (earth science/continental drift).
- Two new N-case catalog rows: N16 and N17 (science-lookup questions that should NOT delegate).
- Routing mini-catalog v3.6 fixture at `tests/routing-mini-catalog-v3.6.md` (P9, P10, N16, N17).
- Routing baseline v3.6 at `tests/routing-baseline-v3.6.md` — BATTERY PASS: P 8/10, N 17/17.

### Changed

- Battery thresholds rescaled to P ≥ 8/10 and N ≥ 15/17 to match the expanded 10P/17N catalog.

## [3.5.0] - 2026-05-25

### Added

- P3+P7 mini-battery catalog fixture at `tests/routing-mini-catalog-p3p7.md` for fast-iteration confirmation before running the full battery.
- P7-targeted paraphrases added to agent description: question-form (`"Is our reasoning sound..."`), back-reference (`"evaluate whether a claim..."`), and evaluate-whether variants.
- Routing baseline v3.5 at `tests/routing-baseline-v3.5.md` — BATTERY PASS: P 6/8, N 15/15.

### Fixed

- P3 routing fragility: prompt mid-sentence rewritten to eliminate structural embedding that suppressed delegation.
- P7 routing fragility: vocabulary gap closed — agent description now covers the "evaluate whether" and question-form trigger shapes that P7 exercises.

## [3.4.0] - 2026-05-25

### Added

- `--repeat` and `--min-pass` flags on `check-routing.py` enabling K-of-N aggregation: run each prompt N times, require K passes — reduces false FAIL/PASS verdicts from single-run non-determinism.
- K>N guard and K-of-N self-test fixtures in the battery runner.
- Rerun-to-stability methodology documented in `docs/testing-agents-headlessly.md` (Section 10).
- Routing baseline v3.4 at `tests/routing-baseline-v3.4.md` — canonical best-of-3: P 6/8, N 15/15.

## [3.3.0] - 2026-05-25

### Added

- `scripts/check-body-budget.py` — checks generated agent body against the ~500-line target; includes `--self-test`.
- `scripts/git-hooks/pre-commit` — combined body-budget + sync-drift gate; blocks commits that would push the agent body over budget or leave `shared/` and the generated agent tree out of sync.
- `scripts/install-hooks.sh` — idempotent installer that symlinks the above hook into `.git/hooks/pre-commit` (preserves any existing hook as `.bak` on first run).
- `scripts/smoke-test-hook.sh` — end-to-end smoke test for the pre-commit hook.
- `.githooks/pre-commit` extended with body-budget gate (for contributors using the `core.hooksPath` opt-in path).
- Contributor setup documentation in README.md for both hook opt-in paths.

## [3.2.0] - 2026-05-24

### Added

- `shared/spine/references/assumption-taxonomy.md` — canonical classification guide for the five assumption types used in Phase 2 (physical law, engineering constraint, current constraint, convention, untested belief); emitted to `first-principles/agents/references/assumption-taxonomy.md`.
- Phase 2 cross-reference from assumption-taxonomy to the agent body.
- Self-application worked example (`shared/examples/self-application.md`) — first-principles analysis applied to a live design decision about the agent itself (body length vs. scope).
- Four second-pass worked examples covering distinct reasoning shapes not present in the original six:
  - `software-systems-2.md` — Build vs. Buy (authentication service); capability-cost-risk trade-off shape.
  - `product-business-2.md` — Feature prioritization under a binding engineering-capacity constraint.
  - `personal-general-2.md` — Mortgage paydown vs. index investment; quantitative expected-value chain.
  - `science-engineering-2.md` — In-service mechanical component failure analysis; diagnostic/backward-reasoning shape.
- Worked Examples navigation subsection added to the agent spine.
- All five new examples synced to the generated agent surface.

### Changed

- Spine appendices (assumption taxonomy, output template, validation rubric) extracted out of the inlined agent body into on-demand reference files, reducing recurring token cost per invocation.

## [3.1.0] - 2026-05-23

### Added

- `scripts/check-routing.py` — headless routing battery: issues each catalog prompt through `claude -p --output-format stream-json`, scores DELEGATE / NO-DELEGATE from the event stream, and exits non-zero if P-case or N-case thresholds are not met.
- `tests/routing-catalog.md` — initial routing test catalog: 8 P-cases (should delegate) and 15 N-cases (should NOT delegate), with per-prompt annotations and pass thresholds.
- `docs/testing-agents-headlessly.md` — documents the stream-json methodology, two-signal detection rule, jq extraction strategies, and `--permission-mode bypassPermissions` requirement for reproducible headless agent testing.
- Routing baseline v3.1 recorded in `tests/routing-catalog.md`.

### Fixed

- Agent description scope-line tightened to explicitly exclude performance optimization, debugging, and general Q&A — closes a class of false-positive delegations where the agent was invoked for routine coding tasks.

## [3.0.0] - 2026-05-23

### Removed

- Standalone monolith skill at `first-principles-thinking/`. Users who copied this to `~/.claude/skills/` should remove that local copy manually:
  `rm -rf ~/.claude/skills/first-principles-thinking`
- 7 namespaced plugin skills at `first-principles/skills/{thinking,five-whys,pre-mortem,trade-off,fishbone,inversion,second-order}/`. The Phase 26 forwarding language ("still installable") is superseded — these surfaces no longer exist.

### Added

- First-principles agent surface at `first-principles/agents/first-principles.md` (initially shipped Phase 23 in the v3.0-alpha series; now the sole installable interface).
- 6 on-demand companion-tool reference siblings under `first-principles/agents/references/{five-whys,fishbone,inversion,pre-mortem,trade-off,second-order}.md`.
- 6 worked-example siblings under `first-principles/agents/references/examples/` (migrated from the deleted monolith examples directory).

### Upgrade path

- Install: `claude --plugin-dir ./first-principles` for dev, or via the marketplace (`/plugin marketplace add chrisdavidson/first-principles-skill` then `/plugin install first-principles@first-principles-skill`).
- Invoke: `@agent-first-principles:first-principles` (auto-routing) or `/first-principles:first-principles` (explicit).
- If you previously copied `first-principles-thinking/` into `~/.claude/skills/`, delete that local copy manually — Claude Code does not auto-remove it.

### Reference

- Per-technique deep procedures now ship as agent-loaded reference files (`first-principles/agents/references/`).
- The 5-phase methodology text formerly carried by the monolith body is inlined in the agent body itself.
