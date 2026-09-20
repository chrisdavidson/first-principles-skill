---
name: pre-mortem
description: Runs a focused pre-mortem only — prospective-hindsight failure analysis. Invoke via /pre-mortem only.
disable-model-invocation: true
metadata:
  version: "9.4.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/pre-mortem/SKILL.md by sync-content.py -->

# Focused Pre-Mortem Mode

You are running in focused-pre-mortem mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

## When to reach for this

Use a pre-mortem once a plan has enough specificity to reason about particular
failure modes, but before it is finalised and carries organizational momentum.
Not the right tool for evaluating options (use trade-off analysis) or for tracing
something that already went wrong (use 5-Whys).

---

## Framing

Before any other step, adopt this premise explicitly:

> It is approximately six months from now. This plan has failed — not merely
> underperformed, but failed badly. That outcome is a fact.
> Working backward: what caused it?

This past-tense framing is not rhetorical. It bypasses the optimism bias that
makes forward-looking risk lists generic. Do not skip it or soften it to
"might fail" — the grammatical shift from possibility to accomplished fact is
the mechanism.

---

## Procedure

1. **Restate the premise.** Before writing anything, say or write: "The plan has
   already failed. What caused it?" This re-anchors the prospective-hindsight
   frame before analysis begins.

2. **Write independently.** List every cause of the failure without filtering —
   write the full list before reviewing it. Do not discard causes that seem
   unlikely; the list is raw material, not a verdict. Generate from at least
   three named viewpoints — for example the implementer, the person who has to
   live with the result, whoever pays for it, and a competitor who benefits
   from the failure. One generator asked once returns one perspective's
   failures, and the causes it misses are systematically the ones outside the
   frame it was asked in.

3. **Interrogate the list adversarially.** Re-read each item and ask which ones
   contradict the plan's own stated premise, or the recommendation the analysis
   is about to make. A cause that would embarrass the conclusion is higher
   signal than one that merely adds risk to it. In a facilitated session these
   are the items a junior participant suppresses; written by a single analyst
   they are the items that get hedged into vagueness rather than dropped, so
   look for the softened ones, not the missing ones.

4. **Identify recurring patterns.** Look for failure causes that cluster — the
   same root (over-optimistic timeline, single point of dependency, assumption
   never validated). A cluster is a structural weakness in the plan, not an
   isolated risk.

5. **Act on findings.** Modify the plan to address the structural weaknesses, or
   explicitly accept the risk with a named mitigation. A pre-mortem with no
   downstream plan change was box-ticking.

**Exit criterion:** The failure has been stated as having already happened, causes
are written from that stance, causes are clustered into structural weaknesses, and
every cluster has either a named plan change or an explicitly accepted risk with a
named mitigation. A pre-mortem that ends without one of those two outcomes per
cluster is box-ticking, not a finding.

---

## Output contract

The exit criterion above names four things the pre-mortem must produce. This is
what they look like on the page, in this order:

**Premise** — one line, past tense, stating the failure as accomplished fact.
Not "the plan might fail"; the grammatical shift is the mechanism, and a premise
written in the conditional has already lost it.

**Causes** — the unfiltered list, one per line, written before any grouping
appears. The viewpoints from step 2 are visible in it: if every cause is a
technical one, step 2 was run once rather than three times. Writing the clusters
first and back-filling causes into them inverts the procedure and produces the
generic risk list the whole framing exists to avoid.

**Clusters** — the structural weaknesses the causes fall into, each named, and
each naming the causes it absorbs. A cluster is a claim that several causes share
one root; a heading with one cause under it is a cause, not a cluster. When the
pre-mortem runs inside a first-principles analysis, each cluster also cites the
chain ids (`Cn`) or ground-truth ids (`GT-N`) it bears on, so the finding lands
somewhere a reader can check it against.

**Disposition** — per cluster, one of exactly two things: a named plan change, or
an explicitly accepted risk with a named mitigation. "Worth watching", "we should
keep this in mind" and "a risk we accept" with nothing named after it are none of
the above. A cluster whose disposition is an accepted risk still names what makes
the risk survivable; that is what distinguishes accepting a risk from noticing one.

A pre-mortem missing any of the four has not run. A pre-mortem whose causes list
is shorter than its cluster list ran backwards.

---

## Example

**Plan:** Host a dinner party for twelve people in two weeks, cooking a full
three-course meal from scratch for the first time at this scale.

**Framing applied:** It is two weeks from now. The dinner party has failed badly.
What caused it?

**Backward-derived failure causes:**
- Underestimated preparation time; last two courses were served an hour late
- A key ingredient unavailable the day before; no substitution plan
- One course required equipment not owned and not sourced in advance
- Two guests had dietary restrictions not asked about until the day of
- Energy depleted by the time guests arrived; host unable to enjoy the evening

**Pattern identified:** Every cause traces back to a single structural weakness —
no dry run at smaller scale and no contingency check before commitment. The plan
assumed novelty would resolve itself on the day.

---

## Failure modes

**Forward-looking framing.** "What could go wrong?" produces a generic risk list.
If causes feel speculative and mild, the past-tense premise was not adopted.

**Running it too early.** A pre-mortem on a plan with insufficient specificity
yields generic concerns. The plan must have enough detail to reason about
particular failure modes — vague plans produce vague analyses.

**Anchoring (in group settings).** When facilitated, the most senior voice in the
room shapes the list. Run independent writing before any sharing — each
participant writes silently before the group compares lists.

**First-speaker anchoring.** The first cause named draws subsequent thinking
toward it. Write exhaustively before ranking or grouping.

**No follow-through.** A pre-mortem with no downstream plan change was
box-ticking. Findings must modify the plan or be explicitly accepted with
named mitigations.

---

## Handoff

The probable failure causes identified here feed Phase 5 (Validate). Add the
highest-signal structural weaknesses to the adversarial validation pass — each
one is a weak-link candidate for the signed-off analysis to address or explicitly
accept.

## Focused-mode validation

**Check the output against its own completion condition before presenting it.** The
procedure above states one, in whichever form this technique uses — an exit criterion, a
stop test, or an output contract. Read that condition again and confirm the output actually
produced meets every requirement it names, not just the ones that were easiest to satisfy.

**This is a scope-proportionate check, not the six-criterion Self-Audit Gate.** That gate
scores a six-section analysis document; this run produced one technique's output sections,
not six, so walking all six criteria against it would score structure that was never
produced. The larger of the two components: a focused run does not acquire evidence — it
opens no cited source — so a claim resting on a source this run did not open stays marked
rather than being resolved as confirmed.

**Carry the mark forward.** Anything this run could not verify is carried into the output
marked with a `?` rather than dropped or silently asserted as fact.

**Revise once, then stop.** If the check fails, revise the output and check it again.
Revise at most one time. If it still fails after that pass, present the output with the
gap named rather than revising again.

**End every run with a validation line, without exception.** State exactly one of the
following, verbatim, never silently:

- `Focused-mode validation: satisfied`
- `Focused-mode validation: revised once, now satisfied`
- `Focused-mode validation: not satisfied - <reason>`

Close with the reason this line is unconditional: a silent run is indistinguishable from a
run that skipped the check.

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as candidate inputs for Phase 2. Carry the `?` marks
with it — this run opened no cited source.
