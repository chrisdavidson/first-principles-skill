---
phase: 23-ship-v9-0-0
plan: 01
subsystem: planning-state
tags: [conformance, requirements-traceability, roadmap-reconciliation, gate-registry]

# Dependency graph
requires:
  - phase: 22-cap-the-recursion
    provides: "CONF-14/CONF-15 deliverables (depth rule, product/apparatus split, rework cap) and the CR-01/CR-02/CR-03 findings"
  - phase: 24-diagnosis-name-the-mechanism-not-the-instance
    provides: "D-06 discharge — CR-01/CR-02/CR-03 dispositions releasing v9.0.0's D-05 hold (docs/v9.1-claim-containment-diagnosis.md § 3)"
provides:
  - "Nine v9.0.0 requirement boxes (CONF-03..06, CONF-11..13, CONF-14..15) re-derived live and ticked, each with its own inline evidence line in .planning/REQUIREMENTS.md"
  - ".planning/STATE.md reconciled to the live position (Phase 23 executing, Phase 24 complete), with dated supersession notes for the released hold, the HELD heading and the no-second-disclosure claim"
  - ".planning/ROADMAP.md's Phase 23 row and Active Milestone summary no longer assert an unqualified hold; backlog entry 999.56 files Phase 17's [x]/open-gap contradiction"
  - "PHASE_BASE_SHA captured for plan 23-05's phase-wide CR-02/CR-03 no-fix fence"
affects: ["23-02", "23-03", "23-04", "23-05"]

tech-stack:
  added: []
  patterns: ["re-derivation over inheritance for requirement ticks (D-02)", "supersede-by-addition for planning-state documents (D-07)"]

key-files:
  created: []
  modified:
    - ".planning/REQUIREMENTS.md"
    - ".planning/STATE.md"
    - ".planning/ROADMAP.md"

key-decisions:
  - "CONF-13 ticks as a review finding, not a requirement shortfall (D-11): the scanner's own check passes (literal_scan_non_exempt=0) while its disclosed exemption bound is what let CR-01 through, and that bound is stated rather than discovered."
  - "STATE.md's stale 'Current focus' and 'Operator Next Steps' sections (describing Phase 24 as not-yet-started) were corrected with dated supersession notes beyond the plan's three named edits, to satisfy the acceptance criterion that no HELD/held line survive without a superseding note in the same block."
  - "ROADMAP.md's '## Active Milestone' v9.0.0 summary paragraph (a second HELD assertion outside the Phase 23 bullet) was corrected in place, since ROADMAP.md carries no byte-verbatim constraint analogous to STATE.md's halt block."
  - "total_phases in STATE.md frontmatter is mechanically 11 real '### Phase N' headers plus the backlog's '### Phase 999.x' header count (65 before, 66 after filing 999.56) — recorded here because the denominator's intended meaning is not otherwise documented, and this is the reading that reproduces the pre-existing value exactly."

requirements-completed: [REL-03]

# Metrics
duration: ~35min
completed: 2026-09-09
---

# Phase 23 Plan 01: Reconcile Surfaces and Re-Derive Nine Requirement Boxes Summary

**Nine v9.0.0 requirement boxes (CONF-03..06, CONF-11..13, CONF-14..15) re-derived live against
the tree this session and ticked on their own recorded evidence — none inherited from a phase
number, a VERIFICATION.md verdict, or the battery's green — with STATE.md and ROADMAP.md
reconciled to the fact that Phase 24 discharged D-06 and released v9.0.0's D-05 hold.**

## Performance

- **Duration:** ~35 min
- **Started:** 2026-09-09 (PHASE_BASE_SHA captured first, before any edit)
- **Completed:** 2026-09-09T16:43:53Z
- **Tasks:** 3 completed
- **Files modified:** 3 (`.planning/REQUIREMENTS.md`, `.planning/STATE.md`, `.planning/ROADMAP.md`)

## PHASE_BASE_SHA

PHASE_BASE_SHA: 40064eeaaad2ad9a0fbe407dfc875dff631c3b82

Captured via `git rev-parse HEAD` before any Phase 23 work began, and re-confirmed via a second
`git rev-parse HEAD` after Tasks 1-3 completed — both reads returned the identical SHA. `.planning/`
is gitignored (`commit_docs: false`), so Tasks 1-3 made no commit of their own and HEAD did not
move during this plan's Task 1-3 work; the only commit this plan makes is the metadata commit
below, carrying this SUMMARY.md, which is force-tracked despite `.planning/`'s blanket gitignore.
Plan 23-05 Task 2 uses `40064ee` as the base of the phase-wide diff proving no fix was written for
CR-02 or CR-03 anywhere in this phase.

## Accomplishments

- All nine open v9.0.0 requirement boxes re-derived live this session and ticked, each carrying
  its own artifact-plus-reading evidence line dated 2026-09-09, inline in `.planning/REQUIREMENTS.md`.
- `.planning/STATE.md` and `.planning/ROADMAP.md` reconciled to the true live position: Phase 23
  executing, Phase 24 complete (6/6 plans), the D-05 hold released by D-13, and D-14's disclosure
  obligation recorded — all by dated addition, never by deleting or rewording the Phase 22 halt
  block or the "HELD" heading, both confirmed byte-identical to their pre-edit text.
- Phase 17's `[x]`/"1 blocking gap open" self-contradiction filed as backlog entry `999.56`,
  tiered `apparatus` with the claim-audience argument, anchored by quoted text rather than a line
  number, per D-08 — filed, not fixed.

## Task Commits

`.planning/REQUIREMENTS.md`, `.planning/STATE.md` and `.planning/ROADMAP.md` are all gitignored
(`commit_docs: false`), so Tasks 1-3 made no git commits of their own — consistent with the
plan's own note that this plan "makes no commit of its own and HEAD does not move while it runs."
Only this SUMMARY.md (force-tracked under `.planning/phases/`) is committed, as the plan metadata
commit below.

1. **Task 1: Re-derive the nine open requirement boxes live** — no commit (gitignored files);
   evidence recorded inline in `.planning/REQUIREMENTS.md`, see table below.
2. **Task 2: Reconcile STATE.md and ROADMAP Phase 23 row** — no commit (gitignored files).
3. **Task 3: File Phase 17's contradiction as backlog 999.56** — no commit (gitignored files).

**Plan metadata:** committed after this SUMMARY.md is written (see below).

## Files Created/Modified

- `.planning/REQUIREMENTS.md` — nine boxes ticked with inline evidence; Traceability table Status
  column updated for the same nine; footer `*Last updated*` line rewritten.
- `.planning/STATE.md` — `## Current Position` rewritten to name Phase 23 executing and Phase 24
  complete (6/6); frontmatter `total_phases` 65 → 66 (see Decisions) and `last_updated` refreshed;
  `## Project Reference` § "Current focus" and `## Operator Next Steps` corrected with dated
  supersession notes (stale "Phase 24 not yet started" framing); `## Accumulated Context` gained
  three dated supersession notes (beneath the "HELD" heading, beneath the D-A "Superseded"
  paragraph for D-14, and a new D-05-released-per-D-13 note) — the Phase 22 halt block and the
  "HELD" heading text themselves are unchanged (see Self-Check below).
- `.planning/ROADMAP.md` — Phase 23 bullet's `**HELD**` annotation replaced with a dated
  hold-released note (checkbox stays `[ ]`); `## Active Milestone` v9.0.0 summary paragraph
  corrected (second HELD assertion, outside the Phase 23 bullet); backlog entry `### Phase
  999.56` appended (Phase 17 contradiction, filed not fixed); Phase 22 bullet re-confirmed
  unchanged and internally consistent (D-01 misalignment 1 resolved against STATE.md, not this
  row).

## Nine Requirements — Evidence Table

| Requirement | Artifact / Command | Literal Reading (2026-09-09) |
|---|---|---|
| CONF-03 | `docs/conformance-baseline.md` § Headline, "Files unreadable by `_slice_sections`" | `0 of 14` (shared-examples), `0 of 14` (generated-twin); target 4→0 met both |
| CONF-04 | same artifact, "§4 `chain_blocks` (malformed)" and "`### Conclusion` heading-swept blocks (malformed)" | `31 (0 malformed)` on both rows, both columns; target 19→0 of 28 met (denominator moved 28→31, recorded not silently paired) |
| CONF-05 | same artifact, "§2 verdict cells (non-conforming)" and "§6 untraced claims (marked/silent)"; `scripts/check-conf-gate.py:223` | `77 (0 non-conforming)` both columns; `2 untraced (2 marked, 0 silent)` both columns; `_MARKED_RATCHET: int = 4` confirmed equal to disclosed bound 2's `2+2` |
| CONF-06 | `python3 scripts/check-conf-gate.py --self-test` / live leg; `scripts/check-firewall-battery.sh:567`; `.github/workflows/validation.yml:319` | "SELF-TEST PASS — 44 controls run"; live leg fires 3 falsification arms then "PASS"; `CONF-GATE` registered in both files, confirmed by grep |
| CONF-11 | `python3 scripts/gen-gate-docs.py --self-test` / `--check` | "SELF-TEST PASS — 74 controls run"; "harvested 22/22 expected script-backed entries (22 total)", exit 0 |
| CONF-12 | `python3 scripts/gen-gate-docs.py --describe`; `python3 scripts/_gate_registry.py --self-test` | `derived_counts.literal_scan_non_exempt = 0`; "SELF-TEST PASS — 21 controls run" (includes `d01-live-battery-equality`) |
| CONF-13 | `python3 scripts/gen-gate-docs.py --describe`; `docs/gates/CONF-SURFACE.md` § Disclosed bounds (5)/(6) | `literal_scan_non_exempt = 0`; disclosed bound: the `headline-provenance-delta` exemption strips the entire `N → M` run including its terminus (D-11) — CR-01 is the live counter-instance, dispositioned in `docs/v9.1-claim-containment-diagnosis.md` § 3, not fixed here |
| CONF-14 | `docs/PROCESS.md` §1/§1.1/§1.2/§2/§3/§3.1; `CONTRIBUTING.md:74`; `.planning/ROADMAP.md:2346`/`:2421` | All six PROCESS.md sections present; CONTRIBUTING.md cites the depth rule; backlog 999.30 and 999.31 both titled "...RESOLVED (2026-09-08 by Phase 22 ...)" |
| CONF-15 | `CLAUDE.md` § "Review protocol" (line 247), `CLAUDE.md:186`, `CLAUDE.md:280` | Product/apparatus split (item 1), `/bm:code-review` output shape (item 2, YAML block), block-only-on-product (item 3) all present; rework cap cited (not restated) at line 186; line 280: "No script, control or CI job enforces any of this" |

## Decisions Made

- **CONF-13 ticks as a review finding, not a requirement shortfall (D-11).** The scanner's own
  check passes clean (`literal_scan_non_exempt = 0`); the disclosed exemption bound — that the
  scanner strips the entire `N → M` run, including its terminus, so a stale final value reads as
  exempt rather than as a hit — is what let CR-01 through undetected, and D-11 requires that bound
  be published rather than discovered. Recorded inline in `.planning/REQUIREMENTS.md`.
- **`total_phases` in STATE.md frontmatter is `### Phase N` headers (11) + backlog `### Phase
  999.x` headers** (54 before Task 3, 55 after filing 999.56 → 65 → 66). This derivation is
  recorded because the counter's intended denominator is not documented anywhere else, and this
  reading exactly reproduces the pre-existing value (65) before this plan's own backlog addition
  moved it — the least-surprising live derivation available. If this reading is wrong, the next
  agent to touch this counter should look here first rather than re-deriving from scratch.
- **STATE.md's "Current focus" and "Operator Next Steps" sections were also corrected**, beyond
  the plan's three explicitly named STATE.md edits (`## Current Position`, frontmatter,
  `## Accumulated Context`), because both asserted Phase 24 as not-yet-started and the ship as
  held without qualification — which the plan's own acceptance criterion ("check every hit of
  `held|HELD` ... and list the disposition of each") required be resolved. Both were corrected by
  dated addition (kept verbatim below the note), matching D-07's convention rather than the plan's
  D-07-scoped Accumulated-Context edits specifically, since these two sections carry no
  byte-verbatim constraint.
- **ROADMAP.md's "## Active Milestone" v9.0.0 summary paragraph was corrected in place** (not by
  addition) since it carries no analogous verbatim-preservation requirement — only STATE.md's
  Phase 22 halt block and "HELD" heading do.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] STATE.md's "Current focus" and "Operator Next Steps" sections stated Phase 24 as future work after Phase 24 had already completed**
- **Found during:** Task 2, while checking every `held|HELD` hit per the acceptance criteria.
- **Issue:** `## Project Reference` § "Current focus" (line ~27) and `## Operator Next Steps`
  items 1-2 described `/bm:plan-phase 24` as not-yet-run and the ship as held on Phase 24's
  future output, contradicting the live fact (Phase 24 is 6/6 complete) that Task 2's own
  `## Current Position` edit already established.
- **Fix:** Added dated supersession notes in both locations (D-07 convention: add, do not delete
  or reword), stating Phase 24's completion and D-13's hold release, then leaving the original
  text intact beneath each note.
- **Files modified:** `.planning/STATE.md`
- **Verification:** `/usr/bin/grep -n "held\|HELD" .planning/STATE.md` re-run after the fix; every
  hit now sits inside a block carrying a superseding note (see table below).
- **Committed in:** metadata commit (part of this plan's only commit; the edited file itself is
  gitignored)

**2. [Rule 1 - Bug] ROADMAP.md's "## Active Milestone" summary asserted v9.0.0's release "HELD" a second time, outside the Phase 23 bullet**
- **Found during:** Task 2, `/usr/bin/grep -n "HELD" .planning/ROADMAP.md` after editing the
  Phase 23 bullet — a second, unedited hit remained.
- **Issue:** The `## Active Milestone` section's v9.0.0 paragraph independently restated "open,
  release HELD" and "waits on Phase 24's PROSE-04 dispositions," both now false.
- **Fix:** Rewrote the paragraph in place to state the hold was released 2026-09-09 per D-13, and
  that Phase 23 now runs in full — this section carries no verbatim-preservation constraint, so
  correction in place (rather than addition) was used.
- **Files modified:** `.planning/ROADMAP.md`
- **Verification:** `/usr/bin/grep -n "HELD" .planning/ROADMAP.md` now returns zero hits.
- **Committed in:** metadata commit (edited file is gitignored)

## `held`/`HELD` disposition table (STATE.md, acceptance criterion)

| Line (pre-edit content) | Disposition |
|---|---|
| "Those dispositions are what release v9.0.0's held ship." (Current focus) | Section rewritten with a dated note; sentence's premise (Phase 24 still pending) corrected — see Deviation 1 |
| "### v9.0.0 is OPEN and its release is HELD — read this before touching Phase 22 or 23" | Heading kept byte-verbatim; a dated supersession note was added immediately beneath it (D-07) |
| "conformance-baseline reading — is **held**." (verbatim carried paragraph) | Left untouched — part of the byte-verbatim carried block; covered by the new note beneath the heading above it |
| "The three items D-05 held (the 17-stamp bump..." (new text this plan added) | Not a residual claim — this is the plan's own new sentence stating what WAS held, in explicitly past tense, citing the release |
| "FIREWALL: GREEN (26/26) held throughout the entire defective state" (Phase 22 halt record, verbatim) | Untouched — part of the byte-verbatim Phase 22 halt block; "held" here means "remained green," not "release held," and is historical, not a live claim |
| "release v9.0.0's held ship" (Operator Next Steps item 1) | Section rewritten with a dated note; corrected — see Deviation 1 |

## `HELD` disposition table (ROADMAP.md, acceptance criterion)

| Line (pre-edit content) | Disposition |
|---|---|
| Phase 23 bullet: `**HELD** (23-CONTEXT.md D-05/D-06): ...` | Replaced with a dated hold-released note; checkbox stays `[ ]` |
| `## Active Milestone`: "**v9.0.0 — Conformance** — Phases 17-23, **open, release HELD**." | Rewritten in place — see Deviation 2 |

Post-fix: `/usr/bin/grep -n "HELD" .planning/ROADMAP.md` returns zero hits.

## Verification Results

```
$ python3 scripts/report-conformance.py --self-test
report-conformance: SELF-TEST PASS — 102 controls run
$ python3 scripts/report-conformance.py --check
report-conformance: PASS — no drift
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST PASS — 44 controls run
$ python3 scripts/check-conf-gate.py
check-conf-gate: PASS (3 falsification arms fired and recovered)
$ python3 scripts/gen-gate-docs.py --self-test
gen-gate-docs: SELF-TEST PASS — 74 controls run
$ python3 scripts/gen-gate-docs.py --check
harvested 22/22 expected script-backed entries (22 total)
$ python3 scripts/_gate_registry.py --self-test
_gate_registry: SELF-TEST PASS — 21 controls run
$ echo $?
0
```

- `/usr/bin/grep -c "^- \[ \] \*\*CONF-" .planning/REQUIREMENTS.md` → `0` (no CONF box remains
  unticked).
- `test -f .planning/STATE.md && grep -q "Phase: 23" ... && ! grep -q "Phase: 24 ... EXECUTING" ...
  && grep -q "v9.1-claim-containment-diagnosis" ... && grep -A 6 "^### v9.0.0 is OPEN..." | grep -qi
  "superseded"` → `RECONCILED`.
- `git diff` on a pre-edit copy of the Phase 22 halt record block → identical (confirmed via
  `diff` against a saved pre-edit copy of `.planning/STATE.md`, isolating the block from `####
  The Phase 22 halt record, verbatim` to the next `---`).
- `/usr/bin/grep -q "^### Phase 999\.56:" .planning/ROADMAP.md && grep -A 30 "^### Phase 999\.56:"
  ... | grep -qi "Phase 17"` → `FILED`.
- `/usr/bin/grep -c "^### Phase 999\." .planning/ROADMAP.md` → `55` (one more than the pre-task
  count of 54).
- `git rev-parse HEAD` before and after all Task 1-3 work → both
  `40064eeaaad2ad9a0fbe407dfc875dff631c3b82` (unchanged, confirming `.planning/`'s gitignore kept
  HEAD stationary).

## Known Stubs

None. This plan edits only planning-state Markdown (`.planning/REQUIREMENTS.md`,
`.planning/STATE.md`, `.planning/ROADMAP.md`) and runs pre-existing read-only gate scripts; no
shipped artifact, UI, or data-rendering surface is touched.

## Threat Flags

None. Per the plan's own threat model: no process boundary is crossed, no untrusted input is
parsed, no artifact reaches a user — all three edited files are gitignored planning state.

## Next Steps

- Plan 23-02 (Wave 2): `_rows_v9()` + `_self_test_v9_rows_sentinel()`, regenerate both matrix
  artifacts, sweep the `HEADLINE-LOCK` coverage-headline move across all five registered surfaces.
- This plan's nine evidence readings (table above) are the input plan 23-02's matrix rows cite,
  and plan 23-05's CHANGELOG entry restates figures derived from them, per the plan's own output
  contract.

## Self-Check: PASSED

- `test -f .planning/REQUIREMENTS.md` → FOUND
- `test -f .planning/STATE.md` → FOUND
- `test -f .planning/ROADMAP.md` → FOUND
- `test -f .planning/phases/23-ship-v9-0-0/23-01-SUMMARY.md` → FOUND (this file)
- `/usr/bin/grep -c "^- \[ \] \*\*CONF-" .planning/REQUIREMENTS.md` → `0` → FOUND (zero unticked)
- `/usr/bin/grep -q "^### Phase 999\.56:" .planning/ROADMAP.md` → FOUND
- `git rev-parse HEAD` → `40064eeaaad2ad9a0fbe407dfc875dff631c3b82` → matches PHASE_BASE_SHA above
- No git commit hashes to verify for Tasks 1-3 (gitignored files, no commits made) — this is
  expected per the plan's own note, not a gap.
