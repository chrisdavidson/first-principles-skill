# Phase 1: Sharpen the Methodology and Harden the Output Format - Research

**Researched:** 2026-05-16
**Domain:** Content authoring — sharpening a 5-phase reasoning methodology and hardening its output template (pure Markdown, no code)
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** Output template uses **strict shape, honest depth** — all sections must be present and in fixed order, but any section may be marked `Nothing material here — [reason]` when justified. Prevents box-ticking while keeping the auditable shape intact.
- **D-02:** Conclusion-to-ground-truth traceability map takes the form of **derivation chains** (`GT-1 + GT-2 → intermediate → conclusion`), not a flat linking table. Ground truths get stable IDs. Chains are verbose by nature — instructions should keep them disciplined (one chain per conclusion, no redundant restatement).
- **D-03:** Output template includes a **dedicated "Abandoned Reasoning" (Dead Ends) section** where discarded paths and why-they-failed are recorded. This gives Phase 5's dead-end demonstrations a natural home.
- **D-04:** Reason Upward is **free but self-documenting** — no prescribed sub-steps for *how* to reason upward, but Claude must narrate its own reasoning path as it goes. Freedom is in the method; mandatory transparency replaces prescribed structure.
- **D-05:** Reason Upward's exit criterion is **both conditions**: the problem's core question is answered AND every conclusion offered has a complete derivation chain back to named ground truths.
- **D-06:** Four assumption categories carry **prescribed actions plus a stakes-escalation rule** — physical law → accept as ground-truth candidate; current constraint → record expiry conditions; convention → must be explicitly challenged before use; untested belief → must be verified or flagged unverified. Higher stakes = push assumption down toward physical law or verified ground truth.
- **D-07:** An unverified assumption **is allowed in a derivation chain but must be visibly flagged** (e.g. `GT-3?: unverified`). Any conclusion depending on it inherits an explicit confidence caveat.
- **D-08:** The test-run **dogfoods a real open project design decision** from this skill build, not a toy or neutral problem.
- **D-09:** The test-run is **kept as a working draft in `.planning/`**, not shipped as an `examples/` file (that is Phase 5's scope).

### Claude's Discretion

- Exact wording of each phase's entry/exit criteria and the precise names of each phase's output artifact
- How per-phase artifacts accumulate into the final output document
- The phrasing of each phase's rationale statement (METH-06 requires rationale, not bare imperatives)
- The exact section list and ordering of the output template (beyond the mandated assumptions table, derivation-chain traceability map, and Abandoned Reasoning section)
- Which specific open project design decision is chosen as the test-run subject

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope. Items belonging to later phases: the validation rubric (Phase 3), companion tools (Phase 4), the four shipped worked examples (Phase 5), `SKILL.md` frontmatter and body assembly (Phase 2). The Phase 1 test-run is explicitly kept as a draft for Phase 5 to polish (D-09) rather than shipped here.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| METH-01 | Each of the 5 phases has explicit entry and exit criteria stating when the phase is done | Original skill has none — gap analysis below covers what must be added |
| METH-02 | Each phase names the concrete artifact it must produce before the next phase begins | Original skill has no named artifacts — gap analysis below covers what each phase should produce |
| METH-03 | The Challenge-Assumptions phase includes an assumption-classification scheme (physical law / current constraint / convention / untested belief) | Original has only "categories" of assumptions (technical, business, resource, historical) — the 4-type classification must replace this |
| METH-04 | The standardized output format is a strict template with required sections, including the assumptions table | Original has an assumptions table but no strict shape enforcement or "must be present" language |
| METH-05 | The output format requires an explicit conclusion-to-ground-truth traceability map | Original has a linear arrow chain (`Ground Truth → Step 1 → Step 2 → Solution`) — must become derivation chains per D-02 |
| METH-06 | Methodology instructions state the rationale behind each rule rather than bare imperatives | Original phases are bare-imperative bullet lists — rationale statements must be added throughout |
</phase_requirements>

---

## Summary

Phase 1 is a **content authoring** phase, not a software build. It produces three artifacts in Markdown: (1) a sharpened 5-phase methodology with per-phase entry/exit criteria and named output artifacts, (2) a hardened output template with an assumptions table and derivation-chain traceability map, and (3) a test-run working draft that dogfoods the methodology on a real design decision. None of this touches `SKILL.md` (that is Phase 2).

The original `first-principles-skill` (`github.com/chrisdavidson/first-principles-skill`) provides a concrete, working baseline. It is a functional skill with a 5-phase structure and a standardized output format. However, it fails all six of the Phase 1 requirements: phases have no entry/exit criteria, no named artifacts, no rationale statements; the output template has no strict shape enforcement; and the traceability is a flat linear arrow chain, not derivation chains. The enhancement work is additive rather than rewrite work — the phase names, logical ordering, and basic assumption-table pattern are all sound and should be preserved. What must be added is precision, auditability, and rigor at every layer.

The dominant risk for this phase is the classic two-sided failure: too abstract (phases stay inspiring labels, no operational meaning) versus too prescriptive (strict template causes box-ticking, filled but not reasoned). The locked decisions (D-01 through D-07) directly mitigate both: strict shape but honest depth (D-01), one high-freedom phase (D-04), self-documenting rather than prescribed sub-steps (D-04), and explicit flagging of unverified assumptions rather than blocking progress (D-07). The planner's task is to translate these decisions into concrete task actions — specifically, what text to write for each phase definition and what sections to include in the template.

**Primary recommendation:** Author the methodology as standing instructions (not one-time steps), give each phase a one-sentence operation, a named artifact, an entry criterion, and an exit criterion, then write the template as a strict-shape document where the section list is fixed but content depth is flexible. Test the whole thing by running the methodology on a real, contested design question from the current skill build.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| 5-phase methodology definition | Phase 1 content (standalone Markdown docs) | Phase 2 (embeds into SKILL.md) | Methodology must be stable before it is embedded; Phase 1 owns authoring, Phase 2 owns placement |
| Output template shape | Phase 1 content | Phase 2 (embedded as standing instruction in SKILL.md body) | Template is the contract all later phases calibrate against; Phase 1 must finalize it |
| Assumption classification scheme | Phase 1 content (Challenge-Assumptions phase definition) | Phase 3 (rubric scores correct application) | Classification is methodology content; rubric scores against it, not defines it |
| Derivation-chain format | Phase 1 (template section D-02) | Phase 5 (examples demonstrate the format) | Phase 1 defines the chain format; examples demonstrate it, not invent it |
| Test-run dogfooding draft | Phase 1 (`.planning/` working draft) | Phase 5 (polishes into a shipped example) | D-09: test-run is a Phase 1 verification artifact, not a Phase 5 deliverable |
| Validation rubric | Phase 3 | — | Explicitly deferred; Phase 1 must not author the rubric |
| SKILL.md frontmatter and body | Phase 2 | — | Phase 1 produces content, Phase 2 places it |

---

## Baseline Analysis: Original Skill

This section documents what the original `chrisdavidson/first-principles-skill` already contains per phase, what the output format looks like, and where it falls short of the 6 success criteria. The planner uses this as the before/after delta to scope each task.

[VERIFIED: github.com/chrisdavidson/first-principles-skill — SKILL.md fetched directly]

### Original Frontmatter

```yaml
name: First Principles Thinking
description: <trigger phrases in English and Chinese>
version: 0.2.0
```

Note: `version` at top level is not in the Agent Skills open standard schema — it should move to `metadata: { version: "..." }` in Phase 2. Phase 1 does not touch frontmatter.

### Original 5-Phase Definitions

**Phase 1 — Identify the Problem's Essence:**
- Operation: "Strip away implementation details to find the core problem"
- Three sub-steps: state the problem, separate symptoms from causes, define success criteria
- Key questions listed (implicit)
- Entry criterion: NONE
- Exit criterion: NONE
- Named artifact: NONE
- Rationale: NONE (bare imperative bullets)

**Phase 2 — Challenge All Assumptions:**
- Operation: "Identify and interrogate every assumption"
- Three sub-steps: list explicit assumptions, surface implicit assumptions, test each assumption
- Assumption categories: technical, business, resource, historical (4 dimensions — NOT the physical law / constraint / convention / untested belief classification required by METH-03)
- Red flags listed for detecting false assumptions
- Entry criterion: NONE
- Exit criterion: NONE
- Named artifact: NONE
- Rationale: NONE

**Phase 3 — Establish Ground Truths:**
- Operation: "Identify irreducible facts"
- Three sub-steps: physics/math constraints, business invariants, user needs
- Ground Truth Test described (facts must be irreducible, provably true, not conventionally believed)
- Entry criterion: NONE
- Exit criterion: NONE
- Named artifact: NONE
- Rationale: NONE

**Phase 4 — Reason Upward:**
- Operation: "Build solutions from ground truths"
- Three sub-steps: start minimal, add only what's necessary, challenge each layer
- Building Blocks Approach described
- Entry criterion: NONE
- Exit criterion: NONE
- Named artifact: NONE
- Rationale: NONE

**Phase 5 — Validate the Reasoning:**
- Operation: "Ensure solution soundness"
- Three sub-steps: trace back to ground truths, identify weak links, stress test
- Entry criterion: NONE
- Exit criterion: NONE
- Named artifact: NONE
- Rationale: NONE

### Original Standardized Output Format

```markdown
## First Principles Analysis: [Topic]

### 1. Problem Essence
**Core problem:** [One sentence]
**Success criteria:** [Measurable outcomes]

### 2. Assumptions Challenged
| Assumption | Challenge | Verdict |
|------------|-----------|---------|
| [Assumption] | [Why question it] | [Keep/Discard/Modify] |

### 3. Ground Truths
- [Irreducible fact 1]
- [Irreducible fact 2]
- [Irreducible fact 3]

### 4. Reasoning Chain
Ground Truth → [Step 1] → [Step 2] → Solution

### 5. Conclusion
**Recommended approach:** [Description]
**Key insight:** [What the first principles analysis revealed]
**Trade-offs acknowledged:** [What we're accepting]
```

### Worked Example: Microservices Architecture Review [VERIFIED: fetched from GitHub]

The existing example (`examples/architecture-review.md`) is the strongest part of the original skill. It:
- Follows the 5-phase structure with real data (team size 12, 2 deploy conflicts/month, 200ms latency budget)
- Shows explicit assumption verdicts ("Netflix has 2000+ engineers. We have 12. **Discard** - Different scale")
- Traces conclusions to ground truths ("30% time already on infrastructure → Microservices would increase this to 50%+")
- Recommends a modular monolith over microservices with defined revisit triggers

What it lacks: no assumption classification by type (law/constraint/convention/belief), no derivation chains with stable IDs, no "Abandoned Reasoning" section, no rationale for why each phase step matters.

### Gap Analysis: Where Original Falls Short

| Requirement | Original Status | What Must Be Added |
|-------------|-----------------|---------------------|
| METH-01: Entry/exit criteria | ABSENT from all 5 phases | An entry criterion ("begin when X") and exit criterion ("done when Y") for each phase |
| METH-02: Named per-phase artifacts | ABSENT from all 5 phases | A concrete named artifact each phase must produce (e.g., "Essence Statement", "Classified Assumptions Table") |
| METH-03: Assumption classification scheme | Wrong taxonomy (technical/business/resource/historical) | Replace with 4-type scheme (physical law / current constraint / convention / untested belief) with prescribed treatments per D-06 |
| METH-04: Strict output template | Template present but not enforced ("strict shape" language absent; no "must be present" rules) | Add enforcement language, fixed section order, the "Nothing material here — [reason]" escape valve per D-01 |
| METH-05: Derivation-chain traceability | Flat arrow chain: `Ground Truth → Step 1 → Step 2 → Solution` | Replace with per-conclusion derivation chains with stable GT-IDs per D-02; add Abandoned Reasoning section per D-03 |
| METH-06: Rationale statements | ABSENT — all instructions are bare imperatives | Add a rationale clause to every phase instruction ("...because X") |

---

## Standard Stack

### Core

No external packages. Phase 1 is pure Markdown content authoring. The "stack" is the authoring methodology itself.

| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| Markdown (CommonMark) | n/a | All deliverable files | Mandated by project constraints (pure-Markdown v1); SKILL.md format requirement |
| Git | System | Version control for artifacts | Standard project tooling |

### No External Dependencies

This phase produces text files. No npm packages, Python packages, or other runtime dependencies are required. Step 2.6 (Environment Availability Audit) is SKIPPED — the phase has no external dependencies beyond git and a text editor.

---

## Package Legitimacy Audit

Not applicable. Phase 1 installs no external packages.

---

## Architecture Patterns

### How Phase 1 Artifacts Fit in the 3-Layer Architecture

Phase 1 produces **content** that Phase 2 places into the architecture. The research (ARCHITECTURE.md) establishes that the skill is a 3-layer context-loading system: Layer 1 (frontmatter), Layer 2 (SKILL.md body — always resident), Layer 3 (on-demand references/examples). Phase 1's deliverables become the core of Layer 2.

### System Architecture Diagram

```
Phase 1 Authoring Scope
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Sharpened 5-Phase Methodology (Markdown prose)        │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Phase 1: Identify Essence                        │  │
│  │   Entry → [operation] → Exit → [named artifact] │  │
│  │                                                  │  │
│  │ Phase 2: Challenge Assumptions                   │  │
│  │   Entry → [classification scheme + D-06 rules]  │  │
│  │          → Exit → [classified assumptions table] │  │
│  │                                                  │  │
│  │ Phase 3: Establish Ground Truths                 │  │
│  │   Entry → [irreducibility test]                  │  │
│  │          → Exit → [ground truth list with IDs]  │  │
│  │                                                  │  │
│  │ Phase 4: Reason Upward (HIGH-FREEDOM per D-04)  │  │
│  │   Entry → [self-documenting narration rule]      │  │
│  │          → Exit → both conditions (D-05)         │  │
│  │                                                  │  │
│  │ Phase 5: Validate                                │  │
│  │   Entry → [rubric note — rubric is Phase 3]     │  │
│  │          → Exit → [signed-off analysis]          │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  Hardened Output Template (Markdown)                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Strict-shape document per D-01:                  │  │
│  │   § Problem Essence                              │  │
│  │   § Assumptions Table (classified, per METH-03) │  │
│  │   § Ground Truths (with stable IDs)              │  │
│  │   § Derivation Chains (per D-02)                 │  │
│  │   § Abandoned Reasoning / Dead Ends (per D-03)  │  │
│  │   § Conclusion + Confidence Caveats (per D-07)  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  Test-Run Draft (.planning/ working file)              │
│  → Real design decision from this skill build (D-08)  │
│  → Full trace: every conclusion → named ground truth   │
│  → Kept as draft for Phase 5 to polish (D-09)         │
│                                                         │
└─────────────────────────────────────────────────────────┘
           │
           │ consumed by
           ↓
Phase 2: SKILL.md Skeleton and Frontmatter
(embeds methodology as standing instructions in Layer 2)
```

### Recommended Deliverable Structure

Phase 1 produces working files, not the final skill directory. The planner should create tasks that produce:

```
.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/
├── 01-CONTEXT.md          (already exists — input)
├── 01-RESEARCH.md         (this file — input to planner)
├── methodology.md         (sharpened 5-phase procedure — authored in this phase)
├── output-template.md     (hardened output template — authored in this phase)
└── test-run-draft.md      (dogfooding test run — authored in this phase, kept as draft)
```

These working files are the Phase 1 artifacts. Phase 2 takes `methodology.md` and `output-template.md` and embeds them into `SKILL.md`. Phase 5 takes `test-run-draft.md` and polishes it into a shipped example.

### Pattern: Each Phase Definition Has Four Required Components

Every phase definition in `methodology.md` must have all four of these or METH-01 and METH-02 are not satisfied:

```markdown
### Phase N: [Name]

**Why this phase exists:** [rationale — satisfies METH-06]

**Entry criterion:** [what must be true before this phase begins]

**Operation:** [the concrete action this phase performs]

**Named artifact:** [the specific output this phase produces, referenced by name]

**Exit criterion:** [what must be true for this phase to be complete]
```

### Pattern: Assumption Classification Table (METH-03 + D-06)

The hardened assumptions table replaces the original's three-column format with a five-column format that encodes the classification:

```markdown
| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| [Assumption text] | physical law / current constraint / convention / untested belief | [per D-06 prescribed action] | Accept / Challenge / Discard | [source or "unverified — flagged"] |
```

Types and prescribed treatments (D-06):
- **physical law** → accept as a ground-truth candidate
- **current constraint** → record what would change it (expiry conditions)
- **convention** → must be explicitly challenged before use
- **untested belief** → must be verified or flagged unverified (D-07 applies)

### Pattern: Derivation Chains with Stable IDs (D-02)

Each ground truth gets a stable identifier (`GT-1`, `GT-2`, etc.). The traceability map is per-conclusion, showing the reasoning steps:

```markdown
## Derivation Chains

### Conclusion: [Conclusion text]
GT-1 (team size = 12, verified) + GT-3 (deploy frequency = 2 conflicts/month, verified)
→ [intermediate: coordination cost is low at current scale]
→ [conclusion: microservices overhead exceeds coordination benefit]
**Confidence:** HIGH (all ground truths verified)

### Conclusion: [Another conclusion]
GT-2 (latency budget = 200ms, verified) + GT-4?: [unverified — budget assumed from PM]
→ [intermediate: ...]
→ [conclusion: ...]
**Confidence:** MEDIUM (GT-4 unverified — conclusion inherits caveat per D-07)
```

Key rules from D-02 and D-07:
- One chain per conclusion — no redundant restatement
- Unverified ground truths get the `?` suffix: `GT-N?`
- Any conclusion with an unverified input inherits a `MEDIUM` or `LOW` confidence caveat

### Pattern: Abandoned Reasoning Section (D-03)

```markdown
## Abandoned Reasoning

### Dead End: [Name of discarded path]
**What was tried:** [brief description]
**Why abandoned:** [the specific failure — assumption false, contradicts ground truth, etc.]
**What it ruled out:** [what this dead end saves the reader from re-exploring]
```

This section is required in every analysis. If no reasoning was abandoned, write: `Nothing material here — all reasoning paths pursued led to the conclusion above. [Optional: describe the problem's constraint space that made alternative paths infeasible.]`

### Anti-Patterns to Avoid

- **Box-ticking:** Filling the template sections with words that say nothing — e.g., "Assumption: Things might be different than we think. Challenge: Why? Verdict: Keep." The `Nothing material here` escape valve is specifically for avoiding forced fabrication.
- **Chain padding:** Writing derivation chains that restate the same idea multiple times with different wording. One chain per conclusion, no restatement.
- **Over-prescribing Phase 4:** Reason Upward must remain high-freedom per D-04. Do not add sub-steps to this phase in `methodology.md` — the only constraint is self-documenting narration.
- **Assumption re-classification drift:** The four types (physical law / current constraint / convention / untested belief) are locked by D-06. Do not substitute synonyms or add a fifth type.
- **Shipping the test-run:** D-09 is explicit — the test-run belongs in `.planning/`, not in `examples/`. Phase 5 ships examples.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Assumption classification | A novel 5-type or 6-type taxonomy | The 4-type scheme in D-06 (physical law / current constraint / convention / untested belief) | User has locked this in CONTEXT.md D-06; it is derived from established first-principles thinking literature |
| Traceability format | A flat linking table or a novel format | Derivation chains per D-02 | User has locked this in CONTEXT.md D-02; flat tables lose the reasoning steps that make chains auditable |
| Output template strictness | A fully optional template | Strict-shape + honest-depth per D-01 | Prevents box-ticking (PITFALLS.md Pitfall 4) while keeping auditability |
| Phase 4 structure | Prescribed sub-steps for Reason Upward | Mandatory self-documenting narration only, per D-04 | Over-prescribing Phase 4 is the specific failure mode D-04 mitigates |

**Key insight:** All four of these are locked by user decisions in CONTEXT.md, not open design questions. The planner should not task discovery work on any of them.

---

## Common Pitfalls

### Pitfall 1: Methodology Phases Written as One-Time Steps

**What goes wrong:** Phase definitions written as "First, do X. Then do Y." read as already-done instructions from turn 2 onward (skill content is injected once and stays resident). By Phase 5 of an analysis, Phase 1's instructions read as past tense.

**Why it happens:** Writing sequentially feels natural. The methodology is a sequence, so sequential prose feels right.

**How to avoid:** Write every phase instruction as a standing instruction — "When working on this phase, do X" or imperative present tense "Do X" rather than "First, do X" chains. The methodology is a *procedure Claude follows*, not a *recipe that runs once*.

**Warning signs:** Instructions use "first", "then", "next" as structural connectors rather than "while", "when", "at this stage".

### Pitfall 2: Exit Criteria That Are Not Testable

**What goes wrong:** An exit criterion like "when you are confident the ground truths are solid" cannot be checked. The point of explicit exit criteria is auditability — a skeptic should be able to verify the phase was done.

**Why it happens:** Confident-sounding criteria feel rigorous but are actually vague.

**How to avoid:** Write exit criteria as observable state checks: "Exit when: each listed assumption has a classification from the 4-type scheme AND a prescribed treatment has been applied or explicitly declined with justification." A skeptic can verify this by looking at the table.

**Warning signs:** Exit criteria contain "confident", "satisfied", "adequate", "sufficiently" without a concrete threshold.

### Pitfall 3: Test-Run Problem That Is Too Safe

**What goes wrong:** The test-run dogfoods a settled, non-controversial design decision ("should we use Markdown?") that produces a clean march to the obvious answer. D-08 specifically requires a **genuinely unresolved** design decision. A clean march test-run cannot demonstrate the Abandoned Reasoning section or show derivation chains under uncertainty.

**Why it happens:** Safe problems are easier to complete. The dogfooding goal gets served as a box to tick rather than a real test.

**How to avoid:** Choose a design decision where reasonable people could disagree and where at least one false assumption is genuinely present to be discovered. Good candidates from this skill build: "Should the assumption classification scheme use 4 types or be more granular?", "Should Phase 4 (Reason Upward) have any prescribed sub-steps at all?", "Should the output template require a separate Dead Ends section or integrate dead ends inline?"

**Warning signs:** The test-run has zero dead ends, all ground truths are verified, and the conclusion was obvious before running the methodology.

### Pitfall 4: Rationale Statements That Are Still Imperatives

**What goes wrong:** METH-06 requires each rule to state its rationale, not be a bare imperative. A "rationale" that says "Challenge assumptions because you should challenge assumptions" is circular and fails the requirement.

**Why it happens:** Adding "because X" to a bare imperative feels like it satisfies the requirement, but often the "because" just restates the instruction in different words.

**How to avoid:** Each rationale should answer "what does failing this step cost the analysis?" — e.g. "Challenge assumptions because an unchallenged assumption that is false propagates silently through every later step, making the conclusion trace back to an error rather than a ground truth. The analysis looks rigorous while being built on sand."

**Warning signs:** The rationale uses "in order to", "so that", or "because it is important" without stating the specific failure mode that omitting the step produces.

### Pitfall 5: Derivation Chains That Are Actually Flat Lists

**What goes wrong:** The derivation chains section is authored as: "GT-1 supports the conclusion. GT-2 also supports the conclusion." This is a flat list with GT labels, not a chain. D-02 specifies a step chain that shows *how* ground truths combine into intermediates and how intermediates combine into conclusions.

**Why it happens:** Flat lists are faster to write. The distinction between "GT-1 supports X" and "GT-1 + GT-3 → intermediate → X" seems stylistic but is structurally significant — the intermediate is where the reasoning happens.

**How to avoid:** Enforce the format `GT-N + GT-M → [intermediate claim] → [conclusion]`. The intermediate must be a new claim that could not be stated from either ground truth alone. If no intermediate exists, it suggests the conclusion is too close to the ground truth (not interesting) or the chain is missing a step.

**Warning signs:** Chains have no intermediate step — they go directly from GT-IDs to conclusion.

---

## Code Examples

Verified patterns for Phase 1 content authoring:

### Correct Phase Definition Format (all 4 required components)

```markdown
### Phase 2: Challenge Assumptions

**Why this phase exists:** An unchallenged assumption that is false propagates invisibly through every later reasoning step. By explicitly classifying and testing each assumption before establishing ground truths, the analysis prevents false premises from masquerading as verified facts — the single most common cause of first-principles analysis that sounds rigorous but isn't.

**Entry criterion:** The Essence Statement from Phase 1 is complete.

**Operation:** For each assumption (explicit and implicit) relevant to the problem, classify it by type, apply the prescribed treatment, and record the verdict. When stakes are high, push the assumption toward physical law or verified ground truth status rather than accepting a weaker classification.

**Named artifact:** Classified Assumptions Table — a table with columns: Assumption, Type, Treatment, Verdict, Verification.

**Exit criterion:** Every assumption in scope has a classification from the 4-type scheme (physical law / current constraint / convention / untested belief) AND has a recorded verdict and verification note (or explicit "unverified — flagged" per D-07).
```

### Correct Derivation Chain Format (D-02)

```markdown
### Conclusion: A modular monolith is preferable to microservices for this team

GT-1 (team size = 12 engineers, source: org chart) + GT-3 (2 deploy conflicts/month, source: git log analysis)
→ [coordination overhead at current scale is low — 12 engineers produce fewer than 3 deploy conflicts/month]
→ [microservices' primary benefit — independent deploy velocity — does not address the team's actual bottleneck]

GT-2 (infrastructure time = 30% of engineering capacity, source: time-tracking data) + GT-4 (microservices baseline overhead = 20-25% additional infrastructure, source: CNCF 2024 survey)
→ [adopting microservices would push infrastructure time to ~50-55%]
→ [the coordination problem microservices would solve costs less than the infrastructure overhead they would add]

**Confidence:** HIGH — all ground truths verified. Would revisit if GT-3 (deploy conflicts) rises above 10/month.
```

### Correct Abandoned Reasoning Entry (D-03)

```markdown
## Abandoned Reasoning

### Dead End: "Use microservices to enable independent team scaling"

**What was tried:** Reasoning from "we may hire more engineers" as a ground truth to "therefore we need microservices now."

**Why abandoned:** Future team size is a current constraint (type: current constraint), not a physical law or verified fact. GT-1 (current team = 12) is verified; "future team = 50" is speculative. An assumption of type "untested belief" cannot anchor a derivation chain without inheriting a confidence caveat — and in this case, the caveat would need to be so strong (we have no hiring plan, no funding round announced) that the conclusion collapses. The analysis was redesigned around verified ground truths only.

**What it ruled out:** Proactive microservices adoption justified by projected growth. Any future revisit of this decision should first verify the team-size ground truth at that time.
```

### Phase 4 (Reason Upward) Definition — High-Freedom Format (D-04)

```markdown
### Phase 4: Reason Upward

**Why this phase exists:** The methodology has established what is true (ground truths) and what can be discarded (false assumptions). Now Claude must construct from those truths upward to an answer. This phase is deliberately high-freedom because the right method for combining ground truths depends entirely on the problem's structure — there is no single "correct" way to reason upward that works across engineering, business, and scientific domains. Prescribing sub-steps would constrain reasoning that should be shaped by the problem, not the methodology.

**Entry criterion:** The Ground Truths list is complete (all ground truths carry IDs and verification notes), and the Classified Assumptions Table from Phase 2 is finalized.

**Operation:** Reason upward from the ground truths toward an answer using whatever approach the problem calls for. As you go, narrate what you are trying, what you are building on, and why. If a reasoning path leads to a dead end, record it in the Abandoned Reasoning section before changing course. Do not use analogies as evidence — any reference to how others have solved similar problems must be grounded in a verified ground truth about their situation, not used as direct justification.

**Named artifact:** Derivation Chains — one chain per conclusion, formatted as `GT-N + GT-M → [intermediate] → [conclusion]`, with confidence levels per D-07.

**Exit criterion:** BOTH conditions must hold: (1) the problem's core question is answered, AND (2) every conclusion offered has a complete derivation chain back to named ground truths. Partial conclusions or incomplete chains do not exit this phase.
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `Ground Truth → Step 1 → Step 2 → Solution` (flat linear chain) | Per-conclusion derivation chains with stable GT-IDs (`GT-1 + GT-2 → intermediate → conclusion`) | Phase 1 (D-02) | Conclusions become individually auditable; unverified inputs are visibly flagged |
| Assumption categories: technical / business / resource / historical | 4-type classification: physical law / current constraint / convention / untested belief | Phase 1 (D-06 from CONTEXT.md) | Classification drives prescribed treatment, not just labeling |
| No entry/exit criteria | Explicit entry criterion + exit criterion per phase | Phase 1 (METH-01) | Phase skipping becomes detectable; analysis is auditable phase-by-phase |
| Bare imperative bullets ("List explicit assumptions") | Rationale-carrying instructions ("...because unchallenged assumptions propagate invisibly...") | Phase 1 (METH-06) | Claude can generalize the method to novel problem types; brittleness reduced |
| No dedicated dead-ends section | Required "Abandoned Reasoning" section (D-03) | Phase 1 | Discarded reasoning becomes auditable; Phase 5 examples have a natural home for dead-end demonstrations |

**Deprecated/outdated from the original:**
- Assumption categories (technical/business/resource/historical): replaced by the 4-type classification scheme
- Flat `Reasoning Chain` section: replaced by per-conclusion derivation chains
- Optional-feel output template ("things to include"): replaced by strict-shape document with required sections

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The working files (`methodology.md`, `output-template.md`, `test-run-draft.md`) should be staged in `.planning/phases/01-...` rather than in a separate scratch location | Recommended Deliverable Structure | Low — location is a planning convention, not a correctness requirement. Planner may choose a different staging location. |
| A2 | The test-run should pick from among the three candidate design questions listed in Pitfall 3 | Common Pitfalls — Pitfall 3 | Low — these are examples, not a locked list. The key constraint from D-08 is that the problem be genuinely unresolved; the specific question is Claude's discretion. |
| A3 | Phase 5's exit criterion requires BOTH conditions (from D-05) meaning partial analysis that answers the question without complete chains does not pass — this is a stricter gate than "mostly done" | Code Examples section | Medium — misreading D-05 as an OR condition (either the question is answered OR chains are complete) would produce incomplete traceability. D-05 is explicitly AND. |

---

## Open Questions

1. **How many ground truths typically occupy the test-run?**
   - What we know: The microservices example has 6 empirical ground truths, which produced a convincing analysis
   - What's unclear: Whether 6 is a target, a minimum, or just what that problem needed
   - Recommendation: Do not set a fixed count. The exit criterion for Phase 3 (ground truths complete when all truths are irreducible and verified) is the gate, not a number. The planner should not impose a count in task instructions.

2. **Should `methodology.md` and `output-template.md` be a single file or two separate files?**
   - What we know: Phase 2 will embed both into `SKILL.md`; the template is the concrete encoding of the methodology phases
   - What's unclear: Whether keeping them separate in `.planning/` aids review or creates unnecessary navigation
   - Recommendation: Two separate files — `methodology.md` (the procedure, Phase 2 embeds as standing instructions) and `output-template.md` (the template, Phase 2 embeds as the output format). They serve different functions in `SKILL.md` and are easier to review independently.

3. **What is the right test-run problem for dogfooding?**
   - What we know: D-08 requires a genuine unresolved design decision from the skill build; D-09 says keep as draft
   - What's unclear: The specific question — user has left this to Claude's discretion (CONTEXT.md "Claude's Discretion")
   - Recommendation: The best candidates from the current build are: (a) "Should Phase 4 (Reason Upward) have any prescribed sub-steps, or should it remain fully free-form?", (b) "Should the output template's Abandoned Reasoning section be required or optional?", or (c) "Should assumption classification use 4 types or allow a 'mixed / uncertain' fifth category?" All three were real design discussions during the planning phase. The planner should pick one and lock it as the test-run subject.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Manual verification against success criteria (no automated test framework; pure-Markdown content authoring) |
| Config file | none |
| Quick run command | Read each deliverable and check success criteria checklist manually |
| Full suite command | Run the methodology on the test-run problem and verify every conclusion traces to a named ground truth |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| METH-01 | Each of the 5 phases has an entry criterion and an exit criterion | Manual inspection | n/a — content review | ❌ Wave 0 (methodology.md does not exist yet) |
| METH-02 | Each phase names a concrete artifact it produces | Manual inspection | n/a — content review | ❌ Wave 0 |
| METH-03 | Challenge-Assumptions phase includes the 4-type classification scheme with prescribed treatments | Manual inspection | n/a — content review | ❌ Wave 0 |
| METH-04 | Output template is strict-shape with required sections | Manual inspection | n/a — content review | ❌ Wave 0 (output-template.md does not exist yet) |
| METH-05 | Output template includes per-conclusion derivation chains with GT-IDs | Manual inspection | n/a — content review | ❌ Wave 0 |
| METH-06 | Every phase instruction states a rationale | Manual inspection | n/a — content review | ❌ Wave 0 |
| SC-4 | Test-run produces an analysis where every conclusion traces to a named ground truth | Dogfooding run | n/a — produce and inspect the draft | ❌ Wave 0 (test-run-draft.md does not exist yet) |
| SC-5 | At least one phase (Reason Upward) is deliberately high-freedom | Manual inspection | n/a — content review | ❌ Wave 0 |

All requirements require manual inspection of authored content — this is expected for a content-authoring phase. There is no automated test runner applicable.

### Sampling Rate

- **Per task commit:** Re-read the authored file and check success-criteria checklist for that task
- **Per wave merge:** Full manual review of all three deliverables against all 6 requirements
- **Phase gate:** Run the test-run methodology in full and verify every conclusion in `test-run-draft.md` has a complete derivation chain before marking Phase 1 done

### Wave 0 Gaps

- [ ] `methodology.md` — covers METH-01, METH-02, METH-03, METH-06, SC-5 — does not exist; Wave 0 task creates it
- [ ] `output-template.md` — covers METH-04, METH-05 — does not exist; Wave 0 task creates it
- [ ] `test-run-draft.md` — covers SC-4 — does not exist; Wave 0 task creates it by running the methodology on a real design question

---

## Security Domain

This phase is pure Markdown content authoring with no authentication, data storage, user input, API calls, or executable code. The ASVS categories do not apply. No security review is required for this phase.

---

## Environment Availability

Step 2.6: SKIPPED — no external dependencies. Phase 1 requires only a text editor and git, both available in the current environment.

---

## Sources

### Primary (HIGH confidence)

- `github.com/chrisdavidson/first-principles-skill` — SKILL.md, examples/architecture-review.md, references/software-examples.md fetched directly. Original methodology text, output format, and worked example captured verbatim for gap analysis.
- `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/01-CONTEXT.md` — locked decisions D-01 through D-09, canonical constraints for Phase 1 content.
- `.planning/REQUIREMENTS.md` — full text of METH-01 through METH-06.
- `.planning/research/PITFALLS.md` — Pitfall 3 (too abstract) and Pitfall 4 (box-ticking) directly shaped the anti-patterns and pitfalls sections above.
- `.planning/research/FEATURES.md` — entry/exit criteria feature expectations, assumption-classification scheme description.
- `.planning/research/ARCHITECTURE.md` — 3-layer loading model; Phase 1 produces Layer 2 content.

### Secondary (MEDIUM confidence)

- `.planning/research/SUMMARY.md` — Phase 1 rationale, abstract-vs-prescriptive risk framing, methodology-sharpening flagged as highest-risk requirement.
- `.planning/PROJECT.md` — core value, constraints (pure Markdown, no code), Key Decisions table.

### Tertiary (LOW confidence)

None for this phase. All findings are derived from fetched primary sources or project documents authored in the current session.

---

## Metadata

**Confidence breakdown:**
- Baseline analysis (original skill): HIGH — fetched from GitHub directly
- Gap analysis (what is missing): HIGH — direct comparison of original to requirements
- Deliverable structure: HIGH — derived from locked decisions in CONTEXT.md
- Authoring patterns and examples: HIGH — derived from locked decisions and research documents
- Test-run subject candidates: MEDIUM — reasoning about which real design questions are genuinely unresolved; final choice is Claude's discretion

**Research date:** 2026-05-16
**Valid until:** This research has no time-sensitive claims. Valid until the original skill's SKILL.md changes materially (the baseline analysis would need updating) or until CONTEXT.md decisions change.
