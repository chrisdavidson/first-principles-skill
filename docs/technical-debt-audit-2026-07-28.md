# Technical Debt Audit — 2026-07-28

Quick task `260728-pa2`. Determines — with measurement, not inference — what technical debt in
this repository should be removed. "Determine" is the operative verb: the primary deliverable is
an evidence-backed recommendation per candidate. Removals are executed only where deadness is
*proven* and the removal is not a judgement call; everything else is written up for the user to
decide.

> **Disposition addendum — 2026-07-28, same day.** The user reviewed the recommendations below
> and selected a subset to act on. What was executed, and the two selections that further
> measurement *refuted*, are recorded in [Disposition](#disposition) at the end of this document.
> Where the disposition contradicts a verdict in the table below, **the disposition is
> authoritative** — the table rows are left as originally written rather than edited after the
> fact, so the correction stays visible.

## Method

**Open-trace liveness oracle.** A throwaway Python tool under the local scratchpad directory
installs a `sys.addaudithook` on the `open` / `io.open` **and** `open_code` events (the separate
audit event CPython's import machinery and script-execution loader use to read `.py` source — a
hook on `open` alone misses every imported module, because a fresh `.pyc` bytecode cache means the
interpreter never re-reads the `.py` source at all; empirically confirmed here: the first hook
version saw 0 `tests/*.py` source hits against 12 `tests/__pycache__/*.pyc` hits from the exact
same run). The hook is loaded via a `sitecustomize.py` on `PYTHONPATH`, which auto-runs at every
interpreter start including nested `python3` subprocesses that inherit the environment — this is
the practical, transitive-tracing equivalent of the `PYTHONSTARTUP`-style wrapping the plan calls
for.

The tool runs every `python3`-based command in `scripts/check-firewall-battery.sh` (the 14 gates
routed through the `gate()` helper, minus the two non-Python subprocess gates VAL-01 `claude
plugin validate` and VAL-02 `markdownlint-cli2`, which are external binaries this technique cannot
trace — documented as a stated method limitation below) plus a full `python3 -m pytest tests/ -q`
run. Each run's opened-path set is appended (union) into a single file per the plan's instruction.
`__pycache__/<mod>.cpython-*.pyc` hits are then mechanically mapped back to their source
`<dir>/<mod>.py`, on the same cache-elision reasoning, and folded into the LIVE SET. The union of
both runs, normalized, is the **LIVE SET**: every tracked path under `tests/`, `scripts/`, and
`docs/` that is absent from it is a *candidate*, not a conclusion.

**Decision rule** (from PLAN.md `<decision_rule>`, applied mechanically): a candidate may be
**REMOVE-EXECUTED** only if all four hold — (1) zero inbound references anywhere in the tracked
tree; (2) not opened by the battery or by pytest per the open-trace above; (3) no collateral edit
needed in 2+ other tracked files to keep the tree valid after removal; (4) not in the plan's
protected set (frozen `RR-*` sentinel excerpts, `FROZEN-EVIDENCE`-diffed paths, TRACE-03
existence-checked baselines, `docs/adoption-telemetry.csv`, `scratchpad/`, `.planning/`,
`docs/history/`, git history itself). Anything failing 1–4 is **RECOMMEND-REMOVE** (with measured
impact) or **KEEP** (with the reason it earns its place).

**LIVE SET size vs. M-3.** M-3 (planner's earlier trace, `open`-only, battery-only, no `open_code`)
reported 58 files / 316KB under `tests/`. This tool's battery-only run (same `open`-only event, no
`open_code`, pyc-mapped, for apples-to-apples comparison) measured **100 files / 486.0KB** under
`tests/` — materially higher. Adding `open_code` did not change the total further in this run
(battery-opens stayed at 100/486.0KB with or without the `open_code` hook active — the extra event
only mattered for `scripts/*.py` source and `__pycache__`-mapped modules, not for the additional
`tests/` baseline `.md` files the two runs disagree on). The union with the full `pytest tests/ -q`
collection (which imports and executes all 137 tests, not just the battery's narrower self-test
subset) brings the final `tests/`-scope LIVE SET to **125 files / 701.8KB**. Per M-9/honesty
requirements, this discrepancy is reported rather than silently adopted: the difference is not
reconciled to a specific cause beyond the plausible ones named above (event coverage, exact
self-test command set, and the pytest-union step this plan explicitly requires but M-3 did not
include), and no removal in this document relies on the smaller M-3 figure — every verdict below
uses this run's own, larger, more inclusive LIVE SET, which is the conservative direction (it
marks *more* files live, not fewer, so it does not risk under-counting liveness).

**A limitation the Task 3 gate caught that the open-trace could not.** The open-trace hooks
`open`/`io.open`/`open_code` — it proves a file is *read*. It does not see `os.path.exists()`,
directory-presence checks, or file counts, which never call `open()`. Task 3 found this the hard
way: deleting four files that were genuinely never *read* by anything removed their containing
directory (git does not track empty directories), and a fixture-integrity self-test that asserts
the directory's *existence* — not its contents — regressed the battery. See the
`baseline-truncated/analyses` evidence entry and Gate Verification below for the full account. This
is why Task 3 re-runs the actual battery and pytest rather than trusting this Method's LIVE SET
alone to authorize a deletion.

## Verdict Table

| Candidate | Inbound refs | LIVE SET member | Verdict | Rationale |
|---|---|---|---|---|
| `scripts/snapshot-traffic.sh` | 0 (M-6) | No | RECOMMEND-REMOVE | Zero references and absent from the LIVE SET, but the adoption-telemetry surface it feeds is tied to the v8.8 user decision that this is a personal/portfolio tool and adoption is no longer graded — "abandoned scaffolding or paused work" is a call the user owns, not a measurement (criterion-4-adjacent judgement ground). See Evidence. |
| `scripts/check-sub-skill-routing.py` | 15 (excl. self) | Yes | RECOMMEND-REMOVE | Deprecated thin shim. LIVE because `tests/test_65_doc_invariants.py` runs it as a subprocess to pin its CLI-default prose, and `_battery_core.py` cites its line numbers as move-from provenance — real usage, not a path literal. 15 referencing files force criterion 3 (2+ collateral edits). |
| `scripts/check-focused-output.py` | 18 (excl. self) | Yes | RECOMMEND-REMOVE | Same shape as above — LIVE via `test_65_doc_invariants.py` (`--dry-run` CLI probe) and `_battery_core.py` provenance comments. 18 referencing files force criterion 3. |
| `scripts/check-routing.py` | 38 (excl. self) | Yes | KEEP | Docs call it "not wired into the CI workflow," but the open-trace shows it is **dynamically imported and executed** by `check-step0-live.py --self-test`'s routing-count drift guard (`importlib.util.spec_from_file_location` + `exec_module`, then calls `parse_catalog()` — STEP0-06, one of the 16 battery gates). Not a standalone gate command, but a real, load-bearing library dependency of one. Fails criterion 2 outright. |
| `scripts/check-body-budget.py` | n/a (battery-internal) | Yes | KEEP | Report-only since TEARDOWN-01, but directly invoked by `check-firewall-battery.sh` on every run (`[INFO] body-size` line, reproduced here: `check-body-budget: REPORT — body is 615 lines`). The teardown record's stated reason for keeping it — "Phase 165 needs the body's growth to stay visible even though nothing will block it" — still holds: the number is still printed on every battery run and nothing since has made growth-visibility moot. |
| `scripts/check-inventory.py` | 2 (M-6) | Yes | KEEP | LIVE — imported by `tests/test_81_inventory.py`, which genuinely runs (unlike the three broken-collection files below) and is part of the 137-pass pytest count. Real dependency, not a stale reference. |
| `scripts/run-live-monitoring.sh` | 2 (M-6) | No | RECOMMEND-REMOVE | Absent from the LIVE SET and referenced only by `docs/live-monitoring-runbook.md` and `scripts/check-traceability.py` (a `deliverable_path` string, not an import) — 2 referencing files trips criterion 3. |
| `tests/step0-baseline-v*.md`, `tests/step0-captures-v*/**` (all versions), `tests/routing-baseline-v3.*.md`, `tests/routing-baseline-v7.11.md`, `tests/routing-battery-baseline-v7.11.md`, `tests/focused-output-baseline-v*.md`, `tests/sub-skill-routing-baseline-v*.md`, `tests/quality-catalog-v8.7.md`, `tests/quality-probe-v8.7/**`, `tests/quality-baseline-v8.7/**`, `tests/quality-baseline-v8.7-regenerated/**`, `tests/quality-baseline-v8.7-postfix/**` | n/a | Mixed (many absent) | KEEP (protected) | Every one of these is a literal path or glob in `check-firewall-battery.sh`'s `FROZEN-EVIDENCE` `git diff --quiet` list. Deleting any single file inside them fails the battery immediately — a mechanically provable dependency, not a judgement call. LIVE SET absence here is expected and does not indicate dead weight: the gate protects the git *object*, not run-time reads. Criterion 4 bars removal regardless of criteria 1–3. |
| `tests/quality-fixtures-v8.7/baseline-truncated/analyses/{condA-P1,condA-P2,condA-P3,condB-P1}.md` | 0 | No (but see Task 3) | RECOMMEND-REMOVE | Looked REMOVE-EXECUTED at Task 2 measurement time (0 refs, absent from the open-trace LIVE SET, no glob protection) but **regressed the battery when actually deleted**: `check-quality-harness.py --self-test`'s "baseline integrity" sub-check asserts the `analyses/` **subdirectory exists** — an existence check the open-trace technique cannot see, because `os.path.exists`/directory-presence checks never call `open()`. Deleting all four files (git does not track empty directories) removed the directory itself. Reverted in Task 3; battery confirmed GREEN again after revert. Downgraded to RECOMMEND-REMOVE — a real removal is possible here, but only paired with whatever edit makes the self-test's existence assumption match (or an explicit placeholder file), which is exactly the kind of collateral change criterion 3 exists to catch and which this audit's open-trace alone did not surface. |
| `tests/quality-fixtures-v8.7/calibration-v8.6-corpus.{md,tsv}` | 5 (excl. self) | No | RECOMMEND-REMOVE | Absent from the LIVE SET but cited by 5 tracked files (`docs/v8.7-quality-baseline-freeze.md`, `scripts/check-quality-harness.py` comment, both v8.13 `detect0*` proof docs, and a sibling README) — criterion 3 fails. |
| `tests/quality-fixtures-v8.7/README.md` | 2 (excl. self) | No | KEEP | Directory README for a fixture set whose other 24/31 members are genuinely LIVE (opened directly by `QUAL-01`'s self-test). READMEs are expected to be absent from an open-trace by nature — documentation is read by humans, not gates. Not debt. |
| `tests/quality-baseline-v8.10-oos/**` (10 files), `tests/defrobust-v8.11/**` (5 files) | many (10 and 3 docs respectively) | No | KEEP | Both are genuinely frozen milestone evidence (v8.10 CORRECTGATE-01 out-of-sample corpus; v8.11 DEFROBUST-01 mutually-blind captures), cited across 10 and 3 tracked docs respectively — criterion 3 alone would force RECOMMEND-REMOVE, but the underlying content is load-bearing history, not stale scaffolding. **Finding, not a removal candidate:** neither directory is covered by the `FROZEN-EVIDENCE` glob list, unlike their same-kind siblings (`tests/quality-baseline-v8.7*`, `tests/quality-probe-v8.7`) — a real gate-coverage gap the user may want to close by extending the glob, not something this audit fixes. |
| `tests/routing-baseline-v7.13.md`, `tests/routing-battery-baseline-v8.5.md` | 3 and 1 (excl. self) | No | RECOMMEND-REMOVE | Same kind of artifact as `tests/routing-baseline-v7.11.md` and `tests/routing-battery-baseline-v4.3.md` (both `FROZEN-EVIDENCE`-protected) but **not** included in that glob — an inconsistency in the gate's own coverage, named here rather than silently exploited. Cited in historical prose only (`docs/v7.13-live-remeasure-verdict.md`, `docs/v8.0-final-closure.md`, `docs/requirements-traceability.md`, `docs/v8.5-live-remeasure-verdict.md`); criterion 3 (3 and 1 referencing docs) plus the project's own no-rewrite-history discipline argue for a recommendation, not an execution. |
| `tests/detect01-red-run-v8.13.md`, `tests/detect02-reversal-proof-v8.13.md`, `tests/detect05-blast-radius-sweep-v8.13.md`, `tests/detect06-injection-proof-v8.13.md` | 0–3 (mostly cross-referencing each other) | No | KEEP | Absent from the open-trace by design — these are v8.13's own fault-injection proof record (days old, the milestone's primary evidentiary artifact for the DETECT-01…06 defect-check corrections), read by humans and cited across the milestone's docs/tests, not executed by any gate. Same category as the frozen quality baselines: narrative/evidentiary documents are supposed to be dead to an open-trace. Not debt. |
| `52-02-SUMMARY.md` (repo root) | 0 (M-6) | No | RECOMMEND-REMOVE | A Phase-52 (v3.12, 2026-05-30) GSD execution summary misfiled at the repository root instead of `.planning/`. `.planning/phases/52-*` no longer exists (archived by prior milestone cleanups) and no other copy was found anywhere in the tracked tree — this is the **only surviving copy** of that historical record. Per the plan's own branching, that drops it to RECOMMEND-REMOVE rather than REMOVE-EXECUTED even at 0 references: destroying the only copy of history is a judgement call, not a measurement. |
| `main.py` (root builder) + `templates/agent.md.tmpl` + `templates/skill.md.tmpl` | 13 (main.py, excl. self); templates referenced only by main.py | No | RECOMMEND-REMOVE | v4.0-era interactive skill/agent scaffolder. Absent from the LIVE SET — and the reason is itself the headline finding: `tests/test_59_02_task1.py`, `tests/test_60_01_check_agent_candidate.py`, and `tests/test_64_01_install.py` exist specifically to test `main.py` (they `importlib`-import it and exercise its functions) but none of their internal functions are named `test_*` (they're `check_*`, run only via each file's own `if __name__ == "__main__"` block) — so `pytest tests/ -q` **collects zero items from all three**, verified live: `pytest tests/test_59_02_task1.py tests/test_60_01_check_agent_candidate.py tests/test_64_01_install.py -v` → `collected 0 items`. `main.py` is therefore genuinely untested by the pytest boundary despite three files that look like its regression suite. 13 referencing files (docs, `docs/data/matrix.json`, `README.md`, `scripts/check-traceability.py`, and the three inert test files) trip criterion 3 regardless. |
| `dev/check-links.sh` | 0 | No | REMOVE-EXECUTED | Standalone v3.0-era link checker hardcoded to `SKILL_DIR="./first-principles-thinking"` — the pre-plugin-split monolith directory name, which **does not exist in this repository** (`ls first-principles-thinking` → No such file or directory). The script would fail immediately (`cd "$SKILL_DIR" \|\| exit 1`) if ever invoked. Zero inbound references, absent from the LIVE SET, zero collateral edits, not in the protected set. All four criteria pass. See Gate Verification. |
| Generated plugin tree (`first-principles/**`) | n/a | n/a | KEEP / no findings | `python3 scripts/sync-content.py --check` is clean (DUAL-04, re-confirmed at Task 2 execute time). Every generated `.md` in the tree carries its `<!-- DO NOT EDIT — generated from ... -->` (or equivalent) marker, checked case-insensitively; the one exception, `first-principles/README.md`, is deliberately hand-maintained (not in the sync tool's generated-target list per `CLAUDE.md`'s own architecture diagram). No orphaned or duplicated files found. |
| `.planning/config.json`'s `quick_branch_template` unknown-key warning | n/a | n/a | Not applicable | `.planning/` is git-ignored end to end (confirmed: `git check-ignore -v .planning/config.json` → matches `.planning/` in `.gitignore`). This is local tooling ergonomics on the user's own machine, not repository debt — no tracked file to act on. |

## Evidence

### `scripts/snapshot-traffic.sh`

- **Inbound references:** 0 tracked files reference it (`git grep -l -F` against the full tracked
  tree, excluding the file itself and `scratchpad/` — reproduced at execute time, matches M-6).
- **LIVE SET membership:** absent. Not opened by any battery gate or by the `tests/` pytest run.
- **What it is:** a traffic-snapshot shell script feeding `docs/adoption-telemetry.csv`. That CSV
  is itself modified-and-uncommitted since before this milestone (protected — never touched by
  this plan) and its consumption pattern was explicitly re-scoped at v8.8: "this is a
  personal/portfolio tool, NOT distribution — adoption no longer graded" (`docs/README.md`,
  `.planning/STATE.md`).
- **What breaks if removed:** nothing measurable — no gate, test, or doc opens it, and the
  adoption-telemetry consumer chain it feeds is already off the grading path.
- **What is lost:** the only mechanism that has ever populated `docs/adoption-telemetry.csv`. If
  the user still wants periodic traffic snapshots for their own reference (distinct from
  "adoption is graded"), removing the script forecloses that without a replacement.
- **Verdict:** RECOMMEND-REMOVE, not RECOMMEND-EXECUTED, because "is this abandoned scaffolding or
  intentionally-paused personal tooling" is exactly the kind of call the decision rule's criterion
  4 reserves for the user, not an open-trace or reference-count measurement.

### `scripts/check-sub-skill-routing.py` / `scripts/check-focused-output.py`

- **Inbound references:** 15 and 18 respectively (excluding self), spanning `CHANGELOG.md`,
  `CLAUDE.md`, four `docs/` files, `scripts/_battery_core.py`, `scripts/check-routing-battery.py`,
  and several `tests/*-baseline*.md`/`*-catalog.md` files.
- **LIVE SET membership:** both LIVE, but not for the reason their prose citations would suggest.
  `tests/test_65_doc_invariants.py` (part of the 137-test pytest suite) runs
  `check-focused-output.py --dry-run` as a live subprocess to assert its output still says
  "4 P-prompts, 1 N-prompts", and asserts both scripts' `--help` text still reports the documented
  `--p-threshold`/`--n-threshold` defaults. `scripts/_battery_core.py` additionally carries
  `# verbatim-move-from: scripts/check-sub-skill-routing.py lines N-M` provenance comments for code
  that was ported into the merged battery. Both are real, mechanism-level dependencies, not
  incidental documentation.
- **What breaks if removed:** `test_65_doc_invariants.py`'s CLI-default and delegation-prose
  assertions would need rewriting or deleting (a real, non-trivial pytest-suite edit); `CLAUDE.md`,
  `CHANGELOG.md`, and four `docs/` files reference them by name as the documented deprecated-shim
  delegation path; `_battery_core.py`'s provenance comments would become dangling citations.
- **What it would cost to remove:** at minimum, a coordinated edit across `test_65_doc_invariants.py`
  plus every doc that documents the deprecation-shim pattern — well over the criterion-3 threshold.
- **What is lost:** the documented backward-compatible entry points for callers who still invoke the
  two old script names directly instead of `check-routing-battery.py`.

### `scripts/run-live-monitoring.sh`

- **Inbound references:** 2 (`docs/live-monitoring-runbook.md`, `scripts/check-traceability.py`'s
  `deliverable_path` string — a path literal, not an open, consistent with honesty rule #2).
- **LIVE SET membership:** absent — not opened by the battery or by pytest.
- **What breaks if removed:** `docs/live-monitoring-runbook.md`'s runbook instructions would
  reference a missing script; `check-traceability.py`'s traceability row would point at a deleted
  deliverable.
- **What it would cost to remove:** two file edits (the runbook and the traceability entry) —
  right at the criterion-3 threshold, which the decision rule treats as disqualifying.
- **What is lost:** the only scripted entry point the runbook currently documents for live
  monitoring runs; the runbook's manual-command instructions would need to be inlined or rewritten.

### `tests/quality-fixtures-v8.7/baseline-truncated/analyses/{condA-P1,condA-P2,condA-P3,condB-P1}.md`

- **Inbound references:** 0 — no tracked file outside the four files themselves mentions
  `baseline-truncated/analyses` in any form.
- **LIVE SET membership:** absent. The sibling `baseline-truncated/blinding-key.tsv` and
  `baseline-truncated/scorelines.tsv` in the same directory ARE opened directly by
  `check-quality-harness.py --self-test` (QUAL-01) — confirming the fixture directory as a whole is
  live infrastructure, while these four specific `analyses/*.md` files inside it are not.
- **What breaks if removed:** nothing measurable — QUAL-01's self-test reads the `.tsv` scorelines
  directly; it does not read these four markdown analysis bodies.
- **What is lost:** four historical analysis documents from the truncated-baseline fixture case.
  Given the sibling `.tsv` files are what the self-test actually asserts against, these look like
  leftover source material for the fixture's construction rather than a live input.

### `tests/quality-fixtures-v8.7/baseline-truncated/analyses/{condA-P1,condA-P2,condA-P3,condB-P1}.md` (attempted, reverted)

- **Inbound references:** 0, re-confirmed immediately before deletion in Task 3.
- **LIVE SET membership:** absent, re-confirmed with a freshly re-run open-trace immediately before
  deletion in Task 3 (not relying on the Task 2 reading, per the plan's explicit instruction).
- **What actually happened:** deleted via `git rm` in Task 3. `bash scripts/check-firewall-battery.sh`
  regressed: `FIREWALL: RED (1 gate(s) failed; 15/16 passed)`, with `[FAIL] QUAL-01
  check-quality-harness.py --self-test`. Running the self-test directly isolated the cause exactly:
  `self-test FAIL: baseline integrity on the truncated fixture reported findings, but none names the
  count mismatch: ['.../tests/quality-fixtures-v8.7/baseline-truncated: analyses/ subdirectory does
  not exist']`. The four files were the only members of `analyses/`; deleting all of them removed the
  directory (git does not track empty directories), and a self-test sub-check that asserts the
  directory's *existence* — not its contents being read — failed.
- **Root cause of the audit miss:** the open-trace technique hooks `open`/`open_code`, which fires
  for file reads and module imports. It does not fire for `os.path.exists()`, `Path.is_dir()`, or any
  other presence/count check that never calls `open()`. This is precisely the failure mode the plan's
  honesty requirement #2 warned about ("a file can be absent from an open-trace and still be
  load-bearing... an existence check is a real dependency") — this audit checked for that pattern
  deliberately for directories named in `check-traceability.py`'s deliverable-path list, but did not
  extend the same suspicion to `check-quality-harness.py`'s own internal fixture-integrity assertions
  before executing the deletion. Caught here because Task 3 re-runs the actual battery rather than
  trusting the open-trace alone — which is exactly why that gate exists.
- **Recovery:** reverted with `git checkout HEAD -- <path>` for each of the four files; re-ran the
  battery with only `dev/check-links.sh` removed and confirmed `FIREWALL: GREEN (16/16)` and
  `137 passed` — the baseline is restored. See Gate Verification for both full transcripts.
- **Verdict, corrected:** RECOMMEND-REMOVE, not REMOVE-EXECUTED. See the verdict table for the
  reasoning on what a real removal here would additionally require.

### `tests/quality-fixtures-v8.7/calibration-v8.6-corpus.{md,tsv}`

- **Inbound references:** 5 (`docs/v8.7-quality-baseline-freeze.md`, `scripts/check-quality-harness.py`
  comment, `tests/detect02-reversal-proof-v8.13.md`, `tests/detect05-blast-radius-sweep-v8.13.md`,
  `tests/quality-baseline-v8.7-regenerated/README.md`).
- **LIVE SET membership:** absent.
- **What breaks if removed:** five tracked files cite it by name as calibration provenance for the
  v8.6 quality-A/B corpus; removal would leave five dangling citations.
- **What is lost:** the calibration corpus record cited as the basis for the harness's v8.6 blind
  A/B measurement — a provenance document, not executable infrastructure.

### `tests/routing-baseline-v7.13.md` / `tests/routing-battery-baseline-v8.5.md`

- **Inbound references:** 3 (`docs/requirements-traceability.md`, `docs/v7.13-live-remeasure-verdict.md`,
  `docs/v8.0-final-closure.md`) and 1 (`docs/v8.5-live-remeasure-verdict.md`) respectively.
- **LIVE SET membership:** both absent.
- **What breaks if removed:** three and one historical-verdict documents respectively would cite a
  now-missing file.
- **What is lost:** frozen routing-baseline snapshots from two prior milestones' live re-measures —
  the same category of evidence as `tests/routing-baseline-v7.11.md` and
  `tests/routing-battery-baseline-v4.3.md`, which ARE protected by `FROZEN-EVIDENCE`. This asymmetry
  is a gate-coverage gap: either these two should be added to the glob (treat them as equally
  protected) or the glob's current scope was a deliberate narrowing this audit cannot see the reason
  for. Recorded for the user to decide; not resolved here.

### `52-02-SUMMARY.md`

- **Inbound references:** 0 (M-6, reproduced at execute time).
- **LIVE SET membership:** absent.
- **What breaks if removed:** nothing measurable.
- **What is lost:** the only surviving copy of the Phase 52 Plan 02 execution summary (v3.12,
  2026-05-30, sync-content.py `SKILLS` tuple extension) — `.planning/phases/52-*` no longer exists on
  disk. Whether a misfiled historical record at the repo root should be deleted outright or relocated
  into `.planning/` (which is itself gitignored, so relocating it would also remove it from the public
  repository) is the user's call.

### `main.py` + `templates/agent.md.tmpl` + `templates/skill.md.tmpl`

- **Inbound references:** `main.py` — 13, excluding self (`README.md`, `docs/data/matrix.json`,
  `docs/requirements-matrix.md`, `docs/v8.1-grok-review-assessment.md`,
  `docs/v8.2-grok-reassessment.md`, `scripts/check-traceability.py`, four historical
  `tests/step0-captures-*/S-N03-run*.txt` capture excerpts, and the three test files below). The two
  `.tmpl` files are referenced only by `main.py`'s own `TEMPLATES_DIR` constant — no independent
  inbound references, so they are bundled with `main.py` rather than given separate rows.
- **LIVE SET membership:** absent for all three — and the reason is the headline finding of this
  surface. `tests/test_59_02_task1.py`, `tests/test_60_01_check_agent_candidate.py`, and
  `tests/test_64_01_install.py` were plainly written to test `main.py` — they `importlib`-import it,
  call functions like `check_pep723_header()`, `check_parses()`,
  `check_description_budget_behavior()` — but every one of those functions is named `check_*`, not
  `test_*`, and each file only runs them through its own `if __name__ == "__main__": main()` block.
  `pytest`'s default `python_files = test_*.py` glob still collects the *files* (hence they show as
  imported in a raw LIVE SET pass before this distinction is made), but finds zero `test_*`-prefixed
  callables inside them. Reproduced live: `python3 -m pytest tests/test_59_02_task1.py
  tests/test_60_01_check_agent_candidate.py tests/test_64_01_install.py -v` → `collecting ...
  collected 0 items` / `no tests ran in 0.03s`. None of the three contributes to the 137-pass count.
- **What breaks if removed:** nothing in the offline battery or the pytest boundary — confirmed by
  the same "collected 0 items" result above. 13 tracked files would carry dangling references, and
  the three inert test files would need to be deleted or rewritten alongside it (their `check_*`
  functions have nothing left to test).
- **What is lost:** the only scaffolding tool in the repo for interactively generating a new
  `SKILL.md`/agent `.md` candidate from a template — described in its own docstring as the thing
  `docs/GETTING-STARTED.md`-adjacent contributor workflows would use to add a fourteenth companion
  skill. Removing it forecloses that workflow without a documented replacement.
- **Recommendation, not execution, because:** whether a genuinely untested, un-exercised v4.0-era
  builder tool is still wanted (with its test coverage repaired) or should be retired outright is a
  product decision, not something zero references vs. thirteen references settles by itself — and 13
  referencing files trip criterion 3 regardless.

### `dev/check-links.sh`

- **Inbound references:** 0 — no tracked file mentions `check-links.sh` anywhere (`git grep -n
  "check-links\.sh"` returns nothing beyond the file itself).
- **LIVE SET membership:** absent — not opened by the battery or by pytest.
- **What it is:** a standalone bash link-checker, hardcoded to `SKILL_DIR="./first-principles-thinking"`
  — the pre-plugin-split monolith directory name from before the v3.0 rearchitecture. That directory
  **does not exist** in this repository (`ls first-principles-thinking` → No such file or directory);
  the script's own `cd "$SKILL_DIR" || exit 1` would fail on line 1 of actual execution if anyone ran
  it today. `scripts/check-links.py` is the real, actively-gated (VAL-03) successor.
- **What breaks if removed:** nothing — it is already broken and unreferenced.
- **What is lost:** nothing usable in its current state.
- **Verdict:** REMOVE-EXECUTED — passes all four criteria cleanly and is additionally the clearest
  case in this audit (an artifact that could not even run against the current tree).

## Findings (non-candidate)

- **M-7 — dangling public-repository link, and a disclosure asymmetry.** `docs/README.md:147` links
  `history/` to `docs/history/`, which was made untracked and gitignored by the two git-history
  rewrites recorded under M-2 (already pushed, already closed, not reopened by this audit). The link
  **resolves on this disk** (VAL-03 is green, `docs/history/` still exists as an untracked local
  directory) but is a 404 for anyone reading the pushed public repository, since `docs/history/` was
  never committed after the rewrite. Widening the search during Task 2 found that
  `docs/requirements-traceability.md` already discloses this correctly in three places — calling
  `docs/history/` "**local-only, git-ignored**" and "not present in a fresh clone" — while
  `docs/README.md`'s own index entry for the same path carries no such caveat and presents it as an
  ordinary navigable link. The inconsistency, not just the 404, is the finding: one document in the
  tree already states the true status; the most-visible entry point does not. Recorded here, not
  fixed — fixing it is a judgement call (re-track the 67 snapshots publicly, edit the link/prose to
  stop pointing at a now-private local-only directory, or bring `docs/README.md`'s caveat in line
  with `docs/requirements-traceability.md`'s) that belongs to the user, per the plan's explicit
  instruction not to resolve it in this task.
- **Superseded documents, swept and cleared.** Beyond M-7, no other tracked markdown link points at
  a path M-2 made untracked (`git grep` for `.jsonl` link targets across every tracked `.md` file
  returned zero hits). Every older milestone's `docs/README.md` section already carries forward a
  supersession pointer to the milestone that superseded it (v8.9 supersedes v8.7's flat-6/6 finding,
  v8.10 supersedes v8.9's MEASUREMENT verdict, and so on) — the project's own no-rewrite-history
  discipline is already being followed correctly. **No removal candidates found on this surface** —
  a valid and complete outcome per the plan's own instruction not to manufacture one.
- **Stale config (`quick_branch_template`).** Confirmed local-only: `.planning/config.json` is
  git-ignored end to end. The unknown-key warning it emits on every tooling invocation is a
  local-ergonomics nit on this machine, not repository debt — there is no tracked file to act on.
- **Generated plugin tree.** Swept for orphans (files present under `first-principles/` with no
  corresponding source under `shared/`, which `sync-content.py` would therefore never regenerate).
  None found — `sync-content.py --check` is clean and every generated file carries its marker comment
  except the one file (`first-principles/README.md`) that is deliberately hand-maintained, not
  sync-tool output. **No removal candidates found on this surface.**

## Gate Verification

**Pre-state (Task 1, before any edit in this plan; HEAD `4e1d3c9`):**

```
$ bash scripts/check-firewall-battery.sh
...
FIREWALL: GREEN (16/16)

$ python3 -m pytest tests/ -q
...
137 passed in 1.87s
```

**Attempted removal (Task 3, mid-execution — regression, reverted):** deleting all four
`tests/quality-fixtures-v8.7/baseline-truncated/analyses/*.md` files alongside
`dev/check-links.sh`:

```
$ bash scripts/check-firewall-battery.sh
...
[FAIL] QUAL-01         check-quality-harness.py --self-test
...
FIREWALL: RED (1 gate(s) failed; 15/16 passed)

$ python3 scripts/check-quality-harness.py --self-test
self-test FAIL: baseline integrity on the truncated fixture reported findings, but none names the
count mismatch: ['.../tests/quality-fixtures-v8.7/baseline-truncated: analyses/ subdirectory does
not exist']
self-test: baseline sub-check FAILED
```

The four `analyses/*.md` files were reverted with `git checkout HEAD -- <path>` (one command per
file). They are **not** part of the final commit.

**Post-state (Task 3, final — only `dev/check-links.sh` removed):**

```
$ bash scripts/check-firewall-battery.sh
...
FIREWALL: GREEN (16/16)

$ python3 -m pytest tests/ -q
...
137 passed in 1.43s
```

Both boundaries match the Task 1 pre-state exactly (`GREEN (16/16)`, `137 passed`) with the one
executed removal in place. The regression above is recorded rather than worked around — no
criterion was softened to make it pass; the candidate that caused it was reverted and its verdict
row corrected to RECOMMEND-REMOVE.

**REMOVE-EXECUTED set == deletions in this commit:** `dev/check-links.sh`. One row, one file, one
deletion — verified with `git diff --cached --name-status` before committing (excludes the
telemetry CSV and `scratchpad/`, confirmed below).

## Decisions For the User

Ordered by measured impact — largest first.

1. **`main.py` + `templates/*.tmpl` (the v4.0-era builder) — 13 referencing files, genuinely
   untested.** The three test files that exist specifically to exercise it
   (`tests/test_59_02_task1.py`, `tests/test_60_01_check_agent_candidate.py`,
   `tests/test_64_01_install.py`) collect zero pytest items each (`check_*` functions, not `test_*`)
   — verified live. Decide: repair the test collection and keep the scaffolding tool, or retire the
   whole trio (`main.py`, both `.tmpl` files, and the three now-pointless test files) together.
2. **`scripts/check-sub-skill-routing.py` / `scripts/check-focused-output.py` (deprecated shims,
   15/18 referencing files).** Both are still exercised by `tests/test_65_doc_invariants.py`'s CLI
   probes, not just documentation. Decide: retire the shims and rewrite/delete the corresponding
   `test_65` assertions together, or keep the backward-compatible entry points.
3. **`tests/quality-fixtures-v8.7/baseline-truncated/analyses/*.md` (4 files) — real removal is
   possible, but not as attempted here.** Removing them cleanly requires also satisfying (or
   removing) `check-quality-harness.py`'s existence assertion on the `analyses/` subdirectory — a
   collateral code change this audit did not make. Decide whether that fixture-integrity check
   should be relaxed, or the directory kept with a placeholder.
4. **`tests/routing-baseline-v7.13.md` / `tests/routing-battery-baseline-v8.5.md` vs. the
   `FROZEN-EVIDENCE` gate's own coverage gap.** Same kind of artifact as their protected siblings
   but excluded from the glob. Decide: extend `FROZEN-EVIDENCE`'s glob to cover them (treat as
   equally protected), or accept the current asymmetry and remove them along with editing their 3
   and 1 citing documents respectively.
5. **`tests/quality-baseline-v8.10-oos/` and `tests/defrobust-v8.11/` — same coverage-gap shape,
   opposite direction.** These are unambiguously load-bearing frozen evidence (cited by 10 and 3
   docs respectively) that happen not to be in the `FROZEN-EVIDENCE` glob either. No removal is
   recommended; the decision here is only whether to add them to the glob so a future accidental
   edit is caught mechanically instead of by hand-checking.
6. **`docs/README.md:147`'s `history/` link (M-7) — a disclosure asymmetry, not just a 404.**
   `docs/requirements-traceability.md` already states `docs/history/` is local-only and git-ignored;
   `docs/README.md`'s index entry does not carry that caveat. Decide: re-track the 67 snapshots
   publicly, edit the link/prose to stop pointing at a private local-only directory, or bring the two
   documents' disclosures in line with each other.
7. **`scripts/run-live-monitoring.sh`, `tests/quality-fixtures-v8.7/calibration-v8.6-corpus.{md,tsv}`,
   `52-02-SUMMARY.md`, `scripts/snapshot-traffic.sh`.** Each RECOMMEND-REMOVE with a small (0–5)
   citing-file count; lowest-impact of the set. `52-02-SUMMARY.md` is the only surviving copy of its
   phase's history — confirm no other copy is wanted before deleting.

**Executed in this plan:** `dev/check-links.sh` only — zero references, targets a directory that no
longer exists in this repository, and both boundary checks stayed green after removal.

---

## Disposition

Recorded 2026-07-28, after the user reviewed the recommendations above and selected which to act
on. Commits `8c2c733`, `fff95fd`, `2bb2ca5`.

### Executed

| Action | Evidence |
|---|---|
| Removed `scripts/snapshot-traffic.sh` | 0 inbound references, absent from the live set. Fed the adoption-telemetry surface retired by the v8.8 personal/portfolio-tool decision. |
| Removed `52-02-SUMMARY.md` (repo root) | 0 inbound references. User confirmed the loss of the only surviving copy of that phase record is acceptable. |
| Extended the `FROZEN-EVIDENCE` glob by four paths | `tests/routing-baseline-v7.13.md`, `tests/routing-battery-baseline-v8.5.md`, `tests/quality-baseline-v8.10-oos/`, `tests/defrobust-v8.11/`. Resolves the coverage asymmetry in the **keep** direction: the first two were RECOMMEND-REMOVE candidates *only* because they lacked the protection their siblings had. Non-vacuity proven by fault injection — appending to a file in each of the four leaves the old path list clean (`git diff --quiet` exit 0) and trips the new one. |
| De-linked `docs/README.md`'s `history/` entry | Was a live 404 on the public repository (resolves only on a machine holding the local copies, so VAL-03 never flagged it). Now carries the same "local-only, git-ignored" disclosure `docs/requirements-traceability.md` makes. No tracked file links into `history/` any more. |
| Wired the three builder check-suites into pytest | New `tests/test_builder_check_adapters.py`. pytest count 137 → 157. |

**On the pytest repair specifically.** The obvious fix — renaming `check_*` to `test_*` — would
have been *worse than the gap*. Those 19 functions signal failure by **returning** `False`, and
pytest only warns on a non-`None` return; it does not fail. A rename would therefore have
collected all 19 and reported every one as PASSING regardless of its result: a silent false green
over `main.py`, which is exactly the condition the repair set out to end. The adapter asserts on
the returned bool instead, and leaves each file's standalone `main()` runner working. It carries
its own non-vacuity guard (fails if zero checks are discovered or a suite drops out), and forcing
`check_conflict_abort` to return `False` makes pytest report `1 failed, 19 passed` — reverted.

### Refuted by measurement — NOT executed

Both were selected by the user for removal. Re-measuring before acting showed the audit had
under-described each one. Neither was removed.

**1. `scripts/run-live-monitoring.sh` — not dead; a CI gate asserts it exists.**
The verdict row above calls its `check-traceability.py` reference "a `deliverable_path` string,
not an import". That is wrong. `scripts/check-traceability.py` carries a named sentinel,
**`GEN-02-RUNBOOK`**, whose D-03 dual-artifact check asserts that *both*
`docs/live-monitoring-runbook.md` **and** `scripts/run-live-monitoring.sh` exist — and
`check-traceability.py --self-test` is the **TRACE-03 CI gate**. Removing the wrapper fails
TRACE-03. Worse, the sentinel binds that existence to requirement **GEN-02's `reproducible`
coverage tier**: the comment states in terms that "any future revert of the tier, deletion of the
GEN-02 row, or removal of the runbook/wrapper fails CI". Removing the script would therefore not
be a two-file cleanup — it would mean deleting a named gate assertion and demoting a requirement's
coverage tier, degrading the traceability headline. The runbook it backs is also still marked
`Status: ACTIVE` and documents the live monitoring cadence for GR-03/GR-04.
**Correct verdict: KEEP.** This is the same class of error as item 2 — an existence check is a
real dependency that an open-trace cannot see.

**2. `tests/quality-fixtures-v8.7/baseline-truncated/analyses/*.md` — a deliberate negative
fixture, not dead weight.**
The selected action was to relax `check-quality-harness.py`'s `analyses/` existence assertion so
the four files could be removed. Reading the fixture's purpose first shows why that inverts the
intent: `baseline-truncated/` is the **D-15 item 6 negative fixture**, and QUAL-01's self-test
asserts that `check_baseline_integrity()` *finds* a row-count-versus-file-count mismatch on it.
The four `analyses/*.md` files are the **file-count side of the mismatch the gate is built to
detect**. `tests/quality-fixtures-v8.7/README.md` even records a mutation experiment (row G)
adding a fifth analysis to prove the negative depends on that mismatch and nothing incidental.
They show 0 inbound references and no open-trace hit because they are **counted and stat'd, never
opened** — the same blind spot that made the original removal attempt turn the battery red.
Relaxing the assertion would delete gate coverage while appearing to pay down debt.
**Correct verdict: KEEP (protected).**

### Declined by the user

- `tests/quality-fixtures-v8.7/calibration-v8.6-corpus.{md,tsv}` — left in place.
- The two deprecated shims (`check-sub-skill-routing.py`, `check-focused-output.py`) — kept. They
  are genuinely exercised by `tests/test_65_doc_invariants.py`'s CLI probes.

### Post-disposition state

    FIREWALL: GREEN (16/16)
    157 passed
