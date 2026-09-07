---
phase: 21-generate-the-claim-surface
plan: 20
subsystem: infra
tags: [claim-surface, gen-gate-docs, literal-scanner, sha256-pin, ratchet, ci-gates]

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    provides: "21-19's roster_arm_shape_census_problems() generalization and the confirmed 135/135 deferred-literal-ledger baseline this plan's Task 1 pins against"
provides:
  - "A deferred-literal-ledger ratchet with a same-commit repin obligation on shrink plus a sha256 key-set digest lock closing the same-size-substitution hole (T-21-20-01/02)"
  - "A relative (ledger-size-scaled) load-bearing floor replacing the absolute len(problems) > 100 assertion that turned RED on successful remediation (WR-05)"
  - "Two more stale hand-maintained population-count literals found and fixed during the docstring sweep (27-row gate table -> live 31; 24 thin pages -> live 15), beyond the plan-scoped '16 controls' fix"
  - "A published, self-file-ratcheted measurement of the py-docstrings-only blind spot (353 hits / 19 surfaces live; gen-gate-docs.py's own 30-hit share two-sided-ratcheted)"
affects: [21-generate-the-claim-surface, future-conf13-work]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "sha256 key-set digest pin over a dict's sorted keys (hashlib.sha256 of a UTF-8, \\x1f-separated, one-key-per-line blob), same idiom as check-quality-harness.py's CONTRACT-06 detector pins, applied to a permit ledger rather than a function's source bytes"
    - "Three-predicate ratchet shape (growth / un-repinned shrink / key-set drift) generalising the two-predicate ledger-size ratchet from plan 21-16"
    - "Read-only measurement helper (_nonmodule_docstring_hits) that feeds derived_counts but never literal_scan_problems -- publishing a blind spot's size without closing it"

key-files:
  created: []
  modified:
    - scripts/gen-gate-docs.py
    - docs/gates/CONF-SURFACE.md
    - CLAUDE.md
    - docs/ARCHITECTURE.md

key-decisions:
  - "Predicate 3 (key-set digest) is the only one of three predicates that closes the verifier's same-size-substitution reproduction -- documented in the function's own docstring so a future reader does not delete it as redundant with the size checks"
  - "Did not widen the standing .py literal scan to cover function/class docstrings (Task 3): would require ~350 prose remediations or refilling the just-locked ledger; publishes the blind spot's live size instead, with a two-sided ratchet scoped to this phase's own file only"
  - "Extended the docstring sweep beyond the plan's one named target (_control_registry_self_test_passes' '16 controls') after finding two more stale population-count literals live-wrong by inspection (_gate_table_rows' '27-row' vs live 31; _normalise_numbers' '24 thin pages' vs live 15) -- fixed both under Rule 1 (bug), same no-hand-typed-number discipline"
  - "Left two adjacent findings unfixed and logged to deferred-items.md: a stale '28 generated detail pages' code COMMENT (out of scope -- comments are never scanned, and Task 2's sweep was scoped to function docstrings) and an ambiguous, non-diverging illustrative example inside _normalise_numbers' docstring"

requirements-completed: [CONF-13]

# Metrics
duration: not precisely tracked (no start timestamp captured at plan launch)
completed: 2026-09-07
---

# Phase 21 Plan 20: Ledger ratchet hardening, relative load-bearing floor, and a published py-docstrings-only measurement Summary

**Closed the verifier's exact GAP B reproduction (a same-size ledger substitution producing zero findings) with a sha256 key-digest pin, replaced an absolute load-bearing floor that turns RED on successful remediation with one relative to the ledger's own size, and turned an unquantified py-docstrings-only disclosed bound into a published, self-file-ratcheted derived measurement.**

## Performance

- **Duration:** not precisely tracked
- **Completed:** 2026-09-07
- **Tasks:** 3/3 completed
- **Files modified:** 4 (`scripts/gen-gate-docs.py`, `docs/gates/CONF-SURFACE.md`, `CLAUDE.md`, `docs/ARCHITECTURE.md`)

## Accomplishments

- `literal_ledger_ratchet_problems` now runs three independent predicates (growth / un-repinned shrink / key-set digest drift) instead of one, closing both the headroom hole (T-21-20-02) and the same-size-substitution hole (T-21-20-01) the size-only ratchet could not see.
- `_control_ledger_not_an_unconditional_permit`'s arm (b) no longer asserts an absolute `len(problems) > 100` — replaced with a floor relative to the ledger's own live size, so successful remediation can never turn it RED (WR-05, demonstrated both ways in falsification 6).
- The py-docstrings-only disclosed bound's live size is now a derived, re-measured `derived_counts` field (`literal_scan_nonmodule_docstring_hits`=353, `literal_scan_nonmodule_docstring_surfaces`=19) rather than an unquantified prose claim, with a two-sided ratchet on `scripts/gen-gate-docs.py`'s own 30-hit share (the file the WR-08 stale-literal defect actually landed in).
- Control count rose from 64 to 69 across the plan (2 + 1 + 2, one rename), matching the plan's stated arithmetic exactly.

## Task Commits

1. **Task 1: Turn the ledger's size cap into a repin obligation plus a key-set digest lock** - `c9ceca2` (feat)
2. **Task 2: Make the load-bearing floor relative, and remove the stale docstring count literal** - `fcd328b` (fix)
3. **Task 3: Quantify and ratchet the py-docstrings-only blind spot, then regenerate** - `267f50f` (feat)

**Plan metadata:** committed together with this SUMMARY (see final commit below)

## Files Created/Modified

- `scripts/gen-gate-docs.py` — `_deferred_ledger_keys_digest`, extended `literal_ledger_ratchet_problems` (3 predicates), renamed/added ledger ratchet controls, relative `_control_ledger_not_an_unconditional_permit`, `own-registry-docstring-has-no-count` control, `_nonmodule_docstring_hits`, `nonmodule_docstring_selffile_ratchet_problems`, two self-file ratchet controls, two more stale-literal docstring fixes (`_gate_table_rows`, `_normalise_numbers`), `import hashlib`
- `docs/gates/CONF-SURFACE.md` — rewritten section (6) (repin obligation, key digest, disclosed bound) and bound (4) (py-docstrings-only: published measurement, self-file ratchet, decision not to widen); Facts fence regenerated (69 controls, 18 derived_counts entries, `ledger-repin-and-key-digest` anchor)
- `CLAUDE.md`, `docs/ARCHITECTURE.md` — regenerated CONF-SURFACE table cells (control_ids/control_count=69)

## Decisions Made

- **Predicate ordering and non-redundancy (T-21-20-01):** the key-set digest predicate is documented, in the function's own docstring, as the ONE predicate a same-size substitution cannot evade — explicit so a future reader does not delete it as "redundant" with the size checks.
- **No widening of the standing `.py` scan (Task 3):** re-measured live at 353 non-module-docstring hits across 19 of 22 registered `.py` surfaces (was 345/19 at planning time — the small rise reflects this plan's own docstring edits). Widening would require either ~350 prose remediations or refilling the now size-pinned, key-digest-locked ledger — exactly the regression Task 1 closes. Published the size instead; two-sided-ratcheted only `scripts/gen-gate-docs.py`'s own share (the file the WR-08 defect landed in).
- **Extended the docstring sweep beyond the plan's one named target.** Task 2's action named `_control_registry_self_test_passes`' "16 controls" specifically but also instructed a general sweep ("rewrite those the same way; report how many were found and what each said"). The sweep found two more genuinely stale population-count literals — `_gate_table_rows`' docstring claimed "27-row" (live: 31, since the registry grew to 31 entries after this docstring was written); `_normalise_numbers`' docstring claimed "24 thin fully-generated pages" (live: 15, since `NARRATIVE_ENTRIES` grew to 16 members). Both fixed under Rule 1 (auto-fix bugs — a wrong hand-maintained claim is a defect), using the same no-hand-typed-number rewrite discipline as the plan's one named target.
- **Two findings from the same sweep left unfixed, logged to `.planning/phases/21-generate-the-claim-surface/deferred-items.md`:** a stale `"28 generated detail pages"` code comment (live: 31) — out of scope because Task 2's action scoped the sweep to *function docstrings*, and a `#`-comment is never read by the standing scanner regardless of scope, so it carries no `--check`/`--self-test` risk; and an ambiguous illustrative example inside `_normalise_numbers`' own docstring (`` `27` diverging from a Facts-fence `27` ``, which reads as non-diverging since both numbers match) — reviewed and judged to be a hypothetical illustration, not a current population claim in the same shape as the two genuine fixes above.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed a second, unrelated stale population-count literal: `_gate_table_rows`'s "27-row" claim**
- **Found during:** Task 2's function-docstring sweep (the plan's own instruction to sweep beyond the one named target)
- **Issue:** `_gate_table_rows`'s docstring claimed the gate table renders "27-row"; the live non-anticipatory registry-entry count is 31 (measured via `len(_gate_registry.ENTRIES)` minus `_ANTICIPATORY_KEYS`, which is empty) — a WR-08-shaped defect predating this plan.
- **Fix:** Rewrote to name the property (one row per non-anticipatory entry) without a hand-typed number, noting in-docstring that the prior literal went stale as the registry grew.
- **Files modified:** `scripts/gen-gate-docs.py`
- **Verification:** `/usr/bin/grep -c '27-row' scripts/gen-gate-docs.py` returns 0; live count confirmed at 31 via direct measurement.
- **Committed in:** `fcd328b` (Task 2 commit)

**2. [Rule 1 - Bug] Fixed a third stale population-count literal: `_normalise_numbers`'s "24 thin fully-generated pages" claim**
- **Found during:** Task 2's function-docstring sweep
- **Issue:** Claimed 24 thin (non-`NARRATIVE_ENTRIES`) pages; live count is 15 (`len(ENTRIES)`=31 minus `len(NARRATIVE_ENTRIES)`=16, confirmed against the actual generated page set too).
- **Fix:** Rewrote to describe the population as "live-counted... that moves as gates are added" without a hand-typed number.
- **Files modified:** `scripts/gen-gate-docs.py`
- **Verification:** `/usr/bin/grep -c '24 thin' scripts/gen-gate-docs.py` returns 0; live thin-page count confirmed at 15 by two independent computations (registry arithmetic and actual `generate_all()` page-set inspection).
- **Committed in:** `fcd328b` (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (both Rule 1 — stale hand-maintained literals found during the plan's own instructed sweep, same category as the plan's one named target)
**Impact on plan:** Both fixes are inside the exact activity the plan's Task 2 action prescribed ("sweep this file's remaining function docstrings for any other count literal naming a control roster or gate population and rewrite those the same way"). No scope creep — these are the sweep's intended yield, not unrelated work.

## Falsification Arms — Exact Failure Text

**Task 1 (ledger ratchet, 5 arms):**

1. **Same-size substitution (the verifier's exact reproduction).** Remove one real ledger entry, add `("CLAUDE.md", "99 gates")` in its place (size unchanged, 135 -> 135):
   ```
   deferred-literal-ledger ratchet: live key-set digest 'sha256:24aa21e2ca56dae8ab693c537fa43691dbf8a98b790efec87fd8dd094e1fc81a' != pinned 'sha256:0a249f6de8c4b520d3e76590cfc6d1b8296497c5cbfef05bd7533d64a0f068bc' -- the ledger's key set changed; if this is a deliberate, adjudicated remediation, re-pin _DEFERRED_LEDGER_KEYS_DIGEST to the live value in this same commit (this digest proves the key set changed deliberately, never that the change was adjudicated)
   ```
   Same-size substitutions producing zero findings: **0** (was 1).

2. **Un-repinned shrink (headroom closed).** Remove one real ledger entry without re-pinning (135 -> 134):
   ```
   deferred-literal-ledger ratchet: live ledger size 134 is below the pinned maximum 135 -- lower _DEFERRED_LEDGER_MAX to the live size in this same commit so the shrink is locked in and cannot silently refill with a new, never-adjudicated permit
   ```

3. **Growth still fails (unregressed).** Registered control `ledger-ratchet-fires`: a synthetic ledger one entry larger than its pin produces exactly one finding naming both figures (`1`/`2`) — confirmed via `--self-test`.

4. **End-to-end via `--check` on a scratch copy.** Pre-mutation: clean scratch copy, `--check` exits 0, zero `DRIFT:` lines. Post-mutation (same-size substitution in the real `_DEFERRED_LITERAL_HITS` source literal): `--check` exits 1, the digest-mismatch finding (not a `DRIFT:` line) carries the failure — confirmed the digest finding appears BEFORE the drift-diff stage (the function returns before `cmd_check` reaches its drift comparison).

5. **Digest is a derivation, not a constant.** Two synthetic ledgers differing in exactly one key produce different digests; the same ledger rebuilt in reverse insertion order produces the identical digest — proved by registered control `ledger-key-digest-derived`, run via `--self-test`.

**Task 2 (relative floor + docstring sweep, 3 arms):**

6. **Remediation no longer turns the tree red.** On a scratch copy: monkeypatched `run_literal_scan` to a synthetic 3-hit read, shrunk the ledger to 1 entry (re-pinned max + digest) — relative form:
   ```
   RELATIVE FORM: PASS (as expected)
   ```
   Restored the absolute `len(problems) > 100` form on the same fixture:
   ```
   ABSOLUTE FORM: FAILED (as expected): emptying the ledger produced only 3 findings -- expected a large, non-zero count proving the ledger is load-bearing
   ```
   This is the evidence WR-05 was a real latent trap, not a hypothetical: the absolute form fails on a genuinely-remediated small-hit-population world; the relative form scales with the ledger and passes.

7. **Relative floor is not vacuous.** `literal_scan_problems` monkeypatched to return `[]` unconditionally, real ledger (135 entries) in place:
   ```
   FAILED (as expected): emptying the ledger produced only 0 findings, fewer than the ledger's own 135 entries -- the ledger is not load-bearing
   ```

8. **Docstring control fires.** Reinserted `16 controls` into `_control_registry_self_test_passes`' docstring on a scratch copy:
   ```
   gen-gate-docs: SELF-TEST FAIL [own-registry-docstring-has-no-count] -- _control_registry_self_test_passes' docstring carries a digit: "...`scripts/_gate_registry.py --self-test`'s\n16 controls -- including the ONLY duplicate-`key`/`gate_id` check -- ..."
   ```

**Task 3 (py-docstrings-only measurement + self-file ratchet, 4 arms + 1 invariance check):**

9. **Measurement is derived, not constant.** Added a fabricated function docstring literal to `scripts/check-agent.py` (a registered surface OTHER than `gen-gate-docs.py`) on a scratch copy: total rose from 353 to 354, no constant edited.

10. **Self-file ratchet fires upward.** Added a fabricated docstring literal to a new function inside `scripts/gen-gate-docs.py` on a scratch copy:
    ```
    nonmodule-docstring self-file ratchet: scripts/gen-gate-docs.py's live non-module-docstring hit count 31 exceeds the pinned 30 -- a new hand-maintained count literal landed in a function/class docstring in this file (the WR-08 shape) and must be fixed or the pin explicitly raised alongside a written justification
    ```

11. **Self-file ratchet demands a re-pin downward.** Removed a real count literal (`"two"` from `SlugCollisionError`'s docstring) from `scripts/gen-gate-docs.py` on a scratch copy without lowering the pin:
    ```
    nonmodule-docstring self-file ratchet: scripts/gen-gate-docs.py's live non-module-docstring hit count 29 is below the pinned 30 -- lower _SELF_FILE_NONMODULE_DOCSTRING_HITS to the live count in this same commit so the shrink is locked in
    ```

12. **Drift gate still binds.** Hand-edited `docs/gates/CONF-SURFACE.md`'s Facts fence `control_count` from `69` to `999` on a scratch copy:
    ```
    DRIFT: docs/gates/CONF-SURFACE.md
    ```

**Invariance check (not an arm — no mutation, asserts an unchanged property):** `literal_scan_non_exempt` = 0 both before and after this plan (unchanged); `len(_DEFERRED_LITERAL_HITS)` = 135 both before and after this plan (unchanged) — the standing scan's enforced surface set and behaviour are provably unwidened.

**Arm count:** 5 (Task 1) + 3 (Task 2) + 4 (Task 3) = **12**, matching the plan's stated total exactly. Across the gap-closure wave: 8 (21-17) + 7 (21-18) + 10 (21-19) + 12 (21-20) = **37**.

## Before/After `SELF-TEST PASS — N controls run`

- Pre-plan baseline (post-21-19): `SELF-TEST PASS — 64 controls run`
- After Task 1 (`ledger-ratchet-allows-shrink` renamed to `ledger-ratchet-requires-repin-on-shrink`; `ledger-key-digest-fires`, `ledger-key-digest-derived` added): `SELF-TEST PASS — 66 controls run`
- After Task 2 (`own-registry-docstring-has-no-count` added): `SELF-TEST PASS — 67 controls run`
- After Task 3 (`selffile-docstring-ratchet-fires`, `selffile-docstring-ratchet-requires-repin-on-shrink` added): `SELF-TEST PASS — 69 controls run`
- Net delta: **+5** across the plan (2 + 1 + 2), matching the plan's stated arithmetic exactly, with one rename (`ledger-ratchet-allows-shrink` -> `ledger-ratchet-requires-repin-on-shrink`) and `ledger-ratchet-allows-shrink` confirmed absent from the file post-plan.

## Re-pinned Values, with Reason for Each Re-pin

- **`_DEFERRED_LEDGER_MAX`:** unchanged at `135` — the ledger size did not move this plan (Task 1 only added the digest lock and repin obligation; no ledger entries were added or removed). `plan 21-19`'s SUMMARY assertion that the ledger is unmoved is confirmed by direct measurement (`len(_DEFERRED_LITERAL_HITS)` == 135).
- **`_DEFERRED_LEDGER_KEYS_DIGEST`:** newly pinned at `sha256:0a249f6de8c4b520d3e76590cfc6d1b8296497c5cbfef05bd7533d64a0f068bc` — first pin of this constant (did not exist before this plan); computed via `_deferred_ledger_keys_digest(_DEFERRED_LITERAL_HITS)` over the unmodified real ledger.
- **`_SELF_FILE_NONMODULE_DOCSTRING_HITS`:** newly pinned at `30` — first pin of this constant. Live count of function/async-function/class docstring literal hits inside `scripts/gen-gate-docs.py` itself, measured via `_nonmodule_docstring_hits()` filtered to `scripts/gen-gate-docs.py#` relpaths, after all of this plan's own docstring edits landed (the pin reflects the post-plan state, not a mid-plan snapshot).

## Re-measured Blind-Spot Totals (Live, Not Planning-Time)

- **Total non-module-docstring hits, all 22 registered `.py` surfaces:** `353` (planning-time reading was 345; the ~8-hit rise reflects this plan's own docstring edits across Tasks 1-3, e.g. new controls' docstrings, the rewritten ledger-ratchet docstring, etc. — expected, since the plan explicitly instructs re-measuring rather than trusting the planning figure).
- **`.py` surfaces contributing at least one hit:** `19` of 22 (unchanged from the planning-time reading).
- **`scripts/gen-gate-docs.py`'s own share:** `30` hits (this is the number pinned into `_SELF_FILE_NONMODULE_DOCSTRING_HITS`).
- Both totals are published as live `derived_counts` fields (`literal_scan_nonmodule_docstring_hits`, `literal_scan_nonmodule_docstring_surfaces`) rather than restated by hand on any page — visible in `docs/gates/CONF-SURFACE.md`'s Facts fence.

## Standing Literal Scan — Unchanged Behaviour, Explicitly Stated

The standing `.py`-branch scanner in `run_literal_scan()` (`ast.get_docstring(ast.parse(src))`, module docstrings only) was **not modified or widened** by this plan. Confirmed by direct measurement, before and after all three tasks:
- `literal_scan_non_exempt` = `0` (unchanged)
- `len(_DEFERRED_LITERAL_HITS)` = `135` (unchanged)
- `LITERAL_SCAN_SURFACES` = 30 registered surfaces (unchanged; `scripts/_gate_registry.py` diff is empty across the whole plan)

Everything Task 3 added (`_nonmodule_docstring_hits`, the two new `derived_counts` fields, the self-file ratchet) sits alongside the standing scan, reading the same `.py` sources independently, and never feeds its findings into `literal_scan_problems` or any `--check` finding except the one self-file ratchet scoped to `scripts/gen-gate-docs.py`.

## Issues Encountered

None beyond the deviations documented above. All falsification arms and the plan's own automated `<verify>` blocks passed on the first attempt after each task's edits; no fix-attempt-limit was approached.

## Verification Run (Plan-Level, Post-Task-3)

- `python3 scripts/gen-gate-docs.py --self-test` — exit 0, `SELF-TEST PASS — 69 controls run`
- `python3 scripts/gen-gate-docs.py --check` — exit 0, `harvested 22/22 expected script-backed entries (22 total)`, zero `DRIFT:` lines
- `bash scripts/check-firewall-battery.sh` — **25/26 passed, 1 PREREQ** (`VAL-03` blocked: no pytest-capable interpreter in this environment — `.venv` absent, bare `python3` cannot `import pytest`). This is a pre-existing environment limitation, confirmed unrelated to this plan (same condition would block VAL-03 regardless of this plan's changes; `CLAUDE.md` itself documents this as `FIREWALL: BLOCKED`, exit 2, a distinct outcome from a genuine gate failure). All 25 non-prerequisite gates, including `CONF-SURFACE` itself, report `[PASS]`. **Not claiming `FIREWALL: GREEN`** — the plan's stated success criterion assumed a pytest-capable interpreter is available, which it is not in this worktree.
- `python3 scripts/check-registration.py` — exit 0, `14/14 skills name-matched`, `23/24 battery gates CI-registered + 1 battery-only by design`
- `sh .githooks/pre-commit` — exit 0 (both pre-commit hook invocations during Task commits also passed, since commits succeeded without `--no-verify`)
- `sh scripts/git-hooks/pre-commit` — exit 0
- `git diff --stat -- scripts/_gate_registry.py` (base commit to HEAD) — empty; the registry is fully unmodified by this plan
- `CLAUDE.md` and `docs/ARCHITECTURE.md` CONF-SURFACE table cells: `control_ids=69; control_count=69; disclosed_bounds_anchors=7` — matches the live `--describe` emission exactly (mechanically confirmed by grep)

## Known Stubs

None. This plan is a pure-Python generator/gate hardening plan; no UI or data-rendering surface is touched.

## Threat Flags

None. All six threat-register entries (T-21-20-01 through T-21-20-06, plus T-21-20-SC) were disposed of within this plan's own scope: five `mitigate` entries are the Task 1/2/3 work itself (each cross-referenced above via its falsification arm), and the two `accept` entries (T-21-20-05, not widening the standing scan; T-21-20-SC, no package installs) required no code change beyond the invariance check confirming the accepted-risk boundary held. No new network surface, auth path, file-access pattern, or schema change at a trust boundary was introduced.

## Next Phase Readiness

- Phase 21 (Generate the Claim Surface) gap-closure wave is complete: plans 21-17 through 21-20 close all items `21-VERIFICATION.md` flagged, plus the WR-05 latent-risk disposition this plan's own objective documents in full.
- The deferred-literal ledger is now both size-pinned (repin-obligated on shrink) and key-digest-locked — any future plan touching `_DEFERRED_LITERAL_HITS` must re-pin BOTH `_DEFERRED_LEDGER_MAX` and `_DEFERRED_LEDGER_KEYS_DIGEST` in the same commit as the edit, per the standing CONTRACT-06-style rule (never recompute a pin to make a failing check pass).
- Two minor, pre-existing findings are logged (not fixed) in `.planning/phases/21-generate-the-claim-surface/deferred-items.md` for a future reviewer: a stale `#`-comment count (out of scanner reach by construction) and an ambiguous illustrative docstring example. Neither blocks this plan's or the phase's completion.
- No blockers for downstream work. `VAL-03`'s pytest-interpreter prerequisite (environment-level, pre-existing, unrelated to this plan) is the only firewall-battery item not at `[PASS]`.

## Self-Check: PASSED

- Commit `c9ceca2` found in `git log --oneline --all`
- Commit `fcd328b` found in `git log --oneline --all`
- Commit `267f50f` found in `git log --oneline --all`
- `scripts/gen-gate-docs.py` exists on disk
- `docs/gates/CONF-SURFACE.md` exists on disk
- `python3 scripts/gen-gate-docs.py --self-test` and `--check` both re-run clean immediately before writing this summary (see Verification Run section above)

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-07*
