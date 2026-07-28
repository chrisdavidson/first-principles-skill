# DETECT-05 Blast-Radius Sweep and Goodhart Decision Rule — v8.13 Phase 186

This file matches none of the FROZEN-EVIDENCE globs (`tests/step0-baseline-v*.md`,
`tests/step0-captures-v*`, `tests/routing-baseline-v3.*.md`,
`tests/routing-battery-baseline-v4.3.md`, `tests/routing-baseline-v7.11.md`,
`tests/routing-battery-baseline-v7.11.md`, `tests/focused-output-baseline-v*.md`,
`tests/sub-skill-routing-baseline-v*.md`, `tests/quality-catalog-v8.7.md`,
`tests/quality-probe-v8.7`, `tests/quality-baseline-v8.7-regenerated`, `tests/quality-baseline-v8.7`,
`tests/quality-baseline-v8.7-postfix`), so it can be added without touching a frozen path.

All file paths in this document are given in inline code, never as a markdown link, so no link
gate can ever be tripped by this record.

## §1 — What this is

`.planning/` is gitignored (`commit_docs: false` per `.planning/config.json`), so a completeness
proof that lives only in a plan's execution record is not a git deliverable — it disappears the
moment the session ends and cannot be re-run by any future reader. This file is the tracked,
git-reachable record: the sweep that proves the blast-radius set named in this phase's context is
complete (D-07), and the pre-registered decision rule that governs whether the Goodhart guard's
published conclusion survives (D-10).

## §2 — The sweep, re-runnable

Three `git grep` commands, run from the repo root at commit **`1edcec0`** (this plan's Task 1
commit — the tree state immediately before this task's own commit). All three exclude this record
file itself via a `:!tests/detect05-blast-radius-sweep-v8.13.md` pathspec. The reason is
structural and independent of which files it drops: this file quotes every detector column name,
every corpus path and every figure phrase named below by construction, so without the exclusion
the sweep returns its own record as a site and can never close. The exclusion drops exactly one
file — itself.

**Command A** — the seven detector column names, over tracked files excluding `.planning`,
`scripts`, `*.tsv` and `*.jsonl` (source code and raw data are not blast-radius sites; they define
or carry the columns, they don't publish a stale figure in prose):

```
git grep -l -E 'verdict_flag|chain_flag|untraced_flag|nonconforming_verdict_cells|malformed_chain_blocks|conclusion_claims|untraced_claims' -- ':!.planning' ':!scripts' ':!*.tsv' ':!*.jsonl' ':!tests/detect05-blast-radius-sweep-v8.13.md'
```

**Command B** — the four corpus path stems, over tracked `*.md` excluding `.planning`:

```
git grep -l -E 'quality-baseline-v8\.7(-postfix|-regenerated)?|quality-baseline-v8\.10-oos' -- '*.md' ':!.planning' ':!tests/detect05-blast-radius-sweep-v8.13.md'
```

**Command C** — the narrative figure phrases, in both the Unicode-arrow and ASCII-arrow forms,
over tracked `*.md` excluding `.planning`:

```
git grep -l -E 'flat 6/6|one clean document|6/6 (→|->) 6/6' -- '*.md' ':!.planning' ':!tests/detect05-blast-radius-sweep-v8.13.md'
```

**Why Command C exists — the honest half of D-07.** Command A keys on column names and Command B
on corpus paths, so a sentence that quotes a moved figure while naming neither is invisible to
both. That is not hypothetical — it was found during planning. `docs/README.md:99` quotes
`flat 6/6 untraced-§6 defect` and is returned by neither A nor B; it is Command C's only unique
contribution. A sweep whose blind spot is undisclosed proves nothing; disclosing the blind spot and
closing it is the point.

**Measured cardinalities, at this task's execution (re-run at commit `1edcec0`, matching the
figures cited in `186-CONTEXT.md`/`186-RESEARCH.md` exactly — not narrowed to match them):**

| Command | Files returned |
|---|---|
| A | **14** |
| B | **25** |
| C | **9** |

A is a subset of B (confirmed: `comm -23 <A> <B>` is empty — every column-name hit also quotes a
corpus path). The union of all three is **26** distinct files. These are the numbers actually
returned by the commands above, run verbatim, at this commit — not tightened to fit any
pre-decided row count. If a later re-run of this sweep returns a different cardinality, that is a
signal the tree changed since this record was written, not a defect in this record.

## §3 — Full classified hit list

Every file the sweep returns, plus one file found by reading (`tests/quality-baseline-v8.10-oos/README.md`,
which becomes a sweep hit only after Plan 03 writes detector column names into it). No silent
omissions. Each row carries one disposition: CORRECTED / QUALIFIED / DISPOSITIONED-FROZEN /
DISPOSITIONED-UNMOVED / DISPOSITIONED-OUT-OF-SCOPE / NO-ACTION.

### §3a — Substantive dispositions (14 rows)

| # | File | Lines | What it quotes | Disposition | Where the correction lives |
|---|---|---|---|---|---|
| 1 | `docs/v8.7-quality-baseline-freeze.md` | 128-129 | site 1 — `verdict_flag`/`chain_flag`/Q-P2-run1 figures | CORRECTED | Plan 01 (this plan), commit `1edcec0` |
| 2 | `docs/v8.7-quality-baseline-freeze.md` | 217 + `## Honest limits` | site 3 / D-16 — Goodhart guard pre-registration + saturation limit | CORRECTED | Plan 01 (this plan), Task 3 |
| 3 | `docs/v8.7-post-fix-remeasure.md` | 46-51, 83-84 | site 2 — `--compare` code block + defect-incidence figures | CORRECTED | Plan 02 |
| 4 | `docs/v8.7-post-fix-remeasure.md` | 151-162 §3 | site 5 — canonical Goodhart verdict | CORRECTED | Plan 04 |
| 5 | `docs/v8.10-fix-contract-oos-validation.md` | 134, 152, 169 | site 6 — detector-output table, `Q-N1` row | CORRECTED | Plan 03 |
| 6 | `docs/v8.9-diagnose-contract-fix.md` | 212-213 | site 7 — reconciliation tuple | CORRECTED | Plan 02 |
| 7 | `tests/quality-baseline-v8.10-oos/README.md` | (whole file, addition) | site 4 — qualifies the frozen sibling TSV's constant `verdict_flag` column | QUALIFIED | Plan 03 |
| 8 | `tests/quality-baseline-v8.7-regenerated/README.md` | 219-221 | site 8a — same stale figures as row 1 | DISPOSITIONED-FROZEN | inside a FROZEN-EVIDENCE directory, uncorrectable in place; correction carried by row 1 |
| 9 | `tests/quality-baseline-v8.7-postfix/README.md` | 86-92 | site 8b — same stale figures as row 3 | DISPOSITIONED-FROZEN | inside a FROZEN-EVIDENCE directory, uncorrectable in place; correction carried by row 3 |
| 10 | `tests/quality-fixtures-v8.7/calibration-v8.6-corpus.md` | 28-40, 138, 148, 150 | site 9 — all three flags unmoved at 6/6; `condB-P3` `nonconforming_verdict_cells` moved 4→15 under a saturated flag | QUALIFIED | Plan 03 |
| 11 | `tests/quality-fixtures-v8.7/README.md` | 260-286 | site 10 — all nine pinned detector fields for both synthetic fixtures | DISPOSITIONED-UNMOVED | all eighteen fields still reproduce exactly under the corrected detector (evidence command below); nothing is stale |
| 12 | `docs/v8.12-coding-findings.md` | 162-171 | site 11 — the historical flat 6/6 untraced figure it compares against | QUALIFIED | Plan 02; now re-measures 4/6 |
| 13 | `docs/detector-contract-fix-plan.md` | 50-53 | the pre-registered diagnosis, this milestone's own blast-radius table | DISPOSITIONED (D-08) | Plan 04; Claim/Status columns preserved, disposition appended |
| 14 | `docs/v8.9-diagnose-contract-fix.md` | 118 | the global `untraced_flag=1` claim | DISPOSITIONED-OUT-OF-SCOPE | `untraced_flag` and the tracing logic are named out of scope in `REQUIREMENTS.md`, and D-06 limits untraced corrections to lines already being amended; this line is not one. Recorded as a known residual for a successor, not silently dropped |

Row 7 is the one row in this table that **no** sweep command returns — it was found by reading,
not by grep. It becomes a sweep hit only after Plan 03 writes the qualification into it, so its
status legitimately differs between this task's run and Plan 04's re-run; recorded here rather
than left for a reader to discover.

**Site 10's evidence command**, run this task (re-run of the command recorded during planning,
reproduced exactly): import `scripts/check-quality-harness.py` via
`importlib.util.spec_from_file_location`, register the module in `sys.modules` under the spec name
**before** calling `exec_module` (a frozen dataclass in the harness fails to construct otherwise),
then call `detect_defects(text, analysis_id)` on the text of
`tests/quality-fixtures-v8.7/analyses-conformant.md` and
`tests/quality-fixtures-v8.7/analyses-defective.md`.

```python
import importlib.util as u, sys
s = u.spec_from_file_location('qh', 'scripts/check-quality-harness.py')
mm = u.module_from_spec(s)
sys.modules['qh'] = mm
s.loader.exec_module(mm)
mm.detect_defects(open('tests/quality-fixtures-v8.7/analyses-conformant.md', encoding='utf-8').read(), 'conformant')
mm.detect_defects(open('tests/quality-fixtures-v8.7/analyses-defective.md', encoding='utf-8').read(), 'defective')
```

Measured output, this task, verbatim on the count/flag fields:

- `conformant`: `conclusion_claims=3, untraced_claims=0, untraced_flag=0, verdict_cells=3,
  nonconforming_verdict_cells=0, verdict_flag=0, chain_blocks=2, malformed_chain_blocks=0,
  chain_flag=0`.
- `defective`: `conclusion_claims=3, untraced_claims=1, untraced_flag=1, verdict_cells=3,
  nonconforming_verdict_cells=1, verdict_flag=1, chain_blocks=2, malformed_chain_blocks=1,
  chain_flag=1`.

Both match `tests/quality-fixtures-v8.7/README.md:260-286`'s pinned figures exactly — all eighteen
fields reproduce, so row 11 is correctly DISPOSITIONED-UNMOVED, not stale.

### §3b — Every remaining sweep hit, dispositioned (16 rows)

An earlier draft of this record carried a bare NO-ACTION list asserting the remaining files "quote
no baseline figure that moved." Per-file verification during planning showed that claim was
**false for three of them**, and a fourth (a pre-registration document) was absent from the record
entirely. That correction is recorded here rather than silently fixed — a completeness proof that
itself carried an unchecked assumption is worth naming. Every row below was re-verified by grep at
this task's execution, not inherited from the earlier draft on faith.

**Four files DO quote a moved figure**, all on the `untraced` axis of the postfix corpus (6/6 to
4/6, cause FIX-CONTRACT-01, which shipped 2026-07-24, one day before this milestone began). Each is
DISPOSITIONED-OUT-OF-SCOPE on the same basis as §3a row 14 — `untraced_flag` and the tracing logic
are named out of scope in `REQUIREMENTS.md`, and D-06 limits untraced corrections to lines already
being amended, which none of these is:

| # | File | Lines | What it quotes | Disposition | Where the correction lives |
|---|---|---|---|---|---|
| 15 | `docs/README.md` | 99 | quotes `flat 6/6 untraced-§6 defect` in the index row describing the v8.9 diagnosis document. Returned by Command C only — the blind-spot file that motivated C. Quoting only the figure phrase here, never the whole line: that line also contains a markdown link, and reproducing it verbatim would trip both this file's own no-links assertion and the link gate | DISPOSITIONED-OUT-OF-SCOPE | not corrected; the file **does** quote a moved figure — recorded honestly rather than dismissed |
| 16 | `docs/v8.10-correctness-instrument-design.md` | 11, 316 | quotes the Phase 166 primary defect as flat `6/6 → 6/6`; the postfix side of that pair now reads 4/6. Previously mis-listed NO-ACTION | DISPOSITIONED-OUT-OF-SCOPE | not corrected; the file **does** quote a moved figure — recorded honestly rather than dismissed |
| 17 | `docs/v8.12-coding-protocol.md` | 322, 325, 330 | quotes `the flat 6/6` as the historical figure. Also a pre-registration document, so D-08 applies independently: it records what was believed when it was written and is dispositioned, never rewritten | DISPOSITIONED-OUT-OF-SCOPE | not corrected; the file **does** quote a moved figure — recorded honestly rather than dismissed |
| 18 | `docs/v8.12-section-census-protocol.md` | 34-35 | names the postfix corpus as "the set that produced the flat 6/6 untraced-§6 result." Also a pre-registration document (D-08). Was absent from the record entirely in the earlier draft | DISPOSITIONED-OUT-OF-SCOPE | not corrected; the file **does** quote a moved figure — recorded honestly rather than dismissed |

**The remaining twelve are NO-ACTION**, each with the verified reason recorded — not a blanket
phrase:

| # | File | Lines | Verified reason | Disposition |
|---|---|---|---|---|
| 19 | `docs/v8.10-fix-contract-oos-protocol.md` | 192, 196 | the `≥4/6` figures are pre-registered thresholds for a hand-read aggregate, not detector defect-incidence figures | NO-ACTION |
| 20 | `docs/v8.11-defrobust-protocol.md` | 34, 165, 169 | names the oos analyses path structurally; no figure | NO-ACTION |
| 21 | `docs/v8.12-section-census-findings.md` | 120, 265 | the `6/6 split` is a twelve-document corpus split across two baseline directories, not a flag aggregate | NO-ACTION |
| 22 | `docs/v8.7-correctness-spot-check.md` | 283 | `3/6 correct` is a per-document arithmetic-accuracy tally from Phase 162, not a detector figure | NO-ACTION |
| 23 | `tests/defrobust-v8.11/read-input.md` | 1160 | the only match is the ground-truth ID list `GT-3/6/9`; a figure-shaped false positive | NO-ACTION |
| 24 | `tests/defrobust-v8.11/README.md` | 8 | names the oos analyses path; no figure | NO-ACTION |
| 25 | `tests/detect01-red-run-v8.13.md` | 63-64 | names the `Q-P2-run1` cell *shape* as a fixture descriptor; quotes no figure | NO-ACTION |
| 26 | `tests/detect02-reversal-proof-v8.13.md` | 206-230 | v8.13's own reversal-proof record; already publishes the **corrected** figures and labels the superseded ones as previously published, so nothing in it is stale. Previously listed NO-ACTION for the wrong reason | NO-ACTION |
| 27 | `tests/quality-baseline-v8.7/README.md` | 14 | FROZEN-EVIDENCE path; names the regenerated corpus directory only, quotes no figure. Checked and confirmed no moved figure — not edited under any circumstance | NO-ACTION |
| 28 | `tests/quality-catalog-v8.10-oos.md` | 32, 42-45 | catalog prompt text; names corpora and `Q-N` IDs only | NO-ACTION |
| 29 | `tests/quality-catalog-v8.7.md` | 11 | FROZEN-EVIDENCE path; names a sibling README only, quotes no figure. Checked and confirmed no moved figure — not edited under any circumstance | NO-ACTION |
| 30 | `tests/quality-probe-v8.7/README.md` | 112 | FROZEN-EVIDENCE path; the `2,454 / 16,866 = 14.6%` figure is a token-count ratio, not a defect figure. Checked and confirmed no moved figure — not edited under any circumstance | NO-ACTION |

For rows 27, 29 and 30, FROZEN-EVIDENCE status was checked explicitly and each came back with no
moved figure, so none needed DISPOSITIONED-FROZEN. Had any quoted one, it would have been
DISPOSITIONED-FROZEN and never edited.

**Escalation clause, discharged.** Every row in this table was re-checked by grep at this task's
execution, not inherited from the earlier draft on faith. No file's grep showed a quoted moved
figure whose stated disposition did not account for it — the four rows that do quote a moved
figure (rows 15-18) are marked as such, not dispositioned to NO-ACTION.

### §3c — Machine-checkable manifest

Every file path named in §3a and §3b, one bare path per line, sorted, no backticks and no other
text. Twenty-seven paths: the twenty-six the sweep returns plus
`tests/quality-baseline-v8.10-oos/README.md` (row 7, found by reading). This block is what makes
completeness checkable by `comm` instead of by eye.

<!-- SWEEP-MANIFEST-START -->
```manifest
docs/README.md
docs/detector-contract-fix-plan.md
docs/v8.10-correctness-instrument-design.md
docs/v8.10-fix-contract-oos-protocol.md
docs/v8.10-fix-contract-oos-validation.md
docs/v8.11-defrobust-protocol.md
docs/v8.12-coding-findings.md
docs/v8.12-coding-protocol.md
docs/v8.12-section-census-findings.md
docs/v8.12-section-census-protocol.md
docs/v8.7-correctness-spot-check.md
docs/v8.7-post-fix-remeasure.md
docs/v8.7-quality-baseline-freeze.md
docs/v8.9-diagnose-contract-fix.md
tests/defrobust-v8.11/README.md
tests/defrobust-v8.11/read-input.md
tests/detect01-red-run-v8.13.md
tests/detect02-reversal-proof-v8.13.md
tests/quality-baseline-v8.10-oos/README.md
tests/quality-baseline-v8.7-postfix/README.md
tests/quality-baseline-v8.7-regenerated/README.md
tests/quality-baseline-v8.7/README.md
tests/quality-catalog-v8.10-oos.md
tests/quality-catalog-v8.7.md
tests/quality-fixtures-v8.7/README.md
tests/quality-fixtures-v8.7/calibration-v8.6-corpus.md
tests/quality-probe-v8.7/README.md
```
<!-- SWEEP-MANIFEST-END -->

**Found-by-reading exception list** — the single entry permitted to be absent from the sweep
output at this task's own commit: `tests/quality-baseline-v8.10-oos/README.md`. A reader checking
completeness by `comm` against a fresh sweep should expect exactly this one path (or fewer, once
Plan 03 writes into it) on the "in record but not in sweep" side of the comparison, and nothing on
the "in sweep but not in record" side.

## §4 — Measured per-axis attribution (D-02), the table every correction block must match

**Method.** The harness at commit `c4eab10` (FIX-CONTRACT-01, shipped 2026-07-24 — the day before
this milestone began) was re-run over each corpus's frozen `analyses/` directory and diffed
cell-by-cell against both the frozen `defect-incidence.tsv` and the current
`defect-incidence-corrected.tsv`. A cell where `frozen == c4eab10 != corrected` moved **only**
because of v8.13 (DETECT-02/DETECT-03). A cell where `frozen != c4eab10 == corrected` moved
**only** because of FIX-CONTRACT-01 (already shipped, pre-v8.13). `_chain_ids`, `_chain_blocks`,
`_conclusion_claims`, `_claim_is_traced`, and the other untraced-axis functions are byte-identical
between `c4eab10` and HEAD — v8.13 touched only `_verdict_conforms` (DETECT-02) and
`_chain_block_well_formed` (DETECT-03), neither of which the untraced-axis pipeline calls.

- **regenerated** — `verdict_flag` 5/6 to 6/6 caused by DETECT-02 (Q-P2-run1's
  `nonconforming_verdict_cells` 0→14); `chain_flag` 6/6 to 5/6 caused by DETECT-03 (Q-P1-run2's
  `malformed_chain_blocks`/`chain_flag` 1/1→0/0); `untraced_flag` unmoved at 6/6. Both v8.13 causes
  are genuine here — this corpus is the one where DETECT-02 and DETECT-03 are cleanly,
  independently attributable with no FIX-CONTRACT-01 mixing.
- **oos** — `nonconforming_verdict_cells` Q-N1 19 to 2 and Q-N5 15 to 1 caused by DETECT-02;
  `malformed_chain_blocks`/`chain_flag` Q-N1 1 to 0 caused by DETECT-03. No FIX-CONTRACT-01
  contribution — this corpus's frozen TSV was generated 2026-07-24T12:06, already after
  FIX-CONTRACT-01 shipped that same day; `c4eab10` output matches the frozen file exactly on every
  cell.
- **postfix** — every cell that moved, including the whole `chain_flag` 4/6 to 6/6 headline and the
  whole `untraced_flag` 6/6 to 4/6 movement, is caused by FIX-CONTRACT-01 alone. v8.13 contributed
  **zero** movement on this corpus — DETECT-02/DETECT-03 change no cell on the postfix corpus that
  FIX-CONTRACT-01 had not already changed.

**D-06's proposed attribution for the untraced axis is REFUTED by this measurement and is not
written anywhere in this phase's corrections.** `186-CONTEXT.md`'s D-06 proposed attributing
`untraced_flag` movement to "collateral movement from the chain fix changing claim segmentation" —
this is empirically false: the untraced-axis functions are byte-identical between `c4eab10` and
HEAD, so DETECT-03 cannot be the cause of any untraced-axis movement on any corpus. The true cause,
on both corpora where the axis moved (postfix, and the untraced-adjacent claim-count movement on
regenerated), is FIX-CONTRACT-01 alone — already shipped, pre-v8.13.

Why this matters, on the record: this project has shipped a false attribution twice already —
Phase 184's chain-axis claim in the D-19 pinned-calibration comment (corrected in `893f3c0`) and
the Phase 184 gap-closure M-6 pre-measurement. Writing D-06's proposed wording as literally stated
would have been a third instance of the same failure mode. It is not written here.

**D-06's surviving half, stated, not glossed.** The roadmap's out-of-scope premise that
`untraced_flag` and the tracing logic are "unaffected" is strained. The tracing *logic* is
untouched by v8.13 — confirmed by the byte-identical function diff above — but its *outputs*
moved, and moved for a cause wholly outside this milestone (FIX-CONTRACT-01, 2026-07-24, one day
before v8.13 began). `untraced_flag` was simply never re-measured after that fix landed; this is
the first re-measurement, not a v8.13 causal effect.

## §5 — D-10: the pre-registered decision rule

Written here, committed in its own commit, before any verdict prose exists (Plan 04 writes the
verdict; this task's commit is the first commit to touch `tests/detect05-blast-radius-sweep-v8.13.md`,
and precedes any commit touching `docs/v8.7-post-fix-remeasure.md` §3 — provable from `git log`).
Three parts:

**Conclusion test.** The guard's conclusion — that form-without-substance is not what happened —
**SURVIVES** if and only if, recomputed over Phase 185's corrected defect-incidence figures with
the band scorelines unchanged, the machine-computed `GOODHART_FLAG` reads `clear`. It
**DOES NOT SURVIVE** if the recomputed flag reads anything else.

**Reasoning test, judged separately (D-09).** The published reasoning **STANDS** only if all three
of its per-axis directional claims hold under the corrected figures. If any one is false, the
reasoning is **REFUTED** and must be restated with the corrected directions rather than quietly
swapped.

**Strength test, mandatory regardless of the first two.** The record must state, for each of the
three signals the guard keys on, whether that signal was *capable* of falsifying the conclusion. A
conclusion supported by signals that could not have moved is a weaker conclusion, and saying "the
flag is still clear" without saying that is technically true and materially misleading.

Per D-13, "the conclusion does not survive" is a complete and publishable answer under this rule,
and equally may not be chased toward. The rule decides; the phase's appetite does not.

## §6 — Disclosed erosion of the pre-registration

Two disclosures, both stated plainly:

**(a)** True blindness was already lost before this rule was written — the corrected per-corpus
tables and the axis-inversion reading were computed and read during this phase's discussion and
research, and Phase 185's corrected siblings have been committed since `1c2b71a`.

**(b) Stronger, and the one that matters.** `--compare` was already run during Phase 186
*planning*, and its value was known before this rule was written down (recorded in
`186-RESEARCH.md` R1/R7: the recomputed `GOODHART_FLAG` is `clear`, byte-identical to the published
value). This rule is therefore pre-registered relative to the **verdict prose**, not relative to
the **number**. What is genuinely fixed in advance is the wording of the test, not analyst
ignorance of the outcome. Claiming blindness here would itself be the dishonesty this phase exists
to correct.

## §7 — Scope limit, on the record

This phase corrects what is provably wrong and states what is now uncertain. It does not
re-litigate v8.7 through v8.10 conclusions beyond the figures and the one guard named here.
