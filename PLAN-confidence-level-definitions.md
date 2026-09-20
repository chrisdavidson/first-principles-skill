# Phased plan: define HIGH / MEDIUM / LOW positively, and re-base Criterion 5 on calibration

**Status.** Phases 0–3 executed 2026-09-20 in `shared/`, synced, battery re-run. Per-phase
execution notes are recorded inline under each phase heading. Phase 4's live re-measurement is
the remaining leg.

**Derived from `PLAN-PRAOR-loop-backlog.md` item C3 / 999.137**, workstream C ("Make Observe
actually observe"):

> Define HIGH/MEDIUM/LOW positively in `output-template.md`; re-base Criterion 5 Rigorous on
> **calibration** ("each rating is the highest its inputs and hops license, and no higher"),
> keeping the caps. — Technique §D3. *Removes the structural incentive to inflate. An honest
> MEDIUM becomes Rigorous.*

The same finding is stated in four other places in that document, and this plan closes all five
readings of it:

| Where | What it says there |
|---|---|
| §1.2 claim 4 | "The confidence model rewards HIGH and never defines it — Criterion 5 Rigorous requires every conclusion to rest on a HIGH chain, and HIGH/MEDIUM/LOW are only ever defined as caps" |
| §2.1, row 2 | "Observe is weak where it matters … §D1–D3: no method, no rival, undefined HIGH" |
| §2.3, bullet 1 | "Without D-07 transitivity and a positive definition of HIGH, a named Observe limb still signs off on false certainty" |
| §4, target 4 | "Confidence is calibrated, not maximised. HIGH/MEDIUM/LOW defined positively; D-07 made transitive; Criterion 5 Rigorous re-based on calibration so an honest MEDIUM can be Rigorous" |
| §5, C3 / 999.137 | The operative item (quoted above) |

**Backlog numbering.** `.planning/ROADMAP.md` runs to `999.135` after `PLAN-premortem-wiring.md`.
IDs proposed here start at `999.136`. These are reservations, not registrations.

---

## 1. The defect, stated precisely

### 1.1 The specification gap (confirmed in the tree)

`HIGH`, `MEDIUM` and `LOW` appear throughout `shared/spine/references/output-template.md`,
`shared/spine/references/validation-rubric.md` and `shared/spine/SKILL-body.md`. **Not one of
those occurrences says what the words mean.** Every rule about them is a *cap*:

- **D-07, the unverified-input rule** (`output-template.md`): a chain consuming a `GT-N?` input
  must end MEDIUM or LOW. A ceiling.
- **The transitivity ceiling** (same paragraph, also in Criterion 5 Rigorous): a chain is rated
  no higher than the lowest-rated chain its head cites. A ceiling.

Both say what a chain may **not** be. Neither says what HIGH **is**. A model with no positive
definition, asked to pick a label, falls back on how confident the prose *feels* — which is the
default optimism the technique review names in §D3.

The transitivity half of C2 / 999.136 has since landed — `output-template.md` and the rubric both
carry "rated no higher than the lowest-rated chain its head cites". That is a third cap. It does
not supply a definition, and it is not a substitute for one.

### 1.2 The incentive, caught in a live capture

This is the part worth reading twice, because the repo has a witness rather than an argument.

`validation-rubric.md` Criterion 5 Rigorous currently contains:

> Every claim in the Conclusion section rests on at least one HIGH-confidence chain, so that
> this aggregation yields HIGH.

`DEMO-first-principles-multiregion-latency.md` is the better-behaved of the two untracked
captures in the working tree: eleven chains, D-07 respected on every one of them, four rated
HIGH and seven MEDIUM, and an overall Conclusion rating of MEDIUM that correctly matches its
weakest contributing chain. It is the most honestly-banded output this repository has produced.

Its own Criterion 5 verdict block (`:473`):

> **Band: Sound**
> Justification: Every chain names its weakest link and every `?` input carries a caveat, but one
> Conclusion claim rests on no HIGH chain, so the overall rating is correctly MEDIUM and this
> criterion is not Rigorous.

Read the justification as a sentence about incentives: *the rating is correct, therefore the
score is lower.* The gate docked a run for being right. Everything the analysis would have had to
do to score Rigorous — rate a chain HIGH whose head carries a `?` — is the P1 defect the demo
review found, and the ticket-triage capture in the same working tree still commits it: `C1` on
head `GT-1 + GT-9?` and `C7` on head `GT-2 + GT-4 + GT-13?`, both rated **HIGH**.

So the two captures bracket the problem exactly:

| Capture | Banding | Criterion 5 outcome |
|---|---|---|
| `DEMO-…-ticket-triage.md` | 2 of 8 chains rated HIGH on `?`-carrying heads (D-07 violated) | would clear the HIGH requirement |
| `DEMO-…-multiregion-latency.md` | every band correct, overall MEDIUM | **Sound — docked for it** |

A rule that scores the second below the first is not a stricter rule. It is a rule pointing the
wrong way.

### 1.3 The third failure mode the fix must not create

Defining the levels and removing the HIGH requirement invites the mirror defect: a model that
learns MEDIUM is safe and bands everything MEDIUM. A document where all eleven chains carry the
same defensive label tells a reader nothing about which parts to trust — it has the same
information content as no labels at all, and it is cheaper to produce than a calibrated one.

**Under-rating must therefore be a defect of the same kind as over-rating**, stated in the same
sentence, or the fix relocates the problem instead of closing it. This is the one substantive
addition this plan makes to §D3's recommendation, which names only the inflation direction.

### 1.4 Why a definition and not a stricter cap

A fourth cap would be the cheap move and it does not work. Caps compose to a ceiling and leave
the floor unspecified, so the model still picks freely underneath; and each additional cap is
another rule to apply at the moment the technique review identifies as the one where attention
fails. One positive definition replaces the question "is this label forbidden?" — which requires
holding three ceilings at once — with "which of these three descriptions is this chain?", which
is a single lookup against artifacts the chain already carries on the page.

---

## 2. Target state (falsifiable)

1. **The three levels are defined positively**, in `output-template.md`, in terms the analysis
   can decide by inspecting what it has already written — head identifiers, hop forms,
   `[Assumes:]` annotations — with no new artifact and no new tooling.
2. **The existing caps are derived, not replaced.** D-07 and the transitivity ceiling remain
   verbatim, re-framed as the fast check for the Inputs axis.
3. **Criterion 5 Rigorous scores calibration.** An analysis whose every band is the band its
   axes license is Rigorous, whether its conclusion is HIGH, MEDIUM or LOW.
4. **Both miscalibration directions band below Rigorous**: one miscalibrated chain → Sound, a
   pattern → Hand-wavy.
5. **The gates still pass**, with one recorded literal update in `check-high-confidence-bound.py`
   and no weakening of what HC-BOUND asserts.
6. **Both captures re-score against the new descriptor, and each is docked for a defect that
   is actually there.** Re-scoring them by hand is the acceptance test; it needs no live run.
   The prediction written here before the re-score was run — multiregion Rigorous, ticket-triage
   Sound — was wrong in both halves, and §8 records what the re-score actually found and what
   it changed in the definition.

---

## 3. The definition

Three axes, each decidable by inspection. **The band is the lowest the three axes license** — a
chain is not HIGH because two axes are clean.

| Axis | What it asks | Read from |
|---|---|---|
| **Inputs** | Is every identifier on the head line verified? | The head line's `GT-N` / `GT-N?` / `Cn` tokens and their provenance labels |
| **Inference** | Does each hop follow from the line above it? | The hop lines and their `[Assumes: A-N]` annotations |
| **Rivals** | Does a competing conclusion from the same ground truths survive? | The Phase 5 rival step, and §5 Abandoned Reasoning |

The Rivals axis has no prescribed step yet; that arrives with C4 / 999.138 (Phase 5's method).
It is included here because a band that ignores live rivals is not a confidence rating, and
because stating the axis now gives C4 something to attach to. It is written so that it is
**decidable against an artifact the template already requires** — section 5, Abandoned Reasoning,
whose entries name what was ruled out and which chain ruled it out. §8 records why an earlier,
stricter formulation of this axis was withdrawn.

**HIGH — nothing on this chain is outstanding.** Every head identifier is an unsuffixed `GT-N`
with a named read-at-source location, or a `Cn` itself rated HIGH; every hop follows by
deduction, by arithmetic that recomputes when redone independently, or by a regularity cited to
an unsuffixed ground truth, with no premise the page does not state; and the strongest rival the
analysis considered is named together with what rules it out, that ruling-out input itself
unsuffixed.

**MEDIUM — exactly one axis is short, and the shortfall is named and bounded.** The confidence
line names which axis, names the specific input, hop or rival, and states what would close it. A
MEDIUM chain is one whose weakness a reader can point at.

**LOW — the shortfall is unbounded, or more than one axis is short.** Two axes short at once; or
a `?` input with no available verification path; or a hop whose missing premise cannot even be
stated as an assumption; or a surviving rival no available observation would settle.

**Calibration rule.** Each rating is the highest its inputs, hops and rivals license, **and no
higher** — over-rating and under-rating are the same defect, and Criterion 5 scores calibration,
not altitude.

The exact wording landed in the tree is in Phase 1 below.

---

## 4. Phases

### Phase 0 — Record the before-state (apparatus). 999.136

`PLAN-PRAOR-loop-backlog.md` §6 constraint 1 says instrument before editing `shared/`, because
editing the body first destroys the artifact that demonstrates the gap. The full A1–A4 instrument
is not a prerequisite here: the relevant before-state is two hand-scored captures, and both
already exist in the working tree.

**Executed.** The readings in §1.2 above are the record — chain-by-chain bands and the Criterion
5 verdict text from both captures, taken before any edit. Both files are untracked; Phase 4
should commit them, or this plan's before-state is unreproducible.

### Phase 1 — Define the levels (product). 999.137

`shared/spine/references/output-template.md`: new `### Confidence levels, defined` subsection in
§4, placed immediately before the `### Conclusion C1:` chain template so the definition is in
hand as each chain is written, rather than recalled from a distant global rule. The D-07
paragraph that follows the template is left byte-unchanged; the subsection's closing paragraph
does the framing, so the cap's own wording — asserted verbatim in several places — does not move.

Placement is the point, not decoration: the technique review's §D3 and
`grok-recommendation-confidence-levels.md` tip 1 both find that the model applies the rule when
it is salient at the moment of writing and drifts when it is not.

**Executed.** See §5 for the landed text.

### Phase 2 — Re-base Criterion 5 on calibration (product). 999.138

`shared/spine/references/validation-rubric.md`, Criterion 5:

- **Rigorous** — the HIGH requirement becomes a calibration requirement. The phrase "at least one
  HIGH-confidence" survives in a re-scoped clause (a claim so supported *may* be presented at
  HIGH), which is both the honest statement and what keeps HC-BOUND's HC-9 assertion meaningful.
- The "**A conclusion without a HIGH chain is a banding matter, not a gate failure**" paragraph —
  which docks one such conclusion to Sound — is replaced by its inverse: a conclusion without a
  HIGH chain is Rigorous when every band it rests on is licensed.
- **Sound** — gains single-chain miscalibration in either direction.
- **Hand-wavy** — gains the pattern case, and the uniform-band case from §1.3.
- Both EXCEPT clauses, the caps, and the adversarial-pass paragraph are untouched.

**Executed.** See §5.

### Phase 3 — Reconcile the gates (apparatus). 999.139

One literal in `scripts/check-high-confidence-bound.py` tracks the edited sentence. HC-9's
negative control mutates the canonical rubric by replacing the old sentence; once that sentence
no longer exists the `.replace()` is a no-op, the mutation stops removing the phrase, and the
control silently stops testing anything — an anti-masking failure, not a passing gate.

The fix is to re-point the mutation at the new sentence so it still removes "at least one
HIGH-confidence" from the Criterion 5 Rigorous region. **What HC-BOUND asserts is unchanged**:
the phrase must be present, and its removal must be detected. Only the surrounding words move.

Then `python3 scripts/sync-content.py --write` and `bash scripts/check-firewall-battery.sh`.

**Executed.** See §6 for the result.

### Phase 4 — Re-measure (apparatus). 999.140 — **not executed**

1. Re-score both captures by hand against the landed Criterion 5 text (target state item 6).
2. Commit the two `DEMO-*.md` captures so the before-state is reproducible.
3. A fresh live run on the multiregion prompt, read as a recorded observation with its N under
   K-of-5 discipline — never as a gate (`docs/v8.7-constraint-teardown.md` §2 item 3).
4. The question that run answers: does the model use the Inference and Rivals axes at all, or
   does it keep banding on inputs alone and treat the other two as decoration? A capture where
   every MEDIUM cites an input and none cites a hop or a rival is a null result for two thirds of
   this change, and should be recorded as one.

---

## 5. Landed text

### 5.1 `output-template.md` — the new subsection

Placed between the structured-technique conversion rules and `### Conclusion C1:`. Reproduced
here so this plan is auditable without a diff. **Two clauses below were superseded by the
§8 acceptance test** — the Inference and Rivals axes were scoped after the re-score; the
file is the authority and §8.2 states what moved.

> ### Confidence levels, defined
>
> `HIGH`, `MEDIUM` and `LOW` name how much of a chain is **outstanding** — not how strongly the
> analysis believes its conclusion. Three axes decide the band, each answerable by inspecting
> what the chain already carries on the page:
>
> - **Inputs** — the provenance of every identifier on the head line: an unsuffixed `GT-N` with
>   a named read-at-source location, a `?`-marked ground truth, or a `Cn` carrying its own band.
> - **Inference** — whether each hop follows from the line above it, or needs a premise supplied
>   by an `[Assumes: A-N]` annotation.
> - **Rivals** — whether a competing conclusion from the same ground truths survives, and what
>   rules it out.
>
> **The band is the lowest the three axes license.** A chain is not HIGH because two of them are
> clean.
>
> **HIGH — nothing on this chain is outstanding.** Every identifier on the head line is an
> unsuffixed `GT-N` whose read-at-source location is named, or a `Cn` itself rated HIGH; every
> hop follows from the line above it by deduction, by arithmetic that recomputes when redone
> independently of the chain text, or by a regularity cited to an unsuffixed ground truth, with
> no premise the page does not state; and the strongest rival conclusion the analysis considered
> is named together with the ground truth or chain that rules it out, that ruling-out input
> itself unsuffixed. A chain nobody sought a rival to is unexamined, not certain: it is MEDIUM
> at best.
>
> **MEDIUM — exactly one axis is short, and the shortfall is named and bounded.** One of: an
> identifier on the head line is `?`-marked or is a `Cn` rated MEDIUM; or at most one hop rests
> on a stated `[Assumes: A-N]` premise rather than a derivation; or a rival survives. The
> confidence line names which axis is short, names the specific input, hop or rival, and states
> what would close it — the verification that would remove an input as a cause of the downgrade,
> the evidence that would establish an assumed premise, or the observation that would settle
> between this conclusion and its rival. A MEDIUM chain is one whose weakness a reader can point
> at.
>
> **LOW — the shortfall is unbounded, or more than one axis is short.** Two or more axes short at
> once; or an input is `?` with no verification path available; or a hop's missing premise cannot
> be stated as an assumption, so the analysis cannot say what would make the step valid; or a
> rival survives that no available observation would settle. A LOW chain is reportable, and a
> conclusion resting on it alone is not actionable.
>
> **Calibration rule.** Each rating is the highest its inputs, hops and rivals license, **and no
> higher**. Rating above what the axes license over-claims. Rating below it is a defect of the
> same kind: a chain meeting HIGH on all three axes and written MEDIUM misreports the analysis's
> own strength, and a document whose every chain carries the same defensive band tells a reader
> nothing about which parts to trust. Criterion 5 scores calibration, not altitude — an analysis
> whose every band is the one its axes license is Rigorous whether its conclusion is HIGH,
> MEDIUM or LOW.
>
> **The caps are consequences, not extra rules.** The unverified-input rule (D-07) below and the
> ceiling at the lowest-rated chain a head cites are what the Inputs axis says, restated for the
> two cases that occur most often; they are the fast check, and these definitions are what they
> check for. A cap never licenses a band on its own — it bounds from above, and the band is still
> the lowest any of the three axes licenses.

### 5.2 `validation-rubric.md` — Criterion 5

Rigorous, replacing *"Every claim in the Conclusion section rests on at least one HIGH-confidence
chain, so that this aggregation yields HIGH."*:

> Every rating is calibrated: each chain carries the band its inputs, hops and rivals license
> under the three-axis definition in `output-template.md` — no chain rated above what those axes
> permit, and none rated below it. A Conclusion claim supported by at least one HIGH-confidence
> chain may be presented at HIGH; a claim with no such chain is presented at the band its weakest
> contributing chain licenses, and presenting it so is Rigorous rather than a shortfall.
> Under-rating is a defect of the same kind as over-rating, and this criterion scores
> calibration, not altitude.

Replacing the "banding matter" paragraph:

> **A conclusion without a HIGH chain is not a shortfall.** A conclusion resting on no
> HIGH-confidence chain, uncovered by either EXCEPT clause above, is Rigorous on this criterion
> when every band it rests on is the band that chain's axes license and the Conclusion's own
> rating equals its weakest contributing chain's. A MEDIUM or LOW overall Conclusion rating is a
> legitimate, honestly-caveated analysis — `output-template.md` permits it and this criterion
> now scores it as Rigorous when it is calibrated. What bands this criterion below Rigorous is a
> band that does not match its axes in either direction, never a band that is merely low, and a
> verdict block reporting Rigorous alongside a MEDIUM overall rating is the expected shape of an
> honest analysis rather than a contradiction. An exception is claimed, not assumed: …

Sound gains one clause; Hand-wavy gains two. The exact text is in the file.

---

## 6. Blast radius, and what actually happened

| Surface | Expected | Result |
|---|---|---|
| `sync-content.py --write` | Regenerates both rubric and template copies on the agent surface | Clean |
| **HC-BOUND** | HC-9's mutation literal re-pointed; assertion unchanged | Updated in the same commit, self-test passes |
| **SCAN-GUARD** | Pins Phase 15 scan prescription text, not Criterion 5 band prose | Untouched |
| **HARN-01** | Pins `"HIGH-confidence derivation chain"` as the Phase 3 read population | **Untouched, and now better founded** — the definition makes "feeds a HIGH-confidence chain" mean "every input read at source", which is exactly the population the Phase 3 step already reads for |
| **CONF-GATE / CONF-SURFACE** | Conformance targets and generated tables | See §7 |
| **QUAL-01** | `_selfaudit_calibration_defects` already exists in `check-quality-harness.py` | Unchanged by this plan; it is the natural home for A2 / 999.129's confidence columns later |

---

## 7. Risks

- **The definition is longer than the caps it explains.** Root cause 4 (turn budget) is real, and
  this is a net-add to a reference file the agent loads on demand — not to `SKILL-body.md`, which
  is where the budget actually binds. One sentence went into the body; the rest sits in
  `output-template.md`, which Phase 4 reads anyway.
- **The Rivals axis writes a cheque C4 / 999.138 has to cash.** Until Phase 5 prescribes the
  rival step, the axis is decidable but unprompted, and the honest consequence — no rival sought
  means MEDIUM at best — will pull bands down before C4 pulls them back up. That is the correct
  direction to be wrong in, and it is visible rather than silent.
- **Self-grading remains self-grading.** This raises the floor under Criterion 5 and removes a
  perverse incentive. It does not add a second grader, and a model that wants to clear its own
  gate can still assert that an axis is clean. The honest ceiling is "the gate no longer punishes
  calibration", not "the gate is adversarial".
- **Re-scoring the two captures is a hand check by the same kind of reader that wrote them.**
  Target-state item 6 is a sanity test, not evidence. The evidence is Phase 4.

---

## 8. The acceptance test, and what it changed

Target-state item 6, run by hand against the landed text. It is recorded here in full because it
falsified two things this plan asserted before running it, and the corrections it forced are the
most useful part of the work.

### 8.1 What the re-score found

| Capture | Chains | Miscalibrated under the new definition | New band | Old band |
|---|---|---|---|---|
| `DEMO-…-multiregion-latency.md` | 11 (4 HIGH, 7 MEDIUM) | **C10** — rated HIGH while hop 1 rests on `[Assumes: A20]`, which the endpoint depends on, and whose verification the line itself names as outstanding | **Sound** (one chain) | Sound |
| `DEMO-…-ticket-triage.md` | 8 (5 HIGH, 3 MEDIUM) | **C1** (`GT-1 + GT-9?`) and **C7** (`GT-2 + GT-4 + GT-13?`) — both HIGH on `?`-carrying heads | **Hand-wavy** (a pattern) | Sound |

Two things to read off that table.

**The good run stays at Sound, but the reason changes completely.** It was docked for rating its
conclusion MEDIUM when the rating was correct. It is now docked for `C10`, where the defect is
real: the chain rates itself HIGH, names `A20` as its weakest link, and states the verification
that is still outstanding — *"Verify by reading the PostgreSQL WAL-internals documentation"* —
all in the same breath. D-07 does not catch this, because `A20` is an assumption and not a
`GT-N?` ground truth, and the Inputs axis alone reads that head as clean. The Inference axis is
what sees it. That is the clearest evidence in this plan that the definition does work the caps
were not doing.

**The defective run moves from Sound to Hand-wavy.** Two chains rated HIGH on `?`-carrying heads
is a pattern, not an isolated entry. The old rule reached Sound by one clause and stopped; the
new one grades the pattern as a pattern. The two captures now separate by a band, in the right
direction — which is the whole point, and was not true before.

### 8.2 What the re-score changed in the definition

Both corrections came from checking the definition against a real analysis instead of reasoning
about it. Both made the definition **less** strict, and more discriminating.

1. **The Inference axis was scoped to hops the endpoint depends on, and to unpriced assumptions.**
   The first draft shorted the axis on any `[Assumes: A-N]` annotation anywhere on the chain.
   Applied to the multiregion capture, that demoted `C1` and `C4` — both of which carry an
   assumption on a hop and both of which *say what happens to the endpoint if it fails*: `C4`'s
   line reads *"if they were not, the CDN result would be weaker evidence still, so the
   conclusion is unaffected"*, and `C1`'s annotation sits on a `→[2nd]` extension the endpoint
   does not rest on. Demoting those is not rigour; it is failing to distinguish an assumption
   that has been priced from one that has not, which is the distinction the axis exists to draw.
   Scoped, the axis leaves `C1` and `C4` at HIGH and still catches `C10`.

2. **The Rivals axis was made answerable from section 5 rather than per chain.** The first draft
   required each HIGH chain to name its own rival. Applied to the capture, that demoted every
   HIGH chain in it, because the rival work is written down in Abandoned Reasoning — three
   entries, each naming what it ruled out and the chain that ruled it out — and not repeated on
   each confidence line. The axis now reads section 5, which the template already requires, and
   treats an endpoint that is itself a ruling-out as having done the rival's work. A rule that
   demotes everything is not strict; it carries no information, which is §1.3's failure mode
   arriving through the front door.

### 8.3 What this test does not establish

It is a hand re-score of two captures by the same kind of reader that produced them, against
wording chosen with those captures in view. It shows the definition is *decidable* and that it
separates these two documents in the right direction. It does not show a model will apply it
unprompted. That is Phase 4, and nothing here substitutes for it.
