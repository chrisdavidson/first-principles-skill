# Roadmap: First Principles Thinking Skill (Enhanced)

## Overview

This milestone delivers the enhanced v1 single skill — a pure-Markdown Claude Code skill that gives Claude a rigorous, auditable first-principles methodology. The journey is a content-build dependency chain, not a software build: first sharpen the 5-phase methodology and harden the output format (the spine everything else calibrates against), then construct the `SKILL.md` skeleton and navigation map, then build the validation rubric (which must exist before examples so examples can be authored to pass it), then the three companion tool references, then four domain-spread worked examples, and finally wire every Layer 3 file into `SKILL.md`, write the human-facing README, and validate the whole skill against the Agent Skills schema. Each phase produces a coherent, verifiable artifact and unblocks the next.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Sharpen the Methodology and Harden the Output Format** - Tighten the 5-phase process with entry/exit criteria, per-phase artifacts, assumption classification, and a strict traceable output template (completed 2026-05-16)
- [x] **Phase 2: SKILL.md Skeleton and Frontmatter** - Build the discoverable, lean SKILL.md body with valid frontmatter, the resident methodology, and the navigation map shape (completed 2026-05-17)
- [x] **Phase 3: Validation Rubric** - Author a falsifiable, evidence-quoting analytic rubric with gate scoring that catches a deliberately weak analysis (completed 2026-05-17)
- [ ] **Phase 4: Companion Tool References** - Build 5-Whys, pre-mortem, and trade-off analysis as self-contained, usable reference components
- [ ] **Phase 5: Domain-Spread Worked Examples** - Produce four worked examples (software, product, personal, science) each showing a real dead-end and passing the rubric
- [ ] **Phase 6: Final SKILL.md Wiring, README, and Validation** - Wire every Layer 3 file into the nav map, write the human README, and pass schema validation

## Phase Details

### Phase 1: Sharpen the Methodology and Harden the Output Format

**Goal**: The 5-phase first-principles methodology is operational — every phase has a concrete operation, a named output artifact, and explicit entry/exit criteria — and the standardized output template demands an auditable conclusion-to-ground-truth trace.
**Depends on**: Nothing (first phase)
**Requirements**: METH-01, METH-02, METH-03, METH-04, METH-05, METH-06
**Success Criteria** (what must be TRUE):

  1. Each of the 5 phases (Identify Essence, Challenge Assumptions, Establish Ground Truths, Reason Upward, Validate) states an explicit "this phase is done when X" exit criterion and names the concrete artifact it must produce.
  2. The Challenge-Assumptions phase includes an assumption-classification scheme distinguishing physical law, current constraint, convention, and untested belief.
  3. The standardized output template is a strict-shape document with required sections including an assumptions table, and it requires an explicit conclusion-to-ground-truth traceability map.
  4. A test run of the methodology on a sample problem produces an analysis where every conclusion visibly traces back to a named ground truth.
  5. Each phase instruction states the rationale for its rule rather than a bare imperative, and at least one phase (Reason Upward) is deliberately left high-freedom.

**Plans**: 3 plans
Plans:
**Wave 1**

- [x] 01-01-PLAN.md — Author methodology.md: the sharpened 5-phase procedure with entry/exit criteria, named artifacts, the 4-type assumption scheme, and rationale statements
- [x] 01-02-PLAN.md — Author output-template.md: the strict-shape six-section output template with the classified assumptions table and per-conclusion derivation chains

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 01-03-PLAN.md — Author test-run-draft.md: a dogfooding run of the methodology on a genuinely unresolved design question, proving end-to-end traceability

### Phase 2: SKILL.md Skeleton and Frontmatter

**Goal**: A loadable, discoverable `SKILL.md` exists — valid frontmatter that triggers reliably, the sharpened methodology resident as standing instructions, a lean body under 500 lines, and a navigation map whose named slots later phases fill.
**Depends on**: Phase 1
**Requirements**: FOUND-01, FOUND-02, FOUND-03, VALID-05
**Success Criteria** (what must be TRUE):

  1. `SKILL.md` has valid YAML frontmatter (`name`, `description`, `metadata.version`) conforming to the Agent Skills schema, and the skill loads without error.
  2. The `description` field states what the skill does and when to use it, includes explicit English trigger phrases, and fits within the character budget without truncation.
  3. The `SKILL.md` body is under 500 lines, with the methodology procedure resident and depth content deferred to placeholder pointers for `references/` and `examples/`.
  4. `SKILL.md` instructs Claude to apply the validation rubric as a validator-fix-repeat feedback loop before presenting conclusions.

**Plans**: 2 plans
Plans:
**Wave 1**

- [x] 02-01-PLAN.md — Build the Layer-3 scaffold: full output-template.md plus eight references/ and examples/ stub files so every nav-map link resolves

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 02-02-PLAN.md — Author SKILL.md: frontmatter, the resident 5-phase methodology, the condensed output skeleton, the VALID-05 validator-fix-repeat instruction, and the navigation map
**UI hint**: yes

### Phase 3: Validation Rubric

**Goal**: `references/validation-rubric.md` exists as a falsifiable self-check — analytic criteria with named, observable levels and gate scoring — that demonstrably catches hand-waving rather than certifying it.
**Depends on**: Phase 1
**Requirements**: VALID-01, VALID-02, VALID-03, VALID-04
**Success Criteria** (what must be TRUE):

  1. `references/validation-rubric.md` defines 6-8 analytic criteria covering all 5 phases and conclusion-to-ground-truth traceability.
  2. Each criterion has 3-4 named levels (e.g. Rigorous / Adequate / Hand-wavy / Absent), each with a concrete observable descriptor rather than an adjective.
  3. The rubric uses a gate scoring model — any criterion scored at its lowest band fails the whole analysis and forces revision.
  4. Applying the rubric to a deliberately weak (hand-wavy) sample analysis produces a fail, and each criterion verdict quotes the specific span of the analysis that satisfies or fails it.

**Plans**: 2 plans
Plans:
**Wave 1**

- [x] 03-01-PLAN.md — Author validation-rubric.md: the preamble, gate + hand-wavy-cap scoring model, verdict-block format, and 6 analytic criteria each with a shared 4-level observable-descriptor scale
**Wave 2** *(blocked on Wave 1 completion)*

- [x] 03-02-PLAN.md — Author 03-weak-sample.md: a deliberately-weak analysis and its rubric scoring run, demonstrating an overall fail with per-criterion evidence-quoting verdicts

### Phase 4: Companion Tool References

**Goal**: Three companion thinking tools — 5-Whys, pre-mortem, and trade-off analysis — exist as self-contained `references/` components, each fully usable as a sub-procedure and promotion-ready for the future milestone-2 split.
**Depends on**: Phase 1
**Requirements**: TOOL-01, TOOL-02, TOOL-03
**Success Criteria** (what must be TRUE):

  1. `references/five-whys.md` is a usable component with when-to-use, a branching procedure with a test-based stop criterion, a mini-example, failure modes, and an explicit handoff to the 5-phase spine.
  2. `references/pre-mortem.md` is a usable component with prospective-hindsight framing, a procedure, a mini-example, failure modes, and an explicit handoff to Phase 5 (Validate).
  3. `references/trade-off-analysis.md` is a usable component with a weighted-criteria-before-scoring procedure, a mini-example, failure modes, and a handoff to the 5-phase spine.
  4. No companion tool file carries its own YAML frontmatter or trigger description — each is a reference component, not a separate skill.

**Plans**: TBD

### Phase 5: Domain-Spread Worked Examples

**Goal**: Four worked examples exist in `examples/`, one per domain, each applying the methodology in the standardized output format, each exercising the method differently, and each showing at least one abandoned reasoning step.
**Depends on**: Phase 2, Phase 3
**Requirements**: EX-01, EX-02, EX-03, EX-04
**Success Criteria** (what must be TRUE):

  1. `examples/` contains four worked examples covering software/systems, product/business, personal/general, and science/engineering, each following the standardized output format.
  2. Each example shows at least one abandoned or dead-end reasoning step, not a clean march to the answer.
  3. Each example, when scored against the validation rubric, passes the gate (no criterion at the lowest band).
  4. The four examples differ in structure and methodology emphasis — no two are the same skeleton with domain nouns swapped.

**Plans**: TBD

### Phase 6: Final SKILL.md Wiring, README, and Validation

**Goal**: The skill is complete and shippable — every Layer 3 file is wired into the `SKILL.md` navigation map one level deep, companion tools are described and linked, a human-facing README documents copy/symlink install, and the skill passes Agent Skills schema validation.
**Depends on**: Phase 4, Phase 5
**Requirements**: FOUND-04, FOUND-05, TOOL-04, PKG-01, PKG-02, PKG-03
**Success Criteria** (what must be TRUE):

  1. Every `references/` and `examples/` file links one level deep directly from `SKILL.md`, and `SKILL.md` briefly describes each companion tool and says when to reach for it.
  2. All cross-references between `SKILL.md`, `references/`, and `examples/` resolve correctly with forward-slash paths.
  3. The skill installs by copy or symlink into a Claude Code skills directory with no build step, and the directory name matches the frontmatter `name`.
  4. `README.md` describes the skill, its methodology, and installation for human readers.
  5. The skill passes Agent Skills schema validation.

**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Sharpen the Methodology and Harden the Output Format | 3/3 | Complete   | 2026-05-16 |
| 2. SKILL.md Skeleton and Frontmatter | 2/2 | Complete   | 2026-05-17 |
| 3. Validation Rubric | 2/2 | Complete   | 2026-05-17 |
| 4. Companion Tool References | 0/TBD | Not started | - |
| 5. Domain-Spread Worked Examples | 0/TBD | Not started | - |
| 6. Final SKILL.md Wiring, README, and Validation | 0/TBD | Not started | - |
