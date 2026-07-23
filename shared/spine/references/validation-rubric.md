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

**Assumption Audit (verify before scoring)**

The scan itself is not performed here — the agent already performed it at the end of Phase 4
(`SKILL.md`, "End-of-phase Assumption Audit") before this rubric is ever applied. This
rubric's job is narrower: verify the audit ran and its table is exhaustive, not repeat the
scan.

Before scoring any criterion, confirm the audit table below is present in the analysis and
covers every named derivation chain step from section 4 — one row per chain per step, in
order, with no step skipped. Do not proceed to verdict blocks until this is confirmed.

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| [chain producing conclusion X] | 1 | [step text] | [assumption or "none"] | [yes / n/a] |
| [chain producing conclusion X] | 2 | [step text] | [assumption or "none"] | [yes / n/a] |
| [chain producing conclusion Y] | 1 | [step text] | [assumption or "none"] | [yes / n/a] |

If the table is missing, or any named derivation chain step in section 4 has no corresponding
row, the audit did not run exhaustively — this is a Criterion 2 defect (see Criterion 2's
descriptors below), not a separate gate. Do not re-perform the scan to fill a missing table;
a missing or incomplete table is itself the evidence to score against.

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
  non-generic content, all required relationships are explicit,
  and every observable structural test in this criterion's Rigorous descriptor returns pass.

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
  each success criterion contains a pass/fail structural test — a verb + subject + outcome
  triplet where the outcome is a property of the Conclusion section — so that a reviewer
  applies each criterion by scanning the Conclusion section without analyst interpretation;
  the statement is specific enough that it appears nowhere in an analysis of a different but
  related problem without modification (it names a property unique to this problem, not a
  generic template phrase).
  If this section uses the honest-depth escape valve (`Nothing material here — [reason]`), the
  stated reason is specific to this analysis's problem — it names a property of the problem
  that makes an Essence Statement unnecessary or redundant, and that reason appears in no
  other analysis without alteration.

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
  or names what verification confirms the assumption — not "unclear" or "possibly true";
  at least one assumption has been challenged (not merely labelled Accept); if any assumption
  is used in a derivation chain despite being unverified, the Verification cell reads
  "unverified — flagged"; the agent has visited every named derivation chain step in section 4
  and surfaced any assumption that step requires to hold — not already in the Assumptions Table
  — adding it to the table before scoring; the Assumption Audit artifact produced before
  scoring (per "How to Apply This Rubric") records this scan and confirms it was exhaustive
  over named derivation chain steps, not an open-ended survey of the universe of conceivable
  assumptions.

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
  contains at least one intermediate claim (a claim that cannot be stated from either
  named GT alone), and reaches a conclusion; the Abandoned Reasoning section either documents
  at least one dead end using the What-was-tried / Why-abandoned / What-it-ruled-out structure,
  OR uses the honest-depth escape valve with a reason that is specific to this analysis's
  problem and appears in no other analysis without alteration; no analogy
  is used as direct evidence (any reference to how others solved a similar problem is grounded
  in a named GT about their situation, not offered as standalone justification);
  each chain step that introduces an assumption not already in the Assumptions Table
  declares that assumption inline using `[Assumes: X]` appended to the step text —
  a reviewer applies this check by scanning each chain step for the `[Assumes:` token.

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
  caused the downgrade and what specific verification raises confidence to HIGH; the
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
  does not reach — rather than restating the recommended approach.

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
