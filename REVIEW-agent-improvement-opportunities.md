# Review of the demo run: agent and harness improvement opportunities

Reviews the analysis captured in `DEMO-first-principles-ticket-triage.md` (run at HEAD `3c3ed42`,
plugin `9.2.1`, via `--plugin-dir first-principles`) for chains that do not hold and for gaps in
the measurement apparatus. Findings are tiered `product` / `apparatus` per
[docs/PROCESS.md](docs/PROCESS.md) §2 and CLAUDE.md's review protocol.

Every finding below was established against the artifact or the source, never inferred from the
run's own self-report — which turned out to matter, because the self-report is one of the findings.

```yaml
findings:
  product:   {critical: 3, warning: 1, info: 2}
  apparatus: {critical: 1, warning: 3, info: 0}
  total: 10
blocking: 3        # product only
status: issues_found
```

---

## R1 — Root cause: the run opened zero reference files

**Tier:** product · **Severity:** critical · explains P1, P3 and P4

The capture contains sidechain events for the subagent's own turns (6 `assistant`, 7 `user`,
15 `tool_progress`), so its tool calls are visible in full. The complete census:

```
ALL tool_use across every event: {'Agent': 1, 'Skill': 1, 'ToolSearch': 1, 'Bash': 1, 'WebFetch': 3}
Read/Grep/Glob calls: NONE
```

The agent never opened `validation-rubric.md`, never opened `output-template.md`, and never opened
any companion-technique reference or `-detail.md` appendix. It nonetheless emitted a six-criterion
Self-Audit Gate, an Assumption Audit scan, a self-audit scan and a §6→§4 closure ledger — all
structurally plausible, all reconstructed from the body's prose.

**Why that is decisive.** Every format the run deviated from exists *only* in the files it did not
open:

| Token | occurrences in `SKILL-body.md` | in the reference that defines it |
|---|---|---|
| `Rigorous` | **0** | 18 (`validation-rubric.md`) |
| `Sound` | **0** | 13 |
| `Hand-wavy` | **0** | 20 |
| `Band:` | **0** | 2 |
| `Quoted span` | **0** | 3 |
| `Confidence:` | **0** | 2 (`output-template.md`) |
| `Unverified input rule` | **0** | 1 |
| `GT-N?` | 5 | 7 |

The last row is the control. `GT-N?` is the one concept in this set that the body states inline —
and the run applied `?`-marking correctly and pervasively (6 of 16 ground truths, propagated into
chain confidence lines). The concepts available only by reading were the concepts not applied. This
is not a capability limit.

**The internal contrast that names the fix.** Two phases in the same body ask the agent to open
something. They are written differently, and they produced opposite outcomes in this one run:

- **Phase 3** (`SKILL-body.md:145`) is an explicit read imperative that names its tools:
  *"**Acquire the evidence — attempt the read before assigning the label.** … attempt to open the
  cited source directly, with Read for a local path or repository file, Grep to locate the asserted
  figure or wording within it, or WebFetch for a URL, before recording the provenance label."*
  → **It worked.** Three WebFetches, eight `read-at-source` ground truths, and a Phase 3 failure
  record written for the 404.
- **Phase 5** (`SKILL-body.md:295-298`) delegates via a bare markdown link:
  *"Score the completed analysis against the criteria in the [Self-Audit Gate](…/validation-rubric.md)
  as a feedback loop… Do not re-author the criteria here; apply them."*
  → **It did not.** Zero reads; the criteria were re-authored, which is the one thing the sentence
  forbids.

There is precedent for this exact surface failing: CLAUDE.md's key-invariants section records that
at v8.14.0 *"the Phase 5 Self-Audit Gate never fired"* because agent-body reference links resolved
against the session working directory. That was fixed by anchoring links with
`${CLAUDE_PLUGIN_ROOT}`. **This is a different failure with the same blast radius** — the link is
correctly anchored now and the gate did fire, but nothing was read, so it fired against invented
criteria. A link that resolves is not a read that happens.

**Fix.** Rewrite the Phase 5 step as a read imperative in Phase 3's voice — name the tool, and put
the read before the scoring, not beside it. Phase 3's wording is the working template and is
already in the file.

---

## Product findings

### P1 — Two chains rated HIGH while consuming unverified ground truths

**Tier:** product · **Severity:** critical · **Blocking**

The rule is stated twice, on two canonical surfaces:

- `output-template.md:335` — *"**Unverified input rule (D-07):** A chain that includes any `GT-N?`
  input must end with a MEDIUM or LOW confidence line… **A HIGH confidence claim cannot rest on an
  unverified ground truth.**"*
- `validation-rubric.md:419` — *"no chain that consumes a GT-N? input is rated HIGH confidence."*

Extracted labels and heads from the artifact:

| Chain | Label | Head | D-07 |
|---|---|---|---|
| C1 | **HIGH** | `GT-1 + GT-9?` | **violated** |
| C2 | HIGH | `GT-1 + GT-2` (both read-at-source) | clean |
| C3 | MEDIUM | `C2 + GT-9? + GT-11?` | clean — correctly demoted |
| C4 | HIGH | `GT-14 + GT-15` (identities) | clean |
| C5 | MEDIUM | `GT-10? + GT-16?` | clean |
| C6 | MEDIUM | `GT-3 + GT-5 + GT-6` (all read-at-source) | clean — demoted on *assumptions*, correctly |
| C7 | **HIGH** | `GT-2 + GT-4 + GT-13?` | **violated** |
| C8 | **HIGH** | `C3 + C6 + C5` (all MEDIUM) | see P2 |

C1 and C7 are direct violations. Under `validation-rubric.md:442` this is precisely the **Sound**
band descriptor — *"a chain is rated HIGH confidence while consuming a GT-N? input (the rating does
not match the unverified-input rule)"* — so Criterion 5 should have banded Sound. It reported
neither Sound nor Rigorous; see P3.

Worth noting that C3, C5 and C6 are demoted *correctly*, and C6's demotion is the subtle one: its
head is entirely read-at-source and it is MEDIUM because of two unverified *assumptions* (A9, A11).
The agent understands the rule. It applied it to five chains and not to two.

### P2 — The decision chain is rated HIGH while composed of three MEDIUM chains

**Tier:** product · **Severity:** critical · **Blocking** · *specification gap, not just a slip*

C8 — *"the decision"*, the chain the entire recommendation rests on — is labelled **HIGH** and its
head is `C3 + C6 + C5`. All three inputs are MEDIUM, and their MEDIUM status traces to four
`?`-marked ground truths (GT-9?, GT-10?, GT-11?, GT-16?).

**This is compliant with D-07 as written**, and that is the finding. D-07 forbids a HIGH chain that
*"includes any `GT-N?` input"* — a token-level test. C8's head cites no `GT-N?`; it cites chains.
The rubric's nearest neighbour (`validation-rubric.md:417`) constrains *"the overall Conclusion
section's confidence rating"* to match the weakest contributing chain, which is a different object
from a chain-on-chain composition.

So the most consequential confidence claim in the document passes the letter of a rule written to
prevent exactly it. Confidence is being treated as a label attached to a chain rather than a
property propagated through one.

**Fix.** Add a transitivity clause to D-07 and to the Criterion 5 Rigorous descriptor: a chain
whose head cites another chain inherits the minimum confidence of every cited chain, and a chain's
label may never exceed that minimum. One sentence in each of the two sources; the concept is
already there, only the composition case is missing.

### P3 — All six verdict blocks non-conforming, in a vocabulary that does not exist

**Tier:** product · **Severity:** critical · **Blocking** · *this is why P1 went unreported*

Prescribed (`validation-rubric.md:170-181`):

```text
**Criterion N: [Criterion Name]**
Quoted span: "[…]"
Band: [**Rigorous** / **Sound** / **Hand-wavy** / **Absent**]
Justification: […]
```

Emitted:

```text
**Criterion 1 — Problem Essence: PRESENT.** Section 1 distils past the asked question…
```

Four deviations on every one of the six blocks: the colon follows the criterion *name* rather than
the number; no `Quoted span:` line; no `Justification:` line; and no `Band:` line — because
**`PRESENT` is not a band.** `/usr/bin/grep -rn "PRESENT"` over both `SKILL-body.md` and
`validation-rubric.md` returns nothing: the vocabulary was invented, not misapplied.

**The consequence is the real defect, not the formatting.** The gate's four bands are where the
substantive checks live — the D-07 rule that catches P1 is a clause *inside* the Rigorous and Sound
descriptors. Replacing a four-band quality scoring with a binary presence test means those
descriptors were never applied. The gate reported six passes without running the checks that
constitute it.

And the Criterion 5 verdict it did emit is false three ways in one sentence:

> *"Criterion 5 — Conclusion: PRESENT. Every conclusion traces to a chain; the two HIGH-confidence
> conclusions (C2's 40% ceiling, C6's dominance threshold) rest only on read-at-source pricing."*

- "the **two** HIGH-confidence conclusions" — the document labels **five** chains HIGH (C1, C2, C4, C7, C8).
- it names **C6**, which the document labels **MEDIUM**.
- "rest only on read-at-source pricing" — false for C1 (GT-9?) and C7 (GT-13?).

Also note the gate's clearing conditions are *"no criterion scores Absent"* and *"at most one
criterion scores Hand-wavy"*. Against a PRESENT/absent vocabulary those conditions are
unevaluable, so the reported pass is not a pass on the rubric's own terms.

### P4 — No per-chain `**Confidence:**` lines, and no chain states what would raise it

**Tier:** product · **Severity:** warning

`Confidence:` occurs **0 times** in the output. The template prescribes a trailing
`**Confidence:** [HIGH / MEDIUM / LOW]` line per chain (`output-template.md:332`), and requires
that a MEDIUM or LOW line *"name the unverified input and state what verification would raise
confidence to HIGH"*.

The run carried confidence in heading parentheticals instead — `*(MEDIUM — rests on GT-11?, A15)*`.
That half-satisfies the rule: the causing input **is** named on every demoted chain, which is the
harder half. What is missing everywhere is the remediation half — no chain says what verification
would lift it. Given C7 exists precisely to price the missing measurement, the information was
available and simply not routed into the confidence lines.

Secondary effect worth recording: `**Confidence:**` is a load-bearing string elsewhere in the
toolchain — `_extract_heading_block` uses it as a block terminator (`check-quality-harness.py:9772`)
and raises `_ContractAnchorError` when it is absent. That path reads templates rather than analyses
today, so nothing broke; an emission with zero such lines is nonetheless a shape the toolchain
assumes exists.

### P5 — C6's arithmetic uses a number its own assumption does not license

**Tier:** product · **Severity:** info

A9 is stated as *"a stable prefix is **≥50%** of the 2,400 input tokens"*. C6's arithmetic uses
**70%**. A lower bound does not license a point estimate at the favourable end of it.

Recomputed at the bound the assumption actually states:

```
prefix 70%: cached input $5,328  cache-only $23,328   + effort=low -> $11,328  (65% cut)
prefix 50%: cached input $7,920  cache-only $25,920   + effort=low -> $13,920  (57% cut)
```

**The conclusion survives** — 57% still beats the proposal's 40%, so C6's dominance finding holds
at the weak end of its own assumption. The defect is that the chain does not say so. Stating the
bound and computing at the midpoint understates the chain's robustness while overstating its
precision, and the 65% figure is quoted in the Conclusion without its range.

### P6 — `p = 0.85` enters C4 as an unflagged assumption

**Tier:** product · **Severity:** info

C4 step 1 reads *"at p = 0.85 the independent-error formula yields 0.939"*. Haiku's per-call
accuracy is the quantity the analysis elsewhere insists has never been measured (GT-13?). The
Assumption Audit scan records that step as `— | n/a` — a clean pass, no assumption surfaced.

It is used only to reconstruct the staff engineer's reasoning, not to support a conclusion, so
nothing downstream is contaminated. But the audit's own rule is exhaustiveness over every chain
step, and "assume Haiku is 85% accurate" is an assumption by any reading.

---

## Apparatus findings

### H1 — `detect_defects` has no confidence dimension at all

**Tier:** apparatus · **Severity:** critical (for the instrument, not the product)

The detector's ten columns are `conclusion_claims`, `untraced_claims`, `verdict_cells`,
`nonconforming_verdict_cells`, `chain_blocks`, `malformed_chain_blocks`, `dependency_cycles`,
`ungrounded_chains`, `selfaudit_disagreements`, and the provenance group. **None of them reads a
confidence label.** `_chain_block_well_formed` is shape-only — arrow form, GT heads, table-row and
sentence-boundary refusals — and says nothing about HIGH/MEDIUM/LOW.

So P1 and P2 — a rule stated twice on canonical surfaces, with a band descriptor written expressly
to score its violation — are mechanically invisible. The detector gave this analysis a clean
reading on every dimension it has (0 untraced, 0 malformed, 0 cycles) while three confidence
defects sat in it.

**Fix.** Three columns, all computable from the emission alone, which is the detector's own
admissibility standard:

- `high_conf_chains` — count of chains labelled HIGH.
- `high_conf_unverified_head` — HIGH chains whose head cites a `GT-N?`. Would have caught P1 (=2).
- `confidence_inversions` — chains whose label exceeds the minimum label of the chains their head
  cites. Would have caught P2 (=1).

The label is already parseable in both emitted shapes (trailing `**Confidence:**` line and heading
parenthetical), and chain heads are already extracted by `_chain_blocks`.

### H2 — The self-audit reconciliation structurally cannot see Criterion 5

**Tier:** apparatus · **Severity:** warning

```python
_SELFAUDIT_CONTRADICTIONS: dict[int, tuple[str, ...]] = {
    2: ("nonconforming_verdict_cells",),
    4: ("malformed_chain_blocks", "_dependency_cycles"),
    6: ("untraced_claims",),
}
```

Criteria 2, 4 and 6 are reconciled against measurement. **Criterion 5 has no entry** — and
Criterion 5 is where every confidence rule lives. A false Criterion 5 self-report is therefore
unreconcilable by construction, which is exactly what P3's three-way-false sentence is.

The absence is honest rather than careless: there was no mechanical field to reconcile against,
because of H1. Fix H1 and this becomes a one-line addition — `5: ("high_conf_unverified_head",
"confidence_inversions")`.

### H3 — The reconciliation's live reach is 1 in 7, and its `0` cannot be told from agreement

**Tier:** apparatus · **Severity:** warning · *anti-masking*

`_selfaudit_bands` requires `^\*\*Criterion N:…\*\*$` plus `^Band:\s*\*\*(Rigorous|Sound|Hand-wavy|Absent)\*\*`.
Run across every analysis the project has measured:

```
analysis                    bands parsed
condA-P1                               0    <- reconciliation vacuous
condA-P2                               0    <- vacuous
condA-P3                               0    <- vacuous
condB-P1                               0    <- vacuous
condB-P2                               0    <- vacuous
condB-P3                               6    {1..6: Rigorous}
DEMO-TRIAGE (this run)                 0    <- vacuous
```

**The mechanism is sound.** On `condB-P3`, the one analysis it can parse, it fires correctly:
3 disagreements, against a self-report of Rigorous on all six criteria with 15 nonconforming
verdict cells, 3 malformed chains and 4 untraced claims in the mechanical record. The logic works.

**The reach is the defect.** On 6 of 7 measured artifacts it parses nothing and writes `0` into
`selfaudit_disagreements` — the same value it writes for genuine agreement. The docstring is
explicit that this must not happen (*"absence of a self-audit is a separate defect… and is not
silently recoded as agreement here"*), and in the function's return value that holds: it returns
`[]`. The masking is in the TSV, where `[]` and "reconciled, agreed" both render as `0`.

That is a mechanism built to catch a self-report contradicting the record — the docstring cites the
2026-08-30 observation of an analysis self-scoring Rigorous with every chain malformed — sitting
blind on six of seven cases without saying so.

**Fix.** Two parts, both small: (a) add a `selfaudit_bands_parsed` column so `0 disagreements / 0
parsed` is distinguishable from `0 disagreements / 6 parsed`; (b) widen the criterion-head regex to
the forms actually emitted (em-dash separator, name-then-colon) and treat a parsed criterion with a
non-vocabulary verdict word as its own finding rather than as no claim — `PRESENT` should surface as
"claimed a band outside the vocabulary", not vanish.

### H4 — HC-BOUND proves the bound is *written*, not *obeyed* — and says so honestly

**Tier:** apparatus · **Severity:** warning

`check-high-confidence-bound.py --describe` reports its registered surfaces as exactly the two
`validation-rubric.md` copies. It is a structural gate over rubric text: it verifies the
HIGH-confidence tightening is present and well-formed on both surfaces and that all three
documented EXCEPT exceptions exist. It reads no analysis output, so it cannot observe P1.

**This is a coverage gap, not a false claim, and the distinction is worth stating plainly** because
the project has been burned by the other kind twice this week. CLAUDE.md's gate row describes
HC-BOUND as a *"Structural validation gate"* checking the bound *"is present and well-formed on
both rubric surfaces"*. That description is accurate. Nobody published a claim that the bound is
enforced on output. The gap is that the rule with two canonical statements and a dedicated CI gate
has no instrument anywhere that reads an actual analysis — which H1 closes.

### H5 — Nothing measures whether a run opened its reference files

**Tier:** apparatus · **Severity:** warning · *highest leverage missing instrument*

R1 was detectable only because I walked the raw `.jsonl` by hand. No script, gate or column records
how many reference files a run opened, and a run that opens zero is indistinguishable — in the
analysis, in the TSV, in every committed artifact — from one that opens all of them.

Given that the v8.14.0 precedent recorded in CLAUDE.md is *this same surface silently not firing*,
and that the on-demand `-detail.md` architecture (`SLUGS_WITH_DETAIL`, GATE-02-v8.5) deliberately
moved content *out* of the always-loaded body and behind pointers, the number of reference reads per
run is the load-bearing unmeasured quantity for the whole design. GATE-02-v8.5's own published
description concedes the boundary in as many words: it *"proves the pointer exists and is
well-formed, NOT that it is followed."*

**Fix.** A `reference_reads` census over the capture, in the shape the provenance group already
uses: per run, the set of `references/*.md` paths opened with Read, and the count. Cheap — the
parser is ~20 lines over the same `.jsonl` the provenance columns already walk — and it converts
"is the on-demand architecture actually used?" from an assumption into a reading.

---

## Priority order

| # | Change | Tier | Closes | Cost |
|---|---|---|---|---|
| 1 | Rewrite Phase 5's rubric consultation as a read imperative, in Phase 3's voice | product | R1, and thereby P3/P4 and most of P1 | one paragraph in `SKILL-body.md` |
| 2 | Add `high_conf_chains`, `high_conf_unverified_head`, `confidence_inversions` to `detect_defects` | apparatus | H1; makes P1/P2 mechanically visible | one function + 3 columns + self-test fixtures |
| 3 | `selfaudit_bands_parsed` column; widen criterion-head regex; non-vocabulary verdict as a finding | apparatus | H3 | small, in the same module |
| 4 | Add `5:` to `_SELFAUDIT_CONTRADICTIONS` pointing at #2's fields | apparatus | H2 | one line, after #2 |
| 5 | D-07 transitivity clause in `output-template.md` + Criterion 5 Rigorous descriptor | product | P2 | one sentence in each of two sources |
| 6 | `reference_reads` census over the capture | apparatus | H5 | ~20 lines |
| 7 | Require MEDIUM/LOW chains to state the raising verification; bound-vs-point-estimate note | product | P4, P5, P6 | rubric wording |

Items 1 and 5 touch `shared/` and require `sync-content.py --write`. Items 2-4 and 6 are offline
measurement changes that add no live gate and no CI job beyond QUAL-01's existing self-test.

**One caution on ordering.** #2 before #1 is deliberate if the goal is evidence: fixing the body
first removes the artifact that demonstrates the gap, and the next run is a different prompt, so
there would be nothing to measure the fix against. Landing the instrument first gives a before
reading on this capture and an after reading on the re-run.

## Checked and cleared

Stated so the absence of a finding is not read as an absence of a check.

- **Arithmetic** — 42/42 numeric claims reproduce independently from source prices, including all
  six trade-off column totals and the sensitivity reweighting. No computational error.
- **Provenance** — all 8 `read-at-source` ground truths join to real WebFetch calls, every literal
  located verbatim in the cited source, and the disclosed 404 is real. One agent dispatch, as the
  single-dispatch guardrail requires.
- **Chain form** — 8/8 chain blocks well-formed, 0 dependency cycles, 0 ungrounded chains,
  0 untraced conclusion claims, per the mechanical detector.
- **`?`-propagation** — every `?`-marked ground truth is enumerated by ID with a stated reason, and
  the `?` is carried into the chains that consume it. The demotions of C3, C5 and C6 are correct,
  C6's on assumptions rather than ground truths.
- **Verdict-cell nonconformance** — real (20/20) but pre-existing: 100% across all six frozen v8.7
  baseline analyses too. Inherited, not introduced by this run, and out of scope here.
- **Abandoned Reasoning** — both entries are genuine discards with stated reasons, one of them
  against the analysis's own interest (refusing to fabricate a churn elasticity).
