# Phase 1: Sharpen the Methodology and Harden the Output Format - Context

**Gathered:** 2026-05-16
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase authors the **content spine** of the skill — the sharpened 5-phase
first-principles methodology and the hardened standardized output template. It
produces, as Markdown content:

- The 5-phase procedure (Identify Essence → Challenge Assumptions → Establish
  Ground Truths → Reason Upward → Validate), each phase with a concrete
  operation, a named output artifact, and explicit entry/exit criteria.
- The assumption-classification scheme (physical law / current constraint /
  convention / untested belief) with prescribed treatments.
- The strict standardized output template — required sections including the
  assumptions table and a conclusion-to-ground-truth traceability map.
- A test-run of the methodology on a real problem, demonstrating a full trace.

Phase 2 later embeds this content into `SKILL.md`. Phase 1 produces the
methodology itself — it does **not** create `SKILL.md`, frontmatter, the
validation rubric, companion tools, or shipped `examples/` files. The
methodology **ports and sharpens** the original `first-principles-skill`; it
does not start from scratch.

</domain>

<decisions>
## Implementation Decisions

### Output Template Strictness
- **D-01:** The output template uses **strict shape, honest depth**. All
  sections must be present and in fixed order, but any section may be marked
  `Nothing material here — [reason]` when justified. Rationale: prevents the
  box-ticking failure mode (research Pitfall 2) where headings are filled but
  no real reasoning happened, while keeping the auditable shape intact.
- **D-02:** The conclusion-to-ground-truth traceability map takes the form of
  **derivation chains** — each conclusion shown as a step chain
  (`GT-1 + GT-2 → intermediate → conclusion`), not a flat conclusion→GT-ID
  linking table. Ground truths get stable IDs. Note for planning: chains are
  verbose by nature — the template/instructions should keep them disciplined
  (one chain per conclusion, no redundant restatement).
- **D-03:** The output template includes a **dedicated "Abandoned Reasoning"
  (Dead Ends) section** where discarded paths and why-they-failed are recorded.
  This gives Phase 5's required dead-end demonstrations a natural home and makes
  abandoned reasoning auditable rather than hidden.

### Reason Upward — High-Freedom Phase Design
- **D-04:** Reason Upward is **free but self-documenting**: no prescribed
  sub-steps for *how* to reason upward, but Claude must narrate its own
  reasoning path as it goes (what it tried, what it built on). Freedom is in
  the method; mandatory transparency replaces prescribed structure. This is the
  deliberate guard against over-prescription required by Success Criterion 5.
- **D-05:** Reason Upward's exit criterion is **both conditions**: the
  problem's core question is answered AND every conclusion offered has a
  complete derivation chain back to named ground truths. Nothing partial passes
  to the Validate phase.

### Assumption Classification — Treatment Rules
- **D-06:** The four assumption categories carry **prescribed actions plus a
  stakes-escalation rule**:
  - physical law → accept as a ground-truth candidate
  - current constraint → record what would change it (expiry conditions)
  - convention → must be explicitly challenged before use
  - untested belief → must be verified or flagged unverified
  - **Escalation:** the higher the stakes of the conclusion resting on an
    assumption, the more it must be pushed down toward physical law or verified
    ground truth. Classification drives the method, it is not just labelling.
- **D-07:** An unverified assumption **is allowed in a derivation chain but
  must be visibly flagged** (e.g. `GT-3?: unverified`). Any conclusion
  depending on it inherits an explicit confidence caveat. This keeps the
  methodology honest about uncertainty without forcing analysis to a halt or
  manufacturing false precision — the skeptic still sees exactly where the soft
  spot is.

### Methodology Test-Run
- **D-08:** The Success-Criterion-4 test-run **dogfoods a real open project
  design decision** from this skill build (e.g. a genuine unresolved design
  choice in the methodology/skill itself), not a toy or neutral problem. This
  directly serves PROJECT.md's stated dogfooding goal and proves the method on
  a real, non-trivial problem.
- **D-09:** The test-run is **kept as a working draft** (in `.planning/`, not
  shipped) — a reference Phase 5 can later polish into one of its four worked
  examples. It is a verification artifact for this phase; it must **not** ship
  as an `examples/` file from Phase 1 (that would pull Phase 5's scope forward).

### Claude's Discretion
Remaining HOW details are left to the researcher and planner, consistent with
the decisions above:
- Exact wording of each phase's entry/exit criteria and the precise names of
  each phase's output artifact.
- How the per-phase artifacts accumulate into the final output document
  (the template *is* effectively the cumulative document).
- The phrasing of each phase's rationale statement (METH-06 requires every
  rule to state its rationale, not a bare imperative).
- The exact section list and ordering of the output template (beyond the
  mandated assumptions table, derivation-chain traceability map, and Abandoned
  Reasoning section).
- Which specific open project design decision is chosen as the test-run subject.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and requirements
- `.planning/ROADMAP.md` §"Phase 1" — phase goal, the 6 requirements
  (METH-01…METH-06), and the 5 success criteria this phase must satisfy.
- `.planning/REQUIREMENTS.md` §"Methodology" — full text of METH-01 through
  METH-06.
- `.planning/PROJECT.md` — core value, constraints (pure Markdown, no code),
  and the Key Decisions table (enhance-don't-rewrite; dogfood the methodology).

### Project research (consumed for Phase 1 design)
- `.planning/research/SUMMARY.md` — executive summary; the Phase 1 rationale
  and the abstract-vs-prescriptive risk framing.
- `.planning/research/PITFALLS.md` — Pitfall 1 (methodology too abstract) and
  Pitfall 2 (too prescriptive / box-ticking) directly shape this phase's
  design; D-01 and D-04 are the mitigations.
- `.planning/research/FEATURES.md` — methodology feature expectations
  (entry/exit criteria, named artifacts, traceability).
- `.planning/research/ARCHITECTURE.md` — the 3-layer skill structure;
  confirms Phase 1 produces content, Phase 2 places it.

### Source skill (external — researcher should fetch)
- `github.com/chrisdavidson/first-principles-skill` — the original skill being
  ported and sharpened: the existing 5-phase methodology, the original
  standardized output format, and `references/`/`examples/` content. Phase 1
  enhances this baseline rather than authoring fresh. The researcher should
  retrieve and read the original `SKILL.md` and its methodology section.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None in this repository. The repo currently contains only planning docs
  (`.planning/`), `CLAUDE.md`, and an untouched `uv` Python scaffold
  (`main.py`, `pyproject.toml`, `.python-version`, `README.md`).
- The methodology content to sharpen lives in the **external** original repo
  (`github.com/chrisdavidson/first-principles-skill`) — see Canonical
  References.

### Established Patterns
- No skill files (`SKILL.md`, `references/`, `examples/`) exist yet — Phase 1
  is the first content authored.

### Integration Points
- Phase 1's methodology content is consumed by Phase 2 (embedded as the
  resident procedure in `SKILL.md`) and calibrated against by Phase 3 (the
  validation rubric scores analyses produced in this output format). The
  template's section shape (D-01/D-02/D-03) is the contract those phases build
  on.

</code_context>

<specifics>
## Specific Ideas

- The `uv` Python scaffold (`main.py`, `pyproject.toml`) must remain
  untouched — it is reserved for milestone 3 and is explicitly out of scope.
- The test-run (D-08/D-09) should pick a *genuine* unresolved design question
  from the skill build so the dogfooding is real, not staged.
- Derivation chains (D-02) are the user's deliberate choice over a simpler
  linking table — they show reasoning *steps*, not just endpoints. Authoring
  should make the richer form readable, not let it sprawl.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope. Scope-adjacent items
(the validation rubric, companion tools, the four shipped worked examples,
`SKILL.md` and its frontmatter) belong to Phases 2–6 and were not pulled
forward. The Phase 1 test-run is explicitly kept as a draft for Phase 5 to
polish (D-09) rather than shipped here.

</deferred>

---

*Phase: 1-Sharpen the Methodology and Harden the Output Format*
*Context gathered: 2026-05-16*
