# Audit before writing — pre-registered measurement

Registered 2026-10-10, before any run.

## Question

Does the 999.198 body, which runs its checks before a section is appended and holds sections 2 to
4 until the Assumption Audit has run, reduce in-place rewrites of the analysis file?

## Arm

One arm, N: the generated `first-principles/` tree at the commit recorded on the line below,
exported with `git archive` outside the repository before any run.

**Arm commit:** (filled in before the first run)

There is no concurrent control arm. The control is the pooled 99 current-body transcripts read by
`tests/skip-rate/phase_turns.py` (five captures, 33 to 46 percent of assembled runs with six or
more rewrites in each). This saves about $99. The accepted risk is that time or model drift
between those captures and this one is not controlled.

## Runs

The 14 prompts of `tests/example-rerun-2/prompts.json`, two repeats, 28 runs. Stage 1 is repeat 1
of every prompt, stage 2 is repeat 2. Model `claude-sonnet-5`, CLI 2.1.289, the same
`claude -p --plugin-dir` transport as `tests/skip-rate/`. At most two runs at a time, each in its
own empty working directory. Routing misses are retried at most twice. A run that ends on a
usage-limit stub is discarded and re-run.

## Measure

`phase_turns.is_rewrite`, unedited, counted per run. The denominator is the runs whose transcript
reaches the `assemble` milestone.

## Baseline

87 assembled runs of 99. 34 of 87 had six or more rewrites (39.1 percent). Median rewrites 4.
Median first Self-Audit Gate turn 28. Median total turns among assembled runs 43. No run above 90
turns.

## Decision rule

Exact one-sided binomial at p0 = 34/87, alpha at most 0.05. The primary reading is that the number
of assembled runs with six or more rewrites does not exceed the critical value for the number of
assembled runs:

| assembled | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 |
|-----------|----|----|----|----|----|----|----|----|----|----|----|
| critical  | 3  | 3  | 3  | 4  | 4  | 4  | 5  | 5  | 5  | 5  | 6  |

- **Primary:** runs with six or more rewrites at most the critical value.
- **Secondary:** median rewrites among assembled runs at most 2 (the ROADMAP falsifier).
- **No regression**, all of: assembled runs at least 90 percent of dispatched runs; median first
  Self-Audit Gate turn at most 28; median total turns among assembled runs at most 43, the
  baseline's, so that churn moved into whole-draft re-issues, which `is_rewrite` does not count,
  cannot pass; no assembled run at 90 turns or more; and every assembled run complete, meaning no
  leftover `.s2`, `.s3`, `.s4` or `.draft` sidecar and all six `## 1.` to `## 6.` headings present
  in the delivered analysis, so a run cannot score fewer rewrites by dropping sections.
- **Uninformative:** fewer than 18 assembled runs after both stages.
- **Futility stop:** after stage 1, if 5 or more assembled runs have six or more rewrites, stage 2
  is not run and the verdict is `futility-stop`.

The result is `shown effective` only if the primary, the secondary and every no-regression
condition hold. Any other outcome means the body change is not released: it is restored to the
9.19.4 body and the null result is recorded.

## Reported, not verdict-bearing

- Mean rewrites.
- Rewrites split into before the held append, after it but before the Self-Audit Gate (closure
  Step 0 "add the missing chain" and the adversarial pass can still edit sections 3 and 4, which
  the design permits), and after the gate.
- Duplicate-section writes. A re-issued sidecar is not counted by `is_rewrite`, which is why total
  turns gate and this count does not.
- Leftover sidecars, cost, agent minutes.
- Category mix from `tests/audit-first/rewrite_causes.py` (report-only).

## Cost

Mean $3.53 per run (55 runs, `tests/skip-rate/readings.json`): about $49 for stage 1, $99 for both,
worst case $173.

## What this cannot establish

One model, one CLI version, print mode, a historical control, and no judgement of analysis quality.
The instrument counts splice-style edits only. Two biases, stated plainly:

1. The baseline ran at maxTurns 60. 14 of 87 assembled runs exceeded 60 turns and were censored, so
   their rewrite counts are lower bounds. The arm runs at maxTurns 90. This biases the comparison
   against the new body, since a run allowed more turns can rewrite more.
2. p0 = 34/87 is an estimate from 87 runs (Wilson 95 percent interval 29.5 to 49.6 percent) and is
   treated as exact. The true one-sided alpha of the primary test therefore exceeds the nominal
   0.05.

## Falsifiers

- `python3 tests/audit-first/run_audit.py --self-test` reproduces the baseline and the critical
  table above.
- `python3 tests/audit-first/run_audit.py read` prints the verdict from the committed cells.

Neither script is a gate (each is a measurement tool, not a gate): neither is registered in the battery, CI or the gate registry.
