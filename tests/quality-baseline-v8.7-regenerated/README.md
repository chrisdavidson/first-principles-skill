# v8.7 Regenerated Quality Baseline — Pre-Fix, Channel-Matched

**Generated:** 2026-07-22. **Status:** FROZEN read-only evidence — never regenerated, never
hand-edited to match a later result. This directory is the pre-fix side of the Phase 166
post-fix comparison. It was produced end-to-end by `scripts/check-quality-harness.py`'s
`--run`/`--rejudge` composition (Phase 164 Plan 04), spending 18 of this phase's declared 19
live `claude -p` invocations (the 19th is Plan 01's D-22 transport probe,
`tests/quality-probe-v8.7/`).

**Two limitation findings bound what Phase 166 is allowed to claim from this evidence — read
["Reproducibility"](#reproducibility-the-headline-finding) and
["Within-condition noise floor"](#within-condition-noise-floor-d-08) before citing any number
here as a result.**

## Provenance

| | |
|---|---|
| Command | `python3 scripts/check-quality-harness.py --run --rejudge tests/quality-baseline-v8.7/analyses --catalog tests/quality-catalog-v8.7.md --repeat 2 --out /tmp/qh-run` |
| Date | 2026-07-22 |
| `claude` CLI version | 2.1.217 (Claude Code) |
| Repo commit at run time | `348e873` (Plan 04 Task 1 — the `--run`/`--rejudge`/`--dry-run`/`--resume` composition this run exercised) |
| Catalog | `tests/quality-catalog-v8.7.md` at commit `0239f61` |
| Arm | Single arm, pre-fix (agent body at `HEAD`, before Phase 165's output-contract fix) — not a two-arm A/B; Phase 166 is pre-fix vs. post-fix, not 590-vs-612 (D-08) |
| Problems | 3, freshly worded, same topics as the original v8.6 experiment for continuity (D-09): REST/JSON→gRPC migration (Q-P1), subscription churn / loyalty program (Q-P2), attic insulation vs. window replacement (Q-P3) |
| Runs | 3 problems × 2 runs = **6 generations**, `claude -p` over the approach-② bypass wrapper, no plugin dir on the judge dispatch |
| Judging | 6 fresh judgings (one per generation) + **6 re-judgings** of the Phase-162-frozen corpus through the same channel = 12 judge dispatches |
| Live spend | **18 invocations** (6 generation + 6 fresh judging + 6 re-judging), one manifest row each, all outcome `completed`, zero re-dispatches — `manifest.tsv` |

**Why two runs per problem, not one (D-08 noise-floor rationale, in this harness's own
words):** the source experiment (`docs/v8.6-quality-ab-experiment.md`) ran exactly one run per
cell, and its own authors called the exact 35/35 band-total tie between arms "partly luck" —
a single run per condition cannot distinguish a real effect from ordinary run-to-run
variation. This baseline spends its budget on **within-condition repeats** instead of a second
arm, buying a noise floor: if two pre-fix runs of the same problem already differ by up to 3
band points (see below), a same-sized post-fix "improvement" in Phase 166 is not yet
distinguishable from noise.

## Aggregate result

Six per-analysis band totals (weights: Rigorous=3, Sound=2, Hand-wavy=1, Absent=0; max 18 per
analysis, 108 across six):

| Packet | Source | C1 | C2 | C3 | C4 | C5 | C6 | Judge verdict | Derived verdict | Total /18 |
|---|---|---|---|---|---|---|---|---|---|---|
| P03 | Q-P1-run1 | Rigorous | Sound | Rigorous | Sound | Sound | Sound | PASS | PASS | 14 |
| P04 | Q-P1-run2 | Rigorous | Sound | Rigorous | Sound | Sound | Rigorous | PASS | PASS | 15 |
| P02 | Q-P2-run1 | Rigorous | Sound | Rigorous | Sound | Sound | Rigorous | PASS | PASS | 15 |
| P05 | Q-P2-run2 | Rigorous | Sound | Rigorous | Sound | Sound | Sound | PASS | PASS | 14 |
| P06 | Q-P3-run1 | Rigorous | Hand-wavy | Sound | Sound | Sound | Sound | PASS | PASS | 12 |
| P01 | Q-P3-run2 | Rigorous | Sound | Rigorous | Sound | Sound | Rigorous | PASS | PASS | 15 |

- **Aggregate band total: 85 / 108.** Mean per-analysis: **14.17**.
- **Pass split: 6 PASS / 0 FAIL** (derived verdict agrees with the judge's stated verdict on
  all six — zero D-14 disagreements, zero `UNPARSEABLE` cells across either scoreline file).
- **Per-criterion column sums** (of a possible 18 each, six analyses): C1=18, C2=11, C3=17,
  C4=12, C5=12, C6=15 (sums to 85, matching the aggregate).

**No figure above was a target.** The original v8.6 experiment's headline (band total 35/35
across both arms, mean 11.67 each, 2/3 PASS per arm) is a different experiment — three
problems in **two** arms (A and B), one run each, six analyses total. This baseline is a single
arm at **six** generations (two runs per problem). Neither the old 35/35 figure nor this run's
own 85/108 was steered toward the other; they are not directly comparable totals (different
run counts), and this run's number is simply whatever the six live dispatches produced.

### Within-condition noise floor (D-08)

| Problem | Run 1 total | Run 2 total | Spread |
|---|---|---|---|
| Q-P1 | 14 | 15 | 1 |
| Q-P2 | 15 | 14 | 1 |
| Q-P3 | 12 | 15 | **3** |

**Maximum within-problem run-to-run spread: 3 band points out of 18**, on Q-P3 (attic
insulation vs. window replacement) — one run scored a single Hand-wavy (C2) with everything
else Sound/Rigorous (12/18), the other scored three Rigorous and three Sound with zero
Hand-wavy (15/18), on the same prompt, same agent body, same judge channel. **A Phase 166
post-fix movement on any one problem smaller than roughly 3 band points cannot be told apart
from this baseline's own run-to-run noise on that problem.** Q-P1 and Q-P2 both show a
narrower spread of 1, so the noise floor is not uniform across problems — Phase 166 should
read each problem's movement against its own row here, not against a single project-wide
number.

## Reproducibility (the headline finding)

This is a section of its own, not a footnote, because it is the first live measurement this
project has ever taken of a judge's own reproducibility, and the number is not small.

The six Phase-162-frozen analyses (`tests/quality-baseline-v8.7/analyses/`) were re-judged
through this run's own `claude -p` channel — byte-unchanged, including their trailing
transport-metadata tail (see "The extraction contract" below for why that tail was kept). The
result, mapped per-document via `tests/quality-baseline-v8.7/blinding-key.tsv` and
`rejudge-blinding-key.tsv`:

| Document | Original (Phase 162, Agent-tool channel) | Re-judged (this run, `claude -p` channel) | Cell agreement | Delta | Verdict |
|---|---|---|---|---|---|
| condB-P2 | 10/18 (R,H,S,H,H,S) | 11/18 (R,H,S,S,H,S) | 5/6 | +1 | FAIL → FAIL |
| condA-P1 | 12/18 (R,H,S,S,S,S) | 14/18 (R,S,R,S,S,S) | 4/6 | +2 | PASS → PASS |
| condB-P1 | 12/18 (R,S,S,H,S,S) | 14/18 (R,S,S,S,S,R) | 4/6 | +2 | PASS → PASS |
| condB-P3 | 13/18 (R,S,S,H,S,R) | 14/18 (R,S,S,S,S,R) | 5/6 | +1 | PASS → PASS |
| condA-P2 | 11/18 (R,H,S,S,S,H) | 12/18 (R,H,S,S,S,S) | 5/6 | +1 | **FAIL → PASS (VERDICT FLIP)** |
| condA-P3 | 12/18 (R,S,S,H,S,S) | 12/18 (R,S,S,H,S,S) | **6/6 (exact)** | +0 | PASS → PASS |

- **Aggregate: 70/108 → 77/108 (delta +7).** **Pass split: 4 PASS/2 FAIL → 5 PASS/1 FAIL** —
  one document (condA-P2) flipped FAIL to PASS on re-judging, with no change to its underlying
  text.
- **Only 1 of 6 documents (condA-P3) reproduced its full six-band vector exactly.** Cell-level
  agreement across all 36 scored cells: **29/36 (80.6%)**. Per-criterion agreement across the
  six documents: C1 6/6, C2 5/6, C3 5/6, **C4 3/6**, C5 6/6, **C6 4/6** — C4 (chain rigor) is
  the least reproducible single criterion.
- **The deltas are directional, not symmetric noise.** Five of six documents moved up
  (+1, +2, +2, +1, +1); the sixth moved by exactly zero. **None moved down.** A judge
  reproducing its own scoring at random would be expected to move some documents down as often
  as up; this run shows a one-sided drift toward higher bands on byte-identical input, not
  variance scattered around a stable mean.

**What this means for every live measurement in this project:** re-judging six unchanged
documents through the same channel on a different day moved the aggregate by +7 band points
out of 108 and flipped one of six verdicts, with no change whatsoever to the text being
scored. **A post-fix aggregate improvement smaller than roughly this magnitude (order +7/108,
one verdict flip) cannot be distinguished from re-judging the same documents on a different
day.** Phase 166 must read its own aggregate delta against this floor, not treat any positive
movement as evidence the fix worked.

**The byte-passthrough asymmetry:** the re-judge arm received the frozen corpus's analysis
files **byte-unchanged, including their trailing transport-metadata tail** (e.g.
`agentId: a684fc4e1bbe09c6f (use SendMessage with to: ...)\n<usage>subagent_tokens: ...` —
present on all six frozen files; see `tests/quality-probe-v8.7/README.md`'s "flagged
assumptions"). Stripping it would have changed the document under measurement and turned a
reproducibility measurement into a comparison of two different texts. This run's own
freshly-extracted analyses (`analyses/`) carry **no** such tail — the D-22 probe found the
primary extraction channel (`task_notification.summary`) ends at the analysis's own last
sentence, with no metadata appended. This asymmetry is real and is recorded here rather than
normalised away: the fresh-arm analyses and the re-judged frozen-corpus analyses are not quite
the same *shape* of document (one has an appended tail, one does not), even though both were
judged through the identical `claude -p` channel.

## Comparison basis (D-04)

**The channel-matched re-judged scoreline (`rejudge-scorelines.tsv`, 77/108, 5 PASS/1 FAIL) is
the Phase 166 comparison basis.** The original Agent-tool scoreline
(`tests/quality-baseline-v8.7/scorelines.tsv`, 70/108, 4 PASS/2 FAIL) is retained as historical
provenance and as the reproducibility evidence above, and is **explicitly not the comparison
basis** — comparing a post-fix `claude -p`-judged run against a pre-fix Agent-tool-judged run
would confound the fix's effect with the judging-channel change D-02 exists to remove.

`REQUIREMENTS.md` MEASURE-01 currently names "4 PASS / 2 FAIL, band total 35/35" (the original
two-arm experiment's figures) as the frozen basis; that text needs reconciling against the
figures in this README. **Phase 167 owns that reconciliation** — this document does not modify
`REQUIREMENTS.md`.

## Contents

- `analyses/Q-P{1,2,3}-run{1,2}.md` — the six freshly-generated analyses (one per problem, two
  runs each), extracted via `task_notification.summary` per the D-22 probe (see "The extraction
  contract" below). Each contains all six numbered output-contract sections.
- `captures/Q-P{1,2,3}-run{1,2}.jsonl` — the six raw generation stream captures, committed
  unmodified.
- `judgments/P0{1..6}-judge.jsonl` + `P0{1..6}-rationale.md` — the six **fresh** judge
  dispatches' raw responses (verbatim `.jsonl`) and their free-text rationale (never parsed
  into a score, captured as evidence per D-12).
- `rejudge-judgments/P0{1..6}-judge.jsonl` + `P0{1..6}-rationale.md` — the six **re-judge**
  dispatches' raw responses and rationale, over the frozen corpus. The run wrote the fresh and
  re-judged raw judge responses into two separate directories (matching the two arms'
  independent packet-ID shuffles — both arms reuse the `P01`–`P06` packet-ID space, so a single
  merged directory would have collided); together the two directories hold the twelve raw judge
  responses D-02 spends.
- `manifest.tsv` — one row per of the eighteen live invocations: kind, source identifier, run
  index, destination path, wall-clock duration, outcome (all `completed`), and re-dispatch
  reason (none — zero re-dispatches occurred).
- `scorelines.tsv` — the fresh baseline's eleven-column scorelines (`packet_id`, `C1`..`C6`,
  `judge_verdict`, `derived_verdict`, `agreement`, `source_id`).
- `rejudge-scorelines.tsv` — the D-02 channel-matched re-judge scorelines, same eleven columns,
  `source_id` naming the frozen-corpus file each row re-judged.
- `defect-incidence.tsv` — the D-18 mechanical defect detector's ten-column output over the six
  fresh analyses (D-21: reported alongside the band scores above, not alone).
- `blinding-key.tsv` — the fresh arm's packet-ID-to-source-analysis mapping, six rows, held in
  the directory root only (never inside or beside a packet).
- `rejudge-blinding-key.tsv` — the re-judge arm's packet-ID-to-frozen-corpus-source mapping, six
  rows. **The run wrote two separate six-row blinding-key files, one per arm** (rather than one
  file with twelve rows across both arms) — this is the shape `write_run_manifest`'s packet
  builder actually produced, copied here unedited.
- `run.log` — the one-line completion log the `--run` invocation printed.

## The extraction contract (why this evidence is trustworthy)

This README's own extraction contract differs from `tests/quality-baseline-v8.7/README.md`'s:
that document describes the **synchronous** Agent-tool channel (an orchestrator dispatching an
Agent-tool subagent inside an interactive session, where the analysis appears in the matching
`tool_result` block). This harness runs a fully scripted `claude -p` subprocess instead (D-01),
under which the Agent dispatch is **asynchronous**, and Plan 01's D-22 live transport probe
(`tests/quality-probe-v8.7/README.md`) found a different channel carries the verbatim text:

- **Primary channel:** the `system`/`task_notification` event's `summary` field, matched by
  `tool_use_id` against the Agent dispatch's `tool_use.id`. The probe confirmed this field ends
  at the analysis's own last sentence, with no trailing metadata, in every capture checked.
- **Guardrail A** (never the top-level `result` field): the top-level `result.result` field is
  an orchestrator paraphrase running at roughly 15-17% of the full payload's length and opens
  by falsely claiming to be "verbatim in substance" — confirmed directly on this project's own
  captures, not assumed from prior research.
- **Guardrail B** (dispatch count, not `tool_result` count): a run is rejected if it contains
  **more than one Agent dispatch** of `first-principles:first-principles`, not more than one
  `tool_result` block — a subagent using any internal tool legitimately produces extra unrelated
  `tool_result` events, so counting those would falsely reject well-formed runs.

Both guardrails run on every one of the six generations extracted into `analyses/` above (D-15
items 1-2), and both fire non-vacuously on negative fixtures per this harness's offline
self-test (`--self-test`, item 1 and item 2).

## Defect incidence (D-18/D-19/D-21)

`defect-incidence.tsv` reports three of the four defect families the original v8.6 experiment's
judges found (per `tests/quality-fixtures-v8.7/calibration-v8.6-corpus.md`'s D-19 calibration):
**untraced Conclusion claims** (`untraced_flag`), **non-conforming Verdict cells**
(`verdict_flag`), and **malformed Derivation Chains** (`chain_flag`). It does **not** cover the
fourth reported family — the near-absent `[Assumes: X]` inline token — a content-aware reading
this structural detector does not attempt (see the calibration finding, §4, for why).

Over this baseline's six fresh analyses: **`untraced_flag` 6/6, `verdict_flag` 5/6** (Q-P2-run1
is clean — the one instance in this whole baseline where a document scored zero
non-conforming Verdict cells), **`chain_flag` 6/6**. The `verdict_flag` 5/6 here differs from
the Phase-162-frozen corpus's own 6/6 on this family (`calibration-v8.6-corpus.md` §6) — an
observed difference between the two corpora, not a detector change.

**Per D-21, defect counts and rubric band scores must be read together.** The three families
above map onto this rubric's C2 (Verdict vocabulary), C4 (chain rigor), and C6 (Conclusion
traceability) — see the Aggregate result table above for this baseline's own C2/C4/C6 column
sums (11, 12, 15 respectively). Phase 166's verdict is required to report both the defect-count
movement and the C2/C4/C6 band movement together, and to name the Goodhart signature explicitly
if it appears: **defect counts falling while C2, C4, and C6 do not move.**

## Frozen-evidence discipline

These files are committed as-is. They are **never regenerated** (no live `claude` invocation
reproduces this exact run — it already happened) and **never hand-edited** to change a scored
outcome, a claim, a band, or a number. Any correction to this evidence would be a fresh
eighteen-invocation run with its own provenance record, never a silent edit of this one. Phase
166's post-fix re-measure reads this directory (specifically `rejudge-scorelines.tsv` as the
comparison basis) but does not modify it. `tests/quality-baseline-v8.7/` (the original
Phase-162-frozen corpus this baseline re-judged) remains separately frozen and untouched by
this plan — confirmed by `git diff --quiet -- tests/quality-baseline-v8.7` staying clean
through every commit in this plan.
