<!-- GENERATED — DO NOT EDIT. Source: shared/spine/references/validation-rubric.md. Regenerate via: scripts/sync-content.py --write. -->

# Self-Audit Gate

> **Scope:** This is the Layer-3 scoring instrument read on demand by the validator-fix-repeat loop
> already resident in `SKILL.md`. It scores a completed first-principles analysis against the
> six-section output format defined in `references/output-template.md`. The loop instruction
> itself — when to apply, what to fix, when to stop — lives in `SKILL.md` under
> "Before presenting conclusions" and is **not** repeated here. Come here only to score
> an analysis in progress; use `SKILL.md` for the loop procedure and `output-template.md`
> for authoring guidance.
>
> **What this instrument scores:** the structure of *this analysis*. It is not a rubric for the
> subject matter. When a request asks for a rubric, scorecard, or grading scheme applied to the
> thing being analyzed — an article's argument, a proposal, a design — that is a **separate
> deliverable** that belongs in the analysis body. Producing it does not satisfy this gate, and
> this gate does not substitute for it. Both must appear. (Historically named the "Validation
> Rubric"; renamed because that name collided with subject-matter rubrics and the collision was
> observed to cause this gate to be skipped.)

## How to Apply This Gate

Score the completed analysis against all 6 criteria below. For each criterion, produce exactly
one verdict block in the format prescribed in the Verdict Block Format section. An analysis
clears this gate only when it satisfies **both** of the following conditions — clearing
one condition alone does not constitute a pass:

1. **Gate cleared** — no criterion scores Absent.
2. **Hand-wavy cap cleared** — at most one criterion scores Hand-wavy.

If either condition is not met, revise the analysis and re-score — bounded to **at most one re-perception pass** per analysis, per the rule stated in full under `SKILL.md`'s Turn discipline section. After that single pass, any criterion still failing — or newly failing as a result of the revision — is presented as an unresolved gap with a stated confidence caveat instead of being re-scored again.

**Assumption Audit (verify before scoring)**

The scan itself is not performed here — the agent already performed it at the end of Phase 4
(`SKILL.md`, "End-of-phase Assumption Audit") before this gate is ever applied. This
gate's job is narrower: verify the audit ran and its table is exhaustive, not repeat the
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

## Exceptions Summary

Three conditions relax the HIGH-confidence requirements introduced into Criteria 3 and 5.
This section is a navigation aid, listing them together for quick reference; where its
wording differs from the per-criterion clause, the per-criterion clause governs.

**(a) Unreachable source** — Criterion 3. A ground truth cites a source the Phase 3
verification step could not open; the Phase 3 failure record naming which source and why
unreachable is the satisfying evidence; the ground truth may feed only MEDIUM or LOW chains.

**(b) Speculative chain** — Criterion 5. A chain is explicitly marked speculative and the
analysis states the claim it supports is not load-bearing; the mark plus that statement is
the satisfying evidence; the chain may remain MEDIUM.

**(c) Absent-fails derivation** — Criterion 5. A chain establishes that a conclusion does not
follow from an assumption shown to be false; the named false assumption is the satisfying
evidence; the chain may remain MEDIUM.

An exception is claimed, not assumed: an analysis relying on one names it in the relevant
verdict block and cites the required evidence; an unclaimed exception is not applied on the
analysis's behalf.

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
  This verdict routes back to Phase 1 to re-frame the Essence Statement — or, when the cause is an input that was never supplied, to re-opening input under the Input Contract — rather than an in-place rewrite of output section 1; the route is bounded by the same rule described under `SKILL.md`'s "Before presenting conclusions" section.

### Criterion 2: Challenge Assumptions

Scores the **Classified Assumptions Table** — a table with columns Assumption, Type, Treatment,
Verdict, Verification — in the Assumptions Table section (output section 2). Folds in:
four-type classification quality and unverified-flag discipline (D-07).

- **Rigorous** — every row in the Assumptions Table has a Type value drawn from exactly the
  four-type scheme (physical law / current constraint / convention / untested belief); the
  Treatment cell uses the vocabulary of the prescribed treatment for that type; the Verdict
  cell records Accept, Challenge, or Discard as a leading token followed by an em-dash and a
  specific justification — not the bare token alone; the Verification cell cites a specific
  source or names what verification confirms the assumption — not "unclear" or "possibly true";
  at least one assumption has been challenged (not merely labelled Accept); if any assumption
  is used in a derivation chain despite being unverified, the Verification cell reads
  "unverified — flagged"; the Assumption Audit performed at the end of Phase 4 (`SKILL.md`,
  "End-of-phase Assumption Audit") visited every named derivation chain step in section 4 and
  surfaced any assumption not already in the Assumptions Table, recording it there; the
  Assumption Audit artifact produced before scoring (per "How to Apply This Rubric") confirms
  this scan was exhaustive over named derivation chain steps, not an open-ended survey of the
  universe of conceivable assumptions.

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

Scores the **Ground Truths list** — a numbered list of verified facts with stable GT-IDs,
source citations, and a provenance label, with unverified and delegate-reported entries marked
with the `GT-N?` suffix — in the Ground Truths section (output section 3).

**Provenance check (apply before banding).** A citation being present is not verification. For
each unsuffixed ground truth, ask whether the analysis read the asserted figure in the cited
source — `read-at-source` — or merely received it from a sub-agent, search result, or summary
without opening the citation (`reported-by-delegate`, which requires the `?`). Score against
what the analysis did, not against how well-formed the citation looks.

- **Rigorous** — every GT-item carries a stable identifier (GT-1, GT-2, etc.) that matches
  the identifiers referenced in the Derivation Chains section; every verified GT has a source
  citation that is more specific than "common knowledge" or "known fact"; every GT carries a
  provenance label; every unverified or delegate-reported GT is marked with the `?` suffix;
  the `?`-marked GTs are **enumerated by ID** and that enumeration matches the suffixed entries
  in the Ground Truths list when checked against it; every unsuffixed GT feeding a
  HIGH-confidence chain names its read-at-source location; no assumption that was discarded in
  Phase 2 (Verdict: Discard) appears in this list. Every unsuffixed GT whose cited source is
  reachable feeds at least one HIGH-confidence chain EXCEPT: the Phase 3 failure record names
  the source as unreachable, in which case the GT may feed only MEDIUM or LOW chains, evidenced
  by that record naming which source and why unreachable.

  **Check the enumeration, do not quote it.** Quoting the analysis's own provenance summary as
  the satisfying span does not discharge this criterion — that verifies a summary was written,
  not that it is correct. Read the Ground Truths list, collect the IDs actually carrying `?`,
  and compare against the enumeration. Cite the comparison as the satisfying span (*"enumerated
  GT-2, GT-5, GT-9, GT-14; list carries `?` on exactly those four"*). Where a stated count and
  its enumeration disagree, the enumeration governs and the mismatched count is itself a defect.

  **Reachability is decided by the Phase 3 record, not re-decided here.** A source is reachable
  when the Phase 3 verification step opened it, and unreachable when the Phase 3 failure record
  names it with a specific reason; the analyst reads the record and does not re-argue
  reachability per ground truth. This requirement is not satisfied by a ground truth that feeds
  no chain at all — a GT no derivation chain consumes is already a Criterion 4 defect, and the
  requirement presupposes at least one load-bearing chain consumes the GT. A single unsuffixed
  GT whose reachable source feeds only MEDIUM or LOW chains bands this criterion Sound; the same
  shortfall across multiple GTs bands it Hand-wavy.

- **Sound** — GT-IDs are present and stable, but one or more verified GTs cite "common
  knowledge," "known fact," or no source at all; OR provenance labels are missing though the
  `?` suffixes themselves are correctly applied; OR one unread GT (unverified or
  delegate-reported) is used without the `?` suffix **and it feeds only MEDIUM or LOW
  confidence chains**; OR the `?`-marked GTs are summarized by a bare count rather than
  enumerated, though the suffixes in the list are themselves correct.

  An enumeration that **disagrees with the list** does not band here — it bands **Hand-wavy**.
  A count that merely accompanies a correct enumeration and disagrees with it is a defect but
  bands Sound, since the enumeration governs and remains checkable.

- **Hand-wavy** — GT-IDs are present but they are not stable (the same ID is used for
  different facts at different points in the document, or IDs are renumbered between sections);
  OR the list includes an assumption that was assigned a Discard verdict in Phase 2; OR
  multiple unread GTs are used in chains without the `?` suffix; OR **the `?` enumeration
  disagrees with the Ground Truths list** — an enumeration that omits a suffixed GT understates
  the analysis's unverified inputs in the direction that flatters it, and unlike a bare count it
  was checkable, so a mismatch is a stronger failure than never enumerating at all; OR **any
  unsuffixed GT feeds a HIGH-confidence chain without naming a read-at-source location** — a
  HIGH-confidence conclusion resting on a figure nobody read is the failure this criterion
  exists to catch, and a single instance is enough to land here.

  **Fix — acquire before you downgrade.** Branch one, preferred: acquire the evidence — open
  the cited source, per the Phase 3 verification step, and let the read move the provenance
  label. Branch two: downgrade the confidence — carry the `?` and drop the chain from HIGH,
  taken only when the source cannot be opened or opens without containing the asserted figure or wording. The preference, explicitly: acquisition is preferred when the source is reachable, because a gate whose only available Fix weakens the output resolves every failure toward less claim rather than more evidence. The unreachable case is not a free pass — the downgrade branch still requires the Phase 3 failure record, which source and why unreachable, or `citation does not support the claim`, so a reader can tell a downgrade from a skipped attempt.

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
Reasoning (D-03). The one-line form is the degenerate case, used only when the whole chain fits on one physical line; a chain that does not fit uses the head-plus-arrow-led form, and a hop is split rather than continued on a second line.

- **Rigorous** — every conclusion stated anywhere in the document (in section 4 or section 6)
  has exactly one derivation chain in section 4; each chain names the GT-IDs it consumes,
  contains at least one intermediate claim (a claim that cannot be stated from either
  named GT alone), and reaches a conclusion; each chain is rendered in the prescribed
  arrow-led form. A hop occupies exactly one physical line. Every line after the head begins with `→` and carries exactly one complete hop; a hop is never broken across physical lines. Hops rendered as an ordered list do not satisfy the prescribed form; the Abandoned Reasoning
  section either documents
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
  (assumption false, contradicts a GT, circular, intermediate could not be established); OR
  one or more chains render their hops as an ordered list (`1.`, `2.`, `3.`) instead of the
  prescribed arrow-led hop form, OR break a single hop across physical lines rather than
  splitting it into two hops, which splits one chain into disconnected
  fragments even where every hop is individually sound — **this clause is why the criterion
  cannot be scored on reasoning quality alone.** A chain that names its GT-IDs, carries a
  genuine intermediate and reaches a conclusion satisfies every other Rigorous requirement
  while still failing the prescribed form; scoring only the semantics is what lets a
  Rigorous verdict coexist with a section of malformed chains.

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
  chain that contributes to it, counting only chains not covered by an EXCEPT clause stated
  in this same descriptor; no chain that consumes a GT-N? input is rated HIGH confidence.
  Every claim in the Conclusion section rests on at least one HIGH-confidence chain, so that
  this aggregation yields HIGH. EXCEPT: a chain is explicitly marked speculative — for
  example `[Speculative]` — and the analysis states, in the same place, that the claim it
  supports is not load-bearing and is offered for exploration only; that mark plus that
  statement is the satisfying evidence, and the chain may remain MEDIUM. EXCEPT: a chain is
  an absent-fails derivation — of the form "if [assumption] were true we could conclude X;
  [assumption] is false; therefore X does not follow" — whose named false assumption is the
  satisfying evidence, and the chain may remain MEDIUM because it establishes what does not
  follow rather than what does.

  **A conclusion without a HIGH chain is a banding matter, not a gate failure.** A conclusion
  resting on no HIGH-confidence chain, uncovered by either EXCEPT clause above, bands this
  criterion below Rigorous rather than failing the gate — one such conclusion bands Sound;
  the same shortfall across multiple conclusions bands Hand-wavy. A MEDIUM or LOW overall
  Conclusion rating remains a legitimate, honestly-caveated analysis — `output-template.md`
  permits it and this criterion does not forbid it; what such an analysis is not is Rigorous
  on Criterion 5, and its verdict block must say so rather than reporting Rigorous alongside
  a MEDIUM rating. An exception is claimed, not assumed: an analysis relying on one of the
  two EXCEPT clauses above names it in the Criterion 5 verdict block and cites the evidence
  that clause requires; an unclaimed exception is not applied on the analysis's behalf.

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
presented. If either condition is not met, revise the relevant sections and re-score — bounded
to **at most one re-perception pass** per analysis, per the rule stated in full under "How to
Apply This Gate" at the top of this document. If a criterion still fails after that single
pass, present it as an unresolved gap with a stated confidence caveat instead of re-scoring
again. This closing note restates that bound; it does not create a second, looser one.
