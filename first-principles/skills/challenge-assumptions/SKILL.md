---
name: challenge-assumptions
description: Slash-only Phase 2 stub — classify and test every assumption before reasoning.
disable-model-invocation: true
metadata:
  version: "8.17.2"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/challenge-assumptions/SKILL.md by sync-content.py -->

# Focused Challenge Assumptions Mode

You are running in focused-challenge-assumptions mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

## When to reach for this

Use this phase once the Essence Statement from Phase 1 is complete. An unchallenged
assumption that is false propagates invisibly through every later reasoning step. By
explicitly classifying and testing each assumption before establishing ground truths,
the analysis prevents false premises from masquerading as verified facts.

---

## Procedure

Identify every assumption — explicit and implicit — that bears on the problem. For each
one, classify it by type using the four-type scheme below, apply the prescribed treatment,
and record the verdict. Surface hidden assumptions: things that are treated as given but
have never been verified. When the assumption space feels too broad to enumerate by
intuition, use the fishbone procedure to brainstorm causes by category, then bring each
branch into this table as an `untested belief`. When a conclusion feels too clean or a
goal feels too obvious, use the inversion procedure to enumerate what would guarantee
failure — each unverified precondition becomes an `untested belief` row in this table.
When the stakes of a conclusion rest heavily on a particular assumption, push that
assumption down toward physical law or verified ground truth status rather than accepting
a weaker classification. Classification drives the method — it is not merely labelling.

**The four assumption types and their prescribed treatments:**

| Type | Prescribed Treatment |
|------|---------------------|
| **physical law** | Accept as a ground-truth candidate. Physical laws do not expire and cannot be negotiated away. |
| **current constraint** | Record the expiry conditions — what would have to change for this constraint to lift. |
| **convention** | Explicitly challenge before use. Ask whether the convention holds in this specific context or merely carries historical inertia. |
| **untested belief** | Verify, or flag as unverified. An unverified belief may be used in a derivation chain but must be visibly flagged (e.g., `GT-N?: unverified`) and any conclusion depending on it inherits an explicit confidence caveat. |

**Stakes-escalation rule:** The higher the stakes of the conclusion resting on an
assumption, the more that assumption must be pushed toward physical law or verified ground
truth. A critical conclusion resting on a convention or untested belief is a fragile
conclusion — either verify the assumption or flag the conclusion's confidence accordingly.

For a refined within-type subtype catalog with prescribed treatments and cited evidence,
see the Assumption Taxonomy reference. Subtypes are recommended-but-not-required; the
parent type's treatment remains a valid fallback.

**Named artifact:** Classified Assumptions Table — a table with columns: Assumption,
Type, Treatment, Verdict, Verification.

**Exit criterion:** Every assumption in scope has a classification from the four-type
scheme (physical law / current constraint / convention / untested belief) AND has a
recorded verdict and verification note, or an explicit "unverified — flagged" note per
D-07.

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
