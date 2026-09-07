---
phase: 21-generate-the-claim-surface
plan: 13
subsystem: infra
tags: [gate-registry, claim-surface, pre-commit, gen-gate-docs, self-test]

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    provides: "plan 21-11's CONF-SURFACE claim-surface generator/drift gate and plan 21-12's claim-surface conformance closure"
provides:
  - "Five PRECOMMIT: registry rows (one per hook gate) instead of two rows standing in for five"
  - "hook_gate_invocations()/hook_roster_problems(): a derived floor comparing both hook scripts' own invocation sequences against each other and against the registry's run_command set"
  - "A disambiguated population-arithmetic sentence: '{N} pre-commit gates' plus a separately-derived hook_mechanism_count, replacing the ambiguous '{N} pre-commit** hooks' wording"
  - "Three corrected hand-written count literals (docs/TESTING.md's 'Two gates', CLAUDE.md's '(24 controls)'/'(42 controls)')"
affects: [21-16]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Derived hook-invocation floor: regex-over-source-text extraction (hook_gate_invocations) mirroring battery_gate_ids()'s existing idiom, compared bidirectionally against the registry's run_command set"
    - "Two separately-derived population figures (precommit_count vs hook_mechanism_count) so a reader can never mistake one noun's count for the other's"

key-files:
  created:
    - docs/gates/PRECOMMIT-conformance-generator-self-test.md
    - docs/gates/PRECOMMIT-claim-surface-generator-self-test.md
    - docs/gates/PRECOMMIT-claim-surface-drift-gate.md
  modified:
    - scripts/_gate_registry.py
    - scripts/gen-gate-docs.py
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - docs/TESTING.md
    - docs/gates/CONF-SURFACE.md

key-decisions:
  - "New PRECOMMIT: entries backed by a script another entry already claims consumes for (report-conformance.py claimed by conformance-baseline-drift-gate; gen-gate-docs.py claimed by CONF-SURFACE) leave consumes=() themselves, following the pre-existing DUAL-04/GATE-02-v8.5 precedent of one claiming row per shared script."
  - "hook_roster_problems() takes optional args defaulting to a live read of both real hook files and the real PRECOMMIT: run_command set, so it can be called with zero arguments (as the plan's Task 1 verify command does) while still accepting explicit synthetic tuples for pure, disk-I/O-free falsification-arm controls."
  - "The pre-commit clause's parenthetical states the hook_mechanism_count digit explicitly ('2 hook mechanisms run the identical set...') rather than dropping it, satisfying the plan's 'states the mechanism count separately' requirement."

requirements-completed: [CONF-12, CONF-13]

# Metrics
duration: 33min
completed: 2026-09-07
---

# Phase 21 Plan 13: Disambiguate the pre-commit gate/hook count and close CONF-13's exposed stale literals Summary

**Registered one PRECOMMIT: entry per hook gate (2 -> 5), added a hook-roster floor deriving the registry's run_command set from both hook scripts' own source text, disambiguated the population-arithmetic sentence's "pre-commit" noun to state gates separately from hook mechanisms, and corrected the three hand-written count literals CONF-13 exposed as stale.**

## Performance

- **Duration:** 33 min
- **Started:** 2026-09-07T07:19:00-04:00 (approx, first Read)
- **Completed:** 2026-09-07T07:30:22-04:00
- **Tasks:** 3
- **Files modified:** 9 (6 modified, 3 created)

## Accomplishments
- `scripts/_gate_registry.py`'s `ENTRIES` now carries one `PRECOMMIT:` row per hook GATE (5 total: sync-drift-gate, conformance-generator-self-test, conformance-baseline-drift-gate, claim-surface-generator-self-test, claim-surface-drift-gate), floored by set equality against both `.githooks/pre-commit` and `scripts/git-hooks/pre-commit`'s own derived invocation sequences, in both directions, plus a hook-divergence check — all via `hook_gate_invocations()`/`hook_roster_problems()`, four new registered self-test controls, and `_registry_precommit_ids()`'s dead `e.script is not None` clause removed.
- `scripts/gen-gate-docs.py`'s `_population_counts` now derives a second, independent `hook_mechanism_count` (distinct hook script relpaths on disk) alongside `precommit_count` (PRECOMMIT: row count); `_population_arithmetic_sentence` renders `"**5 pre-commit gates** (2 hook mechanisms run the identical set in the identical order)"`, replacing the ambiguous `"**2 pre-commit** hooks"` wording. Two new registered self-test controls assert the noun and the independence of the two derivations.
- `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/TESTING.md` and `docs/gates/` regenerated via `gen-gate-docs.py --write` (34 files written, run twice to converge after CONF-SURFACE's own facts-fence self-reference stabilized).
- Three hand-written count literals corrected: `docs/TESTING.md`'s "Two gates ... the sync-drift gate and the conformance-baseline drift gate" -> a five-gate enumeration; `CLAUDE.md`'s "(24 controls)" -> "(33 controls)" and "(42 controls)" -> "(43 controls)" for `check-provenance.py`/`check-conf-gate.py`. `docs/ARCHITECTURE.md`'s "five gates each, up from three" and "Two gates are called GATE-02" statements were verified against the hooks and left byte-unchanged (already correct).

## Task Commits

1. **Task 1: Register one PRECOMMIT entry per hook gate and floor the roster against the hooks themselves** - `7df2fe8` (feat)
2. **Task 2: Disambiguate the arithmetic sentence's nouns and regenerate the claim surface** - `535f0b5` (feat)
3. **Task 3: Correct the three live stale hand-written count literals this gap exposed** - `418575e` (docs)

_No plan-metadata commit in this worktree run — orchestrator handles STATE.md/ROADMAP.md centrally after merge._

## Files Created/Modified
- `scripts/_gate_registry.py` - 3 new PRECOMMIT: entries, `_HOOK_PATHS`/`hook_gate_invocations()`/`hook_roster_problems()`, 4 new self-test controls, dead-clause removal, docstring count updates (28 -> 31 rows)
- `scripts/gen-gate-docs.py` - `hook_mechanism_count` in `_population_counts`, disambiguated `_population_arithmetic_sentence`, extended `_control_population_arithmetic_derived` plus 2 new controls
- `CLAUDE.md` - regenerated gate table/arithmetic sentence (generated region) + 2 corrected control-count literals (hand-written)
- `docs/ARCHITECTURE.md` - regenerated gate table/arithmetic sentence (generated region only; hand-written prose confirmed correct, untouched)
- `docs/TESTING.md` - regenerated gate index (generated region) + corrected "Two gates" -> "Five gates" sentence (hand-written)
- `docs/gates/CONF-SURFACE.md` - regenerated Facts fence (checked_files/derived_counts/control_ids/control_count moved to reflect the 3 new pages and 51 controls)
- `docs/gates/PRECOMMIT-conformance-generator-self-test.md` - new thin detail page
- `docs/gates/PRECOMMIT-claim-surface-generator-self-test.md` - new thin detail page
- `docs/gates/PRECOMMIT-claim-surface-drift-gate.md` - new thin detail page

## Decisions Made
- New PRECOMMIT: entries sharing a script with an existing consumes-bearing entry (report-conformance.py, gen-gate-docs.py) left `consumes=()` themselves, following the DUAL-04/GATE-02-v8.5 precedent — the field-resolution floor is per-script, not per-entry, so duplicating the same field names across sibling rows would be redundant, not additive.
- `hook_roster_problems()` uses optional args defaulting to live reads (both real hook files, real registry `run_command` set) so it supports both the zero-arg live-check call shape the plan's Task 1 verify command uses AND pure, disk-I/O-free calls from the falsification-arm controls.
- Kept the hook_mechanism_count digit visible in the rendered sentence's parenthetical ("2 hook mechanisms run the identical set...") per the plan's "states the mechanism count separately" instruction, rather than dropping it as an implicit "both."

## Deviations from Plan

None - plan executed exactly as written. All three tasks' documented "EXPECTED INTERMEDIATE STATE" (Task 1's `entries-count-matches-architecture-table` self-test failure and `gen-gate-docs.py --check` drift) occurred exactly as predicted and cleared in Task 2 as designed.

## Correction Record (for plan 21-16)

| Literal | Live figure | Command | Disposition |
|---|---|---|---|
| `docs/TESTING.md:64` "Two gates ... the sync-drift gate and the conformance-baseline drift gate" | 5 gates | `.githooks/pre-commit`/`scripts/git-hooks/pre-commit`'s 5 `$PY` invocation lines | Corrected to a five-gate enumeration |
| `CLAUDE.md`'s `check-provenance.py --self-test` comment "(24 controls)" | 33 | `python3 scripts/check-provenance.py --describe` -> `control_count: 33` | Corrected to "(33 controls)" |
| `CLAUDE.md`'s `check-conf-gate.py --self-test` comment "(42 controls)" | 43 | `python3 scripts/check-conf-gate.py --describe` -> `control_count: 43` | Corrected to "(43 controls)" |
| `docs/ARCHITECTURE.md`'s "five gates each, up from three" | 5 (both hooks, verified) | Read of both hook files' header comments and `$PY` line counts | Confirmed correct — left unchanged |
| `docs/ARCHITECTURE.md`'s "Two gates are called GATE-02" | Correct number, different noun (VAL-04/GATE-02 vs GATE-02-v8.5) | Manual read | Confirmed correct — left unchanged (not a defect) |

## Falsification Arms Recorded (verbatim failure text)

**Hook `missing=` (registered control `cr04-hook-roster-missing-fires`):**
```
hook-roster missing=: hook gate(s) with no PRECOMMIT: registry row: ['python3 scripts/check-agent.py --self-test']
```

**Hook `extra=` (registered control `cr04-hook-roster-extra-fires`):**
```
hook-roster extra=: PRECOMMIT: registry row(s) naming an invocation neither hook makes: ['python3 scripts/check-links.py --check']
```

**Hook divergence (registered control `cr04-hook-roster-divergence-fires`):**
```
hook-divergence: the two hook scripts' derived invocation sequences differ: ['python3 scripts/sync-content.py --check', 'python3 scripts/report-conformance.py --self-test'] != ['python3 scripts/sync-content.py --check', 'python3 scripts/report-conformance.py --check']
```

**Arithmetic-noun regression (registered control `arithmetic-sentence-names-gates-not-hooks`, on an rsync scratch copy):**
```
gen-gate-docs: SELF-TEST FAIL [arithmetic-sentence-names-gates-not-hooks] — Gates run on three surfaces: **23 in CI** (`.github/workflows/validation.yml`, on push/PR to master), **26 tallied in the offline battery** (`bash scripts/check-firewall-battery.sh`), and **5 pre-commit** hooks. The battery is a strict superset of CI: all 23 CI gates plus 1 battery-only gate plus 2 inline checks. That is 23 + 1 + 2 = 26.
```
Real tree `git status --porcelain` was byte-identical before and after this scratch run.

**Deleted PRECOMMIT row (registered control `cr04-hook-roster-live-positive`, on an rsync scratch copy):**
```
_gate_registry: SELF-TEST FAIL [cr04-hook-roster-live-positive] — ["hook-roster missing=: hook gate(s) with no PRECOMMIT: registry row: ['python3 scripts/gen-gate-docs.py --self-test']"]
```
Real tree `git status --porcelain` was byte-identical before and after this scratch run.

## Verification Evidence

- `python3 scripts/_gate_registry.py --self-test` -> `_gate_registry: SELF-TEST PASS — 20 controls run`
- `python3 scripts/gen-gate-docs.py --self-test` -> `gen-gate-docs: SELF-TEST PASS — 51 controls run`
- `python3 scripts/gen-gate-docs.py --check` -> exit 0, `harvested 22/22 expected script-backed entries (22 total)`
- `bash scripts/check-firewall-battery.sh` -> `FIREWALL: GREEN (26/26)` (total unchanged; ran `uv sync` first to make VAL-03's pytest leg resolvable in this worktree, which had no `.venv`)
- `sh .githooks/pre-commit` -> exit 0
- `sh scripts/git-hooks/pre-commit` -> exit 0
- Four independent pre-commit-count surfaces mechanically confirmed equal at 5: `docs/TESTING.md`, `CLAUDE.md`'s hand-written section, `CLAUDE.md`'s generated arithmetic sentence, `.githooks/pre-commit`'s `$PY` invocation count.

## Issues Encountered
- This worktree checkout had no `.planning/` plan/state files (`.planning/` is gitignored except force-tracked `*-SUMMARY.md` files) — copied `21-13-PLAN.md`, `21-CONTEXT.md`, `PROJECT.md`, `STATE.md`, `config.json` from the main repo working tree before starting.
- This worktree had no `.venv`, so VAL-03's pytest leg initially reported `[PREREQ]`/`BLOCKED` rather than `[PASS]`/GREEN. Ran `uv sync` (declared project dev dependency, not a package-manager install of a new/unverified package) to create it, after which the full battery read GREEN 26/26.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- CONF-12's `missing:` gap (hook-roster derivation) and CONF-13's three exposed stale literals are both closed.
- Plan 21-16 can consume the Correction Record above directly rather than re-deriving which literals were already dealt with.

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-07*

## Self-Check: PASSED

All 9 created/modified files confirmed present on disk; all 3 task commit hashes (`7df2fe8`, `535f0b5`, `418575e`) confirmed present in `git log --oneline -5`.
