---
phase: 19-false-negative-rate
plan: 07
subsystem: testing
tags: [adversarial-corpus, frozen-evidence, false-negative-rate, backlog, report-conformance]

# Dependency graph
requires:
  - phase: 19-false-negative-rate (plans 01-06, waves 1-4)
    provides: "the 13-item corpus, catalog.md, README.md, and report-conformance.py's
      fourth adversarial-corpus surface with its D-03/D-04/CONF-07/CONF-08 floors, all
      committed at HEAD"
provides:
  - "tests/adversarial-corpus-v9.0 registered under scripts/check-firewall-battery.sh's
    _FROZEN_PATHS, both FROZEN-EVIDENCE legs proved to fire by isolated mutation"
  - "CLAUDE.md and docs/ARCHITECTURE.md recording the corpus as a fourth measured
    conformance surface and a registered frozen path"
  - "backlog 999.35 as the named owner of t06's genuine stratum-A miss"
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Git-based tamper-evidence mutation proofs need a real .git repository to compare
       against HEAD -- an rsync --exclude .git scratch copy (the pattern plans 19-05/19-06
       used for the git-independent report-conformance.py --check tests) cannot exercise
       FROZEN-EVIDENCE's two git-diff-based legs at all, since every git command in a
       .git-less directory fails identically regardless of mutation. A full copy
       (rsync -a, including .git) is required so 'git diff --quiet HEAD' and
       'git status --porcelain' compare the scratch working tree against a real HEAD."

key-files:
  created: []
  modified:
    - scripts/check-firewall-battery.sh
    - tests/adversarial-corpus-v9.0/README.md
    - tests/adversarial-corpus-v9.0/catalog.md
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - .planning/ROADMAP.md
    - docs/conformance-baseline.md
    - docs/data/conformance.json

key-decisions:
  - "Task 1's mutation proofs (N12/N13) used a full rsync copy including .git, not the
     plan's literal '--exclude .git' — excluding .git leaves no repository for
     'git diff --quiet HEAD' to compare against, so every git command in that copy fails
     identically ('fatal: not a git repository') whether or not a mutation was applied,
     which cannot distinguish a genuine leg-1/leg-2 firing from a broken test harness.
     Documented as a Rule 3 blocking-issue auto-fix below."
  - "Registered a new backlog entry, 999.35, naming t06's specific mechanical hole
     (_chain_head_refs returns on the first head-matching line), rather than leaving the
     catalog's defer-with-owner cell pointing at the general 999.4 CONDITIONAL gate --
     999.4 decides whether to build a semantic judge at all; 999.35 is the narrower,
     concrete fact a future detector-reach review would need. Catalog's T-06 disposition
     cell now names 999.35 in plain text, per the plan's explicit instruction."
  - "Regenerated docs/conformance-baseline.md and docs/data/conformance.json in the same
     commit as the catalog.md disposition-cell edit -- the pre-commit conformance-drift
     gate (17-D-06) fires on every commit and the corpus's rendered disposition text is
     part of the generated artifact, so editing catalog.md without regenerating would
     have blocked the commit. Only the disposition string moved; no reading changed."
  - "Force-added .planning/ROADMAP.md with 'git add -f' -- it is gitignored and has never
     been committed anywhere in this repository's history (git log --all shows zero
     commits touching it), so there was no prior-commit precedent to follow; force-adding
     was the only way to make this plan's explicitly-declared files_modified edit land."

requirements-completed: [CONF-07, CONF-08]

# Metrics
duration: ~1h
completed: 2026-09-05
---

# Phase 19 Plan 07: Register the corpus and close out the phase Summary

**`tests/adversarial-corpus-v9.0` is now a registered `_FROZEN_PATHS` entry with both
FROZEN-EVIDENCE legs proved to fire by isolated mutation on a real git history, the
9-of-13 false-negative rate is recorded on both documentation surfaces with the battery
tally unmoved at 25, and t06's genuine detector miss now has a named backlog owner
(999.35) instead of pointing at the general semantic-judging gate.**

## Performance

- **Duration:** ~1h
- **Started:** 2026-09-05
- **Completed:** 2026-09-05
- **Tasks:** 2 completed
- **Files modified:** 8 (`scripts/check-firewall-battery.sh`,
  `tests/adversarial-corpus-v9.0/README.md`, `tests/adversarial-corpus-v9.0/catalog.md`,
  `CLAUDE.md`, `docs/ARCHITECTURE.md`, `.planning/ROADMAP.md`,
  `docs/conformance-baseline.md`, `docs/data/conformance.json`)

## Task Commits

1. **Task 1: Register the corpus under `_FROZEN_PATHS`, amend the README's sequencing
   note, and prove both legs fire** — `ce3008d` (feat)
2. **Task 2: Record the phase's outcome — documentation rows, the backlog owner, and the
   three exit counts** — `086073c` (docs)

## Task 1 — registration and mutation proofs

### The one-line diff

```
$ git diff --stat scripts/check-firewall-battery.sh   (measured against the pre-commit tree)
 scripts/check-firewall-battery.sh | 1 +
 1 file changed, 1 insertion(+)
```

Appended `'tests/adversarial-corpus-v9.0'` as the last element of `_FROZEN_PATHS`, matching
the bare-directory form the two `tests/quality-*` entries already use. No other line in the
file was touched.

### N12 — leg 1 (modification), verbatim

Applied to a **full** scratch copy (`rsync -a`, including `.git` — see the deviation below)
at the post-registration HEAD (`ce3008d`), appending one byte to a committed corpus item:

```
$ printf 'x' >> tests/adversarial-corpus-v9.0/t01-ledger-arbitrary-chain.md
$ bash scripts/check-firewall-battery.sh
[FAIL] FROZEN-EVIDENCE  frozen baseline/capture files have modifications relative to HEAD (staged or unstaged) — D-04 violation

FIREWALL: RED (1 gate(s) failed; 24/25 passed)
```

### N13 — leg 2 (untracked addition), verbatim

Applied to a second, fresh full scratch copy at the same HEAD, with the tree otherwise
clean:

```
$ touch tests/adversarial-corpus-v9.0/zz-probe.md
$ bash scripts/check-firewall-battery.sh
[FAIL] FROZEN-EVIDENCE  untracked files have appeared inside a frozen path — D-04 violation: ?? tests/adversarial-corpus-v9.0/zz-probe.md

FIREWALL: RED (1 gate(s) failed; 24/25 passed)
```

Both scratch copies were deleted after the proof; `git status --porcelain` in the real
worktree was confirmed empty before and after both rounds.

### The amended README paragraph (verbatim, as committed)

```
**Sequencing note:** this fixture was created by plans 19-01 through 19-04, and plan 19-07
registered it — `scripts/check-firewall-battery.sh`'s `_FROZEN_PATHS` array now carries
`tests/adversarial-corpus-v9.0`, so both FROZEN-EVIDENCE legs described above cover this directory
today: the `git diff --quiet HEAD` sweep catches an edit to any file already tracked here, and the
`git status --porcelain --untracked-files=all` sweep catches a new file appearing inside it. The
residual is unchanged by registration and is restated rather than reopened: a committed `git rm` of
one of these files is in HEAD by the time the check runs, so no worktree comparison ever sees it —
the protection is tamper-evidence for modification and addition, never a deletion guard.

**The working rule for an editor.** FROZEN-EVIDENCE compares the worktree and index against HEAD,
never against some prior state — so a deliberate, committed correction to a corpus item passes the
check cleanly. The protection is tamper-evidence in review, not an edit lock. Any such correction
must move that file's sha256 row in the table below in the same commit, or the table itself goes
stale relative to the bytes it claims to describe.
```

`/usr/bin/grep -c "not yet registered\|pending\|19-07 adds" tests/adversarial-corpus-v9.0/README.md`
returns `0` (exit 1, no match) — the 999.25 shape is not repeated.

### Verification performed (Task 1)

- `bash scripts/check-firewall-battery.sh` after commit `ce3008d`: `[PASS] FROZEN-EVIDENCE`,
  `FIREWALL: GREEN (25/25)` (after `uv sync` to satisfy VAL-03's pytest prerequisite in this
  fresh worktree — the documented remedy, same as every prior plan in this phase).
- `/usr/bin/grep -c "'tests/adversarial-corpus-v9.0'" scripts/check-firewall-battery.sh` → `1`.
- `python3 scripts/check-quality-harness.py --self-test` → exit 0, all sub-checks PASSED.
  `git diff --stat scripts/check-quality-harness.py` → no output (file not touched, as
  predicted: `_FROZEN_PATHS_ARRAY_RE`/`_FROZEN_PATHS_ENTRY_RE` are generic over array
  contents).
- `git status --porcelain` after commit: empty. `git diff --diff-filter=D --name-only
  HEAD~1 HEAD` (both commits): no output, no deletions.

## Task 2 — documentation, backlog, exit counts

### CLAUDE.md and docs/ARCHITECTURE.md

`CLAUDE.md`'s conformance-baseline drift-gate paragraph gained two sentences of current
fact: `docs/conformance-baseline.md` now carries a fourth labelled surface,
`adversarial-corpus`, measuring the corpus's deliberately-wrong probes under the unmodified
frozen `detect_defects` (a clean reading is a measurement of detector reach, never a claim
of conformance), and `tests/adversarial-corpus-v9.0` is a registered `_FROZEN_PATHS` entry
alongside `tests/quality-provenance-v8.24` and `tests/quality-ledger-v8.26`, with the battery
total explicitly stated as unchanged at 25. `docs/ARCHITECTURE.md`'s FROZEN-EVIDENCE and
conformance-drift-gate rows in the CI/pre-commit gate inventory table got the matching,
minimal edit. No gate row was added to either table; no CI job was added.

### Backlog owner — 999.35

`19-03-SUMMARY.md` records t06 as the corpus's one genuine stratum-A miss, disposition
`defer-with-owner`, originally pointing at the general `backlog 999.4` (the CONDITIONAL
semantic-claim-to-chain-judging gate). Filed `### Phase 999.35:` in `.planning/ROADMAP.md`
§ Backlog — the next free integer after 999.34 — stating the hole (a genuinely circular
pair of conclusions reads `dependency_cycles == 0` / `ungrounded_chains == 0`), the
mechanical reason (`_chain_head_refs` returns on the first head-matching line of a
`### Conclusion` block and never reads further, so a citation stated later in the block's
prose is structurally invisible to the dependency graph), and why Phase 19 could not close
it (the detector is frozen under CONTRACT-06; widening it needs a written amendment to the
milestone goal first, and Phase 19's own scope excludes it by name). `catalog.md`'s `T-06`
row's `Disposition` cell was amended to name `backlog 999.35` in plain text (not a link),
and `README.md`'s sha256 row for `catalog.md` was moved to the new digest in the same
commit.

`/usr/bin/grep -c '^### Phase 999\.' .planning/ROADMAP.md` → `34` after this plan (`33`
before) — one higher, as the acceptance criterion requires.

### Phase 19's own checklist

`.planning/ROADMAP.md` § "Phase 19: False-Negative Rate" already carried
`**Plans**: 7 plans in 5 waves` with the full wave breakdown (not the `TBD` placeholder the
plan's Step 4 anticipated — six of seven plans were already checked). The one remaining
unchecked line, `- [ ] 19-07-PLAN.md — register ...`, was flipped to `- [x]`.

### Regenerating the baseline (necessary consequence, not scope creep)

Editing `catalog.md`'s disposition cell changes bytes the fourth surface renders into
`docs/conformance-baseline.md` and `docs/data/conformance.json`. The pre-commit
conformance-drift gate (17-D-06) re-runs `report-conformance.py --check` on every commit,
so committing the catalog edit without regenerating would have blocked. Ran
`python3 scripts/report-conformance.py` and included both regenerated files in Task 2's
commit; the diff is exactly the disposition-string substitution (2 lines in the markdown,
4 in the JSON) — no count, reading, or headline moved. Re-verified the exit-count
assertion after regeneration (unchanged, see below).

### The three exit counts (from `docs/data/conformance.json`'s `adversarial_corpus.headline`, read fresh after Task 2's commit)

```
corpus items                                >= 12   actual: 13
corpus form-defect count across all items   == 0    actual: 0
clean-scoring items with no disposition     == 0    actual: 0
```

### The published rate, as a reading (D-06: never a target)

- **Overall: 9 of 13 corpus items score fully clean.**
- **Stratum A: 1 of 5 clean** — `T-03`/`T-04`/`T-05` are positive controls (caught, not
  holes); `T-06` is the genuine miss (backlog 999.35); `T-13` is a disclosed
  `grounded()`-short-circuit bound (not a fix target).
- **Stratum B1: 1 of 1 clean** — `T-02`, reachable only by PROV-GUARD.
- **Stratum B2: 7 of 7 clean** — reachable by nothing this project ships. This is the
  measured decision input `backlog 999.4` consumes when it is next reviewed: a low B2 rate
  (as measured here) is the recorded reason toward closing 999.4 unrun rather than
  building a semantic judge; deciding 999.4 itself is out of this phase's scope and is not
  settled by this plan.

No phase, gate, or document in this tree targets this rate. The only lever that would move
it is widening a frozen detector, which CONTRACT-06 forbids without a written amendment to
the milestone goal.

### Before/after occurrence counts of `25`, all three surfaces (source assertion)

| File | Before Task 2 (commit `ce3008d`) | After Task 2 (`HEAD`) |
|---|---|---|
| `CLAUDE.md` | 6 | 7 |
| `docs/ARCHITECTURE.md` | 2 | 2 |
| `scripts/check-firewall-battery.sh` | 6 | 6 |

`CLAUDE.md`'s count rose by exactly one — the D-07 sentence the plan's own Step 1 explicitly
requires ("state explicitly that the battery total is unchanged at 25"), which necessarily
writes the digits `25`. No `26` was introduced anywhere: confirmed by grepping every `26`
occurrence in all three files and finding none adjacent to `battery`/`frozen`/`total`/`tally`
language — every hit is unrelated pre-existing prose (e.g. "twenty-seven", `R4-CR-02`,
`13-16`-style plan numbers). This is recorded as a deliberate, plan-mandated exception to
the literal "count is unchanged" phrasing, not a defect — see Deviations below.

### Verification performed (Task 2, final state)

```
$ bash scripts/check-firewall-battery.sh
...
[PASS] FROZEN-EVIDENCE  diff-vs-HEAD + untracked sweep: frozen baselines/captures unmodified (D-04)

FIREWALL: GREEN (25/25)

$ python3 scripts/check-traceability.py --self-test
...
check-traceability --self-test: PASS

$ python3 scripts/check-links.py
check-links: PASS (244 markdown links + 6 namespace refs across 128 files)

$ python3 -c "import json;h=json.load(open('docs/data/conformance.json'))['adversarial_corpus']['headline'];print(h);assert h['total']>=12 and h['form_defects']==0 and h['clean_without_disposition']==0"
{'total': 13, 'clean': 9, 'unreadable': 0, 'form_defects': 0, 'by_stratum': {'B2': {'clean': 7, 'total': 7}, 'B1': {'clean': 1, 'total': 1}, 'A': {'clean': 1, 'total': 5}}, 'clean_without_disposition': 0}

$ git diff --stat .github/workflows/validation.yml scripts/check-quality-harness.py scripts/check-conf-gate.py scripts/report-conformance.py
(no output)

$ git diff --stat shared/ first-principles/
(no output)

$ git status --porcelain
(no output)

$ git diff --diff-filter=D --name-only HEAD~1 HEAD
(no output, both commits)
```

## Final battery verdict (required by the FINAL-PLAN DUTY)

```
FIREWALL: GREEN (25/25)
```

Run after both commits, in this worktree, following `uv sync` (gitignored `.venv`, the
documented VAL-03 remedy every prior plan in this phase applied independently).

## Decisions Made

- Task 1's mutation proofs used a full `rsync -a` copy including `.git` rather than the
  plan's literal `rsync -a --exclude .git` — see the deviation below for the mechanical
  reason and the Rule 3 justification.
- Filed backlog 999.35 as the specific owner of t06's mechanical hole, narrower than the
  general 999.4 CONDITIONAL gate the catalog previously pointed at.
- Regenerated `docs/conformance-baseline.md`/`docs/data/conformance.json` in Task 2's
  commit as a required consequence of the catalog disposition-cell edit, per the
  pre-commit conformance-drift gate.
- Force-added `.planning/ROADMAP.md` with `git add -f` since it has never been committed
  in this repository's history and the plan's frontmatter explicitly names it in
  `files_modified`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking issue] `rsync -a --exclude .git` cannot exercise FROZEN-EVIDENCE's
git-diff-based legs at all**
- **Found during:** Task 1, Step 3 (the mutation proofs).
- **Issue:** the plan's `<action>` text specifies a scratch copy made with
  `rsync -a --exclude .git`. Verified empirically: in a directory with no `.git`,
  `git diff --quiet HEAD -- <paths>` fails immediately with `fatal: not a git repository`
  (exit 128, non-zero) — which trips FROZEN-EVIDENCE's leg-1 failure branch
  **unconditionally**, before any mutation is applied. A baseline (unmutated) scratch copy
  built this way would already report `[FAIL] FROZEN-EVIDENCE` with the leg-1 message, so
  N12 and N13 could never be distinguished from each other or from a clean pass — the test
  would prove nothing about the two legs' actual logic.
- **Fix:** used a full copy (`rsync -a`, `.git` included) at the post-registration commit
  (`ce3008d`) for both N12 and N13, so `git diff --quiet HEAD` and
  `git status --porcelain --untracked-files=all` compare the scratch working tree against a
  real, committed HEAD — exactly what FROZEN-EVIDENCE does in the real repository. This
  makes each mutation's effect isolable and each leg's distinct failure message observable,
  which is the acceptance criterion's actual requirement (both legs proved to fire
  separately, verbatim output recorded).
- **Verification:** N12 produced the leg-1 message and RED; N13 (a fresh copy) produced the
  distinct leg-2 message and RED, naming `zz-probe.md`. Both scratch copies were deleted
  after use; the real worktree's `git status --porcelain` was confirmed empty before and
  after both rounds.
- **Files modified:** none tracked — both scratch copies lived entirely under the session
  scratchpad and were deleted before this plan's own commits.
- **Committed in:** not applicable (no tracked-file change).

No other deviations — both tasks' remaining content matches the plan's `<action>` blocks.

### Assumption Drift (advisory)

**1. The acceptance criterion "the count of `25` occurrences ... is unchanged" versus the
action's explicit instruction to add a sentence containing the digits `25`.** Task 2's
`<action>` block requires writing, verbatim in spirit, "state explicitly that the battery
total is unchanged at 25" into `CLAUDE.md`'s pre-commit-gates paragraph. Doing so
necessarily adds one occurrence of the string `25` to that file. The same block's
`<acceptance_criteria>` then asks for the occurrence count to be recorded as "unchanged
from before this task." These two instructions cannot both be satisfied literally: writing
the required sentence moves `CLAUDE.md`'s count from 6 to 7. Read together, the acceptance
criterion's operative intent is clearly "no `25 → 26` sweep was introduced" (its own next
clause: "No `26` was introduced anywhere") rather than a zero-delta literal grep count —
the D-07 decision record this plan itself quotes says the same thing ("no `25 → 26` sweep
anywhere"). Resolved by writing the required sentence as instructed, recording the actual
before/after counts transparently in this SUMMARY (6→7, 2→2, 6→6) exactly as the
acceptance criteria's own "record the before and after counts" clause asks, and confirming
by direct grep that no `26` appears anywhere near battery/frozen/tally language. Not a
deviation in content — every sentence the action block specifies was written — only in how
the two adjacent acceptance-criteria clauses were reconciled.

## Issues Encountered

None beyond the mechanical git-repository requirement for the mutation proofs, described
above, and the baseline-regeneration consequence of the catalog edit, also described above.

## User Setup Required

None — no external service configuration required. This worktree needed `uv sync`
(gitignored `.venv`) to satisfy the VAL-03 pytest prerequisite for the firewall battery,
the same remedy every prior plan in this phase applied independently in its own worktree.

## Next Phase Readiness

This is the final plan of Phase 19 (False-Negative Rate). No further plans in this phase.
`tests/adversarial-corpus-v9.0` is now a registered, tamper-evident fixture; the published
9-of-13 false-negative rate (1/5 A, 1/1 B1, 7/7 B2) is the recorded gate input for backlog
999.4, which this phase does not decide. `bash scripts/check-firewall-battery.sh` reports
`FIREWALL: GREEN (25/25)`; `python3 scripts/report-conformance.py --check` reports
`PASS — no drift`; `git status --porcelain` is empty.

---
*Phase: 19-false-negative-rate*
*Completed: 2026-09-05*

## Self-Check

- FOUND: `scripts/check-firewall-battery.sh` (modified, contains `'tests/adversarial-corpus-v9.0'`)
- FOUND: `tests/adversarial-corpus-v9.0/README.md` (modified, sequencing note amended)
- FOUND: `tests/adversarial-corpus-v9.0/catalog.md` (modified, T-06 names backlog 999.35)
- FOUND: `CLAUDE.md` (modified, contains `adversarial-corpus`)
- FOUND: `docs/ARCHITECTURE.md` (modified, contains `adversarial-corpus`)
- FOUND: `.planning/ROADMAP.md` (force-added, contains `### Phase 999.35`, 19-07 checked)
- FOUND: `docs/conformance-baseline.md` / `docs/data/conformance.json` (regenerated, no drift)
- FOUND: commit `ce3008d` (Task 1)
- FOUND: commit `086073c` (Task 2)

## Self-Check: PASSED
