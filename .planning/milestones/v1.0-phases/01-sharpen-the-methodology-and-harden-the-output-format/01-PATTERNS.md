# Phase 1: Sharpen the Methodology and Harden the Output Format — Pattern Map

**Mapped:** 2026-05-16
**Files analyzed:** 3 (all new — no skill files exist in this repository yet)
**Analogs found:** 0 / 3 in-repo; all patterns sourced from RESEARCH.md verified external sources

---

## Honest Statement: No In-Repo Analogs Exist

This repository currently contains only planning documents (`.planning/`), `CLAUDE.md`,
and an untouched `uv` Python scaffold. There are no existing skill files (`SKILL.md`,
`references/`, `examples/`), no application source code, and no Markdown content files
that could serve as structural analogs for the Phase 1 deliverables.

This is expected and documented in CONTEXT.md `## Existing Code Insights`:
> "The repo currently contains only planning docs (`.planning/`), `CLAUDE.md`,
> and an untouched `uv` Python scaffold."

The closest analogs are:
1. The **original external skill** (`github.com/chrisdavidson/first-principles-skill`),
   analyzed in full in RESEARCH.md — its baseline patterns are the before-state Phase 1 sharpens.
2. The **verified code examples** in RESEARCH.md `## Code Examples` — these are the
   locked patterns the planner must implement, derived from decisions D-01 through D-09.

All pattern excerpts below are sourced from RESEARCH.md, which extracted them directly from
primary sources (the fetched original SKILL.md and the locked decisions in CONTEXT.md).

---

## File Classification

| New File | Role | Data Flow | Closest Analog | Match Quality |
|----------|------|-----------|----------------|---------------|
| `methodology.md` | content-document (methodology procedure) | standing-instruction (read-once, apply repeatedly) | None in-repo. External: original `SKILL.md` phase definitions (baseline to sharpen) | no in-repo match |
| `output-template.md` | content-document (output template) | template-enforcement (strict shape, flexible depth) | None in-repo. External: original `SKILL.md` Standardized Output Format section (baseline to replace) | no in-repo match |
| `test-run-draft.md` | content-document (worked analysis draft) | analysis-trace (full methodology run with derivation chains) | None in-repo. External: `examples/architecture-review.md` from original skill (best analog for output shape) | no in-repo match |

---

## Pattern Assignments

### `methodology.md` (content-document, standing-instruction)

**Location:** `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/methodology.md`

**What it is:** The sharpened 5-phase first-principles reasoning procedure. Written as
standing instructions — not one-time steps — because skill content stays resident in
context across turns (RESEARCH.md Pitfall 1). Covers requirements METH-01, METH-02,
METH-03, METH-06, and Success Criterion 5 (Phase 4 high-freedom).

---

**Pattern: Phase Definition Block (all four required components)**

Source: RESEARCH.md `## Architecture Patterns — Pattern: Each Phase Definition Has Four Required Components`
Apply to: All five phase definitions in `methodology.md`

```markdown
### Phase N: [Name]

**Why this phase exists:** [rationale — satisfies METH-06]

**Entry criterion:** [what must be true before this phase begins]

**Operation:** [the concrete action this phase performs]

**Named artifact:** [the specific output this phase produces, referenced by name]

**Exit criterion:** [what must be true for this phase to be complete]
```

METH-01 and METH-02 are satisfied only when all five phases have all four components.
A phase definition missing any one component is incomplete.

---

**Pattern: Correct Phase Definition — Challenge Assumptions (verified full example)**

Source: RESEARCH.md `## Code Examples — Correct Phase Definition Format`
Apply to: Phase 2 definition specifically; use as the structural model for all five phases

```markdown
### Phase 2: Challenge Assumptions

**Why this phase exists:** An unchallenged assumption that is false propagates invisibly
through every later reasoning step. By explicitly classifying and testing each assumption
before establishing ground truths, the analysis prevents false premises from masquerading
as verified facts — the single most common cause of first-principles analysis that sounds
rigorous but isn't.

**Entry criterion:** The Essence Statement from Phase 1 is complete.

**Operation:** For each assumption (explicit and implicit) relevant to the problem,
classify it by type, apply the prescribed treatment, and record the verdict. When stakes
are high, push the assumption toward physical law or verified ground truth status rather
than accepting a weaker classification.

**Named artifact:** Classified Assumptions Table — a table with columns: Assumption,
Type, Treatment, Verdict, Verification.

**Exit criterion:** Every assumption in scope has a classification from the 4-type scheme
(physical law / current constraint / convention / untested belief) AND has a recorded
verdict and verification note (or explicit "unverified — flagged" per D-07).
```

---

**Pattern: Correct Phase Definition — Reason Upward (high-freedom format, D-04)**

Source: RESEARCH.md `## Code Examples — Phase 4 (Reason Upward) Definition`
Apply to: Phase 4 definition only. This phase must NOT have prescribed sub-steps.

```markdown
### Phase 4: Reason Upward

**Why this phase exists:** The methodology has established what is true (ground truths)
and what can be discarded (false assumptions). Now Claude must construct from those
truths upward to an answer. This phase is deliberately high-freedom because the right
method for combining ground truths depends entirely on the problem's structure — there
is no single "correct" way to reason upward that works across engineering, business, and
scientific domains. Prescribing sub-steps would constrain reasoning that should be
shaped by the problem, not the methodology.

**Entry criterion:** The Ground Truths list is complete (all ground truths carry IDs and
verification notes), and the Classified Assumptions Table from Phase 2 is finalized.

**Operation:** Reason upward from the ground truths toward an answer using whatever
approach the problem calls for. As you go, narrate what you are trying, what you are
building on, and why. If a reasoning path leads to a dead end, record it in the
Abandoned Reasoning section before changing course. Do not use analogies as evidence —
any reference to how others have solved similar problems must be grounded in a verified
ground truth about their situation, not used as direct justification.

**Named artifact:** Derivation Chains — one chain per conclusion, formatted as
`GT-N + GT-M → [intermediate] → [conclusion]`, with confidence levels per D-07.

**Exit criterion:** BOTH conditions must hold: (1) the problem's core question is
answered, AND (2) every conclusion offered has a complete derivation chain back to named
ground truths. Partial conclusions or incomplete chains do not exit this phase.
```

Note: The exit criterion is AND, not OR (D-05). This is documented as a medium-risk
misread in RESEARCH.md Assumptions Log item A3.

---

**Pattern: Assumption Classification — Four Types with Prescribed Treatments (D-06)**

Source: RESEARCH.md `## Architecture Patterns — Pattern: Assumption Classification Table`
Apply to: Phase 2 definition body and the output-template.md Assumptions Table section

The four types are locked by D-06. Do not substitute synonyms or add a fifth type.

| Type | Prescribed Treatment |
|------|---------------------|
| physical law | accept as a ground-truth candidate |
| current constraint | record what would change it (expiry conditions) |
| convention | must be explicitly challenged before use |
| untested belief | must be verified or flagged unverified (D-07: flag as `GT-N?: unverified` if used in a derivation chain) |

Stakes-escalation rule (D-06): the higher the stakes of the conclusion resting on an
assumption, the more that assumption must be pushed down toward physical law or verified
ground truth. Classification drives the method, it does not merely label.

---

**Pattern: Rationale Statement Quality (METH-06 compliance)**

Source: RESEARCH.md `## Common Pitfalls — Pitfall 4`
Apply to: Every phase's "Why this phase exists" field

A compliant rationale answers "what does failing this step cost the analysis?" not
"why is this step important." Warning signs of non-compliant rationales:
- Uses "in order to", "so that", or "because it is important" without stating the
  specific failure mode that omitting the step produces
- Restates the instruction in different words (circular)

Compliant example from RESEARCH.md: "Challenge assumptions because an unchallenged
assumption that is false propagates silently through every later step, making the
conclusion trace back to an error rather than a ground truth. The analysis looks rigorous
while being built on sand."

---

**Pattern: Standing Instruction Phrasing (anti-one-time-step)**

Source: RESEARCH.md `## Common Pitfalls — Pitfall 1`
Apply to: Every phase's Operation field and all body prose in `methodology.md`

Write as: "When working on this phase, do X" or imperative present tense "Do X"
Do NOT write as: "First, do X. Then do Y." sequential chains with "first/then/next"

Warning signs: Instructions use "first", "then", "next" as structural connectors rather
than "while", "when", "at this stage".

---

**Pattern: Exit Criteria Must Be Observable (not subjective)**

Source: RESEARCH.md `## Common Pitfalls — Pitfall 2`
Apply to: Every phase's Exit criterion field

Write exit criteria as observable state checks a skeptic can verify by inspecting the
artifact. Do NOT use: "confident", "satisfied", "adequate", "sufficiently" without a
concrete threshold.

Compliant form: "Exit when: each listed assumption has a classification from the 4-type
scheme AND a prescribed treatment has been applied or explicitly declined with
justification."

---

### `output-template.md` (content-document, template-enforcement)

**Location:** `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/output-template.md`

**What it is:** The strict-shape output template Claude fills in for every first-principles
analysis. Covers requirements METH-04 and METH-05. The section list is fixed and ordered;
any section may be marked `Nothing material here — [reason]` when justified (D-01 escape
valve), but no section may be omitted entirely.

---

**Pattern: Strict Shape with Honest Depth Escape Valve (D-01)**

Source: RESEARCH.md `## Architecture Patterns — Hardened Output Template`
Apply to: Every section heading in `output-template.md`

Required sections (fixed order, per RESEARCH.md Architecture diagram):
1. Problem Essence
2. Assumptions Table (classified, per METH-03)
3. Ground Truths (with stable IDs)
4. Derivation Chains (per D-02)
5. Abandoned Reasoning / Dead Ends (per D-03)
6. Conclusion + Confidence Caveats (per D-07)

The escape valve (D-01): any section may contain `Nothing material here — [reason]`
when no genuine content belongs there. The section header must still be present.

---

**Pattern: Hardened Assumptions Table — Five-Column Format (METH-03 + D-06)**

Source: RESEARCH.md `## Architecture Patterns — Pattern: Assumption Classification Table`
Apply to: Section 2 (Assumptions Table) of `output-template.md`

```markdown
| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| [Assumption text] | physical law / current constraint / convention / untested belief | [per D-06 prescribed action] | Accept / Challenge / Discard | [source or "unverified — flagged"] |
```

This replaces the original skill's three-column format:
`| Assumption | Challenge | Verdict |`

The Type and Treatment columns are the additions that satisfy METH-03.

---

**Pattern: Ground Truths with Stable IDs**

Source: RESEARCH.md `## Architecture Patterns — Pattern: Derivation Chains with Stable IDs`
Apply to: Section 3 (Ground Truths) of `output-template.md`

```markdown
## Ground Truths

- **GT-1** [fact text] — source: [verification source]
- **GT-2** [fact text] — source: [verification source]
- **GT-3?** [fact text] — unverified: [reason; inherits caveat per D-07]
```

The `GT-N` stable identifier is assigned here and referenced by derivation chains.
The `?` suffix marks unverified ground truths (D-07). IDs do not change once assigned.

---

**Pattern: Derivation Chains — Per-Conclusion with Intermediates (D-02)**

Source: RESEARCH.md `## Code Examples — Correct Derivation Chain Format`
Apply to: Section 4 (Derivation Chains) of `output-template.md`

```markdown
## Derivation Chains

### Conclusion: [Conclusion text]

GT-1 (team size = 12 engineers, source: org chart) + GT-3 (2 deploy conflicts/month,
source: git log analysis)
→ [coordination overhead at current scale is low — 12 engineers produce fewer than
   3 deploy conflicts/month]
→ [microservices' primary benefit — independent deploy velocity — does not address
   the team's actual bottleneck]

**Confidence:** HIGH — all ground truths verified. Would revisit if GT-3 rises above
10/month.
```

Key rules:
- One chain per conclusion — no redundant restatement (D-02)
- Each chain requires at least one intermediate step (`→ [intermediate claim]`); a chain
  that goes directly GT-IDs → conclusion is missing a step (RESEARCH.md Pitfall 5)
- Unverified GT inputs use `GT-N?` notation; the conclusion inherits a `MEDIUM` or `LOW`
  confidence caveat (D-07)

The intermediate is where the reasoning happens. If no intermediate can be stated, the
conclusion is either too close to the ground truth (trivial) or the chain is incomplete.

---

**Pattern: Abandoned Reasoning Section — Required Structure (D-03)**

Source: RESEARCH.md `## Code Examples — Correct Abandoned Reasoning Entry`
Apply to: Section 5 (Abandoned Reasoning) of `output-template.md`

```markdown
## Abandoned Reasoning

### Dead End: [Name of discarded path]

**What was tried:** [brief description]

**Why abandoned:** [the specific failure — assumption false, contradicts ground truth,
assumption classification too weak to anchor the chain, etc.]

**What it ruled out:** [what this dead end saves the reader from re-exploring]
```

If no reasoning was abandoned, write:
`Nothing material here — all reasoning paths pursued led to the conclusion above.
[Optional: describe the problem's constraint space that made alternative paths infeasible.]`

Do NOT omit this section. The `Nothing material here` form still satisfies D-03.

---

**Pattern: Conclusion Section with Confidence Caveats (D-07)**

Source: RESEARCH.md `## Architecture Patterns — Hardened Output Template` and D-07
Apply to: Section 6 (Conclusion) of `output-template.md`

Every conclusion must carry an explicit confidence level. Any conclusion that depends on
an unverified GT (`GT-N?`) inherits a caveat:

```markdown
## Conclusion

**Recommended approach:** [description]

**Key insight:** [what the first-principles analysis revealed that was non-obvious]

**Trade-offs acknowledged:** [what is being accepted]

**Confidence:** HIGH / MEDIUM / LOW
[If MEDIUM or LOW: state which GT-N? inputs caused the downgrade and what would
need to be verified to raise it]
```

---

**Pattern: Original Output Format (baseline — what gets replaced)**

Source: RESEARCH.md `## Baseline Analysis — Original Standardized Output Format`
Apply to: Understanding the before-state when authoring `output-template.md`

The original format from `github.com/chrisdavidson/first-principles-skill`:
```markdown
### 4. Reasoning Chain
Ground Truth → [Step 1] → [Step 2] → Solution
```

This flat arrow chain is the format that METH-05 and D-02 replace with per-conclusion
derivation chains. It is documented here so the planner can see the exact delta.

---

### `test-run-draft.md` (content-document, analysis-trace)

**Location:** `.planning/phases/01-sharpen-the-methodology-and-harden-the-output-format/test-run-draft.md`

**What it is:** A full first-principles analysis run on a real, genuinely unresolved
design decision from this skill build (D-08). Kept as a working draft in `.planning/`;
NOT shipped as `examples/` content (D-09 — that is Phase 5's scope). Covers Success
Criterion 4 (every conclusion traces to a named ground truth).

---

**Pattern: Test-Run Must Use the Output Template Shape**

Source: RESEARCH.md `## Common Pitfalls — Pitfall 3` and D-08/D-09
Apply to: Structure of `test-run-draft.md`

The test-run is a full application of the methodology, producing a document that follows
the sections defined in `output-template.md`. It is not a summary or a sketch — it must
demonstrate the complete trace so Success Criterion 4 can be verified.

```
test-run-draft.md sections (same as output-template.md):
1. Problem Essence (the chosen design decision stated as a core question)
2. Assumptions Table (classified per METH-03)
3. Ground Truths (with stable GT-IDs)
4. Derivation Chains (one per conclusion, with intermediates)
5. Abandoned Reasoning (must have at least one — D-08 requires a non-trivial problem)
6. Conclusion + Confidence Caveats
```

---

**Pattern: Test-Run Problem Selection (D-08 — genuinely unresolved)**

Source: RESEARCH.md `## Common Pitfalls — Pitfall 3` and `## Open Questions — Question 3`
Apply to: Choice of design question for `test-run-draft.md`

The problem must be genuinely unresolved — reasonable people could disagree and at least
one false assumption is present to be discovered. RESEARCH.md identifies three strong
candidates (Open Questions, item 3):

- (a) "Should Phase 4 (Reason Upward) have any prescribed sub-steps, or should it
  remain fully free-form?"
- (b) "Should the output template's Abandoned Reasoning section be required or optional?"
- (c) "Should assumption classification use 4 types or allow a 'mixed / uncertain'
  fifth category?"

Warning signs that the chosen problem is too safe (Pitfall 3):
- The test-run has zero dead ends
- All ground truths are verified
- The conclusion was obvious before running the methodology

---

**Pattern: Worked Analysis — External Baseline (architecture-review.md)**

Source: RESEARCH.md `## Baseline Analysis — Worked Example: Microservices Architecture Review`
Apply to: Understanding what "good" looks like for `test-run-draft.md` output quality

The original `examples/architecture-review.md` (fetched from GitHub, verified) is the
strongest existing reference for analysis quality. It demonstrates:
- Following the 5-phase structure with real, specific data (team size 12, 2 deploy
  conflicts/month, 200ms latency budget)
- Explicit assumption verdicts with justification ("Netflix has 2000+ engineers. We have
  12. Discard — Different scale")
- Tracing conclusions to ground truths with specific quantification ("30% time already
  on infrastructure → Microservices would increase this to 50%+")
- A concrete recommendation with revisit triggers

What the test-run must add that the original lacks:
- Assumption classification by the 4-type scheme (not just verdict)
- Derivation chains with stable GT-IDs and explicit intermediates
- An Abandoned Reasoning section
- Rationale for each phase step

---

## Shared Patterns

### Strict Shape + Honest Depth Escape Valve
**Source:** RESEARCH.md D-01 and `## Architecture Patterns — Hardened Output Template`
**Apply to:** `output-template.md` (defines the rule) and `test-run-draft.md` (applies it)

```markdown
[Any section may contain:]
Nothing material here — [reason explaining why this section has no content for
this particular analysis and that the omission is justified, not lazy]
```

The section header must be present. The escape valve prevents forced fabrication (box-
ticking) while keeping the auditable shape intact. It is the mitigation for RESEARCH.md
Pitfall 2 (too prescriptive / box-ticking).

---

### Unverified Ground Truth Flagging (D-07)
**Source:** RESEARCH.md D-07 and `## Architecture Patterns — Derivation Chains`
**Apply to:** Section 3 (Ground Truths) of `output-template.md` and all derivation chains in `test-run-draft.md`

```markdown
GT-N?: [fact text] — unverified: [specific reason the fact could not be verified]
```

Any conclusion chain that includes a `GT-N?` input must carry the confidence caveat:
```markdown
**Confidence:** MEDIUM — GT-N unverified: [state what would need to be confirmed to raise
to HIGH]
```

This keeps the analysis honest about uncertainty without halting it. A skeptic can see
exactly where the soft spot is.

---

### No Prescribed Sub-Steps for Phase 4
**Source:** RESEARCH.md D-04 and `## Architecture Patterns — Anti-Patterns to Avoid`
**Apply to:** Phase 4 definition in `methodology.md`

Phase 4 (Reason Upward) must not receive prescribed sub-steps in `methodology.md`. The
only constraint is mandatory self-documenting narration. This is a hard constraint from
D-04 and is the deliberate guard against over-prescription (Success Criterion 5).

```
WRONG: Adding sub-steps like "Step 4a: list all possible solutions. Step 4b: score
       each against ground truths. Step 4c: select highest-scoring solution."
RIGHT: "Reason upward from the ground truths toward an answer using whatever approach
       the problem calls for. As you go, narrate what you are trying, what you are
       building on, and why."
```

---

### Derivation Chain Intermediate Requirement
**Source:** RESEARCH.md `## Common Pitfalls — Pitfall 5`
**Apply to:** Section 4 of `output-template.md` and all chains in `test-run-draft.md`

A derivation chain with no intermediate step is a flat list with GT labels, not a chain.
The intermediate is a new claim that could not be stated from either ground truth alone.

```
WRONG (flat list): GT-1 + GT-2 → conclusion
RIGHT (chain):     GT-1 + GT-2 → [intermediate claim] → conclusion
```

If no intermediate can be stated, the conclusion is either trivial (already a ground
truth restatement) or the chain is missing a reasoning step.

---

## No Analog Found

All three Phase 1 files have no close match in this codebase. The table below records
the reason and the fallback pattern source for each.

| File | Role | Data Flow | Reason No Analog Exists | Fallback Source |
|------|------|-----------|------------------------|-----------------|
| `methodology.md` | content-document | standing-instruction | No skill files exist in this repo; Phase 1 is the first content authored | RESEARCH.md `## Code Examples` (verified patterns from locked decisions) |
| `output-template.md` | content-document | template-enforcement | No skill files exist in this repo | RESEARCH.md `## Architecture Patterns` (derivation chain, assumptions table, abandoned reasoning patterns) |
| `test-run-draft.md` | content-document | analysis-trace | No worked examples exist in this repo | RESEARCH.md `## Baseline Analysis — Worked Example` (original architecture-review.md, fetched from GitHub; used as quality baseline, not structural template) |

---

## Locked Constraints Summary for Planner

The following are locked by user decisions in CONTEXT.md and must not be reopened as
design questions in the plan. The planner should reference these as already-decided when
writing task actions.

| Decision | Constraint | Files Affected |
|----------|-----------|----------------|
| D-01 | Strict shape, honest depth; escape valve is `Nothing material here — [reason]` | `output-template.md` |
| D-02 | Derivation chains per conclusion, not flat table; one chain per conclusion; intermediates required | `output-template.md`, `test-run-draft.md` |
| D-03 | Abandoned Reasoning section is required in every analysis | `output-template.md`, `test-run-draft.md` |
| D-04 | Phase 4 has no prescribed sub-steps; mandatory self-documenting narration only | `methodology.md` |
| D-05 | Phase 4 exit criterion is AND: question answered AND all chains complete | `methodology.md` |
| D-06 | Exactly four assumption types with exactly these prescribed treatments; no synonyms, no fifth type | `methodology.md`, `output-template.md` |
| D-07 | Unverified assumptions allowed in chains but flagged `GT-N?`; conclusions inherit confidence caveat | `output-template.md`, `test-run-draft.md` |
| D-08 | Test-run dogfoods a genuinely unresolved design decision from this skill build | `test-run-draft.md` |
| D-09 | Test-run stays in `.planning/` as a draft; NOT shipped as `examples/` content | `test-run-draft.md` location |

---

## Metadata

**Analog search scope:** `/home/chrisdavidson/programming/first-principles-skills` (full repository)
**Files scanned:** All non-git files (confirmed via directory listing — 20 files excluding `.venv`)
**In-repo skill files found:** 0
**External patterns sourced from:** RESEARCH.md (which fetched and analyzed `github.com/chrisdavidson/first-principles-skill` directly)
**Pattern extraction date:** 2026-05-16
