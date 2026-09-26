# Track B Neutral Rubric

**Frozen 2026-09-25, before any Track B run.** Referenced by
`docs/trackb-preregistration.md`.

<!-- This file is handed verbatim to a blinded judge. It must not mention any other
     rubric, any comparison, or the existence of more than one document under study:
     a judge who infers that a contrast exists stops scoring on the document's own
     terms. The rationale for this rubric's design lives in the pre-registration,
     which the judge never sees. -->

Score the document on its own terms. Nothing below rewards any particular format.

---

## What you are scoring

You are scoring one analysis document, `analysis.md`, on the five criteria below.

Score it **entirely on its own terms**, as the only document you have ever been asked
to evaluate. Judge the quality of the thinking as presented to a reader who has to act
on it.

**Format carries no marks.** A flowing essay, a bulleted memo, a numbered report and a
single dense paragraph are all equally eligible for the top band on every criterion.
Do not reward structure, headings, tables, labelled sections or any particular
vocabulary. Do not penalise their absence. Length carries no marks either: a short
document that does the work scores above a long one that does not.

Reward the document for **doing the thinking**, not for **displaying a method**.

---

## The five criteria

### 1. Decision usefulness

Could a reader who has to make this decision act on this document?

- **3 — Rigorous.** Reaches a clear position and says what to do about it. The
  recommendation is specific enough to be executed or rejected, and the document makes
  plain who it is for and under what conditions it applies.
- **2 — Sound.** Reaches a position, but its practical edge is blunt: the
  recommendation is directionally clear yet under-specified, or hedged past the point
  of usefulness in one or two places.
- **1 — Hand-wavy.** Surveys considerations without landing anywhere a reader could
  act on, or lands somewhere so general it would fit any problem of this shape.
- **0 — Absent.** No position, or a position unrelated to the question asked.

### 2. Evidence grounding

Are the load-bearing factual claims actually supported?

- **3 — Rigorous.** Every claim the conclusion leans on is either derived in view of
  the reader, sourced, or explicitly flagged as an estimate with its basis given.
  Numbers come from somewhere the reader can see.
- **2 — Sound.** Most load-bearing claims are grounded; one or two are asserted
  where support was available and would have been easy to give.
- **1 — Hand-wavy.** The conclusion rests substantially on claims presented as fact
  with no visible support, or on figures with no stated origin.
- **0 — Absent.** Essentially unsupported throughout, or support is fabricated —
  a citation that does not say what it is claimed to say scores 0 regardless of the
  rest.

### 3. Assumption surfacing

Does the document make its own load-bearing assumptions visible?

- **3 — Rigorous.** The assumptions the conclusion depends on are named as
  assumptions, and the document engages with at least the most consequential one —
  testing it, bounding it, or saying what happens if it is wrong.
- **2 — Sound.** Assumptions are named but left largely unexamined, or the most
  consequential one is engaged while others pass unremarked.
- **1 — Hand-wavy.** Assumptions are gestured at generically ("assuming conditions
  hold") without identifying which specific ones the argument needs.
- **0 — Absent.** Proceeds as though its premises were facts.

### 4. Calibration

Does the document's confidence match its actual support?

- **3 — Rigorous.** Confidence is expressed and it tracks the evidence: strong where
  the support is strong, explicitly weaker where it is thin. The document distinguishes
  what it knows from what it is inferring.
- **2 — Sound.** Broadly calibrated, with one or two places where the confidence
  expressed runs ahead of or behind what was shown.
- **1 — Hand-wavy.** Uniform confidence throughout regardless of support, in either
  direction — flatly assertive about everything, or so hedged that well-supported
  findings are buried alongside speculation.
- **0 — Absent.** Confident conclusions resting on acknowledged guesswork, with no
  signal to the reader which is which.

### 5. Falsifiability

Does the document say what would change its mind?

- **3 — Rigorous.** States what evidence would overturn the conclusion, or what it
  would take for the recommendation to be wrong, specifically enough that someone could
  go and check.
- **2 — Sound.** Acknowledges the conclusion could be wrong and gestures at the
  conditions, without making them checkable.
- **1 — Hand-wavy.** Generic caveats ("further research is needed", "results may
  vary") that would apply unchanged to any document.
- **0 — Absent.** Presented as settled, with no acknowledgement that it could be
  wrong.

---

## Scoring

Total = the sum of the five criteria, 0–15.

Award each criterion independently. A document may be rigorous on evidence and absent
on falsifiability; do not smooth scores toward a central impression.

Where a document genuinely does not need a criterion — the problem admits no useful
falsification test, say — score what it does with that fact. A document that says *why*
the criterion does not apply here, specifically, scores 3. One that simply omits it
scores 0. A reason that could be copy-pasted onto any problem scores 1.

---

## Output format

Write one short paragraph per criterion explaining the band you assigned, then close
your response with exactly this block and nothing after it:

```text
=== TRACKB-SCORELINE-START ===
C1: <Rigorous|Sound|Hand-wavy|Absent>
C2: <Rigorous|Sound|Hand-wavy|Absent>
C3: <Rigorous|Sound|Hand-wavy|Absent>
C4: <Rigorous|Sound|Hand-wavy|Absent>
C5: <Rigorous|Sound|Hand-wavy|Absent>
=== TRACKB-SCORELINE-END ===
```

Replace each placeholder with exactly one value from its listed vocabulary. Do not add,
omit, reorder or rename any line inside the block.
