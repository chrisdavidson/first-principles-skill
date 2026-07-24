# Quality Harness Prompt Catalog — v8.10 Out-of-Sample

## Purpose

This is the fresh-problem catalog for Phase 173 (`CORRECTGATE-01`'s out-of-sample validation of
FIX-CONTRACT-01, requirement CGATE-01). It is read via `--catalog`, matching the shape
`tests/quality-catalog-v8.7.md`, `tests/routing-catalog.md`, and `tests/step0-fixture-catalog.md`
already use.

**This is a fresh authoring, not a reconstruction.** Every row below is a brand-new topic,
distinct in both domain and decision shape from the three topics used consistently since v8.6:
Q-P1 (REST/JSON→gRPC service migration), Q-P2 (subscription-churn/loyalty-program economics), and
Q-P3 (attic insulation vs. window replacement) — all three defined in `tests/quality-catalog-v8.7.md`
and re-run as the frozen six `tests/quality-baseline-v8.7-postfix/analyses/*.md`. Phase 173 exists
to generate genuinely out-of-sample evidence, so re-running the same three topics with new numbers
would not serve that purpose — six new domains are used instead (org/people, manufacturing capex,
software-architecture, logistics build-vs-buy, personal/career, healthcare-ops capex).

Each prompt is worded as a decision a person is actually facing, with enough concrete numbers that
the agent can reason rather than ask for context — the same posture `tests/quality-catalog-v8.7.md`
and `tests/step0-fixture-catalog.md` take. Each prompt contains no technique name and fires no
Step 0 trigger phrase — **confirmed live against `scripts/check-step0-emulator.py --prompt` in this
session, once per row, after finalizing wording** — so all six reach the full six-section composer,
not a focused technique. This catalog makes no claim about what any of the six fresh analyses will
actually conclude, trace, or score — that is explicitly out of scope for this catalog and reserved
for the Plan 02 live capture and Plan 03 hand-read.

## Run Command

```bash
mkdir -p /tmp/qh-173/captures
python3 scripts/check-quality-harness.py --probe Q-N1 \
    --catalog tests/quality-catalog-v8.10-oos.md \
    --plugin-dir first-principles \
    --out /tmp/qh-173/captures
```

## Catalog

| ID | Prompt | Notes |
|---|---|---|
| Q-N1 | Our streaming-data team has a Kafka/Flink capability gap and a streaming feature is committed to a customer in 6 months. We could hire one senior streaming engineer — a search we estimate at about 3 months and roughly $195,000 in first-year compensation — or train two of our current mid-level engineers through an 8-week external program costing about $12,000 each, plus several more months of on-the-job ramp afterward. The team is 7 people and lost 2 engineers to attrition last year. Should we hire externally, train internally, or do both? | Hiring-vs-upskilling / org-people decision. Classifies `full-composer` on the offline Step 0 emulator (confirmed this session); no technique name. Off-catalog against `tests/routing-catalog.md`, `tests/routing-battery-catalog.md`, `tests/step0-fixture-catalog.md`. Topic-distinct from Q-P1/Q-P2/Q-P3 (org/people domain, not infra/subscription/home-energy). Fresh authoring. |
| Q-N2 | Our specialty-coffee roastery is selling out capacity most weeks. We're deciding between buying a second 35kg roaster for $88,000 plus $15,000 in electrical and ventilation work, or adding a second daily shift on our current 15kg machine at about $4,200 a month in labor, which wears the machine faster. Demand is up 20 percent year over year, but two of our largest wholesale accounts are on month-to-month terms with no long-term commitment. Should we buy the second roaster, add the shift, or hold off? | Manufacturing-capex / throughput decision. Classifies `full-composer` (confirmed this session); no technique name. Off-catalog against the three routing/Step-0 catalogs. Topic-distinct from Q-P1/Q-P2/Q-P3 (small-manufacturing capex, not infra/subscription/home-energy). Fresh authoring. |
| Q-N3 | We maintain separate native iOS and Android apps, each about 60,000 lines of code with 4 engineers per platform. We're considering consolidating both into a single Flutter codebase, which would need about 5 engineers and roughly 7 months, during which feature work on both platforms would largely stall. About a third of our users are on older devices, and our biggest customer renews their contract in 9 months and is asking for two specific features. Should we consolidate to Flutter, keep both native codebases, or delay the decision? | Cross-platform mobile-rewrite / software-architecture decision. Classifies `full-composer` (confirmed this session); no technique name. Off-catalog against the three routing/Step-0 catalogs. Topic-distinct from Q-P1/Q-P2/Q-P3 (client-app consolidation, not service-to-service infra migration — different shape from Q-P1 despite both being software). Fresh authoring. |
| Q-N4 | West-coast orders make up 35 percent of our roughly 4,500 weekly orders and are growing. We're deciding whether to open a second warehouse on the west coast — about $420,000 a year on a 3-year lease, 8 new hires, and 2-day delivery — or hand west-coast fulfillment to a third-party logistics provider at about $3.10 per order with 2-day delivery but less control over packaging and returns. Should we build our own warehouse, use the 3PL, or split volume between them? | Fulfillment build-vs-buy / logistics decision. Classifies `full-composer` (confirmed this session); no technique name. Off-catalog against the three routing/Step-0 catalogs. Topic-distinct from Q-P1/Q-P2/Q-P3 (physical logistics, not infra/subscription/home-energy). Fresh authoring. |
| Q-N5 | I'm a data analyst making $95,000 a year, deciding between a part-time master's degree in machine learning — about $46,000 over 2 years at 15 hours a week — or self-study plus certifications, costing around $3,000 over the same 2 years, with more free time to build and ship a portfolio of real projects. Employers in the roles I want seem to screen partly on credentials and partly on demonstrated shipped work, and I'd keep working full-time either way. Should I pursue the master's, self-study, or some combination? | Part-time master's-vs-self-study / personal-career decision. Classifies `full-composer` (confirmed this session); no technique name. Off-catalog against the three routing/Step-0 catalogs. Topic-distinct from Q-P1/Q-P2/Q-P3 (individual career decision, not organizational infra/subscription/home-energy). Fresh authoring. |
| Q-N6 | Our four-dentist practice is deciding whether to buy an in-house CBCT imaging machine for about $110,000 plus roughly $9,000 a year in service and compliance costs. It would let us do same-day scans instead of referring out, capturing about $180 per scan on the roughly 25 referrals we send out each month, but the machine would sit idle much of the week. A neighboring practice has offered to share referrals with us if we buy one. Should we buy the CBCT machine, keep referring out, or explore the shared-referral arrangement first? | Clinic-imaging-capex / healthcare-ops decision. Classifies `full-composer` (confirmed this session); no technique name. Off-catalog against the three routing/Step-0 catalogs. Topic-distinct from Q-P1/Q-P2/Q-P3 (healthcare-practice capex, not infra/subscription/home-energy — closest in shape to Q-N2's capex-vs-labor-shift structure but a distinct domain and distinct specific tradeoff, per candidate-list review at plan time). Fresh authoring. |
