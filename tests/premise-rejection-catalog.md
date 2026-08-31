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

## Third run — PR-P1, 2026-08-31 (n=1), first run with verified provenance

Re-run while verifying the three columns appended to `_DEFECT_RECORD_FIELDS`. **This is the
first PR-P1 run whose agent body is known.** It was dispatched through
`check-quality-harness.py --probe` over the Plan-36-locked `claude -p --plugin-dir
first-principles` transport, so it read the working tree at 8.23.0.

**The two runs above did not.** Both were dispatched through the in-session `Agent` tool,
which resolves to the installed plugin; `~/.claude/plugins/installed_plugins.json` pins that
to a cache of commit `5fc9edd` at **v8.20.0**, and that cached agent body does not contain the
arrow-led wrap rule at all. Either the session was launched with an override this transcript
does not record, or run 2's improvement is not attributable to the fix it is recorded against.
**The "Post-fix re-run" section above should be read with that caveat**; it is left unedited
because which body ran is not established either way, and rewriting it on a guess would
replace one unsupported attribution with another. Run 3 is confounded against both prior runs
on two axes at once (plugin version and transport) and is not a matched comparison.

| Axis | run 1 | run 2 | run 3 |
|---|---|---|---|
| Provenance | Agent tool, body unknown | Agent tool, body unknown | `--plugin-dir`, **8.23.0 verified** |
| Chain blocks / malformed | 6 / 5 | 7 / 0 | 5 / **0** |
| §6 claims / untraced | 8 / 1 | 7 / 0 | 4 / **0** |
| Verdict cells / non-conforming | 15 / 0 | 16 / 0 | 16 / **0** |
| Dependency cycles / ungrounded | 0 / 0 | 0 / 0 | 0 / 0 |
| Self-audit disagreements | 2 | 0 | **0** |
| §2 premise verdict | A1 `convention` → Discard | A1 `convention` → Discard | A1 `convention` → **Discard**, refuted by GT-4 read-at-source |

The premise axis passes a third time, on a verified body. GAP-1 — that no gate locks this in —
is unchanged.

### The ledger blind spot (GAP-7) — FIXED

Run 3 scored `claims 14, untraced 3, selfaudit_disagreements 1` before the fix. All three
findings were artifacts of one detector defect, not properties of the analysis.

Run 3 traced its Conclusion through an explicit `§6→§4 closure ledger` — each claim quoted
beside the chain that produced it — rather than through inline parentheticals:

```text
- "Lambda is 2.10× more expensive per unit of actual compute than Fargate"  → chain C1 ✓
```

`_conclusion_claims` mined the ledger's ten rows as ten additional claims, and
`_claim_is_traced` — which only accepts a citation found *inside* the claim text — left the
three prose claims those rows discharged counted as untraced. `selfaudit_calibration` then
reported Criterion 6 as an over-claim.

**Criterion 6 does not require an inline citation.** Its Rigorous band requires that every
Conclusion claim "traces to a specific named derivation chain in section 4" and says nothing
about where the citation sits; `output-template.md` §6 prescribes three prose blocks and gives
no citation instruction at all. A ledger discharges that obligation at least as well as a
parenthetical. So an analysis that traced its claims *more* explicitly scored worse on both
numerator and denominator — and the newly widened schema converted the detector's blind spot
into a charge against the agent.

**This is the 8.23.0 Criterion 4 finding with the surfaces reversed.** There, the rubric scored
only semantics and the agent's Rigorous verdict was defensible — the rubric was the defect. Here
the rubric is right and the instrument is wrong. Both were found the same way: by disagreeing
with a self-report and then asking which side was mistaken rather than assuming it was the agent.

**Fix (`scripts/check-quality-harness.py`), two independent halves:**

1. `_conclusion_claims` skips fenced code blocks — verbatim structural content, not §6 prose.
   This is general: any fenced formula or captured snippet in §6 was being mined for claims.
2. `_claim_is_traced` accepts a closure-ledger entry, via a new `ledger_fragments` parameter
   that defaults empty so every prior call site keeps its exact behaviour.

**Credit is deliberately narrow**, because a rule that credited any ledger-shaped line would
let an agent discharge its whole Conclusion with three cosmetic rows. An entry must cite a
chain id that actually appears in section 4 (so a ledger cannot invent its own authority),
quote at least four content tokens (so `"serverless is cheaper"` identifies no particular
claim), and cover 70% **of the fragment's** tokens — measured over the fragment and never the
claim, so a long claim cannot earn credit by being long enough to contain a short unrelated
quote. Overlap rather than substring, because a ledger paraphrases lightly: `"Lambda is 2.10×
more expensive …"` against a claim reading `"… it is 2.10× more expensive …"`.

**Verification.** Pinned by `_selftest_ledger_traceability` (self-test Item 17), ten controls:
three positive/fault-injection, four anti-overreach, one discriminating the fence rule from the
claim filter, one frozen-corpus movement pin. Five fault injections — removing the fence skip,
dropping the ledger clause, dropping the minimum-fragment guard, measuring coverage over the
claim, dropping the chain-citation requirement — each fail the sub-check on the control that
owns it.

**Measured movement.** Run 3 goes to `claims 4, untraced 0, selfaudit_disagreements 0`. Runs 1
and 2 are byte-unchanged: neither has a fenced §6 block or a ledger. The frozen v8.7 corpus is
unchanged on both axes — `_CALIBRATION_CONCLUSION_CLAIMS` `[9, 9, 8, 5, 6, 4]` and
`_CALIBRATION_UNTRACED_CLAIMS` `[4, 5, 6, 3, 3, 4]`, measured before the change and re-measured
after. Those two pins are new: `_CALIBRATION_UNTRACED_FLAGS` is saturated at `[1]*6` and is
structurally blind to this axis, and two of the five injections above move the corpus and are
caught by nothing else.

## Fourth run — PR-P1, 2026-08-31 (n=1), v8.24.0 verified body

Dispatched through `check-quality-harness.py --probe` over the same Plan-36-locked transport as
run 3, so the body is verified: `DEFAULT_PLUGIN_DIR` is the repo-relative `first-principles/`,
which was sync-clean at commit `3f41fbc`, **v8.24.0**. This is the first matched pair in the
series — run 3 and run 4 differ in plugin version and in nothing else about the transport.

The capture is **not committed**. It lives at `…/scratchpad/prp1-rerun/PR-P1.{md,jsonl}`, a
location subject to reaping, and every finding below is stated so that GAP-8, GAP-9 and GAP-10
reproduce from the snippets quoted here without it. Only GAP-11 needs the capture. Freezing run 4
as a second provenance fixture is an open decision, not a step already taken.

| Axis | run 1 | run 2 | run 3 | run 4 |
|---|---|---|---|---|
| Provenance | Agent tool, body unknown | Agent tool, body unknown | `--plugin-dir`, 8.23.0 | `--plugin-dir`, **8.24.0** |
| Chain blocks / malformed | 6 / 5 | 7 / 0 | 5 / 0 | 8 / **8** |
| §6 claims / untraced | 8 / 1 | 7 / 0 | 4 / 0 | 9 / **0** |
| Verdict cells / non-conforming | 15 / 0 | 16 / 0 | 16 / 0 | 24 / **3** |
| Dependency cycles / ungrounded | 0 / 0 | 0 / 0 | 0 / 0 | **8 / 8** |
| Self-audit disagreements | 2 | 0 | 0 | **3** |
| Provenance labels / literals located | n/a | n/a | 7 / 35 | **0 / 0** |
| §2 premise verdict | A1 `convention` → Discard | A1 `convention` → Discard | A1 `convention` → Discard | A1 `convention` → **Discard** |

**The premise axis passes a fourth time.** Routing reached `DELEGATE` (one `Agent` block in the
capture), §1 recovered the cost question without naming Lambda migration, and A1 was classified
`convention` and discarded. GAP-1 — that no gate locks this in — is still unchanged.

**Every other column moved the wrong way, and three of the four causes are instrument defects
rather than analysis defects.** That ratio is the reason this section is longer than the run it
describes. The one genuine agent deviation is GAP-10.

**n=1, and the two runs are not interchangeable samples.** Run 4 is the longer analysis by content
(8 chains against 5, 24 assumption rows against 16) and the shorter by bytes (32,446 against
35,312). Whether it is *better* is not established here and is not decidable by `detect_defects`,
which counts structural conformance; the governing record demotes even K-of-5 from this class of
harness to a recorded observation (`docs/v8.7-constraint-teardown.md` §2 item 3), and this is n=1.

### Bold chain labels defeat the self-reference guard (GAP-8) — OPEN

`_chain_head_refs` skips a block's own label line before reading the head, and its comment names
the exact failure the skip prevents:

> Skip the block's own markdown heading. `_chain_blocks` starts each block at its heading line,
> and that line carries the chain's OWN id (`### Conclusion C1:`) — reading it as a head would
> make every composing chain self-referential and report the whole section as one cycle.

That is precisely what run 4 produced. The guard is `if s.startswith("#")`, but the label layer
accepts **two** forms — `_CHAIN_HEADING_RE` (hash-led) and `_CHAIN_BOLD_RE` (bold-led, no
hashes) — and `_chain_blocks` starts each block at whichever matched. The guard covers the first
form only. Run 4 labelled its chains `**C1 — The premise is false as a general claim. …**`, so
the label line was read as the head:

| Block, first chain | `_chain_head_refs` |
|---|---|
| run 3, `### Conclusion C1: …` | `({GT-1, GT-2, GT-3, GT-6}, set())` |
| run 4, `**C1 — …**` | `(set(), {'C1'})` |

Every chain therefore cites itself and no ground truth, giving 8 self-edges and 8 unreachable
chains — `_dependency_cycles` and `_ungrounded_chains` both report all of `c1`–`c8` — and one of
the three self-audit disagreements (Criterion 4 contradicted by `_dependency_cycles`). **All of it
is artifact.** Stripping only the bold label line from run 4's C1, changing nothing else, returns
`({GT-1, GT-3, GT-5}, set())`.

The guard was correctly reasoned and keyed to the wrong property: markdown heading *syntax*,
rather than *is this the block's own label line*. `_chain_ids` and `_chain_head_refs` disagree
about what a label is, and the disagreement is invisible while every analysis uses hash headings.

**Measured fix direction — prototyped, deliberately NOT applied.** Widening the guard to
`s.startswith("#") or _CHAIN_BOLD_RE.match(s)`:

| Surface | Before | After |
|---|---|---|
| run 4 cycles / ungrounded | 8 / 8 | **0 / 0** |
| run 4 self-audit disagreements | 3 | **2** (Criterion 4 vs `malformed_chain_blocks` correctly survives — that is GAP-9) |
| run 3, all columns | — | unchanged |
| frozen v8.7 corpus, all six analyses, every column | — | unchanged; `malformed [2, 2, 2, 2, 3, 3]` still matches `_CALIBRATION_MALFORMED_CHAIN_BLOCKS` |

It is left unapplied because the missing work is the controls, not the line: a positive control on
a bold-labelled composing chain, and an anti-overreach control proving a genuinely bold-led *head*
line is not swallowed by the widened guard.

**Failure direction: false positive.** Unlike GAP-5 and GAP-11, this defect reports defects that
are not there, so it cannot hide a real one. It is the safer direction and is still wrong.

### A wrapped hop is unrepresentable under the prescribed chain form (GAP-9) — OPEN

`_chain_block_well_formed` absorbs a following line into the candidate segment only while that
line is arrow-led, and `_CHAIN_FORM_LINE_RE` then requires two arrows in the joined candidate. A
single hop wrapped across physical lines emits a continuation that is *not* arrow-led — it is the
middle of a bracket — so the join stops there and the candidate retains one arrow. All 8 of run
4's chains fail this way. Unwrapping C1's brackets onto single lines, content otherwise unchanged,
flips it to `True`.

**The head-form difference between the two canonical surfaces was measured and is not the cause.**
`SKILL-body.md:208` renders the head as `GT-1 + GT-6 → [intermediate claim]` and
`output-template.md:131` renders it as `GT-1 (label) + GT-6 (label)` with the first arrow on the
next line. Crossing head form against wrap over four minimal probes:

| Head form | hop on one line | hop wrapped |
|---|---|---|
| `GT-1 + GT-3 → [claim]` (`SKILL-body.md`) | True | **False** |
| `GT-1 + GT-3 (label)` / `→ [claim]` (`output-template.md`) | True | **False** |

Both forms fail identically. The surfaces do differ and should be reconciled on their own merits,
but that difference is inert here — **the cause is the wrap, and neither surface says a hop may
not wrap.** Both state the rule as *every line after the head begins with `→`*, which is literally
true and is satisfiable only by never breaking a hop across lines. Neither says so.

So the rule as written is unimplementable for a long intermediate, and which runs pass is decided
by an undocumented rendering preference:

| | run 3 | run 4 |
|---|---|---|
| §4 longest line | 479 chars | 514 chars |
| §4 lines over 200 chars | 23 | 3 |
| malformed chains | 0 / 5 | 8 / 8 |

Run 3 passed by emitting 479-character unwrapped lines. Run 4 wrapped near 90 columns. Neither was
told which to do, and the difference is the entire delta on this axis.

**Resolution is a real choice and is not made here.** Either (a) state the no-wrap rule explicitly
on both surfaces, which makes the instrument correct at the cost of prescribing very long lines,
or (b) teach the join bracket-awareness so a continuation inside an unclosed `[` is absorbed. (b)
touches hardened code: `_chain_block_well_formed`'s Phase 184-03/184-04 history records a
head-arrow guard that was tried and reverted for keying on *where the line break fell* rather than
on whether the absorbed line belonged to the same claim, which is close enough to (b) that it
should be read before attempting it.

The second self-audit disagreement (Criterion 4 contradicted by `malformed_chain_blocks`) is
downstream of this and is **correct given the mechanical record** — it survives the GAP-8 fix, and
should, until this one is resolved.

### Run 4 hoisted an expiry qualifier into the verdict token (GAP-10) — OPEN

The one finding on this run that is an agent deviation rather than an instrument defect. Three
Verdict cells do not conform:

```text
**Accept with expiry** — lifts only if AWS introduces a Lambda spot/preemptible tier; none exists today
**Accept with expiry** — lifts only if AWS decouples the dials
**Accept with expiry** — lifts if you adopt scheduled scale-to-zero on ECS
```

`_VERDICT_VOCAB` is exactly `accept | challenge | discard` and `_VERDICT_FORM_RE` requires the
token to lead and be followed immediately by U+2014. `Accept with expiry` is a fourth token the
Verdict Vocabulary does not define.

**This is not a hole in the contract, which is what it first looks like.** All three rows are type
`current constraint`, whose prescribed treatment is *"record the expiry conditions"* — so the
template does prescribe a treatment the verdict vocabulary has no dedicated token for, and the
obvious reading is that the agent filled a gap. Run 3 refutes that reading. It carried **four**
`current constraint` rows on this same prompt and rendered every one conformingly, by putting the
expiry in the justification where it belongs:

```text
**Accept** — expires at term end (1 or 3 years)
**Challenge** — expires if you run outside us-east-1; per-region rates differ, and AWS revises them
```

The vocabulary is adequate and was demonstrated adequate one milestone earlier on the identical
case. Run 4 moved the qualifier from the justification into the token slot, three times.

Criterion 2's self-audit claimed **Rigorous** and was contradicted by `nonconforming_verdict_cells`
— the third disagreement, and the only one of the three that is **correct on both sides**: the
mechanical record is right and the self-report is wrong. Its justification asserts *"Verdicts lead
with Accept/Challenge/Discard"*, which is false for three of its own 24 rows.

**Candidate fix, not taken:** the Verdict Vocabulary bullets give a worked example for each token;
none of the three shows an expiry. Adding `Accept — expires at <condition>` to the **Accept**
bullet would demonstrate the form at the point of use. Widening `_VERDICT_VOCAB` instead is the
more expensive option — it moves the 267-cell census `_VERDICT_FORM_RE`'s separator policy is
calibrated against — and run 3 is evidence it is unnecessary.

### PROV-GUARD reports clean on an analysis it parsed nothing from (GAP-11) — OPEN

The most serious of the four, because it fails green. On run 4 the verifier returns:

```text
provenance_labels 0, unmatched_sources 0, unreadable_sources 0, literals_checked 0,
unlocated_literals 0, misattributed_literals 0, zero_literal_gts 0, orphan_fetches 7,
provenance_flag 0
```

`provenance_flag=0` is PASS. It was reached by parsing **zero** ground truths out of a section 3
containing sixteen, twelve of them `read-at-source` labelled.

Two independent form dependencies, either sufficient alone:

| Symbol | Requires | Run 4 wrote |
|---|---|---|
| `_GT_LINE_RE` (`check-provenance.py:127`) | `- **GT-n**` list item | `1. **GT-n** — …` |
| `_READ_AT_SOURCE_LABEL` (`:133`) | `*Provenance: read-at-source.*`, period **inside** the emphasis | `*Provenance: read-at-source* — aws.amazon.com/…` |

Measured by normalizing only the list marker and the label period, leaving all content untouched:
12 labels are then found, and all 12 report `unmatched_sources` — a third dependency, in
`_source_string`, which expects run 3's `— source: <url>; read-at-source: <location>` clause shape
rather than run 4's source clause trailing the label.

**The provenance itself is real.** The capture carries six `WebFetch` calls — `lambda/pricing`,
`fargate/pricing`, the Lambda quotas doc, `savingsplans/compute-pricing`, `ec2/spot`, and
`ec2/pricing/on-demand` — and every source run 4 cites corresponds to one of them. The sixth is
recorded in the analysis as a **failed** read (*"the page returned pricing methodology but not the
rate matrix… Reason: citation does not support the claim"*) with no ground truth asserted from it.
An analysis that reported its own failed read honestly scored zero on the instrument built to
check exactly that.

**Nothing in the gate observes the dependency, on either leg.** The live leg reads a single
committed fixture in a single rendering, so its `7/7 sources matched, 35/35 literals located` is a
statement about that document's style. The 24 self-test controls are tempdir/in-memory and are
built by `_gt_line`, whose docstring states it emits *"the exact form `_GT_LINE_RE` /
`_source_string` / `_label` parse"* — the same bullet-and-period form as the fixture. Positive and
negative controls alike share the rendering whose variation breaks the gate.

This is the same class as GAP-5 and the same direction: **silently green.** The README's framing of
PROV-GUARD as *"the first check in the stack that can falsify a `read-at-source` label"* holds only
for analyses rendered like the fixture.

**The smallest fix is not a wider regex.** A zero-coverage floor — an analysis that yields zero
parsed ground truths, or zero labels against a capture containing fetches, must not be able to
return PASS — is independent of how many renderings the parser accepts, and it converts every
future rendering surprise from a silent pass into a loud failure. Widening `_GT_LINE_RE` to admit
ordered-list items and relaxing the label period are then improvements rather than load-bearing
guesses. Neither is applied here.

## Promotion

| Target | Cost | Note |
|---|---|---|
| `tests/routing-catalog.md` | low | Adds 4 DELEGATE rows. Scores routing only — would not test the premise axis at all. |
| `tests/quality-catalog-v8.7.md` | **blocked** | That catalog's pre/post comparison is a matched pair over exactly Q-P1/Q-P2/Q-P3 (D-07). Adding rows breaks the same-prompt property the v8.7 baseline freeze depends on. Use a new `v8.x` catalog instead. |
| `tests/step0-fixture-catalog.md` | low | Adds `full-composer` classification rows; STEP0-08 asserts named pairs, not row counts. |
| New judged catalog + baseline | medium | The only target that actually scores the premise axis. Needs a frozen baseline like `tests/quality-baseline-v8.7/`. |
