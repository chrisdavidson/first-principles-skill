# Phase 2: SKILL.md Skeleton and Frontmatter — Research

**Researched:** 2026-05-16
**Domain:** Agent Skills file format — YAML frontmatter authoring, SKILL.md body composition, stub file conventions
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** Skill `name` is `first-principles-thinking`. Lives at `<repo>/first-principles-thinking/SKILL.md`. Repo root stays free for future collection.
- **D-02:** `metadata.version` is `"2.0"` (quoted string, under `metadata` key — never a top-level `version:` key).
- **D-03:** Trigger phrases are port-and-extend: keep the original skill's English trigger phrases, then add phrases for the extended capabilities. Chinese triggers are dropped (D-04).
- **D-04:** Triggers are English-only. Chinese trigger phrases are explicitly dropped.
- **D-05:** Output template split: condensed skeleton (section list + key shape rules) stays resident in `SKILL.md` body. Full annotated template moves to `references/output-template.md`. The `references/output-template.md` file is real content this phase (not a stub).
- **D-06:** Phase 1 methodology embeds essentially verbatim (92 lines) — only mechanical framing adaptation allowed (heading levels, intro sentence). No `methodology-deep-dive.md` split needed.
- **D-07:** Phase 2 creates stub files now for all not-yet-built Layer-3 files so nav-map links resolve immediately.
- **D-08:** Each stub is a descriptive placeholder — `#` heading + 1–2 sentences naming the file's future content and authoring phase. Stubs carry NO YAML frontmatter.
- **D-09:** VALID-05 validator-fix-repeat instruction is fully written into the `SKILL.md` body this phase, linking to `references/validation-rubric.md` with a real, resolving link.

### Claude's Discretion

- Exact wording of the `description` (third person, what+when, within budget) and the specific extended English trigger phrases beyond the ported originals.
- The `SKILL.md` body heading structure and any quick-reference checklist.
- Exactly which output-template shape rules make the resident condensed skeleton vs. live only in the full `references/output-template.md`.
- The example stub filenames — research recommends `examples/software-systems.md`, `product-business.md`, `personal-general.md`, `science-engineering.md`.
- The mechanical framing adaptation when `methodology.md` is embedded.

### Deferred Ideas (OUT OF SCOPE)

None from discussion. Authoring the rubric, companion tools, worked examples, final nav-map link audit, README, and schema validation are all later phases (3–6). Phase 2 only creates their stub slots.

</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| FOUND-01 | `SKILL.md` has valid YAML frontmatter (`name`, `description`, `metadata.version`) conforming to the Agent Skills schema | Frontmatter schema section below provides exact constraints; recommended frontmatter block is verbatim-ready |
| FOUND-02 | The `description` field triggers reliably — states what/when, with explicit English trigger phrases, within the budget | Trigger phrase inventory (ported + extended) provided; budget arithmetic verified |
| FOUND-03 | The `SKILL.md` body stays under 500 lines, with depth content pushed to `references/` and `examples/` | Line budget arithmetic shows comfortable headroom; content allocation rules prescribe what stays resident |
| VALID-05 | `SKILL.md` instructs Claude to apply the rubric as a validator → fix → repeat feedback loop | VALID-05 instruction pattern documented; links to `references/validation-rubric.md` which exists as a stub after this phase |

</phase_requirements>

---

## Summary

Phase 2 builds the installable shell of the skill — the YAML frontmatter that triggers discovery, the SKILL.md body that carries the resident methodology, and the stub directory structure that prevents broken links throughout the build. This is a content-assembly and wiring phase: the methodology content (Phase 1 output) is already written; this phase places it correctly inside the Agent Skills file format and wires the navigation map.

The primary technical research domain is the Agent Skills frontmatter schema and the description-as-trigger pattern. The schema is well-specified and the constraints are tight: `name` must match the directory name exactly, `description` drives all triggering and has a 1,024-char hard cap, and the `SKILL.md` body has a 500-line target for optimal performance. The original skill's trigger phrases have been retrieved verbatim from the source repo and are ready to port forward.

The body budget arithmetic is favorable. The Phase 1 methodology is 92 lines; the full output-template is 145 lines but only a condensed skeleton (estimated 20–30 lines) stays resident. With frontmatter, heading structure, the nav map, and the VALID-05 instruction, the body should land comfortably in the 220–280-line range — well under the 500-line ceiling with room for Phases 3–6 to add nav-map entries without risk.

**Primary recommendation:** Assemble `SKILL.md` in one wave: frontmatter → methodology (verbatim from methodology.md with framing adaptation) → condensed output-skeleton → VALID-05 instruction → nav map. Author `references/output-template.md` from the full `output-template.md`. Create all stubs. Verify line count before committing.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Skill discovery / triggering | Layer 1 (frontmatter) | — | `description` field is the only content loaded at session startup; it is the sole trigger mechanism |
| Always-resident methodology procedure | Layer 2 (SKILL.md body) | — | Must stay in context for the entire analysis session — resident by design |
| Condensed output template skeleton | Layer 2 (SKILL.md body) | Layer 3 (references/output-template.md) | Shape rules stay resident; full annotated template is on-demand |
| Validator-fix-repeat instruction | Layer 2 (SKILL.md body) | Layer 3 (references/validation-rubric.md) | The instruction is always-resident; the rubric content it points to is on-demand |
| Navigation map | Layer 2 (SKILL.md body) | — | Pointers to Layer 3 files live resident; the pointed-to files are on-demand |
| Full annotated output template | Layer 3 (references/) | — | On-demand depth; too long to carry as resident content |
| Validation rubric content | Layer 3 (references/) | — | Applied at one moment (Phase 5 Validate); zero token cost until read |
| Companion tool content | Layer 3 (references/) | — | Invoked situationally; one file per tool for minimal load |
| Worked examples | Layer 3 (examples/) | — | Calibration material; one file per domain for targeted load |

---

## Standard Stack

This phase has no installable packages — it is pure Markdown authoring. The "stack" is the file format specification and the content being assembled.

### Core

| Component | Version/Source | Purpose | Why This |
|-----------|---------------|---------|---------|
| Agent Skills open standard | Current (agentskills.io) | Governs SKILL.md frontmatter schema and directory layout | The authoritative, cross-client format; authoring to it keeps the skill portable |
| YAML 1.2 frontmatter | n/a | The `---`-delimited metadata block at the top of SKILL.md | Required by the spec; only the frontmatter is schema-constrained |
| CommonMark Markdown | n/a | SKILL.md body + all references/ and examples/ files | No format restrictions on the body beyond what CommonMark provides |
| Phase 1 `methodology.md` | Local — `.planning/phases/01-.../methodology.md` | Source content for the resident methodology (92 lines, embeds verbatim per D-06) | Phase 1 output; embedding verbatim preserves the rigor that was already hardened |
| Phase 1 `output-template.md` | Local — `.planning/phases/01-.../output-template.md` | Source content for both the condensed skeleton (resident) and `references/output-template.md` (full) | Phase 1 output; D-05 specifies this split |

### Package Legitimacy Audit

Not applicable — this phase installs no packages and creates no code files. The only "dependencies" are the Phase 1 Markdown files already present in the repo and the Agent Skills spec document.

---

## Architecture Patterns

### System Architecture Diagram

```
Original skill description (GitHub source)
        ↓  [port English trigger phrases]
D-03 trigger phrase inventory
        ↓  [assemble description: what + when + triggers]
SKILL.md YAML frontmatter
  name: first-principles-thinking
  description: [assembled, ≤1024 chars]
  metadata.version: "2.0"
        ↓
SKILL.md body (Layer 2, always-resident)
  ├── methodology.md (92 lines) → [embed verbatim + framing]
  ├── condensed output skeleton (20–30 lines) ──────────────────────→ references/output-template.md (full, 145 lines)
  ├── VALID-05 validator-fix-repeat instruction ─────────────────────→ references/validation-rubric.md (stub → Phase 3)
  └── navigation map
        ├── references/validation-rubric.md ──────────────────────── [stub]
        ├── references/five-whys.md ──────────────────────────────── [stub]
        ├── references/pre-mortem.md ─────────────────────────────── [stub]
        ├── references/trade-off-analysis.md ─────────────────────── [stub]
        ├── examples/software-systems.md ─────────────────────────── [stub]
        ├── examples/product-business.md ─────────────────────────── [stub]
        ├── examples/personal-general.md ─────────────────────────── [stub]
        └── examples/science-engineering.md ──────────────────────── [stub]
```

Arrows show what each body section links to at runtime (one level deep, all resolve immediately after this phase).

### Recommended Project Structure

```
first-principles-thinking/          # directory name MUST match frontmatter `name`
├── SKILL.md                        # Layer 1 + 2: frontmatter + resident body
└── references/
│   ├── output-template.md          # REAL content this phase (from Phase 1 output-template.md)
│   ├── validation-rubric.md        # STUB → Phase 3 authors
│   ├── five-whys.md                # STUB → Phase 4 authors
│   ├── pre-mortem.md               # STUB → Phase 4 authors
│   └── trade-off-analysis.md       # STUB → Phase 4 authors
└── examples/
    ├── software-systems.md         # STUB → Phase 5 authors
    ├── product-business.md         # STUB → Phase 5 authors
    ├── personal-general.md         # STUB → Phase 5 authors
    └── science-engineering.md      # STUB → Phase 5 authors
```

Note: `README.md` and `LICENSE` are NOT Phase 2 deliverables — Phase 6 authors the README. Do not create them here.

---

## Frontmatter Schema (Prescriptive)

All constraints are HIGH confidence — verified against the Agent Skills open standard and Claude Code official documentation.

### Required Fields

| Field | Hard Constraint | For This Skill |
|-------|----------------|----------------|
| `name` | 1–64 chars; lowercase letters, numbers, hyphens only; no leading/trailing/consecutive hyphens; **must equal parent directory name** | `first-principles-thinking` — matches D-01, carries the literal trigger phrase, avoids reserved words `anthropic`/`claude` |
| `description` | 1–1024 chars; non-empty; **no XML tags**; **third person** | See "Description & Trigger Phrases" section below |

### Recommended Optional Fields

| Field | Setting | Rationale |
|-------|---------|-----------|
| `metadata.version` | `"2.0"` (quoted string) | D-02: signals enhanced successor to original 1.x; `metadata` is spec-sanctioned home for arbitrary keys |
| `license` | `MIT` | Matches original repo's license |

### Fields Explicitly NOT Used

| Field | Why Not |
|-------|---------|
| `when_to_use` | Description alone can carry the triggers within budget — using `when_to_use` reduces the hard-cap headroom for `description` without benefit |
| `disable-model-invocation` | Would prevent Claude from auto-loading the skill — defeats purpose |
| `context: fork` | Runs in isolated subagent with no conversation history — wrong for a methodology reasoning about the current conversation |
| `model`, `effort` | Hard-coding these in a reusable skill is inappropriate |
| `paths` | Skill is domain-agnostic — glob-scoping would suppress triggering |
| `hooks`, `shell` | No executable behavior in a pure-Markdown skill |
| Top-level `version:` | Not in the schema; may be ignored or flagged by validators |

### Recommended Frontmatter Block

```yaml
---
name: first-principles-thinking
description: >-
  Decomposes any problem into verified fundamental truths and reasons upward
  from them instead of by analogy or convention. Use when the user wants to
  analyze from first principles, think from scratch, question a design,
  challenge assumptions, is this the right approach, why are we doing it this
  way, is there a better solution, evaluate an architectural decision, justify
  a decision from ground truths, apply a pre-mortem or 5-Whys, or asks
  whether reasoning is sound. Make sure to use this skill whenever the user
  wants to avoid reasoning by analogy or convention, even if they do not
  explicitly say "first principles".
license: MIT
metadata:
  version: "2.0"
---
```

This draft is within the 1,024-char hard cap. The planner should verify the final character count before committing; the `>-` scalar strips newlines to a single line when parsed.

---

## Description & Trigger Phrases

### Budget Arithmetic

| Budget | Value | Source |
|--------|-------|--------|
| `description` hard cap | 1,024 chars | Agent Skills spec |
| Combined `description` + `when_to_use` truncation | 1,536 chars | Claude Code listing cap |
| Target (leave headroom) | ≤ 900 chars for `description` | ~12% safety margin; space for future polish |

Since Phase 2 does not use `when_to_use`, the entire 1,024-char budget is available for `description`.

### Original Skill's English Trigger Phrases (Verbatim, Source-Fetched)

[VERIFIED: github.com/chrisdavidson/first-principles-skill/SKILL.md — fetched this session]

The original `description` field contained the following English triggers (Chinese phrases are dropped per D-04):

- `analyze from first principles`
- `think from scratch`
- `question this design`
- `is this the right approach`
- `why are we doing it this way`
- `is there a better solution`
- `challenge assumptions`

The original skill's `name` is `First Principles Thinking` (with spaces and caps — this is an old format not conforming to the current open-standard `name` constraint of lowercase-alnum-hyphen). The v2 `name` `first-principles-thinking` is correct for the current schema.

### Extended English Trigger Phrases (Claude's Discretion — Recommended)

These cover the v2 enhanced capabilities not in the original:

- `evaluate a design` / `evaluate this architecture` — covers the explicit "evaluate architectural decisions" use case
- `justify this decision from first principles` — covers the traceability requirement
- `apply a pre-mortem` / `run a pre-mortem` — companion tool now usable as sub-procedure
- `apply 5-Whys` / `run a 5-Whys` — companion tool now usable as sub-procedure
- `is this reasoning sound` / `check whether this reasoning is sound` — covers the validation rubric use case
- `reason from scratch` — natural synonym for "think from scratch"

**Description writing rules:**
1. Third person only (`"Decomposes..."` not `"I can help you..."`).
2. State what it does first, then "Use when..." clause.
3. Include the literal words users type — front-loaded.
4. Be "pushy" against under-triggering: include a clause like "Make sure to use this skill whenever the user wants to avoid reasoning by analogy or convention, even if they do not explicitly say 'first principles'." [CITED: anthropics/skills skill-creator guidance]
5. No XML tags in the description.

---

## Body Composition & Line Budget

### Budget Arithmetic

| Component | Line Count | Status |
|-----------|-----------|--------|
| Phase 1 `methodology.md` (embeds verbatim per D-06) | 92 | Measured |
| Full `output-template.md` (Phase 1 output) | 145 | Measured |
| Condensed output skeleton (resident, per D-05) | ~20–30 | Estimated — section headings + key shape rules only |
| Frontmatter + document heading | ~8 | Estimated |
| VALID-05 validator-fix-repeat instruction | ~8–12 | Estimated — a short paragraph + link |
| Navigation map section | ~20–25 | Estimated — headings + bullet links to 8 Layer-3 files |
| **Total body estimate** | **~150–170 lines** | Comfortably under 500 |

The 500-line ceiling is safe. Even with generous heading structure and a quick-reference checklist (Claude's discretion), the body should not exceed ~250 lines.

### What Stays Resident vs. Goes to `references/output-template.md`

| Content | Stays Resident in SKILL.md | Goes to references/output-template.md |
|---------|---------------------------|---------------------------------------|
| The 6 required section names in fixed order | Yes — core shape the model needs always | — |
| The honest-depth escape valve instruction ("Nothing material here — [reason]") | Yes — a core rule that applies throughout | — |
| The derivation-chain format (`GT-N + GT-M → intermediate → conclusion`) | Yes — essential inline reference | — |
| The `GT-N?` unverified notation | Yes — used throughout the methodology | — |
| Section-by-section prompt text and placeholder examples | No | Yes |
| Full type-definitions table for assumption types | No (summary reference in methodology suffices) | Yes |
| Verdict vocabulary and stakes-escalation wording | No | Yes |

---

## VALID-05 Instruction Pattern

The validator-fix-repeat instruction must be explicit and must link to `references/validation-rubric.md`. A recommended body pattern:

```markdown
## Before presenting conclusions

Score the completed analysis against the rubric in
[references/validation-rubric.md](references/validation-rubric.md):

1. **Validate** — apply each rubric criterion; quote the specific span
   of your analysis that satisfies or fails it.
2. **Fix** — revise any criterion that does not pass.
3. **Repeat** — re-score until every criterion passes the gate.

Do not present conclusions until the rubric gate is cleared.
```

This is a stub-compatible instruction — it links to `references/validation-rubric.md` which exists as a stub from Phase 2, and Phase 3 fills it. The instruction is complete now; the rubric content arrives later.

---

## Stub File Convention (D-07, D-08)

### Format

Every stub is:
1. A `#` heading matching the file's future content
2. One or two sentences: (a) what the file will contain, (b) which phase authors it
3. NO YAML frontmatter (explicitly required by Phase 4 SC4 — companion tool files must not carry their own frontmatter)
4. Plain CommonMark, UTF-8, LF line endings, forward-slash paths

### Stub Template

```markdown
# [File Title]

[Description of what this file will contain]. Authored in Phase [N].
```

### Recommended Stub Filenames and Content

| File | Stub Heading | Stub Body |
|------|-------------|-----------|
| `references/validation-rubric.md` | `# Validation Rubric` | The falsifiable self-check scoring rubric — 6–8 analytic criteria covering the 5 phases and traceability, with named levels (Rigorous/Adequate/Hand-wavy/Absent) and a gate scoring model. Authored in Phase 3. |
| `references/five-whys.md` | `# 5-Whys` | A self-contained root-cause drill-down procedure — when to use it, a branching procedure with a test-based stop criterion, a mini-example, failure modes, and a handoff to the 5-phase spine. Authored in Phase 4. |
| `references/pre-mortem.md` | `# Pre-Mortem` | A prospective-hindsight failure analysis procedure — the framing instruction, a procedure, a mini-example, failure modes, and a handoff to Phase 5 (Validate). Authored in Phase 4. |
| `references/trade-off-analysis.md` | `# Trade-Off Analysis` | A structured option-comparison procedure — weighted criteria before scoring, a mini-example, failure modes, and a handoff to the 5-phase spine. Authored in Phase 4. |
| `examples/software-systems.md` | `# Worked Example: Software and Systems` | A complete first-principles analysis of a software or systems design question, following the standardized output format and showing at least one abandoned reasoning path. Authored in Phase 5. |
| `examples/product-business.md` | `# Worked Example: Product and Business` | A complete first-principles analysis of a product or business decision, following the standardized output format and showing a dead-end. Authored in Phase 5. |
| `examples/personal-general.md` | `# Worked Example: Personal and General` | A complete first-principles analysis of a personal or general decision, following the standardized output format and showing a dead-end. Authored in Phase 5. |
| `examples/science-engineering.md` | `# Worked Example: Science and Engineering` | A complete first-principles analysis of a science or engineering question, following the standardized output format and showing a dead-end. Authored in Phase 5. |

---

## Navigation Map Pattern

The navigation map is the "table of contents" section of the SKILL.md body. It names each Layer-3 file, states what it contains, and says when to open it. All links must be relative, forward-slash, one level deep from SKILL.md.

Example structure for the nav map (Claude's discretion on exact wording):

```markdown
## Companion thinking tools

Reach for a companion tool when the analysis needs it:

- **Stuck on why something is true** → [references/five-whys.md](references/five-whys.md) — root-cause drill-down procedure
- **Stress-testing a proposed solution** → [references/pre-mortem.md](references/pre-mortem.md) — prospective-hindsight failure analysis
- **Choosing between viable options** → [references/trade-off-analysis.md](references/trade-off-analysis.md) — weighted trade-off procedure

## Validation

Before presenting conclusions, apply the rubric in
[references/validation-rubric.md](references/validation-rubric.md) as a validator → fix → repeat loop.

## Output template (full)

The condensed section list above is the required shape. For full annotated guidance on each section, see
[references/output-template.md](references/output-template.md).

## Worked examples

Match the domain, then read the relevant example to calibrate format and rigor:

- Software and systems → [examples/software-systems.md](examples/software-systems.md)
- Product and business → [examples/product-business.md](examples/product-business.md)
- Personal and general → [examples/personal-general.md](examples/personal-general.md)
- Science and engineering → [examples/science-engineering.md](examples/science-engineering.md)
```

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Trigger phrase coverage | A custom triggering mechanism or keywords list outside the description | The `description` field's what+when pattern with literal trigger phrases | This is exactly what the `description` field is designed for; adding any meta-layer is scope creep |
| Versioning | A top-level `version:` frontmatter key | `metadata.version: "2.0"` | Top-level `version:` is not in the schema and may be flagged by validators |
| Cross-file navigation | A scripted link-checker | `skills-ref validate` (Phase 6) + manual review | Pure-Markdown phase; no scripts |
| Description character counting | Manual estimation | `echo -n "string" | wc -c` or equivalent | Fast, accurate, eliminates budget guessing |

---

## Common Pitfalls

### Pitfall 1: Description missing the "Use when..." clause

**What goes wrong:** The description is a label ("First-principles thinking methodology") with no trigger situations. Claude never fires the skill.
**Why it happens:** Authors write descriptions as names, not selection instructions.
**How to avoid:** Follow the `<what it does>. Use when <concrete situations>.` pattern. Verify with `/doctor` in Claude Code.
**Warning signs:** Description is a noun phrase; no situational language present.

### Pitfall 2: `name` field does not match directory name

**What goes wrong:** The `name` frontmatter value and the actual directory name differ. `skills-ref validate` fails; Claude Code may not discover the skill.
**Why it happens:** Easy to forget the open-standard constraint that name must equal dirname.
**How to avoid:** The directory must be named `first-principles-thinking` to match `name: first-principles-thinking`. Create the directory with this exact name from the start.
**Warning signs:** `skills-ref validate` returns a name≠dirname error.

### Pitfall 3: Stub files carrying YAML frontmatter

**What goes wrong:** A stub file like `references/five-whys.md` gets a `name:` / `description:` frontmatter block, making it look like an independent skill. Phase 4 Success Criterion 4 and Phase 2 D-08 both prohibit this.
**Why it happens:** Copy-paste from SKILL.md templates.
**How to avoid:** Stubs are plain Markdown with NO `---` frontmatter blocks. The stub format is: `#` heading + 1–2 sentences only.

### Pitfall 4: methodology.md embedded with re-sharpening

**What goes wrong:** The implementer "improves" the methodology prose while embedding it, introducing drift from the Phase 1 hardened content.
**Why it happens:** Small wording improvements look harmless. They break the Phase 1 test-run traceability and may introduce regressions.
**How to avoid:** D-06 is explicit: embed essentially verbatim, mechanical framing adaptation only (heading levels, intro sentence). Mark as "adapted from Phase 1 methodology.md" in a comment or note if needed. Re-sharpening happens in a future phase, not during embedding.

### Pitfall 5: VALID-05 instruction referencing a rubric that doesn't exist yet

**What goes wrong:** The instruction links to `references/validation-rubric.md` but the stub file was not created, so the link is broken. Phase 6's link audit will catch it, but broken links are confusing earlier.
**How to avoid:** D-09 and D-07 together ensure this: create the stub first, then write the instruction. The planner should sequence stub creation before VALID-05 instruction authoring.

### Pitfall 6: Description over the 1,024-char hard cap

**What goes wrong:** The description is silently truncated or the schema validator rejects it.
**How to avoid:** Measure the assembled description string before finalizing: `echo -n "..." | wc -c`. Target ≤ 900 chars for a safety margin.

---

## Code Examples

### Correct frontmatter block

```yaml
---
name: first-principles-thinking
description: >-
  Decomposes any problem into verified fundamental truths and reasons upward
  from them instead of by analogy or convention. Use when the user wants to
  analyze from first principles, think from scratch, question a design,
  challenge assumptions, is this the right approach, why are we doing it this
  way, is there a better solution, evaluate an architectural decision, justify
  a decision from ground truths, apply a pre-mortem or 5-Whys, or asks
  whether reasoning is sound. Make sure to use this skill whenever the user
  wants to avoid reasoning by analogy or convention, even if they do not
  explicitly say "first principles".
license: MIT
metadata:
  version: "2.0"
---
```

[CITED: Agent Skills open standard spec + Claude Code docs frontmatter reference]

### Stub file format (no frontmatter)

```markdown
# Validation Rubric

The falsifiable self-check scoring rubric — 6–8 analytic criteria covering the
5 phases and traceability, with named levels (Rigorous / Adequate / Hand-wavy /
Absent) and a gate scoring model. Authored in Phase 3.
```

[CITED: D-08 from 02-CONTEXT.md]

### VALID-05 instruction (inline body pattern)

```markdown
## Before presenting conclusions

Score the completed analysis against the rubric in
[references/validation-rubric.md](references/validation-rubric.md) as a feedback loop:

1. **Validate** — apply each rubric criterion; quote the specific span of your
   analysis that satisfies or fails each criterion.
2. **Fix** — revise every criterion that does not pass.
3. **Repeat** — re-score after fixing until every criterion clears the gate.

Do not present conclusions until the rubric gate is cleared.
```

[CITED: D-09 from 02-CONTEXT.md; validator-loop pattern from official best-practices]

### Measuring the description character count

```bash
echo -n "Decomposes any problem into verified fundamental truths..." | wc -c
```

---

## State of the Art

| Old Pattern | Current Pattern | Notes |
|-------------|----------------|-------|
| Original `name: First Principles Thinking` (spaces + caps) | `name: first-principles-thinking` (lowercase-alnum-hyphen) | Open standard's `name` constraint requires lowercase + hyphens only; the original predates this constraint |
| Chinese trigger phrases in `description` | English-only triggers (D-04) | User decision; not a format change |
| `version: 0.2.0` as top-level frontmatter key (original skill) | `metadata: { version: "2.0" }` (nested under metadata) | Top-level `version:` not in the schema; `metadata` is the spec-sanctioned location |
| Triggers embedded as a comma-separated phrase-list in `description` | Structured `<what it does>. Use when <situations>.` description pattern | Current best practice; the "use when" clause is the highest-leverage change |

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The condensed output skeleton can be expressed in 20–30 lines | Body Composition & Line Budget | Body could run longer; still within 500-line ceiling with ample margin, so low risk |
| A2 | The recommended description draft is under 1,024 chars | Frontmatter Schema | Description would need trimming before commit; planner should include a character-count verification step |

**All other claims in this research were verified or cited — no further user confirmation needed.**

---

## Open Questions

1. **Exact condensed output-skeleton wording**
   - What we know: the condensed skeleton must include the 6 required section names, the `GT-N?` notation, and the derivation-chain format — these are the shape rules a reader needs without the full annotations.
   - What's unclear: the exact line count of the condensed version will depend on how much annotation is stripped. This is Claude's discretion per the context decisions.
   - Recommendation: the planner should direct the implementer to strip all "Type Definitions," "Verdict Vocabulary," and prose explanation from the template, keeping only headings + one-line descriptions + format examples. Measure the result and verify it fits.

2. **Whether to include a quick-reference checklist in the body**
   - What we know: CLAUDE.md mentions a "quick-reference checklist" as a possible body element; it is Claude's discretion.
   - What's unclear: a checklist would add 10–20 lines and may overlap with the VALID-05 instruction.
   - Recommendation: omit from Phase 2 body; if needed, it can be added in Phase 6's final pass when the full nav map is wired and line count is confirmed.

---

## Environment Availability

Step 2.6: SKIPPED — Phase 2 is pure Markdown content authoring with no external tool dependencies beyond a text editor. No runtimes, databases, or CLI tools are required to write the files.

Note for planner: `skills-ref validate` is the Phase 6 validation tool. Phase 2 does not run it; Phase 6 does.

---

## Validation Architecture

### Test Framework

Phase 2 has no automated test framework — it is a content-authoring phase. Validation is structural, not behavioral.

| Property | Value |
|----------|-------|
| Framework | None (content verification by inspection) |
| Config file | n/a |
| Quick run command | `wc -l first-principles-thinking/SKILL.md` |
| Full suite command | `wc -l first-principles-thinking/SKILL.md && echo -n "$(grep -A1 'description' first-principles-thinking/SKILL.md | tail -1)" | wc -c` |

### Phase Requirements → Verification Map

| Req ID | Behavior | Verification Type | Check |
|--------|----------|------------------|-------|
| FOUND-01 | SKILL.md has valid frontmatter (`name`, `description`, `metadata.version`) | Structural inspection | Confirm YAML parses; `name` value matches directory name; `metadata.version: "2.0"` present |
| FOUND-02 | `description` triggers reliably, English trigger phrases, within budget | Character count + phrase check | `echo -n "..." | wc -c` ≤ 1,024; all ported trigger phrases present; "Use when" clause present |
| FOUND-03 | SKILL.md body under 500 lines | Line count | `wc -l SKILL.md` < 500 |
| VALID-05 | Body instructs validator → fix → repeat loop with link to validation-rubric.md | Link + content check | Link `references/validation-rubric.md` resolves to the stub; loop instruction present |

### Wave 0 Gaps

No test files needed — this phase's verification is structural inspection, not automated testing. The planner should include verification steps as tasks within the implementation wave, not as separate test files.

---

## Security Domain

Not applicable — this phase authors Markdown and YAML only. There are no endpoints, user inputs, secrets, or code execution paths. The only security note from the overall research:

- Do NOT add `allowed-tools` to the frontmatter. A pure-Markdown reasoning skill needs no pre-approved tool access. Omitting `allowed-tools` is the correct and secure choice.

---

## Sources

### Primary (HIGH confidence)

- Agent Skills open standard specification — agentskills.io/specification — `name`/`description` constraints, optional fields, `skills-ref validate` tooling, directory conventions
- Claude Code official docs — code.claude.com/docs/en/skills — 500-line body budget, 1,024-char description cap, 1,536-char listing truncation, `disable-model-invocation`, skill content lifecycle
- Claude Code skill authoring best practices — platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices — description writing (third person, what+when), progressive disclosure, one-level-deep references, anti-patterns
- anthropics/skills skill-creator/SKILL.md — "pushy" description wording, `metadata.version` example, preserve-name-on-update rule
- `github.com/chrisdavidson/first-principles-skill` SKILL.md (fetched this session) — original English trigger phrases verbatim: `analyze from first principles`, `think from scratch`, `question this design`, `is this the right approach`, `why are we doing it this way`, `is there a better solution`, `challenge assumptions`
- Phase 1 `methodology.md` (local, `.planning/phases/01-.../methodology.md`) — 92-line source content for resident methodology embedding
- Phase 1 `output-template.md` (local, `.planning/phases/01-.../output-template.md`) — 145-line source content for condensed skeleton + `references/output-template.md`
- Phase 2 `02-CONTEXT.md` (local) — all locked decisions D-01 through D-09

### Secondary (MEDIUM confidence)

- `.planning/research/ARCHITECTURE.md` — 3-layer loading model, SKILL.md as table of contents pattern, one-level-deep rule, build order rationale — corroborated by official docs
- `.planning/research/STACK.md` — frontmatter schema details, versioning conventions — corroborated by official docs
- `.planning/research/PITFALLS.md` — description-never-triggers pitfall, SKILL.md bloat pitfall — corroborated by official docs
- `.planning/research/FEATURES.md` — trigger-phrase patterns, progressive disclosure — corroborated by official docs

---

## Metadata

**Confidence breakdown:**

- Frontmatter schema: HIGH — verified against official spec and official Claude Code docs
- Trigger phrases (ported): HIGH — fetched verbatim from source repo this session
- Trigger phrases (extended): MEDIUM — Claude's discretion per D-03; specific wording is a recommendation
- Body line budget: HIGH — measured from Phase 1 outputs; estimates clearly flagged as estimates
- Stub conventions: HIGH — derived directly from locked decisions D-07/D-08

**Research date:** 2026-05-16
**Valid until:** 2026-08-16 (stable spec; 90-day estimate)
