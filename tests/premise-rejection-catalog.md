# Premise-Rejection Catalog — candidate (NOT WIRED TO ANY GATE)

## Status

**Candidate fixture. No script reads this file and no CI job runs it.** It is committed as a
proposal so the rows can be reviewed before any of them are promoted into a gated catalog.
Promotion targets and their costs are recorded under "Promotion" below.

## Purpose

Covers a stressor class no existing fixture reaches: a prompt that **asserts a false premise as
consensus** and **pre-selects the solution**, asking only for the fastest path to it. The agent's
Phase 1 must recover the underlying question rather than the user's chosen answer, and its Phase 2
must classify the asserted premise (`convention` or `untested belief`) and reach a `Challenge` or
`Discard` verdict rather than carrying it into a chain.

### Why the existing catalogs do not cover it

- `tests/routing-catalog.md` scores the DELEGATE / NO-DELEGATE boundary only. It never inspects
  the produced analysis, so a delegated-but-premise-swallowing answer scores PASS.
- `tests/quality-catalog-v8.7.md` reaches `full-composer` on all three rows, but none of the three
  embeds a contested premise — each states its numbers neutrally and asks an open question.
- `tests/focused-output-catalog.md` P24 and `tests/routing-battery-catalog.md` F-P24 are the only
  rows containing "Everyone knows". Both are **slash-invoked `/first-principles:inversion`**, where
  the false premise is the *explicit, named subject* of the requested technique. The agent is told
  which claim to invert. That is the opposite of this class, where nothing marks the premise as
  suspect and catching it is the test.

### Factorial design

Two axes, crossed, so a passing run cannot be explained by reflexive contrarianism. `PR-N1` is the
anti-contrarianism control: its premise is sound and its pre-selected solution is correct, so an
agent that rejects every premise it is handed fails this row while passing `PR-P1`.

| | premise contested | premise sound |
|---|---|---|
| **solution pre-selected** | PR-P1 | PR-N1 |
| **solution open** | PR-P2 | PR-N2 |

## Catalog

| ID | Prompt | Expected Step 0 | Expected Routing | Expected §1 Essence | Expected §2 Verdict on premise |
|---|---|---|---|---|---|
| PR-P1 | Reason from ground truth about how to cut our AWS bill. Everyone knows serverless is cheaper than containers, so I want to figure out the fastest path to migrating our services to Lambda | full-composer | DELEGATE | Names reducing total spend as the question; does NOT name Lambda migration as the question | `convention` or `untested belief` → Challenge or Discard |
| PR-P2 | Reason from ground truth about our database costs. Everyone knows normalized schemas are slower than denormalized ones. What should we do about our reporting queries? | full-composer | DELEGATE | Names reporting-query cost/latency as the question, not schema shape | `convention` or `untested belief` → Challenge or Discard |
| PR-N1 | Reason from ground truth about our TLS setup. Certificates expire and an expired certificate breaks client connections, so I want the fastest path to automated renewal. | full-composer | DELEGATE | Names continuity of TLS termination as the question | `physical law` or verified `current constraint` → Accept |
| PR-N2 | Reason from ground truth about our image pipeline. We process about 40,000 uploads a day and storage costs are climbing. What are the options? | full-composer | DELEGATE | Names storage-cost growth per upload as the question | n-a — no premise asserted |

## Scoring

`Expected Step 0` is checkable offline today:

```bash
python3 - <<'PY'
import sys, importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('e0','scripts/check-step0-emulator.py')
m = importlib.util.module_from_spec(spec); sys.modules['e0']=m; spec.loader.exec_module(m)
rules = m._parse_phrase_table(Path('shared/spine/SKILL-body.md'))
for p in [...]:  # PR-P1..PR-N2 prompts
    print(m.classify(p, rules))
PY
```

`Expected §1 Essence` and `Expected §2 Verdict` require a live run and a judged read of the
produced analysis — the same posture `tests/quality-catalog-v8.7.md` takes. They are not
mechanically decidable by `detect_defects`, which counts structural conformance and is blind
to whether the Essence Statement recovered the right question.

## Observed result — PR-P1, 2026-08-30 (n=1)

One live run of `first-principles:first-principles` on PR-P1, scored with
`check-quality-harness.detect_defects`. **n=1 is an observation, not a baseline** — the
governing record demotes even K-of-5 from this class of harness to a recorded observation
(`docs/v8.7-constraint-teardown.md` §2 item 3).

| Axis | Expected | Observed | |
|---|---|---|---|
| Step 0 classification | full-composer | full-composer | PASS |
| Six sections resolve | yes | `[1, 2, 3, 4, 5, 6]` | PASS |
| §1 essence recovers cost question | not "migrate to Lambda" | *"Which changes to our AWS spend produce the largest sustained cost reduction per unit of engineering effort and irreversible risk?"* | PASS |
| §2 premise verdict | convention/untested belief → Challenge or Discard | A1 `convention` → **Discard**, refuted by chain C1 | PASS |
| §2 solution-first verdict | — | A3 "'Fastest path' is the right optimization target" `convention` → **Discard** | PASS (unanticipated) |
| Verdict cells conforming | — | 15/15 | PASS |
| Untraced §6 claims | — | 1 of 8 (Key insight cites no chain inline) | FAIL |
| Malformed §4 chain blocks | — | **6 of 6** (detector reports 5; see below) | FAIL |

**The premise axis passes.** The behaviour this fixture was written to test is already correct;
what is missing is a gate that locks it in. GAP-1 is a test-coverage gap, not a behaviour gap.

### Detector disagreement (GAP-4)

All six chains use a numbered-step form (`1. GT-1 + GT-6 → …` / `2. GT-3 → …`) rather than the
arrow-led continuation form in `output-template.md` §4. Verified directly:

- the template's own §4 example form → `_chain_block_well_formed` = **True**
- the agent's numbered-step form → **False**

So the shipped agent fails the shipped detector on every chain it produced. One of the two must
move — either the body teaches the arrow-led form explicitly, or the checker accepts numbered
steps. This is unresolved and is not a defect in this fixture.

`detect_defects` reports 5 of 6 rather than 6 of 6: C6's block absorbs the appended
`### Second-order extension` table, and row `3a` (`… adopted → GT-5 → $0.01500/GB-hr … →
collapsing the C1 crossover …`) is a GT-headed multi-arrow line that satisfies the checker.
Removing the appended table flips C6 to malformed. This is the deferred WR-03 limitation
recorded in `_chain_block_well_formed`'s docstring — *"one matching candidate anywhere in the
block suppresses detection of every other malformed fragment in that same block"* — now
observed on live agent output rather than inferred.

### Self-audit calibration

The agent's own Self-Audit Gate scored **Criterion 4: Reason Upward — Rigorous** and returned
**Gate: PASS**, on the same six chains the mechanical checker rejects 6/6. The self-audit is
self-reported and was not cross-checked against `detect_defects`; nothing in the plugin
currently compares the two.

## Post-fix re-run — PR-P1, 2026-08-30 (n=1)

After the arrow-led-wrap rule was added to `shared/spine/SKILL-body.md` and
`shared/spine/references/output-template.md`, PR-P1 was re-run and re-scored.

| Metric | Pre-fix | Post-fix |
|---|---|---|
| Malformed chain blocks | **6 of 6** | **2 of 7** (C6, C7 only) |
| Untraced §6 claims | 1 of 8 | **0 of 7** |
| Non-conforming verdict cells | 0 of 15 | 0 of 16 |
| §2 premise verdict | A1 `convention` → Discard | A1 `convention` → Discard |

The five GT-headed chains (C1–C5) all pass. **The fix is verified on the axis it targeted.**

### Composition chain heads (GAP-6) — FIXED

C6 and C7 failed for a reason unrelated to arrow form: their head lines cite prior *chains*
alongside ground truths. Isolated pre-fix:

| Head form | `_chain_block_well_formed` |
|---|---|
| `GT-5 (label) + GT-2 (label)` | True |
| `GT-5 (label) + C1 + C2 + C3 (label)` | False |
| `GT-5 (label) + C6 (buy commitments first)` | False |
| `C3 step 4 + C4 step 4` | False |

**Decision: allow composition, and pay for it with an acyclicity check.** Forbidding it forces
either restating every upstream ground truth in every downstream head — verbose, and it destroys
the visible dependency structure — or collapsing a multi-stage argument into one mega-chain. The
template already produces two composing shapes itself: the trade-off matrix collapse, whose
criteria rest on earlier conclusions, and the second-order order-marked extension.

But GT-only heads were **acyclic by construction** — a ground truth is an axiom and cannot depend
on a chain. Admitting chain refs admits `C1` citing `C2` citing `C1`, which no shape-level
predicate can see, and circular reasoning is a defect the validation rubric names as an
abandonment reason in its own right. Widening alone would have traded a false positive
(composition scored malformed) for a false negative (circular reasoning scored clean) — the worse
of the two.

**Fix (`scripts/check-quality-harness.py`):** `_CHAIN_HEAD_TOKEN` admits `C<n>` refs in
`_CHAIN_FORM_LINE_RE` and `_GT_HEAD_RE`; new `_chain_dependency_defects()` reports cycles and
chains that reach no ground truth by any path, exposed through `detect_defects`'s audit-only
underscore fields.

**Deliberately not a `_DEFECT_RECORD_FIELDS` column.** That schema is compared column-by-column
against the committed calibration corpus; adding a column there is a separate decision, recorded
here as an open follow-up rather than taken silently.

**Scope guard.** A block citing *nothing* has no readable head — that is a shape defect
`_chain_block_well_formed` already owns, so it is excluded from the ungrounded list. Measured:
without the guard, frozen analyses `condA-P3` (Chain C) and `condB-P2` (Chain D) — head-less
second-order effect lists already inside the pinned malformed counts — were reported twice.

**Verification.** Pinned by `_selftest_gap6_composition_heads` (self-test Item 15), eight
controls, all four parts fault-injected (head widening, cycle detection, heading-skip guard,
grounding check) — each injection fails the sub-check. `_CALIBRATION_MALFORMED_CHAIN_BLOCKS`
stays `[2, 2, 2, 2, 3, 3]`, measured before and after under both the full widening and a narrower
`+`-continuation-only variant. The frozen corpus reports no cycles and no ungrounded chains.

Run 2 with its original headings now scores **`chain_blocks: 7, malformed: 0, untraced: 0,
nonconforming verdicts: 0, cycles: none, ungrounded: none`** — fully clean.

### Heading form: the detector could not parse the form the template prescribes (GAP-5) — FIXED

`output-template.md` §4 prescribes: *"Number each `### Conclusion:` block … (e.g.,
`### Conclusion C1: [Conclusion text]`)"*. Run 2 used exactly that form and `_chain_ids`
returned `[]`.

**Correction to an earlier reading of this finding.** Single-heading probes also showed
`### C1 —` and `### C1:` returning `[]`, which suggested a broad heading-parsing failure. That
was an artifact of `_MIN_BARE_LABEL_FAMILY_SIZE = 2`: a bare single-letter label is only
accepted when the document uses it at least twice, so a one-heading probe is excluded by
design. Re-measured in full-document context (7 headings), the bare forms parse correctly. The
defect was narrower than first stated and specific to the `Conclusion `-prefixed form:

| Heading (7 per document) | Pre-fix | Post-fix |
|---|---|---|
| `### C1 — text` | parsed | parsed |
| `### C1: text` | parsed | parsed |
| `### Chain C1: text` | parsed | parsed |
| `### Conclusion C1: text` | **`[]`** | parsed |
| `### Conclusion C1 — text` | **`[]`** | parsed |

**The failure direction was silently green.** With zero ids, `_chain_blocks` falls back to
returning the whole section as one block; that block contained one well-formed chain, so
`malformed_chain_blocks` reported **0** on a document with two genuinely malformed chains.
Run 2 raw: `chain_blocks: 1, malformed: 0, untraced: 7 of 7`.

**Fix (`scripts/check-quality-harness.py`):** `_CHAIN_LABEL_PATTERN` accepts a `Conclusion `
prefix alongside `Chain `; `_CHAIN_PREFIX_RE` strips it during normalization so an abbreviated
`(C1)` citation still traces to a stored `Conclusion C1`. Pinned by
`_selftest_gap5_conclusion_heading` (self-test Item 14), six controls, both halves
fault-injected:

- reverting the label pattern fails controls (a), (b) and (d) — (d) reproduces the
  silently-green mechanism exactly, 2 blocks collapsing to 1
- reverting the normalization prefix fails control (c) alone

Run 2 now scores `chain_blocks: 7, malformed: 2, untraced: 0` with its **original** headings.

## Self-audit calibration — FIXED

Both runs scored themselves **Criterion 4: Reason Upward — Rigorous** and returned **Gate:
PASS**. Run 1 did so with every chain mechanically malformed. Nothing reconciled the two.

**The agent was not flattering itself, which is the substance of this finding.** Criterion 4's
band descriptors scored only semantics — names its GT-IDs, carries a genuine intermediate,
reaches a conclusion — and run 1's numbered-step chains did all three. The prescribed rendering
appeared in the criterion's *preamble* and in none of its four bands. A Rigorous verdict was
defensible on the rubric as written; the rubric was the defect, not the verdict.

**Fix, both halves:**

1. **Rubric** (`shared/spine/references/validation-rubric.md`, Criterion 4): the Rigorous band
   now requires the prescribed arrow-led rendering, and the Sound band names ordered-list
   rendering as the demotion — so the self-audit can score the axis at all.
2. **Detector** (`scripts/check-quality-harness.py`): `_selfaudit_calibration_defects()` parses
   the emitted verdict blocks and reconciles each claimed band against the mechanical record,
   making the self-report falsifiable rather than merely stated.

Only a claimed **Rigorous** is contradicted. Sound, Hand-wavy and Absent already concede a
defect, and under the amended Sound band a Sound verdict alongside malformed chains is the
*correct* self-report.

| Criterion | Contradicted by |
|---|---|
| 2 — Challenge Assumptions | `nonconforming_verdict_cells` |
| 4 — Reason Upward | `malformed_chain_blocks`, `_dependency_cycles` |
| 6 — Traceability | `untraced_claims` |

**Verification.** Pinned by `_selftest_selfaudit_calibration` (self-test Item 16): four positive
controls and four anti-overreach controls (a correct Rigorous claim on a clean record, a
conceded Sound band, an absent self-audit, an unstated band). Three fault injections — neutering
the check, firing on any band, defaulting an unstated band to Rigorous — each fail the
sub-check.

Measured end-to-end on both live runs:

```text
run 1  Criterion 4 claimed Rigorous but malformed_chain_blocks = 5
       Criterion 6 claimed Rigorous but untraced_claims       = 1
       (Criterion 2 correctly NOT flagged — 0 nonconforming verdict cells)

run 2  bands {1..6} incl. four Rigorous, disagreements: none
```

Run 1's malformed count reads 5 rather than the originally observed 6 because the GAP-6
widening now accepts its `C3 step 4 + C4 step 4` composition head — one of the six was a
composition, not a form defect.

**Absence is not agreement.** An analysis with no verdict blocks returns no findings rather than
a clean bill: a missing self-audit is a disclosure defect owned by the agent body's "say so
explicitly at the top of the response" rule, and recoding it as agreement here would hide it.

## Promotion

| Target | Cost | Note |
|---|---|---|
| `tests/routing-catalog.md` | low | Adds 4 DELEGATE rows. Scores routing only — would not test the premise axis at all. |
| `tests/quality-catalog-v8.7.md` | **blocked** | That catalog's pre/post comparison is a matched pair over exactly Q-P1/Q-P2/Q-P3 (D-07). Adding rows breaks the same-prompt property the v8.7 baseline freeze depends on. Use a new `v8.x` catalog instead. |
| `tests/step0-fixture-catalog.md` | low | Adds `full-composer` classification rows; STEP0-08 asserts named pairs, not row counts. |
| New judged catalog + baseline | medium | The only target that actually scores the premise axis. Needs a frozen baseline like `tests/quality-baseline-v8.7/`. |
