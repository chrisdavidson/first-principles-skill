# Phase 6: Final SKILL.md Wiring, README, and Validation - Context

**Gathered:** 2026-05-18
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase finalizes the assembled skill and proves it shippable. It is the
last phase of v1 — the milestone closes when it passes.

It delivers three things:

1. **Final SKILL.md wiring** — the navigation map is restructured into one
   consolidated "Skill files" section so every `references/` and `examples/`
   file is linked one level deep from `SKILL.md`, and every companion tool is
   described with when to reach for it.
2. **A human-facing `README.md`** — currently empty. A comprehensive README
   describing the skill, its methodology, its companion tools and worked
   examples, when to use it, its fork lineage, and copy/symlink installation.
3. **Schema + cross-reference validation** — the skill passes Agent Skills
   schema validation (`skills-ref`), every internal cross-reference resolves,
   and a repo-wide Markdown lint pass is clean.

**Scope note — the build is nearly done already.** Phases 1–5 produced the
`SKILL.md` body and all 9 Layer-3 files (`references/` ×5, `examples/` ×4), and
the nav map already links every one of them. During discussion all 9
cross-references were verified to resolve. So this phase is *finalization*, not
construction: restructure the nav map, write the README from scratch, and run
the validation tooling. It does NOT re-author methodology, rubric, companion
tools, or examples — that content is locked from Phases 1–5.

**Out of scope:** anything touching the `uv` Python scaffold (`main.py`,
`pyproject.toml`) — reserved for milestone 3; the repo root stays reserved for
the milestone-2 collection. No executable code added to the skill itself.

</domain>

<decisions>
## Implementation Decisions

### README depth & audience
- **D-01:** `README.md` is **comprehensive**. It is the human-facing front
  door (GitHub readers, people deciding whether to install). It covers: what
  the skill is, a readable summary of the 5-phase methodology, the companion
  tools, the worked-examples list, when to use it (trigger situations), the
  fork lineage, and installation. It is not a minimal "what + install" stub.
- **D-02:** The README **summarizes the methodology in readable prose, then
  explicitly points to `SKILL.md` and `first-principles-thinking/references/output-template.md`
  as the authoritative/canonical spec.** `SKILL.md` stays the single source of
  truth — the README orients a human, it does not re-specify the methodology.
  Goal: no drift between README and SKILL.md.
- **D-03:** The README has a **dedicated "Relationship to the original"
  section** (the skill is a fork/enhancement of
  `github.com/chrisdavidson/first-principles-skill`, MIT, same author). It
  names what the v2.0 enhanced successor adds over the original: the
  validation rubric, the three companion tools (5-Whys, pre-mortem, trade-off),
  the four domain-spread worked examples, and the sharpened 5-phase
  methodology with entry/exit criteria and named artifacts.

### Schema validation gate
- **D-04:** "Passes Agent Skills schema validation" is satisfied by
  **installing `skills-ref` and running `skills-ref validate ./first-principles-thinking`**,
  capturing the pass output as evidence. `skills-ref` is the authoritative
  validator CLAUDE.md calls "the gate"; it is NOT currently installed on this
  machine, so installation (per the `agentskills/agentskills` repo
  instructions) is part of the phase work. **Contingency:** if `skills-ref`
  cannot be installed cleanly (network/permissions), the plan must flag the
  validation task for manual intervention (`autonomous: false`) rather than
  silently passing — a documented manual conformance check against the
  CLAUDE.md frontmatter constraints is the fallback evidence, but `skills-ref`
  is the preferred gate.
- **D-05:** PKG-02 ("all cross-references resolve correctly") is verified by a
  **one-time host-side link-resolution check** — a grep/script pass that
  extracts every relative Markdown link from `SKILL.md`, `references/`, and
  `examples/` and asserts each target file exists. This is host-side tooling
  run during the phase; it is **NOT bundled into the skill** (pure-Markdown v1
  constraint — no executable code ships in the skill).
- **D-06:** A **repo-wide `markdownlint` pass** is run over the skill files
  using the CLAUDE.md-recommended config: `MD013` (line length) **off**;
  `MD003` (consistent ATX headings), `MD040` (fenced-code language), `MD041`
  (first line heading) **on**. Like the link check, `markdownlint` is host-side
  tooling, not bundled into the skill.

### SKILL.md wiring scope
- **D-07:** The `SKILL.md` navigation map is **restructured into a single
  consolidated "Skill files" navigation section** with grouped subsections —
  replacing the current distributed inline links plus the two separate
  "Companion thinking tools" and "Worked examples" sections. Subsections:
  **Companion tools** (each with a 2–3 sentence blurb — see D-08),
  **Worked examples** (one line per domain), and **Reference docs**
  (`output-template.md`, `validation-rubric.md`).
- **D-08:** Each of the **3 companion tools is expanded to a 2–3 sentence
  blurb** in `SKILL.md` (the current entries are one line each): what the tool
  does, when to reach for it, and how it hands back to the 5-phase spine. This
  satisfies TOOL-04 with real description, not just a trigger line.
- **D-09:** The inline links to `references/output-template.md` (at the
  "Output format" section) and `references/validation-rubric.md` (at the
  "Before presenting conclusions" section) are **kept inline at their
  functional body locations AND also listed in the consolidated map**. The
  functional links stay where the model reasons about output format / the
  rubric; the map is the complete index. Minor duplication is intentional —
  each placement serves a purpose. All paths use forward slashes.

### README install coverage
- **D-10:** The README documents **both `cp` (copy) and `ln -s` (symlink)
  installation, into both the personal scope (`~/.claude/skills/`) and the
  project scope (`.claude/skills/`)** — personal marked as the recommended
  default. The symlink path notes that it keeps the cloned repo as the live
  source of truth (edits picked up without re-copying). The install section
  **must call out the correctness requirement that the installed directory be
  named `first-principles-thinking`** (must equal the frontmatter `name`),
  since the skill lives in a `first-principles-thinking/` subdirectory of the
  repo.
- **D-11:** The README is **user-facing only**. The host-side dev/validation
  tooling (`skills-ref`, `markdownlint`) stays documented in `CLAUDE.md` and is
  NOT given a contributing section in the README.

### Claude's Discretion
- Exact prose wording of all README sections.
- Exact heading text for the consolidated "Skill files" section and the
  ordering of its three subsections.
- Implementation of the one-time link-resolution check (bash/grep/node) and
  where it lives (it is throwaway host-side tooling, not committed into the
  skill — committing it to the repo for reuse is acceptable but optional).
- Whether `skills-ref` is installed via npm or by cloning the `agentskills`
  repo — follow that repo's current install instructions.
- Concrete shell command snippets in the README install section.
- Wording of the methodology summary in the README (prose form, links to
  canonical).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and requirements
- `.planning/ROADMAP.md` §"Phase 6: Final SKILL.md Wiring, README, and
  Validation" — phase goal, requirements (FOUND-04, FOUND-05, TOOL-04, PKG-01,
  PKG-02, PKG-03), and the 5 success criteria.
- `.planning/REQUIREMENTS.md` §"Skill Foundation" (FOUND-04, FOUND-05),
  §"Companion Tools" (TOOL-04), §"Packaging" (PKG-01, PKG-02, PKG-03).
- `.planning/PROJECT.md` — core value, the pure-Markdown / no-executable-code
  constraint, the "enhance, don't rewrite" Key Decision, the install model,
  and the three-milestone vision (why the repo root and `uv` scaffold are
  left untouched).

### Authoring spec for frontmatter, structure, and install
- `CLAUDE.md` §"Technology Stack" — the prescriptive frontmatter schema
  (`name` constraints, `description`, `metadata.version`), the `<500`-line
  body budget, directory conventions (`references/`, `examples/`, no
  `scripts/`), the "What NOT to Use" anti-patterns, and the explicit
  "one-level-deep references" rule (FOUND-04). Treat as the authoring spec.
- `CLAUDE.md` §"Installation" and §"Where Skills Live" — the copy/symlink
  install model and the personal-vs-project scope table the README documents
  (D-10).
- `CLAUDE.md` §"Validation" and §"Development Tools" — `skills-ref validate`
  as the schema gate, the `markdownlint` config recommendations (`MD013` off;
  `MD003`/`MD040`/`MD041` on), and the note that there is no
  `claude skill validate` command.

### The skill being finalized
- `first-principles-thinking/SKILL.md` — the body and current nav map to
  restructure (D-07/D-08/D-09).
- `first-principles-thinking/references/` — `output-template.md`,
  `validation-rubric.md`, `five-whys.md`, `pre-mortem.md`,
  `trade-off-analysis.md` (all exist; nav-map link targets).
- `first-principles-thinking/examples/` — `software-systems.md`,
  `product-business.md`, `personal-general.md`, `science-engineering.md`
  (all exist; nav-map link targets).

### Prior phase context (decisions this phase must respect)
- `.planning/phases/02-skill-md-skeleton-and-frontmatter/02-CONTEXT.md` — D-01
  (skill name `first-principles-thinking` = dirname), D-02 (`metadata.version`
  `"2.0"`), the 3-layer loading model, and the explicit statement that the
  final nav-map audit, README, and schema validation are Phase 6 work.

### Source skill (external — for the README lineage section)
- `github.com/chrisdavidson/first-principles-skill` — the original MIT skill
  the README's "Relationship to the original" section (D-03) describes.

### Project research (background, optional)
- `.planning/research/STACK.md` — `skills-ref` tooling and frontmatter schema
  detail.
- `.planning/research/ARCHITECTURE.md` — the "SKILL.md as table of contents"
  navigation pattern the consolidated map (D-07) implements.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- The skill is fully built: `first-principles-thinking/SKILL.md` (176 lines)
  plus 9 Layer-3 files. Phase 6 edits `SKILL.md` and creates `README.md`; it
  does not author new skill content.
- `README.md` exists at the repo root but is **empty (0 lines)** — Phase 6
  writes it from scratch.
- No `.planning/codebase/` maps exist — this is a pure-Markdown skill repo,
  not an application codebase.

### Established Patterns
- The 3-layer skill model (Phase 2 D-05/D-07): frontmatter = Layer 1,
  `SKILL.md` body = Layer 2 (always-on), `references/` + `examples/` = Layer 3
  (on-demand). The consolidated nav map (D-07) is the Layer-2 index into
  Layer 3.
- All Layer-3 files are plain Markdown with **no YAML frontmatter** (Phase 2
  D-08) — do not add frontmatter to them.

### Integration Points
- The restructured `SKILL.md` nav map must link all 9 Layer-3 files one level
  deep with forward-slash relative paths — no nested `SKILL.md → a.md → b.md`
  chains (CLAUDE.md anti-pattern).
- `skills-ref validate` checks `SKILL.md` frontmatter and that `name` equals
  the parent directory name (`first-principles-thinking`).

</code_context>

<specifics>
## Specific Ideas

- During discussion, all 9 Layer-3 cross-references were checked and confirmed
  to resolve — the link audit is expected to confirm correctness, not fix
  breakage. If the audit finds a broken link, that is a real defect to fix.
- `skills-ref` is confirmed NOT installed on the build machine — installing it
  is in-scope phase work (D-04).
- The README's "Relationship to the original" section should be concrete about
  v2.0 additions, not vague — it is the project's whole premise that this is an
  enhanced successor.
- The consolidated "Skill files" section is a restructure of existing links,
  not new wiring — the current SKILL.md already links every file; D-07 changes
  *how* they are presented, not *whether* they are linked.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope. The v2 requirements (META-01
dogfooding reference, META-02 expanded taxonomy, META-03 extra examples) and
milestones 2–3 (skill collection, Python builder) remain out of scope and
unchanged.

</deferred>

---

*Phase: 6-Final SKILL.md Wiring, README, and Validation*
*Context gathered: 2026-05-18*
