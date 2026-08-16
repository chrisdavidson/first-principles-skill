# First Principles Thinking

A Claude Code plugin that gives Claude a systematic methodology for decomposing any problem into verified fundamental truths and reasoning upward from there. Use it when you want analysis that traces every conclusion back to a ground truth rather than reasoning by analogy or convention — for software design decisions, product strategy, or any domain where "we've always done it this way" is not a sufficient justification.

## When to use it

Trigger the agent when you find yourself asking:

- "Challenge the assumptions behind this design"
- "Is this the right approach, or are we just following convention?"
- "Why are we doing it this way — what are the actual ground truths?"
- "Evaluate this architectural decision from first principles"
- "Justify this decision without appealing to how others have solved it"
- "Apply a pre-mortem to this proposal"
- "Is our reasoning sound, or have we reasoned by analogy?"

Claude will also route to the agent automatically when you ask it to think from scratch, question a design, or avoid reasoning by analogy — without requiring the explicit phrase "first principles."

## The methodology

The agent applies a five-phase procedure. Each phase produces a named artifact; that artifact is the entry condition for the next phase — the chain is what makes the analysis auditable.

**Phase 1 — Identify Essence:** Strips away implementation details, historical framing, and symptoms to expose the core question. Produces an *Essence Statement* — a single sentence naming the real problem plus a checkable list of success criteria.

**Phase 2 — Challenge Assumptions:** Identifies every assumption (explicit and implicit), classifies each by type (physical law / current constraint / convention / untested belief), and applies the prescribed treatment per type. Produces a *Classified Assumptions Table*. Unchallenged assumptions that are false propagate invisibly through every later step — this phase closes that path.

**Phase 3 — Establish Ground Truths:** Compiles the verified facts that survived Phase 2 scrutiny. Each fact carries a stable GT-ID and a source citation. Unverified inputs may be included but are marked `GT-N?` and inherit a confidence caveat. Produces the *Ground Truths list*.

**Phase 4 — Reason Upward:** Constructs answers from the ground truths using whatever reasoning approach the problem calls for — derivation is free-form but must be self-documenting. Dead-end paths are recorded, not quietly discarded. Produces *Derivation Chains* in the format `GT-N + GT-M → [intermediate claim] → [conclusion]`.

**Phase 5 — Validate:** Adversarial pass over the completed chains. Finds the weakest link in each chain, checks whether unverified assumptions are load-bearing, and applies a validation rubric as a systematic gate. Produces the *Signed-off analysis* — the complete output document with all conclusions traced and all weak links either resolved or explicitly flagged.

For the complete procedure with entry/exit criteria per phase and the exact output document structure, see [`first-principles/agents/first-principles.md`](first-principles/agents/first-principles.md). The agent body is the authoritative spec — the summary above orients; it defines. For a one-page working reference with each phase's exit gate, the assumption-type treatments, and the derivation-chain format, see [docs/METHODOLOGY-CHEATSHEET.md](docs/METHODOLOGY-CHEATSHEET.md).

## Companion tools

Thirteen tools extend the methodology when the analysis calls for them. The eight companion-technique skills ship both as on-demand reference siblings of the agent (loaded automatically when the relevant trigger fires) and as standalone slash-only skills for direct invocation (`/first-principles:<name>`). The five focused-mode phase skills are slash-only stubs for direct phase invocation:

- **[Five Whys](first-principles/agents/references/five-whys.md)** (`/first-principles:five-whys`) — Root-cause drill-down procedure. Use it during Phase 3 when an analysis is stuck on *why* something is true and the surface explanation feels insufficient.
- **[Fishbone (Ishikawa)](first-principles/agents/references/fishbone.md)** (`/first-principles:fishbone`) — Breadth-first cause-category brainstorm. Use it during Phase 2 (Challenge Assumptions) when the assumption space is multi-causal and intuition cannot enumerate it confidently. Branches enter the Classified Assumptions Table as `untested belief` rows; reach for Five Whys instead when the problem is single-chain depth.
- **[Inversion](first-principles/agents/references/inversion.md)** (`/first-principles:inversion`) — Failure-enumeration procedure. Use it during Phase 2 (Challenge Assumptions) when a conclusion feels too clean; enumerate what would guarantee failure and hand each unverified precondition back to the Classified Assumptions Table as an `untested belief` row.
- **[Pre-mortem](first-principles/agents/references/pre-mortem.md)** (`/first-principles:pre-mortem`) — Prospective-hindsight failure analysis. Use it during Phase 5 to stress-test a proposed solution by imagining it has already failed and working backward to the failure modes.
- **[Trade-off Analysis](first-principles/agents/references/trade-off.md)** (`/first-principles:trade-off`) — Weighted-criteria decision procedure. Use it during Phase 4 when multiple viable options remain after ground truths are established. Criteria are weighted before scoring to prevent post-hoc rationalization.
- **[Second-Order Thinking](first-principles/agents/references/second-order.md)** (`/first-principles:second-order`) — Downstream-consequence extension procedure. Use it during Phase 4 (Reason Upward) to extend a Derivation Chain with 2nd/3rd-order effects before handing off to Phase 5; contradicting effects route back to Phase 2 for re-challenging.
- **[Estimate](first-principles/agents/references/estimate.md)** (`/first-principles:estimate`) — Fermi/dimensional-analysis magnitude rebuild. Use it during Phase 4 (Reason Upward) when a conclusion turns on a quantity whose order of magnitude has no trustworthy direct lookup; rebuilds the magnitude from constituent unit-factors with explicit lower/upper bounds as a quantitative Derivation Chain step.
- **[Theoretical Limit](first-principles/agents/references/theoretical-limit.md)** (`/first-principles:theoretical-limit`) — Constraint-relaxation upper-bound derivation. Use it during Phase 4 (Reason Upward) when a conclusion needs the ceiling the fundamentals permit once conventions are stripped; names the governing law, derives the law-permitted limit, and brackets the gap to the conventional figure.
- **Identify Essence** (`/first-principles:identify-essence`) — Phase 1 focused-mode stub. Invoke directly to strip framing artifacts and expose the core question; produces an Essence Statement with success criteria.
- **Challenge Assumptions** (`/first-principles:challenge-assumptions`) — Phase 2 focused-mode stub. Invoke directly to classify and test every assumption (physical law / constraint / convention / untested belief) before reasoning upward.
- **Ground Truths** (`/first-principles:ground-truths`) — Phase 3 focused-mode stub. Invoke directly to compile GT-ID-anchored verified facts for use as derivation-chain inputs.
- **Reason Upward** (`/first-principles:reason-upward`) — Phase 4 focused-mode stub. Invoke directly to build derivation chains upward from named ground truths; records dead-end paths explicitly.
- **Validate** (`/first-principles:validate`) — Phase 5 focused-mode stub. Invoke directly to stress-test each derivation chain for weak links and apply the validation rubric before presenting conclusions.

## Worked examples

Fourteen domain-spread examples show the methodology applied end-to-end, each with a real dead-end and a validation rubric pass:

- **[Software and systems](first-principles/agents/references/examples/software-systems.md)** — Evaluating a microservices migration decision for a monolithic codebase, tracing the actual constraints and ground truths rather than following distributed-systems fashion.
- **[Product and business](first-principles/agents/references/examples/product-business.md)** — Deciding whether to build a new pricing tier, decomposing the business assumptions and grounding the recommendation in verified market and unit-economics facts.
- **[Personal and general](first-principles/agents/references/examples/personal-general.md)** — Evaluating a career transition, separating the real constraints from conventions and untested beliefs about what the options actually are.
- **[Science and engineering](first-principles/agents/references/examples/science-engineering.md)** — Choosing a materials approach for a physical product, grounding the trade-offs in verified physical properties rather than industry convention.
- **[Ishikawa fishbone](first-principles/agents/references/examples/ishikawa-fishbone.md)** — A worked fishbone-style cause-category brainstorm; branches hand back to Phase 2's Classified Assumptions Table as `untested belief` rows.
- **[Composed Inversion + Second-Order](first-principles/agents/references/examples/composed-inversion-second-order.md)** — A worked analysis combining Inversion at Phase 2 with Second-Order Thinking at Phase 4; demonstrates the hand-back semantics for both tools and the route-back-to-Phase-2 path on contradicting downstream effects.
- **[Software and systems 2](first-principles/agents/references/examples/software-systems-2.md)** — Build vs. Buy software decision: build own auth or adopt a managed identity provider.
- **[Product and business 2](first-principles/agents/references/examples/product-business-2.md)** — Feature prioritization under a binding engineering-capacity constraint.
- **[Personal and general 2](first-principles/agents/references/examples/personal-general-2.md)** — Mortgage paydown vs. index investment: a quantitative expected-value analysis.
- **[Science and engineering 2](first-principles/agents/references/examples/science-engineering-2.md)** — In-service mechanical component failure analysis (diagnostic reasoning shape).
- **[Self-application](first-principles/agents/references/examples/self-application.md)** — Meta: applying the methodology to a contested design decision about the agent itself (agent body length vs. scope).
- **[Decompose / irreducibility](first-principles/agents/references/examples/decompose-irreducibility.md)** — Reduce-to-primitives irreducibility drill (five-whys decompose mode) applied to thermal energy storage.
- **[Estimate (Fermi)](first-principles/agents/references/examples/estimate-fermi.md)** — Order-of-magnitude rebuild of a quantity from verifiable unit factors (Fermi / dimensional analysis).
- **[Theoretical limit (Carnot)](first-principles/agents/references/examples/theoretical-limit-carnot.md)** — Law-permitted-ceiling analysis grounded in the Carnot bound (constraint relaxation).

## Relationship to the original

This project is a fork and enhancement of [`github.com/chrisdavidson/first-principles-skill`](https://github.com/chrisdavidson/first-principles-skill), MIT licensed, authored by the same person. The original is a complete, working skill with a 5-phase methodology, a standardized output format, multilingual triggers (English + Chinese), and worked examples.

The v3.8 enhanced successor adds four things the original does not have:

1. **Validation rubric** — a scoring/self-check the model applies after Phase 5 to verify the analysis met the rigor bar, with explicit criteria, levels, and a gate that blocks presenting conclusions until the rubric clears.
2. **A companion-skill surface** — eight techniques as fully described on-demand reference siblings of the agent, each with when-to-use guidance tied to a specific phase of the 5-phase spine, plus five focused-mode phase stubs for direct phase invocation. All thirteen are listed under [Companion tools](#companion-tools) above.
3. **Domain-spread worked examples** — each demonstrating a real dead-end and a complete validation pass, listed under [Worked examples](#worked-examples) above.
4. **Sharpened 5-phase methodology** — explicit entry and exit criteria per phase, named artifacts with stable IDs, a stakes-escalation rule for assumptions, and derivation chain format requirements that close the gaps where the original is loose.

[![Validation](https://github.com/chrisdavidson/first-principles-skill/actions/workflows/validation.yml/badge.svg)](https://github.com/chrisdavidson/first-principles-skill/actions/workflows/validation.yml) [![Version](https://img.shields.io/github/v/tag/chrisdavidson/first-principles-skill?label=version&color=blue)](./CHANGELOG.md) [![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE) [![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)](docs/GETTING-STARTED.md)

## Install

From the Claude Code plugin marketplace — no clone required:

```sh
/plugin marketplace add chrisdavidson/first-principles-skill
/plugin install first-principles@first-principles-skill
```

Then invoke it in a session:

```text
@agent-first-principles:first-principles   # auto-routed
/first-principles:first-principles         # explicit
```

Verify with `/doctor`; the `first-principles` agent should appear in the listing.

Two other install routes exist — a local development install (`claude --plugin-dir`, or a symlink
into `~/.claude/skills/` that always reads your working tree) and a project-scoped install under
`.claude/plugins/`. Those, the compatibility caveats, and the version-pinning behaviour that makes
the marketplace route unsuitable for plugin development are in
[docs/GETTING-STARTED.md](docs/GETTING-STARTED.md).

The v2.x dual install (root monolith + 7 namespaced plugin skills) was removed in v3.0.0.
Slash-only companion skills were re-added under `first-principles/skills/` in v3.8.0 — standalone
direct-invoke skills, not the full plugin-skill surfaces from v2.x. See
[CHANGELOG.md](./CHANGELOG.md) for the full upgrade path and for how the skill surface reached its
current size.

## Contributing

Canonical content lives in `shared/`. The agent surface (`first-principles/agents/first-principles.md`) and its on-demand reference siblings under `first-principles/agents/references/` are **generated** from `shared/` by `scripts/sync-content.py`. Edit `shared/` — never the generated agent tree directly.

**One-time setup — opt into the pre-commit drift gate (recommended):**

```sh
git config core.hooksPath .githooks
```

With the gate on, every `git commit` runs `scripts/sync-content.py --check` and fails the commit if `shared/` and the generated agent tree have drifted. Remediation:

```sh
python3 scripts/sync-content.py --write && git add -u
```

**Python requirement:** the sync script needs Python ≥ 3.12 and PyYAML. Easiest is `uv run scripts/sync-content.py --check` ([install uv](https://docs.astral.sh/uv/getting-started/installation/)); alternatively `pip install --user 'pyyaml>=6.0'` and use plain `python3`.

The hook opt-in is per-clone (Git does not propagate `core.hooksPath` automatically), so each contributor configures it once locally.

**One-time setup — opt into the body-budget pre-commit hook (recommended):**

```sh
./scripts/install-hooks.sh
```

The installer symlinks `scripts/git-hooks/pre-commit` into `.git/hooks/pre-commit` (preserving any existing hook as `.bak` on first run, idempotent on re-run). The hook blocks commits that would push the generated agent body (`first-principles/agents/first-principles.md`) over the 644-line budget (`MAX_LINES = 644` in `scripts/check-body-budget.py`). Bypass for intentional in-progress work: `git commit --no-verify`.

Why a body-line budget: keeps the generated agent body bounded (currently 644 lines) so it loads quickly into model context and stays under Claude Code's recommended budget for skill body length.

> **Note:** the body-budget installer composes BOTH gates (body budget + sync drift) into a single `.git/hooks/pre-commit`, so contributors who use the installer do not also need the `core.hooksPath = .githooks` opt-in above. Conversely, `.githooks/pre-commit` now also runs the body-budget check, so either opt-in path gives full coverage. The two mechanisms are mutually exclusive at the Git level (Git honors one hooks path or the other); pick whichever you prefer. The installer prints a WARNING if it detects `core.hooksPath` is set.

### Testing the agent

The first-principles agent's routing (when it should and shouldn't auto-delegate) is tested via a reproducible headless battery: `scripts/check-routing.py --catalog tests/routing-catalog.md` issues each prompt through `claude -p` and scores DELEGATE / NO-DELEGATE from the stream-json event stream. Sequential execution against a fresh session per prompt; exit code 0 iff the P-case and N-case thresholds are both met.

The underlying methodology (why `stream-json` is required, the two-signal detection rule, jq extraction strategies, and the `--permission-mode bypassPermissions` requirement) is documented in [docs/testing-agents-headlessly.md](docs/testing-agents-headlessly.md). For the battery thresholds and the pass criterion, see `tests/routing-catalog.md`.

## License

MIT. See [LICENSE](./LICENSE).
