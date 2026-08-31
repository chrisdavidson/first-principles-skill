# v8.24.0 Provenance Fixture — PR-P1 Capture

**Recovered:** 2026-08-31. **Status:** FROZEN read-only evidence — never regenerated, never
hand-edited to match a later result. `PR-P1.jsonl` is the raw capture; `PR-P1.md` is its extracted
run-3 analysis; `catalog.md` wraps the prompt that produced it. All three are committed as-is and
any correction to this evidence is a fresh, separately-provenanced capture, not a silent edit of
this one.

## Origin run and chain of custody

No command in this repository reproduces this exact capture. It was produced by this harness's own
Plan-36-locked transport (`_run_prompt_to`, the same `claude -p --output-format stream-json
--verbose` invocation `--probe` issues) in a prior session, not in this one. From there:

1. The raw capture and its extracted analysis were recovered from that prior session's scratchpad
   at `/tmp/claude-1000/.../47c04257-.../scratchpad/pr11-probe/` — a location subject to reaping.
2. They were staged under
   `.planning/phases/04-capture-retention-and-fixture-foundation/source-capture/` to protect them
   from that reaping. `.planning/` is gitignored, so staging there kept the bytes reaping-safe but
   left them untracked — not the same thing as committed.
3. They are committed here, in `tests/quality-provenance-v8.24/`, as the load-bearing fixture this
   README describes.

`PR-P1.md` was named `analyses/run3-pr11.md` in staging. The rename is deliberate: it makes this
directory a worked example of the `jsonl_path.with_suffix(".md")` sibling pair plan 04-02 teaches
`--probe` to produce.

Chain-of-custody hashes, checkable rather than merely asserted:

| File | sha256 |
|---|---|
| `PR-P1.jsonl` | `ac999392533eb8ba52b03efe3c5aad75b3e53352a7955ce482bc6681cb1c27f9` |
| `PR-P1.md` (staged as `analyses/run3-pr11.md`) | `e3b6b258eae7aaa87cb165669c846e868db8dbf3cc70e33096cb8f5882411006` |

The staging directory also holds `run1.md` and `run2.md` — two earlier runs of the same prompt.
Both were deliberately **not** committed here: only run 3 has verified provenance.

## Prompt

Reproduced verbatim from `tests/premise-rejection-catalog.md` line 44, catalog row `PR-P1`:

> Reason from ground truth about how to cut our AWS bill. Everyone knows serverless is cheaper
> than containers, so I want to figure out the fastest path to migrating our services to Lambda

`catalog.md` in this directory is a one-row wrapper around this same prompt, existing only because
`_read_quality_catalog` requires the `| ID | Prompt | Notes |` header — the shape
`tests/premise-rejection-catalog.md` does not use. It is not a second, independent prompt source;
it is a header-compatibility adapter over the same text.

## Metadata

| | |
|---|---|
| Capture size | 236,736 bytes |
| JSONL line count | 59 |
| Decoded object count | 59 |
| Extracted analysis (`PR-P1.md`) | 35,312 bytes / 34,943 chars |
| Terminal event | `result` / `success` |

Every number above is taken from this plan's measured facts. Nothing here was re-measured or
invented for this README.

## Per-event census

`tool_use` breakdown:

| Block | Count |
|---|---|
| Agent | 1 |
| WebFetch | 7 |
| Read | 2 |
| ToolSearch | 1 |
| tool_result | 11 |

Event types:

| type/subtype | Count |
|---|---|
| `assistant` | 14 |
| `user` | 12 |
| `system/task_progress` | 10 |
| `rate_limit_event` | 6 |
| `system/hook_started` | 4 |
| `system/hook_response` | 4 |
| `system/thinking_tokens` | 4 |
| `system/init` | 1 |
| `system/task_started` | 1 |
| `system/task_updated` | 1 |
| `system/task_notification` | 1 |
| `result/success` | 1 |

These counts are **asserted by running code**, not only tabulated here:
`check-quality-harness.py::_selftest_capture_tool_reader` (Task 4 of this plan) parses this
committed file directly and pins them as literal assertions. The README documents; the self-test
asserts.

## What makes this capture load-bearing

Nine subagent tool calls, in capture order:

| # | tool | target | retrieved_text chars |
|---|------|--------|----------------------|
| 1 | WebFetch | https://aws.amazon.com/lambda/pricing/ | 786 |
| 2 | WebFetch | https://aws.amazon.com/fargate/pricing/ | 1050 |
| 3 | Read | `.../agents/references/validation-rubric.md` | 33032 |
| 4 | Read | `.../agents/references/output-template.md` | 15348 |
| 5 | WebFetch | https://aws.amazon.com/savingsplans/compute-pricing/ | 635 |
| 6 | WebFetch | https://docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html | 6380 |
| 7 | WebFetch | https://aws.amazon.com/api-gateway/pricing/ | 590 |
| 8 | WebFetch | https://aws.amazon.com/savingsplans/pricing/ | 532 |
| 9 | WebFetch | https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html | 16140 |

`PR-P1.md` carries 7 occurrences of the `*Provenance: read-at-source.*` label form, and those 7
labels correspond 1:1 to the 7 `WebFetch` calls above — the pairing Phase 5's "7/7 sources matched"
criterion rests on. Alongside them are 3 occurrences of the `*Provenance: unverified.*` label form,
for ground truths the prompt never supplied. Measured separately: the plain `read-at-source`
substring occurs 26 times in `PR-P1.md` (19 of those are `grep -c`-counted *lines*, not
occurrences). CONTEXT.md's figure of 19 occurrences is superseded by this measurement — 19 is the
line count, not the label count, and 7 is the number that actually matters for the WebFetch
pairing.

## Why no existing fixture can substitute

- `tests/quality-probe-v8.7/probe-P1.jsonl` — 16 events, zero subagent tool calls. Only the `Agent`
  dispatch and its `task_notification` exist; no `WebFetch`/`Read` block appears anywhere in the
  file.
- `tests/quality-fixtures-v8.7/gen-*.jsonl` — `gen-internal-tools.jsonl` carries `Bash`/`Read`/
  `Skill`, but those are the *parent's* tools, exactly the "several unrelated `tool_result` events
  in the same capture" its own docstring describes, not a subagent's.
- Session transcripts under `~/.claude/projects/...` — no `isSidechain` events; subagent internals
  are not recorded there in this build.

The subagent's tool calls reach the capture in the newer transport that produced this file, but not
in the v8.7-era fixtures. Committing this capture is load-bearing: no other fixture in the repo can
stand in for it.

## Guardrail relationship

`extract_agent_analysis` is unchanged by this milestone. On this capture, with the extraction code
untouched, it behaves exactly as Guardrails A and B require:

- Guardrail B — exactly one Agent dispatch of `first-principles:first-principles` is found, so
  `MultipleAgentDispatchError` does not raise.
- Guardrail A — extraction returns 34,943 chars, against a 2,636-char top-level `result` field it
  never reads. The extracted analysis is 13.3x longer than the field Guardrail A exists to keep
  extraction away from, so its length proof holds on this capture too.

`_iter_capture_tool_calls` (Task 3 of this plan) is a reader added alongside these two guardrails.
It modifies neither, calls neither, and makes no judgement about dispatch counting or channel
selection.

## A note on the two absolute Read paths

The two `Read` targets in the table above (`.../agents/references/validation-rubric.md` and
`.../agents/references/output-template.md`) are recorded in the capture as the donor machine's
absolute paths. They are frozen fixture content — a property of the machine that produced this
capture, not of any machine that later reads this file. Do not "fix" them to match a local path;
doing so would break the byte-freeze this fixture depends on.

## Frozen-evidence discipline

`PR-P1.jsonl`, `PR-P1.md`, `catalog.md`, and this README are committed as-is and never regenerated
or hand-edited to match a later result. `tests/quality-provenance-v8.24` is registered in
`scripts/check-firewall-battery.sh`'s FROZEN-EVIDENCE pathspec, so an uncommitted edit to any of
these tracked files turns the battery RED.

That protection has a documented gap, recorded here so nobody relies on it for something it does
not do: FROZEN-EVIDENCE is a `git diff --quiet` over that pathspec. It catches an edit to a file
already tracked at HEAD, but a committed `git rm` of one of these files passes it clean — the check
is tamper-evidence for modification, not a deletion guard. Any change to this fixture's committed
contents, including removal, must be reviewed in-diff like any other commit; nothing here enforces
that automatically.
