# First Principles Analysis Output Template

> **Note:** This is the full annotated template with complete section guidance, type
> definitions, and prescriptions. A condensed skeleton showing just the required section
> names and chain format lives resident in the agent body (`SKILL.md` on the skill surface, `agents/first-principles.md` on the agent surface) for quick reference. Come here
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
| [Assumption text] | [physical law / current constraint / convention / untested belief] | [prescribed action per type — see below] | [Accept / Challenge / Discard] — [justification/reason] | [source, or "unverified — flagged" if used in a chain per D-07] |

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

The Verdict cell is a token prefix followed by an em-dash and the justification — the bare
token leads so it stays matchable, and the em-dash prose carries the reasoning:

- **Accept** — the assumption survives challenge and may be used in the analysis (e.g., "Accept — survives P2 challenge; physical-law backed by GT-1")
- **Challenge** — the assumption is questionable; probe further before use (e.g., "Challenge — vendor benchmark unverified, flagged GT-5?")
- **Discard** — the assumption is false or irrelevant; remove from the reasoning chain (e.g., "Discard — contradicted by GT-2, no longer load-bearing")

**A current-constraint verdict records its expiry at the point of use.** An assumption classified `current constraint` is accepted only until that constraint lapses; the verdict cell says when. The expiry belongs in the em-dash justification and never in the token slot — the token slot carries one of the three tokens above and nothing else.

**Conforming — a current constraint recording its expiry:**

```text
Accept — expires at term end (1 or 3 years); until then the constraint is contractual, not physical
```

**Non-conforming — the expiry hoisted into the token slot:**

```text
Current constraint (expires at term end) — contractual, not physical
```

The vocabulary above is unchanged because run 3 rendered four current-constraint rows conformingly on the identical prompt by putting the expiry in the justification — this is a worked example, not a schema change.

---

## 3. Ground Truths

List the irreducible, verified facts the analysis builds on. Each ground truth carries a stable identifier used by the Derivation Chains section. Once assigned, an ID does not change.

A ground truth must pass this test: it is a fact that is true regardless of what solution is chosen, verifiable independently of the analysis, and not derived from another item on this list.

Every ground truth carries a **provenance label** answering one question: *did this analysis read the asserted figure or wording in the cited source?* The answer decides the suffix. A citation being present is not verification — a citation can name a real document and be wrong about what is in it.

**Verified ground truth form** (provenance `read-at-source` — no suffix):

- **GT-1** [fact text] — source: [verification source — data, measurement, published spec, direct observation]; read-at-source: [page, table, section, or quoted passage where the figure was read]
- **GT-2** [fact text] — source: [verification source]; read-at-source: [where read]

**Delegate-reported ground truth form** (provenance `reported-by-delegate` — `?` required):

- **GT-3?** [fact text] — cited to: [source the delegate named]; reported-by-delegate: [which sub-agent, search, or summary supplied it] — cited source not opened by this analysis

**Unverified ground truth form (D-07)** (provenance `unverified` — `?` required):

- **GT-4?** [fact text] — unverified: [specific reason the fact could not be verified in this analysis]

The `?` suffix signals that this ground truth has not been read at its source — whether because it is an untested belief or because a delegate reported it and nobody opened the citation. Any conclusion depending on a `GT-N?` input inherits a confidence caveat in the Derivation Chains section. The analysis may proceed with such inputs — but the uncertainty must be visible.

**The `?` is the default.** Drop it only when the read-at-source location can be named. A delegate report counts as read-at-source only when it quotes the source's own wording and that quote was checked — not when it merely supplies a well-formed citation.

**Provenance summary (required):** enumerate the `?`-marked ground truths **by ID**, and for every unsuffixed ground truth feeding a HIGH-confidence chain, name its read-at-source location. Write the list, not a number:

```text
?-marked: GT-2, GT-5, GT-9, GT-14 (4 of 22)
Read-at-source: GT-3 — 45 CFR 164.514(b)(2)(i), subsections (A)/(B)/(R) quoted verbatim
```

A stated integer does not satisfy this — an integer cannot be checked against the list it summarizes, and an enumeration can. Where a count and its enumeration disagree, **the enumeration governs.** Neither an empty enumeration nor a count of zero satisfies this on its own; the named locations are the auditable part.

IDs are stable once assigned. GT-3 remains GT-3 throughout the document even if GT-3 is later verified or discarded.

---

## 4. Derivation Chains

Show how the ground truths combine into conclusions. Every conclusion offered in this analysis must have exactly one chain here — no more (no redundant restatement), no fewer (no orphaned conclusions).

**Chain numbering convention.** Number each `### Conclusion:` block in this section `C1`,
`C2`, ... in document order (e.g., `### Conclusion C1: [Conclusion text]`). The §6→§4
closure ledger (the agent body — `SKILL.md` on the skill surface, `agents/first-principles.md` on the agent surface — "Before presenting conclusions") cites these IDs when mapping a
Conclusion-section (section 6) claim back to the chain in this section that established it.

**Chain format:**

```text
GT-N + GT-M → [intermediate claim] → [conclusion]
```

The one-line form is the degenerate case, used only when the whole chain fits on one physical line; a chain that does not fit uses the head-plus-arrow-led form, and a hop is split rather than continued on a second line.

Each chain must contain at least one intermediate step. A chain that goes directly from GT-IDs to conclusion is incomplete — the intermediate is where the reasoning happens. The intermediate must be a new claim that could not be stated from either ground truth alone. If no intermediate can be stated, the conclusion is either a restatement of a ground truth (trivial) or a reasoning step is missing.

**No-wrap rule.** A hop occupies exactly one physical line. Every line after the head begins with `→` and carries exactly one complete hop; a hop is never broken across physical lines. The head line carries the GT identifiers and their brief fact labels; a chain needing more hops continues on further arrow-led lines. A hop too long for comfort is SPLIT, not wrapped — the analysis renders as Markdown, so a long hop soft-wraps for the reader without breaking the form.

```text
GT-1 ([brief fact label]) + GT-6 ([brief fact label])
→ [intermediate claim]
→ [further intermediate]
→ [conclusion]
```

**Conforming — head, then one hop per line:**

```text
GT-1 (Lambda $/GB-s, AWS pricing) + GT-6 (Fargate $/vCPU-hr, AWS pricing)
→ Lambda costs 2.10× per unit of actual compute
→ sustained workloads belong on Fargate
```

**Non-conforming — a hop broken across physical lines:**

```text
GT-1 (Lambda $/GB-s, AWS pricing) + GT-6 (Fargate $/vCPU-hr, AWS pricing)
→ Lambda costs 2.10× per unit of actual compute
  once idle-time billing is included
→ sustained workloads belong on Fargate
```

The continuation line does not begin with `→`, so the chain terminates at the head's first hop and what remains reads as an incomplete chain.

**Non-conforming — the same hops rendered as a numbered list:**

```text
1. GT-1 (Lambda $/GB-s, AWS pricing) + GT-6 (Fargate $/vCPU-hr, AWS pricing)
2. Lambda costs 2.10× per unit of actual compute
3. sustained workloads belong on Fargate
```

A numbered list restates each hop as its own GT-headed one-hop chain, which reads as several incomplete chains rather than one complete one — the intermediate steps stop being connected to the conclusion they build toward.

**One-inference rule.** A hop states exactly ONE inference. If a hop joins two claims with "and", or carries a parenthetical that could stand as its own claim, it is two hops — split it.

TELL (not the rule): a hop past ~200 characters is almost always two hops. Measure the hop, then split — do not wrap it, and do not trim words to hit a number.

Inline annotations (`*[Assumes: A14 — …]*`) attach to the end of the hop line they qualify and do not start a new hop.

### Converting structured-technique outputs into chains

Structured-technique outputs (trade-off matrices, second-order effect lists) do not appear in this section as-is — each converts into the chain format above using the rule for its technique below. This subsection is the single source of truth for the conversion; the per-technique Handoff sections point back here rather than restating it, so future structured techniques extend this one place.

**Trade-off matrix → one chain.** A trade-off matrix collapses into ONE chain whose intermediate cites the winning weighted total and whose endpoint names a single recommended option:

```text
GT-refs (criteria's factual basis) → weighted totals (the winning total vs. the runner-up, naming the high-weight criteria that drive it) → recommended option
```

Example: `GT-2 + GT-5 (criteria facts) → weighted totals: B=82 > A=64, driven by reliability×warranty → recommend B`. The full matrix stays in the technique's own output — this subsection carries only the single collapsed chain, never the matrix re-expressed row-by-row (that would violate the one-chain-per-conclusion rule above). An exact tie between weighted totals still resolves to a single named recommended option; a tie must not produce a multi-option chain endpoint. **Exact-tie tiebreak (deterministic):** on an exact tie, prefer the option with fewer `GT-N?` (unverified) inputs among its winning criteria; if still tied, name both totals in the chain intermediate but select the first-listed option as the chain endpoint, and flag the tie explicitly in the Conclusion section's confidence line.

**Second-order effect list → order-marked extension.** A second-order effect list extends the parent chain IN PLACE as additional order-marked steps, each carrying the same evidentiary discipline as the first-order steps that produced the conclusion:

```text
GT-N → first-order conclusion →[2nd] [2nd-order effect] →[3rd] [3rd-order effect] (contradicts GT-M → back to Phase 2)
```

Example: `GT-1 → first-order conclusion →[2nd] flag-config surface grows →[3rd] flag debt accumulates (contradicts GT-4 → back to P2)`. The order marks (`[2nd]`, `[3rd]`) make the extension's sequence legible. A contradicting effect routes the conclusion back to Phase 2 — never directly to Phase 3 or past Phase 2. A pass that surfaces no non-contradicting downstream effect leaves the parent chain unextended — a clean no-op, not an error.

### Conclusion C1: [Conclusion text]

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

**Citation form.** Every Conclusion-section claim either names the chain that established it inline — `(chain C1)` — or is discharged by a §6→§4 closure ledger row that quotes the claim and names its chain. A claim doing neither is cut, not softened.

**Conforming — inline chain citation:**

```text
**Recommended approach:** Move sustained workloads to Fargate (chain C1).
```

**Conforming — closure-ledger row:**

```text
- "Move sustained workloads to Fargate" → chain C1 ✓
```

**Non-conforming — a claim naming no chain and quoted by no ledger row:**

```text
**Recommended approach:** Move sustained workloads to Fargate.
```

Both forms are accepted because both discharge the same obligation: the ledger is process output emitted before the analysis (see the agent body — `SKILL.md` on the skill surface, `agents/first-principles.md` on the agent surface — "Before presenting conclusions"), not a seventh output section, and the chain IDs cited are the `C1`/`C2` IDs assigned by §4's chain-numbering convention.
