---
phase: 22-cap-the-recursion
plan: 07
subsystem: apparatus
tags: [reach-widening, literal-scan, deferred-ledger, d-05, conf-13]
dependency_graph:
  requires:
    - "22-01 — docs/PROCESS.md exists and is committed (a3579fb), the ordering precondition this plan's own T-22-07-01 threat exists to enforce"
    - "22-02 — CONTRIBUTING.md's depth-rule sentence and true five-gate count landed, so this plan's widening scans settled prose, not a moving target"
    - "22-06 — most recent gen-gate-docs.py state (ledger at 152 entries, both guards pinned) this plan builds on"
  provides:
    - "scripts/gen-gate-docs.py — LITERAL_SCAN_MD_GLOBS widened to 10 entries (docs/PROCESS.md, CONTRIBUTING.md added); registered_surfaces 37 -> 39, checked_files 67 -> 69"
    - "scripts/gen-gate-docs.py — 30 new hand-adjudicated 999.44 deferred-literal-ledger entries, each with a unique written reason; _DEFERRED_LEDGER_MAX repinned 152 -> 182, _DEFERRED_LEDGER_KEYS_DIGEST recomputed fresh"
    - "docs/gates/CONF-SURFACE.md — hand-maintained narrative updated to cite the fresh literal_scan_ledger_adjudicated (68) and literal_scan_ledger_max (182) figures, and to name docs/PROCESS.md/CONTRIBUTING.md as 999.44 surfaces"
  affects:
    - "22-08 (records this widening's completion; the root README.md gap this plan deliberately did not close is filed there as a finding)"
tech_stack:
  added: []
  patterns:
    - "REACH widening (D-05): pointing an existing product-guard at more product surface, never adding a guard whose subject is another guard's own correctness"
    - "frozen-historical-measurement vs NOT-A-COUNT: the two ledger-attribution categories for a hit that cannot be exempted by an existing LITERAL_EXEMPTION_CLASSES matcher (D-22-A, no new class)"
    - "falsify by scratch-copy mutation, never by reading: the widening's own proof-of-detection is a disposable rsync --exclude .git copy with an injected wrong count, not a rising registered_surfaces number"
key_files:
  created: []
  modified:
    - scripts/gen-gate-docs.py
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - docs/gates/CONF-SURFACE.md
decisions:
  - "Combined Tasks 1, 2 and 3 into a single commit: Task 1's widening alone leaves --check failing by design (33 non-exempt hits), and the installed pre-commit hook's gate 5 runs --check on every commit with no --no-verify permitted, so no task boundary between the widening and its own ledger attribution is independently committable"
  - "Reworded _emit_deferred_ledger_backlog_id()'s docstring after a first draft introduced two new count-shaped literals into gen-gate-docs.py's own non-module docstrings (WR-08 shape), rather than raising _SELF_FILE_NONMODULE_DOCSTRING_HITS — the reword restored the pin to 29 unchanged"
  - "Hand-updated docs/gates/CONF-SURFACE.md's own narrative prose (D-06 containment: a number stated outside a generated fence must also appear inside one) — this page is a hybrid surface, its Facts/How-to-run fences regenerate but its surrounding narrative is preserved verbatim across --write, so a stale hardcoded citation of a fence value only self-heals if hand-edited"
metrics:
  duration: "~70 minutes"
  completed: 2026-09-08
---

# Phase 22 Plan 07: Widen CONF-13's Literal Scanner to docs/PROCESS.md and CONTRIBUTING.md Summary

Executed D-05's REACH widening in full: `LITERAL_SCAN_MD_GLOBS` grew from 8 to 10 entries
(`docs/PROCESS.md`, `CONTRIBUTING.md` added), `registered_surfaces` moved 37 → 39 and
`checked_files` 67 → 69 (both read live from `--describe`, never predicted), and every one of
the 30 resulting non-exempt hits was routed through a named, uniquely-worded `999.44`
deferred-literal-ledger entry rather than a new `LITERAL_EXEMPTION_CLASSES` matcher. The widening
was proved to buy real detection — not just a larger number — by injecting a wrong hand-maintained
gate count into `CONTRIBUTING.md` on a disposable scratch copy and watching `--check` fail by
name.

## What Was Built

### Precondition confirmation (Task 1)

- `test -f docs/PROCESS.md` → exit 0
- `git log --oneline -1 -- docs/PROCESS.md` → `a3579fb feat(22-01): write docs/PROCESS.md §3 — the rework cap and its append-only exception ledger`

The precondition — `docs/PROCESS.md` must exist on disk and be committed before
`LITERAL_SCAN_MD_GLOBS` names it — was confirmed, not assumed, before any edit.

### `registered_surfaces` / `checked_files`, before and after

| Reading | Before | After (live `--describe`) |
|---|---|---|
| `registered_surfaces` | 37 | **39** |
| `checked_files` | 67 | **69** |

Both new surfaces (`docs/PROCESS.md`, `CONTRIBUTING.md`) appear inside `registered_surfaces` and
`checked_files`, never in a `declined` list — confirmed by reading `read.read_relpaths` via
`--describe`, not by grepping for the tuple entries alone. `/usr/bin/grep -c '"README.md",'
scripts/gen-gate-docs.py` stayed at `0` — the root `README.md` was deliberately not added
(22-CONTEXT.md defers it by name; filed as a finding by plan 22-08).

### Complete non-exempt hit list `--check` reported immediately after widening (Task 1)

33 raw hits, before any ledger attribution:

```
docs/PROCESS.md:33: hand-maintained count literal 'four literals'
docs/PROCESS.md:33: hand-maintained count literal 'literals to one'
docs/PROCESS.md:60: hand-maintained count literal 'literals — at two'
docs/PROCESS.md:89: hand-maintained count literal '16 gates'
docs/PROCESS.md:91: hand-maintained count literal '17 rows'
docs/PROCESS.md:111: hand-maintained count literal 'item — one'
docs/PROCESS.md:125: hand-maintained count literal '"13 plans,"'
docs/PROCESS.md:125: hand-maintained count literal 'plans," "4'
docs/PROCESS.md:125: hand-maintained count literal 'plans," "4 rounds," "41%,"'
docs/PROCESS.md:135: hand-maintained count literal 'one verification → plan'
docs/PROCESS.md:141: hand-maintained count literal '**13 gap-closure plans'
docs/PROCESS.md:141: hand-maintained count literal 'plans across 4'
docs/PROCESS.md:143: hand-maintained count literal '1 (4 plans,'
docs/PROCESS.md:143: hand-maintained count literal '(4 plans,'
docs/PROCESS.md:145: hand-maintained count literal '13 plans,'
docs/PROCESS.md:148: hand-maintained count literal '2 gap-closure plans'
docs/PROCESS.md:174: hand-maintained count literal 'four plans'
docs/PROCESS.md:174: hand-maintained count literal 'plans closed three'
docs/PROCESS.md:174: hand-maintained count literal 'two plans'
docs/PROCESS.md:174: hand-maintained count literal 'plans to three'
docs/PROCESS.md:175: hand-maintained count literal 'Two plans,'
docs/PROCESS.md:183: hand-maintained count literal '2 plans'
docs/PROCESS.md:184: hand-maintained count literal 'four plans'
docs/PROCESS.md:184: hand-maintained count literal '(32 falsification arms,'
docs/PROCESS.md:191: hand-maintained count literal '2 was plans'
docs/PROCESS.md:191: hand-maintained count literal 'plans 21-17..21-20, four'
docs/PROCESS.md:193: hand-maintained count literal '3 was plans'
docs/PROCESS.md:200: hand-maintained count literal 'four plans'
docs/PROCESS.md:200: hand-maintained count literal 'plans closed three'
docs/PROCESS.md:208: hand-maintained count literal '4 was plans'
docs/PROCESS.md:211: hand-maintained count literal '13 gap-closure plans'
CONTRIBUTING.md:40: hand-maintained count literal 'Five gates'
CONTRIBUTING.md:82: hand-maintained count literal 'one shot and check'
literal-scan: 33 non-exempt hit(s) found
```

These 33 raw hits normalise (by whitespace-collapsed `(relpath, text)` key) to **30 unique ledger
keys** — some text windows recur (e.g. `'four plans'` × 3, `'plans closed three'` × 2) because
CONF-13's adjacency heuristic captures overlapping windows over the same sentence and because the
same clause is legitimately restated at more than one place in `docs/PROCESS.md`'s own §3.1
exception-ledger table plus its narrative expansion.

### Every new ledger key, its backlog id and its written reason (Task 2)

All 30 entries carry backlog id `999.44` (via two new explicit branches in
`_emit_deferred_ledger_backlog_id()`, placed before the `999.41` default, per D-22-D). No two
reasons are textually identical.

**`CONTRIBUTING.md` (2 entries):**

| Text | Occ | Reason |
|---|---|---|
| `Five gates` | 1 | Correct: the same fixed five-gate pre-commit pipeline already ledgered for `CLAUDE.md`'s and `docs/TESTING.md`'s own `'Five gates'` hits (999.42) — verified again here against both hook scripts, 2026-09-08, on this newly-registered surface. |
| `one shot and check` | 1 | NOT-A-COUNT: `'run the whole offline set in one shot and check for a GREEN verdict'` uses `'one shot'` as an idiom for a single invocation, not a count of any external population. |

**`docs/PROCESS.md` (28 entries)** — grouped by the closed event or structural fact each
describes:

- **999.28's historical defect shape** (`'four literals'`, `'literals to one'`) — two overlapping
  windows over the same sentence describing `_BAND_BULLETS`' pre-fix narrowability; a closed,
  already-remediated (plans 15-12/15-13) past code state.
- **This phase's own REACH widening count** (`'literals — at two'`) — names exactly how many
  surfaces plan 22-07 registers (two), fixed the moment this commit lands.
- **CR-05's worked example** (`'16 gates'`, `'17 rows'`) — `'16 gates'` quotes the same restored
  `docs/README.md` sentence already ledgered under that file's own `999.44` entry; `'17 rows'` is
  the closed count of figures plan 22-04 restored.
- **The D-01 corollary's singular determiner** (`'item — one'`) — NOT-A-COUNT: `'one'` means "any
  single entry," not a population count.
- **The frozen-count-class citation itself** (`'"13 plans,"'`, `'plans," "4'`,
  `'plans," "4 rounds," "41%,"'`) — three overlapping windows over the same quoted-exemplar list
  naming the class of frozen counts §2's standing constraint distinguishes from the moving battery
  total.
- **The round definition** (`'one verification → plan'`) — NOT-A-COUNT: `'one'` is an identity (a
  round IS a single such cycle), not an external count.
- **Phase 21's headline figure, restated three times** (`'**13 gap-closure plans'`,
  `'13 gap-closure plans'`, `'plans across 4'`, `'13 plans,'`) — the closed 13-plans/4-rounds
  measurement, cited at different points in §3's narrative.
- **Round 1's composition** (`'1 (4 plans,'`, `'(4 plans,'`, `'2 plans'`, `'(32 falsification
  arms,'`) — the closed count of round 1's own plans (4), the planner's compression judgement (2
  plans considered), and the plan-checker's confirmation (32 falsification arms).
- **The superseded CONF-15/ROADMAP wording, quoted verbatim** (`'2 gap-closure plans'`) —
  NOT-A-COUNT: a citation of the old wording D-06 explicitly changes, not a live rule this file
  states.
- **Round 2's composition, restated twice** (`'four plans'` × 3 — two for round 2, one
  coincidentally for round 1; `'plans closed three'` × 2 — round 2's outcome, in the table and the
  narrative; `'Two plans,'` — round 4's composition).
- **Round-number identifiers** (`'2 was plans'`, `'3 was plans'`, `'4 was plans'`) — NOT-A-COUNT:
  each identifies which round is being described, not a count.
- **The plan-range identifier plus its size** (`'plans 21-17..21-20, four'`) — combines a
  plan-number identifier with the frozen count of how many plans that range spans.
- **Round 3's growth** (`'two plans'`, `'plans to three'`) — the closed pre- and post-growth halves
  of the same sentence.

Full verbatim reasons are recorded in `scripts/gen-gate-docs.py`'s `_DEFERRED_LITERAL_HITS` dict
(commit `a2067f1`), each keyed on its exact `(relpath, text)` pair.

### `_DEFERRED_LEDGER_MAX` / `_DEFERRED_LEDGER_KEYS_DIGEST`, before and after

| Guard | Before | After |
|---|---|---|
| `_DEFERRED_LEDGER_MAX` | 152 | **182** |
| `_DEFERRED_LEDGER_KEYS_DIGEST` | `sha256:1663c1a1…4db63` | **`sha256:b758aa0d…66579`** |

Both recomputed fresh from the actual final `_DEFERRED_LITERAL_HITS` dict in the same commit,
never derived from the previous pin. `literal_scan_ledger_entries` (182) equals
`literal_scan_ledger_max` (182); `literal_scan_non_exempt` is `0`.

### The six phase invariants, each confirmed by its own command

| # | Invariant | Reading |
|---|---|---|
| 1 | `control_count` unchanged | `gen-gate-docs.py --describe` → `74` |
| 2 | Battery total unchanged, GREEN | `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)` |
| 3 | No CI job added | `git diff --name-only HEAD~1 HEAD` contains no `.github/workflows/validation.yml` |
| 4 | `check-quality-harness.py` byte-unchanged | `git diff scripts/check-quality-harness.py` → empty (three CONTRACT-06 pins untouched) |
| 5 | `_GATED_SURFACES` untouched | `git diff --name-only HEAD~1 HEAD` contains no `scripts/check-conf-gate.py` |
| 6 | Coverage headline unmoved | `docs/requirements-traceability.md` still states `192 reproducible / 94 audit-only / 0 gap / 286 total` |

No exemption class, matcher, control, gate, script or CI job was added:
`git diff scripts/gen-gate-docs.py | grep -cE "^\+.*LiteralExemptionClass\(|^\+def _match_|^\+def _control_"`
→ `0`.

### Every derived surface, regenerated and confirmed

`python3 scripts/gen-gate-docs.py --write` regenerated 34 files. Only 4 carried a real diff:
`CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/gates/CONF-SURFACE.md`, `scripts/gen-gate-docs.py`
(source). `docs/TESTING.md` regenerated byte-identical (its generated index does not render
`registered_surfaces`/`checked_files` by value).

- `/usr/bin/grep -c "registered_surfaces=39" CLAUDE.md` → `1`; `registered_surfaces=37` → `0`
- `/usr/bin/grep -c "checked_files=69" CLAUDE.md` → `1`; `checked_files=67` → `0`
- `docs/ARCHITECTURE.md` carries the same two new figures (`registered_surfaces=39` → `1`,
  `=37` → `0`)

**A finding beyond the plan's own read_first list:** `docs/gates/CONF-SURFACE.md` is a *hybrid*
surface — its `<!-- GENERATED:FACTS -->`/`<!-- GENERATED:HOW-TO-RUN -->` fences regenerate from
`--describe`, but its surrounding narrative prose is preserved verbatim across `--write` (per the
page's own `narrative-preserved-across-regeneration` control). That prose hardcoded two figures
that moved with this widening (`literal_scan_ledger_adjudicated`: 38 → 68,
`literal_scan_ledger_max`: 152 → 182) and named only `docs/README.md` as a `999.44` surface. All
three were hand-corrected in the same commit — this is exactly the "surface still carrying the old
ones" case the plan's own acceptance criteria anticipated and asked to be named.

### The falsification arm (proves detection, not just a larger number)

1. Confirmed the real tree's `git status --porcelain` was **empty of untracked files** (only the
   already-staged/modified tracked files from this plan's own edits) immediately before the
   mutation.
2. Created a disposable copy: `rsync -a --exclude .git ./ "$SCRATCH"/`.
3. Mutated `CONTRIBUTING.md:40` in the scratch copy only: `Five gates fire` → `Seven gates fire`.
4. Ran `python3 scripts/gen-gate-docs.py --check` inside the scratch copy:

   ```
   CONTRIBUTING.md:40: hand-maintained count literal 'Seven gates' (no exemption class matches)
   CONTRIBUTING.md: deferred-literal-ledger key no longer matches any live hit: 'Five gates' (remove this ledger entry -- its underlying prose was likely already fixed)
   harvested 22/22 expected script-backed entries (22 total)
   literal-scan: 1 non-exempt hit(s) found
   ```

   Exit code: **1**. `--check` FAILED, naming the exact injected hit by file, line and text.
5. Deleted the scratch copy (`rm -rf`), confirmed via a subsequent `ls` reporting "No such file or
   directory."
6. Confirmed the real repository's `git status --porcelain` was **unchanged** — identical to step
   1 — before and after the entire mutation/detection/cleanup sequence.

## Deviations from Plan

### 1. [Rule 3 — blocking issue] Tasks 1, 2 and 3 combined into a single commit

- **Found during:** attempting to commit Task 1 alone, per the standard per-task-commit protocol.
- **Issue:** Task 1's own `<action>` explicitly states `--check` is expected to FAIL at the end of
  that task (33 non-exempt hits, by design — Task 2's input). The installed pre-commit hook (both
  `.githooks/pre-commit` and `scripts/git-hooks/pre-commit`) runs `gen-gate-docs.py --check` as its
  fifth and final gate on every commit, and `--no-verify` is forbidden. Committing Task 1's
  widening alone therefore fails the hook and cannot land as an isolated commit under this
  project's own installed gates.
- **Fix:** completed Task 2's ledger attribution and Task 3's `--write`/re-gate in the same working
  session before making any commit, then staged and committed all four modified files together.
- **Files modified:** `scripts/gen-gate-docs.py`, `CLAUDE.md`, `docs/ARCHITECTURE.md`,
  `docs/gates/CONF-SURFACE.md`.
- **Verification:** the single commit (`a2067f1`) passed both pre-commit hooks and the full
  battery, and every one of the plan's 14 `<verification>` items independently re-run above.
- **Commit:** `a2067f1`.

### 2. [Rule 1 — bug] Reworded `_emit_deferred_ledger_backlog_id()`'s docstring to avoid a self-inflicted WR-08 regression

- **Found during:** Task 2, after adding the two new `999.44` branches.
- **Issue:** the first-draft docstring wording ("one of the three D-05/D-22-D REACH-widened
  surfaces'…") introduced two new count-shaped literals into `gen-gate-docs.py`'s own non-module
  docstrings, tripping `nonmodule_docstring_selffile_ratchet_problems()` (live count 31 vs. pinned
  `_SELF_FILE_NONMODULE_DOCSTRING_HITS = 29`).
- **Fix:** reworded the docstring to state the same fact without the count-adjacent phrasing
  ("a D-05/D-22-D REACH-widened surface's own hand-adjudicated historical figures"). Re-verified:
  live non-module-docstring hit count for this file returned to `29`, matching the pin —
  `_SELF_FILE_NONMODULE_DOCSTRING_HITS` was left unchanged, not raised.
- **Files modified:** `scripts/gen-gate-docs.py`.
- **Verification:** `nonmodule_docstring_selffile_ratchet_problems()` returns no problems; live
  count re-measured at `29` via a standalone `_nonmodule_docstring_hits()` invocation.
- **Commit:** `a2067f1`.

### 3. [Rule 1 — bug] Hand-corrected `docs/gates/CONF-SURFACE.md`'s stale self-referential narrative

- **Found during:** Task 3, after `--write` regenerated the Facts fence with fresh figures.
- **Issue:** `--check`'s D-06 containment floor failed twice — `docs/gates/CONF-SURFACE.md` stated
  `'38'` and `'152'` outside its generated fences (in hand-maintained prose citing
  `literal_scan_ledger_adjudicated` and `literal_scan_ledger_max`) with no matching literal inside
  a fence, because the fresh fence now carries `68` and `182`. This page's narrative is preserved
  verbatim across `--write` (a documented, intentional property — `narrative-preserved-across-
  regeneration`), so a stale citation of a moved fence value does not self-heal.
  Also named only `docs/README.md` as a `999.44` surface, no longer accurate now that
  `docs/PROCESS.md` and `CONTRIBUTING.md` carry `999.44` entries too.
- **Fix:** hand-edited the three affected sentences: the `=38` → `=68` and `=152` → `=182`
  citations, the surface-naming sentence (now lists all three `999.44` surfaces with their
  originating plans), and added a matching "plan 22-07 grew it a second time, 152 → 182" sentence
  to the existing growth-history paragraph, following the same idiom as the pre-existing
  "plan 22-04 (D-22-D) grew it 134 → 152" sentence.
- **Files modified:** `docs/gates/CONF-SURFACE.md`.
- **Verification:** `python3 scripts/gen-gate-docs.py --check` → exit 0, no containment finding.
- **Commit:** `a2067f1`.

**Total deviations:** 1 process deviation (Rule 3, task-boundary/commit-boundary mismatch, fully
disclosed) + 2 auto-fixed bugs (Rule 1, both self-inflicted by this plan's own edits, both fixed
and re-verified before the single commit landed).
**Impact on plan:** none of the three affects the plan's stated scope, success criteria or
threat-model dispositions — all fixes are within the files the plan already names as
`files_modified`.

## Verification

All 14 plan-level `<verification>` items re-run on the live tree, in order:

1. `test -f docs/PROCESS.md` → exit 0; `git log --oneline -1 -- docs/PROCESS.md` → `a3579fb`
2. `registered_surfaces`/`checked_files` → `39 69` (baseline `37 67`)
3. Both new surfaces in `registered_surfaces` and `checked_files`, in no `declined` list — confirmed
4. `/usr/bin/grep -E "^    \('(docs/PROCESS|CONTRIBUTING)\.md'" scripts/gen-gate-docs.py | /usr/bin/grep -vc "'999.44'"` → `0`
5. `/usr/bin/grep -c "TODO: written reason" scripts/gen-gate-docs.py` → `1` (the maintenance-harness's own emitter template string, not a ledger placeholder — same pre-existing condition 22-03/22-04/22-05/22-06 documented)
6. `git diff scripts/gen-gate-docs.py | /usr/bin/grep -cE "^\+.*LiteralExemptionClass\(|^\+def _match_|^\+def _control_"` → `0`
7. `/usr/bin/grep -c "registered_surfaces=37" CLAUDE.md` → `0`; `checked_files=67` → `0`
8. `--describe` → `control_count` `74`, `literal_scan_non_exempt` `0`
9. `--self-test` → exit 0; `--check` → exit 0
10. `python3 scripts/check-links.py` → exit 0 (312 markdown links + 6 namespace refs, 160 files)
11. `git diff scripts/check-quality-harness.py` → empty; `git diff --name-only` contains no `.github/workflows/validation.yml` and no `scripts/check-conf-gate.py`
12. `sh .githooks/pre-commit` → exit 0; `sh scripts/git-hooks/pre-commit` → exit 0
13. `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN`, total `26`
14. Scratch-copy falsification arm → `--check` FAILS naming the injected `CONTRIBUTING.md` hit; real tree `git status --porcelain` unchanged before and after

## Issues Encountered

None beyond the three deviations documented above, all resolved before the single commit landed.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `LITERAL_SCAN_MD_GLOBS` holds 10 entries; `docs/PROCESS.md` and `CONTRIBUTING.md` are opened, not
  declined; `registered_surfaces` reads 39 and `checked_files` reads 69 from the live emission on
  every generated surface that carries these figures.
- Every hit on the two new surfaces resolves to a named `999.44` ledger entry with a unique
  hand-written reason; no catch-all, no `999.41` fallthrough, no placeholder.
- Both ledger guards are repinned fresh from the actual final state (182 / the recomputed digest).
- No exemption class, matcher, control, gate, script or CI job was added; `control_count` is `74`
  and the battery total is `26`.
- The three CONTRACT-06 pins are byte-unchanged and `_GATED_SURFACES` is untouched.
- The widening is proved to detect a wrong `CONTRIBUTING.md` count by scratch-copy mutation, not by
  a number having risen.
- The root `README.md` was not added; it is filed as a finding by plan 22-08.
- Battery confirmed `FIREWALL: GREEN (26/26)` on the full tree with this plan's commit applied;
  both `.githooks/pre-commit` and `scripts/git-hooks/pre-commit` exit 0.
- No blockers for downstream plans in this phase.

## Self-Check: PASSED

- `[ -f scripts/gen-gate-docs.py ]` → FOUND (modified)
- `[ -f CLAUDE.md ]` → FOUND (modified)
- `[ -f docs/ARCHITECTURE.md ]` → FOUND (modified)
- `[ -f docs/gates/CONF-SURFACE.md ]` → FOUND (modified)
- `git log --oneline --all | grep -q a2067f1` → FOUND (the single commit this plan makes)
- All plan-level `<verification>` commands re-run above with observed (not assumed) output,
  including `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)` and the
  scratch-copy falsification arm's exact `--check` failure message.

---
*Phase: 22-cap-the-recursion*
*Completed: 2026-09-08*
