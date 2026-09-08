---
phase: 22-cap-the-recursion
plan: 08
subsystem: docs
tags: [terminal-disposition, backlog, depth-rule, exit-counts, product-apparatus-split]
dependency_graph:
  requires:
    - "22-01/22-02 — docs/PROCESS.md §1 (depth rule) and CLAUDE.md/CONTRIBUTING.md's depth-rule sentences, cited as this plan's closing authority"
    - "22-03/22-04 — CR-03, CR-04, CR-05, CR-06 closed (product findings from Phase 21)"
    - "22-05/22-06 — 999.31 items 1, 2 and 4 closed (product), item 3 apparatus"
    - "22-07 — LITERAL_SCAN_MD_GLOBS widened, registered_surfaces 37 -> 39, 30 new 999.44 ledger entries"
  provides:
    - ".planning/ROADMAP.md — terminal RESOLVED dispositions for 999.30, 999.31, 999.43; five new backlog entries (999.44-999.48) for every finding this phase declined to fix"
  affects: []
tech_stack:
  added: []
  patterns:
    - "closed-by-decision under the depth rule, citing docs/PROCESS.md §1, for an apparatus item whose fix would extend the guard-over-guard recursion"
    - "correct a mis-tiered backlog entry's framing by annotation in a closing paragraph, never by editing the original body in place"
    - "give a declined apparatus finding an unambiguous tracking home so 'never blocking' does not degrade into 'never tracked'"
key_files:
  created: []
  modified:
    - .planning/ROADMAP.md
decisions:
  - "CR-01 and CR-02's tracking home: both remain inside 999.43 itself, which narrows to exactly these two items rather than closing outright, rather than moving them to a fresh entry — the entry already documents both in full and a reader already knows to look there"
  - "999.43's original body text ('Every one of the six is an apparatus finding') was left unedited in place; the D-01 tiering correction (four of six are product) was recorded as an annotation in the closing paragraph, preserving the record of how the entry was originally filed"
  - "Exit count 4 (findings in 22-REVIEW.md carrying no product|apparatus tier) was not driven — 22-REVIEW.md does not exist until /bm:code-review 22 runs post-implementation; no placeholder file was written"
metrics:
  duration: "~55 minutes"
  completed: 2026-09-08
---

# Phase 22 Plan 08: Terminal Dispositions for 999.30, 999.31 and 999.43 Summary

Recorded terminal dispositions in `.planning/ROADMAP.md` for the three meta-guard backlog entries
this phase owns. **999.30** (both items apparatus, closed-by-decision under the depth rule) and
**999.31** item 3 (`_BAND_BULLETS` membership lock, also closed-by-decision) record accepted,
still-reproducible limitations — no code changed. **999.31** items 1, 2 and 4, and **999.43**'s
CR-03/CR-04/CR-05/CR-06, are recorded as closed by the plans that actually fixed them (22-05,
22-06, 22-03, 22-04), with the figures they landed. **999.43**'s CR-01/CR-02 are given an
unambiguous tracking home (they stay in 999.43 itself, narrowed to exactly those two). Five new
backlog entries (999.44-999.48) file every finding this phase declined to fix. Three of D-09's
four exit counts were driven to their targets and read live; the fourth (findings in
`22-REVIEW.md` with no product/apparatus tag) is honestly recorded as deferred to
`/bm:code-review 22` — no placeholder review file was written. `git diff --name-only` for this
plan is empty (`.planning/ROADMAP.md` is gitignored); the battery read `FIREWALL: GREEN (26/26)`
on the unmodified tree.

## What Was Built

### Task 1 — 999.30's terminal disposition

Header changed from `(terminal disposition due by v9.0.0 Phase 22)` to
`(RESOLVED 2026-09-08 by Phase 22 — closed-by-decision, D-03)`, title preserved byte-for-byte.
Closing paragraph states, per item:

- **Item 1** (`_VALIDATE_LEG_SYMBOLS` unlocked registry): reproduction restated — dropping
  `"_check_cross_surface"` from the tuple and deleting the real call leaves `--self-test` at rc 0
  while `(validate-census) CALL-SITE CENSUS: PASS` is a false claim.
- **Item 2** (ENTRY-SOURCE LOCK unanchored/unfloored): reproduction restated — aliasing the third
  argument to `frozenset(REQUIRED_BRANCHES)` while leaving the expected triple in an inert comment
  leaves both `ROSTER LOCK: PASS` and `ENTRY-SOURCE LOCK: PASS` at rc 0.
- Both tiered **apparatus** under D-01 (subject is another guard's own correctness).
- Disposition: **closed-by-decision**, citing `docs/PROCESS.md` §1's depth rule verbatim
  (*"a guard guards the product; a guard is not itself guarded"*) — fixing either here would be the
  fourth consecutive round on this exact defect class.
- Cost stated plainly: both reproductions remain reproducible today; `_VALIDATE_LEG_SYMBOLS_LOCK`
  was NOT added, and the ENTRY-SOURCE LOCK was NOT anchored or floored.
- Chain named: this entry is the third link of `999.27 → 999.28 → 999.30`, the chain CONF-14
  requires the depth rule to cite.

No code changed in this task.

### Task 2 — 999.31's and 999.43's terminal dispositions

**999.31.** Header changed to `(RESOLVED 2026-09-08 by Phase 22 — split disposition, D-03)`, title
preserved byte-for-byte. Closing paragraph states each item:

- **Item 1 — product, closed by plan 22-05.** "Nine found in total" replaced by an
  enumeration-derived figure of **eleven** constructs (ten with one arm per literal,
  `_VALIDATE_LEG_SYMBOLS` the one disclosed exception).
- **Item 2 — product, closed by plan 22-05.** The `zip` comment now matches the plain
  `zip(_BAND_BULLETS, _BAND_NAMES)` call; the code was not changed.
- **Item 3 — apparatus, closed-by-decision**, same authority as 999.30: `_BAND_BULLETS` still has
  no membership lock; a same-cardinality proper-subset substitution plausibly still reports full
  coverage.
- **Item 4 — product, closed by plan 22-06.** "Eight not-found reporting arms" replaced by a
  per-site-neutralization census: 19 candidate arms, **CONTROLLED=3, SIBLING-ONLY=0,
  UNCONTROLLED=16**. The 16-arm residual is published as a bounded limitation, not closed.

**999.43.** Header (no prior due-date parenthetical) gained
`(RESOLVED 2026-09-08 by Phase 22 — split disposition, D-02/D-03)`, title preserved byte-for-byte.
Also corrected the entry's own `**Requirements:**`/`**Plans:**` lines, which previously read
"disposition owed by Phase 22" and a `TBD` checklist item — these had to change for exit count 1's
"disposition owed by Phase 22" arm to reach 0 (see Deviations). Closing paragraph states:

- **CR-01 and CR-02 — apparatus, auto-filed, never blocking, carried forward unfixed.**
  `harvest()`'s "never raises" docstring still does not cover `subprocess.TimeoutExpired` or a
  `text=True` decode `ValueError`; `check-links.py --describe` still emits `scan_globs` as a 3-key
  dict where the vocabulary documents a sorted list (`docs/gates/VAL-03.md` still publishes 3
  entries for an 11-glob gate), with nine further shape/order violations across nine scripts.
  **Tracking home, quoted verbatim from the closing paragraph:** *"both remain tracked from this
  same entry, 999.43, which narrows to exactly these two items rather than closing outright."*
- **CR-03, CR-04, CR-05, CR-06 — product, closed as Phase 22 phase scope, not gap-closure (D-02).**
  CR-03/CR-04/CR-06 closed by plan 22-03 (the false ledger claim removed; Stage 4's five-gate
  enumeration restored; the three `run_command` values made runnable). CR-05 closed by plan 22-04,
  which restored **17** deleted historical figures (not the sixteen the entry's own filed count
  states — the origin review's table collapsed two identical occurrences into one row and missed a
  17th deletion; corrected count re-derived and stated in `22-04-SUMMARY.md`).
- **Framing correction**, added as an annotation rather than an in-place edit: the entry's own body
  states "Every one of the six is an apparatus finding," which D-01's claim-audience cut
  contradicts for four of the six (product). The original body text was left untouched.

### Task 3 — filed declined findings, drove the exit counts

**Five new backlog entries**, following the 999.40/999.41/999.42 shape:

- **999.44** — the CONF-13 over-fire group on `docs/README.md`, `docs/PROCESS.md` and
  `CONTRIBUTING.md`. Entry count read live: **48** (18 from `docs/README.md`, 2 from
  `CONTRIBUTING.md`, 28 from `docs/PROCESS.md`, counted by parsing `_DEFERRED_LITERAL_HITS`'
  dict-literal source range and tallying `'999.44'` occurrences within it — not a whole-file grep).
- **999.45** — the root `README.md` is unscanned by CONF-13 (`grep -c '"README.md",'
  scripts/gen-gate-docs.py` → 0), deliberately not fixed to avoid a third scope-widening inside
  the capping phase.
- **999.46** — root-level Markdown (`CONTRIBUTING.md`, root `README.md`, `CLAUDE.md`) is outside
  VAL-03's link-checking reach entirely; live evidence: `check-links.py --describe`'s three glob
  families contain no root-level entry; this phase's own new links on two of those surfaces were
  verified by hand as a consequence.
- **999.47** — `CONTRIBUTING.md`'s `<!-- generated-by: gsd-doc-writer -->` marker is dead (zero
  matches anywhere else in the repo); an observation, not a fix.
- **999.48** — the CR-06 follow-on `run_command` shape-validation control, declined under D-22-C
  (plan 22-03), filed with its reasoning so the decline is disputable rather than an omission.

**Exit counts driven and read:**

| # | Arm | Command | Result |
|---|---|---|---|
| 1a | Open-and-unowned: due-by header | `grep -c "terminal disposition due by v9.0.0 Phase 22" .planning/ROADMAP.md` | **0** (baseline 2) |
| 1b | Open-and-unowned: owed line | `grep -c "disposition owed by Phase 22" .planning/ROADMAP.md` | **0** (baseline 1) |
| 2a | CR-03 ledger claim | `grep -c "verified by grep across the five files" scripts/gen-gate-docs.py` | **0** |
| 2b | CR-04 Stage 4 bullets | `awk '/^## Stage 4/,/^## Stage 5/' docs/DATA-FLOW.md \| grep -c '^- \*\*'` | **5** |
| 2c | CR-05 hedges | `grep -o "a handful of entries\|several more live entries\|it holds only a single entry\|several docs/metadata items\|the whole battery stayed green\|cited across many surfaces" docs/README.md \| wc -l` | **0** |
| 2d | CR-06 heredoc | `grep -c "python3 - <<'PYEOF' # inline" scripts/_gate_registry.py` | **0** |
| 3 | Depth-rule surfaces | `grep -l "a guard guards the product; a guard is not itself guarded" CLAUDE.md CONTRIBUTING.md docs/PROCESS.md \| wc -l` | **3** (baseline 0) |
| 4 | REVIEW.md tags | deferred — see below | N/A |

**Exit count 4, honestly marked as unbuildable in-wave.** `22-REVIEW.md` does not exist until
`/bm:code-review 22` runs after implementation. Recorded command shape for when it does:

```sh
grep -cE "^### (CR|WR)-[0-9]" .planning/phases/22-cap-the-recursion/22-REVIEW.md   # total findings, N
grep -cE "^### (CR|WR)-[0-9]+.*\[(product|apparatus)\]" .planning/phases/22-cap-the-recursion/22-REVIEW.md   # tagged findings
# N minus the second number must be 0
```

Expected tag convention: a `[product]` or `[apparatus]` bracketed tag suffixed onto each
`### CR-NN` / `### WR-NN` finding heading, per `CLAUDE.md`'s review-protocol block (D-08) — the
regex is written to adjust if the reviewer emits a different literal convention.
`test -f .planning/phases/22-cap-the-recursion/22-REVIEW.md` confirmed non-zero exit (file
absent) — no placeholder was written.

**Whole-tree confirmation.** `python3 scripts/gen-gate-docs.py --self-test` → exit 0 (74
controls). `--check` → exit 0. `--describe` → `control_count` 74, `registered_surfaces` 39 (list
length), `literal_scan_non_exempt` 0. `python3 scripts/check-links.py` → PASS (312 markdown links
+ 6 namespace refs, 160 files). `sh .githooks/pre-commit` → exit 0. `sh scripts/git-hooks/pre-commit`
→ exit 0. `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)` (run with no
timeout limit imposed). `git status --porcelain` on the tracked tree → empty (`.planning/` is
gitignored except force-tracked `NN-MM-SUMMARY.md` files, so `.planning/ROADMAP.md`'s edits do not
appear here — expected, not a failure).

## Deviations from Plan

### [Rule 3 — blocking issue] 999.43's `**Requirements:**`/`**Plans:**` lines also needed correcting for exit count 1b to reach 0

- **Found during:** Task 3, running exit count 1's second arm after Task 2 appeared complete.
- **Issue:** the plan's Task 2 `<action>` only specified editing 999.43's header and appending a
  closing paragraph. But 999.43's pre-existing body also carried the literal text
  `**Requirements:** none — carried forward, disposition owed by Phase 22` and a `- [ ] TBD` plans
  checklist — both untouched by a header-plus-append edit, and the first is exactly the string
  `<verification>` item 2 and Task 1's own `<verify>` grep for.
- **Fix:** changed `**Requirements:**` to read "disposition recorded by Phase 22 below" and the
  `Plans:` checklist item to `[x] Disposition recorded (RESOLVED 2026-09-08 by Phase 22) — see
  closing paragraph below", inside the same task's diff, no new file touched.
- **Files modified:** `.planning/ROADMAP.md` (already the task's sole target).
- **Verification:** `grep -c "disposition owed by Phase 22" .planning/ROADMAP.md` → 0 (was 1
  before the fix, confirmed via an intermediate re-run).

No other deviations. Both tasks' `<action>` and `<acceptance_criteria>` items were executed and
independently re-verified on the live tree.

## Verification

All 12 plan-level `<verification>` items re-run on the live tree, in order:

1. `grep -c "terminal disposition due by v9.0.0 Phase 22" .planning/ROADMAP.md` → **0** (baseline 2)
2. `grep -c "disposition owed by Phase 22" .planning/ROADMAP.md` → **0** (baseline 1)
3. `grep -cE "^### Phase 999\.(30|31|43):.*RESOLVED 2026-09-08 by Phase 22" .planning/ROADMAP.md` → **3**
4. Each of the three original titles greps to exactly **1** (confirmed individually for 999.30, 999.31, 999.43)
5. `grep -c "^### Phase 999.44" .planning/ROADMAP.md` → **1**
6. `grep -c "verified by grep across the five files" scripts/gen-gate-docs.py` → **0**
7. `awk '/^## Stage 4/,/^## Stage 5/' docs/DATA-FLOW.md | grep -c '^- \*\*'` → **5**
8. `grep -o "a handful of entries\|several more live entries\|it holds only a single entry\|several docs/metadata items\|the whole battery stayed green\|cited across many surfaces" docs/README.md | wc -l` → **0**
9. `grep -c "python3 - <<'PYEOF' # inline" scripts/_gate_registry.py` → **0**
10. `grep -l "a guard guards the product; a guard is not itself guarded" CLAUDE.md CONTRIBUTING.md docs/PROCESS.md | wc -l` → **3**
11. `test -f .planning/phases/22-cap-the-recursion/22-REVIEW.md` → non-zero (absent, confirmed)
12. `git status --porcelain` → empty (no tracked file changed; `.planning/ROADMAP.md` is gitignored)
13. `python3 scripts/gen-gate-docs.py --self-test` → exit **0**; `--check` → exit **0**
14. `--describe` → `control_count` **74**, `registered_surfaces` **39**, `literal_scan_non_exempt` **0**
15. `python3 scripts/check-links.py` → exit **0**
16. `sh .githooks/pre-commit` → exit **0**; `sh scripts/git-hooks/pre-commit` → exit **0**
17. `bash scripts/check-firewall-battery.sh` → **FIREWALL: GREEN**, total **26**

## Issues Encountered

None beyond the one in-scope Rule 3 fix documented under Deviations.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- 999.30, 999.31 and 999.43 all carry terminal RESOLVED dispositions; no open-and-unowned
  meta-guard backlog entry remains (exit count 1 at 0/0).
- All four product findings carried from Phase 21 (CR-03, CR-04, CR-05, CR-06) are closed (exit
  count 2 at 0/4 across all arms).
- Three surfaces state the depth rule verbatim (exit count 3 at 3/3).
- Exit count 4 is honestly deferred to `/bm:code-review 22`, with its command shape and expected
  tag convention recorded above — this is the depth-rule review-protocol block's (D-08) first live
  test.
- Five new backlog entries (999.44-999.48) give every declined finding a named home.
- No code changed anywhere in this plan; the battery reads `FIREWALL: GREEN (26/26)` on the
  unmodified tree, `control_count` is 74, `registered_surfaces` is 39.
- `.planning/ROADMAP.md` was copied to the main checkout
  (`/home/chrisdavidson/Projects/first-principles-skill/.planning/ROADMAP.md`) because it is
  gitignored in this worktree and cannot travel via the merge — the orchestrator's copy now
  matches this plan's final edit byte-for-byte (confirmed via `diff`).
- This is the last plan of Phase 22 per the plan sequence (22-01 through 22-08); no blockers for
  phase close.

## Self-Check: PASSED

- `[ -f .planning/ROADMAP.md ]` → FOUND (edited; gitignored, so not tracked by git, but present on
  disk in both the worktree and the main checkout, confirmed identical by `diff`)
- No commit hash to check for `.planning/ROADMAP.md` itself — it is gitignored and carries no
  commit. This SUMMARY.md's own commit is the one git-visible artifact this plan produces.
- All 17 plan-level `<verification>` commands re-run above with observed (not assumed) output,
  including `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)`.

---
*Phase: 22-cap-the-recursion*
*Completed: 2026-09-08*
