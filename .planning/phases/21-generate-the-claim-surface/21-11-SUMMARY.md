---
phase: 21-generate-the-claim-surface
plan: 11
subsystem: tooling
tags: [conf-surface, battery-registration, pre-commit-hooks, ci-gate, drift-gate, d-21-c]
status: complete

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    plan: 10
    provides: "CONF-13's non-exempt findings driven to zero (--check exits 0
      pre-registration); the confirmed forward note that registering
      CONF-SURFACE would move the battery 25/25 -> 26/26."
  - phase: 21-generate-the-claim-surface
    plan: 04
    provides: "BATTERY_ONLY_GATE_IDS verbatim live value ({\"QUAL-01\"}),
      recorded for this plan's byte-unchanged comparison."
provides:
  - "CONF-SURFACE registered as a battery gate (scripts/check-firewall-battery.sh),
    a matching `gen-gate-docs (CONF-SURFACE)` CI job
    (.github/workflows/validation.yml), and both pre-commit hooks
    (.githooks/pre-commit, scripts/git-hooks/pre-commit), in
    self-test-before-check order (WR-05)."
  - "scripts/_gate_registry.py's CONF-SURFACE entry landed as a real
    registered gate (gate_id set, removed from the now-empty
    _ANTICIPATORY_KEYS) rather than the anticipatory placeholder plan
    21-02 seeded."
  - "The battery total's 25 -> 26 move (and CI 22 -> 23, pre-commit-gates-
    per-hook 3 -> 5), produced entirely by scripts/gen-gate-docs.py --write
    against the now-real registry entry, on every surface the generator
    reaches (CLAUDE.md, docs/ARCHITECTURE.md, docs/TESTING.md,
    docs/gates/CONF-SURFACE.md) plus the two surfaces it does not
    (docs/README.md's supersession-chain line; CLAUDE.md's/
    docs/ARCHITECTURE.md's hand-written history paragraphs)."
  - "A genuine pre-existing bug fix: both pre-commit hooks' PY resolution
    changed from \"uv run\" (bare-script PEP-723 isolation) to
    \"uv run python3\" (project-locked .venv), which the new
    gen-gate-docs.py gates exposed — its harvest() subprocess-invokes
    sibling scripts needing PyYAML via sys.executable, which the bare form
    starved."
affects: [21-12]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "hook interpreter resolution must match CLAUDE.md's documented
      'uv run python3 scripts/<name>.py, not uv run scripts/<name>.py'
      convention whenever a hook-invoked script subprocess-invokes a
      sibling script via sys.executable — the bare form's PEP-723 isolation
      silently starves that subprocess of the project's locked
      dependencies."
    - "self-test's own live positive control (check-reports-full-drift-count)
      transitively enforces the same invariant the terminal --check gate
      exists to check, so a real generated-region mutation is caught at the
      self-test gate before the --check gate ever runs; both are still
      independently real, proven by running --check standalone against the
      same mutated tree."

key-files:
  created: []
  modified:
    - scripts/check-firewall-battery.sh
    - .github/workflows/validation.yml
    - scripts/_gate_registry.py
    - scripts/gen-gate-docs.py
    - .githooks/pre-commit
    - scripts/git-hooks/pre-commit
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - docs/TESTING.md
    - docs/gates/CONF-SURFACE.md
    - docs/README.md

key-decisions:
  - "Ran `gen-gate-docs.py --write` inside Task 1 (not deferred whole to
    Task 2) because scripts/_gate_registry.py's own self-test control
    (`entries-count-matches-architecture-table`) requires the live
    docs/ARCHITECTURE.md table to already carry CONF-SURFACE's row the
    moment CONF-SURFACE stops being anticipatory — D-01's battery-id
    equality floor and the anticipatory-exclusion mechanism are coupled
    (both keyed off `_ANTICIPATORY_KEYS`/`gate_id`), so there is no
    intermediate state where the registry is self-consistent but the table
    is still stale. Task 2's own `--write` re-run is idempotent (produces
    zero further diff) and its scope became: wire both hooks, prove they
    fire by mutation, and sweep the two surfaces the generator does not
    reach."
  - "Fixed the hooks' PY=\"uv run\" -> PY=\"uv run python3\" bug in Task 2
    rather than deferring or routing around it: without the fix, every
    contributor with `uv` installed would have a pre-commit hook that
    silently fails CONF-SURFACE's self-test with a D-04-floor-violation
    reason unrelated to real drift, on every commit, forever (Rule 1/3 —
    correctness-blocking, not a scope expansion)."

requirements-completed: [CONF-12]

# Metrics
duration: ~3.5h (single session)
completed: 2026-09-06
---

# Phase 21 Plan 11: Register the Drift Gate Summary

**Registered `CONF-SURFACE` as a battery gate, CI job and both pre-commit hooks (D-21-C); the
`25 -> 26` battery-total move landed on every stating surface, produced entirely by the generator
itself rather than swept by hand — the phase's own demonstration.**

## Status: COMPLETE

## Performance

- **Duration:** ~3.5h, single session
- **Tasks:** 2
- **Commits:** `7bbb2a6` (Task 1), `31643bd` (Task 2)

## Accomplishments

### Task 1: Register CONF-SURFACE in the battery and add its CI job

Added `gate "CONF-SURFACE"` to `scripts/check-firewall-battery.sh`, copying the `CONF-GATE`
block's shape: `python3 scripts/gen-gate-docs.py --self-test` then `--check`, self-test first
(WR-05 ordering). Added the matching `gen-gate-docs (CONF-SURFACE)` CI job to
`.github/workflows/validation.yml`, copying `check-conf-gate`'s block verbatim with the
substitutions the plan named.

Landed `scripts/_gate_registry.py`'s CONF-SURFACE entry as a real registered gate: `gate_id`
changed from `None` to `"CONF-SURFACE"`, `mechanism` changed from the placeholder string to
`_ci("gen-gate-docs")`, and `_ANTICIPATORY_KEYS` emptied (CONF-SURFACE was its only member). The
entry's `consumes` tuple was already correctly filled by an earlier plan (verified against
`gen-gate-docs.py --describe`'s live emission — all 7 keys matched exactly), so no change was
needed there.

Ran `gen-gate-docs.py --write` to bring `docs/ARCHITECTURE.md`'s/`CLAUDE.md`'s/`docs/TESTING.md`'s
generated regions and `docs/gates/CONF-SURFACE.md`'s Facts fence into agreement with the now-real
entry — required by `_gate_registry.py`'s own `entries-count-matches-architecture-table` self-test
control, which asserts the live table's row count against `len(ENTRIES)` minus anticipatory
entries; with `_ANTICIPATORY_KEYS` now empty, that control needed the row to already exist.

**Deviation (Rule 1, bug):** the newly-real CONF-SURFACE entry widened CONF-13's own scanned
docstring surface to include `scripts/gen-gate-docs.py` itself (previously excluded while
anticipatory). Its module docstring restated the same hand-maintained "41% of all review findings"
figure `scripts/_gate_registry.py`'s docstring carries (which was never scanned, since
`_gate_registry.py` is not itself a script-backed registry entry). Reworded to point at that
figure's source instead of re-typing it, and refreshed two stale comments ("generate_all() is a
stub", "the anticipatory CONF-SURFACE") left over from an earlier plan that no longer matched the
landed state. Fixed inline before the file was staged; `gen-gate-docs.py --check` confirmed 0
non-exempt findings after the fix.

**Verification (all run against the real repo):**

- `bash scripts/check-firewall-battery.sh`:
  ```
  FIREWALL: GREEN (26/26)
  ```
- **Call-site derivation** (counted, not read from header prose): 25 `gate`/`gate_prereq` call
  sites in `scripts/check-firewall-battery.sh` (VAL-03 has two — a `gate` branch and a
  `gate_prereq` branch, mutually exclusive at runtime), 24 unique gate ids after dedup (23 prior +
  `CONF-SURFACE`). `24 + 2 inline (INVARIANT-CHECK, FROZEN-EVIDENCE) = 26`.
- `python3 scripts/_gate_registry.py --self-test`: `SELF-TEST PASS — 16 controls run`.
- `python3 scripts/gen-gate-docs.py --self-test`: `SELF-TEST PASS — 49 controls run`.
- `python3 scripts/gen-gate-docs.py --check`: exit 0, `harvested 22/22 expected script-backed
  entries (22 total)`.
- `python3 scripts/check-registration.py` (live): exit 0 — `Battery gates: 24 registered ...
  CI-matched: 23; battery-only by design: 1 (QUAL-01)`.
- `BATTERY_ONLY_GATE_IDS`: byte-unchanged — `scripts/check-registration.py` was not modified at
  all in this plan (`git diff --stat -- scripts/check-registration.py` empty).

**REG-GUARD mutation-proof arms (rsync scratch copy, deleted after use, real repo
`git status --porcelain` confirmed empty before and after):**

- **Arm 1 — job deleted:** removed the `gen-gate-docs:` job block from the scratch copy's
  `.github/workflows/validation.yml`. `python3 scripts/check-registration.py` exit 1:
  ```
  battery gate has no CI job: 'CONF-SURFACE' is registered in scripts/check-firewall-battery.sh
  but no job in .github/workflows/validation.yml declares it (expected a `name: <job> (<GATE-ID>)`
  entry)
  ```
- **Arm 2 — suffix dropped:** renamed `name: gen-gate-docs (CONF-SURFACE)` to `name: gen-gate-docs`
  (job block kept). `python3 scripts/check-registration.py` exit 1, identical failure text naming
  `CONF-SURFACE` — proving the grammar, not merely the job's existence, is what REG-GUARD checks.

### Task 2: Wire both pre-commit hooks, then let the generator produce the 25 -> 26 move

Appended two gates to **both** `.githooks/pre-commit` and `scripts/git-hooks/pre-commit`, in
lockstep and the same order: `$PY scripts/gen-gate-docs.py --self-test || exit $?` then
`exec $PY scripts/gen-gate-docs.py --check`. This forced the exec-slot handover: the previously-
terminal `report-conformance.py --check` became a plain `|| exit $?`, and `gen-gate-docs.py --check`
took the terminal slot. Both files' command sequences are identical (5 commands, exactly one
`exec`, last) modulo the pre-existing `echo`-vs-`printf` cosmetic asymmetry the files' own header
comment already documents.

**Deviation (Rule 1/3, bug, blocking):** wiring exposed that both hooks resolved `PY="uv run"`
(the bare-script form). `scripts/gen-gate-docs.py`'s `harvest()` subprocess-invokes several
sibling scripts via `sys.executable` (D-21-A) to run their `--describe` legs; under
`uv run scripts/gen-gate-docs.py` (bare form), `uv` builds a fresh PEP-723-isolated environment
scoped to *that script's own* declared dependencies (none), so `sys.executable` inside it lacks
the PyYAML several harvested siblings need — `--self-test`/`--check` silently degraded to a
D-04-floor-violation exit ("registry entry requests field X but the script's `--describe` does not
emit it") rather than the intended CONF-13 residual check. Reproduced identically via
`uv run scripts/gen-gate-docs.py --check` directly in the real repo (not just the scratch copy),
confirming this was not scratch-environment noise. Fixed by changing `PY="uv run"` to
`PY="uv run python3"` in both hooks, matching the "`uv run python3 scripts/<name>.py`, NOT
`uv run scripts/<name>.py`" convention `.github/workflows/validation.yml`'s own header (quoted in
`CLAUDE.md`) already documents for exactly this class of version-drift risk. Verified the fix
resolves the D-04-floor-violation symptom in the scratch copy (with `uv sync` run there too) before
proceeding to the mutation-proof arms below.

Updated each hook's header comment (three gates -> five, describing all five in order) and the
"Two gates fire" section in `CLAUDE.md` (rewritten to five). Ran `python3 scripts/gen-gate-docs.py
--write`, which was a no-op diff (Task 1 had already produced the generated-region move) — the
remaining work was sweeping the two current-fact battery-total statements the generator does not
reach: `docs/README.md`'s supersession-chain line (`battery 15/15 -> 25/25` corrected to `-> 26/26`
— its endpoint is the current live total, not a historical figure) and `CLAUDE.md`'s/
`docs/ARCHITECTURE.md`'s hand-written history paragraphs immediately below the generated table
(added a `CONF-SURFACE` registration sentence to each; corrected "currently 25/25" -> "26/26" and
the `gate`/`gate_prereq` tally 23 -> 24). `docs/MEASUREMENT-MAP.md` and `docs/COMPONENT-DIAGRAM.md`
carried no numeric battery-total or pre-commit-gate-count literal in scope — swept and confirmed
clean, nothing to change.

**Hook-firing mutation-proof arms (full local git repo in scratch, `uv sync`'d, deleted after use,
real repo `git status --porcelain` confirmed empty before and after both arms):**

- **Arm A — generated-region drift:** hand-edited `CLAUDE.md`'s generated battery-total line
  (`**26 tallied**` -> `**99 tallied**`) and attempted a commit. **Blocked, exit 1.** The failure
  surfaced at gate 4 (`gen-gate-docs.py --self-test`), not gate 5, because self-test's own live
  positive control (`check-reports-full-drift-count`) internally calls `main(["--check"])` against
  the real tree and asserts no drift — it reported:
  ```
  gen-gate-docs: SELF-TEST FAIL [check-reports-full-drift-count] — DRIFT: CLAUDE.md
  --- a/CLAUDE.md
  +++ b/CLAUDE.md
  @@ -175,7 +175,7 @@ ...
  -Gates run on three surfaces: ... **99 tallied in the offline battery** ...
  +Gates run on three surfaces: ... **26 tallied in the offline battery** ...
  ```
  Independently confirmed `gen-gate-docs.py --check` (gate 5's exact command) run standalone
  against the same mutated tree *also* fails, exit 0 command line printing the same `CLAUDE.md`
  diff — proving gate 5's mechanism is real and would have caught it independently, even though
  gate 4 fired first in the sequential hook.
- **Arm B — self-test broken, unrelated to drift:** reset the CLAUDE.md mutation, then injected
  `assert False, "INJECTED SELF-TEST BREAKAGE"` as the first statement inside the
  `check-reports-full-drift-count` control (a defect with no relationship to real tree drift).
  Attempted a commit. **Blocked, exit 1, no commit landed** (`git log --oneline -1` still showed
  the pre-mutation baseline commit). Failure:
  ```
  gen-gate-docs: SELF-TEST FAIL [check-reports-full-drift-count] — INJECTED SELF-TEST BREAKAGE (mutation-proof arm B)
  ```
  No `--check` DRIFT output appeared anywhere in the captured output — gate 5 never ran, proving
  the self-test-before-check ordering is real, not merely documented.

**Determinism proof (25 -> 26 move fully attributable to the generator):** archived the
pre-registration commit (`649145a0b44f1da3edba54d6a4955af1c09cdcda`) into a scratch directory via
`git archive`, copied in only this plan's non-generated source edits (`check-firewall-battery.sh`,
`_gate_registry.py`, `gen-gate-docs.py`, `validation.yml`), and ran `gen-gate-docs.py --write`
there. The resulting `CLAUDE.md`, `docs/ARCHITECTURE.md` and `docs/TESTING.md` generated-region
spans are **byte-identical** to the real committed tree. `docs/gates/CONF-SURFACE.md`'s own Facts
fence differs only in its derived literal-scan counts (`deferred-remediation`=134/`hits`=153 in
the archived-and-rewritten copy vs. 138/157 in the real tree) — expected and explained: Task 2's
own added narrative (the hook headers, the CLAUDE.md/ARCHITECTURE.md history-paragraph sentences,
the PY-fix comments) is additional scan-surface text the archived pre-registration state does not
contain, and CONF-SURFACE's own Facts fence describes the live scan surface as-is.

**Verification:**

- `python3 scripts/gen-gate-docs.py --write` twice: byte-identical (no residual diff after the
  second run).
- `python3 scripts/gen-gate-docs.py --check`: exit 0, zero non-exempt scanner findings.
- `bash scripts/check-firewall-battery.sh`: `FIREWALL: GREEN (26/26)`.
- `python3 scripts/check-links.py`: `PASS (303 markdown links + 6 namespace refs across 156
  files)`; `--self-test` PASS.
- `python3 scripts/check-traceability.py --self-test`: PASS (HEADLINE-LOCK invariance arms
  unmoved).
- `python3 scripts/check-quality-harness.py --self-test`: PASS — all three CONTRACT-06 pins
  (`chain_detector_pin`, `conclusion_claims_pin`, `slice_sections_pin`) byte-unchanged.
- `git diff --stat -- CHANGELOG.md docs/v8.0-final-closure.md`: empty (frozen documents untouched).
- `git status --porcelain`: empty in the real repo before and after every scratch mutation.

## Per-surface battery-total readings (final)

| Surface | Reading |
|---|---|
| `CLAUDE.md` (generated table + arithmetic sentence) | 26 |
| `CLAUDE.md` (hand-written history paragraph, "currently **26/26**") | 26 |
| `CLAUDE.md` ("Pre-commit gates" section) | 5 gates, described in order |
| `docs/ARCHITECTURE.md` (generated table + arithmetic sentence) | 26 |
| `docs/ARCHITECTURE.md` (hand-written history paragraph) | 26 (CONF-SURFACE sentence added) |
| `docs/TESTING.md` (generated index) | CONF-SURFACE row present, key column no longer `—` |
| `docs/gates/CONF-SURFACE.md` (generated Facts fence) | `registered_surfaces`=30, `checked_files`=57 (includes its own script now) |
| `docs/README.md` (supersession-chain line) | `battery 15/15 -> 26/26` |
| `docs/MEASUREMENT-MAP.md` | No battery-total or pre-commit-gate-count literal in scope — nothing to change |
| `docs/COMPONENT-DIAGRAM.md` | No battery-total or pre-commit-gate-count literal in scope — nothing to change |
| `CHANGELOG.md`, `docs/v8.0-final-closure.md` | Untouched (historical, protected) |

## Task Commits

1. **Task 1: Register CONF-SURFACE in the battery and add its CI job** — `7bbb2a6` (feat)
2. **Task 2: Wire both pre-commit hooks, sweep the 25 -> 26 move** — `31643bd` (feat)

**Plan metadata:** this commit (SUMMARY only — STATE/ROADMAP excluded per worktree mode; the
orchestrator owns those writes after the wave completes)

## Files Created/Modified

- `scripts/check-firewall-battery.sh` — `gate "CONF-SURFACE"` registration block; header prose
  updated (gate count, tally arithmetic, new composition-change note)
- `.github/workflows/validation.yml` — new `gen-gate-docs (CONF-SURFACE)` job
- `scripts/_gate_registry.py` — CONF-SURFACE entry landed as real (`gate_id`, `mechanism`);
  `_ANTICIPATORY_KEYS` emptied; surrounding comments updated
- `scripts/gen-gate-docs.py` — module docstring reworded (dropped a restated "41%" hand-maintained
  literal, corrected stale "stub"/"anticipatory" comments); `cmd_check`'s harvest-summary print
  statement no longer hardcodes "anticipatory CONF-SURFACE"
- `.githooks/pre-commit`, `scripts/git-hooks/pre-commit` — two new gates appended (self-test then
  check), exec-slot handover, `PY="uv run"` -> `PY="uv run python3"` bug fix, header comments
  updated
- `CLAUDE.md` — generated table regenerated; history paragraph and "Pre-commit gates" section
  updated
- `docs/ARCHITECTURE.md` — generated table regenerated; history paragraph updated
- `docs/TESTING.md` — generated index regenerated (CONF-SURFACE row no longer `—`)
- `docs/gates/CONF-SURFACE.md` — Facts fence regenerated
- `docs/README.md` — supersession-chain line corrected (25/25 -> 26/26)

## Decisions Made

See `key-decisions` in frontmatter, summarized: (1) `--write` ran inside Task 1 because
`_gate_registry.py`'s own self-test requires it the moment the anticipatory exclusion is removed —
there is no self-consistent intermediate state; (2) the `PY="uv run"` -> `"uv run python3"` bug fix
was applied immediately rather than deferred, since leaving it would have shipped a pre-commit hook
that silently fails for every future contributor with `uv` installed.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] gen-gate-docs.py's own docstring restated a hand-maintained "41%" figure**
- **Found during:** Task 1, running `gen-gate-docs.py --check` after landing CONF-SURFACE as a
  real (non-anticipatory) registry entry
- **Issue:** CONF-SURFACE's widened scan surface now included `scripts/gen-gate-docs.py`'s own
  module docstring, which restated `scripts/_gate_registry.py`'s "41% of all review findings"
  figure verbatim, with no corroborating fence — the standard CONF-13 violation shape.
- **Fix:** Reworded to point at `_gate_registry.py`'s docstring for the figure instead of
  re-typing it; also corrected two stale comments describing a pre-`--write`-landed state
  ("`generate_all()` is a stub", "the anticipatory CONF-SURFACE") that no longer matched reality.
- **Files modified:** `scripts/gen-gate-docs.py`
- **Verification:** `gen-gate-docs.py --check` exits 0 with zero non-exempt findings after the fix.
- **Committed in:** `7bbb2a6`

**2. [Rule 1/3 - Bug, blocking] Both pre-commit hooks' PY="uv run" starved gen-gate-docs.py's
harvest() of PyYAML**
- **Found during:** Task 2, the first hook-firing mutation-proof arm
- **Issue:** `PY="uv run"` (bare-script form) gives `gen-gate-docs.py` a PEP-723-isolated
  environment scoped to its own (empty) declared dependencies; its `harvest()` shells out to
  sibling scripts needing PyYAML via `sys.executable`, which resolves inside that same starved
  environment — `--self-test`/`--check` degraded to an unrelated D-04-floor-violation exit.
  Reproduced directly in the real repo with `uv run scripts/gen-gate-docs.py --check`, confirming
  this was a real, non-scratch-specific defect.
- **Fix:** `PY="uv run"` -> `PY="uv run python3"` in both hook files, matching the documented
  project convention already followed by every CI job.
- **Files modified:** `.githooks/pre-commit`, `scripts/git-hooks/pre-commit`
- **Verification:** re-ran both mutation-proof arms after the fix; both correctly blocked for the
  intended reason (real drift / injected self-test breakage), not the PyYAML-starvation symptom.
- **Committed in:** `31643bd`

**Total deviations:** 2 auto-fixed (both Rule 1, one also Rule 3/blocking) — both surfaced by the
plan's own required verification steps, fixed before the affected files were staged.

## Assumption Drift (advisory)

- **Found during:** Task 2, sweeping surfaces the generator does not reach
- **Planned assumption:** the plan's action text states "the pre-commit count `2 -> 3` propagate[s]
  to `CLAUDE.md`, `docs/ARCHITECTURE.md` and `docs/TESTING.md`'s generated regions without a hand
  edit," alongside the `25 -> 26` move.
- **What turned out true:** no such move exists in the generated output. The generator's
  registered-surfaces/pre-commit-hooks count (rendered as `**2 pre-commit** hooks` in the
  arithmetic sentence) tracks the number of pre-commit-only *mechanism rows* in the registry
  (`PRECOMMIT:sync-drift-gate`, `PRECOMMIT:conformance-baseline-drift-gate` — both unchanged, since
  CONF-SURFACE's own mechanism renders as `(CI)`, not a third synthetic pre-commit-only row) and
  the number of hook *files* (2, unchanged). What actually moved from 3 to 5 is the number of
  gate *commands* inside each hook file's body — a fact stated only in the hooks' own header prose
  and in `CLAUDE.md`'s hand-written "Pre-commit gates" section, both updated by hand in this plan
  (not generated).
- **Why it matters:** advisory only — this did not change what needed sweeping (the hooks' header
  prose and `CLAUDE.md`'s narrative were updated regardless, just not via the mechanism the plan
  text predicted), and no acceptance criterion depended on a literal `2 -> 3` generated-region diff
  existing. Recorded so a future reader checking `git diff` for that specific move does not
  conclude it was missed.

## Disclosed Scanner Bound (backlog)

D-21-E's CONF-13 candidate surface set is Markdown files plus Python module docstrings
(`ast.get_docstring()`) — it structurally cannot reach shell scripts. Both pre-commit hooks and
`scripts/check-firewall-battery.sh` carry hand-maintained gate-count prose in `#`-comments that is
now outside the scanner's reach and was updated by hand in this plan, matching plan 21-10's own
disclosed-bound pattern for the same class of surface:

- `.githooks/pre-commit:2`, `scripts/git-hooks/pre-commit:2` — `"Five gates for shared/ <->
  generated trees..."` (hand count, correct as of this plan)
- `scripts/check-firewall-battery.sh:18` — `"# Gates (26):"` (hand count, correct as of this plan)
- `scripts/check-firewall-battery.sh:26` — `"# 23 of the 24 non-inline gates..."` (hand count,
  correct as of this plan)

Filed as a named backlog item (no new id assigned — matches the existing `999.33`-class root cause
plan 21-10 already recorded for `.py` docstrings; shell comments are the same shape one file-type
wider) rather than silently absorbed. No action taken beyond recording it here, per the plan's own
instruction to note rather than fix a surface D-21-E does not scan.

## Issues Encountered

None beyond the two deviations above, both resolved within this plan's own scope.

## Next Phase Readiness

- **This plan is COMPLETE.** Both tasks landed: `7bbb2a6` (Task 1), `31643bd` (Task 2).
- `bash scripts/check-firewall-battery.sh` reports **FIREWALL: GREEN (26/26)** against the
  committed state.
- CONF-SURFACE is fully self-documenting: its own registry entry, `docs/gates/CONF-SURFACE.md`
  page, and table row in both generated tables — no self-documentation exceptions.
- No blockers for plan 21-12.

## Known Stubs

None. CONF-SURFACE's generated table row, detail page, CI job and both pre-commit hooks are fully
wired and drift-checked — no placeholder or silently-absorbed gap.

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-06*

## Self-Check: PASSED

- FOUND: commit `7bbb2a6` (Task 1), `31643bd` (Task 2) — `git log --oneline --all`
- FOUND: `scripts/check-firewall-battery.sh` contains `gate "CONF-SURFACE"`
- FOUND: `.github/workflows/validation.yml` contains `name: gen-gate-docs (CONF-SURFACE)`
- FOUND: `.githooks/pre-commit` and `scripts/git-hooks/pre-commit` both contain
  `scripts/gen-gate-docs.py --self-test` and `exec $PY scripts/gen-gate-docs.py --check`
- FOUND: `docs/gates/CONF-SURFACE.md` exists with a regenerated Facts fence
- FOUND: `python3 scripts/gen-gate-docs.py --check` exits 0 (real exit code confirmed)
- FOUND: `python3 scripts/gen-gate-docs.py --self-test` exits 0 (49 controls)
- FOUND: `python3 scripts/_gate_registry.py --self-test` exits 0 (16 controls)
- FOUND: `python3 scripts/check-registration.py` (live) exits 0
- FOUND: `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (26/26)`
- FOUND: `git diff --stat -- CHANGELOG.md docs/v8.0-final-closure.md` empty
- FOUND: `git status --short` shows only this plan's intended files; both scratch copies deleted
  after use with the real repo confirmed clean before and after
