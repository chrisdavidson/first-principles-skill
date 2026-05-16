# Phase 2: SKILL.md Skeleton and Frontmatter — Pattern Map

**Mapped:** 2026-05-16
**Files analyzed:** 10 (1 primary content file + 1 full reference file + 8 stubs)
**Analogs found:** 2 / 10 (the 8 stubs have no analog — they are brand-new placeholder files)

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `first-principles-thinking/SKILL.md` | skill-entry-point (Layer 1 + 2) | content-assembly | `.planning/phases/01-.../methodology.md` (body) | content-source — embeds verbatim |
| `first-principles-thinking/references/output-template.md` | reference (Layer 3) | content-copy | `.planning/phases/01-.../output-template.md` | content-source — full copy with minor framing |
| `first-principles-thinking/references/validation-rubric.md` | stub | n/a | none | no analog — brand-new stub |
| `first-principles-thinking/references/five-whys.md` | stub | n/a | none | no analog — brand-new stub |
| `first-principles-thinking/references/pre-mortem.md` | stub | n/a | none | no analog — brand-new stub |
| `first-principles-thinking/references/trade-off-analysis.md` | stub | n/a | none | no analog — brand-new stub |
| `first-principles-thinking/examples/software-systems.md` | stub | n/a | none | no analog — brand-new stub |
| `first-principles-thinking/examples/product-business.md` | stub | n/a | none | no analog — brand-new stub |
| `first-principles-thinking/examples/personal-general.md` | stub | n/a | none | no analog — brand-new stub |
| `first-principles-thinking/examples/science-engineering.md` | stub | n/a | none | no analog — brand-new stub |

---

## Pattern Assignments

### `first-principles-thinking/SKILL.md` (skill-entry-point, content-assembly)

**Primary analog:** `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/methodology.md`
**Secondary analog for condensed skeleton:** `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/output-template.md`

This file has no codebase analog in the traditional sense — no SKILL.md exists yet. The "pattern" is an assembly operation: frontmatter from the spec (provided verbatim in RESEARCH.md) + methodology body from the Phase 1 content source + condensed output skeleton extracted from the Phase 1 output-template + VALID-05 instruction + navigation map.

**Frontmatter pattern** (from RESEARCH.md § "Recommended Frontmatter Block"):

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

Rules governing this block:
- `name` must equal the parent directory name exactly (`first-principles-thinking`)
- `description` must be third person, state what+when, ≤ 1,024 chars; measure with `echo -n "..." | wc -c`
- `metadata.version` is a quoted string; never a top-level `version:` key
- No `when_to_use`, `disable-model-invocation`, `context: fork`, `model`, `effort`, `paths`, `hooks`, `shell`, or `allowed-tools`

**Methodology body pattern** — embed from `.planning/phases/01-.../methodology.md` lines 1–93, essentially verbatim (D-06). Permitted adaptations: adjust heading levels to fit inside SKILL.md's heading hierarchy (e.g. promote `###` phases to `##` if the document structure warrants it), add a single intro sentence to seat the block inside the skill. Do not re-word, re-order, or condense any phase's content. The following excerpts show what must be preserved:

Opening framing (lines 1–3):
```markdown
This document is a **standing procedure** Claude follows whenever first-principles
thinking is required. It is not a recipe that runs once — every instruction is
written in imperative present tense to be re-applied in full on each analysis.
```

Phase connection chain (lines 6–11):
```markdown
Each phase produces a named artifact. That artifact is the entry condition for the next phase. The chain is:

> **Essence Statement** → **Classified Assumptions Table** → **Ground Truths list** → **Derivation Chains** → **signed-off analysis**
```

The four-type assumption table (lines 39–45 of methodology.md) — must stay intact:
```markdown
| Type | Prescribed Treatment |
|------|---------------------|
| **physical law** | Accept as a ground-truth candidate. Physical laws do not expire and cannot be negotiated away. |
| **current constraint** | Record the expiry conditions — what would have to change for this constraint to lift. |
| **convention** | Explicitly challenge before use. Ask whether the convention holds in this specific context or merely carries historical inertia. |
| **untested belief** | Verify, or flag as unverified. An unverified belief may be used in a derivation chain but must be visibly flagged (e.g., `GT-N?: unverified`) and any conclusion depending on it inherits an explicit confidence caveat. |
```

**Condensed output-template skeleton pattern** — extract from `.planning/phases/01-.../output-template.md` lines 13–19 and lines 94–98. Keep only:
- The 6 required section names in fixed order (lines 13–19)
- The honest-depth escape valve instruction (lines 7–10)
- The derivation-chain format example (lines 94–98)
- The `GT-N?` unverified notation rule (brief reference)

Strip from the resident version: the full Type Definitions table (lines 41–57), the Verdict Vocabulary (lines 60–64), the Stakes-Escalation Rule prose beyond one line, and all section-by-section placeholder text. Those belong in `references/output-template.md` only.

Section names to keep resident (from output-template.md lines 13–19):
```markdown
1. Problem Essence
2. Assumptions Table
3. Ground Truths
4. Derivation Chains
5. Abandoned Reasoning
6. Conclusion
```

Derivation-chain format to keep resident (from output-template.md lines 94–98):
```markdown
GT-N + GT-M → [intermediate claim] → [conclusion]
```

**VALID-05 instruction pattern** (from RESEARCH.md § "VALID-05 Instruction Pattern"):

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

**Navigation map pattern** (from RESEARCH.md § "Navigation Map Pattern"):

```markdown
## Companion thinking tools

Reach for a companion tool when the analysis needs it:

- **Stuck on why something is true** → [references/five-whys.md](references/five-whys.md)
- **Stress-testing a proposed solution** → [references/pre-mortem.md](references/pre-mortem.md)
- **Choosing between viable options** → [references/trade-off-analysis.md](references/trade-off-analysis.md)

## Output template (full)

For full annotated guidance on each section, see
[references/output-template.md](references/output-template.md).

## Worked examples

- Software and systems → [examples/software-systems.md](examples/software-systems.md)
- Product and business → [examples/product-business.md](examples/product-business.md)
- Personal and general → [examples/personal-general.md](examples/personal-general.md)
- Science and engineering → [examples/science-engineering.md](examples/science-engineering.md)
```

All link paths are relative from `first-principles-thinking/SKILL.md`, one level deep, forward-slash only.

**Body line budget:** Frontmatter (~8) + methodology verbatim (92) + condensed skeleton (~25) + VALID-05 instruction (~10) + nav map (~22) = ~157 lines. Well under the 500-line ceiling. Even with generous heading structure the body should not exceed ~230 lines.

---

### `first-principles-thinking/references/output-template.md` (reference, content-copy)

**Analog:** `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/output-template.md` (lines 1–146 — the entire file)

This file is a direct port of the full Phase 1 output-template with minor framing adaptation. The following content from the source must be preserved intact in the reference file:

Full "How to Use This Template" block (output-template.md lines 1–20) — the strict-shape rule, the honest-depth escape valve instruction, and the fixed section order list.

Complete Type Definitions and Prescribed Treatments section (output-template.md lines 41–57):
```markdown
**physical law** — a constraint imposed by physics, mathematics, or formal logic...
**current constraint** — a real limitation that applies now but could change...
**convention** — a practice or standard that exists because it has been adopted...
**untested belief** — a claim held as true that has not been empirically verified...
```

Verdict Vocabulary (output-template.md lines 60–64):
```markdown
- **Accept** — the assumption survives challenge and may be used in the analysis
- **Challenge** — the assumption is questionable; probe further before use
- **Discard** — the assumption is false or irrelevant; remove from the reasoning chain
```

Full Derivation Chains section instruction (output-template.md lines 88–110) — including the chain format, the intermediate-step requirement, and the D-07 unverified input rule.

Full Abandoned Reasoning section instruction (output-template.md lines 115–129) — including the escape valve example text.

Full Conclusion section instruction (output-template.md lines 131–146) — including the confidence caveat rule for MEDIUM/LOW conclusions.

**Framing adaptation permitted:** Add a brief note at the top indicating this is the full annotated template and that the condensed skeleton lives in SKILL.md. No other changes. Do NOT add YAML frontmatter — this is a `references/` file, not a skill.

---

### Stub Files (8 files — no analog)

All eight stub files follow the same pattern. There are no existing analogs — these are the first content files in the `references/` and `examples/` directories.

**Stub pattern** (from RESEARCH.md § "Stub File Convention"):

```markdown
# [File Title]

[Description of what this file will contain, and which phase authors it.]
```

Rules:
- NO YAML frontmatter (no `---` delimiters, no `name:`, no `description:` keys)
- Plain CommonMark, UTF-8, LF line endings
- `#` heading only (not `##` or deeper) — this is the document title
- 1–2 sentences of placeholder text: what the file will contain + authoring phase
- Must be obviously incomplete so no reader mistakes it for real content

**Per-file stub content** (from RESEARCH.md § "Recommended Stub Filenames and Content"):

`references/validation-rubric.md`:
```markdown
# Validation Rubric

The falsifiable self-check scoring rubric — 6–8 analytic criteria covering the
5 phases and traceability, with named levels (Rigorous / Adequate / Hand-wavy /
Absent) and a gate scoring model. Authored in Phase 3.
```

`references/five-whys.md`:
```markdown
# 5-Whys

A self-contained root-cause drill-down procedure — when to use it, a branching
procedure with a test-based stop criterion, a mini-example, failure modes, and
a handoff to the 5-phase spine. Authored in Phase 4.
```

`references/pre-mortem.md`:
```markdown
# Pre-Mortem

A prospective-hindsight failure analysis procedure — the framing instruction, a
procedure, a mini-example, failure modes, and a handoff to Phase 5 (Validate).
Authored in Phase 4.
```

`references/trade-off-analysis.md`:
```markdown
# Trade-Off Analysis

A structured option-comparison procedure — weighted criteria before scoring, a
mini-example, failure modes, and a handoff to the 5-phase spine. Authored in
Phase 4.
```

`examples/software-systems.md`:
```markdown
# Worked Example: Software and Systems

A complete first-principles analysis of a software or systems design question,
following the standardized output format and showing at least one abandoned
reasoning path. Authored in Phase 5.
```

`examples/product-business.md`:
```markdown
# Worked Example: Product and Business

A complete first-principles analysis of a product or business decision,
following the standardized output format and showing a dead-end. Authored in
Phase 5.
```

`examples/personal-general.md`:
```markdown
# Worked Example: Personal and General

A complete first-principles analysis of a personal or general decision,
following the standardized output format and showing a dead-end. Authored in
Phase 5.
```

`examples/science-engineering.md`:
```markdown
# Worked Example: Science and Engineering

A complete first-principles analysis of a science or engineering question,
following the standardized output format and showing a dead-end. Authored in
Phase 5.
```

---

## Shared Patterns

### No-frontmatter rule for all non-SKILL files
**Source:** CONTEXT.md D-08, RESEARCH.md § "Stub File Convention"
**Apply to:** All 9 files other than `SKILL.md` (the 4 `references/` stubs, the 4 `examples/` stubs, and `references/output-template.md`)

No file other than `SKILL.md` carries a YAML frontmatter block. Adding `---` delimiters to any `references/` or `examples/` file would make it look like an independent skill and violates Phase 4 Success Criterion 4.

### Forward-slash relative paths
**Source:** CLAUDE.md § "Technology Stack — UTF-8, LF line endings, forward-slash paths"
**Apply to:** All links in `SKILL.md` body (nav map, VALID-05 instruction)

All links from `SKILL.md` use relative paths with forward slashes: `references/five-whys.md`, `examples/software-systems.md`, etc. Never backslash, never absolute, never nested through an intermediate file.

### One-level-deep references
**Source:** CLAUDE.md § "What NOT to Use — Deeply nested references"
**Apply to:** All nav-map links in `SKILL.md`

All Layer-3 files are linked directly from `SKILL.md` — never through an intermediate file. `SKILL.md → references/five-whys.md` is correct. `SKILL.md → references/index.md → five-whys.md` is not.

### Verbatim content preservation (no re-sharpening)
**Source:** CONTEXT.md D-06, RESEARCH.md Pitfall 4
**Apply to:** The methodology body section of `SKILL.md`

The Phase 1 methodology content is embedded as-is. Only mechanical framing adaptations are allowed: adjusting heading levels so the phases nest correctly under the SKILL.md document structure, and adding one intro sentence to seat the block. Any content change — condensing, rewording, reordering — is out of scope for this phase and risks introducing regressions in the hardened Phase 1 content.

---

## No Analog Found

All 8 stub files and the directory structure itself are brand-new — the repo contains no `first-principles-thinking/` directory, no `references/` files, and no `examples/` files. The planner should use the stub pattern from RESEARCH.md (documented above) rather than any codebase analog.

| File | Role | Reason |
|------|------|--------|
| `references/validation-rubric.md` | stub | No rubric content exists anywhere in the repo yet |
| `references/five-whys.md` | stub | No companion tool content exists yet |
| `references/pre-mortem.md` | stub | No companion tool content exists yet |
| `references/trade-off-analysis.md` | stub | No companion tool content exists yet |
| `examples/software-systems.md` | stub | No worked examples exist yet |
| `examples/product-business.md` | stub | No worked examples exist yet |
| `examples/personal-general.md` | stub | No worked examples exist yet |
| `examples/science-engineering.md` | stub | No worked examples exist yet |

---

## Metadata

**Analog search scope:** Entire repo (excluding `.git`, `.venv`); only planning docs and Python scaffold exist — no skill files
**Files scanned:** `.planning/phases/01-.../methodology.md`, `.planning/phases/01-.../output-template.md`, `.planning/phases/01-.../01-CONTEXT.md`, `CLAUDE.md` (for frontmatter spec guidance)
**Pattern extraction date:** 2026-05-16
