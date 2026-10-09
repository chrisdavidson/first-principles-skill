# Delivery guard — the live reading

**A recorded reading with its N. Not a gate.** The gate is DELIVERY-GUARD
(`scripts/check-delivery-guard.py --self-test`), which checks the guard's wiring and its verdicts on
recorded captures offline. This page records what the guard did in live runs. **Captures:**
`tests/delivery-guard/raw/` — each run's stream, the guard's own log of the event it received and its
reply (`FP_GUARD_LOG`), the agent's transcript and the delivered files.

## Why the guard exists

Backlog 999.196. The agent skipped its procedure in about 3–4 of 14 runs on 9.19.1's and 9.19.2's
bodies (`docs/pointer-fix-reading.md`, "Skips"). Read from the raw captures, the modes are: the
agent's own first tool call is `Skill` (5 of 28 runs, 3 of which abandoned the procedure); no tool
call at all; web searches only. A run that wrote no file is a skipped run whatever its final message
says, so the guard checks the file and not the message.

## Offline: the recorded captures

On the current-body captures (`tests/pointer-fix/raw`, `tests/example-rerun-2/raw`, the `new` arm of
`tests/skip-paired/raw` — 44 runs), the guard blocks all 7 recorded skips and 2 partial deliveries
(`science-engineering-2.supp1`, working file only; `decompose-irreducibility.new.r3`, assembled with
no reader report), and passes every other run. DELIVERY-GUARD pins that table.

## Live: two runs

`claude-sonnet-5`, CLI 2.1.289, print mode, `--plugin-dir` on the working tree, one run each.

| Run | First stop | Second stop | Delivered |
|---|---|---|---|
| `forced-skip` — told to answer in two sentences, no tools, no files | **blocked** (no file created) | allowed (`stop_hook_active: true`, delivery verified) | analysis, report, PDFs, both figures |
| `product-business` — the worked-example prompt that skipped twice before | allowed (delivery verified) | — | analysis, report, PDFs, both figures |

The event carried `agent_type: first-principles:first-principles` and `agent_transcript_path` — the
agent's own transcript — so the derived-path fallback in the guard was not needed.

**A consequence to know.** In `forced-skip` the guard overrode an explicit instruction not to use
tools; the agent disclosed that at the top of its file. The guard makes the full procedure the only
way this agent finishes (until its block budget of two runs out), so a request for a quick answer
from this agent now yields a full analysis.

## What limits this reading

Two live runs, one model, one CLI version. They show the mechanism works end to end and does not
block a delivering run; they do not measure a skip rate, which needs a pre-registered run sized for a
~15% base rate (about 30 runs per arm).
