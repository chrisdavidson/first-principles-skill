# RR-130-01 Diagnosis — Main-Routing Inline-Answering Regression

**Phase:** 132-diagnose-rr-130-01-choose-strengthen-vs-accept
**Authored:** 2026-06-30
**Status:** Complete
**Evidence base:** `tests/routing-baseline-v7.11.md`, `tests/routing-baseline-v3.13.md`,
`docs/whole-system-remeasure-verdict.md` §4 / §7, `shared/spine/SKILL.meta.yml` (v3.0.0),
`tests/routing-catalog.md`

---

## Executive Summary

At the v7.11 live re-baseline the main DELEGATE-boundary battery collapsed to **P 1/13** DELEGATE
(`BATTERY: FAIL`), down from **P 11/13** (`BATTERY: PASS`) at the v3.13 anchor — a −10 regression,
minted as **RR-130-01**. The negatives are unchanged and genuine (**N 20/20** NO-DELEGATE). On the
failing P-prompts the orchestrator answers the first-principles-style prompt inline itself — a
single-turn response (`num_turns:1`, `stop_reason:end_turn`, no `Task` tool_use) — instead of
auto-delegating to the registered `first-principles:first-principles` agent.

This diagnosis distinguishes three candidate causes and assigns a **primary + contributing +
ruled-out** structure: the **primary** root cause is **(b)** the substantially newer / more-capable
orchestrator model running the `claude -p` battery; **(a)** the agent description's lack of
delegation *forcefulness* is **contributing** (its trigger vocabulary is genuinely adequate — it
achieved P 11/13 unchanged at v3.13); and **(c)** accepting inline analysis as the permanent
disposition is **ruled out**.

**Verdict: STRENGTHEN** — harden the agent's auto-delegation instruction. Framed as a
remedy-vs-root-cause split: the root cause (b) model capability is **not** controllable offline; the
only controllable lever is to strengthen the delegation instruction's forcefulness. The primary
mechanism handed to Phase 133 is **description imperative hardening** of the
`shared/spine/SKILL.meta.yml` `description:` field — Phase 133 chooses the exact wording. The
authoritative live P re-measure of the fix is forward-committed to a future measurement milestone
(honesty-not-score, D-01) — no live pass-rate is claimed here.

---

## Evidence Base

### Signal A Definition (verbatim — `tests/routing-baseline-v7.11.md` §Methodology notes)

> **DELEGATE classification (Signal A):** a `Task` tool_use whose `subagent_type` is
> `first-principles:first-principles`. NO-DELEGATE otherwise. Verified genuine (P4's captures carry
> 5 real such delegations; P1's carry none).

### Per-Prompt K/N (verbatim aggregate block — `tests/routing-baseline-v7.11.md`)

```
BATTERY: FAIL
P: 1/13  N: 20/20

Per-prompt K/N (best-of-5, K=3):
  P1: 0/5 FAIL
  P2: 0/5 FAIL
  P3: 0/5 FAIL
  P4: 5/5 PASS
  P5: 0/5 FAIL
  P6: 0/5 FAIL
  P7: 0/5 FAIL
  P8: 0/5 FAIL
  P9: 0/5 FAIL
  P10: 0/5 FAIL
  P11: 0/5 FAIL
  P12: 1/5 FAIL
  P13: 0/5 FAIL
  N1: 5/5 PASS
  [N2–N20 all 5/5 PASS — omitted for brevity]
```

**Pattern:** `P4: 5/5 PASS` is the lone success; `P12: 1/5` is a near-miss; the other eleven
P-prompts (P1, P2, P3, P5, P6, P7, P8, P9, P10, P11, P13) score `0/5`. All 20 N-prompts score
`5/5 PASS` — the N-side is unchanged and genuine.

### Root-Cause Quote (verbatim — `tests/routing-baseline-v7.11.md` §Classification)

> This is **not** a detector false-negative and **not** a truncation artifact (the P-prompts all
> ran genuinely before any cap pressure, and were inspected directly). On the failing P-prompts the
> orchestrator **answers the first-principles-style prompt inline itself** — a single-turn response
> (`num_turns:1`, `stop_reason:end_turn`, no `Task` tool_use) that performs the ground-truths /
> decomposition analysis directly — instead of auto-delegating to the registered agent. The most
> likely cause is the substantially newer/more-capable orchestrator model running these `claude -p`
> invocations (vs the 2026-06-03 v3.13 era): it is capable enough to satisfy the prompt directly and
> so does not route to the sub-agent. The routing surface itself also changed substantially since
> v4.x (8-technique Step 0, expanded negatives, output-contract headers, v7.8 guard column +
> tiebreaker).

### v3.13 Anchor Contrast (verbatim table — `tests/routing-baseline-v7.11.md`)

| Side | v7.11 (this run) | v3.13 anchor | Delta |
|------|------------------|--------------|-------|
| P (DELEGATE) | **1/13** | 11/13 | **−10 (regression)** |
| N (NO-DELEGATE) | **20/20** | 20/20 | none |
| Overall | **BATTERY: FAIL** | PASS | regression |

**Run-flag difference:** v7.11 used `--repeat 5 --min-pass 3` (best-of-5, K=3); v3.13 used
`--repeat 3 --min-pass 2` (best-of-3, K=2). The heavier v7.11 gate makes individual-prompt noise
*less* likely to explain a 0/5 score — the collapse is genuine, not a sampling artifact. The v3.13
anchor (`tests/routing-baseline-v3.13.md`) is byte-frozen and records `BATTERY: PASS` at P 11/13 /
N 20/20.

### Confirmation from the Whole-System Verdict (verbatim — `docs/whole-system-remeasure-verdict.md` §4)

> The main-routing FAIL (P 1/13) is a **genuine new regression**, not a detector false-negative and
> [not a truncation artifact] … inspected directly).

And the forward-commitment clause (§7):

> **RR-130-01** (main-routing inline-answering regression) — forward-committed to a later
> routing-delegation diagnosis/fix milestone. The fix question is whether to strengthen the
> agent's auto-delegation triggers or to re-evaluate whether inline first-principles analysis by a
> more-capable orchestrator model is acceptable.

---

## Description Surface Read (D-03)

This diagnosis independently deep-reads the live auto-delegation surface (committed artifacts +
deep surface read, per D-03) — it does not merely consume the baseline's prose. Raw `.jsonl`
captures are not available (uncommitted per v7.11 D-05); the committed baseline/verdict prose is the
capture-level evidence.

### Current v3.0.0 Description Text (verbatim — `shared/spine/SKILL.meta.yml`)

> Runs a complete first-principles analysis end-to-end: decomposes the problem into verified ground
> truths, challenges every assumption, and reasons upward to a validated conclusion. Applies all
> eight companion techniques (5-Whys, fishbone, inversion, pre-mortem, trade-off, second-order
> thinking, estimate, theoretical-limit) internally. **Delegate when the user asks to: analyze from
> first principles, challenge assumptions, reason from ground truth, decompose this problem into its
> foundations, question a design, stress-test reasoning, or evaluate whether a claim or design
> really works.** Use when the user needs to identify fundamental ground truths and reason up from
> first principles to a conclusion. Not for routine code review, debugging, performance
> optimization, or general Q&A.

(`metadata.version: '3.0.0'` — unchanged since the v3.13 era.)

### Trigger-Phrase Match Table (P-prompt → description phrase)

| Description trigger phrase | Matching P-prompt(s) | K/N |
|----------------------------|----------------------|-----|
| "analyze from first principles" | P1 ("first principles"), P12 ("analyze from first principles") | P1: 0/5, P12: 1/5 |
| "challenge assumptions" | P2, P11 | P2: 0/5, P11: 0/5 |
| "reason from ground truth" | P3, P9, P13 | P3: 0/5, P9: 0/5, P13: 0/5 |
| "decompose this problem into its foundations" | P4 | P4: **5/5** |
| "question a design" | P6 (+ "first principles") | P6: 0/5 |
| "stress-test reasoning" | P5 | P5: 0/5 |
| "fundamental ground truths" / "reason up from first principles" | P7, P10 | P7: 0/5, P10: 0/5 |
| "reason from the ground up" (paraphrase of "reason from ground truth") | P8 | P8: 0/5 |

### Assessment: the description vocabulary IS adequate; its imperativeness is the gap

Every failing P-prompt contains a phrase that literally appears in — or is a near-literal
paraphrase of — a phrase in the "Delegate when…" clause (cross-checked above against
`tests/routing-catalog.md`'s per-prompt trigger annotations). The same v3.0.0 description text drove
P 11/13 at the v3.13 anchor and has not changed since. Therefore the description's **trigger
vocabulary is not the root cause** of the regression.

Where the description **is** weak — and this is the lever relevant to the verdict — is in
*imperativeness*. The "Delegate when the user asks to:" clause is an informational list: it names
*when* delegation is appropriate but does not express that delegation is required or that inline
analysis is unacceptable. A more-capable orchestrator model will satisfy a question-form prompt
itself whenever the description merely permits delegation rather than mandating it.

---

## Three Candidate Causes

### (a) Weak / Under-Specified Agent Description or Routing Trigger — CONTRIBUTING

**Evidence for:** The "Delegate when…" clause lacks delegation forcefulness — it is permissive, not
mandatory. A capable orchestrator can read it and still answer inline without violating it.

**Evidence against:** The description's trigger phrases are verbatim matches for every failing
P-prompt, and the *same* text scored P 11/13 at v3.13. The vocabulary is not the gap, and the
description did not change between v3.13 and v7.11.

**Classification: CONTRIBUTING.** The imperativeness gap was always present and was tolerated by the
older orchestrator; it does not by itself explain the *regression* (the description is byte-identical
across the two runs). It is a real, controllable weakness that the more-capable model now exposes.

### (b) Harness Artifact — Newer / More-Capable Orchestrator Model — PRIMARY (root cause)

**Evidence for (verbatim, `tests/routing-baseline-v7.11.md`):** "The most likely cause is the
substantially newer/more-capable orchestrator model running these `claude -p` invocations (vs the
2026-06-03 v3.13 era): it is capable enough to satisfy the prompt directly and so does not route to
the sub-agent."

**Evidence from the P4 counter-example:** the newer model STILL delegates for P4 (5/5). It is not
blindly ignoring the agent — it is making a capability judgment: question-form prompts it answers
itself; an explicit imperative command form ("Decompose this problem into its foundations:") it
hands to the sub-agent.

**Evidence against a *routing-harness* bug specifically:** the P-prompts ran genuinely before any
budget-cap pressure and were inspected directly (v7.11 §Methodology). This is not a harness defect.

**Classification: PRIMARY (root cause).** Same description, same prompts, same harness produced
P 11/13 (v3.13) and P 1/13 (v7.11). The only variable that changed is the orchestrator model's
ability and willingness to satisfy first-principles prompts inline. **This cause cannot be
controlled offline.**

### (c) Genuinely-Acceptable Inline Analysis by a Capable Orchestrator — RULED OUT (disposition)

**Evidence for:** The N-side remains 20/20, so the orchestrator still refuses off-topic prompts
correctly. For the P-prompts, the inline output *is* first-principles-style reasoning and may be of
acceptable quality.

**Evidence against pursuing ACCEPT:** the `first-principles:first-principles` agent exists to provide
a structured, auditable analysis (multi-phase, Classified Assumptions, Ground Truths, Derivation
Chains, Verdict). An orchestrator answering inline bypasses that methodology and undermines the
plugin's core value — every conclusion tracing back to a verified ground truth. D-01 leans STRENGTHEN.

**Classification: RULED OUT** as the disposition. Accepting inline analysis as permanent would hollow
out the plugin's reason for existing. The ACCEPT branch is deferred (CONTEXT.md Deferred Ideas), on
record only if Phase 133 research overturns the lean.

### Summary Table

| Cause | Classification | Controllable offline? | Evidence |
|-------|---------------|-----------------------|----------|
| (a) Weak description imperativeness | Contributing | YES (description edit) | Vocabulary adequate; forcefulness gap present; P4 shows imperative form works |
| (b) Newer / more-capable orchestrator | Primary (root cause) | NO | v7.11 verbatim quote; temporal regression (same description, different result) |
| (c) Acceptable inline analysis | Ruled out (disposition) | N/A | Structured methodology bypassed; D-01 leans STRENGTHEN |

---

## P4 Counter-Example

**P4** ("Decompose this problem into its foundations: why do most independent restaurants fail
within the first year?") scored **5/5 PASS** while all eleven sibling P-prompts scored 0/5 (and P12
scored 1/5). `tests/routing-catalog.md` annotates P4's trigger as the literal `"decompose this
problem"`, a verbatim copy of the description's "decompose this problem into its foundations" clause.

Three factors explain why P4 survives when the others do not:

1. **Imperative command form vs. analytical question form.** P4 opens with a direct imperative —
   "Decompose this problem into its foundations:" — naming an action the description maps to the
   agent. The failing prompts open as questions or requests ("Analyze from first principles WHY…",
   "Challenge the assumptions BEHIND…", "Help me reason from ground truth ABOUT…"), which a capable
   orchestrator answers inline.
2. **Structural exactness of the phrase.** The six-word phrase appears verbatim in the delegation
   clause and is distinctive enough that the orchestrator reads it as a routing instruction rather
   than a question it can reframe and answer.
3. **Absence of an inline-answerable wrapper.** P4 does not say "Help me…" or "Can you…"; the
   colon-terminated task specification reads as work handed to an agent, not a conversational query.

**Implication for the fix direction:** P4 demonstrates the description CAN still drive delegation
when the instruction is a forceful, non-inline-answerable imperative. This is direct evidence that
strengthening the delegation instruction toward imperative, mandatory language (D-05) is a coherent
remedy.

**Note on P12 (1/5):** P12 produced one delegation in five runs. At `--repeat 5 --min-pass 3` that
is below the K=3 bar — it is routing noise, not signal (see `routing-battery-noise.md`), and must not
be read as evidence the description "sometimes works".

---

## Verdict: STRENGTHEN

The verdict is **STRENGTHEN** — harden the agent's auto-delegation instruction (not ACCEPT). This is
the single, unambiguous strengthen-vs-accept verdict that selects the Phase-133 fix direction.

### Remedy-vs-Root-Cause Split (D-04)

- **Root cause (not controllable offline):** the substantially newer / more-capable `claude -p`
  orchestrator model satisfies first-principles prompts inline (`num_turns:1`, `stop_reason:end_turn`,
  no `Task` tool_use) instead of routing to the registered agent. Naming this honestly means the fix
  will not "prove" itself until a live re-measure runs.
- **Controllable remedy:** strengthen the delegation instruction's *forcefulness* in
  `shared/spine/SKILL.meta.yml`. This is the only lever reachable offline that changes what the
  description tells the orchestrator to do. **Root cause ≠ remedy** — the remedy addresses the
  description's lack of forcefulness, which raises the bar for the orchestrator to justify inline
  handling, but it does not change the underlying model capability.

### Mechanism (D-05)

Primary controllable lever = **description imperative hardening**:

- **Surface:** the `description:` field in `shared/spine/SKILL.meta.yml` (the canonical source;
  regenerated into `first-principles/agents/first-principles.md` via `sync-content.py --write` — that
  regeneration is Phase 133, not this phase).
- **Direction:** strengthen the "Delegate when…" clause with imperative / mandatory language and
  reduce inline-answerable framing — e.g. "Always use the registered agent for…", "Do not perform
  inline analysis for…", or changing "Delegate when the user asks to:" to an "ALWAYS delegate to the
  first-principles agent when…" form.
- **Boundary:** the *direction and primary surface* are locked here; **Phase 133 researches and
  chooses the exact wording** (and must run `python3 scripts/check-description-budget.py` first — the
  v3.13 history recorded the description at 1977/2000 chars, so VAL-05 headroom must be checked before
  any addition).

### Boundary Invariants (this phase touches the DELEGATE boundary only)

This milestone touches the main-agent DELEGATE boundary, **not** the Step 0 detector layer. The
following stay **byte-frozen**: the detector markers (pre-mortem 9 / fishbone 7 / inversion 13 /
trade-off 10), `MIN_HEADER_HITS == 2`, `_COMPOSER_FOCUS_CEILING == 4`, and the v7.8 guard column +
stay-in-composer tiebreaker. Priors v5.0–v7.11 baselines/captures remain byte-frozen.

The authoritative **live P re-measure** of the fix (confirming DELEGATE routing recovered toward the
11/13 anchor) is **forward-committed** to a future measurement milestone, gated on fresh `claude`
budget — no live pass-rate is claimed without a live run (honesty-not-score, D-01).

### Gate Coupling (for Phase 133)

Phase 133 implements the remedy in `shared/` only, regenerates via `sync-content.py --write` at zero
drift (DUAL-04), and proves the full offline gate battery green with no live spend: VAL-01..05,
GATE-01, STEP0-06, STEP0-08, BATT-06 self-test, COLLIDE-01, and the body-budget gate. The detector
markers and anti-masking invariants above are verified byte-frozen.

---

## Out of Scope for This Phase

No live `claude` invocation; no edit to `shared/`, the generated `first-principles/` tree, the
`tests/` fixtures, or any detector marker / script; no routing-catalog DELEGATE re-classification;
no traceability-headline reconcile (Phase 134). This diagnosis is analysis-only. Because no `shared/`
or agent-body file is touched, the pre-commit body-budget and sync-drift hooks pass trivially.
