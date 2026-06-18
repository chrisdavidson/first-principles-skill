<!-- generated-by: gsd-doc-writer -->
# Getting Started

This guide walks you through installing the first-principles plugin and invoking the agent and companion skills for the first time.

## Prerequisites

- **Claude Code CLI** (required for all users)
- **Python ≥ 3.12 + PyYAML** (required only for contributors editing `shared/` source)

No Node.js, no build step. The plugin is pure Markdown.

## Installation

### Option 1: Plugin marketplace (recommended)

Inside a Claude Code session:

```sh
/plugin marketplace add chrisdavidson/first-principles-skill
/plugin install first-principles@first-principles-skill
```

### Option 2: Local development install

Clone the repo and point Claude Code at the plugin directory:

```bash
git clone https://github.com/chrisdavidson/first-principles-skill.git
claude --plugin-dir ./first-principles-skill/first-principles
```

### Option 3: Project-scoped install

Place the `first-principles/` directory under `.claude/plugins/` inside your project repo. This version-controls the plugin with the codebase so the whole team gets the same agent version.

## Verifying the install

Inside a Claude Code session, run:

```sh
/doctor
```

The `first-principles` agent should appear in the agent listing. If it does not, confirm `claude --plugin-dir` was passed correctly or that the marketplace install completed without errors.

## Invoking the agent

The agent routes automatically when your prompt matches known trigger phrases — you do not need to type a slash command:

- "Analyze from first principles…"
- "Challenge the assumptions behind…"
- "Reason from ground truth about…"
- "Decompose this problem into its foundations…"
- "Stress-test the reasoning behind…"
- "Question the design of…"
- "Evaluate whether a claim or design really works…"

To invoke explicitly:

```
@agent-first-principles:first-principles
```

or:

```
/first-principles:first-principles
```

## Companion skills

Eleven focused-mode skills extend the methodology. Each can be invoked directly:

| Skill | Invocation | When to use |
|-------|-----------|-------------|
| Identify Essence | `/first-principles:identify-essence` | Strip away implementation details to name the core question |
| Challenge Assumptions | `/first-principles:challenge-assumptions` | Classify and challenge every assumption in play |
| Ground Truths | `/first-principles:ground-truths` | Compile verified facts with stable GT-IDs |
| Reason Upward | `/first-principles:reason-upward` | Build derivation chains from ground truths |
| Validate | `/first-principles:validate` | Adversarial pass over completed chains |
| Five Whys | `/first-principles:five-whys` | Root-cause drill-down (use during Phase 3) |
| Fishbone | `/first-principles:fishbone` | Multi-causal assumption brainstorm (use during Phase 2) |
| Inversion | `/first-principles:inversion` | Failure-enumeration (use during Phase 2) |
| Pre-mortem | `/first-principles:pre-mortem` | Prospective-hindsight failure analysis (use during Phase 5) |
| Trade-off | `/first-principles:trade-off` | Weighted-criteria decision between options (use during Phase 4) |
| Second-order | `/first-principles:second-order` | Downstream-consequence extension (use during Phase 4) |

## What the agent produces

A complete first-principles analysis produces a six-section document (the fixed-shape output defined in `shared/spine/references/output-template.md`):

1. **Problem Essence** — the core question stated in one sentence, plus checkable success criteria
2. **Assumptions Table** — every assumption classified by type with a prescribed treatment and verdict
3. **Ground Truths** — verified facts with stable GT-N IDs and source citations
4. **Derivation Chains** — conclusions in the form `GT-N + GT-M → [intermediate] → [conclusion]`
5. **Abandoned Reasoning** — dead ends that were explored and ruled out, so future analysts do not re-explore them
6. **Conclusion** — synthesis of what the chains established, with recommended approach, key insight, trade-offs, and confidence level

All six sections are always present in this fixed order. If a section has no content for a given analysis, the template requires an explicit `Nothing material here — [reason]` note rather than omitting the heading.

## Common issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Agent does not appear in `/doctor` | Plugin not installed or wrong path | Re-run install; confirm `first-principles/agents/first-principles.md` exists |
| Companion skills not found | Skills directory not under the plugin root | Confirm `first-principles/skills/` is present |
| Routing not triggering automatically | Trigger phrase not matched | Use explicit invocation `@agent-first-principles:first-principles` |
| `sync-content.py` fails | Python < 3.12 or PyYAML missing | `pip install --user 'pyyaml>=6.0'` or use `uv run scripts/sync-content.py` |

## Next steps

- [Architecture](ARCHITECTURE.md) — how the source-of-truth and generated surfaces relate
- [Configuration](CONFIGURATION.md) — frontmatter fields, skill schema, and gate options
- [Development](DEVELOPMENT.md) — how to edit shared/ and run the sync pipeline
- [Testing](TESTING.md) — validation scripts and routing battery
