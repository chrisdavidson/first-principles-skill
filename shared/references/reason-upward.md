# Reason Upward

> Construct an answer from verified ground truths using whatever approach the
> problem calls for — reasoning is free-form, but it must be self-documenting.

---

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
too, its `head` being the chains it rests on.

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
