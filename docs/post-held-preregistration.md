# Post-held-append churn — pre-registered measurement

Registered 2026-10-10, before any run.

## Question

Does the 999.200 body, which is the 999.198 body plus a Type-cell refusal in the held-append call and a
rule to write the derived process blocks only after the last section 4 and 6 edit (D-10), reduce
in-place rewrites of the analysis file after the held append?

## Arm

One arm: the generated `first-principles/` tree at the commit recorded on the line below, exported
with `git archive` outside the repository before any run.

**Arm commit:** (filled in before the first run)

There is no concurrent control arm. The comparator is the 24 assembled runs of the committed 999.198
arm (`tests/audit-first/readings.json`), which this arm does not touch. Arm directory
`tests/post-held-append/`, rule `post-held-v1` selected by its `rule.json`. The run cache is
`$HOME/.cache/fp-post-held/`; the 999.198 cache is not reused.

### Type-cell rule

The shipped refusal sits inside the existing held-append call. It fires on a section 2 draft whose
Type cell names two or more of physical law, current constraint, convention, untested belief, or
contains `/`. It is narrower than D-10's literal non-single-token wording: it does not refuse one type
plus other words, and it does not refuse a cell naming none of the four.

The strict form (Type cell not exactly one of the four) fires on 15 of the 24 replayed 999.198 drafts
(`python3 tests/audit-first/replay_drafts.py --rule strict` prints `STRICT TYPE-CELL FIRES 15 of 24`).
It was rejected because each refusal costs about 2 turns, and a 15-of-24 fire rate puts the median gate
turn ceiling (D-06) at risk. The shipped rule fires on 8 of 24 (`python3
tests/audit-first/replay_drafts.py` prints `TYPE-CELL FIRES 8 of 24`).

The full held-append call, replayed on the 24 drafts, refuses 10 of 24 (`CALL REFUSES 10 of 24`): the
Type-cell rule is the first line shown for 6, the identifier-order (GT-N) check precedes it for 2 of
the 8 Type-cell fires (those two show the GT-N line first), and the GT-N check alone accounts for 4.
The awk was tested only under GNU awk 5.4.1 (`awk`, `gawk`, `gawk --posix`); mawk, nawk, original-awk
and busybox were not available. The rule lives in the held-append call of the agent body.

## Runs

The 14 prompts of `tests/example-rerun-2/prompts.json`, two repeats, 28 runs scheduled. Stage 1 is
repeat 1 of every prompt, stage 2 is repeat 2. Model `claude-sonnet-5`, CLI 2.1.289 (re-checked before
the run), the same `claude -p --plugin-dir` transport and retry policy as the 999.198 arm: at most two
runs at a time, routing misses retried at most twice, usage-limit stubs discarded and re-run. The
denominator is the runs reaching `assemble`.

## Primary

A one-sided permutation test that the mean per-run post-held-append rewrite count (rewrites after the
held append: held-to-gate plus post-gate) in the new arm is lower than in the comparator. Statistic:
comparator mean minus new-arm mean; the pooled values are shuffled 20000 times with a fixed seed of
999200 and p = (count + 1) / (20001); alpha 0.05. The comparator is the 24 assembled runs of
`tests/audit-first/readings.json`, 73 post-held commands in all (58 held-to-gate, 15 post-gate).

## Must-hold secondaries

- The number of assembled runs with six or more rewrites at most the critical value of the exact
  one-sided binomial at p0 = 34/87 (the 999.198 primary, with its critical table).
- Median rewrites among assembled runs at most 2.

## No regression

Assembly rate at least 0.90 of dispatched runs; no leftover sidecar and no missing section; median first
Self-Audit Gate turn at most 28 (D-06; the 999.198 arm's was 26); median total turns among assembled runs
at most 43; no assembled run at the 90-turn cap.

## Decision

`shown effective` only if the primary, both secondaries, every no-regression condition hold and at
least 18 runs assembled. After stage 1, 5 or more assembled runs with six or more rewrites stops the
measurement (`futility-stop`). Fewer than 18 assembled after both stages is `uninformative`. Any other
outcome is `not-shown-effective`, and the 999.200 body is not released.

## Reader definitions

A call the checked append refused (`NOT APPENDED`) is not the held append: under this rule the held
turn is the first held-append call that was not refused (`held_append_ok`). The 999.198 arm's own
`held_append_turn` counts a refused call. For the 999.198 arm the two readings split 23 of 24 runs
identically; they differ in `N.software-systems.r2`, where one rewrite sits between its refused and its
successful append (committed as held-to-gate, pre-held under `held_append_ok`). The comparator keeps its
committed split, 73 post-held commands where the refusal-aware reading gives 72. That one command favours
the new arm slightly. Falsifier: `python3 tests/audit-first/run_audit.py held`.

## Reported, not verdict-bearing

- Mean and median rewrites and post-held rewrites per run, against the 999.198 arm.
- The `.process` share and the target-file split (analysis, process, answer) of the rewrite commands.
- The `NOT APPENDED` fire rate: runs, refusals by message (Type cell, GT-N, missing), turns spent.
- Duplicate-section writes, cost, and the category mix from `tests/audit-first/rewrite_causes.py`.

## Cost

About $95 for 28 runs (28 x $3.38, the 999.198 arm's mean over 24 runs, $81.11 in all); $80 to $110
expected, up to about $140 if two runs reach 90 turns. Stage 1 alone is about $47 and yields about 12 to
14 assembled runs, which is `uninformative` by itself.

## What this cannot establish

One model, one CLI version, print mode, a historical comparator rather than a concurrent one, and no
judgement of analysis quality.

- Sensitivity: an arm whose every per-run post-held count is the comparator's, floor-halved, gives
  p = 0.0712 and does not clear. Only a larger drop clears: an all-zero arm gives p = 0.00005, and a
  noise-sized arm (the largest comparator value removed, one 0 added) gives p = 0.240.
- The 90-turn condition is a tail event. With the 999.198 arm's rate of 1 run in 24, an unchanged body
  passes it about 36% of the time (0.958^24, an estimate from one observation), so passing it is weak
  evidence.
- With 24 runs per arm, a difference in the six-or-more-rewrite count between 999.198 and 999.200 is not
  detectable.
- The removal ceilings from research (Type-cell at most 6 of 40, derived blocks at most 18 of 40 of
  heavy-run commands) are ceilings, not forecasts, and this arm cannot attribute an effect to either
  change separately.

## Constants

Each line below is machine-checked against `tests/audit-first/run_audit.py`.

- Rule: post-held-v1
- Permutations: 20000
- Seed: 999200
- Alpha: 0.05
- Rewrite-heavy threshold: 6
- Secondary median ceiling: 2
- Median gate turn ceiling: 28
- Median turns ceiling: 43
- Turn cap: 90
- Futility threshold: 5
- Minimum assembled: 18

## Falsifiers

- `python3 tests/audit-first/run_audit.py --self-test`
- `python3 tests/audit-first/run_audit.py read --arm-dir tests/post-held-append`

Neither is a gate: each is a measurement tool, registered in no battery, CI job or gate registry.
