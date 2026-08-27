---
phase: 01-evidence-acquisition
plan: 02
subsystem: validation-scripts
tags: [gate, offline-harness, self-test, act-limb, harn-01]

# Dependency graph
requires: ["01-01"]
provides:
  - "scripts/check-act-limb.py — HARN-01 offline gate over the emitted Act-limb prose"
affects: [01-evidence-acquisition (Phase 4 / HARN-04 registration)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Derive self-test fixtures by mutating in-memory copies of the real emitted file, never hand-typed literals — a hand-typed fixture drifts from the prose it mirrors"
    - "Paragraph-scoped mutation (isolate the target paragraph, mutate a copy, substitute it back into the full text) so a negative control can strip an anchor from one occurrence without corrupting a second, legitimate occurrence of the same string elsewhere in the file"
    - "Named substring per negative control, asserted against the checker's own failure messages, so a fixture cannot pass for the wrong reason"

key-files:
  created:
    - scripts/check-act-limb.py
  modified: []

key-decisions:
  - "Tasks 1 and 2 were implemented and committed as a single logical commit rather than split into two. The self-test battery (Task 2) exercises the checker functions and slice/paragraph helpers Task 1 defines; building them in the same pass avoided an artificial intermediate state where the file exists with checkers but no way to prove they are non-vacuous. Both tasks' acceptance criteria were independently verified in full before committing."
  - "The plan's Task 1 acceptance-criteria literal `python3 -c \"...import check_act_limb as m...\"` does not work as written: `check-act-limb.py` has a hyphenated filename, and Python's `import` statement cannot resolve `check_act_limb` (underscore) to a file named with a hyphen — confirmed by reproducing the identical failure against the pre-existing `check-agent.py` (`ModuleNotFoundError: No module named 'check_agent'`). Verified the same intent (both checkers return an empty list against the real files, and `main([])` returns 0) via `importlib.util.spec_from_file_location`, the exact mechanism this repo's own `scripts/check-links_anchors_test.py` uses to import a hyphenated-filename script under test."

patterns-established:
  - "A gate's self-test proves each negative control fails FOR THE NAMED REASON, not merely that it fails — every control declares the substring its intended failure message must contain, mirroring check-agent.py and sync-content.py's GATE-02 control-battery convention."

requirements-completed: [HARN-01]

# Metrics
duration: 45min
completed: 2026-08-27
---

# Phase 1 Plan 2: Evidence Acquisition — HARN-01 Gate Summary

**Shipped `scripts/check-act-limb.py`, a stdlib-only offline gate that structurally asserts plan 01's Phase 3 Act-limb verification step (bound, tool instruments, failure path, provenance-label branches, injection-containment sentence) and the Criterion 3 Fix note are present, well-formed, and correctly placed in the emitted `first-principles/agents/` tree, backed by a 13-control self-test battery (2 positive, 10 negative, 1 dispatch) that derives every fixture by mutating in-memory copies of the real emitted files.**

## Performance

- **Duration:** ~45 min
- **Tasks:** 2/2 completed (implemented and committed together — see Deviations)
- **Files created:** 1 (`scripts/check-act-limb.py`, 501 lines)

## Accomplishments

- `_slice(text, start_heading, end_heading)` returns the text strictly between two headings, or `None` on a missing/out-of-order heading — `None` is a failure the caller must report, never a silently-empty pass (the D-11 vacuity failure mode this repo has been bitten by before).
- `_paragraph_containing(slice_text, anchor)` returns every blank-line-delimited block containing an anchor; every count-sensitive check (`Body-2`, `Body-3`, `Rubric-2`) asserts exactly one occurrence and names the observed count in its failure message rather than accepting "at least one."
- `_check_body_text` runs nine checks (Body-1 through Body-9) against the Phase 3 slice: placement (twice — in-slice and whole-file), the four literal anchors that make up the step's paragraph (tool instruments, population bound + exclusion clause, failure path, provenance-label branches, injection-containment sentence), and cross-file coherence proving the step and the pre-existing Exit criterion name the same population.
- `_check_rubric_text` runs four checks (Rubric-1 through Rubric-4) against the Criterion 3 slice: placement, exact-count presence of the Fix note lead, both Fix branches plus the stated preference, and a scope-discipline check proving the Fix note was not duplicated into Criterion 2 or Criterion 5.
- The self-test battery (controls a–m) builds every negative fixture by mutating an in-memory copy of the real `AGENT_FILE` / `RUBRIC_FILE` text — never a hand-typed literal — including a paragraph-scoped mutation helper (`_mutate_body_removing_from_step_paragraph`) that strips an anchor from only the step's paragraph, leaving a second legitimate occurrence of the same string elsewhere in the file (e.g. the population bound's second occurrence in the Exit criterion) untouched.
- Control (m) is a re-entrancy-guarded dispatch control, following the `sync-content.py` GATE-02 idiom exactly: a module-level `_HARN01_DISPATCH_REENTRANT` sentinel set only for the duration of a nested `main(["--self-test"])` call and restored in a `finally`, proving the CLI dispatch layer itself reaches the self-test block (not merely that `_run_self_test()` is correct when called directly).
- Live run against the real emitted tree: `python3 scripts/check-act-limb.py` → `check-act-limb: PASS`, exit 0.
- Self-test: `python3 scripts/check-act-limb.py --self-test` → all 13 controls (a)–(m) print "correctly failed" / "PASS" as intended, exit 0.

## Task Commits

1. **Task 1 + Task 2 (combined): Write scripts/check-act-limb.py — checker, live mode, CLI, and self-test battery** - `9673345` (feat)

## Files Created

- `scripts/check-act-limb.py` — HARN-01 gate. Stdlib-only (`import argparse, contextlib, io, re, sys; from pathlib import Path`), no PyYAML, no `subprocess`, no network call. `main(argv: list[str] | None = None) -> int` accepts an argv list and returns an int (per the plan's Task 1 spec, differing from `check-agent.py`'s `main()`). Module docstring names HARN-01, states the gate asserts the emitted tree (never `shared/`), and carries the one required sentence deferring registration to Phase 4 / HARN-04.

## Deviations from Plan

### Auto-fixed / Resolved Issues

**1. [Rule-permitted GSD mechanics] Tasks 1 and 2 committed as one commit, not two**
- **Found during:** Task 1, while drafting the checker functions
- **Issue:** The plan's Task 1 (`_check_body_text`, `_check_rubric_text`, `_slice`, `_paragraph_containing`, live mode, CLI) and Task 2 (the `--self-test` battery) are tightly coupled — the self-test's fixtures are built by calling the exact helpers Task 1 defines, and a Task-1-only commit would ship checker functions with no proof they are non-vacuous.
- **Resolution:** Wrote the full file (checker + self-test + CLI) in one pass and verified both tasks' full acceptance-criteria sets independently before committing once.
- **Files modified:** `scripts/check-act-limb.py`
- **Verification:** All Task 1 and Task 2 acceptance criteria were run and observed passing (see Verification Results below) before the single commit.
- **Committed in:** `9673345`

**2. [Rule 1 - plan defect] Task 1's `import check_act_limb` acceptance-criteria literal does not resolve**
- **Found during:** Task 1 acceptance-criteria verification
- **Issue:** `python3 -c "import sys; sys.path.insert(0,'scripts'); import check_act_limb as m; ..."` raises `ModuleNotFoundError: No module named 'check_act_limb'` — Python's `import` statement cannot map the underscore identifier onto a file named with a hyphen (`check-act-limb.py`). Reproduced the identical failure against the repo's own pre-existing `check-agent.py` (`import check_agent` also fails the same way) to confirm this is a general Python behavior, not a defect in the new script.
- **Fix:** Verified the acceptance criterion's actual intent — `_check_body_text` / `_check_rubric_text` return empty lists against the real files, and `main([])` returns 0 — via `importlib.util.spec_from_file_location`, the exact mechanism `scripts/check-links_anchors_test.py` already uses in this repo to import a hyphenated-filename script under test.
- **Files modified:** None (verification-only; no plan defect requiring a checkpoint, mirroring how 01-01-SUMMARY.md handled `check-agent.py`'s bare-invocation usage-error).
- **Verification:** `importlib.util.spec_from_file_location('check_act_limb', 'scripts/check-act-limb.py')` load + `m._check_body_text(...)`, `m._check_rubric_text(...)` both returned `[]`; `m.main([])` returned `0` and printed `check-act-limb: PASS`.

---

**Total deviations:** 2 (1 GSD-mechanics combination, 1 plan-literal correction) — no scope change, no architecture change, no files added beyond the plan's declared `files_modified` list.

## Vacuity Probe (Task 2's second acceptance criterion)

Per the plan: "temporarily replacing `_B2_POPULATION`'s constant value with a string that also appears in the real body (e.g. `the`) makes control (d) report a wrong-pass and the command exit 1."

**Method:** Edited the committed `scripts/check-act-limb.py` in place, replacing `_B2_POPULATION`'s value with `"the"`, ran `python3 scripts/check-act-limb.py --self-test`, observed the result, then restored the file via `git checkout -- scripts/check-act-limb.py` (safe — the file was already committed; `git status --porcelain` was clean both before and after).

**Observed exit code:** `1` (not `0`) — the self-test correctly reports the perturbation as a failure.

**Observed mechanism (a nuance worth recording):** the perturbation did not manifest as a silent wrong-*pass* on control (d) as the plan's illustrative wording anticipated. Because `_mutate_body_removing_from_step_paragraph` strips **every** occurrence of the target string from the step paragraph — including from `_B1_STEP_LEAD` itself, since the step-lead sentence contains the word "the" twice ("before assigning **the** label", "attempt **the** read") — replacing `_B2_POPULATION` with `"the"` also corrupts the step-lead sentence in the fixture. The mutated paragraph then no longer matches `_B1_STEP_LEAD` verbatim, so `_check_body_text` reports zero paragraph matches (`Body-4..9: step paragraph occurs 0 time(s)...`) rather than a bound-specific failure. Control (d)'s wrong-*reason* detection (`_check_negative`'s `elif not any(expected_substring in f for f in failures)` branch) correctly caught this as `failed for the WRONG reason (expected substring 'the bound', ...)`, and the overall self-test still exited 1. This is arguably a **stronger** proof of non-vacuity than a bare wrong-pass would have been: the self-test's own reason-checking machinery, not just the presence of *a* failure, is what caught the degraded constant.

**Restored constant:** confirmed `_B2_POPULATION` back to its original value; `python3 scripts/check-act-limb.py --self-test` re-run and confirmed `check-act-limb --self-test: PASS`, exit 0; `git status --porcelain` clean.

## Verification Results

1. `python3 scripts/check-act-limb.py --self-test` — exit 0, all 13 controls (a)-(m) print "correctly failed" or "PASS".
2. `python3 scripts/check-act-limb.py` — exit 0, `check-act-limb: PASS`, against the real emitted tree.
3. `bash scripts/check-firewall-battery.sh` — **FIREWALL: RED (16/17 passed)**, not GREEN/17 as the plan's acceptance criterion states. The sole failure is the pre-existing VAL-03 `python3 -m pytest scripts/check-links_anchors_test.py -q` sub-check (`No module named pytest` — this worktree's system `python3` has no pytest, identical root cause to the gap 01-01-SUMMARY.md already documented and explicitly identified as outside that plan's scope). Independently confirmed via `uv run --with pytest python3 -m pytest scripts/check-links_anchors_test.py -q` → `8 passed`. The other two VAL-03 sub-checks (`check-links.py --self-test`, live `check-links.py`) independently passed with exit 0. Not auto-fixed: installing `pytest` is a package-manager install, excluded from Rule 3 auto-fix, and no file this plan modifies references pytest.
4. `git status --porcelain scripts/check-firewall-battery.sh` — empty (untouched, as required).
5. `git status --porcelain CLAUDE.md` — empty (untouched, as required).
6. `python3 scripts/sync-content.py --check` — exit 0.

## Phase 4 Handoff (verbatim, for HARN-04)

`scripts/check-act-limb.py --self-test` is the HARN-01 gate command and is **NOT** yet registered in `scripts/check-firewall-battery.sh`, whose tally is still 17. Phase 4 must add the `gate "HARN-01" ...` block, move the tally comment and the reported total, and add the HARN-01 row to CLAUDE.md's gate-inventory table.

## Anchor Literals

No anchor literal deviated from plan 01-01's `<interfaces>` B1-B7 / R1-R4 set — all eleven anchors were confirmed verbatim against the live emitted tree (`first-principles/agents/first-principles.md`, `first-principles/agents/references/validation-rubric.md`) before being hardcoded as module-level constants in `scripts/check-act-limb.py`:

| Anchor | Constant | Whole-file count confirmed |
|---|---|---|
| B1 | `_B1_STEP_LEAD` | 1 |
| B2 | `_B2_POPULATION` | 2 (step + Exit criterion) |
| B3 | `_B3_TOOLS` (list) | — (co-occurrence check) |
| B4 | `_B4_EXCLUSION` | 1 |
| B5 | `_B5_NO_FALLBACK` | 1 |
| B6 | `_B6_READ_AT_SOURCE`, `_B6_REPORTED_BY_DELEGATE` | — (co-occurrence check) |
| B7 | `_B7_EVIDENCE_NOT_INSTRUCTION` | 1 |
| R1 | `_R1_FIX_LEAD` | 1 |
| R2 | `_R2_ACQUIRE` | — (presence check) |
| R3 | `_R3_DOWNGRADE` | — (presence check) |
| R4 | `_R4_PREFERENCE` | 1 (confirmed on a single unwrapped line, per 01-01's Assumption Drift advisory) |

## Known Stubs

None — the script is a complete, self-contained gate with no UI or data-fetching surface.

## Threat Flags

None beyond this plan's own `<threat_model>` (T-01-06 through T-01-09, T-01-SC), all mitigated as designed:
- T-01-06 (assertion-set vacuity) — mitigated by controls (c)-(l), each a separate negative fixture per anchor.
- T-01-07 (`_slice` silent-vacuity / D-11) — mitigated by `_slice` returning `None` on a missing heading (control j) and exact-count checks naming the observed count (controls c, h, i all assert `expected exactly 1`).
- T-01-08 (elevation of privilege via the new script) — mitigated: stdlib-only, read-only, no `subprocess`/network/write; confirmed by the import-block grep (Task 1) and `git status --porcelain` staying clean after `--self-test` (Task 2).
- T-01-09 (unregistered gate indistinguishable from forgotten) — mitigated by the module docstring's explicit Phase-4/HARN-04 deferral sentence, confirmed present exactly once by grep.
- T-01-SC (package installs) — not applicable; no packages installed.

## User Setup Required

None.

## Next Phase Readiness

- `scripts/check-act-limb.py` passes both its live run and its self-test against the real emitted tree as committed at `9673345`.
- Phase 4 / HARN-04 has the exact registration handoff text above; no further action needed from this plan.
- The one open item carried forward — `pytest` not available to this worktree's system `python3`, causing `bash scripts/check-firewall-battery.sh` to report 16/17 instead of 17/17 — is a pre-existing environment gap first documented in 01-01-SUMMARY.md, confirmed unchanged and independently verified via `uv` in this plan, and is not this plan's responsibility to fix.

---
*Phase: 01-evidence-acquisition*
*Completed: 2026-08-27*

## Self-Check: PASSED

- FOUND: scripts/check-act-limb.py
- FOUND commit: 9673345 (Task 1 + Task 2, combined)
