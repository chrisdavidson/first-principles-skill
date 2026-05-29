# Changelog

All notable changes to this project are documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
