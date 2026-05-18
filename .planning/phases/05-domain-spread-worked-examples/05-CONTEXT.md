# Phase 5: Domain-Spread Worked Examples - Context

**Gathered:** 2026-05-17
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase authors four complete worked examples in `first-principles-thinking/examples/`,
one per domain (software/systems, product/business, personal/general, science/engineering).
Each example is a full first-principles analysis written in the standardized six-section
output format, showing at least one abandoned reasoning step, and passing the validation
rubric gate. The four example stub files already exist (3-line placeholders); this phase
fills them in.

**Fixed by ROADMAP / REQUIREMENTS (not open for discussion):**
- The four domains and the four `examples/*.md` filenames.
- The six-section output format (`references/output-template.md`).
- The validation rubric the examples must pass (`references/validation-rubric.md`).
- The "show ≥1 abandoned/dead-end reasoning step" rule (Success Criterion 2).
- Requirements EX-01 (software), EX-02 (product/business), EX-03 (personal/general),
  EX-04 (science/engineering).

Out of scope: wiring the examples into `SKILL.md`'s navigation map and cross-reference
checking — that is Phase 6.

</domain>

<decisions>
## Implementation Decisions

### Problem Selection
- **D-01:** Claude proposes the concrete problems (user retained veto). The slate below
  is **locked** — one domain-authentic problem per example:
  - **Software/systems (EX-01):** A team wants to break a monolith into microservices to
    fix slow deploys — is that the right move?
  - **Product/business (EX-02):** Should a SaaS product add a free tier to grow adoption?
  - **Personal/general (EX-03):** Should I take a higher-paying job that requires relocating?
  - **Science/engineering (EX-04):** How should an off-grid solar install be sized
    (battery and panels)?
- **D-02:** Problems lean **realistic and domain-authentic** — the kind of problem a real
  practitioner in that domain would actually face — not the everyday/non-technical register.
  Note: Phase 4's companion-tool mini-examples deliberately used everyday scenarios
  specifically to avoid preempting these four domains (Phase 4 D-04), so there is no
  conflict — the worked examples are free to be domain-authentic. Domain facts stay
  illustrative (per PROJECT.md Out of Scope: "domain facts stay illustrative, not
  authoritative") — the science/engineering example must not require a physics primer
  to follow; unverifiable domain facts go through the `GT-N?` mechanism.

### Differentiation (Success Criterion 4 — no two examples may be the same skeleton)
- **D-03:** Each example makes a **different part of the methodology its deepest section**:
  - **Microservices (EX-01):** Phase 1 **Essence** re-framing (symptom vs cause — deploy
    speed is not an architecture problem) **plus a large Abandoned Reasoning section** —
    the wrong path (just split the monolith) is the centerpiece of the example.
  - **Free tier (EX-02):** Phase 2 **Challenge Assumptions** — the Classified Assumptions
    Table carries the analysis ("free tier → conversion" is an untested belief); the
    dead-end is an analogy-ban violation ("competitors all have a free tier").
  - **Relocation (EX-03):** Phase 1 **Essence** again, but a *different re-framing move*:
    stated goal vs real goal (the decision is not actually about the compensation delta).
    Lighter derivation chains, human stakes. EX-01 and EX-03 sharing Phase 1 emphasis is
    intentional and acceptable because they demonstrate two distinct re-framing operations
    — symptom→cause vs stated-goal→real-goal.
  - **Solar sizing (EX-04):** Phases 3–4 **Ground Truths + Derivation Chains** —
    quantitative chains anchored in physical-law ground truths — **plus Phase 5**
    confidence caveats: the daily energy load is genuinely an untested belief, carried as
    a `GT-N?` input, so at least one chain ends MEDIUM/LOW with a stated verification path.
- **D-04:** Structural variety is **natural, not contrived**. Differences in chain count,
  assumptions-table size, and dead-end depth fall out of the problems themselves. Do **not**
  manufacture edge-case demonstrations (e.g. do not force a "Nothing material here" escape
  valve, or a competing-conclusions structure, just to show the format's range). The escape
  valve and `GT-N?` appear only where the specific problem genuinely calls for them — the
  `GT-N?` in EX-04 qualifies because the solar problem authentically has an unverifiable
  input, not because EX-04 was assigned to "demonstrate `GT-N?`".

### Companion-Tool Integration
- **D-05:** The worked examples stay **pure 5-phase**. No example invokes or demonstrates
  5-Whys, pre-mortem, or trade-off analysis. Each example demonstrates exactly one thing —
  the six-section output format applied end-to-end. The companion tools are already
  illustrated by their own Phase 4 mini-examples; adding a second procedure layer inside
  the worked examples would dilute their focus.

### Depth & Rubric Scoring
- **D-06:** **No fixed length target.** Each example's length follows its problem and its
  designated emphasis (D-03); the planner sets a rough length band per example. A worked
  example should be thorough enough to imitate, not padded.
- **D-07:** Each example file is a **pure six-section analysis** — exactly what
  `output-template.md` produces — with **no inline validation-rubric verdict blocks**. The
  file IS a clean specimen of the output format. Passing the rubric gate (Success
  Criterion 3) is checked at verification time against `references/validation-rubric.md`;
  the scoring is not baked into the example file.

### Claude's Discretion
Consistent with the decisions above, the researcher and planner decide:
- The specific framing, scenario details, and numbers within each locked problem (D-01) —
  e.g. the exact monolith/team setup, the SaaS product specifics, the relocation
  particulars, the solar load/site parameters.
- The exact content of each example's six sections: which assumptions populate each
  Assumptions Table, which facts become ground truths, the derivation chains, and the
  specific dead-end(s) recorded in Abandoned Reasoning.
- The precise per-example length band (D-06).
- How many derivation chains and how many abandoned-reasoning entries each example carries
  (≥1 dead-end is the floor per Success Criterion 2).
- Whether examples are authored one-per-plan or grouped, and the wave/dependency structure.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Output format the examples must follow
- `first-principles-thinking/references/output-template.md` — the full annotated
  six-section output template (Problem Essence, Assumptions Table, Ground Truths,
  Derivation Chains, Abandoned Reasoning, Conclusion). Every example must conform to this
  strict-shape document exactly — fixed section order, all six sections present.

### Rubric the examples must pass
- `first-principles-thinking/references/validation-rubric.md` — the 6-criterion scoring
  instrument. Each example must clear the gate (no criterion Absent) and the hand-wavy cap
  (at most one criterion Hand-wavy) per Success Criterion 3.

### Methodology being demonstrated
- `first-principles-thinking/SKILL.md` — the five-phase methodology spine and the
  artifact chain (Essence Statement → Classified Assumptions Table → Ground Truths list →
  Derivation Chains → signed-off analysis). The examples are demonstrations of this
  methodology applied; authoring them requires understanding the per-phase operations,
  the four-type assumption scheme, and the `GT-N?` / confidence-caveat rules (D-07 in
  SKILL.md).

### Example stub files to fill in
- `first-principles-thinking/examples/software-systems.md` — EX-01 stub
- `first-principles-thinking/examples/product-business.md` — EX-02 stub
- `first-principles-thinking/examples/personal-general.md` — EX-03 stub
- `first-principles-thinking/examples/science-engineering.md` — EX-04 stub

### Prior-phase context worth honoring
- `.planning/phases/04-companion-tool-references/04-CONTEXT.md` — Phase 4 D-04 explains
  why the companion-tool mini-examples used everyday scenarios (to avoid preempting these
  four domains). Confirms the worked examples may be domain-authentic without overlap.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- The four `examples/*.md` files already exist as 3-line stubs with a one-line description
  each — the planner fills the bodies in place, keeping the existing filenames and the
  `# Worked Example: [Domain]` H1 already present.
- `output-template.md` is itself a section-by-section author's guide — the planner can
  treat its prescriptions as the authoring checklist for each example.
- `validation-rubric.md` Criterion descriptors double as a quality target — authoring an
  example to score Rigorous on all six criteria is the concrete bar.

### Established Patterns
- Pure-Markdown skill, no executable code (CLAUDE.md constraint). Examples are Markdown only.
- UTF-8, LF, forward-slash relative paths in any cross-references.
- Prior phases (1–4) used numbered decision IDs and "why" rationale in their reference
  files; the examples themselves follow `output-template.md`'s shape rather than that
  convention, but the same rigor standard applies.

### Integration Points
- Examples are Layer-3 files read on-demand. Phase 6 wires them into the `SKILL.md`
  navigation map — this phase only authors the files; it does not touch `SKILL.md`.

</code_context>

<specifics>
## Specific Ideas

- The four locked problems (D-01) are the concrete specifics this phase is built around.
- EX-01's value is largely in its Abandoned Reasoning section — the example should read as
  an analysis that *nearly* reached the wrong conclusion (microservices) before the
  methodology caught it.
- EX-04 is the designated home for an authentic `GT-N?` input and a MEDIUM/LOW-confidence
  chain — because the off-grid solar problem genuinely has an unverifiable input (real
  daily energy load), not as a contrived format demonstration.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope. (Note: a self-referential "the skill
analyzing its own design" example is tracked separately as v2 requirement META-01 in
REQUIREMENTS.md and is not part of this phase.)

</deferred>

---

*Phase: 05-domain-spread-worked-examples*
*Context gathered: 2026-05-17*
