# Focused-Output Catalog — v4.2 (FU-21-1 / FU-21-2 canonical gate)

## Purpose

This catalog is the canonical FU-21 technique-dispatch gate. It verifies that
explicit slash invocations of the first-principles sub-skills produce the correct
focused-technique output (Path 2: `/first-principles:<technique>` invoked with
substantive content → the corresponding focused analysis fires).

Two gate sub-requirements:
- **FU-21-1:** Slash invocation with a substantive plan → focused pre-mortem output.
- **FU-21-2:** Slash invocation with a confidence-flip claim → focused inversion output.

The over-trigger guard (N1) ensures that non-slash debugging traffic never produces
any focused output. The N2 row preserves the v3.8 lineage: plan-shaped slash invocation
must produce focused-pre-mortem without drifting to full-composer.

## Run Command

```bash
python3 scripts/check-focused-output.py \
  --catalog tests/focused-output-catalog.md \
  --repeat 5 --min-pass 3 \
  --p-threshold 2 --n-threshold 1
```

> Note: All three P-prompts must pass K-of-N (thresholds passed explicitly above).
> The script's built-in defaults remain at 0 until Phase 66 calibrates them — do not omit the threshold flags from the run command.

---

## Positive Cases — Slash-invoked focused output (P-prefixed rows count toward --p-threshold)

| # | Prompt | Expected | Technique | Rationale |
|---|--------|----------|-----------|-----------|
| P12 | /first-principles:pre-mortem We are launching a new data pipeline in two weeks. The pipeline ingests customer transaction records, transforms them through three ETL stages, and loads into a reporting database. Engineering is confident; we have tested each stage in isolation. Walk through this plan as if it has already failed — what caused it? | focused-pre-mortem | pre-mortem | FU-21-1: slash invocation with substantive plan and ETL-stage specifics produces focused pre-mortem analysis. The plan includes enough concrete detail (stages, timeline, confidence signal) for the agent to run the procedure end-to-end without asking for clarification. |
| P24 | /first-principles:inversion Everyone knows that shipping features faster leads to more customer satisfaction. Invert this claim — what would have to be true for rapid feature shipping to cause customer dissatisfaction? | focused-inversion | inversion | FU-21-2: slash invocation with a clear confidence-flip claim produces focused inversion output. The claim is concrete and directly invertible. v3.8 was 5/5 PASS — robust. |
| P25 | /first-principles:pre-mortem Our team is planning a cloud infrastructure migration: moving from on-premise servers to AWS over three months. Phase 1 (month 1) migrates the dev and staging environments. Phase 2 (month 2) migrates non-critical production services. Phase 3 (month 3) migrates the core production database. We have a runbook and a rollback plan for each phase. Assume this migration has already failed at month 2 — what caused it? | focused-pre-mortem | pre-mortem | N2-boundary fixture (FOCUS-03, D-02/D-03): a distinct plan-shaped scenario (infrastructure migration with explicit phases and rollback plan) that slash-invokes :pre-mortem. Validates that focused-pre-mortem fires on plan-shaped content beyond the auth-rollout scenario in N2. The multi-phase structure is realistic; Phase/Ground Truths/Verdict vocabulary in the output is expected (Signal A routing-envelope priority handles it). |

---

## Negative Controls — Confirms focused output only fires on slash invocations (N-prefixed rows count toward --n-threshold)

| # | Prompt | Expected | Off-Target Risk | Rationale |
|---|--------|----------|-----------------|-----------|
| N1 | I'm feeling nervous about a production deployment. There are a lot of moving parts and something could go wrong. What could be the issue here? | NOT-any-focused | Over-trigger: non-slash debugging traffic must never produce focused-pre-mortem output | Over-trigger guard: debugging-shaped prompt with NO slash prefix and vocabulary like "nervous", "moving parts", "what could be wrong" must never produce any focused-<technique> output. The expected value NOT-any-focused matches any of {none, ambiguous, full-composer} — the over-trigger guard structurally holds regardless of which non-focused classification the run produces. |
| N2 | /first-principles:pre-mortem We have a written plan to roll out the new authentication system across all teams next quarter. Before we lock the timeline, walk through how this could go badly — what failure modes should we prepare for? | focused-pre-mortem | Drift: plan-shaped slash invocation could produce full-composer (agent runs multiple techniques despite the slash) | Slash routing must hold on plan-shaped prompts. This row preserves v3.8 N2 lineage (D-03). N-prefix kept to maintain v3.8 row-ID continuity; the expected value is focused-pre-mortem, not NOT-any-focused — the N-prefix only routes which threshold bucket the match counts toward. Auth-rollout prompt verbatim from tests/sub-skill-routing-catalog.md line 65. |
