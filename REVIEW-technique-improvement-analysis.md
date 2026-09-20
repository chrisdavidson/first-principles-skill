# Technique and Validation Improvement Analysis

**Scope.** This review covers the eight companion techniques the `first-principles` agent runs, Phase 4 (Reason Upward, where most of the techniques get applied) and the validation layer (the Phase 5 operation plus the Self-Audit Gate rubric).
**Method.** I read the sources in `shared/` directly: `shared/references/*.md`, their four `-detail.md` appendices, `shared/spine/SKILL-body.md` and `shared/spine/references/validation-rubric.md`. I also read the assembled agent (`first-principles/agents/first-principles.md`, 807 lines) to see what the agent actually receives, and I recomputed the numbers in the worked examples myself.
**Nothing was modified.** This is analysis only. Any change it proposes would be made in `shared/`, followed by `python3 scripts/sync-content.py --write`.

**Relation to `REVIEW-agent-improvement-opportunities.md`.** That review covers a single demo run: the agent never opened its reference files, it rated chains HIGH while they rested on unverified inputs, and it used verdict vocabulary that doesn't exist. This document covers the *methodology content* itself. The two overlap in one place, the confidence model (§D3), and I've cross-referenced it there.

---

## Summary

The techniques are well chosen and mostly well written. Each one has a clear "when to use it", a clear boundary with its neighbours, and an explicit handoff into the five-phase spine. The problems cluster in four areas:

1. **Two worked examples model the errors their own techniques warn against.** The estimate example has an error of roughly 38,000× (about 4.6 orders of magnitude) that it labels "the right order of magnitude". The theoretical-limit example overstates headroom by using the loosest bound available. An LLM copies examples more readily than it follows prose, so these are the most important fixes. (§B7, §B8)
2. **Wiring gaps: two techniques are never called from any phase.** Pre-mortem and trade-off are described in the "Companion tools" summary, but no phase's Operation tells the agent to run them. Step 0 also claims Phase 4 "enumerates all eight" techniques, which Phase 4's own text doesn't do. (§A1, §A2)
3. **Validation checks form, not reasoning.** No criterion in the Self-Audit Gate asks whether each hop actually follows from the previous one, whether the arithmetic is right, or whether a rival conclusion was considered. A well-formatted chain with a non-sequitur hop can score Rigorous. (§D1, §D2)
4. **The confidence model rewards HIGH ratings and never defines HIGH.** Criterion 5's Rigorous band requires every conclusion to rest on a HIGH chain, and HIGH/MEDIUM/LOW are never defined positively. That pushes toward inflated confidence, which is the P1 failure the demo review found. (§D3)

### Top recommendations

| # | Change | Where | Effort |
|---|---|---|---|
| 1 | Fix the estimate worked example: the unit error, and the analogy used in place of a first-principles value | `shared/references/estimate-detail.md` | small |
| 2 | Add a **hop-validity** limb to Criterion 4, and an **arithmetic re-check** step to Phase 5 | `validation-rubric.md`, `SKILL-body.md` Phase 5 | small–medium |
| 3 | Wire **pre-mortem** (and inversion of the headline conclusion) into Phase 5's Operation, and **trade-off** into Phase 4's | `SKILL-body.md` | small |
| 4 | Add a **rival-conclusion / sensitivity** step to Phase 5: which ground truth, if false, flips the answer? | `SKILL-body.md` Phase 5 + Criterion 5 | medium |
| 5 | Decouple Criterion 5 Rigorous from "every claim rests on a HIGH chain"; score calibration instead; define HIGH/MEDIUM/LOW | `validation-rubric.md`, `output-template.md` | medium |
| 6 | Fix the theoretical-limit example; require the **tightest applicable bound**, and generalise the technique beyond physics | `theoretical-limit*.md` | small–medium |
| 7 | Trade-off: add scoring anchors, knock-out criteria and a mandatory weight-flip sensitivity check | `trade-off.md` | small |
| 8 | Resolve the Step 0 "all eight in Phase 4" contradiction, and the drift between the `/reason-upward` and `/validate` stubs and the agent body | `SKILL-body.md`, `reason-upward.md`, `validate.md` | small |

Under this repo's review protocol, all eight are **product**-tier: each changes the shipped methodology the agent executes. None requires a new gate.

---

## A. Cross-cutting findings: how the techniques are wired

### A1. Pre-mortem and trade-off are never invoked from a phase

I counted how often each technique name appears inside the five phase sections of the assembled agent (`first-principles/agents/first-principles.md:131-229`):

| Technique | Mentions in phase text | Called as an instruction? |
|---|---|---|
| fishbone | 2 | yes, in Phase 2 |
| inversion | 2 | yes, in Phase 2 |
| five-whys (reduce-to-primitives mode) | 1 | yes, in Phase 3 |
| estimate | 3 | yes, in Phase 4 |
| theoretical-limit | 3 | yes, in Phases 1 and 4 |
| second-order | 4 | yes, and mandatory: Phase 4 exit criterion (3) |
| **trade-off** | 1 | **no.** The one mention is inside a decision-rule parenthesis ("trade-off = qualitative weighted scoring"). |
| **pre-mortem** | **0** | **no** |

The only place either technique is placed in a phase is the "Companion tools" summary. Pre-mortem is at `first-principles.md:448` ("Use during Phase 5"), and trade-off is at `:453` ("Use during Phase 4"). Several other things point the same way: pre-mortem's own handoff says its output "feed[s] Phase 5 (Validate)" (`pre-mortem.md:109`), inversion says it "pairs with Pre-mortem when you want to stress-test in Phase 5", and inversion also suggests "invert the headline conclusion" after Phase 4 (`inversion.md:25`). Yet the Phase 5 Operation (`first-principles.md:222`) calls none of them.

**Effect.** Phase 5, the phase that exists to be "the adversarial pass", has no adversarial technique attached to it. It relies on free-form weakest-link inspection by the same model that wrote the chains.

**Suggested change.** In Phase 5's Operation add something like: *"When the conclusion is a plan or recommendation, apply the pre-mortem procedure to it; when it is a claim, invert the headline conclusion using the inversion procedure. Each structural weakness found becomes a named weak link or a confidence caveat."* In Phase 4 add: *"When two or more viable options remain, apply the trade-off procedure and collapse it into a chain per output-template §4."* The collapse form already exists (`trade-off.md:118-121`).

### A2. Step 0's "all eight in Phase 4" contradicts the phase text

`first-principles.md:122-125` says full-composer mode runs "Phase 4 enumerating all eight companion techniques", and that focused mode "only enumerate[s] the named technique in Phase 4". But three of the eight live in Phases 2–3 (fishbone, inversion, five-whys), pre-mortem belongs in Phase 5, and Phase 4's own text describes itself as "deliberately high-freedom" with applications that are conditional ("When a conclusion turns on a quantity…").

This causes two problems:
- **Mandatory padding.** Taken literally, "enumerate all eight" makes the agent run theoretical-limit on a hiring decision, or fishbone on a pricing question. That produces filler the rubric can't tell apart from analysis.
- **The focused-mode instruction doesn't line up.** `focused-fishbone` is told to enumerate fishbone "in Phase 4", but fishbone is a Phase 2 technique that feeds the Assumptions table.

**Suggested change.** Replace "enumerating all eight companion techniques in Phase 4" with "considering each companion technique at the phase that owns it, applying those whose *when to reach for this* condition fires, and recording a one-line *not applicable — [reason]* for the rest". That keeps the sweep auditable without forcing padding. Focused mode would then run its one technique at the phase that owns it.

### A3. The `/reason-upward` and `/validate` stubs have drifted from the agent body

The agent and the stubs are built from different sources: the body comes from `SKILL-body.md`, the stubs from `shared/references/<phase>.md`. They now disagree:

| Point | Agent body | Stub source |
|---|---|---|
| Phase 4 exit criterion | "ALL FOUR", including the end-of-phase Assumption Audit (`first-principles.md:212`) | "ALL THREE"; no Assumption Audit (`reason-upward.md:67`) |
| Phase 5 rubric use | "The criteria in the Self-Audit Gate are **not** applied at this step" (`:222`) | "Apply the **Validation Rubric** as a systematic check" (`validate.md:26-28`): the retired name, applied at the wrong step |

HARN-03 checks parity for the technique stubs. It apparently doesn't cover these two phase stubs, or it checks tokens rather than the exit criteria. Either way, a user running `/reason-upward` gets a looser phase than the agent does.

**Suggested change.** Bring both stub sources in line with the body. Better still, generate the phase stubs' Procedure and Exit criterion from `SKILL-body.md` the same way `{{PROCEDURE:slug}}` works, so they can't drift again.

### A4. Quota rules ("at least five", "at least three") invite padding

Inversion requires "at least five" failure conditions (`inversion.md:55`), and second-order requires "at least three" consequences per layer (`second-order.md:51,55`). Quotas help against thin output, but an LLM satisfies them by writing near-duplicates. Inversion's own worked example lists **four** conditions (`inversion.md:80-83`), which breaks its own rule.

**Suggested change.** Change the quota into a coverage prompt: "walk at least these lenses: technical, people/organisational, external/market, economic, time/dependency; one condition per lens where one exists, marking the ones that don't apply". Then fix the example so it complies.

### A5. Guidance written for human groups is spent on a single model

Pre-mortem step 3 ("Would I have suppressed this in a group?", `pre-mortem.md:43`) and the anchoring failure modes (`:94-99`), plus fishbone-detail's "blank-canvas paralysis… primes the group", were written for facilitated human sessions. For a single model they cost context and do nothing. What a model actually needs is a way to get *diverse* output from one generator.

**Suggested change.** Replace them with perspective rotation: "generate causes from the viewpoint of at least three named stakeholders (e.g. the implementer, the end user, the funder, an adversary/competitor), then merge".

---

## B. Per-technique findings

Each entry lists what works, the gaps and a suggested change. Evidence is cited by file and line under `shared/references/`.

### B1. Five-Whys & Decompose

**Works:** the two modes are clearly separated. The lateral scan ("what else caused this?") guards against single-thread drilling. The stop test (law / definition / measurement) is crisp. The detail file's warning that a vendor spec is not a measurement is valuable.

**Gaps**
- **Causal mode has no counterfactual test.** A link is accepted when it is "evidenced", but the procedure never asks *"had this cause been absent, would the symptom still have occurred?"* That question separates a cause from something that merely co-occurred, and it's the standard check in root-cause practice.
- **The stop rule stops at the first actionable level.** "Stop when a corrective action within your control exists" (`five-whys.md:66-68`) ends drilling at shallow fixes: "retrain the operator", "add a reminder". Nothing checks whether the fix removes the *class* of failure or only this instance. The classic failure is stopping at "human error".
- **Causal mode has no verdict format.** Reduce mode records `Verified — […]` / `Assumed — unverified` per branch (`:86-88`). Causal mode says "flag unevidenced links as assumed" (`:73-74`) with no required notation, so the `?` discipline doesn't carry over reliably.
- **"Direct measurement" in the core stop test lists "a datasheet spec"** (`:110-111`) without qualification. The qualification (a traceable, calibrated process) exists only in the detail file, which the agent may never open (see the demo review's R1).

**Suggested change**
- Add a counterfactual line to causal mode: "Validate each causal link with evidence **and** the counterfactual: would removing this cause have prevented the effect? A link that fails the counterfactual is a contributing condition, not a cause."
- Add a depth guard: "If the corrective names a person or 'be more careful', drill one level further. Ask what made the error possible or likely."
- Give causal links the same `Evidenced — <source>` / `Assumed` verdict format as reduce mode.
- Move the one-line spec caveat from the detail file into the core stop test.

### B2. Fishbone (Ishikawa)

**Works:** the category presets come with a decision rule, the set is locked before brainstorming, candidates are explicitly treated as `untested belief` and handed to Phase 2, and the exit criterion is good.

**Gaps**
- **Interactions are claimed but never captured.** The description says "multiple interacting contributors" (`fishbone.md:4`), but the exit criterion requires "each candidate cause attached to exactly one category" (`:115`), and no step records an interaction between causes.
- **"Prioritise" has no criterion.** Step 5 says "identify the branches most likely contributing based on available evidence" (`:109-112`) with no rule for doing it.
- **No discriminating test.** The most useful output of a cause map is *which observation would tell candidates apart* ("if it's the template server, lateness correlates with edit volume; if it's the all-hands, lateness appears only on meeting weeks"). The procedure never asks for one.
- **No "is the effect real?" check.** The default six-category set has no Measurement category (6M has one). In software and knowledge work, a metric artifact is a frequent "cause" of an apparent problem.

**Suggested change**
- Step 5: prioritise by (a) evidence that the cause was present when the effect occurred, and (b) whether it explains the effect's *pattern* (timing, scope, what changed). For each top branch, name one discriminating observation.
- Add an optional "Interactions" line listing pairs of causes that only produce the effect together.
- Add "Measurement / Observation" to the default set, or add a step 0: "confirm the effect is real and correctly measured".

### B3. Inversion

**Works:** the claim-versus-plan boundary with pre-mortem is sharp, "might not hold is a hedge, not an inversion" is a good rule, and the Phase 2 handoff is disciplined.

**Gaps**
- **Steps 3→4 are logically muddled.** Step 3 lists *sufficient* conditions for failure. Step 4 then asks, for each one, "the precondition whose absence would cause it". The precondition you actually want is simply *not-(that failure condition)*. The detour through "absence" produces double negatives and confuses LLM output. The worked example quietly does the simple thing ("tuning load is lower").
- **The output contract requires `## Stress-Test Verdict`** (`inversion.md:125`), but the procedure has no step that produces a verdict or says how to reach one.
- **The worked example breaks the "at least five" rule** (see A4).
- **No ranking.** All unverified preconditions enter Phase 2 with equal weight. The ones that matter are those both *plausible to fail* and *load-bearing*.

**Suggested change**
- Rewrite step 4 as: "For each failure condition, write the precondition the claim silently depends on, which is the negation of that condition."
- Add step 7: "Verdict: the claim **survives** (every load-bearing precondition verified), **survives conditionally** (list the unverified load-bearing ones) or **fails** (a precondition is known false)."
- Tag each precondition `load-bearing: yes/no`.

### B4. Pre-mortem

**Works:** the past-tense framing and the reasoning for it are good, clustering into structural weaknesses is the right move, and the "plan change or accepted risk per cluster" exit criterion is strong.

**Gaps**
- **Nothing calls it** (A1).
- **No likelihood or impact triage.** Every cause is listed raw, and nothing separates probable fatal failures from unlikely ones.
- **No early-warning signals.** Standard pre-mortem practice attaches an early-warning signal ("tripwire") to each accepted risk, so you would know early that this failure is under way. An accepted risk without one is just a label.
- **It hands off to Phase 5 only** (`:109`). Many pre-mortem causes are really unverified assumptions about the plan, and those belong in the Phase 2 table like inversion's output.
- **No output contract**, unlike inversion and trade-off, so the focused `/pre-mortem` output isn't structurally detectable in the same way.
- **The example is trivial** (a dinner party). A software or product example would transfer better to this plugin's real users.

**Suggested change**
- Add "tag each cluster likelihood (H/M/L) × impact (H/M/L); act on H/H first".
- Extend the exit criterion: every accepted risk names a **leading indicator** and the date or threshold at which it will be checked.
- Route "the plan assumed X" causes into Phase 2 as `untested belief` rows.
- Add an output contract (`## Failure Premise`, `## Failure Causes`, `## Structural Weaknesses`, `## Plan Changes & Accepted Risks`).
- Replace the group-dynamics steps (A5).

### B5. Trade-off analysis

**Works:** locking weights before scoring is the right core discipline, and the higher-is-better scale rule, the independence failure mode and the near-tie sensitivity check are all good.

**Gaps**
- **No scoring anchors.** A 1–5 score with no definition of what 1 and 5 mean *for each criterion* is where the arbitrariness sits. Locking weights doesn't help if scores float.
- **The weighted sum is fully compensatory.** A fatal flaw (fails a regulatory requirement, exceeds the budget ceiling) can be outweighed by high scores elsewhere. There's no knock-out or must-have stage.
- **Scores aren't tied to evidence.** Each score is really a claim, but nothing requires it to cite a GT-ID. A score resting on an unverified belief should carry `?` like any other input.
- **Sensitivity only runs on near-ties** (within 10%). The weight-flip question ("how much would weight W have to change for the ranking to flip?") is informative for every result, not just close ones.
- **No option-generation or status-quo step.** "Name the options" takes the user's list as given. "Do nothing" or "defer" is often the real competitor and is never prompted. Dominated options aren't eliminated up front, even though the "when to use" section mentions dominance.
- **Example label mix-up:** the table under "Step 2 — criteria locked" shows weights, which step 3 assigns (`trade-off.md:56-67`).

**Suggested change**
- Step 2b: mark any **must-have** criteria. Options failing one are eliminated before scoring.
- Step 3b: write a one-line anchor for 1 and 5 on each criterion before scoring.
- Step 4: every score cites its evidence (GT-N / GT-N?). A score resting on `GT-N?` caps the resulting chain at MEDIUM.
- Always report the smallest single-weight change that flips the winner.
- Step 1: include the status-quo / do-nothing option unless explicitly excluded, and drop dominated options before scoring.

### B6. Second-order thinking

**Works:** it pairs neatly with inversion, the contradiction check against ground truths is the load-bearing output, the routing back to Phase 2 is well specified, and the depth-stopping rule is sensible.

**Gaps**
- **No actor-response lens.** The most important second-order effects are usually *how other agents react*: competitors respond, users game the metric (Goodhart), incentives shift, feedback loops appear. The procedure asks about "behaviour, system state or context" generically.
- **No time-horizon split.** Short-run and long-run effects often have opposite signs ("worse before better", or the reverse). Nothing prompts a check across time horizons.
- **The procedure contradicts its own failure mode.** The failure mode says to "mark each layer's evidentiary status and downgrade chain confidence" (`second-order.md:105`), but no procedure step does that. It lives only in the failure-mode prose.
- **The contradiction check only looks at ground truths and premises.** An effect that undermines the *goal* in the Essence Statement's success criteria (the change achieves X but defeats the reason X was wanted) is the most decision-relevant contradiction, and it isn't checked.

**Suggested change**
- Step 2: enumerate effects under three lenses: **actors' responses and incentives**, **system state**, and **time (near versus long run)**.
- Step 5: check each effect against the ground truths, the premises **and the Phase 1 success criteria**.
- Add a step: tag each effect `derived` (follows from a GT) or `speculative` (plausible but unevidenced), and cap the chain's confidence accordingly.

### B7. Estimate (Fermi / dimensional analysis). The worked example is wrong

**Works:** the core procedure is excellent: units shown cancelling, first-principles sourcing, the bracket as the deliverable, and a decision-resolution stop criterion.

**The worked example contradicts the technique** (`estimate-detail.md:1-43`). I recomputed it:

| Step in the example | Value | Problem |
|---|---|---|
| Salt energy density: 1.5 kJ/(kg·°C) × 275 °C | 0.115 kWh/kg → 8.7 kg/kWh | correct |
| Salt cost per kWh of *capacity*: 8.7 × $0.60 | $5.2/kWh | correct |
| "Central magnitude": ÷ 10,000 cycles | **$0.00052 per delivered kWh** | a different quantity: per-cycle, per-delivered-kWh |
| "System LCOS $20–50/kWh… The unit-factor product gives the right order of magnitude" | $20–50 | **off by about 38,000× (about 4.6 orders of magnitude)**. $20–50 is *capacity capital cost* (salt $5.2 plus 3–5× for the rest of the system ≈ $21–31), not a levelised per-delivered-kWh cost |
| Bracket built from "typically 3–5× the salt cost" and "confirmed by NREL" | | uses a survey figure and an industry multiplier as the factor value, which is exactly the "analogy as factor value" failure mode (`:49-52`) |
| Decision check against Li-ion at $150–300/kWh | | compares thermal kWh with electrical kWh. At ~41% conversion, $20–50/kWh_th ≈ $49–122/kWh_e. The conclusion happens to survive, but the reasoning doesn't |
| `cycle_life` justified as "(inorganic salt chemistry; definition)" | | a design life is an engineering assumption, not a definition |

The example shows units that don't mean the same thing being compared, an analogy standing in for a first-principles value, a bracket not derived from the factor ranges, and the "Wait —" moment resolved by switching to a looked-up figure rather than fixing the decomposition. A model that learns from this example learns to do all of that.

**Other gaps in the core procedure**
- **Multiplying the extremes of every factor overstates the bracket.** The chance that every factor sits at its extreme at once is small. Standard practice combines ranges in log space (or takes the geometric mean of the bounds), and names the one or two factors that dominate the uncertainty.
- **Decomposition is multiplicative only.** "Sub-quantities that multiply to the target" (`estimate.md:51`) excludes additive structure (capex + opex; sum of components), which is common.
- **No triangulation.** The strongest Fermi check is a second, independent decomposition (for example top-down versus bottom-up). A reference-class figure used only as a *check*, never as a value, is legitimate and currently has no sanctioned place.

**Suggested change**
- Rebuild the example consistently in one unit (capacity capex, $/kWh_th). Take the balance-of-system multiplier as an explicitly flagged `Assumed` factor with a range, then convert to kWh_e before comparing with Li-ion.
- Add: "identify the dominant uncertain factor; combine ranges geometrically, or state that the extremes-product is a worst case".
- Allow additive decomposition.
- Add a triangulation step: a second independent decomposition, or a reference figure explicitly labelled *sanity check only*.

### B8. Theoretical limit. The example uses the loosest bound

**Works:** the "name the law, derive the bound, bracket the gap" structure, separating irreducible headroom from convention-imposed headroom, and "best incumbent is not the ceiling".

**Gaps**
- **The worked example overstates headroom** (`theoretical-limit-detail.md:17-34`). It uses the Carnot limit (63%) against a conventional 40–42% and concludes that "most of this gap is engineering headroom". But Carnot assumes a reversible process running infinitely slowly, at zero power. The endoreversible (Curzon–Ahlborn) efficiency at maximum power for the same temperatures is 1 − √(308/833) ≈ **39%**, so real plants at 40–42% are already at or above the efficiency expected when a plant is run to deliver maximum power. Most of the "21 points of headroom" isn't available at useful output power. The technique has no step asking for the *tightest* applicable bound, so it defaults to the loosest.
- **The example opens with a misapplied law.** Its first computation treats the storage tanks as the Carnot reservoirs (33%). It then notices the conventional figure "exceeds" that and corrects itself. As a teaching example this models the error. The explanation also calls the heat-exchanger ΔT loss the "Carnot penalty", which it isn't; it is a loss from irreversibility.
- **It only covers physics.** The technique requires "the governing physical law". Most of this plugin's domains (software, product, business; see the example set) have hard bounds that aren't physics: speed-of-light latency, Amdahl's law, Little's law and queueing limits, information-theoretic compression bounds, total addressable market, regulatory caps, hours in a day. As written, the technique either fails to apply or pushes the model to force a physics framing.
- **There is no middle tier.** Decisions usually hinge on the *practically achievable* ceiling, such as best demonstrated in a lab or an endoreversible bound, between convention and the ideal limit.

**Suggested change**
- Add a step: "Name every applicable bound and use the **tightest**. State what assumption separates the ideal bound from the practical one (rate, scale, reversibility)."
- Bracket three tiers: ideal limit → practical/demonstrated limit → conventional figure.
- Generalise "governing physical law" to "governing hard constraint (physical, mathematical, informational, or a legal/market cap)", with non-physics examples in the decision rule.
- Rewrite the CSP example to reach the correct Carnot figure in one step and bring in the Curzon–Ahlborn comparison. Add one software example, such as a cross-region latency floor from the speed of light in fibre. The untracked `DEMO-first-principles-multiregion-latency.md` suggests there is already demand for exactly this.

---

## C. Phase 4: Reason Upward

**Works:** it gives deliberate freedom in *how* to reason, requires the reasoning to explain itself, records dead ends in Abandoned Reasoning, bans analogy as evidence, and runs an end-of-phase Assumption Audit (a strong addition).

**Gaps**
1. **"High freedom" conflicts with mandatory techniques.** The phase says prescribing sub-steps "would constrain reasoning", yet exit criterion (3) makes second-order mandatory, and Step 0 says all eight are enumerated here (A2). The model gets two contradictory signals. **Change:** state plainly that second-order is the one mandatory pass and that every other technique is conditional on its own trigger.
2. **Trade-off isn't wired in** (A1). A multi-option recommendation, the most common Phase 4 output, has no instructed procedure.
3. **Hop validity isn't required.** The chain format governs *shape*: one hop per line, heads, arrows. Nothing asks that each hop state *why* it follows (the inference rule, or which GT licenses it). "One inference per hop" (`first-principles.md:173`) is about granularity, not validity. **Change:** "each hop must follow from the previous claim plus the GTs/assumptions it names; a hop that needs an unstated premise gets `[Assumes: X]`". The Assumption Audit mechanism already exists, so this links hop validity to it.
4. **Numbers aren't checked when they're computed.** Estimate and theoretical-limit put numbers into chains, and nothing in Phase 4 or 5 requires re-computing them (B7 shows why this matters). **Change:** any hop that computes a number shows the expression, and Phase 5 recomputes it (D2).
5. **Only one conclusion is ever built.** Phase 4 constructs the answer and never builds the strongest rival. Adding the rival here gives Phase 5 something to test against (D2).
6. **The format text is heavy with parser workarounds.** About a third of the chain-format prose, repeated verbatim in the rubric and the `/reason-upward` stub, describes what "the mechanical form check detects only when…". Those are limitations of the measuring tool, placed in text the model reads while reasoning, and they take attention and turns away from substance. **Change (apparatus-adjacent):** keep the *rules* in the body and move the notes about what the checker can't see to `docs/`, or to one sentence ("the form checker is partial; the rule binds everywhere").

---

## D. Validation: Phase 5 and the Self-Audit Gate

### D1. The gate scores form and bookkeeping, not reasoning

Across the six criteria, the Rigorous descriptors check that artifacts exist, IDs resolve, hop lines are well formed, `[Assumes:]` tokens are present, confidence lines name their causes and §6 claims cite chains. Nowhere does a criterion ask:

- does each hop actually **follow** from its inputs?
- is the **arithmetic** right?
- was a **rival conclusion** considered, and why was it rejected?
- **how sensitive** is the answer to its least-verified ground truth?

Criterion 4 even states its priority outright: "this clause is why the criterion cannot be scored on reasoning quality alone". Form defects cap the score at Sound, but no clause lowers the score of a well-formed chain whose middle hop is a non-sequitur. The demo review's "Checked and cleared" section had to verify 42 numeric claims *by hand*. The gate never asked for it.

**Suggested change: add a semantic limb to Criterion 4** (Rigorous: "every hop's inference is stated and valid; every computed figure is shown and recomputes"; Sound: "one hop needs an unstated premise"; Hand-wavy: "a hop does not follow, or a computed figure is wrong"). It needs no new tooling, because the model scores it the way it already scores the Key-Insight limb of Criterion 6.

### D2. The Phase 5 operation has no method

The operation (`first-principles.md:222`) is: trace each chain, name the weakest link, check whether any `GT-N?` is load-bearing. That's a good start, but it's self-inspection by the author with no adversarial procedure. Suggested method, in order:

1. **Recompute:** re-derive every computed figure in §4 independently of the chain text.
2. **Sensitivity:** for each conclusion, name the single GT or assumption whose falsity would flip it, and say whether it is `?`-marked. A flip-point on a `?` input is the real weakest link, which makes "weakest link" concrete and checkable.
3. **Rival conclusion:** state the strongest alternative answer and the specific GT or chain that rules it out. If nothing rules it out, the conclusion is contingent.
4. **Adversarial technique:** pre-mortem for a plan, inversion of the headline for a claim (A1).
5. **Falsification condition:** "what observation would change this conclusion?" One line per conclusion. It also becomes the natural "verification that would raise confidence" that D-07 already requires on MEDIUM/LOW lines.

Criterion 5's Absent band already fails an analysis where "no weak-link identification… was performed". Steps 2–3 give the bands something observable to score against.

### D3. The confidence model: undefined levels, and an incentive toward HIGH

- **HIGH/MEDIUM/LOW are never defined positively.** The template and rubric define only *caps*: `GT-N?` → ≤ MEDIUM, and a chain ≤ the chains its head cites. Nothing says what HIGH *means* (for example, "every input read at source, every hop deductive or evidenced, no live rival"). Without that, the rating falls back on the model's default optimism.
- **Criterion 5 Rigorous requires HIGH.** It says: "Every claim in the Conclusion section rests on at least one HIGH-confidence chain" (`validation-rubric.md:435`). The text then says MEDIUM is legitimate but "not Rigorous". An agent trying to clear its own gate is therefore rewarded for rating HIGH. The demo review found exactly that: chains rated HIGH while consuming unverified ground truths (P1), and a HIGH decision chain composed of three MEDIUM chains (P2).
- **One grader, grading itself.** The same model scores its own work once, with one re-perception pass. Without a prompt that pushes it adversarially, self-grading tends toward leniency.

**Suggested change**
- Define the three levels positively in `output-template.md`.
- Re-base Criterion 5 Rigorous on **calibration**: "each rating is the highest its inputs and hops license, and no higher". An honest MEDIUM analysis can then be Rigorous. Keep the caps.
- Require each verdict block to **name at least one defect found**, or give a specific reason no defect exists. This counters the lenient self-grading.

### D4. Focused mode has no substantive validation

Focused runs deliberately skip the six-criterion gate and "run a scope-proportionate check" (`first-principles.md:127`). The technique files, though, only give an *exit criterion* (structural completeness). A light semantic check per technique would cost little: for example, "is each cause counterfactually necessary?" for five-whys, "does the bracket's whole width drive the same decision?" for estimate, or "does the winner survive the smallest weight flip?" for trade-off. The mechanics for each already sit in the technique; they just aren't framed as the validation step.

---

## E. Checked and fine

Listed so the absence of a finding here isn't read as the absence of a check.

- **Technique selection and boundaries:** every technique states its nearest neighbour and a decision rule, and there are no gaps or overlaps in the claim / plan / cause / magnitude / bound / options / consequences split.
- **Handoffs into the spine:** fishbone, inversion and second-order route unverified output to Phase 2 and never skip to Phase 3. That's consistent and correct.
- **Five-whys solar example:** the arithmetic checks out (200 W × 5 PSH = 1,000 Wh < 1,200 Wh), and the `?` propagation is correct.
- **Fishbone preset decision table:** reasonable, with a correct default fallback.
- **Phase 3 provenance model** (read-at-source / reported-by-delegate / unverified): the strongest part of the methodology. It is out of scope here apart from noting that the techniques' "direct measurement" anchor should reuse its vocabulary.
- **The bounded re-entry rule** (one re-perception pass) is sound and shouldn't be loosened by any change above.

## F. Implementation notes, for when you decide

- All technique and rubric edits go in `shared/`, followed by `python3 scripts/sync-content.py --write`. The pre-commit sync-drift gate enforces this.
- Changing rubric band wording may affect SCAN-GUARD, HC-BOUND and HARN-01/02 because they assert specific prescription text. Run `bash scripts/check-firewall-battery.sh` after any rubric or `SKILL-body.md` edit.
- Adding output contracts (pre-mortem, B4) touches the BATT-06 header-hit anti-masking constants (`pre-mortem=9`, and so on) that INVARIANT-CHECK asserts. Treat that as a deliberate, recorded change, not a side effect.
- Per the demo review's ordering caution, if you want before/after evidence for D1–D3, capture a baseline run *before* editing the rubric.
