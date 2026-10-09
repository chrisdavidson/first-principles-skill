# Protocol — Re-running the worked examples on the current agent (example-rerun-2)

**Id:** `example-rerun-2` · **Registered:** 2026-10-08, before any run under this id.
**Predecessor:** [`example-rerun`](example-rerun-protocol.md) (v9.13.0, read in
[`example-rerun-reading.md`](example-rerun-reading.md)).

## 1. What is compared

Each of the 14 worked examples in `shared/examples/` is re-run once on the agent at commit
`2628e725` (v9.19.1 plus 24 commits; 51 commits to `shared/spine/` and `shared/agent/` since v9.13.0, including the
structured summary block, section-3 provenance roll-up and pre-check lines), and the re-run is
compared with the committed example **and** with the v9.13.0 re-run of the same prompt.

The question is the one the goal sets: **does anything in the shipped examples need updating**
in light of what the current agent produces on the same problems? A difference is a candidate
update only when it is a substantive point — a missed consideration, an error, a stale
convention the agent no longer emits — that survives checking against both documents. Length,
hedging and format differences that reflect curation, not reasoning, are not candidates.

As in the predecessor, a committed example is a curated document and a re-run is one live
generation; this compares the two, it does not measure whether the agent got better.

## 2. Prompts — `tests/example-rerun-2/prompts.json`

Identical to `tests/example-rerun/prompts.json` with one deliberate change:
`composed-inversion-second-order` uses the **full-context** prompt the predecessor's
supplementary run used, because the reading found the one-sentence prompt omitted context the
example's scenario states. No prompt names a technique.

## 3. Transport

As the predecessor, unchanged: the same `claude -p` invocation and model pin
(`tests/delivery/run_delivery.py`), empty working directory, persistence on, the agent's own
transcript kept, routing misses retried at most twice, one run per example, sequential.

One change, to remove the predecessor's `self-application` contamination: the plugin body is a
`git archive` export of `first-principles/` at `2628e725` into a scratch directory **outside
the repository**, so the agent's reference paths cannot lead it back to `shared/examples/`.
Whether any re-run read a worked example is checked in its transcript, not assumed.

## 4. Readings

**Mechanical** — `tests/example-rerun-2/run_examples.py compare`, the predecessor's instrument
unchanged.

**Qualitative** — one judge per example, given the committed example, this re-run and the
v9.13.0 re-run: same recommendation; what the re-run catches that the example misses; what it
gets wrong. A judgement, not a measurement, reported and attributed, never tallied. Every
candidate update is checked against the documents by the main session before it is reported.

## 5. What this cannot establish

One run per example. Correctness in general — conformance does not predict it
(`docs/v8.7-correctness-spot-check.md`). A recorded reading, never a gate.
