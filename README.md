# First Principles Thinking

A Claude Code skill that gives Claude a systematic methodology for decomposing any problem into verified fundamental truths and reasoning upward from there. Use it when you want analysis that traces every conclusion back to a ground truth rather than reasoning by analogy or convention — for software design decisions, product strategy, or any domain where "we've always done it this way" is not a sufficient justification.

## When to use it

Trigger this skill when you find yourself asking:

- "Challenge the assumptions behind this design"
- "Is this the right approach, or are we just following convention?"
- "Why are we doing it this way — what are the actual ground truths?"
- "Evaluate this architectural decision from first principles"
- "Justify this decision without appealing to how others have solved it"
- "Apply a pre-mortem to this proposal"
- "Is our reasoning sound, or have we reasoned by analogy?"

Claude will also apply this skill automatically when you ask it to think from scratch, question a design, or avoid reasoning by analogy — without requiring the explicit phrase "first principles."

## The methodology

The skill applies a five-phase procedure. Each phase produces a named artifact; that artifact is the entry condition for the next phase — the chain is what makes the analysis auditable.

**Phase 1 — Identify Essence:** Strips away implementation details, historical framing, and symptoms to expose the core question. Produces an *Essence Statement* — a single sentence naming the real problem plus a checkable list of success criteria.

**Phase 2 — Challenge Assumptions:** Identifies every assumption (explicit and implicit), classifies each by type (physical law / current constraint / convention / untested belief), and applies the prescribed treatment per type. Produces a *Classified Assumptions Table*. Unchallenged assumptions that are false propagate invisibly through every later step — this phase closes that path.

**Phase 3 — Establish Ground Truths:** Compiles the verified facts that survived Phase 2 scrutiny. Each fact carries a stable GT-ID and a source citation. Unverified inputs may be included but are marked `GT-N?` and inherit a confidence caveat. Produces the *Ground Truths list*.

**Phase 4 — Reason Upward:** Constructs answers from the ground truths using whatever reasoning approach the problem calls for — derivation is free-form but must be self-documenting. Dead-end paths are recorded, not quietly discarded. Produces *Derivation Chains* in the format `GT-N + GT-M → [intermediate claim] → [conclusion]`.

**Phase 5 — Validate:** Adversarial pass over the completed chains. Finds the weakest link in each chain, checks whether unverified assumptions are load-bearing, and applies a validation rubric as a systematic gate. Produces the *Signed-off analysis* — the complete output document with all conclusions traced and all weak links either resolved or explicitly flagged.

For the complete procedure with entry/exit criteria per phase and the exact output document structure, see [`first-principles-thinking/SKILL.md`](first-principles-thinking/SKILL.md). For the full annotated output template with section-by-section guidance, type definitions, and verdict vocabulary, see [`first-principles-thinking/references/output-template.md`](first-principles-thinking/references/output-template.md). These two files are the authoritative spec — the summary above orients; they define.

## Companion tools

Three tools extend the methodology when the analysis calls for them:

- **[Five Whys](first-principles-thinking/references/five-whys.md)** — Root-cause drill-down procedure. Use it during Phase 3 when an analysis is stuck on *why* something is true and the surface explanation feels insufficient.
- **[Ishikawa (fishbone)](first-principles-thinking/references/ishikawa-diagram.md)** — Breadth-first cause-category brainstorm. Use it during Phase 2 (Challenge Assumptions) when the assumption space is multi-causal and intuition cannot enumerate it confidently. Branches enter the Classified Assumptions Table as `untested belief` rows; reach for Five Whys instead when the problem is single-chain depth.
- **[Inversion](first-principles-thinking/references/inversion.md)** — Failure-enumeration procedure. Use it during Phase 2 (Challenge Assumptions) when a conclusion feels too clean; enumerate what would guarantee failure and hand each unverified precondition back to the Classified Assumptions Table as an `untested belief` row.
- **[Pre-mortem](first-principles-thinking/references/pre-mortem.md)** — Prospective-hindsight failure analysis. Use it during Phase 5 to stress-test a proposed solution by imagining it has already failed and working backward to the failure modes.
- **[Trade-off Analysis](first-principles-thinking/references/trade-off-analysis.md)** — Weighted-criteria decision procedure. Use it during Phase 4 when multiple viable options remain after ground truths are established. Criteria are weighted before scoring to prevent post-hoc rationalization.
- **[Second-Order Thinking](first-principles-thinking/references/second-order-thinking.md)** — Downstream-consequence extension procedure. Use it during Phase 4 (Reason Upward) to extend a Derivation Chain with 2nd/3rd-order effects before handing off to Phase 5; contradicting effects route back to Phase 2 for re-challenging.

## Worked examples

Four domain-spread examples show the methodology applied end-to-end, each with a real dead-end and a validation rubric pass:

- **[Software and systems](first-principles-thinking/examples/software-systems.md)** — Evaluating a microservices migration decision for a monolithic codebase, tracing the actual constraints and ground truths rather than following distributed-systems fashion.
- **[Product and business](first-principles-thinking/examples/product-business.md)** — Deciding whether to build a new pricing tier, decomposing the business assumptions and grounding the recommendation in verified market and unit-economics facts.
- **[Personal and general](first-principles-thinking/examples/personal-general.md)** — Evaluating a career transition, separating the real constraints from conventions and untested beliefs about what the options actually are.
- **[Science and engineering](first-principles-thinking/examples/science-engineering.md)** — Choosing a materials approach for a physical product, grounding the trade-offs in verified physical properties rather than industry convention.
- **[Ishikawa fishbone](first-principles-thinking/examples/ishikawa-fishbone.md)** — A worked fishbone-style cause-category brainstorm; branches hand back to Phase 2's Classified Assumptions Table as `untested belief` rows.
- **[Composed Inversion + Second-Order](first-principles-thinking/examples/composed-inversion-second-order.md)** — A worked analysis combining Inversion at Phase 2 with Second-Order Thinking at Phase 4; demonstrates the hand-back semantics for both tools and the route-back-to-Phase-2 path on contradicting downstream effects.

## Relationship to the original

This skill is a fork and enhancement of [`github.com/chrisdavidson/first-principles-skill`](https://github.com/chrisdavidson/first-principles-skill), MIT licensed, authored by the same person. The original is a complete, working skill with a 5-phase methodology, a standardized output format, multilingual triggers (English + Chinese), and worked examples.

The v2.0 enhanced successor adds four things the original does not have:

1. **Validation rubric** — a scoring/self-check the model applies after Phase 5 to verify the analysis met the rigor bar, with explicit criteria, levels, and a gate that blocks presenting conclusions until the rubric clears.
2. **Three companion tools** — Five Whys, pre-mortem, and trade-off analysis as fully described reference files, each with when-to-use guidance tied to a specific phase of the 5-phase spine.
3. **Four domain-spread worked examples** — software/systems, product/business, personal/general, and science/engineering, each demonstrating a real dead-end and a complete validation pass.
4. **Sharpened 5-phase methodology** — explicit entry and exit criteria per phase, named artifacts with stable IDs, a stakes-escalation rule for assumptions, and derivation chain format requirements that close the gaps where the original is loose.

[![Validation](https://github.com/chrisdavidson/first-principles-skills/actions/workflows/validation.yml/badge.svg)](https://github.com/chrisdavidson/first-principles-skills/actions/workflows/validation.yml)

## Install

Pick one path — installing both creates two copies of the methodology and risks Claude Code routing ambiguity between `/first-principles-thinking` (v1.2 monolith skill) and `/first-principles:thinking` (v2.0 plugin spine).

> **Pick one, not both.** The two install paths ship the *same* methodology under different invocation namespaces. Installing both makes it ambiguous which one Claude Code routes a given trigger phrase to. Choose the path that matches how you want to invoke the skill, and uninstall the other if you have it.

### v1.2 single-skill (monolith)

For users who want the methodology plus all companion references bundled under a single skill directory. Invoked as `/first-principles-thinking`. The installed directory **must be named `first-principles-thinking`** — the name must match the skill's frontmatter `name` field, and renaming it will break skill discovery.

```sh
git clone https://github.com/chrisdavidson/first-principles-skills.git
cd first-principles-skills

# Copy (snapshot — does not stay in sync with the repo)
cp -r first-principles-thinking ~/.claude/skills/first-principles-thinking

# Or symlink (keeps the cloned repo as the live source of truth — edits picked up without re-copying; recommended for contributors)
ln -s "$(pwd)/first-principles-thinking" ~/.claude/skills/first-principles-thinking
```

Verify with `/doctor` inside Claude Code; the skill should appear in the listing.

### v2.0 plugin (7 skills)

For users who want namespace-addressable companion tools (`/first-principles:five-whys`, `:fishbone`, `:inversion`, `:pre-mortem`, `:trade-off`, `:second-order`) alongside the spine (`/first-principles:thinking`). Each companion is its own skill under the `first-principles` plugin namespace.

```sh
git clone https://github.com/chrisdavidson/first-principles-skills.git
claude --plugin-dir ./first-principles-skills/first-principles
```

Marketplace install (`/plugin marketplace add ...`) is coming with the v2.0 release.

### Project-scoped install

Either path can also be installed into a single project (committed to that repo's VCS) by targeting `.claude/skills/<name>/` inside the project instead of `~/.claude/skills/`. Use this when a team wants the skill version-controlled with a specific codebase.

## Contributing

Canonical content lives in `shared/`. The monolith (`first-principles-thinking/`) and the plugin (`first-principles/skills/`) are **generated** from `shared/` by `scripts/sync-content.py`. Edit `shared/` — never the generated trees directly.

**One-time setup — opt into the pre-commit drift gate (recommended):**

```sh
git config core.hooksPath .githooks
```

With the gate on, every `git commit` runs `scripts/sync-content.py --check` and fails the commit if `shared/` and the generated trees have drifted. Remediation:

```sh
python3 scripts/sync-content.py --write && git add -u
```

**Python requirement:** the sync script needs Python ≥ 3.12 and PyYAML. Easiest is `uv run scripts/sync-content.py --check` ([install uv](https://docs.astral.sh/uv/getting-started/installation/)); alternatively `pip install --user 'pyyaml>=6.0'` and use plain `python3`.

The hook opt-in is per-clone (Git does not propagate `core.hooksPath` automatically), so each contributor configures it once locally.
