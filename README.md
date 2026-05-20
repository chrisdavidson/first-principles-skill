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

## Relationship to the original

This skill is a fork and enhancement of [`github.com/chrisdavidson/first-principles-skill`](https://github.com/chrisdavidson/first-principles-skill), MIT licensed, authored by the same person. The original is a complete, working skill with a 5-phase methodology, a standardized output format, multilingual triggers (English + Chinese), and worked examples.

The v2.0 enhanced successor adds four things the original does not have:

1. **Validation rubric** — a scoring/self-check the model applies after Phase 5 to verify the analysis met the rigor bar, with explicit criteria, levels, and a gate that blocks presenting conclusions until the rubric clears.
2. **Three companion tools** — Five Whys, pre-mortem, and trade-off analysis as fully described reference files, each with when-to-use guidance tied to a specific phase of the 5-phase spine.
3. **Four domain-spread worked examples** — software/systems, product/business, personal/general, and science/engineering, each demonstrating a real dead-end and a complete validation pass.
4. **Sharpened 5-phase methodology** — explicit entry and exit criteria per phase, named artifacts with stable IDs, a stakes-escalation rule for assumptions, and derivation chain format requirements that close the gaps where the original is loose.

## Installation

The skill lives in the `first-principles-thinking/` subdirectory of this repo. The installed directory **must be named `first-principles-thinking`** — this name must match the frontmatter `name` field, and renaming it will break skill discovery.

### Personal install (recommended)

Available across all your projects:

```bash
git clone https://github.com/chrisdavidson/first-principles-skills.git

# Copy (standalone — does not stay in sync with the repo):
cp -r first-principles-skills/first-principles-thinking ~/.claude/skills/first-principles-thinking

# Or symlink (keeps the cloned repo as the live source of truth — edits picked up without re-copying):
ln -s "$(pwd)/first-principles-skills/first-principles-thinking" ~/.claude/skills/first-principles-thinking
```

### Project install

Scoped to one repo, committed to VCS:

```bash
# Copy into your project:
cp -r first-principles-skills/first-principles-thinking /path/to/your-project/.claude/skills/first-principles-thinking

# Or symlink:
ln -s /path/to/first-principles-skills/first-principles-thinking /path/to/your-project/.claude/skills/first-principles-thinking
```
