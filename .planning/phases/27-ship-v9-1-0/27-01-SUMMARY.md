---
phase: 27-ship-v9-1-0
plan: 01
subsystem: recurrence-reading-instrument
tags: [measurement, evidence-freeze, sweep-protocol, REL-08]
dependency-graph:
  requires: []
  provides:
    - "tests/recurrence-reading-v9.1/protocol.md (D-18's published sweep protocol)"
    - "tests/recurrence-reading-v9.1/README.md (frozen-evidence discipline + D-27-05 supersession)"
    - "_FROZEN_PATHS entry for tests/recurrence-reading-v9.1"
  affects:
    - "plan 27-03 (report-conformance.py reader that re-derives the sixth labelled surface)"
    - "plan 27-04 (pre-arm reading, fills pending chain-of-custody rows)"
    - "plan 27-09 (post-arm reading, fills remaining pending rows)"
tech-stack:
  added: []
  patterns:
    - "frozen human/agent-produced evidence, figure re-derived from it forever after (live-conformance mechanism, D-07)"
    - "in-process literal-scan testing of draft prose before writing to disk (Phase 26 precedent)"
key-files:
  created:
    - tests/recurrence-reading-v9.1/protocol.md
    - tests/recurrence-reading-v9.1/README.md
  modified:
    - scripts/check-firewall-battery.sh
decisions:
  - "D-27-01/02/03/04/05 (27-01-PLAN.md) all published verbatim in protocol.md/README.md, not re-derived"
metrics:
  duration: "~25 minutes"
  completed: "2026-09-10"
---

# Phase 27 Plan 01: Publish the Recurrence-Reading Sweep Protocol and Frozen-Evidence Directory Summary

Published the measurement instrument for REL-08's recurrence reading — the sweep protocol's own
text, the frozen-evidence directory discipline, and the `_FROZEN_PATHS` registration — before any
reading is taken and before any release act runs.

## What was built

**Task 1 — `tests/recurrence-reading-v9.1/protocol.md`.** The published sweep protocol: what is
counted (the quantity-shaped claim class per `docs/PROCESS.md` §2, cited not restated); the
product/apparatus surface lists in walk order; the hit criterion (a `file:line` quantity-shaped
value disagreeing with a live value obtained by a named, re-runnable command); six reasoned
exclusions (frozen historical counts, generated regions, consistency-shaped claims, the 17 version
stamps while the release bracket is open, `docs/history/`, explicitly-labelled illustrative
values); the walk-order/de-duplication rule; the six-file record format (D-27-01's fixed
eight-column header, the `**Totals this file:**` self-check line, the explicit zero-finding case);
the two fence classes (FENCED / RELEASE-OWNED, D-27-03's four RELEASE-OWNED sub-classes,
`HELD-WITH-DISCLOSED-EXCEPTION` for a break on a FENCED site); the union trip predicate (D-27-04's
three conjunctive conditions, disputed-site naming rule); the two-instruments-never-summed
statement naming the four scanner functions by name; the prohibition against substituting
`gen-gate-docs.py --check`'s own output for the sweep; and the reproducibility clause.

**Task 2 — `tests/recurrence-reading-v9.1/README.md` and `_FROZEN_PATHS` registration.** The
frozen-evidence discipline: what the directory is and how its figures are derived (never
hand-typed); a provenance/chain-of-custody table with all six expected filenames listed `pending`
in every measured column, with a preamble sentence explaining that convention explicitly; reader
independence (isolation mechanism recorded per-row, not asserted generically); what was
deliberately not committed (scratch notes, a not-a-hit ledger) and why; the amendment rule
(a correction is a new file, `--no-verify` forbidden, modeled on the existing
`tests/live-conformance-catalog.md` amendment-procedure comment); and D-27-05's explicit
supersession record — CONTEXT.md D-07 names `tests/live-conformance-v9.0/` as the template, its
mechanism claim (freeze once, derive forever) holds, but its file shape does not transfer because
there is no session to capture and no document to score, so the shape adopted is
`tests/adversarial-corpus-v9.0/catalog.md`'s single machine-parsed table, replicated per
(timing x reader/arm) cell.

Registered `'tests/recurrence-reading-v9.1'` in `scripts/check-firewall-battery.sh`'s
`_FROZEN_PATHS` array, immediately after `'tests/live-conformance-catalog.md'` — the only change
to that file this plan makes.

## Draft-prose literal-scan discipline (Task 1)

Before writing `protocol.md` to disk, the full draft text was tested in-process against
`scripts/gen-gate-docs.py`'s `_scan_text_for_literal_hits()` (import pattern from
`27-RESEARCH.md`'s Code Examples section — `sys.modules` populated before `exec_module`).

Initial draft: 4 hits — two on a verbatim quote of `docs/PROCESS.md`'s own "13 plans," "4 rounds"
worked example (line 59), two on "17 version stamps" (exclusion 4 and fence sub-class (c), lines
65/127). All four were reworded (Rule 1, drafting discipline rather than a gate requirement, since
`tests/` is not a `LITERAL_SCAN_SURFACES` member today): the PROCESS.md quote was paraphrased to
describe the example without repeating its digits, and both "17 version stamps" occurrences were
reworded to "the version stamps enumerated by `scripts/check-version-stamps.py`."

**One residual hit remains, kept deliberately:** line 66, `'4. **The version stamps'` — this is
the Markdown ordered-list marker `4.` for exclusion item 4, a false-positive artifact of the
scanner's digit-adjacent-word pattern matching a list number, not a quantity-shaped claim about
live state. Rewording the list to avoid numbering would reduce readability for no correctness
gain, and the plan's own acceptance criterion permits a residual hit transcribed here with its
reason for being kept.

## Deviations from Plan

None. Both tasks executed exactly as specified in `27-01-PLAN.md`, including the drafting
discipline pass (not a gate requirement, done anyway per the Phase 26 precedent) and the
`_FROZEN_PATHS`-single-line-only constraint.

## Verification

- `test -f tests/recurrence-reading-v9.1/protocol.md` + all 11 required section headings present:
  `PROTOCOL-SECTIONS-OK` (observed).
- `/usr/bin/grep -c "^| " tests/recurrence-reading-v9.1/protocol.md` → `1` (the eight-column
  record header, reproduced verbatim).
- `FENCED` appears 2x, `RELEASE-OWNED` 2x, `HELD-WITH-DISCLOSED-EXCEPTION` 1x in `## Fence
  classes` (observed via grep).
- `## Prohibition` contains the literal string `gen-gate-docs.py --check` inside a forbidding
  sentence (observed at line 170).
- `## Exclusions` contains exactly 6 numbered items, each with a reason clause in the same list
  item (observed by direct read of the rendered section).
- No section instructs the reader to consult another reader's output (the one match for "other
  reader" is a rule statement — "an intersection would let one reader's miss silently discharge
  the other reader's hit" — not an instruction to consult).
- `git diff --numstat scripts/check-firewall-battery.sh` (from the pre-plan commit) → `1\t0` —
  one line added, zero removed (observed).
- `/usr/bin/grep -Fc 'TOTAL=$((TOTAL + 1))'` on `scripts/check-firewall-battery.sh` → `4` before
  and `4` after the edit (observed both readings, unchanged).
- `bash scripts/check-firewall-battery.sh` final line: `FIREWALL: GREEN (26/26)` (observed,
  re-run after Task 2's commit; it read RED with one FROZEN-EVIDENCE failure in the window between
  writing `README.md` and committing it — expected per the amendment rule, and GREEN immediately
  after commit `af39d15`).
- `tests/recurrence-reading-v9.1/README.md` contains all 6 required section headings (observed).
- README's `## The live-conformance template, and where it does not transfer` names `27-CONTEXT.md`
  D-07 explicitly and states which half is kept (mechanism) and which is superseded (file shape)
  (observed at lines 69-86).
- Chain-of-custody table has a header row plus all 6 filename rows, each `pending` in every
  measured column, with the preamble sentence explaining the convention (observed).
- `sh .githooks/pre-commit` exit 0, both before and after the Task 2 commit (observed).
- `git diff --name-only` from the phase base commit (`9ee3ae8`) touches, beyond this plan's two
  new files and the one-line battery-script edit: `.planning/phases/26-.../26-07-SUMMARY.md`,
  `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/MEASUREMENT-MAP.md`, `docs/README.md`,
  `docs/gates/CONF-SURFACE.md`, `scripts/gen-gate-docs.py` — all of these are Phase 26 plan 07's
  own already-committed work (commits `53bb85a`/`9ee3ae8`/`97fdceb`/`f189c99`, landed before this
  plan started); `9ee3ae8` was chosen as the diff base because it is the last commit recorded in
  `STATE.md`'s git log at session start, but Phase 26's own close landed one commit later
  (`f189c99`). No file outside `tests/recurrence-reading-v9.1/` and
  `scripts/check-firewall-battery.sh` was touched by this plan's own two commits (`442fd01`,
  `af39d15`), confirmed by inspecting each commit's own file list independently.
- `python3 scripts/gen-gate-docs.py --check` → exit 0 (observed). `python3
  scripts/gen-gate-docs.py --self-test` → `SELF-TEST PASS — 112 controls run` (observed, took
  ~13s under load).

## Self-Check: PASSED

- `tests/recurrence-reading-v9.1/protocol.md` — FOUND
- `tests/recurrence-reading-v9.1/README.md` — FOUND
- `scripts/check-firewall-battery.sh` contains `tests/recurrence-reading-v9.1` — FOUND
- Commit `442fd01` — FOUND (`git log --oneline --all | grep 442fd01`)
- Commit `af39d15` — FOUND (`git log --oneline --all | grep af39d15`)
