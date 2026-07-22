# v8.7 Correctness Spot-Check — Frozen Quality-Baseline Evidence

**Generated:** 2026-07-22. **Status:** FROZEN read-only evidence — never regenerated, never
edited to match a later result. This directory is the raw input to Phase 162's correctness
spot-check (`docs/v8.7-correctness-spot-check.md`); it is also the evidence base for
`docs/v8.6-quality-ab-experiment.md`'s blind A/B verdict, from which these six analyses,
their scores, and the blinding key originate unchanged.

## Scope note (Phase 164, D-11)

This directory remains the evidence base for `docs/v8.7-correctness-spot-check.md` and for the
v8.6 blind A/B verdict, both of which cite these exact paths. It is **no longer the comparison
basis** for the milestone's post-fix measurement (MEASURE-01) — that comparison uses
`tests/quality-baseline-v8.7-regenerated/` instead, because that baseline was generated from
freshly authored prompts that Phase 166's post-fix re-measure re-generates from, and this
directory's own original prompts are unrecoverable (see that directory's README). These same
six analyses were additionally re-judged through the scripted `claude -p` judge channel Phase
164 built, and that re-judged scoreline lives in the regenerated baseline's own directory
(`rejudge-scorelines.tsv`) — so the scoreline in this directory now also serves as
reproducibility evidence, alongside its original role as provenance for the two documents named
above. The files in this directory are unchanged by Phase 164 and stay unchanged.

## Provenance

| | |
|---|---|
| Arm A | agent body **590 lines** at `HEAD` (post-v8.6 compression) |
| Arm B | agent body **612 lines** at `ddf0e4a` (v8.5 terminal, pre-v8.6-compression) |
| Problems | 3, none drawn from the routing catalogs: REST/JSON→gRPC migration (P1), subscription churn / loyalty program (P2), attic insulation vs. window replacement (P3) |
| Runs | 6 (3 problems × 2 arms), one run per cell, `claude -p --plugin-dir` over the approach-② bypass wrapper |
| Judging | 6 independent judge subagents, each given exactly one anonymised analysis file plus `shared/spine/references/validation-rubric.md`, with no indication a comparison existed |
| Blinding | shuffled opaque judge IDs (X7/K2/M9/Q4/R6/T3); mapping key held only by the orchestrator until scoring completed |

## Aggregate result

Both arms **2/3 PASS**, band total **35/35**, mean **11.67** each. Per-criterion deltas
(A−B) point in both directions and cancel exactly (C1 0, C2 −1, C3 0, C4 +2, C5 +1, C6 −2).
Failures track the *problem* (P2 failed in both arms; P1 and P3 passed in both), not the
arm. Full analysis of this result lives in `docs/v8.6-quality-ab-experiment.md`; this
README documents only the evidence's provenance and chain of custody, not its
interpretation.

## Contents

- `analyses/cond{A,B}-P{1,2,3}.md` — the six full analysis documents, one per (arm, problem)
  cell. Each contains all six numbered output-contract sections (Problem Essence,
  Assumptions Table, Ground Truths, Derivation Chains, Abandoned Reasoning, Conclusion).
- `scorelines.tsv` — six rows: `judge_id  C1  C2  C3  C4  C5  C6  PASS/FAIL` (bands:
  Rigorous=3, Sound=2, Hand-wavy=1, Absent=0; hand-wavy cap and precedence rules per the
  validation rubric).
- `blinding-key.tsv` — maps each opaque judge ID to its source file
  (`judge_id  cond{A,B}-P{N}`).

## The extraction contract (why this evidence is trustworthy)

Each analysis was extracted from the `tool_result` block whose `tool_use_id` matches the
orchestrating Agent's `tool_use.id` — **not** from the stream's `result` field. The `result`
field is an orchestrator summary running at roughly 15% of the full payload (one measured
pair: agent `tool_result` = 16,866 chars vs. `result` field = 2,454 chars); scoring it would
have scored a summary of the analysis, not the analysis itself. This independently
corroborates the same diagnosis made of the v8.5 S-P02 Step 0 measurement.

Runs carrying multiple `tool_result` blocks were re-extracted individually rather than
concatenated. Two of the six original B-arm runs were found to have absorbed an
orchestrator `Read` tool call of `shared/spine/references/validation-rubric.md` itself into
the same message stream; naive concatenation would have glued the rubric text onto the
analysis, artificially inflating those two documents and producing a confident but false
"compression hurt quality" verdict (the corruption ran in the direction that would have
made B — the pre-compression arm — look *better*, so the failure mode is not a case of the
extraction bug flattering the analysis under test). Both were corrected by matching
`tool_result.tool_use_id` to the Agent `tool_use.id` before scoring.

These two traps — orchestrator-summary substitution and multi-block concatenation — are
the two documented near-misses in `docs/v8.6-quality-ab-experiment.md`'s "Methodology
warnings" section. Recording the extraction contract here, alongside the frozen files it
produced, is what lets a later reader trust that `analyses/*.md` really are the raw
agent-authored documents and not an artifact of how they were pulled out of the transport
stream.

## Frozen-evidence discipline

These six files, `scorelines.tsv`, and `blinding-key.tsv` are committed as-is. They are
**never regenerated** (no live `claude` invocation reproduces them — the analyses already
exist from the run this README documents) and **never hand-edited** to change a scored
outcome, a claim, or a number. Any correction to this evidence would have to be a fresh run
with its own provenance record, not a silent edit of this one. Phase 162's correctness
spot-check (`docs/v8.7-correctness-spot-check.md`) reads these files but does not modify
them.
