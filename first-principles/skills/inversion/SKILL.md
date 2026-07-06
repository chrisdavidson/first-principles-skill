---
name: inversion
description: Runs a focused inversion only — enumerates failure preconditions. Invoke via /inversion only.
disable-model-invocation: true
metadata:
  version: "8.0.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/inversion/SKILL.md by sync-content.py -->

# Focused Inversion Mode

You are running in focused-inversion mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

## When to reach for this

Use inversion during Phase 2 (Challenge Assumptions) when a claim is sitting in
the Classified Assumptions Table and you want to surface the hidden preconditions
it depends on — by reasoning backward from its failure rather than forward from
its support. Also a useful sanity check after Phase 4: invert the headline
conclusion and ask whether any necessary precondition is unverified.

**Decision rule — inversion vs. pre-mortem:** inversion stress-tests a **claim**;
[pre-mortem](pre-mortem.md) stress-tests a **plan**. With only a stated belief,
conclusion, or design principle in hand, inversion is the right tool. If a
concrete plan with actions and a timeline exists, pre-mortem fits better — it
reasons about implementation failure modes that claim-level inversion cannot see.

**Not a good fit:** stress-testing a plan with timelines and dependencies — use
[pre-mortem](pre-mortem.md). Tracing what already went wrong on a single causal
chain — use 5-Whys. Inversion is the negative-direction pass on a claim;
[second-order](second-order.md) thinking is the positive-direction pass
on the same conclusion — run inversion first to find what could fail, then
second-order to trace consequences of what holds.

---

## Procedure

1. **State the claim precisely.** Write the claim in one sentence in the form
   "X is true" or "X will hold." Avoid hedges. The sharper the claim, the
   sharper the inverted form.

2. **Invert it.** Rewrite the claim as its failure: "X is false" or "X does not
   hold." Resist softening the inverted form — "X might not hold" is not an
   inversion, it is a hedge.

3. **Enumerate failure-guaranteeing conditions.** List every condition that
   would *guarantee* the inverted form. These are not risks; they are
   sufficient causes of failure. Write at least five before stopping.

4. **Derive necessary preconditions.** For each failure-guaranteeing condition,
   identify the precondition whose absence would cause it. This converts a
   failure list into a list of things the original claim silently depends on.

5. **Check each precondition's status.** For every necessary precondition, ask:
   is it verified, conventionally assumed, or untested? Anything not currently
   verified is unverified by default.

6. **Record each unverified precondition as an `untested belief`.** Each
   unverified precondition becomes one row in the Classified Assumptions Table
   with type `untested belief`, routed back to Phase 2 for the
   challenge-and-verify operation.

---

## Worked mini-example

**Claim:** "Switching our primary database from Postgres to a managed NoSQL
service will reduce operational toil."

- **Inverted form:** "Switching to managed NoSQL will *not* reduce operational
  toil — toil will stay the same or increase."
- **Failure-guaranteeing conditions:**
  - The new service requires more frequent capacity tuning than the current setup
  - Application code requires substantial rewrites that introduce new bugs
  - Existing monitoring and runbooks do not transfer and must be rebuilt
  - The managed service's failure modes are unfamiliar to the on-call rotation
- **Necessary preconditions of the original claim:** tuning load is lower; query
  patterns port cleanly; observability and runbooks transfer; on-call engineers
  reach operational fluency within the migration window.
- **Returned `untested belief` rows (to Phase 2):**
  - `untested belief`: new service's tuning frequency is lower than current Postgres
  - `untested belief`: current query patterns port cleanly to the target data model
  - `untested belief`: observability tooling has equivalent coverage post-migration
  - `untested belief`: on-call rotation can reach operational fluency in window

---

## Failure modes

**Inverting only the surface claim instead of its necessary preconditions.**
Flipping "X is good" to "X is bad" and stopping there produces no new information
— the value of inversion is in the *preconditions* the failure form forces into
view. Always carry the inversion through to step 4 of the procedure.

**Treating the inverted claim as the new conclusion rather than a stress test.**
Inversion is diagnostic, not assertive. The inverted form is a thinking device
for surfacing dependencies, not a finding. "The claim is false because I could
invert it" is the same error as "the cause is real because I drew it on a fishbone."

**Confusing inversion with pre-mortem when a plan exists.** If the artifact under
analysis is a plan with timelines and dependencies, claim-level inversion will
miss the implementation-failure modes that [pre-mortem](pre-mortem.md) is
designed to surface. Use the claim-vs-plan decision rule above.

---

## Output contract

The focused inversion output MUST include these four level-2 section headers, verbatim,
as real `##` headings in the response. Strict on the header strings; soft on content.
This structure enables reliable downstream detection.

Required headers:

- `## Inverted Claim`
- `## Failure-Guaranteeing Conditions`
- `## Necessary Preconditions`
- `## Stress-Test Verdict`

---

## Handoff

The unverified preconditions surfaced here enter the 5-phase methodology at
Phase 2 (Challenge Assumptions). Each precondition is recorded as an
`untested belief` — the fourth assumption class in Phase 2's four-type scheme —
because inversion surfaces silent dependencies, not verified facts. Add each
unverified precondition as a row in the Classified Assumptions Table with type
`untested belief`.

Do not route inverted preconditions directly to Phase 3 (Establish Ground Truths).
Promotion happens inside Phase 2's challenge-and-verify operation, not by
skipping it. A precondition is promoted only after evidence confirms it — until
then it stays `untested belief`, and any chain depending on it inherits the D-07 caveat.

For the positive-direction counterpart, pair inversion with
[second-order-thinking](second-order.md): inversion surfaces what must
hold; second-order traces downstream consequences once it does. Inversion
stress-tests claims; [pre-mortem](pre-mortem.md) stress-tests plans.

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
