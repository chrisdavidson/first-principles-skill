---
name: reason-upward
description: Slash-only Phase 4 stub — build derivation chains upward from named ground truths.
disable-model-invocation: true
metadata:
  version: "9.10.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/reason-upward/SKILL.md by sync-content.py -->

# Focused Reason Upward Mode

You are running in focused-reason-upward mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

## When to reach for this

Use this phase once the Ground Truths list is complete — all ground truths carry IDs and
verification notes — and the Classified Assumptions Table from Phase 2 is finalized. The
methodology has established what is true (ground truths) and what can be discarded (false
assumptions). The task now is to construct an answer from those truths. This phase is
deliberately high-freedom because the right method for combining ground truths depends
entirely on the problem's structure.

---

## Procedure

Reason upward from the ground truths toward an answer using whatever approach the problem
calls for. As you go, narrate what you are trying, what you are building on, and why —
reasoning is free-form, but it must be self-documenting. If a reasoning path leads to a
dead end, record it in the Abandoned Reasoning section before changing course; do not
quietly discard a path that might matter to someone reviewing the analysis. Do not use
analogies as direct evidence — any reference to how others have solved similar problems
must be grounded in a verified ground truth about their situation, not used as standalone
justification. Before handing off to Phase 5, apply the second-order effects procedure
to extend the relevant Derivation Chain with 2nd/3rd-order effects. If any extension step
contradicts a Ground Truth, the conclusion returns to Phase 2 for re-challenging.

**Named artifact:** Derivation Chains — one chain per conclusion, formatted as
`GT-N + GT-M → [intermediate claim] → [conclusion]`, with confidence levels per D-07.

**Confidence rule (D-07):** a chain that includes any `GT-N?` input is rated MEDIUM or LOW, and a
chain is rated no higher than the lowest-rated chain its head cites — a ceiling, never a reason to
rate a chain HIGH. A MEDIUM or LOW chain's confidence line explains only its own chain's rating, so
its validity never depends on how far away a cap originates. It names each `GT-N?` input with the
verification that would remove it as a cause of the downgrade. It names each `Cn` on the chain's
head rated below HIGH and need not re-explain that `Cn`, whose own confidence line carries the
explanation. For each downgrade cause belonging to the chain itself — for example a weak inference
step or an absent-fails derivation — it states what would remove it as a cause of the downgrade or a
stated reason no verification path exists: for an absent-fails derivation, the absent-fails
exception, or an explicit account of why no available evidence settles that cause. The absent-fails
exception covers a chain showing that a conclusion does not follow because an assumption it needs is
false, and it is the only exception that can stand in for a verification path. Directly above every
`**Confidence:**` line, write one `**Pre-check:**` line naming `head` (every head identifier, each
`Cn` with its own band), `?-marked` (the `?` identifiers on `head`, or `none`), `lowest cited` (the
lowest `Cn` band in `head`, or `none`) and `Inputs ceiling` (LOW if a cited chain is LOW, else
MEDIUM if anything is `?`-marked or a cited chain is MEDIUM, else HIGH), fields separated by ` · `;
the label never sits above that ceiling. The Conclusion's `**Confidence:**` line gets a pre-check
too, its `head` being every chain the Conclusion rests on, each with its band, plus any
`GT-N?` the Conclusion rests on directly — a `GT-N?` the Conclusion uses without routing it
through a chain still caps the Conclusion, and omitting it from `head` hides the one input
most likely to be doing so.

`head` is followed by a space and no colon; `?-marked`, `lowest cited` and `Inputs ceiling` each
carry a colon, as in this worked pair:

```text
**Pre-check:** head GT-1, GT-3?, C2 (MEDIUM) · ?-marked: GT-3? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-3? is unverified; …
```

**Chain form:**

The one-line form is the degenerate case, used only when the whole chain fits on one physical line; a chain that does not fit uses the head-plus-arrow-led form, and a hop is split rather than continued on a second line.

The head line lists the inputs the chain consumes: each is a `GT-N` identifier (`GT-N?` when the ground truth is unverified) or a `Cn` identifier, optionally followed by a parenthesized gloss, joined to the next by `+`. The first `→` closes the head. An input carrying unparenthesized prose — `C2's threshold` — is not an identifier and does not parse; write `C2 (threshold)` in every position. The mechanical form check detects that violation only when the prose input is the last one before the first `→`; in an earlier position the check matches the well-formed remainder and scores the head conforming, so the rule binds in positions the check does not reach.

```text
GT-1? ([brief fact label]) + C2 ([brief fact label])
→ [intermediate claim]
→ [conclusion]
```

The head grammar governs the head line only. A hop is prose: `C2's saving` is fine after the first `→`, and is not an input reference. One exception: a hop must not begin with a `GT-N` identifier, which the form check reads as the head of a new chain and which therefore ends this one — write `→ the duty cycle stated in GT-4 is the binding term`, not `→ GT-4's stated duty cycle is the binding term`. The form check detects that violation only while fewer than two hops precede it; in a later position the check matches the preceding hops and scores the chain conforming, so the rule binds in positions the check does not reach.

The mechanical form check additionally rejects a chain whose head or first hop closes its own sentence before the next `→`: it reads the following arrow-led line as a new statement and ends the chain there, so a chain satisfying every rule above is scored malformed for that reason alone. The check reaches only that position — a hop that closes its own sentence from the second hop onward does not change the verdict — which is why intermediate hops carry no terminal punctuation in this project's worked examples.

Each chain must include at least one intermediate step; a chain that goes directly from
its head inputs to a conclusion is a flat list, not a derivation.

**End-of-phase Assumption Audit:** Once the chains — including their second-order
extensions — exist, visit every chain step in order and name any assumption that step
requires to hold that is not already in the Classified Assumptions Table; add each
surfaced assumption back to that table, and mark the originating step inline with
`[Assumes: X]`. When the same undeclared assumption surfaces on more than one step, add it
to the table once and mark each originating step `[Assumes: X]` referencing it — do not
create duplicate table rows for one assumption. A step that introduces no assumption
beyond those already in the table gets no `[Assumes: X]` mark — a clean pass, not an
error. Emit the completed audit as a scan table, one row per chain per step, in order,
with columns `Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table?`,
as process output.

**Exit criterion:** ALL FOUR conditions must hold: (1) the problem's core question as
stated in the Essence Statement is answered, AND (2) every conclusion offered has a
complete derivation chain back to named ground truths, AND (3) the second-order effects
procedure pass has been applied and no extension step contradicts a Ground Truth, AND (4)
the end-of-phase Assumption Audit has run and the Classified Assumptions Table reflects
every assumption surfaced from a chain step. Partial conclusions, incomplete chains, a
silently-skipped second-order pass, or a silently-skipped Assumption Audit do not satisfy
this criterion and do not exit this phase.

## Focused-mode validation

**Check the output against its own completion condition before presenting it.** The
procedure above states one, in whichever form this technique uses — an exit criterion, a
stop test, or an output contract. Read that condition again and confirm the output actually
produced meets every requirement it names, not just the ones that were easiest to satisfy.

**This is a scope-proportionate check, not the six-criterion Self-Audit Gate.** That gate
scores a six-section analysis document; this run produced one technique's output sections,
not six, so walking all six criteria against it would score structure that was never
produced. The larger of the two components: a focused run does not acquire evidence — it
opens no cited source — so a claim resting on a source this run did not open stays marked
rather than being resolved as confirmed.

**Carry the mark forward.** Anything this run could not verify is carried into the output
marked with a `?` rather than dropped or silently asserted as fact.

**Run the technique's own semantic check before declaring the output satisfied.** The
completion condition above is structural — it asks whether the required parts are present.
This asks whether the content holds up. One question, per technique:

- **five-whys** — is each cause counterfactually necessary: would the symptom still have
  happened without it?
- **fishbone** — does each prioritised cause carry an observation that distinguishes it
  from its siblings?
- **inversion** — is each precondition stated as a claim that can be false, and tagged for
  whether the conclusion survives it being false?
- **estimate** — does the bracket's whole width drive the same decision? If the low and
  high ends point different ways, the bracket has not yet answered the question.
- **trade-off** — does the winner survive the smallest weight flip, and is the status quo
  among the options?
- **pre-mortem** — does every fatal or costly cluster carry a tripwire that someone is
  positioned to see?
- **second-order** — has any effect been checked against what the decision is *for*, not
  only against what is true?
- **theoretical-limit** — is the bound the tightest applicable one, and is the demonstrated
  tier an observed figure rather than a calculated one?

A failed semantic check is a `not satisfied` result, not a caveat to attach to a satisfied
one.

**Escalate to the full composer when a `?` becomes load-bearing.** If a claim this run could
not verify turns out to be one the answer does not survive being false — load-bearing in the
validation rubric's sense — stop and say so, in this form:

- `Focused-mode escalation: <the ?-marked claim> is load-bearing - recommend a full analysis`

A focused run acquires no evidence, so it cannot resolve that claim; continuing produces a
confident-looking answer resting on exactly the thing nobody checked. Escalation is the
honest exit, and it is the only case where a focused run should decline to answer in its own
terms. Recommend the escalation; do not silently perform a full analysis instead — the run
was asked for one technique.

**Revise once, then stop.** If the check fails, revise the output and check it again.
Revise at most one time. If it still fails after that pass, present the output with the
gap named rather than revising again.

**End every run with a validation line, without exception.** State exactly one of the
following, verbatim, never silently:

- `Focused-mode validation: satisfied`
- `Focused-mode validation: revised once, now satisfied`
- `Focused-mode validation: not satisfied - <reason>`

Close with the reason this line is unconditional: a silent run is indistinguishable from a
run that skipped the check.

**Then state the residual, on its own line, every time — including after `satisfied`.**
Verbatim:

- `Focused-mode residual: this run opened no cited source, so any ?-marked claim is unverified, not merely uncited.`

This is the one thing the reader of a focused run cannot infer from the output. The
completion-condition check above is a rule *this document* gives the model; the residual is a
fact about the run that its reader needs, and until it is emitted the reader has no way to
tell a focused analysis from a full one that happened to be short. `satisfied` means the
output met its completion condition — never that its claims were verified against a source.

---

If a fuller analysis is needed afterward, invoke the main
`first-principles` agent with this output as Derivation Chains for Phase 5
validation, with the ground truths those chains cite entering Phase 2 as
candidates — the chains rest on inputs this run did not verify. Carry the
`?` marks with it — this run opened no cited source.
