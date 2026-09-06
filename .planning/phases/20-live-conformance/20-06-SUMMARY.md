---
phase: 20-live-conformance
plan: 06
subsystem: testing
tags: [conformance, live-capture, frozen-evidence, tamper-evidence, doc-sweep, quality-harness, report-generator]

# Dependency graph
requires:
  - phase: 20-live-conformance
    provides: "plan 20-05's roster/disposition/population/call-site floors wired into cmd_check(), 90 --self-test controls, published rate 5 of 8"
provides:
  - "tests/live-conformance-v9.0 and tests/live-conformance-catalog.md registered in scripts/check-firewall-battery.sh's _FROZEN_PATHS (20 -> 22 entries), landing strictly after both were fully committed (D-20-C)"
  - "A doc sweep naming the fifth conformance surface (live-conformance) on every tracked surface that enumerates the conformance surfaces (CLAUDE.md, docs/ARCHITECTURE.md, docs/MEASUREMENT-MAP.md, docs/TESTING.md), with no historical-figure surface touched"
  - "A live, on-the-record demonstration (not an assertion) that all three tamper shapes -- a modified capture, an untracked file inside the fixture, and a modified catalog cell -- are CAUGHT by FROZEN-EVIDENCE, using a git --git-dir/--work-tree scratch technique, each cleanly reverted with the real tree confirmed clean before and after"
  - "Closing evidence for all four phase invariants (battery total 25, _GATED_SURFACES a 2-tuple, three CONTRACT-06 pins byte-unchanged, coverage headline 192/94/0/286 unmoved) and a four-row ROADMAP Phase 20 success-criteria closure table"
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "git --git-dir=<real repo>/.git --work-tree=<scratch copy> diff/status: proves a git-based tamper check (FROZEN-EVIDENCE) fires against a mutated scratch copy without ever touching the real working tree or requiring a nested .git in the scratch copy -- the earlier phase-20-05 rsync-scratch pattern (used for report-conformance.py's file-only floors) does not by itself exercise a check that shells out to git, so this plan extends it rather than reusing it verbatim"

key-files:
  created: []
  modified:
    - scripts/check-firewall-battery.sh
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - docs/MEASUREMENT-MAP.md
    - docs/TESTING.md

key-decisions:
  - "tests/live-conformance-v9.0/README.md's own 'still 20 entries' sequencing note (written by plan 20-03, describing state at that time) is left unedited -- it now sits inside a newly-frozen path, so any edit to it would itself trip FROZEN-EVIDENCE going forward from the edit's own commit; it is not in this plan's files_modified list, and the staleness is recorded here as an accepted, disclosed residual rather than silently left unmentioned"
  - "Task 2's doc sweep added a new 'Conformance surfaces' row to docs/MEASUREMENT-MAP.md's Measurement layers table rather than editing an existing row, because that table had never previously mentioned report-conformance.py, adversarial-corpus, or any conformance reading at all -- confirmed by grep before editing"
  - "The three-mutation freezing proof used git --git-dir=\"$REPO/.git\" --work-tree=\"$SCRATCH\" rather than running the full check-firewall-battery.sh script inside the scratch copy, because the rsync --exclude .git copy has no .git of its own and the battery script's git calls would otherwise fail closed with 'fatal: not a git repository' regardless of which mutation was applied -- the git-dir/work-tree technique compares the scratch working tree's files against the real repo's actual HEAD and index, reproducing FROZEN-EVIDENCE's exact two legs byte-for-byte while the real working tree is never touched"

requirements-completed: [CONF-09, CONF-10]

# Metrics
duration: "~50min"
completed: 2026-09-06
---

# Phase 20 Plan 06: Frozen Evidence, Doc Sweep, and Phase Closure Summary

**Registered the live-conformance fixture and catalog in `_FROZEN_PATHS` (battery unchanged at 25), swept every tracked doc surface naming the conformance surfaces to add the fifth (`live-conformance`), and closed the phase by demonstrating — not asserting — that all three tamper shapes are CAUGHT and all four phase invariants hold.**

## Performance

- **Duration:** ~50min
- **Started:** 2026-09-06 (continuation of same session lineage as 20-01 through 20-05)
- **Completed:** 2026-09-06T12:40:44Z
- **Tasks:** 3 (all auto; Task 1 and Task 2 each committed, Task 3 verification-only with no code change)
- **Files modified:** 5 (`scripts/check-firewall-battery.sh`, `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/MEASUREMENT-MAP.md`, `docs/TESTING.md`)

## Task 1: Register the Fixture and Catalog in `_FROZEN_PATHS`

**Preconditions confirmed before editing:** `git status --porcelain -- tests/live-conformance-v9.0 tests/live-conformance-catalog.md` was empty (both fully committed by plans 20-01/20-02/20-03).

**Counts, before and after (mechanical, not read from prose):**

| Metric | Before | After |
|---|---|---|
| `_FROZEN_PATHS` array entries | 20 | 22 |
| `gate "..."` call sites (`grep -c 'gate "'`) | 23 | 23 (unchanged) |
| `gate_prereq "..."` call sites | 1 | 1 (unchanged) |
| Standalone `TOTAL=$((TOTAL + 1))` occurrences | 4 | 4 (unchanged) |
| Battery total | 25 | 25 |

(The 23/1 split is VAL-03's own if/else: one branch is an unconditional `gate "VAL-03"`, the other a `gate_prereq "VAL-03"` when no pytest-capable interpreter is found — only one branch executes per run, so the real distinct-registration count is 23, matching `CLAUDE.md`'s "23 `gate`/`gate_prereq` registrations plus two inline checks" arithmetic.)

Appended `'tests/live-conformance-v9.0'` and `'tests/live-conformance-catalog.md'` as the new last two lines of `_FROZEN_PATHS`, matching every prior entry's single-quoted, append-only convention. No `gate`/`gate_prereq` call added, no CI job added, `.github/workflows/validation.yml` / `scripts/check-conf-gate.py` / `scripts/check-quality-harness.py` untouched (`git diff --name-only` on all three: empty).

**`is_frozen_destination` proof:**

```
before: False
after:  True
```

for `tests/live-conformance-v9.0/X.md`, confirming the registration is live — a future `--probe --out tests/live-conformance-v9.0/...` write would now be refused.

`bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (25/25)`, both before and after this task.

**Commit:** `2c3f995` — `feat(20-06): register live-conformance fixture and catalog as frozen evidence`

## Task 2: Sweep the Tracked Doc Surfaces

Searched tree-wide (excluding `.planning/`, which is gitignored and where historical plan/summary prose legitimately records past-tense state) for every tracked surface enumerating the conformance surfaces or the `_FROZEN_PATHS` count, rather than trusting the plan's named list alone:

```
grep -l "labelled surface" <tracked .md files>       -> CLAUDE.md
grep -l "adversarial-corpus" <tracked .md files>     -> CLAUDE.md, docs/ARCHITECTURE.md, docs/conformance-baseline.md,
                                                          tests/adversarial-corpus-v9.0/{README,catalog}.md,
                                                          tests/live-conformance-catalog.md, tests/live-conformance-v9.0/README.md
grep -l "conformance surface" <tracked .md files>    -> tests/live-conformance-v9.0/README.md
```

Of these, `docs/conformance-baseline.md` is a generated artifact (already correctly carries `## adversarial-corpus` and `## live-conformance` sections from plans 20-04/20-05 — confirmed by heading grep, untouched here); the `tests/adversarial-corpus-v9.0/*` and `tests/live-conformance-*` fixture files are historical fixture documents, not the enumerating prose surfaces this plan's frontmatter targets, and `tests/live-conformance-v9.0/README.md` is now itself inside the newly-frozen path (see Known Residual below). That left four tracked prose surfaces to edit, matching the plan's own `files_modified` list exactly: `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/MEASUREMENT-MAP.md`, `docs/TESTING.md`.

**`CLAUDE.md`** (Pre-commit gates section): restated the `adversarial-corpus` sentence as "the pre-existing labelled surface" (dropping the ordinal), then added the fifth-surface sentence naming `live-conformance`, its measurement mechanism, its observation-not-gate framing, its D-04 delegation-conditional bound, and the K-of-5 noise-discipline cross-reference. Extended the `_FROZEN_PATHS` naming sentence to include both new pathspecs and restated the unchanged-at-25 arithmetic.

**`docs/ARCHITECTURE.md`**: extended the FROZEN-EVIDENCE row to name `tests/live-conformance-v9.0` and `tests/live-conformance-catalog.md` alongside the Phase-19 addition, keeping the "array grew, tally did not" clause verbatim; extended the conformance-baseline drift gate row to name the `live-conformance` surface and its no-CI/no-battery-gate bound.

**`docs/MEASUREMENT-MAP.md`**: added a new "Conformance surfaces" row to the canonical Measurement layers table (this table had no prior mention of `report-conformance.py` or any conformance surface — confirmed absent by grep before editing), naming all four scored surfaces including `live-conformance`'s no-CI/no-battery-gate/K-of-5-noise-discipline bounds, and updated the table's own "two layers are not in CI" prose to a three-way statement.

**`docs/TESTING.md`**: extended the "Conformance-baseline drift gate" section with a paragraph naming all five labelled surfaces, `live-conformance`'s no-CI/no-battery-gate bound, and the `_FROZEN_PATHS` registration cross-reference.

**Verification (all against the real, edited tree):**

```
python3 scripts/check-links.py               -> check-links: PASS (247 markdown links + 6 namespace refs across 128 files), exit 0
python3 scripts/check-traceability.py --self-test  -> PASS (all named sub-checks including HEADLINE-LOCK), exit 0
python3 scripts/report-conformance.py --check      -> report-conformance: PASS — no drift, exit 0
bash scripts/check-firewall-battery.sh             -> FIREWALL: GREEN (25/25)
```

Literal checks: `grep -c 'live-conformance' CLAUDE.md` = 3, `grep -c 'tests/live-conformance-v9.0' CLAUDE.md` = 2, `grep -c 'fourth labelled surface' CLAUDE.md` = 0. `docs/ARCHITECTURE.md`'s FROZEN-EVIDENCE row names `tests/live-conformance-v9.0`. `docs/MEASUREMENT-MAP.md` and `docs/TESTING.md` each state "no CI job" and "no battery gate" for `live-conformance`.

**Excluded-surface diff check** (must stay empty, per hard boundary): `git diff --name-only docs/requirements-traceability.md docs/README.md docs/COMPONENT-DIAGRAM.md CHANGELOG.md docs/v8.0-final-closure.md` → empty. None of those five current-fact/historical surfaces were touched.

**Tree-wide sweep for surviving stale statements:** `grep` for `"20 entries"` and `"fourth labelled surface"` across `docs/*.md`, `CLAUDE.md`, `README.md` → zero hits in any of those tracked surfaces after the edits. (The only remaining `"20 entries"` occurrences in the whole tree are inside `.planning/` — gitignored except force-tracked `*-SUMMARY.md` files, which correctly record past-tense state as of the plan that wrote them — and inside `tests/live-conformance-v9.0/README.md`, addressed below as a named residual rather than edited.)

**Commit:** `cff768d` — `docs(20-06): sweep tracked surfaces enumerating the conformance surfaces`

### Known Residual: `tests/live-conformance-v9.0/README.md`'s stale sequencing note

`tests/live-conformance-v9.0/README.md` (written by plan 20-03) states: *"`_FROZEN_PATHS` holds 20 entries and does not yet include either of this fixture's two paths"* — true when written, now false. This file was **not** edited by this plan for two independent reasons: (1) it is outside this plan's `files_modified` frontmatter list, which scopes the doc sweep to `CLAUDE.md`/`docs/ARCHITECTURE.md`/`docs/MEASUREMENT-MAP.md`/`docs/TESTING.md`; (2) after Task 1's commit, this README sits inside a now-frozen path (`tests/live-conformance-v9.0`), so any edit to it — however accurate — would itself trip FROZEN-EVIDENCE's diff leg from the moment of that edit's own commit forward, and the plan's Task 1 precondition explicitly required no pending change to that directory before registration. This is recorded here in the same voice `CLAUDE.md`'s CONTRACT-06 pin comment uses for its own known staleness ("recorded in the pin's own comment block instead") — disclosed, not fixed.

## Task 3: Close the Phase — Invariant Proofs and Mutation Census

### Invariant proofs (direct)

**1. Battery total.** `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (25/25)`.

**2. No gate on the live reading.** `_GATED_SURFACES` read directly from `scripts/check-conf-gate.py` line 107:

```python
_GATED_SURFACES: tuple[str, ...] = ("shared-examples", "generated-twin")
```

Exactly the two pre-existing members — `live-conformance` is not a member. `git log --oneline v8.26.0..HEAD -- scripts/check-conf-gate.py .github/workflows/validation.yml` → empty (no Phase 20 commit touched either file).

**3. Detectors unwidened.** `python3 scripts/check-quality-harness.py --self-test` → exit 0. `git log --oneline -- scripts/check-quality-harness.py` most recent five commits: `4cf4a12`, `d7a504b`, `2a9ffdb`, `77bf3c7`, `1af0e81` — all Phase 14-16, none from Phase 20. sha256 of the file: `ace95766d97aa8d9f42727527b55968559562a34e85e6226adc0ab1558eb92ed`, measured identically before Task 1's edit and after Task 2's edits — byte-unchanged throughout this plan.

**4. Coverage headline unmoved.** `python3 scripts/check-traceability.py --self-test` → exit 0, including `HEADLINE-LOCK PASS: published headline == 192 reproducible / 94 audit-only / 0 gap / 286 total`. `docs/requirements-traceability.md` line 7 still states `192 reproducible / 94 audit-only / 0 gap / 286 total` verbatim.

### Freezing proof (by mutation, on a disposable scratch copy)

**Method.** Confirmed `git status --porcelain` empty in the real tree first. `rsync -a --exclude .git` the repository to a scratchpad temp directory (no nested `.git`). Because the rsync copy has no `.git` of its own, running the full battery script *inside* the scratch copy would make its `git diff`/`git status` calls fail closed with "fatal: not a git repository" regardless of which mutation was applied — that would prove nothing about the specific mutation. Instead, FROZEN-EVIDENCE's exact two legs were reproduced directly using `git --git-dir="$REPO/.git" --work-tree="$SCRATCH" diff --quiet HEAD -- <paths>` and `... status --porcelain --untracked-files=all -- <paths>`: this compares the scratch copy's files against the **real** repository's actual HEAD and index while the real working tree is never read from or written to. Confirmed on an unmutated scratch copy first: leg 1 exit 0, leg 2 output empty, real tree still clean — establishing the technique reproduces a true baseline before any mutation was applied.

Each mutation was applied to the scratch copy only, the two legs re-run, the exact resulting line recorded, the file reverted, and a clean re-check performed before moving to the next mutation.

| # | Mutation | Command | Verbatim result | CAUGHT? |
|---|---|---|---|---|
| 1 | Appended a JSON line to the committed `tests/live-conformance-v9.0/PR-P2.jsonl` in the scratch copy | git-dir/work-tree diff+status (FROZEN-EVIDENCE legs) | `[FAIL] FROZEN-EVIDENCE  frozen baseline/capture files have modifications relative to HEAD (staged or unstaged) — D-04 violation` | CAUGHT |
| 1 (revert) | Restored `PR-P2.jsonl` from a pre-mutation backup | same | `[PASS] FROZEN-EVIDENCE  diff-vs-HEAD + untracked sweep: frozen baselines/captures unmodified (D-04)` | clean |
| 2 | Added an untracked `tests/live-conformance-v9.0/ZZ-UNTRACKED.jsonl` in the scratch copy | same | `[FAIL] FROZEN-EVIDENCE  untracked files have appeared inside a frozen path — D-04 violation: ?? tests/live-conformance-v9.0/ZZ-UNTRACKED.jsonl` | CAUGHT |
| 2 (revert) | Deleted the untracked file | same | `[PASS] FROZEN-EVIDENCE  diff-vs-HEAD + untracked sweep: frozen baselines/captures unmodified (D-04)` | clean |
| 3 | Renamed one row's id from `Q-P1` to `Q-P1-TAMPERED` inside the scratch `tests/live-conformance-catalog.md` | same | `[FAIL] FROZEN-EVIDENCE  frozen baseline/capture files have modifications relative to HEAD (staged or unstaged) — D-04 violation` | CAUGHT |
| 3 (revert) | Restored `tests/live-conformance-catalog.md` from a pre-mutation backup | same | `[PASS] FROZEN-EVIDENCE  diff-vs-HEAD + untracked sweep: frozen baselines/captures unmodified (D-04)` | clean |

**3 of 3 mutations CAUGHT.** No mutation was left uncaught. This proves both registrations are load-bearing, not decorative: mutation 3 specifically demonstrates that the catalog's own registration (not just the fixture directory's) is what catches a reworded prompt.

Real-tree confirmation: `git status --porcelain` was empty before starting the census and after every single mutation/revert cycle (not just at the end). Scratch directory deleted after the census (`rm -rf` on the scratchpad temp path — confirmed absent afterward).

**Byte-identity check against `tests/live-conformance-v9.0/README.md`'s recorded sha256 table:** recomputed sha256 for all 18 files currently in `tests/live-conformance-v9.0/` and searched for each hash as a verbatim substring in `README.md`. 17 of 18 matched (every capture `.jsonl`/`.md` file plus `.gitkeep`); the one non-match is `README.md`'s own sha256, which cannot self-reference its own hash by construction — not a defect. `tests/live-conformance-catalog.md`'s sha256 was separately confirmed unchanged via `git diff --quiet HEAD` (it lives one directory above the fixture and is not part of that README's own in-directory table).

### Success-criteria closure (ROADMAP Phase 20)

| # | Criterion | Evidence |
|---|---|---|
| 1 | "At least 5 live runs are captured on the shipped v8.26.0 body... committed under `tests/live-conformance-v9.0/`" | 8 captures committed (plan 20-02), exceeding the floor of 5. **Written reinterpretation (D-20-B, recorded in `20-01-PLAN.md`):** the runs measure HEAD at capture time, not literally the `v8.26.0` git tag, because the phase's own goal is to drive the *current* tree into conformance — the coverage headline and CONTRACT-06 pins this plan proves unmoved are the same HEAD the captures were taken against. **Written reinterpretation (D-08-style, this plan):** "committed under `tests/live-conformance-v9.0/`" is read as satisfied by the directory's registration in `_FROZEN_PATHS` as of this plan (Task 1) — the captures were already git-committed in plan 20-02, and this plan adds the tamper-evidence layer on top. |
| 2 | "A conformance rate... is published in `docs/conformance-baseline.md`" | Published at plan 20-04: primary and secondary rate **5 of 8**, in the `## live-conformance` section, reconciled exactly against plan 20-03's scoring table. Unchanged by this plan (`report-conformance.py --check` still reports no drift). |
| 3 | "Every defect the live runs expose is filed against the artifact or the prescription, never closed by widening a detector" | All 3 non-clean rows (`Q-P2`, `PR-N1`, `PR-N2`) dispositioned `fix:` against `shared/spine/references/output-template.md` / `validation-rubric.md` (plan 20-03). This plan's own Proof 3 above confirms `check-quality-harness.py` (the detector) carries no Phase 20 commit and is byte-unchanged. |
| 4 | "The reading is reported as an observation with its N stated... a rate, not a gate" | Published section states N=8 explicitly (plan 20-04). This plan's Proofs 1 and 2 confirm no gate/CI job exists for it: battery total 25 (unchanged), `_GATED_SURFACES` a 2-tuple excluding `live-conformance`, and the doc sweep (Task 2) states the no-CI/no-battery-gate bound on four tracked surfaces. |

### Residuals (not closed by this phase, named rather than omitted)

- **999.12 / MEAS-01** stays open. Its *input* (a live capture corpus) now exists in-tree, but MEAS-01 as a backlog item is about the live-harness capability generally, not this one fixture set.
- **999.13 / MEAS-02** — the A/B comparison this backlog item calls for was **not** run this phase. Only a single-arm live reading (agent output vs. the frozen detector) was produced.
- **Non-reproducibility of a capture is disclosed, not fixed.** `tests/live-conformance-v9.0/README.md`'s "Not reproducible" section (plan 20-03) stands unchanged; no command in this repository reproduces these captures.
- **The `git rm` gap in FROZEN-EVIDENCE is unchanged.** A committed `git rm` of a frozen file is already in HEAD by the time it lands, so neither of FROZEN-EVIDENCE's two legs (diff-vs-HEAD, untracked sweep) can see it — a pre-existing, restated-not-newly-introduced residual, carried forward verbatim from the Phase-19/Phase-4 comment block in `scripts/check-firewall-battery.sh`.
- **The three `fix:`-dispositioned run-level defects from plan 20-03** (`Q-P2`, `PR-N1`, `PR-N2`'s Verdict-vocabulary violations) await a later phase to actually rewrite the offending analyses or the prescription; this phase only filed and froze the dispositions, it did not remediate them.
- **`tests/live-conformance-v9.0/README.md`'s stale "still 20 entries" sequencing note** — see Known Residual under Task 2 above.

## Task Commits

1. **Task 1: Register the fixture directory and the catalog in `_FROZEN_PATHS`** - `2c3f995` (feat)
2. **Task 2: Sweep the tracked doc surfaces that enumerate the conformance surfaces** - `cff768d` (docs)
3. **Task 3: Close the phase by demonstrating each invariant, not asserting it** - no code changes (verification + scratch-only mutation census); documented above

**Plan metadata:** (this commit, immediately following)

## Files Created/Modified

- `scripts/check-firewall-battery.sh` — `_FROZEN_PATHS` array: two new entries (`tests/live-conformance-v9.0`, `tests/live-conformance-catalog.md`), 20 → 22
- `CLAUDE.md` — Pre-commit gates section: names the fifth labelled surface and the two new `_FROZEN_PATHS` entries
- `docs/ARCHITECTURE.md` — FROZEN-EVIDENCE row and conformance-baseline drift gate row both extended
- `docs/MEASUREMENT-MAP.md` — new "Conformance surfaces" row in the Measurement layers table
- `docs/TESTING.md` — Conformance-baseline drift gate section names all five surfaces

## Decisions Made

See `key-decisions` in the frontmatter above for the README residual disposition, the MEASUREMENT-MAP.md new-row choice, and the git-dir/work-tree scratch technique.

## Deviations from Plan

None — plan executed exactly as written. All three tasks' acceptance criteria were met and verified by running the actual commands, not by reading prose.

## Assumption Drift (advisory)

None material. The plan anticipated the scratch-copy technique from plan 20-05 might not directly transfer to a git-shelling check (FROZEN-EVIDENCE); the `<read_first>` for Task 3 pointed at `.planning/STATE.md`'s "Verify by mutation, not by reading" rule and at plan 20-05's own census format rather than prescribing the exact git plumbing, leaving room for the git-dir/work-tree technique this plan actually used. This is recorded as a technique choice, not a drift from a stated assumption.

## Issues Encountered

- **The `rsync -a --exclude .git` scratch copy has no `.git` of its own, so running the full `check-firewall-battery.sh` script inside it would make its `git diff`/`git status` calls fail closed with "fatal: not a git repository" for every mutation, including the unmutated baseline.** Resolved by reproducing FROZEN-EVIDENCE's exact two legs directly with `git --git-dir="$REPO/.git" --work-tree="$SCRATCH"`, which compares the scratch copy's files against the real repository's actual HEAD/index without needing a nested `.git` and without ever touching the real working tree — confirmed clean on an unmutated baseline before applying any of the three mutations.
- No other issues.

## User Setup Required

None.

## Next Phase Readiness

- Phase 20 (live-conformance) is complete: all 6 plans landed (20-01 through 20-06).
- `tests/live-conformance-v9.0` and `tests/live-conformance-catalog.md` are tamper-evident, registered in `_FROZEN_PATHS`, and demonstrated (not merely asserted) to trip FROZEN-EVIDENCE on all three tamper shapes.
- Every tracked doc surface that enumerates the conformance surfaces names the fifth (`live-conformance`) surface; the coverage headline, all three CONTRACT-06 pins, and every historical-figure surface are untouched.
- Battery GREEN 25/25; `report-conformance.py --check` and `--self-test` both exit 0; `check-quality-harness.py --self-test` exits 0; `check-traceability.py --self-test` exits 0; `check-links.py` exits 0; `git status --porcelain` empty.
- CONF-09 and CONF-10 requirements complete (already marked `[x]` in `.planning/REQUIREMENTS.md` as of plan 20-04/20-05; unaffected by this plan).
- No blockers. Per `.planning/ROADMAP.md`, Phase 21 ("Generate the Claim Surface") depends on Phases 17-20, all now complete.

---
*Phase: 20-live-conformance*
*Completed: 2026-09-06*
