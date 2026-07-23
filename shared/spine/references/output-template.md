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

### Converting structured-technique outputs into chains

Structured-technique outputs (trade-off matrices, second-order effect lists) do not appear in this section as-is — each converts into the chain format above using the rule for its technique below. This subsection is the single source of truth for the conversion; the per-technique Handoff sections point back here rather than restating it, so future structured techniques extend this one place.

**Trade-off matrix → one chain.** A trade-off matrix collapses into ONE chain whose intermediate cites the winning weighted total and whose endpoint names a single recommended option:

```text
GT-refs (criteria's factual basis) → weighted totals (the winning total vs. the runner-up, naming the high-weight criteria that drive it) → recommended option
```

Example: `GT-2 + GT-5 (criteria facts) → weighted totals: B=82 > A=64, driven by reliability×warranty → recommend B`. The full matrix stays in the technique's own output — this subsection carries only the single collapsed chain, never the matrix re-expressed row-by-row (that would violate the one-chain-per-conclusion rule above). An exact tie between weighted totals still resolves to a single named recommended option; a tie must not produce a multi-option chain endpoint.

**Second-order effect list → order-marked extension.** A second-order effect list extends the parent chain IN PLACE as additional order-marked steps, each carrying the same evidentiary discipline as the first-order steps that produced the conclusion:

```text
GT-N → first-order conclusion →[2nd] [2nd-order effect] →[3rd] [3rd-order effect] (contradicts GT-M → back to Phase 2)
```

Example: `GT-1 → first-order conclusion →[2nd] flag-config surface grows →[3rd] flag debt accumulates (contradicts GT-4 → back to P2)`. The order marks (`[2nd]`, `[3rd]`) make the extension's sequence legible. A contradicting effect routes the conclusion back to Phase 2 — never directly to Phase 3 or past Phase 2. A pass that surfaces no non-contradicting downstream effect leaves the parent chain unextended — a clean no-op, not an error.

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
