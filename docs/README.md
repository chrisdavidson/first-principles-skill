# docs/ — Documentation Index

![First Principles hero banner](assets/hero.svg)

> **Final state — start here:** [`v8.0-final-closure.md`](v8.0-final-closure.md) — terminal
> release record, accepted limitations, final coverage headline (133/96/0/229), and deferred-ledger
> disposition summary.
>
> Later milestones v8.1 (a Grok-review triage that selectively implemented 7 docs/metadata items), v8.2 (a fresh analysis-only re-investigation of the 19 not-approved items), v8.3 (a technique-overlap + context-optimization evaluation, findings-only, byte-freeze untouched), and v8.4 (an implementation-readiness evaluation that returned a GO verdict on the GROK-04 hero banner — specified and costed but deliberately not built, awaiting a future milestone — and a NO-GO on reference-file extraction) left this terminal baseline unchanged.

Milestone v8.5 (Context Optimization — Execute the Reference-File Split) is the first implementation + live milestone since v8.1: it executed the 4-file reference split (five-whys, theoretical-limit, estimate, fishbone into core + on-demand `-detail.md` siblings, dropping 398 lines off the skill surface) and ran the milestone's only live spend — a 72-call re-measure — narrowly relaxing the byte-freeze to re-open and re-measure exactly RR-108-04/RR-108-05, unlike the v8.2–v8.4 analysis-only milestones. The detector constants stayed byte-unchanged and the coverage headline stayed 133/96/0/229.

Milestone v8.6 (Agent-Body Procedure Compression) is the second consecutive live-measure milestone: it compressed the always-loaded, auto-routed agent body's inlined `## Procedure` prose for four techniques — estimate and theoretical-limit (no emission detector, zero measured-floor risk) and five-whys and fishbone (marker-pinned) — cutting the agent body 612 to 590 lines, the surface v8.5's reference-file split structurally could not shrink, since the agent body inlines only `## Procedure`. It then ran a small 2-row live Step-0 re-measure confirming neither compressed detector-covered row regressed (fishbone 3/5 to 4/5, five-whys 0/5 to 2/5 unbanked). The detector constants and the coverage headline stayed unchanged (133/96/0/229).

This folder documents the first-principles plugin system. New here? Start with [GETTING-STARTED.md](GETTING-STARTED.md), then [ONBOARDING.md](ONBOARDING.md), then [DATA-FLOW.md](DATA-FLOW.md).

---

## Core docs

| Document | What it covers |
|----------|----------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture: `shared/` → generation pipeline, plugin layout, five-phase agent methodology, measurement subsystem, CI + pre-commit gate table |
| [CONFIGURATION.md](CONFIGURATION.md) | Skill frontmatter rules, version-string format, reserved words, anti-masking invariants (`MIN_HEADER_HITS=2`, `_COMPOSER_FOCUS_CEILING=4`) |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Contributor workflow: `shared/` source-of-truth model, validation-script inventory, standard editing loop, pre-commit hook setup, key invariants |
| [FIVE-PHASE-FLOW.md](FIVE-PHASE-FLOW.md) | Mermaid flow diagram of the 5-phase methodology: Step 0 mode selection, phase chain with named artifacts, companion-technique handoff edges, and the second-order route-back |
| [GETTING-STARTED.md](GETTING-STARTED.md) | Install the plugin, invoke the agent and thirteen companion skills, slash invocation |
| [METHODOLOGY-CHEATSHEET.md](METHODOLOGY-CHEATSHEET.md) | One-page quick reference: the 5-phase flow, named artifacts, assumption types, derivation-chain format, and all 13 companion/focused skills with slash commands |
| [TESTING.md](TESTING.md) | How to run every CI gate and the two pre-commit gates — VAL/DUAL/GATE/STEP0/BATT/TRACE matrix, each mapped to its script |
| [testing-agents-headlessly.md](testing-agents-headlessly.md) | Headless testing: routing battery, two-layer Step 0 harness, `stream-json` capture |

## System-connection docs

| Document | What it covers |
|----------|----------------|
| [DATA-FLOW.md](DATA-FLOW.md) | End-to-end trace: `shared/` source edit → `sync-content.py` → generated plugin → CI gates → measurement harness |
| [MEASUREMENT-MAP.md](MEASUREMENT-MAP.md) | Layered test stack: routing battery ↔ Step 0 emulator ↔ Step 0 live ↔ traceability matrix ↔ BATT-06 sentinels; which gate owns which residual |
| [COMPONENT-DIAGRAM.md](COMPONENT-DIAGRAM.md) | Mermaid diagrams of the generation pipeline and measurement stack — what reads what, what generates what |
| [ONBOARDING.md](ONBOARDING.md) | Contributor on-ramp: end-to-end "make a change" walkthrough from `shared/` edit to shipped, gated plugin artifact |

## Requirements & traceability

| Document | What it covers |
|----------|----------------|
| [v8.0-final-closure.md](v8.0-final-closure.md) | **Terminal record** — final baselines, accepted limitations, coverage headline, deferred-ledger disposition summary |
| [requirements-traceability.md](requirements-traceability.md) | Authoritative requirements traceability surface: active residuals, coverage headline, compact historical ledger, gap findings |
| [requirements-matrix.md](requirements-matrix.md) | Generated 229-row capability → requirement → test matrix |
| [v8.1-grok-review-assessment.md](v8.1-grok-review-assessment.md) | Rated inventory of external-review (Grok) recommendations: 26 itemized GROK-NN rows with invasiveness score, already-done verification, verdict, effort estimate; SELECT-01 dispositions recorded (7 approved / 19 not approved, Phase 144) |
| [v8.2-grok-reassessment.md](v8.2-grok-reassessment.md) | Fresh re-investigation of the 19 not-approved items; 18 keep-won't-do / 1 promote-candidate (GROK-04 hero banner) — non-binding input to a future milestone decision |

## Optimization studies

| Document | What it covers |
|----------|----------------|
| [v8.3-technique-context-optimization-eval.md](v8.3-technique-context-optimization-eval.md) | Per-technique overlap map (8 techniques), agent-body line accounting, composer-vs-pull-when-needed trade-off, and a prioritized optimization plan — findings-only, no `shared/` change. |
| [v8.4-implementation-readiness-eval.md](v8.4-implementation-readiness-eval.md) | Go/no-go verdicts + costed implementation-readiness plans for the GROK-04 hero banner (GO) and on-demand reference-file extraction (NO-GO) — neither built. |

## v8.5 — Context optimization (reference-file split)

| Document | What it covers |
|----------|----------------|
| [v8.5-byte-freeze-relaxation.md](v8.5-byte-freeze-relaxation.md) | Governing record narrowly re-opening RR-108-04/RR-108-05's re-measure disposition + the 4 split files' content; all other frozen constants keep gating. |
| [v8.5-split-measurement.md](v8.5-split-measurement.md) | Split verification + budget proof (SPLIT-02/03): skill surface −398 lines, agent body +14 (cost-of-mechanism), full offline battery green, body 612/644. |
| [v8.5-live-remeasure-verdict.md](v8.5-live-remeasure-verdict.md) | Live 72-call re-measure honest verdict (MEASURE-03): five per-row floor judgments, fishbone 3/5 CLOSE, S-P02/S-P10/S-P14 CARRY, D-05 fired-set diff, run economics. |

## v8.6 — Agent-body procedure compression

| Document | What it covers |
|----------|----------------|
| [v8.6-measured-reduction.md](v8.6-measured-reduction.md) | Re-derived per-technique + headline agent-body line reduction (COMPRESS-01/02/03) — assembled agent body 612 to 590 lines (-22), estimate / theoretical-limit / five-whys / fishbone Procedure-slice word-count deltas, offline battery re-proof. |
| [v8.6-live-remeasure-verdict.md](v8.6-live-remeasure-verdict.md) | Live 2-row Step-0 re-measure honest verdict (MEASURE-01/02) — S-P03 fishbone 4/5 SUSTAINED (+1), S-P04 five-whys 2/5 SUSTAINED (+2, unbanked), D-05 fired-set / composer-ceiling provenance trace, RR-117-01 re-point to `_load_excerpt_v86`. |
| [v8.6-quality-ab-experiment.md](v8.6-quality-ab-experiment.md) | Post-hoc blind A/B of analysis *quality* at 590 vs 612 body lines, scored by 6 independent blinded judges against the validation rubric — no detectable difference (both arms 2/3 PASS, band total 35/35); failures track the problem, not the arm. Also reports the rubric's 2-level effective range and four reproducible output-contract defects. |

## Reference & history

| Document | What it covers |
|----------|----------------|
| [gen-01-decision.md](gen-01-decision.md) | ADR: the original GEN-01 generation-pipeline decision |
| [gen-01-rearch-milestone.md](gen-01-rearch-milestone.md) | ADR: the GEN-01 rearchitecture milestone record |
| [live-monitoring-runbook.md](live-monitoring-runbook.md) | Runbook for live routing-battery and Step 0 monitoring runs |
| [history/](history/) | Frozen per-milestone snapshots (REQUIREMENTS, ROADMAP, MILESTONE-AUDIT) — immutable archives |
