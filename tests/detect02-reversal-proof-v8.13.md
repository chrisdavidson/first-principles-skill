# DETECT-02 Reversal Proof — v8.13 Phase 183

This file matches none of the FROZEN-EVIDENCE globs (`tests/step0-baseline-v*.md`,
`tests/step0-captures-v*`, `tests/routing-baseline-v3.*.md`,
`tests/routing-battery-baseline-v4.3.md`, `tests/routing-baseline-v7.11.md`,
`tests/routing-battery-baseline-v7.11.md`, `tests/focused-output-baseline-v*.md`,
`tests/sub-skill-routing-baseline-v*.md`, `tests/quality-catalog-v8.7.md`,
`tests/quality-probe-v8.7`, `tests/quality-baseline-v8.7-regenerated`, `tests/quality-baseline-v8.7`,
`tests/quality-baseline-v8.7-postfix`), so it can be added without touching a frozen path.

All file paths in this document are given in inline code, never as a markdown link, so no link
gate can ever be tripped by this record.

## 1. What this is and why it exists

`_verdict_conforms` in `scripts/check-quality-harness.py` was inverted against the canonical
output contract: `shared/spine/references/output-template.md` and
`shared/spine/references/validation-rubric.md` Criterion 2 both prescribe a Verdict token
followed by an em-dash and a justification, and the rubric names the bare token alone as the
defect, yet the pre-fix predicate accepted only the bare token and rejected the prescribed form.
DETECT-02 (Plan 183-01) corrected the predicate. This file is the recorded proof of the direction
change that correction produces when the four analysis corpora are re-scored under it. A reversal
nobody wrote down is not evidence, exactly as Phase 182's red run was not evidence until it was
recorded (`tests/detect01-red-run-v8.13.md`).

## 2. Provenance

- **Base commit SHA the phase started from:** `213524b` (Phase 182's final commit — the tree
  state DETECT-02 began correcting).
- **Commit the re-score commands in this file were actually run against:** `9192fc3` (Plan
  183-01's final commit, current `HEAD` at the time this file was written — the tree state in
  which `_verdict_conforms` is already corrected).
- **DETECT-03 three-symbol pin-hash (must stay unchanged by this plan — confirms the re-score
  ran against a tree where only the DETECT-02-owned symbols moved):**
  `3 f3dfdd82079bd19add3b69d4f6d553ae963db1f1c22fb0027022278993d91afc`
  produced by:
  ```
  python3 -c 'import ast,hashlib,sys;src=open(sys.argv[1],encoding="utf-8").read();t=ast.parse(src);N={"_chain_block_well_formed"};C={"_ARROW","_CHAIN_FORM_LINE_RE"};s=[ast.get_source_segment(src,n) for n in t.body if (isinstance(n,ast.FunctionDef) and n.name in N) or (isinstance(n,ast.Assign) and any(getattr(x,"id","") in C for x in n.targets))];print(len(s),hashlib.sha256("\n".join(s).encode()).hexdigest())' scripts/check-quality-harness.py
  ```
  Re-run in this plan against commit `9192fc3` and confirmed byte-identical to Plan 183-01's own
  recorded value.
- **Five-symbol pin-hash before this phase (at commit `213524b`):**
  `5 8ecbaee0882c8f02f0760de8377db53720b1fb108951d0cb737e797f8b902add`
- **Five-symbol pin-hash after Plan 183-01's fix (at commit `9192fc3`, re-run in this plan and
  confirmed byte-identical to Plan 183-01's recorded value):**
  `5 eb8d02649c7929201b6e0b857c889bf0084b5a47544c3d56ff1bc06523bdba38`
  This is the symbol expected to move — it covers `_verdict_conforms` and `_VERDICT_VOCAB`, the
  two DETECT-02-owned symbols this phase's fix legitimately changes. It has moved. The
  DETECT-03-only three-symbol hash above has not, proving the change is confined to DETECT-02's
  owned surface.
- **`python3 --version`:** `Python 3.13.5`
- **`uname -srm`:** `Linux 6.12.57+deb13-amd64 x86_64`
- **Run date:** 2026-07-27

## 3. The decision Criterion 2 asked for

ROADMAP Success Criterion 2 for this phase requires the separator and empty-justification
treatment to be decided and documented, not left to the reader of the regex. The decision made in
Plan 183-01 (recorded there as P183-D1/P183-D2) and re-affirmed here:

- **U+2014 EM DASH is the only accepted separator.** U+2013 EN DASH and U+002D HYPHEN-MINUS are
  rejected.
- **An empty or whitespace-only justification after the separator is rejected.** A justification
  must contain at least one non-whitespace character after the em-dash.

Evidence for this decision, each independently checked:

- **Both canonical sources name only the em-dash.** `output-template.md`'s Verdict Vocabulary
  section and `validation-rubric.md`'s Criterion 2 Rigorous descriptor both prescribe "a leading
  token followed by an em-dash and a specific justification"; neither mentions an en-dash or a
  hyphen as an acceptable alternative.
- **Codepoint dump of `shared/spine/references/output-template.md` lines 69-71** (the three
  Verdict Vocabulary bullet examples): all six dash occurrences in those three lines are `—`
  (U+2014). Zero en-dash, zero hyphen.
- **A 267-cell census across all four frozen analysis corpora** (`tests/quality-baseline-v8.7/`,
  `tests/quality-baseline-v8.7-postfix/`, `tests/quality-baseline-v8.7-regenerated/`,
  `tests/quality-baseline-v8.10-oos/`) found zero en-dash separators and zero hyphen separators
  in any Verdict cell — the strict em-dash-only decision moves no pinned figure in either
  direction, on any frozen corpus.

The three formerly observation-only fixtures (`V-OBS-ENDASH`, `V-OBS-HYPHEN`,
`V-OBS-EMPTY-AFTER-DASH`) were promoted in Plan 183-01 from `expected=None` to `expected=False`,
so this decision is now mechanically asserted by `contract_pin_strict_report()` and
`--self-test`, not merely described in a docstring.

## 4. The re-score

Four `--detect-defects ... --out ...` commands, each `--out` path inside a scratch directory
outside every corpus directory, run against commit `9192fc3`:

```
mkdir -p /tmp/detect02-rescore-v8.13
python3 scripts/check-quality-harness.py --detect-defects tests/quality-baseline-v8.7-regenerated/analyses --out /tmp/detect02-rescore-v8.13/regenerated.tsv
python3 scripts/check-quality-harness.py --detect-defects tests/quality-baseline-v8.7-postfix/analyses --out /tmp/detect02-rescore-v8.13/postfix.tsv
python3 scripts/check-quality-harness.py --detect-defects tests/quality-baseline-v8.7/analyses --out /tmp/detect02-rescore-v8.13/baseline.tsv
python3 scripts/check-quality-harness.py --detect-defects tests/quality-baseline-v8.10-oos/analyses --out /tmp/detect02-rescore-v8.13/oos.tsv
```

Each command printed `Defect-detection TSV written: <path>` and exited 0. No frozen file was
written by any of the four commands — every `--out` path resolves under `/tmp/detect02-rescore-v8.13/`,
never inside `tests/quality-baseline-v8.7-regenerated`, `tests/quality-baseline-v8.7-postfix`,
`tests/quality-baseline-v8.7`, or `tests/quality-baseline-v8.10-oos`.

`tests/quality-probe-v8.7/` was checked and confirmed to hold only `probe-P1.jsonl` and
`README.md` — it has no `analyses/` subdirectory, so it is not re-scorable by `--detect-defects`.
That fact is recorded here rather than silently passed over; no fifth command was run for it and
none should be.

**Ordering determinism.** The `-regenerated` re-score was run a second time, to a different
`--out` path in the same scratch directory (`regenerated-2.tsv`), and `cmp` against the first
run's output exited 0 — byte-identical. `run_detect_defects` emits rows in `sorted(glob('*.md'))`
filename order and neither this plan nor Plan 183-01 modified that ordering or the per-cell row
order inside `_nonconforming_verdict_text`.

**What this section does not claim.** DETECT-04 / Phase 185 owns producing each corpus's
permanent per-corpus TSV sibling carrying the corrected figures alongside the frozen
`defect-incidence.tsv` (a filename with a `-corrected` suffix on the frozen name). This phase
deliberately creates none — the four TSVs above are scratch files under `/tmp`, not committed,
and are not that deliverable.

## 5. Before and after, verdict columns only

Columns: analysis id, before `verdict_cells`, before `nonconforming_verdict_cells`, before
`verdict_flag`, after `nonconforming_verdict_cells`, after `verdict_flag`. "Before" is taken from
the frozen record for that corpus (not recomputed); "after" is the re-score in section 4. Every
frozen "before" row was confirmed internally consistent with a pre-fix run before use.

### `tests/quality-baseline-v8.7-regenerated/` (before: frozen `defect-incidence.tsv`)

| id | before verdict_cells | before nonconforming | before verdict_flag | after nonconforming | after verdict_flag |
|---|---|---|---|---|---|
| Q-P1-run1 | 10 | 10 | 1 | 10 | 1 |
| Q-P1-run2 | 11 | 11 | 1 | 11 | 1 |
| **Q-P2-run1** | **14** | **0** | **0** | **14** | **1** |
| Q-P2-run2 | 10 | 10 | 1 | 10 | 1 |
| Q-P3-run1 | 9 | 9 | 1 | 9 | 1 |
| Q-P3-run2 | 14 | 5 | 1 | 14 | 1 |

`Q-P2-run1` is the reversal Criterion 4 names: `nonconforming_verdict_cells` moves `0` → `14`,
`verdict_flag` moves `0` → `1`.

### `tests/quality-baseline-v8.7-postfix/` (before: frozen `defect-incidence.tsv`)

| id | before verdict_cells | before nonconforming | before verdict_flag | after nonconforming | after verdict_flag |
|---|---|---|---|---|---|
| Q-P1-run1 | 10 | 10 | 1 | 10 | 1 |
| Q-P1-run2 | 0 | 0 | 0 | 0 | 0 |
| Q-P2-run1 | 8 | 8 | 1 | 8 | 1 |
| Q-P2-run2 | 8 | 8 | 1 | 8 | 1 |
| Q-P3-run1 | 10 | 10 | 1 | 10 | 1 |
| Q-P3-run2 | 8 | 8 | 1 | 8 | 1 |

`Q-P1-run2` has zero Verdict cells in both before and after (its `verdict_cells` count is `0`);
its `verdict_flag` stays `0` throughout for that structural reason, not because any cell became
conforming. Every other row's `verdict_flag` is `1` in both before and after.

### `tests/quality-baseline-v8.7/` (before: `tests/quality-fixtures-v8.7/calibration-v8.6-corpus.tsv`,
the pre-fix verdict-column record for this corpus, since it has no `defect-incidence.tsv` of its
own)

| id | before verdict_cells | before nonconforming | before verdict_flag | after nonconforming | after verdict_flag |
|---|---|---|---|---|---|
| condA-P1 | 13 | 13 | 1 | 13 | 1 |
| condA-P2 | 8 | 8 | 1 | 8 | 1 |
| condA-P3 | 10 | 10 | 1 | 10 | 1 |
| condB-P1 | 8 | 8 | 1 | 8 | 1 |
| condB-P2 | 7 | 7 | 1 | 7 | 1 |
| condB-P3 | 15 | 4 | 1 | 15 | 1 |

Every `verdict_flag` in this corpus is `1` both before and after; `condB-P3`'s nonconforming
count moves `4` → `15` (the stale calibration-vector figure Plan 183-01 flagged with an in-source
caveat), but no document's flag changes.

### `tests/quality-baseline-v8.10-oos/` (before: frozen `defect-incidence.tsv`)

| id | before verdict_cells | before nonconforming | before verdict_flag | after nonconforming | after verdict_flag |
|---|---|---|---|---|---|
| Q-N1 | 19 | 19 | 1 | 2 | 1 |
| Q-N2 | 20 | 20 | 1 | 20 | 1 |
| Q-N3 | 13 | 13 | 1 | 13 | 1 |
| Q-N4 | 15 | 15 | 1 | 15 | 1 |
| **Q-N5** | **15** | **15** | **1** | **1** | **1** |
| Q-N6 | 12 | 12 | 1 | 12 | 1 |

`Q-N1` moves `19` → `2` nonconforming cells and `Q-N5` moves `15` → `1`; neither reaches
`verdict_flag=0` because at least one nonconforming cell remains in each document.

**Attribution.** Only these three verdict columns (`verdict_cells`, `nonconforming_verdict_cells`,
`verdict_flag`) are attributed to DETECT-02 in this file. Any movement visible in the
`conclusion_claims` / `untraced_claims` / `untraced_flag` / `chain_blocks` /
`malformed_chain_blocks` / `chain_flag` columns between the frozen "before" rows and the re-scored
"after" rows predates this phase — it is FIX-CONTRACT-01 (quick task 260724-bq3, commits
`02c8b66` and `c4eab10`), which corrected the untraced-claim and chain-label detectors before
these TSVs were frozen. That movement is not claimed here, and the DETECT-03 pin-hash staying
byte-identical (section 2) corroborates that this phase touched no chain-side symbol.

## 6. Criterion 4, measured against both halves

ROADMAP Success Criterion 4, verbatim:

> 4. On the frozen corpus the direction **reverses**: `Q-P2-run1` becomes **nonconforming** and the
>    em-dash documents become **conforming**. (DETECT-02)

**First half — HOLDS.** `Q-P2-run1` in `tests/quality-baseline-v8.7-regenerated/` moves from
`nonconforming_verdict_cells=0`, `verdict_flag=0` to `nonconforming_verdict_cells=14`,
`verdict_flag=1` (section 5). The document previously published as "the one clean document in
this baseline" (`docs/v8.7-quality-baseline-freeze.md`, the "Defect incidence" bullet naming
`verdict_flag` 5/6 with `Q-P2-run1` as the exception) is now flagged.

**Second half — NOT DEMONSTRABLE on any of the three frozen v8.7 corpora.** No document in
`tests/quality-baseline-v8.7-regenerated/`, `tests/quality-baseline-v8.7-postfix/`, or
`tests/quality-baseline-v8.7/` becomes conforming under the corrected check: every `verdict_flag`
in all three corpora's before/after tables above reads `1` after the fix, with the single
structural exception of `Q-P1-run2` in the postfix corpus, whose flag was already `0` before the
fix because it has zero Verdict cells to begin with — not because any cell became conforming.
The reason: these corpora's Verdict cells read like `**UNVERIFIED — flagged**`, `**REJECTED**`,
`**ACCEPTED**`, `**Rejected.**` and `**Likely incomplete**` — tokens outside the
Accept/Challenge/Discard vocabulary the corrected predicate matches. They were generated before
the D-08 Verdict form was in force, so they conform under neither the old rule nor the new one,
and no fix to `_verdict_conforms` alone can make them conform.

**Second half — DEMONSTRABLE on `tests/quality-baseline-v8.10-oos/`.** `Q-N1` moves 19/19 → 2/19
nonconforming cells and `Q-N5` moves 15/15 → 1/15 (section 5). Neither reaches `verdict_flag=0`,
so on this corpus the reversal is a **cell-count reversal, not a flag flip**, and is reported in
those terms rather than as a document becoming fully conforming.

This is recorded as a finding under HONESTY-NOT-SCORE (D-01), not as a criterion narrowed to fit
the result: the criterion is quoted above exactly as written, and both halves' measured outcomes
are stated plainly, including the half that does not hold on the corpora it names. The
`Q-P2-run1` reversal alone already falsifies the published "one clean document in this baseline"
sentence in `docs/v8.7-quality-baseline-freeze.md` — correcting that published sentence is
DETECT-05 / Phase 186's contract, not this phase's; it is not corrected or annotated here.

## 7. Removal protocol discharged

The six DETECT-02 fixture ids deleted from `_DETECT01_PINNED_RED` by Plan 183-01:
`V-ACCEPT-EMDASH`, `V-ACCEPT-EMDASH-BOLD`, `V-CHALLENGE-EMDASH`, `V-DISCARD-EMDASH-BOLD`,
`V-BARE-TOKEN`, `V-BARE-TOKEN-BOLD`. The three `C-*` ids (`C-TEMPLATE-C1`, `C-TEMPLATE-FORMAT`,
`C-MULTILINE-DIGITS`) were deliberately left in place — they belong to DETECT-03 and are Phase
184's contract, not this phase's.

Strict-report reproduction, re-run in this plan against commit `9192fc3`:

```
python3 -c "import importlib.util as u, sys; \
s = u.spec_from_file_location('qh', 'scripts/check-quality-harness.py'); \
mm = u.module_from_spec(s); sys.modules['qh'] = mm; s.loader.exec_module(mm); \
sys.exit(mm.contract_pin_strict_report())"
```

stdout:

```
contract_pin AXES C-TEMPLATE-C1: MULTILINE, NON-NUMERIC-GT
contract_pin STRICT-FAIL [DETECT-03] C-TEMPLATE-C1: contract expects True, current code returns False — carried until DETECT-03
contract_pin AXES C-TEMPLATE-FORMAT: NON-NUMERIC-GT
contract_pin STRICT-FAIL [DETECT-03] C-TEMPLATE-FORMAT: contract expects True, current code returns False — carried until DETECT-03
contract_pin AXES C-MULTILINE-DIGITS: MULTILINE
contract_pin STRICT-FAIL [DETECT-03] C-MULTILINE-DIGITS: contract expects True, current code returns False — carried until DETECT-03
contract_pin: 16 asserted fixtures, 0 observation-only, 3 PINNED-RED carried (DETECT-02: 0, DETECT-03: 3) — this red state is the DETECT-01 deliverable, not a passing invariant
```

Exit code: **1**. Zero `STRICT-FAIL [DETECT-02]` lines; exactly three `STRICT-FAIL [DETECT-03]`
lines. This is the completeness proof `tests/detect01-red-run-v8.13.md` section 9 designated for
this phase: `contract_pin_strict_report()` exiting non-zero with no remaining `[DETECT-02]`
failure is the only signal that says DETECT-02's red is fully gone, and it is gone.
