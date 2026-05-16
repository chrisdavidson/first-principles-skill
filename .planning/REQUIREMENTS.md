# Requirements: First Principles Thinking Skill (Enhanced)

**Defined:** 2026-05-16
**Core Value:** When Claude applies this skill, every conclusion traces back to a verified ground truth and every assumption is explicitly challenged — reasoning a skeptic cannot dismiss as hand-waving.

## v1 Requirements

Requirements for the enhanced single skill (pure Markdown). Each maps to roadmap phases.

### Skill Foundation

- [ ] **FOUND-01**: `SKILL.md` has valid YAML frontmatter (`name`, `description`, `metadata.version`) conforming to the Agent Skills schema
- [ ] **FOUND-02**: The `description` field triggers reliably — states what the skill does and when to use it, with explicit English and Chinese trigger phrases, within the budget limit
- [ ] **FOUND-03**: The `SKILL.md` body stays under 500 lines, with depth content pushed to `references/` and `examples/`
- [ ] **FOUND-04**: Every `references/` and `examples/` file links one level deep directly from `SKILL.md`
- [ ] **FOUND-05**: The skill installs by copy or symlink into a Claude Code skills directory with no build step

### Methodology

- [x] **METH-01**: Each of the 5 phases has explicit entry and exit criteria stating when the phase is done
- [x] **METH-02**: Each phase names the concrete artifact it must produce before the next phase begins
- [x] **METH-03**: The Challenge-Assumptions phase includes an assumption-classification scheme (physical law / current constraint / convention / untested belief)
- [x] **METH-04**: The standardized output format is a strict template with required sections, including the assumptions table
- [x] **METH-05**: The output format requires an explicit conclusion-to-ground-truth traceability map
- [x] **METH-06**: Methodology instructions state the rationale behind each rule rather than bare imperatives

### Validation Rubric

- [ ] **VALID-01**: `references/validation-rubric.md` defines 6-8 analytic criteria covering the 5 phases and traceability
- [ ] **VALID-02**: Each rubric criterion has 3-4 named levels, each with a concrete observable descriptor
- [ ] **VALID-03**: The rubric uses a gate scoring model — any criterion at the lowest band fails the analysis and forces revision
- [ ] **VALID-04**: The rubric requires Claude to quote the specific span of its analysis that satisfies or fails each criterion
- [ ] **VALID-05**: `SKILL.md` instructs Claude to apply the rubric as a validator → fix → repeat feedback loop

### Companion Tools

- [ ] **TOOL-01**: `references/5-whys.md` is a usable component — when-to-use, branching procedure with test-based stop criterion, mini-example, failure modes, and handoff to the 5-phase spine
- [ ] **TOOL-02**: `references/pre-mortem.md` is a usable component — prospective-hindsight framing, procedure, mini-example, failure modes, and handoff to Phase 5 (Validate)
- [ ] **TOOL-03**: `references/trade-off-analysis.md` is a usable component — weighted-criteria-before-scoring procedure, mini-example, failure modes, and handoff to the 5-phase spine
- [ ] **TOOL-04**: `SKILL.md` briefly describes each companion tool, says when to reach for it, and links to its reference file

### Worked Examples

- [ ] **EX-01**: `examples/` contains a software/systems worked example that follows the output format and shows at least one abandoned reasoning step
- [ ] **EX-02**: `examples/` contains a product/business worked example that follows the output format and shows a dead-end
- [ ] **EX-03**: `examples/` contains a personal/general worked example that follows the output format and shows a dead-end
- [ ] **EX-04**: `examples/` contains a science/engineering worked example that follows the output format and shows a dead-end

### Packaging

- [ ] **PKG-01**: `README.md` describes the skill, its methodology, and installation for human readers
- [ ] **PKG-02**: All cross-references between `SKILL.md`, `references/`, and `examples/` resolve correctly
- [ ] **PKG-03**: The skill passes Agent Skills schema validation

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Methodology Depth

- **META-01**: A self-application / dogfooding reference showing the skill analyzing its own design
- **META-02**: Expanded assumption-classification taxonomy, refined after observing real usage
- **META-03**: Additional within-domain examples where one example proves insufficient

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Splitting into multiple separate skills | Explicitly milestone 2 — v1 stays a single skill; splitting now fragments triggering and duplicates the methodology spine |
| Executable validation script (scripted scoring) | Violates the pure-Markdown v1 constraint; a script is a separate deliverable with its own testing burden — a possible later milestone |
| Python skill-builder program | Explicitly milestone 3 — the `uv` scaffold stays untouched as that foundation |
| Generic critical-thinking content (fallacy lists, bias catalogs, debate tactics) | Scope creep — not first-principles thinking; adds tokens Claude already has |
| Domain-specific deep content (e.g. a rocket-physics primer) | This is a methodology skill, not a domain skill — domain facts stay illustrative, not authoritative |
| Exhaustive example library (10+ examples) | Diminishing returns and maintenance bloat past one strong example per domain |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| FOUND-01 | Phase 2 | Pending |
| FOUND-02 | Phase 2 | Pending |
| FOUND-03 | Phase 2 | Pending |
| FOUND-04 | Phase 6 | Pending |
| FOUND-05 | Phase 6 | Pending |
| METH-01 | Phase 1 | Complete |
| METH-02 | Phase 1 | Complete |
| METH-03 | Phase 1 | Complete |
| METH-04 | Phase 1 | Complete |
| METH-05 | Phase 1 | Complete |
| METH-06 | Phase 1 | Complete |
| VALID-01 | Phase 3 | Pending |
| VALID-02 | Phase 3 | Pending |
| VALID-03 | Phase 3 | Pending |
| VALID-04 | Phase 3 | Pending |
| VALID-05 | Phase 2 | Pending |
| TOOL-01 | Phase 4 | Pending |
| TOOL-02 | Phase 4 | Pending |
| TOOL-03 | Phase 4 | Pending |
| TOOL-04 | Phase 6 | Pending |
| EX-01 | Phase 5 | Pending |
| EX-02 | Phase 5 | Pending |
| EX-03 | Phase 5 | Pending |
| EX-04 | Phase 5 | Pending |
| PKG-01 | Phase 6 | Pending |
| PKG-02 | Phase 6 | Pending |
| PKG-03 | Phase 6 | Pending |

**Coverage:**
- v1 requirements: 27 total
- Mapped to phases: 27 ✓
- Unmapped: 0 ✓

---
*Requirements defined: 2026-05-16*
*Last updated: 2026-05-16 after roadmap creation*
