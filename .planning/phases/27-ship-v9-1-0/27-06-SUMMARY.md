---
phase: 27-ship-v9-1-0
plan: 06
subsystem: release-act-two-matrix-rows-and-headline-sweep
tags: [release, matrix-rows, headline-sweep, HEADLINE-LOCK, containment, disclosed-bound, REL-07]

dependency-graph:
  requires:
    - "27-05: release act one (all 17 version stamps at 9.1.0), so this plan's release act runs
      against a tree already at 9.1.0"
    - "27-04: the pre-release recurrence reading, whose 61 FENCED sites this plan's release act
      must not touch"
  provides:
    - "_rows_v91() (18 rows, 9 reproducible + 9 audit-only) and the V91-ROWS equality sentinel in
      scripts/check-traceability.py"
    - "The coverage headline moved 208/97/0/305 -> 217/106/0/323 across all five
      COVERED_HEADLINE_SURFACES plus docs/requirements-matrix.md and docs/data/matrix.json"
    - "docs/gates/CONF-SURFACE.md's numbered disclosed bound (14), naming the two surfaces
      HEADLINE-LOCK verifies but does not produce"
    - "REL-07 ticked in .planning/REQUIREMENTS.md with evidence matching the mechanism's measured
      reach"
  affects:
    - "plan 27-07 (fence adjudication) -- no FENCED site collided with this plan's release act;
      one genuinely new containment finding ('18' on CLAUDE.md) was resolved, not deferred, as
      disclosed below"
    - "plan 27-09 (post-arm reading) -- the tree this plan produces is the one that reading
      measures"

tech-stack:
  added: []
  patterns:
    - "in-process testing of new prose against _scan_text_for_literal_hits() and
      _containment_missing_numbers() before it reaches disk (Phase 26 precedent, reused here for
      both the headline-history row and the new disclosed bound)"
    - "chain_terminus_problems()'s three-outcome discriminator (current/stale/uncorroborable) used
      diagnostically to locate the one delta chain the headline move invalidated"

key-files:
  created: []
  modified:
    - scripts/check-traceability.py
    - docs/requirements-matrix.md
    - docs/data/matrix.json
    - docs/requirements-traceability.md
    - docs/COMPONENT-DIAGRAM.md
    - docs/README.md
    - docs/MEASUREMENT-MAP.md
    - CLAUDE.md
    - docs/gates/CONF-SURFACE.md
    - docs/gates/TRACE-03.md
    - scripts/gen-gate-docs.py
    - .planning/REQUIREMENTS.md

decisions:
  - "The v9.1 hop appended to CLAUDE.md's requirements-ledger chain introduced a new bare digit
    ('18', the v9.1 milestone's own row count) that CONTAIN-01's containment check on CLAUDE.md
    had never seen before -- confirmed live as the ONLY new missing number (every other digit
    CLAUDE.md carries was already ledgered). Resolved as a Rule 1 fix in the SAME commit: added
    ('CLAUDE.md', '18') to _DEFERRED_CONTAINMENT_HITS as CANNOT-REACH (no
    check-traceability.py --describe field exposes a per-milestone matrix-row count), re-pinned
    _CONTAINMENT_LEDGER_MAX 20 -> 21 and its keys digest. scripts/gen-gate-docs.py was not in this
    plan's declared files_modified list -- disclosed as a deviation below."
  - "Bound (14) on docs/gates/CONF-SURFACE.md is prose-only, no new LITERAL_SCAN_DISCLOSED_BOUNDS
    anchor -- per the plan's own preference, avoiding the coincidental-corroboration trap Phase 26
    plans 05-07 each hit. Confirmed no anchor added: disclosed_bounds_anchors stays 14 before and
    after."
  - "The draft bound's first wording ('five registered surfaces', 'five surfaces') tripped two
    non-exempt literal-scan hits (spelled-out numbers) on the live tree despite testing clean
    against a mis-called scanner primitive (wrong argument order caught the mistake only once the
    real --check was re-run) -- reworded to point at COVERED_HEADLINE_SURFACES and the
    registered_surfaces/narrative_regions generated fields instead of stating either population as
    a digit, then re-verified at zero hits with the corrected call."

requirements-completed: [REL-07]

metrics:
  duration: "~1h50m"
  completed: "2026-09-11"
---

# Phase 27 Plan 06: Release Act Two — Matrix Rows and Headline Sweep Summary

Registered this milestone's 18 requirements as matrix rows behind a live-derived `V91-ROWS` equality sentinel, let the coverage headline move as a consequence of that registration (`208/97/0/305 → 217/106/0/323`), swept it across all five `COVERED_HEADLINE_SURFACES` plus both tracked matrix artifacts via `HEADLINE-LOCK`, extended the one delta chain the move invalidated, and published the sweep's actual reach as a new numbered disclosed bound rather than let REL-07's clause read wider than the mechanism measures.

## What was built

**Task 1 — `_rows_v91()` and `V91-ROWS` (commit `8f16db9`, landed with Task 2).** Added `_rows_v91()` immediately after `_rows_v9()` in `scripts/check-traceability.py`, returning the 18 `MatrixRow` objects from the plan's own D-27-07 table: 9 reproducible (`CONTAIN-01`, `CONTAIN-02`, `CONTAIN-04`, `NARR-02`, `RATCHET-01`, `RATCHET-02` → `scripts/gen-gate-docs.py`; `REL-05` → `scripts/check-version-stamps.py`; `REL-06` → `scripts/check-firewall-battery.sh`; `REL-07` → `scripts/check-traceability.py#_self_test_headline_lock`) and 9 audit-only (`PROSE-01..04`, `CONTAIN-03`, `NARR-01`, `RATCHET-03`, `RATCHET-04`, `REL-08`), each carrying its own named `gap_rationale` transcribed from D-27-07's table — no blanket count-based reasoning. Registered the extend call in `build_matrix_rows()` as inclusion path (j), with its own docstring paragraph mirroring paths (a)-(i)'s style.

Added `_self_test_v91_rows_sentinel()` mirroring `_self_test_v9_rows_sentinel()`'s eight lettered controls exactly: (a) row-count drift guard (18); (b) `bare_id` set EQUALITY against `_EXPECTED_V91_IDS`; (c) tier partition pinned BY ID via `_EXPECTED_V91_AUDIT_ONLY_IDS` (all nine named individually); (d) deep-resolve every reproducible row's `artifact_link`, assert every audit-only row's link is empty; (e) REL-07 positive counter-check; (f) milestone/key lock; (g) capability lock; (h) LIVE ANCHOR FLOOR asserting the observed `#_self_test_*`-prefixed anchor set equals exactly `{'_self_test_headline_lock'}`, then a live positive confirming REL-07's link resolves to `[]`. No `MatrixRow` literal and no bare `18` appears anywhere inside the sentinel outside the count assertion's own message (confirmed by direct source-slice inspection). Registered the dispatch call in `_run_self_test()` immediately after `_self_test_v9_rows_sentinel` and before `_self_test_headline_lock`, and added a `V91-ROWS:` paragraph to `_run_self_test()`'s own docstring roster.

**Roster cross-check (run this session, `.planning/` unreadable by any gate):**

```python
ids = {r.bare_id for r in ct._rows_v91()}
req_ids = set(re.findall(r'^- \[[ x]\] \*\*((?:PROSE|CONTAIN|NARR|RATCHET)-\d+|REL-0[5-8])\*\*',
                          open('.planning/REQUIREMENTS.md').read(), re.M))
ids == req_ids  # -> True
```

Output: `row count 18`, `equal: True`, `missing from rows: set()`, `extra in rows: set()`. `_rows_v91()`'s docstring records the residual limitation in one sentence, citing CONTEXT.md D-17.

Per the acceptance criteria, at the end of Task 1 (before Task 2's sweep) `--self-test` was **expected** to exit non-zero: all eight `V91-ROWS` controls passed, and the only failures were `HEADLINE-LOCK` naming the five registered surfaces plus the matrix artifacts, still stating the pre-registration headline — confirmed live, transcribed above the sweep. No commit was made at that point (the pre-commit hook would have blocked it, and landing registration without its sweep would put a contradictory tree in history) — Tasks 1 and 2 landed in one commit as instructed.

**Task 2 — emit, sweep, extend (commit `8f16db9`).** Ran the sanctioned `emit` command (`docs/requirements-matrix.md` + `docs/data/matrix.json`, 18 new `v9.1/` rows, `git diff` on both shows no hand edit). The live `--describe` headline (`217 reproducible / 106 audit-only / 0 gap / 323 total`) matched D-27-07's predicted arithmetic (`208+9=217`, `97+9=106`, `305+18=323`) exactly — no re-examination needed. Ran `gen-gate-docs.py --write`, which touched `CLAUDE.md`, `docs/README.md`, `docs/MEASUREMENT-MAP.md` (the three `_NarrativeRegion`-backed headline sentences) and `docs/gates/CONF-SURFACE.md` / `docs/gates/TRACE-03.md` (their own generated Facts fences) as mechanical side effects; `docs/ARCHITECTURE.md` was confirmed unaffected (its TRACE-03 row states no raw digit, only field names). Hand-edited the two surfaces HEADLINE-LOCK verifies but does not write: `docs/requirements-traceability.md` line 7's coverage-headline value, line 9's row-count sentence, the "97 audit-only rows"/"106 audit-only rows" bold line, the "Generated matrix (N rows)" cross-link, a new headline-history row 14 (naming all nine audit-only IDs individually with reasons transcribed from `_rows_v91()`'s own docstring), and the "moved twelve times" preamble recount — all following row 13's exact precedent shape (confirmed by diffing this plan's edits against `ed73189`, v9.0's own analogous sweep commit); and `docs/COMPONENT-DIAGRAM.md`'s two Mermaid node labels (`MATRIX` and `TRACEABILITY`), again matching that same precedent commit's shape.

**The one FENCED site NOT touched, confirmed deliberately:** `docs/requirements-traceability.md:294`'s "the current 91-row audit-only total" is a *different*, unrelated stale reference in the GAP-02 candidate-work-list section — found by Reader B in plan 27-04's pre-arm reading and recorded FENCED. It was untouched in v9.0's own analogous sweep (`ed73189`) too, confirming it is a pre-existing, separately-tracked staleness, not part of this release act's scope; its content is confirmed byte-identical before and after this plan (only its line number shifted, from my own insertions above it).

**Delta-chain extension.** `chain_terminus_problems()` initially flagged `CLAUDE.md`'s own requirements-ledger chain as `uncorroborable` (its terminus still read `208/97`/`305` against a page whose fence now stated `217/106`/`323`) — extended the chain with the new v9.1 hop (`208/97 → 217/106, row count 305 → 323`), re-verified `current` afterward. No other surface's chain was invalidated (`docs/gates/SCAN-GUARD.md` and `docs/gates/CONF-SURFACE.md`'s own growth chains were unaffected by this plan's edits).

**Genuinely new containment finding, resolved (Rule 1).** Extending CLAUDE.md's chain introduced a bare "18" with no same-page in-fence match — `_containment_missing_numbers()` confirmed it as the *only* new missing number (every other digit on the page was already ledgered). Added `('CLAUDE.md', '18')` to `_DEFERRED_CONTAINMENT_HITS` as `CANNOT-REACH` (re-verified live: `check-traceability.py --describe` exposes no per-milestone row-count field), re-pinned `_CONTAINMENT_LEDGER_MAX` 20 → 21 and its keys digest, and fixed one self-test control (`_control_delta_chain_hops_claude_row_count_recovered`) whose hardcoded expected terminus `('305',)` went stale with the chain extension. **`scripts/gen-gate-docs.py` was not in this plan's declared `files_modified` list** — disclosed as a deviation below.

**Task 3 — disclosed bound and REL-07 tick (commit `e67f878`).** Added numbered disclosed bound (14) to `docs/gates/CONF-SURFACE.md`, naming `docs/requirements-traceability.md` and `docs/COMPONENT-DIAGRAM.md` (citing bound (9) for the Mermaid fence) as the two surfaces HEADLINE-LOCK verifies but does not produce, and stating what REL-07's clause is satisfied in (the number is machine-derived and machine-verified) versus not satisfied in (no file is manually touched). Added prose-only, with no new `LITERAL_SCAN_DISCLOSED_BOUNDS` anchor, per the plan's stated preference — `disclosed_bounds_anchors` stays 14 before and after, so the coincidental-corroboration check Phase 26 plans 05-07 each had to run does not apply here (no anchor moved). Ticked REL-07 in `.planning/REQUIREMENTS.md` with a Category-C evidence block (transcribed below), and updated the `## Traceability` row to `Complete`.

## The headline sweep, in numbers

| Field | Before | After |
|---|---|---|
| Coverage headline (prose) | 208 reproducible / 97 audit-only / 0 gap / 305 total | 217 reproducible / 106 audit-only / 0 gap / 323 total |
| Coverage headline (slash) | 208/97/0/305 | 217/106/0/323 |
| `docs/requirements-matrix.md` rows | 305 | 323 (18 new `v9.1/` rows) |
| `containment_ledger_entries` / `_max` | 20 | 21 |
| `literal_scan_ledger_entries` / `_max` | 180 | 180 (unchanged) |
| `disclosed_bounds_anchors` | 14 | 14 (unchanged — bound (14) added no new anchor) |
| `control_count` (gen-gate-docs.py) | 112 | 112 (unchanged — one control's expected value updated, none added) |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `scripts/gen-gate-docs.py` hand-edited to resolve a genuinely new containment finding this plan's own release act introduced**
- **Found during:** Task 2, immediately after extending CLAUDE.md's delta chain with the new v9.1 hop.
- **Issue:** The new hop's text states "the 18 v9.1 milestone requirements registered as matrix rows" — a bare digit ("18") outside any generated fence. `CONTAIN-01`'s containment check (widened to reach `CLAUDE.md` at Phase 25) has no corroborating literal for "18" anywhere in CLAUDE.md's generated regions, so `gen-gate-docs.py --check` failed exit 1: `containment: CLAUDE.md states '18' outside a generated fence with no matching literal inside one (D-06)`. Confirmed by direct introspection that every OTHER missing number on the page was already an adjudicated `_DEFERRED_CONTAINMENT_HITS` entry — '18' was the sole new one, and the pre-existing "19"/"20"/"23" milestone-row-count mentions in the same paragraph pass today only by coincidental corroboration against unrelated generated fields (the same shape the `_CONTAINMENT_LEDGER_MAX` comment already documents for other entries), not by design.
- **Fix:** Added `('CLAUDE.md', '18')` to `_DEFERRED_CONTAINMENT_HITS` as `CANNOT-REACH (no harvest field)` under backlog `999.69`, re-pinned `_CONTAINMENT_LEDGER_MAX` 20 → 21 and recomputed `_CONTAINMENT_LEDGER_KEYS_DIGEST` via `_deferred_ledger_keys_digest()`, both in the same commit as the finding (`8f16db9`). Also updated `_control_delta_chain_hops_claude_row_count_recovered`'s hardcoded expected terminus from `('305',)` to `('323',)`, since the chain extension moved the live terminus and the control's assertion would otherwise fail against the real tree.
- **Why judged Rule 1 rather than a fence violation or an architectural question:** the finding is a direct, mechanical consequence of Task 2's own sanctioned action (extending the delta chain per the plan's own instruction); leaving it unresolved would fail the pre-commit hook (gate 5) and block the commit entirely; the fix follows the exact precedent shape `_DEFERRED_CONTAINMENT_HITS` already uses for ten other CLAUDE.md entries (CANNOT-REACH, no harvest field, deferred under 999.69) — no new mechanism, no widened detector, just one more enumerated, individually-adjudicated permit.
- **Scope discipline confirmed:** the ledger's entry format, its ratchet mechanism, and its ID vocabulary (999.69) are all pre-existing; nothing was invented. `git diff` on `scripts/gen-gate-docs.py` is isolated to the one new ledger entry, the `_CONTAINMENT_LEDGER_MAX`/`_CONTAINMENT_LEDGER_KEYS_DIGEST` re-pin and their comment blocks, and the one stale-terminus control fix.
- **Verification:** before the fix, `gen-gate-docs.py --check` exited 1 naming `CLAUDE.md`'s `'18'`; after, `--check` exits 0 and `--self-test` reports `SELF-TEST PASS — 112 controls run` (control count unchanged — one existing control's hardcoded expectation was corrected, none added).
- **Files modified:** `scripts/gen-gate-docs.py`.
- **Commit:** `8f16db9`.

### Non-code events, disclosed rather than silently absorbed

**2. A first draft of Task 3's new disclosed-bound prose tripped two literal-scan hits, caught only after a mis-called in-process test passed vacuously.** The first wording ("HEADLINE-LOCK verifies **five** registered surfaces... `COVERED_HEADLINE_SURFACES` registers **five** surfaces...") was tested in-process against `_scan_text_for_literal_hits()` before being written to disk, per the plan's own instruction — but the test call used the function's two positional arguments in the wrong order (`(text, relpath)` instead of the actual `(relpath, text)` signature), so it silently scanned the wrong string and reported zero hits. The mistake surfaced only when the real, on-disk `gen-gate-docs.py --check` was re-run after `--write`, which correctly found two non-exempt spelled-out-number hits ("five registered surfaces", "five surfaces"). Reworded to remove both spelled-out digit claims — pointing at `COVERED_HEADLINE_SURFACES` and the `registered_surfaces`/`narrative_regions` generated fields by name instead of stating either population as a number — and re-verified with the corrected call signature this time (`_scan_text_for_literal_hits(relpath, text)` → `[]`), then confirmed against the real `--check` (`literal_scan_non_exempt` returned to 0). Recorded here because the near-miss is instructive: a scanner-test tool used with reversed arguments passes exactly as vacuously as no test at all, and the real `--write`/`--check` cycle is what actually caught it.

---

**Total deviations:** 1 auto-fixed (Rule 1, one file outside the plan's declared `files_modified` list, disclosed above), plus 1 non-code near-miss disclosed for its own instructive value. No scope creep beyond what was necessary to land a self-consistent, gate-passing release act.

## Assumption Drift (advisory)

None material. The plan's own D-27-08 anticipated the two-surface residue and named it explicitly as the object of Task 3's disclosed bound; nothing here drifted from that framing.

## Verification (observed this session)

- `python3 scripts/check-traceability.py --self-test` → exit 0, `check-traceability --self-test: PASS`, all eight `V91-ROWS` lettered controls PASS, `HEADLINE-LOCK PASS` across every block (observed after both commits).
- `python3 scripts/check-traceability.py --describe`'s `coverage_headline` → `{'prose': '217 reproducible / 106 audit-only / 0 gap / 323 total', 'slash': '217/106/0/323'}` (observed).
- `/usr/bin/grep -c "^| v9.1/" docs/requirements-matrix.md` → `18` (observed).
- `/usr/bin/grep -l "217/106/0/323" docs/requirements-traceability.md CLAUDE.md docs/README.md docs/MEASUREMENT-MAP.md docs/COMPONENT-DIAGRAM.md` → all five paths listed (observed).
- `git diff` on `docs/requirements-matrix.md` and `docs/data/matrix.json` shows no hand edit — both produced solely by the `emit` command (observed).
- Roster cross-check: `_EXPECTED_V91_IDS == {req ids parsed from .planning/REQUIREMENTS.md}` → `True` (observed, transcribed above).
- `chain_terminus_problems()` in-process call over the four registered containment surfaces returns `[]` after the extension (observed; the pre-extension state returned one `uncorroborable` verdict for `CLAUDE.md`, confirmed transiently before the fix).
- Every FENCED pre-arm site (61 sites, plan 27-04) re-checked by direct content comparison against `faa9bfd` (the commit immediately preceding this plan) — all confirmed byte-identical; only line numbers shifted where this plan inserted content above them (`CLAUDE.md:68/330/381`, `docs/README.md:110/217`, `docs/MEASUREMENT-MAP.md:17`, `scripts/gen-gate-docs.py:3390`, `docs/requirements-traceability.md:294`).
- `python3 scripts/gen-gate-docs.py --self-test` → `SELF-TEST PASS — 112 controls run` (observed, both commits).
- `python3 scripts/gen-gate-docs.py --check` → exit 0, `harvested 22/22 expected script-backed entries` (observed, both commits).
- `python3 scripts/report-conformance.py --self-test` → `SELF-TEST PASS — 110 controls run`; `--check` → `PASS — no drift` (observed).
- `sh .githooks/pre-commit` → exit 0 (observed, both commits).
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)` (observed, final run after both commits).
- `git diff --diff-filter=D --name-only HEAD~1 HEAD` → empty for both commits (no unexpected deletions, observed).
- `/usr/bin/grep -c "^- \[x\] \*\*REL-07\*\*" .planning/REQUIREMENTS.md` → `1` (observed).
- `git check-ignore -v .planning/REQUIREMENTS.md` → confirmed gitignored, no commit expected for its edits (observed).
- Both containment-ledger pins (`literal_scan_ledger_max` 180 unchanged, `containment_ledger_max` 20 → 21) recorded before and after; the move and its re-pin landed in the SAME commit (`8f16db9`) (observed).

## Self-Check: PASSED

- `scripts/check-traceability.py` contains `_rows_v91` and `_self_test_v91_rows_sentinel` — FOUND.
- `docs/requirements-matrix.md` contains `v9.1/REL-07` — FOUND.
- `docs/data/matrix.json` contains `v9.1` — FOUND.
- Commit `8f16db9` — FOUND (`git log --oneline --all | grep 8f16db9`).
- Commit `e67f878` — FOUND (`git log --oneline --all | grep e67f878`).
- `docs/gates/CONF-SURFACE.md` contains `**(14) HEADLINE-LOCK verifies` — FOUND.
- `.planning/REQUIREMENTS.md` REL-07 checkbox reads `[x]` — FOUND.

## Requirements Note

`requirements: [REL-07]` is fully discharged by this plan: the 18 v9.1.0 requirements are registered as matrix rows behind a live-derived equality sentinel, and the coverage-headline move is produced by `HEADLINE-LOCK`'s sweep across all five registered surfaces plus both tracked matrix artifacts — verified this session against fresh command output, not inherited from any prior plan's evidence.

## Next Phase Readiness

- Release act two (matrix-row registration and headline sweep) is complete and committed. The tree now carries 323 matrix rows at coverage headline `217/106/0/323`.
- Every FENCED pre-arm site from plan 27-04 is confirmed byte-unchanged; no collision between this plan's release act and the pre-arm fence arose (D-15's open interaction #1 does not fire here).
- The one genuinely new containment finding this plan's own release act introduced was resolved in the same commit, not deferred — plan 27-07's fence adjudication has nothing new to reconcile from this plan.
- Next release acts (per D-14's ordering): the `[9.1.0]` CHANGELOG entry and the post-arm recurrence reading (plan 27-09), plus REL-06's own battery-total verification.

---
*Phase: 27-ship-v9-1-0*
*Completed: 2026-09-11*
