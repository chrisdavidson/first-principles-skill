# Phase 4: Companion Tool References - Pattern Map

**Mapped:** 2026-05-17
**Files analyzed:** 3 (stubs being replaced in place)
**Analogs found:** 2 / 3 (all three share the same two analogs)

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `first-principles-thinking/references/five-whys.md` | Layer-3 on-demand reference component | request-response (invoked from SKILL.md nav-map → returns procedure output) | `first-principles-thinking/references/validation-rubric.md` | role-match (same layer, same on-demand load model; different length target) |
| `first-principles-thinking/references/pre-mortem.md` | Layer-3 on-demand reference component | request-response | `first-principles-thinking/references/validation-rubric.md` | role-match |
| `first-principles-thinking/references/trade-off-analysis.md` | Layer-3 on-demand reference component | request-response | `first-principles-thinking/references/validation-rubric.md` | role-match |

**Secondary analog for all three:** `first-principles-thinking/references/output-template.md` — shows how a completed Layer-3 reference uses its opening scope note and navigates between sections with `---` dividers.

---

## Pattern Assignments

### All three files share the same structural pattern

All three files are the same artifact type (Layer-3 on-demand reference component, no YAML frontmatter, tight sub-procedure). The pattern excerpts below apply to all three. File-specific differences are called out in the Per-Tool Variations section.

---

### Opening Pattern

**Analog:** `first-principles-thinking/references/validation-rubric.md` lines 1–9; `first-principles-thinking/references/output-template.md` lines 1–5

Both completed references open with an `H1` title followed immediately by a blockquote scope note (using `>`). The scope note orients the reader in one or two sentences: what the file is for, when to come here, and what it does NOT replace. It is tight — never more than 3 sentences.

**Rubric opening** (lines 1–9):
```markdown
# Validation Rubric

> **Scope:** This is the Layer-3 scoring instrument read on demand by the validator-fix-repeat loop
> already resident in `SKILL.md`. It scores a completed first-principles analysis against the
> six-section output format defined in `references/output-template.md`. The loop instruction
> itself — when to apply, what to fix, when to stop — lives in `SKILL.md` under
> "Before presenting conclusions" and is **not** repeated here. Come here only to score
> an analysis in progress; use `SKILL.md` for the loop procedure and `output-template.md`
> for authoring guidance.
```

**Output-template opening** (lines 1–5):
```markdown
# First Principles Analysis Output Template

> **Note:** This is the full annotated template with complete section guidance, type
> definitions, and prescriptions. A condensed skeleton showing just the required section
> names and chain format lives resident in `SKILL.md` for quick reference. Come here
> for the complete instructions when authoring or reviewing an analysis.
```

**Apply to companion tools as:** an `H1` matching the stub title (e.g., `# 5-Whys`) followed by a brief blockquote scope note: what the tool does + the trigger condition that brought the reader here. Keep to 1–2 sentences. Do NOT use `**Scope:**` as the bold label — that phrasing belongs to the rubric. Write the note in third person from the tool's perspective. The scope note is NOT the "When to reach for this" section — it is a two-line orientation before the first `H2`.

---

### Section Heading Style

**Analog:** `first-principles-thinking/references/validation-rubric.md` heading list; `first-principles-thinking/references/output-template.md` heading list

Both completed references use `##` (H2) for top-level sections. They do NOT use H3 for the primary procedure sections — H3 is reserved for sub-sections within a section (e.g., `### Type Definitions` inside `## 2. Assumptions Table`). The companion tools are tight enough (~100 lines) that sub-sections within sections are unlikely to be needed; use `**bold**` inline labels for any enumerated sub-items within a section instead.

**Rubric section headings** (from grep output):
```
## How to Apply This Rubric
## Scoring Model
## Verdict Block Format
## Criteria
### Criterion 1: Identify Essence     ← H3 only when there are 6 parallel items under one H2
```

**Output-template section headings:**
```
## How to Use This Template
## 1. Problem Essence
## 2. Assumptions Table
## 3. Ground Truths
## 4. Derivation Chains
## 5. Abandoned Reasoning
## 6. Conclusion
```

**Apply to companion tools as:** Use `##` for every named component (When to reach for this, Procedure, Example, Failure modes, Handoff). No H3 needed in files under ~100 lines. If the procedure has named sub-steps, use a numbered list with `**bold step name**` rather than promoting to H3.

---

### Section Dividers

**Analog:** `first-principles-thinking/references/validation-rubric.md` lines 31, 88, 125; `first-principles-thinking/references/output-template.md` lines 27, 38, etc.

Both completed references use `---` (horizontal rule) between major `H2` sections to create visual breathing room. The divider appears on its own line, preceded and followed by a blank line.

```markdown
## Scoring Model

[body]

---

## Verdict Block Format
```

**Apply to companion tools as:** Place `---` between every `H2` section. This is the established rhythm of the reference layer.

---

### Procedure Section: Imperative Mood, Numbered Steps

**Analog:** `first-principles-thinking/references/output-template.md` — every step uses imperative: "State the core problem," "List every assumption," "Show how the ground truths combine."

**Rubric** uses a slightly different style (scoring band definitions, not a procedure), but `output-template.md` is the cleaner model for imperative procedure writing.

The RESEARCH.md provides validated code examples for each tool's procedure section. These are the canonical patterns to copy directly:

**Five-Whys procedure excerpt** (from RESEARCH.md lines 467–486):
```markdown
## Procedure

**State the symptom.** Write one sentence: the observable problem that keeps occurring.

**Ask: Why did this happen?** Write every cause you can identify — do not filter yet.

**For each cause, ask why again.** At each level, ask "What else caused this?" before
going deeper. Multiple valid causes each become their own branch.

**Stop drilling a branch when BOTH hold:**
- You can state a specific corrective action that would prevent recurrence.
- That action is within your practical control.

If a branch produces a cause with no actionable corrective, record it and move to the
next branch. A cause outside your control is a real finding — note it, do not discard it.

**Validate each causal link** with observable evidence, not inference. If you cannot
point to evidence for a link, flag it as assumed.
```

**Pre-mortem framing block** (from RESEARCH.md lines 490–501):
```markdown
## Framing

Before any other step, adopt this premise explicitly:

> It is [date approximately 6 months from now]. This plan has failed — not
> merely underperformed, but failed badly. That outcome is a fact.
> Working backward: what caused it?

This past-tense framing is not rhetorical. It bypasses the optimism bias that makes
forward-looking risk lists generic. Do not skip it or soften it to "might fail."
```

**Trade-off weights-lock procedure** (from RESEARCH.md lines 506–518):
```markdown
## Procedure

1. **Name the options.** List each option being compared.
2. **List criteria.** Identify 5–8 criteria that matter. Lock this list — no new
   criteria after this step.
3. **Assign weights. Lock them now.** Give each criterion a relative weight
   (e.g., 1–5). Lock the weights before scoring any option. If you cannot assign
   weights without looking at how options score, you are not ready to use this tool.
4. **Score each option** on each criterion independently (e.g., 1–5).
5. **Compute:** weight × score per criterion; sum per option.
6. **Read the result** and check: if it surprises you, re-examine the weights
   — but only if you can state why a weight was wrong before seeing the result.
```

**Apply to all three files as:** Write the Procedure section in imperative mood (second person or direct command). Use numbered lists for sequential steps; use `**bold label**` + period for named steps that are not purely sequential. Never use passive voice ("the analyst identifies...") or third person ("one should ask...").

---

### Handoff Section Pattern

**Analog:** No direct analog exists in the shipped references — the handoff is a new pattern for Phase 4. The RESEARCH.md defines the shape exactly.

The handoff is 1–3 sentences only (RESEARCH.md Pitfall 5 warning: "more than 3–4 lines" is a warning sign). It names: (1) what the tool's output is, (2) which phase of the 5-phase methodology it feeds, and (3) which artifact it contributes to.

**Pattern from RESEARCH.md** (lines 451–454):
```markdown
## Handoff

Return to the 5-phase methodology. The root cause(s) identified here feed Phase 2
(Challenge Assumptions) — add each root cause as a challenged assumption row in the
Classified Assumptions Table.
```

**Apply to each file as:**
- `five-whys.md`: Feed Phase 2 (Challenge Assumptions) or Phase 4 (Reason Upward) depending on where the analysis is stuck. Name the artifact (Assumptions Table or derivation chain).
- `pre-mortem.md`: Feed Phase 5 (Validate). Name the artifact (the validation pass on the proposed conclusion).
- `trade-off-analysis.md`: Feed Phase 4 (Reason Upward). Name the artifact (the derivation chain selecting between viable options).

The handoff must not re-explain what Phase 2, 4, or 5 does. It is a pointer, not a summary.

---

### No YAML Frontmatter

**Analog:** Both `validation-rubric.md` and `output-template.md` open directly with `# Title` — no `---` frontmatter block, no `name:`, no `description:`.

The stub files confirm this: all three stubs open with `# Title` and no frontmatter.

**Apply to all three files as:** The very first character of each authored file is `#`. No `---` block appears anywhere before the title. This is SC-4 and is non-negotiable.

---

## Per-Tool Variations

These are the D-01 per-tool structural differences. The shared patterns above apply to all three; these override or extend for each file.

### `five-whys.md`

**Section order** (from RESEARCH.md architecture pattern):
1. `## When to reach for this` — use-case + contrast (when NOT to use)
2. `## Procedure` — branching drill-down with test-based stop criterion (bold-step format, not numbered)
3. `## Example` — mini-example with a recurring household problem (bread going stale, or equivalent)
4. `## Failure modes`
5. `## Handoff`

**Critical discipline to encode in Procedure:** The stop criterion is the Corrective Action Test, not a count. The word "five" must not appear as a stop rule. The branching requirement ("What else caused this?") must appear at each level.

**Example shape:** Show as a nested bullet list (symptom → first-level causes → second-level causes per branch) ending at the branch that reaches the corrective action. Annotate which branch triggers the stop criterion.

### `pre-mortem.md`

**Section order** (from RESEARCH.md — pre-mortem has an extra Framing section):
1. `## When to reach for this`
2. `## Framing` — the grammatical shift (mandatory first step; blockquote the premise)
3. `## Procedure` — independent write → share → pattern
4. `## Example`
5. `## Failure modes`
6. `## Handoff`

**Critical discipline to encode in Framing:** The past-tense framing instruction is a mandatory step, not an optional context note. The blockquoted premise uses past tense: "has failed," not "might fail." The word "already" or an equivalent does work that "could happen" cannot.

**Solo adaptation note:** Pre-mortem is solo-compatible (Claude applies it alone). The procedure is written for solo use; group facilitation notes belong in Failure modes as a contrast, not as the primary framing.

### `trade-off-analysis.md`

**Section order** (from RESEARCH.md):
1. `## When to reach for this`
2. `## Procedure` — weights locked before scoring (the weights-lock step is step 3, mandatory)
3. `## Example`
4. `## Failure modes`
5. `## Handoff`

**Critical discipline to encode in Procedure:** Weights are locked at step 3, before any option is scored at step 4. The word "lock" or "finalize" must appear at the weights step. The sensitivity check (near-tie → identify the swing criterion) belongs either at the end of the Procedure or as a note after step 6.

**Example shape:** Show a compact table (options as rows, criteria as columns, with weight row and score rows). Keep to 3 options × 4–5 criteria maximum to stay within the line budget.

---

## Shared Patterns

### No YAML Frontmatter (SC-4)
**Source:** `first-principles-thinking/references/validation-rubric.md` line 1; `first-principles-thinking/references/output-template.md` line 1
**Apply to:** All three companion tool files — non-negotiable.
```markdown
# [Tool Name]
```
File begins with `#` — no `---` block above it.

### Blockquote Scope Note (Opening)
**Source:** `first-principles-thinking/references/validation-rubric.md` lines 3–9
**Apply to:** All three companion tool files
```markdown
> [1–2 sentence orientation: what this file is, when to come here.]
```

### Section Dividers
**Source:** `first-principles-thinking/references/validation-rubric.md` (between every H2 section)
**Apply to:** All three companion tool files — `---` between every `##` section.

### Imperative Procedure Prose
**Source:** `first-principles-thinking/references/output-template.md` (every step: "State...", "List...", "Show...")
**Apply to:** The `## Procedure` section of all three files. Second person or direct command; never passive or third person.

### Handoff as Pointer Only
**Source:** RESEARCH.md lines 451–454 (Pitfall 5 pattern)
**Apply to:** The `## Handoff` section of all three files — 1–3 sentences: output → target phase → artifact. No re-explanation of the target phase.

---

## No Analog Found

| File | Role | Component | Reason |
|------|------|-----------|--------|
| All three files — `## Handoff` section | reference component | handoff pointer | No completed reference in the codebase yet has a handoff section pointing back to the resident methodology. The handoff is a new pattern for Phase 4. RESEARCH.md Pitfall 5 defines the shape; use that directly. |

---

## Metadata

**Analog search scope:** `first-principles-thinking/references/` (all files), `first-principles-thinking/SKILL.md`
**Files scanned:** 5 (`validation-rubric.md`, `output-template.md`, `five-whys.md` stub, `pre-mortem.md` stub, `trade-off-analysis.md` stub, `SKILL.md`)
**Pattern extraction date:** 2026-05-17
