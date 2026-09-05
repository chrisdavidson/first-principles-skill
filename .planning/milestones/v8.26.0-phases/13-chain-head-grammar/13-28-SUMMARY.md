---
phase: 13-chain-head-grammar
plan: 28
subsystem: quality-harness
tags: [chain-head-grammar, quality-harness, QUAL-01, doc-correction, traceability, phase-close]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar
    provides: "plans 13-01..13-27's complete R1-R10 grammar, the eighteen-fixture render
      contract, the chain-form surface sweep, the rendered-example claim floor, and every
      residual disposition 13-27 handed forward"
provides:
  - "A corrected mechanism explanation for the GTHOP-LATE worked example on the shipped,
    model-facing output template (IN-04)"
  - "Both | QUAL-01 | doc rows (CLAUDE.md, docs/ARCHITECTURE.md) corrected exactly once
    against the tree as it stands after plan 13-27, byte-identical from 'As of Phase 11'
    onward, with four new locked tokens proven load-bearing by an eight-mutation sweep"
  - "A disclosed, dated note recording that CHAINHEAD-01..07 and the milestone's remaining
    twelve requirements are deliberately row-less until Phase 16's lockstep registration"
  - "Phase 13 closed at FIREWALL: GREEN (23/23) with _chain_block_well_formed proven
    byte-identical to its pre-13-22 value across all seven plans in this batch"
affects: [Phase 16 (ship), any future edit to _chain_block_well_formed or the QUAL-01 doc rows]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Shared-suffix byte-identity maintained by extracting the 'As of Phase 11' onward
      substring from both doc rows, applying identical string replacements to the shared
      text, and reassembling with each file's own distinct prefix — verified by direct
      byte comparison, not by reading."
    - "Eight-mutation sweep (4 new tokens x 2 rows) run on a disposable rsync scratch copy,
      each mutation's exit code, stdout/stderr token/relpath presence checked
      programmatically, then the scratch copy diffed byte-identical against the worktree
      to confirm full restoration before deletion."

key-files:
  created: []
  modified:
    - shared/spine/references/output-template.md
    - first-principles/agents/references/output-template.md
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - scripts/check-quality-harness.py
    - docs/requirements-traceability.md

key-decisions:
  - "Task 1's two figure sets were measured with _render_example_chain_blocks (the '### Conclusion'-block
    reading leg 5 actually uses), not _chain_blocks (the section-4-slice reading), per the
    plan's explicit instruction — this reproduces the review's '19 malformed blocks' figure,
    not the alternate 7-block figure the section-4 reading would have produced."
  - "The GT-led-hop and split-head reproductions were rebuilt independently (not copied from
    the review) using the module's own live functions (_GT_HEAD_RE, _chain_block_well_formed)
    to confirm WR-06's finding by direct measurement rather than by trusting the review's prose."
  - "The new chain-form-surface-sweep and rendered-example-claim-floor descriptions were
    folded into existing legs (2) and (3) rather than added as new numbered legs (6)/(7), to
    avoid renumbering every subsequent leg reference in an already enormous shared paragraph."
  - "The CHAINHEAD deferral note was written as a new, separate blockquote paragraph
    immediately after the D-02 note rather than editing D-02's text, per the plan's explicit
    instruction that D-02 is scoped to v7.12/v7.13/v8.0 and must not be silently widened."

patterns-established: []

requirements-completed: [CHAINHEAD-01, CHAINHEAD-02, CHAINHEAD-03, CHAINHEAD-04, CHAINHEAD-05]

# Metrics
duration: ~110min
completed: 2026-09-03
---

# Phase 13 Plan 28: Close the Seventh Gap-Closure Batch — Correct Both QUAL-01 Doc Rows Once Summary

Corrected the shipped template's IN-04 mechanism explanation, rewrote both `| QUAL-01 |` doc
rows exactly once against the final post-13-27 code state (four new locked tokens, re-measured
figures, corrected attribution), and disclosed the CHAINHEAD-01..07 matrix-registration
deferral — closing Phase 13 at `FIREWALL: GREEN (23/23)` with the frozen detector unchanged.

## Task 1: IN-04 mechanism correction and figure re-measurement

**IN-04 fix.** `shared/spine/references/output-template.md`'s GTHOP-LATE explanation claimed the
form check "never evaluates the leading identifier" of a GT-led hop in a later chain position.
Read `_ARROW_LED_GT_RE`'s use inside `_chain_block_well_formed`
(`scripts/check-quality-harness.py:4389`, `if _ARROW_LED_GT_RE.match(s): break`) — the check
does match and evaluate that line; it simply terminates absorption there because the segment
has already satisfied its two-arrow requirement on the preceding hops. Replaced the sentence
with: "the check has already satisfied its two-arrow requirement on the hops that precede it, so
the leading identifier ends the chain there without changing the verdict." Regenerated the
shipped mirror with `python3 scripts/sync-content.py --write`.
`grep -c 'never evaluates the leading identifier' shared/spine/references/output-template.md
first-principles/agents/references/output-template.md` → `0` on both (verified this run).

**Figure set (i) — out-of-scope-surface parenthetical (WR-02).** Measured with
`_render_example_chain_blocks` (the `### Conclusion`-block reading leg 5 actually uses, per
task instruction) + the unmodified `_chain_block_well_formed`, against every
`shared/examples/*.md` file read via `_read_render_example_texts`:

```
--- scope: all fourteen (14 files) ---
resolvable into six sections: 10
unresolvable: 4
files with >=1 malformed ### Conclusion chain block: 7
malformed ### Conclusion blocks total: 19
--- scope: the other twelve (non-claiming) (12 files) ---
resolvable into six sections: 9
unresolvable: 3
files with >=1 malformed ### Conclusion chain block: 7
malformed ### Conclusion blocks total: 19
```

Scoped to "the other twelve (non-claiming)" — matching the doc row's own framing — this
replaces the stale, arithmetically-inconsistent "eight of ten resolvable... four files do not
resolve" (10 + 4 = 14, misattributed to twelve) with "three do not resolve into six template
sections at all; seven of the nine that do carry at least one malformed section-4 chain, 19
malformed blocks in total" — matching `13-REVIEW.md` WR-02's own measured table exactly.

**Figure set (ii) — chain-start-candidate behaviour (WR-06).** Independently reconstructed both
named reproductions and drove them through the live, unmutated `_chain_block_well_formed`:

- GT-led-hop reproduction (a `→ GT-9's stated duty cycle...` line appended after the second
  arrow of `shared/examples/ishikawa-fishbone.md`'s first `### Conclusion` chain):
  `_GT_HEAD_RE` matched **2** lines in the block (the head and the GT-led hop) — confirming
  WR-06's count exactly. The block scored `True` (conforming).
- Split-head reproduction (the C1/C2/C4/C5 head wrapped across two physical lines, arrows
  following): stepping through `_chain_block_well_formed`'s own per-candidate loop by hand
  showed **2** candidates actually examined — the first (`C1 (2.20× at full duty) + C2
  (conditional on an`) scored nothing (no continuation absorbed, `matched=False`); the second
  (`unmeasured threshold) + C4 (...) + C5 (...)`) absorbed both arrow lines and scored `True`.
  This is a later candidate literally absorbing an earlier, unresolved one — the mechanism the
  retracted sentence claimed could not happen.

Verdict: the "exactly one examined chain-start candidate" claim does **not** survive
measurement. Replaced with the operative property WR-06 gives: "the first chain-start candidate
in each of those blocks already satisfies the form check's two-arrow requirement on its
truncated segment, so the block scores conforming regardless of what follows."

`python3 scripts/sync-content.py --check` → exit 0. `bash scripts/check-firewall-battery.sh` →
`FIREWALL: GREEN (23/23)` (both verified this run). Committed `dfffc39`.

## Task 2: Correct both `| QUAL-01 |` rows once, pin four new locked tokens

Extracted the "As of Phase 11" onward substring from both rows (confirmed byte-identical before
editing, 11782 chars), applied nine targeted string replacements to the shared substring only
(each old substring confirmed to occur exactly once before replacing), and reassembled each
file with its own distinct prefix. Corrections applied:

1. Fixture/family counts: fifteen → eighteen worked examples (added the R10 over-rejection
   bound and the `R-HEAD-PERIOD-BAD`/`R-HEAD-PERIOD-OK`/`R-HEAD-PERIOD-LATE` triple, plan
   13-26); ten → thirteen chain-family fixtures; fifteen → eighteen locked ids.
2. Cross-surface literal reconciliation: nine (R1-R9) → ten (R1-R10) hand-transcribed
   literals; per-surface counts updated (rubric: R1,R6-R10; `reason-upward.md`: R6-R10;
   contract surfaces: all ten).
3. Named the **chain-form surface sweep** (`_render_chain_form_surface_problems`, plan 13-24)
   and the point-back fork `estimate-detail.md`/`theoretical-limit-detail.md` took instead of
   registration.
4. Named the **rendered-example claim floor** (plan 13-23).
5. Replaced the stale out-of-scope parenthetical with task 1's re-measured figures.
6. Replaced the falsified "exactly one examined chain-start candidate" sentence with the
   operative property task 1 confirmed.
7. Added R10's over-rejection bound to DISCLOSED LIMITATIONS alongside R7/R9's under-detection
   bounds (covering both directions, closing round-6 gap-4), and folded in 13-27-SUMMARY's
   HANDED TO 13-28 WR-06 advisory verbatim (the `Cn`-as-head-input worked-example gap).

Code side: added `over-rejection bound`, `R-HEAD-PERIOD-BAD`, `chain-form surface sweep`,
`rendered-example claim floor` to `_QUAL01_DOC_ROW_TOKENS` and the registry-lock
`expected_qual01_doc_row_tokens` copy (each with a per-token rationale comment in the existing
convention), moved the negative-case count floor from `26` (2×13) to `34` (2×17), and updated
the `_selftest_render_contract` docstring's count-lock sentence to match (the `(m2) DOCSTRING
COUNT LOCK` derives its expectation live from the two registries, so a stale docstring number
fails self-test by name).

Verification (all run this session):
- Byte-comparison of both rows' "As of Phase 11" onward text: **identical**.
- `grep -c 'over-rejection bound' CLAUDE.md docs/ARCHITECTURE.md` → `1`/`1`; same for
  `R-HEAD-PERIOD-BAD`, `chain-form surface sweep`, `rendered-example claim floor`.
- `grep -c 'eight of ten resolvable' CLAUDE.md docs/ARCHITECTURE.md` → `0`/`0`.
- `grep -c 'exactly one examined chain-start candidate' CLAUDE.md docs/ARCHITECTURE.md` →
  `0`/`0`.
- `python3 scripts/check-quality-harness.py --self-test` → exit 0.
- **Eight-mutation sweep**, on a disposable `rsync --exclude .git --exclude .venv --exclude
  .pytest_cache` scratch copy: for each of the 4 new tokens × 2 rows, stripped only that token
  from that file's `| QUAL-01 |` line, ran `--self-test`, confirmed non-zero exit naming both
  the token and the relpath, then restored the original text. All 8/8 mutations detected
  (`exit=1`, token and relpath both present in output, in every case). The scratch copy was
  diffed byte-identical against the worktree after the sweep (both `CLAUDE.md` and
  `docs/ARCHITECTURE.md`, `diff` exit 0) before deletion — confirming no residual mutation
  leaked.
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (23/23)`.

Committed `e39550b`.

## Task 3: Disclose the CHAINHEAD matrix deferral, record closing evidence

Added a dated, separate blockquote note to `docs/requirements-traceability.md`, placed
immediately after (not inside) the existing v8.0 D-02 note: `CHAINHEAD-01..07` and the
milestone's remaining twelve requirements (Phase 14's LEDGER-01..04, Phase 15's SCAN-01..04,
Phase 16's SHIP-01..04) are deliberately row-less until Phase 16 registers all nineteen in one
lockstep batch, citing ROADMAP's Phase 16 success criterion 3 verbatim ("This milestone's 19
requirements are registered as matrix rows; the resulting coverage-headline move ... is produced
by `HEADLINE-LOCK`'s sweep rather than a hand edit, and the sentinel confirms it."). No coverage
figure was touched — `git diff docs/requirements-traceability.md` shows no `175`/`91`/`0`/`266`
figure line changed.

Closing evidence, all captured this session:
- `grep -c 'CHAINHEAD' docs/requirements-traceability.md` → `3` (the new note; ≥1 required).
- The note names "Phase 16" and "success criterion 3" explicitly.
- `python3 scripts/check-traceability.py --self-test` → exit 0, `HEADLINE-LOCK PASS` on every
  named sub-check.
- `python3 scripts/check-version-stamps.py` → exit 0, `17 stamps, all '8.25.0'` — compared
  directly against `git show 58c8e968:.claude-plugin/marketplace.json` (the pre-batch base
  commit), also `"8.25.0"`. Unchanged.
- `python3 scripts/sync-content.py --check` → exit 0.
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (23/23)`.
- `git status --porcelain` → empty after the commit.
- **Detector digest comparison:** `git diff 66e4cc4 HEAD -- scripts/check-quality-harness.py`'s
  first changed hunk starts at line 6521; `_chain_block_well_formed` (lines 4277-4397, 121
  lines) sits entirely outside every changed hunk across all three of this plan's commits and
  all seven plans in the batch. Direct extraction (`sed -n '4277,4397p'`) from the current tree
  and from `git show 66e4cc4:scripts/check-quality-harness.py` (the pre-13-22 commit) diffed
  **byte-for-byte identical** (`diff` exit 0, 121 lines both sides). The self-test's own
  `chain_detector_pin` sub-check, which asserts the live source's sha256 against the pinned
  `_CHAIN_DETECTOR_PINNED_DIGEST` (`sha256:d7d42d7a0bd781bd...`, `scripts/check-quality-harness.py:4436`),
  reported `PASSED` on every run this session.

Committed `5bbad66`.

## Deviations from Plan

None — plan executed exactly as written. The one environment step outside the plan's own text
was running `uv sync --group dev` in this worktree before the first firewall-battery run:
each Claude Code worktree is a separate checkout, and `.venv/` (gitignored) does not carry over
from the main repo's checkout, so `VAL-03`'s pytest leg reported `[PREREQ]`/`FIREWALL: BLOCKED`
until the tracked `pyproject.toml`/`uv.lock` recipe (documented in `CLAUDE.md`'s own commands
section) was synced. This installs nothing beyond the project's own already-vetted dev
dependencies (`pytest`, `pyyaml`, etc., per `uv.lock`), so it is environment setup, not a
package-legitimacy decision under Rule 3's exclusion.

## Assumption Drift (advisory)

None material. The plan's read_first pointers (13-REVIEW.md, 13-VERIFICATION-round6.md,
13-27-SUMMARY.md) matched the live tree exactly at every location cited — no drift found
between what those documents described and what the code and doc rows actually stated before
this plan's edits.

## Known Stubs

None. This plan only edits documentation/prose (a template's mechanism explanation, two doc
rows, a traceability note) and a self-test's registry/floor constants — no UI, no data-fetching
code, nothing that could carry a stub in the sense this section tracks.

## Threat Flags

None. All four files this plan modifies (`shared/spine/references/output-template.md` and its
generated mirror, `CLAUDE.md`, `docs/ARCHITECTURE.md`, `scripts/check-quality-harness.py`,
`docs/requirements-traceability.md`) are within the plan's own declared `files_modified` list
and threat model; no new network endpoint, auth path, file-access pattern, or schema change at a
trust boundary was introduced.

---
*Phase: 13-chain-head-grammar*
*Completed: 2026-09-03*

## Self-Check: PASSED

- FOUND: `shared/spine/references/output-template.md` (IN-04 fix present, verified via grep
  this run)
- FOUND: `first-principles/agents/references/output-template.md` (regenerated mirror present)
- FOUND: `CLAUDE.md` (corrected `| QUAL-01 |` row present)
- FOUND: `docs/ARCHITECTURE.md` (corrected `| QUAL-01 |` row present)
- FOUND: `scripts/check-quality-harness.py` (four new tokens, updated floor, present)
- FOUND: `docs/requirements-traceability.md` (CHAINHEAD deferral note present)
- FOUND: commit `dfffc39` (Task 1) — `git log --oneline --all | grep dfffc39` confirmed
- FOUND: commit `e39550b` (Task 2) — `git log --oneline --all | grep e39550b` confirmed
- FOUND: commit `5bbad66` (Task 3) — `git log --oneline --all | grep 5bbad66` confirmed
- `python3 scripts/sync-content.py --check` exits 0 (verified this run)
- `python3 scripts/check-quality-harness.py --self-test` exits 0 (verified this run)
- `python3 scripts/check-traceability.py --self-test` exits 0, HEADLINE-LOCK passing (verified
  this run)
- `python3 scripts/check-version-stamps.py` exits 0, `8.25.0` unchanged from pre-batch commit
  `58c8e968` (verified this run)
- `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (23/23)` (verified this run,
  final run after all three commits)
- `git status --porcelain` empty after the final commit (verified this run)
