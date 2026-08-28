---
phase: 02-loop-closure
plan: 03
subsystem: testing
tags: [python-stdlib, gate-harness, negative-controls, self-test]

# Dependency graph
requires:
  - phase: 02-loop-closure
    plan: 01
    provides: The canonical "at most one re-perception pass" bound (L1), the degradation path (L2), the Phase-1 re-entry route (L3), the re-entry firing record (L4), the removed unbounded Repeat instruction (X1 absence), and the Phase 3 exit-criterion exception clause (L10a/L10b) in shared/spine/SKILL-body.md
  - phase: 02-loop-closure
    plan: 02
    provides: The mid-run AskUserQuestion re-open clause (L5/L6/L7/L7b) in shared/agent/input-contract.md, and the bounded rubric re-score instruction (L8/L9) plus removed unbounded X2 in shared/spine/references/validation-rubric.md
provides:
  - "scripts/check-loop-closure.py: an offline, deterministic, stdlib-only gate (HARN-02) asserting every re-entry edge and its bound survives across the three shared/ source files, with a negative control per assertion"
  - "A shared _BOUND module constant asserted against both SKILL-body.md and validation-rubric.md, so the two prose sites cannot diverge without failing the gate on both (assertion D1)"
  - "Two scoped single-line assertions (S1: the Repeat item; S2: the Phase 3 exit-criterion line) and one scoped paragraph assertion (S3: the Turn discipline bound paragraph names the second-order edge) with their own anchor-arity negative controls"
affects: [04-battery-registration]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Whole-text presence checks (must-contain-anywhere) require a strip-EVERY-occurrence negative control, not a single-site one — a duplicated literal in the source text otherwise leaves a single-site-stripped negative control wrongly passing, because the text-wide `target not in text` assertion is still satisfied by the surviving copy"
    - "Scoped single-line/paragraph assertions (S1/S2/S3) pair a presence-or-absence check on the anchor's own content with a separate anchor-arity control (zero or many matches is itself a failure, not a silent pick of the first match)"
    - "Pure check functions taking text and returning list[str] failure messages, never raising/printing, mirroring check-agent.py's _check_agent_text contract, extended from one source file to three"

key-files:
  created:
    - scripts/check-loop-closure.py
  modified: []

key-decisions:
  - "Combined Task 1 (checker core + CLI) and Task 2 (self-test) into a single commit rather than two, since both operate on the same single file this plan is scoped to (files_modified names exactly one path) and splitting them would have required authoring a throwaway stub only to immediately overwrite it in the next commit — a GSD-internal commit-granularity mechanic, not a content decision. Task 3 (falsification probes + non-regression proof) produced no additional file diff, so it has no commit of its own; its evidence is recorded in this SUMMARY instead."
  - "Chose to strip ALL occurrences of a target literal for the whole-text presence negative controls (N1-N4, N9-N11), not a single-site strip, after N4 (L2, the degradation-path phrase) revealed the real text states that phrase twice — once in the canonical Turn discipline bound paragraph, once in the Repeat item's own sentence. A single-site strip left the second copy standing, and the `target not in text` assertion never fired: a WRONGLY PASSED negative control. The line/paragraph-scoped controls (N6-N8, N13) stayed single-site, since their targets are confirmed single-occurrence within their scoped line or paragraph — verified by direct count before writing each control."
  - "Followed the plan's `<resolved_design_decisions>` verbatim on all three open questions: qualitative bound token (not numeric), a new dedicated script (not an extension of check-agent.py), and the rubric edit treated as required (checked as a full third source, not optional) since one of the five re-entry edges lives only in the rubric."

patterns-established:
  - "A whole-text `must CONTAIN` gate assertion needs an all-occurrences negative control, verified by an explicit occurrence count check during authoring — a single-site strip is only sufficient when the target is independently confirmed to occur exactly once in the real source"

requirements-completed: [HARN-02]

# Metrics
duration: ~45min
completed: 2026-08-28
---

# Phase 2 Plan 03: HARN-02 Loop-Closure Gate Summary

**New offline, stdlib-only `scripts/check-loop-closure.py` reads `shared/spine/SKILL-body.md`, `shared/agent/input-contract.md`, and `shared/spine/references/validation-rubric.md` as three separate strings and asserts all nine pinned re-entry-edge literals (L1-L9), both removed-unbounded-instruction absences (X1, X2), two scoped single-line checks, and one scoped bound-paragraph check are present — backed by a `--self-test` running one positive control, thirteen negative controls, two anti-masking controls, and two anchor-arity controls, all nineteen passing, plus three on-disk falsification probes proving the controls are load-bearing against the real files.**

## Performance

- **Duration:** ~45 min
- **Completed:** 2026-08-28
- **Tasks:** 3 (all `type="auto"`, no checkpoints); Tasks 1-2 combined into one commit (see Decisions Made), Task 3 is verification-only with no additional file diff
- **Files modified:** 1 (`scripts/check-loop-closure.py`, new file)

## Accomplishments

- Authored `scripts/check-loop-closure.py`: stdlib-only (`argparse`, `sys`, `pathlib`), `_require_python_version()` gating Python <3.12, exit codes 0/1/2 matching the repo's convention.
- Three pure check functions (`_check_body_text`, `_check_input_contract_text`, `_check_rubric_text`), each taking `text: str` and returning `list[str]` failure messages, never raising or printing — mirroring `check-agent.py`'s `_check_agent_text` contract, doubled to three sources per the plan's Pitfall 3 guidance.
- A single shared `_BOUND` module constant (`"at most one re-perception pass"`) asserted against both `SKILL-body.md` (L1) and `validation-rubric.md` (L8) — this one constant IS cross-file drift assertion D1: the two prose sites cannot diverge without editing the constant, which fails both files at once.
- Scoped assertions S1 (the `3. **Repeat**` line contains `re-perception pass`), S2 (the Phase 3 exit-criterion line contains both the preserved completeness claim L10a and the new re-entry exception clause L10b), and S3 (exactly one paragraph inside `### Turn discipline` contains the bound, and that paragraph names `second-order` — the only assertion protecting the second-order→Phase 2 edge, which has no site-of-trigger sentence of its own).
- `--self-test` running: 1 positive control (live tree must be clean), 13 negative controls (N1-N13, each mutating an in-memory copy of exactly one real file), 2 anti-masking controls (proving a failure names the correct source file and not the other), and 2 anchor-arity controls (proving a duplicated S1/S2 anchor reports "expected exactly one" rather than silently matching the first). All 19 controls pass.
- Three on-disk falsification probes (Task 3): stripped L1 from `SKILL-body.md`, L5 from `input-contract.md`, and L8 from `validation-rubric.md` on the real files, confirmed the gate exits 1 naming the correct source file each time, then restored each file with `git checkout --` and confirmed the gate returns to exit 0 with a clean `git status`.
- Confirmed via `git diff --name-only -- scripts/check-firewall-battery.sh shared first-principles` (empty output) that no out-of-scope file was touched, and via `bash scripts/check-firewall-battery.sh` (run for information only, not as the acceptance signal) that the tally is unchanged at 16/17, with the sole failure still `VAL-03` for the pre-existing reason `No module named pytest` (confirmed directly via `python3 -m pytest scripts/check-links_anchors_test.py -q`).

## Task Commits

1. **Task 1 + Task 2 (combined): Write the HARN-02 checker core, CLI, and self-test** - `babb142` (feat)
   - Task 3 (falsification probes + non-regression proof) is verification-only and produced no additional file diff; its evidence is recorded below under "Task 3 Verification Evidence."

## Files Created/Modified

- `scripts/check-loop-closure.py` (new) - HARN-02 gate: three pure check functions over three `shared/` source strings, a shared `_BOUND` constant, an aggregator, a live-tree CLI path, and a 19-control `--self-test`.

## Exact Literal Set the Gate Asserts

Matches this plan's `<gate_contract>` exactly — no literal from either 02-01 or 02-02 required rewording, confirmed against both SUMMARYs before writing the checker and re-verified with a direct `text.count()` sanity script against the real files before finalizing the design.

`shared/spine/SKILL-body.md` — must CONTAIN: L1 `at most one re-perception pass` (occurs once), L2 `unresolved gap with a confidence caveat` (occurs **twice** — see Deviations), L3 `returns to Phase 1 to re-frame the Essence Statement` (once), L4 `name which re-entry edge fired` (once); must NOT contain: X1 `until every criterion clears the gate` (confirmed absent); scoped: S1 (`3. **Repeat**` line contains `re-perception pass`), S2 (`**Exit criterion:** All ground truths have stable IDs` line contains both L10a `complete enough that Phase 4 can reason upward` and L10b `re-entry`), S3 (exactly one Turn discipline paragraph contains L1 and also contains `second-order`).

`shared/agent/input-contract.md` — must CONTAIN: L5 `not only before the analysis starts`, L6 `does not confirm framing on every delegation`, L7 `AskUserQuestion`, L7b `` If `AskUserQuestion` is unavailable at runtime `` (all occur once each).

`shared/spine/references/validation-rubric.md` — must CONTAIN: L8 `at most one re-perception pass` (the same `_BOUND` constant as L1 — D1), L9 `Turn discipline`; must NOT contain: X2 `revise the analysis and re-score from the beginning` (confirmed absent from the exact literal string; see Threat Flags below for a related but out-of-scope residual finding).

## Task 3 Verification Evidence

**Falsification probe 1 — `SKILL-body.md`, strip L1 on disk:**
```
check-loop-closure: FAIL — SKILL-body.md: missing the re-entry bound ("at most one re-perception pass")
check-loop-closure: FAIL — SKILL-body.md: expected exactly one paragraph in Turn discipline containing the bound ("at most one re-perception pass"), found 0
exit=1
```
Restored with `git checkout -- shared/spine/SKILL-body.md`; gate then printed `check-loop-closure: PASS` and `git status --porcelain shared/spine/SKILL-body.md` was empty.

**Falsification probe 2 — `input-contract.md`, strip L5 on disk:**
```
check-loop-closure: FAIL — input-contract.md: missing the mid-run scope clause ("not only before the analysis starts")
exit=1
```
No message named `SKILL-body.md`. Restored with `git checkout -- shared/agent/input-contract.md`; gate returned to `PASS`, file clean.

**Falsification probe 3 — `validation-rubric.md`, strip L8 on disk:**
```
check-loop-closure: FAIL — validation-rubric.md: missing the re-entry bound ("at most one re-perception pass")
exit=1
```
Restored with `git checkout -- shared/spine/references/validation-rubric.md`; gate returned to `PASS`, file clean.

**Non-regression gates, all exit 0:** `check-loop-closure.py --self-test`, `check-loop-closure.py`, `sync-content.py --check`, `sync-content.py --self-test`, `check-agent.py --self-test`, `check-agent.py --file first-principles/agents/first-principles.md`, `check-links.py`, `check-version-stamps.py`, `check-quality-harness.py --self-test`.

**Scope confirmation:** `git diff --name-only` and `git status --porcelain` after all three probes and restores show the tree clean except for the single committed addition, `scripts/check-loop-closure.py`. `git diff --name-only -- scripts/check-firewall-battery.sh shared first-principles` produced no output — nothing in those three paths changed.

**Battery run (informational only, not the acceptance signal, per this plan's own instruction and Pitfall 7):** `bash scripts/check-firewall-battery.sh` reports `FIREWALL: RED (1 gate(s) failed; 16/17 passed)`, sole failure `VAL-03`. Confirmed the underlying reason is unchanged: `python3 -m pytest scripts/check-links_anchors_test.py -q` → `No module named pytest`. This is the pre-existing, unrelated environment gap documented in `02-RESEARCH.md` Pitfall 7 and both prior plans' SUMMARYs — not a regression introduced here.

**Battery registration is deliberately deferred.** `scripts/check-firewall-battery.sh` was read (lines 150-180) for its registration shape only, per Task 3's `<read_first>` instruction, and was not modified. Adding a `gate "HARN-02" ...` line and moving the printed tally past 17 is Phase 4's HARN-04, not this plan's — confirmed untouched by the scope-confirmation diff above.

## Decisions Made

- Combined Task 1 and Task 2 into a single commit (`babb142`) rather than an intermediate stub-then-fill sequence — both tasks build the same one file this plan is scoped to (`files_modified: [scripts/check-loop-closure.py]`), and a stub commit followed immediately by an overwrite commit would have added process noise without adding review value. Task 3 produced no additional diff (it is a verification-only task: three on-disk probe-and-restore cycles plus a set of non-regression gate runs), so it has no commit of its own — its evidence is recorded in this SUMMARY's "Task 3 Verification Evidence" section instead.
- Followed all three of the plan's `<resolved_design_decisions>` exactly as written (qualitative bound token, new dedicated script, rubric edit treated as required) — none were reopened, per the plan's own instruction.
- Chose to strip every occurrence of a target literal, rather than a single site, for the six whole-text "must CONTAIN" negative controls (N1-N4, N9-N11) — see Deviations below for why this was necessary for N4 specifically, and why it was then applied uniformly to the rest of that class of control for consistency and to guard against a future duplication of any of the other five literals going undetected the same way.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] N4's negative control wrongly passed because L2 is stated twice in the real source text**
- **Found during:** Task 2, first `--self-test` run (`check-loop-closure --self-test: N4 (body: strip L2 degradation path) FAIL — WRONGLY PASSED (expected a failure, got none)`)
- **Issue:** `_DEGRADE` (`"unresolved gap with a confidence caveat"`) occurs twice in `shared/spine/SKILL-body.md` as authored by plan 02-01 — once in the canonical Turn discipline bound paragraph, once in the Repeat item's own sentence (`"report it as an unresolved gap with a confidence caveat instead of fixing it again"`). N4's first draft used a single-site `str.replace(target, "REMOVED", 1)`, per the plan's stated preference for single-site substitution over a regex sweep. That preference is correct for a scoped, single-line/paragraph assertion, but wrong for a whole-text `target not in text` presence check: removing only one of the two copies left the second copy standing, so the text-wide assertion never fired — the negative control was not load-bearing.
- **Fix:** Added a `_strip_everywhere()` helper (removes ALL occurrences, asserting at least one exists) and used it for the six whole-text presence negative controls (N1-N4, N9-N11). The four line/paragraph-scoped controls (N6-N8, N13) were left on the single-site `_replace_once`/`_mutate_line` path, since their targets were independently confirmed (via a direct `.count()` check against the real, scoped text) to occur exactly once within their scoped line or paragraph — the single-site guidance is correct there.
- **Files modified:** `scripts/check-loop-closure.py` (within the same, not-yet-committed working state — the fix landed before the Task 1+2 commit, so it does not appear as a separate commit)
- **Verification:** Re-ran `python3 scripts/check-loop-closure.py --self-test`; all 19 controls, including N4, now report PASS. Confirmed by direct inspection that L1, L3, L4, L5, L6, L8 each occur exactly once in their respective real files (a Python one-liner count check), so the fix's scope is limited to N4's actual defect and does not mask a similar problem elsewhere.

---

**Total deviations:** 1 auto-fixed (1 bug in the gate's own self-test design, caught by the self-test itself before any commit).
**Impact on plan:** The fix strengthens exactly the property Task 2's `<action>` calls out as load-bearing ("Every negative control fails for the EXPECTED reason, matched against the failure message, not merely because some failure occurred") — it is a correction within Task 2's own stated scope, not new scope. No plan file, requirement, or literal was reworded.

## Issues Encountered

- See the auto-fixed N4 issue above — resolved before the first commit, so the committed script never carried the WRONGLY-PASSED control.

## Threat Flags

| Flag | File | Description |
|------|------|--------------|
| threat_flag: unbounded-residual (informational, out of scope) | `shared/spine/references/validation-rubric.md` | The file's final "Usage Note" section (line 396-397, untouched by plans 02-01/02-02/02-03) reads: `"If either condition is not met, revise the relevant sections and re-score from the beginning."` This is a *different* sentence from X2 (`"revise the analysis and re-score from the beginning"`) — it says "the relevant sections," not "the analysis" — so it does not match X2's pinned literal and this gate correctly reports X2 absent. It still restates the same unbounded "re-score from the beginning" idea, sitting a few lines below plan 02-02's already-bounded rubric instruction at line 29. This gate's `<gate_contract>` did not name this second sentence, `files_modified` for this plan names only `scripts/check-loop-closure.py`, and this plan's scope is the gate script, not `shared/` prose — so it was not fixed here. Flagged for whoever next touches `validation-rubric.md` or extends this gate. |

## Next Phase Readiness

- `python3 scripts/check-loop-closure.py --self-test` exits 0 (all 19 controls PASS) and `python3 scripts/check-loop-closure.py` exits 0 against the live tree, both independently re-confirmed after the on-disk falsification probes were restored.
- `grep -c "import yaml" scripts/check-loop-closure.py` returns 0 — stdlib-only confirmed.
- All nine non-regression gates named in the plan's `<verification>` block exit 0; the tree is clean of everything except the one committed file; `scripts/check-firewall-battery.sh` is byte-identical to the pre-plan tree (confirmed via the scope-confirmation diff) and its printed tally is unchanged at 17 gates registered, 16 passing (VAL-03's pre-existing pytest gap unaffected).
- HARN-02 is satisfied and standalone-runnable. Phase 4's HARN-04 (adding a `gate "HARN-02" ...` line to `scripts/check-firewall-battery.sh` and moving the printed tally past 17) has no work already done against it — confirmed by the untouched-battery-file evidence above, so the next phase should not assume registration was forgotten.
- The Threat Flags entry above (the rubric's still-unbounded Usage Note sentence) is a candidate finding for whoever next edits `validation-rubric.md` — it is a pre-existing residual, not something this plan introduced or was scoped to fix.

---
*Phase: 02-loop-closure*
*Completed: 2026-08-28*

## Self-Check: PASSED

- FOUND: scripts/check-loop-closure.py
- FOUND commit: babb142
