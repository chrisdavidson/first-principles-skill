# First Principles Methodology — Cheat Sheet

One-page orientation to the 5-phase methodology, its artifacts, and its 8+5 skill roster. The
agent body (`first-principles/agents/first-principles.md`, sourced from `shared/spine/SKILL-body.md`)
is the authoritative spec — this page orients, it does not define.

## The artifact chain

**Essence Statement** → **Classified Assumptions Table** → **Ground Truths list** →
**Derivation Chains** → **Signed-off analysis**

Each phase produces the named artifact that is the entry condition for the next phase.

## The five phases

| Phase | What you do | Named artifact | Exit gate |
|---|---|---|---|
| 1. Identify Essence | Strip framing/symptoms to expose the core question and its success criteria | Essence Statement | A skeptic agrees the statement names the real question, not a symptom or proxy |
| 2. Challenge Assumptions | Classify every assumption by type, apply its treatment, record a verdict | Classified Assumptions Table | Every assumption classified, verdicted, and verified or flagged |
| 3. Establish Ground Truths | Compile facts that pass the irreducibility test; assign stable GT-IDs | Ground Truths list | All ground truths have IDs, citations or `?` flags, and pass irreducibility |
| 4. Reason Upward | Build derivation chains from ground truths toward an answer | Derivation Chains | Question answered, every conclusion chained, second-order pass applied and non-contradicting |
| 5. Validate | Stress-test each chain, find weak links, apply the validation rubric | Signed-off analysis | Every conclusion traces to a ground truth; every weak link resolved or caveated |

## Mode selection (Step 0)

A technique-specific trigger phrase (e.g. "root cause", "trade-off analysis", "theoretical
limit") routes to a focused single-technique analysis that still runs all five phases but only
enumerates that one technique in Phase 4. Otherwise `full-composer` mode runs all five phases
with all eight companion techniques enumerated in Phase 4.

## Assumption types & treatments

| Type | Prescribed treatment |
|---|---|
| physical law | Accept as a ground-truth candidate — does not expire, cannot be negotiated away |
| current constraint | Record the expiry conditions — what would have to change for it to lift |
| convention | Explicitly challenge before use — historical inertia or genuine fit? |
| untested belief | Verify, or flag `GT-N?: unverified`; any dependent conclusion inherits a confidence caveat |

## Derivation chain format

```text
GT-N + GT-M → [intermediate claim] → [conclusion]
```

At least one intermediate step is required — a chain that jumps straight from GT-IDs to a
conclusion is a flat list, not a derivation. `GT-N?` marks an unverified input; any conclusion
depending on it inherits a MEDIUM or LOW confidence rating.

## Companion techniques (8)

| Technique | Phase | Use when | Slash command |
|---|---|---|---|
| Five Whys | Phase 3 | Causal depth ("why does this recur?") or reduce-to-primitives definitional/physical reduction | `/first-principles:five-whys` |
| Fishbone | Phase 2 | Breadth-first cause categories when the assumption space is multi-causal | `/first-principles:fishbone` |
| Inversion | Phase 2 | What would guarantee failure — a conclusion feels too clean | `/first-principles:inversion` |
| Pre-mortem | Phase 5 | Imagine it already failed and work backward to find weak links | `/first-principles:pre-mortem` |
| Trade-off | Phase 4 | Weighted-criteria scoring over surviving options | `/first-principles:trade-off` |
| Second-Order | Phase 4 | 2nd/3rd-order consequences before the Phase 5 handoff | `/first-principles:second-order` |
| Estimate | Phase 4 | Fermi/dimensional-analysis magnitude rebuild with explicit bounds | `/first-principles:estimate` |
| Theoretical Limit | Phase 4 | The law-permitted ceiling once conventions are stripped | `/first-principles:theoretical-limit` |

## Focused-phase skills (5)

Slash-only stubs invoking a single phase directly: `identify-essence`, `challenge-assumptions`,
`ground-truths`, `reason-upward`, `validate` (e.g. `/first-principles:reason-upward`).

## Running the whole methodology

`/first-principles-analysis <problem>` — the launcher. It dispatches the composer agent
explicitly, which is the reliable way to reach it: automatic delegation fired on roughly one
prompt in seventeen when measured on 2026-07-27
(`dispatch-attribution-findings.md`). The methodology is
unchanged; only the route to it differs.

## Output document

Six fixed sections, in order: Problem Essence, Assumptions Table, Ground Truths, Derivation
Chains, Abandoned Reasoning, Conclusion. Honest-depth escape valve: a section with no genuine
content is marked `Nothing material here — [reason]`, never padded.

## Invoking

`@agent-first-principles:first-principles` or `/first-principles:first-principles`. For install
instructions see [GETTING-STARTED.md](GETTING-STARTED.md).
