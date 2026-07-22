# Quality Harness Prompt Catalog — v8.7

## Purpose

This is the prompt catalog for `scripts/check-quality-harness.py` (HARNESS-01), the promoted
blind-judged quality-measurement instrument. It is read via `--catalog`, matching the shape
`tests/routing-catalog.md` and `tests/step0-fixture-catalog.md` already use.

**The original v8.6 A/B experiment's P1/P2/P3 prompts are unrecoverable — confirmed, not assumed.**
Nothing in git, nothing surviving in `/tmp`, nothing in the Phase 162 summary; only one-line prose
descriptions of the three topics survive in `tests/quality-baseline-v8.7/README.md`'s Provenance
table. Reconstructing the verbatim prompts from the six frozen analyses they produced would derive
the input from the outputs it produced, which is circular (D-06).

The three rows below are **fresh authorings**, not reconstructions, that keep the same three topics
— REST/JSON→gRPC migration, subscription churn / loyalty program, attic insulation vs. window
replacement (D-09) — for continuity with Phase 162's correctness spot-check, which verified exactly
these domains' numbers. Both the pre-fix baseline this phase freezes and the Phase 166 post-fix
re-measure generate from this same catalog, so the two are a matched pair and the comparison is a
strict same-prompt comparison rather than one confounded by different prompts on each side (D-07).

Each prompt is worded as a decision a person is actually facing, with enough concrete numbers that
the agent can reason rather than ask for context — the same posture `tests/step0-fixture-catalog.md`'s
rows take. Each prompt contains no technique name and fires no Step 0 trigger phrase (confirmed live
against `scripts/check-step0-emulator.py`), so all three reach the full six-section composer, not a
focused technique.

## Run Command

```bash
mkdir -p /tmp/qh-probe
python3 scripts/check-quality-harness.py --probe Q-P1 \
    --catalog tests/quality-catalog-v8.7.md \
    --plugin-dir first-principles \
    --out /tmp/qh-probe
```

## Catalog

| ID | Prompt | Notes |
|---|---|---|
| Q-P1 | Our platform team runs 22 internal microservices that talk to each other over REST/JSON, handling 340,000 requests per minute at peak with a median inter-service latency of 48ms. Our infrastructure lead wants to migrate the six highest-traffic services to gRPC over the next two quarters, citing a competitor's public benchmark claiming 30 percent lower p99 latency. The migration needs 5 engineers for about 10 weeks, our on-call rotation currently has only 3 people covering it, and every team that consumes those services would have to regenerate client stubs and redeploy. Should we commit the team to this migration now, or hold off another year? | REST/JSON-to-gRPC migration decision (D-09 topic 1). Fresh authoring, not a reconstruction of the unrecoverable original P1. Classifies `full-composer` on the offline Step 0 emulator; no technique name; off-catalog against `tests/routing-catalog.md`, `tests/routing-battery-catalog.md`, `tests/step0-fixture-catalog.md`. |
| Q-P2 | Our subscription product has 48,000 active members paying $19 a month, and monthly churn has climbed from 4.2 percent to 6.8 percent over the last two quarters. Customer success wants to launch a loyalty program that lets members redeem points for account credit, costing around $310,000 a year to run, betting it will pull churn back toward 5 percent. A rival service just launched a similar program last month. Marketing wants a final call within three weeks before the next board update. Should we fund the loyalty program at that price point? | Subscription-churn / loyalty-program decision (D-09 topic 2) — the problem known to reliably fail in both arms of the original v8.6 A/B. Fresh authoring, not a reconstruction of the unrecoverable original P2. Classifies `full-composer`; no technique name; off-catalog against the three routing/Step-0 catalogs. |
| Q-P3 | Our 1948 house is losing around 35 percent of its heating energy through some combination of the attic and the windows. One contractor quoted $4,200 to blow in R-49 attic insulation, replacing the current R-13. A second quote came in at $18,500 for full triple-pane window replacement across all 14 windows. Our winter heating bill currently averages $410 a month over the four coldest months, and we plan to stay in this house for at least another 10 years. Should we do the insulation, the windows, both, or neither this year? | Attic-insulation-versus-window-replacement decision (D-09 topic 3). Fresh authoring, not a reconstruction of the unrecoverable original P3. Classifies `full-composer`; no technique name; off-catalog against the three routing/Step-0 catalogs. |
