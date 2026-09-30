# Erratum — Track B arm T captured orchestrator summaries, not agent output

**Raised:** 2026-09-26 · **Tier:** product (`docs/PROCESS.md` §2 — a false sentence on a
committed evidence surface is product regardless of whether its subject is apparatus)
**Concerns:** `tests/trackb-run-v9.13/` (frozen), `docs/trackb-preregistration.md` §7
**Does not concern:** `docs/EVIDENCE.md`, which publishes no comparative claim — the null
result was never published, and `gen-evidence-card.py` controls C06/C07 kept it unpublished.

---

## 1. The finding

**Every one of the ten arm-T captures in `tests/trackb-run-v9.13/generations/` is the main
session's *summary* of the agent's analysis, not the agent's analysis.**

The `first-principles` agent's output contract is six fixed sections — Problem Essence,
Assumptions Table, Ground Truths, Derivation Chains, Abandoned Reasoning, Conclusion — with
`GT-N` ground-truth identifiers and `→`-led derivation chains. None of it survives into the
captures:

| Marker | Occurrences across all 10 arm-T captures |
|---|---|
| `Problem Essence` | 0 |
| `Assumptions Table` | 0 |
| `Ground Truths` | 0 |
| `Derivation Chain` | 0 |
| `Abandoned Reasoning` | 0 |
| `GT-`*N* identifier | 0 |
| `(chain C`*n*`)` citation | 0 |

Three captures say what they are in their own first line:

> `TB-04-T`: "Here's the analysis, **distilled from** the full first-principles breakdown:"
> `TB-05-T`: "Here's **what the first-principles analysis found**:"
> `TB-06-T`: "The analysis is done. Here's the **synthesized result**:"

"Distilled", "found", "synthesized" — these are the orchestrator reporting on a document it
holds and the capture does not.

## 2. Mechanism

`run_prompt()` in `scripts/check-trackb-comparative.py` captures `claude -p` stdout. With
`--plugin-dir` loaded, the main session dispatches the analysis to the `first-principles`
subagent via the `Agent` tool and then **writes its own prose summary of the returned
document** as its final message. Print-mode stdout is that final message. The subagent's
document is a separate message in the transcript, carrying `parent_tool_use_id`, and
`-p` without `--output-format stream-json` never emits it.

The pre-registration already recorded the neighbouring half of this behaviour (§2): with the
plugin loaded the agent runs as a background task, and a 600-second print-mode ceiling
truncated the first attempt to a 54-word delegation stub. Setting
`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0` fixed the truncation. It did not change *which
message* print mode returns.

## 3. Why the extraction-integrity check did not catch it

§7 of the pre-registration exists for precisely this fault class, and names it:

> This project's harness has twice come close to fabricating a decisive result through
> extraction faults — **once by an orchestrator paraphrasing an analysis by ~85%** […]

The implemented check (`extraction_problems()`) tests rubric-contamination and a **120-word
floor**. The summaries run 282–699 words, so the floor never fired. The check was built to
catch a *truncation*; this is a *substitution* of one well-formed document for another, and
length cannot distinguish them.

## 4. What this does and does not invalidate

**Arm C is unaffected.** No plugin, no subagent, no summarisation layer: the control captures
are genuine direct model output.

**The `null` status stands as recorded, and its meaning narrows.** The run measured *a summary
of the agent's analysis* against *an unaided analysis*. That is a real comparison and a null is
a legitimate outcome for it, but it is not the comparison the pre-registration's H1 states
("an analysis produced via the `first-principles` agent"). The run record should be read as
answering the narrower question.

**The per-criterion readings inherit the same narrowing.** In particular the evidence-grounding
figures — arm T `Rigorous 2 / Sound 12 / Hand-wavy 6`, arm C `0 / 12 / 8` — describe summaries
on the agent side. A summariser drops derivations, tables and sources as a matter of course,
which is the single most likely thing to depress an evidence-grounding score.

**Measured, not assumed:** during the 2026-09-26 transport probe the subagent issued 9
`WebSearch` and 9 `WebFetch` calls on `TB-04`'s prompt. The corresponding frozen capture
`TB-04-T` contains **zero URLs**. Whatever sourcing the agent did, the capture does not carry
it.

## 4a. A second, independent reason arm T's meaning is unclear

Measured 2026-09-26 while running the successor protocol: on `TB-05`, with the plugin loaded,
the main session **never dispatched the agent at all**. Its transcript carries zero `Agent`
tool calls and it says why in its own first line — *"This is a general reasoning question,
unrelated to the repo — I'll answer directly rather than invoking any tooling."* The prompt
asks for careful ground-up reasoning but does not name the agent, so whether delegation happens
is a routing decision, and it can go either way.

**Track B cannot tell us how often that happened in its own run.** Plain `claude -p` records no
tool use, so a capture is the same text whether the agent ran or not. Three of the ten arm-T
captures prove dispatch by describing it (§1's quoted first lines). For the other **seven,
dispatch is undeterminable from the evidence that exists.**

So arm T is not merely "the agent's output, summarised". It is *either* a summary of the
agent's output *or* an undelegated direct answer, cell by cell, with no way to tell which from
the record. Both readings are consistent with the frozen captures.

## 5. Consequence for any conclusion drawn from arm T

Any claim of the form *"the agent was instructed to do X and did not do X"* that rests on an
arm-T capture is **not established by that capture**, because the capture is not the agent's
emission. The instruction may have been followed and the evidence removed downstream.

## 6. Disposition

`tests/trackb-run-v9.13/` is registered in `_FROZEN_PATHS` and is **not edited** — editing it
would turn FROZEN-EVIDENCE red and would destroy the record this erratum describes. The frozen
run stands; this document is the correction that travels with it.

A superseding run requires a new pre-registration id per §6 of the original, which is
`docs/emission-phase1-preregistration.md`.

## 7. Falsifiers

Each exits non-zero if the claim it pins is false.

```sh
# 1. No arm-T capture carries any of the six section headings or a GT- identifier.
! /usr/bin/grep -lE 'Problem Essence|Assumptions Table|Derivation Chain|Abandoned Reasoning|GT-[0-9]' \
    tests/trackb-run-v9.13/generations/TB-*-T.txt

# 2. Arm-T captures carry zero chain citations.
test "$(cat tests/trackb-run-v9.13/generations/TB-*-T.txt | /usr/bin/grep -cE '\(chain C[0-9]')" -eq 0

# 3. The three self-describing first lines are present as quoted.
/usr/bin/grep -q 'distilled from the full first-principles breakdown' \
    tests/trackb-run-v9.13/generations/TB-04-T.txt
/usr/bin/grep -q "Here's what the first-principles analysis found" \
    tests/trackb-run-v9.13/generations/TB-05-T.txt
/usr/bin/grep -q 'synthesized result' tests/trackb-run-v9.13/generations/TB-06-T.txt

# 4. The extraction check's floor is 120 words and every arm-T capture exceeds it,
#    so the floor could not have fired.
/usr/bin/grep -q 'min_words: int = 120' scripts/check-trackb-comparative.py
for f in tests/trackb-run-v9.13/generations/TB-*-T.txt; do
    test "$(wc -w < "$f")" -gt 120 || exit 1
done

# 5. Arm-T captures carry zero URLs.
test "$(cat tests/trackb-run-v9.13/generations/TB-*-T.txt | /usr/bin/grep -cE 'https?://')" -eq 0

# 6. Exactly 3 of the 10 arm-T captures prove dispatch by describing it, so 7 do not (§4a).
test "$(/usr/bin/grep -lE "distilled from the full first-principles breakdown|\
Here's what the first-principles analysis found|synthesized result" \
    tests/trackb-run-v9.13/generations/TB-*-T.txt | wc -l)" -eq 3

# 7. §4a's specimen: TB-05 dispatched no agent, and says so; TB-03 did, so the miss
#    is a routing outcome rather than a property of the transport.
test "$(/usr/bin/grep -c '"name":"Agent"' tests/emission-stage-a-v9.14/raw/TB-05.jsonl)" -eq 0
/usr/bin/grep -q "I'll answer directly rather than invoking any tooling" \
    tests/emission-stage-a-v9.14/documents/TB-05.orchestrator.md
test "$(/usr/bin/grep -c '"name":"Agent"' tests/emission-stage-a-v9.14/raw/TB-03.jsonl)" -ge 1
```

## 8. Correction, 2026-09-30

Two sentences above were checked against the tree while planning the superseding run
(`docs/trackb-2-preregistration.md`) and found false. Neither is silently rewritten; both are
corrected here, with the falsifier that caught each.

**(i) §6's naming of the superseding pre-registration is wrong.** The line "A superseding run
requires a new pre-registration id per §6 of the original, which is
`docs/emission-phase1-preregistration.md`" is false: that document's own text states
"Supersedes nothing" — it asks a different, mechanical question (does the delivered document
show its derivations?), not the comparative question this erratum concerns. The comparative
successor is [`docs/trackb-2-preregistration.md`](trackb-2-preregistration.md).

**(ii) §7 falsifier 7 pointed at the wrong files for both of its two assertions.** As written it
checked `tests/emission-stage-a-v9.14/raw/TB-05.jsonl` for zero `"name":"Agent"` occurrences and
`tests/emission-stage-a-v9.14/documents/TB-05.orchestrator.md` for the quoted refusal line. Both
checks are wrong: `raw/TB-05.jsonl` is the **dispatched retry** (it carries exactly 1
`"name":"Agent"` occurrence, confirmed below), and the quoted line does not occur in
`documents/TB-05.orchestrator.md` at all — it occurs in the voided **first attempt**,
`raw-attempt1/TB-05.jsonl`. §4a's underlying claim (TB-05's first attempt dispatched no agent) is
still true; only the falsifier's file targets were wrong.

Corrected falsifier, run against the same evidence:

```sh
# Zero-dispatch leg: the FIRST attempt, not the dispatched retry.
test "$(/usr/bin/grep -c '"name":"Agent"' tests/emission-stage-a-v9.14/raw-attempt1/TB-05.jsonl)" -eq 0
# Quote leg: the first attempt's own transcript, not the orchestrator document.
/usr/bin/grep -q "I'll answer directly rather than invoking any tooling" \
    tests/emission-stage-a-v9.14/raw-attempt1/TB-05.jsonl
```

Measured exit codes, both re-run at correction time: the **original** falsifier 7 (both legs
against `raw/TB-05.jsonl` and `documents/TB-05.orchestrator.md`) exits **non-zero** (the first
leg's count is 1, not 0, and the second leg's grep finds no match) — confirming it was broken.
The **corrected** falsifier above exits **0** on both legs.

TB-03's leg (`raw/TB-03.jsonl` carries >= 1 `"name":"Agent"` occurrence) was already correct and
is unchanged.
