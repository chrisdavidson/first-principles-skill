# Phase 2: SKILL.md Skeleton and Frontmatter - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-16
**Phase:** 2-SKILL.md Skeleton and Frontmatter
**Areas discussed:** Skill name & directory, Description & triggers, Body composition, Nav-map placeholders

---

## Skill name & directory

### Skill name

| Option | Description | Selected |
|--------|-------------|----------|
| first-principles-thinking | Descriptive gerund, contains the literal trigger phrase, avoids reserved words. Directory `<repo>/first-principles-thinking/`. | ✓ |
| first-principles-skill | Matches the original repo name, but `skill` is filler discouraged by best-practice guidance. | |
| first-principles | Shortest; less explicit that it is a thinking methodology. | |

**User's choice:** first-principles-thinking
**Notes:** Skill lives in its own subdirectory of the repo; the repo root stays free for the future milestone-2 collection.

### metadata.version

| Option | Description | Selected |
|--------|-------------|----------|
| 2.0 | Signals the enhanced/extended successor to the original `first-principles-skill`. | ✓ |
| 1.0 | Treats this as a fresh skill at its own v1; loses the lineage. | |
| 0.1 | Pre-1.0; signals still in initial development. | |

**User's choice:** 2.0
**Notes:** —

---

## Description & triggers

| Option | Description | Selected |
|--------|-------------|----------|
| Port original + extend | Keep the original's proven trigger phrases and add phrases for the enhanced scope. | ✓ |
| Port original verbatim | Use the original's phrases as-is; risks under-triggering for new uses. | |
| Rewrite fresh | Author from scratch; discards field-tested triggering. | |

**User's choice:** Port original + extend
**Notes:** After this question the user directed that **Chinese trigger phrases be removed — not required**. This changed locked requirement FOUND-02 and Phase 2 Success Criterion 2; the user chose "Update docs now", so both `REQUIREMENTS.md` and `ROADMAP.md` were amended to English-only during the discussion.

### Reconcile the dropped Chinese-triggers requirement

| Option | Description | Selected |
|--------|-------------|----------|
| Update docs now | Amend FOUND-02 and Success Criterion 2 to English-only, then capture in CONTEXT.md. | ✓ |
| Capture in CONTEXT only | Record the override but leave the source docs mismatched. | |
| Keep Chinese after all | Reconsider and retain the English+Chinese triggers. | |

**User's choice:** Update docs now
**Notes:** `REQUIREMENTS.md` FOUND-02, its last-updated line, and `ROADMAP.md` Phase 2 Success Criterion 2 were edited to remove the "and Chinese" clause.

---

## Body composition

### Output template placement

| Option | Description | Selected |
|--------|-------------|----------|
| Resident inline | Full template in the SKILL.md body (~320–360 lines). | |
| Condensed skeleton + ref | Section list + shape rules resident; full template → `references/output-template.md`. | ✓ |
| Full reference file | Entire template in a reference; body just points to it. | |

**User's choice:** Condensed skeleton + ref
**Notes:** The 92-line methodology embeds resident, essentially verbatim from Phase 1's `methodology.md`. The user confirmed "Next area" with no further questions on body composition.

---

## Nav-map placeholders

### Placeholder strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Annotated list, no links | Name future slots as plain text; no links until files exist. | |
| Stub files created now | Phase 2 creates placeholder `.md` files so links resolve immediately. | ✓ |
| Real links to future paths | Write final links now; broken until later phases fill them. | |

**User's choice:** Stub files created now

### Stub content

| Option | Description | Selected |
|--------|-------------|----------|
| Descriptive placeholder | Heading + 1–2 sentences: what the file will hold and which phase authors it. | ✓ |
| Minimal marker | A single "Stub — authored in Phase N." line. | |
| Heading only | Just the `#` title, no body. | |

**User's choice:** Descriptive placeholder
**Notes:** Stubs stay plain Markdown with no YAML frontmatter (companion-tool files carrying frontmatter is disallowed in Phase 4).

---

## Claude's Discretion

- Exact wording of the `description` and the specific extended English trigger phrases beyond the ported originals.
- The `SKILL.md` body heading structure and any quick-reference checklist.
- Exactly which output-template shape rules make the resident condensed skeleton.
- The example stub filenames (research recommends software-systems / product-business / personal-general / science-engineering).
- The mechanical framing adaptation when `methodology.md` is embedded.

## Deferred Ideas

None — discussion stayed within phase scope.
