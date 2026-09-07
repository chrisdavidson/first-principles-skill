---
phase: 21-generate-the-claim-surface
plan: 23
subsystem: claim-surface-verification-harness
tags: [literal-scan, py-population, conf-13, gap-closure-round-3, gate-registry]
dependency_graph:
  requires:
    - "scripts/_gate_registry.py::_hook_roster_arm_clauses (plan 21-21)"
    - "scripts/gen-gate-docs.py::_roster_arm_census_sources (plan 21-22, live glob pattern)"
  provides:
    - "scripts/_gate_registry.py::HAND_TRANSCRIPTION_FINDING_SHARE"
    - "scripts/gen-gate-docs.py::_py_docstring_scan_scripts (live glob over scripts/*.py)"
    - "scripts/gen-gate-docs.py::literal-scan-py-population-complete control"
    - "scripts/gen-gate-docs.py::literal-scan-covers-registry-module control"
    - "docs/gates/CONF-SURFACE.md's widened .py-population disclosed bound"
  affects:
    - "scripts/_gate_registry.py"
    - "scripts/gen-gate-docs.py"
    - "docs/gates/CONF-SURFACE.md"
    - "CLAUDE.md"
    - "docs/ARCHITECTURE.md"
tech_stack:
  added: []
  patterns:
    - "population-completeness floor: set EQUALITY against a live glob, never subset (19-D-04/CR-03/plan-21-22 precedent, ported again)"
    - "phase-justification figures relocated to named module constants rather than deleted or hidden in comments"
decisions: []
metrics:
  duration: "~1 session"
  completed: "2026-09-07"
---

# Phase 21 Plan 23: Widen CONF-13's Literal-Scan Population to Every scripts/*.py Summary

One-liner: Closed the CONF-13 twin of CR-01 -- `_py_docstring_scan_scripts()` derived its
population from the same registry-derived set that caused CR-01, making
`scripts/_gate_registry.py` and six other `.py` files structurally invisible to CONF-13's
standing scanner -- by fixing the four literals the widening exposes in prose first, then
widening the population to a live glob, then regenerating the claim surface.

## What Was Built

### Task 1 -- Make the registry's module docstring conform, keeping the justification figure in the tree (COMPLETE, verified)

Applied all four replacements from the plan's `<interfaces>` to `scripts/_gate_registry.py`'s
module docstring, and added a new module-level constant, `HAND_TRANSCRIPTION_FINDING_SHARE:
str = "41%"`, immediately below `ARCHITECTURE_PATH`, with a provenance comment. Updated
`scripts/gen-gate-docs.py`'s own module docstring to name the constant instead of the
now-outdated "see the registry docstring" pointer.

**The four literals, quoted before and after:**

1. `Gate registry (Phase 21, D-01): one entry per documented gate row.`
   -> `Gate registry (Phase 21, D-01): a single entry per documented gate row.`
2. `Hand-transcribed gate documentation produced 41% of all review findings across`
   -> `Hand-transcribed gate documentation produced the measured share of all review
      findings across` (figure moved to `HAND_TRANSCRIPTION_FINDING_SHARE`)
3. `is the fix: it holds \`len(ENTRIES)\` entries, one per row`
   -> `is the fix: it holds \`len(ENTRIES)\` entries -- a single entry per row`
4. `is registered as one of \`ENTRIES\` in its own right`
   -> `is registered as an \`ENTRIES\` member in its own right`

**The new constant, verbatim:**

```python
# Measured across Phases 13-15 (this phase's own milestone justification):
# the share of all review findings in those phases directly caused by
# hand-transcribed gate documentation drifting out of sync with the scripts
# it described. A frozen historical measurement, not a derived count -- it
# does not move as the code in this file changes, and re-measuring it is out
# of scope for this module. Kept here, in a named constant rather than
# inline prose, so CONF-13's standing literal scanner (which reads this
# module's own docstring) sees no hand-maintained count claim while the
# figure itself stays in the tracked tree.
HAND_TRANSCRIPTION_FINDING_SHARE: str = "41%"
```

**Verified post-fix hit list for the registry docstring, in-process** (`ast.get_docstring` +
`_scan_text_for_literal_hits`): exactly 1 hit, `'three CONTRACT-06 sha256 pins'`, exemption
`sha256-digest`. Non-exempt hits = 0 (was 4). `gen-gate-docs.py`'s own docstring hit set
confirmed byte-identical before and after the pointer edit (`'three CONTRACT-06 sha256
pins'`, exempt `sha256-digest`, same text and exemption, line number shifted by the inserted
wrap only).

**The `sha256-digest` hit the plan-checker cited was confirmed exempt, not one of the four
fixed:** measured in-process over the widened (pre-fix) population, the registry docstring
carried 5 hits total -- the 4 non-exempt findings this task fixed, plus `'three CONTRACT-06
sha256 pins'` at exemption `sha256-digest`, unaffected by any of this task's edits. Stated
explicitly per the plan's `<output>` instruction.

`/usr/bin/grep -rn '41%' --include=*.py --include=*.md scripts/ docs/ CLAUDE.md` -> exactly
one line, `scripts/_gate_registry.py:59:HAND_TRANSCRIPTION_FINDING_SHARE: str = "41%"`. No
`#`-comment was used as the destination for any of the four literals -- the figure moved into
a typed constant; the comment above it is provenance narrative, not the figure's hiding place.

Commit: `ef1d9ae` -- `fix(21-23): make the registry's module docstring conform to CONF-13`

### Task 2 -- Widen the literal-scan .py population, floor it against re-narrowing (COMPLETE, verified)

Rewrote `_py_docstring_scan_scripts()` to derive its population by live glob over
`scripts/*.py` (modelled on `_roster_arm_census_sources()`, plan 21-22's identical shape over
a different population), returning sorted repo-relative paths. `_expected_harvest_scripts()`
itself is untouched (confirmed by isolated `git diff`) and still backs `harvest()`'s own
floor.

Added two permanent controls, registered in both `_CONTROLS` and `_CONTROL_IDS`:

- `literal-scan-py-population-complete`: set-EQUALITY floor between the `.py` members of
  `LITERAL_SCAN_SURFACES` and a live independent glob of `scripts/*.py`, plus a
  strict-superset check against `_expected_harvest_scripts()` and a named-presence assertion
  for `scripts/_gate_registry.py`.
- `literal-scan-covers-registry-module`: positive half proves the real registry docstring is
  clean (drives the real `literal_scan_problems`/`LiteralScanRead` path, not a hand-simulated
  equivalent); negative half proves a reintroduced literal is caught and named. The synthetic
  negative fixture (`"This fixture module docstring carries seven items for the test."`) is a
  local variable in the control function's body, not a docstring, so it carries no self-match
  risk regardless of splitting -- confirmed by direct measurement before use.

### Task 3 -- Regenerate, state the widened scope, prove invariants (COMPLETE, verified)

Added a purely-additive, digit-free paragraph to `docs/gates/CONF-SURFACE.md`'s disclosed
bound (4), stating the population is now every `.py` file directly under `scripts/`, its
origin (previously `ENTRIES`-derived, which made `scripts/_gate_registry.py` unable to be
scanned), and that the surviving docstring-only bound is unaffected. The existing hand-written
narrative is otherwise byte-unchanged (`git diff` shows only the new block as an insertion,
zero deletions in that region). Ran `--write` then `--check`, then the full gate set.

Commit: `4595878` -- `docs(21-23): regenerate the claim surface with the widened CONF-13
population`

## Evidence

### Before/after `SELF-TEST PASS` lines

- `_gate_registry.py --self-test`: `21 controls run` before and after Task 1 (unchanged --
  this task did not touch `_CONTROLS`/`_CONTROL_IDS`).
- `gen-gate-docs.py --self-test`: `71 controls run` (pre-plan, matching 21-22's committed
  state) -> `73 controls run` (post Task 2/3, +2 for the new controls).
- Between Task 2 and Task 3's `--write`, `--self-test` reported exactly two expected failures
  (`[check-dispatch-wired]`, `[check-reports-full-drift-count]`), both drift from the
  not-yet-regenerated `CLAUDE.md` -- no other control failed. Task 3's `--write` cleared both.

### Re-measured figures (widened population, before Task 1's prose fix)

In-process, matching the plan's `<interfaces>` measurements exactly: `read_relpaths` 60 -> 67,
`hits` 160 -> 165, `non-exempt` 0 -> 4, all four non-exempt findings and the one exempt
`sha256-digest` hit located precisely where the plan predicted.

### Final regenerated figures (after Task 1's fix + Task 2's widening + Task 3's `--write`)

| Field | Before this plan | After | Predicted |
|---|---|---|---|
| `registered_surfaces` / `checked_files` | 30 / 60 | 37 / 67 | 37 / 67 (match) |
| `literal_scan_surfaces` / `literal_scan_read_files` | 30 / 60 | 37 / 67 | 37 / 67 (match) |
| `literal_scan_hits` | 160 | 161 | 161 (match) |
| `literal_scan_exempt_sha256-digest` | 1 | 2 | 2 (match) |
| `literal_scan_non_exempt` | 0 | 0 | 0 (match) |
| `control_ids` / `control_count` | 71 | 73 | 73 (match, +2 from 21-22's figure) |
| `literal_scan_nonmodule_docstring_surfaces` | 19 | 23 | 23 (match) |
| `literal_scan_nonmodule_docstring_hits` | 353 | **383** | 378 (**diverges, +5**) |

**One unpredicted move, explained:** `literal_scan_nonmodule_docstring_hits` landed at 383,
not the plan's predicted 378 -- a divergence of 5 measured hits. Per the orchestrator's
prior-wave note, the plan's own interface figures were measured before 21-22 fully landed on
this exact tree state; re-measuring rather than trusting the stale figure (as instructed) is
what surfaced this. It is **not gated**: `_nonmodule_docstring_hits()` is a published
measurement only (never fed into `literal_scan_non_exempt` or `--check`), and the one file
that DOES carry an enforced ratchet on this measurement --
`scripts/gen-gate-docs.py`'s own share, via `_SELF_FILE_NONMODULE_DOCSTRING_HITS` -- was
re-measured directly and stayed at exactly 30, matching the pin, both before and after Task 2's
edits. No re-pin was needed or performed.

`roster_arm_census_population` stayed at 29 throughout this plan (untouched by this plan's
edits, confirmed unchanged in the regenerated Facts fence).

### Falsification arms (five total across the plan, each run on an `rsync -a --exclude .git`
scratch copy; real tree `git status --porcelain` confirmed showing only this plan's own
staged/committed edits before and after every single falsification)

**1 -- the CONF-13 twin arm (Task 2).** Injected a synthetic hand-maintained count literal
(`"This fixture carries nine items for the test."`) into a scratch copy's
`scripts/_gate_registry.py` module docstring.
`--check` exited **1**:
```
scripts/_gate_registry.py#__doc__:31: hand-maintained count literal 'fixture carries nine' (no exemption class matches)
harvested 22/22 expected script-backed entries (22 total)
literal-scan: 1 non-exempt hit(s) found
```
`--self-test` exited **1**, naming `literal-scan-covers-registry-module`:
```
gen-gate-docs: SELF-TEST FAIL [literal-scan-covers-registry-module] — (LiteralHit(relpath='scripts/_gate_registry.py#__doc__', line=22, text='three CONTRACT-06 sha256 pins'), LiteralHit(relpath='scripts/_gate_registry.py#__doc__', line=31, text='fixture carries nine'))
```

**2 -- the whole excluded class, not one file (Task 2).** Same injection into a fresh scratch
copy's `scripts/_battery_core.py` module docstring instead. `--check` exited **1**:
```
scripts/_battery_core.py#__doc__:3: hand-maintained count literal 'fixture carries nine' (no exemption class matches)
harvested 22/22 expected script-backed entries (22 total)
literal-scan: 1 non-exempt hit(s) found
```

**3 -- re-narrowing is visible (Task 2).** Reverted `_py_docstring_scan_scripts()` to
`_expected_harvest_scripts()` on a fresh scratch copy. `--self-test` exited **1**, naming
`literal-scan-py-population-complete` and all seven missing relpaths:
```
gen-gate-docs: SELF-TEST FAIL [literal-scan-py-population-complete] — population != live glob of scripts/*.py -- missing=['scripts/_battery_core.py', 'scripts/_gate_registry.py', 'scripts/_skill_io.py', 'scripts/check-body-budget.py', 'scripts/check-links_anchors_test.py', 'scripts/check-routing.py', 'scripts/trace-tests-usage.py'] extra=[]
```
(Two additional pre-existing `[check-dispatch-wired]`/`[check-reports-full-drift-count]`
DRIFT failures also fired on this scratch copy, from the not-yet-regenerated `CLAUDE.md` --
expected and unrelated to this falsification.)

**4 -- registry-covered control is not vacuous (Task 2).** Direct in-process invocation of
`_control_literal_scan_covers_registry_module()`: passes on the real tree (positive half:
`[]` over the real docstring). Negative half confirmed separately: `_literal_hits_outside_generated`
against the synthetic fixture text returns exactly 1 hit (`'seven items'`), and the control's
own assertion (`len(negative) == 1` naming `scripts/_gate_registry.py`) is what falsification 1
above independently exercised end to end through the real `--self-test` path.

**5 -- the widened scope is drift-gated, not decorative (Task 3).** On a fresh scratch copy
taken after Task 3's `--write`: `--check` exited **0** first. Then hand-edited the committed
`literal_scan_read_files` value inside the CONF-SURFACE Facts fence from `67` to `99`.
`--check` then exited **1**:
```
DRIFT: docs/gates/CONF-SURFACE.md
```

### Ledger and exemption invariants (measured before Task 1, after Task 2, after Task 3 -- all identical)

- `len(_DEFERRED_LITERAL_HITS)`: 135 (unchanged throughout)
- `_DEFERRED_LEDGER_MAX`: 135 (unchanged)
- `_DEFERRED_LEDGER_KEYS_DIGEST`: `sha256:0a249f6de8c4b520d3e76590cfc6d1b8296497c5cbfef05bd7533d64a0f068bc` (unchanged)
- `LITERAL_EXEMPTION_CLASSES` membership and names: `version-stamp-count`,
  `headline-provenance-delta`, `plan-number-identifier`, `retired-body-budget`,
  `maxturns-60-value`, `sha256-digest`, `commonmark-heading-depth`, `deferred-literal-ledger`
  (unchanged, same 8 classes throughout)
- `literal_ledger_staleness_problems(run_literal_scan())` -> `[]` after Task 3's widening (no
  ledger key went stale)
- All three `scripts/check-quality-harness.py` CONTRACT-06 sha256 pins byte-unchanged --
  `git diff --stat scripts/check-quality-harness.py` is empty (file carries no hunk anywhere in
  this plan's diff)

### The seven newly-covered relpaths -- confirmed present in `checked_files`

`_battery_core.py`, `_gate_registry.py`, `_skill_io.py`, `check-body-budget.py`,
`check-links_anchors_test.py`, `check-routing.py`, `trace-tests-usage.py` -- all seven
individually confirmed present (via grep) in `docs/gates/CONF-SURFACE.md`'s committed
`checked_files` list after Task 3's regeneration.

### Full gate set (real tree, after Task 3's `--write`)

- `python3 scripts/gen-gate-docs.py --self-test` -- exit 0, `SELF-TEST PASS — 73 controls run`
- `python3 scripts/gen-gate-docs.py --check` -- exit 0, zero `DRIFT:` lines, `harvested 22/22`
- `python3 scripts/_gate_registry.py --self-test` -- exit 0, `SELF-TEST PASS — 21 controls run`
- `python3 scripts/check-registration.py` -- exit 0, `PASS (discovered 14 skills, agent
  present, manifest parsed, 14/14 names verified, 23/24 battery gates CI-registered + 1
  battery-only by design)`
- `python3 scripts/report-conformance.py --self-test` -- `SELF-TEST PASS — 101 controls run`,
  exit 0
- `python3 scripts/report-conformance.py --check` -- `PASS — no drift`, exit 0
- `sh .githooks/pre-commit` -- exit 0
- `sh scripts/git-hooks/pre-commit` -- exit 0
- `bash scripts/check-firewall-battery.sh` -- `FIREWALL: GREEN (26/26)` -- an invariance check
  only, matching the plan's own framing (the battery was GREEN 26/26 throughout every
  defective state this phase found, including this one)

Battery total unchanged at 26; new battery gates = 0; new CI jobs = 0; new REG-GUARD
exemptions = 0.

## Assumption Drift (advisory)

**Planned:** the orchestrator's prior-wave note flagged that this plan's own interface figures
("read files 60 -> 67, hits 160 -> 165") were measured before 21-22 fully landed and might be
stale, directing re-measurement rather than trust.

**Actual:** every figure the plan explicitly staked a claim on (`read_relpaths`, `hits`,
`non_exempt`, the four fixed literals' text, the one exempt `sha256-digest` hit,
`control_ids`/`control_count`, `literal_scan_nonmodule_docstring_surfaces`) matched the plan's
predictions exactly once re-measured against the real, post-21-22 tree. The one figure that
diverged, `literal_scan_nonmodule_docstring_hits` (383 measured vs. 378 predicted), is a
published-only measurement with no gate depending on its exact value, and the one file with an
enforced ratchet on this measurement (`scripts/gen-gate-docs.py`'s own share, pin 30) was
independently re-measured and stayed exactly at its pin.

**Why:** the prior wave's own edits (21-21, 21-22) touched `scripts/gen-gate-docs.py` and
`scripts/_gate_registry.py`'s docstrings/comments in ways this plan's own interface-figure
measurement (taken during planning, before 21-22 fully settled) could not have accounted for
precisely -- consistent with the orchestrator's warning. Recorded here per the advisory
protocol rather than silently accepted.

## Deviations from Plan

**1. [Not a Rule 1-4 deviation -- an executor decision about MECHANICS, per the
`checkpoint:*` boundary] Rewrote `docs/gates/CONF-SURFACE.md`'s disclosed-bound (4) edit as a
purely-additive insertion rather than an in-place rewrite of the existing paragraph.**
- **Found during:** Task 3, drafting the disclosed-bound (4) update.
- **Issue:** The plan's acceptance criteria require the edited passage to contain literally
  zero digit characters (`grep -n '[0-9]'` over the added/changed lines returns nothing). My
  first draft rewrote the existing paragraph in place, which necessarily re-emitted its
  pre-existing digit-bearing identifiers (`CR-01`, `plan 21-20 Task 3`, `bound (6)`) as newly
  "added" diff lines, since any line I touch at all is rendered as `+` even where a substring
  is byte-identical to the original.
- **Fix:** Left the existing bound (4) paragraph completely untouched (byte-identical, so it
  never appears as a `+`/`-` line in the diff) and added a new, separate, digit-free paragraph
  immediately after it, following the same house style 21-22 used for its own added
  "roster-arm shape census" paragraph (an unnumbered bold lead-in, references to "this phase's
  round-two verification" rather than "CR-01" or a plan number). Verified with
  `git diff | grep '^+' | grep -c '[0-9]'` -> 0, and confirmed the standing scanner itself adds
  zero new hits from the addition (three pre-existing hits on unrelated, untouched lines are
  the only hits in the whole file, all already ledgered).
- **Files modified:** `docs/gates/CONF-SURFACE.md`.
- **Commit:** `4595878` (Task 3's single commit; the false-start rewrite was corrected before
  staging, so the committed diff only ever contained the clean, purely-additive version).

### Auto-fixed Issues

None beyond the mechanics deviation above -- no Rule 1/2/3 auto-fixes were needed; the plan's
own drafted replacement text (verified against the live detector during planning) matched the
live tree's behavior exactly once applied.

## Self-Check

- `[ -f scripts/_gate_registry.py ]` -> FOUND
- `[ -f scripts/gen-gate-docs.py ]` -> FOUND
- `[ -f docs/gates/CONF-SURFACE.md ]` -> FOUND
- `git log --oneline --all | grep -q ef1d9ae` -> FOUND
- `git log --oneline --all | grep -q a55e1be` -> FOUND
- `git log --oneline --all | grep -q 4595878` -> FOUND

## Self-Check: PASSED

## Verification Summary

- In-process: the `.py` members of `LITERAL_SCAN_SURFACES` equal `ls scripts/*.py` by set
  equality (29 == 29); `run_literal_scan()` reads 67 files, finds 161 hits, and
  `literal_scan_problems` returns `[]`. Verified by running the code, not by inspection.
- `scripts/_gate_registry.py`'s module docstring scores exactly 1 hit, exempt under
  `sha256-digest`.
- `python3 scripts/gen-gate-docs.py --self-test` -- exit 0, `SELF-TEST PASS — 73 controls run`
  (was 71, +2 exactly as predicted).
- `python3 scripts/gen-gate-docs.py --check` -- exit 0, zero `DRIFT:` lines, `harvested 22/22`.
- `python3 scripts/_gate_registry.py --self-test` -- exit 0; `check-registration.py` -- exit 0;
  `report-conformance.py --self-test` -- `PASS — 101 controls run`; `--check` -- `PASS — no
  drift`.
- `sh .githooks/pre-commit` and `sh scripts/git-hooks/pre-commit` -- both exit 0.
- `LITERAL_EXEMPTION_CLASSES`, `_DEFERRED_LITERAL_HITS`, `_DEFERRED_LEDGER_MAX` and
  `_DEFERRED_LEDGER_KEYS_DIGEST` all confirmed unchanged, before and after every task.
- `bash scripts/check-firewall-battery.sh` -- `FIREWALL: GREEN (26/26)` -- an invariance
  check, never claimed as evidence a defect was closed.
- All three CONTRACT-06 sha256 pins byte-unchanged (`git diff --stat
  scripts/check-quality-harness.py` empty).
- Five falsification arms recorded above, each with exact exit code and failure/finding text;
  real tree `git status --porcelain` confirmed empty of scratch-copy contamination before and
  after every one.
