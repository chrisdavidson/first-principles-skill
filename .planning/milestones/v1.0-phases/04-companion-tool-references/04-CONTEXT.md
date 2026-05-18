# Phase 4: Companion Tool References - Context

**Gathered:** 2026-05-17
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase authors the **three companion thinking-tool reference files** that
replace the descriptive stubs created in Phase 2 (D-07). It produces, as
Markdown content:

- `first-principles-thinking/references/five-whys.md` — a root-cause
  drill-down: when-to-use, a branching procedure with a test-based stop
  criterion, a mini-example, failure modes, and a handoff to the 5-phase spine.
- `first-principles-thinking/references/pre-mortem.md` — a prospective-hindsight
  failure analysis: framing instruction, procedure, mini-example, failure
  modes, and a handoff to Phase 5 (Validate).
- `first-principles-thinking/references/trade-off-analysis.md` — a structured
  option comparison: a weighted-criteria-before-scoring procedure, a
  mini-example, failure modes, and a handoff to the 5-phase spine.

Each file is a self-contained, usable Layer-3 reference component carrying **no
YAML frontmatter** (Phase 4 Success Criterion 4; consistent with Phase 2 D-08).

Phase 4 **only fills the three stub files in place** — same paths, same nav-map
links. It does **not** edit `SKILL.md` (the "Companion thinking tools" section
already links all three, and the SKILL.md descriptions of each tool —
**TOOL-04** — are Phase 6). It does **not** author the four shipped worked
examples (Phase 5) or do the final nav-map audit / README / schema validation
(Phase 6).

**Filename note:** the canonical filename for the 5-Whys tool is
**`five-whys.md`** — that is the existing stub, the existing `SKILL.md` nav-map
link, and the ROADMAP name. `REQUIREMENTS.md` TOOL-01 says `5-whys.md`; that is
a stale typo — do not create a second file. Use `five-whys.md`.

</domain>

<decisions>
## Implementation Decisions

### File Structure
- **D-01:** Each file is **shaped to its own tool** — *not* a single shared
  section template across all three. 5-Whys is structured around its branching
  drill-down, pre-mortem around its prospective-hindsight framing, trade-off
  around its weighted matrix. Headings and ordering vary per tool.
- **D-02:** Two **shared anchors** keep the three readable as one coherent set:
  every file **opens with a clear "when to reach for this" framing** and
  **ends with the handoff** to the methodology. Everything between is per-tool.
- **D-03:** Regardless of per-tool shaping, **all five ROADMAP components must
  appear in each file** — when-to-use, the procedure, a mini-example, failure
  modes, and the handoff. Per-tool shaping changes *arrangement and emphasis*,
  never *presence*. (See ROADMAP Success Criteria 1–3.)

### Mini-Examples
- **D-04:** All three mini-examples draw from **one shared domain:
  everyday / non-technical** scenarios. Rationale: keeps the tool's *mechanics*
  visible rather than domain knowledge, keeps the references domain-agnostic,
  and stays clear of all four Phase 5 worked-example domains
  (software / product / personal / science) so nothing is preempted.
- **D-05:** Within that shared everyday domain, each tool gets a **separate
  scenario**, chosen to play to that tool's strength — 5-Whys on a recurring
  problem, pre-mortem on a plan that could fail, trade-off on a real choice.
  A single scenario run through all three was rejected: it risks forcing one
  situation through three mismatched lenses.

### Reference Depth
- **D-06:** Each file is a **tight sub-procedure** — lean, roughly **under
  ~100 lines, no table of contents**, just enough to apply the tool correctly.
  Rationale: these are Layer-3 files loaded on-demand; length is recurring
  token cost every time the tool is reached for. Matches CLAUDE.md's "keep each
  focused" guidance. The fuller `validation-rubric.md` (~19 KB) is *not* the
  model for these — companion tools are sub-procedures, not the rubric.

### Promotion-Readiness
- **D-07:** "Promotion-ready for the milestone-2 split" means **self-contained
  body content only**. Each file's body must be complete enough that a reader
  needs nothing but that file to apply the tool. The *only* thing a future
  split into a separate skill adds is YAML frontmatter and a directory — that
  work is deferred entirely to milestone 2. **No forward-looking "what a split
  would add" notes go in the files now** (nothing to maintain or later strip).
- **D-08:** The handoff (D-02) remains a real section and a ROADMAP-mandated
  component, but it is written as a **pointer back to the methodology, not a
  hard dependency** — applying the tool from its own file alone must not
  require having read the 5-phase spine. This is consistent with D-07's
  self-contained-body requirement. (The user did *not* ask to actively
  decouple the handoff beyond this — only that the body stand alone.)

### Claude's Discretion
Consistent with the decisions above, the researcher and planner decide:
- The exact per-tool structure of each file's procedure section (D-01) — the
  branching shape for 5-Whys, the framing-block shape for pre-mortem, the
  weighted-matrix shape for trade-off.
- The specific everyday scenario chosen for each tool's mini-example (D-05).
- The wording of each "when to reach for this" opener and each handoff (D-02),
  including exactly where each tool plugs into the 5-phase methodology — note
  ROADMAP fixes the *targets*: five-whys → 5-phase spine, pre-mortem → Phase 5
  (Validate), trade-off → 5-phase spine.
- Which failure modes to surface for each tool.
- The test-based stop criterion's exact phrasing for the 5-Whys branching
  procedure.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and requirements
- `.planning/ROADMAP.md` §"Phase 4: Companion Tool References" — phase goal
  ("self-contained, usable reference components, promotion-ready for the
  milestone-2 split"), requirements (TOOL-01, TOOL-02, TOOL-03), and the 4
  success criteria — including the per-tool component lists and SC-4 (no
  frontmatter).
- `.planning/REQUIREMENTS.md` §"Companion Thinking Tools" — full text of
  TOOL-01, TOOL-02, TOOL-03. **TOOL-04** (SKILL.md describes/links each tool)
  is **Phase 6**, not this phase. Note the `5-whys.md` vs `five-whys.md` typo
  in TOOL-01 — the canonical filename is `five-whys.md` (see domain note).
- `.planning/PROJECT.md` — core value ("reasoning a skeptic cannot dismiss as
  hand-waving"), the pure-Markdown / no-code constraint, and the Key Decision
  that companion tools live as `references/` files inside the single skill
  (components, not separate skills) — the basis for D-07.

### The skill the files plug into
- `first-principles-thinking/SKILL.md` — the shipped skill. Relevant parts:
  the resident 5-phase methodology (the handoff targets in D-08 must name real
  phases — Phase 5 Validate for pre-mortem, the spine for the other two), and
  the existing **"Companion thinking tools"** section (lines ~161–167) which
  *already* links all three files with a one-line description each. Phase 4
  must keep those three links resolving — fill the stubs, do not move or rename
  the files, do not edit SKILL.md.
- `first-principles-thinking/references/five-whys.md`,
  `pre-mortem.md`, `trade-off-analysis.md` — the current descriptive stubs
  being replaced in place. Each carries **no frontmatter** — the authored
  files must stay frontmatter-free.
- `first-principles-thinking/references/output-template.md` — the standardized
  output format the methodology produces; the handoffs should reference it
  correctly where a tool feeds back into the spine.

### Authored-reference quality bar
- `first-principles-thinking/references/validation-rubric.md` — a completed
  Layer-3 reference from Phase 3. Useful as a *quality reference* for how an
  authored reference component reads — but **not a length model**: D-06
  mandates the companion tools be far tighter (~under 100 lines) than this
  ~19 KB rubric.

### Phase 1 outputs — methodology source
- `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/methodology.md`
  — the sharpened 5-phase procedure; the handoffs (D-08) must point at real
  phase operations and artifacts.
- `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/01-CONTEXT.md`
  — Phase 1 decisions (the Abandoned Reasoning section, derivation chains) the
  handoffs may reference.

### Project research
- `.planning/research/PITFALLS.md` — Pitfall 1 (methodology too abstract) and
  Pitfall 2 (too prescriptive / box-ticking); the companion tools must be
  *usable* sub-procedures without becoming rigid checklists.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- The three stub files already exist at the correct paths
  (`first-principles-thinking/references/{five-whys,pre-mortem,trade-off-analysis}.md`).
  Phase 4 replaces stub content in place — no new files, no path changes.
- `first-principles-thinking/references/validation-rubric.md` is a finished
  Layer-3 reference — a quality reference for tone and structure of an authored
  component (but explicitly *not* a length model — see D-06).
- No `.planning/codebase/` maps exist. The "codebase" is the shipped skill
  under `first-principles-thinking/`.

### Established Patterns
- The 3-layer skill model (Phase 2): `SKILL.md` body = always-on; `references/`
  = on-demand Layer 3. The companion tools are Layer-3 references — D-06's
  "keep them tight" decision flows directly from on-demand load cost.
- Reference components carry **no YAML frontmatter** (Phase 2 D-08, Phase 4
  SC-4) — non-negotiable for all three files.
- Phase 2/3 reference files are linked one level deep directly from `SKILL.md`
  — already true for these three; Phase 4 must not break that.

### Integration Points
- `SKILL.md`'s "Companion thinking tools" section already links and one-line-
  describes all three files. Phase 4 fills the link targets; it does **not**
  edit `SKILL.md`. Expanding those SKILL.md descriptions is TOOL-04 / Phase 6.
- The handoffs (D-02, D-08) are the seam back into the 5-phase methodology —
  each must name a real phase/artifact so a reader can return to the spine.

</code_context>

<specifics>
## Specific Ideas

- The companion tools must be **genuinely usable as sub-procedures**, not just
  descriptive prose about the tool — a reader should be able to *run* the
  procedure from the file alone (this is what D-07's self-contained-body
  requirement enforces).
- 5-Whys' stop criterion is **test-based, not count-based** — the procedure
  stops when a test is satisfied, not after a fixed five iterations (ROADMAP
  SC-1 wording: "test-based stop criterion").
- Trade-off analysis must put **weighted criteria before scoring** — criteria
  and their weights are fixed *before* options are scored, to prevent
  reverse-engineering weights to favor a preferred option (ROADMAP SC-3).
- Pre-mortem uses **prospective hindsight** — the framing assumes the failure
  has already happened and works backward, rather than asking "what could go
  wrong" forward (ROADMAP SC-2).

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope. Adjacent work was explicitly kept
out: the SKILL.md tool descriptions (TOOL-04) and final nav-map audit / README
/ schema validation are Phase 6; the four shipped worked examples are Phase 5;
the future split of these tools into separate skills is milestone 2 (D-07
deliberately authors only self-contained bodies now, adding nothing the split
would later have to maintain or strip).

</deferred>

---

*Phase: 4-Companion Tool References*
*Context gathered: 2026-05-17*
