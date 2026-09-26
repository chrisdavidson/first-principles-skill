# emission-phase1 Stage A — findings

**Protocol:** [`docs/emission-phase1-preregistration.md`](emission-phase1-preregistration.md)
**Run id:** `emission-stage-a-v9.14` · **Model:** `claude-sonnet-5` (pinned)
**Status:** complete — transport probe (n=1, `TB-04`) and the registered ten-prompt run.

This page reports what has been measured. The n=1 probe in §2 is reported as n=1; §3 is the
registered ten-prompt reading and scores the predictions fixed before it ran.

---

## 1. The question, and why it is not the one originally asked

A pivot evaluation dated 2026-09-26 proposed re-scoping the product claim onto
**derivation-showing** — "every load-bearing number is derived in view or marked" — and made
one objection the gate on the whole proposal:

> The trade-off procedure is inlined in the always-loaded agent body and it prescribes exactly
> the missing behaviour […] `TB-04-T` still emitted 82/70/63 with no weights, no anchors and no
> GT-IDs.

Its Phase 1 was therefore: add an *emission*-level requirement to the agent body, re-run, and
see whether instruction moves emission at all. ~30 live calls to kill or continue the pivot.

**That test was not run, because a cheaper one came first and answered the question.**
`TB-04-T` is not the agent's emission. It is the main session's summary of the agent's
emission — see [`docs/trackb-transport-erratum.md`](trackb-transport-erratum.md), which
carries the finding and its falsifiers. So "was the instruction ignored?" was **unmeasured**,
not answered, and the cheapest falsifying test was to capture the agent's own document and
look.

## 2. The transport probe — `TB-04`, the pivot's own specimen

One live invocation, 2026-09-26, on the byte-identical `TB-04` prompt, capturing the
subagent's document instead of the orchestrator's summary.

| Reading | Frozen `TB-04-T` (what Track B judged) | The agent's own document |
|---|---|---|
| Words | 663 | **5,850** |
| Six-section headings | 0 of 6 | **6 of 6** |
| `GT-`*N* identifiers | 0 | **143** |
| Derivation-chain hops (`→`-led) | 0 | **36** |
| Visible numeric derivations | 0 | **3** |
| URLs | 0 | **14** |
| Weight/score table | no | **yes** |

The orchestrator's summary of that same document, captured in the same run, is 585 words and
carries none of it.

### 2.1 The prescription was followed

The agent's document contains, verbatim, the three behaviours the body's trade-off procedure
prescribes and the pivot reported as absent:

- **Weights locked** — a `Criteria & Weights:` table giving all seven criteria a 1–5 weight,
  each with its own anchored scale (`1 means…` / `5 means…`), and a stated
  `Total weight budget: 24.`
- **Arithmetic shown and reconciled** — `Recompute check: B's advantage = Impact(+10)+Cost(+4)
  +Durability(+3) = +17; C's advantage = Speed(+3)+Equity(+3)+Feasibility(+4)+Capacity(+4) =
  +14; net +3, matching 84−81. ✓`
- **Sensitivity bounded** — `Flip test: the smallest single-weight change that flips B↔C is
  Δ=2 […] No Δ=1 change closes the 3-point gap.`

Set beside the pivot's §4, which offered a weights table, a totals line and a reweighting
check as an *"illustrative target — not generated output"*: the agent already generates it.

### 2.2 The summary did not merely compress — it inverted the finding

| | |
|---|---|
| The agent's document | "This is real but narrow, **not robust**." |
| The summary Track B judged | "and the ranking is **robust to reasonable reweighting**." |

A judge scoring the summary on evidence grounding saw an unsupported robustness assertion. The
document it was made from says the opposite, and shows the work. This is the sharpest available
statement of what the transport defect costs: not detail, but truth value.

### 2.3 Sourcing

The subagent issued **9 `WebSearch` and 9 `WebFetch` calls** on this one prompt and its
document carries 14 URLs, including per-ground-truth source links and two logged Phase 3 fetch
failures (403 Forbidden; truncated fetch). The pivot's reading that no URL appears in any of the ten agent-arm
outputs is a property of the summaries, not of the agent.

### 2.4 The same comparison within a single invocation

§2's table sets a 2026-09-26 document beside a 2026-09-25 summary, so run-to-run variation is
confounded with the transport. The stronger comparison is available at no extra cost: each run
captures *both* layers of the *same* invocation. Reading them with the same detector:

| Prompt | Layer | Words | Sections | `GT-`*N* | Hops | Derivations | Capture check |
|---|---|---|---|---|---|---|---|
| `TB-01` | agent document | 6,669 | 6/6 | 118 | 17 | 4 | valid |
| `TB-01` | orchestrator summary | 501 | 2/6 | **0** | **0** | **0** | void |
| `TB-02` | agent document | 6,566 | 6/6 | 76 | 18 | 5 | valid |
| `TB-02` | orchestrator summary | 492 | 0/6 | **0** | **0** | **0** | void |

**`TB-01`'s summary is the instructive one, because it superficially passes.** It opens with
`## Problem Essence` and `## Ground Truths (verified)` and cites sources in prose
(graphql.org, MDN, samnewman.io). A reader — or a judge — would take it for a structured
analysis. It carries **zero** ground-truth identifiers, **zero** derivation-chain hops and
**zero** visible derivations. The apparatus that makes a ground truth checkable is exactly what
does not survive, whether or not the section headings do.

This is also why capture condition 2 counts headings rather than trusting appearance, and why
the threshold is four of six: `TB-01`'s summary clears two.

## 3. Ten-prompt reading

Registered per §4 of the pre-registration; in progress. Predictions P1–P3 were registered
before it started and are scored on completion whatever they return. The reading is scored
only when the unread prompts can no longer change it — a partial run reports `PENDING`, never
a verdict.

**A caveat on P2, recorded 2026-09-26 while P2 was still `PENDING` at 3 of 7**, so that it
cannot be mistaken for a rationalisation written after the number landed:

> **URL count is a crude proxy for sourcing, and it undercounts.** A ground truth can be
> properly grounded without carrying a link — `TB-07`'s `GT-8` is *"Unit identities: 1 acre =
> 4,046.86 m²; 1 TWh = 1,000 GWh"*, sourced to "SI/Imperial definitions", which is the correct
> grounding for a definitional fact and would be worse with a URL bolted on. P2 was registered
> as a check on whether the fetching observed in the TB-04 probe generalises, and it answers
> that. It is **not** a measure of whether load-bearing claims are grounded, and a low P2 must
> not be read as one.

Whatever P2 returns, that reading stands as registered.

### 3.1 The ten-prompt reading, first attempt

Every prompt run once, 2026-09-26, `claude-sonnet-5` pinned. `disp` is the number of `Agent`
dispatches in the transcript.

| id | words | sec/6 | `GT-`*N* | hops | deriv | urls | wt table | disp |
|---|---|---|---|---|---|---|---|---|
| TB-01 | 6,669 | 6 | 118 | 17 | 4 | 0 | yes | 1 |
| TB-02 | 6,566 | 6 | 76 | 18 | 5 | 8 | – | 1 |
| TB-03 | 4,516 | 6 | 87 | 10 | 5 | 1 | – | 2 |
| TB-04 | 5,850 | 6 | 143 | 36 | 3 | 14 | yes | 1 |
| **TB-05** | **0** | **0** | 0 | 0 | 0 | 0 | – | **0** |
| TB-06 | 6,980 | 6 | 90 | 13 | 1 | 0 | – | 1 |
| TB-07 | 5,655 | 6 | 86 | 15 | **16** | 0 | – | 1 |
| **TB-08** | 1,301 | **2** | **0** | **0** | 0 | 0 | – | 1 |
| TB-09 | 6,863 | 6 | 100 | 24 | 2 | 0 | yes | 1 |
| TB-10 | 4,513 | 6 | 107 | 21 | 3 | 2 | – | 1 |

**Against the frozen Track B arm T, which is the same ten prompts:** 0 of 10 captures carried
*any* of the six section headings and 0 carried a single `GT-`*N* identifier. Here 8 of 10 carry
all six, and the eight conforming documents carry 807 ground-truth identifiers between them.

### 3.2 Three outcomes, not two

| Outcome | n | What it is |
|---|---|---|
| Dispatched, full six-section contract | **8** | the agent's output contract, as designed |
| Dispatched, sound reasoning, non-conforming format | **1** | `TB-08` |
| Never dispatched | **1** | `TB-05` |

**`TB-08` is not a bad analysis and should not be filed as one.** It separates the four given
facts from the causal story wrapped around them, challenges baseline comparability, states what
three runs can and cannot establish, reaches a calibrated conclusion and adds an explicit *"what
should NOT be concluded"* section. What it does not do is emit the contract: it uses its own
`Step 1…Step 6` headings, and carries **zero** `GT-`*N* identifiers and **zero** derivation
chains, so no claim in it can be traced to the ground truth it rests on.

One explanation was tested and **failed**: the agent records a `Mode:` marker, and a
single-technique mode would make a different shape expected rather than defective. But the
marker is absent from `TB-01`, `TB-03`, `TB-06` and `TB-07` too, all of which produced 6/6. Mode
does not explain `TB-08`. On this evidence the contract's emission is **variable**, which is the
pivot evaluation's own §1.4 framing — *"the behaviour is not absent — it is inconsistent"* —
holding at the agent's own emission layer rather than at the summary layer where it was measured.

### 3.3 The pre-registered predictions, scored

| | Registered before the run | Result | Verdict |
|---|---|---|---|
| **P1** | ≥4 of 6 sections in ≥8 of 10 | 8/10 | **HOLDS** (exactly at the threshold) |
| **P2** | ≥1 URL in ≥5 of 10 | 4/10 | **REFUTED** |
| **P3** | derivations in more than 1 of 10 | 8/10 | **HOLDS** |

**P2 is refuted and is reported as refuted.** Read with §3's pre-committed caveat, it says the
heavy fetching seen on `TB-04` (9 `WebSearch`, 9 `WebFetch`, 14 URLs) does **not** generalise:
most runs ground their ground truths without fetching anything. It does not say those ground
truths are unsourced — `TB-07` cites SI definitions for a unit identity, which is the right
source — but it does mean the earlier reading that sourcing is routine was too strong, and the
pivot's interest in citation verification is *less* supported by this run than §2.3 suggested
on n=1. That correction runs against the direction of this page's other findings, which is why
it is stated here rather than in a footnote.

**P1 holding at exactly 8 of 10 is a weak pass and is not rounded up.** One more `TB-08` and it
would have failed.

### 3.4 The one permitted re-run, and both readings

§3 of the pre-registration allows a void capture to be re-run **once**. `TB-05` was void for a
routing miss, so it was re-run. The second attempt dispatched the agent and returned a full
document: 6,357 words, 6/6 sections, 140 `GT-`*N*, 17 hops, a weights table, 0 URLs.

Both readings are reported, because a pre-registered re-run is still a re-run and the reader is
owed the number before it:

| | First attempt | After the permitted re-run |
|---|---|---|
| **P1** ≥4/6 sections in ≥8 of 10 | 8/10 HOLDS | **9/10 HOLDS** |
| **P2** ≥1 URL in ≥5 of 10 | 4/10 REFUTED | **4/10 REFUTED** |
| **P3** derivations in >1 of 10 | 8/10 HOLDS | **9/10 HOLDS** |

Three things keep this honest rather than convenient:

1. **P2 did not move.** The re-run emitted no URLs, so no threshold flipped on the strength of a
   second attempt. Had P2 crossed from 4 to 5 here, that would have needed saying loudly; it did
   not arise.
2. **The routing miss is not erased.** That `TB-05` first returned an undelegated direct answer
   is a measurement, recorded in [`docs/trackb-transport-erratum.md`](trackb-transport-erratum.md)
   §4a with its own falsifiers, and the first transcript is retained at
   `tests/emission-stage-a-v9.14/raw-attempt1/TB-05.jsonl`. **Dispatch failed once in eleven
   dispatched-or-attempted runs** and that rate belongs in any reading of this page.
3. **`TB-08` was not re-run**, because it was not void for a mechanical fault — the agent was
   dispatched and produced an analysis. Re-running it would have been re-rolling a result, which
   the protocol does not permit and which is the fault §7 of the pre-registration names.

## 4. Verdict against the pre-registered GO/NO-GO

§4 of the pre-registration defines three readings. This is **A-REFUTES**.

It was established at n=1 on `TB-04` — the very specimen the objection rested on, and one its
own provenance table records as a *"single specimen"* — and it is corroborated at n=10: eight
of ten prompts produced the full contract, carrying 807 ground-truth identifiers and 154
derivation-chain hops between them, against **zero of each** in the frozen captures of the same
ten prompts.

The reading is **A-REFUTES rather than A-MIXED**, and the distinction is worth stating because
`TB-08` is real: A-MIXED is defined as *format present but derivations absent*, which describes
one prompt here, not the population. Where the contract is emitted, the derivations come with
it.

**Stage B is therefore not authorised**, and §7 of the pre-registration forbids running it
anyway on this reading. Concretely: **no emission requirement is added to the agent body.**
The behaviour it would have induced is already present in the agent's output.

That is the pivot's own recommendation honoured rather than overridden. It said *"do not commit
to it — run Phase 1"*, and named the assumption Phase 1 had to test. The assumption failed in
the direction that makes the work unnecessary.

## 5. What this redirects the work toward

The derivation gap is not in the agent. It is in **what survives between the agent and the
reader**. Three things follow, and none of them is a body edit:

1. **The measurement apparatus was reading the wrong artifact.** Fixed here for this protocol
   (`scripts/check-emission-stage-a.py`, capture condition 2). Any future comparative run that
   captures `claude -p` stdout under `--plugin-dir` inherits the same defect.
2. **Where the document goes — now measured, and the answer is largely reassuring.** This item
   previously called the surfacing question open and said the available evidence pointed the
   wrong way. **That reading is retracted**, and it was retracted by a measurement costing no
   live calls at all: the transcripts already captured carry the answer.

   | Route the document took | n |
   |---|---|
   | Streamed by the subagent into the session transcript | **9 of 10** |
   | Arrived only as a collapsed `Agent` tool result | 1 of 10 (`TB-03`) |

   So the document is not generally withheld from the session — it is *in the stream* in nine
   runs out of ten. What discards it is **print mode specifically**: `claude -p` returns the
   orchestrator's final message and nothing else, even though the same run's transcript carries
   the whole document. The defect is narrower than feared: it is a property of how the
   measurement was taken, not of the dispatch path in general.

   **The caveat is real and the claim must not be stretched past it.** This measures what the
   *transport* carries, not what an *interface renders*. A streamed document is present in the
   transcript; whether a given UI shows it expanded, collapsed, or truncated is a rendering
   question no transcript can answer, and the `Agent` tool's own documentation — *"the agent's
   final report is not shown to the user — relay what matters"* — describes an expectation on
   the caller that cuts the other way. Reading either fact as settling the other is the error
   this item made the first time. What is now settled is the transport; the rendering question
   stands open and needs a different instrument.
3. **Citation verification is reachable on a minority of runs, not routinely.** This item said
   citation verification had become *easier* to reach than the pivot judged, written from the
   n=1 probe, and **P2's refutation retracts that** (§3.3): the pivot's stated blocker — that no URL is
   emitted, so there is nothing to verify — was indeed measured on summaries and is not
   absolute, but fetching does not generalise. Four of ten documents carry a URL. So a
   citation-verification product would have nothing to check on most runs, which is a weaker
   position than this item originally claimed and close to the pivot's own §2.3b conclusion by
   a different route. The other limitations of `check-provenance.py` the pivot recorded are
   untouched by this finding and still stand.

## 6. A registration decision, recorded rather than left silent

`scripts/check-emission-stage-a.py` carries a twelve-control `--self-test` but is **registered
in neither the battery nor CI**, and that is a choice, not an oversight — backlog 999.173's
residual is precisely a checker that shipped registered nowhere, so its reading gated nothing.

The reasoning: this is a one-shot measurement protocol, not a product guard, and
`docs/PROCESS.md`'s rule is that a guard guards the product and is not itself guarded. The one
control with standing value — C08, which asserts the frozen Track B arm-T captures still fail
the document check and so keeps [`docs/trackb-transport-erratum.md`](trackb-transport-erratum.md)
falsifiable — is already covered from the other side by FROZEN-EVIDENCE, which fails if any
byte of `tests/trackb-run-v9.13/` changes.

If Stage A's transport is ever reused for a standing measurement, that is the point at which
registration becomes owed.

## 7. Limitations, stated rather than glossed

- **n=10, one run per prompt, one model.** Within-arm variance is uncontrolled: this repository
  has measured up to 3 band points on an identical prompt. `TB-08` may be a stable property of
  that prompt or a one-off, and this design cannot tell which.
- **P1 passed at exactly its threshold**, 8 of 10. One more `TB-08` would have refuted it. It is
  reported as a pass because it was registered as one, not because 8 of 10 is comfortable.
- **The contract's emission is variable and that is now measured, not assumed.** 8 of 10
  conforming is the headline; 1 non-conforming and 1 undelivered are the rest of it.
- **The derivation detector is weak and its weakness is published.** Document-level sensitivity
  1 of 2 on the only hand-audited corpus (pre-registration §6). Every derivation count on this
  page is a floor, not a measurement.
- **No quality claim.** Nothing here scores whether the agent's document is *better*. It counts
  artifacts. `docs/v8.7-correctness-spot-check.md`'s finding — that conformance does not predict
  correctness — applies to every count on this page.
- **The agent emitted the document twice in this run** (a full emission, then a complete
  re-emission). The readings above are of the final emission. Whether that double emission is
  routine is unmeasured at n=1.
- **The weight-table reading is a weak discriminator and should not be read as one.** It fires
  on any Markdown table whose header names a weight or score column, and it fires on the frozen
  `TB-01-T` *summary* as well as on the agent's document. It distinguishes "a table exists"
  from nothing; the locked weights, anchored scales and reconciled arithmetic quoted in §2.1
  were read by hand, not by this detector.
- **Nothing here is published to `docs/EVIDENCE.md`.** No comparative claim clears, and the
  card's standing no-comparison disclaimer is untouched.
