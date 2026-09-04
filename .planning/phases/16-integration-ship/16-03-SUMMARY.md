---
phase: 16-integration-ship
plan: 03
subsystem: version-stamps
tags: [version-01, dual-04, gate-01, ship-01, release-status-prose]
dependency-graph:
  requires:
    - "192/94/0/286 headline swept onto all five COVERED_HEADLINE_SURFACES (16-02)"
  provides:
    - "17 hand-maintained version stamps at 8.26.0 (VERSION-01 live leg: '17 stamps, all 8.26.0')"
    - "generated tree (first-principles/agents/, first-principles/skills/*/SKILL.md) regenerated with zero drift (DUAL-04)"
    - "GATE-01 (check-agent.py) passing against the regenerated shipped agent"
    - "zero tracked-doc occurrences of the literal 'unreleased' or 'still reads 8.25.0' in CLAUDE.md/docs/ARCHITECTURE.md"
  affects:
    - ".claude-plugin/marketplace.json, first-principles/.claude-plugin/plugin.json, shared/spine/SKILL.meta.yml"
    - "14x shared/skills/*/SKILL.md, 14x generated first-principles/skills/*/SKILL.md, first-principles/agents/first-principles.md"
    - "CLAUDE.md, docs/ARCHITECTURE.md"
tech-stack:
  added: []
  patterns:
    - "manual 17-stamp bump verified by check-version-stamps.py's live leg BEFORE sync-content.py --write, so a missed stamp is caught before it propagates into the generated tree (the v8.14 failure-mode guard)"
key-files:
  created: []
  modified:
    - .claude-plugin/marketplace.json
    - first-principles/.claude-plugin/plugin.json
    - shared/spine/SKILL.meta.yml
    - shared/skills/challenge-assumptions/SKILL.md
    - shared/skills/estimate/SKILL.md
    - shared/skills/first-principles-analysis/SKILL.md
    - shared/skills/fishbone/SKILL.md
    - shared/skills/five-whys/SKILL.md
    - shared/skills/ground-truths/SKILL.md
    - shared/skills/identify-essence/SKILL.md
    - shared/skills/inversion/SKILL.md
    - shared/skills/pre-mortem/SKILL.md
    - shared/skills/reason-upward/SKILL.md
    - shared/skills/second-order/SKILL.md
    - shared/skills/theoretical-limit/SKILL.md
    - shared/skills/trade-off/SKILL.md
    - shared/skills/validate/SKILL.md
    - first-principles/agents/first-principles.md
    - first-principles/skills/challenge-assumptions/SKILL.md
    - first-principles/skills/estimate/SKILL.md
    - first-principles/skills/first-principles-analysis/SKILL.md
    - first-principles/skills/fishbone/SKILL.md
    - first-principles/skills/five-whys/SKILL.md
    - first-principles/skills/ground-truths/SKILL.md
    - first-principles/skills/identify-essence/SKILL.md
    - first-principles/skills/inversion/SKILL.md
    - first-principles/skills/pre-mortem/SKILL.md
    - first-principles/skills/reason-upward/SKILL.md
    - first-principles/skills/second-order/SKILL.md
    - first-principles/skills/theoretical-limit/SKILL.md
    - first-principles/skills/trade-off/SKILL.md
    - first-principles/skills/validate/SKILL.md
    - CLAUDE.md
    - docs/ARCHITECTURE.md
decisions:
  - "CLAUDE.md's TRACE-03 row: replaced 'unreleased, so this row carries no version stamp: the shipped version is whatever .claude-plugin/marketplace.json says, and VERSION-01 moves all 17 stamps in lockstep at release' with 'shipped at v8.25.0' — the evergreen half restated VERSION-01's own row content, so it was deleted as redundant rather than kept as a hedge, per the plan's own instruction."
metrics:
  duration: "~25 minutes"
  completed: "2026-09-04"
---

# Phase 16 Plan 03: Bump version stamps to 8.26.0 Summary

Moved all 17 hand-maintained version stamps from `8.25.0` to `8.26.0` in lockstep, verified the
live leg BEFORE regenerating the tree (closing the v8.14 one-missed-stamp failure mode), propagated
the bump to the generated `first-principles/` tree with zero drift, and retired three
time-qualified release-status sentences in `CLAUDE.md` and `docs/ARCHITECTURE.md` that the bump
itself falsified.

## What was built

**Task 1** — Edited the version value at all 17 hand-maintained stamp locations: two JSON
manifests (`.claude-plugin/marketplace.json`, `first-principles/.claude-plugin/plugin.json`),
`shared/spine/SKILL.meta.yml` (the one stamp matching no `shared/skills/*/SKILL.md` glob), and
all 14 `shared/skills/*/SKILL.md` frontmatter `version:` fields — quoting, key placement and
surrounding formatting preserved byte-for-byte, value changed only. Ran the VERSION-01 live leg
immediately after editing and before touching the generated tree, per the plan's explicit
ordering discipline.

**Task 2** — Ran `sync-content.py --write` to regenerate `first-principles/agents/` and all 14
`first-principles/skills/*/SKILL.md` stubs from `shared/`, confirmed `sync-content.py --check`
reports zero drift (DUAL-04), and ran `check-agent.py` (GATE-01) against the regenerated shipped
agent in-plan rather than waiting for the battery.

**Task 3** — Corrected three sentences in `CLAUDE.md` and `docs/ARCHITECTURE.md` that Task 1's
own bump falsified:
1. `CLAUDE.md`'s SCAN-GUARD registration sentence — "registered under Phase 15 (unreleased at
   time of writing — `.claude-plugin/marketplace.json` still reads 8.25.0...)" → "registered at
   v8.26.0 under Phase 15", matching the PROV-GUARD/REG-GUARD voice two lines above it.
2. The identical clause in `docs/ARCHITECTURE.md`'s sibling paragraph, same correction.
3. `CLAUDE.md`'s TRACE-03 row — "landed the Phase 10 review fixes — unreleased, so this row
   carries no version stamp: the shipped version is whatever `.claude-plugin/marketplace.json`
   says, and VERSION-01 moves all 17 stamps in lockstep at release" → "landed the Phase 10 review
   fixes — shipped at v8.25.0" (Phase 10 shipped in v8.25.0 per `CHANGELOG.md:14`; the evergreen
   half was deleted as redundant with the VERSION-01 row above rather than kept as a
   now-meaningless hedge, per the plan's own instruction).

The battery-tally sentence further down in `CLAUDE.md` ("SCAN-GUARD (added under Phase 15,
v8.26.0) moved it from 23 to 24") was checked and confirmed already correct — left unchanged, as
instructed.

## Verification performed (observed, not assumed)

- `python3 scripts/check-version-stamps.py --self-test` → exit 0, `PASS (7 fixture trees, 11
  named assertions)`.
- `python3 scripts/check-version-stamps.py` → exit 0, first line exactly
  `check-version-stamps: 17 stamps, all '8.26.0'`, last line `check-version-stamps: PASS`.
- `/usr/bin/grep -rc "8\.25\.0" .claude-plugin/marketplace.json first-principles/.claude-plugin/plugin.json shared/spine/SKILL.meta.yml`
  → `0` for all three (exit 1, no matches).
- `git status --porcelain` immediately after Task 1's edits → exactly 17 modified files, no
  others.
- `python3 scripts/sync-content.py --write` → `wrote 48 files`; `python3 scripts/sync-content.py --check`
  → exit 0, no drift.
- `python3 scripts/check-agent.py` → exit 0, `COVERAGE — validated
  .../first-principles/agents/first-principles.md`, `check-agent: PASS`.
- `git diff --stat first-principles/` → 15 files changed (14 skill stubs + the agent), 15
  insertions/15 deletions.
- `/usr/bin/grep -rc "8\.25\.0" first-principles/ | /usr/bin/grep -v ":0$"` → no output (zero
  residual old-version lines in the generated tree).
- `git diff first-principles/ | /usr/bin/grep "^[-+]" | /usr/bin/grep -v "^[-+][-+]" | /usr/bin/grep -vc "8\.2[56]\.0"`
  → `0` (every changed line in the generated tree is a version line).
- `/usr/bin/grep -rn "unreleased" CLAUDE.md docs/ARCHITECTURE.md` → no output, exit 1 (zero
  occurrences).
- `/usr/bin/grep -rc "still reads 8.25.0" CLAUDE.md docs/ARCHITECTURE.md` → `0` for both files.
- `/usr/bin/grep -c "SCAN-GUARD was registered at v8.26.0" CLAUDE.md` → `1`;
  `/usr/bin/grep -c "SCAN-GUARD was registered at v8.26.0" docs/ARCHITECTURE.md` → `1`.
- `python3 scripts/check-traceability.py --self-test` → exit 0, `check-traceability --self-test:
  PASS`, run again after the Task 3 edits.
- `git status --porcelain` after all three task commits → empty (clean tree).
- Plan-level sanity re-run of `bash scripts/check-firewall-battery.sh` (not part of this plan's
  own `<verification>` block, run as an extra check) → `FIREWALL: RED (1 gate(s) failed, 1
  prerequisite(s) unmet; 22/24 passed)`. Investigated and confirmed **out of scope for this plan**
  — see "Deferred to 16-04" below.

## Deviations from Plan

None — plan executed exactly as written; all three tasks' own `<verify>` commands and
acceptance criteria passed as specified.

## Deferred to 16-04 (out of scope for this plan, not a deviation)

**`QUAL-01` (`check-quality-harness.py --self-test`) currently fails**, caused by wave 1
(16-01)'s matrix-row registration, not by any edit in this plan. `scripts/check-quality-harness.py`
carries its own internal hardcoded locked anchor set (`render_u_required`, restated in a
coverage-floor entry) that has not been updated to include `_selftest_ledger_traceability` — a
Phase-14-era self-test function that wave 1 newly pointed `v8.26/LEDGER-04`'s `artifact_link` at
for the first time. Full detail, root cause, and why this is confirmed to be `16-04-PLAN.md`
Task 1's job (its own `<action>` explicitly anticipates fixing exactly this class of regression
from "the 20 new matrix rows (16-01)") is recorded in
`.planning/phases/16-integration-ship/deferred-items.md`. Not fixed here: `scripts/check-quality-harness.py`
is outside this plan's `files_modified` list and none of its three tasks touch matrix-row
registration; this plan's own `<verification>` block does not require the full battery to pass,
and all four checks it does require (version-stamps both legs, sync-content --check, check-agent,
traceability self-test) pass. A `[PREREQ] VAL-03` line also appeared in that same battery run —
a missing pytest interpreter in this worktree's Python environment (SHIP-06's BLOCKED semantics,
not a gate failure), unrelated to this plan's edits.

## Known Stubs

None. This plan edits version-stamp values and release-status prose only; no UI or data-flow
component is touched.

## Threat Flags

None. Per the plan's own threat model, every edit in this plan is either a version-value change
already covered by VERSION-01/DUAL-04/GATE-01, or documentation prose with no new input-handling,
auth, network, or schema surface — T-16-08 through T-16-11 were mitigated as specified and
verified above; T-16-SC is accepted with no applicable surface.

## Self-Check: PASSED

- `.claude-plugin/marketplace.json` — FOUND (modified, commit `59dd484`), contains `8.26.0`
- `first-principles/.claude-plugin/plugin.json` — FOUND (modified, commit `59dd484`), contains `8.26.0`
- `shared/spine/SKILL.meta.yml` — FOUND (modified, commit `59dd484`), contains `8.26.0`
- All 14 `shared/skills/*/SKILL.md` — FOUND (modified, commit `59dd484`), each contains `8.26.0`
- `first-principles/agents/first-principles.md` and all 14 generated
  `first-principles/skills/*/SKILL.md` — FOUND (regenerated, commit `714c95a`)
- `CLAUDE.md`, `docs/ARCHITECTURE.md` — FOUND (modified, commit `c1b98b3`)
- Commit `59dd484` (Task 1) — FOUND in `git log --oneline`
- Commit `714c95a` (Task 2) — FOUND in `git log --oneline`
- Commit `c1b98b3` (Task 3) — FOUND in `git log --oneline`
- `python3 scripts/check-version-stamps.py` re-run at summary time — confirmed exit 0,
  `17 stamps, all '8.26.0'`, `check-version-stamps: PASS`
- `python3 scripts/check-version-stamps.py --self-test` re-run at summary time — confirmed exit 0
- `python3 scripts/sync-content.py --check` re-run at summary time — confirmed exit 0
- `python3 scripts/check-agent.py` re-run at summary time — confirmed exit 0
- `python3 scripts/check-traceability.py --self-test` re-run at summary time — confirmed exit 0
- `/tmp/16-03-l2.txt` (the `unreleased` grep) — confirmed empty at summary time
