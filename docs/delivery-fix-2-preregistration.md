# Pre-Registration — Does v2 of the final-message rule deliver the whole deliverable?

**Id:** `delivery-fix-2` · **Registered:** 2026-09-28, before any run under this id.
**Binding:** as [`docs/delivery-fix-preregistration.md`](delivery-fix-preregistration.md) — the
same prompts, passes, transport, capture, cut-off definition and success rule (§2, §4) — except
the fix (§1 here) and the fidelity definition (§2 here).

## 1. The fix — v2, `540eb1bf` on branch `delivery-fix`

v1 failed on two counts (see that document's §6): it relied on the agent sending a *later* message,
which it did not do unprompted, and it scoped the re-send to "the six-section document", which
dropped the process output. v2 replaces v1's paragraph:

> **Your final message is the whole deliverable — never a fragment of it.** Whoever dispatched
> this analysis receives your final message and nothing else: text in any earlier message never
> reaches them. Your reasoning and your output share one budget per message, so a long analysis
> can be cut off by the output limit. **If you are resumed after an output-limit cut ("Output
> token limit hit"), do not continue from where the text broke off.** In that resumed message,
> write everything you were emitting again **from its very first line** — every process-output
> block, all six sections, every table, chain, verdict and confidence line — verbatim, and end
> your turn with it, so that message is the complete deliverable. Condense, summarise and omit
> nothing, and do not re-derive anything: the content is already decided and you are copying it.
> Do the same if you are told the reader received only part of your output: your next message is
> the complete deliverable, from its first line.

## 2. Fidelity, per section

v2's resumed message is itself a full copy, so the first rendering can hold the document twice and
a whole-document word ratio would count it twice. **Whole with fidelity** is therefore judged per
section: every heading, at any level, that the agent wrote in its first rendering — process output
included — must reach the caller with at least **90%** of the most words that heading was ever
written with. `tests/delivery-fix-2/run_fix2.py` implements it; its 7 offline controls pass a
verbatim re-send (also at a demoted heading level) and fail a tail-only delivery, a re-send that
drops process output, and a condensed section. **Replayed before any run, it marks all 7 frozen
cut-off events LOST** — the 6 of the pre-fix `delivery` corpus and v1's `TB-02.r1`.

## 3. Success rule — unchanged

**Operational** if at least 3 cut-off events occur and every one is whole with fidelity; **not
operational** if any is not; **inconclusive** below 3 events in 24 runs. A re-send that is itself
cut off, and any no-cut-off run whose caller lost sections, are reported.

## 4. Outcome and deviation — v2 is not operational

**Deviation, stated:** as with v1, the run was stopped once a cut-off event had decided the
verdict — after 3 of 12 runs (`TB-02.r1`, `TB-02.r2` without a cut-off; `TB-02.r3` with one).

**v2 fixed the structure and failed on fidelity.** On `TB-02.r3` the agent was cut off at 64,000
output tokens with 4,667 words written; resumed, it did exactly what v2 asked — restarted from the
first line, wrote every section including process output, and ended its turn — and the caller
received all 5,731 words. But the overlapping sections came back **shorter**: Ground Truths 751 →
482 words, the classified assumptions table 750 → 612, conclusion C4 483 → 257, and conclusion C5
(349 words), a five-whys chain (278) and one dead end (121) not at all. Fidelity 0.762: **LOST**.

**The finding that matters more than the verdict.** The re-send spent 14,964 output tokens on
5,731 words — it did not re-reason at length — and it still condensed. **A re-sent long document
is regenerated, not copied.** Every instruction-only fix inherits this: v1 and v2 differ in when
and what they re-send, and both lose fidelity because the second writing is a new writing. A
fidelity-preserving fix has to deliver the text the agent already wrote, through a channel that
does not depend on writing it again.
