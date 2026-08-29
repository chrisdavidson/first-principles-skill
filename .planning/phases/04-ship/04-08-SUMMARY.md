---
phase: 04-ship
plan: 08
subsystem: docs
tags: [requirements-traceability, changelog, doc-hygiene, gap-closure, traceability-matrix]

# Dependency graph
requires:
  - phase: 04-ship (04-07)
    provides: "docs/requirements-traceability.md already at a single consistent 90 audit-only figure, which this plan's edits build on top of"
provides:
  - "Five corrected sites (CHANGELOG.md, docs/requirements-traceability.md x2, docs/v8.18-praor-loop-closure.md, scripts/check-traceability.py) qualifying the false unqualified '\"first...since v7.9\" claim with FORM A (\"v8.x\" scope) and naming the _rows_v711() counterexample"
  - "build_matrix_rows()'s docstring corrected from 'Four inclusion paths' to 'Five inclusion paths', documenting the previously-undocumented v7.11 path (d) and reletting the v8.18 path to (e)"
  - "Proof that the docstring-only edit changed no behavior: TRACE-03 --self-test passes and the regenerated matrix pair (docs/requirements-matrix.md, docs/data/matrix.json) is byte-identical to the tracked copies"
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "FORM A / FORM B qualifier selection per-site based on what the surrounding sentence actually claims (registration/row-count sentences get FORM A 'v8.x' scope; gate-backed-discriminator sentences get FORM B), rather than blanket-applying one qualifier everywhere"
    - "Naming the falsifying counterexample (_rows_v711() / headline-history row 3) inline at each corrected site so a future reader can audit the corrected claim without trusting the author or re-deriving the fact themselves"

key-files:
  created: []
  modified:
    - CHANGELOG.md
    - docs/requirements-traceability.md
    - docs/v8.18-praor-loop-closure.md
    - scripts/check-traceability.py

key-decisions:
  - "Classified the departure-addendum sentence (docs/requirements-traceability.md, 'the first milestone block since v7.9 (Phase 123 RECON-01) to add rows rather than resting on audit alone') as a fifth defective site beyond the verification report's four-site list — v7.11 also added matrix rows (11 audit-only), so the 'to add rows' framing does not survive the same counterexample that falsifies the other four sites"
  - "Kept six already-correct occurrences (docs/requirements-traceability.md's FORM B departure-addendum sentence, docs/README.md, docs/v8.18-praor-loop-closure.md's FORM B sentence, two of CHANGELOG.md's three occurrences, scripts/check-traceability.py:890) byte-unchanged, confirmed independently rather than trusted from the plan's own classification"
  - "Reflowed two corrected sentences (docs/requirements-traceability.md row 8, docs/v8.18-praor-loop-closure.md Traceability opener) onto single lines rather than the plan's suggested two-line form, after discovering the plan's literal replacement text would have split a markdown table cell across lines (breaking table rendering) and would have made the corrected phrase fail its own single-line grep acceptance criterion"

patterns-established: []

requirements-completed: [SHIP-04, SHIP-05]

# Metrics
duration: 40min
completed: 2026-08-29
---

# Phase 04-ship Plan 08: Close GAP 2 — false "first...since v7.9" primacy claim Summary

**Qualified five sites (CHANGELOG.md, `docs/requirements-traceability.md` x2, `docs/v8.18-praor-loop-closure.md`, and a `scripts/check-traceability.py` docstring) that falsely asserted the v8.18 traceability block was the first requirement block registered as matrix rows since v7.9, and fixed the same-root-cause docstring miscount (`build_matrix_rows()` said "Four inclusion paths" while its body has five, `_rows_v711()` being the undocumented one) that let the false claim look true to four separate authors.**

## Performance

- **Duration:** ~40 min
- **Tasks:** 3 completed (Task 1 read-only, no commit; Tasks 2 and 3 each committed)
- **Files modified:** 4

## Accomplishments
- Ran the full-tree sweep for `"since v7.9"` and independently classified all 11 surviving hits into `already-correct` / `defective` / `historical` buckets, each with the full sentence quoted and a justification
- Found a fifth defective site (the `docs/requirements-traceability.md` departure-addendum sentence) beyond the verification report's four-site list, and stated that finding explicitly
- Confirmed `_rows_v711()` exists and is extended into `build_matrix_rows()` by direct inspection, not by trusting the plan's `<interfaces>` block
- Qualified all five defective sites with FORM A ("v8.x" scope), each naming the `_rows_v711()` counterexample or headline-history row 3 so a future reader can audit the claim
- Corrected `build_matrix_rows()`'s docstring: "Four inclusion paths" → "Five inclusion paths", documented the previously-undocumented v7.11 path as (d), relettered the v8.18 path to (e) with its claim qualified
- Proved the docstring edit changed no behavior: `--self-test` passes, `git diff` shows no `rows.extend`/`def` line touched, `ast.parse` succeeds, and the regenerated matrix pair is byte-identical to the tracked copies
- Re-confirmed the whole-tree gate set: sync-content clean, 17 stamps at `8.18.0`, check-links clean, firewall battery reported the same documented `BLOCKED` (pytest-prerequisite) outcome as plan 04-07, with all 19 non-VAL-03 gates `[PASS]`

## Task Commits

Each task was committed atomically:

1. **Task 1: Classify every "since v7.9" occurrence in the tracked tree** - verification-only, no file changes, no commit (matches plan's own `<action>`: "no file modified — classification output goes in the SUMMARY")
2. **Task 2: Qualify the defective claims in the three Markdown surfaces** - `eb4637a` (docs)
3. **Task 3: Fix build_matrix_rows()'s inclusion-path miscount and its unqualified claim, and prove no behavior changed** - `4287a95` (fix)

**Plan metadata:** (this SUMMARY commit)

## Files Created/Modified
- `CHANGELOG.md` - Site 7 (the `## [8.18.0]` Added section's traceability-rows bullet) qualified to FORM A, naming `_rows_v711()`
- `docs/requirements-traceability.md` - Site 1 (departure addendum, "to add rows rather than resting on audit alone") and Site 3 (headline-history row 8) both qualified to FORM A, naming the v7.11 block/row 3
- `docs/v8.18-praor-loop-closure.md` - Site 4 (`## 5. Traceability` opening paragraph) qualified to FORM A, naming `_rows_v711()`
- `scripts/check-traceability.py` - `build_matrix_rows()`'s docstring: path count corrected 4→5, new path (d) documenting `_rows_v711()` inserted, v8.18 path relettered (d)→(e) with its claim qualified to FORM A

## Decisions Made

**Task 1 classification table** (one row per surviving "since v7.9" hit, file/anchor/bucket/justification):

| # | File | Anchor text (full sentence) | Bucket | Justification |
|---|------|------------------------------|--------|----------------|
| 1 | `docs/requirements-traceability.md` (departure addendum, line 22 pre-edit) | "The v8.18 milestone's 23 requirements ... **are** registered as matrix rows — the first milestone block since v7.9 (Phase 123 RECON-01) to add rows rather than resting on audit alone." | `defective` | The clause "to add rows rather than resting on audit alone" distinguishes v8.18 from v7.12/v7.13/v8.0 (audit-only, no rows), but v7.11 (headline-history row 3) **did** add matrix rows — 11 audit-only rows registered via `_rows_v711()`. The unqualified "first...since v7.9...to add rows" is therefore false; v7.11 is a second counterexample distinct from the gate-backed one the next sentence correctly uses. This is the fifth site beyond the verification report's four-site list — see the exhaustiveness verdict below. |
| 2 | `docs/requirements-traceability.md` (departure addendum, line 28 pre-edit) | "...so v8.18's 21 gate-backed requirements are the first since v7.9 to satisfy the same test the note above applies to v7.12/v7.13/v8.0." | `already-correct` | FORM B (gate-backed-property scope). True because v7.11's 11 rows are audit-only with no deterministic offline gate behind them — v8.18's 21 reproducible rows genuinely are the first since v7.9 to be gate-backed. Left byte-unchanged. |
| 3 | `docs/requirements-traceability.md` (headline-history row 8, line 47 pre-edit) | "...the first milestone block added since v7.9 (row 2 above)." | `defective` | Unqualified; v7.11 (row 3, five rows above in the same table) added a milestone block of rows. Fixed to FORM A with an explicit in-table pointer to row 3. |
| 4 | `docs/v8.18-praor-loop-closure.md` (line 160 pre-edit) | "`_rows_v818()`, the first milestone requirement block added since v7.9." | `defective` | Unqualified primacy claim, same false-since-v7.9 pattern. Fixed to FORM A naming `_rows_v711()` and Phase 131 RECON-03. |
| 5 | `docs/v8.18-praor-loop-closure.md` (line 183 pre-edit) | "...the first requirement block since v7.9 to carry that property — where the requirement blocks the D-01 note was written to guard against were paperwork-only additions with nothing re-runnable behind them." | `already-correct` | FORM B (gate-backed property). Left byte-unchanged. |
| 6 | `docs/README.md` (line 188) | "...the first **v8.x** milestone requirement block registered as matrix rows since v7.9." | `already-correct` | Already carries FORM A explicitly (bolded "v8.x"). This is the canonical FORM A reference the other sites were corrected to match. Not edited. |
| 7 | `CHANGELOG.md` (line 52 pre-edit) | "...requirement ID — the first milestone requirement block registered as matrix rows since v7.9." | `defective` | Unqualified. Fixed to FORM A naming `_rows_v711()` and its 11-row count. |
| 8 | `CHANGELOG.md` (line 63 pre-edit) | "...the first v8.x milestone block since v7.9 to register matrix rows — a stated departure from the historical Phase 142 D-01 note..." | `already-correct` | Already carries FORM A explicitly. Read the complete sentence per the plan's flag on this site: confirmed clean, not edited. |
| 9 | `CHANGELOG.md` (line 67 pre-edit) | "...gate, the first requirement block since v7.9 with that property." | `already-correct` | FORM B (gate-backed property, referring back to "a re-runnable offline gate" two sentences earlier). Left byte-unchanged. |
| 10 | `scripts/check-traceability.py` (line 890 pre-edit, `_rows_v818()` docstring) | "No v8.x milestone has added a row since v7.9 (Phase 123) for that reason. v8.18's requirements are the first since v7.9 to pass headline-history row 2's test — 'each backed by a deterministic offline gate' — because HARN-01/HARN-02/HARN-03 are deterministic, offline, and (per D-01/D-03) both battery- and CI-registered." | `already-correct` | Two claims in sequence: the first sentence is scoped to "v8.x" milestones specifically (true — v7.11 is not v8.x); the second is FORM B (gate-backed property, true for the same reason as sites 2/5/9). Both survive the v7.11 counterexample. Confirmed by full-sentence read per the plan's flag on this site; `_rows_v818()`'s own docstring is explicitly untouched by Task 3 (which edits only `build_matrix_rows()`'s docstring). |
| 11 | `scripts/check-traceability.py` (line 1010-1011 pre-edit, `build_matrix_rows()` docstring path (d)) | "(d) v8.18 milestone (23 rows, 21 reproducible + 2 audit-only) — first milestone block since v7.9 (Phase 4/D-05): the discriminator is headline-history row 2's phrase 'each backed by a deterministic offline gate'..." | `defective` | Unqualified "first milestone block since v7.9" — same false claim, and the same undocumented-v7.11-path defect that caused it (v7.11 was absent from this docstring's enumeration). Fixed as part of Task 3: relettered to (e), qualified to FORM A, and (d) is now the newly-documented v7.11 path. |

**Verification-report exhaustiveness verdict:** The verification report's four-site list (`CHANGELOG.md:52`, `docs/requirements-traceability.md:47`, `docs/v8.18-praor-loop-closure.md:159-160`, `scripts/check-traceability.py:1010-1011`) was **not exhaustive**. Site 1 above — the departure-addendum sentence in `docs/requirements-traceability.md` — is a fifth genuine defect the report did not name, because it makes a narrower claim ("first...to add rows rather than resting on audit alone") that still fails against the v7.11 counterexample even though it is phrased differently from the other four sites' "first milestone [requirement] block...since v7.9" pattern. The planner's independent read caught this; this execution's own third read confirmed it independently before editing.

**Per-site verdicts requested by the plan for `CHANGELOG.md:63` and the departure-addendum occurrence:**
- `CHANGELOG.md:63` ("...the first v8.x milestone block since v7.9 to register matrix rows — a stated departure from the historical Phase 142 D-01 note...") — **already-correct.** Full sentence read; carries FORM A's "v8.x" scope explicitly. Not edited.
- `docs/requirements-traceability.md` departure-addendum occurrence — this plan found **two** distinct claims in that addendum, not one: the site-1 claim above is `defective`, but the immediately-following site-2 claim (FORM B, "gate-backed requirements are the first since v7.9 to satisfy the same test...") is `already-correct`. Both full sentences are quoted above.

**Inclusion-path count derivation (Task 3):** Grouped the way the pre-existing docstring itself groups (per-`rows.extend()` call is too fine-grained — the docstring's (a) covers eleven separate `rows.extend()` calls for methodology and test-network sub-groups). Reading `build_matrix_rows()`'s body top to bottom: (a) live-shipping [11 extends: 4 methodology + 7 test-network], (b) active tail [1 extend], (c) v7.9 milestone [1 extend], v7.11 milestone [1 extend, previously undocumented], (e) v8.18 milestone [1 extend] — five groups total, fifteen `rows.extend()` calls. This matches the plan's own derivation; the docstring was corrected to "Five inclusion paths" accordingly.

**Table/blockquote-formatting deviation (not scope, but load-bearing for correctness):** The plan's literal suggested replacement text for site 3 (`docs/requirements-traceability.md` headline-history row 8) and site 4 (`docs/v8.18-praor-loop-closure.md`) both embed a line break in the middle of the qualified phrase. Applying that text verbatim to site 3 split a markdown table cell across two source lines, which breaks table rendering (a table row must be single-line source in this renderer) — confirmed by inspecting the result immediately after the edit and reflowing to a single line before proceeding. The same issue would have made site 4's own acceptance criterion (`grep -c "first **v8.x** milestone requirement block added since v7.9"` printing `1`) fail, since the corrected phrase spanned two lines in the plan's suggested form. Both were reflowed onto single lines carrying the identical corrected text; this is a formatting adjustment to the plan's literal suggested prose, not a change to which claim was corrected or how it was qualified.

## Task 3: build_matrix_rows() docstring — before/after

**Before:**
```
Four inclusion paths per D-05:
(a) Live-shipping requirements ...
(b) Active tail ...
(c) v7.9 milestone (8 rows) ...
(d) v8.18 milestone (23 rows, 21 reproducible + 2 audit-only) — first milestone block
    since v7.9 (Phase 4/D-05): ...
```

**After:**
```
Five inclusion paths. (a)-(c) were enumerated per the original D-05; (d) has been in the
body since Phase 131 RECON-03 but went undocumented here until 2026-08-29; (e) was added
at v8.18 Phase 4.
(a) Live-shipping requirements ...
(b) Active tail ...
(c) v7.9 milestone (8 rows) ...
(d) v7.11 milestone (11 rows) — all audit-only (Phase 131 RECON-03, D-04): ...
(e) v8.18 milestone (23 rows, 21 reproducible + 2 audit-only) — first **v8.x** milestone block
    since v7.9 (Phase 4/D-05; the v7.11 block at (d) is the last non-v8.x addition): ...
```

## Whole-tree gate re-confirmation

Run in order:

1. `python3 scripts/check-traceability.py --self-test` — exit 0, `V818-ROWS PASS` lines present. PASS.
2. `python3 scripts/check-traceability.py emit --md-output docs/requirements-matrix.md --json-output docs/data/matrix.json` then `git diff --quiet docs/requirements-matrix.md docs/data/matrix.json` — exit 0 both. Byte-identical, proving the docstring edit changed no behavior. PASS.
3. `python3 -c "import ast,sys; ast.parse(open('scripts/check-traceability.py').read())"` — exit 0. PASS.
4. `python3 scripts/sync-content.py --check` — exit 0, no output. PASS.
5. `python3 scripts/check-version-stamps.py` — `17 stamps, all '8.18.0'`, `PASS`, exit 0. PASS.
6. `python3 scripts/check-links.py --self-test && python3 scripts/check-links.py` — both exit 0, `check-links: PASS (244 markdown links + 6 namespace refs across 127 files)`. PASS.
7. `bash scripts/check-firewall-battery.sh` — **verbatim final line:**

```
FIREWALL: BLOCKED (1 prerequisite(s) unmet; 19/20 passed)
```

Exit code: 2.

**This is the same documented `BLOCKED` outcome plan 04-07 reported, not a gate failure and not a regression introduced by this plan.** The single unmet item is `[PREREQ] VAL-03`: no pytest-capable interpreter is available in this worktree checkout (`.venv/bin/python3` absent; bare `python3` on `PATH` has no `pytest` module). All 19 other gates printed `[PASS]`: `DUAL-04`, `GATE-02-v8.5`, `STEP0-06`, `STEP0-08`, `VAL-01`, `VAL-02`, `VAL-04`, `VAL-05`, `VERSION-01`, `GATE-01`, `BATT-06`, `TRACE-03`, `COLLIDE-01`, `QUAL-01`, `HARN-01`, `HARN-02`, `HARN-03`, plus the `INVARIANT-CHECK` and `FROZEN-EVIDENCE` inline checks. Per the plan's own instruction, this is reported as-is rather than fixed within this plan's scope (`files_modified` does not include creating a `.venv`).

`git diff --name-only HEAD~2 HEAD` lists exactly `CHANGELOG.md`, `docs/requirements-traceability.md`, `docs/v8.18-praor-loop-closure.md`, `scripts/check-traceability.py` — matching the plan's `files_modified` list exactly, no more, no less.

## Deviations from Plan

1. **[Rule 1 - Formatting fix] Reflowed the plan's suggested two-line replacement text onto single lines for sites 3 and 4.** Found during Task 2. The plan's literal suggested prose for `docs/requirements-traceability.md` headline-history row 8 and `docs/v8.18-praor-loop-closure.md`'s Traceability opener both embed a line break mid-phrase. Applied verbatim, the row-8 replacement split a markdown table cell across two source lines (breaking table rendering — a table row is single-line source), and the v8.18-praor-loop-closure.md replacement would have made its own acceptance criterion (a single-line grep match on the full qualified phrase) fail. Fix: reflowed both onto single lines carrying the identical corrected wording and meaning. Verified: `sed` inspection confirmed row 8 returned to single-line table format; `grep -c` on the full qualified phrase now returns `1` for both sites as the acceptance criteria require. Files: `docs/requirements-traceability.md`, `docs/v8.18-praor-loop-closure.md`. Commit: `eb4637a`.
2. **[Rule 1 - Prose cleanup] Reflowed the departure-addendum blockquote (site 1) into a smoother wrap** after the initial word-for-word insertion of the plan's suggested text left an awkward mid-sentence line break ("load-bearing. The" / "each\n> backed"). No wording was changed from the plan's suggested replacement text — only which words landed on which `>`-prefixed line, since blockquote line-wrapping (unlike table-cell content) does not affect rendering but does affect readability. Files: `docs/requirements-traceability.md`. Commit: `eb4637a`.

No architectural deviations, no Rule 4 escalations, no auth gates.

## Issues Encountered

- `bash scripts/check-firewall-battery.sh` reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 19/20 passed)` for the same reason plan 04-07 documented: this worktree checkout has no `.venv` with `pytest` installed. Not fixed in-scope, per this plan's `files_modified` (does not include environment setup) and per the wave note that this may resurface for any plan in this wave running its own battery inside this same worktree.
- Acceptance criterion `command grep -c "first milestone block" scripts/check-traceability.py` (Task 3) is specified to print `0` but prints `2` after the edit. Both matches are pre-existing, out-of-scope occurrences of a *different* claim — "first milestone block since **v5.3**" (lines 790 and, unchanged, path (c)'s own text) — describing the v7.9 block's own primacy relative to v5.3, not v7.9. These predate this plan (confirmed via `git show HEAD~2:scripts/check-traceability.py`, which already had 3 such matches: the two v5.3 ones plus the one this task corrected). This task's edit reduced the count from 3 to 2 by fixing exactly the one in-scope "since v7.9" occurrence; the two remaining hits are unrelated to the gap this plan closes and are outside `<interfaces>`'s eleven-site "since v7.9" inventory (they don't contain the string "since v7.9" — grep -n confirms both read "since v5.3"). The more specific criterion on the same line ("first **v8.x** milestone block" prints `1`) and the plan-level `<verification>` sweep (`grep -rn "since v7.9"`, confirmed above to show no unqualified survivor) both pass cleanly; this one criterion's grep pattern was written without accounting for the pre-existing unrelated v5.3 phrase.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- GAP 2 from `04-VERIFICATION.md` is closed: no unqualified "first...since v7.9" primacy claim survives in the tracked tree; every qualified claim names the `_rows_v711()` counterexample or headline-history row 3; `build_matrix_rows()`'s docstring now matches its own body in both count (five) and content (v7.11 documented).
- The battery's `FIREWALL: BLOCKED` outcome (pytest prerequisite absent in this worktree) is an environment condition affecting this worktree, not something either GAP-closure plan in this wave caused or can fix within its own scope; the orchestrator's merge onto the main tree (which has a populated `.venv`) is expected to resolve it.

---
*Phase: 04-ship*
*Completed: 2026-08-29*
