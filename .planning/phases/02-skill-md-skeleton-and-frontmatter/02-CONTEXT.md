# Phase 2: SKILL.md Skeleton and Frontmatter - Context

**Gathered:** 2026-05-16
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase builds the **discoverable, loadable shell** of the skill — it turns
Phase 1's free-standing methodology content into an actual installable Claude
Code skill. It produces:

- `SKILL.md` with valid YAML frontmatter (`name`, `description`,
  `metadata.version`) conforming to the Agent Skills schema.
- A `description` field that triggers reliably — what + when, with explicit
  English trigger phrases, within the character budget.
- The Phase-1 5-phase methodology embedded **resident** in the body as standing
  instruction, plus a condensed output-template skeleton.
- A navigation map whose named slots Phases 3–6 fill, backed by stub files.
- The validator-fix-repeat instruction (VALID-05) wired into the body.

Phase 2 places content into a skill structure; it does **not** author the
validation rubric (Phase 3), the companion tools (Phase 4), or the worked
examples (Phase 5) — it creates their stub files only. It does **not** do the
final nav-map link audit, the README, or schema validation (Phase 6).

</domain>

<decisions>
## Implementation Decisions

### Skill Identity & Location
- **D-01:** The skill's `name` is **`first-principles-thinking`**. The Agent
  Skills schema requires `name` to exactly equal the directory name, so the
  skill lives at **`<repo>/first-principles-thinking/SKILL.md`** — its own
  subdirectory of the repo root. The repo root (`first-principles-skills`,
  plural) is deliberately left free for the future milestone-2 collection.
  Rationale: descriptive gerund, carries the literal trigger phrase "first
  principles thinking", avoids the reserved words `anthropic`/`claude` and the
  filler suffix `skill`.
- **D-02:** `metadata.version` is set to **`"2.0"`** (quoted string). It
  signals this is the enhanced/extended successor to the original
  `first-principles-skill` — the project's whole premise is "v2 of that skill".
  Version goes under `metadata`, never as a top-level `version:` key.

### Description & Triggers
- **D-03:** Trigger phrases are sourced **port-and-extend**: keep the original
  skill's field-tested English trigger phrases (the researcher fetches them
  from the source repo), then add phrases covering what the enhanced version
  newly does — e.g. evaluating a design, challenging assumptions, checking
  whether reasoning is sound, applying the self-check rubric. Honors
  "enhance, don't rewrite" while widening trigger coverage.
- **D-04:** Triggers are **English-only — Chinese trigger phrases are dropped**
  (the user decided they are not required). This changed a locked requirement:
  **FOUND-02** in `REQUIREMENTS.md` and **Phase 2 Success Criterion 2** in
  `ROADMAP.md` were both amended during this discussion to remove the
  "and Chinese" clause, so the phase verifies cleanly against English-only.

### Body Composition
- **D-05:** The standardized output template is split. A **condensed skeleton**
  — the required section list plus the key shape rules — stays **resident** in
  the `SKILL.md` body. The **full annotated template** moves to a new Layer-3
  file, **`references/output-template.md`**, which Phase 2 authors from Phase
  1's `output-template.md`. This is a real file with a real, resolving nav-map
  link (not a stub). Rationale: keeps the always-on body lean (~230 lines)
  while the full detail is one Read away.
- **D-06:** The 5-phase methodology procedure embeds **resident** in the body,
  **essentially verbatim** from Phase 1's `methodology.md` (92 lines). Only
  mechanical framing adaptation is allowed — heading levels, an intro sentence
  to seat it inside `SKILL.md`. No `methodology-deep-dive.md` split is needed;
  the methodology fits comfortably under the 500-line body budget. The Phase-1
  procedure must keep its rigor — entry/exit criteria, named artifacts, the
  4-type assumption scheme, rationale statements.

### Navigation Map & Placeholders
- **D-07:** Phase 2 **creates stub files now** for every not-yet-built Layer-3
  file, so nav-map links resolve immediately rather than dangling. Stubs to
  create: `references/validation-rubric.md`, `references/five-whys.md`,
  `references/pre-mortem.md`, `references/trade-off-analysis.md`, and four
  `examples/` files (one per domain). The skill loads with zero broken links
  through the whole build.
- **D-08:** Each stub is a **descriptive placeholder** — a `#` heading plus 1–2
  sentences stating what the file will contain and which phase authors it
  (e.g. `# Validation Rubric` / "The falsifiable self-check scoring rubric.
  Authored in Phase 3."). Stubs are **plain Markdown with NO YAML frontmatter**
  — companion-tool files carrying their own frontmatter is explicitly
  disallowed (Phase 4 Success Criterion 4).
- **D-09:** The **VALID-05 validator-fix-repeat instruction** is fully written
  into the `SKILL.md` body this phase: it instructs Claude to apply the
  validation rubric as a validator → fix → repeat loop before presenting
  conclusions. Because the rubric stub exists after Phase 2, the instruction
  links to `references/validation-rubric.md` with a real, resolving link — the
  behavioral instruction is complete now; Phase 3 fills the rubric content.

### Claude's Discretion
Left to the researcher and planner, consistent with the decisions above:
- Exact wording of the `description` (third person, what+when, within budget)
  and the specific extended English trigger phrases beyond the ported originals.
- The `SKILL.md` body heading structure and any quick-reference checklist.
- Exactly which output-template shape rules make the resident condensed
  skeleton vs. live only in the full `references/output-template.md`.
- The example stub filenames — research recommends `examples/software-systems.md`,
  `product-business.md`, `personal-general.md`, `science-engineering.md`.
- The mechanical framing adaptation when `methodology.md` is embedded.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and requirements
- `.planning/ROADMAP.md` §"Phase 2: SKILL.md Skeleton and Frontmatter" — phase
  goal, requirements (FOUND-01, FOUND-02, FOUND-03, VALID-05), and the 4
  success criteria. **Note:** Success Criterion 2 was amended this discussion
  (Chinese trigger phrases removed — English-only).
- `.planning/REQUIREMENTS.md` §"Skill Foundation" (FOUND-01, FOUND-02 [amended
  to English-only], FOUND-03) and §"Validation Rubric" (VALID-05).
- `.planning/PROJECT.md` — core value, the pure-Markdown / no-code constraint,
  the "enhance, don't rewrite" Key Decision, and the install model.
- `CLAUDE.md` §"Technology Stack" — the prescriptive frontmatter schema
  guidance this phase must follow: `name` constraints (lowercase-alnum-hyphen,
  must equal dirname, no reserved words), `description` as trigger,
  `metadata.version`, the <500-line body budget, directory conventions, and
  the explicit "What NOT to Use" anti-patterns. Highly relevant — treat as the
  authoring spec for the frontmatter and structure.

### Phase 1 outputs — the content this phase embeds
- `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/methodology.md`
  — the sharpened 5-phase procedure, embedded resident in `SKILL.md` (D-06).
- `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/output-template.md`
  — the strict output template; condensed skeleton goes resident, full version
  becomes `references/output-template.md` (D-05).
- `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/01-CONTEXT.md`
  — Phase 1 decisions (strict-shape template, derivation chains, the Abandoned
  Reasoning section) the resident content must preserve.

### Project research
- `.planning/research/ARCHITECTURE.md` — the 3-layer loading model, the
  recommended project structure and file naming, and the
  "SKILL.md as table of contents" navigation pattern this phase implements.
- `.planning/research/STACK.md` — frontmatter schema details and the
  `skills-ref` validation tooling.
- `.planning/research/FEATURES.md` — skill discoverability and triggering
  expectations relevant to the `description`.
- `.planning/research/PITFALLS.md` — triggering and body-bloat pitfalls.

### Source skill (external — researcher should fetch)
- `github.com/chrisdavidson/first-principles-skill` — the original skill's
  `SKILL.md`: its frontmatter shape and, specifically, its English trigger
  phrases, which D-03 ports forward.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- No codebase maps exist (`.planning/codebase/` is absent) and the repo holds
  no skill files yet — Phase 2 authors `SKILL.md` for the first time.
- The reusable *content* is the Phase 1 output: `methodology.md` and
  `output-template.md` in the phase-01 directory (see Canonical References).
- The repo otherwise contains only planning docs (`.planning/`), `CLAUDE.md`,
  and an untouched `uv` Python scaffold (`main.py`, `pyproject.toml`,
  `.python-version`, `README.md`) — out of scope, do not touch.

### Established Patterns
- The 3-layer skill model (`.planning/research/ARCHITECTURE.md`): frontmatter =
  Layer 1, `SKILL.md` body = Layer 2 (always-on), `references/` + `examples/` =
  Layer 3 (on-demand). Phase 2 builds Layers 1–2 and the Layer-3 skeleton.

### Integration Points
- Phase 2's `SKILL.md` body and `references/output-template.md` are the
  contract Phase 3 (rubric calibrates against this output format), Phase 5
  (examples authored to this format), and Phase 6 (final nav-map link audit,
  README, schema validation) build on.
- The stub files (D-07/D-08) are the named slots Phases 3–6 fill in place.

</code_context>

<specifics>
## Specific Ideas

- The repo root must stay reserved for the future skill collection — the v1
  skill is one subdirectory (`first-principles-thinking/`), not the repo root.
- The `uv` Python scaffold is reserved for milestone 3 — leave it untouched.
- Stubs must be obviously incomplete (descriptive placeholder text naming the
  authoring phase) so an agent or reader never mistakes a stub for real
  content — but never carry frontmatter.
- The resident methodology should preserve Phase 1's rigor verbatim; this
  phase places content, it does not re-sharpen or re-condense the methodology.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope. Authoring the rubric, the
companion tools, the worked examples, the final nav-map link audit, the
README, and schema validation are all later phases (3–6); Phase 2 only creates
their stub slots.

</deferred>

---

*Phase: 2-SKILL.md Skeleton and Frontmatter*
*Context gathered: 2026-05-16*
