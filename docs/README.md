# docs/ — Documentation Index

> **Final state — start here:** [`v8.0-final-closure.md`](v8.0-final-closure.md) — terminal
> release record, accepted limitations, final coverage headline (133/96/0/229), and deferred-ledger
> disposition summary.

This folder documents the first-principles plugin system. New here? Start with [GETTING-STARTED.md](GETTING-STARTED.md), then [ONBOARDING.md](ONBOARDING.md), then [DATA-FLOW.md](DATA-FLOW.md).

---

## Core docs

| Document | What it covers |
|----------|----------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture: `shared/` → generation pipeline, plugin layout, five-phase agent methodology, measurement subsystem, CI + pre-commit gate table |
| [CONFIGURATION.md](CONFIGURATION.md) | Skill frontmatter rules, version-string format, reserved words, anti-masking invariants (`MIN_HEADER_HITS=2`, `_COMPOSER_FOCUS_CEILING=4`) |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Contributor workflow: `shared/` source-of-truth model, validation-script inventory, standard editing loop, pre-commit hook setup, key invariants |
| [GETTING-STARTED.md](GETTING-STARTED.md) | Install the plugin, invoke the agent and thirteen companion skills, slash invocation |
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
| [v8.1-grok-review-assessment.md](v8.1-grok-review-assessment.md) | Rated inventory of external-review (Grok) recommendations: 26 itemized GROK-NN rows with invasiveness score, already-done verification, verdict, effort estimate; SELECT-01 disposition column for Phase 144 |

## Reference & history

| Document | What it covers |
|----------|----------------|
| [gen-01-decision.md](gen-01-decision.md) | ADR: the original GEN-01 generation-pipeline decision |
| [gen-01-rearch-milestone.md](gen-01-rearch-milestone.md) | ADR: the GEN-01 rearchitecture milestone record |
| [live-monitoring-runbook.md](live-monitoring-runbook.md) | Runbook for live routing-battery and Step 0 monitoring runs |
| [history/](history/) | Frozen per-milestone snapshots (REQUIREMENTS, ROADMAP, MILESTONE-AUDIT) — immutable archives |
