# Phase 5: Domain-Spread Worked Examples — Pattern Map

**Mapped:** 2026-05-17
**Files analyzed:** 4 (example stub files to be filled in)
**Analogs found:** 4 / 4 (one primary structural analog for all four; `output-template.md` is the canonical pattern source)

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `first-principles-thinking/examples/software-systems.md` | worked-example document | transform (analysis → artifact chain) | `first-principles-thinking/references/output-template.md` | exact (defines the required structure) |
| `first-principles-thinking/examples/product-business.md` | worked-example document | transform (analysis → artifact chain) | `first-principles-thinking/references/output-template.md` | exact |
| `first-principles-thinking/examples/personal-general.md` | worked-example document | transform (analysis → artifact chain) | `first-principles-thinking/references/output-template.md` | exact |
| `first-principles-thinking/examples/science-engineering.md` | worked-example document | transform (analysis → artifact chain) | `first-principles-thinking/references/output-template.md` | exact |

**Secondary analog** (prose rigor and heading conventions): `first-principles-thinking/references/five-whys.md` and `first-principles-thinking/references/pre-mortem.md` — these are the most complete authored reference documents in the project and establish the prose style and ATX heading discipline the examples must match.

---

## Pattern Assignments

### All four files share one structural analog: `output-template.md`

This is a pure content-authoring phase. The "pattern to copy" is not a code pattern — it is the six-section document structure defined in `first-principles-thinking/references/output-template.md`. The same structural pattern applies to all four example files with per-file emphasis differences documented in the variant notes below.

---

### Shared Structural Pattern: Document Skeleton

**Analog:** `first-principles-thinking/references/output-template.md` (lines 17–24)

**Section order (fixed, no omissions allowed):**

```markdown
## 1. Problem Essence
## 2. Assumptions Table
## 3. Ground Truths
## 4. Derivation Chains
## 5. Abandoned Reasoning
## 6. Conclusion
```

Every example must open with the existing H1 stub heading (preserved verbatim), then follow this section order. The `##`-level headings are not optional — all six must appear even if a section uses the honest-depth escape valve.

**H1 preservation rule (lines 121–122 of RESEARCH.md):** The author replaces everything below the H1, but the H1 itself is kept exactly as it appears in the stub:

```markdown
# Worked Example: Software and Systems
# Worked Example: Product and Business
# Worked Example: Personal and General
# Worked Example: Science and Engineering
```

---

### Shared Structural Pattern: Problem Essence Section

**Analog:** `first-principles-thinking/references/output-template.md` (lines 29–36)

```markdown
## 1. Problem Essence

**Core problem:** [One sentence. Strip away implementation details and surface the underlying question.]

**Success criteria:** [Measurable, observable outcomes that would confirm the problem is solved.]
```

The Essence Statement is a single sentence naming the core question — not the symptom, not the triggering event. Success criteria must be checkable conditions a reader can verify against the final conclusion without asking for clarification. The section fails Criterion 1 of the validation rubric if the core problem restates the user's prompt rather than the re-framed underlying question.

---

### Shared Structural Pattern: Assumptions Table

**Analog:** `first-principles-thinking/references/output-template.md` (lines 40–68)

```markdown
## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| [Assumption text] | [physical law / current constraint / convention / untested belief] | [prescribed action per type] | [Accept / Challenge / Discard] | [source, or "unverified — flagged" if used in a chain] |
```

Required constraints on every row:
- **Type** must be drawn from exactly the four-type scheme: `physical law`, `current constraint`, `convention`, `untested belief`. No freeform labels.
- **Treatment** must use the vocabulary prescribed for that type (e.g., for `current constraint`: record expiry conditions; for `convention`: explicitly challenge before use).
- **Verdict** must be one of: `Accept`, `Challenge`, `Discard`.
- **Verification** must cite a specific source or say `"unverified — flagged"` — never leave blank or write `"unclear"`.
- At least one assumption must be challenged (not all `Accept`).

---

### Shared Structural Pattern: Ground Truths List

**Analog:** `first-principles-thinking/references/output-template.md` (lines 74–89)

**Verified ground truth form:**

```markdown
## 3. Ground Truths

- **GT-1** [fact text] — source: [verification source]
- **GT-2** [fact text] — source: [verification source]
```

**Unverified ground truth form (for EX-04 only — GT-5?):**

```markdown
- **GT-5?** [fact text] — unverified: [specific reason the fact could not be verified]
```

Rules:
- IDs are **stable**: once assigned, GT-3 stays GT-3 throughout the entire document. Never renumber between sections.
- No discarded assumption (Verdict: Discard from section 2) may appear in this list.
- Every verified GT must have a source citation more specific than "common knowledge."
- Only EX-04 genuinely requires `GT-N?` notation. EX-01, EX-02, EX-03 have no authentic unverifiable inputs — do not force the `?` suffix where it does not belong.

---

### Shared Structural Pattern: Derivation Chains

**Analog:** `first-principles-thinking/references/output-template.md` (lines 95–114)

```markdown
## 4. Derivation Chains

### Conclusion: [Conclusion text]

GT-N ([brief fact label]) + GT-M ([brief fact label])
→ [intermediate claim — a new inference statable from combining GT-N and GT-M but from neither alone]
→ [conclusion]

**Confidence:** HIGH
```

For chains that consume a `GT-N?` input (EX-04 only):

```markdown
**Confidence:** MEDIUM
[Name the unverified GT-N? input and state what verification would raise confidence to HIGH.]
```

Critical structural rules:
- **Every chain must have at least one intermediate step.** A chain that goes `GT-N + GT-M → conclusion` directly is structurally invalid (fails Criterion 4 scoring).
- The intermediate must be a claim that cannot be stated from either named GT alone.
- Exactly one chain per conclusion. No redundant chains restating the same conclusion.
- No analogy-as-evidence: any reference to how others solved a similar problem must be grounded in a named GT about their situation, not offered as standalone justification.
- A HIGH-confidence chain may not consume a `GT-N?` input.

---

### Shared Structural Pattern: Abandoned Reasoning Section

**Analog:** `first-principles-thinking/references/output-template.md` (lines 118–134)

```markdown
## 5. Abandoned Reasoning

### Dead End: [Name of discarded path]

**What was tried:** [Brief description of the reasoning path that was pursued.]

**Why abandoned:** [The specific failure — assumption false, contradicts a ground truth, classification too weak to anchor the chain, etc.]

**What it ruled out:** [What this dead end saves the reader from re-exploring.]
```

Rules:
- Every example must have at least one dead end (Success Criterion 2 from CONTEXT.md).
- The "Why abandoned" reason must be specific — "ran out of time" or "seemed unlikely" are invalid (would score Sound at best; potentially Hand-wavy under Criterion 4).
- If the honest-depth escape valve is used anywhere in this section, the reason must be specific to this problem — not copy-pasteable to any analysis.
- Per D-03, EX-01's Abandoned Reasoning section is the centerpiece (2 dead-ends, large section); EX-02, EX-03, EX-04 each carry 1 dead-end.

---

### Shared Structural Pattern: Conclusion Section

**Analog:** `first-principles-thinking/references/output-template.md` (lines 139–151)

```markdown
## 6. Conclusion

**Recommended approach:** [Description of the recommended course of action.]

**Key insight:** [The non-obvious finding the first-principles analysis revealed — what reasoning by analogy or convention would have missed.]

**Trade-offs acknowledged:** [What is being accepted, deprioritized, or deferred.]

**Confidence:** [HIGH / MEDIUM / LOW]
```

Rules:
- No new claims in the Conclusion. Every claim must trace to a named derivation chain in section 4 (Criterion 6).
- The Key Insight must be a non-obvious finding — not a restatement of the recommended approach.
- Confidence must match the weakest chain that contributes to the conclusion. If any chain is MEDIUM, the conclusion confidence is MEDIUM.
- MEDIUM or LOW confidence requires naming the specific `GT-N?` input and stating the verification path.

---

## Per-File Variant Notes

These notes layer on top of the shared patterns above. Each example differs only in which section carries the most depth (D-03).

### EX-01: `examples/software-systems.md` — Emphasis: Phase 1 Essence + Large Abandoned Reasoning

**Deepest sections:** Section 1 (Problem Essence re-framing: symptom→cause) and Section 5 (Abandoned Reasoning: the centerpiece).

**Essence re-framing type:** Symptom→cause. The stated triggering question ("should we move to microservices?") is replaced by the real question: "What is the actual bottleneck in the deploy cycle, and what is the minimum intervention to remove it?"

**Assumptions Table size:** 5 rows. The assumption "microservices enable faster deploys" is classified as `convention / untested belief` and receives Verdict: Challenge.

**Ground Truths:** 5 entries (GT-1 through GT-5). All are measurable/observed facts; no `GT-N?` suffix appears anywhere in EX-01.

**Derivation Chains:** 3 chains:
- Chain A: why the architecture is not the primary bottleneck
- Chain B: why the coupling problem is separable from microservices
- Chain C: what the minimum viable intervention is

All chains are qualitative. All confidence ratings are HIGH (no unverifiable inputs).

**Abandoned Reasoning:** 2 dead-ends (the largest Abandoned Reasoning section of the four examples):
1. "Split the monolith as specified" — abandoned because the anchor assumption ("microservices = faster deploys") is an untested belief that does not survive Phase 2 scrutiny.
2. "Move the test suite to a faster runner" — explored but found insufficient on its own (intermediate path, not the full solution).

**Target length band:** 350–450 lines.

**Conclusion confidence:** HIGH.

---

### EX-02: `examples/product-business.md` — Emphasis: Phase 2 Assumptions Table

**Deepest section:** Section 2 (Assumptions Table carries the analysis — 6–8 rows, all fully populated).

**Key Assumptions Table move:** The "competitors all have a free tier" statement is classified as `convention` (analogy-as-evidence attempt) with Verdict: Challenge. The Verification cell notes it cannot anchor a derivation chain without a named GT about competitor conversion economics.

**Assumptions Table size:** 6–8 rows. Every row's Verification cell must be non-generic. At minimum the following assumptions appear:
- "A free tier drives top-of-funnel growth" — untested belief, Challenge
- "Free users convert to paid at a meaningful rate" — untested belief, Challenge, Verification: "unverified — flagged"
- "Competitors' free tier economics are profitable" — untested belief, Challenge
- "All our competitors have a free tier, so we need one" — convention, Challenge, Verdict: Discard (analogy-as-evidence)
- "Adding a free tier has no opportunity cost" — untested belief (false), Discard

**Ground Truths:** 4 entries. GT-4 is the verified gap ("conversion rate for this product in this ICP segment is unknown and has not been measured") — note this is verified-as-absent, not `GT-N?`. No `GT-N?` suffix in EX-02.

**Derivation Chains:** 2–3 chains. The main chain shows how GT-4 (verified data gap) causes the conclusion to be "pilot first" rather than a binary yes/no.

**Abandoned Reasoning:** 1 dead-end: the competitor-parity argument — "Competitors have free tiers, therefore we need one." Abandoned because it is an analogy-as-evidence move without a named GT grounding competitor economics.

**Target length band:** 250–350 lines.

**Conclusion confidence:** HIGH (the "run a pilot" recommendation follows from the verified data gap; the uncertainty is in the pilot's outcome, not in the recommendation itself).

---

### EX-03: `examples/personal-general.md` — Emphasis: Phase 1 Essence (stated-goal→real-goal)

**Deepest section:** Section 1 (Problem Essence re-framing: stated-goal→real-goal).

**Essence re-framing type:** Stated-goal→real-goal. This is a different operation from EX-01's symptom→cause. The stated question ("should I take this job?") is replaced with: "Am I on a career trajectory that will let me achieve what I care about in 5–10 years, and does this offer accelerate or threaten that trajectory?"

**Tone:** Personal and human, not technical. The analysis reads as something a thoughtful person would actually do before a major life decision. Derivation chains are lighter and less arithmetic-heavy than EX-01 or EX-04.

**Assumptions Table size:** 5–6 rows. The stated-goal assumption ("the decision is about the compensation delta") receives Verdict: Discard. GT-5 is the person's explicitly stated real goal — a concrete career goal (e.g., "build expertise in distributed systems and reach principal level within 3 years"), not an abstract placeholder.

**Ground Truths:** 5 entries (GT-1 through GT-5). GT-5 is the stated real goal — verified by direct statement from the person, not by external measurement. No `GT-N?` suffix in EX-03.

**Derivation Chains:** 2–3 chains. The main chain reasons from the real goal (GT-5) and the effective compensation delta (GT-1 + GT-2 + GT-3, applying CoL and marginal tax adjustments) to a conditional recommendation.

**Abandoned Reasoning:** 1 dead-end: "Take the job — $70K more is always better." Abandoned because (a) the effective gain after CoL and tax is substantially less than $70K, and (b) the chain assumes the goal is to maximize compensation — an assumption discarded in Phase 2.

**Target length band:** 200–300 lines (lightest of the four examples).

**Conclusion confidence:** MEDIUM (conditional on partner situation and real-goal alignment).

---

### EX-04: `examples/science-engineering.md` — Emphasis: Phases 3–4 Ground Truths + Quantitative Chains + GT-N? confidence caveat

**Deepest sections:** Section 3 (Ground Truths, including the load table as derivation of GT-5?) and Section 4 (Derivation Chains with explicit unit arithmetic).

**GT-N? pattern — the structurally novel feature of EX-04:**

```markdown
- **GT-5?** Daily energy load estimate: approximately 1.5 kWh/day — unverified: actual
  usage depends on occupant behavior, seasonal variation in lighting hours and refrigerator
  duty cycle, and the actual level of "occasional AC loads." This figure cannot be verified
  without an energy-monitoring period or on-site measurement.
```

The load breakdown table (per-appliance Wh/day summing to ~1,495 Wh/day) appears in the Ground Truths section as supporting derivation of GT-5?, making the unverified input's basis visible.

**Derivation Chains — quantitative format with unit arithmetic:**

```
GT-1 (5.5 PSH) + GT-2 (0.80 derating factor) + GT-5? (1.5 kWh/day load)
→ Required daily panel output = 1.5 kWh / 0.80 = 1,875 Wh/day
→ Panel capacity = 1,875 Wh / 5.5 PSH ≈ 341 W; recommend 400 W array (17% margin for winter)

**Confidence:** MEDIUM — GT-5? (daily load estimate) is unverified. If measured load
exceeds 1.8 kWh/day consistently, upsize to 3 × 200 W panels. Verification: install
energy monitor for 30 days before finalizing system size.
```

Both main chains (panel sizing and battery sizing) consume GT-5? and therefore both end with MEDIUM confidence and an explicit verification path. This is the only example where any chain falls below HIGH confidence.

**Abandoned Reasoning:** 1 dead-end: "Size to the peak instantaneous load, not the daily energy." Abandoned because the water pump (250 W peak) runs only 30 min/day — the relevant constraint for battery and panel sizing is daily energy throughput (Wh/day), not peak instantaneous power (W). Peak power matters for inverter and wire sizing only.

**Target length band:** 350–450 lines.

**Conclusion confidence:** MEDIUM (inherits from the MEDIUM chains; verification path stated).

---

## Shared Patterns (Cross-Cutting)

### Prose Style
**Source:** `first-principles-thinking/references/five-whys.md` and `first-principles-thinking/references/pre-mortem.md`
**Apply to:** All four example files

The existing reference documents establish this project's prose register:
- Direct, active-voice sentences. No hedging filler ("it is worth noting that...").
- Procedure steps stated as imperatives or declaratives, not as possibilities.
- Short paragraphs; one idea per paragraph in discursive sections.
- Section introductory sentences state the purpose of the section, not a summary of the conclusion.
- ATX headings (`##`, `###`) are used consistently — no Setext-style underline headings.

### Honest-Depth Escape Valve
**Source:** `first-principles-thinking/references/output-template.md` (lines 12–16)
**Apply to:** Any section where no genuine content exists

```markdown
> Nothing material here — [reason explaining why this section has no content
> for this particular analysis and that the omission is justified, not lazy]
```

Constraints:
- The stated reason must be specific to this problem — not copy-pasteable to any analysis.
- The section heading must still appear (the escape valve lives under the heading, not in place of it).
- Per D-04 (no contrived demonstrations), do not force an escape valve where the problem has genuine content. None of the four examples have been scoped to use the escape valve in any section — all sections have authentic content from the scenario briefs.

### No Inline Rubric Verdict Blocks
**Source:** CONTEXT.md D-07
**Apply to:** All four example files

The rubric gate is a verification-time check against `references/validation-rubric.md`. No verdict block appears inside any example file. The examples are clean specimens of the output format, not annotated scoring exercises.

### No Companion-Tool Procedures
**Source:** CONTEXT.md D-05
**Apply to:** All four example files

5-Whys, pre-mortem, and trade-off analysis procedures do not appear in any example. Each example demonstrates exactly one thing: the six-section output format applied end-to-end.

### Encoding and Path Conventions
**Source:** `CLAUDE.md`
**Apply to:** All four example files

- UTF-8, LF line endings.
- Forward-slash paths in any cross-references (e.g., `references/output-template.md`).
- No Windows-style backslash paths.

---

## No Analog Found

All four files have a direct structural analog (`output-template.md`). No file lacks a pattern source.

The one structurally novel element — `GT-N?` notation with MEDIUM/LOW confidence chains — is fully documented in `output-template.md` (lines 83–88 and 110–114) and applies only to EX-04.

---

## Metadata

**Analog search scope:** `first-principles-thinking/references/` (all five files read), `first-principles-thinking/examples/` (all four stubs read), `first-principles-thinking/SKILL.md` (lines 1–80 read)
**Files scanned:** 10
**Pattern extraction date:** 2026-05-17
