# Protocol — Does every live report carry a structured summary the checker accepts?

**Id:** `structured-summary-live` · **Registered:** 2026-10-01, before any `claude` call under
this id.

## 1. What this confirms

The handoff's live "Done when" items (`~/Projects/agent-router/integrations/first-principles/handoff/fp-structured-summary.md`), LIVE-01 through LIVE-03, one sentence each:

- **LIVE-01** — in a live rerun of the 14 worked examples, 14 of 14 reports carry exactly one
  structured-summary block that passes `scripts/check-summary-block.py`, including its
  cross-checks against the report's own prose.
- **LIVE-02** — in that rerun, the Self-Audit Gate still clears at least as often as the
  2026-09-29 baseline (14/14).
- **LIVE-03** — median cost per run rises by no more than 10% against that baseline ($2.73).

The block restates the prose, so a block that disagrees with its prose is a defect, whichever
side is wrong (D-03 of the phase's locked decisions).

## 2. Prompts

The 14 `shared/examples/*.md` setups, exactly as agent-router's `run_examples.py` extracts and
assembles them (`extract_setup`, `--entry launcher`) — byte-identical to the 2026-09-29
baseline's own `prompt.txt` files, checked before dispatch by falsifier `p4` and copied under
`tests/structured-summary-live/baseline/prompts/` in this repo.

## 3. Transport

The exact command:

```
python3 ~/Projects/agent-router/integrations/first-principles/run_examples.py --entry launcher --jobs 3 --fp-repo /home/chrisdavidson/Projects/first-principles-skill --out ~/Projects/agent-router/integrations/first-principles/runs/structured-summary-live
```

No `--model` — the baseline used the CLI default, and the init event's own `model` field is
recorded per run so a model other than `claude-opus-5-5` is disclosed beside the cost figure
rather than assumed. The runner passes `--permission-mode bypassPermissions`, user-approved
2026-09-30 solely for comparability with the baseline transport and not widened for this run.
The runner's sha256 is pinned (`tests/structured-summary-live/run.py`'s `RUNNER_SHA256`) and
checked before every dispatch.

The baseline is agent-router's `runs/2026-09-29-examples-latest/`: median cost **$2.7343755**
from raw `cost_usd` floats, total **$39.5900182**, gate cleared **14/14** derived from
`state/trace/*.jsonl` `run_end` records (never `trace.py`'s own stricter `cleared`
re-derivation). Its figures are copied into this repo under
`tests/structured-summary-live/baseline/`.

Per run, the init event's `first-principles` plugin path must equal this repo's own
`first-principles/` tree, and `git rev-parse HEAD` plus the `first-principles/` tree hash are
recorded in `manifest.json` before dispatch. agent-router's own HEAD at plan time was
`d1c0bf96b1ad944836c38cf622b0b4d8c96423b0` (77-01-SUMMARY), with its co-loaded
`agent-router-fp` plugin identical to that reference point — it loads alongside
`first-principles` on every run and is part of this instrument, not a bystander.

## 4. Criteria

Pass requires all four, computed by `tests/structured-summary-live/read.py`:

- **(a) runs** — 14/14 rows `complete` in the merged `raw/summary.json`, on this working tree's
  plugin (every run's `loaded_body` equal to `[str(EXPECTED_PLUGIN)]`). Command:
  `python3 tests/structured-summary-live/read.py verdict --leg runs`.
- **(b) blocks** — 14/14 reports carry exactly one structured-summary block, and
  `python3 scripts/check-summary-block.py --json <report>` (the unchanged checker, default live
  mode — never `--exemplar`, never `--schema`) exits 0 on each. The report is the longest
  `raw/<name>/analysis-*.md` by character count (all candidate names recorded); a run with zero
  analysis file is a shortfall under D-08 (§5). Command:
  `python3 tests/structured-summary-live/read.py verdict --leg blocks`.
- **(c) gate** — cleared in 14/14, counted only when the block's `gate.cleared` is `true`, the
  report's last `**Gate result:**` line reads `cleared`, and the checker reported none of
  `SB-GATE-CLEARED`, `SB-GATE-RESULT`, `SB-GATE-PASSES`, `SB-GATE-BANDS`, `SB-INVARIANT`,
  `SB-REENTRY`. agent-router's `trace.py` `cleared` field (no `Hand-wavy` band at all — stricter
  than the rubric's one-`Hand-wavy` cap) is shown in the reading as an informational column,
  never as the measure. Command:
  `python3 tests/structured-summary-live/read.py verdict --leg gate`.
- **(d) cost** — median of raw `cost_usd` floats <= **$3.00** (the $2.73 baseline plus 10%; the
  exact +10% of the raw baseline median is $3.0078, and the stricter $3.00 is used instead).
  Command: `python3 tests/structured-summary-live/read.py verdict --leg cost`.

## 5. Pass rule, void rules, shortfalls

**Pass** = (a)–(d) all hold.

A usage/spend-limit stub (the corrected `is_limit_stub`, `scripts/check-trackb-comparative.py`,
fixed 2026-09-30) is not a counted attempt: stop, report paused, resume later — no sleep loop.
Only examples with ZERO analysis file are relaunched (`--only`), **at most 3** counted attempts
per example; an example that produced a report is final, whatever it says — it is never re-run
for a better reading.

A loaded body other than this tree's plugin, or a plugin/checker/runner identity change between
invocations, voids the run: it is reported, and any re-run is a new id.

A shortfall is reported per run with what the block got wrong and which side needs the change —
template, example, or checker — and the checker is never loosened to pass it. Falsifier:

```
git diff ab23ef45be849f9d4e66b73fcb8d37072a5efe87..HEAD -- scripts/check-summary-block.py
```

`PHASE75_CLOSE = ab23ef45be849f9d4e66b73fcb8d37072a5efe87` — the orchestrator-decided close point
recorded in 77-01-SUMMARY.md (HEAD at that plan's start), chosen over the plan's own raw
`git log --grep` hit `d604b09c` because three further Phase 75 gap-closure commits landed after
that hit and before this plan, each found by Phase 76's own preflight/execution/review loop and
each disclosed here rather than smoothed over:

| Commit | Effect on the checker |
|---|---|
| `2d9a776e` | **Relaxes** — widens accepted Type-cell forms to the taxonomy's locked em-dash subtype. Fixes a false failure on a correct block; accepts no wrong value. |
| `acc37477` | **Relaxes** — widens to a nested-paren subtype form sanctioned by `assumption-taxonomy.md`. Same class: fixes a false failure, accepts no wrong value. |
| `ab23ef45` | **Tightens** — keeps a compound cell's first type (with its em-dash subtype) whole instead of splitting it, narrowing what is accepted and correcting a prior over-wide read. |

All three commits are *inside* the `PHASE75_CLOSE` frame, not after it, so the falsifier's
window starts after the real stabilization point: no commit has touched
`scripts/check-summary-block.py` since `PHASE75_CLOSE`.

## 6. Self-application

Per D-12: the 2026-09-29 baseline's `self-application` example read its own worked example
(answer-key contamination). Now that the `self-application` worked example itself carries a
structured-summary block (Phase 76), a repeat read hands the run a ready-made block rather than
one it had to construct unaided. Its row is reported separately in the reading and flagged `†`
if it reads the example again — it still counts in the literal 14 for every criterion in §4.

## 7. What one run of 14 shows, and what it does not

One sample per example, on one model: 14/14 shows the format holding on these particular runs,
not a rate. A 13/14 result is a finding reported, not re-rolled
(`docs/v8.7-constraint-teardown.md` §2 item 3 governs K-of-N readings generally, and this run is
N=1 per example — a single pass/fail confirmation, not a noise-floor measurement). Block-vs-parser
disagreements — `tests/structured-summary-live/read.py crossread` against agent-router's
`trace.py` — are listed per example with the field, the block's value, and the parser's value;
which side was wrong is established by reading the prose, not assumed from either reader.

## 8. Pre-run amendments

Empty at registration. Any change made before the first registered dispatch under this id is
appended here with its date and reason.
