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

**Nothing about the environment enters the document.** The six sections above are the whole deliverable, and none of them has a slot for the state of the session that produced it. Tooling, connector, authorisation, permission, quota, configuration, model, harness and transcript state are all environment state, and none of it belongs in the analysis — not in a section, not appended after §6, not as a footnote. The class is *any* fact about the machinery rather than about the problem; it is not a list of forbidden words, and a new kind of environment fact is covered by this rule on the day it first exists. A prefix such as "Unrelated to this analysis", "Separately" or "Note:" does not make such a paragraph admissible — it marks the writer as already knowing the paragraph does not belong, which is the point at which it is dropped rather than labelled. Where environment state genuinely blocked the analysis, it is already disclosed in its proper place: a failed reference read under the template's own disclosure rule, and an unmet evidence need as a `?`-marked input carried into the Assumptions Table and named on the affected `**Confidence:**` line. Environment state that blocked nothing is reported to the user outside the deliverable, after the document ends, or not at all.

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

**These five columns are the whole table — no ID column.** Assumptions are referred to by the
`[Assumes: A-N]` marks the chains carry and by the `A-N` labels used in the Assumption Audit
scan; adding a sixth ID column to this table duplicates that identity in a second place, and two
places that name the same thing drift. A run that adds one is deviating from this template even
though nothing rejects it today.

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
token leads so it stays matchable, and the em-dash prose carries the reasoning. **The separator
is an em-dash, never a colon.** `Accept: the figure is audited` puts the token and the reasoning
on one side of a punctuation mark that appears throughout ordinary prose, so the cell stops being
matchable — which is the whole property the token-first form exists to provide. Measured: a single
run using the colon form scored ten non-conforming verdict cells at once. The em-dash is not a
stylistic preference here; it is the delimiter:

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

Each chain must contain at least one intermediate step. A chain that goes directly from its head inputs to conclusion is incomplete — the intermediate is where the reasoning happens. The intermediate must be a new claim that could not be stated from any single head input alone. If no intermediate can be stated, the conclusion is either a restatement of a head input (trivial) or a reasoning step is missing.

**No-wrap rule.** A hop occupies exactly one physical line. Every line after the head begins with `→` and carries exactly one complete hop; a hop is never broken across physical lines. A chain needing more hops continues on further arrow-led lines. A hop too long for comfort is SPLIT, not wrapped — the analysis renders as Markdown, so a long hop soft-wraps for the reader without breaking the form.

```text
GT-1 ([brief fact label]) + GT-6 ([brief fact label])
→ [intermediate claim]
→ [further intermediate]
→ [conclusion]
```

**Head-input rule.** The head line lists the inputs the chain consumes: each is a `GT-N` identifier (`GT-N?` when the ground truth is unverified) or a `Cn` identifier, optionally followed by a parenthesized gloss, joined to the next by `+`. The first `→` closes the head. An input carrying unparenthesized prose — `C2's threshold` — is not an identifier and does not parse; write `C2 (threshold)` in every position. The mechanical form check detects that violation only when the prose input is the last one before the first `→`; in an earlier position the check matches the well-formed remainder and scores the head conforming, so the rule binds in positions the check does not reach.

```text
GT-1? ([brief fact label]) + C2 ([brief fact label])
→ [intermediate claim]
→ [conclusion]
```

The head grammar governs the head line only. A hop is prose: `C2's saving` is fine after the first `→`, and is not an input reference. One exception: a hop must not begin with a `GT-N` identifier, which the form check reads as the head of a new chain and which therefore ends this one — write `→ the duty cycle stated in GT-4 is the binding term`, not `→ GT-4's stated duty cycle is the binding term`. The form check detects that violation only while fewer than two hops precede it; in a later position the check matches the preceding hops and scores the chain conforming, so the rule binds in positions the check does not reach.

The mechanical form check additionally rejects a chain whose head or first hop closes its own sentence before the next `→`: it reads the following arrow-led line as a new statement and ends the chain there, so a chain satisfying every rule above is scored malformed for that reason alone. The check reaches only that position — a hop that closes its own sentence from the second hop onward does not change the verdict — which is why intermediate hops carry no terminal punctuation in this project's worked examples.

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

**Non-conforming — an input carrying unparenthesized prose:**

```text
GT-13? (bill composition unknown) + GT-12? (duty cycle unknown) + C2's threshold
→ target quantity: fraction of total AWS bill removed by the migration
→ the bracket straddles zero, so its two ends recommend opposite actions
```

`C2's threshold` is not an identifier — it is a possessive prose phrase — so the head does not parse; the third input must be written `C2 (threshold)`.

**Conforming — the same head with the upstream chain as an input:**

```text
GT-13? (bill composition unknown) + GT-12? (duty cycle unknown) + C2 (threshold)
→ target quantity: fraction of total AWS bill removed by the migration
→ the bracket straddles zero, so its two ends recommend opposite actions
```

Exactly one token differs from the block above: a `Cn` identifier with a parenthesized gloss is an admissible head input, on equal footing with a `GT-N` identifier.

**Conforming — a chain consuming only upstream conclusions:**

```text
C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold) + C4 (unconditional, zero code change) + C5 (~73% ceiling, no execution-model change)
→ C4 and C5 deliver verified savings that do not depend on any property of your workload
→ C2's saving depends entirely on a duty-cycle figure nobody has measured
```

A head may consist entirely of `Cn` inputs with no `GT-N` term. The second hop's `C2's saving` is prose, not a head input — the head-only scope note is what permits it here.

**Non-conforming, and undetected by the form check — the same prose input in a non-final position:**

```text
GT-13? (bill composition unknown) + C2's threshold + GT-12? (duty cycle unknown)
→ target quantity: fraction of total AWS bill removed by the migration
→ the bracket straddles zero, so its two ends recommend opposite actions
```

This head breaks the same rule as the non-conforming block above and is equally non-conforming, but the mechanical form check scores it conforming — with a well-formed input still to its right the check matches from `GT-12?` onward and never reaches `C2's threshold`. Write `C2 (threshold)` wherever the input sits; the rule is the contract, and the check is a partial instrument for it.

**Non-conforming — a hop beginning with a GT-N identifier:**

```text
C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)
→ GT-4's stated duty cycle is the binding term in both estimates
→ the bracket straddles zero, so its two ends recommend opposite actions
```

The second line reads as the head of a new chain because it begins with a `GT-N` identifier, so this chain ends after its head and what remains is an incomplete chain — the possessive is not the problem, the leading identifier is.

**Conforming — the same hop with the identifier moved off the front:**

```text
C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)
→ the duty cycle stated in GT-4 is the binding term in both estimates
→ the bracket straddles zero, so its two ends recommend opposite actions
```

Exactly one clause is reordered and the chain is whole again; naming a ground truth inside a hop is fine, leading with its identifier is not.

**Non-conforming, and undetected by the form check — the GT-led hop in a later position:**

```text
C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)
→ the bracket straddles zero, so its two ends recommend opposite actions
→ the second reading is the binding one
→ GT-4's stated duty cycle is the binding term in both estimates
```

This hop breaks the same rule as the non-conforming block above and is equally non-conforming, but the mechanical form check scores it conforming — the check has already satisfied its two-arrow requirement on the hops that precede it, so the leading identifier ends the chain there without changing the verdict. Write `→ the duty cycle stated in GT-4 is the binding term in both estimates` wherever the hop sits; the rule is the contract, and the check is a partial instrument for it.

**Non-conforming — the first hop closing its own sentence:**

```text
C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)
→ C1's saving is unconditional and does not depend on workload shape.
→ C2's saving is real only above the duty-cycle threshold this estimate assumes
```

This chain violates none of R1-R9 — every input parses, every hop states one inference, no hop leads with a `GT-N` identifier — and is scored malformed anyway, because the mechanical form check ends the chain the moment the first hop closes its own sentence, before its two-arrow requirement is satisfied, and never reaches the well-formed hop that follows.

**Conforming — the same chain with the first hop's terminal period removed:**

```text
C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)
→ C1's saving is unconditional and does not depend on workload shape
→ C2's saving is real only above the duty-cycle threshold this estimate assumes
```

Exactly one character differs from the block above: the terminal period. Removing it, and nothing else, restores the two-arrow match the check requires.

**Non-conforming, and undetected by the form check — the same period moved to a later hop:**

```text
C1 (2.20× at full duty) + C2 (conditional on an unmeasured threshold)
→ C1's saving is unconditional and does not depend on workload shape
→ the migration case does not rest on C1 alone
→ C2's saving is real only above the duty-cycle threshold this estimate assumes.
```

This block breaks the identical rule one hop later and is equally non-conforming, but the mechanical form check scores it conforming — with two hops already matched before the closing sentence is reached, the check has satisfied its two-arrow requirement and the sentence-closing period on the third hop has no following line left to block. Write the closing hop with no terminal punctuation wherever it sits; the rule is the contract, and the check is a partial instrument for it.

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

### Confidence levels, defined

`HIGH`, `MEDIUM` and `LOW` name how much of a chain is **outstanding** — not how strongly the analysis believes its conclusion. Three axes decide the band, each answerable by inspecting what the chain already carries on the page:

- **Inputs** — the provenance of every identifier on the head line: an unsuffixed `GT-N` with a named read-at-source location, a `?`-marked ground truth, or a `Cn` carrying its own band.
- **Inference** — whether each hop the chain's endpoint depends on follows from the line above it, or needs a premise supplied by an `[Assumes: A-N]` annotation.
- **Rivals** — whether a competing conclusion from the same ground truths survives, and what rules it out. Section 5 is where the ruling-out is written down, so a chain answers this axis by pointing at its own Abandoned Reasoning entry as readily as by carrying the rival on its confidence line.

**The band is the lowest the three axes license.** A chain is not HIGH because two of them are clean.

**HIGH — nothing on this chain is outstanding.** Every identifier on the head line is an unsuffixed `GT-N` whose read-at-source location is named, or a `Cn` itself rated HIGH; every hop the endpoint depends on follows from the line above it by deduction, by arithmetic that recomputes when redone independently of the chain text, or by a regularity cited to an unsuffixed ground truth; and the strongest rival conclusion the analysis considered is named — on this confidence line or in a section 5 entry this chain points to — together with the ground truth or chain that rules it out, that ruling-out input itself unsuffixed. A chain whose endpoint a live alternative still contests is unexamined, not certain: it is MEDIUM at best.

An `[Assumes: A-N]` annotation on a hop shorts the Inference axis **unless** the confidence line says what becomes of the endpoint when that assumption fails and the endpoint still stands — *"A2 is that the CDN'd assets are versioned; if they were not, the CDN result would be weaker evidence still, so the conclusion is unaffected"*. An annotation on a hop that only qualifies a second-order extension, and not the endpoint, is outside this axis and the chain says which case it is. Stating the sensitivity is the work; an unexamined assumption is not the same thing as one whose falsity has been priced.

The Rivals axis is answered when a section 5 entry names a competing conclusion to this chain's endpoint and the chain or ground truth that ruled it out, or when the endpoint is itself a ruling-out — a chain establishing that some option does not work has already done the rival's work and does not need a rival of its own. It is short when a competing conclusion has been raised anywhere in the analysis and nothing settles it, and when the analysis reaches a positive recommendation with no section 5 content bearing on it at all.

**MEDIUM — exactly one axis is short, and the shortfall is named and bounded.** One of: an identifier on the head line is `?`-marked or is a `Cn` rated MEDIUM; or at most one hop the endpoint depends on rests on a stated `[Assumes: A-N]` premise whose failure the chain has not priced; or a rival to the endpoint is live and nothing in the analysis settles it. The confidence line names which axis is short, names the specific input, hop or rival, and states what would close it — the verification that would remove an input as a cause of the downgrade, the evidence that would establish an assumed premise, or the observation that would settle between this conclusion and its rival. A MEDIUM chain is one whose weakness a reader can point at.

**LOW — the shortfall is unbounded, or more than one axis is short.** Two or more axes short at once; or an input is `?` with no verification path available; or a hop's missing premise cannot be stated as an assumption at all, so the analysis cannot say what would make the step valid; or a rival survives that no available observation would settle. A LOW chain is reportable, and a conclusion resting on it alone is not actionable.

**Calibration rule.** Each rating is the highest its inputs, hops and rivals license, **and no higher**. Rating above what the axes license over-claims. Rating below it is a defect of the same kind: a chain meeting HIGH on all three axes and written MEDIUM misreports the analysis's own strength, and a document whose every chain carries the same defensive band tells a reader nothing about which parts to trust. Criterion 5 scores calibration, not altitude — an analysis whose every band is the one its axes license is Rigorous whether its conclusion is HIGH, MEDIUM or LOW.

**The caps are consequences, not extra rules.** The unverified-input rule (D-07) below and the ceiling at the lowest-rated chain a head cites are what the Inputs axis says, restated for the two cases that occur most often; they are the fast check, and these definitions are what they check for. A cap never licenses a band on its own — it bounds from above, and the band is still the lowest any of the three axes licenses.

**Confidence pre-check (Inputs axis).** Directly above every `**Confidence:**` line — each §4 chain's and the §6 Conclusion's — write one `**Pre-check:**` line, with nothing between it and the `**Confidence:**` line it checks:

```text
**Pre-check:** head GT-1, GT-3?, C2 (MEDIUM) · ?-marked: GT-3? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-3? is unverified; …
```

Four fields, separated by ` · `: `head` lists every identifier on the chain's head line (the part before the first `→`), in order, comma-separated, a `?` suffix kept (`GT-3?`), each `Cn` followed by its own stated band in parentheses (`C2 (MEDIUM)`) — for the §6 roll-up, `head` is every chain the Conclusion rests on, each with its band, plus any `GT-N?` the Conclusion rests on directly. `?-marked` lists the `?`-suffixed identifiers from `head`, comma-separated, or the token `none`. `lowest cited` is the lowest band among the `Cn` in `head`, or `none` when `head` cites no chain. `Inputs ceiling` is the Inputs axis's bound: `LOW` if `lowest cited` is LOW; otherwise `MEDIUM` if `?-marked` is not `none` or `lowest cited` is MEDIUM; otherwise `HIGH`.

This is the Inputs axis of "Confidence levels, defined" made procedural — Inference and Rivals are not scored on this line, and can only lower the band further. The ceiling bounds from above, as the caps-are-consequences paragraph above states; the `**Confidence:**` label may equal it or sit below it, and never above it — a below-ceiling label is explained by the Confidence line itself, not by the pre-check. In §6, the pre-check line is itself a Conclusion-section claim under the Claim inventory rule below, and it is cited by the chains its own `head` names.

### Conclusion C1: [Conclusion text]

GT-N ([brief fact label, source]) + GT-M ([brief fact label, source])
→ [intermediate claim — a new inference statable from combining GT-N and GT-M but from neither alone]
→ [conclusion — the claim this chain establishes]

**Pre-check:** head [every head identifier; each Cn with its band, e.g. C2 (MEDIUM)] · ?-marked: [the GT-N? identifiers, or none] · lowest cited: [lowest Cn band, or none] · Inputs ceiling: [HIGH / MEDIUM / LOW]
**Confidence:** [HIGH / MEDIUM / LOW]
[If MEDIUM or LOW: name each GT-N? input with the verification that would remove it as a cause of the downgrade; name each Cn on this chain's head rated below HIGH, which need not be re-explained here; and give each downgrade cause belonging to this chain itself — for example a weak inference step or an absent-fails derivation — with what would remove it as a cause of the downgrade or a stated reason no verification path exists (the validation-rubric absent-fails EXCEPT clause, for an absent-fails derivation, or an explicit account of why no available evidence settles that cause).]

**Unverified input rule (D-07):** A chain that includes any `GT-N?` input must end with a MEDIUM or LOW confidence line. The line must name the unverified input and state the verification that would remove it as a cause of the downgrade. A HIGH confidence claim cannot rest on an unverified ground truth. A chain is also rated no higher than the lowest-rated chain its head cites — the stated confidence label of each `Cn` on its head line, the part before the first `→`. This is a ceiling: it bounds the rating from above and is never a reason to rate a chain HIGH, and a cited chain rated MEDIUM under a validation-rubric EXCEPT clause still caps every chain that cites it. Every MEDIUM or LOW confidence line explains only its own chain's rating, so its validity never depends on how far away a cap originates. The line names each `GT-N?` input with the verification that would remove it as a cause of the downgrade. It names each `Cn` on the chain's head rated below HIGH and need not re-explain that `Cn`, whose own confidence line carries the explanation, so no line has to trace a cited chain's lineage. For each downgrade cause belonging to the chain itself — for example a weak inference step or an absent-fails derivation — the line states what would remove it as a cause of the downgrade or a stated reason no verification path exists. A stated reason is the validation-rubric absent-fails EXCEPT clause, for an absent-fails derivation, or an explicit account of why no available evidence settles that cause; "speculative" is never such a reason. The validation-rubric absent-fails EXCEPT clause is the only clause that can stand in for a verification path, and naming any other clause, including the speculative EXCEPT clause, stands in for nothing. A chain cited on another chain's head is load-bearing, so the rubric's speculative EXCEPT clause no longer covers it, and the cited chain's own confidence line states its verification path; a speculative chain with no verification path is not cited on another chain's head, and stays speculative or moves to Abandoned Reasoning (§5).

---

## 5. Abandoned Reasoning

Record every reasoning path that was explored and discarded. This section is required in every analysis. Dead ends are not failures — they are part of the reasoning record and save future analysts from re-exploring paths that have already been ruled out.

### Dead End: [Name of discarded path]

**What was tried:** [Brief description of the reasoning path that was pursued.]

**Why abandoned:** [The specific failure — assumption false, contradicts a ground truth, assumption classification too weak to anchor the chain, conclusion circular, intermediate could not be established, speculative with no verification path (so not cited on another chain's head), etc. Be precise: "we ran out of time" is not a valid abandonment reason.]

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

**Pre-check:** head [each chain the Conclusion rests on with its band, e.g. C1 (MEDIUM), C3 (HIGH); plus any GT-N? it rests on directly] · ?-marked: [ids, or none] · lowest cited: [lowest band, or none] · Inputs ceiling: [HIGH / MEDIUM / LOW]
**Confidence:** [HIGH / MEDIUM / LOW]

If Confidence is MEDIUM or LOW: name each chain contributing to the Conclusion that is rated below HIGH, and each `GT-N?` input the Conclusion rests on directly with the verification that would remove it as a cause of the downgrade. The line need not restate a named chain's verification path or no-path reason; the named chain's own §4 confidence line carries it. Give any downgrade cause belonging to the Conclusion itself with what would remove it as a cause of the downgrade or a stated reason no verification path exists, as §4 defines. A MEDIUM or LOW conclusion without this explanation does not satisfy D-07.

**Claim inventory.** A Conclusion-section claim is a bold lead-in whose colon closes the bold span, or a numbered or bulleted list item, and the three lead-ins this template prescribes — `**Recommended approach:**`, `**Key insight:**`, `**Trade-offs acknowledged:**` — are always claims and each must cite a chain; nothing inside a fenced block is ever a claim whatever its shape, a near-paraphrase restatement or direct entailment of an already-cited claim earlier in the same section is not a second claim, and prose carrying neither a bold colon lead-in nor a list marker is not a claim at all. Three bounds are measured, not assumed: a bold lead-in whose colon-terminated span is the entire physical line and carries no citation of its own is a section-intro label, and the citation obligation then falls to the list items beneath it; a bold span whose closing `**` is not immediately preceded by the colon is not matched at all — write `**Label:** text` to match, not `**Label: text**`; and a list item counts only when it closes its own sentence or runs past forty characters. Enumerate by this rule, not by recollection — the rule is the contract and the extractor is a partial instrument for it.

**Citation form.** Every Conclusion-section claim either names the chain that established it inline — `(chain C1)` — or is discharged by a §6→§4 closure ledger row that quotes the claim and names its chain. A claim doing neither is cut, not softened. Ledger discharge requires the structural row form the closure-ledger example below shows — a list marker, then the quoted claim, then an arrow, then the chain id — and a prose sentence that merely quotes something and names a chain is not a ledger row. This is detected only when the row sits inside section 6: the ledger emitted as process output before the analysis is not visible to the check, and inline citation is therefore the mechanically checkable form.

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

**Caveats.** A caveat qualifying an existing Conclusion-section claim either names the chain it qualifies inline or carries the marker `no chain — flagged assumption only` (em dash, lower case, no trailing punctuation inside the marker), and a marked caveat still scores untraced: the marker discloses the gap, it does not discharge the claim, because it is honest labelling rather than a citation and the extractor is deliberately not taught to recognise it. A caveat doing neither is cut, not softened.

**Not a claim — a bold lead-in alone on its line, carrying no citation:**

```text
**Recommended approach — three steps, in this order:**
```

This is the hinge of "detectable from the emission alone" — an author can dodge extraction by putting the lead-in on its own line, and the claim obligation then falls to the numbered items beneath it.

**A claim — the same lead-in carrying its assertion on the same line:**

```text
**Recommended approach:** Move sustained workloads to Fargate before evaluating Lambda (chain C1).
```

Nothing follows the closing `**` in the block above and something does here, which is the whole difference.

**A claim — the lead-in alone on its line, but carrying its own citation:**

```text
**Recommended approach, established in chain C1:**
```

The section-intro-label exclusion is conditional on carrying no citation; naming the chain inside the label keeps it a claim.

**Not matched at all — a bold span whose colon sits inside it:**

```text
**Overall confidence: HIGH.**
```

The extractor requires the colon to close the bold span, so this line is not a claim and not a non-claim — it is never looked at.

**A claim — the same statement with the colon closing the bold span:**

```text
**Overall confidence:** HIGH — seven of eight chains rest on figures read at source (chain C1).
```

One character moved, and the statement enters the inventory.

**Not a claim — a short list item with no sentence-ending punctuation:**

```text
- Measure duty cycle first
```

Twenty-four characters and no terminal punctuation, so it falls under the assertiveness floor.

**A claim — a short list item closing its own sentence:**

```text
- Size the Savings Plan after cleanup.
```

Also under forty characters, so the terminal punctuation is the only thing carrying it over the floor. The two items above are worded differently only so each block is uniquely locatable by the fixture-extraction guard — a true one-character minimal pair would make one block's text a literal prefix of the other's, which no substring needle can discriminate (the `R-HEAD-PERIOD-*` lesson) — and a later control proves the axis is punctuation by re-scoring each block with its punctuation toggled.

**Conformant but still untraced — a caveat carrying the flagged-assumption marker:**

```text
**Trade-offs acknowledged:** the ~73% figure is a ceiling requiring an all-upfront commitment; the realized figure on a no-upfront plan is materially lower — no chain — flagged assumption only.
```

The marker satisfies the Caveats rule above and the claim still scores untraced; that is honesty-not-score, not a defect, and it is why the extractor is not taught to recognise the marker.

**Conformant and traced — the same caveat citing the chain it qualifies:**

```text
**Trade-offs acknowledged:** the ~73% figure is a ceiling requiring an all-upfront commitment; the realized figure on a no-upfront plan is materially lower (chain C5).
```

Naming C5 discharges the claim; the marker discloses it. The two rewrites land on different Criterion 6 bands, and that band is assigned by a model — no gate in this tree checks it.
