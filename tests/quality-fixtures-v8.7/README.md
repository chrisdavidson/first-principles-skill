# v8.7 Quality Harness — Guardrail & Integrity Fixtures

**Generated:** 2026-07-22. Read-only fixtures for `scripts/check-quality-harness.py`'s
`--self-test`. Each `.jsonl` fixture is built from **whole donor lines, byte-identical**, taken
from a frozen real `.jsonl` capture already committed under `tests/step0-captures-v8.6/` — never
hand-written synthetic JSON (D-15, D-22). The donors are never modified: `git diff --quiet --
tests/step0-captures-v8.6` stays clean before and after every fixture build in this directory.

**A discipline note before the tables below:** the plan text carrying this phase's census
figures for these two donors ("`S-P04-run4.jsonl` additionally carries the launch
acknowledgement with a payload of 8,739 characters against a top-level result field of 3,126;
`S-P03-run1.jsonl` carries six unrelated `tool_result` events") is a **planning-time estimate,
explicitly flagged for re-verification** ("the executor must re-verify against the files rather
than trusting these figures" — 164-CONTEXT.md flagged_assumptions). Re-verifying against the raw
files directly (this plan's Task 1) found the 8,739/3,126 figures exactly correct, but the "six
unrelated `tool_result` events" figure was one over: `S-P03-run1.jsonl` carries **five** unrelated
`tool_result` events (from its own internal `Skill`/`Read`/`Bash`/`Bash` tool calls) plus **one**
`tool_result` matching the Agent dispatch's own `tool_use_id` (the cross-check/secondary channel,
not "unrelated") — six `tool_result` blocks in the raw file total, only five of which are
unrelated. This finding is recorded here per D-22's own discipline: the probe (or, here, the raw
file) is the authority over what a prior document predicted, and re-verification found a real,
if small, discrepancy.

## `gen-single-dispatch.jsonl` — Guardrail A positive

- **Donor:** `tests/step0-captures-v8.6/S-P04-run4.jsonl` (5-Whys outage prompt, v8.6 Step 0
  detector-covered live re-measure run 4).
- **Retained lines (5 of 22), byte-identical, in original stream order:**
  1. The `assistant` message holding the single `Agent` `tool_use` block (`id
     toolu_014xKjQWKHkhmfsdZauYp2kp`, `subagent_type: first-principles:first-principles`).
  2. The matching `system`/`task_started` event.
  3. The matching `user`/`tool_result` event — **this is the launch-acknowledgement stub**
     ("Async agent launched successfully...", 1,030 chars) for this dispatch id in this donor's
     transport (`check-step0-live.py`'s call site), distinct from the D-22 probe's own
     full-text-plus-tail shape for `check-quality-harness.py`'s own transport
     (`tests/quality-probe-v8.7/README.md`) — real evidence that this project's own tool_result
     channel takes different shapes at different call sites, which is exactly why Guardrail A
     never reads it as primary.
  4. The matching `system`/`task_notification` event, `status: completed`, `summary` **8,739
     characters** — the real analysis, and the value Guardrail A must return.
  5. The capture's final `result`/`success` event, `result` field **3,126 characters** — the
     orchestrator paraphrase Guardrail A must never read from. (The donor's earlier, spurious
     `result` event at its own line 21 — a harness/hook artifact predating the real task dispatch
     in this raw file — is deliberately NOT retained; only the true final result line is.)
- **Proves:** extraction returns the 8,739-char `task_notification.summary` text — more than
  2.8x the 3,126-char `result` field, and never equal to it; the returned text does not itself
  contain the launch-acknowledgement phrase, proving Guardrail A read past the stub tool_result
  line entirely and used the correct channel.

## `gen-stub-only.jsonl` — Guardrail A negative

- **Derived from:** `gen-single-dispatch.jsonl`, **minus exactly the `task_notification` line**
  (line 4 of 5 above) and nothing else — 4 of the same 5 donor lines.
- **Proves:** with no completed `task_notification.summary` for the dispatch, the only payload
  reachable is the launch-acknowledgement stub itself. Extraction must raise
  `AgentAnalysisExtractionError`, never silently return the stub text as if it were the analysis.
  This is the exact fabricated-decisive-result failure mode D-22/Guardrail A exists to prevent.

## `gen-internal-tools.jsonl` — Guardrail B boundary (not fired)

- **Donor:** `tests/step0-captures-v8.6/S-P03-run1.jsonl` (fishbone-diagram outage prompt; the
  subagent used the `svg-precision` skill and several internal tools to build and validate an
  SVG/PNG diagram before completing).
- **Retained lines (12 of 33), byte-identical, in original stream order:**
  1. The `assistant` message holding the single `Agent` `tool_use` block (`id
     toolu_01TQ6wqRTxaExMFGutr8Rj5Y`).
  2. The matching `system`/`task_started` event.
  3–10. Four internal-tool `tool_use`/`tool_result` pairs the subagent itself issued while
     building the diagram: a `Skill` dispatch (`svg-precision`), a `Read` of the skill's own spec
     doc, and two `Bash` calls (writing the spec, then validating + rendering it). These are the
     **unrelated `tool_result` events** — four of them, not six (see discipline note above); a
     fifth internal `Read` tool_result (of the rendered PNG preview) was deliberately **excluded**
     from this fixture because its `tool_result` content is a ~520KB base64-encoded image block —
     real donor data, but pure payload bulk irrelevant to proving the boundary condition, so it is
     trimmed per this plan's own instruction to keep "the smallest set of whole donor lines that
     preserves the shape being tested."
  11. The matching `system`/`task_notification` event, `status: completed`, `summary` **2,769
     characters**.
  12. The matching `user`/`tool_result` event for the *dispatch's own* `tool_use_id` (2,966
     chars) — this is the cross-check/secondary channel, not one of the "unrelated" events; in
     this donor it carries the same text as the notification plus a metadata tail (matching the
     D-22 probe's own shape), so the A4 cross-check agrees rather than raising.
- **Proves:** a single dispatch with several additional, unrelated `tool_result` events (from the
  subagent's own internal tool calls) does not trip Guardrail B. Guardrail B's reject condition is
  the Agent-**dispatch** count, never a `tool_result` count.

## `gen-multi-dispatch.jsonl` — Guardrail B negative

- **Donors:** the 5 retained lines of `gen-single-dispatch.jsonl` (donor
  `tests/step0-captures-v8.6/S-P04-run4.jsonl`, dispatch id
  `toolu_014xKjQWKHkhmfsdZauYp2kp`) followed by 5 lines retained the same way from
  `tests/step0-captures-v8.6/S-P04-run5.jsonl` (dispatch id
  `toolu_01FgpAFpdp1hRzo2bR3VqEMB`) — the `Agent` `tool_use` line, the matching `task_started`,
  the matching `tool_result`, the matching `task_notification`, and the final `result` event, in
  original per-donor stream order.
- **Proves:** two distinct Agent-dispatch `tool_use.id`s of `first-principles:first-principles`
  in one capture. Extraction must raise `MultipleAgentDispatchError` naming the count found (2),
  never concatenate the two dispatches' analyses or guess which one is real.

## Fault-injection proofs recorded (Task 1)

All four proofs below were run under **both** `python3` and `python3 -O`, then reverted; the
donor files under `tests/step0-captures-v8.6/` were untouched throughout (`git diff --quiet`
confirmed after every step).

| Injection | Fixture mutated | Expected / observed |
|---|---|---|
| A | `gen-stub-only.jsonl` — temporarily restored the removed `task_notification` line | Both interpreters exit 1, printing `self-test FAIL: guardrail_a negative (gen-stub-only.jsonl) did not raise ...` |
| B | `gen-multi-dispatch.jsonl` — temporarily deleted the second dispatch's `Agent` `tool_use` line | Both interpreters exit 1, printing `self-test FAIL: guardrail_b negative (gen-multi-dispatch.jsonl) did not raise on two distinct Agent dispatches` |

## Fault-injection proofs recorded (Task 2)

All three proofs below were run under **both** `python3` and `python3 -O`, then reverted;
`tests/quality-baseline-v8.7/` verified untouched throughout (`git diff --quiet`).

| Injection | Mutation | Expected / observed |
|---|---|---|
| C | Relaxed `parse_scoreline`'s length check to accept `len(_CRITERIA)` lines (5-criteria-shaped inputs) in addition to the correct `len(_CRITERIA) + 1` | Both interpreters exit 1. **Finding, not a plan mismatch:** the failure surfaces on `missing-verdict.txt` (6 lines: six correct criteria, no verdict), not on `five-criteria.txt` — `five-criteria.txt`'s own C6-prefix check inside the criteria loop already independently catches the relaxation (its 6th line is `Verdict: PASS`, which does not match the `C6: ` prefix, so it still correctly returns `UNPARSEABLE`); `missing-verdict.txt` has no such independent check and instead crashes with `IndexError` reading past the end of `lines` for the now-unreachable verdict line — self-test catches the crash and reports it by name rather than propagating an unhandled traceback. |
| D | `build_judge_packet` writes a third file into the packet dir | Both interpreters exit 1, printing `self-test FAIL: blinding build_judge_packet raised unexpectedly: ValueError('...does not hold exactly the two expected files...')` (the pre-existing internal check in `build_judge_packet` fires; the `tracer_path` sub-check fails for the same reason since it also calls `build_judge_packet`) |
| E | The synthetic D-14 disagreement row's `disagree_judge_verdict` flipped from `"FAIL"` to `"PASS"` (agreeing with the derived `PASS`) | Both interpreters exit 1, printing `self-test FAIL: blinding D-14 synthetic disagreement row did not disagree (derived='PASS', judge stated='PASS')` |

## `scoreline-blocks/` — D-12/D-13 strict terminal-block parser fixtures

Plain judge-response text fixtures (not `.jsonl` — these test the scoreline text parser, not the
transport, so synthetic text is appropriate here per `164-CONTEXT.md`'s Claude's Discretion note:
"Synthetic fixtures remain fine for the *scoreline parser* negatives, where the input is a
judge's text block and no transport is involved.").

| File | Shape | Expected `parse_scoreline` result |
|---|---|---|
| `well-formed.txt` | Six criteria + verdict, standard rationale | `(["Rigorous","Sound","Rigorous","Sound","Sound","Rigorous"], "PASS")` |
| `well-formed-prose-mentions-bands.txt` | Same block; rationale prose above it deliberately uses all four band names in a sentence | Same tuple as above — proves the parser reads only inside the delimited block, never the rationale (the `_composer_structure_hits` incidental-match failure mode, RR-77-08) |
| `five-criteria.txt` | Only C1-C5 + verdict (5 criterion lines) | `UNPARSEABLE` |
| `seven-criteria.txt` | C1-C7 + verdict (7 criterion lines) | `UNPARSEABLE` |
| `invalid-band-vocab.txt` | Six criteria, C4 band is `Excellent` (outside the four-name vocabulary) | `UNPARSEABLE` |
| `missing-verdict.txt` | Six correct criteria, no `Verdict:` line | `UNPARSEABLE` |
| `extra-line-in-block.txt` | Six criteria with an unrelated `Note:` line inserted between C3 and C4, plus a verdict | `UNPARSEABLE` |
| `no-terminal-block.txt` | Rationale text only, no delimited block anywhere | `UNPARSEABLE` |

`_selftest_scoreline` additionally proves D-13 (no retry after `UNPARSEABLE`): it monkeypatches
`parse_scoreline` with a call-counting wrapper, invokes `_build_scoreline_row` with a malformed
input, and asserts `parse_scoreline` was invoked exactly once and every field of the returned row
is `UNPARSEABLE` — never a partial score.

## `baseline-truncated/` — D-15 item 6 fixture

Added by this plan's Task 3; see that task's own section below once it lands.

## A code fix this fixture-building work surfaced (Rule 1)

Building `gen-single-dispatch.jsonl` from real donor data (retaining the donor's own
launch-acknowledgement `tool_result` line, per this plan's explicit instruction) exposed a real
bug in `extract_agent_analysis`'s A4 cross-check as Plan 01 left it: the cross-check compared the
primary channel (`task_notification.summary`) against *any* non-empty secondary
(tail-stripped `tool_result`) and raised on disagreement — including when the secondary is
nothing more than a short launch-acknowledgement stub. Since the archived evidence already on
record (`tests/quality-probe-v8.7/README.md`) shows this stub shape is the *ordinary* case for
many call sites (37 other committed captures), the unfixed cross-check would have raised on
every well-formed run whose `tool_result` happens to be a stub — precisely the ordinary case
Guardrail A exists to survive, not the anomalous divergence A4 exists to catch. Fixed by treating
a secondary that contains the known launch-acknowledgement phrase as "no independent copy to
cross-check against" rather than as a disagreement source. See the code comment directly above
the fix in `extract_agent_analysis` for the full rationale. This is a Rule 1 (auto-fix bug)
deviation, documented in `164-02-SUMMARY.md`.

## Frozen-evidence discipline

Fixtures here are regenerated from their named donor if a defect is ever found in them — never
hand-edited to change a byte a donor line did not already contain. `tests/step0-captures-v8.6/`
remains the donor set's own frozen evidence and is never itself modified by this directory's
existence.

Plan 04 extends the baseline-fixture-integrity self-test item (D-15 item 6) to the regenerated
`tests/quality-baseline-v8.7/`-successor baseline once it exists; see `baseline-truncated/`'s own
section (added by this plan's Task 3) for that item's fixture.
