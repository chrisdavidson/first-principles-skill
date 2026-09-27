# Pre-Registration — Is the chain-hygiene movement the body or the prompts?

**Id:** `w4-paired` · **Registered:** 2026-09-26, before any run under this id.
**Binding:** arms, prompts, repeats, transport, instrument, outcomes and decision rules are fixed
below before any data exists under this id. A change requires a new id.

---

## 1. The question

[`docs/live-conformance-v9.14-reading.md`](live-conformance-v9.14-reading.md) compares the live
corpus captured on the v9.12.0 body with the one captured on the v9.0.0 body. After its
correction and its offline adjudication, real positives stand on two axes:

- **Leading-GT hops** — a derivation hop that begins with a `GT-N` identifier, which §4 of the
  output template forbids and which the detector scores as a malformed chain block. v9.0: 0 of 64
  blocks. v9.14: 3 of 49.
- **Verdict qualifier drift** — a prescribed token followed by a qualifier before the em-dash, or
  by no rationale. Documents carrying one: v9.0 3 of 8, v9.14 6 of 9.

Both corpora were produced from **different prompts**, one run each. Neither can say whether the
movement comes from the body or from the prompts. This run holds the prompts fixed and varies
only the body.

## 2. Arms

| Arm | Body | Source |
|---|---|---|
| `old` | `v9.0.0` | a detached worktree at tag `v9.0.0`, `--plugin-dir <worktree>/first-principles` |
| `new` | `v9.12.0` | a detached worktree at tag `v9.12.0` — byte-identical to HEAD's plugin tree at registration |

Neither agent definition pins a model; both carry `maxTurns: 60`.

## 3. Prompts — five, verbatim from their catalogs

| Id | Source | Why it is in the set |
|---|---|---|
| `TB-02` | `tests/trackb-catalog-v9.13.md` | carried a leading-GT hop on the new body |
| `TB-06` | `tests/trackb-catalog-v9.13.md` | carried 7 of v9.14's 17 nonconforming verdict cells |
| `TB-10` | `tests/trackb-catalog-v9.13.md` | carried two malformed blocks (three leading-GT hops) and two nonconforming verdict cells |
| `Q-P2` | `tests/live-conformance-catalog.md` | carried 31 of v9.0's 33 nonconforming verdict cells |
| `PR-N1` | `tests/live-conformance-catalog.md` | carried a qualifier-drift verdict cell on the old body |

Selecting on defects observed under *one* body biases that body's re-run **toward** regression to
the mean, not against the other arm, and the set is drawn from both corpora so the bias is
symmetric.

## 4. Repeats, order and transport

- **3 repeats per prompt per arm — 30 generations.** Estimated cost at the Stage A rate:
  about $65.
- **Order:** prompt by prompt; within a repeat both arms run back to back, and the arm that goes
  first alternates by repeat, so time-of-run drift falls on both arms.
- **Sequential, one invocation at a time.**
- **Transport:** identical to [`docs/emission-phase1-preregistration.md`](emission-phase1-preregistration.md)
  §3 — `claude -p --model claude-sonnet-5 --plugin-dir <arm> --output-format stream-json
  --verbose --no-session-persistence --permission-mode bypassPermissions`, with
  `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`. The document is the **subagent's** own emission,
  extracted by `scripts/check-emission-stage-a.py`'s `extract_subagent_text`, never stdout.

## 5. Instrument

`scripts/check-quality-harness.py`'s `detect_defects`, unmodified, over each extracted document.
A document on which it raises `SectionResolutionError` is **unreadable** and is counted per arm,
never dropped.

## 6. Outcomes

**Primary, per arm, over readable documents (at most 15):**

- **A1** — documents with at least one malformed chain block. Each malformed block's cause is
  also reported (leading-GT hop or other), because A1 is the detector's reading, not the rule's.
- **A2** — documents with at least one nonconforming verdict cell.

**Reported, never interpreted as a body effect:**

- Untraced conclusion claims. The two bodies were given **different contracts**: `**Confidence:**`
  became a claim that must cite a chain after `v9.0.0`, so a difference here is expected by
  construction.
- Block-level and cell-level rates, and per-prompt tables for every axis.
- Unreadable and void documents per arm.

## 7. Decision rule — per primary axis, fixed now

Let `d = new − old`, in documents. `p` is a one-sided Fisher exact test on the 2×2 table of
documents with/without the defect, in the direction of `d`.

| Reading | Condition |
|---|---|
| **Body difference supported** (named direction) | `|d| ≥ 3` and `p ≤ 0.10` |
| **No difference detected at this N** | `|d| ≤ 1` |
| **Inconclusive** | anything else |

**What each reading licenses.** None authorises an agent-body edit by itself. *Supported, new
worse* files a backlog entry naming the rule and this evidence. *No difference detected* closes
W4's question for that axis as not attributable to the body at this N, and says so in the reading.
*Inconclusive* is published as inconclusive and is not re-run under this id.

## 8. Voids and stops

- A generation is **void** if its extracted document is not from the subagent, carries fewer
  than 4 of 6 sections, or runs under 120 words — the Stage A thresholds. A void is retried
  **once**; a second void is recorded as void and counts against that arm's readable total.
- If one arm accumulates more than **3** voids, the run stops and reports what it has.
- A usage-limit or transport failure is not a void: the run pauses and resumes, and the stub is
  kept in `raw/`.

## 9. What this cannot establish

- **Two points, not a trend.** v9.0.0 and v9.12.0 bracket several milestones; a difference is not
  attributed to any one of them.
- **One model, today.** Neither arm reproduces the conditions either original corpus was captured
  under; both are re-captured now so that the comparison is fair, at the cost of comparability
  with either frozen corpus.
- **Form, not quality.** Every outcome counts artifacts. `docs/v8.7-correctness-spot-check.md`
  measured that conformance does not predict correctness.
- **A reading, never a gate** — K-of-N live readings are barred from gating by
  `docs/v8.7-constraint-teardown.md` §2 item 3.
