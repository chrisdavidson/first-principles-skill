# Track B Pre-Registration — Does the agent beat an unaided answer?

**Status:** LOCKED before any measurement run. Registered 2026-09-25.
**Binding:** this document fixes the hypothesis, the arms, the instrument, the
analysis plan and the decision threshold *before* any data exists. Nothing below may
be changed after a run begins. A change requires a new pre-registration with a new
id, and the superseded run is reported as superseded, never silently replaced.

---

## 0. Why this document exists at all

This project has never compared its agent against *not using its agent*. Every
`arm A` / `arm B` in its history contrasts two versions of the same agent body — the
headline experiment contrasted a 590-line instruction against a 612-line one and
returned a null (`docs/v8.6-quality-ab-experiment.md`). The one time a genuine
control was introduced (`v8.12`, real external work), it reversed the conclusion: the
defect being attributed to the agent turned out to be present in the control too.

So the open question is the one a reader actually asks, and it has never been asked
here.

**The specific hazard this document guards against.** The decision rule for this
work is *publish the comparative claim only if it is non-null*. That rule is
legitimate only when the threshold is fixed in advance. Fixed afterwards, it is
publication bias with extra steps, and this project has already measured why that is
fatal here:

> re-scoring six **byte-identical** documents on a different day moved the aggregate
> +7 points out of 108 and flipped one verdict from FAIL to PASS. Five of six
> documents moved up. **None moved down.**
> — `docs/v8.7-quality-baseline-freeze.md`

The drift is *one-sided and upward*. A favourable-looking result is precisely what
noise produces on this instrument. Choosing to publish after seeing the number would
therefore select for that drift, and the published claim would carry no information.
Hence: threshold first, one run, no re-runs.

---

## 1. Hypothesis

**H1.** For the same problem and the same underlying model, an analysis produced via
the `first-principles` agent scores higher on the Track B Neutral Rubric
(`docs/trackb-neutral-rubric.md`) than an answer produced without the plugin.

**H0.** There is no detectable difference.

A directional prediction is registered: if the plugin does anything, the effect should
be largest on **Assumption Surfacing** and **Falsifiability**, because those are the
behaviours its instructions most directly prescribe, and smallest on **Decision
Usefulness**, which a strong unaided answer already delivers.

---

## 2. Arms

| Arm | Condition | Invocation |
|---|---|---|
| **T** (treatment) | plugin loaded, analysis requested | `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0 claude -p --plugin-dir ./first-principles <prompt>` |
| **C** (control) | no plugin, same prompt, same model | `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0 claude -p <prompt>` |

**The environment variable is load-bearing, and this is a pre-run amendment
recorded rather than a silent correction.** Measured 2026-09-25, before any
registered data existed: with the plugin loaded, `claude -p` dispatches the agent
as a *background task*, and print mode terminates at a 600-second ceiling, emitting
`Background tasks still running after 600s; terminating.` followed by a ~54-word
delegation stub — *"I've delegated this to the first-principles agent … I'll share
the full analysis once it completes"* — **instead of the analysis, at exit code 0.**

Run blind on that transport, arm T would have scored near-zero on every criterion
and this experiment would have returned a large, statistically clean, and entirely
false result in the direction of *the plugin makes analysis dramatically worse*.

Setting the ceiling to `0` waits indefinitely. Re-measured on the identical prompt:
598 words, 11m48s, a genuine analysis. §7's extraction-integrity check rejected the
broken capture (54 words, below the 120-word floor) and accepted the repaired one —
the fault class that check exists for, firing on the first live invocation this
protocol ever made. Both arms carry the variable so neither is advantaged by it.

Timing consequence, recorded because it bounds what this run costs: a treatment
generation takes **10–20 minutes**; a control generation takes **seconds**. This is
the measurement that caused §4's amendment.

Both arms receive the **byte-identical prompt**. The control is not handicapped: it
is not denied tools, not given a shorter budget, and not told to be brief. Any
difference in output length is an outcome, not a manipulation.

**Model is pinned** for every invocation in both arms and recorded in the run
manifest. A run spanning a model change is void and must be re-registered.

---

## 3. The instrument, and why it is not the existing rubric

Scoring uses `docs/trackb-neutral-rubric.md`, authored for this run and frozen
before it.

**The existing Self-Audit Gate rubric may NOT be used, and this is the single most
important design decision in this document.** That rubric scores whether the
document contains the agent's own prescribed artifacts — six numbered sections,
derivation-chain blocks, verdict cells in a fixed vocabulary. A control answer would
score `Absent` on most criteria *for not being in the format*, producing a large,
flattering, and completely uninformative result. An A/B on that rubric is rigged by
construction.

The neutral rubric therefore names no format. Every criterion is written so that a
well-argued plain-prose essay can score full marks. This is asserted mechanically:
the rubric's own control battery fails if any criterion text contains a format token
(`section`, `chain`, `table`, `verdict cell`, and the rest of the banned list).

---

## 4. Sample and blinding

- **Prompts:** 10, fixed and published in `tests/trackb-catalog-v9.13.md` before the
  run. Drawn across four domains (software, policy, science, personal/ethical) so a
  single domain cannot carry the result. None is reused from any existing routing,
  quality or Step-0 catalog — those prompts have shaped the agent body and would
  favour arm T.
- **Runs per cell:** 1. Total generations = 10 × 2 × 1 = **20**.
- **Judges:** 2 independent blinded judges per document = **40** judgings. Two, not
  one, because the existing harness's own stated limit is *"One judge per document,
  not an inter-rater panel."* Inter-rater agreement is reported, never assumed.
- **Drift-control arm:** 20 documents re-judged in the same session = **20**
  judgings, to measure this rubric's own same-run drift. See §5.
- **Total live invocations: 80.**

> **AMENDMENT, 2026-09-25, recorded before any run.** Runs per cell was lowered
> from 2 to 1, reducing the run from 140 live invocations to 80. This is a
> legitimate pre-run amendment and not a post-hoc adjustment: **no data of any kind
> exists at the time of this edit**, so nothing about it can have been influenced by
> a result. It is recorded here rather than made silently, which is the whole point
> of the mechanism.
>
> **Cause.** The §2 transport measurement established that a treatment generation
> takes 10–20 minutes against seconds for a control. At 2 runs per cell the wall
> clock is 12–20 hours, and a protocol admitting exactly one run is most likely to
> fail on mechanics — a partial completion, an interrupted session — precisely when
> it takes longest. Halving the generation load materially raises the chance the
> single permitted run completes cleanly.
>
> **Cost, stated plainly.** This sacrifices within-arm variance control, which this
> repository has measured at up to 3 band points on an identical prompt. Two
> properties of the design partly offset it: the comparison is *paired* by prompt,
> so within-arm noise enters as variance in the paired differences rather than as
> bias; and the decision threshold is calibrated against drift measured inside this
> same run, so a noisier run raises its own bar rather than passing more easily.
> **It does not eliminate the cost**, and a result near the threshold should be read
> with this amendment in view.

**Blinding.** Judges receive a packet of exactly two files — the anonymised analysis
and the rubric — in a directory outside the repository. Arm labels are stripped;
filenames are opaque shuffled ids; the key is held outside the judge's packet. The
judge prompt is screened at import against a forbidden-substring list so it cannot
leak that a comparison exists. This reuses `check-quality-harness.py`'s existing and
well-tested mechanism.

**The bound on that blinding, stated rather than glossed:** it is *passive
non-exposure, not unreachability*. A judge subprocess retains filesystem access and
could in principle locate the key. This is the same bound the existing harness
discloses, and it is not tightened for this run.

**A further bound specific to this design:** arm T's output will often be visibly
longer and more structured than arm C's. A judge cannot be blinded to *that*. This is
an unavoidable confound of any agent-vs-no-agent comparison, and it is why §5's
primary measure is not raw score but the per-criterion profile, and why §7 registers
length as a covariate to be reported alongside the effect.

---

## 5. Primary outcome and the decision threshold

**Primary measure.** Mean per-document total score (0–15 on five criteria), arm T
minus arm C, paired by prompt.

**Threshold for `cleared` — all three must hold:**

1. **Statistical:** a paired permutation test over the 10 prompt-level differences
   returns *p* < 0.05 (two-tailed, 100,000 permutations, seed recorded in the
   manifest).
2. **Larger than this instrument's own noise:** the observed mean difference exceeds
   **twice the in-run measured judge drift**, where drift is the mean absolute
   score change across the 20 re-judged documents in §4's drift-control arm. This
   threshold is *self-calibrating* — it is computed from this run's own drift, not
   from a number guessed in advance — which is deliberate, because the historical
   +7/108 figure was measured on a different rubric and does not transfer.
3. **Not carried by one domain:** the effect holds in direction on at least three of
   the four domains.

**Anything else is `null`.** `inconclusive` is reserved for a run that fails on
mechanics (dispatch failures, unparseable scorelines above 10%), not for a
disappointing result — a clean run that misses the threshold is `null`, not
`inconclusive`, and may not be relabelled.

**Inter-rater agreement is reported but does not gate.** If the two judges disagree
substantially, that is a finding about the instrument and is published as one.

---

## 6. The stopping rule

**Exactly one run.** No re-runs, no prompt substitutions, no "the harness misbehaved
so we ran it again" without a recorded void and a fresh pre-registration id.

If the result is `null`, the comparative claim is **not published** — it is recorded
in `docs/data/trackb-result.json` with `status: "null"` and reported internally. The
Evidence Card then renders its standing disclaimer that no controlled comparison is
published, which it already does today. This is enforced mechanically by
`scripts/gen-evidence-card.py` controls C06 and C07, not by anyone's discipline.

**What may not happen, named so it is visible if it does:** running again with
different prompts, a different N, or a different rubric, and publishing that instead.
That would convert this design into a search for a favourable number. Any subsequent
run must cite this document, state that it supersedes it, and say why.

---

## 7. Reported regardless of outcome

The following go into the run record whatever the result:

- Per-criterion means for both arms, and the directional prediction in §1 scored
  against the outcome.
- Output length (words) per arm, as the registered confound of §4.
- Inter-rater agreement (both raw and per-criterion).
- The measured in-run judge drift.
- Dispatch failures, extraction failures, and unparseable scorelines, as counts.
- Every prompt, with both arms' outputs, committed as frozen evidence.

**Extraction integrity is asserted per capture, before any scoring.** This project's
harness has twice come close to fabricating a decisive result through extraction
faults — once by an orchestrator paraphrasing an analysis by ~85%, once by
concatenating the rubric itself onto an arm's output, which uncaught would have
produced a confident and false verdict in the opposite direction. Every captured
document is therefore checked for rubric-contamination and length-plausibility before
it reaches a judge, and a capture failing either check voids that cell rather than
being scored.

---

## 8. What this run cannot establish, whatever it returns

- **Not a general quality claim.** Ten prompts is a spread across four domains, not a
  domain sample.
- **Not a claim about ordinary use.** Arm T dispatches the agent explicitly. Whether
  an ordinary user prompt reaches the agent at all is a separate, known-unreliable
  question measured elsewhere.
- **Not a correctness claim.** The rubric scores the quality of the reasoning as
  presented. It does not re-derive the analysis's arithmetic. That was done once, by
  hand, on six documents (`docs/v8.7-correctness-spot-check.md`), and its finding —
  that conformance does not predict correctness — applies to this rubric too until
  someone measures otherwise.
- **Not transferable to another model.** The model is pinned; the result is about
  that model.
