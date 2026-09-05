---
phase: 18-exemplar-conformance
plan: 14
subsystem: check-conf-gate.py (CONF-GATE) — documentation reconciliation
tags: [gap-closure, doc-sweep, CONF-GATE, WR-08, residual-ledger]
dependency-graph:
  requires: [18-13]
  provides: [WR-08-closed]
  affects: [CLAUDE.md, docs/ARCHITECTURE.md, .githooks/pre-commit, scripts/git-hooks/pre-commit]
tech-stack:
  added: []
  patterns:
    - "re-derive the published figure from the command's own output at edit time, never transcribe a number from a prior SUMMARY or plan"
    - "tree-wide sweep pattern wide enough to catch both an alternate spelling and an out-of-file-list surface, replacing a narrow two-file grep -c predicate"
decisions:
  - "No code change to scripts/check-conf-gate.py in this plan, per its own scope boundary — it is the fourth and final plan in this gap-closure round, reconciling a settled figure rather than moving it."
  - "Left nine WR/IN findings from 18-REVIEW.md open by explicit disposition rather than closing a fourth round against the phase's rework cap of 2 (already at round 3 on explicit instruction)."
metrics:
  duration: "~35 minutes"
  completed: "2026-09-05"
---

# Phase 18 Plan 14: Close WR-08 — reconcile CONF-GATE doc rows and hook mirrors with the 42-control end state Summary

Closed WR-08 from `18-REVIEW.md`, the last of the four BLOCKER-adjacent findings this gap-closure
round targets. Three tracked surfaces stated a stale CONF-GATE control count or a stale battery
count as current fact — `CLAUDE.md:39` said "18 controls" (actual 42, after plans 18-11..18-13
moved it 32 → 42), and both pre-commit hook mirrors said "the offline battery stays at 24"
(actual 25, corrected by plan 18-10 everywhere else but these two lines). Root cause: plan
18-10's own verification predicate (`grep -c "18-control" CLAUDE.md docs/ARCHITECTURE.md`) was
scoped to the hyphenated spelling and to two files, so the spaced form `18 controls` and both
hook copies were structurally invisible to it — the exact drift class this phase exists to stop,
reproduced on the phase's own paperwork. Task 1 corrected all three literals and widened both
CONF-GATE doc rows to describe the shipped enforcement (comment-stripped census, roster equality
lock, per-surface population floors, controllable D-08 arm) and its disclosed bounds. Task 2
re-swept with a predicate wide enough to have caught 18-10's own miss and recorded the full
nineteen-row `18-REVIEW.md` WR/IN residual ledger. Battery unmoved, `GREEN (25/25)`; no gate id,
CI job or battery slot added — this round adds controls inside an existing gate, never a new one.

## What Was Built

**Task 1 (WR-08).** Re-derived the control count live: `python3 scripts/check-conf-gate.py
--self-test` → `check-conf-gate: SELF-TEST PASS — 42 controls run` (verbatim, quoted again under
Verification below). Edited, in one commit:

- `CLAUDE.md:39` — `(18 controls)` → `(42 controls)`.
- `.githooks/pre-commit:20` and `scripts/git-hooks/pre-commit:18` — `so the offline battery stays
  at 24.` → `so the offline battery stays at 25.`, both files, same commit.
- `CLAUDE.md:174` (the `| CONF-GATE |` row) — `32-control` → `42-control`; `six enforcement call
  sites` → `seven enforcement call sites` (plan 18-12 adds `_population_floor_problems` as the
  seventh); added the four enforcement properties plans 18-11..18-13 shipped (comment-stripped
  census / BL-01, roster equality lock against `_LIVE_CALL_SITES_LOCK` / BL-02, per-surface
  `_POPULATION_FLOORS` denominator floors / BL-03, the D-08 arm returning problems instead of
  exiting with offline controls over its four internal predicates / BL-04-WR-06); amended the
  "What it does not assert" clause to move the commented-out case onto the CAUGHT side and add the
  population floor's shrinkage-not-substitution bound and the D-08 controls' falsifiability-not-
  corpus-meaning bound.
- `docs/ARCHITECTURE.md:153` (the `| CONF-GATE |` row) — same corrections in the row's shorter
  register: `32-control` → `42-control`, one clause naming the four new enforcement properties,
  and the existing "Does not assert" sentence extended with the shrinkage-not-substitution bound.

Left untouched, as the plan's scope boundary requires: `docs/conformance-baseline.md` (states the
ratchet figure 4, unmoved by this round), `docs/v8.0-final-closure.md` (historical, states no
count), and `scripts/check-firewall-battery.sh` (battery count 25, already correct).

**Task 2 (sweep + ledger).** No shipped file changed. Produced the tree-wide sweeps, the width
demonstration and the residual ledger recorded below.

## Re-derivation (verbatim, the figure every edit above uses)

```
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST PASS — 42 controls run
```

rc 0.

## Sweep 1 — control counts, both spellings, tracked surfaces (verbatim, classified)

```
$ /usr/bin/grep -rnE '\b[0-9]+[- ]controls?\b' CLAUDE.md docs/ .githooks/ scripts/ .github/
CLAUDE.md:37:...# PROV-GUARD: provenance-verifier self-test (24 controls)
CLAUDE.md:39:...# CONF-GATE: exemplar-conformance comparator self-test (42 controls)
CLAUDE.md:168:| HARN-01 | ... (58 controls); an anti-masking assertion fails the gate ...
CLAUDE.md:173:| PROV-GUARD | ... The self-test's 24 controls are tempdir/in-memory ...
CLAUDE.md:174:| CONF-GATE | ... a 42-control offline `--self-test` floored ... (four new BL-01..BL-04 clauses)
docs/v8.18-praor-loop-closure.md:114:...for **47 controls in total**. Re-verification on
docs/whole-system-remeasure-verdict.md:93:...S-N01/02/03/04 controls) | broader bar |
docs/ARCHITECTURE.md:147:| HARN-01 | ... (58 controls); an anti-masking assertion ...
docs/ARCHITECTURE.md:153:| CONF-GATE | ... a 42-control offline `--self-test`, which now enforces ...
scripts/check-act-limb-branches.md:187:- [x] Self-test exits 0 with all 58 controls (50 from phases 1-7 + 8 from phase 8)
scripts/check-focused-parity.py:1913,1925,1933,1976,1988,1999,2009,2066,2075,2080,2092,2119,2156:
    (comment labels "Agent-N control" / "Parity-N control" — coincidental digit-space-control matches)
scripts/check-provenance.py:1627:"""D-16 control battery: positive and negative controls for every named
scripts/check-registration.py:1581:"check-registration --self-test: PASS (29 controls: discovery "
scripts/check-conf-gate.py:180:...byte-identical generated twin left `--self-test` at 34 controls and the
scripts/check-conf-gate.py:333:...`--self-test` still reported `SELF-TEST PASS — 32 controls run` at rc 0.
scripts/check-quality-harness.py:571,2764,2797,2805,3141,16752: "item N control N" (QUAL-01's own numbering)
scripts/check-selfaudit-scan.py:568:# per-literal Rubric-11 controls below (plan 15-12, closing WR-01):
```

Classification (every hit):

| Hit | Class | Reason |
|---|---|---|
| `CLAUDE.md:37` (24 controls, PROV-GUARD) | (b) | PROV-GUARD's own current figure, unrelated to CONF-GATE |
| `CLAUDE.md:39` (42 controls, CONF-GATE) | (a) | current CONF-GATE figure, now correct |
| `CLAUDE.md:168` (58 controls, HARN-01) | (b) | HARN-01's own current figure |
| `CLAUDE.md:173` (24 controls, PROV-GUARD prose) | (b) | PROV-GUARD's own current figure |
| `CLAUDE.md:174` (42-control, CONF-GATE row) | (a) | current CONF-GATE figure, now correct |
| `docs/v8.18-praor-loop-closure.md:114` (47 controls) | (b) | historical HARN-01 milestone record, unrelated to CONF-GATE |
| `docs/whole-system-remeasure-verdict.md:93` (04 controls) | (b) | routing-battery measurement doc, unrelated to CONF-GATE, coincidental digit match |
| `docs/ARCHITECTURE.md:147` (58 controls, HARN-01) | (b) | HARN-01's own current figure |
| `docs/ARCHITECTURE.md:153` (42-control, CONF-GATE row) | (a) | current CONF-GATE figure, now correct |
| `scripts/check-act-limb-branches.md:187` (58 controls) | (b) | HARN-01's own current figure |
| `scripts/check-focused-parity.py` (13 hits, "Agent-N control"/"Parity-N control") | (b) | comment labels, coincidental digit-space-"control" match, not a count claim at all |
| `scripts/check-provenance.py:1627` (D-16 control battery) | (b) | PROV-GUARD's own docstring, coincidental match ("16 control") |
| `scripts/check-registration.py:1581` (29 controls) | (b) | REG-GUARD's own current figure |
| `scripts/check-conf-gate.py:180` (34 controls) | (b) | historical narrative comment recording plan 18-12's own BL-03 measurement at the time it was taken, not a current-fact claim |
| `scripts/check-conf-gate.py:333` (32 controls) | (b) | historical narrative comment recording plan 18-11's own BL-02 measurement at the time it was taken, not a current-fact claim |
| `scripts/check-quality-harness.py` (6 hits, "item N control N") | (b) | QUAL-01's own internal fixture numbering, coincidental match |
| `scripts/check-selfaudit-scan.py:568` (Rubric-11 controls) | (b) | SCAN-GUARD's own docstring, coincidental match ("11 controls") |

**Zero hits classified (c).** No stale CONF-GATE control-count statement remains.

## Sweep 2 — battery counts (verbatim, classified)

```
$ /usr/bin/grep -rn "battery stays at\|offline battery\|24/24\|25/25" CLAUDE.md docs/ .githooks/ scripts/ .github/
CLAUDE.md:186:...currently **25/25**... QUAL-01 ... moved the battery from 15 to 16; VERSION-01 ...
    moved it from 16 to 17; HARN-01/02/03 ... moved it from 17 to 20; HC-BOUND ... moved it from
    20 to 21; REG-GUARD ... moved it from 21 to 22; PROV-GUARD ... moved it from 22 to 23;
    SCAN-GUARD ... moved it from 23 to 24. CONF-GATE ... moved it from 24 to 25. ...
docs/audit-2026-08-16-duplication-staleness.md:17:...wired into CI and the offline battery (16 → 17 gates)...
docs/v8.18-praor-loop-closure.md:136:...moving the offline battery's tally from **17 → 20**...
docs/v8.7-constraint-teardown.md:241:...offline battery, or pytest. Both are recorded here...
docs/whole-system-remeasure-verdict.md:24:...this phase stops at "surface reconciled + offline battery green."
docs/whole-system-remeasure-verdict.md:147:...full offline battery green — STRENGTHEN
docs/CONFIGURATION.md:156:...deliberately not registered in the offline battery or in CI (D-06).
docs/MEASUREMENT-MAP.md:23:...and QUAL-01 runs only in the offline battery. ...
docs/README.md:50,52,79,105,192: (historical milestone prose; :105 states "battery 15/15 → 25/25")
docs/v8.0-final-closure.md:21,112,113: (historical; "battery 15/15 GREEN" ... "it is 25/25 today")
docs/ARCHITECTURE.md:122:...**25 tallied in the offline battery**...
.githooks/pre-commit:20:...so the offline battery stays at 25.
scripts/git-hooks/pre-commit:18:...so the offline battery stays at 25.
scripts/check-firewall-battery.sh:4:# One-shot offline battery runner — Phase 128 READY-03 (D-06).
scripts/check-traceability.py:5087:..."The offline battery moved 17 → 20 and coverage is now {_prose}."
```

Classification: every current-fact hit states **25** (`CLAUDE.md:186`'s "25/25" and its own
25-step derivation chain ending "CONF-GATE ... moved it from 24 to 25"; `docs/ARCHITECTURE.md:122`'s
"25 tallied"; both hook files' "stays at 25"; `docs/README.md:105` and `docs/v8.0-final-closure.md:112-113`'s
"25/25 today"). Every bare `24` appears only inside a historical delta transition (`23 to 24`,
`24 to 25`) or a milestone-scoped narration of a prior count (`16 → 17`, `17 → 20`), never as a
bare current-fact `24`. `check-traceability.py:5087` is a synthetic in-code fixture string
(`_i2_unrelated_line`), not a document claim. **Zero class (c) hits** — no bare current-fact `24`
for the battery remains anywhere in the swept surfaces.

## Sweep 3 — the hook mirror (verbatim diff)

```
$ diff .githooks/pre-commit scripts/git-hooks/pre-commit
3,9c3
< # Opt in:  git config core.hooksPath .githooks
< #
< # Mirrors scripts/git-hooks/pre-commit verbatim (module logic; header prose
< # and printf-vs-echo usage differ cosmetically between the two files, a
< # pre-existing asymmetry). The body-budget gate that used to run here was
< # retired under TEARDOWN-01 (docs/v8.7-constraint-teardown.md) -- see
< # scripts/check-body-budget.py, which now always exits 0.
---
> # Installed by scripts/install-hooks.sh as .git/hooks/pre-commit (symlink).
12c6,10
< # diverged (scripts/sync-content.py --check).
---
> # diverged (scripts/sync-content.py --check). The body-budget gate that used
> # to run alongside it was retired under TEARDOWN-01
> # (docs/v8.7-constraint-teardown.md) -- the reporting script
> # (scripts/check-body-budget.py) now always exits 0, so gating a commit on it
> # here would be dead weight.
20a19,20
> #
> # POSIX sh only -- no bashisms. Quote all expansions.
33,34c33,34
<     echo "pre-commit: neither 'uv' nor 'python3' on PATH." >&2
<     echo "  Install one of them, or bypass this hook with 'git commit --no-verify'." >&2
---
>     printf "pre-commit: neither 'uv' nor 'python3' on PATH.\n" >&2
>     printf "  Install one of them, or bypass this hook with 'git commit --no-verify'.\n" >&2
38c38
< # --- Gate 1: sync-drift gate (preserved verbatim from prior version) --------
---
> # --- Gate 1: sync-drift gate (compositional preservation) --------------------
```

All differences are the documented cosmetic asymmetry (`.githooks/pre-commit:5`'s own stated
"header prose and printf-vs-echo usage differ cosmetically"). The D-06 sentence this plan edits is
byte-identical in both files, confirmed directly:

```
$ sed -n '20p' .githooks/pre-commit; sed -n '18p' scripts/git-hooks/pre-commit
# .github/workflows/validation.yml, so the offline battery stays at 25.
# .github/workflows/validation.yml, so the offline battery stays at 25.
```

Nothing enforces this mirror (IN-09, below, stays open) — this is a hand-verified property, not a
gated one, and it was verified by hand in this same commit.

## Width demonstration — the new predicate reaches what 18-10's own predicate could not

Method: reconstructed the pre-Task-1 state on a disposable scratch copy (`CLAUDE.md`,
`docs/ARCHITECTURE.md` and both hook files copied out of the worktree, then the three literals
this plan just fixed were re-inserted by `sed`), never mutating the real tree. `git status
--porcelain` on the real tree was empty before and after.

```
$ /usr/bin/grep -c "18-control" width-demo/CLAUDE.md width-demo/ARCHITECTURE.md
width-demo/CLAUDE.md:0
width-demo/ARCHITECTURE.md:0

$ /usr/bin/grep -n '\b18[- ]controls\?\b' width-demo/CLAUDE.md width-demo/ARCHITECTURE.md
width-demo/CLAUDE.md:39:...# CONF-GATE: exemplar-conformance comparator self-test (18 controls)

$ /usr/bin/grep -n "battery stays at 24" width-demo/githooks-pre-commit width-demo/scripts-git-hooks-pre-commit
width-demo/githooks-pre-commit:20:# ...so the offline battery stays at 24.
width-demo/scripts-git-hooks-pre-commit:18:# ...so the offline battery stays at 24.
```

18-10's predicate (`grep -c "18-control" CLAUDE.md docs/ARCHITECTURE.md`) returns **0 hits** on
all three reconstructed residual sites — exactly reproducing why 18-10 shipped them undetected.
Sweep 1's wider pattern (spaced spelling, `\b18[- ]controls?\b`) catches the `CLAUDE.md:39`
residual by itself; Sweep 2's pattern (`battery stays at 24`, run against both hook files, which
18-10's file list never named) catches the other two. Together the two sweep patterns return all
**3** residual sites 18-10 missed, on both axes named in the finding: the alternate spelling and
the out-of-file-list surface. The scratch copy was discarded immediately after.

## Residual Ledger

This gap-closure round (plans 18-11 through 18-14) closed the four BLOCKER findings
(BL-01, BL-02, BL-03, BL-04) and the three stale-figure residuals (WR-08); the rest of
`18-REVIEW.md`'s WARNING and INFO findings are deliberately left open, per the phase's rework cap.

| ID | Finding | Disposition | Backlog candidate? |
|---|---|---|---|
| WR-01 | `if problems:` → `if False:` silently suppresses the whole failure report | OPEN | Yes — pair with IN-04 (the row-sourced D-03 loop the behavioural `run_live(rows)` fix depends on); a repo-wide accepted bound QUAL-01's and SCAN-GUARD's own censuses disclose for themselves, not unique to CONF-GATE |
| WR-02 | `contract-surface-excluded` is vacuous for 2 of 3 comparators it claims to cover | OPEN | Yes — a control-fixture strengthening, not a corpus/enforcement hole; low urgency |
| WR-03 | `report-conformance.py` has zero CI/battery coverage | OPEN — explicitly out of this round's scope fence (no new gate id, CI job, or battery slot permitted) | Yes — deliberately deferred; needs a new `CONF-MEAS` gate id, which is new-gate scope this round forbids by design |
| WR-04 | Documented exit code 2 is unreachable (import failure exits 1 with a traceback) | OPEN | Yes — minor, low urgency |
| WR-05 | `_claim_floor_problems` silently skips an unreadable floored file, no report | OPEN | Yes — minor, low urgency |
| WR-06 | `_run_d08_arm` exits the process from inside a helper | **CLOSED by plan 18-13** (confirmed against `18-13-SUMMARY.md`: "provides: [BL-04-closed, WR-06-closed]") | — |
| WR-07 | `heading_malformed_blocks` sum scope load-bearing and uncontrolled | **CLOSED by plan 18-12** (confirmed against `18-12-SUMMARY.md`: "provides: [BL-03-closed, WR-07-closed]") | — |
| WR-08 | Three surfaces state stale counts; 18-10's own predicate could not see them | **CLOSED by plan 18-14** (this plan) | — |
| WR-09 | 13 of 14 claim floors protected only by an adjacent copy-paste block | OPEN | Yes — the loosening direction is still a reviewable source diff, and BL-03's population floors independently reduce the exposure; accepted as-is for this milestone |
| WR-10 | `report-conformance.py --self-test` prints a `DRIFT:` block on a clean pass | OPEN | Yes — cosmetic (stderr noise), not a correctness defect |
| IN-01 | Unused `discover_artifacts` re-export | OPEN | No — trivial, accepted as-is |
| IN-02 | Dead `isinstance(..., int)` guard in the marked-total computation | OPEN | No — trivial, accepted as-is |
| IN-03 | Published prose says "carry the marker"; column counts marked among *untraced* only | OPEN | Yes — a one-word disclosure-prose fix (`docs/conformance-baseline.md`), low urgency |
| IN-04 | (CONVENTION) live leg re-reads/re-measures all 28 gated artifacts from disk a second time | OPEN | Yes — pairs with WR-01's behavioural fix |
| IN-05 | (CONVENTION) `_CONTROLS` types callables as `object` | OPEN | No — repo-wide pattern (also in `report-conformance.py`), not a new deviation |
| IN-06 | The control roster lock (`_CONTROL_IDS`) is id-only and set-compared | OPEN | Yes — same shape as other id-only rosters in the repo; low urgency |
| IN-07 | `live-call-site-census` is a strict subset of `live-call-form-lock` | OPEN | No — an inflated-count observation, not a defect |
| IN-08 | `product-business-2.md` defines chain C2 and never cites it in §6 | OPEN | No — permitted by `output-template.md`; fixing BL-03 (done) already removed the exposure this enabled |
| IN-09 | (CONVENTION) the two pre-commit hook copies are hand-mirrored with no drift gate | OPEN — demonstrated hand-verifiable this round (Sweep 3), still not gated | Yes — either generate one from the other or add a normalized-body equality assertion to `scripts/install-hooks.sh` |

All nineteen `18-REVIEW.md` WR-01..WR-10 / IN-01..IN-09 findings are named above with exactly one
disposition each, cross-checked against the three preceding plans' own SUMMARYs (not this plan's
prior expectation) for the three CLOSED entries.

## Verification (run in order, from the repo root)

1. `python3 scripts/check-conf-gate.py --self-test` → `check-conf-gate: SELF-TEST PASS — 42
   controls run`, rc 0
2. `python3 scripts/check-conf-gate.py` → `COVERAGE — measured 28 artifacts across
   shared-examples, generated-twin`, three `D-08(a)/(b)/(c) ... 0 -> 1` lines, `check-conf-gate:
   PASS`, rc 0
3. `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (25/25)`, rc 0 (a fresh worktree
   again reported `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 24/25 passed)` on the first run
   because no interpreter could import pytest for VAL-03's third leg; ran `uv sync` to materialize
   `.venv`, resolving the prerequisite — an environment setup step, not a code change; `.venv`
   stays gitignored)
4. `python3 scripts/check-registration.py --self-test && python3 scripts/check-registration.py` →
   both rc 0
5. `python3 scripts/check-links.py` → `check-links: PASS (244 markdown links + 6 namespace refs
   across 128 files)`, rc 0
6. `python3 scripts/report-conformance.py --check` → `report-conformance: PASS — no drift`, rc 0
7. `python3 scripts/sync-content.py --check` → rc 0
8. `git status --porcelain` → exactly the four `files_modified` (`CLAUDE.md`,
   `docs/ARCHITECTURE.md`, `.githooks/pre-commit`, `scripts/git-hooks/pre-commit`), confirmed
   after Task 1's commit and unchanged through Task 2 (which touches no shipped file)
9. `git diff --stat scripts/check-quality-harness.py` → empty (CONTRACT-06 intact across the
   whole gap-closure round)

## Source Assertions

- `/usr/bin/grep -n "18 controls\|18-control" CLAUDE.md docs/ARCHITECTURE.md` → no hits (exit 1).
- `/usr/bin/grep -rn "battery stays at 24" .githooks/pre-commit scripts/git-hooks/pre-commit` → no
  hits (exit 1); `/usr/bin/grep -rn "battery stays at 25" .githooks/pre-commit
  scripts/git-hooks/pre-commit` → exactly one hit in each file.
- `/usr/bin/grep -c "32-control" CLAUDE.md docs/ARCHITECTURE.md` → `0` for both files.
- `/usr/bin/grep -n "six enforcement call sites" CLAUDE.md` → no hits (exit 1);
  `/usr/bin/grep -c "seven enforcement call sites" CLAUDE.md` → `1`.
- `git diff --stat CLAUDE.md docs/ARCHITECTURE.md` → `CLAUDE.md | 4 ++--` and
  `docs/ARCHITECTURE.md | 2 +-` — line-count-only edits, no structural change.

## Deviations from Plan

None — both tasks executed exactly as written. Task 1's doc-row rewrites folded in the four
BL-01..BL-04 enforcement properties as separate clauses appended to the existing sentence
structure (rather than replacing the whole sentence), which was a judgment call on presentation,
not a substantive deviation — every required literal, count and disclosed-bound clause the
acceptance criteria name is present and independently grep-confirmed above.

## Assumption Drift (advisory)

None material. This plan's own note flagged plan 18-13's N18 residual (the mandated call-form
literal makes the pre-refactor fragment a strict substring of the new one, invisible to the
containment-based form-lock check) as a disclosure this plan's residual ledger must carry
alongside the `18-REVIEW.md` findings — it is not a `18-REVIEW.md` WR/IN finding itself (it
originates in `18-13-SUMMARY.md`'s own Deviations section), so it is not double-counted in the
nineteen-row ledger above; it is recorded here instead, matching where `18-13-SUMMARY.md` already
disclosed it, with no new information added by this plan.

## Self-Check: PASSED

- `CLAUDE.md` contains `(42 controls)`, `42-control offline`, `seven enforcement call sites`,
  and no `(18 controls)` / `32-control` / `six enforcement call sites`: FOUND
- `docs/ARCHITECTURE.md` contains `42-control offline` and no `32-control`: FOUND
- `.githooks/pre-commit` and `scripts/git-hooks/pre-commit` both contain `stays at 25` and no
  `stays at 24`: FOUND
- Commit `9eff2b2` (Task 1) exists in `git log`: FOUND
- `python3 scripts/check-conf-gate.py --self-test` → 42 controls, rc 0: FOUND
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (25/25)`: FOUND
- `git status --porcelain` → clean after Task 1's commit, unaffected by Task 2: FOUND
