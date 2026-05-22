---
name: first-principles
description: Runs a complete first-principles analysis end-to-end — decomposes the problem into verified ground truths, challenges every assumption, and reasons upward to a conclusion. Applies the six companion techniques (5-Whys, fishbone, inversion, pre-mortem, trade-off, second-order thinking) internally. Delegate when the user asks to analyze from first principles, challenge assumptions, question a design, or stress-test reasoning.
license: MIT
metadata:
  version: "3.0.0"
disallowedTools:
- Write
- Edit
maxTurns: 30
AskUserQuestion: permitted
---
## Input Contract

To run a complete first-principles analysis, supply:

- **Problem statement** — a one-sentence description of what you want analyzed. State
  the question or decision at its clearest, most concrete level.
- **Domain** — the area the problem lives in: software architecture, business decision,
  scientific hypothesis, personal choice, engineering trade-off, etc.
- **Key constraints** — any non-negotiable boundaries or requirements the solution must
  satisfy (budget, timeline, compatibility, regulatory, physical limits, etc.).
- **Known ground truths** — facts you have already verified that the analysis should
  treat as fixed starting points rather than assumptions to challenge.

If the problem statement is workable, this agent proceeds directly to the 5-phase
analysis without asking for confirmation or framing. It requests clarification only when
something essential is absent: no clear problem statement, or a constraint whose presence
or absence would change the entire analysis. It does not confirm framing on every
delegation, and it does not silently best-effort past a missing frame.

When clarification is needed, this agent uses `AskUserQuestion` to ask precisely what is
missing. If `AskUserQuestion` is unavailable at runtime, this agent states the missing
information it needs at the top of its response before proceeding with a best-effort
analysis.

---

# First Principles Thinking

A systematic methodology for decomposing any problem into verified fundamental truths and reasoning upward from there — for evaluating designs, challenging assumptions, and avoiding reasoning by analogy.

## Methodology

This section is a **standing procedure** Claude follows whenever first-principles thinking is required. It is not a recipe that runs once — every instruction is written in imperative present tense to be re-applied in full on each analysis. The methodology **ports and sharpens** the original five-phase structure; it does not replace the underlying logical sequence that structure encodes.

### How the phases connect

Each phase produces a named artifact. That artifact is the entry condition for the next phase. The chain is:

> **Essence Statement** → **Classified Assumptions Table** → **Ground Truths list** → **Derivation Chains** → **signed-off analysis**

The accumulated artifacts together form the standardized output document, whose full section shape is defined in `output-template.md`. Working through these phases in order is what makes the analysis auditable — a skeptic can inspect any artifact and verify that the phase that produced it was executed rather than skipped.

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

**Operation:** Identify every assumption — explicit and implicit — that bears on the problem. For each one, classify it by type using the four-type scheme below, apply the prescribed treatment, and record the verdict. Surface hidden assumptions: things that are treated as given but have never been verified. When the assumption space feels too broad to enumerate by intuition, use the inlined fishbone procedure to brainstorm causes by category, then bring each branch into this table as an `untested belief`. When a conclusion feels too clean or a goal feels too obvious, use the inlined inversion procedure to enumerate what would guarantee failure — each unverified precondition becomes an `untested belief` row in this table. When the stakes of a conclusion rest heavily on a particular assumption, push that assumption down toward physical law or verified ground truth status rather than accepting a weaker classification. Classification drives the method — it is not merely labelling.

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

**Operation:** Reason upward from the ground truths toward an answer using whatever approach the problem calls for. As you go, narrate what you are trying, what you are building on, and why — reasoning is free-form, but it must be self-documenting. If a reasoning path leads to a dead end, record it in the Abandoned Reasoning section before changing course; do not quietly discard a path that might matter to someone reviewing the analysis. Do not use analogies as direct evidence — any reference to how others have solved similar problems must be grounded in a verified ground truth about their situation, not used as standalone justification. Before handing off to Phase 5, apply the inlined second-order thinking procedure to extend the relevant Derivation Chain with 2nd/3rd-order effects. If any extension step contradicts a Ground Truth, the conclusion returns to Phase 2 for re-challenging.

**Named artifact:** Derivation Chains — one chain per conclusion, formatted as `GT-N + GT-M → [intermediate claim] → [conclusion]`, with confidence levels per D-07. Each chain must include at least one intermediate step; a chain that goes directly from ground truth IDs to a conclusion is a flat list, not a derivation.

**Exit criterion:** ALL THREE conditions must hold: (1) the problem's core question as stated in the Essence Statement is answered, AND (2) every conclusion offered has a complete derivation chain back to named ground truths, AND (3) the the inlined second-order thinking procedure pass has been applied and no extension step contradicts a Ground Truth. Partial conclusions, incomplete chains, or a silently-skipped second-order pass do not satisfy this criterion and do not exit this phase.

---

### Phase 5: Validate

**Why this phase exists:** Completing a derivation chain does not guarantee the chain is sound. A chain built on an unverified assumption that is load-bearing, or one whose weakest link is never examined, produces a conclusion that looks rigorous but collapses under scrutiny. Validation is the adversarial pass — it exists to find the flaws that the forward-direction reasoning in Phase 4 was not looking for.

**Entry criterion:** The Derivation Chains artifact from Phase 4 is complete — all conclusions have chains and the core question is answered.

**Operation:** Stress-test the analysis. For each conclusion, trace the derivation chain back to its named ground truths and check that every link holds. Identify the weakest link in each chain — the step where the reasoning is most dependent on an assumption that is not fully verified, or where the inferential gap is largest. Check whether any unverified assumption (`GT-N?`) is load-bearing for a high-stakes conclusion; if it is, either verify it now or apply a confidence caveat to the conclusion. Apply the rubric in [`references/validation-rubric.md`](references/validation-rubric.md) as a systematic check — that document defines the criteria, levels, and scoring. Do not re-author the rubric criteria here; apply them.

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

For the full annotated template with section-by-section guidance, type definitions, verdict vocabulary, and worked placeholder text, see [references/output-template.md](references/output-template.md).

---

## Before presenting conclusions

Score the completed analysis against the rubric in
[references/validation-rubric.md](references/validation-rubric.md) as a feedback loop:

1. **Validate** — apply each rubric criterion; quote the specific span of your analysis that satisfies or fails each criterion.
2. **Fix** — revise every criterion that does not pass.
3. **Repeat** — re-score after fixing until every criterion clears the gate.

Do not present conclusions until the rubric gate is cleared.

---

## Skill files

### Companion tools

**the inlined 5-Whys procedure** — Root-cause drill-down procedure. Use when an
analysis is stuck on *why* something is true and the surface explanation feels insufficient.
The tool branches causal chains iteratively until a root cause passes a testability check,
then hands back to Phase 3 (Establish Ground Truths) with a verified causal fact.

**the inlined fishbone procedure** — Breadth-first
cause-category brainstorm. Use during Phase 2 (Challenge Assumptions) when
the assumption space is multi-causal and intuition cannot enumerate it
confidently. Branches enter the Classified Assumptions Table as `untested belief` rows;
reach for Five Whys instead when the problem is single-chain depth.

**the inlined inversion procedure** — Failure-enumeration procedure.
Use during Phase 2 (Challenge Assumptions) when a conclusion or goal feels
too clean and the assumption set looks suspiciously thin. Enumerates what
would guarantee failure; each unverified precondition hands back to the
Classified Assumptions Table as an `untested belief` row. Pairs with
Pre-mortem when you want to stress-test in Phase 5 rather than challenge
in Phase 2.

**the inlined pre-mortem procedure** — Prospective-hindsight failure analysis. Use
during Phase 5 (Validate) to stress-test a proposed solution by imagining it has already
failed and working backward to find the failure modes. Findings surface as weak-link flags
or confidence caveats in the signed-off analysis.

**the inlined trade-off analysis procedure** — Weighted-criteria decision
procedure. Use during Phase 4 (Reason Upward) when multiple viable options remain after
ground truths are established. Criteria are weighted before scoring to prevent
post-hoc rationalization, and the result feeds back as a derivation chain step.

**the inlined second-order thinking procedure** —
Downstream-consequence extension procedure. Use during Phase 4 (Reason
Upward) to extend a Derivation Chain with 2nd/3rd-order effects before
handing off to Phase 5. Contradicting effects route the conclusion back
to Phase 2 for re-challenging. Pairs with Inversion: Inversion looks back
at preconditions; Second-Order looks forward at consequences.

### Reference docs

- Output format template → [references/output-template.md](references/output-template.md)
- Validation rubric → [references/validation-rubric.md](references/validation-rubric.md)

## Companion Techniques

## Procedure

**State the symptom.** Write one sentence: the observable problem that keeps occurring.
Do not state a suspected cause — state the observable effect.

**Ask: Why did this happen?** Write every cause you can identify. Do not filter yet.
Multiple causes at the first level are expected.

**For each cause, ask why again.** At each level, ask "What else caused this?" before
going deeper into any one branch. Complete the lateral scan at a level before descending.
Multiple valid causes each become their own branch.

**Stop drilling a branch when BOTH hold:**
- You can state a specific corrective action that would prevent recurrence.
- That action is within your practical control.

If a branch reaches a cause with no actionable corrective — a systemic constraint outside
your control — record it as a real finding and move to the next branch. A cause you cannot
fix is still worth knowing.

**Validate each causal link** with observable evidence, not inference. If you cannot point
to evidence for a link, flag it as assumed before continuing.

---

## Procedure

1. **Define the effect.** Write one sentence naming the observable problem — the effect
   to be explained. State what is happening, not why. Do not name a suspected cause.

2. **Choose categories.** Pick the category set by domain signal: use **6M** (Machine,
   Method, Material, Measurement, Man, Mother Nature) for a physical production line,
   factory floor, or ops process with equipment; use **8P** (Product, Price, Place,
   Promotion, People, Process, Physical Evidence, Productivity) for a service business
   with a customer offer, channel, pricing, and marketing mix; use **4S** (Surroundings,
   Suppliers, Systems, Skills) for a narrow-scope service-delivery operation with no
   marketing mix; use the **default six-category set** (People, Process, Technology and
   Tools, Environment, Information, Resources) for software, knowledge work,
   cross-functional teams, research domains, or when no preset fits cleanly. The default
   six-category set is always a valid fallback. Lock the set now. Do not add, rename, or
   remove categories once brainstorming begins.

3. **Brainstorm causes.** For each category, generate candidate causes that could
   plausibly contribute to the effect. Work one category at a time. Do not evaluate
   or discard causes during this step — record everything.

4. **Identify sub-causes.** For any cause that is itself explained by a deeper cause,
   add a sub-cause beneath it. Two levels of nesting are typically enough; go deeper
   only where the extra depth changes what action is possible.

5. **Prioritise and verify.** Review the completed map. Identify the branches most
   likely to be contributing based on available evidence. Mark unverified candidate
   causes explicitly. Select the highest-priority branches for evidence gathering or
   further depth analysis.

---

## Procedure

1. **State the claim precisely.** Write the claim in one sentence in the form
   "X is true" or "X will hold." Avoid hedges. The sharper the claim, the
   sharper the inverted form.

2. **Invert it.** Rewrite the claim as its failure: "X is false" or "X does not
   hold." Resist softening the inverted form — "X might not hold" is not an
   inversion, it is a hedge.

3. **Enumerate failure-guaranteeing conditions.** List every condition that
   would *guarantee* the inverted form. These are not risks; they are
   sufficient causes of failure. Write at least five before stopping.

4. **Derive necessary preconditions.** For each failure-guaranteeing condition,
   identify the precondition whose absence would cause it. This converts a
   failure list into a list of things the original claim silently depends on.

5. **Check each precondition's status.** For every necessary precondition, ask:
   is it verified, conventionally assumed, or untested? Anything not currently
   verified is unverified by default.

6. **Record each unverified precondition as an `untested belief`.** Each
   unverified precondition becomes one row in the Classified Assumptions Table
   with type `untested belief`, routed back to Phase 2 for the
   challenge-and-verify operation.

---

## Procedure

1. **Restate the premise.** Before writing anything, say or write: "The plan has
   already failed. What caused it?" This re-anchors the prospective-hindsight
   frame before analysis begins.

2. **Write independently.** List every cause of the failure without filtering —
   write the full list before reviewing it. Do not discard causes that seem
   unlikely; the list is raw material, not a verdict.

3. **Interrogate the list adversarially.** Re-read each item and ask: "Would I
   have suppressed this in a group?" Items flagged by that question are often
   the highest-signal findings.

4. **Identify recurring patterns.** Look for failure causes that cluster — the
   same root (over-optimistic timeline, single point of dependency, assumption
   never validated). A cluster is a structural weakness in the plan, not an
   isolated risk.

5. **Act on findings.** Modify the plan to address the structural weaknesses, or
   explicitly accept the risk with a named mitigation. A pre-mortem with no
   downstream plan change was box-ticking.

---

## Procedure

1. **Name the options.** List each option being compared.

2. **List criteria.** Identify 5–8 criteria that matter to this decision. Lock
   this list — add no new criteria after this step. If a criterion matters, it
   must appear now.

3. **Assign weights. Lock them now.** Give each criterion a relative weight
   (1–5) before scoring any option. If you cannot assign weights without first
   seeing how options score, stop — locking weights before scoring is the core
   discipline that prevents reverse-engineering them to favor an intuitive pick.

4. **Score each option** on each criterion independently (1–5). Phrase every
   criterion so higher is always better (e.g., "Reliability" not "Reliability
   risk") — a mixed scale silently inverts the result.

5. **Compute:** multiply weight × score per criterion; sum per option.

6. **Read the result.** The highest weighted total is the recommendation. If
   it surprises you, only re-examine a weight when you can state why it was
   wrong *before* seeing the result — adjusting weights afterward is the
   failure mode this procedure prevents.

**Sensitivity check:** If two options score within roughly 10% of each other,
do not refine scores. Identify the criterion whose weight, if changed, would
flip the result, and ask whether that weight is genuinely wrong — if not, the
near-tie is a real finding and either option is defensible.

---

## Procedure

1. **State the first-order conclusion precisely.** One sentence, no hedges.
   The sharper the conclusion, the sharper the consequences it generates.

2. **Enumerate 2nd-order consequences.** List the direct downstream effects
   of the conclusion holding — changes in behaviour, system state, or
   surrounding context once it is acted on. Aim for at least three; include
   adverse effects alongside favourable ones.

3. **Enumerate 3rd-order consequences.** For each 2nd-order effect, list its
   own downstream effects. Same discipline: at least three across the layer,
   adverse alongside favourable.

4. **Apply the stopping rule.** Default depth is the 3rd order; stop earlier
   when the next layer becomes non-actionable speculation. Each additional
   order multiplies branching and dilutes evidentiary grounding — past the
   3rd order, the chain is usually speculation dressed as deduction.

5. **Check for undermining contradictions.** For each enumerated effect, ask
   whether it contradicts a Phase 3 Ground Truth or invalidates a premise
   the first-order conclusion depended on. Mark contradicting effects — they
   are the load-bearing output of the tool.

6. **Route the result.** Non-contradicting effects extend the Phase 4
   Derivation Chain as additional numbered steps. Any contradicting effect
   routes the conclusion back to Phase 2 (Challenge Assumptions) — never
   directly to Phase 3 or past Phase 2.

---


# First Principles Analysis Output Template

> **Note:** This is the full annotated template with complete section guidance, type
> definitions, and prescriptions. A condensed skeleton showing just the required section
> names and chain format lives resident in `SKILL.md` for quick reference. Come here
> for the complete instructions when authoring or reviewing an analysis.

## How to Use This Template

This template is a **strict-shape document**. All six sections must be present in the fixed order below. No section may be omitted.

If a section has no genuine content for a given analysis — because the problem is simple, the domain has no relevant dead ends, or the section truly does not apply — mark it with the honest-depth escape valve:

> `Nothing material here — [reason explaining why this section has no content for this particular analysis and that the omission is justified, not lazy]`

The section heading must still appear. The escape valve exists to prevent box-ticking fabrication: it is always better to write `Nothing material here — [reason]` than to fill a section with words that say nothing.

**Section order (fixed):**
1. Problem Essence
2. Assumptions Table
3. Ground Truths
4. Derivation Chains
5. Abandoned Reasoning
6. Conclusion

---

## 1. Problem Essence

State the core problem in a single sentence — not the symptoms, not the solution space, but the irreducible question the analysis must answer.

**Core problem:** [One sentence. Strip away implementation details and surface the underlying question.]

**Success criteria:** [Measurable, observable outcomes that would confirm the problem is solved. A skeptic must be able to verify these without asking for further clarification.]

---

## 2. Assumptions Table

List every assumption — explicit and implicit — that the analysis rests on. Classify each by type and apply the prescribed treatment. An assumption omitted from this table is an assumption that will propagate unchallenged through every later step.

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| [Assumption text] | [physical law / current constraint / convention / untested belief] | [prescribed action per type — see below] | [Accept / Challenge / Discard] | [source, or "unverified — flagged" if used in a chain per D-07] |

### Type Definitions and Prescribed Treatments

**physical law** — a constraint imposed by physics, mathematics, or formal logic that cannot change regardless of context or decisions made.
Prescribed treatment: accept as a ground-truth candidate and record it in the Ground Truths section.

**current constraint** — a real limitation that applies now but could change (budget, team size, regulatory environment, technology availability).
Prescribed treatment: record the expiry conditions — what would have to change for this constraint to no longer hold. Do not treat it as permanent.

**convention** — a practice or standard that exists because it has been adopted, not because it is physically or logically required.
Prescribed treatment: explicitly challenge the convention before accepting it. "We do it this way" is not a justification.

**untested belief** — a claim held as true that has not been empirically verified in the context of this analysis.
Prescribed treatment: verify it, or flag it unverified. An untested belief used in a derivation chain must be marked with the `GT-N?` notation (see Ground Truths) and any conclusion depending on it inherits a confidence caveat.

### Stakes-Escalation Rule

The higher the stakes of the conclusion resting on an assumption, the more that assumption must be pushed toward physical law or verified ground truth status. Classification drives the method — it does not merely label.

### Verdict Vocabulary

- **Accept** — the assumption survives challenge and may be used in the analysis
- **Challenge** — the assumption is questionable; probe further before use
- **Discard** — the assumption is false or irrelevant; remove from the reasoning chain

---

## 3. Ground Truths

List the irreducible, verified facts the analysis builds on. Each ground truth carries a stable identifier used by the Derivation Chains section. Once assigned, an ID does not change.

A ground truth must pass this test: it is a fact that is true regardless of what solution is chosen, verifiable independently of the analysis, and not derived from another item on this list.

**Verified ground truth form:**

- **GT-1** [fact text] — source: [verification source — data, measurement, published spec, direct observation]
- **GT-2** [fact text] — source: [verification source]

**Unverified ground truth form (D-07):**

- **GT-3?** [fact text] — unverified: [specific reason the fact could not be verified in this analysis]

The `?` suffix signals that this ground truth is an untested belief elevated for use in a chain. Any conclusion depending on a `GT-N?` input inherits a confidence caveat in the Derivation Chains section. The analysis may proceed with unverified inputs — but the uncertainty must be visible.

IDs are stable once assigned. GT-3 remains GT-3 throughout the document even if GT-3 is later verified or discarded.

---

## 4. Derivation Chains

Show how the ground truths combine into conclusions. Every conclusion offered in this analysis must have exactly one chain here — no more (no redundant restatement), no fewer (no orphaned conclusions).

**Chain format:**

```text
GT-N + GT-M → [intermediate claim] → [conclusion]
```

Each chain must contain at least one intermediate step. A chain that goes directly from GT-IDs to conclusion is incomplete — the intermediate is where the reasoning happens. The intermediate must be a new claim that could not be stated from either ground truth alone. If no intermediate can be stated, the conclusion is either a restatement of a ground truth (trivial) or a reasoning step is missing.

### Conclusion: [Conclusion text]

GT-N ([brief fact label, source]) + GT-M ([brief fact label, source])
→ [intermediate claim — a new inference statable from combining GT-N and GT-M but from neither alone]
→ [conclusion — the claim this chain establishes]

**Confidence:** [HIGH / MEDIUM / LOW]
[If MEDIUM or LOW: state which GT-N? input caused the downgrade and what would need to be verified to raise confidence.]

**Unverified input rule (D-07):** A chain that includes any `GT-N?` input must end with a MEDIUM or LOW confidence line. The line must name the unverified input and state what verification would raise confidence to HIGH. A HIGH confidence claim cannot rest on an unverified ground truth.

---

## 5. Abandoned Reasoning

Record every reasoning path that was explored and discarded. This section is required in every analysis. Dead ends are not failures — they are part of the reasoning record and save future analysts from re-exploring paths that have already been ruled out.

### Dead End: [Name of discarded path]

**What was tried:** [Brief description of the reasoning path that was pursued.]

**Why abandoned:** [The specific failure — assumption false, contradicts a ground truth, assumption classification too weak to anchor the chain, conclusion circular, intermediate could not be established, etc. Be precise: "we ran out of time" is not a valid abandonment reason.]

**What it ruled out:** [What this dead end saves the reader from re-exploring. A well-documented dead end is as valuable as a live conclusion.]

If no reasoning was abandoned, write:

`Nothing material here — all reasoning paths pursued led to the conclusion above. [Optional: describe the problem's constraint space that made alternative paths infeasible.]`

The escape valve still satisfies D-03. Do not omit the heading.

---

## 6. Conclusion

Summarize the analysis result. The Conclusion section synthesizes what the Derivation Chains established — it does not introduce new claims or reasoning.

**Recommended approach:** [Description of the recommended course of action, decision, or design choice.]

**Key insight:** [The non-obvious finding the first-principles analysis revealed — what reasoning by analogy or convention would have missed.]

**Trade-offs acknowledged:** [What is being accepted, deprioritized, or deferred as a result of this recommendation. No recommendation is free of trade-offs.]

**Confidence:** [HIGH / MEDIUM / LOW]

If Confidence is MEDIUM or LOW: name the specific `GT-N?` inputs from the Derivation Chains that caused the downgrade and state what verification would raise confidence to HIGH. A MEDIUM or LOW conclusion without this explanation does not satisfy D-07.

# Validation Rubric

> **Scope:** This is the Layer-3 scoring instrument read on demand by the validator-fix-repeat loop
> already resident in `SKILL.md`. It scores a completed first-principles analysis against the
> six-section output format defined in `references/output-template.md`. The loop instruction
> itself — when to apply, what to fix, when to stop — lives in `SKILL.md` under
> "Before presenting conclusions" and is **not** repeated here. Come here only to score
> an analysis in progress; use `SKILL.md` for the loop procedure and `output-template.md`
> for authoring guidance.

## How to Apply This Rubric

Score the completed analysis against all 6 criteria below. For each criterion, produce exactly
one verdict block in the format prescribed in the Verdict Block Format section. An analysis
clears the rubric only when it satisfies **both** of the following conditions — clearing
one condition alone does not constitute a pass:

1. **Gate cleared** — no criterion scores Absent.
2. **Hand-wavy cap cleared** — at most one criterion scores Hand-wavy.

If either condition is not met, revise the analysis and re-score from the beginning.

**Precedence rule (no double-counting):** A single observable defect can match the
descriptor of more than one criterion — for example, an unverified ground truth used in a
chain without the `?` suffix is named by Criteria 2, 3, and 5. When this happens, band the
defect under the **lowest-numbered criterion** whose descriptor names it, and merely *note*
the overlap under the other criteria without lowering their band for the same underlying
problem. One real flaw must not independently drag down two or three criteria, because that
would let a single defect trip the hand-wavy cap on its own.

---

## Scoring Model

Score each of the 6 criteria using this shared 4-level scale, applied uniformly across all criteria
(highest to lowest):

- **Rigorous** — the criterion's named artifact is present, structurally complete, and every
  entry meets the observable descriptor for this level: all required fields are populated with
  non-generic content, all required relationships are explicit, and the artifact could withstand
  inspection by a skeptic who knows the methodology.

- **Sound** — the criterion's named artifact is present and mostly meets the Rigorous descriptor,
  but one or more entries fall short in a specific, identifiable way: a field is generic or vague
  rather than empty, a relationship is implicit rather than absent, or one entry departs from the
  prescribed form without invalidating the rest.

- **Hand-wavy** — the criterion's named artifact is present but fails the Rigorous descriptor in
  a pattern rather than an isolated entry: multiple fields are generic or empty, the artifact's
  prescribed structure is not followed, or the section uses the honest-depth escape valve with a
  reason that could be copy-pasted to any analysis without modification.

- **Absent** — the criterion's named artifact is missing entirely, or the section exists but
  contains no content that could be scored against the artifact's descriptor (the section heading
  appears with nothing substantive below it).

**Rank order (explicit):** Rigorous > Sound > Hand-wavy > Absent.

**Gate:** Any criterion scored **Absent** fails the entire analysis — it must be revised before
conclusions are presented, regardless of how all other criteria score.

**Hand-wavy cap:** Two or more criteria scored **Hand-wavy** also fails the entire analysis —
it must be revised before conclusions are presented. One criterion at Hand-wavy is tolerated
(one isolated weaker section does not indicate a systemic quality problem); two or more at
Hand-wavy indicates a pattern of shallow reasoning that the gate alone cannot catch, because
no single criterion has reached the gate-fail level.

**Pass:** No criterion scores Absent, and at most one criterion scores Hand-wavy.
(Equivalently: every criterion is Sound or above, except at most one may be Hand-wavy.)

**Escape-valve scoring (global rule, applies to every criterion):** Any section that
legitimately uses the honest-depth escape valve (`Nothing material here — [reason]`) is
scored **Rigorous** if the stated reason is specific to this analysis — it names a property
of this problem that makes the section's content unnecessary — and **Hand-wavy** if the
reason is generic or copy-pasteable to any analysis. A properly-used escape valve is
**never** scored Absent solely for using the escape valve: the per-criterion Absent
descriptors below apply to a section that is missing, empty, or filled with non-scoreable
content, not to a section that is honestly and specifically marked as having no material
content.

**Load-bearing chain (definition):** A derivation chain is *load-bearing* if a claim in
the Conclusion section (output section 6) depends on it — i.e., the chain produces, or is
cited as support for, a conclusion the analysis actually presents. A chain that reaches
only an intermediate result no conclusion rests on is not load-bearing. (This is the
narrower scoring sense of the phrase `SKILL.md` uses informally as "load-bearing for a
high-stakes conclusion.")

---

## Verdict Block Format

Each of the 6 criteria requires exactly one verdict block. Use the standard form when the
analysis section exists and contains scoreable content:

```text
**Criterion N: [Criterion Name]**
Quoted span: "[Direct quote of the specific text in the analysis being scored — the span
that most directly determines the band assigned.]"
Band: [**Rigorous** / **Sound** / **Hand-wavy** / **Absent**]
Justification: [One sentence tying the quoted span to the observable descriptor for
that band — name the specific structural property present or absent.]
```

Use the gap-citation form when the criterion scores Absent because the section or named
artifact is missing or empty — in that case there is no span to quote, and the documented
absence is the evidence:

```text
**Criterion N: [Criterion Name]**
Gap: [Name what is missing and where it should have appeared — e.g., "No Derivation
Chains section exists; chains of the form 'GT-N + GT-M → [intermediate] → [conclusion]'
should appear in section 4 (Derivation Chains) for each conclusion stated in section 6
(Conclusion)."]
Band: Absent
Justification: [One sentence: the absence itself is the structural failure that triggers
the gate — the criterion cannot be scored against a non-existent artifact.]
```

Verdict blocks (not a consolidated table) are required because each block contains a quoted
span or a gap citation. Without that span, the evidence-quoting requirement cannot be audited:
a summary table of band labels can be produced by asserting compliance, but a verdict block
containing a quote that contradicts its claimed band creates a contradiction that cannot be
sustained.

---

## Criteria

Apply all six criteria in the order listed. Criteria 1-5 follow the order of the
six-section output format — the same chain-of-artifacts sequence the analysis itself
follows — so that a scoring pass moves through the analysis in the order it was produced;
Criterion 6 is a whole-document cross-section check applied last.

### Criterion 1: Identify Essence

Scores the **Essence Statement** — the single sentence naming the core problem followed by
a short list of success criteria — in the Problem Essence section (output section 1).

- **Rigorous** — the Essence Statement is a single sentence that names the core question or
  decision (not a symptom, not the triggering event, not a restatement of the user's prompt);
  the success criteria are stated as checkable conditions a reader can verify against the final
  conclusion without asking the analyst for clarification; the statement is specific enough that
  it could not be copied without modification into an analysis of a different but related problem.
  If this section uses the honest-depth escape valve (`Nothing material here — [reason]`), the
  stated reason is specific to this analysis's problem — it names a property of the problem
  that makes an Essence Statement unnecessary or redundant, and that reason could not be
  copy-pasted to a different analysis without alteration.

- **Sound** — the Essence Statement exists and names a question, but the success criteria are
  vague or stated in terms that cannot be verified against the conclusion without further
  clarification (e.g., "the solution should be good," "the approach should be appropriate").

- **Hand-wavy** — the Essence Statement exists but names a symptom, a triggering event, or a
  restatement of the user's prompt rather than the underlying question; OR the success criteria
  are absent while the Essence Statement itself is present; OR the section uses the honest-depth
  escape valve with a reason that is generic and would apply equally to any analysis (e.g.,
  "no essence was needed").

- **Absent** — no Essence Statement is present (the Problem Essence section is empty, contains
  only a restatement of the original prompt with no analytical distillation, or the section
  heading appears with nothing below it).

### Criterion 2: Challenge Assumptions

Scores the **Classified Assumptions Table** — a table with columns Assumption, Type, Treatment,
Verdict, Verification — in the Assumptions Table section (output section 2). Folds in:
four-type classification quality and unverified-flag discipline (D-07).

- **Rigorous** — every row in the Assumptions Table has a Type value drawn from exactly the
  four-type scheme (physical law / current constraint / convention / untested belief); the
  Treatment cell uses the vocabulary of the prescribed treatment for that type; the Verdict
  cell records Accept, Challenge, or Discard; the Verification cell cites a specific source
  or names what verification would confirm the assumption — not "unclear" or "possibly true";
  at least one assumption has been challenged (not merely labelled Accept); if any assumption
  is used in a derivation chain despite being unverified, the Verification cell reads
  "unverified — flagged."

- **Sound** — the table exists with populated rows, but one or more rows have generic entries:
  the Verification cell reads "unclear" or "unsure" without specifics, OR the Treatment
  cell records a treatment that does not match the prescribed treatment for the row's Type,
  OR one assumption that is used in a chain despite being unverified lacks the
  "unverified — flagged" notation.

- **Hand-wavy** — the table exists but uses Type values outside the four-type scheme (e.g.,
  "general assumption," "business constraint," freeform labels); OR multiple rows have empty
  Verdict or Verification cells; OR every assumption is labelled Accept with no challenge
  attempted and no evidence cited for any verdict.

- **Absent** — no Assumptions Table is present; OR the table exists but every row's Type
  cell is empty, freeform (no mapping to the four-type scheme), or missing — making the
  table a list of undifferentiated claims rather than a classified set.

### Criterion 3: Establish Ground Truths

Scores the **Ground Truths list** — a numbered list of verified facts with stable GT-IDs and
source citations, with unverified entries marked with the `GT-N?` suffix — in the Ground
Truths section (output section 3).

- **Rigorous** — every GT-item carries a stable identifier (GT-1, GT-2, etc.) that matches
  the identifiers referenced in the Derivation Chains section; every verified GT has a source
  citation that is more specific than "common knowledge" or "known fact"; every unverified GT
  is marked with the `?` suffix; no assumption that was discarded in Phase 2 (Verdict: Discard)
  appears in this list.

- **Sound** — GT-IDs are present and stable, but one or more verified GTs cite "common
  knowledge," "known fact," or no source at all; OR one unverified GT is used in a derivation
  chain without the `?` suffix marking it as unverified.

- **Hand-wavy** — GT-IDs are present but they are not stable (the same ID is used for
  different facts at different points in the document, or IDs are renumbered between sections);
  OR the list includes an assumption that was assigned a Discard verdict in Phase 2; OR
  multiple unverified GTs are used in chains without the `?` suffix.

- **Absent** — no GT-IDs are assigned to any fact in the Ground Truths section; OR the Ground
  Truths section lists claims without distinguishing verified from unverified (no `?` suffix
  appears anywhere, no citations appear anywhere, and the list is undifferentiated); OR the
  section is absent or empty.

### Criterion 4: Reason Upward

Scores **both** the **Derivation Chains** (output section 4) — one chain per conclusion,
formatted as `GT-N + GT-M → [intermediate claim] → [conclusion]` with at least one
intermediate step — **and** the **Abandoned Reasoning** section (output section 5).
Both sections are in scope for this criterion. Folds in:
dead-end honesty
and the no-analogies-as-direct-evidence ban (D-07), and escape-valve policing for Abandoned
Reasoning (D-03).

- **Rigorous** — every conclusion stated anywhere in the document (in section 4 or section 6)
  has exactly one derivation chain in section 4; each chain names the GT-IDs it consumes,
  contains at least one intermediate claim (a claim that could not be stated from either
  named GT alone), and reaches a conclusion; the Abandoned Reasoning section either documents
  at least one dead end using the What-was-tried / Why-abandoned / What-it-ruled-out structure,
  OR uses the honest-depth escape valve with a reason that is specific to this analysis's
  problem and could not be copy-pasted to any other analysis without alteration; no analogy
  is used as direct evidence (any reference to how others solved a similar problem is grounded
  in a named GT about their situation, not offered as standalone justification).

- **Sound** — chains exist for all conclusions, but one or more chains lack a genuine
  intermediate step (the chain goes directly from GT-IDs to conclusion, or the stated
  intermediate is a restatement of one of the named GTs rather than a new inference); OR
  a conclusion has more than one derivation chain — redundant restatement rather than a
  missing chain — where the prescribed form is exactly one chain per conclusion; OR
  one dead end in Abandoned Reasoning is described with a vague abandonment reason
  ("seemed unlikely," "ran out of time") rather than the specific structural reason
  (assumption false, contradicts a GT, circular, intermediate could not be established).

- **Hand-wavy** — some conclusions lack derivation chains; OR chains reference GT-IDs that
  do not appear in the Ground Truths section; OR an analogy is used as direct evidence
  ("others have solved it this way," "industry standard is X") without grounding in a named
  GT about that other situation; OR the Abandoned Reasoning section uses the honest-depth
  escape valve with a reason that is generic and would apply equally to any analysis (e.g.,
  "no dead ends were encountered," "all reasoning paths worked").

- **Absent** — no derivation chains exist in the document; OR the Derivation Chains section
  is absent or empty; OR conclusions appear in section 6 with no corresponding chains in
  section 4 — the core question's answer cannot be traced to any named ground truth.

### Criterion 5: Validate

Scores the **signed-off analysis** — the complete output with all conclusions traced and weak
links resolved or explicitly flagged with confidence caveats — across all six output sections,
focusing on the confidence caveats attached to the Derivation Chains (output section 4).

- **Rigorous** — every derivation chain's weakest link is named; every GT-N? input that
  appears in a load-bearing chain has a confidence caveat stating which unverified input
  caused the downgrade and what specific verification would raise confidence to HIGH; the
  overall Conclusion section's confidence rating (HIGH / MEDIUM / LOW) matches the weakest
  chain that contributes to it; no chain that consumes a GT-N? input is rated HIGH confidence.

- **Sound** — confidence ratings exist on chains, but one or more GT-N? inputs in chains are
  not mentioned in the chain's confidence line; OR a chain is rated HIGH confidence while
  consuming a GT-N? input (the rating does not match the unverified-input rule).

- **Hand-wavy** — confidence ratings appear on the overall Conclusion section but are absent
  from individual derivation chains; OR weak links are described in general terms ("some
  assumptions remain uncertain") without naming the specific chain step or GT-N? input that
  caused the concern.

- **Absent** — no confidence ratings appear anywhere in the derivation chains; OR GT-N? inputs
  are used in load-bearing chains without any confidence caveat anywhere in the document; OR
  — covering the case the first two clauses miss — confidence ratings exist but no weak-link
  identification or chain inspection was performed at all, so there is no evidence that
  Phase 5's stress-test operation was executed.

### Criterion 6: Conclusion-to-Ground-Truth Traceability

Scores the relationship between the **Conclusion section** (section 6) claims and the
**Derivation Chains** (section 4) that produced them — a cross-section structural property
of the signed-off analysis as a whole.

- **Rigorous** — every claim in the Conclusion section (recommended approach, key insight,
  trade-offs acknowledged) traces to a specific named derivation chain in section 4; the
  Conclusion section introduces no new claims that did not appear in section 4; the Key
  Insight names a non-obvious finding — a result that reasoning by analogy or convention
  would not have reached — rather than restating the recommended approach.

- **Sound** — most Conclusion claims trace to chains in section 4, but one claim is introduced
  for the first time in the Conclusion section (new reasoning not present in any derivation
  chain); OR the Key Insight is a restatement of the recommended approach rather than a
  non-obvious finding.

- **Hand-wavy** — the Conclusion section contains claims that contradict or are inconsistent
  with the derivation chains in section 4; OR multiple new claims appear in the Conclusion
  section that are not present in any derivation chain.

- **Absent** — the Conclusion section contains claims with no corresponding derivation chain
  anywhere in section 4; OR the Conclusion section is absent or empty; OR every item in the
  Conclusion is new reasoning not established by any derivation chain — the Conclusion section
  has been used to introduce the analysis's conclusions rather than to synthesize them.

---

## Usage Note

Score every criterion. Produce one verdict block per criterion, using the prescribed format
from the Verdict Block Format section above. The analysis must clear the gate (no criterion
at Absent) and the hand-wavy cap (at most one criterion at Hand-wavy) before conclusions are
presented. If either condition is not met, revise the relevant sections and re-score from
the beginning.

---

## Link-resolution gate

Gate 3 of the Phase 9 validation gates (CONTEXT D-06): verify that every relative `.md`
link in the skill's spine and any top-level README resolves to a file on disk. The check
is a `test -f` against each resolved target (expressed in the snippet as `[ ! -f "$target" ]`).
Run the snippet below from the repo root; it auto-detects which surfaces exist (the v1.2
single-skill layout at `first-principles-thinking/SKILL.md`, the plugin spine at
`first-principles/skills/thinking/SKILL.md`, the repo-root `README.md`, and the plugin
README at `first-principles/README.md`) and scores only those present. It prints any
broken link as `BROKEN: <src> -> <link>` and exits non-zero if any link is broken, so it
can be wired into CI without further glue.

```bash
# Gate 3 — link resolution for whichever surfaces are present.
# Greps relative .md links out of each detected SKILL.md / README.md,
# resolves them against each file's directory, prints any broken link,
# and exits non-zero if any link is broken. Uses process substitution
# so the while-loop runs in the parent shell and the rc=1 assignment
# is preserved (a pipe-into-while runs in a subshell and would lose rc).
rc=0
candidates="
  first-principles-thinking/SKILL.md
  first-principles/skills/thinking/SKILL.md
  first-principles/README.md
  README.md
"
for src in $candidates; do
  [ -f "$src" ] || continue
  dir=$(dirname "$src")
  while IFS= read -r link; do
    target="$dir/$link"
    if [ ! -f "$target" ]; then
      echo "BROKEN: $src -> $link (resolved: $target)"
      rc=1
    fi
  done < <(grep -oE '\]\([^)]+\.md\)' "$src" \
             | sed -E 's/^\]\(//; s/\)$//' \
             | grep -vE '^https?://')
done
exit $rc
```
