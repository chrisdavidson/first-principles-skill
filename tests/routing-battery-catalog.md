# Routing Battery Catalog — v4.3 (Merged: Boundary + Focused-Output)

## Purpose

This is the single merged catalog (BATT-01, D-07) that unions
`tests/sub-skill-routing-catalog.md` (boundary discipline rows) and
`tests/focused-output-catalog.md` (focused-output rows) into one two-expectation-column
fixture. Each row carries both an `Expected Boundary` column and an `Expected Output`
column; `n-a` means "this signal is not scored for this row" (D-01/D-02).

## De-Collision Scheme

The two source catalogs use **colliding row IDs for different prompts** — `P12`/`P24`/`N1`
denote a non-slash oblique prompt in `sub-skill-routing-catalog.md` but a slash-prefixed
prompt in `focused-output-catalog.md`. The merged catalog de-collides them with prefixes
(D-03, Option A):

- `B-` prefix — boundary rows from `tests/sub-skill-routing-catalog.md`
- `F-` prefix — focused-output rows from `tests/focused-output-catalog.md`

`parse_merged_catalog` strips the leading `[A-Z]-` prefix before testing `rid[0] in
("P","N")`, so `B-P12` classifies as a P-row and `B-N1` as an N-row.

## Run Command

```bash
python3 scripts/check-routing-battery.py \
  --catalog tests/routing-battery-catalog.md \
  --repeat 5 --min-pass 3 \
  --boundary-p-threshold 2 \
  --focused-p-threshold 4 --focused-n-threshold 1
```

## Anti-Regression Warning

> Do not re-collapse B-* and F-* rows into a shared ID namespace — the two source
> catalogs use colliding IDs for genuinely different prompts. Do not "fix" any
> `none-or-other` expectation in the B-* rows by re-expecting direct sub-skill firing;
> all eleven sub-skills are `disable-model-invocation: true` (Path 2 architecture).
> Do not remove the `n-a` sentinels — they encode which signal applies to each prompt
> and drive the both-match auto-pass logic in `_both_match`.

## History

This catalog was created in Phase 67 to union `tests/sub-skill-routing-catalog.md`
(boundary discipline, 4 rows: B-P12/B-P24/B-N1/B-N2) and `tests/focused-output-catalog.md`
(FU-21 gate, 5 rows: F-P12/F-P24/F-P25/F-P26/F-N1) under B-/F- de-collided IDs. The
merge eliminates the fixture-drift failure mode that motivated v4.3: both catalogs are now
a single committed source of truth parsed by one battery (`scripts/check-routing-battery.py`).

---

## Merged Catalog

| # | Prompt | Expected Boundary | Expected Output | Signal | Lineage |
|---|--------|-------------------|-----------------|--------|---------|
| B-P12 | "The plan looks solid and the team is excited, but I am nervous. Before we lock it in, I want to surface every way this could blow up." | none-or-other | n-a | boundary | Verbatim from `.planning/eval/v2.0-routing-prompts.md` line 42. Under the Path 2 / Phase 46 architecture, all eleven sub-skills are registered `disable-model-invocation: true` (slash-only stubs); the orchestrator never auto-routes to them. Composer-routing (`none-or-other`) is the architecturally correct outcome. FU-21-1 correctness is now measured by `scripts/check-focused-output.py`. |
| B-P24 | "We are confident the data migration will go fine. I would rather figure out everything that would make it go wrong instead." | none-or-other | n-a | boundary | Verbatim from `.planning/eval/v2.0-routing-prompts.md` line 54. Under the Path 2 / Phase 46 architecture, all eleven sub-skills are registered `disable-model-invocation: true`; the orchestrator never auto-routes to them. Composer-routing (`none-or-other`) is the architecturally correct outcome. FU-21-2 correctness is now measured by `scripts/check-focused-output.py`. |
| B-N1 | I'm nervous about my Python script — it crashes on startup and I can't figure out why. Surface what could be wrong with my error handling. | none-or-other | n-a | boundary | Adjacent vocabulary (`nervous`, `surface`, `what could be wrong`) overlaps the widened `:pre-mortem` trigger surface, but the prompt is a debugging request explicitly excluded by the `shared/spine/SKILL.meta.yml` scope clause ("Not for routine code review, debugging, performance optimization, or general Q&A"). Style precedent: mirrors N5 and N13 in `tests/routing-catalog.md` — vocabulary-adjacent to the trigger class but off-scope. |
| B-N2 | "We have a written plan to roll out the new authentication system across all teams next quarter. Before we lock the timeline, walk through how this could go badly — what failure modes should we prepare for?" | none-or-other | n-a | boundary | Under the Path 2 / Phase 46 architecture, `none-or-other` (composer-routing) is the only architecturally correct outcome at the orchestrator boundary — sub-skills are `disable-model-invocation: true` and never auto-route. The pre-mortem-vs-inversion boundary-correctness intent of this prompt (plan-shaped traffic must not be poached by `:inversion`) has migrated to the focused-output catalog (`tests/focused-output-catalog.md`), where slash-invoked technique dispatch is the canonical FU-21 gate. |
| F-P12 | /first-principles:pre-mortem We are launching a new data pipeline in two weeks. The pipeline ingests customer transaction records, transforms them through three ETL stages, and loads into a reporting database. Engineering is confident; we have tested each stage in isolation. Walk through this plan as if it has already failed — what caused it? | n-a | focused-pre-mortem | focused | FU-21-1: slash invocation with substantive plan and ETL-stage specifics produces focused pre-mortem analysis. The plan includes enough concrete detail (stages, timeline, confidence signal) for the agent to run the procedure end-to-end without asking for clarification. |
| F-P24 | /first-principles:inversion Everyone knows that shipping features faster leads to more customer satisfaction. Invert this claim — what would have to be true for rapid feature shipping to cause customer dissatisfaction? | n-a | focused-inversion | focused | FU-21-2: slash invocation with a clear confidence-flip claim produces focused inversion output. The claim is concrete and directly invertible. v3.8 was 5/5 PASS — robust. |
| F-P25 | /first-principles:pre-mortem Our team is planning a cloud infrastructure migration: moving from on-premise servers to AWS over three months. Phase 1 (month 1) migrates the dev and staging environments. Phase 2 (month 2) migrates non-critical production services. Phase 3 (month 3) migrates the core production database. We have a runbook and a rollback plan for each phase. Assume this migration has already failed at month 2 — what caused it? | n-a | focused-pre-mortem | focused | N2-boundary fixture (FOCUS-03, D-02/D-03): a distinct plan-shaped scenario (infrastructure migration with explicit phases and rollback plan) that slash-invokes :pre-mortem. Validates that focused-pre-mortem fires on plan-shaped content beyond the auth-rollout scenario in P26. The multi-phase structure is realistic; Phase/Ground Truths/Verdict vocabulary in the output is expected (Signal A routing-envelope priority handles it). |
| F-P26 | /first-principles:pre-mortem We have a written plan to roll out the new authentication system across all teams next quarter. Before we lock the timeline, walk through how this could go badly — what failure modes should we prepare for? | n-a | focused-pre-mortem | focused | Preserves v3.8 N2 lineage (D-03): plan-shaped slash invocation must produce focused-pre-mortem without drifting to full-composer (agent runs multiple techniques despite the slash). Auth-rollout prompt verbatim from tests/sub-skill-routing-catalog.md line 65. Re-IDed from N2 to P26 because its expected verdict is focused-pre-mortem (a positive expectation), so it belongs in the P bucket rather than the N bucket. |
| F-N1 | I'm feeling nervous about a production deployment. There are a lot of moving parts and something could go wrong. What could be the issue here? | n-a | NOT-any-focused | focused | Over-trigger guard: debugging-shaped prompt with NO slash prefix and vocabulary like "nervous", "moving parts", "what could be wrong" must never produce any focused-<technique> output. The expected value NOT-any-focused matches any of {none, ambiguous, full-composer} — the over-trigger guard structurally holds regardless of which non-focused classification the run produces. |
