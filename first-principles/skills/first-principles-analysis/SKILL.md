---
name: first-principles-analysis
description: Runs the full five-phase first-principles analysis. Slash-only.
disable-model-invocation: true
metadata:
  version: "8.25.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/first-principles-analysis/SKILL.md by sync-content.py -->

# Full First-Principles Analysis — Launcher

You are running the composer launcher. Your job is **not** to perform the analysis
yourself. Your job is to hand it to the `first-principles:first-principles` agent and
return what that agent produces.

## Procedure

1. **Collect the problem statement.** Take everything the user supplied after the slash
   command as the problem. If they supplied nothing, ask for the one thing the agent
   cannot start without — a one-sentence statement of the question or decision to be
   analysed — and stop until you have it.

2. **Dispatch the agent.** Invoke the `first-principles:first-principles` agent via the
   Task tool. Pass through, verbatim:
   - the problem statement,
   - the domain, if the user named one,
   - any constraints the user stated,
   - the paths to any files or directories the user pointed at.

3. **Return the agent's analysis.** Present what the agent produced. Do not summarise it
   down to a verdict, and do not re-run any phase yourself.

## Do not analyse inline

Even if the problem looks small enough to answer directly, delegate it. Answering inline
is the exact failure this launcher exists to prevent: it produces well-written prose that
is not a first-principles analysis — no assumptions table, no derivation chains, no
confidence ratings, and nothing the validation rubric can score.

## Why this launcher exists

Automatic delegation to the composer agent is unreliable. Measured on 2026-07-27, the
agent was reached on roughly one in seventeen prompts explicitly built from its own
documented trigger phrases, while explicit dispatch through the Task tool succeeded. This
command converts an unreliable implicit route into a deliberate one.

The agent itself is unaffected and remains the single source of truth for the
methodology — this launcher adds a reliable way to reach it, and changes nothing about
what it does once reached.

## If the dispatch fails

If the agent cannot be dispatched — it is not installed, or the Task tool returns an
error — say so plainly and stop. Do not silently fall back to analysing the problem
yourself: a first-principles analysis that never ran is a result the user needs to know
about, and prose that resembles one is worse than an honest failure.

To reach the individual techniques instead, the focused slash commands remain available:
`/five-whys`, `/fishbone`, `/inversion`, `/pre-mortem`, `/trade-off`, `/second-order`,
`/estimate`, `/theoretical-limit`, and the five phase commands `/identify-essence`,
`/challenge-assumptions`, `/ground-truths`, `/reason-upward`, `/validate`.
