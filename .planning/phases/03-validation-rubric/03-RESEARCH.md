# Phase 3: Validation Rubric — Research

**Researched:** 2026-05-16
**Domain:** Analytic rubric design, falsifiable LLM self-evaluation, gate scoring models, fail-demonstration construction
**Confidence:** HIGH (internal artifacts verified directly; rubric design findings cross-referenced across multiple authoritative sources)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** Exactly 6 criteria — one per methodology phase (Identify Essence, Challenge Assumptions, Establish Ground Truths, Reason Upward, Validate) plus one for conclusion-to-ground-truth traceability. Carving rigor-critical sub-features into their own criterion was rejected; sub-features fold into the relevant per-phase criterion (classification quality into Challenge Assumptions, dead-end honesty into Reason Upward, etc.).
- **D-02:** Gate + hand-wavy cap, not a pure single-band gate. Two failure conditions: (1) gate — any criterion at the lowest band fails the analysis; (2) hand-wavy cap — too many criteria at the second-lowest band also fails. Exact cap threshold deferred to research (D-05).
- **D-03:** One shared 4-level scale applied uniformly to all 6 criteria. Per-criterion tailored vocabularies rejected. Level descriptors remain criterion-specific and must be concrete observables, not adjectives.
- **D-04:** The deliberately-weak sample analysis required by Success Criterion 4 lives as a separate, non-shipped `.planning/` verification artifact — not embedded in validation-rubric.md and not in `examples/`. Mirrors Phase 1's test-run-draft.md pattern.
- **D-06:** Band labels are left to the planner. The stub's proposal (Rigorous / Adequate / Hand-wavy / Absent) is a starting point, not a locked decision.
- **D-07:** Scored output uses per-criterion verdict blocks — each criterion gets a self-contained block with: quoted span, band assigned, one-line justification. Consolidated scoring tables rejected.
- **D-08:** The rubric actively polices the honest-depth escape valve. A section marked `Nothing material here — [reason]` scores the top band only if the rubric verdict confirms the stated reason is genuine. A lazy or generic "Nothing material here" is scored as hand-wavy or as a fail.
- **D-09:** When a criterion scores the gate-fail band and no span exists to quote (because the section or artifact is simply missing), the verdict cites the gap explicitly — names what is missing and where it should have appeared.

### Claude's Discretion

- The exact hand-wavy cap threshold (D-05) — research must justify it.
- The final 4 band labels (D-06).
- The wording of each criterion and its 4 observable level descriptors.
- Criterion ordering within the rubric.
- The precise construction of the weak sample analysis and how concisely the shipped rubric demonstrates the verdict-block format.

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope. Companion tools (Phase 4), worked examples (Phase 5), and final nav-map audit / README / schema validation (Phase 6) were not pulled forward.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| VALID-01 | `references/validation-rubric.md` defines 6–8 analytic criteria covering the 5 phases and traceability | Criterion set locked at 6 by D-01; research documents what each must score |
| VALID-02 | Each criterion has 3-4 named levels, each with a concrete observable descriptor | Analytic rubric design findings; observable vs. adjective descriptor guidance |
| VALID-03 | The rubric uses a gate scoring model — any criterion at the lowest band fails the analysis | Conjunctive scoring model findings; gate rationale documented |
| VALID-04 | The rubric requires Claude to quote the specific span of its analysis that satisfies or fails each criterion | Evidence-quoting verdict block design (D-07); falsifiable self-evaluation research |

</phase_requirements>

---

## Summary

Phase 3 authors `first-principles-thinking/references/validation-rubric.md` — replacing the one-sentence stub with a fully operative analytic rubric. The rubric is a Layer-3 reference component: frontmatter-free, read on demand by the validator-fix-repeat loop already resident in `SKILL.md`, and consuming no always-on context tokens. Its job is to make hand-waving instrumentally harder to pass than genuine reasoning — not as an aspiration, but as a structural property of how the scoring works.

The research resolves the four open questions flagged in CONTEXT.md and STATE.md. The most critical: the hand-wavy cap threshold (D-05) is justified at **2 out of 6** criteria — the smallest cap that catches "mediocre everywhere, terrible nowhere" analyses while staying tolerant of one genuinely-shallow section. The analytic rubric literature (Brookhart, conjunctive scoring research) confirms that observable descriptors must be statements of presence/absence or count, never adjectives, and that a conjunctive (gate) model is the correct structure when any single below-minimum criterion indicates a structural fault rather than a compensatable weakness. Falsifiable LLM self-evaluation research identifies that the single most effective mechanism is mandatory evidence-quoting: a criterion that requires quoting the actual span being scored cannot be passed by adding keywords or asserting compliance.

The D-04 weak sample should be constructed by selectively degrading three distinct failure modes in the existing test-run-draft.md: dropping derivation-chain intermediate steps (Reason Upward criterion fails), replacing assumption classifications with generic labels without treatment (Challenge Assumptions criterion fails), and abusing the honest-depth escape valve in Abandoned Reasoning (escape-valve policing criterion triggers). This produces a multi-criterion fail demonstration where each verdict block quotes a specific broken span.

**Primary recommendation:** Author the rubric as 6 criteria in methodology-phase order (Identify Essence → Challenge Assumptions → Establish Ground Truths → Reason Upward → Validate → Traceability), each with a shared 4-level scale and criterion-specific observable descriptors. Gate: any criterion at Level 1 (lowest) fails the analysis. Hand-wavy cap: 2 or more criteria at Level 2 also fails. Evidence-quoting in verdict blocks is the structural mechanism that makes self-certification instrumentally harder than genuinely passing.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Criterion definitions (what to score) | `validation-rubric.md` (Layer 3, on-demand) | — | The rubric is the criteria authority; SKILL.md does not duplicate them |
| Validator loop instruction (when to apply) | `SKILL.md` (Layer 1, always-on) | — | Already shipped in Phase 2 (D-09 there); Phase 3 only fills the link target |
| Verdict-block format | `validation-rubric.md` | — | The format belongs in the rubric so the loop instruction stays lean |
| Weak-sample fail demonstration | `.planning/phases/03-validation-rubric/` | — | Verification artifact only; not shipped with the skill |
| Observable anchors (what passing looks like) | `output-template.md` (Layer 3) | `methodology.md` (.planning, source) | Rubric descriptors must be checkable against output-template.md section structure |

---

## Standard Stack

This phase has no software packages. The deliverable is Markdown content.

**Canonical documents the rubric must calibrate against (all verified by direct inspection):**

| Document | Path | Role in Rubric |
|----------|------|----------------|
| SKILL.md methodology | `first-principles-thinking/SKILL.md` | Defines the 5 phases, named artifacts, exit criteria the rubric scores |
| Output template | `first-principles-thinking/references/output-template.md` | Defines section structure, chain format, escape valve, verdict vocabulary — rubric descriptors must be observable against this structure |
| Methodology source | `.planning/phases/01-.../methodology.md` | Per-phase operations, named artifacts, exit criteria (the source the SKILL.md copied from) |
| Weak-sample base | `.planning/phases/01-.../test-run-draft.md` | Passing-quality analysis to deliberately weaken for D-04 fail demonstration |
| Existing stub | `first-principles-thinking/references/validation-rubric.md` | Being replaced in-place; frontmatter-free (Phase 2, D-08) |

---

## Package Legitimacy Audit

No external packages. Not applicable.

---

## Architecture Patterns

### Analytic Rubric Structure (the standard form)

An analytic rubric is a grid: criteria as rows, performance levels as columns, observable descriptors at each cell intersection. [CITED: Brookhart (2018), Frontiers in Education; multiple university teaching center sources]

The structure mandates:
- **Criteria** represent distinct, assessable capabilities — not phase names used as labels, but verifiable behaviors the phase must have produced.
- **Level descriptors** are observable statements, not adjectives. "Rigorous" is not a descriptor. "Every conclusion has a derivation chain containing at least one intermediate step, and each chain names the GT-IDs it consumes" is a descriptor — a reader can check yes or no without interpretation. [CITED: Brookhart 2018; ASU Teach Online best practices]
- **Level count:** 3–5 levels is the documented consensus; 4 levels is the most common for analytic rubrics in higher-education and competency assessment contexts. [CITED: multiple university teaching center sources, Mertler rubric design guide] D-03 locks 4 levels — this is consistent with standard practice.

### Conjunctive vs. Compensatory Scoring

Two fundamental models exist for multi-criterion assessment: [CITED: Meyers 2018, Journal of Competency-Based Education; Haladyna & Hess 1999, Educational Assessment]

**Compensatory model:** High performance on one criterion can offset low performance on another. Total score determines pass/fail. A student who excels at 5 criteria and fails 1 passes as long as the aggregate is high enough.

**Conjunctive model (gate):** Each criterion must independently meet a minimum threshold. One criterion below the gate fails the whole assessment regardless of other scores. Documented rationale: when below-minimum performance on a specific dimension indicates a structural fault that cannot be compensated by excellence elsewhere — the criterion failure is not an accidental dip, it is evidence of a missing capability.

**The gate model is correct for this rubric** because: absence of derivation chains cannot be compensated by excellent assumption classification; an Essence Statement that names a symptom rather than a core question propagates error through every later phase regardless of how well-formed the ground truths are. Each criterion failing at the lowest band represents a structural failure in the analysis, not an isolated weakness.

**Hybrid / partial conjunctive models** are documented in the competency assessment literature and clinical OSCE settings (where a minimum number of stations must be passed in addition to the aggregate score). [CITED: OSCE conjunctive standards literature, PubMed 33290124] The hand-wavy cap (D-02) is exactly this structure: a secondary gate that fires when too many criteria reach the second-lowest level, even if none reach the lowest.

### Recommended Project Structure

```
first-principles-thinking/
├── SKILL.md                       # Layer 1: always-on; validator loop already resident
└── references/
    └── validation-rubric.md       # Layer 3: on-demand; this phase's deliverable

.planning/phases/03-validation-rubric/
├── 03-CONTEXT.md                  # Locked decisions
├── 03-RESEARCH.md                 # This file
└── 03-weak-sample.md              # D-04 verification artifact (non-shipped)
```

### Pattern: Observable Descriptors (the core authoring discipline)

**What:** Every level descriptor is a statement that can be verified by inspection of the analysis text — it names a specific artifact, count, presence/absence, or structural property.

**When to use:** Always. No exceptions for any criterion or any level.

**Examples of the distinction:**

| Adjective (wrong) | Observable descriptor (correct) |
|-------------------|----------------------------------|
| "Rigorous derivation" | "Every conclusion has a derivation chain with at least one intermediate step; each chain names the GT-IDs it consumes" |
| "Assumptions are well-classified" | "Every row in the Assumptions Table has a Type value drawn from the four-type scheme (physical law / current constraint / convention / untested belief) and a non-empty Verdict cell" |
| "Adequate traceability" | "The Conclusion section names at least one GT-ID for each claimed conclusion" |
| "Escape valve abused" | "One or more section is marked 'Nothing material here' without a reason clause, or the reason clause is generic and would apply to any analysis" |

[CITED: Brookhart 2018 Frontiers in Education; ASU Teach Online "Best Practices for Designing Effective Rubrics"]

### Pattern: Verdict Block Format (D-07)

Each of the 6 criteria gets a self-contained scored block:

```markdown
### Criterion N: [Criterion Name]

**Quoted span:** "[Direct quote from the analysis being scored]"
**Band:** [Level label]
**Justification:** [One sentence tying the quoted span to that band's observable descriptor]
```

For a gate-fail (Level 1) verdict where the section or artifact is absent (D-09):

```markdown
### Criterion N: [Criterion Name]

**Gap:** [Name what is missing and where it should have appeared]
**Band:** [Lowest level label]
**Justification:** [One sentence: the documented absence is the evidence]
```

### Anti-Patterns to Avoid

- **Presence-checking as criteria:** "Does an Assumptions Table exist?" is a presence check, not a quality criterion. Replace with "Does each row in the Assumptions Table carry a Type, Treatment, Verdict, and Verification column populated with a non-generic entry?" — a quality check.
- **Adjective levels:** "Excellent / Good / Fair / Poor" without observable descriptors are not rubric levels; they are grade-book labels.
- **Compensatory scoring for structural faults:** Allowing a missing derivation chain to be offset by perfect assumption classification defeats the purpose of the methodology's chain-of-artifacts structure.
- **Pass-by-keyword:** A rubric that a model can pass by inserting the correct vocabulary without doing the underlying work (e.g., writing "GT-1 + GT-2 →" without an intermediate step). The descriptor must name the intermediate step explicitly to make keyword-insertion insufficient.
- **Escape valve as a free pass:** A `Nothing material here` entry that scores the same as a substantive entry incentivizes skipping real reasoning. D-08 addresses this directly.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Rubric structure | A novel scoring system | Standard 4-level analytic rubric with observable descriptors | Analytic rubric design is a documented discipline; the standard form is understood, studied, and known to produce reliable scoring when descriptors are observable |
| Gate model | A custom aggregation formula | Conjunctive scoring (any-criterion-fails-all) | Compensatory averaging is documented to allow structural failures to be hidden by aggregate scores; conjunctive is the right model for methodology self-assessment |
| Fail demonstration | A synthetic analysis written from scratch | Deliberately weaken test-run-draft.md | The test-run-draft.md is already in the exact output format, was authored to pass the methodology, and serves as a natural base — weakening known-good content produces targeted, nameable failures; writing from scratch risks introducing unintended confounds |

---

## D-05 Research: Justified Hand-Wavy Cap Threshold

**The question:** Out of 6 criteria, how many at the second-lowest band should trip the cap?

### Evidence Base

**From competency assessment literature:** [CITED: OSCE conjunctive standards, PubMed 33290124; Meyers 2018 CBE Journal] Hybrid conjunctive models (gate + secondary threshold) are documented in high-stakes professional assessment. The rationale is always the same: prevent "excessive compensation" where strong performance in many areas masks consistent-but-not-catastrophic weakness across the board. The secondary threshold is always set to be tolerant of isolated second-lowest performance but intolerant of systemic mediocrity.

**From analytic rubric design principles:** [CITED: ASU Teach Online; NCSU rubric best practices] A second-lowest band on an analytic rubric represents "developing" or "approaching proficiency" — below the standard for independent execution but not absent. Allowing one such rating is considered acceptable in educational contexts because some criteria may be genuinely harder to satisfy. Allowing a majority at that level defeats the rubric's purpose as a quality gate.

**Applying to this rubric specifically:**

- 6 criteria total.
- A cap of 1: catches only the case where exactly 1 criterion is at the second-lowest band — this is too strict and would reject analyses with one legitimately-shallow section (e.g., Abandoned Reasoning genuinely marked Nothing-material-here for a simple problem). This would generate false positives.
- A cap of 3: allows half the criteria to be at the second-lowest band — an analysis where 3 of 6 criteria are "developing" is not a minor weakness, it is a systemic quality problem. But 3 is the 50% line, and the intent is to catch "mediocre everywhere" — 3/6 already is "everywhere." This sets the cap too permissively for a methodology skill that must catch hand-waving.
- A cap of 2: flags the analysis when 2 or more criteria are at the second-lowest band. This means:
  - A single second-lowest criterion is tolerated (one section is weaker than ideal but the rest of the analysis is solid).
  - Two or more second-lowest criteria are not tolerated (the analysis is weak in at least two distinct phases — a pattern, not an outlier).

**Justification for 2 out of 6:**

This is the minimum cap that catches "mediocre everywhere, terrible nowhere." If an analysis scores at the second-lowest band on, say, both Challenge Assumptions and Reason Upward, it means both the assumption-challenging work and the derivation-chain work are sub-standard simultaneously. That is not a coincidence — it is a pattern of shallow reasoning that the gate alone cannot catch (since neither criterion reaches the gate-fail level). A cap of 2 catches this pattern while remaining tolerant of one isolated weaker section.

The cap at 2 also has a practical asymmetry property: it is easier for a hand-wavy analysis to score two or more criteria at second-lowest than to score any criterion at the gate-fail level. This means the cap catches a real failure mode that the gate misses, without firing on passing-quality analyses.

**Recommendation:** Cap at **≥2** second-lowest-band scores triggers a fail. [ASSUMED — this specific threshold is reasoned from rubric design principles and competency assessment literature but is not a precise empirical finding for this exact 6-criterion configuration; it should be treated as a well-justified default rather than a fixed datum.]

---

## Falsifiable LLM Self-Evaluation: Design Properties

**The problem:** A model applying a self-evaluation rubric to its own output has a documented tendency toward optimism/self-consistency bias — it tends to confirm its own reasoning as adequate. [CITED: Masood 2026, Medium; sycophancy research from EMNLP 2025] Any rubric criterion phrased as a question the model can answer "yes" to about its own work ("Is this analysis rigorous?") will tend to be answered "yes." This is not dishonesty — it is a structural feature of how language models generate consistent continuation text.

### Properties That Make Self-Evaluation Falsifiable

**Property 1: Mandatory evidence-quoting (D-07)**

The single most effective mechanism. [CITED: Masood 2026; G-Eval step-by-step reasoning requirement] A criterion that requires the model to quote the specific span of the analysis being scored cannot be passed by asserting compliance without producing evidence. The key constraint is that the quoted span must *satisfy the observable descriptor at the claimed level* — if the quoted span does not contain the artifact the descriptor requires (e.g., an intermediate step in a derivation chain), the quote itself demonstrates the failure.

This is D-07's rationale: verdict blocks that contain a quote make the verdict auditable. A quote of text that lacks a derivation chain's intermediate step, next to a "Rigorous" band claim, creates a contradiction the model cannot easily sustain across the same verdict block.

**Property 2: Observable descriptors for the lowest band that describe absence or structural failure**

The gate-fail descriptor for each criterion must name what is missing or broken in terms that can be checked without interpretation. "No derivation chains are present" or "The Assumptions Table has rows with empty Verdict cells" are checkable. "The analysis lacks rigor" is not.

When a criterion fails at the gate level because a section is simply absent, D-09 requires citing the gap explicitly. This is a key falsifiability mechanism: a claim that the analysis is rigorous when the Assumptions Table is empty is a falsifiable claim — it is directly contradicted by the absence of the table.

**Property 3: Negative criteria that name specific hand-waving patterns**

[CITED: PITFALLS.md Pitfall 5; Masood 2026 rubric design guidance] Criteria that check for the *presence of correct artifacts* can be gamed by adding those artifacts superficially. Adding negative criteria — criteria that fire when specific patterns of low-rigor reasoning are present — makes it harder to satisfy both the positive and negative criteria simultaneously.

For this rubric, negative criteria include:
- Analogies used as evidence (banned by the methodology's Reason Upward phase — "do not use analogies as direct evidence")
- Conclusions introduced in the Conclusion section that do not trace to any derivation chain
- `GT-N?` inputs on load-bearing chains without confidence caveats
- `Nothing material here` without a genuine, analysis-specific reason

**Property 4: Escape-valve policing (D-08)**

The honest-depth escape valve is the single most gameable feature of the output format. A model can mark any section `Nothing material here — this analysis had no dead ends` and avoid scoring scrutiny on that section. D-08 closes this: the rubric must actively check whether the stated reason is genuine. The observable descriptor for this check: "The stated reason is specific to this analysis's problem — it could not be copy-pasted to a different analysis without alteration."

**Property 5: Criteria calibrated to the weakest-link problem, not the best section**

[CITED: PITFALLS.md; conjunctive scoring rationale] Compensatory scoring rewards having one excellent section while overlooking multiple shallow ones. The gate + cap structure ensures scoring is calibrated to weakness, not strength. The model cannot compensate a failed derivation chain with a perfect Essence Statement.

### Known Limits of LLM Self-Evaluation

The sycophancy research (EMNLP 2025) confirms that even with well-designed rubrics, models under conversational pressure (user rebuttal, social cues) tend toward self-consistency rather than honest self-critique. This is not a failure of rubric design — it is an inherent limit of the self-evaluation approach. The rubric cannot eliminate this tendency; it can only make it instrumentally harder to satisfy the rubric while reasoning badly.

The PROJECT.md already acknowledges this: "the validation rubric is a Markdown rubric the model applies" — not a guaranteed correctness oracle. Scoping it honestly is correct.

---

## Criterion-by-Criterion Research Notes

Each criterion must score against the relevant phase's named artifact and exit criterion (from `methodology.md` / `SKILL.md`). These notes are drawn from direct inspection of the shipped methodology and output template. [VERIFIED: direct codebase inspection]

### Criterion 1: Identify Essence

**Named artifact:** Essence Statement — a single sentence naming the core problem, followed by success criteria as a short checkable list.

**Exit criterion (from methodology.md):** "A skeptic reading the statement would agree it names the real question — not a symptom, not a proxy, not the triggering event."

**Observable scoring targets at each level:**
- Top band: Essence Statement is a single sentence; success criteria are stated as checkable conditions (a reader can verify yes/no against the final conclusion); the statement could not be equally well applied to a different, related problem without modification.
- Second band: Essence Statement exists and names a question, but success criteria are vague or stated in terms that cannot be verified against the conclusion (e.g., "the solution should be good").
- Third band: Essence Statement exists but restates the triggering event or problem description rather than the underlying question; OR success criteria are absent.
- Gate-fail band: No Essence Statement is present (Problem Essence section is empty or contains only a restatement of the user's prompt); OR the section uses the honest-depth escape valve without a genuine reason (escape-valve policing per D-08).

### Criterion 2: Challenge Assumptions

**Named artifact:** Classified Assumptions Table — columns: Assumption, Type, Treatment, Verdict, Verification.

**Exit criterion:** "Every assumption in scope has a classification from the four-type scheme AND has a recorded verdict and verification note, or an explicit 'unverified — flagged' note."

**Sub-features folded in (D-01):** 4-type classification quality; stakes-escalation application; D-07 unverified flagging discipline.

**Observable scoring targets:**
- Top band: Every row has a Type drawn from the four-type scheme; Verdict and Verification cells are non-empty and non-generic; at least one assumption has been challenged (not just labelled); if any assumption is used in a chain despite being unverified, the Verification cell reads "unverified — flagged."
- Second band: Table exists with populated rows, but one or more rows have generic entries (e.g., Verification = "unclear" without specifics, or Treatment applied does not match the Type's prescribed treatment).
- Third band: Table exists but uses a classification vocabulary outside the four-type scheme; OR multiple rows have empty Verdict/Verification cells; OR no assumption is challenged (all are labelled "Accept" without evidence).
- Gate-fail band: No Assumptions Table is present; OR the table exists but every row's Type cell is empty or freeform (no mapping to the four-type scheme).

### Criterion 3: Establish Ground Truths

**Named artifact:** Ground Truths list — numbered facts with GT-IDs and source citations; unverified entries marked GT-N?.

**Exit criterion:** "All ground truths have stable IDs, source citations or explicit unverified flags, and have passed the irreducibility test."

**Observable scoring targets:**
- Top band: Every GT-item has a stable ID; every verified GT has a source citation (not just "common knowledge"); every unverified GT is marked with the `?` suffix; no discarded assumptions from Phase 2 appear in the list.
- Second band: GT-IDs are present, but one or more verified GTs cite "common knowledge," "known fact," or no source; OR one unverified GT is used in a chain without the `?` suffix.
- Third band: GT-IDs are present but unstable (numbers change between references in the same document); OR the list includes assumptions discarded in Phase 2.
- Gate-fail band: No GT-IDs are assigned; OR the Ground Truths section lists claims without distinguishing verified from unverified; OR the section is absent or marked with the escape valve without a genuine reason.

### Criterion 4: Reason Upward

**Named artifact:** Derivation Chains — one chain per conclusion, format: `GT-N + GT-M → [intermediate claim] → [conclusion]`.

**Exit criterion:** "(1) core question is answered, AND (2) every conclusion has a complete derivation chain back to named ground truths."

**Sub-features folded in (D-01):** Dead-end honesty in Abandoned Reasoning; no analogies as direct evidence; escape-valve policing for Abandoned Reasoning section.

**Observable scoring targets:**
- Top band: Every conclusion stated anywhere in the document has exactly one derivation chain in section 4; each chain names GT-IDs, contains at least one intermediate step (a claim not statable from either GT alone), and reaches a conclusion; Abandoned Reasoning is either populated with a named dead end (What tried, Why abandoned, What ruled out) or uses the escape valve with a specific reason that could not be copy-pasted to any other analysis.
- Second band: Chains exist for all conclusions, but one or more chains lack a genuine intermediate step (the chain goes directly from GT-IDs to conclusion, or the intermediate restates a GT); OR one dead end in Abandoned Reasoning is described with a vague abandonment reason ("ran out of time," "seemed unlikely") rather than a structural reason.
- Third band: Some conclusions lack derivation chains; OR chains reference GT-IDs that do not exist in the Ground Truths section; OR an analogy is used as direct evidence ("others have solved it this way").
- Gate-fail band: No derivation chains exist; OR the Derivation Chains section is absent; OR conclusions appear only in the Conclusion section with no derivation chains at all.

### Criterion 5: Validate

**Named artifact:** Signed-off analysis — complete output with all conclusions traced and weak links resolved or flagged.

**Exit criterion:** "Every weak link is either resolved or explicitly flagged with a confidence caveat that a reader can evaluate."

**Observable scoring targets:**
- Top band: Every chain's weakest link is named; every GT-N? input in a load-bearing chain has a confidence caveat stating which GT-N? caused the downgrade and what verification would raise it; the overall conclusion's confidence rating matches the weakest chain that contributes to it.
- Second band: Confidence ratings exist for chains, but one or more GT-N? inputs in chains are not mentioned in the confidence line; OR a chain's confidence is rated HIGH while consuming a GT-N? input.
- Third band: Confidence ratings are present only on the overall conclusion but missing from individual chains; OR weak links are described in general terms without naming the specific chain step.
- Gate-fail band: No confidence ratings appear anywhere in the derivation chains; OR GT-N? inputs are used in chains without any confidence caveat; OR the Validate phase has not been executed (no stress-testing language, no weak-link identification).

### Criterion 6: Conclusion-to-Ground-Truth Traceability

**Named artifact:** The complete signed-off analysis as a whole — the relationship between Conclusion section claims and the Derivation Chains that produced them.

**Exit criterion (derived from METH-05):** "An explicit conclusion-to-ground-truth traceability map" — every conclusion in the Conclusion section must trace back to a named ground truth via a complete derivation chain.

**Observable scoring targets:**
- Top band: Every claim in the Conclusion section (recommended approach, key insight, trade-offs) traces to a specific named derivation chain in section 4; the Conclusion section introduces no new claims that did not appear in section 4; the Key Insight is a non-obvious finding, not a restatement of the conclusion.
- Second band: Most Conclusion claims trace to chains, but one claim is introduced for the first time in the Conclusion section; OR the Key Insight is a restatement of the Conclusion rather than a non-obvious finding.
- Third band: The Conclusion section contains claims that contradict the derivation chains; OR multiple new claims appear in the Conclusion section not present in section 4.
- Gate-fail band: The Conclusion section contains claims with no derivation chain anywhere in section 4; OR the Conclusion section is absent; OR every item in the Conclusion is new reasoning not found in the derivation chains.

---

## Constructing the Weak Sample (D-04)

### Source Material

`test-run-draft.md` is a passing-quality analysis of "should the 4-type assumption classification scheme add a fifth 'mixed/uncertain' category?" It follows the exact output format and produces clean derivation chains. [VERIFIED: direct inspection]

### Recommended Failure Injections

To produce a multi-criterion fail demonstration with specific, nameable per-criterion failures:

**Injection 1 — Flatten derivation chains (Criterion 4 failure):**

Remove intermediate steps from all chains. The chains should go directly from GT-ID pairs to conclusions:
```
GT-2 + GT-4 → adding a fifth category contradicts the scheme's purpose.
```
No intermediate claim. The intermediate is where the reasoning happens — its absence is detectable by the descriptor at Level 2 ("chain lacks a genuine intermediate step").

**Injection 2 — Strip assumption classification specificity (Criterion 2 failure):**

Replace Type values in the Assumptions Table with "general assumption" or leave them blank; leave Verdict and Verification cells empty or generic ("possibly true," "unsure"). This violates the four-type scheme requirement and makes every row unclassified.

**Injection 3 — Abuse the escape valve (Criterion 4 failure, Criterion 5 secondary):**

Replace the Abandoned Reasoning section's documented dead ends with:
```
Nothing material here — no dead ends were encountered.
```

This is a generic escape-valve abuse: the original test-run-draft.md documents two real dead ends (encoding confidence gradations into the type taxonomy; dropping classification entirely). The weak sample pretends they do not exist. The rubric's escape-valve policing (D-08) flags this: the stated reason is not specific to this analysis — it could be copy-pasted to any analysis.

**Why these three injections:**

Each targets a different criterion, producing a multi-criterion fail where each verdict block quotes a specific span. The fail is not declared globally — it is localized to the specific broken artifact in each criterion's verdict block. This demonstrates that the rubric produces actionable verdicts, not just binary pass/fail pronouncements.

**What to preserve in the weak sample:**

Keep the Problem Essence, Ground Truths list (with GT-IDs), and the Conclusion section. This ensures the weak sample is recognizably an analysis attempt, not a blank document — the rubric must catch subtler failures, not just emptiness.

### Artifact Location

`.planning/phases/03-validation-rubric/03-weak-sample.md`

This mirrors Phase 1's pattern: verification artifacts live in `.planning/phases/`, not in `references/` or `examples/`.

---

## Common Pitfalls

### Pitfall 1: Criterion Names as Presence Checks

**What goes wrong:** A criterion named "Assumptions Table" that scores presence vs. absence. Claude can "pass" this criterion by including an Assumptions Table with empty or generic cells.

**Why it happens:** Criterion names naturally gravitate toward the section headings in the output format. But a section's presence is not quality.

**How to avoid:** Every criterion's top-band descriptor must describe the *quality* of the artifact, not its existence. Gate-fail can describe absence, but Level 2, 3, and 4 distinguish degrees of quality.

**Warning signs:** Any criterion where all four level descriptors could be written as "the section exists" (L4), "the section is mostly there" (L3), "the section is partial" (L2), "the section is absent" (L1).

### Pitfall 2: Observable Descriptors Drift Into Adjectives

**What goes wrong:** An intended observable descriptor contains an evaluative adjective: "assumptions are well-classified," "chains are clearly derivable."

**Why it happens:** Adjectives are shorter to write. Concrete observables require naming the specific artifact, count, or structural property.

**How to avoid:** Apply the adjective-test: remove all adjectives from the descriptor and check if the remainder still conveys a verifiable condition. If removing "well" from "well-classified" leaves nothing checkable, the descriptor needs rewriting.

**Warning signs:** Level descriptors that contain words like "adequate," "sufficient," "thorough," "clear," "good," or "appropriate" without a referent.

### Pitfall 3: Escape-Valve Descriptor Absence

**What goes wrong:** The rubric does not include a descriptor for how to score legitimate escape-valve use. Claude then either treats all escape-valve sections as failures (too strict) or treats them all as passing (too permissive).

**Why it happens:** Escape-valve policing (D-08) is a cross-cutting concern — it applies to any section, not one criterion. It is easy to omit from any single criterion's descriptors because it feels like "someone else's problem."

**How to avoid:** At minimum, Criterion 4 (Reason Upward, which governs the Abandoned Reasoning section) must include a top-band descriptor that specifies what a legitimate escape valve looks like vs. what a generic one looks like. Criterion 1 should include escape-valve policing for Problem Essence.

**Warning signs:** Rubric says "the section may use the honest-depth escape valve" without specifying what distinguishes genuine from generic use.

### Pitfall 4: Verdict Block Format Creep

**What goes wrong:** Verdict blocks start being replaced by consolidated summary tables "for readability." This removes the per-criterion auditability that makes evidence-quoting enforceable.

**Why it happens:** A table of 6 rows with 3 columns (criterion, band, score) looks cleaner than 6 individual prose blocks.

**How to avoid:** The rubric's usage instructions must specify the block format (D-07) and explain why it is required: without a quoted span in each block, the evidence-quoting requirement cannot be verified.

### Pitfall 5: Hand-Wavy Cap Threshold Applied Inconsistently

**What goes wrong:** The rubric states "2 or more criteria at Level 2 fails the analysis" but the level labels are ambiguous about which level is "Level 2" (the second-lowest).

**Why it happens:** Level labels like "Adequate" can be read as the second-highest or the second-lowest depending on the scale direction.

**How to avoid:** The scoring model section of the rubric must specify the level labels in explicit rank order from lowest to highest (or highest to lowest), and name which level is the "gate-fail" band and which is the "cap-trigger" band by label, not by number. Both the gate and the cap must reference the level *label*, not a number.

---

## Code Examples

### Observable Descriptor vs. Adjective: Concrete Contrast

The distinction that matters most for rubric authoring. [CITED: Brookhart 2018; ASU Teach Online best practices]

**Adjective (unpublishable):**
```
Level 4 (Rigorous): The assumption classification is thorough and well-applied.
```

**Observable descriptor (publishable):**
```
Level 4 (Rigorous): Every row in the Assumptions Table has a Type value
drawn from the four-type scheme (physical law / current constraint /
convention / untested belief); the Treatment cell uses the vocabulary of
the prescribed treatment for that type; the Verdict cell records Accept,
Challenge, or Discard; the Verification cell cites a specific source or
names what verification would confirm the assumption — not "unclear" or
"possibly true."
```

### Gate + Cap Scoring Model: Prose Pattern

```markdown
## Scoring Model

Score each of the 6 criteria below using the shared 4-level scale:
**[Level 4 label] / [Level 3 label] / [Level 2 label] / [Level 1 label]**
(highest to lowest)

**Gate:** Any criterion scored [Level 1 label] → the analysis fails and must
be revised before being presented.

**Hand-wavy cap:** Two or more criteria scored [Level 2 label] → the analysis
fails and must be revised before being presented.

**Pass:** All criteria at [Level 3 label] or above, with at most one at
[Level 2 label].
```

### Verdict Block: Passing Example

```markdown
### Criterion 2: Challenge Assumptions

**Quoted span:** "A1: Every real assumption falls cleanly into exactly one of
the four types. | untested belief | verify, or flag unverified | Discard |
False. Counterexample constructed below (→ GT-3): a single assumption that is
simultaneously a convention and an untested belief."

**Band:** [Level 4 label]

**Justification:** Row has Type (untested belief), Treatment matching the
prescribed treatment for that type, Verdict (Discard), and Verification citing
a specific counterexample rather than a generic hedge.
```

### Verdict Block: Fail Example (Gap Citation per D-09)

```markdown
### Criterion 4: Reason Upward

**Gap:** No derivation chains exist in section 4. The Derivation Chains
section is missing entirely — chains of the form "GT-N + GT-M →
[intermediate] → [conclusion]" should appear for each conclusion stated
in section 6.

**Band:** [Level 1 label]

**Justification:** Absence of the derivation chains section means the
core question's answer cannot be traced to any named ground truth —
the gate-fail condition.
```

---

## State of the Art

| Old Approach | Current Approach | Notes |
|--------------|------------------|-------|
| Holistic rubric (single overall score) | Analytic rubric (per-criterion scores) | Analytic rubrics provide actionable feedback per dimension; holistic rubrics mask which dimension failed. [CITED: DePaul rubric types guide] |
| Compensatory scoring (average across criteria) | Conjunctive gate model (any criterion below minimum fails all) | Conjunctive scoring is standard in competency-based education where each criterion represents a non-substitutable capability. [CITED: Meyers 2018 CBE] |
| LLM self-evaluation by assertion ("the analysis is rigorous") | LLM self-evaluation by evidence-quoting (must quote the span being scored) | Evidence-quoting requirement documented in G-Eval and rubric-based LLM judge literature. [CITED: Masood 2026] |
| Escape valve as pass-through ("Nothing material here" scores top) | Escape valve subject to rubric policing (reason must be analysis-specific) | D-08 closes this gap by making the escape valve's justification itself a scoreable artifact |

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Hand-wavy cap at ≥2 out of 6 second-lowest criteria is the right threshold | D-05 threshold research | If wrong: cap too strict (rejects passing analyses) or too permissive (passes mediocre-everywhere analyses). Justification is principled but not empirically calibrated to this exact rubric. |
| A2 | Placing Traceability as Criterion 6 (last, after the 5 phases) is the right ordering | Claude's Discretion on criterion ordering | If wrong: a different ordering may make the rubric easier to apply sequentially. Low risk — the ordering affects usability, not correctness. |
| A3 | Three failure injections into the weak sample (flatten chains, strip classification, abuse escape valve) are sufficient to demonstrate per-criterion fail verdicts | D-04 weak sample construction | If wrong: some criteria may score above gate-fail even with these injections, requiring additional injections. The test-run-draft.md can be weakened further if needed. |

---

## Open Questions

1. **Band label vocabulary (D-06)**
   - What we know: The 4-level structure, gate band (lowest), and cap band (second-lowest) are locked by D-03 and D-02.
   - What's unclear: Which exact label words best signal the gate and cap bands to a model applying the rubric. The stub proposed Rigorous / Adequate / Hand-wavy / Absent — "Absent" names the gate-fail state, "Hand-wavy" names the cap-trigger state.
   - Recommendation: The stub's proposal is well-calibrated — "Absent" unambiguously communicates structural absence or failure; "Hand-wavy" is the exact failure mode the rubric is designed to catch. The planner should evaluate whether preserving these labels or finding alternatives (e.g., "Missing" / "Weak" / "Developing" / "Rigorous") serves the rubric's self-application context better.

2. **Criterion ordering**
   - What we know: 6 criteria; methodology-phase order is a natural default.
   - What's unclear: Whether leading with the most failure-prone criteria (Challenge Assumptions and Reason Upward, where most hand-waving occurs) would produce better self-evaluation outcomes than the natural phase order.
   - Recommendation: Use methodology-phase order (Identify Essence → Challenge Assumptions → Establish Ground Truths → Reason Upward → Validate → Traceability). Phase order is the most legible mapping to the methodology's own chain-of-artifacts structure.

3. **Weak-sample failure depth**
   - What we know: Three targeted injections into test-run-draft.md will produce failures in Criteria 2 and 4.
   - What's unclear: Whether the weak sample should also fail Criterion 5 (Validate) by removing confidence caveats, to demonstrate gate-fail on a third criterion.
   - Recommendation: Three injections producing two distinct criterion failures (Criterion 2 and Criterion 4) plus a hand-wavy cap trigger (two second-lowest scores on other criteria) is sufficient for Success Criterion 4. A third gate-fail is optional for extra coverage.

---

## Environment Availability

This phase is pure Markdown authoring. No external tools, services, or runtimes required beyond a text editor. Step 2.6 SKIPPED — no external dependencies.

---

## Validation Architecture

> `workflow.nyquist_validation` not explicitly set in config — treating as enabled.

This phase produces Markdown content, not executable code. Formal test infrastructure (pytest, jest, etc.) does not apply. Validation is behavioral: apply the rubric to the weak sample and verify it produces fails.

### Phase Requirements → Validation Map

| Req ID | Behavior | Test Type | Automated Command | Notes |
|--------|----------|-----------|-------------------|-------|
| VALID-01 | `validation-rubric.md` defines exactly 6 criteria covering 5 phases + traceability | Manual count | — | Count criteria in shipped file |
| VALID-02 | Each criterion has 4 named levels, each with an observable descriptor (no adjectives) | Manual audit | — | Apply adjective-test to every level descriptor |
| VALID-03 | Gate model: any criterion at lowest band fails | Manual scoring | — | Score weak sample; verify any Level 1 band produces fail verdict |
| VALID-04 | Evidence quoting: verdict blocks contain quoted span + band + justification | Manual scoring | — | Apply rubric to weak sample; verify each block has quoted span |
| SC-4 | Rubric applied to weak sample produces a fail with per-criterion verdict quotes | Behavioral | — | Apply rubric to 03-weak-sample.md; verify at least 2 criteria fail with specific quoted spans |

### Wave 0 Gaps

None — this phase creates new Markdown files; no test infrastructure is needed.

---

## Security Domain

> This phase authors Markdown content with no executable code, no user input validation, no authentication, no cryptography, and no network operations. `security_enforcement` defaults to enabled but ASVS categories V2–V6 are not applicable. The only relevant security consideration is Pitfall 7 (scope creep toward executable code), which is a project-level constraint already documented.

---

## Sources

### Primary (HIGH confidence)

- `first-principles-thinking/SKILL.md` — Phase definitions, named artifacts, exit criteria, the validator-fix-repeat loop instruction, output format. Verified by direct inspection.
- `first-principles-thinking/references/output-template.md` — Section structure, chain format, honest-depth escape valve, verdict vocabulary. Verified by direct inspection.
- `.planning/phases/01-.../methodology.md` — Sharpened per-phase operations and exit criteria. Verified by direct inspection.
- `.planning/phases/01-.../test-run-draft.md` — Passing-quality analysis in exact output format; confirmed usable as weak-sample base. Verified by direct inspection.
- `.planning/phases/03-validation-rubric/03-CONTEXT.md` — All locked decisions (D-01 through D-09). Verified by direct inspection.
- `.planning/research/PITFALLS.md` — Pitfall 5 (rubric vague/gameable), Pitfall 4 (box-ticking), escape-valve concerns. Verified by direct inspection.

### Secondary (MEDIUM–HIGH confidence)

- [Frontiers in Education: Appropriate Criteria: Key to Effective Rubrics (Brookhart 2018)](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2018.00022/full) — Observable vs. adjective descriptors; criteria quantity; descriptive language rationale.
- [ASU Teach Online: Best Practices for Designing Effective Rubrics](https://teachonline.asu.edu/2019/02/best-practices-for-designing-effective-rubrics/) — Observable descriptors, parallel structure, 3–5 levels standard.
- [NCSU Teaching Resources: Rubric Best Practices, Examples, and Templates](https://teaching-resources.delta.ncsu.edu/rubric_best-practices-examples-templates/) — Analytic vs. holistic rubrics; level descriptor guidance.
- [Meyers 2018, Journal of Competency-Based Education: Scoring models in competency-based educational assessment](https://www.researchgate.net/publication/327440654_Scoring_models_in_competency-based_educational_assessment) — Conjunctive vs. compensatory scoring model definitions and rationale.
- [Haladyna & Hess 1999, Educational Assessment: An Evaluation of Conjunctive and Compensatory Standard-Setting Strategies](https://eric.ed.gov/?id=EJ604332) — Gate model in educational assessment.
- [PubMed 33290124: Conjunctive standards in OSCEs](https://pubmed.ncbi.nlm.nih.gov/33290124/) — Hybrid conjunctive model rationale; "excessive compensation" framing.
- [Masood 2026, Medium: Rubric-Based Evaluations & LLM-as-a-Judge](https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80) — LLM judge biases, evidence-quoting as falsifiability mechanism, concrete observable descriptors.
- [EMNLP 2025: Challenging the Evaluator — LLM Sycophancy Under User Rebuttal](https://aclanthology.org/2025.findings-emnlp.1222/) — LLM self-evaluation sycophancy; limits of evidence-quoting under social pressure.

### Tertiary (MEDIUM confidence)

- [DePaul University Teaching Commons: Types of Rubrics](https://resources.depaul.edu/teaching-commons/teaching-guides/feedback-grading/rubrics/Pages/types-of-rubrics.aspx) — Holistic vs. analytic rubric types.
- [PITFALLS.md Pitfall 5](/.planning/research/PITFALLS.md) — Rubric gamability; falsifiable criterion design; negative criteria; evidence-quoting requirement. MEDIUM confidence (project research, grounded in cited sources).

---

## Metadata

**Confidence breakdown:**
- Criterion structure (6 criteria, 4 levels, observable descriptors): HIGH — standard analytic rubric design is well-documented; the 4-level shared scale is consistent with published guidance.
- Gate model (conjunctive, any-criterion-fails-all): HIGH — conjunctive scoring is documented and the rationale fits this rubric's structural failure modes.
- Hand-wavy cap threshold (≥2 of 6 at second-lowest): MEDIUM — principled reasoning from rubric design and hybrid conjunctive model literature, but not empirically calibrated to this specific rubric configuration.
- Falsifiable self-evaluation design properties: HIGH — evidence-quoting, observable descriptors, and negative criteria are documented in LLM evaluation research.
- D-04 weak-sample construction: MEDIUM — injection strategy is reasoned; actual fail outcomes must be verified by applying the rubric to the constructed weak sample.

**Research date:** 2026-05-16
**Valid until:** 90 days — rubric design principles and LLM evaluation research are stable domains; the internal artifacts are project-controlled.
