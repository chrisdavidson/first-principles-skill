---
phase: 22-cap-the-recursion
plan: 04
subsystem: docs+apparatus
tags: [product-findings, cr-05, deferred-ledger, honesty-not-score]
dependency_graph:
  requires:
    - "22-03 — closed CR-03, CR-04, CR-06; left the deferred-literal ledger at 134 entries, both guards repinned fresh"
  provides:
    - "docs/README.md — all 17 historical figures CR-05 found deleted, restored verbatim"
    - "scripts/gen-gate-docs.py — explicit 999.44 backlog branch, 18 new hand-adjudicated ledger entries, both guards repinned to 152"
    - "docs/gates/CONF-SURFACE.md — corrected narrative naming 999.44 and the live figures, and an honest statement that a deliberate, re-pinned ledger GROWTH is legal"
  affects:
    - "22-08 (records CR-05 closed; exit count 2 — product findings carried from Phase 21 — now at 0/4)"
tech_stack:
  added: []
  patterns:
    - "restore true content and attribute it through the named per-hit ledger, never delete it to satisfy a guard (D-22-A, this plan's own worked example)"
    - "explicit named backlog-id branch for a new ledger surface, never the 999.41 default (D-22-D)"
    - "re-pin both deferred-ledger guards fresh from the real final state, in the same commit as any ledger-key change, never incrementally"
key_files:
  created: []
  modified:
    - docs/README.md
    - scripts/gen-gate-docs.py
    - docs/gates/CONF-SURFACE.md
decisions:
  - "Row 17 (the now-false 'two pre-commit gates') restored as the live, true 'five pre-commit gates' count rather than the stale pre-3c17833 digit — falsifiability restored without restoring a wrong number, per the plan's own judgement-call instruction"
  - "describe()'s ledger_adjudicated computation widened to recognize 999.44 alongside 999.42 as hand-adjudicated (Rule 1 fix, directly caused by adding the 999.44 branch) — otherwise the 18 individually-reasoned docs/README.md entries would be misclassified as mechanically pinned, understating what the ledger actually certifies"
  - "docs/gates/CONF-SURFACE.md's '(6) The ledger ratchets down, never up' claim corrected to state growth is legal when re-pinned and deliberate (D-22-D) — left unchanged, this very commit's own action would have falsified it, the same defect class CR-05 exists to end"
metrics:
  duration: "~65 minutes"
  completed: 2026-09-08
---

# Phase 22 Plan 04: Restore CR-05's 17 Deleted docs/README.md Figures Summary

Closed **CR-05**, the last of the four product-tier findings carried from Phase 21 — CONF-13's
non-exempt-literal zero had been reached partly by deleting 17 true, permanently-stable historical
measurements from `docs/README.md` and substituting unfalsifiable hedges, including one stated as
a gating criterion on opening any post-v8.11 milestone. All 17 rows are restored verbatim, each
resulting ledger key is individually attributed under a new named `999.44` backlog branch, and
`literal_scan_hits` rose (160 → 179) while `literal_scan_non_exempt` held at 0 — the guard's zero
is now reached by attribution, not deletion.

## What Was Built

**Task 1 — restore all 17 rows.** Re-derived the restore set independently via
`git show 3c17833 -- docs/README.md` rather than trusting `22-RESEARCH.md`'s own table. **The
re-derivation confirmed exactly 17 distinct edits, matching the research table's own count
(HIGH confidence) and no discrepancy was found** — one more than the origin review's "sixteen
instances" (the review's table had collapsed two identical "about five live entries" → "several
more live entries" occurrences into one row and missed a 17th deletion, "while 16 gates stayed
green" → "while the whole battery stayed green," found independently in the diff). All 17 rows
were applied via an exact-string Python replacement script asserting each search string's expected
occurrence count before substituting, so no accidental double-application or partial match could
land silently.

**Row 17 judgement call.** The final row restores `"the two pre-commit gates"` into `docs/README.md`'s
nav row for `TESTING.md` — but that count is now **false**: five pre-commit gates fire as of
CONF-SURFACE (plan 21-13/21-11). Restoring the literal `"two"` would trade one falsehood for
another. Chosen fix: state the current, live, true count instead — `"the five pre-commit gates"`
— verified against `docs/TESTING.md:67` (`"Five gates fire on every git commit..."`) and
`CLAUDE.md`'s own Pre-commit gates section. This restores the sentence's falsifiability without
restoring a digit the tree itself would immediately falsify.

After Task 1's edit alone, `python3 scripts/gen-gate-docs.py --check` reported **19 non-exempt
literal hits** on `docs/README.md` (one more than the plan's Task 1 acceptance criteria's
minimum-8 floor implied, because two of the 17 restored rows each split into two separate
scanner-matched windows within the same sentence — see Task 2 below). That failure was the
expected evidence the restore was real, per the plan's own design.

**Task 2 — attribute every hit, repin both guards.** Added an explicit `docs/README.md` branch to
`_emit_deferred_ledger_backlog_id()` returning `'999.44'`, placed before the trailing `'999.41'`
default (D-22-D) — falling through to the default would file these Markdown hits under a backlog
entry whose published title says it holds Python module docstrings, a factually wrong label
reached by a default branch (the catch-all `T-21-09-02` exists to reject). Ran
`python3 scripts/gen-gate-docs.py --emit-deferred-ledger`, diffed its 152-entry output against the
live 134-entry `_DEFERRED_LITERAL_HITS` dict, confirmed **zero removals and zero occurrence/backlog-id
mismatches on the 134 pre-existing keys**, and merged: the 134 existing hand-written reasons were
preserved unchanged; the 18 new `docs/README.md` keys each received an individually hand-written
reason (not the emitter's `TODO: written reason` placeholder) naming the specific figure, that it
is a closed historical measurement of a past state, and its verification (`git show 3c17833`,
2026-09-06). Two pairs of keys (`'**0 items'` / `'items each** for two'`, and `'6 live rows'` /
`'rows to 0'`) come from the same restored sentence split into two scanner windows — their reasons
name that fact explicitly rather than duplicating unrelated boilerplate across figures.

Re-pinned both guards fresh from the real final state (never incrementally):

| Guard | Before (end of wave 3) | After |
|---|---|---|
| `_DEFERRED_LEDGER_MAX` | 134 | **152** |
| `_DEFERRED_LEDGER_KEYS_DIGEST` | `sha256:d968f66d09bbd83c2bb65bbfb13d42cafc80310a3193aefe40768baa25395f3a` | `sha256:3ba9791b998420e5e6b1bb8e660e136198d2d636075bd1ec03902f006f29009f` |

**Rule 1 fix (in-scope, directly caused by this task):** `describe()`'s `ledger_adjudicated`
computation counted only backlog id `'999.42'` as hand-adjudicated, folding everything else
(including the 18 new, individually-reasoned `999.44` entries) into `ledger_mechanical`. Left
unfixed, `literal_scan_ledger_mechanical` would have misrepresented 18 hand-written, per-figure
reasons as mechanically pinned, without per-entry adjudication — understating what the ledger
actually certifies, in the same phase whose whole point is that a guard's own self-description
must stay honest. Widened the condition to `_bid in ("999.42", "999.44")`.

**Full list of 18 ledger keys added, all backlog `999.44`** (relpath is `docs/README.md` for
every row):

| Matched text | Occ | Reason (abbreviated) |
|---|---|---|
| `7 docs/metadata items),` | 1 | v8.1 selectively implemented 7 docs/metadata items |
| `19 not-approved items),` | 1 | v8.2's re-investigation covered the 19 not-approved items |
| `612 to 590 lines, the surface` | 1 | v8.6 cut the agent body from 612 to 590 lines |
| `five entries` | 1 | use-journal.md needed about five entries of real, non-harness use |
| `five live entries` | 2 | both 2026-07-25/07-26 dispositions state "about five live entries" (the CR-05 gating criterion) |
| `**one** entry` | 1 | the use-journal limb held exactly one entry as of 2026-07-29 |
| `**0 items` | 1 | main.py's three dedicated test files collected 0 items each for two years |
| `items each** for two` | 1 | same restored sentence as `**0 items`, second scanner window |
| `sixteen green gates` | 1 | sixteen green gates sat over an inert version-stamp path (2026-07-29 GREENMEAN-01 finding) |
| `6 live rows` | 1 | v8.14's own milestone audit compared 6 live rows to 0 baseline rows |
| `rows to 0` | 1 | same restored sentence as `6 live rows`, second scanner window |
| `16 gates` | 1 | v8.13's launcher sat undeliverable while 16 gates stayed green |
| `16 surfaces` | 1 | v8.7-constraint-teardown.md is cited by 16 surfaces |
| `fixture (9)` | 1 | TRACE-03's own fixture carries a population of 9 |
| `13 live matrix rows'` | 1 | whole-system-remeasure-verdict.md anchors provenance for 13 live matrix rows' dispositions |
| `13 rows` | 1 | whole-system-remeasure-verdict.md is referenced by 13 rows of the traceability matrix |
| `three new offline gates` | 1 | the 2026-08-27 PRAO review's gaps were closed by HARN-01/02/03 |
| `gate and the five` | 1 | NOT-A-RESTORE — row-17 judgement call; "five" is live-verified, not a 3c17833 restore |

**Task 3 — prove attribution, not deletion; regenerate every surface.** Ran
`gen-gate-docs.py --write`, `--self-test`, `--check` in sequence. The first `--self-test` run
failed on a **D-06 containment** problem: `docs/gates/CONF-SURFACE.md`'s hand-written narrative
still cited the stale `20`/`114`/`134` figures (its own Facts fence had already moved to
`38`/`114`/`152`). Corrected the three narrative call-outs to the live figures, and rewrote the
"(6) The ledger ratchets down, never up" paragraph — this plan's own repin, `134 → 152`, would
otherwise have falsified that claim the moment it landed, the exact CR-05 defect shape in a
different guard's own documentation. The rewritten paragraph states the ledger's real invariant:
any size change (either direction) must be re-pinned in the same commit; a deliberate, attributed
growth (like this plan's) is legal and distinct from a detector accepting a non-conforming artifact
(CONTRACT-06 untouched). A second self-test pass then failed a narrower containment problem: two
bare `17`s in the new prose had no matching digit inside a generated fence (the Facts fence states
`38`, not `17`) — reworded both to point at `docs/PROCESS.md` §1.2 for the count instead of
re-stating a second, unfenced digit. After that, `--self-test` passed (74 controls), `--write`
regenerated 34 files with only `docs/README.md`, `scripts/gen-gate-docs.py` and
`docs/gates/CONF-SURFACE.md` carrying real diffs (`CLAUDE.md` and `docs/ARCHITECTURE.md`
regenerated byte-identical — their gate tables don't render the literal-scan facts), and `--check`
exited 0.

**Anti-gaming pair, read from `--describe`:**

| Measurement | End of wave 3 (this plan's base commit) | After this plan |
|---|---|---|
| `literal_scan_hits` | **160** | **179** (delta **+19**) |
| `literal_scan_non_exempt` | 0 | **0** |
| `literal_scan_ledger_entries` | 134 | **152** |
| `literal_scan_ledger_max` | 134 | **152** |

`literal_scan_hits` rose while `literal_scan_non_exempt` stayed at 0 — the pair together is the
claim CR-05 required proven: the restore returned real, verifiable content to a scanned surface
(more for the scanner to find), and the guard's zero is reached because every hit is named and
reasoned, not because the hits were removed.

`git diff --name-only` confirms only three files changed: `docs/README.md`,
`scripts/gen-gate-docs.py`, `docs/gates/CONF-SURFACE.md`. Neither `docs/COMPONENT-DIAGRAM.md` nor
`docs/MEASUREMENT-MAP.md` appears (they were correctly fixed the first time, per the plan), and no
path under `.github/` appears — no CI job was added or changed.

## Deviations from Plan

### Combined commit (Rule 3 — blocking issue, plan-mandated)

The plan's own `<objective>` states: *"The restore and its attribution must therefore land in the
same commit, or `literal_scan_non_exempt` moves off zero and pre-commit gate 5 blocks every
subsequent commit."* Verified mechanically: attempting `gen-gate-docs.py --check` after Task 1
alone reported 19 non-exempt hits (exit 1), and pre-commit gate 5 runs exactly that check — a
commit of Task 1 alone would have been rejected by the hook. Task 3's own regeneration of
`docs/gates/CONF-SURFACE.md` was also required before `--check` would pass (its hand-written
narrative cited the pre-plan `20`/`114`/`134` figures), so all three tasks' file changes were
staged and committed together as one `feat(22-04)` commit rather than three separate per-task
commits. This is not a silent deviation from the standard one-commit-per-task convention — it is
the plan's own explicitly stated technical constraint, confirmed by running the actual gate before
committing.

### Rule 1 fix — `ledger_adjudicated` misclassification (in `scripts/gen-gate-docs.py`, Task 2's own file)

`describe()`'s `ledger_adjudicated` computation recognized only backlog id `'999.42'` as
hand-adjudicated. Directly caused by this task's own change (adding `999.44` as a second
hand-adjudicated backlog id): left unfixed, the 18 new individually-reasoned `docs/README.md`
entries would have been silently folded into `literal_scan_ledger_mechanical`, understating what
the ledger certifies — a correctness/honesty regression in the very guard this plan exists to
correct. Fixed inline, verified via `--describe` (`literal_scan_ledger_adjudicated` moved from 20
to 38, `literal_scan_ledger_mechanical` stayed correctly at 114), and folded into the same commit.

### Rule 1 fix — CONF-SURFACE.md's "ratchets down, never up" claim (in `docs/gates/CONF-SURFACE.md`, Task 3's own file)

Not present in the plan's `<action>` text, but directly caused by Task 2's legitimate ledger growth
(134 → 152): the pre-existing narrative asserted the ledger only ever shrinks, which this commit's
own repin falsifies. Corrected in place rather than left standing, per the exact discipline CR-05
itself is the worked example of — a guard's documentation asserting something the guard's own
state now contradicts.

No other deviations. All three tasks' `<action>` and `<acceptance_criteria>` items were executed
and independently re-verified on the live tree.

## Verification

All 12 plan-level `<verification>` items re-run on the live tree, in order:

1. `/usr/bin/grep -o "a handful of entries\|several more live entries\|it holds only a single entry\|several docs/metadata items\|the whole battery stayed green\|cited across many surfaces" docs/README.md | wc -l` → **0** (baseline 7)
2. `/usr/bin/grep -c "about five live entries" docs/README.md` → **1** (at least 1 required)
3. `/usr/bin/grep -c "^    ('docs/README.md'" scripts/gen-gate-docs.py` → **18** (at least 8 required; baseline 0)
4. `/usr/bin/grep "^    ('docs/README.md'" scripts/gen-gate-docs.py | /usr/bin/grep -vc "'999.44'"` → **0**
5. `/usr/bin/grep -c "TODO: written reason" scripts/gen-gate-docs.py` → **1** — see "Documented Pre-Existing Discrepancy" below (not the actual ledger dict body, which is independently confirmed at 0)
6. `python3 scripts/gen-gate-docs.py --describe` → `literal_scan_hits`=179 (> wave-3's 160), `literal_scan_non_exempt`=0, `literal_scan_ledger_entries`=152=`literal_scan_ledger_max`
7. `python3 scripts/gen-gate-docs.py --self-test` → exit 0 (74 controls)
8. `python3 scripts/gen-gate-docs.py --check` → exit 0
9. `python3 scripts/check-links.py` → exit 0 (312 markdown links + 6 namespace refs, 160 files)
10. `sh .githooks/pre-commit` → exit 0; `sh scripts/git-hooks/pre-commit` → exit 0
11. `bash scripts/check-firewall-battery.sh` → **FIREWALL: GREEN (26/26)**
12. Exit count 2 → **0**: all four arms from `22-RESEARCH.md` §7 item 2 re-run and confirmed —
    CR-03 `grep -c "verified by grep across the five files" scripts/gen-gate-docs.py` → 0; CR-04
    `awk '/## Stage 4/,/## Stage 5/' docs/DATA-FLOW.md | grep -c "^- \*\*"` → 5; CR-05
    `grep -c "a handful of entries\|several more live entries\|it holds only a single entry" docs/README.md`
    → 0; CR-06 `grep -c "python3 - <<'PYEOF' # inline" scripts/_gate_registry.py` → 0.

### Documented Pre-Existing Discrepancy (not a deviation — out of scope, not caused by this plan)

Verification item 5 measures `1`, both before and after this plan's commit — confirmed identical
to the condition `22-03-SUMMARY.md` already documented for the same reason. The one match is
`emit_deferred_ledger()`'s own output-template string (`'"TODO: written reason"),'`) — the
maintenance harness's boilerplate for whoever runs `--emit-deferred-ledger`, not a leftover
placeholder inside an actual `_DEFERRED_LITERAL_HITS` entry. Independently confirmed by parsing the
dict body's own literal source range and checking the substring is absent there: it is (0
occurrences). Editing `emit_deferred_ledger()`'s template string is out of this plan's `<action>`
and touches code this plan's `read_first` list does not name — logged, not fixed, per SCOPE
BOUNDARY.

## Issues Encountered

None beyond the documented pre-existing discrepancy above and the two in-scope Rule 1 fixes
documented under Deviations.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- All four product findings carried from Phase 21 (`CR-03`, `CR-04`, `CR-05`, `CR-06`) are now
  closed and mechanically verified. Exit count 2 (D-09) has reached **0/4**.
- The deferred-literal ledger stands at 152 entries (up from 134), both guards repinned fresh;
  plan 22-07's later widening of `LITERAL_SCAN_MD_GLOBS` (adding `docs/PROCESS.md` and
  `CONTRIBUTING.md`) starts its own repin arithmetic from this new base, not from 134.
- `literal_scan_ledger_adjudicated` now correctly counts both `999.42` and `999.44` entries (38
  total); any future new hand-adjudicated backlog id must be added to that same tuple or it will
  silently misclassify as mechanical.
- Battery confirmed `FIREWALL: GREEN (26/26)` on the full tree with this plan's commit applied;
  both `.githooks/pre-commit` and `scripts/git-hooks/pre-commit` exit 0.
- No blockers for downstream plans in this phase.

## Self-Check: PASSED

- `[ -f docs/README.md ]` → FOUND (modified)
- `[ -f scripts/gen-gate-docs.py ]` → FOUND (modified)
- `[ -f docs/gates/CONF-SURFACE.md ]` → FOUND (modified)
- `git log --oneline --all | grep -q acc25dc` → FOUND (combined Task 1+2+3 commit)
- All plan-level `<verification>` commands re-run above with observed (not assumed) output,
  including `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)`.

---
*Phase: 22-cap-the-recursion*
*Completed: 2026-09-08*
