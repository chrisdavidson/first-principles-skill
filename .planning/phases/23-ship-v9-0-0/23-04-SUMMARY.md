---
phase: 23-ship-v9-0-0
plan: 04
subsystem: release-gate-reconciliation
tags: [reg-guard, gate-registry, conf-gate, conf-surface, falsification-mutation, no-fix-fence]

# Dependency graph
requires:
  - phase: 23-ship-v9-0-0
    plan: 03
    provides: "All 17 version stamps at 9.0.0, commit a27a308"
provides:
  - "Verbatim FIREWALL: GREEN (26/26) reading on the post-stamp-bump tree"
  - "Battery/registry/CI id-set reconciliation by equality, with the exact one-way exemption boundary REG-GUARD's own code enforces (QUAL-01 only, scoped to the 24 call-site ids)"
  - "Gate-count surface sweep: every stating surface already agreed with the live composition — zero edits needed"
  - "Registration floor proven to fire by name on three scratch-copy mutations, including a count-preserving id swap"
affects: ["23-05"]

tech-stack:
  added: []
  patterns: ["set reconciliation scoped to the checker's own comparison population, not an assumed uniform population", "falsification by disposable rsync scratch copy, reverted and md5-confirmed"]

key-files:
  created: []
  modified: []

key-decisions:
  - "REG-GUARD's own CI-job-registration axis (verify_ci_job_registration / extract_battery_gate_ids) scopes its battery-gate population to the 24 gate/gate_prereq call sites only, NOT the 26-member set that includes the two inline checks (INVARIANT-CHECK, FROZEN-EVIDENCE) — confirmed by reading the live script and by running it, not assumed from the plan's Set A definition. Reported both scopes explicitly rather than silently picking one."
  - "No hand edit was needed anywhere in task 2's sweep — every gate-count-stating surface already agreed with the live-derived composition (26 total: 24 registrations + 2 inline). Recording that as the finding, per the plan's own instruction not to manufacture an edit."

requirements-completed: [REL-02]

# Metrics
duration: ~35min
completed: 2026-09-09
---

# Phase 23 Plan 04: Confirm REL-02 — Battery GREEN with Every Phase 21/22 Control Registered Summary

**The battery reads `FIREWALL: GREEN (26/26)` on the post-stamp-bump tree, the battery/registry/CI
id sets reconcile by equality inside the exact comparison scope REG-GUARD's own code uses (one
exemption, QUAL-01, not three), every gate-count-stating surface already agreed with that
composition so no edit was made, and the registration floor was proven — not assumed — to fire by
name on three scratch-copy mutations including one that preserves both id-set counts.**

## Performance

- **Duration:** ~35 min
- **Completed:** 2026-09-09
- **Tasks:** 3 completed (task 1: reconciliation, no commit — reading/recording only; task 2:
  surface sweep, no commit — nothing needed changing; task 3: mutation proof, no commit —
  scratch-copy only)
- **Files modified:** 0 tracked files (this plan makes no commit)

## Accomplishments

### Task 1 — Battery reading and three-way set reconciliation

- Ran `bash scripts/check-firewall-battery.sh` on the post-stamp-bump tree (commit `413d5c5`,
  the last commit before this plan). Verdict recorded verbatim below. Not BLOCKED — GREEN.
- Derived **Set A** (26 members) by parsing `scripts/check-firewall-battery.sh`'s own `gate` /
  `gate_prereq` call sites (24) plus its two inline checks (INVARIANT-CHECK, FROZEN-EVIDENCE),
  and **Set B** (26 members) by parsing `scripts/_gate_registry.py`'s `gate_id="..."` ENTRIES.
  `diff` on the two sorted lists is empty — **A == B by equality**, not subset.
- For the CI-job axis, read `scripts/check-registration.py`'s actual implementation
  (`extract_battery_gate_ids` / `_BATTERY_GATE_RE` / `verify_ci_job_registration`) rather than
  assuming the plan's 26-member Set A applies uniformly. **Found and reported honestly:**
  `_BATTERY_GATE_RE` (`^[ \t]*gate(?:_prereq)?[ \t]+"([^"]+)"`) matches only `gate`/`gate_prereq`
  call sites — it structurally cannot see INVARIANT-CHECK or FROZEN-EVIDENCE, which are inline
  printf checks, not `gate "<ID>"` calls. So REG-GUARD's own CI-job-completeness axis operates
  over a **24-member** population (Set A′), not 26. Confirmed by running the live script
  (`python3 scripts/check-registration.py`), which prints "Battery gates: 24 registered" verbatim.
  **Set C** (23 job-declared ids from `.github/workflows/validation.yml`, including the `GATE-02`
  alias VAL-04's job also carries) computed by parsing every `name:` field under `jobs:`.
  **A′ minus C = {QUAL-01} exactly**, matching `BATTERY_ONLY_GATE_IDS = frozenset({"QUAL-01"})`
  in `scripts/check-registration.py`. **C minus A′ = {GATE-02}** (the pre-existing alias name,
  not a second battery registration — `VAL-04`'s job is `check-trigger-collisions (VAL-04/GATE-02)`).
  If the full 26-member Set A had been used uncritically for this comparison, A minus C would
  read `{QUAL-01, INVARIANT-CHECK, FROZEN-EVIDENCE}` — three members, not one — which would have
  been a **false positive finding** manufactured by ignoring how the checker itself scopes the
  comparison. Reporting the correct scope, evidenced by the live script's own output, is the
  point of "checked against the script rather than against prose."
- Ran `python3 scripts/_gate_registry.py --self-test` (PASS, 21 controls) and
  `python3 scripts/check-registration.py --self-test` (PASS, 29 controls) — both exit 0.
- Discharged the CONF-GATE / CONF-SURFACE naming obligations by direct grep:
  `CONF-GATE` is hit in both `scripts/check-firewall-battery.sh` (`gate "CONF-GATE"` call site,
  line 567, plus header/comment mentions) and `.github/workflows/validation.yml`
  (`name: check-conf-gate (CONF-GATE)`, line 319). `CONF-SURFACE` is hit in both files likewise
  (`gate "CONF-SURFACE"`, line 582; `name: gen-gate-docs (CONF-SURFACE)`, line 333).
- Confirmed CONF-11/12/13 coverage: `scripts/gen-gate-docs.py` names CONF-13 at its own literal
  scanner (`run_literal_scan()`, the standing hand-maintained count-literal scanner), and the
  battery's `CONF-SURFACE` call site runs exactly `gen-gate-docs.py --self-test` then `--check` —
  the two legs that exercise that scanner and the `--describe`-derived generated regions (CONF-11,
  CONF-12). No separate call site is needed; CONF-SURFACE's two legs are what cover all three.
- Confirmed Phase 22 registered no gate, as a **positive finding stated with its reason**, not a
  gap: `CLAUDE.md` § "Review protocol" states in its own words, "No script, control or CI job
  enforces any of this" — CONF-14/CONF-15 are prose deliverables (the depth rule in
  `docs/PROCESS.md`, the product/apparatus review split), and no gate was invented to cover them
  in this phase, per the plan's instruction.
- Derived the battery tally from counted call sites: **26 total = 24 `gate`/`gate_prereq`
  registrations + 2 inline checks** (INVARIANT-CHECK, FROZEN-EVIDENCE), counted directly from
  `scripts/check-firewall-battery.sh`'s source, not read off any prose surface.
- Captured the CR-02/CR-03 fence baseline into the scratchpad
  (`cr02-base.txt` 37 lines, `cr03-base.txt` 42 lines — both non-empty, guarding the vacuous
  case). `git status --porcelain` was empty before and after this task — it modifies nothing.

**Battery verdict, verbatim** (`bash scripts/check-firewall-battery.sh`, full output):

```
=== Phase 128 Offline Firewall Battery (READY-03 / D-06) ===

[PASS] DUAL-04         sync-content.py --check
[PASS] GATE-02-v8.5    sync-content.py --self-test (pointer drift-guard)
[PASS] STEP0-06        check-step0-live.py --self-test
[PASS] STEP0-08        check-step0-emulator.py --self-test
[PASS] VAL-01          claude plugin validate ./first-principles
[PASS] VAL-02          markdownlint-cli2 first-principles/**/*.md
[PASS] VAL-03          check-links.py --self-test + live + .venv/bin/python3 -m pytest check-links_anchors_test.py
[PASS] VAL-04          check-trigger-collisions.py --self-test + live
[PASS] VAL-05          check-description-budget.py
[PASS] VERSION-01      check-version-stamps.py --self-test + live
[PASS] REG-GUARD       check-registration.py --self-test + live
[PASS] GATE-01         check-agent.py --self-test + live shipped agent (AGENT_FILE)
[PASS] BATT-06         check-routing-battery.py --self-test
[PASS] TRACE-03        check-traceability.py --self-test
[PASS] COLLIDE-01      check-install-collisions.py --self-test + live
[PASS] QUAL-01         check-quality-harness.py --self-test
[PASS] PROV-GUARD      check-provenance.py --self-test + live
[PASS] HARN-01         check-act-limb.py --self-test
[PASS] HARN-02         check-loop-closure.py --self-test
[PASS] HARN-03         check-focused-parity.py --self-test
[PASS] SCAN-GUARD      check-selfaudit-scan.py --self-test + live
[PASS] HC-BOUND        check-high-confidence-bound.py --self-test
[PASS] CONF-GATE       check-conf-gate.py --self-test + live
[PASS] CONF-SURFACE    gen-gate-docs.py --self-test + --check
[INFO] body-size       check-body-budget: REPORT — body is 773 lines (historical reference figure 644, gate retired — TEARDOWN-01)
[PASS] INVARIANT-CHECK  pre-mortem=9 fishbone=7 inversion=13 trade-off=10 MIN_HEADER_HITS=2
[PASS] FROZEN-EVIDENCE  diff-vs-HEAD + untracked sweep: frozen baselines/captures unmodified (D-04)

FIREWALL: GREEN (26/26)
```

Not used to discharge any criterion by itself in this Summary — every claim above stands on its
own set comparison, grep, or script exit status, per the plan's explicit instruction.

### Task 2 — Gate-count surface sweep

- Enumerated every tracked-Markdown hit for battery-tally patterns (`26/26`, `24 -> 25`,
  `25 -> 26`, "battery total", "N gates", etc.), outside `.planning/` (planning artifacts are not
  a shipped surface) and outside protected historical/frozen documents
  (`docs/v8.*`, `CHANGELOG.md`, `docs/requirements-*`, `tests/*/README.md`, `docs/audit-*`) which
  state superseded counts on purpose (protected by an invariance property, not exemption).
- **`CLAUDE.md` § "CI gates"** (generated region, lines 142-182): its own summary sentence
  ("23 in CI ... 26 tallied ... 5 pre-commit ... 23 + 1 + 2 = 26") and the hand-written narration
  immediately below it (`GATE-02-v8.5` ... `CONF-SURFACE was registered at v9.0.0 under Phase 21
  ... moved it from 25 to 26`) — **both agree** with the task-1 derived composition (26). No edit.
- **`docs/ARCHITECTURE.md`** (generated gate table, same source): identical generated sentence
  ("23 in CI, 26 tallied, 5 pre-commit, 23+1+2=26") plus its own hand-written registration-history
  narration ending "this is the `25 -> 26` move produced by CONF-SURFACE itself" — **agrees**,
  chain terminus (26) matches the value counted in task 1. No edit.
- **`docs/TESTING.md`** (generated index, lines 10-46): no hand-written narration outside the
  generated fence states a gate count needing reconciliation. No edit.
- **`docs/README.md:107`**: the row inside "## Standing of the nine milestone documents"
  states "battery 15/15 -> 26/26" — this is inside **CR-03's own fenced section**
  (D-09/D-14 no-fix), so it was read to recognise it and left alone regardless of whether it
  agreed or disagreed. (It happens to already read 26/26, current — the CR-03 finding in that
  same row is about the "13 matrix rows" count, not the battery figure, and is not this plan's
  concern.) No edit — fenced.
- **`CONTRIBUTING.md`**, **`docs/DEVELOPMENT.md`**: reference the battery script by name/command
  but state no numeric gate-count literal. No hit requiring reconciliation.
- **`docs/README.md:62`** and **`docs/PROCESS.md:78,93`**: state "16 gates stayed green" as a
  **historical** v8.13 narrative fact (dated incident record), not a current-fact claim about the
  present battery composition. Out of scope by the same historical-document convention.
- **`docs/requirements-traceability.md`** and **`docs/requirements-matrix.md`**: state historical
  coverage-headline deltas (a *different* count — requirement rows, not battery gates) and
  per-requirement gate-pointer cells; no current battery-tally literal needing reconciliation.
- **No hand edit was made inside any generated region.** `gen-gate-docs.py --check` passing
  (exit 0, "harvested 22/22 expected script-backed entries") is the proof.
- **CR-01 fence:** `git diff --name-only HEAD -- docs/gates/CONF-SURFACE.md` is empty — untouched.
- **CR-02 fence:** re-extracted `CLAUDE.md` § "Review protocol" from the working tree (37 lines,
  non-empty) and diffed against `$SCRATCH/cr02-base.txt` — **empty diff**.
- **CR-03 fence:** re-extracted `docs/README.md` § "Standing of the nine milestone documents"
  from the working tree (42 lines, non-empty) and diffed against `$SCRATCH/cr03-base.txt` —
  **empty diff**.
- All three fences held — no HALT was triggered.
- Ran `python3 scripts/gen-gate-docs.py --self-test` (PASS, 74 controls), then `--check` (exit 0,
  "harvested 22/22 expected script-backed entries"), then the full battery again (GREEN 26/26),
  then `sh .githooks/pre-commit` explicitly (exit 0, all five pre-commit gates green — the
  `report-conformance` "DRIFT" line in its own output is its self-test's own mutated-fixture
  noise, the same expected internal signal `23-03-SUMMARY.md` recorded).
- **Nothing needed changing. No commit exists for task 2** — `git status --porcelain` was empty
  both before and after the sweep.

### Task 3 — Falsification by mutation, not by reading

- Confirmed `git status --porcelain` empty in the real tree before mutation 1 and after mutation
  3's revert.
- Copied the repository with `rsync -a --exclude .git` into the session scratchpad. Confirmed
  both `scripts/check-registration.py` and `scripts/_gate_registry.py` resolve `REPO_ROOT` via
  `Path(__file__).resolve().parents[1]`, not git (same finding as `23-03-SUMMARY.md`), so the
  plan-20-06 git-worktree workaround was not needed — a plain `rsync` copy runs both gates natively.
- Three mutations applied to the scratch copy only, each reverted and confirmed byte-identical by
  `diff` + `md5sum` before the next, with the real repository's `git status --porcelain` unaffected
  throughout.

| # | Mutation | Command | Verbatim result | CAUGHT? |
|---|---|---|---|---|
| 1 | Removed the `gate "CONF-GATE" ... "python3 scripts/check-conf-gate.py"` call-site block from the scratch copy's `scripts/check-firewall-battery.sh`, leaving `scripts/_gate_registry.py`'s CONF-GATE entry untouched | `python3 scripts/_gate_registry.py --self-test` | `_gate_registry: SELF-TEST FAIL [d01-live-battery-equality] — ["D-01: registry names gate id(s) the battery does not register: ['CONF-GATE']"]` — exit 1 | YES — names the exact removed id. **Note:** `check-registration.py --self-test` (in-memory fixtures) still PASSes and its *live* run also still PASSes (exit 0) after this mutation — REG-GUARD's own CI-job axis only checks "every battery-registered gate has a CI job," and CONF-GATE's CI job is unaffected by removing it from the battery; the catch comes from `_gate_registry.py`'s registry<->battery id-equality control, not from REG-GUARD. Recorded as the honest division of labor between the two scripts, not glossed over. |
| 2 | Removed the `gen-gate-docs:` / `name: gen-gate-docs (CONF-SURFACE)` job block from the scratch copy's `.github/workflows/validation.yml`, leaving the battery registration in place | `python3 scripts/check-registration.py` (live; corrected to capture Python's own exit code directly rather than a downstream pipe's) | `Failures:\n    battery gate has no CI job: 'CONF-SURFACE' is registered in scripts/check-firewall-battery.sh but no job in .github/workflows/validation.yml declares it (expected a \`name: <job> (<GATE-ID>)\` entry)` — exit 1 | YES — REG-GUARD's CI-job axis fires naming `CONF-SURFACE` exactly. |
| 3 | Renamed `scripts/_gate_registry.py`'s `INVARIANT-CHECK` entry's `gate_id="INVARIANT-CHECK"` to `gate_id="INVARIANT-CHECK-X"` in the scratch copy — a same-count rename, not a deletion or addition | `python3 scripts/_gate_registry.py --self-test` | `_gate_registry: SELF-TEST FAIL [d01-live-battery-equality] — ["D-01: registry names gate id(s) the battery does not register: ['INVARIANT-CHECK-X']"]` — exit 1 | YES — the set-equality floor fires by name. **Both counts unchanged**, confirmed directly: registry's distinct `gate_id="..."` count stayed **26** before and after (one renamed, none added/removed); the battery's `gate`/`gate_prereq` call-site count stayed **24** before and after (the battery script itself was not touched in this mutation). A count-based floor (`len(registry_ids) == len(battery_ids)`) would have shown 26 == 26 (or 24 == 24 depending on scope) both before and after and **passed** — it is the id-set equality comparison, not a count comparison, that catches the swap. |

`check-registration.py`'s live run after mutation 1 alone (with mutation 2 and 3 not yet applied)
remained PASS — recorded above as the finding about scope, not softened into a false CAUGHT.

Real repository confirmed clean (`git status --porcelain` empty) before mutation 1 and after
mutation 3's revert. No tracked file was modified and no commit was made for task 3. The scratch
mutation copy was deleted after use.

## Verification Results

```
$ bash scripts/check-firewall-battery.sh   (post-stamp-bump tree, before any task-2 edits — none made)
FIREWALL: GREEN (26/26)

$ python3 scripts/_gate_registry.py --self-test
_gate_registry: SELF-TEST PASS — 21 controls run

$ python3 scripts/check-registration.py --self-test
check-registration --self-test: PASS (29 controls: ...)

$ /usr/bin/grep -n "CONF-GATE" scripts/check-firewall-battery.sh .github/workflows/validation.yml
scripts/check-firewall-battery.sh:567:gate "CONF-GATE" \
.github/workflows/validation.yml:319:    name: check-conf-gate (CONF-GATE)
(plus header/comment mentions in the battery script)

$ /usr/bin/grep -n "CONF-SURFACE" scripts/check-firewall-battery.sh .github/workflows/validation.yml
scripts/check-firewall-battery.sh:582:gate "CONF-SURFACE" \
.github/workflows/validation.yml:333:    name: gen-gate-docs (CONF-SURFACE)
(plus header/comment mentions in the battery script)

$ python3 scripts/gen-gate-docs.py --self-test && echo EXIT:0
gen-gate-docs: SELF-TEST PASS — 74 controls run
EXIT:0

$ python3 scripts/gen-gate-docs.py --check && echo EXIT:0
harvested 22/22 expected script-backed entries (22 total)
EXIT:0

$ bash scripts/check-firewall-battery.sh && echo EXIT:0   (re-run after task 2's sweep, no edits made)
FIREWALL: GREEN (26/26)
EXIT:0

$ sh .githooks/pre-commit && echo EXIT:0
(report-conformance self-test's own mutated-fixture DRIFT line, expected internal noise)
report-conformance: SELF-TEST PASS — 102 controls run
report-conformance: PASS — no drift
gen-gate-docs: SELF-TEST PASS — 74 controls run
harvested 22/22 expected script-backed entries (22 total)
EXIT:0

$ git diff --name-only HEAD -- docs/gates/CONF-SURFACE.md
(empty — CR-01 fence holds)

$ diff $SCRATCH/cr02-base.txt $SCRATCH/cr02-working.txt ; echo EXIT:$?
EXIT:0   (empty diff — CR-02 fence holds, 37 lines both sides)

$ diff $SCRATCH/cr03-base.txt $SCRATCH/cr03-working.txt ; echo EXIT:$?
EXIT:0   (empty diff — CR-03 fence holds, 42 lines both sides)

$ git status --porcelain | /usr/bin/grep -c . | /usr/bin/grep -qx 0 && python3 scripts/check-registration.py --self-test && python3 scripts/_gate_registry.py --self-test && bash scripts/check-firewall-battery.sh && echo TASK3_VERIFY:PASS
TASK3_VERIFY:PASS

$ git status --porcelain
(empty, both before task 1 and after task 3)
```

## Deviations from Plan

None — plan executed exactly as written. No auto-fixes, no architectural questions, no
checkpoints. One methodological correction was made mid-task-1/3 and is disclosed rather than
silently absorbed: an early attempt to read `check-registration.py`'s live exit code through
`| tail -N; echo $?` captured `tail`'s exit status, not Python's, and was re-run capturing the
script's own exit code directly (`python3 ... > file 2>&1; echo $?`) before any verdict was
recorded in this Summary — no incorrect CAUGHT/PASS verdict was ever written down.

## Known Stubs

None. This plan reads scripts and Markdown surfaces and performs disposable scratch-copy
mutations; no UI, no mock data path, no product code touched.

## Threat Flags

None. Per the plan's own threat model (T-23-06, T-23-07, T-23-11, all `mitigate`): T-23-06 was
proven to fire by name on three mutation shapes (task 3); T-23-07 was discharged by task 1's
counted-composition derivation and task 2's surface sweep finding zero disagreement; T-23-11 was
discharged by the three fence checks (CR-01 untouched, CR-02 and CR-03 both empty-diff
section-scoped). No new network, auth, or trust-boundary surface introduced.

## Next Steps

- Plan 23-05: REL-04 — the `[9.0.0]` CHANGELOG entry closing SHIP-05 by name, the CR-01/CR-02/CR-03
  disclosures required by D-14 and ROADMAP success criterion 6 (citable paths already staged in
  `23-CONTEXT.md` D-14's table), and the final `docs/conformance-baseline.md` post-milestone
  reading. Plan 23-05 should read this Summary's battery tally (26) rather than re-deriving it
  from prose, per this plan's own `<output>` instruction.
- **Carried-forward finding for 23-05 to adjudicate, not resolved here:** `docs/gates/CONF-SURFACE.md`
  is **CHANGED** relative to the pre-Phase-23 baseline `40064ee` (diffed in commit `ed73189`,
  plan 23-02) — three derived counts moved
  (`literal_scan_exempt_headline-provenance-delta` 11->13, `literal_scan_hits` 211->213,
  `literal_scan_nonmodule_docstring_hits` 383->398) as a mechanical consequence of plan 23-02's
  headline sweep regenerating that page via `gen-gate-docs.py --write`. No prose changed and no
  fix for CR-01 was written — this plan's own CR-01 fence (`git diff --name-only HEAD -- ...`)
  correctly reports it unmodified **within this plan's own commits** (there are none), but the
  file is not byte-identical to the pre-Phase-23 baseline for the reason stated above. This plan
  does not resolve whether that regeneration is compatible with D-09/D-14's "ships live and
  uncorrected" framing for CR-01 — it is reported here, unresolved, for 23-05 to adjudicate.

## Self-Check: PASSED

- `bash scripts/check-firewall-battery.sh` -> `FIREWALL: GREEN (26/26)` — CONFIRMED (re-run, same result)
- `python3 scripts/_gate_registry.py --self-test` -> exit 0 — CONFIRMED
- `python3 scripts/check-registration.py --self-test` -> exit 0 — CONFIRMED
- `git diff --name-only HEAD -- docs/gates/CONF-SURFACE.md` -> empty — CONFIRMED
- `git status --porcelain` -> empty — CONFIRMED
- No commit hashes to verify — this plan made no commits (all three tasks are read/record or
  scratch-copy-only, per the plan's own `<files>` declarations)
