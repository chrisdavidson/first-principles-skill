# D-19 Calibration — `detect_defects` vs. the Phase-162 Judge Reading

**Command that produced the committed TSV:**

```sh
python3 scripts/check-quality-harness.py --detect-defects \
    tests/quality-baseline-v8.7/analyses \
    --out tests/quality-fixtures-v8.7/calibration-v8.6-corpus.tsv
```

**Run date:** 2026-07-22. **Input:** the six frozen analyses in
`tests/quality-baseline-v8.7/analyses/` (byte-unchanged; this run reads them and writes only
the two new files in this directory — `git diff --quiet -- tests/quality-baseline-v8.7`
stays clean before and after). **Output:** `calibration-v8.6-corpus.tsv`, committed unedited.

This is the calibration D-19 requires: the only human-equivalent reading of this corpus that
exists is the independent-judge finding recorded in `docs/v8.6-quality-ab-experiment.md`
§ "Finding 3 — four reproducible methodology defects". This document compares the mechanical
detector's per-document rollups against that reading, records agreement and disagreement
honestly, and does not alter the detector's definitions to make the numbers match.

---

## 1. Document-level rollups vs. the judge-reported figures

| Defect family | Detector (6 docs) | Judge-reported (Finding 3) | Verdict |
|---|---|---|---|
| Untraced Conclusion claims (`untraced_flag`) | **6/6** | 6/6 ("flagged in all six documents") | **AGREE** |
| Verdict-vocabulary violations (`verdict_flag`) | **6/6** | 6/6 ("a spec-vs-behaviour mismatch, 6/6") | **AGREE** |
| Malformed Derivation Chains (`chain_flag`) | **6/6** | 4/6 ("flagged in 4") | **DISAGREE** |

Per-document values (from `calibration-v8.6-corpus.tsv`):

| analysis_id | untraced_flag | verdict_flag | chain_flag |
|---|---|---|---|
| condA-P1 | 1 | 1 | 1 |
| condA-P2 | 1 | 1 | 1 |
| condA-P3 | 1 | 1 | 1 |
| condB-P1 | 1 | 1 | 1 |
| condB-P2 | 1 | 1 | 1 |
| condB-P3 | 1 | 1 | 1 |

The detector reports **every** document as carrying at least one malformed chain block. The
judges reported this in only four of six. The two families that agree (untraced Conclusion
claims, Verdict vocabulary) reach 6/6 in both readings with no adjustment.

## 2. Per-claim untraced counts (D-20) — no judge counterpart

The judge reading never produced a per-claim number; Finding 3 reports document-level presence
only ("flagged in all six documents"). D-20 introduces this finer-grained count specifically so
partial improvement is visible in Phase 166. There is nothing to agree or disagree with here —
this row is new information the mechanical detector adds, not a re-measurement of something the
judges already scored:

| analysis_id | conclusion_claims | untraced_claims | untraced_claims / conclusion_claims |
|---|---|---|---|
| condA-P1 | 9 | 4 | 4/9 |
| condA-P2 | 10 | 6 | 6/10 |
| condA-P3 | 9 | 7 | 7/9 |
| condB-P1 | 5 | 3 | 3/5 |
| condB-P2 | 6 | 3 | 3/6 |
| condB-P3 | 4 | 4 | 4/4 |

## 3. Per-family verdicts

### Untraced Conclusion claims — AGREE

Both readings land on 6/6. The detector's own claim-extraction rule (a bolded lead-in ending in
a colon, or a numbered/bulleted list item, filtered to items carrying sentence-ending punctuation
or exceeding forty characters) is a narrower definition of "claim" than a human reader's
intuitive one — plausibly it under-counts claims (a bare `**No — not as proposed.**` opening
line, for instance, is *not* counted as a claim because it neither ends in a colon nor appears
as a list item — see `condA-P1.md`). Despite that narrower net, at least one claim in every
document still fails to name a chain identifier or a traced ground-truth pair, so the
document-level rollup still lands on 6/6. The agreement is real, not an artifact of a
generous definition.

### Verdict-vocabulary violations — AGREE

Both readings land on 6/6. Note this is not uniform in magnitude: `condB-P3`'s assumption
table uses the plain words `Accept`/`Challenge`/`Discard` in eleven of its fifteen Verdict
cells (e.g. `| A-1 | ... | Accept as ground-truth candidate | Accept | Fourier conduction... |`)
— only four cells (`**Unverified — flagged**`, on rows A-5, A-6, A-7, A-14) carry an outcome
sentence instead of the prescribed vocabulary. Every other document in the corpus fails on
**every** Verdict cell (e.g. `condA-P1`: 13/13 non-conforming). The document-level flag is 1 in
both cases, so the rollup agrees, but the *severity* the detector's per-cell count exposes
(`nonconforming_verdict_cells` / `verdict_cells`) is not uniform across the corpus the way a
bare 6/6 headline implies — Phase 166 should read the per-cell ratio alongside the flag, not
the flag alone.

### Malformed Derivation Chains — DISAGREE

The detector reports 6/6; the judges reported 4/6. The definitional reason, concretely:

Every document in the corpus contains at least one section-4 block that the analysis itself
labels as a chain (`DC-4`, `DC-5`, `Chain D`, `Chain E`, `Chain 4`, `Chain 5`, ...) but that is
actually a trade-off matrix or a second-order/third-order effects list — exactly
`docs/v8.6-quality-ab-experiment.md`'s own defect 4 ("Trade-off matrices and second-order effect
lists are presented as chains... without the prescribed form"). The detector applies the
`GT-N + GT-M → [intermediate] → [conclusion]` requirement literally to *every* block it
identifies as a chain, with no carve-out for a block whose author has structured it as a table
or a bulleted list rather than prose — so a trade-off table (e.g. `condA-P1`'s `DC-4`) or a
second-order bullet list (e.g. `condB-P2`'s `Chain D`) is always malformed under this
definition, in all six documents, not four.

One concrete example the two-arrow-line check catches for a different reason — a real
form violation, not a trade-off/second-order block: `condB-P1`'s **Chain D — cost:**

> `GT-6 + A5 → cost scales with call-graph edges plus fixed tooling/observability/CI investment
> → for 40 services, expect a multi-quarter program with a prolonged dual-stack period in which
> the system is strictly more complex than either endpoint.`

This line has two arrows, but its first input pairs a Ground Truth (`GT-6`) with a raw,
un-elevated Assumption ID (`A5`) rather than a second Ground Truth — output-template.md's
prescribed form is `GT-N + GT-M`, not `GT-N + A-M`. The parser's literal read of "one or more
ground-truth identifiers... joined by plus signs" does not accept `A5` as a qualifying
identifier, so this line does not match and the block is reported malformed. Whether a human
reader would flag this as a form violation or accept it as informal shorthand for an already-
accepted assumption is exactly the kind of scoping question a judge and a literal parser can
reasonably answer differently.

Because the record cited in Finding 3 states only the aggregate ("flagged in 4") and does not
name which two documents were *not* flagged, this disagreement cannot be resolved to a specific
per-document mismatch — only the aggregate 6/6-vs-4/6 gap is verifiable from what is committed.
**This is recorded as a scoping disagreement, not a parser bug.** The parser is not failing to
read a shape the corpus uses; it is applying the prescribed form from
`shared/spine/references/output-template.md` § 4 more literally and more uniformly than the
independent judges evidently did. No change is made to `_chain_block_well_formed` or the
`_CHAIN_FORM_LINE_RE` pattern to bring the detector's count down to 4/6 — tuning the definition
until it reproduces the judges' number would destroy the independence that makes this
calibration worth having (T-164-13).

## 4. Defect coverage — one of the source experiment's four defects is not covered

`docs/v8.6-quality-ab-experiment.md` § Finding 3 reports four reproducible methodology defects.
This detector covers three of them:

- **Defect 1** (Verdict column vocabulary) — covered, via `verdict_flag`/`nonconforming_verdict_cells`.
- **Defect 2** (the `[Assumes: X]` inline token is essentially never emitted) — **NOT covered.**
  Judges read for this by scanning derivation-chain steps for an inline token and counting its
  absence; that is a content-aware reading of whether a step *introduces* an assumption not
  already in the Assumptions Table, which this detector — a structural parser that never reads
  prose for meaning — cannot do without becoming exactly the kind of whole-document semantic
  reader D-18 explicitly declines to build. Declaring this omission is required precisely so
  Phase 166 does not report "improvement" against a narrower defect set than the baseline was
  described with.
- **Defect 3** (Conclusions with no chain in section 4) — covered, via
  `untraced_flag`/`untraced_claims` (D-20's per-claim refinement of the same defect).
- **Defect 4** (trade-off/second-order lists presented as chains) — covered, via
  `chain_flag`/`malformed_chain_blocks`, discussed above under "Malformed Derivation Chains".

## 5. The Goodhart guard (D-21)

Phase 165 will be written with this detector's definitions visible — the classic setup for
satisfying the form of a fix without repairing the substance. Defect counts and rubric band
scores must therefore be read together, not the defect counts alone. The band-score side of
that pair, for this exact frozen corpus, is `tests/quality-baseline-v8.7/scorelines.tsv`
(bands: Rigorous=3, Sound=2, Hand-wavy=1, Absent=0; C2, C4, and C6 are the bands this milestone's
three covered defects map onto — Verdict vocabulary is scored under Criterion 2, chain form
under Criterion 4, and Conclusion traceability under Criterion 6). Phase 166's verdict is
required to state both the defect-count movement and the band-score movement, and to call out
the Goodhart signature by name if it appears: **defect counts fall while the C2, C4, and C6
bands do not move.** A drop in `untraced_flag`/`verdict_flag`/`chain_flag` with no corresponding
lift in C2/C4/C6 across `scorelines.tsv` would mean Phase 165 satisfied this detector's specific
definitions without producing analyses a rubric-scoring judge would call better — the precise
failure mode this calibration exists to make visible, not to prevent on its own.

## 6. Observed calibration vector (pinned in the self-test)

The exact per-family flag vectors observed by this run, over the six analyses in filename order
(`condA-P1, condA-P2, condA-P3, condB-P1, condB-P2, condB-P3`), are pinned in
`scripts/check-quality-harness.py`'s `_selftest_defects` so a future change to the detector's
definitions moves this vector loudly rather than silently:

- `untraced_flag`: `[1, 1, 1, 1, 1, 1]` (6/6)
- `verdict_flag`: `[1, 1, 1, 1, 1, 1]` (6/6)
- `chain_flag`: `[1, 1, 1, 1, 1, 1]` (6/6)

These are the detector's **observed** output, not the judge-reported figures — the sentinel's
job is to make a future edit to `detect_defects` visible, not to assert that this vector is
correct or final.
