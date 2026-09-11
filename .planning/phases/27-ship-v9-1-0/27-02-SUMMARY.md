---
phase: 27-ship-v9-1-0
plan: 02
subsystem: requirements-re-derivation
tags: [re-derivation, evidence, PROSE, CONTAIN, NARR, RATCHET, ship-precondition]
dependency-graph:
  requires:
    - "27-01: tests/recurrence-reading-v9.1/ (not used by this plan directly, but the phase's own measurement instrument)"
  provides:
    - "Fourteen re-derived requirement boxes (.planning/REQUIREMENTS.md) with fresh command-and-literal-output evidence, satisfying Phase 23 D-02/D-03's re-derivation-not-inheritance rule"
    - "PROSE-01..04 ticked for the first time (closing the Phase 24 completion gap where they read COMPLETE but the boxes stayed unticked)"
  affects:
    - "plan 27-05..09 (the release acts): all fourteen boxes now read clean, no ship blocker carried forward from this plan"
tech-stack:
  added: []
  patterns:
    - "re-derivation against live tree this session, never inheritance from a prior plan's evidence (Phase 23 D-02/D-03)"
key-files:
  created: []
  modified:
    - .planning/REQUIREMENTS.md
decisions: []
metrics:
  duration: "~35 minutes"
  completed: "2026-09-11"
---

# Phase 27 Plan 02: Re-derive the Fourteen Pre-Existing v9.1.0 Requirement Boxes Summary

Re-derived all fourteen pre-existing v9.1.0 requirement boxes — PROSE-01..04, CONTAIN-01..04,
NARR-01..02, RATCHET-01..04 — against the live tree this session, before any release act runs.
**No box failed re-derivation; no ship blocker is raised by this plan.**

## What was built

**Task 1 — PROSE-01 through PROSE-04, re-derived and ticked for the first time.** All four boxes
read `- [ ]` at plan start despite Phase 24 reading COMPLETE — the exact gap this plan's objective
names. Each was re-derived against the live text of `docs/v9.1-claim-containment-diagnosis.md`
this session, not against `24-*-SUMMARY.md`:

- **PROSE-01**: confirmed the document names the mechanism (containment's `N → M` delta exemption)
  at the mechanism level ("mechanism-level answer to backlog 999.49's root question", line 209),
  states the exemption is "correct in intent" (line 115), and re-ran section 1.4's live-tree
  invocation this session — `detail_page_containment_problems()` on `docs/gates/CONF-SURFACE.md`'s
  current text still returns `problems == []`, matching the page's own 2026-09-09 recorded result.
- **PROSE-02**: confirmed `docs/gates/SCAN-GUARD.md` is still a currently-unflagged live sibling
  site (`problems == []`, terminus `100` corroborated against its own FACTS fence, also `100`).
  Checked section 2's Published Counts for staleness: re-running `census-delta-vectors.py --rung
  all` today returns a different row count than the page's own pinned 671 — this is **not** a
  stale current-fact claim, because the page's own discipline (1) states every quantity there is a
  frozen, commit-pinned dated measurement, not a current-fact assertion; it is recorded in the
  evidence line rather than silently observed, and is explicitly **not** treated as a Rule-1-style
  fix or a candidate pre-arm site, since it fails the hit criterion on its face (a dated measurement
  disagreeing with a *later* live state, by design, is not the same shape as a current-fact claim
  disagreeing with the present).
- **PROSE-03**: confirmed section 4 states the consistency-shaped class is not covered, names
  `999.50`/`999.51` (also independently confirmed present and named live in `.planning/ROADMAP.md`,
  at line numbers that have moved since the diagnosis page's own frozen transcript — consistent
  with the page's own symbol-not-line-number citation discipline rather than a break), and states
  the reason (no mechanism compares a value where none exists to compare).
- **PROSE-04**: confirmed section 3's "What this section discharges" names `23-CONTEXT.md` D-06 by
  id, and that CR-01/CR-02/CR-03 each carry a disposition — CR-01 and CR-03 accepted with a stated
  bound, CR-02 "dispositioned by routing, not by fix" with the routing and its reason both recorded
  (no digit, nothing for a quantity-comparison mechanism to corroborate).

Traceability table rows for PROSE-01..04 updated from `Pending` to `Complete`.

**Task 2 — CONTAIN-01 through CONTAIN-04, existing `[x]` boxes re-derived against a fresh
`--describe` run.** All four were already ticked from Phase 25/26; per the plan's own instruction
that inherited evidence must not be trusted, each was re-verified this session:

- **CONTAIN-01**: `derived_counts.containment_surfaces == 4` this session;
  `containment_surface_roster_problems()` confirmed by direct read to be a set-EQUALITY test
  (`missing =`/`extra =`), never subset; the four surfaces named by path from `_CONTAINMENT_SURFACES`
  and its independent lock: `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/TESTING.md`,
  `docs/gates/*.md`.
- **CONTAIN-02**: `chain_termini_stale == 0` this session (the current/uncorroborable split has
  moved from Phase 25's 3/2 to today's 5/0 as later Phase 26 plans corroborated remaining chains —
  the stale=0 reading is unchanged and is the requirement's own load-bearing figure). The mutation
  proof was **not** re-run, per the plan's own instruction, and cited instead to
  `25-04-SUMMARY.md`'s transcript. What was newly re-derived: the arm's live `cmd_check()` call
  site, `scripts/gen-gate-docs.py:4691`, confirmed inside `cmd_check()`'s own body (lines
  4568-4818) and distinct from three other call sites at 6649/6669/6691, which are `--self-test`
  fixtures, not the live check path.
- **CONTAIN-03**: confirmed `docs/gates/CONF-SURFACE.md:476` still carries the REACH-or-LEVEL
  determination heading naming all three CONTAIN requirements, and quoted the CONTAIN-02
  determination clause verbatim (argument stated: "The arm's subject is a page's own claim about a
  live figure, never a checker's own correctness").
- **CONTAIN-04**: `literal_scan_ledger_entries == 180 == literal_scan_ledger_max` and
  `containment_ledger_entries == 20 == containment_ledger_max` this session (the containment
  ledger has moved 23 → 20 since plan 26-06's own reading, via later Phase 26 reconciliation; the
  literal ledger is unchanged at 180). The published delta is cited to `docs/gates/
  CONF-SURFACE.md`'s disclosed bound (11) by heading, not restated as digits in
  `.planning/REQUIREMENTS.md`.

Verify command run: `python3 scripts/gen-gate-docs.py --describe | python3 -c "..."` →
`CONTAIN-REDERIVE-OK containment_surfaces=4 literal_max=180 containment_max=20`.

**Task 3 — NARR-01, NARR-02, RATCHET-01 through RATCHET-04, re-derived and evidence blocks
appended.** All six were already ticked; each re-verified against the live tree this session:

- **NARR-01**: `docs/PROCESS.md` §2's opening clause quoted verbatim, confirmed widened to "every
  restated moving count on a product surface — not the gate-battery count alone", with the battery
  total surviving as the worked example and the frozen-historical-count paragraph confirmed present
  and intact immediately after.
- **NARR-02**: fresh `--describe` reading — `narrative_regions == 3` (grown from 2 to 3 since this
  box was first ticked, as plan 26-05 added CLAUDE.md's own region), `narrative_restatement_finding
  == 0`. All three host surfaces (`docs/README.md`, `docs/MEASUREMENT-MAP.md`, `CLAUDE.md`)
  confirmed by name from `_NARRATIVE_REGIONS`, and each confirmed to carry its marker pair on disk
  by direct `grep -n "GENERATED"`.
- **RATCHET-01**: confirmed both `.githooks/pre-commit` and `scripts/git-hooks/pre-commit` still
  run `--self-test` at line 103 followed by `--check` at line 108, same order, both files — the
  wiring, not the mutation (cited to `26-07-SUMMARY.md`), is what was re-derived here.
- **RATCHET-02**: `_DEFERRED_LEDGER_MAX`'s own comment block (line 3698) still states the
  size-only scope sentence verbatim, citing the same `('CLAUDE.md', '(43 controls)')` instance; the
  live ledger entry count equals the pin, referenced from Task 2's reading rather than re-run.
- **RATCHET-03**: `/usr/bin/grep -n "RATCHET-03" .planning/ROADMAP.md docs/gates/CONF-SURFACE.md`
  still returns both landing sites this session. Evidence line states explicitly that the
  requirement is discharged by a recorded DROP verdict, not by a shipped scan — no diff-review
  hedge-word scanner exists in this tree.
- **RATCHET-04**: `docs/gates/CONF-SURFACE.md:522`'s heading quoted verbatim, and its landing
  commit `78b45a9` confirmed dated before NARR-01/NARR-02/RATCHET-01/RATCHET-02's own wiring
  commits.

Verify command run: the Python completeness scan over all fourteen IDs →
`UNTICKED: []`, exit 0.

## Deviations from Plan

None. All three tasks executed exactly as specified; no box failed re-derivation, so no ship
blocker was raised. The one item flagged during PROSE-02's re-derivation — `census-delta-vectors.py
--rung all`'s live row count no longer matching the page's own pinned `671` — was evaluated against
the hit criterion and found NOT to qualify as a stale current-fact claim (the page's own discipline
explicitly frames that figure as a dated, commit-pinned measurement, never a present-tense
assertion), so it was recorded in the evidence line as an observation rather than treated as a
Rule 1 fix or a candidate pre-arm site for plan 27-04. No fix was made to any shipped document by
this plan.

## Verification

- `/usr/bin/grep -c "^- \[x\] \*\*PROSE-0" .planning/REQUIREMENTS.md` → `4` (observed).
- `/usr/bin/grep -c "^- \[ \] \*\*PROSE-0" .planning/REQUIREMENTS.md` → `0` (observed).
- `python3 scripts/gen-gate-docs.py --describe | python3 -c "...assert...; print('CONTAIN-REDERIVE-OK ...')"`
  → `CONTAIN-REDERIVE-OK containment_surfaces=4 literal_max=180 containment_max=20` (observed).
- Completeness scan over all fourteen IDs → `UNTICKED: []`, exit 0 (observed).
- `git check-ignore -v .planning/REQUIREMENTS.md` → `.gitignore:1:.planning/	.planning/REQUIREMENTS.md`
  (observed) — confirms no commit is expected from this plan's own file edits.
- `git status --porcelain` → empty (observed) — no tracked file was modified by this plan's edits.
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)` (observed, floor check only,
  not evidence for any individual box).

## Self-Check: PASSED

- `.planning/REQUIREMENTS.md` contains all fourteen `- [x] **ID**` boxes — FOUND (verified by the
  completeness scan above).
- `.planning/REQUIREMENTS.md` Traceability table PROSE-01..04 rows read `Complete` — FOUND
  (verified by direct read after edit).
- No commit exists for this plan's `.planning/REQUIREMENTS.md` edits (gitignored, `commit_docs:
  false`) — CONFIRMED absent from `git log`, as expected.
