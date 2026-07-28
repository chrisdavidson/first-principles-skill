# Technical Debt Audit — 2026-07-28

Quick task `260728-pa2`. Determines — with measurement, not inference — what technical debt in
this repository should be removed. "Determine" is the operative verb: the primary deliverable is
an evidence-backed recommendation per candidate. Removals are executed only where deadness is
*proven* and the removal is not a judgement call; everything else is written up for the user to
decide.

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

## Verdict Table

| Candidate | Inbound refs | LIVE SET member | Verdict | Rationale |
|---|---|---|---|---|
| `scripts/snapshot-traffic.sh` | 0 (M-6) | No | RECOMMEND-REMOVE | Zero references and absent from the LIVE SET, but the adoption-telemetry surface it feeds is tied to the v8.8 user decision that this is a personal/portfolio tool and adoption is no longer graded — "abandoned scaffolding or paused work" is a call the user owns, not a measurement (criterion-4-adjacent judgement ground). See Evidence. |

*(Table continues in Task 2.)*

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

## Findings (non-candidate)

- **M-7 — dangling public-repository link.** `docs/README.md:147` links `history/` to
  `docs/history/`, which was made untracked and gitignored by the two git-history rewrites recorded
  under M-2 (already pushed, already closed, not reopened by this audit). The link **resolves on
  this disk** (VAL-03 is green, `docs/history/` still exists as an untracked local directory) but is
  a 404 for anyone reading the pushed public repository, since `docs/history/` was never committed
  after the rewrite. This is recorded as a finding for the user, not fixed here — fixing it is a
  judgement call (re-track the 67 snapshots publicly, or edit the link/prose to stop pointing at a
  now-private local-only directory) that belongs to the user, per the plan's explicit instruction
  not to resolve it in this task.

## Gate Verification

*(Filled by Task 3.)*

## Decisions For the User

*(Filled by Task 3.)*
