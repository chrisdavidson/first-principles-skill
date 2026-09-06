---
phase: 20-live-conformance
plan: 03
subsystem: testing
tags: [conformance, live-capture, quality-harness, disposition, chain-of-custody]

# Dependency graph
requires:
  - phase: 20-live-conformance
    provides: "plan 20-02's 8 committed live .jsonl+.md captures under tests/live-conformance-v9.0/, all outcome completed"
provides:
  - "Offline detect_defects reading over all 8 landed analyses, both D-20-A rate figures, and the two PR-P1 comparisons"
  - "A well-formed disposition (accept-with-reason x5, fix x3) for every catalog row's Notes cell"
  - "tests/live-conformance-v9.0/README.md — the fixture's chain-of-custody record"
affects: [20-04, 20-05, 20-06]

# Tech tracking
tech-stack:
  added: []
  patterns: ["offline scoring pass over live captures before any surface-code change", "disposition-cell-as-filed-defect (fix / accept-with-reason / defer-with-owner)"]

key-files:
  created:
    - tests/live-conformance-v9.0/README.md
  modified:
    - tests/live-conformance-catalog.md

key-decisions:
  - "All 3 non-clean rows (Q-P2, PR-N1, PR-N2) dispositioned fix: against shared/spine/references/output-template.md's Verdict Vocabulary section and validation-rubric.md Criterion 2's Rigorous descriptor, never against a detector; no backlog entry needed since fix: only requires naming a shared/ path"
  - "5 clean rows dispositioned accept-with-reason:, each explicitly stating a clean reading means the instrument found nothing, against adversarial-corpus's published 10-of-13 false-negative rate — never a quality endorsement"

requirements-completed: [CONF-09]

# Metrics
duration: "~1h"
completed: 2026-09-06
---

# Phase 20 Plan 03: Score, Disposition and Chain-of-Custody Summary

**Scored all 8 landed live captures with the unmodified, CONTRACT-06-frozen `detect_defects`: primary rate 5 of 8 clean, secondary conditional rate 5 of 8 (all 8 completed); filed a specific, named disposition against the prescription for every non-clean row (Q-P2 31/31 nonconforming verdict cells, PR-N1 and PR-N2 1 cell each) and an honest, non-endorsing accept-with-reason for every clean row; wrote the fixture's machine-verified chain-of-custody README.**

## Performance

- **Duration:** ~1h
- **Started:** 2026-09-06 (continuation of same session lineage as 20-01/20-02)
- **Completed:** 2026-09-06
- **Tasks:** 3 (1 offline-scoring read-only task with no commit, 2 auto tasks each committed)
- **Files modified:** 2 (`tests/live-conformance-catalog.md` edited, `tests/live-conformance-v9.0/README.md` created); zero script edits

## Task 1: Offline Scoring — Full Per-Run Reading

Ran `python3 scripts/check-quality-harness.py --detect-defects tests/live-conformance-v9.0 --out /tmp/live-conformance-defects.tsv` (exit 0, 8 rows written) and independently re-derived every D-20-A count directly from `report-conformance.py`'s own `build_row`-equivalent path (`_render_example_chain_blocks` + `_chain_block_well_formed` for `heading_malformed_blocks`, `detect_defects` for `nonconforming_verdict_cells` and `silent_untraced_claims`, `_slice_sections`'s absence of a raised `SectionResolutionError` for `section_resolution`). This task wrote nothing to disk (no commit) — it is a pure read/score pass, verified by `git status --porcelain` staying empty throughout.

| id | outcome | `section_resolution` | `heading_malformed_blocks` | `nonconforming_verdict_cells` | `silent_untraced_claims` | clean |
|---|---|---|---|---|---|---|
| Q-P1 | completed | OK | 0 | 0 | 0 | yes |
| Q-P2 | completed | OK | 0 | 31 | 0 | no |
| Q-P3 | completed | OK | 0 | 0 | 0 | yes |
| PR-P1 | completed | OK | 0 | 0 | 0 | yes |
| PR-P2 | completed | OK | 0 | 0 | 0 | yes |
| PR-N1 | completed | OK | 0 | 1 | 0 | no |
| PR-N2 | completed | OK | 0 | 1 | 0 | no |
| PR-P1-R2 | completed | OK | 0 | 0 | 0 | yes |

No row read `no-analysis` in any of the four defect columns — all 8 runs completed and produced a persisted, readable `.md` (`classify_invocation_outcome` independently re-run against every `.jsonl` in this session, all 8 return `completed`).

**Primary rate (clean over runs attempted):** `5 of 8`.
**Secondary conditional rate (clean over runs completed):** `5 of 8` (identical figure here because all 8 attempted runs completed — the two rates only diverge on a transport-layer stub, which did not occur).

**Outcome breakdown:** 8 `completed` / 0 `rate_limit_stub` / 0 `transport_error_stub` / 0 `no_terminal_result`.

**The three non-clean runs, exact defect text located and quoted (not merely counted):**
- **`Q-P2` — 31 of 31 Verdict cells nonconforming.** The analysis used its own richer vocabulary throughout the Assumptions Table (`Accepted as a modelling convention`, `**Unverified — flagged**`, `**Unverified — flagged, LOAD-BEARING**`, `**Challenged — rejected**`, `**Verified approximately true**`, `**Partially verified by construction**`) instead of the prescribed leading token `Accept`/`Challenge`/`Discard` immediately followed by an em-dash. Verified by calling `_verdict_cells` + `_verdict_conforms` directly against the sliced section 2 text — every one of the 31 extracted cells fails the token-then-em-dash form check.
- **`PR-N1` — 1 of 12 nonconforming (assumption A3).** Cell text: `**Accept as necessary, Challenge as sufficient** — it closes one of the three conditions in C1 and leaves the other two manual`. The compound-verdict phrase inserts descriptive text between the leading token and the em-dash, so the regex's `\s*[*_]*\s*—` gap between token and separator is not satisfied.
- **`PR-N2` — 1 of 19 nonconforming (assumption A4).** Cell text: `Accept provisionally — affects which price constants apply, not the structure`. The adverb `provisionally` sits between the token and the em-dash for the same structural reason.

**PR-P1 vs PR-P1-R2 (within-body variance, D-02):** both read clean (0/0/0/0). `conclusion_claims` (6 vs. 11), `verdict_cells` (21 vs. 17) and `chain_blocks` (9 vs. 9) differ, so two runs of the identical prompt against the identical HEAD body are not verbatim-identical in shape even though the conformance reading is unchanged. **Explicit caveat, as required:** at N=2 this is a single observation about run-to-run variance, not evidence of a trend.

**PR-P1 (HEAD) vs PR-P1 (v8.24.0, read-only, `tests/quality-provenance-v8.24/PR-P1.md`):** the v8.24.0 capture scores `conclusion_claims=4`, `untraced_claims=3`, `silent_untraced_claims=3`, `verdict_cells=16`, `nonconforming_verdict_cells=0`, `chain_blocks=5`, `selfaudit_disagreements=1` — under D-20-A's own rubric, the v8.24.0 capture would **not** have scored clean (3 silent untraced claims), while the HEAD capture does. **Explicit caveat, as required:** at N=2 across two different bodies separated by 28 rewritten worked-example files, this is a two-point observation consistent with an improvement and equally consistent with ordinary run-to-run variance (as `PR-P1`/`PR-P1-R2` already demonstrates on the identical body) — it is not strong enough alone to attribute the difference to Phase 18's exemplar rewrite. `git status --porcelain tests/quality-provenance-v8.24` confirmed empty both before and after this comparison — the registered `_FROZEN_PATHS` fixture was read, never written.

`python3 scripts/check-quality-harness.py --self-test` exited 0 (all three CONTRACT-06 pins byte-unchanged) both before and after this task.

## Task 2: Filed Dispositions

Replaced all 8 `disposition: MISSING` placeholders in `tests/live-conformance-catalog.md`'s Notes column. Only the text after the literal `disposition: ` marker was edited in each row; every row's `text` field (prompt cell) was independently confirmed byte-identical before/after via `_read_quality_catalog` field comparison.

- **5 clean rows** (`Q-P1`, `Q-P3`, `PR-P1`, `PR-P2`, `PR-P1-R2`) — `accept-with-reason:`, each stating the 0/0/0/0 reading and explicitly that, against `adversarial-corpus`'s published 10-of-13 false-negative rate, a clean reading here means *this instrument found nothing* — never that the analysis is correct. `PR-P1` and `PR-P1-R2`'s dispositions additionally point to the plan's comparison readings.
- **3 non-clean rows** (`Q-P2`, `PR-N1`, `PR-N2`) — `fix:`, each naming the exact offending cell text and filing the defect against `shared/spine/references/output-template.md`'s Verdict Vocabulary section and `shared/spine/references/validation-rubric.md` Criterion 2's Rigorous descriptor. No disposition names a detector; no backlog entry was needed since a `fix:` disposition satisfies the acceptance criterion by naming a `shared/` path directly.

**Verification performed (all against the real, edited file, not assumed):**
- `_read_quality_catalog` parses all 8 rows; every `notes` cell's post-`disposition: ` text starts with one of `fix` / `accept-with-reason` / `defer-with-owner` — confirmed programmatically.
- `/usr/bin/grep -c 'disposition: MISSING'` → `0`.
- Grepped the 8 extracted **disposition-cell texts** (not the whole file) for `_chain_block_well_formed`, `_conclusion_claims`, `_slice_sections`, `widen`, `loosen` — zero hits in any disposition cell. (A whole-file grep for these terms returns non-zero because the phase's own pre-existing D-20-B decision-record prose, written by plan 20-01 and unrelated to any disposition cell, restates the CONTRACT-06 hard constraint in its own words — that prose is outside every Notes cell and is not part of this task's edit surface; the threat model's T-20-10 mitigation is explicitly scoped to "the disposition cells", which is the check actually run here.)
- Byte-identity of every row's prompt (`text`) field confirmed via field-by-field comparison against the pre-edit committed version at `HEAD~1` (all match; only `notes` changed).
- `python3 scripts/check-quality-harness.py --self-test` exits 0.
- `git diff --name-only scripts/` empty.

**Commit:** `4a15d74` — `test(20-03): file dispositions for all 8 live-conformance catalog rows`

## Task 3: Chain-of-Custody README

Wrote `tests/live-conformance-v9.0/README.md` (244 lines) following the `tests/quality-provenance-v8.24/` and `tests/quality-ledger-v8.26/` precedent shape: Purpose, Provenance (body sha `41696efda42c29bb3f26f20143023411d9eb7ae6`, confirmed unchanged from plan 20-01's recorded sha and independently re-diffed against HEAD to show no `shared/`/`first-principles/` drift), Chain of custody (per-file sha256/byte/line-count table, all 16 tracked files including `.gitkeep`), Run inventory and outcomes (the same 8-row table as Task 1, both rate figures), the two PR-P1 comparisons, Bypass disclosure (D-04), the carried-forward non-interactive-branch disclosure finding from 20-02, Not reproducible, Captures-not-read-this-phase (D-06, `999.12` left open), Frozen-evidence discipline and sequencing note (registration deferred to plan 20-06; `_FROZEN_PATHS` confirmed still 20 entries), and Superseded attempts (none — stated explicitly rather than omitted).

**Verification performed:**
- Machine sha256 check: every one of the 16 tracked files in the directory tree has its filename and true, freshly-recomputed sha256 present in the README text — exit 0.
- Literal-string presence checks (each `grep -c` ≥ 1): the 40-character body sha, `conditional on delegation having occurred`, `no command in this repository reproduces`, `999.12`, `n/a`, `_FROZEN_PATHS` — all confirmed present as contiguous, single-line substrings after two line-wrap corrections (the first draft split two of these phrases across a markdown soft-wrap, which a literal grep does not span; both sentences were reflowed onto single lines).
- `tests/live-conformance-v9.0/catalog.md` confirmed absent.
- `python3 scripts/report-conformance.py --check` → `report-conformance: PASS — no drift` (adding the README does not move any published figure, since nothing reads this surface yet).
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (25/25)`.
- `_FROZEN_PATHS` array counted programmatically → still 20 entries (no premature registration).
- `python3 scripts/check-quality-harness.py --self-test` → exit 0.
- `git diff --name-only scripts/` → empty.

**Commit:** `a9ff6e3` — `test(20-03): add chain-of-custody README for the live-conformance fixture`

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] README's two acceptance-criterion literal strings were split across a markdown line-wrap on first draft**
- **Found during:** Task 3's automated verify command
- **Issue:** `conditional on delegation having occurred` and `no command in this repository reproduces` were each authored as prose that happened to soft-wrap mid-phrase in the source markdown (`having\noccurred`, `this\nrepository`). A literal `grep -c` over the file does not match across a newline, so both checks read `0` on first run.
- **Fix:** Reflowed both sentences onto single unwrapped lines in the source file. No content changed, only line-wrapping.
- **Verified:** Re-ran the literal-string grep for all 6 required strings; all report `>= 1` after the fix.
- **Files modified:** `tests/live-conformance-v9.0/README.md`
- **Commit:** `a9ff6e3` (the fix was applied before the file was ever committed, so no separate commit was needed)

No other deviations. The `_verdict_conforms` mechanism was called read-only to identify the exact offending cell text for each non-clean disposition; it was never edited, and the CONTRACT-06 self-test confirms this at the end of every task.

## Assumption Drift (advisory)

None material. The plan's `<hard_constraint>` anticipated "a real, unflattering number" appearing in this plan; the observed primary rate (5 of 8) matched that expectation in kind, and no working assumption drifted from the plan's own framing.

## Issues Encountered

None blocking. The two line-wrap issues above were caught and fixed within Task 3 before its first commit.

## User Setup Required

None.

## Next Phase Readiness

- `tests/live-conformance-catalog.md` now carries a real, specific, named disposition for all 8 rows — ready for plan 20-04's `report-conformance.py` fifth surface to read via the `disposition: ` marker.
- `tests/live-conformance-v9.0/README.md` is machine-verified against the real bytes on disk and states everything plan 20-04's and 20-06's own read_first lists require (body sha, both rate figures, D-04/D-06 disclosures, the sequencing note).
- Battery GREEN 25/25, `report-conformance.py --check` clean, zero script edits, `_FROZEN_PATHS` still 20 entries, all three CONTRACT-06 pins byte-unchanged throughout.
- No blockers for plan 20-04.

---
*Phase: 20-live-conformance*
*Completed: 2026-09-06*

## Self-Check: PASSED

- `tests/live-conformance-v9.0/README.md` — FOUND
- `tests/live-conformance-catalog.md` — FOUND
- `4a15d74` (Task 2 commit) — FOUND
- `a9ff6e3` (Task 3 commit) — FOUND

No missing items.
