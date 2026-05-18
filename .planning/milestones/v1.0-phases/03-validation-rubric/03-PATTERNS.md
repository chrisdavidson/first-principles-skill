# Phase 3: Validation Rubric — Pattern Map

**Mapped:** 2026-05-16
**Files analyzed:** 2 (1 replace-in-place, 1 new verification artifact)
**Analogs found:** 2 / 2

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `first-principles-thinking/references/validation-rubric.md` | reference component (scoring instrument) | read-on-demand (Layer 3) | `first-principles-thinking/references/output-template.md` | role-match — same layer, same frontmatter-free convention, same annotated-reference structure |
| `.planning/phases/03-validation-rubric/03-weak-sample.md` | verification artifact (non-shipped) | one-shot demonstration | `.planning/phases/01-.../test-run-draft.md` | exact — same file role, same output format, same `.planning/` location pattern |

---

## Pattern Assignments

### `first-principles-thinking/references/validation-rubric.md` (reference component, read-on-demand)

**Analog:** `first-principles-thinking/references/output-template.md`

**File-level conventions extracted from the analog:**

**No YAML frontmatter** (lines 1–6 of `output-template.md`):
```markdown
# First Principles Analysis Output Template

> **Note:** This is the full annotated template with complete section guidance, type
> definitions, and prescriptions. A condensed skeleton showing just the required section
> names and chain format lives resident in `SKILL.md` for quick reference. Come here
> for the complete instructions when authoring or reviewing an analysis.
```

Pattern: reference files open with a `# Title` H1, then an optional block-quote note explaining the file's scope and relationship to `SKILL.md`. No YAML frontmatter block. This is the Phase 2 D-08 rule applied in practice — the analog is the only fully-authored reference file in the codebase.

**Section structure pattern** (output-template.md lines 8–25):
```markdown
## How to Use This Template

This template is a **strict-shape document**. All six sections must be present in the
fixed order below. No section may be omitted.

...

**Section order (fixed):**
1. Problem Essence
2. Assumptions Table
3. Ground Truths
4. Derivation Chains
5. Abandoned Reasoning
6. Conclusion
```

Pattern: opens with a "how to use" prose section that states the file's structural contract and any mandatory ordering up front. The rubric should mirror this — open with a brief "how to apply this rubric" section that states the 6-criterion structure, the scoring model (gate + cap), and the verdict-block requirement before listing any criteria.

**H2 section, H3 sub-section heading hierarchy** (output-template.md throughout):
```markdown
## 1. Problem Essence
...
## 2. Assumptions Table
...
### Type Definitions and Prescribed Treatments
...
### Stakes-Escalation Rule
...
### Verdict Vocabulary
```

Pattern: top-level sections are H2 (numbered), sub-elements within a section are H3. The rubric should use H2 for the scoring model preamble and for each criterion block, H3 for sub-elements (level scale, verdict block guidance, gate/cap rules).

**Inline code for notation** (output-template.md lines 44, 83–86):
```markdown
| [physical law / current constraint / convention / untested belief] | ...
- **GT-3?** [fact text] — unverified: [...]
The `?` suffix signals that this ground truth is an untested belief...
```

Pattern: notation tokens (`GT-N?`, backtick-wrapped) appear inline in prose and in table cells. The rubric should use this same style for band labels and criterion identifiers when referenced inline.

**Fenced code blocks for format examples** (output-template.md lines 99–103):
```
**Chain format:**

```
GT-N + GT-M → [intermediate claim] → [conclusion]
```
```

Pattern: any required format (verdict block shape, gap-citation shape) is shown in a fenced code block with no language tag. The rubric's verdict-block format prescription must follow this convention.

**Prose lists with bold lead-ins for vocabulary** (output-template.md lines 65–69):
```markdown
### Verdict Vocabulary

- **Accept** — the assumption survives challenge and may be used in the analysis
- **Challenge** — the assumption is questionable; probe further before use
- **Discard** — the assumption is false or irrelevant; remove from the reasoning chain
```

Pattern: defined vocabulary items are bulleted, with the term in bold followed by an em-dash and a one-sentence definition. The rubric's level scale should use this pattern for band label definitions.

**Horizontal rule (`---`) between major sections** (output-template.md lines 26, 69, 91, etc.):
Pattern: `---` separates each numbered top-level section. The rubric should use `---` between the scoring model preamble and the criteria list, and between the criteria list and any usage notes.

---

### `.planning/phases/03-validation-rubric/03-weak-sample.md` (verification artifact, non-shipped)

**Analog:** `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/test-run-draft.md`

**File header pattern** (test-run-draft.md lines 1–13):
```markdown
# Test Run (Draft) — First Principles Analysis

> **Status:** Working draft (D-09). This file dogfoods the methodology in
> `methodology.md` against the output shape in `output-template.md`. It is a
> Phase 1 verification artifact and is **not** a shipped `examples/` file —
> Phase 5 may later polish it into one.
>
> **Subject (D-08):** A genuinely unresolved design question from this skill
> build — candidate (c) from `01-RESEARCH.md` Open Question 3. ...

---
```

Pattern: title as H1, then a block-quote status note naming the artifact's role, which CONTEXT.md decision it satisfies, what it is NOT (not a shipped file), and what it demonstrates. The weak-sample file should open with the same pattern — H1 title, block-quote status naming D-04, noting it is a `.planning/` verification artifact, and stating what failure modes are deliberately injected.

**Full six-section output format** (test-run-draft.md lines 16–225, complete run):

The analog uses the full six-section structure in order:
```markdown
## 1. Problem Essence
## 2. Assumptions Table
## 3. Ground Truths
## 4. Derivation Chains
## 5. Abandoned Reasoning
## 6. Conclusion
```

The weak sample must preserve this same structure — the failure injections degrade quality within sections, they do not remove section headings. Preserved sections (per RESEARCH.md): Problem Essence, Ground Truths (with GT-IDs), Conclusion section. Degraded sections: Assumptions Table (strip classification specificity, empty Verdict/Verification cells), Derivation Chains (remove intermediate steps from chains), Abandoned Reasoning (replace documented dead ends with a generic escape-valve abuse).

**Assumptions Table shape** (test-run-draft.md lines 39–46):
```markdown
| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A1: Every real assumption falls cleanly into exactly one of the four types. | untested belief | verify, or flag unverified | **Discard** | False. Counterexample constructed below (→ GT-3): ... |
```

The weak sample keeps this table shape but injects generic/empty Type and Verdict/Verification cells — the structural shape is preserved so the rubric can quote specific broken cells in verdict blocks.

**Derivation chain format** (test-run-draft.md lines 84–94):
```markdown
### Conclusion: A fifth "mixed / uncertain" category cannot satisfy the scheme's own stated purpose.

GT-2 (the scheme's function is to select a treatment for each assumption)
+ GT-4 (a "mixed" category names the absence of a type, not a treatment)
→ an assumption placed in a "mixed / uncertain" category reaches the end of
Phase 2 without any of the four prescribed treatments being selected — it exits
classification *untreated*
→ adding a fifth "mixed / uncertain" category creates a classification outcome
that does not drive a treatment, which directly contradicts the scheme's stated
purpose.

**Confidence:** HIGH — both inputs (GT-2, GT-4) are verified.
```

The weak sample flattens this to remove the intermediate step — the chain goes directly from GT-ID pair to conclusion, skipping the intermediate claim. The chain section heading (H3 `### Conclusion: ...`) and confidence line are preserved so the rubric can quote the broken chain exactly.

**Abandoned Reasoning structure** (test-run-draft.md lines 147–181):
```markdown
### Dead End: Encode confidence gradations into the type taxonomy

**What was tried:** ...
**Why abandoned:** ...
**What it ruled out:** ...

### Dead End: Drop classification entirely and "just verify everything"

**What was tried:** ...
**Why abandoned:** ...
**What it ruled out:** ...
```

The weak sample replaces both documented dead ends with a single generic escape-valve line:
```
Nothing material here — no dead ends were encountered.
```

The H2 section heading `## 5. Abandoned Reasoning` must still appear (section headings are never removed, per output-template.md), but the content below is replaced with the generic escape valve. This is exactly the D-08 escape-valve abuse pattern the rubric is built to catch.

---

## Shared Patterns

### No YAML Frontmatter on Reference Components

**Source:** Phase 2 D-08 decision; observable in `first-principles-thinking/references/output-template.md` (lines 1–6 — no `---` YAML fence)
**Apply to:** `validation-rubric.md` only (`03-weak-sample.md` is a `.planning/` artifact, not a reference component, and has no frontmatter requirement either)

The rule: reference files in `first-principles-thinking/references/` carry no YAML frontmatter. The file starts directly with the `# Title` H1. Any file with a `---` YAML block at the top would violate this constraint.

### Block-Quote Status/Scope Note at File Open

**Source:** `output-template.md` lines 3–6; `test-run-draft.md` lines 3–13

Both fully-authored files in this codebase open with a block-quote (`>`) note before the first substantive content. For `output-template.md` this explains the relationship to SKILL.md. For `test-run-draft.md` this names the artifact's status, its anchoring decision, and what it is not. Both new files should follow this pattern.

### Fenced Code Blocks Without Language Tags for Format Prescriptions

**Source:** `output-template.md` lines 98–103 (chain format block)
**Apply to:** `validation-rubric.md` verdict-block format prescriptions

When showing a required format (verdict block shape, gap-citation shape, scoring model pattern), use a fenced code block with no language specifier. Do not use ` ```markdown ` — use ` ``` ` only. The analog demonstrates this for the chain format block.

### H3 Sub-Headings Within H2 Sections

**Source:** `output-template.md` (e.g., `## 2. Assumptions Table` contains `### Type Definitions and Prescribed Treatments`, `### Stakes-Escalation Rule`, `### Verdict Vocabulary`)
**Apply to:** `validation-rubric.md` criterion sections

Each criterion is an H2 section. Sub-elements within a criterion (the 4-level scale, any special-case rules like escape-valve policing) are H3 sub-headings within that criterion's H2 block. Do not go deeper than H3.

### Bold Lead-Ins for Defined Terms

**Source:** `output-template.md` lines 65–69 (Verdict Vocabulary) and lines 48–58 (Type Definitions)
**Apply to:** Band label definitions in `validation-rubric.md` scoring model section; per-criterion level descriptors

Format: `- **Term** — prose definition`. Used for the shared 4-level scale definitions and for any per-criterion special vocabulary.

### Horizontal Rule Between Major Sections

**Source:** `output-template.md` (between every numbered H2 section)
**Apply to:** `validation-rubric.md` between the scoring model preamble, the criteria list, and any closing usage notes

Use `---` to separate the scoring model block from the criteria list, and after the last criterion. Do not use `---` between individual criteria within the criteria list — that would over-partition the document.

---

## No Analog Found

No files in this codebase lack a close analog. Both new files have strong matches:

| File | Match Quality | Notes |
|------|--------------|-------|
| `first-principles-thinking/references/validation-rubric.md` | role-match | `output-template.md` is the only fully-authored reference in `references/`; all other references are stubs. The analog is strong for structure/conventions; the rubric's content type (scoring instrument vs. template) differs but the document architecture conventions are identical. |
| `.planning/phases/03-validation-rubric/03-weak-sample.md` | exact | `test-run-draft.md` is the same file role (verification artifact in `.planning/phases/`), same output format, same non-shipped status. The weak sample is a deliberately-degraded version of this exact file. |

---

## Metadata

**Analog search scope:** `first-principles-thinking/references/`, `.planning/phases/01-*/`
**Files read:** 6 (`03-CONTEXT.md`, `03-RESEARCH.md`, `validation-rubric.md` stub, `output-template.md`, `test-run-draft.md`, `01-CONTEXT.md`)
**Pattern extraction date:** 2026-05-16
