# Routing Catalog (v3.1)

**Status:** Committed repo fixture. Consumed by `scripts/check-routing.py --catalog tests/routing-catalog.md`.

**Purpose:** This catalog measures the `first-principles:first-principles` agent's routing
behavior in a live Claude Code session. Each prompt is paired with its expected routing
verdict. **P-cases** expect `DELEGATE` (the agent should auto-invoke). **N-cases** expect
`NO-DELEGATE` (the agent should not be invoked — the prompt is off-topic for first-principles
analysis and should be handled by the main session or another agent).

**Non-determinism note:** Routing is non-deterministic — outcomes vary between sessions,
plugin sets, and Claude routing-model versions. This catalog documents *expected* behavior
measured against thresholds (not per-prompt exactness). A single mis-route does not fail
the battery; the **threshold counts** are the pass criterion.

**Pass thresholds:** P-cases ≥ 6/8 DELEGATE **AND** N-cases ≥ 14/15 NO-DELEGATE.

**History:** Extended from
`.planning/milestones/v3.0-phases/25-agent-description-and-frontmatter-hardening/25-DELEGATION-TESTS.md`
(Phase 25 v2 / Phase 29). New N-prompts added in Phase 30 (v3.1) to broaden negative
coverage across five previously-uncovered or thinly-covered off-topic classes
(refactoring, syntax/typo, performance debugging variants beyond N6, configuration /
how-to, library API). The new N-prompts deliberately touch description-adjacent words
("performance", "optimize", "design") to stress-test the v3.1 scope-line tightening.

---

## Positive Cases — Expected Verdict: DELEGATE

The agent `first-principles:first-principles` should auto-delegate when these prompts
are issued. All eight prompts are carried verbatim from Phase 25 v2 / Phase 29.

| # | Prompt | Expected Routing | Trigger Phrase Matched | Rationale |
|---|--------|-----------------|----------------------|-----------|
| P1 | "Analyze from first principles why most New Year's resolutions fail by February. What are the fundamental drivers, not the surface symptoms?" | DELEGATE | "first principles" | Self-contained (personal domain); literal "first principles" trigger; asks for fundamental decomposition |
| P2 | "Challenge the assumptions behind the claim that working from home reduces productivity. Are they actually valid?" | DELEGATE | "challenge assumptions" | Self-contained (business domain); direct literal trigger phrase match |
| P3 | "Reason from ground truth: why does a hot cup of coffee cool faster on its first ten minutes than its second ten minutes? What do we actually know is true here?" | DELEGATE | "reason from ground truth" | Self-contained (science domain); literal trigger phrase plus explicit ground-truth framing |
| P4 | "Decompose this problem into its foundations: why do most independent restaurants fail within the first year?" | DELEGATE | "decompose this problem" | Self-contained (business domain); direct literal trigger phrase match |
| P5 | "Stress-test the reasoning behind the claim that raising the minimum wage always reduces total employment. Are there hidden assumptions?" | DELEGATE | "stress-test reasoning" | Self-contained (business/economics domain); explicit "stress-test reasoning" trigger phrase in description |
| P6 | "Question the design of standard 40-hour work weeks from first principles. Is the structure actually optimal, or just inherited?" | DELEGATE | "question a design" + "first principles" | Self-contained (business/personal domain); matches both "question a design" and "first principles" triggers |
| P7 | "What are the fundamental ground truths about why human memory degrades over time? Reason up from them to evaluate whether spaced repetition really works." | DELEGATE | "reason from ground truth" | Self-contained (science domain); paraphrase of "reason from ground truth" with explicit ground-truth framing |
| P8 | "Take the modern smartphone form factor apart from the ground up. Decompose this problem: what do we actually know is true about why this shape and size won?" | DELEGATE | "decompose this problem" | Self-contained (software/business domain); literal "decompose this problem" trigger with from-the-ground-up framing |

---

## Negative Cases — Expected Verdict: NO-DELEGATE

The agent should NOT be invoked for these off-topic prompts. The scope line in the
description (v3.1) reads: *"Not for routine code review, debugging, performance
optimization, or general Q&A."*

N1-N10 are carried verbatim from Phase 25 v2. N11-N15 are new in Phase 30 (v3.1).

### Code Review Class

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N1 | "Review this PR for style issues and naming conventions." | NO-DELEGATE | Code review | Routine code review — explicitly excluded by scope line |
| N2 | "Can you check this function for best practices and suggest improvements?" | NO-DELEGATE | Code review | Code quality review — not a first-principles analysis request |
| N3 | "Look over this TypeScript file and flag any issues you see." | NO-DELEGATE | Code review | General code review scan — no first-principles framing |

### Debugging Class

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N4 | "Find the bug in this stack trace. The app crashes on startup." | NO-DELEGATE | Debugging | Explicit debugging request — excluded by scope line |
| N5 | "My tests are failing. Can you help me figure out why this assertion is wrong?" | NO-DELEGATE | Debugging | Test failure diagnosis — routine debugging, no first-principles framing |
| N6 | "Why is this SQL query slow? Help me debug the performance issue." | NO-DELEGATE | Debugging | Performance debugging — explicitly excluded by v3.1 scope line ("performance optimization") |

### General Q&A / Analysis Class

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N7 | "Summarize this article about Kubernetes for me." | NO-DELEGATE | General Q&A | Summary task — general Q&A, no analytical framing |
| N8 | "What's the difference between REST and GraphQL?" | NO-DELEGATE | General Q&A | Informational question — no first-principles or assumption-challenging framing |
| N9 | "Write a regex to match email addresses." | NO-DELEGATE | General Q&A | Task execution request — no analytical or first-principles framing |
| N10 | "How do I configure nginx as a reverse proxy?" | NO-DELEGATE | General Q&A | Factual how-to question — general Q&A, not delegated |

### Refactoring Class (new in v3.1)

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N11 | "Suggest how to refactor this function for readability." | NO-DELEGATE | Refactoring | Routine refactor suggestion — not a first-principles analysis; no trigger phrases |

### Syntax / Typo Help Class (new in v3.1)

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N12 | "Why doesn't this Python list comprehension compile?" | NO-DELEGATE | Syntax/typo | Syntax help — narrow technical question, not first-principles framing |

### Performance Debugging Variants Class (new in v3.1)

This class deliberately touches the word "performance" — it stress-tests the v3.1
scope-line tightening beyond N6.

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N13 | "My Redis cache hit rate dropped from 95% to 60% — what should I check?" | NO-DELEGATE | Performance debugging | Performance debugging variant — touches "performance" but is off-topic; v3.1 scope-line should hold |

### Configuration / How-To Class (new in v3.1)

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N14 | "How do I set up CORS in Express?" | NO-DELEGATE | Config/how-to | Factual how-to / configuration question — general Q&A, not first-principles |

### Library API Class (new in v3.1)

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N15 | "What does the second argument to `Array.prototype.reduce` do?" | NO-DELEGATE | Library API | API lookup question — informational, not first-principles framing |

---

## Catalog History

### v3.1 (Phase 30) — 2026-05-23

Extended the Phase 25 v2 catalog with 5 new N-classes:

- **Refactoring** (N11)
- **Syntax / typo help** (N12)
- **Performance debugging variants** (N13) — deliberately touches "performance" to
  stress-test the 30-01 scope-line tightening beyond N6
- **Configuration / how-to** (N14)
- **Library API** (N15)

P-prompts (P1-P8) are unchanged from Phase 25 v2. N1-N10 are unchanged. Final shape:
**8 P + 15 N = 23 prompts.**

Pass thresholds (v3.1): P ≥ 6/8 DELEGATE **AND** N ≥ 14/15 NO-DELEGATE.

### v2 (Phase 29) — 2026-05-23

Replaced all 8 P-prompts with self-contained, context-independent equivalents spanning
the four target domains (software, business, science, personal). N-prompts unchanged
from v1. See
`.planning/milestones/v3.0-phases/25-agent-description-and-frontmatter-hardening/25-DELEGATION-TESTS.md`.

### v1 (Phase 25) — 2026-05-22

Initial catalog. Used project-context-dependent P-prompts.

---

## See Also

- `tests/routing-baseline-v3.4.md` — v3.4 canonical best-of-3 baseline (P 6/8, N 15/15, recorded 2026-05-25)
- `.planning/milestones/v3.0-phases/25-agent-description-and-frontmatter-hardening/25-DELEGATION-TESTS.md` — source of P1-P8 (v2) and N1-N10
- `.planning/phases/30-routing-quality-patch/30-CONTEXT.md` — D-15 / D-16 / D-17 decisions driving v3.1
- `scripts/check-routing.py` — battery harness that consumes this catalog
- `shared/spine/SKILL.meta.yml` — source of the v3.1 scope-line tightening (regenerated into `first-principles/agents/first-principles.md`)
