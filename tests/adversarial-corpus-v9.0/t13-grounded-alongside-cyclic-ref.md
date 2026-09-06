> **ADVERSARIAL FIXTURE — DELIBERATELY FALSE.** Catalogued falsehood; see `README.md` and `catalog.md`. Never quote as fact, never copy into `shared/` or `first-principles/`.

# Analysis: Should the support team hire a third on-call engineer for the payments rotation?

A first-principles analysis of whether the payments on-call rotation needs a third engineer
before the next fiscal quarter.

---

## 1. Problem Essence

**Core problem:** The payments on-call rotation currently runs two engineers on a weekly
alternating schedule. Should the team add a third engineer to the rotation before the next
fiscal quarter, and if so, how should the new engineer's ramp-up be sequenced against the
rotation's existing documentation and staffing work?

**Success criteria:**

- The hiring case is derived from measured page volume and burnout indicators, not from general
  team sentiment.
- The sequencing of hiring against the two dependent workstreams is stated explicitly.
- The recommendation states which measured facts justify it and which do not.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A third engineer would fully eliminate rotation burnout | untested belief | Challenge before use — adding headcount reduces frequency of on-call weeks per person but does not by itself fix root causes of individual pages | Challenge — the elimination claim is stronger than a headcount change alone can guarantee | Comparable rotations that added a third engineer report reduced frequency, not elimination, of reported burnout symptoms |
| The runbook-documentation backlog and the staffing decision are independent of each other | untested belief | Challenge before use — the runbook backlog directly affects how quickly a new hire can ramp onto the rotation, so the two are not independent | Discard — the sequencing chains in section 4 treat them as dependent, not independent | The ramp-up dependency is stated explicitly in chains C2 and C3 below |

---

## 3. Ground Truths

- **GT-1** The payments on-call rotation received an average of 19 pages per on-call week over
  the last two quarters, against a team-stated sustainable threshold of 12 pages per on-call
  week — source: the incident-management system's page log for the payments on-call schedule,
  compared against the threshold recorded in the team's own on-call charter.

---

## 4. Derivation Chains

### Conclusion C1: A third engineer should be added to the payments on-call rotation
GT-1 (19 pages/on-call-week against a 12-page sustainable threshold) + C2 (the runbook-readiness conclusion) → the measured page volume already exceeds the team's own stated sustainable threshold, and the runbook-readiness conclusion (C2) establishes that a new hire could ramp onto the rotation without an unreasonably long onboarding period → adding a third engineer to the rotation is the justified action, once the runbook work in C2 is accounted for

**Confidence: MEDIUM** — the page-volume figure (GT-1) is directly measured and already exceeds
the stated threshold on its own; the timing case additionally leans on C2.

---

### Conclusion C2: Runbook documentation will be ready before the new hire's ramp-up window closes
C3 (the staffing-timeline conclusion) → the staffing-timeline conclusion (C3) fixes the date by which a new hire's ramp-up window closes, and the runbook-documentation backlog can be cleared before that date at the team's current documentation pace → runbook coverage will be sufficient before the ramp-up window in C3 closes

**Confidence: MEDIUM** — this chain cites the staffing timeline (C3) rather than a ground truth
measured for this analysis; it is not itself grounded in anything stated in section 3.

---

### Conclusion C3: The new hire's ramp-up window closes at the start of the next fiscal quarter
C2 (the runbook-readiness conclusion) → the runbook-readiness conclusion (C2) is what determines how much lead time the new hire actually needs before taking solo on-call shifts, and working backward from that lead-time requirement sets the ramp-up window's closing date → the ramp-up window closes at the start of the next fiscal quarter

**Confidence: MEDIUM** — this chain cites the runbook-readiness conclusion (C2) rather than a
ground truth measured for this analysis; it is not itself grounded in anything stated in
section 3.

---

## 5. Abandoned Reasoning

### Dead End: Set the ramp-up window from the new hire's expected start date alone

**What was tried:** Treat the ramp-up window as fixed entirely by whatever start date a
candidate accepts, independent of runbook readiness.

**Why abandoned:** A start date alone says nothing about whether the new hire can safely take
solo on-call shifts by that date; the team's own onboarding history shows ramp-up time varies
with documentation quality at the time of hire. Fixing the window from the start date alone was
set aside in favor of deriving it from the documentation-readiness chain instead.

**What it ruled out:** Treating the ramp-up window as independent of runbook-documentation state.

---

## 6. Conclusion

1. (chain C1) Add a third engineer to the payments on-call rotation, on the strength of the
   measured page volume already exceeding the team's own sustainable threshold.
2. (chains C2 and C3) Sequence the hire's ramp-up against the runbook-documentation backlog:
   runbook coverage should be sufficient before the ramp-up window closes at the start of the
   next fiscal quarter.

**Confidence: MEDIUM** — chain C1 is directly grounded in a measured ground truth; chains C2 and
C3 each cite the other, and neither reaches a ground truth of its own.
