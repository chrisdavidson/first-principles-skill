# Track B Prompt Catalog — v9.13

**Frozen 2026-09-25, before any Track B run.** Registered by
`docs/trackb-preregistration.md` §4. Ten prompts across four domains.

## Provenance and exclusion rule

**None of these prompts appears in any existing catalog** — not
`tests/routing-catalog.md`, `tests/routing-battery-catalog.md`,
`tests/step0-fixture-catalog.md`, `tests/quality-catalog-*.md`,
`tests/premise-rejection-catalog.md`, or `tests/live-conformance-catalog.md`.

That exclusion is load-bearing, not hygiene. The agent body has been shaped over many
milestones against those prompts — phrase-detection rules were tuned on them, technique
markers were pinned to them. Reusing one would measure how well the agent has been
fitted to its own test set, and would favour arm T for a reason that has nothing to do
with whether the methodology helps.

## The prompt framing, and why it is the conservative choice

Every prompt below **explicitly asks for a rigorous, ground-up analysis**, and the
byte-identical text goes to both arms.

The alternative framing — give both arms a bare problem statement — was considered and
rejected as the *easier* test. A bare prompt confounds two effects: the benefit of
asking for rigour at all, and the benefit of this plugin. Arm C would likely produce a
casual answer, arm T a careful one, and the measured difference would substantially be
the difference between asking and not asking.

Asking both arms for rigour isolates the plugin's own contribution: **given that the
user has already asked for a careful analysis, does routing it through this agent
produce a better one than the model does unaided?** That is the harder question and the
one a prospective user is actually owed an answer to, since they can always just ask
carefully themselves.

This framing is registered as primary. It is expected to *shrink* the measured effect
relative to the bare-prompt framing, and that is the intended direction.

## Catalog

| ID | Domain | Prompt |
|---|---|---|
| TB-01 | software | Reason from the ground up about whether our team should replace our REST API with GraphQL. We have 9 client applications, 3 of them mobile, and our main complaint is that mobile screens need 4–6 round trips to render. Be rigorous and show your reasoning. |
| TB-02 | software | Work this through from first principles and be rigorous: our CI pipeline takes 47 minutes and developers have started batching merges to avoid it. Leadership wants us to buy faster runners. Is that the right call? |
| TB-03 | software | Think carefully and from the ground up about whether a small team of six engineers should adopt a microservice architecture for a product that currently has about 1,200 daily active users and one deployable. |
| TB-04 | policy | Analyse rigorously and from the ground up: a mid-sized city wants to cut commuter car journeys by 20% within three years, and is choosing between free public transit, congestion pricing, and building protected cycle lanes. What should determine the choice? |
| TB-05 | policy | Reason this out carefully from base principles. A national regulator proposes requiring all AI systems used in hiring to publish their training data sources. What would actually follow from that rule, and would it achieve what it is aimed at? |
| TB-06 | policy | Be rigorous and reason from the ground up about whether a university should replace timed written exams with take-home assessments now that capable writing assistants are widely available. |
| TB-07 | science | Reason from first principles, rigorously: how much land would be needed to supply the entire electricity demand of a country of 10 million people using solar photovoltaics alone, and what does that number imply about the feasibility of doing so? |
| TB-08 | science | Think this through carefully from fundamentals. A lab reports that a new catalyst raises the yield of their reaction from 62% to 71%, measured across three runs. What should be concluded, and what should not be? |
| TB-09 | personal | Reason carefully and from the ground up: I am 34, have savings covering 11 months of expenses, and am deciding whether to leave a stable job to join a four-person startup at a 30% pay cut for equity. How should I think about this? |
| TB-10 | personal | Analyse this rigorously and from first principles: a family is deciding whether to move closer to ageing parents, which would mean both adults changing jobs and the children changing schools. What should actually drive the decision? |

## Domain balance

| Domain | Count | IDs |
|---|---|---|
| software | 3 | TB-01, TB-02, TB-03 |
| policy | 3 | TB-04, TB-05, TB-06 |
| science | 2 | TB-07, TB-08 |
| personal | 2 | TB-09, TB-10 |

§5 condition 3 of the pre-registration requires the effect to hold in direction on at
least three of these four domains, so no single domain can carry the result.

## Deliberate design properties

- **TB-02, TB-04 and TB-06 embed a pre-selected solution** the analysis should be
  willing to reject. They test whether either arm recovers the underlying question
  rather than optimising the user's chosen answer.
- **TB-08 has a defensible answer that is largely negative** — three runs do not
  support a strong conclusion. It is included so that the rubric's Calibration
  criterion has something to bite on in both arms.
- **TB-07 is the only prompt with a checkable numerical answer.** It is not scored
  differently, but its arithmetic is recorded in the run manifest for later use.
- **No prompt requires external tool access to answer well.** Arm C is not disadvantaged
  by lacking a plugin that encourages source-fetching, because none of these questions
  turns on a fact that must be looked up.
