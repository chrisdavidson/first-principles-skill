# v8.7 Post-Fix Quality Baseline — Same-Catalog, Post-165

**Generated:** 2026-07-23. **Status:** FROZEN read-only evidence — never regenerated, never
hand-edited to match a later result. This directory is the **post-fix** side of the Phase 166
comparison (D-05): the agent body at post-165 `HEAD` regenerating the same three catalog
problems that produced `tests/quality-baseline-v8.7-regenerated/` (the pre-fix side), plus a
same-day re-judging of that frozen pre-fix baseline's own analyses (the D-02 judge-day
drift-control arm).

**This document records provenance and the raw measured numbers only. It does not compute a
verdict.** The Phase 166 verdict — including the D-03 pre-registered comparison rule, the
Goodhart-signature check, and the noise-floor read — is authored in Plan 03
(`docs/v8.7-post-fix-remeasure.md`). No figure below was a target; they are simply whatever
the eighteen live dispatches produced (honesty-not-score, D-01 global).

## Provenance

| | |
|---|---|
| Command | `python3 scripts/check-quality-harness.py --run --rejudge tests/quality-baseline-v8.7-regenerated/analyses --catalog tests/quality-catalog-v8.7.md --repeat 2 --out /tmp/qh-166-postfix` |
| Launched (UTC) | 2026-07-23T03:17:14Z |
| `claude` CLI version | 2.1.218 (Claude Code) |
| Repo commit at run time (post-165 body under measurement) | `e7bcb65` (full `e7bcb659099e448fcee001a19cbc5b094ca76e41`) |
| Catalog | `tests/quality-catalog-v8.7.md` at commit `0239f61` |
| Arm | Single arm, post-fix (agent body at `HEAD`, after Phase 165's output-contract fix) — not a two-arm A/B, matching the pre-fix regenerated baseline's own shape |
| Problems | Same 3 as the pre-fix baseline, same catalog file, same wording: REST/JSON→gRPC migration (Q-P1), subscription churn / loyalty program (Q-P2), attic insulation vs. window replacement (Q-P3) — the D-01/D-07 strict same-prompt matched pair |
| Runs | 3 problems × 2 runs = **6 generations**, `claude -p` over the approach-② bypass wrapper, no plugin dir on the judge dispatch |
| Judging | 6 fresh judgings (one per post-fix generation) + **6 same-day re-judgings** of the frozen pre-fix analyses (`tests/quality-baseline-v8.7-regenerated/analyses/`) through the same channel and the same session = 12 judge dispatches (D-02) |
| Live spend | **18 invocations** (6 generation + 6 fresh judging + 6 re-judging), one manifest row each, all outcome `completed`, **zero re-dispatches** — `manifest.tsv` |

**D-02 same-day re-judge arm, why it exists here:** the pre-fix baseline's own README
(`tests/quality-baseline-v8.7-regenerated/README.md` §"Reproducibility") measured a +7/108
one-sided drift and one verdict flip when six byte-identical analyses were re-judged on a
different day. Post-fix judging necessarily lands on yet another day, so this run re-judges
the frozen pre-fix analyses (`tests/quality-baseline-v8.7-regenerated/analyses/`) inside the
**same invocation** as the post-fix judging, via the harness's `--rejudge` arm. This gives the
Phase 166 verdict a same-day-anchored pre-fix comparison point alongside the frozen cross-day
number, rather than confounding the fix's effect with judge-day drift.

## Raw measured result

Fresh post-fix scorelines (`scorelines.tsv`, band weights Rigorous=3 / Sound=2 / Hand-wavy=1 /
Absent=0, max 18 per analysis, 108 across six):

| Packet | Source | C1 | C2 | C3 | C4 | C5 | C6 | Judge verdict | Derived verdict | Total /18 |
|---|---|---|---|---|---|---|---|---|---|---|
| P02 | Q-P1-run1 | Rigorous | Sound | Sound | Rigorous | Sound | Rigorous | PASS | PASS | 15 |
| P06 | Q-P1-run2 | Rigorous | Sound | Sound | Sound | Rigorous | Rigorous | PASS | PASS | 15 |
| P01 | Q-P2-run1 | Rigorous | Sound | Rigorous | Rigorous | Sound | Rigorous | PASS | PASS | 16 |
| P03 | Q-P2-run2 | Rigorous | Sound | Rigorous | Rigorous | Sound | Rigorous | PASS | PASS | 16 |
| P04 | Q-P3-run1 | Rigorous | Sound | Rigorous | Rigorous | Sound | Rigorous | PASS | PASS | 16 |
| P05 | Q-P3-run2 | Rigorous | Sound | Rigorous | Rigorous | Sound | Rigorous | PASS | PASS | 16 |

- **Aggregate band total: 94 / 108.** Mean per-analysis: **15.67**.
- **Pass split: 6 PASS / 0 FAIL** (derived verdict agrees with the judge's stated verdict on
  all six — zero D-14 disagreements, zero `UNPARSEABLE` cells).
- **Per-criterion column sums** (of a possible 18 each, six analyses): C1=18, C2=12, C3=16,
  C4=17, C5=13, C6=18 (sums to 94, matching the aggregate).

**Same-day re-judged pre-fix analyses** (`rejudge-scorelines.tsv` — the D-02 drift-control
arm, re-judging `tests/quality-baseline-v8.7-regenerated/analyses/` through this run's own
session, same day as the post-fix judging above):

| Packet | Source | C1 | C2 | C3 | C4 | C5 | C6 | Judge verdict | Derived verdict | Total /18 |
|---|---|---|---|---|---|---|---|---|---|---|
| P03 | Q-P1-run1 | Rigorous | Sound | Rigorous | Sound | Sound | Sound | PASS | PASS | 14 |
| P06 | Q-P1-run2 | Rigorous | Sound | Rigorous | Sound | Rigorous | Sound | PASS | PASS | 15 |
| P01 | Q-P2-run1 | Rigorous | Rigorous | Rigorous | Rigorous | Sound | Rigorous | PASS | PASS | 17 |
| P05 | Q-P2-run2 | Rigorous | Hand-wavy | Rigorous | Rigorous | Sound | Rigorous | PASS | PASS | 15 |
| P02 | Q-P3-run1 | Rigorous | Hand-wavy | Rigorous | Rigorous | Sound | Sound | PASS | PASS | 14 |
| P04 | Q-P3-run2 | Rigorous | Rigorous | Rigorous | Rigorous | Sound | Sound | PASS | PASS | 16 |

- **Aggregate band total: 91 / 108.** Pass split: 6 PASS / 0 FAIL.
- This is the frozen pre-fix analyses scored on this run's own day — a second,
  same-session read of pre-fix quality, distinct from that baseline's own frozen 85/108
  (`tests/quality-baseline-v8.7-regenerated/scorelines.tsv`) and its own cross-day re-judge of
  the original Phase-162 corpus (77/108). Three different scorelines now exist for "the pre-fix
  side"; Plan 03's verdict document is where they get named and reconciled against the D-01/D-01a
  primary-basis rule. This README does not pick among them.

**Defect incidence** (`defect-incidence.tsv`, D-18 mechanical detector, over the six fresh
post-fix analyses):

| Family | Post-fix incidence |
|---|---|
| `untraced_flag` (untraced Conclusion claims) | 6/6 |
| `verdict_flag` (non-conforming Verdict cells) | 5/6 |
| `chain_flag` (malformed Derivation Chains blocks) | 4/6 |

These are the raw per-defect-family counts as measured, reported alongside the band scores per
D-21 — not interpreted here. Whether this differs meaningfully from the pre-fix baseline's own
`untraced_flag` 6/6, `verdict_flag` 5/6, `chain_flag` 6/6 (`tests/quality-baseline-v8.7-regenerated/defect-incidence.tsv`),
and whether any Goodhart signature (defects down while C2/C4/C6 flat) applies, is Plan 03's
question to answer, not this document's.

## Contents

- `analyses/Q-P{1,2,3}-run{1,2}.md` — the six freshly-generated post-fix analyses (one per
  problem, two runs each), extracted via `task_notification.summary` per the D-22 probe
  channel (same extraction contract as `tests/quality-baseline-v8.7-regenerated/`). Each
  contains all six numbered output-contract sections.
- `captures/Q-P{1,2,3}-run{1,2}.jsonl` — the six raw generation stream captures, committed
  unmodified.
- `judgments/P0{1..6}-judge.jsonl` + `P0{1..6}-rationale.md` — the six **fresh** judge
  dispatches' raw responses and free-text rationale (never parsed into a score, captured as
  evidence per D-12).
- `rejudge-judgments/P0{1..6}-judge.jsonl` + `P0{1..6}-rationale.md` — the six **re-judge**
  dispatches' raw responses and rationale, over the frozen pre-fix analyses (D-02). The run
  wrote the fresh and re-judged raw judge responses into two separate directories (both arms
  reuse the `P01`–`P06` packet-ID space, so a single merged directory would have collided).
- `manifest.tsv` — one row per of the eighteen live invocations: kind, source identifier, run
  index, destination path, wall-clock duration, outcome (all `completed`), and re-dispatch
  reason (none — zero re-dispatches occurred).
- `scorelines.tsv` — the fresh post-fix eleven-column scorelines (`packet_id`, `C1`..`C6`,
  `judge_verdict`, `derived_verdict`, `agreement`, `source_id`).
- `rejudge-scorelines.tsv` — the D-02 same-day re-judge scorelines over the frozen pre-fix
  analyses, same eleven columns, `source_id` naming the pre-fix analysis file each row
  re-judged.
- `defect-incidence.tsv` — the D-18 mechanical defect detector's ten-column output over the six
  fresh post-fix analyses (D-21: reported alongside the band scores above, not alone).
- `blinding-key.tsv` — the fresh arm's packet-ID-to-source-analysis mapping, six rows, held in
  the directory root only (never inside or beside a packet).
- `rejudge-blinding-key.tsv` — the re-judge arm's packet-ID-to-pre-fix-source mapping, six rows.
- `run.log` — the one-line completion log the `--run` invocation printed.

## Frozen-evidence discipline

These files are committed as-is. They are **never regenerated** (no live `claude` invocation
reproduces this exact run — it already happened) and **never hand-edited** to change a scored
outcome, a claim, a band, or a number. Any correction to this evidence would be a fresh
eighteen-invocation run with its own provenance record, never a silent edit of this one.
`tests/quality-baseline-v8.7-regenerated/` (the frozen pre-fix baseline the D-02 re-judge arm
read from) and `tests/quality-baseline-v8.7/` (the original Phase-162-frozen corpus) remain
separately frozen and untouched by this plan — confirmed by `git diff --quiet -- tests/quality-baseline-v8.7-regenerated`
and `git diff --quiet -- tests/quality-baseline-v8.7` both staying clean through every commit
in this plan. This directory itself is added to the same battery `FROZEN-EVIDENCE` git-diff
guard once committed, and to `check_baseline_integrity`'s structural self-test coverage
(`scripts/check-quality-harness.py`'s `_selftest_baseline()`), so both prior frozen dirs and
this new one are guarded against silent drift going forward.
