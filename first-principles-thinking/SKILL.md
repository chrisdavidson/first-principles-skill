---
name: first-principles-thinking
description: >-
  Decomposes any problem into verified fundamental truths and reasons upward from them instead of by analogy or convention. Use when the user wants to analyze from first principles, think from scratch, question a design, challenge assumptions, is this the right approach, why are we doing it this way, is there a better solution, evaluate an architectural decision, justify a decision from ground truths, map causes with an Ishikawa or fishbone diagram, pick cause categories, use inversion to invert the question and ask what would guarantee failure, apply second-order thinking to trace downstream consequences, apply a pre-mortem or 5-Whys, or asks whether reasoning is sound. Make sure to use this skill whenever the user wants to avoid reasoning by analogy or convention, even if they do not explicitly say "first principles".
license: MIT
metadata:
  version: "2.0"
---

# First Principles Thinking

A systematic methodology for decomposing any problem into verified fundamental truths and reasoning upward from there — for evaluating designs, challenging assumptions, and avoiding reasoning by analogy.

## Methodology

This section is a **standing procedure** Claude follows whenever first-principles thinking is required. It is not a recipe that runs once — every instruction is written in imperative present tense to be re-applied in full on each analysis. The methodology **ports and sharpens** the original five-phase structure; it does not replace the underlying logical sequence that structure encodes.

### How the phases connect

Each phase produces a named artifact. That artifact is the entry condition for the next phase. The chain is:

> **Essence Statement** → **Classified Assumptions Table** → **Ground Truths list** → **Derivation Chains** → **signed-off analysis**

The accumulated artifacts together form the standardized output document, whose full section shape is defined in the [First Principles Analysis Output Template](#first-principles-analysis-output-template) appendix. Working through these phases in order is what makes the analysis auditable — a skeptic can inspect any artifact and verify that the phase that produced it was executed rather than skipped.

---

### Phase 1: Identify Essence

**Why this phase exists:** Starting an analysis without isolating the core problem produces conclusions that solve a symptom, a proxy, or a convenient restatement of the original question rather than the real one. When the essence is unstated, every subsequent phase is calibrated to the wrong target — the error is invisible until the final conclusion turns out to answer a question nobody asked.

**Entry criterion:** The problem or decision to be analyzed has been stated. It need not be perfectly framed — clarifying the frame is part of this phase's work.

**Operation:** Strip away implementation details, constraints, historical context, and framing artifacts to expose the core question. Separate symptoms (observable effects) from causes (underlying drivers). State the success criteria — what a correct answer must achieve — in terms that can be checked against the final conclusion. Do not confuse "what triggered the analysis" with "what the analysis must answer."

**Named artifact:** Essence Statement — a single sentence naming the core problem or decision, followed by the success criteria as a short, checkable list.

**Exit criterion:** The Essence Statement is written and the success criteria are stated. A skeptic reading the statement would agree it names the real question — not a symptom, not a proxy, not the triggering event.

---

### Phase 2: Challenge Assumptions

**Why this phase exists:** An unchallenged assumption that is false propagates invisibly through every later reasoning step. By explicitly classifying and testing each assumption before establishing ground truths, the analysis prevents false premises from masquerading as verified facts — the single most common cause of first-principles analysis that sounds rigorous but is not.

**Entry criterion:** The Essence Statement from Phase 1 is complete.

**Operation:** Identify every assumption — explicit and implicit — that bears on the problem. For each one, classify it by type using the four-type scheme below, apply the prescribed treatment, and record the verdict. Surface hidden assumptions: things that are treated as given but have never been verified. When the assumption space feels too broad to enumerate by intuition, use [Ishikawa](references/ishikawa-diagram.md) to brainstorm causes by category, then bring each branch into this table as an `untested belief`. When a conclusion feels too clean or a goal feels too obvious, use [Inversion](references/inversion.md) to enumerate what would guarantee failure — each unverified precondition becomes an `untested belief` row in this table. When the stakes of a conclusion rest heavily on a particular assumption, push that assumption down toward physical law or verified ground truth status rather than accepting a weaker classification. Classification drives the method — it is not merely labelling.

**The four assumption types and their prescribed treatments:**

| Type | Prescribed Treatment |
|------|---------------------|
| **physical law** | Accept as a ground-truth candidate. Physical laws do not expire and cannot be negotiated away. |
| **current constraint** | Record the expiry conditions — what would have to change for this constraint to lift. |
| **convention** | Explicitly challenge before use. Ask whether the convention holds in this specific context or merely carries historical inertia. |
| **untested belief** | Verify, or flag as unverified. An unverified belief may be used in a derivation chain but must be visibly flagged (e.g., `GT-N?: unverified`) and any conclusion depending on it inherits an explicit confidence caveat. |

**Stakes-escalation rule:** The higher the stakes of the conclusion resting on an assumption, the more that assumption must be pushed toward physical law or verified ground truth. A critical conclusion resting on a convention or untested belief is a fragile conclusion — either verify the assumption or flag the conclusion's confidence accordingly.

**Named artifact:** Classified Assumptions Table — a table with columns: Assumption, Type, Treatment, Verdict, Verification.

**Exit criterion:** Every assumption in scope has a classification from the four-type scheme (physical law / current constraint / convention / untested belief) AND has a recorded verdict and verification note, or an explicit "unverified — flagged" note per D-07.

---

### Phase 3: Establish Ground Truths

**Why this phase exists:** Reasoning from assumptions treats contested claims as solid foundations. Ground truths — facts that survive the scrutiny applied in Phase 2 — are the only reliable anchors for derivation chains. Without an explicit list of verified ground truths, the analysis cannot distinguish a conclusion built on solid facts from one built on well-packaged conjecture.

**Entry criterion:** The Classified Assumptions Table from Phase 2 is finalized. Assumptions classified as physical law are ready to be promoted to ground truths; others have been challenged and their verdicts recorded.

**Operation:** Compile the verified ground truths from the Phase 2 analysis. A ground truth must pass the irreducibility test: it is a fact, not a belief; it can be traced to a verifiable source; and it cannot be simplified further without losing its essential claim. Assign each ground truth a stable identifier (GT-1, GT-2, etc.) that does not change for the life of the analysis. Unverified facts that must be used may be included but get the `GT-N?` suffix and inherit the confidence caveat rules from D-07. Do not include assumptions that failed Phase 2 scrutiny — discarded assumptions belong in the **Abandoned Reasoning section** of the output document (section 5), not here.

**Named artifact:** Ground Truths list — a numbered list of verified facts with stable GT-IDs and source citations. Unverified entries are marked with the `?` suffix.

**Exit criterion:** All ground truths have stable IDs, source citations or explicit unverified flags, and have passed the irreducibility test. No assumption that was discarded in Phase 2 appears in this list. The list is complete enough that Phase 4 can reason upward without needing to return to Phase 2 for new facts.

---

### Phase 4: Reason Upward

**Why this phase exists:** The methodology has established what is true (ground truths) and what can be discarded (false assumptions). The task now is to construct an answer from those truths. This phase is deliberately high-freedom because the right method for combining ground truths depends entirely on the problem's structure — there is no single correct way to reason upward that works across engineering, business, science, and design domains. Prescribing sub-steps would constrain reasoning that should be shaped by the problem, not by the methodology.

**Entry criterion:** The Ground Truths list is complete — all ground truths carry IDs and verification notes — and the Classified Assumptions Table from Phase 2 is finalized.

**Operation:** Reason upward from the ground truths toward an answer using whatever approach the problem calls for. As you go, narrate what you are trying, what you are building on, and why — reasoning is free-form, but it must be self-documenting. If a reasoning path leads to a dead end, record it in the Abandoned Reasoning section before changing course; do not quietly discard a path that might matter to someone reviewing the analysis. Do not use analogies as direct evidence — any reference to how others have solved similar problems must be grounded in a verified ground truth about their situation, not used as standalone justification. Before handing off to Phase 5, apply [Second-Order Thinking](references/second-order-thinking.md) to extend the relevant Derivation Chain with 2nd/3rd-order effects. If any extension step contradicts a Ground Truth, the conclusion returns to Phase 2 for re-challenging.

**Named artifact:** Derivation Chains — one chain per conclusion, formatted as `GT-N + GT-M → [intermediate claim] → [conclusion]`, with confidence levels per D-07. Each chain must include at least one intermediate step; a chain that goes directly from ground truth IDs to a conclusion is a flat list, not a derivation.

**Exit criterion:** ALL THREE conditions must hold: (1) the problem's core question as stated in the Essence Statement is answered, AND (2) every conclusion offered has a complete derivation chain back to named ground truths, AND (3) the [Second-Order Thinking](references/second-order-thinking.md) pass has been applied and no extension step contradicts a Ground Truth. Partial conclusions, incomplete chains, or a silently-skipped second-order pass do not satisfy this criterion and do not exit this phase.

---

### Phase 5: Validate

**Why this phase exists:** Completing a derivation chain does not guarantee the chain is sound. A chain built on an unverified assumption that is load-bearing, or one whose weakest link is never examined, produces a conclusion that looks rigorous but collapses under scrutiny. Validation is the adversarial pass — it exists to find the flaws that the forward-direction reasoning in Phase 4 was not looking for.

**Entry criterion:** The Derivation Chains artifact from Phase 4 is complete — all conclusions have chains and the core question is answered.

**Operation:** Stress-test the analysis. For each conclusion, trace the derivation chain back to its named ground truths and check that every link holds. Identify the weakest link in each chain — the step where the reasoning is most dependent on an assumption that is not fully verified, or where the inferential gap is largest. Check whether any unverified assumption (`GT-N?`) is load-bearing for a high-stakes conclusion; if it is, either verify it now or apply a confidence caveat to the conclusion. Apply the rubric in [Validation Rubric](#validation-rubric) as a systematic check — that document defines the criteria, levels, and scoring. Do not re-author the rubric criteria here; apply them.

**Named artifact:** Signed-off analysis — the complete output document with all sections present, all conclusions traced to named ground truths, and all weak links either resolved or explicitly flagged with confidence caveats. The signed-off analysis is what the methodology produces as its deliverable.

**Exit criterion:** Every conclusion traces to a named ground truth via a complete derivation chain, AND every weak link is either resolved (the assumption has been verified or reclassified) or explicitly flagged with a confidence caveat that a reader can evaluate. A skeptic inspecting the signed-off analysis can verify both conditions hold without asking the analyst for clarification.

---

## Output format

Every analysis produces a document with these six sections in this fixed order. No section may be omitted.

1. Problem Essence
2. Assumptions Table
3. Ground Truths
4. Derivation Chains
5. Abandoned Reasoning
6. Conclusion

**Honest-depth escape valve:** If a section has no genuine content for a given analysis, mark it:

> `Nothing material here — [reason explaining why this section has no content for this particular analysis and that the omission is justified, not lazy]`

The section heading must still appear. Writing `Nothing material here — [reason]` is always better than filling a section with words that say nothing.

**Derivation chain format:**

```text
GT-N + GT-M → [intermediate claim] → [conclusion]
```

Each chain must contain at least one intermediate step — the intermediate is where the reasoning happens.

**Unverified input notation:** `GT-N?` marks a ground truth that is an untested belief elevated for use in a chain. Any conclusion depending on a `GT-N?` input inherits a MEDIUM or LOW confidence rating with an explicit explanation of what verification would raise it to HIGH.

For the full annotated template with section-by-section guidance, type definitions, verdict vocabulary, and worked placeholder text, see the [First Principles Analysis Output Template](#first-principles-analysis-output-template) appendix.

---

## Before presenting conclusions

Score the completed analysis against the rubric in the
[Validation Rubric](#validation-rubric) appendix as a feedback loop:

1. **Validate** — apply each rubric criterion; quote the specific span of your analysis that satisfies or fails each criterion.
2. **Fix** — revise every criterion that does not pass.
3. **Repeat** — re-score after fixing until every criterion clears the gate.

Do not present conclusions until the rubric gate is cleared.

---

## Skill files

### Companion tools

**[Five Whys](references/five-whys.md)** — Root-cause drill-down procedure. Use when an
analysis is stuck on *why* something is true and the surface explanation feels insufficient.
The tool branches causal chains iteratively until a root cause passes a testability check,
then hands back to Phase 3 (Establish Ground Truths) with a verified causal fact.

**[Ishikawa](references/ishikawa-diagram.md)** — Breadth-first
cause-category brainstorm. Use during Phase 2 (Challenge Assumptions) when
the assumption space is multi-causal and intuition cannot enumerate it
confidently. Branches enter the Classified Assumptions Table as `untested belief` rows;
reach for Five Whys instead when the problem is single-chain depth.

**[Inversion](references/inversion.md)** — Failure-enumeration procedure.
Use during Phase 2 (Challenge Assumptions) when a conclusion or goal feels
too clean and the assumption set looks suspiciously thin. Enumerates what
would guarantee failure; each unverified precondition hands back to the
Classified Assumptions Table as an `untested belief` row. Pairs with
Pre-mortem when you want to stress-test in Phase 5 rather than challenge
in Phase 2.

**[Pre-mortem](references/pre-mortem.md)** — Prospective-hindsight failure analysis. Use
during Phase 5 (Validate) to stress-test a proposed solution by imagining it has already
failed and working backward to find the failure modes. Findings surface as weak-link flags
or confidence caveats in the signed-off analysis.

**[Trade-off Analysis](references/trade-off-analysis.md)** — Weighted-criteria decision
procedure. Use during Phase 4 (Reason Upward) when multiple viable options remain after
ground truths are established. Criteria are weighted before scoring to prevent
post-hoc rationalization, and the result feeds back as a derivation chain step.

**[Second-Order Thinking](references/second-order-thinking.md)** —
Downstream-consequence extension procedure. Use during Phase 4 (Reason
Upward) to extend a Derivation Chain with 2nd/3rd-order effects before
handing off to Phase 5. Contradicting effects route the conclusion back
to Phase 2 for re-challenging. Pairs with Inversion: Inversion looks back
at preconditions; Second-Order looks forward at consequences.

### Reference docs

- Output format template → [First Principles Analysis Output Template](#first-principles-analysis-output-template) appendix
- Validation rubric → [Validation Rubric](#validation-rubric) appendix
