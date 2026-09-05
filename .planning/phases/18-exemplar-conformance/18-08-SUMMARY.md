---
phase: 18-exemplar-conformance
plan: 08
subsystem: testing
tags: [ci-gates, firewall-battery, documentation-sweep, mutation-testing]

# Dependency graph
requires:
  - phase: 18-exemplar-conformance
    plan: 07
    provides: scripts/check-conf-gate.py — the standing CONF-GATE comparator,
      its --self-test battery, and the D-08 live anti-vacuity arm
provides:
  - CONF-GATE registered in scripts/check-firewall-battery.sh (self-test +
    live shape) and in .github/workflows/validation.yml as
    `name: check-conf-gate (CONF-GATE)`; battery reads GREEN 25/25
  - Five doc surfaces (CLAUDE.md x2 locations, docs/ARCHITECTURE.md,
    docs/README.md, docs/v8.0-final-closure.md x2 locations) updated from
    24 to 25 as a current fact; two dated-history surfaces (CLAUDE.md's
    GATE-01 row, CHANGELOG.md's v8.26.0 entry) left byte-unchanged
  - A written mutation ledger proving eight of this phase's success
    criteria by breaking each on a disposable scratch copy, including one
    disclosed negative finding (round 8a's stated expectation does not hold
    against REG-GUARD's actual one-directional check)
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Battery gate registration in the self-test + live shape (PROV-GUARD/
      SCAN-GUARD precedent): two sub-commands under one `gate` call, both
      counted once against TOTAL."
    - "Mutation-on-scratch-copy verification: rsync -a --exclude .git to
      /tmp, mutate, run the live gate, record verbatim output, delete the
      copy, re-confirm the real tree's git status is empty before and
      after — never mutate in place."

key-files:
  created: []
  modified:
    - scripts/check-firewall-battery.sh
    - .github/workflows/validation.yml
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - docs/README.md
    - docs/v8.0-final-closure.md

key-decisions:
  - "Round 8a's mutation (comment out the battery-side `gate \"CONF-GATE\"`
    call, leave the CI job intact) does NOT turn REG-GUARD red, contradicting
    the plan's stated expectation. Verified twice — once by commenting the
    full four-line call, once by literally breaking only the first line — both
    produced `check-registration: PASS ... exit 0`. Root cause: `verify_ci_job_registration`
    iterates over `battery_gate_ids` only; removing a gate from that list
    removes it from consideration entirely rather than surfacing it as an
    orphaned CI job. This is REG-GUARD's actual, disclosed scope (CLAUDE.md's
    own REG-GUARD row states only the battery-to-CI direction), not a defect
    introduced by this plan — recorded honestly per the mutation discipline
    rather than reinterpreted to force a pass."
  - "Round 8b (drop the `(CONF-GATE)` suffix from the CI job's `name:` field,
    leaving the battery registration intact) DOES turn REG-GUARD red, naming
    the gate id with no matching job exactly as predicted — this is the half
    of Criterion 6 that is actually load-bearing against a deleted-CI-job
    regression."
  - "CONF-GATE's gate-table row (CLAUDE.md and docs/ARCHITECTURE.md) states
    both what the gate asserts and what it explicitly does not (citation
    correctness; `heading_malformed_blocks == 0` as measured-reach
    conformance, not a global no-R7-violations claim), matching the plan's
    third success criterion and the HC-BOUND/PROV-GUARD row voice."

patterns-established: []

requirements-completed: [CONF-06]

# Metrics
duration: ~70min (estimated; explicit start timestamp not captured)
completed: 2026-09-05
---

# Phase 18 Plan 08: Exemplar Conformance — Registration, Doc Sweep and Mutation Proof Summary

**Registered CONF-GATE in the battery (self-test + live shape) and in CI as `check-conf-gate (CONF-GATE)`, swept five doc surfaces from 24 to 25 while leaving two dated-history mentions untouched, and proved eight of the phase's success criteria by mutation on disposable scratch copies — including one disclosed negative finding where the plan's stated expectation for a REG-GUARD mutation did not hold against the gate's actual one-directional design.**

## Performance

- **Duration:** ~70 min (estimated)
- **Completed:** 2026-09-05
- **Tasks:** 3 completed
- **Files modified:** 6 (2 registration surfaces, 4 documentation surfaces)

## Accomplishments

- `scripts/check-firewall-battery.sh` gains `gate "CONF-GATE"` immediately after
  `HC-BOUND`, in the self-test + live two-sub-command shape (PROV-GUARD/SCAN-GUARD
  precedent). `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (25/25)`
  with a `[PASS] CONF-GATE` line.
- `.github/workflows/validation.yml` gains a `check-conf-gate` job with
  `name: check-conf-gate (CONF-GATE)`, copying the `check-provenance` block's six-step
  shape verbatim with the script name substituted. The workflow now has 22 `runs-on:`
  entries (was 21).
- `python3 scripts/check-registration.py --self-test` and the live leg both exit 0 —
  REG-GUARD passes on both the plugin axis and the CI-job axis, reporting
  `22/23 battery gates CI-registered + 1 battery-only by design`.
- Five doc surfaces stating the battery count as a current fact now say 25:
  `CLAUDE.md`'s gate table (new CONF-GATE row) and tally paragraph (`24/24` → `25/25`,
  registration count `22` → `23`); `docs/ARCHITECTURE.md`'s inventory table (new
  CONF-GATE row), arithmetic (`21 + 1 + 2 = 24` → `22 + 1 + 2 = 25`), and registration
  history sentence; `docs/README.md`'s staleness table (`24/24` → `25/25`);
  `docs/v8.0-final-closure.md`'s two present-tense mentions (line ~21 and line ~113,
  both `24/24` → `25/25`, the latter appending `CONF-GATE (v9.0.0, Phase 18)` to the
  added-gates list).
- The residual re-grep for `24/24|24 tallied|all 24 battery` across
  `docs/*.md CLAUDE.md README.md CONTRIBUTING.md CHANGELOG.md` returns exactly 2 lines
  (was 7 before this sweep): `CLAUDE.md:161` (GATE-01's dated `60 → 20` incident) and
  `CHANGELOG.md:30` (the `[8.26.0]` entry's own recorded state) — both left byte-unchanged
  as required.
- `python3 scripts/check-links.py` exits 0 (`PASS (244 markdown links + 6 namespace refs
  across 128 files)`) after the doc edits.
- Eight mutation rounds (ten sub-rounds counting 7a/7b and 8a/8b) run on disposable
  `rsync -a --exclude .git` scratch copies under `/tmp` — full ledger below. Seven of the
  ten sub-rounds turned their named gate red exactly as predicted; one (8a) did not, and
  is recorded as a genuine negative finding rather than silently dropped or reinterpreted.
- `scripts/check-quality-harness.py` confirmed byte-identical to the phase-start base:
  `git diff --stat 9a1cde1ead70f607eff4afe96c268b19d4803491 -- scripts/check-quality-harness.py`
  produces no output.
- Final all-green run, in one shot against the untouched real tree: `check-conf-gate.py`
  exits 0 (live + `--self-test`), `check-registration.py` exits 0,
  `report-conformance.py --check` exits 0 (`PASS — no drift`), `sync-content.py --check`
  exits 0, and `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (25/25)`.
  `git status --porcelain` is empty and no `/tmp/conf-mutation-*` scratch directory
  survives.

## Task Commits

Each task was committed atomically:

1. **Task 1: Register CONF-GATE in the battery and in CI** - `99bb95d` (feat)
2. **Task 2: Sweep every doc surface stating the battery count as a current fact** - `fc9b1dd` (docs)
3. **Task 3: Prove every success criterion by mutation on a scratch copy** - committed together with this SUMMARY.md (no source files changed by this task; the mutation work ran entirely on disposable `/tmp` copies, never on the real tree)

**Plan metadata:** committed together with this SUMMARY.md (worktree mode; STATE.md/ROADMAP.md
updates deferred to the orchestrator).

## Files Created/Modified

- `scripts/check-firewall-battery.sh` — adds `gate "CONF-GATE"` (self-test + live) after
  `HC-BOUND`, preceded by a named-purpose comment matching its neighbours' voice.
- `.github/workflows/validation.yml` — adds the `check-conf-gate` job
  (`name: check-conf-gate (CONF-GATE)`), copying `check-provenance`'s six-step shape.
- `CLAUDE.md` — new CONF-GATE gate-table row (states what it asserts and does not),
  updated `Validation scripts` convenience list, updated tally paragraph (25/25, 23
  registrations, CONF-GATE history sentence appended).
- `docs/ARCHITECTURE.md` — new CONF-GATE inventory row, updated three-surface
  arithmetic (`22 + 1 + 2 = 25`), updated registration-history paragraph naming
  CONF-GATE's v9.0.0/Phase 18 registration.
- `docs/README.md` — staleness table's present-tense battery reading updated to 25/25.
- `docs/v8.0-final-closure.md` — both present-tense battery mentions updated to 25/25;
  the second appends CONF-GATE to the list of gates added since v8.0.

## Decisions Made

- **Compact HC-BOUND-shaped gate-table row, not PROV-GUARD's accumulated-history
  shape** — CONF-GATE has no prior-milestone history to accumulate, so its row states
  what it measures and its two disclosed non-assertions in one paragraph, matching the
  interfaces section's explicit instruction.
- **Round 8a recorded as a disclosed negative finding rather than reinterpreted to
  pass.** See `key-decisions` in the frontmatter and the ledger below for the full
  mechanism: REG-GUARD's CI-job axis only iterates over gate ids already present in the
  battery text, so removing a gate from the battery removes it from consideration
  entirely rather than surfacing an orphaned CI job. This is consistent with
  `CLAUDE.md`'s own REG-GUARD row, which documents only the battery→CI direction.
- **Registration-history sentence pattern reused from SCAN-GUARD's precedent**, naming
  the milestone (v9.0.0), phase (18), and shape (self-test + live, matching
  PROV-GUARD/SCAN-GUARD) rather than the `--self-test`-only shape HARN-01/02/03 and
  HC-BOUND use.

## Deviations from Plan

None — all three tasks executed as written, including the mutation task's explicit
instruction to report a round that could not be made to fail "in writing — never quietly
dropped" (round 8a).

## Mutation Ledger (Task 3)

Every round below ran on a disposable `rsync -a --exclude .git <repo> /tmp/conf-mutation-N/`
copy. `git status --porcelain` in the real repo was checked and confirmed empty
immediately before creating each scratch copy and immediately after deleting it — the
real tree was never mutated. All scratch directories were deleted at the end of their
round; `ls -d /tmp/conf-mutation-* 2>/dev/null` returns nothing at the end of Task 3.

### Round 1 — Criterion 1 (`unreadable` / SectionResolutionError target = 0)

- **Mutation:** In `/tmp/conf-mutation-1/shared/examples/estimate-fermi.md`, stripped the
  leading `3. ` from the `## 3. Ground Truths` heading, leaving `## Ground Truths`.
- **Command:** `cd /tmp/conf-mutation-1 && python3 scripts/check-conf-gate.py`
- **Verbatim output:**
  ```
  check-conf-gate: FAIL — TARGET EXCEEDED [shared-examples] unreadable: 1 > target 0
  ```
  Exit code 1.
- **Before:** `git status --porcelain` in the real repo — empty.
- **After:** `git status --porcelain` in the real repo — empty. Scratch copy deleted.
- **Disclosure:** the gate went red and named the broken surface and metric
  (`[shared-examples] unreadable`), but `_targets_problems` aggregates counts per
  surface and never names the individual file — this is the comparator's disclosed
  aggregation granularity (see its own docstring), not a defect. The plan's phrasing
  ("naming that file") is read as satisfied at the surface+metric granularity CONF-GATE
  actually reports at, consistent with every other target-breach round below.

### Round 2 — Criterion 2 (`heading_malformed_blocks` target = 0)

- **Mutation:** In `/tmp/conf-mutation-2/shared/examples/ishikawa-fishbone.md`, re-wrapped
  one hop across two physical lines — removed the leading `→ ` from
  `→ The "felt unsupported" signal maps onto the structurally uncovered account segment`
  and replaced it with two leading spaces (no arrow).
- **Command:** `cd /tmp/conf-mutation-2 && python3 scripts/check-conf-gate.py`
- **Verbatim output:**
  ```
  check-conf-gate: FAIL — TARGET EXCEEDED [shared-examples] heading_malformed_blocks: 1 > target 0
  ```
  Exit code 1.
- **Before:** `git status --porcelain` in the real repo — empty.
- **After:** `git status --porcelain` in the real repo — empty. Scratch copy deleted.

### Round 3 — Criterion 3 (`nonconforming_verdict_cells` target = 0)

- **Mutation:** In `/tmp/conf-mutation-3/shared/examples/software-systems.md`, replaced the
  Verdict cell `Accept — measured ~2/day ceiling; business impact is real even without a
  quantified dollar value` with the bare `Accept`.
- **Command:** `cd /tmp/conf-mutation-3 && python3 scripts/check-conf-gate.py`
- **Verbatim output:**
  ```
  check-conf-gate: FAIL — TARGET EXCEEDED [shared-examples] nonconforming_verdict_cells: 1 > target 0
  ```
  Exit code 1.
- **Before:** `git status --porcelain` in the real repo — empty.
- **After:** `git status --porcelain` in the real repo — empty. Scratch copy deleted.

### Round 4 — Criterion 4 (`silent_untraced_claims` target = 0)

- **Mutation:** In `/tmp/conf-mutation-4/shared/examples/self-application.md`, stripped the
  `(chain C1)` citation from `**Commission the GT-9? measurement** (chain C1) that would
  settle...`, leaving the claim uncited.
- **Command:** `cd /tmp/conf-mutation-4 && python3 scripts/check-conf-gate.py`
- **Verbatim output:**
  ```
  check-conf-gate: FAIL — TARGET EXCEEDED [shared-examples] silent_untraced_claims: 1 > target 0
  ```
  Exit code 1.
- **Before:** `git status --porcelain` in the real repo — empty.
- **After:** `git status --porcelain` in the real repo — empty. Scratch copy deleted.

### Round 5 — Criterion 4 / D-03 (prescribed-lead-in rule)

- **Mutation:** In `/tmp/conf-mutation-5/shared/examples/science-engineering.md`, replaced
  the cited `**Recommended approach:** (chains C1 and C2) Install a 400 W panel array...`
  with `**Recommended approach:** no chain — flagged assumption only Install a 400 W panel
  array...` — a prescribed lead-in carrying the caveat marker in place of its citation.
  (An earlier attempt that merely appended the marker *after* the existing citation did
  not fire, because a cited claim never enters `_untraced_claims_text`; the citation had
  to be replaced, not merely followed, for D-03 to see the claim as marked-and-untraced.)
- **Command:** `cd /tmp/conf-mutation-5 && python3 scripts/check-conf-gate.py`
- **Verbatim output:**
  ```
  check-conf-gate: FAIL — D-03 RULE VIOLATION [shared/examples/science-engineering.md]: marked claim opens with a prescribed lead-in: '**Recommended approach:** no chain — flagged assumption only Install a 400 W pan'
  check-conf-gate: FAIL — MARKED-CLAIM RATCHET VIOLATION: 3 > pinned 2
  ```
  Exit code 1. (The ratchet also fired as a side effect of adding a third marked claim to
  the corpus — expected and consistent with the ratchet's own design.)
- **Before:** `git status --porcelain` in the real repo — empty.
- **After:** `git status --porcelain` in the real repo — empty. Scratch copy deleted.

### Round 6 — Criterion 4 / D-04 (section-intro-label dodge)

- **Mutation:** In `/tmp/conf-mutation-6/shared/examples/product-business.md`, moved the
  bold lead-in `**Key insight:**` onto its own line, separated by a blank line from
  `(chain C1) "Competitors do it"...`, so the bold span carries no citation of its own on
  its line and is read as a section-intro label rather than a claim.
- **Command:** `cd /tmp/conf-mutation-6 && python3 scripts/check-conf-gate.py`
- **Verbatim output:**
  ```
  check-conf-gate: FAIL — D-04 CLAIM FLOOR BREACH [product-business]: conclusion_claims 2 < floor 3
  ```
  Exit code 1.
- **Before:** `git status --porcelain` in the real repo — empty.
- **After:** `git status --porcelain` in the real repo — empty. Scratch copy deleted.

### Round 7 — Criterion 5 (generated surface), two halves

**7a — source edited without regenerating the twin:**

- **Mutation:** In `/tmp/conf-mutation-7/shared/examples/estimate-fermi.md`, appended a
  new line `test comment sentinel` without running `sync-content.py --write`.
- **Command:** `cd /tmp/conf-mutation-7 && python3 scripts/sync-content.py --check`
- **Verbatim output:**
  ```
  DRIFT: first-principles/agents/references/examples/estimate-fermi.md
  --- a/first-principles/agents/references/examples/estimate-fermi.md
  +++ b/first-principles/agents/references/examples/estimate-fermi.md
  @@ -269,3 +269,5 @@
   require tightening `cost_per_kg` and the `system_factor` with current procurement and
   engineering quotes, but the cost-competitiveness conclusion itself does not depend on that
   tightening.
  +
  +test comment sentinel

  Run: python3 scripts/sync-content.py --write && git add -u
  ```
  Exit code 1. DUAL-04 fired and named the drifted file exactly.
- **Before:** `git status --porcelain` in the real repo — empty.
- **After:** `git status --porcelain` in the real repo — empty. Scratch copy deleted
  (fresh `/tmp/conf-mutation-7` recreated for 7b below).

**7b — generated twin hand-edited, source left clean:**

- **Mutation:** In a fresh `/tmp/conf-mutation-7/first-principles/agents/references/examples/decompose-irreducibility.md`
  (the generated twin only — `shared/examples/decompose-irreducibility.md` untouched),
  re-wrapped one hop the same way as round 2: removed the leading `→ ` from
  `→ Round-trip efficiency is the product of the three physical-law-anchored conversion
  efficiencies...`.
- **Command:** `cd /tmp/conf-mutation-7 && python3 scripts/check-conf-gate.py`
- **Verbatim output:**
  ```
  check-conf-gate: FAIL — TARGET EXCEEDED [generated-twin] heading_malformed_blocks: 1 > target 0
  ```
  Exit code 1. The failure names `[generated-twin]` specifically, with no
  `[shared-examples]` failure alongside it — proving the gate reads the two surfaces
  independently rather than only ever checking the source.
- **Before:** `git status --porcelain` in the real repo — empty.
- **After:** `git status --porcelain` in the real repo — empty. Scratch copy deleted.

### Round 8 — Criterion 6 (registration), two halves

**8a — battery-side registration removed, CI job left in place:**

- **Mutation:** In `/tmp/conf-mutation-8/scripts/check-firewall-battery.sh`, commented out
  all four lines of the `gate "CONF-GATE" \ ... "python3 scripts/check-conf-gate.py"` call,
  leaving the `check-conf-gate (CONF-GATE)` CI job in `.github/workflows/validation.yml`
  untouched.
- **Command:** `cd /tmp/conf-mutation-8 && python3 scripts/check-registration.py`
- **Verbatim output (tail):**
  ```
  CI job registration (GATE-02 — battery gate -> validation.yml job):
    Battery gates: 22 registered in scripts/check-firewall-battery.sh
    CI-matched: 21; battery-only by design: 1 (QUAL-01)
  check-registration: PASS (discovered 14 skills, agent present, manifest parsed, 14/14 names verified, 21/22 battery gates CI-registered + 1 battery-only by design)
  ```
  Exit code **0** — REG-GUARD PASSED, not RED. **This round's predicted outcome did not
  hold** and is recorded as a FAILED round per the mutation discipline, not reinterpreted
  to force a pass.
  - **Root cause, confirmed by reading `verify_ci_job_registration`:** the CI-job axis
    iterates only over `battery_gate_ids` (the ids `extract_battery_gate_ids` finds in
    `check-firewall-battery.sh`). Removing `CONF-GATE` from that source text removes it
    from the loop entirely — there is no reverse check that a CI job's declared gate id
    must correspond to a battery-registered gate, so the now-orphaned
    `check-conf-gate (CONF-GATE)` job is never inspected and never reported.
  - **Confirmed twice, same result both times:** first by commenting out the full
    four-line call, then again by breaking only the leading `gate "CONF-GATE" \` line
    (a more literal reading of "comment out the ... line", singular) — both produced
    `PASS`, exit 0, with `Battery gates: 22` (CONF-GATE absent from the count).
  - This is REG-GUARD's actual, disclosed scope — `CLAUDE.md`'s own REG-GUARD row states
    only the battery→CI direction ("every gate `scripts/check-firewall-battery.sh`
    registers has a matching `name: <job> (<GATE-ID>)` job") — not a regression this plan
    introduced.
- **Before:** `git status --porcelain` in the real repo — empty.
- **After:** `git status --porcelain` in the real repo — empty. Scratch copy deleted.

**8b — CI-job suffix dropped, battery registration restored:**

- **Mutation:** In a fresh `/tmp/conf-mutation-8b/.github/workflows/validation.yml`,
  changed `name: check-conf-gate (CONF-GATE)` to `name: check-conf-gate` (suffix
  dropped), leaving the battery's `gate "CONF-GATE"` call intact.
- **Command:** `cd /tmp/conf-mutation-8b && python3 scripts/check-registration.py`
- **Verbatim output (tail):**
  ```
  CI job registration (GATE-02 — battery gate -> validation.yml job):
    Battery gates: 23 registered in scripts/check-firewall-battery.sh
    CI-matched: 21; battery-only by design: 1 (QUAL-01)
    Failures:
      battery gate has no CI job: 'CONF-GATE' is registered in scripts/check-firewall-battery.sh but no job in .github/workflows/validation.yml declares it (expected a `name: <job> (<GATE-ID>)` entry)
  ```
  Exit code 1 — REG-GUARD fired on the CI-job axis and named `CONF-GATE` exactly as
  predicted.
- **Before:** `git status --porcelain` in the real repo — empty.
- **After:** `git status --porcelain` in the real repo — empty. Scratch copy deleted.

### Ledger summary

| Round | Criterion | Predicted | Observed | Verdict |
|---|---|---|---|---|
| 1 | Unreadable target | RED, named | RED, named at surface+metric granularity | PASS (as disclosed) |
| 2 | Heading-malformed target | RED, named | RED, named at surface+metric granularity | PASS (as disclosed) |
| 3 | Verdict-cell target | RED, named | RED, named at surface+metric granularity | PASS (as disclosed) |
| 4 | Silent-untraced target | RED, named | RED, named at surface+metric granularity | PASS (as disclosed) |
| 5 | D-03 rule | RED, named | RED, named the exact file and claim text | PASS |
| 6 | D-04 floor | RED, named | RED, named the exact file | PASS |
| 7a | Sync drift | RED, named | RED, named the exact file with a diff | PASS |
| 7b | Twin-surface independence | RED, named `[generated-twin]` only | RED, named `[generated-twin]` only | PASS |
| 8a | Battery-side gate removal | RED, named missing CI job | **PASS, exit 0 — did not fire** | **FAILED (disclosed)** |
| 8b | CI-job suffix removal | RED, named on CI-job axis | RED, named `CONF-GATE` on CI-job axis | PASS |

**9 of 10 sub-rounds** confirmed their predicted defect exactly (rounds 1-4 at the
comparator's own disclosed surface+metric granularity, matching its docstring; rounds
5-7b and 8b at file/claim granularity). **1 of 10 (round 8a)** did not reproduce as
predicted and is recorded as a genuine negative finding with its root cause traced to
source, per the mutation discipline's explicit instruction that a round which cannot be
made to fail is reported in writing rather than dropped.

## Final All-Green Run

Run against the untouched real tree, in this order, immediately after the mutation work:

```
$ python3 scripts/check-conf-gate.py
check-conf-gate: COVERAGE — measured 28 artifacts across shared-examples, generated-twin
check-conf-gate: D-08(a) hop re-wrap on shared/examples/personal-general.md — heading_malformed_blocks 0 -> 1
check-conf-gate: D-08(b) verdict-cell strip on shared/examples/personal-general.md — nonconforming_verdict_cells 0 -> 1
check-conf-gate: D-08(c) citation removal on shared/examples/personal-general.md — silent_untraced_claims 0 -> 1
check-conf-gate: PASS
(exit 0)

$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST PASS — 18 controls run
(exit 0)

$ python3 scripts/check-registration.py
... CI-matched: 22; battery-only by design: 1 (QUAL-01)
check-registration: PASS (discovered 14 skills, agent present, manifest parsed, 14/14 names verified, 22/23 battery gates CI-registered + 1 battery-only by design)
(exit 0)

$ python3 scripts/report-conformance.py --check
report-conformance: PASS — no drift
(exit 0)

$ python3 scripts/sync-content.py --check
(exit 0, no output)

$ bash scripts/check-firewall-battery.sh
... [PASS] CONF-GATE       check-conf-gate.py --self-test + live
FIREWALL: GREEN (25/25)

$ git status --porcelain
(empty)

$ ls -d /tmp/conf-mutation-* 2>/dev/null
(no output — no scratch copy survives)

$ git diff --stat 9a1cde1ead70f607eff4afe96c268b19d4803491 -- scripts/check-quality-harness.py
(empty — byte-identical to the phase-start base)
```

## Issues Encountered

- This worktree's `.git` HEAD was on a stale pre-Phase-18 commit at spawn time (well
  behind the expected base `9a1cde1e`, which already includes plans 18-01 through 18-07
  merged). Corrected via `git reset --hard` to the expected base per the worktree
  branch-check protocol before any plan work began. Phase 18 planning artifacts
  (`18-08-PLAN.md`, `18-CONTEXT.md`, `18-RESEARCH.md`, `18-PATTERNS.md`, prior plans'
  `SUMMARY.md` files, `PROJECT.md`, `STATE.md`, `config.json`) were copied in from the
  main repo checkout before reading, since `git worktree add` only checks out tracked
  files and `.planning/` is gitignored except for `NN-MM-SUMMARY.md` files.
- `bash scripts/check-firewall-battery.sh` initially reported `BLOCKED` (VAL-03's third
  leg needs a pytest-capable interpreter). Resolved by running `uv sync`, which creates
  a local, gitignored `.venv` — an environment step, not a repo change, matching every
  prior plan in this phase.
- Round 5's first attempt (appending the caveat marker after an existing citation) did
  not fire the D-03 rule, because a cited claim never enters `_untraced_claims_text`.
  The mutation was corrected to replace the citation with the marker rather than append
  to it, which then fired correctly — recorded above as part of the round's narrative
  rather than a separate failed sub-round, since the corrected mutation is what the
  plan's round 5 actually describes ("append the marker to a `**Recommended approach:**`
  claim", read as producing a marked-and-uncited claim).

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Phase 18 (exemplar-conformance) is complete: the corpus is closed at zero on all four
  target counts across both gated surfaces (plan 18-06), a standing CONF-GATE comparator
  exists and is registered in the battery and CI (plans 18-07/18-08), and every doc
  surface stating the battery count as a current fact says 25.
- `scripts/check-quality-harness.py` remains untouched and all three sha256 CONTRACT-06
  pins are intact (confirmed via `git diff --stat` against this phase's starting commit).
- **Open finding for a future plan or backlog item:** REG-GUARD's CI-job axis does not
  detect a battery-side gate registration being removed while its CI job is left
  orphaned (round 8a). It only detects the reverse (a CI job losing its `(GATE-ID)`
  suffix while the battery registration survives, round 8b). Closing this would require
  a second check-registration.py axis: for every CI job whose `name:` field declares a
  gate id, that id must also appear in the battery's registered set. Not fixed by this
  plan — it is outside the plan's stated scope (register CONF-GATE, sweep docs, prove
  criteria by mutation) and touching `check-registration.py`'s detection logic was not
  named in the plan's `files_modified`.
- No blockers to closing the phase.

## Self-Check: PASSED

- FOUND: `scripts/check-firewall-battery.sh` carries `gate "CONF-GATE"` (grep confirms exactly 1)
- FOUND: `.github/workflows/validation.yml` carries `name: check-conf-gate (CONF-GATE)` (grep confirms exactly 1)
- FOUND: `CLAUDE.md` carries a CONF-GATE gate-table row and updated tally (25/25)
- FOUND: `docs/ARCHITECTURE.md` carries a CONF-GATE inventory row and `22 + 1 + 2 = 25`
- FOUND: `docs/README.md` states `battery 15/15 → 25/25`
- FOUND: `docs/v8.0-final-closure.md` states `25/25` at both present-tense locations
- FOUND commit: `99bb95d` (Task 1)
- FOUND commit: `fc9b1dd` (Task 2)
- CONFIRMED: `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (25/25)`
- CONFIRMED: `git status --porcelain` empty; no `/tmp/conf-mutation-*` survives
- CONFIRMED: `scripts/check-quality-harness.py` byte-identical to phase-start base

---
*Phase: 18-exemplar-conformance*
*Completed: 2026-09-05*
