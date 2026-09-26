# Pre-Registration — Does the agent emit its derivations?

**Id:** `emission-phase1` · **Registered:** 2026-09-26, before any run under this id.
**Supersedes nothing.** It is a *new* question, registered under §6 of
[`docs/trackb-preregistration.md`](trackb-preregistration.md), which requires any subsequent
run to cite that document and say why it differs. This one differs because the run it would
otherwise have extended measured the wrong artifact — see
[`docs/trackb-transport-erratum.md`](trackb-transport-erratum.md).

**Binding:** hypotheses, arms, transport, instrument and decision thresholds are fixed below
before any data exists under this id. A change requires a new id.

---

## 1. Where this comes from

A pivot evaluation dated 2026-09-26 proposed re-scoping the product claim from "produces
better reasoning" (unprovable, and measured null by Track B) to "every load-bearing number is
derived in view or marked" (mechanically decidable). It identified one near-fatal objection to
its own proposal, and made testing that objection the first and cheapest step:

> The trade-off procedure is inlined in the always-loaded agent body and it prescribes exactly
> the missing behaviour — *"Assign weights. Lock them now."* […] `TB-04-T` still emitted
> 82/70/63 with no weights, no anchors and no GT-IDs. **This is the closest thing to a natural
> experiment on the pivot's core assumption, and it went the wrong way.**

**That objection rests on an artifact that cannot bear it.** `TB-04-T` is not the agent's
emission; it is the main session's summary of the agent's emission
(`docs/trackb-transport-erratum.md`). A summariser drops a weights table as a matter of
course. So the question "was the instruction ignored?" is, as of today, **unmeasured** rather
than answered in the affirmative.

That changes what the cheapest falsifying test is, and this document re-orders accordingly.

## 2. The two questions, in the order cost requires

| Stage | Question | Live calls | Judges |
|---|---|---|---|
| **A** | When the agent's *own document* is captured, does it already show its derivations? | 10 | none — mechanical |
| **B** | If it does not: does an explicit **emission** requirement make it? | 10 + 20 | 2 per doc |

Stage A is run first because it is cheaper, needs no judge, and can **refute the objection that
motivates Stage B**. Stage B is not authorised until Stage A reports.

## 3. Transport — the correction, stated as a protocol change

Track B captured `claude -p` stdout, which is the **main session's** final message. Under
`--plugin-dir` that message is a summary of the subagent's document.

Every run under this id instead captures the **subagent's** final text message — the assistant
message carrying a non-empty `parent_tool_use_id` — from a `--output-format stream-json
--verbose` transcript. This is the same subagent threading `scripts/check-provenance.py`
already depends on, and the same transport `scripts/check-step0-live.py` has used since
Plan 36.

```sh
CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0 claude -p --model claude-sonnet-5 \
    --plugin-dir ./first-principles \
    --output-format stream-json --verbose \
    --no-session-persistence --permission-mode bypassPermissions "<prompt>"
```

`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0` is retained from Track B §2 for the reason recorded
there: without it, print mode terminates at 600s and emits a delegation stub.

**Capture-integrity check, asserted per capture before anything is scored.** Track B's
120-word floor could not distinguish a summary from a document, which is how this fault
survived. Under this id a capture is **void** unless *all* hold:

1. It came from a message with a non-empty `parent_tool_use_id` (it is the subagent's, not the
   orchestrator's).
2. It carries at least four of the six section headings.
3. It contains no rubric-contamination markers (retained from Track B §7).
4. It is at least 120 words (retained from Track B §7).

Condition 2 is the one Track B lacked. A void capture is re-run **once**; a second void is
recorded as a dispatch failure and its cell is dropped, never scored.

## 4. Stage A — the mechanical reading

**Prompts.** The same ten, unchanged, from `tests/trackb-catalog-v9.13.md`. Reusing them is
deliberate: the frozen Track B captures become a same-prompt comparison surface at the
transport layer, at no additional cost.

**Body.** Shipped, unmodified. Stage A introduces no treatment.

**Reported per document, all mechanically derived, no judge:**

| Reading | How |
|---|---|
| Six-section conformance | count of the six headings present |
| `GT-`*N* identifiers | count |
| Derivation chains (`→`-led) | count |
| Visible numeric derivations | the Stage-A detector, §6 |
| URLs emitted | count of `https?://` |
| Weight/score table present | a table whose header row names a weight or score column |

**Pre-registered predictions, recorded before the run** (scored against the outcome whatever it
is; this is the directional prediction Track B §1 required of itself and got wrong):

- **P1.** At least 8 of 10 captures carry four or more of the six section headings.
  *Rationale: the body makes the six-section format mandatory and the Track B captures'
  failure is attributed to the transport, not the agent.*
- **P2.** At least 5 of 10 captures emit one or more URLs.
  *Rationale: the 2026-09-26 probe observed 9 WebSearch and 9 WebFetch calls on TB-04 alone.*
- **P3.** Visible numeric derivations exceed the frozen arm-T baseline of **1 document in 10**.

**GO/NO-GO A — and both directions are live:**

- **A-REFUTES.** If P1 holds *and* the captures show derivations the summaries did not, then
  the pivot's §2.1 objection is refuted: the instruction was followed and the evidence was
  destroyed downstream. **Stage B is not authorised.** The finding is that the derivation gap
  is substantially a transport artifact, and the work moves to the transport.
- **A-CONFIRMS.** If the agent's own document *also* shows no weights, no derivations and no
  sources, §2.1's objection is confirmed at the right layer for the first time, and Stage B is
  authorised to test whether an emission-level requirement behaves differently from a
  procedure-level one.
- **A-MIXED.** Format present but derivations absent — §2.1 stands on derivations specifically.
  Stage B is authorised, narrowed to derivation.

## 5. Stage B — the emission treatment

Authorised only by an `A-CONFIRMS` or `A-MIXED` reading.

**Treatment.** One addition to the agent body requiring, *at emission*, that any number a
conclusion depends on appear with its arithmetic in view or carry an explicit
`[ungrounded]`/`[external, unverified]` mark. Emission, not procedure — the distinction is the
entire point, since the existing trade-off prescription governs the internal procedure only.

**Arms.** T0 = Stage A's transport-corrected captures (body unmodified). T1 = the same ten
prompts with the treatment. Paired by prompt.

**Instrument.** `docs/trackb-neutral-rubric.md`, unchanged and unread by this document's
author since it was frozen. 2 judges per document, blinded by the existing
`_judge_once()` packet mechanism.

**Threshold, locked now.** Criterion 2 (Evidence grounding) only. The effect clears if
**either**:

- **(a)** mean C2 rises more than **0.6 band points** above the T0 reading, or
- **(b)** the Hand-wavy count falls to **≤2 of 20 judgings**.

Limb (a) is the bar the pivot evaluation named and it is retained **unchanged and
deliberately conservative**. Measured against this run's own instrument it is strict: C2
-specific in-run judge drift, re-derived from the 20 frozen Track B drift pairs, is **0.15
band points**, so twice-drift — Track B's own self-calibrating rule — would be 0.30. Limb (a)
is four times the measured noise. Track B's published 0.90 drift figure is the *fifteen-point
total*, not a per-criterion figure, and does not transfer to a single criterion.

Limb (b) is weaker than limb (a) and is registered as weaker: four Hand-wavy judgings moving to
Sound is a mean shift of only 0.20. It is admitted because the rubric's bands are ordinal and
compressed — clearing the bottom band entirely is a distributional change a mean understates —
and it is named here so that clearing on (b) alone is reported as clearing on the weaker limb,
never as clearing simply.

**Reported regardless:** all five criteria for both arms, the Stage-A mechanical readings for
T1, inter-rater agreement, output length as the registered confound, and the pre-registered
predictions scored.

## 6. The Stage-A derivation detector, and its measured blindness

A line counts as a **visible numeric derivation** when it carries all three of: two or more
numerals; a binary arithmetic operator (`×` `÷` `*` `/` `+`); and a result marker (`=` `≈`
`→`).

**Its false-negative rate is measured, not assumed, and it is bad.** Hand-auditing all 20
frozen Track B captures found **2 documents** carrying genuine visible derivation
(`TB-07-T`, `TB-08-T`). The detector catches **1** of them. It misses `TB-08-T`'s
`"62%→71%, a 9-point / ~14.5% relative increase"` because the `/` sits between a word and a
numeral rather than between two numerals.

**Document-level sensitivity on the only corpus where it has been audited: 1/2 (50%).**

This is published here rather than discovered later because a detector of unknown sensitivity
produces meaningless zeros — the pivot evaluation's own requirement, applied to its own
instrument. The detector is a **reported secondary reading**, never a gate, and no GO/NO-GO in
§4 or §5 turns on it alone. Improving it is Phase 2 work and is explicitly out of scope here:
tuning a detector after seeing the run it will score is the fault this project's
pre-registration discipline exists to prevent.

## 7. Stopping rule

One run per stage. A re-run requires a recorded void and a new id. Stage B may not be run
against a different rubric, a different prompt set or a different N, and may not be run at all
on an `A-REFUTES` reading — that would be searching for a favourable number after the cheap
test came back the wrong way, which §6 of the Track B pre-registration already forbids by name.

## 8. What no outcome here can establish

- **Not a quality claim.** Stage A counts artifacts. Whether showing a derivation makes an
  analysis *better* is Stage B's question, and Stage B measures perceived grounding, not
  correctness.
- **Not a correctness claim.** `docs/v8.7-correctness-spot-check.md` measured that conformance
  does not predict correctness. Nothing here re-derives any analysis's arithmetic.
- **Not a claim about ordinary use.** Every capture dispatches the agent explicitly.
- **Not transferable to another model.** `claude-sonnet-5`, pinned.
