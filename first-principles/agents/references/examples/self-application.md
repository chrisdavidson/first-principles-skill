<!-- GENERATED — DO NOT EDIT. Source: shared/examples/self-application.md. Regenerate via: scripts/sync-content.py --write. -->

# Worked Example: Self-Application (Meta)

A complete first-principles analysis applied to a live, contested design decision
*about the agent that performs first-principles analyses*. The triggering observation
is that `first-principles/agents/first-principles.md` is currently 878 lines while
META-Q4 records a budget of "~500 lines / ~5,000 tokens." Authored in Phase 32 as a
dogfooding example: the methodology turned on the artifact it ships from.

**Scenario.** The single-agent surface shipped in v3.0 inlined the methodology body,
the six companion-tool procedures, the canonical output template, and the validation
rubric into one file at `first-principles/agents/first-principles.md`. Two milestones
later the file measures 878 lines. The recorded budget — `~500 lines / ~5,000
tokens`, encoded as regression gate META-Q4 in `.planning/REQUIREMENTS.md` — is
nominally violated by roughly 75%. Engineering convention reaches reflexively for
the response *"split it"* (extract content into `references/` files). This analysis
strips that response away and asks what the budget is actually optimizing for before
choosing any intervention.

---

## 1. Problem Essence

**Core problem:** What does the ~500-line agent-body budget optimize for, does the
current 878-line body violate that optimization in a measurable way, and what is
the minimum intervention — if any is warranted — that restores the property the
budget exists to protect?

The triggering framing — "the body is too long, how should we split it?" — is a
proposed solution sitting on top of an unverified premise: that the ~500-line
budget is load-bearing for some property of the agent, and that 878 lines breaks
that property. First-principles analysis requires interrogating the budget itself
before reasoning about extractions. The symptom is "over budget"; the underlying
question is whether the budget tracks anything the agent actually depends on.

**Success criteria:**

- The property the ~500-line budget exists to protect is named explicitly and
  traced to a shipped artifact (REQUIREMENTS.md, PROJECT.md, or a regression gate),
  not asserted from general best-practice intuition.
- The 878-line body is decomposed into structural segments with measured line
  ranges so that "which segment is consuming the budget" is a checkable fact, not
  a guess.
- The recommended intervention — if any — addresses the segment that actually
  drives the overage, not the segment that is most syntactically tempting to
  extract.
- If the budget turns out to be a stale convention whose underlying property no
  longer holds, the recommendation revises the budget rather than performing an
  extraction that solves nothing.
- The recommendation does not prejudge the v3.0 inlining decision; if the
  inlining was correct then and remains correct now, the conclusion says so.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| The ~500-line budget is load-bearing for some observable property of the agent | untested belief | Verify before use — locate the artifact that records the budget and the property it protects; if the property is not specified, the budget is a convention, not a constraint | Challenge | Recorded in `.planning/REQUIREMENTS.md` line 53 as META-Q4; the protected property is named as "stays under the ~500-line / ~5,000-token budget" with rationale "New content lives in references/" — i.e., the budget is itself the property, with no independent measurable consequence stated; flagged for further classification |
| The agent body is too long because the methodology procedure is too long | untested belief — diagnostic | Verify by ruling out alternative segments — multiple structural sections could individually account for the overage; collecting confirming evidence for "the methodology is bloated" is not the same as ruling out the appendices, the companion-tool procedures, or accumulated cross-references | Challenge | Unverified — flagged; line-range measurement of the body's structural segments (Section 3, GT-2 through GT-4) is required before any segment can be named as the dominant contributor |
| Aggressive Layer-3 extraction of Phase 1–5 procedural blocks would bring the body under 500 lines | untested belief — methodology | Verify by constructing the alternative — measure the procedural-block line range and compute the resulting body size if the extraction were performed | Discard | Phase 1–5 procedural blocks span lines 45–141 of `first-principles/agents/first-principles.md` (~96 lines). Extracting them yields a body of approximately 782 lines, still 282 lines over budget — the proposed method does not produce the claimed outcome (Chain 2 in Section 4) |
| Extracting content into `references/` always reduces the agent's reasoning quality | convention — context-dependent technical | Challenge specifically by naming the contextual variables — what kind of content, when read by the agent, with what frequency, under what continuation properties | Challenge | The agent body already delegates the Subtype Catalog to `references/assumption-taxonomy.md` (line 92 cross-reference) without an observed reasoning regression. The convention holds only for content the agent must inspect on every single analysis; content the agent looks up conditionally does not appear bound by it |
| The v3.0 inlining decision must be preserved as-shipped | convention — default-response | Challenge by asking whether "preserve the shipped surface" addresses the highest-frequency observed signal versus the cognitively-available response. The v3.0 inlining was justified for *the methodology and companion tools*; the inlining of the Output Template and Validation Rubric appendices is a separate decision that has not been independently scrutinized | Challenge | The PROJECT.md v3.0 rationale (`shared/spine/references` → "absorb their methodology, companion-tool references, and worked examples into the agent's reachable context") names methodology + companion tools + examples; it does not separately justify inlining the Layer-3 appendices that were already authored as Layer-3 reference files |
| A full rewrite or large body restructure is required to bring the budget into compliance | untested belief — false-dichotomy | Challenge the binary framing — enumerate intermediate options (extract one block, extract two appendices, revise the budget, do nothing) and check whether any dominates the poles on cost and reversibility | Discard | At least one intermediate option (de-inline the Output Template and Validation Rubric appendices, leaving methodology and companion tools intact) is testable for body-size impact in Chain 3 and dominates the rewrite on reversibility |

---

## 3. Ground Truths

- **GT-1** The agent body file `first-principles/agents/first-principles.md` is
  currently 878 lines as measured by `wc -l` at the time of this analysis — source:
  direct measurement of the file in this repository on the working branch.

- **GT-2** The procedural body (the methodology proper — Phases 1–5 entry/operation/
  artifact/exit blocks plus the "How the phases connect" preamble) spans lines
  45–141 of the agent body, approximately 96 lines — source: heading scan of
  `first-principles/agents/first-principles.md` (`## Methodology` at line 45;
  `## Output format` at line 142 marks the next top-level heading).

- **GT-3** The inlined companion-tool procedures (six `## Procedure` blocks for
  5-Whys, fishbone, inversion, pre-mortem, trade-off, second-order) span lines
  234–408, approximately 175 lines — source: heading scan of the same file
  (six `## Procedure` headings at lines 234, 259, 291, 320, 345, 376; next
  top-level heading `## How to Use This Template` at line 415 marks the appendix
  boundary).

- **GT-4** Two Layer-3 reference files exist as separate artifacts under
  `shared/spine/references/`: `output-template.md` (150 lines) and
  `validation-rubric.md` (320 lines). Together these contain 470 lines of
  authored Layer-3 reference content that already lives outside the agent body
  in the source-of-truth tree — source: direct `wc -l` measurement of both files
  and inspection of the repository layout.

- **GT-5** The agent body inlines the same Output Template and Validation Rubric
  content as appendices: `## How to Use This Template` begins at line 415 and the
  appendix region runs to line 878 (the end of the file), approximately 464 lines.
  A direct `diff` of agent-body lines 415–567 against
  `shared/spine/references/output-template.md` differs only by the absence of the
  reference file's title-and-Note prefix in the inlined copy — the substantive
  content is the same — source: line-level diff of the two regions.

- **GT-6** The agent body already uses one Layer-3 external reference at line 92:
  the Phase 2 Assumptions Table block delegates the Subtype Catalog to
  `references/assumption-taxonomy.md` via a body-resident link
  ("For a refined within-type subtype catalog with prescribed treatments and
  cited evidence, see [Assumption Taxonomy](references/assumption-taxonomy.md).
  Subtypes are recommended-but-not-required..."). The pattern (link out, one
  level deep, with a one-line description of what the reader will find there)
  is therefore precedent — not novel — for this agent surface. No regression in
  agent reasoning quality has been observed since that delegation shipped in
  Phase 31 — source: direct inspection of `first-principles/agents/first-principles.md`
  line 92 and the Phase 31 phase artifacts under
  `.planning/phases/31-assumption-classification-taxonomy/`.

- **GT-7** The recorded budget is META-Q4 in `.planning/REQUIREMENTS.md` line 53:
  "Agent body in `first-principles/agents/first-principles.md` stays under the
  ~500-line / ~5,000-token budget. New content lives in references/examples/
  where appropriate." The rationale stated for the budget (the *property* the
  budget protects) is itself recorded only as "lives in references/" — no
  independent observable property (token-cost-per-invocation, attention-budget,
  context-window competition, agent-self-test latency) is cited as the
  consequence the budget is sized to prevent — source: direct read of the
  requirements file.

- **GT-8** The regression gates that the agent surface is *actually* checked
  against on every change are `scripts/check-agent.py --self-test` (Checks 1–8,
  with Check 8 verifying the four locked trigger phrases verbatim) and
  `scripts/sync-content.py --check` (lockstep between `shared/` and the agent
  surface). Neither script measures line count or token count; neither encodes
  an observable failure mode tied to the ~500-line figure — source: direct
  read of `scripts/check-agent.py` (Checks enumerated at lines 225–298) and
  `scripts/sync-content.py`.

- **GT-9?** Increasing agent-body line count above some unspecified threshold
  degrades the agent's reasoning quality on first-principles analyses by
  consuming attention budget or crowding the conversation context — unverified:
  no measurement exists in this repository that ties body line count to agent
  reasoning quality. The closest available signal is the routing battery
  (`scripts/check-routing.py`, P ≥ 6/8, N ≥ 14/15), which measures *delegation*
  routing — whether the agent is invoked when it should be — not the analytical
  rigor of the analyses it then produces. The Phase 28 EVAL-01 climbing-gym test
  evaluated rigor but was a single point, not a body-size sweep.

---

## 4. Derivation Chains

### Conclusion: The budget is a convention without a named protected property

GT-7 (META-Q4 records the budget as "stays under ~500 lines" with no independent
observable consequence) + GT-8 (the regression gates that actually run on every
change measure self-test correctness, trigger-phrase preservation, and shared/↔
agent lockstep — they do not measure line count or token cost) + GT-9? (no
measurement in the repository ties body line count to reasoning quality)

→ The budget exists in the requirements register and is treated as a constraint
by the project workflow, but the consequence it is sized to prevent is not
recorded. A skeptic reading META-Q4 cannot tell whether 878 lines breaks
something measurable or merely exceeds a number authored from general
intuition. The shipped regression gates encode the *real* properties the
project depends on (self-test correctness, trigger-phrase preservation, sync
lockstep, routing PASS verdict) and none of them references line count.

→ The ~500-line budget is best classified as a convention — a defensible
heuristic adopted from the wider Claude Code skill-authoring literature
(SKILL.md guidance recommends <500 lines for optimal performance) — not as a
verified constraint binding this specific agent. Treating it as binding when
its underlying property has not been measured is treating a heuristic as a
ground truth.

**Confidence:** MEDIUM — GT-9? is the unverified input. The chain establishes
that the budget is *currently* a convention as recorded; it does not establish
that no measurable cost exists. Verification that would raise confidence to
HIGH: an A/B reasoning-quality comparison of the agent body at 878 lines vs. a
de-inlined ~414-line body on a fixed problem set, or token-cost-per-invocation
measurement showing the inlined appendices contribute a non-trivial fraction
of per-turn context cost.

---

### Conclusion: The methodology procedural block is not the segment consuming the budget

GT-1 (current body: 878 lines) + GT-2 (Phase 1–5 procedural blocks: ~96 lines)
+ GT-3 (six inlined companion-tool procedures: ~175 lines) + GT-5 (inlined
Output Template + Validation Rubric appendices: ~464 lines)

→ The 878 lines decompose into roughly four structural segments: front-matter +
input contract (~44 lines), methodology procedure (~96 lines), interstitial
content + companion-tool prefaces + reference-doc nav (~99 lines), companion-tool
procedures (~175 lines), and appendices (~464 lines). Each of these would
have to be extracted independently to drop the body under 500 lines from
where it stands, *unless* the largest segment is removed — in which case the
body lands near or below the target without further extractions.

→ The 464 lines of inlined appendix content (53% of the body) is the segment
that drives the budget overage. Extracting only the Phase 1–5 procedural
blocks (the path D-04 sketched in Phase 32 CONTEXT as the anchor candidate
for Abandoned Reasoning) saves ~96 lines and leaves the body at approximately
782 lines — still 282 lines over the recorded target. Any extraction that
targets methodology before appendices is targeting a segment that cannot, by
arithmetic, deliver the claimed outcome.

**Confidence:** HIGH — GT-2 and GT-5 are direct line-range measurements of the
shipped artifact. The arithmetic does not depend on any unverified input.

---

### Conclusion: De-inlining the appendices is the minimum-cost intervention that restores the budget property, *if* the budget is treated as binding

GT-4 (Output Template and Validation Rubric already exist as separate files
under `shared/spine/references/`, 470 lines combined) + GT-5 (the agent body
re-inlines those same files verbatim as ~464 lines of appendix content) + GT-6
(the agent body already uses an external Layer-3 reference at line 92 with no
observed regression) + GT-8 (the regression gates `check-agent.py --self-test`
and `sync-content.py --check` do not depend on the appendix content being
inlined; Check 7 verifies no unresolved sync markers, Check 8 verifies the
four trigger phrases — neither check inspects appendix prose)

→ The appendix inlining is a content duplication: the same Layer-3 reference
material exists in two places in the source tree (`shared/spine/references/*`
and the inlined appendix region of the agent body). Removing the appendix
region from the agent body and replacing it with the same one-level-deep
reference link the agent already uses at line 92 ("For the full annotated
template, see `references/output-template.md`. For the scoring rubric, see
`references/validation-rubric.md`.") drops the body from 878 lines to
approximately 414 lines — under the META-Q4 budget by a wide margin — and
preserves the agent's access to the appendix content via the same delegation
pattern Phase 31 proved out.

→ The intervention is configuration-level, not architectural: the body's
`#first-principles-analysis-output-template` and `#validation-rubric` anchors
get replaced with relative-path links to the existing reference files; the
sync pipeline (`scripts/sync-content.py`) already propagates
`shared/spine/references/*` to `first-principles/agents/references/`; no new
content is authored and no shipped artifact is deleted. Reversibility: the
inlining can be restored by reverting the body edit if reasoning-quality
measurement (the GT-9? verification step) shows the de-inlining harmed agent
performance.

**Confidence:** MEDIUM — the chain's structure is HIGH; the *recommendation to
act* inherits the MEDIUM rating from Chain 1's GT-9? dependency. If the budget
is a convention without a measured property (Chain 1), then the intervention
solves a problem whose impact has not been quantified. The intervention is
still defensible — it deduplicates content the source tree already contains
twice, and aligns the agent surface with the Phase 31 delegation precedent —
but it does so to satisfy a recorded number rather than a measured outcome.

---

## 5. Abandoned Reasoning

### Dead End: Aggressively extract the Phase 1–5 procedural blocks into `shared/spine/references/phase-N.md` files

**What was tried:** Take the procedural content of the methodology (Phases 1–5,
each with Why-this-phase / Entry / Operation / Artifact / Exit subsections) and
lift each phase into its own Layer-3 reference file under
`shared/spine/references/`. The motivation was that the procedural blocks are
the most explicitly "procedural" — they read like a recipe — and procedural
content is conventionally the kind that benefits most from being externalized
to a reference file. The proposed shape was:

```text
shared/spine/references/
  phase-1-identify-essence.md
  phase-2-challenge-assumptions.md
  phase-3-establish-ground-truths.md
  phase-4-reason-upward.md
  phase-5-validate.md
```

The agent body's `## Methodology` section would shrink to a one-line preamble
per phase followed by a link to the corresponding reference file, in the same
pattern the body already uses for the Subtype Catalog at line 92.

**Why abandoned:** Three failures, each independently sufficient.

First, GT-2 measures the Phase 1–5 procedural blocks at approximately 96 lines.
Extracting them in full saves at most ~96 lines and leaves the body at
approximately 782 lines — still 282 lines over META-Q4 (the constraint the
extraction was supposed to satisfy). The chain "Phase 1–5 is too long → extract
it → under budget" fails on its arithmetic premise. The reasoning was not
exploring whether extraction is sound; it was extracting from the wrong segment.
GT-5 (~464 lines of inlined appendix content) is the segment whose extraction
would actually move the body under budget — and the appendix extraction is the
path Chain 3 in Section 4 walks instead.

Second, the procedural through-line is the part of the agent body the agent
itself executes on every analysis. The exit criterion of one phase is the entry
criterion of the next ("the Essence Statement is written" → "the Classified
Assumptions Table is built on top of the Essence Statement"). Pushing each
phase to its own file forces the agent to re-establish phase ordering by
chasing one-level-deep links five times per analysis, where the current body
makes the ordering visible at a single read. GT-6 establishes the delegation
precedent at line 92, but that precedent delegates a *catalog* (a reference
lookup) — not a procedural through-line that downstream phases depend on. The
two cases are not equivalent: the agent inspects the Subtype Catalog
conditionally (when a non-trivial assumption appears), while the agent
executes the Phase 1–5 procedure unconditionally. Conventions about "what
content benefits from externalization" do not collapse the difference between
conditional reference content and unconditional procedural content.

Third, the same arithmetic that abandons this path also redirects it. The
appendix region (lines 415–878) contains content that the agent body already
imports verbatim from `shared/spine/references/output-template.md` and
`shared/spine/references/validation-rubric.md` (GT-4 + GT-5). Those files
exist on disk. The path that actually removes the budget overage is not
authoring five new reference files for content that lives inline only in the
body — it is removing the *inlined duplicates* of content that already lives
in reference files. The wrong-segment failure is not a missed optimization;
it is a clear pointer at the right segment.

**What it ruled out:** Procedural-block extraction as a budget-restoring
intervention. The Phase 1–5 procedure stays inline. Future analyses
considering body-size interventions can start from GT-5 (the appendix
duplication) without re-exploring the methodology-extraction path. The
broader lesson — that extraction targets must be chosen by measured line
range, not by perceived "proceduralness" — is the ruling-out that makes
this dead end valuable.

---

### Dead End: Accept that 878 lines is fine because Phase 28 EVAL-01 passed and the routing battery PASSes at this body size

**What was tried:** Argue that since the agent currently passes
`scripts/check-routing.py` at P 7/8, N 15/15 and passed the Phase 28
EVAL-01 climbing-gym rigor test at the size it then had, no body-size
intervention is warranted regardless of the META-Q4 figure. The chain
was: GT-8 records that the gates that actually run pass at 878 lines;
META-Q4's line-count check is the only gate that fails; therefore
META-Q4 is the gate to revise rather than the body.

**Why abandoned:** This path was abandoned not on a flaw in its
reasoning — Chain 1 in Section 4 reaches a related conclusion (the
budget is a convention without a named protected property) — but on
its premise's confusion of two distinct questions. The premise treats
"the agent currently passes the running gates" as evidence that "any
body size below some unknown threshold is acceptable." But the routing
battery measures *delegation routing*, not analytical rigor inside the
analysis. EVAL-01 measured rigor on one specific problem at one
specific body size; it did not produce a body-size threshold below
which rigor is guaranteed (GT-9?). The chain confuses absence of
evidence of harm with evidence of absence of harm. Abandoning the
budget on this premise is symmetric in error to enforcing the budget
on it: both moves treat an unmeasured property as if it were measured.

The correct response to Chain 1's MEDIUM confidence is the one Chain 3
already takes: perform the lowest-cost, fully-reversible intervention
(de-inline the appendices) *and* commission the measurement (GT-9?'s
verification step) that would settle the budget's underlying property.
"Do nothing because no harm has been observed" is not symmetric with
"do something because no harm has been measured" — it is its inverse,
and inherits the same MEDIUM confidence from the same unverified
input.

**What it ruled out:** Using "the gates currently pass" as a standalone
argument against any body-size intervention. The gates that pass
measure properties other than the one META-Q4 nominally protects.
Their passing is necessary but not sufficient evidence about the
budget's load-bearingness.

---

## 6. Conclusion

**Recommended approach:** Execute one configuration-level intervention and
commission one measurement, in parallel.

1. **De-inline the Output Template and Validation Rubric appendices** from
   `first-principles/agents/first-principles.md`. Replace the appendix region
   (currently lines 415–878) with two one-line external references in the
   `### Reference docs` block that already exists at line 226: a link to
   `references/output-template.md` and a link to `references/validation-rubric.md`.
   These reference files already exist in `shared/spine/references/` and already
   propagate to the agent surface via `scripts/sync-content.py`. The intervention
   is authored in `shared/` (the body source) and synced; no hand-edit of the
   agent surface occurs. Expected body size after the change: approximately
   414 lines, comfortably under the META-Q4 budget of ~500. The intervention is
   fully reversible by reverting the body edit.

2. **Commission the GT-9? measurement** that would settle whether body-size
   reduction *matters* for agent reasoning quality. The minimum form is a
   small A/B: run the EVAL-01 climbing-gym fixture (or an equivalent rigor
   probe) against both the pre-intervention 878-line body and the
   post-intervention ~414-line body, holding model and prompt fixed. If the
   measurement shows no rigor difference, META-Q4 should be re-recorded as a
   heuristic with the measurement attached; if it shows a rigor improvement,
   META-Q4's binding force is verified and the intervention is doubly
   justified; if it shows a regression, the intervention is reverted before
   it ships.

The intervention is justified independently of the measurement's outcome
because it deduplicates content that the source tree already contains in
two places (the inlined appendix region of the agent body, and the
authored Layer-3 reference files under `shared/spine/references/`). The
measurement is justified independently of the intervention because META-Q4
will continue to fire on every future content addition and the gate's
binding force should be settled rather than inherited from convention.

**Key insight:** The cognitively-available response to "the agent body is
878 lines vs. a ~500-line budget" is to extract the most procedural-looking
content — the Phase 1–5 methodology blocks. That response is wrong on
arithmetic before any reasoning-quality argument is made: the methodology
proper is ~96 lines and its extraction leaves the body at ~782 lines, still
282 lines over budget. The 464 lines of inlined appendix content — content
that already exists as Layer-3 reference files in the source tree and is
duplicated verbatim into the agent body — is what actually consumes the
budget. The first-principles move is not "split the body" but "measure
which segment consumes the budget, then verify what the budget exists to
protect." Once measured, the right segment is unambiguous, the
intervention is configuration-level rather than architectural, and the
remaining question — whether the budget binds anything observable — is
recognized as the real open question rather than collapsed into the
extraction problem.

**Trade-offs acknowledged:**

- The de-inlining intervention costs the agent one additional read hop for
  Output Template and Validation Rubric content. The Phase 31 delegation
  precedent (GT-6) shows the hop is workable for catalog-style reference
  content; the appendices are also Layer-3 reference content (they exist
  as standalone reference files in `shared/spine/references/`) and are
  thus structurally analogous to the precedent. The trade-off is real but
  small and reversible.

- The intervention does not touch the inlined companion-tool procedures
  (~175 lines, GT-3) or the Phase 1–5 methodology blocks (~96 lines, GT-2).
  Both remain inline. The v3.0 inlining rationale named methodology and
  companion tools specifically; this intervention respects that rationale
  while interrogating the part of v3.0 that was not separately justified —
  the appendix re-inlining of files that already existed as references.

- The MEDIUM confidence on Chain 1 carries into the recommendation: if the
  GT-9? measurement shows the budget tracks nothing measurable, the
  intervention is still defensible on deduplication grounds but no longer
  has an analytical-rigor justification. The measurement is what
  distinguishes a deduplication win from a rigor win; it should not be
  deferred indefinitely.

- The recommendation does not perform the more ambitious restructure
  candidates that were considered and abandoned (Phase 1–5 extraction,
  full rewrite). Those remain available as future moves if measurement
  later identifies them as warranted; the false-dichotomy assumption in
  Section 2 is discharged by the existence of the de-inlining
  intermediate.

**Confidence:** MEDIUM — Chain 2 (where the budget overage actually lives)
is HIGH confidence; Chain 3 (the intervention removes it) is HIGH
confidence on arithmetic and configuration; Chain 1 (the budget's
underlying property) inherits MEDIUM from GT-9?. The recommendation
proceeds at MEDIUM because the GT-9? verification step is named, scoped,
and executable rather than open-ended. Confidence rises to HIGH once the
A/B rigor measurement is performed and either confirms a rigor improvement
or confirms no regression on the de-inlined body.
