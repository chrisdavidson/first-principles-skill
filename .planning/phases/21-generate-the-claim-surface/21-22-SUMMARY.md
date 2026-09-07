---
phase: 21-generate-the-claim-surface
plan: 22
subsystem: claim-surface-verification-harness
tags: [gate-registry, self-test, roster-arm-census, ledger-ratchet, gap-closure-round-3]
dependency_graph:
  requires:
    - "scripts/_gate_registry.py::_hook_roster_arm_clauses (plan 21-21)"
  provides:
    - "scripts/gen-gate-docs.py::_roster_arm_census_sources (live glob over scripts/*.py)"
    - "scripts/gen-gate-docs.py::roster-arm-shape-census-population-complete control"
    - "scripts/gen-gate-docs.py::roster-arm-shape-census-registry-covered control"
    - "docs/gates/CONF-SURFACE.md's roster_arm_census_population derived field"
  affects:
    - "scripts/gen-gate-docs.py"
    - "docs/gates/CONF-SURFACE.md"
    - "CLAUDE.md"
    - "docs/ARCHITECTURE.md"
tech_stack:
  added: []
  patterns:
    - "population-completeness floor: set EQUALITY against a live glob, never subset (19-D-04/CR-03 precedent)"
    - "digit-free hand-written prose that names a generated derived_counts field instead of restating its value"
key_files:
  created: []
  modified:
    - "scripts/gen-gate-docs.py"
    - "docs/gates/CONF-SURFACE.md"
    - "CLAUDE.md"
    - "docs/ARCHITECTURE.md"
decisions: []
metrics:
  duration: "~1 session"
  completed: "2026-09-07"
---

# Phase 21 Plan 22: Widen the Roster-Arm Census to Every scripts/*.py File Summary

One-liner: Closed CR-01's second half by deriving `_roster_arm_census_sources()`'s population
from a live glob over `scripts/*.py` instead of the registry's own `ENTRIES`, which had made
`scripts/_gate_registry.py` structurally unable to be one of its own members, and disposed of
the three parked round-2 findings (WR-10, WR-11, the relative-floor entailment) in the code
that carries them.

## What Was Built

### Task 1 — Widen the census population, correct its claim, publish its reach (COMPLETE, verified)

- `_roster_arm_census_sources()` now derives its population by live glob over every `*.py` file
  directly under `scripts/`, keyed by repo-relative path, instead of calling
  `_expected_harvest_scripts()`. That function itself is unchanged (`git diff` for it is empty)
  and still backs `harvest()`'s own floor.
- `_control_roster_arm_shape_census`'s docstring no longer claims "the live tree carries none of
  the defective roster-arm shapes" — it now states the true, scoped claim ("every `.py` file
  directly under `scripts/` carries none...") plus a DISCLOSED BOUND paragraph (source SHAPE
  within one directory; cannot judge semantic correctness). Its floor was replaced with four
  assertions: population equals a live independent glob (set equality), is a strict superset of
  `_expected_harvest_scripts()`, names `scripts/_gate_registry.py` by presence, and the scan
  returns `[]` over the non-empty population.
- Two new permanent controls registered in both `_CONTROLS` and `_CONTROL_IDS`:
  `roster-arm-shape-census-population-complete` (standalone reproduction of the completeness
  floor, naming the difference set on failure) and `roster-arm-shape-census-registry-covered`
  (positive/negative reproduction of the verifier's exact CR-01 finding against
  `scripts/_gate_registry.py`'s real source, with the negative fixture assembled across
  multiple physical source lines to avoid self-matching this file's own census).
- `describe()`'s `derived_counts` gained `"roster_arm_census_population": len(_roster_arm_census_sources())`
  — the reach is now a generated, drift-gated figure.
- The GAP-A-item-3 comment block and `_control_roster_arm_shape_census_vacuity`'s docstring no
  longer say "every script-backed registry entry" / "22 population members" — both reword
  without a hand-typed count, pointing at `roster_arm_census_population` for the live figure.

### Task 2 — Dispose of WR-10, WR-11 and the relative-floor entailment (COMPLETE, verified)

- **WR-10**: the growth finding in `literal_ledger_ratchet_problems` no longer ends "the ledger
  may shrink but must never grow" — it now names both constants and states the repin obligation
  plan 21-20 added (quoted verbatim below). Only that clause changed; the shrink and digest
  findings are untouched.
- **WR-11**: `literal_ledger_ratchet_problems`'s docstring gained a paragraph recording the
  subsumption — on the real ledger, predicate 3 alone is sufficient to detect any size change,
  but predicates 1/2 are kept for remedy-naming and independent synthetic-triple coverage; the
  redundancy is in the REPORTING, not the coverage.
- **Relative-floor entailment**: `_control_ledger_not_an_unconditional_permit`'s docstring
  gained a paragraph recording that arm (b) is logically entailed by
  `literal_ledger_staleness_problems` passing on the live tree, and why it is kept anyway
  (it fails against a reintroduced catch-all exemption class, which the staleness floor does
  not detect).
- No predicate's behaviour changed — confirmed by `git diff` for `literal_ledger_ratchet_problems`
  showing only the docstring addition and the single growth-message clause (no conditional,
  threshold or comparison operator moved).
- `_SELF_FILE_NONMODULE_DOCSTRING_HITS` did NOT move: live re-measured count is 30, pin is 30,
  both before and after these edits. No re-pin needed.

### Task 3 — Regenerate the claim surface, state the census's reach, prove invariants (COMPLETE, verified)

- Added a digit-free hand-written passage to `docs/gates/CONF-SURFACE.md`'s `## Disclosed
  bounds` region describing the roster-arm census (what it scans, what it proves, its disclosed
  bound, and its CR-01 origin), naming the `roster_arm_census_population` field rather than
  restating its value. Confirmed zero digit characters in the added lines
  (`git diff | grep '^+' | grep -c '[0-9]'` → 0).
- Ran `python3 scripts/gen-gate-docs.py --write` then `--check`. Moves landed exactly as
  predicted: `control_ids`/`control_count` 69 → 71; `derived_counts` 18 → 19 entries with the
  new `roster_arm_census_population` line; the same three figures in the CONF-SURFACE cells of
  `CLAUDE.md` and `docs/ARCHITECTURE.md`. Only `CLAUDE.md`, `docs/ARCHITECTURE.md` and
  `docs/gates/CONF-SURFACE.md` actually changed on disk (`git status --short` after `--write`);
  every other one of the 34 "wrote" targets was byte-identical to what was already committed.
- Ran the full gate set: `--self-test`, `--check`, `check-registration.py`,
  `report-conformance.py --self-test` and `--check`, both pre-commit hooks, and the full battery.
  All pass; results below.

## Evidence

### Before/after `SELF-TEST PASS` lines

- Before (start of this plan, after 21-21): `gen-gate-docs: SELF-TEST PASS — 69 controls run`
- After Task 1: `71` controls registered (verified in-process:
  `len(_CONTROLS) == len(_CONTROL_IDS) == 71`); full `--self-test` could not print its PASS line
  until Task 3's regeneration cleared the expected drift (see below).
- After Task 3: `gen-gate-docs: SELF-TEST PASS — 71 controls run`. Exit 0.

### `--self-test` failures between Task 1/2 and Task 3 (expected, per the plan's own ordering note)

After Task 1 and Task 2, `--self-test` reported exactly two failures, both drift from the
not-yet-regenerated `CLAUDE.md`/`docs/ARCHITECTURE.md` (`[check-dispatch-wired]`,
`[check-reports-full-drift-count]`) — no other control failed. Task 3's `--write` cleared both.

### Seven previously-excluded relpaths — confirmed now in the population

`_battery_core.py`, `_gate_registry.py`, `_skill_io.py`, `check-body-budget.py`,
`check-links_anchors_test.py`, `check-routing.py`, `trace-tests-usage.py` — all seven confirmed
present in `_roster_arm_census_sources()`'s keys in-process after Task 1's edit. Population size
29, matching `ls scripts/*.py | wc -l` = 29 by equality (not similarity).

### Census findings over the widened population

`roster_arm_shape_census_problems()` returns `[]` over the widened 29-file population, both
immediately after Task 1 (before Task 2's unrelated edits) and after the full plan.

### Committed `roster_arm_census_population` fence line vs. shell count

`docs/gates/CONF-SURFACE.md` Facts fence: `` `roster_arm_census_population`=29 `` —
`ls scripts/*.py | wc -l` → `29`. Equal.

### Corrected docstring (verbatim, `_roster_arm_census_sources`)

```
"""Build the live population for `roster_arm_shape_census_problems()`'s
default `sources=None` path: every `.py` file directly under
`scripts/`, read as UTF-8 and keyed by repo-relative path -- derived by
a live glob, not from `_expected_harvest_scripts()`. The roster-arm
rule governs any Python source under `scripts/`, not only the
`--describe`-backed registry entries that function names; deriving the
population from `ENTRIES` made the module that DEFINES those entries
(`scripts/_gate_registry.py`) structurally unable to be one of its own
members -- the CR-01 defect `21-VERIFICATION.md` round 2 recorded.
`_expected_harvest_scripts()` itself is unchanged and still backs
`harvest()`'s own floor; this function simply stopped calling it.
Exposed separately (not inlined into the scan function) so the
anti-vacuity floor can assert the read count independently of the scan
logic itself."""
```

### Reworded growth message (verbatim, WR-10)

```
"deferred-literal-ledger ratchet: live ledger size "
f"{live_size} exceeds the pinned maximum {max_size} -- the "
"ledger must never grow; a shrink is legal only when both "
"_DEFERRED_LEDGER_MAX and _DEFERRED_LEDGER_KEYS_DIGEST are "
"re-pinned to the live values in this same commit"
```

Falsification-6 check (in-process): a synthetic ledger one entry larger than its pin produces
exactly one finding naming both `_DEFERRED_LEDGER_MAX` and `_DEFERRED_LEDGER_KEYS_DIGEST`:
```
deferred-literal-ledger ratchet: live ledger size 2 exceeds the pinned maximum 1 -- the ledger
must never grow; a shrink is legal only when both _DEFERRED_LEDGER_MAX and
_DEFERRED_LEDGER_KEYS_DIGEST are re-pinned to the live values in this same commit
```

### Two added docstring passages (verbatim)

**WR-11 subsumption** (`literal_ledger_ratchet_problems`):
```
WR-11 (21-VERIFICATION.md round 2): on the REAL ledger, any size
change is necessarily also a key-set change, so a single edit fires
predicate 1-or-2 AND predicate 3 together -- predicate 3 alone is
SUFFICIENT to detect that edit. Predicates 1 and 2 are retained anyway,
for two reasons the digest cannot supply: they name the specific
remedy (which pin to lower, and to what value), and they are
independently exercised by the synthetic ledger/pin/digest triples the
permanent controls drive, where a caller supplies a consistent digest
and only the size differs. The redundancy this creates on the real
ledger is in the REPORTING, not in the coverage -- a future reader
deleting a "redundant" predicate would be giving up the remedy-naming
and the independent synthetic-triple coverage, not removing dead code.
```

**Relative-floor entailment** (`_control_ledger_not_an_unconditional_permit`):
```
Relative-floor entailment (21-VERIFICATION.md round 2): in the
PASSING state, arm (b) is logically entailed by
`literal_ledger_staleness_problems` already passing on the live tree
-- every ledger key matches at least one live hit, so emptying the
ledger necessarily produces at least `ledger_size` findings, and arm
(b) is not independent evidence of load-bearingness while the tree is
green. It is kept anyway because it fails against the threat it was
designed for -- a reintroduced catch-all exemption class collapsing
the finding count -- which the staleness floor does not detect; a
reader should not mistake arm (b) for independent evidence in the
passing state.
```

### Pre/post `literal_scan_non_exempt` and ledger size

Unchanged throughout the whole plan: `literal_scan_non_exempt` = 0 (before Task 1, after Task 2,
and after Task 3's regeneration); `len(_DEFERRED_LITERAL_HITS)` = 135 throughout. Net new ledger
entries = 0.

### `_SELF_FILE_NONMODULE_DOCSTRING_HITS`

Did not move: live re-measured count 30 == pinned 30, checked immediately after Task 2's
docstring edits. No re-pin performed or needed.

### Grep-based acceptance criteria (all run against the final tree)

- `/usr/bin/grep -c 'the live tree carries none' scripts/gen-gate-docs.py` → `0`
- `/usr/bin/grep -rc 'may shrink but must never grow' scripts/` → `0` (no file matches)
- `/usr/bin/grep -c '22 population members' scripts/gen-gate-docs.py` → `0`
- `git diff` for `_expected_harvest_scripts` → empty (function unchanged)
- New hand-written passage on `docs/gates/CONF-SURFACE.md`: `git diff | grep '^+' | grep -c '[0-9]'` → `0`

### Regenerated surfaces

`CLAUDE.md`'s and `docs/ARCHITECTURE.md`'s CONF-SURFACE cells both read: `derived_counts=19
entries`, `control_ids=71`, `control_count=71`. `python3 scripts/gen-gate-docs.py --check`
exits 0, zero `DRIFT:` lines, prints `harvested 22/22 expected script-backed entries` — the
harvest population (`_expected_harvest_scripts()`, 22 files) stayed distinct from the census
population (live glob, 29 files).

### Falsification 7 (published reach is drift-gated, not decorative)

On an `rsync -a --exclude .git` scratch copy: `--check` exited 0 first. Then hand-edited the
`roster_arm_census_population` value inside the Facts fence from `29` to `99`; `--check` exited
1 with `DRIFT: docs/gates/CONF-SURFACE.md`. Real tree `git status --porcelain` confirmed
unaffected (only the plan's own intended files staged) before and after.

### Seven falsification arms — exact exit codes and failure text

All seven driven against `rsync -a --exclude .git` scratch copies; real tree `git status
--porcelain` confirmed showing only this plan's own staged/committed edits before and after
every single falsification (never contaminated by a scratch mutation).

**1 — the CR-01 arm.** Reintroduced the clause-marker shape into `scripts/_gate_registry.py`.
`--self-test` exited 1, naming `roster-arm-shape-census` AND
`roster-arm-shape-census-registry-covered`:
```
gen-gate-docs: SELF-TEST FAIL [roster-arm-shape-census] — ['scripts/_gate_registry.py:1701: bare clause-marker membership test against a whole message: \'"missing=" in problems\'']
gen-gate-docs: SELF-TEST FAIL [roster-arm-shape-census-registry-covered] — ['scripts/_gate_registry.py:1701: bare clause-marker membership test against a whole message: \'"missing=" in problems\'']
```

**2 — the whole excluded class.** Reintroduced the shape into `scripts/_battery_core.py`.
`--self-test` exited 1:
```
gen-gate-docs: SELF-TEST FAIL [roster-arm-shape-census] — ['scripts/_battery_core.py:3901: bare clause-marker membership test against a whole message: \'"extra=" in problems\'']
```

**3 — re-narrowing is visible.** Reverted `_roster_arm_census_sources()` to
`_expected_harvest_scripts()`. `--self-test` exited 1, naming
`roster-arm-shape-census-population-complete` and all seven missing relpaths:
```
gen-gate-docs: SELF-TEST FAIL [roster-arm-shape-census-population-complete] — population != live glob of scripts/*.py -- missing=['scripts/_battery_core.py', 'scripts/_gate_registry.py', 'scripts/_skill_io.py', 'scripts/check-body-budget.py', 'scripts/check-links_anchors_test.py', 'scripts/check-routing.py', 'scripts/trace-tests-usage.py'] extra=[]
```

**4 — population floor is not vacuous.** Mutated the census to skip underscore-prefixed
basenames (population 29 → 26, dropping the three `_`-prefixed files). `--self-test` exited 1,
naming `roster-arm-shape-census-population-complete` and the three dropped files:
```
gen-gate-docs: SELF-TEST FAIL [roster-arm-shape-census-population-complete] — population != live glob of scripts/*.py -- missing=['scripts/_battery_core.py', 'scripts/_gate_registry.py', 'scripts/_skill_io.py'] extra=[]
```

**5 — registry-covered control is not vacuous.** In-process: real `scripts/_gate_registry.py`
text plus one appended synthetic defective line (assembled across two physical source lines to
avoid self-match) yields exactly one finding naming the file:
```
['scripts/_gate_registry.py:1698: bare clause-marker membership test against a whole message: \'"extra=" in problems\'']
```

**6 — reworded growth message still fires, names both constants.** See "Reworded growth
message" above — one finding, both constants named; un-repinned-shrink and digest-mismatch
findings confirmed byte-identical to pre-edit text (untouched by this plan).

**7 — published reach is drift-gated.** See "Falsification 7" above — exit 0 then exit 1 with
a named `DRIFT:` line.

### Full gate set (real tree, after Task 3's `--write`)

- `python3 scripts/gen-gate-docs.py --self-test` — exit 0, `SELF-TEST PASS — 71 controls run`
- `python3 scripts/gen-gate-docs.py --check` — exit 0, zero `DRIFT:` lines, `harvested 22/22`
- `python3 scripts/check-registration.py` — exit 0, `PASS (discovered 14 skills, agent present,
  manifest parsed, 14/14 names verified, 23/24 battery gates CI-registered + 1 battery-only by
  design)`
- `python3 scripts/report-conformance.py --self-test` — `SELF-TEST PASS — 101 controls run`, exit 0
- `python3 scripts/report-conformance.py --check` — `PASS — no drift`, exit 0
- `sh .githooks/pre-commit` — exit 0
- `sh scripts/git-hooks/pre-commit` — exit 0
- `bash scripts/check-firewall-battery.sh` — `FIREWALL: GREEN (26/26)`
- `git diff --stat scripts/check-quality-harness.py` — empty; all three CONTRACT-06 sha256 pins
  byte-unchanged (file carries no hunk in this plan's diff)
- Battery total unchanged at 26; new battery gates = 0; new CI jobs = 0; new REG-GUARD
  exemptions = 0; detector-behaviour hunks in the diff = 0 (confirmed via the `git diff` hunk
  for `literal_ledger_ratchet_problems` showing only string-literal changes)

### No exemption class, ledger entry, detector threshold or CONTRACT-06 pin touched

Explicit statement: this plan added zero new `LITERAL_EXEMPTION_CLASSES` members, zero new
`_DEFERRED_LITERAL_HITS` entries (135 before and after), moved zero detector thresholds (only
docstrings and one finding-message string clause changed in `literal_ledger_ratchet_problems`,
confirmed by the isolated diff hunk), and left all three `scripts/check-quality-harness.py`
CONTRACT-06 sha256 pins byte-unchanged (the file carries no hunk at all in this plan's diff).

Commits:
- `2dec1af` — `feat(21-22): widen roster-arm census to every scripts/*.py file, closing CR-01`
- `366e4e5` — `fix(21-22): dispose of WR-10, WR-11 and the relative-floor entailment findings`
- `c682e7b` — `docs(21-22): regenerate the claim surface with the widened roster-arm census`

## Deviations from Plan

None — plan executed exactly as written. All three tasks landed as separate commits (split
retroactively from the combined edit set by reverting and reapplying each task's edits in
isolation, so each commit's diff is scoped to exactly its own task) rather than the single
combined working state used during verification; verification (falsifications, gate runs) was
re-run against the final split-commit tree to confirm nothing was lost in the split.

### Not Applied — planning-record artifacts outside this worktree

Per the orchestrator's explicit instruction for this parallel wave, `.planning/STATE.md` and
`.planning/ROADMAP.md` were not touched (the orchestrator owns those writes centrally after all
worktree agents complete). Both files are also gitignored and absent from this isolated
worktree's checkout, matching plan 21-21's SUMMARY's prior finding — no drafted replacement
content is offered here since this plan's own frontmatter and objective do not direct any edit
to those files (unlike 21-21's Task 2).

## Self-Check

- `[ -f scripts/gen-gate-docs.py ]` → FOUND
- `[ -f docs/gates/CONF-SURFACE.md ]` → FOUND
- `git log --oneline --all | grep -q 2dec1af` → FOUND
- `git log --oneline --all | grep -q 366e4e5` → FOUND
- `git log --oneline --all | grep -q c682e7b` → FOUND

## Self-Check: PASSED

## Verification Summary

- `python3 scripts/gen-gate-docs.py --self-test` — exit 0, `SELF-TEST PASS — 71 controls run`
  (was 69). Verified by running the command.
- `python3 scripts/gen-gate-docs.py --check` — exit 0, zero `DRIFT:` lines, `harvested 22/22`.
- In-process: `len(_roster_arm_census_sources())` == `ls scripts/*.py | wc -l` == 29;
  `roster_arm_shape_census_problems()` returns `[]`.
- `/usr/bin/grep -c 'the live tree carries none' scripts/gen-gate-docs.py` → 0;
  `/usr/bin/grep -rc 'may shrink but must never grow' scripts/` → 0 for every file;
  `/usr/bin/grep -c '22 population members' scripts/gen-gate-docs.py` → 0.
- `literal_scan_non_exempt` = 0, `len(_DEFERRED_LITERAL_HITS)` = 135, unchanged throughout.
- `python3 scripts/check-registration.py` — exit 0, PASS.
- `python3 scripts/report-conformance.py --self-test` — `PASS — 101 controls run`; `--check` —
  `PASS — no drift`.
- `sh .githooks/pre-commit` and `sh scripts/git-hooks/pre-commit` — both exit 0.
- `bash scripts/check-firewall-battery.sh` — `FIREWALL: GREEN (26/26)`.
- All three CONTRACT-06 sha256 pins byte-unchanged; `check-quality-harness.py` carries no hunk.
- Seven falsification arms, each with exact exit code and failure text recorded above; real
  tree `git status --porcelain` confirmed clean of scratch-copy contamination before and after
  each.
