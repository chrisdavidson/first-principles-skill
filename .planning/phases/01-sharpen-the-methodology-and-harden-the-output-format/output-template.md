# First Principles Analysis Output Template

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
