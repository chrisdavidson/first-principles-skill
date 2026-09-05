# Analysis: Should the docs team migrate to a new CMS before the next release cycle?

A first-principles analysis of whether the documentation team should migrate to a new content
management system before the next major release cycle.

---

## 1. Problem Essence

**Core problem:** Authors have reported friction with the current CMS's review workflow. Should
the docs team migrate to a new CMS before the next release cycle, or is the current tooling
adequate with configuration changes alone?

**Success criteria:**

- The migration case is derived from measured authoring throughput, not from general dissatisfaction.
- The timing case is derived from the release calendar, not from convenience.
- The recommendation states which measured facts justify it and which do not.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A new CMS would fully eliminate review-cycle delays | untested belief | Challenge before use — a new CMS reduces friction in the tooling layer but does not by itself change reviewer availability, which is a separate bottleneck | Challenge — the elimination claim conflates a tooling fix with a staffing fix | Reviewer-availability data shows delays persist even on documents that already use a lighter-weight review path in the current tool, indicating the tool is not the sole driver |
| Migration effort can be completed inside the current release cycle | current constraint | Record expiry conditions — this is an estimate based on the current team size and could shift if headcount changes | Accept — the current sizing estimate from the platform team supports a within-cycle migration | Confirmed against the platform team's current capacity estimate; expires if team size or scope changes |

---

## 3. Ground Truths

- **GT-1** Average time from draft submission to publish across the last two release cycles was
  11.4 business days — source: the docs pipeline's own timestamp log for submission and publish
  events.

- **GT-2** The current CMS's review-assignment feature has been the subject of 23 internal
  support tickets over the last two quarters, more than any other docs-tooling feature — source:
  the internal tooling support-ticket tracker, filtered to the docs-CMS component.

---

## 4. Derivation Chains

### Conclusion C1: The migration should be scoped as a review-workflow project, not a platform swap
C2 (the downstream editorial-consolidation conclusion) → the review-workflow friction that motivates the whole migration effort is, on inspection, the same friction the editorial-consolidation project already names as its own justification → framing the migration as a review-workflow project rather than a ground-up platform swap keeps the two efforts aligned rather than duplicated

**Confidence: MEDIUM** — the framing choice follows from how the two initiatives were scoped
relative to each other; neither chain in this document anchors to a measured fact about which
framing is correct.

---

### Conclusion C2: The migration should be sequenced after the editorial-consolidation project (C3) completes
C3 (the editorial-consolidation conclusion, a project not otherwise detailed in this analysis) → the consolidation project's own output determines which content types the new CMS actually needs to support → sequencing the CMS migration after consolidation avoids building support for content types that consolidation may retire

**Confidence: MEDIUM** — this chain cites the consolidation project's expected output rather than
a ground truth measured for this analysis; C3 is referenced as the source of that output but is
not itself derived here.

---

## 5. Abandoned Reasoning

### Dead End: Anchor the migration decision to the ticket count alone

**What was tried:** Treat GT-2's 23 support tickets as sufficient justification on its own —
reason directly from "more tickets than any other feature" to "therefore migrate."

**Why abandoned:** A raw ticket count does not distinguish between a small number of frequent
filers and a broad pattern across the authoring team, and it says nothing about whether a
configuration change inside the current CMS would resolve the same complaints. The count alone
was judged insufficient to carry the derivation and was set aside in favor of the sequencing
argument in chains C1 and C2.

**What it ruled out:** Treating the ticket count as a standalone justification for the migration
decision.

---

## 6. Conclusion

1. (chain C1) Scope the CMS work as a review-workflow project rather than a ground-up platform
   swap, to keep it aligned with the editorial-consolidation effort rather than duplicating it.
2. (chain C2) Sequence the migration after the editorial-consolidation project completes, so the
   new CMS is built to support the content types consolidation actually retains.

**Confidence: MEDIUM** — the sequencing argument is internally consistent, but neither chain in
this document ties its recommendation back to GT-1 or GT-2; both named ground truths describe the
symptom (submission-to-publish time, ticket volume) without either derivation chain reaching them.
