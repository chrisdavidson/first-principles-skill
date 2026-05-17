# Phase 3: Validation Rubric - Context

**Gathered:** 2026-05-17
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase authors **`first-principles-thinking/references/validation-rubric.md`** —
replacing the current descriptive stub with a real, falsifiable analytic rubric.
It produces, as Markdown content:

- An analytic rubric of **6 criteria** covering all 5 methodology phases plus
  conclusion-to-ground-truth traceability.
- A **shared 4-level scale** applied to every criterion, each level carrying a
  concrete observable descriptor (not an adjective).
- A **gate scoring model** with an additional **hand-wavy cap** — the lowest
  band fails the analysis outright; too many second-lowest scores also force
  revision.
- An **evidence-quoting verdict format** — each criterion verdict quotes the
  span of the analysis it scores, names the band, and justifies the score.
- A **deliberately-weak sample analysis** scored against the rubric to prove it
  produces a fail (Success Criterion 4) — authored as a non-shipped `.planning/`
  verification artifact.

The rubric calibrates against the **fixed output contract** already shipped in
Phase 2: the six-section output format, derivation chains, the `GT-N?`
unverified notation, the Abandoned Reasoning section, and the honest-depth
escape valve.

Phase 3 does **not** re-author the validator → fix → repeat loop — that
instruction already lives resident in `SKILL.md` (Phase 2, D-09) and links to
this file. Phase 3 only authors the criteria the loop consumes. It does **not**
build the companion tools (Phase 4), the four shipped worked examples (Phase 5),
or do the final nav-map audit / README / schema validation (Phase 6).

</domain>

<decisions>
## Implementation Decisions

### Criterion Set & Coverage
- **D-01:** The rubric uses **exactly 6 criteria** — one per methodology phase
  (Identify Essence, Challenge Assumptions, Establish Ground Truths, Reason
  Upward, Validate) plus one for conclusion-to-ground-truth **traceability**.
  This is the minimum allowed by VALID-01 (6–8). The "carve out rigor-critical
  sub-features into their own criterion" option was **rejected** — the
  4-type assumption scheme, dead-end honesty, and the unverified-flag/
  confidence-caveat discipline are **folded into the relevant per-phase
  criterion** (e.g. classification quality lives inside the Challenge
  Assumptions criterion; dead-end honesty inside the Reason Upward criterion).
  Rationale: a clean one-criterion-per-phase mapping; each criterion does more
  work but the rubric stays legible.

### Gate Scoring Model
- **D-02:** The rubric uses a **gate + hand-wavy cap**, not a pure single-band
  gate. Two failure conditions:
  1. **Gate** — any criterion scored at the lowest band fails the whole
     analysis and forces revision (VALID-03, mandatory).
  2. **Hand-wavy cap** — too many criteria at the *second-lowest* band also
     fails the analysis. This catches the "mediocre everywhere, terrible
     nowhere" analysis that a pure single-band gate would pass.
- **D-05:** The **exact cap threshold** (how many second-lowest scores trip
  the cap, out of 6) is **deferred to the phase researcher**. STATE.md already
  flags an analytic-rubric-design research pass; the researcher must justify
  the number rather than picking it arbitrarily. CONTEXT.md locks that a cap
  *exists* and what it must catch — research sets the value.

### Level Scale
- **D-03:** **One shared 4-level scale** is applied uniformly to all 6
  criteria. Per-criterion tailored level vocabularies were rejected — a single
  consistent band vocabulary keeps scoring and the gate/cap rule simple. The
  level *descriptors* remain criterion-specific and must be concrete observable
  statements (VALID-02), but the band *names* are shared.
- **D-06:** The **band labels themselves are left to the planner.** The 4-level
  structure, the gate band (lowest), and the capped band (second-lowest) are
  locked; the planner chooses the final label words while authoring. The stub's
  proposal (`Rigorous / Adequate / Hand-wavy / Absent`) is a starting point,
  not a locked decision.

### Evidence-Quoting & Verdict Form
- **D-07:** Scored output uses a **per-criterion verdict block** — each of the
  6 criteria gets its own self-contained block containing: the **quoted span**
  of the analysis being scored, the **band** assigned, and a **one-line
  justification** tying the quote to that band's descriptor. A single
  consolidated scoring table was rejected — verdict blocks make every verdict
  unmissable and auditable on its own.
- **D-09:** When a criterion scores the **gate-fail band** there is often no
  span to quote because the section or artifact is simply missing. In that case
  the verdict **cites the gap explicitly** — it names *what* is missing and
  *where* it should have appeared (e.g. "no derivation chain exists for the
  Conclusion's main claim"). For a fail verdict, the documented absence *is*
  the evidence; the rubric does not force a quote of unrelated nearby content.

### Box-Ticking Defense (honest-depth escape valve)
- **D-08:** The rubric **actively polices the honest-depth escape valve.** A
  section legitimately marked `Nothing material here — [reason]` scores the top
  band **only if** the rubric verdict confirms the stated reason is genuine
  (the problem really had no dead ends / no relevant assumptions / etc.). A
  lazy or generic "Nothing material here" is scored as hand-wavy or as a fail.
  The escape valve is not a free pass — the rubric is the mechanism that stops
  it being abused to skip real reasoning.

### Fail Demonstration Artifact
- **D-04:** The **deliberately-weak sample analysis** required by Success
  Criterion 4 lives as a **separate, non-shipped `.planning/` verification
  artifact** — not embedded in the shipped `validation-rubric.md` and not a new
  shipped `examples/` file. This mirrors Phase 1's `test-run-draft.md` pattern
  (D-09 there): a verification artifact proves the phase, without bloating the
  shipped rubric or adding a file outside the current nav map. The shipped
  rubric still demonstrates the verdict-block format concisely, but the full
  weak-analysis fail run is the verification draft.
  - **Note for research/planning:** Phase 1's `test-run-draft.md` is a
    *passing-quality* analysis in the exact output format — a natural base to
    deliberately weaken (drop chains, skip classification, abuse the escape
    valve) to construct the weak sample.

### Claude's Discretion
Consistent with the decisions above, the researcher and planner decide:
- The exact hand-wavy cap threshold (D-05) — research must justify it.
- The final 4 band labels (D-06).
- The wording of each criterion and its 4 observable level descriptors.
- Criterion ordering within the rubric (e.g. mirror the 5-phase order then
  traceability, or lead with the most failure-prone criteria).
- The precise construction of the weak sample analysis (which rigor failures
  to inject) and how concisely the shipped rubric demonstrates the verdict-block
  format.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and requirements
- `.planning/ROADMAP.md` §"Phase 3: Validation Rubric" — phase goal,
  requirements (VALID-01, VALID-02, VALID-03, VALID-04), and the 4 success
  criteria this phase must satisfy.
- `.planning/REQUIREMENTS.md` §"Validation Rubric" — full text of VALID-01
  through VALID-04. VALID-05 (the validator-fix-repeat loop) is already
  satisfied by Phase 2 — Phase 3 does not re-author it.
- `.planning/PROJECT.md` — core value ("reasoning a skeptic cannot dismiss as
  hand-waving"), the pure-Markdown / no-code constraint, and the Key Decision
  that validation tooling is a Markdown rubric, not a script.

### The output contract the rubric scores against
- `first-principles-thinking/SKILL.md` — the shipped skill: the resident
  5-phase methodology (each phase's named artifact and exit criterion), the
  condensed six-section output format, the `GT-N?` notation, and the
  "Before presenting conclusions" validator → fix → repeat instruction that
  links to this rubric. The rubric's 6 criteria must map onto these 5 phases
  + traceability.
- `first-principles-thinking/references/output-template.md` — the full
  annotated output template: section-by-section guidance, the assumptions
  table shape, derivation-chain format, the honest-depth escape valve, and the
  verdict vocabulary. The rubric's level descriptors must be observable against
  *this* template's structure.
- `first-principles-thinking/references/validation-rubric.md` — the current
  stub being replaced. Carries no frontmatter (Phase 2, D-08) — the authored
  rubric must remain a frontmatter-free reference component.

### Phase 1 outputs — methodology source and weak-sample base
- `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/methodology.md`
  — the sharpened 5-phase procedure (the rubric's per-phase criteria calibrate
  against each phase's operation, named artifact, and exit criterion).
- `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/output-template.md`
  — Phase 1's strict output template (source of the SKILL.md / references copy).
- `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/test-run-draft.md`
  — a passing-quality dogfooded analysis in the exact output format. The
  natural base to deliberately weaken into the D-04 fail-demonstration sample.
- `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/01-CONTEXT.md`
  — Phase 1 decisions D-01 (strict-shape / honest-depth escape valve), D-02
  (derivation chains), D-03 (Abandoned Reasoning section), D-07 (`GT-N?`
  unverified flagging) — the template features the rubric must score.

### Project research
- `.planning/research/PITFALLS.md` — Pitfall 2 (too prescriptive /
  box-ticking) directly motivates D-08; the rubric is the mechanism that
  catches box-ticking. Also flags the unsettled question of falsifiable LLM
  self-evaluation (STATE.md concern for this phase).
- `.planning/research/SUMMARY.md` — executive summary; the rigor-vs-hand-waving
  framing the rubric operationalizes.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- No codebase maps exist (`.planning/codebase/` is absent). The "codebase" is
  the shipped skill: `first-principles-thinking/SKILL.md` and the
  `references/` + `examples/` files (mostly stubs).
- `first-principles-thinking/references/validation-rubric.md` is a stub to be
  **replaced** in place — same path, same nav-map link, no frontmatter.
- `.planning/phases/01-.../test-run-draft.md` is a complete analysis in the
  exact output format — reusable as the base for the D-04 weak sample.

### Established Patterns
- The 3-layer skill model: `SKILL.md` body = always-on; `references/` =
  on-demand Layer 3. The rubric is a Layer-3 reference, read when the
  validator-fix-repeat loop runs.
- Phase 1's verification-artifact pattern (test-run kept in `.planning/`, not
  shipped) — D-04 reuses exactly this pattern for the weak-sample fail run.
- Reference components carry **no YAML frontmatter** (Phase 2, D-08) — the
  authored rubric must stay frontmatter-free.

### Integration Points
- `SKILL.md` "Before presenting conclusions" already links to
  `references/validation-rubric.md` and describes the validator → fix → repeat
  loop. Phase 3 fills the link target; it must not duplicate the loop
  description — the rubric is a scoring instrument, the loop lives in SKILL.md.
- The rubric's 6 criteria are the contract Phase 5 builds on — each shipped
  worked example must pass this rubric's gate (Phase 5 Success Criterion 3).

</code_context>

<specifics>
## Specific Ideas

- The rubric must *catch* a weak analysis, not certify it — the phase goal is a
  rubric that "demonstrably catches hand-waving rather than certifying it."
  D-02 (hand-wavy cap) and D-08 (escape-valve policing) are the two mechanisms
  that make this real rather than aspirational.
- Level descriptors must be **concrete observables**, never adjectives — "every
  conclusion has a derivation chain with at least one intermediate step" is a
  descriptor; "rigorous reasoning" is not (VALID-02).
- The weak sample (D-04) should fail for *specific, named* reasons traceable to
  individual criteria — a convincing fail demonstration localizes each failure,
  it does not just declare the analysis bad.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope. The companion tools (Phase 4), the
four shipped worked examples (Phase 5), and the final nav-map audit / README /
schema validation (Phase 6) were not pulled forward. The validator-fix-repeat
loop is already shipped (Phase 2) and is explicitly not re-authored here.

</deferred>

---

*Phase: 3-Validation Rubric*
*Context gathered: 2026-05-17*
