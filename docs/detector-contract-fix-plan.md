# Detector contract fix — plan

> **Input document.** A plan, not a findings record. Its evidence base is the investigation
> summarised below and reproducible from the frozen corpora named in it. Each phase carries a
> goal, tasks, and a pre-registered acceptance criterion.

## What is broken

Two of the three D-18 defect checks in `scripts/check-quality-harness.py` contradict the output
contract they exist to enforce. The third (`untraced_flag`) is unaffected.

**1 — `_verdict_conforms` is inverted.** It accepts only a bare token (`accept` / `challenge` /
`discard`) after stripping emphasis and punctuation. Both canonical sources prescribe the
opposite:

- `shared/spine/references/output-template.md` — *"The Verdict cell is a token prefix followed by
  an em-dash and the justification — the bare token…"*
- `shared/spine/references/validation-rubric.md`, Criterion 2 Rigorous — *"…as a leading token
  followed by an em-dash and a specific justification — **not the bare token alone**."*

Demonstrated on the frozen corpus: `Q-P2-run1` scores **0/14 nonconforming** — a clean sheet —
and its cells are bare `| Accept`, `| **Challenge**` with no justification, precisely the rubric's
named defect. A freshly generated analysis whose cells read
`**Discard** — contradicted by three independent measurements at 14–26%` scores **16/16
nonconforming**. The check rewards violation and punishes compliance.

**2 — `_chain_block_well_formed` rejects the template's own example.** It matches per physical
line, by design (`"the prescribed form names one line, not a claim spread across several"`), but
the template's canonical worked example spans three lines. Run through the function directly:

| Input | Well-formed? |
|---|---|
| The template's own canonical example | **False** |
| A single-line variant | True |
| A freshly generated conformant chain | **False** |

**Neither check has ever been repaired.** `_verdict_conforms` dates from the original build
(`33e89ef`, Phase 164-03); FIX-CONTRACT-01 repaired the chain-id/tracing functions and did not
touch it.

**QUAL-01 passes because its self-test pins the broken behaviour** —
`_CALIBRATION_VERDICT_FLAGS = [1, 1, 1, 1, 1, 1]` asserts all six calibration documents are
defective, which is what a check that fails the *correct* form would produce on a
mostly-conformant corpus. A green gate is not evidence the invariant holds.

## Blast radius

| Location | Claim | Status |
|---|---|---|
| `v8.7-quality-baseline-freeze.md:128-129` | `verdict_flag` 5/6, "Q-P2-run1 is the one clean document in this baseline" | **Backwards** — Q-P2-run1 is the most contract-violating of the six |
| `v8.7-quality-baseline-freeze.md:217` | Goodhart guard keyed on `untraced_flag`/`verdict_flag`/`chain_flag` | Partly reading an inverted signal |
| `v8.7-post-fix-remeasure.md:84` | `verdict_flag` 5/6, `chain_flag` 4/6 | Both axes suspect |
| `tests/quality-baseline-v8.10-oos/defect-incidence.tsv` | `verdict_flag` 1 on all six rows | Constant, uninformative |

**Disposition (v8.13, DETECT-05, 2026-07-27).**

- Row 1 (`v8.7-quality-baseline-freeze.md:128-129`) — corrected in place at that location.
- Row 2 (`v8.7-quality-baseline-freeze.md:217`) — corrected in place, with the guard's discharge
  canonical at §3 of `v8.7-post-fix-remeasure.md`.
- Row 3 (`v8.7-post-fix-remeasure.md:84`) — corrected in place.
- Row 4 (`tests/quality-baseline-v8.10-oos/defect-incidence.tsv`'s constant `verdict_flag`) — the
  frozen TSV is unmodified by design; the column is qualified in its sibling README.

This four-row list was a starting point, not a boundary: the completeness sweep found more.
`tests/detect05-blast-radius-sweep-v8.13.md` is the full dispositioned hit list — thirty rows
across its §3a and §3b tables, all thirty individually dispositioned there.

The Claim and Status columns above are preserved exactly as written because they record the
diagnosis of what was wrong, not the corrected current state.

## The constraint that shapes the whole plan

**The evidence is frozen; the detector is not.** FROZEN-EVIDENCE (`check-firewall-battery.sh`)
runs `git diff --quiet` over `tests/quality-baseline-v8.7`, `-postfix`, `-regenerated`,
`quality-probe-v8.7` and `quality-catalog-v8.7.md`. Those directories contain the recorded
`defect-incidence.tsv` files.

So: **re-scoring must never overwrite a frozen artifact.** Corrected figures are emitted as new
files sitting alongside the frozen ones. This keeps the gate green, keeps every historical figure
reproducible as originally recorded, and makes the correction a visible addition rather than a
silent rewrite of the past. `tests/quality-baseline-v8.10-oos/` is *not* in the frozen set, but is
treated the same way for consistency.

## Assumption this plan rests on — overturnable

**The template and rubric are canonical; the detector is the outlier.** Two independent canonical
sources agree with each other and disagree with the detector, which is why this is written as a
detector fix rather than a contract change. If the intent was ever that the Verdict cell should be
a bare token, then the template, the rubric, and every generated analysis are wrong instead, and
this plan is the wrong shape. That call should be made explicitly before Phase 2 starts, not
assumed.

---

## Phase 1 — Pin the defect in failing tests (`DETECT-01`)

**Goal.** Encode the correct behaviour as tests that **fail against today's code**, before any
production line changes.

**Why first.** Fixing first and testing after cannot distinguish "I fixed it" from "I changed it
until the number looked right" — the exact failure mode this project has documented in its own
history.

### Tasks

- Add fixtures asserting the prescribed Verdict form (`Accept — justification`, with and without
  bold emphasis) **conforms**, and the bare token **does not**.
- Add fixtures asserting a multi-line chain in the template's shape is well-formed, and that a
  chain missing an intermediate is not.
- Add the **template's own canonical example, lifted verbatim from
  `shared/spine/references/output-template.md`**, as a fixture that must pass.
- Run and confirm every new test **fails**.

### Acceptance criteria

- New tests exist and **fail** against unmodified `check-quality-harness.py`, with the failure
  output recorded.
- No production function changed in this phase.

---

## Phase 2 — Correct `_verdict_conforms` (`DETECT-02`)

**Goal.** Make the check agree with the template and rubric.

### Tasks

- Accept a cell whose leading token is `Accept`/`Challenge`/`Discard` (optionally emphasised)
  followed by an em-dash and non-empty justification text.
- Flag the bare token alone as nonconforming — the rubric's named defect.
- Decide and document the treatment of en-dash and hyphen separators, and of a cell whose
  justification is present but empty after the dash.

### Acceptance criteria

- Phase 1's verdict tests pass; no other self-test item regresses.
- On the frozen corpus the direction **reverses**: `Q-P2-run1` becomes nonconforming and the
  em-dash documents become conforming. Verified by re-scoring into a new file, never overwriting.

---

## Phase 3 — Correct `_chain_block_well_formed` (`DETECT-03`)

**Goal.** Recognise the multi-line chain form the template actually prescribes.

### Tasks

- Match the chain form across the block rather than within one physical line: GT inputs joined by
  `+`, then at least two arrow-led segments, allowing line breaks between them.
- Preserve the existing requirement of at least one genuine intermediate — this fix must not
  become a blanket pass.
- Keep the single-line form conforming; both shapes are legitimate.

### Acceptance criteria

- Phase 1's chain tests pass, **including the template's own example**.
- A chain with no intermediate is still flagged — verified by explicit negative fixture.
- Re-scored chain figures emitted alongside, never overwriting.

---

## Phase 4 — Re-derive the calibration vectors (`DETECT-04`)

**Goal.** Replace the pinned constants that were encoding the broken behaviour.

### Tasks

- Recompute `_CALIBRATION_VERDICT_FLAGS` (and any chain equivalent) from the corrected checks
  against the same calibration documents.
- **Record both vectors, old and new, with the reason for the change** in the self-test's own
  comments. A pinned constant that changes silently is indistinguishable from one that drifted.
- Re-score every frozen corpus into `defect-incidence-corrected.tsv` **beside** each frozen
  `defect-incidence.tsv`, both retained.

### Acceptance criteria

- QUAL-01 `--self-test` passes on corrected constants.
- FROZEN-EVIDENCE still green — `git diff --quiet` clean over every frozen path.
- Every frozen corpus has a corrected sibling; no frozen file modified.
- Old and new vectors both readable in the source with the rationale.

---

## Phase 5 — Correct the published record (`DETECT-05`)

**Goal.** Make the affected published figures honest without erasing what was originally claimed.

### Tasks

- Correct `v8.7-quality-baseline-freeze.md:128-129`, including the specific sentence naming
  Q-P2-run1 as "the one clean document" — it is the opposite.
- Correct `v8.7-post-fix-remeasure.md:84`.
- Re-examine the Goodhart-guard reasoning at `v8.7-quality-baseline-freeze.md:217`: it keys on
  three signals of which one was inverted and one partly broken, so **whether its conclusion
  survives is an open question, not a formality**. State the answer either way.
- Each correction states the original figure, the corrected figure, and why it moved. Amend in
  place with the correction visible — do not silently restate.

### Acceptance criteria

- No published `verdict_flag`/`chain_flag` figure remains uncorrected or unqualified.
- The Goodhart-guard re-examination reaches a stated verdict, including "the conclusion does not
  survive" if that is the finding.
- `check-links` and the full battery pass.

---

## Phase 6 — Guard against recurrence (`DETECT-06`)

**Goal.** Make this class of defect impossible to reintroduce silently.

**The single highest-value test in this plan:** assert that the canonical examples in
`output-template.md` pass the detector that checks conformance to `output-template.md`. One test
would have caught **both** defects on the day they were written.

### Tasks

- Add a self-test item that extracts the worked example from the template at runtime and asserts
  the detector scores it clean — so the test tracks the template rather than a copy of it that can
  drift.
- Add the rubric's Criterion 2 prescribed Verdict form as a fixture, sourced the same way.
- No new script and no new CI gate: these are items inside the existing QUAL-01 self-test, per the
  standing constraint against promoting observations into new instruments.

### Acceptance criteria

- The template-derived item fails if either check regresses — proven by fault injection, not
  assumed.
- Battery composition stays 16/16; no gate added.

---

## Out of scope

- **`untraced_flag` and the tracing logic.** Unaffected — the newly generated analysis scored
  0 untraced claims — and repaired separately by FIX-CONTRACT-01.
- **Re-running any live measurement.** This plan corrects an offline instrument and re-scores
  existing captures. New live runs are a separate decision.
- **Re-opening v8.7–v8.10 conclusions beyond the specific figures listed.** Phase 5 corrects what
  is provably wrong and states what is now uncertain; it does not re-litigate those milestones.

## First action

Phase 1. The tests must be red before anything is fixed, and the template-derived fixture from
Phase 6 should be written in Phase 1 too — it is the one that proves the whole class.
