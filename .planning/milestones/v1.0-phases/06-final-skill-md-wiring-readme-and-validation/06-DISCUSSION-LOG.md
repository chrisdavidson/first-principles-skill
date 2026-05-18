# Phase 6: Final SKILL.md Wiring, README, and Validation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-18
**Phase:** 06-final-skill-md-wiring-readme-and-validation
**Areas discussed:** README depth & audience, Schema validation gate, SKILL.md wiring scope, README install coverage

---

## README depth & audience

### Q1 — How much should README.md contain?

| Option | Description | Selected |
|--------|-------------|----------|
| Comprehensive | What it is + methodology summary + companion tools + examples list + when-to-use + fork lineage + install | ✓ |
| Mid-weight | What it is + brief methodology + install; skip tool/example catalogs | |
| Minimal | What it is in 2-3 sentences + install steps only | |

**User's choice:** Comprehensive

### Q2 — How should the README relate to the canonical SKILL.md?

| Option | Description | Selected |
|--------|-------------|----------|
| Summarize + link to canonical | Prose overview of the 5 phases, then point to SKILL.md / output-template.md as authoritative | ✓ |
| Self-contained | README fully explains the methodology; human never needs SKILL.md | |

**User's choice:** Summarize + link to canonical

### Q3 — How prominently should the README cover the fork lineage?

| Option | Description | Selected |
|--------|-------------|----------|
| Dedicated section | "Relationship to the original" section naming what v2.0 adds | ✓ |
| Brief lineage note | One-line "forked from / enhances X" + MIT attribution | |
| License line only | Just the MIT license/attribution line, no fork narrative | |

**User's choice:** Dedicated section

**Notes:** README is the human-facing front door for a forked MIT skill; the
whole project premise is "enhanced successor", so the lineage section earns
its place. SKILL.md remains the single source of truth — README orients.

---

## Schema validation gate

### Q1 — How should "passes Agent Skills schema validation" be satisfied/proven?

| Option | Description | Selected |
|--------|-------------|----------|
| Install + run skills-ref | Install skills-ref, run `skills-ref validate`, capture pass output as evidence | ✓ |
| Both: skills-ref + manual checklist | skills-ref as gate when it installs cleanly; manual checklist as durable fallback | |
| Manual conformance check only | Documented checklist against CLAUDE.md frontmatter constraints, no host install | |

**User's choice:** Install + run skills-ref

### Q2 — How should PKG-02 (cross-references resolve) be checked?

| Option | Description | Selected |
|--------|-------------|----------|
| One-time link-resolution script | Host-side grep/script extracts every relative link and asserts each target exists | ✓ |
| Manual link review | Reviewer walks every cross-reference by hand | |

**User's choice:** One-time link-resolution script

### Q3 — Should Phase 6 run markdownlint?

| Option | Description | Selected |
|--------|-------------|----------|
| Skip markdownlint | skills-ref + link check already cover the success criteria; markdownlint is optional | |
| Run markdownlint | Repo-wide consistency pass with the CLAUDE.md-recommended config | ✓ |

**User's choice:** Run markdownlint

**Notes:** skills-ref is the authoritative gate but is not installed on the
build machine — installation is in-scope. Link-resolution check and
markdownlint are host-side tooling, NOT bundled into the skill (pure-Markdown
v1 constraint). CONTEXT.md adds a contingency: if skills-ref cannot install,
flag the validation task for manual intervention rather than silently passing.

---

## SKILL.md wiring scope

### Q1 — What should Phase 6 do with the existing nav map?

| Option | Description | Selected |
|--------|-------------|----------|
| Verify-and-polish | Keep the current structure; audit links, polish wording only | |
| Restructure into one file map | Consolidate all Layer-3 links into a single "Skill files" navigation section | ✓ |

**User's choice:** Restructure into one file map

### Q2 — Are the one-line companion-tool entries enough, or expand?

| Option | Description | Selected |
|--------|-------------|----------|
| Keep one-line entries | Already pairs trigger + description + link; satisfies TOOL-04 | |
| Expand to short blurbs | 2-3 sentences per tool: what it does, when to reach for it, handoff to the spine | ✓ |

**User's choice:** Expand to short blurbs

### Q3 — How should the consolidated "Skill files" section be organized?

| Option | Description | Selected |
|--------|-------------|----------|
| Grouped subsections | Companion tools (blurbs) + Worked examples + Reference docs subsections | ✓ |
| Flat table | Single uniform table: file path / what it is / when to read it | |

**User's choice:** Grouped subsections

### Q4 — What happens to the inline output-template / validation-rubric links?

| Option | Description | Selected |
|--------|-------------|----------|
| Keep inline + also in map | Functional links stay where the model reasons; map is the complete index | ✓ |
| Map only | Remove inline links; all 9 links live solely in the consolidated section | |

**User's choice:** Keep inline + also in map

**Notes:** All 9 Layer-3 cross-references were verified to resolve during
discussion — the restructure changes presentation, not whether files are
linked.

---

## README install coverage

### Q1 — What install methods should the README document?

| Option | Description | Selected |
|--------|-------------|----------|
| Copy + symlink, both scopes | cp + ln -s into personal (~/.claude/skills/) and project (.claude/skills/) | ✓ |
| Copy + symlink, personal only | Both methods, personal scope only | |
| Copy only | Single documented path: clone then copy | |

**User's choice:** Copy + symlink, both scopes

### Q2 — Should the README mention host-side validation tooling?

| Option | Description | Selected |
|--------|-------------|----------|
| User-facing only | Dev tooling stays in CLAUDE.md, out of the README | ✓ |
| Add a contributing note | Short "Validating / contributing" section pointing at skills-ref + markdownlint | |

**User's choice:** User-facing only

**Notes:** Install section must call out the correctness requirement that the
installed directory be named `first-principles-thinking` (must equal the
frontmatter `name`).

---

## Claude's Discretion

- Exact prose wording of all README sections and the methodology summary.
- Exact heading text for the consolidated "Skill files" section and the
  ordering of its three subsections.
- Implementation of the one-time link-resolution check (bash/grep/node) and
  whether it is committed to the repo for reuse.
- Whether skills-ref is installed via npm or by cloning the agentskills repo.
- Concrete shell command snippets in the README install section.

## Deferred Ideas

None — discussion stayed within phase scope.
