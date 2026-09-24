# Validate

> The adversarial pass — stress-test the derivation chains to find flaws that
> forward-direction reasoning was not looking for.

---

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
what rules it out. A ruled-out rival becomes an Abandoned Reasoning entry, using the
What-was-tried / Why-abandoned / What-it-ruled-out structure and naming the `GT-N` or `Cn`
that ruled it out, and the record's Rival part points at that entry; a rival nothing rules
out stays live and is named on the affected `**Confidence:**` line as the short Rivals
axis. Not-applicable line: `rival not applicable — [reason]`.

**Adversarial technique.** Weakest-link inspection by the analysis that wrote the chains is
not by itself adversarial — it looks where the forward reasoning was already looking, and
finds what that reasoning already suspected. Apply a structured adversarial technique to
the conclusion, chosen by what the conclusion is. When it is a **plan or recommendation**,
open the [Pre-Mortem procedure](pre-mortem.md) with Read and apply it to that plan. When it
is a **claim**, open the [Inversion procedure](inversion.md) with Read and apply it to the
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
