# emission-phase1 Stage A — captures

**Run id:** `emission-stage-a-v9.14` · **Model:** `claude-sonnet-5` (pinned)
**Protocol:** [`docs/emission-phase1-preregistration.md`](../../docs/emission-phase1-preregistration.md)
**Findings:** [`docs/emission-phase1-stage-a-findings.md`](../../docs/emission-phase1-stage-a-findings.md)
**Why this run exists:** [`docs/trackb-transport-erratum.md`](../../docs/trackb-transport-erratum.md)

---

## What this is

The first captures in this project of the `first-principles` agent's **own analysis document**.

Every prior capture of "the agent" — including all ten arm-T generations in
`tests/trackb-run-v9.13/` — recorded `claude -p` stdout, which under `--plugin-dir` is the
main session's *summary* of the agent's document, not the document. Every arm-T reading in
that run therefore describes a summary. The erratum above carries the finding and its
falsifiers.

Here the capture is the assistant message carrying a non-empty `parent_tool_use_id` — the
subagent's own emission — extracted from a `--output-format stream-json --verbose`
transcript.

## Contents

| Path | What it holds |
|---|---|
| `raw/TB-NN.jsonl` | the full stream-json transcript, as emitted |
| `documents/TB-NN.md` | the agent's document, extracted from that transcript |
| `documents/TB-NN.orchestrator.md` | the main session's summary of the same document, same invocation |
| `stage-a-result.json` | the mechanical readings and the pre-registered prediction tally |

Keeping both layers of each invocation is deliberate: it makes the transport defect measurable
*within* a single run, with no cross-run variation to argue about.

## Provenance note on `TB-04`

`raw/TB-04.jsonl` was captured by the 2026-09-26 transport probe that established the finding,
before the registered ten-prompt run began, and was seeded into this directory rather than
re-spent. It uses the identical transport, model and prompt. It is the specimen the pivot
evaluation's own objection rested on, which is why it was probed first.

## Reading it

```sh
python3 scripts/check-emission-stage-a.py read --out-dir tests/emission-stage-a-v9.14
```

The derivation detector these readings use has a **measured document-level sensitivity of 1 in
2** on the only corpus where it has been hand-audited (pre-registration §6). Derivation counts
here are floors, not measurements, and no decision in the protocol turns on them alone.
