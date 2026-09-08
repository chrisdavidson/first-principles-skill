---
phase: 22-cap-the-recursion
plan: 01
subsystem: docs
tags: [process-contract, depth-rule, rework-cap, product-apparatus-split]
dependency_graph:
  requires: []
  provides:
    - "docs/PROCESS.md — canonical process contract (depth rule, product/apparatus split, rework cap, exception ledger)"
    - "docs/README.md nav row for docs/PROCESS.md"
  affects:
    - "22-04 (restores CR-05's 17 docs/README.md figures)"
    - "22-07 (widens LITERAL_SCAN_MD_GLOBS to include docs/PROCESS.md and CONTRIBUTING.md, ledgers this file's historical counts per D-22-A)"
tech_stack:
  added: []
  patterns:
    - "canonical single-page process contract, cited not restated (D-04)"
    - "claim-audience product/apparatus cut (D-01)"
    - "append-only exception ledger on a tracked, CONF-13-scanned surface (D-07)"
key_files:
  created:
    - docs/PROCESS.md
  modified:
    - docs/README.md
decisions:
  - "D-22-A: historical counts in docs/PROCESS.md attributed through per-hit ledger entries in plan 22-07, not a new LITERAL_EXEMPTION_CLASSES entry"
  - "D-22-B: rework cap's unit changes from plans to rounds, deviation stated explicitly in docs/PROCESS.md §3, not applied silently"
  - "D-22-C: CR-06's proposed follow-on heredoc/expansion control is declined under the depth rule (LEVEL move); recorded in ROADMAP backlog by plan 22-08"
  - "D-22-D: new ledger surfaces (docs/README.md, docs/PROCESS.md, CONTRIBUTING.md) get an explicit named backlog-id branch (999.44) rather than falling through to the 999.41 default, deferred to plans 22-04/22-07"
metrics:
  duration: "~45 minutes"
  completed: 2026-09-08
---

# Phase 22 Plan 01: Write the Process Contract Summary

`docs/PROCESS.md` written and registered in the `docs/README.md` nav — the canonical statement of
this project's stopping rule (the depth rule, the product/apparatus review split, and the rework
cap with its append-only exception ledger), deliberately landed in a commit that does not yet
register it in `LITERAL_SCAN_MD_GLOBS` (that widening is plan 22-07, per this plan's own ordering
constraint).

## What Was Built

**`docs/PROCESS.md`** (227 lines), in three tasks / three commits:

1. **§1 The depth rule + §1.1 REACH is not LEVEL + §1.2 CR-05 worked example, §2 Product and
   apparatus.** States the rule verbatim (`a guard guards the product; a guard is not itself
   guarded`), cites the `999.27 → 999.28 → 999.30` chain as measured justification, defines
   REACH vs. LEVEL in its own subsection citing `_py_docstring_scan_scripts()`'s in-repo
   precedent, writes CR-05 up as the rule's own worked example (with the corrected count of 17,
   not 16), and states D-01's product/apparatus cut by claim-audience with its blocking
   consequence.
2. **§3 The rework cap + §3.1 the append-only exception ledger.** States both limits (2
   gap-closure ROUNDS; a same-class trip), Phase 21's measured evidence (13 plans / 4 rounds
   against a cap of 2), the explicit plans-to-rounds deviation from `REQUIREMENTS.md` CONF-15 /
   ROADMAP criterion 4's wording (D-22-B), and backfills Phase 21's three `RECORDED EXCEPTION`
   blocks from `21-CONTEXT.md` as the ledger's founding rows — including round 2's exception
   having been written retroactively, discovered by the verifier rather than self-reported.
3. **`docs/README.md` nav registration.** One `## Core docs` table row in alphabetical position
   (between `METHODOLOGY-CHEATSHEET.md` and `TESTING.md`), naming all three rules with no stated
   count.

## Decisions Landed (binding on later plans in this phase)

- **D-22-A** — `docs/PROCESS.md`'s historical counts (13 plans, 4 rounds, 41%, 17 figures,
  `999.27 → 999.28 → 999.30`) are routed through per-hit `_DEFERRED_LITERAL_HITS` ledger entries
  in plan 22-07, not a new `frozen-historical-measurement` exemption class. No detector change;
  this plan touched no file under `scripts/`.
- **D-22-B** — the rework cap's unit changes from plans to rounds. `docs/PROCESS.md` §3 states
  the deviation in its own text, naming both the old wording (`REQUIREMENTS.md` CONF-15 / ROADMAP
  criterion 4) and the reason. Neither `REQUIREMENTS.md` nor `ROADMAP.md` is rewritten.
- **D-22-C** — CR-06's proposed follow-on heredoc/expansion control is declined as a LEVEL move
  under the depth rule this plan writes; the decline is recorded in the ROADMAP backlog by plan
  22-08, not silently dropped.
- **D-22-D** — new ledger surfaces (`docs/README.md`, `docs/PROCESS.md`, `CONTRIBUTING.md`) get
  an explicit named backlog-id branch (999.44) rather than falling through to the 999.41 default
  used for `.py#__doc__` keys. Plans 22-04 and 22-07 add the branches; plan 22-08 files the
  matching backlog entry.

## `docs/PROCESS.md` Link Targets

`docs/PROCESS.md` carries two relative links:

| Target | Resolved by |
|---|---|
| `docs/COMPONENT-DIAGRAM.md` (as `COMPONENT-DIAGRAM.md`) | Both — `python3 scripts/check-links.py` (VAL-03, `docs/*.md` glob) and by hand (`test -f docs/COMPONENT-DIAGRAM.md`) |
| `docs/ARCHITECTURE.md` (as `ARCHITECTURE.md`) | Both — `python3 scripts/check-links.py` (VAL-03, `docs/*.md` glob) and by hand (`test -f docs/ARCHITECTURE.md`) |

The inbound link, `docs/README.md` → `docs/PROCESS.md` (`[PROCESS.md](PROCESS.md)`), is also
covered by both VAL-03 and a hand `test -f`. All three links use the bare-filename convention
(no `docs/` prefix); `grep -c "](docs/" docs/PROCESS.md` returns `0`.

## `registered_surfaces` Before and After

| Measurement | Before this plan | After this plan |
|---|---|---|
| `registered_surfaces` (`gen-gate-docs.py --describe`) | 37 | **37 (unchanged)** |
| `checked_files` | 67 | 67 (unchanged) |
| `literal_scan_non_exempt` | 0 | 0 (unchanged) |

`docs/PROCESS.md` exists on disk but is not yet a member of `LITERAL_SCAN_MD_GLOBS` — confirmed
by `gen-gate-docs.py --check` passing with no ledger edit at every task boundary. The widening to
39 surfaces (adding `docs/PROCESS.md` and `CONTRIBUTING.md`) is plan 22-07's work, landing after
this file is fully committed, per this plan's own stated highest-risk ordering constraint
(`22-RESEARCH.md` §8 risk 1 / Pitfall 1).

## Verification

All 12 plan-level `<verification>` items run and passed on the live tree, in order:

1. `test -f docs/PROCESS.md` → exit 0
2. `grep -c "a guard guards the product; a guard is not itself guarded"` → 1
3. `grep -c "999.27 → 999.28 → 999.30"` → 1
4. `grep -c "gap-closure ROUND"` → 1
5. `grep -c "| Phase | Date | Rounds | Plans | Reason |"` → 1
6. `grep -c "\[PROCESS.md\](PROCESS.md)" docs/README.md` → 1
7. `python3 scripts/check-links.py` → exit 0 (312 markdown links + 6 namespace refs, 160 files)
8. `registered_surfaces` → 37 (unchanged)
9. `python3 scripts/gen-gate-docs.py --self-test` → exit 0 (74 controls)
10. `python3 scripts/gen-gate-docs.py --check` → exit 0
11. `sh .githooks/pre-commit` → exit 0 (all 5 pre-commit gates)
12. `grep -c "LITERAL_SCAN_MD_GLOBS" scripts/gen-gate-docs.py` unchanged at 2; `git diff --name-only <plan-base>..HEAD` contains only `docs/PROCESS.md` and `docs/README.md` — no `scripts/` path touched

Also independently re-run per task:
- Task 1 acceptance criteria (9 checks) — all passed, including `test -f docs/PROCESS.md`,
  the verbatim rule string, the chain literal, `### 1.1`/`### 1.2` headings exactly once each,
  `## 2. ` exactly once, `product findings block`/`auto-file` present, zero `](docs/` links, and
  `gen-gate-docs.py --check` exit 0.
- Task 2 acceptance criteria (9 checks) — all passed, including `## 3. The rework cap` exactly
  once, `gap-closure ROUND`, `same-class`, the quoted superseded wording, `### 3.1 ` exactly once,
  the ledger header exactly once, exactly 3 `| Phase 21 |` data rows, `not self-reported`, and the
  plan-number tokens `21-13`/`21-16`/`21-25`.
- Task 3 acceptance criteria (7 checks) — all passed, including the nav row inside `## Core docs`
  exactly once, `check-links.py` exit 0, `git diff --stat docs/README.md` showing exactly 1
  insertion / 0 deletions, both link targets resolved by hand, `registered_surfaces` still 37, and
  `sh .githooks/pre-commit` exit 0.

## Deviations from Plan

None — plan executed exactly as written. Both `git diff --stat docs/README.md` (1 insertion, 0
deletions) and the `scripts/`-path check confirm no scope leaked beyond the two named files.

## Worktree Environment Note (not a plan deviation)

The spawned worktree's `.planning/` directory (gitignored, not copied by `git worktree add`) was
absent at spawn time, and the initial `<worktree_branch_check>` compound script was rejected by
the sandbox as too complex to verify — so HEAD was still on a stale pre-reset commit
(`d4da381`, missing `scripts/gen-gate-docs.py` and other tracked files) when execution began.
Both were corrected before any file was written: `.planning/phases/22-cap-the-recursion/*.md`
were read directly from the main checkout (read-only, permitted across the filesystem), and the
worktree branch reset (`git symbolic-ref` / `git rev-parse --abbrev-ref HEAD` / `git merge-base` /
`git reset --hard 5712aaa...`) was re-run as separate, simple commands per the sandbox's
per-command complexity limit, landing HEAD at the correct expected base before any commit.

## Self-Check: PASSED

- `test -f docs/PROCESS.md` → FOUND
- `test -f docs/README.md` → FOUND (modified)
- `git log --oneline --all | grep -q 47da37d` → FOUND (task 1 commit)
- `git log --oneline --all | grep -q a3579fb` → FOUND (task 2 commit)
- `git log --oneline --all | grep -q 99a9065` → FOUND (task 3 commit)
- All plan-level `<verification>` commands re-run above with observed (not assumed) output.
