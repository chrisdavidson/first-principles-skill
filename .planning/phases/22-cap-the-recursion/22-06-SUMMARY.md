---
phase: 22-cap-the-recursion
plan: 06
subsystem: apparatus
tags: [product-findings, 999-31, not-found-arm-census, deferred-ledger, mutation-verification]
dependency_graph:
  requires:
    - "22-05 — closed 999.31 items 1 and 2; left the deferred-literal ledger at 152 entries, both guards repinned fresh, `'eight arms'` ledger key confirmed still present and unmodified"
  provides:
    - "scripts/check-selfaudit-scan.py — the docstring's not-found-reporting-arm figure re-derived by per-site neutralization (nineteen candidate arms, not eight; CONTROLLED=3, SIBLING-ONLY=0, UNCONTROLLED=16), with its derivation, date and bound stated"
    - "scripts/gen-gate-docs.py — the moved deferred-literal-ledger key ('eight arms' -> 'nineteen not-found reporting arms') hand-adjudicated, both guards repinned fresh"
  affects:
    - "22-08 (records 999.31 item 4 closed; 999.31 fully disposed alongside items 1/2 from 22-05 and item 3's closed-by-decision disposition)"
tech_stack:
  added: []
  patterns:
    - "per-site neutralization on disposable rsync scratch copies, classified CONTROLLED/SIBLING-ONLY/UNCONTROLLED (with an honestly-disclosed fourth CRASH sub-case), as the standard way to measure whether a not-found guard's absence would go undetected"
    - "publish the measured reach with its own bound (CONTROLLED + SIBLING-ONLY + UNCONTROLLED = roster size) rather than a bare corrected number, matching the R7-R12 idiom this project uses everywhere else"
key_files:
  created: []
  modified:
    - scripts/check-selfaudit-scan.py
    - scripts/gen-gate-docs.py
decisions:
  - "The two 'is None' guards whose neutralization crashes --self-test with an uncaught TypeError (Body-1's section guard, Rubric-3..8's scan-block-slice guard) are counted as CONTROLLED, not left as an unclassifiable fourth bucket: their absence is provably, loudly detected (a hard crash, not a silent pass) even though no hand-authored check message names them — the docstring discloses this reasoning explicitly rather than silently folding them into a clean bucket"
  - "The full census (nineteen arms) supersedes the file's prior scope-limited eight-arm figure entirely, rather than patching the old figure's scope one gap at a time — it includes Body-1's and Rubric-3..8's guards (never previously counted in any published figure) and the four Rubric-9/10/13/14 slice guards the 999.31 item 4 backlog finding named as never independently neutralized"
  - "No lock, control, branch id or gate was added for any UNCONTROLLED or CRASH-classified arm — the LEVEL move docs/PROCESS.md section 1 forbids and the plan's own T-22-06-01 threat register entry names by disposition 'mitigate'"
  - "The new deferred-literal-ledger key kept backlog id 999.41 (the correct classification for a .py module docstring hit), matching plan 22-05's precedent, rather than a fresh hand-adjudication id"
metrics:
  duration: "~110 minutes"
  completed: 2026-09-08
---

# Phase 22 Plan 06: Close 999.31 Item 4 — The Not-Found-Arm Census Summary

Closed the phase's one genuinely open measurement — the published "eight not-found reporting
arms" figure in `scripts/check-selfaudit-scan.py`'s module docstring, which the origin backlog
review believed undercounts by at least four. Built a complete candidate roster of nineteen
not-found reporting arms across `_check_body_text` and `_check_rubric_text` (more than double the
published eight), neutralized every one individually on disposable `rsync --exclude .git` scratch
copies, and published the measured result: **CONTROLLED=3, SIBLING-ONLY=0, UNCONTROLLED=16, of
nineteen total**. No lock, control, branch id or gate was added — the low CONTROLLED count is
published as a disclosed, measured limitation, not remediated by extending the apparatus. The
deferred-literal-ledger key the docstring edit moved was re-adjudicated by hand and both its
guards repinned fresh; the battery confirmed `FIREWALL: GREEN (26/26)` afterward.

## What Was Built

### Task 1 — the candidate roster

Swept the file for every not-found reporting form, not only `== -1`:

- `/usr/bin/grep -n -- "== -1" scripts/check-selfaudit-scan.py` → 13 lines
- `/usr/bin/grep -n "is None" scripts/check-selfaudit-scan.py` → 7 lines
- `/usr/bin/grep -n "\.find(\|\.rfind(\|< 0\b\|not in text\|not in section\|IndexError\|except ValueError" scripts/check-selfaudit-scan.py` → swept for `< 0`, `not in`, `IndexError`/`except ValueError` forms — none found as production not-found-reporting idioms (the `.find(` hits outside `== -1`/`is None` sites are all inside mutation-helper functions used to build self-test fixtures — e.g. `_relocate`, `_mutate_within_range`, `_duplicate_within_range` — which `assert ... != -1` on a literal known present, not report a not-found condition on the analyzed text; confirmed by reading each function's boundaries against `/usr/bin/grep -n "^def "`)

Of the 13 `== -1` lines: two (653, 657) are internal to the `_slice(...)` helper (feeding the `is None` report at its callers, not themselves reporting sites) and one (2457) is a comment. The remaining 10 real `== -1` reporting `if`s split into 13 arms (three compound `if`s — Rubric-9's and Rubric-10's `span_idx == -1 or rigorous_idx == -1 or not (...)`, and Rubric-13's `admission_idx == -1 or crit4_idx == -1 or not (...)` — each contribute 2 not-found sub-arms plus one non-not-found ordering check, per the plan's own instruction that arms sharing one `if` are counted as the arms they are). Of the 7 `is None` lines, one (675) is internal to `_slice_to_next_h2` (feeding Body-1's report); the remaining 6 are each their own reporting `if`. **13 + 6 = 19 total roster rows.**

**Roster table** (line, enclosing check, literal/anchor, own-`if` or shared, message):

| # | Line(s) | Enclosing check | Literal / anchor | Own-`if` or shared | Message that fires |
|---|---|---|---|---|---|
| 1 | 892 | Body-1 (`_check_body_text`) | `_BODY_SECTION_START` (via `_slice_to_next_h2`) | own | "Body-1: ... occurs N time(s)..." / "no '## ' heading found..." |
| 2 | 925 | Body-3 | `_BODY_SCAN_LEAD` | own | "Body-3: scan lead ... not found in whole file" |
| 3 | 927 | Body-3 | `_BODY_LEDGER_FENCE_TAIL` | own | "Body-3: ledger fence tail ... not found in whole file" |
| 4 | 931 | Body-3 | `_BODY_LEDGER_CLEAN` | own | "Body-3: ledger-clean handoff ... not found in whole file" |
| 5 | 1100 | Rubric-2 | `_RUBRIC_AA_BLOCK` (`aa_idx`) | own | "Rubric-2: ... not found in whole file" |
| 6 | 1102 | Rubric-2 | `_RUBRIC_SCAN_BLOCK` (`scan_idx`) | own | same shape |
| 7 | 1104 | Rubric-2 | `_RUBRIC_PRECEDENCE` (`precedence_idx`) | own | same shape |
| 8 | 1128 | Rubric-3..8 | `_RUBRIC_SCAN_BLOCK`/`_RUBRIC_PRECEDENCE` (via `_slice`) | own | "Rubric-3..8: scan-block slice not found..." |
| 9 | 1191 | Rubric-9 | `_CRIT4_START`/`_CRIT5_START` (via `_slice`) | own | "Rubric-9: Criterion 4 slice not found..." |
| 10a | 1208 | Rubric-9 | `span_idx` (`_RUBRIC_QUOTED_SPAN_C4` in `crit4_slice`) | shared (compound with 10b + ordering) | "Rubric-9: scan-half quoted-span sentence does not precede the Rigorous band bullet in Criterion 4" |
| 10b | 1208 | Rubric-9 | `rigorous_idx` (`_BAND_RIGOROUS` in `crit4_slice`) | shared | same message |
| 11 | 1224 | Rubric-10 | `_CRIT6_START`/`_USAGE_NOTE` (via `_slice`) | own | "Rubric-10: Criterion 6 slice not found..." |
| 12a | 1241 | Rubric-10 | `span_idx` | shared (compound with 12b + ordering) | "Rubric-10: scan-half quoted-span sentence does not precede the Rigorous band bullet in Criterion 6" |
| 12b | 1241 | Rubric-10 | `rigorous_idx` | shared | same message |
| 13 | 1289 | Rubric-13 | `_RUBRIC_FORMAT_START`/`_RUBRIC_CRITERIA_START` (via `_slice`) | own | "Rubric-13: Verdict Block Format slice not found..." |
| 14 | 1340 | Rubric-13 | `_RUBRIC_FORMAT_ADMISSION_LEAD` (`split_idx`) | own | "Rubric-13: admission sentence not found inside the Verdict Block Format section..." |
| 15a | 1378 | Rubric-13 | `admission_idx` (`_RUBRIC_FORMAT_ADMISSION`, whole file) | shared (compound with 15b + ordering) | "Rubric-13: admission sentence does not precede the Criterion 4 heading (placement violated)" |
| 15b | 1378 | Rubric-13 | `crit4_idx` (`_CRIT4_START`, whole file) | shared | same message |
| 16 | 1417 | Rubric-14 | `_CRIT2_START`/`_CRIT3_START` (via `_slice`) | own | "Rubric-14: Criterion 2 slice not found..." |

19 rows ≥ the `== -1` baseline (13), difference explained above (2 internal-helper lines + 1 comment excluded; 3 compound `if`s split into 6 sub-arms; 6 `is None` sites added).

**Every site the ROADMAP's 999.31 item 4 names by hand is located:** Rubric-9's Criterion-4-slice = row 9 (line 1191); Rubric-10's Criterion-6-slice = row 11 (line 1224); Rubric-13's Verdict-Block-Format-slice = row 13 (line 1289); Rubric-14's Criterion-2-slice = row 16 (line 1417).

`git diff --name-only` was empty for this task — no source file was modified (roster-building only).

### Task 2 — per-site neutralization on disposable scratch copies

`git status --porcelain` on the real repository: **empty before the first mutation**, confirmed again **empty after the last mutation and after scratch-copy deletion**.

Method: one `rsync -a --exclude .git ./ "$SCRATCH"/` scratch copy of the whole tree (needed because the checker resolves sibling files — the agent body, the rubric — relative to the tree, not just the single script). For each roster row, restored the scratch copy's `scripts/check-selfaudit-scan.py` from a pristine snapshot, applied ONE targeted mutation (own-`if` sites: replaced the guard's condition with `False`; compound-`if` sub-arms: replaced only the named sub-term, e.g. `span_idx == -1` → `False`, leaving the sibling sub-term and the ordering check untouched), ran `python3 <scratch>/scripts/check-selfaudit-scan.py --self-test`, and recorded the exit code and firing detail.

**Neutralization table:**

| # | Site (line) | Mutation | Observed rc | Bucket | Firing message |
|---|---|---|---|---|---|
| 1 | Body-1 section guard (892) | `if section is None:` → `if False:` | 1 | **CONTROLLED** (crash — see note below) | Uncaught `TypeError: expected string or bytes-like object, got 'NoneType'`, raised inside `_flat()` ← `_count_flat(section, _BODY_SCAN_LEAD)` — the code removed both the report AND its early `return failures`, so downstream code runs on `section=None` for the fixture that legitimately deletes `_BODY_SECTION_START` |
| 2 | Body-3 lead (925) | `if lead_idx == -1:` → `if False:` | 0 | UNCONTROLLED | `check-selfaudit-scan --self-test: PASS`, "All 100 branches covered" |
| 3 | Body-3 tail (927) | `if tail_idx == -1:` → `if False:` | 0 | UNCONTROLLED | same |
| 4 | Body-3 clean (931) | `if clean_idx == -1:` → `if False:` | 0 | UNCONTROLLED | same |
| 5 | Rubric-2 aa_idx (1100) | `if aa_idx == -1:` → `if False:` | 1 | **CONTROLLED** | `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['R-02-placement-anchor']`; `check-selfaudit-scan --self-test: FAIL — R-02b: no failures produced; Anti-masking: 1 branches uncovered` |
| 6 | Rubric-2 scan_idx (1102) | `if scan_idx == -1:` → `if False:` | 0 | UNCONTROLLED | PASS |
| 7 | Rubric-2 precedence_idx (1104) | `if precedence_idx == -1:` → `if False:` | 0 | UNCONTROLLED | PASS |
| 8 | Rubric-3..8 scan_slice (1128) | `if scan_slice is None:` → `if False:` | 1 | **CONTROLLED** (crash — see note below) | Uncaught `TypeError: expected string or bytes-like object, got 'NoneType'`, raised inside `_flat()` ← `_contains(...)`, same mechanism as Body-1 |
| 9 | Rubric-9 crit4_slice (1191) | `if crit4_slice is None:` → `if False:` | 0 | UNCONTROLLED | PASS |
| 10a | Rubric-9 span_idx (1208, sub-term only) | `span_idx == -1` → `False` | 0 | UNCONTROLLED | PASS — unreachable dead code: a preceding `c4_span_count != 1` check on the same literal already guarantees `span_idx != -1` by the time this line runs |
| 10b | Rubric-9 rigorous_idx (1208, sub-term only) | `rigorous_idx == -1` → `False` | 0 | UNCONTROLLED | PASS |
| — | Rubric-9 whole compound (1208, both `-1` sub-terms AND the ordering check together) | entire condition → `False` | 1 | (ordering check, not a not-found arm) | `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['R-09-crit4-order']` — confirms the ordering sub-check is independently CONTROLLED; the two `-1` sub-arms are each separately UNCONTROLLED per rows 10a/10b |
| 11 | Rubric-10 crit6_slice (1224) | `if crit6_slice is None:` → `if False:` | 0 | UNCONTROLLED | PASS |
| 12a | Rubric-10 span_idx (1241, sub-term only) | `span_idx == -1` → `False` | 0 | UNCONTROLLED | PASS |
| 12b | Rubric-10 rigorous_idx (1241, sub-term only) | `rigorous_idx == -1` → `False` | 0 | UNCONTROLLED | PASS |
| — | Rubric-10 whole compound (1241) | entire condition → `False` | 1 | (ordering check) | `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['R-10-crit6-order']` |
| 13 | Rubric-13 format_slice (1289) | `if format_slice is None:` → `if False:` | 0 | UNCONTROLLED | PASS |
| 14 | Rubric-13 split_idx (1340) | `if split_idx == -1:` → `if False:` | 0 | UNCONTROLLED | PASS |
| 15a | Rubric-13 admission_idx (1378, sub-term only) | `admission_idx == -1` → `False` | 0 | UNCONTROLLED | PASS |
| 15b | Rubric-13 crit4_idx (1378, sub-term only) | `crit4_idx == -1` → `False` | 0 | UNCONTROLLED | PASS |
| — | Rubric-13 whole compound (1378) | entire condition → `False` | 1 | (ordering check) | `ANTI-MASKING GATE FAILURE: 1 branch(es) not covered: ['R-13-format-order']` |
| 16 | Rubric-14 crit2_slice (1417) | `if crit2_slice is None:` → `if False:` | 0 | UNCONTROLLED | PASS |

**Bucket counts: CONTROLLED = 3 (rows 1, 5, 8), SIBLING-ONLY = 0, UNCONTROLLED = 16 (rows 2, 3, 4, 6, 7, 9, 10a, 10b, 11, 12a, 12b, 13, 14, 15a, 15b, 16). 3 + 0 + 16 = 19 = roster size.**

**Classification note on rows 1 and 8 (the CRASH cases).** These do not fit the plan's three-bucket definitions cleanly: CONTROLLED requires "the failure message names this arm specifically," but the failure here is an unhandled Python `TypeError`, not a check-authored assertion message. It is not SIBLING-ONLY either — no sibling count check or the anti-masking floor fires; the crash happens before any check machinery runs. Disposition: classified CONTROLLED because the substantive property CONTROLLED protects — "this guard's absence is detected, not silently passed over" — genuinely holds, more strongly than a graceful message would (a crash is categorically impossible to miss, unlike a printed detail line a caller could ignore). The docstring states this reasoning explicitly rather than folding it into a clean bucket silently.

**Masking-floor relaxation:** none was needed. Every mutation's outcome was observable directly through `--self-test`'s own exit code and top-level message; no broad floor fired ahead of a per-arm result masking it.

`git status --porcelain` on the real repository: confirmed **empty** immediately before the Task 1/2 work began and **empty** again after the last scratch mutation and scratch-copy deletion (`rm -rf` on `/tmp/.../scratchpad/22-06-scratch`, confirmed by a subsequent `ls` reporting "No such file or directory"). `git diff --name-only scripts/check-selfaudit-scan.py` showed no change from Tasks 1-2.

### Task 3 — published figure, ledger re-adjudication, re-gate

Rewrote docstring item (8) (lines 167-203) to state: the CONTROLLED count (3, with the two crash-classified arms' mechanism disclosed inline); the SIBLING-ONLY (0) and UNCONTROLLED (16) counts beside it; the derivation method (per-site neutralization on disposable scratch copies) and date (2026-09-08); and the total roster size (19), so the three buckets are visibly exhaustive. No lock, control, branch id or gate was added for any UNCONTROLLED or crash-classified arm. `branch_count` and `control_count` are unchanged (100, 12 — confirmed by `--describe` before and after).

Full replacement text (verbatim, `~lines 167-203`):

> (8) **`15-REVIEW.md`'s remaining findings, named rather than fixed here**:
> WR-03's not-found reporting arms across `_check_body_text` and
> `_check_rubric_text` were re-censused by per-site neutralization on
> disposable `rsync --exclude .git` scratch copies on 2026-09-08
> (`22-06-SUMMARY.md`, repeating `15-13-SUMMARY.md` Measurement 2's own
> per-arm methodology against the current tree rather than transcribing
> its scope-limited prior figure): nineteen not-found reporting arms
> total — Body-1's section guard; Body-3's scan-lead, ledger-fence-tail
> and ledger-clean guards; Rubric-2's scan-block and Precedence guards
> (`aa_idx`, the third Rubric-2 guard, excluded — independently
> controlled by `R-02-placement-anchor`); Rubric-3..8's scan-block-slice
> guard; Rubric-9's Criterion-4-slice guard plus its span/Rigorous
> ordering sub-guards; Rubric-10's Criterion-6-slice guard plus its
> span/Rigorous ordering sub-guards; Rubric-13's Verdict-Block-Format-slice
> guard, its region-split anchor guard (`split_idx`, the arm plan 15-11
> added), and its admission/Criterion-4-index ordering sub-guards; and
> Rubric-14's Criterion-2-slice guard. Of the nineteen: one is
> independently CONTROLLED — `aa_idx`, via `R-02-placement-anchor`'s own
> branch id; two — Body-1's and Rubric-3..8's slice guards — are
> load-bearing but not through a named branch id: neutralizing either
> crashes `--self-test` with an uncaught `TypeError` (downstream code
> assumes a non-None slice) rather than producing a controlled failure
> message, counted here as CONTROLLED because their absence is provably,
> loudly detected rather than silently passed over, not because a check
> names them; sixteen are UNCONTROLLED — `--self-test` still exits 0 with
> no branch reported uncovered when the guard is neutralized alone —
> including the four sites a 2026-09-08 backlog review (999.31 item 4)
> named as never independently neutralized: Rubric-9's Criterion-4-slice,
> Rubric-10's Criterion-6-slice, Rubric-13's Verdict-Block-Format-slice,
> and Rubric-14's Criterion-2-slice guards. SIBLING-ONLY (a failure
> through a sibling check or the anti-masking floor alone, naming no arm)
> accounts for zero of the nineteen. This census supersedes the file's
> prior published figure, which counted only the WR-03-named subset
> (Body-3, Rubric-2's non-`aa_idx` pair, Rubric-13's
> admission/Criterion-4-index pair, and `split_idx`) and omitted Body-1,
> Rubric-3..8's slice guard, and the four Rubric-9/10/13/14 slice guards
> named above. No lock, control, branch id or gate was added to raise the
> CONTROLLED count; the sixteen-arm UNCONTROLLED residual (with the two
> crash-only guards' own disclosed caveat) is a measured limitation of
> this file's own anti-masking floor, the same shape
> `_VALIDATE_LEG_SYMBOLS` (bound (11) above, backlog 999.30 item 1)
> already discloses — closed-by-decision under the depth rule
> (`docs/PROCESS.md` §1) rather than fixed here.

The first draft additionally quoted the literal message `"All 100 branches covered,"` — `gen-gate-docs.py --check` flagged it as a fresh hand-maintained count literal (`'100 branches'`, no exemption class matched); reworded to "no branch reported uncovered" (no digit) rather than route a second, avoidable new entry through the ledger. Logged under Deviations below.

**Ledger re-adjudication.** `python3 scripts/gen-gate-docs.py --check` (before this task's fix) reported the expected stale-ledger finding — the `'eight arms'` key on `scripts/check-selfaudit-scan.py#__doc__` no longer matched any live hit — plus one new non-exempt hit, `'nineteen not-found reporting arms'`. Ran `--emit-deferred-ledger`, diffed its 152-entry output against the live 152-entry `_DEFERRED_LITERAL_HITS` dict programmatically (AST-parsed and compared by key set, not by eye — script at `/tmp/.../scratchpad/diff_ledger.py`): confirmed exactly one key removed, one key added, and the other 151 keys' backlog-id/count shape unchanged (only their reason text differed from the emitter's fresh `TODO` placeholder, as expected — those 151 entries' real written reasons live only in the committed file, never in the emitter's output). Merged: preserved the 151 unaffected entries' written reasons byte-for-byte; hand-adjudicated the new key with a real reason naming the derivation, date, and the CONTROLLED/SIBLING-ONLY/UNCONTROLLED breakdown:

> `"Re-derived by per-site neutralization on disposable rsync --exclude .git scratch copies, 2026-09-08 (22-06-SUMMARY.md), closing 999.31 item 4 -- CONTROLLED=3 (one via R-02-placement-anchor's own branch id, two -- Body-1's and Rubric-3..8's slice guards -- via an uncaught crash rather than a named check), SIBLING-ONLY=0, UNCONTROLLED=16, of nineteen total candidate not-found reporting arms; the docstring states all three bucket counts and the roster size, not this figure alone."`

**Backlog-id decision:** kept backlog id `999.41` (the correct classification for a `.py` module docstring hit), matching plan 22-05's precedent, rather than a fresh hand-adjudication id. The class-level comment above `_DEFERRED_LITERAL_HITS` — already disclosing plan 22-05's one hand-adjudicated 999.41 exception — was updated to name both hand-adjudicated 999.41 entries explicitly (this plan's key alongside 22-05's), so the comment's own claim stays precise as of this edit (Rule 1 — the same discipline 22-04/22-05 applied to their own class-level comments).

| Guard | Before this plan | After |
|---|---|---|
| `_DEFERRED_LEDGER_MAX` | 152 | **152** (unchanged — one key removed, one added, net zero) |
| `_DEFERRED_LEDGER_KEYS_DIGEST` | `sha256:bf71a11703d09210a274702b9c19db8b3665ddcedcc46836b39b7ed91aa14c74` | **`sha256:1663c1a1f60cd4c45df8df685bc06b54a7b3b39d07e5660a3fa4332d1cc4db63`** |

Ran `--write` (34 files regenerated; `git diff --name-only` showed only `scripts/check-selfaudit-scan.py` and `scripts/gen-gate-docs.py` carrying a real diff — `CLAUDE.md`, `docs/ARCHITECTURE.md` and `docs/gates/SCAN-GUARD.md` regenerated byte-identical, since none of their generated fences render the literal-scan ledger facts or `check-selfaudit-scan.py`'s docstring prose by value; the plan's `files_modified` list named all five as candidates, but only the two Python files ended up carrying a diff — logged under Deviations below), `--self-test` (74 controls, PASS), `--check` (exit 0), both pre-commit hooks (`.githooks/pre-commit` and `scripts/git-hooks/pre-commit`, both exit 0), and `python3 scripts/check-selfaudit-scan.py --self-test` (exit 0, 100 branches). `git diff scripts/check-quality-harness.py` confirmed empty — the three CONTRACT-06 sha256 pins are byte-unchanged. `bash scripts/check-firewall-battery.sh` printed `FIREWALL: GREEN (26/26)`.

**`--describe` readings, before/after (this plan's own commit):**

| Measurement | Value |
|---|---|
| `check-selfaudit-scan.py --describe` `branch_count` | 100 (unchanged) |
| `check-selfaudit-scan.py --describe` `control_count` | 12 (unchanged) |
| `gen-gate-docs.py --describe` `control_count` | 74 |
| `gen-gate-docs.py --describe` `registered_surfaces` | 37 |
| `gen-gate-docs.py --describe` `literal_scan_non_exempt` | 0 |
| `gen-gate-docs.py --describe` `literal_scan_ledger_entries` | 152 (== `literal_scan_ledger_max`) |
| `gen-gate-docs.py --describe` `literal_scan_hits` | 179 (unchanged from end of wave 5) |
| `gen-gate-docs.py --describe` `literal_scan_ledger_adjudicated` | 38 (unchanged — the new key kept backlog id 999.41, so it is not counted as hand-adjudicated by this computation, the same disclosed imprecision plan 22-05 recorded) |
| `gen-gate-docs.py --describe` `literal_scan_ledger_mechanical` | 114 (unchanged, same reason) |

## Deviations from Plan

### Rule 1 fix — avoided restating a redundant count literal (in `scripts/check-selfaudit-scan.py`, this task's own file)

The first draft of the replacement paragraph quoted `"All 100 branches covered,"` (the literal message `--self-test` prints). `gen-gate-docs.py --check` correctly flagged this as a fresh hand-maintained count literal with no exemption class match. Rather than route an avoidable second new entry through the deferred-literal ledger, reworded the clause to state the same fact without a digit ("no branch reported uncovered"). Confirmed by re-running `--check`: only the intended `'nineteen not-found reporting arms'` hit remained.

### Documented pre-existing discrepancy — files_modified named three files that ended up unchanged (not a live bug)

The plan's frontmatter lists `docs/gates/SCAN-GUARD.md`, `CLAUDE.md` and `docs/ARCHITECTURE.md` alongside the two Python files as `files_modified`. After `gen-gate-docs.py --write`, `git diff --name-only` showed only `scripts/check-selfaudit-scan.py` and `scripts/gen-gate-docs.py` carrying a real diff — the other three regenerated byte-identical, because none of their generated fences render the literal-scan ledger facts or `check-selfaudit-scan.py`'s docstring prose by value (the same pattern plan 22-05 observed for `CLAUDE.md`/`docs/ARCHITECTURE.md`). Logged as a stale premise in the plan's frontmatter, not fixed (out of scope to edit the plan), and not committed since there is no diff to commit.

### Documented pre-existing discrepancy — one `TODO: written reason` match survives (not caused by this plan)

Verification item 4 measures `1`, not `0`. The one match is `emit_deferred_ledger()`'s own output-template string (`'"TODO: written reason"),'`) at `~line 2609` — the maintenance harness's boilerplate for whoever next runs `--emit-deferred-ledger`, not a leftover placeholder inside an actual `_DEFERRED_LITERAL_HITS` entry. Confirmed by grep count matching exactly this one line and by the programmatic AST diff above showing zero `TODO`-valued entries in the live dict. The same condition `22-03-SUMMARY.md`, `22-04-SUMMARY.md` and `22-05-SUMMARY.md` already documented for the identical reason. Editing `emit_deferred_ledger()`'s template string is out of this plan's `<action>` and its `read_first` list — logged, not fixed, per SCOPE BOUNDARY.

No other deviations. Both tasks' `<action>` and `<acceptance_criteria>` items were executed and independently re-verified on the live tree.

## Verification

All 12 plan-level `<verification>` items re-run on the live tree, in order:

1. SUMMARY carries a complete candidate roster (19 rows) and three bucket counts (3, 0, 16) summing to the roster size — **confirmed above**
2. `git status --porcelain` before the first mutation and after the last → both **empty**, no leak
3. `git diff scripts/check-selfaudit-scan.py | /usr/bin/grep -cE "^\+def _|^\+.*_LOCK|^\+.*== -1"` → **0**
4. `/usr/bin/grep -c "TODO: written reason" scripts/gen-gate-docs.py` → **1** — see documented pre-existing discrepancy above (the maintenance-harness template string, not a ledger placeholder)
5. `python3 scripts/check-selfaudit-scan.py --self-test` → exit **0**, "All 100 branches covered"
6. `python3 scripts/check-selfaudit-scan.py --describe` → `branch_count` **100**, `control_count` **12**
7. `python3 scripts/gen-gate-docs.py --self-test` → exit **0**; `--check` → exit **0**
8. `python3 scripts/gen-gate-docs.py --describe` → `control_count` **74**, `registered_surfaces` **37**, `literal_scan_non_exempt` **0**
9. `git diff scripts/check-quality-harness.py` → **empty**
10. `sh .githooks/pre-commit` → exit **0**; `sh scripts/git-hooks/pre-commit` → exit **0**
11. `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN`, total **26**
12. `git diff --name-only` → contains no `.github/workflows/validation.yml` — **confirmed** (only `scripts/check-selfaudit-scan.py`, `scripts/gen-gate-docs.py`)

## Issues Encountered

None beyond the two documented pre-existing discrepancies and the one in-scope Rule 1 fix, all recorded under Deviations above.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- 999.31 item 4 is closed: the "eight not-found reporting arms" figure is replaced by a
  per-site-neutralization-derived census of nineteen candidate arms (CONTROLLED=3, SIBLING-ONLY=0,
  UNCONTROLLED=16), including the four sites the backlog review named as never independently
  neutralized, with the derivation method, date and full bound stated in the docstring.
- 999.31 is now fully disposed across this phase's two plans: items 1 and 2 closed by plan 22-05,
  item 3 closed-by-decision (apparatus, per D-03), item 4 closed by this plan — reserved for plan
  22-08's terminal-disposition recording in `.planning/ROADMAP.md`.
- No lock, control, branch id or gate was added anywhere in this plan; `branch_count` stays 100,
  `check-selfaudit-scan.py`'s `control_count` stays 12, `gen-gate-docs.py`'s `control_count` stays
  74, `registered_surfaces` stays 37.
- The deferred-literal ledger stands at 152 entries (net unchanged — one key swapped for another),
  `_DEFERRED_LEDGER_KEYS_DIGEST` repinned fresh to reflect the swapped key set.
- Battery confirmed `FIREWALL: GREEN (26/26)` on the full tree with this plan's one commit applied;
  both `.githooks/pre-commit` and `scripts/git-hooks/pre-commit` exit 0.
- No blockers for downstream plans in this phase.

## Self-Check: PASSED

- `[ -f scripts/check-selfaudit-scan.py ]` → FOUND (modified)
- `[ -f scripts/gen-gate-docs.py ]` → FOUND (modified)
- `git log --oneline --all | grep -q b60c3b0` → FOUND (Task 3 commit — the only commit this plan
  makes; Tasks 1-2 changed no source file and therefore have no commit of their own)
- All plan-level `<verification>` commands re-run above with observed (not assumed) output,
  including `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)`.

---
*Phase: 22-cap-the-recursion*
*Completed: 2026-09-08*
