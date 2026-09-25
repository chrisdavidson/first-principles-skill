---
name: validate
description: Slash-only Phase 5 stub — stress-test each derivation chain for weak links.
disable-model-invocation: true
metadata:
  version: "9.12.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/validate/SKILL.md by sync-content.py -->

# Focused Validate Mode

You are running in focused-validate mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

## When to reach for this

Use this phase once the Derivation Chains artifact from Phase 4 is complete — all
conclusions have chains and the core question is answered. Completing a derivation chain
does not guarantee the chain is sound. A chain built on an unverified assumption that is
load-bearing, or one whose weakest link is never examined, produces a conclusion that
looks rigorous but collapses under scrutiny. Validation is the adversarial pass that
exists to find the flaws forward-direction reasoning was not looking for.

---

## Procedure

Stress-test the analysis in five steps, in this order; each step's output is a part of the
adversarial pass record below, and a step with nothing to act on writes its own
not-applicable line naming the reason instead of being skipped.

**Recompute.** Redo every computed figure in the chains independently of the chain text,
and trace each chain back to its named ground truths to check that every link holds; a
figure that does not recompute is a hop that does not follow. Not-applicable line:
`recompute not applicable — [reason]`.

**Sensitivity.** Name the single ground truth whose falsity would flip the conclusion, and
whether it is `?`-marked; if it is, either verify it now or apply a confidence caveat — no
new cap. This is also where the weakest link in each chain is identified — the step most
dependent on an assumption not fully verified, or where the inferential gap is largest —
named per chain. Not-applicable line: `sensitivity not applicable — [reason]`.

**Rival.** State the strongest rival conclusion the same ground truths would support, and
what rules it out — **for the headline conclusion and for every intermediate chain the
conclusion rests on.** A rival is not only an alternative answer to the question asked; it is
an alternative reading of any step the answer depends on, and a chain whose endpoint nothing
competes with is a chain whose Rivals axis was never exercised rather than one that survived
it. Where an intermediate chain has no live rival, say so on that chain — `rival not
applicable — [reason]` is a result, and silence is not. A ruled-out rival becomes an Abandoned Reasoning entry, using the
What-was-tried / Why-abandoned / What-it-ruled-out structure and naming the `GT-N` or `Cn`
that ruled it out, and the record's Rival part points at that entry; a rival nothing rules
out stays live and is named on the affected `**Confidence:**` line as the short Rivals
axis. Not-applicable line: `rival not applicable — [reason]`.

**Adversarial technique.** Weakest-link inspection by the analysis that wrote the chains is
not by itself adversarial — it looks where the forward reasoning was already looking, and
finds what that reasoning already suspected. Apply a structured adversarial technique to
the conclusion, chosen by what the conclusion is. When it is a **plan or recommendation**,
open the [Pre-Mortem procedure](${CLAUDE_PLUGIN_ROOT}/skills/pre-mortem/SKILL.md) with Read and apply it to that plan. When it
is a **claim**, open the [Inversion procedure](${CLAUDE_PLUGIN_ROOT}/skills/inversion/SKILL.md) with Read and apply it to the
headline conclusion. (Decision rule: inversion stress-tests a claim; pre-mortem
stress-tests a plan.) The procedure is opened, not recalled: a pre-mortem run from
recollection reliably drops the past-tense framing that is the technique's whole mechanism,
and what it produces instead is a forward-looking risk list.

Each structural weakness the pass returns becomes a named weak link on the chain it bears
on, or an explicit confidence caveat on the conclusion it threatens. A weakness that
becomes neither has not been acted on, and the pass that produced it was box-ticking. When
the conclusion is neither a plan nor a claim — a decomposition, a description, an answer
with nothing to commit to and nothing to assert — record the single line `adversarial pass
not applicable — [reason]` and proceed. That line is honest depth, not an opt-out: it names
the reason, and an analysis carrying a plan or claim cannot write it. It waives only this
step's Premise, Causes, Clusters and Disposition parts; the Recompute, Sensitivity, Rival
and Falsification parts each still carry content or their own not-applicable line.

**Falsification.** State the condition under which the conclusion is false — "the
conclusion is false if [observation]" — in the record only. Not-applicable line:
`falsification not applicable — [reason]`.

The criteria in the Self-Audit Gate rubric are not applied at this step — that document
defines the criteria, levels, and scoring, and it scores the analysis's own structure, not
the subject matter. Do not re-author the criteria here, and do not apply them from
recollection: the rubric is opened once, and its criteria applied once, at the Self-Audit
Gate, immediately after that read.

**Adversarial pass record:** Emit the pass as process output under the single top-level
heading `## Adversarial pass (process output)`. The steps above write the record as they
run, each contributing the bold lead-in part below, in this order; a part is its step's
not-applicable line where that step had nothing to act on. **Recompute** — each computed
figure with its recomputed value. **Sensitivity** — the flip ground truth and whether it is
`?`-marked. **Rival** — the rival named and a pointer to its Abandoned Reasoning entry or
to the `**Confidence:**` line carrying it live. **Premise** — one line, stated in the past
tense the technique requires: the plan has already failed, or the headline conclusion is
already false. **Causes** — the unfiltered list, written before any grouping and not
filtered for plausibility while being written; generate causes from the viewpoint of at
least three named stakeholders, because one generator asked once returns one perspective's
failures. **Clusters** — the structural weaknesses those causes fall into, each named, and
each citing the chain ids (`Cn`) or ground-truth ids (`GT-N`) it bears on. **Disposition** —
per cluster, a named plan change, or an explicitly accepted risk with a named mitigation. A
cluster carrying neither is box-ticking, and the exit criterion below does not admit it.
**Falsification** — the condition under which the conclusion is false.

**Named artifact:** Signed-off analysis — the complete output document with all sections
present, all conclusions traced to named ground truths, and all weak links either resolved
or explicitly flagged with confidence caveats.

**Exit criterion:** ALL THREE conditions must hold: (1) every conclusion traces to a named
ground truth via a complete derivation chain, AND (2) every weak link is either resolved
(the assumption has been verified or reclassified) or explicitly flagged with a confidence
caveat that a reader can evaluate, AND (3) the five steps have run and the record is
present with every part — each carrying its content or its step's not-applicable line —
every cluster carrying a named plan change or an explicitly accepted risk with a named
mitigation. A silently omitted step, or a record whose clusters carry no disposition, does
not satisfy this criterion and does not exit this phase. A skeptic inspecting the
signed-off analysis can verify all three conditions hold without asking the analyst for
clarification.

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

**Run the technique's own semantic check before declaring the output satisfied.** The
completion condition above is structural — it asks whether the required parts are present.
This asks whether the content holds up. One question, per technique:

- **five-whys** — is each cause counterfactually necessary: would the symptom still have
  happened without it?
- **fishbone** — does each prioritised cause carry an observation that distinguishes it
  from its siblings?
- **inversion** — is each precondition stated as a claim that can be false, and tagged for
  whether the conclusion survives it being false?
- **estimate** — does the bracket's whole width drive the same decision? If the low and
  high ends point different ways, the bracket has not yet answered the question.
- **trade-off** — does the winner survive the smallest weight flip, and is the status quo
  among the options?
- **pre-mortem** — does every fatal or costly cluster carry a tripwire that someone is
  positioned to see?
- **second-order** — has any effect been checked against what the decision is *for*, not
  only against what is true?
- **theoretical-limit** — is the bound the tightest applicable one, and is the demonstrated
  tier an observed figure rather than a calculated one?

A failed semantic check is a `not satisfied` result, not a caveat to attach to a satisfied
one.

**Escalate to the full composer when a `?` becomes load-bearing.** If a claim this run could
not verify turns out to be one the answer does not survive being false — load-bearing in the
validation rubric's sense — stop and say so, in this form:

- `Focused-mode escalation: <the ?-marked claim> is load-bearing - recommend a full analysis`

A focused run acquires no evidence, so it cannot resolve that claim; continuing produces a
confident-looking answer resting on exactly the thing nobody checked. Escalation is the
honest exit, and it is the only case where a focused run should decline to answer in its own
terms. Recommend the escalation; do not silently perform a full analysis instead — the run
was asked for one technique.

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

**Then state the residual, on its own line, every time — including after `satisfied`.**
Verbatim:

- `Focused-mode residual: this run opened no cited source, so any ?-marked claim is unverified, not merely uncited.`

This is the one thing the reader of a focused run cannot infer from the output. The
completion-condition check above is a rule *this document* gives the model; the residual is a
fact about the run that its reader needs, and until it is emitted the reader has no way to
tell a focused analysis from a full one that happened to be short. `satisfied` means the
output met its completion condition — never that its claims were verified against a source.

---

If a fuller analysis is needed afterward, invoke the main
`first-principles` agent with this output as the Phase 5 verdict to act on
— a Criterion 1 Absent verdict returns to Phase 1 to re-frame the Essence
Statement, any other Absent verdict is fixed in place under the Self-Audit
Gate's Fix/Repeat loop, and each unresolved weak link is carried with the
confidence caveat it was flagged with. Carry the `?` marks with it — this
run opened no cited source.
