# v8.7 Quality Harness — D-22 Live Transport Probe

**Generated:** 2026-07-22. **Status:** FROZEN read-only evidence — never regenerated, never
hand-edited to match a later result. `probe-P1.jsonl` is the raw capture; this file is the
census-backed shape record D-22 requires to exist and be committed **before** any extraction
code is written. Committed in the same commit; the extraction code that reads the channel
named below is added in a later commit (`git log --oneline -- tests/quality-probe-v8.7` is an
ancestor of the commit adding `extract_agent_analysis`).

## Command and environment

```bash
mkdir -p /tmp/qh-probe
python3 scripts/check-quality-harness.py --probe Q-P1 \
    --catalog tests/quality-catalog-v8.7.md --out /tmp/qh-probe
```

This is the exact Plan-36-locked argv `_run_prompt_to` issues under the hood for this flag-set:

```text
claude -p --plugin-dir <repo>/first-principles --no-session-persistence \
  --output-format stream-json --verbose --permission-mode bypassPermissions \
  "<_wrap_for_bypass(Q-P1 prompt text)>"
```

| | |
|---|---|
| Date | 2026-07-22 |
| `claude` CLI version | 2.1.217 (Claude Code) |
| Plugin version | `first-principles@8.6.0` (inline source) |
| Model | `claude-opus-4-8[1m]` |
| Prompt | Catalog row `Q-P1` (REST/JSON→gRPC migration decision) |
| Capture size | 78,597 bytes, 16 JSONL lines |
| Run duration | 169,541 ms (`result.duration_ms`) |
| Terminal event | `{"type":"result","subtype":"success","is_error":false,"api_error_status":null,...}` — a genuine completed run, not an error stub |

## Per-event-type census (16 lines)

| `type`/`subtype` | Count |
|---|---|
| `system`/`hook_started` | 2 |
| `system`/`hook_response` | 2 |
| `system`/`init` | 1 |
| `assistant` | 3 |
| `system`/`task_started` | 1 |
| `user` | 2 |
| `rate_limit_event` | 2 |
| `system`/`task_updated` | 1 |
| `system`/`task_notification` | 1 |
| `result`/`success` | 1 |

Agent dispatches of `first-principles:first-principles`: **exactly 1** — the single `assistant`
`tool_use` block `name: "Agent"`, `id: toolu_01837DVU3u6JW2QdJvCoxSKC`,
`input.subagent_type: "first-principles:first-principles"`.

Unrelated `tool_result` events produced by the subagent's own internal tool calls: **0** (this
run's `task_notification.usage.tool_uses` is `0` — the subagent made no internal tool calls, so
there is nothing to distinguish from the dispatch's own result in this particular capture).

## The channel that carries the verbatim analysis

**Primary: `system`/`task_notification`, field `summary`, matched by `tool_use_id` against the
Agent dispatch's `tool_use.id`.**

- `task_notification.tool_use_id` == `toolu_01837DVU3u6JW2QdJvCoxSKC` (matches the dispatch)
- `task_notification.status` == `"completed"`
- `task_notification.summary` length: **17,717 characters**
- Contains all six output-contract sections in order: `## 1. Problem Essence` .. `## 2.
  Assumptions Table` .. `## 3. Ground Truths` .. `## 4. Derivation Chains` .. `## 5. Abandoned
  Reasoning` .. `## 6. Conclusion`
- Carries **no** trailing transport-metadata tail — the field ends with the analysis's own last
  sentence.
- `task_notification.usage` (separate from the field content): `{"total_tokens": 52140,
  "tool_uses": 0, "duration_ms": 149007}`.

## What the matching `tool_result` actually contained

The `user`/`tool_result` block whose `tool_use_id` matches the same dispatch ID is **not** a short
launch-acknowledgement stub in this capture — it contains the same analysis, **plus a trailing
transport-metadata tail**:

- Length: **17,914 characters** (197 more than `task_notification.summary`)
- `tool_result` text is confirmed **byte-identical to `task_notification.summary` for its first
  17,717 characters** (`tool_result_text.startswith(summary)` is `True`, verified directly against
  the raw capture, not inferred)
- The trailing 197-character tail, quoted in full:
  ```text
  agentId: ab69e34256a1365ec (use SendMessage with to: 'ab69e34256a1365ec', summary: '<5-10 word recap>' to continue this agent)
  <usage>subagent_tokens: 63102
  tool_uses: 0
  duration_ms: 149010</usage>
  ```

This is the opposite of what the archived async-task evidence predicted: **37 other committed
`.jsonl` captures under `tests/step0-captures-v*/` show this same matching `tool_result` as a
~200-character `"Async agent launched successfully…"` acknowledgement stub, not the full
analysis.** This one probe run did not reproduce that stub shape — the `tool_result` here carried
the complete text instead, with a metadata tail appended. Literal occurrences of the string
`"Async agent launched"` anywhere in this capture: **0**.

**Consequence:** the `tool_result` channel is unreliable in *both* directions across this
project's own evidence — sometimes a ~200-char stub, sometimes the full text plus a tail — and
must not be the primary extraction channel. `task_notification.summary` is the channel actually
observed to carry the clean, tail-free verbatim text in every committed capture checked,
including this one, so it is the primary channel; the tail-stripped `tool_result` is retained only
as a cross-check, never as the source of record.

## The top-level `result` field (confirmed NOT the analysis)

- Length: **2,993 characters** — **16.7%** of the `tool_result` payload (2,993 / 17,914), in the
  same range as the ~15% ratio measured on the original v8.6 A/B experiment's synchronous-channel
  captures (`tests/quality-baseline-v8.7/README.md`: 2,454 / 16,866 = 14.6%).
- It literally opens: *"The agent ran and returned a full-composer analysis. Its output, verbatim
  in substance:"* — and then paraphrases. The claim of being "verbatim in substance" at 16.7% of
  the source length is false on its face; this is the orchestrator-summary substitution Guardrail
  A exists to prevent, and this capture proves it decisively: the field asserts fidelity it does
  not have.

## Additional observation not predicted by prior research: no full-length "interleaved assistant text" channel exists in this capture

`164-RESEARCH.md`'s Pattern 1 (drawn from `tests/step0-captures-v7.13/-v8.5/-v8.6` samples
produced by a *different* call site, `check-step0-live.py`'s classification-excerpt harness)
describes the verbatim analysis as also appearing "interleaved later in the stream as ordinary
`assistant`/`text` content blocks," byte-identical to `task_notification.summary`. **This probe's
own three `assistant` events do not exhibit that channel:**

1. A 38-character orchestrator transition ("I'll pass the prompt through verbatim.")
2. The `Agent` tool_use dispatch itself
3. A 2,993-character `assistant`/`text` block — which is exactly the top-level `result.result`
   paraphrase quoted above, not an independent full-length copy

For **this** harness's exact invocation, the only two channels observed to carry the full-length
analysis are `task_notification.summary` and the tail-bearing `tool_result`. There is no third,
independent "interleaved assistant text" reconstruction available to cross-check against.
`extract_agent_analysis`'s cross-check (RESEARCH.md Assumption A4: never silently trust one
channel over another) is therefore implemented against the two channels this probe actually shows
carry full-length text — `task_notification.summary` (primary) and the tail-stripped `tool_result`
(secondary) — rather than against a third "interleaved assistant text" reconstruction that this
capture does not produce. This is a probe-driven adaptation of the plan's literal wording, made for
the same reason D-22 exists: the probe is the authority over what a prior document predicted.

## Verdict

**This probe CONTRADICTS the async-task expectation as archived-evidence predicted it, in one
specific respect: the `tool_result` matching the Agent `tool_use.id` was NOT a ~200-character
launch-acknowledgement stub in this run — it carried the full analysis (plus a metadata tail).**
The dispatch is still asynchronous (a separate `task_started`/`task_updated`/`task_notification`
event sequence runs the subagent to completion before the matching `tool_result` appears at all —
`task_updated` with `status: "completed"` precedes the `tool_result` line in this capture), and
`task_notification.summary` still reliably carries the clean verbatim text with no tail — so
Guardrail A's channel choice (`task_notification.summary`, primary) stands. What changed is that
the `tool_result` fallback cannot be assumed short, and stripping its tail is necessary before
using it as a cross-check. Guardrail A's *intent* — never trust the top-level `result` field — is
decisively vindicated: that field is confirmed a 16.7%-length paraphrase that falsely claims to be
verbatim.

## Frozen-evidence discipline

`probe-P1.jsonl` and this README are committed as-is. They are **never regenerated** (no live
`claude` invocation reproduces this exact capture — this run already happened) and **never
hand-edited** to change a recorded count, length, or verdict. Any correction to this evidence would
be a fresh probe run with its own provenance record, not a silent edit of this one. This is the
single Wave-0 live invocation this plan spends (1 of the phase's declared 19); Plan 04 spends the
remaining 18 (6 generations + 12 judgings).
