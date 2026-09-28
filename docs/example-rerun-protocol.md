# Protocol — Re-running the worked examples on v9.13.0

**Id:** `example-rerun` · **Registered:** 2026-09-28, before any run under this id.

## 1. What is compared

Each of the 14 worked examples in `shared/examples/` is re-run once on the **v9.13.0** agent
(tag `v9.13.0`), and the re-run is compared with the committed example.

**These are not two versions of the same thing.** A committed example is a curated document,
authored and revised across many phases, often by hand; a re-run is one live generation. A
difference therefore mixes what the agent does today with what curation added. This comparison
answers "how does what v9.13.0 produces on each example's problem compare with the example we
ship", not "did the agent get better".

## 2. Prompts — `tests/example-rerun/prompts.json`

Each prompt carries the problem and the user-supplied facts the committed example started from —
its stated scenario, claim or target, and, where an example stated no scenario, the ground truths
that are facts about the user's situation rather than findings. **No prompt names a technique:**
a technique name switches the agent into a focused mode whose output is a different document,
and every example is a full six-section analysis. `self-application` asks about this repository's
own agent file; its re-run starts in an empty directory and can see none of it.

## 3. Transport

As `delivery-fix-4`: empty working directory, session persistence on, the agent's own transcript
kept, routing misses retried at most twice, one run per example, sequential. The re-run's
document is **the file the agent delivered** (v9.13.0's file handoff), or its final message if it
wrote none.

## 4. Readings

**Mechanical — `tests/example-rerun/run_examples.py compare`,** applied identically to both
documents: words; contract sections; distinct ground-truth ids and unverified ones; chains;
abandoned paths; source URLs; the Conclusion's confidence band; and the defect detector's counts
— untraced conclusion claims, malformed chain blocks, nonconforming verdict cells, confidence
inversions. On a defect count, **lower is better**; the others are descriptive.

**Qualitative — one judge per example,** given both documents: does the re-run reach the same
recommendation; what does it do better; what does it get wrong or omit that the example has.
**This reading is a judgement, not a measurement:** this repository has measured a model judge
disagreeing with itself on byte-identical input (`CHAIN-JUDGE`, 7 of 13). It is reported as
qualitative commentary, attributed to the judge, and never tallied into a score.

## 5. What this cannot establish

One run per example. Correctness — `docs/v8.7-correctness-spot-check.md` measured that
conformance does not predict it. A recorded reading, never a gate.
