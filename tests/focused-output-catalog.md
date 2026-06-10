# Focused-Output Catalog — v4.2 (FU-21-1 / FU-21-2 canonical gate)

## Purpose

This catalog is the canonical FU-21 technique-dispatch gate. It verifies that
explicit slash invocations of the first-principles sub-skills produce the correct
focused-technique output (Path 2: `/first-principles:<technique>` invoked with
substantive content → the corresponding focused analysis fires).

Two gate sub-requirements:
- **FU-21-1:** Slash invocation with a substantive plan → focused pre-mortem output.
- **FU-21-2:** Slash invocation with a confidence-flip claim → focused inversion output.

The catalog has **4 P rows (P12, P24, P25, P26)** and **1 N row (N1)**. P26 carries the
v3.8 N2 lineage: plan-shaped slash invocation must produce focused-pre-mortem without
drifting to full-composer. It was re-IDed from N2 to P26 because its expectation is
positive (`focused-pre-mortem`), so it belongs in the P bucket. N1 is the sole negative
control: non-slash debugging traffic must never produce any focused output.

## Run Command

```bash
python3 scripts/check-focused-output.py \
  --catalog tests/focused-output-catalog.md \
  --repeat 5 --min-pass 3 \
  --p-threshold 4 --n-threshold 1
```

> Note: All four P-prompts (P12, P24, P25, P26) must pass K-of-N, and the single
> N-prompt (N1, the over-trigger negative control) must pass at 1/1. The thresholds are
> passed explicitly above for clarity; the script's built-in defaults now gate at these
> calibrated values (4/1), so a bare run is also strict. Passing the flags explicitly is
> still recommended to make intent visible.

---

## Positive Cases — Slash-invoked focused output (P-prefixed rows count toward --p-threshold)

| # | Prompt | Expected | Technique | Rationale |
|---|--------|----------|-----------|-----------|
| P12 | /first-principles:pre-mortem We are launching a new data pipeline in two weeks. The pipeline ingests customer transaction records, transforms them through three ETL stages, and loads into a reporting database. Engineering is confident; we have tested each stage in isolation. Walk through this plan as if it has already failed — what caused it? | focused-pre-mortem | pre-mortem | FU-21-1: slash invocation with substantive plan and ETL-stage specifics produces focused pre-mortem analysis. The plan includes enough concrete detail (stages, timeline, confidence signal) for the agent to run the procedure end-to-end without asking for clarification. |
| P24 | /first-principles:inversion Everyone knows that shipping features faster leads to more customer satisfaction. Invert this claim — what would have to be true for rapid feature shipping to cause customer dissatisfaction? | focused-inversion | inversion | FU-21-2: slash invocation with a clear confidence-flip claim produces focused inversion output. The claim is concrete and directly invertible. v3.8 was 5/5 PASS — robust. |
| P25 | /first-principles:pre-mortem Our team is planning a cloud infrastructure migration: moving from on-premise servers to AWS over three months. Phase 1 (month 1) migrates the dev and staging environments. Phase 2 (month 2) migrates non-critical production services. Phase 3 (month 3) migrates the core production database. We have a runbook and a rollback plan for each phase. Assume this migration has already failed at month 2 — what caused it? | focused-pre-mortem | pre-mortem | N2-boundary fixture (FOCUS-03, D-02/D-03): a distinct plan-shaped scenario (infrastructure migration with explicit phases and rollback plan) that slash-invokes :pre-mortem. Validates that focused-pre-mortem fires on plan-shaped content beyond the auth-rollout scenario in P26. The multi-phase structure is realistic; Phase/Ground Truths/Verdict vocabulary in the output is expected (Signal A routing-envelope priority handles it). |
| P26 | /first-principles:pre-mortem We have a written plan to roll out the new authentication system across all teams next quarter. Before we lock the timeline, walk through how this could go badly — what failure modes should we prepare for? | focused-pre-mortem | pre-mortem | Preserves v3.8 N2 lineage (D-03): plan-shaped slash invocation must produce focused-pre-mortem without drifting to full-composer (agent runs multiple techniques despite the slash). Auth-rollout prompt verbatim from tests/sub-skill-routing-catalog.md line 65. Re-IDed from N2 to P26 because its expected verdict is focused-pre-mortem (a positive expectation), so it belongs in the P bucket rather than the N bucket. |

---

## Negative Controls — Confirms focused output only fires on slash invocations (N-prefixed rows count toward --n-threshold)

The N bucket contains exactly one row: N1, the true over-trigger negative control.
There are no inverted-expectation rows in the N bucket — the former N2 (whose expected
verdict was the positive `focused-pre-mortem`) was re-IDed to P26 and moved to the P
bucket above.

| # | Prompt | Expected | Off-Target Risk | Rationale |
|---|--------|----------|-----------------|-----------|
| N1 | I'm feeling nervous about a production deployment. There are a lot of moving parts and something could go wrong. What could be the issue here? | NOT-any-focused | Over-trigger: non-slash debugging traffic must never produce focused-pre-mortem output | Over-trigger guard: debugging-shaped prompt with NO slash prefix and vocabulary like "nervous", "moving parts", "what could be wrong" must never produce any focused-<technique> output. The expected value NOT-any-focused matches any of {none, ambiguous, full-composer} — the over-trigger guard structurally holds regardless of which non-focused classification the run produces. |
