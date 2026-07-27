# Dispatch attribution — Phase 1a runtime control

> Executes task **1a** of [dispatch-remediation-plan.md](dispatch-remediation-plan.md)
> (`DISPATCH-01`). Its evidence base is [real-use-dispatch-findings.md](real-use-dispatch-findings.md).
> Tasks 1b (historical per-tag bisect) and 1c (P12 discriminator ladder) are **not** executed here;
> see *Consequences* for why 1b is now expected to be uninformative.

## Verdict — `RUNTIME-WIDE`

**Auto-delegation to plugin agents is near-totally suppressed in this runtime. The defect is not
specific to the first-principles agent, and no change to this repository can fix it.**

Applying the decision rule pre-registered in the quick-task plan before any measurement was taken:

| Arm | Prompts | Dispatches | Result |
|---|---:|---:|---|
| Control agent (`mealplan-control:meal-planner`) | 3 | **0** | `c = 0` |
| Paired reference (first-principles P1) | 1 | **0** | `f = 0` |

`c = 0` → **`RUNTIME-WIDE`**.

## The refinement that matters — "near-totally", not "entirely"

The routing battery run roughly two hours earlier scored P **1/13**: prompt **P12** *did* dispatch.
So across every dispatch opportunity observed today — 13 battery P-prompts, 3 control prompts, and
1 paired reference, **17 in total** — exactly **one** produced a `Task` call.

Delegation is therefore **not disabled outright**. The mechanism can still fire. It is suppressed
to roughly 1-in-17 on prompts explicitly constructed to trigger it. This record states the verdict
that way deliberately: "auto-delegation is broken" would be a stronger and less accurate claim than
the evidence supports, and the single P12 dispatch is the reason.

## Why this is delegation specifically, not tool use generally

Every capture in this control returned `turns = 1` with no tool use at all, which on its own would
be consistent with a runtime where tool calling is broken generally. It is not.

The headless re-run recorded in the findings document, issued in the same session window, made
**27 tool calls** — Bash, Read, WebFetch, WebSearch, ToolSearch — and **zero `Task` calls**. Tool
invocation works normally. What does not fire is agent dispatch.

## Validity checks

Each of these was checked because its failure would have invalidated the control:

- **The control agent was loaded.** `mealplan-control:meal-planner` appears in the `system/init`
  agent roster of all three control captures. A non-dispatch by an unloaded agent would prove
  nothing.
- **The control task is non-trivial.** A seven-day meal plan with an aisle-grouped shopping list is
  substantial enough that delegating is the obviously correct behaviour. Had the control task been
  something answerable in one line, a non-dispatch would have been ambiguous between "delegation is
  broken" and "too trivial to hand off". All three sessions instead produced full meal plans inline.
- **The control description is directive, matching the first-principles agent's own shape** —
  `ALWAYS delegate to the meal-planner agent when the user asks to…`, plus an explicit
  `Do not build the meal plan inline for these`. The two agents were compared on equal terms.
- **The domain does not overlap** with first-principles analysis, so a dispatch could not have been
  mis-attributed.
- **Dispatches were counted by structured parse, not string grep.** A raw scan of these captures
  returns false positives — `"Task"` and `"tool_use"` both appear inside system and hook events.
  This was an actual error made and caught earlier in the investigation, and the plan pre-registered
  the parse requirement because of it.
- **The reference arm was run in the same session window**, so the control result cannot be
  confused with a runtime change between the battery run and now. P1 failing again also confirms
  the battery's P-arm result is reproducing rather than being a one-off.

## Consequences for the remediation plan

- **Phases 2a, 2b and 3 are void.** They assume a repository-side cause — an in-repo regression or
  a description shape. Neither can explain a control agent in an unrelated domain failing to route.
- **Phase 1b (historical per-tag bisect) is now expected to be uninformative** and should not be
  run as planned. It would test old first-principles versions against the *current* runtime; since
  the current runtime does not dispatch a freshly-authored control agent either, every tag will
  score near-zero and the result will say nothing about which tag introduced anything. Running it
  would consume ~200 live invocations to confirm a foregone conclusion.
- **Phase 1c (P12 discriminator ladder) changes character but retains value.** P12 is now the only
  known dispatch in 17 opportunities. Understanding what is different about it is no longer a route
  to fixing the description — it is the one available probe into what still gets through.
- **Phase 4 becomes the entire remedy, not a belt-and-braces addition.** The agent needs an
  invocation path that does not depend on model-mediated routing. Its open design question —
  whether the new entry point should be `disable-model-invocation: true` — is now settled in the
  affirmative by this verdict: a model-invocable entry point would inherit the same failure.
- **Phase 5 (documentation of the version-pinned install surface) is unaffected** and still stands.

## Follow-up: explicit dispatch works, and Phase 4 is built

Tested after this verdict was recorded, and it narrows the finding usefully: **explicit dispatch
succeeds.** A prompt instructing the session to invoke the agent through the Task tool returned
`subagent_type=first-principles:first-principles` and a full analysis. What is suppressed is
*implicit auto-routing* only — the agent itself is fully functional and reachable when asked for
by name.

Phase 4 (`DISPATCH-05`) is therefore implemented as a thin launcher,
`/first-principles-analysis`, which dispatches the agent explicitly rather than duplicating the
methodology. Verified end-to-end: the slash command dispatched the agent and returned all six
canonical output sections in order, and the D-18 detector parses the result instead of raising
`SectionResolutionError` — the first output from this path it has been able to score.

**That open item is now resolved — the detector was wrong.** On the launcher's output the detector
flagged 16/16 verdict cells nonconforming and 4/4 chain blocks malformed. Investigated
2026-07-27: `_verdict_conforms` is **inverted** relative to the output template and the validation
rubric, passing the bare token both name as a defect and failing the prescribed
`Accept — justification` form; and `_chain_block_well_formed` matches per physical line, so the
template's own canonical worked example fails the detector built to check conformance to it. The
agent's output was conformant throughout. Scope and consequences — including the affected
published v8.7 figures — are in [detector-contract-fix-plan.md](detector-contract-fix-plan.md).

## Limitations

- **n = 3 on the control**, one session window, one machine, one runtime version. The rule
  pre-registered `c = 0` as decisive at this n, which is defensible for a signal this
  unambiguous, but it remains three prompts.
- **No mechanism is established.** This record shows *that* dispatch does not fire. It does not
  show why, and it cannot distinguish an intentional platform change from a defect. No experiment
  runnable from inside this repository can make that distinction.
- **Nothing here establishes permanence.** The suppression is observed on one date. It may lift
  without notice, which is itself an argument for Phase 4 — a path whose reliability does not
  depend on the answer.
- **The P12 exception remains unexplained**, and this record does not attempt to explain it.

## Provenance

- Control plugin: a throwaway single-agent plugin authored under `/tmp`, validated with
  `claude plugin validate`, never committed and containing nothing derived from this repository.
- Transport: `claude -p --output-format stream-json --verbose --plugin-dir <path>`, one invocation
  per prompt, `--permission-mode bypassPermissions` so headless runs did not stall on prompts.
- Captures and the counting script live under `/tmp` and are not committed. The counts above are
  reproducible from them only on the machine that ran them; this record carries the figures a
  reader can check against its own reasoning, not the raw sessions.
- No change to `shared/`, the generated tree, or any gate was made by this task.
