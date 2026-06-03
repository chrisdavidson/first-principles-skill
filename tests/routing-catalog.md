# Routing Catalog (v3.13)

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

**Pass thresholds:** P-cases ≥ 11/13 DELEGATE **AND** N-cases ≥ 18/20 NO-DELEGATE.

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
| P3 | "Help me reason from ground truth about why a hot cup of coffee cools faster in its first ten minutes than in its second — what do we actually know is true?" | DELEGATE | "reason from ground truth" | Self-contained (science domain); natural mid-sentence embedding of trigger phrase per D-03 structural fix (v3.4 baseline: 0/3 — command-label-plus-colon framing suppressed delegation) |
| P4 | "Decompose this problem into its foundations: why do most independent restaurants fail within the first year?" | DELEGATE | "decompose this problem" | Self-contained (business domain); direct literal trigger phrase match |
| P5 | "Stress-test the reasoning behind the claim that raising the minimum wage always reduces total employment. Are there hidden assumptions?" | DELEGATE | "stress-test reasoning" | Self-contained (business/economics domain); explicit "stress-test reasoning" trigger phrase in description |
| P6 | "Question the design of standard 40-hour work weeks from first principles. Is the structure actually optimal, or just inherited?" | DELEGATE | "question a design" + "first principles" | Self-contained (business/personal domain); matches both "question a design" and "first principles" triggers |
| P7 | "What are the fundamental ground truths about why human memory degrades over time? Reason up from them to evaluate whether spaced repetition really works." | DELEGATE | "fundamental ground truths" + "reason up from first principles" | Self-contained (science domain); v3.4 baseline 1/3 — vocabulary gap: description lacked plural noun "fundamental ground truths" and particle-verb "Reason up from them"; closed by FRAG-03 description fix adding both paraphrases (Plan 01) |
| P8 | "Help me reason from the ground up about why the modern smartphone landed on this particular form factor — what do we actually know is true about why this shape and size won out?" | DELEGATE | "reason from the ground up" + "what do we actually know is true" | Self-contained (software/business domain); mid-sentence Task-delegation trigger "reason from the ground up" with epistemic anchor; (v3.8 baseline: 0/3 main + 2/5 disambig — Skill-vs-Task routing confusion: "Decompose this problem" triggered Skill invocation rather than Task delegation; Signal A blindspot; fixed in v3.9 by prompt rewrite removing bare command-label form; post-fix: 2/3 PASS) |
| P9 | "Help me reason from ground truth about why dissolving table salt in water lowers the freezing point — what do we actually know is true about the underlying mechanism?" | DELEGATE | "reason from ground truth" | Self-contained (science / chemistry domain); natural mid-sentence embedding of trigger phrase; colligative-properties substance requires reasoning from primitives, not lookup; chemistry discipline (new in v3.6) |
| P10 | "What are the fundamental ground truths about why the deep ocean stays cold even directly under the equator? Reason up from them to evaluate whether thermohaline circulation alone explains it." | DELEGATE | "fundamental ground truths" + "reason up from first principles" | Self-contained (science / earth-science domain); multi-trigger annotation mirrors P7 form; requires reasoning from first principles about ocean thermodynamics, not factual lookup; earth-science discipline (new in v3.6) |
| P11 | "I want to challenge the assumptions embedded in how modern universities assign academic credit hours — can you map out the distinct categories of assumptions baked into that model and evaluate whether each one actually holds?" | DELEGATE | "challenge assumptions" | Self-contained (education domain); "challenge assumptions" trigger in natural mid-sentence embedding; framing asks for assumption-taxonomy (categorize + evaluate) rather than a single-assumption refutation — cleanly DELEGATE |
| P12 | "Help me analyze from first principles whether first-principles reasoning itself is a reliable method — what fundamental assumptions does the approach rest on, and do they actually hold under scrutiny?" | DELEGATE | "analyze from first principles" | Self-contained (methodology / meta domain); "analyze from first principles" trigger in natural mid-sentence embedding; self-application framing: the method is applied to an evaluation of itself; cleanly DELEGATE |
| P13 | "I want to reason from ground truth about why antibiotics stop working against bacteria that were once sensitive to them — what do we actually know is true about the underlying biological mechanism?" | DELEGATE | "reason from ground truth" | Self-contained (biology / medicine domain); "reason from ground truth" trigger in natural mid-sentence embedding; worked-examples-domain framing: biology/medicine is a distinct discipline not yet represented in the P-table; requires causal reasoning from first principles, not clinical lookup — cleanly DELEGATE |

---

## Negative Cases — Expected Verdict: NO-DELEGATE

The agent should NOT be invoked for these off-topic prompts. The scope line in the
description (v3.1) reads: *"Not for routine code review, debugging, performance
optimization, or general Q&A."*

N1-N10 are carried verbatim from Phase 25 v2. N11-N15 are new in Phase 30 (v3.1). N16-N17 are new in Phase 39 (v3.6).

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

### Science Lookup Class (new in v3.6)

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N16 | "What's the formula for calculating the freezing-point depression of a 5% NaCl solution?" | NO-DELEGATE | Science formula/homework lookup | Factual formula recall — general Q&A; excluded by the "general Q&A" scope-exclusion clause in shared/spine/SKILL.meta.yml. Domain: chemistry (paired with P9). |
| N17 | "How deep is the average ocean thermocline, and which latitudes have the steepest gradient?" | NO-DELEGATE | Science factual lookup | Factual lookup question — general Q&A; excluded by the "general Q&A" scope-exclusion clause in shared/spine/SKILL.meta.yml. Domain: earth-science (paired with P10). |

### Assumption-Taxonomy Boundary Class (new in v3.13)

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N18 | "What are the main categories of cognitive biases that affect human decision-making?" | NO-DELEGATE | Taxonomy / classification request | Enumeration request about a cognitive-science taxonomy — general Q&A; no first-principles framing, no trigger phrase from the description; excluded by the "general Q&A" scope-exclusion clause in shared/spine/SKILL.meta.yml. Paired with P11 (assumption-taxonomy boundary). |

### Self-Application Boundary Class (new in v3.13)

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N19 | "What is first-principles reasoning and how does it differ from analogical thinking?" | NO-DELEGATE | Methodology explanation | Factual explanation request about a reasoning methodology — general Q&A; no analytical trigger framing; asking "what is" not "analyze / challenge / reason from ground truth"; excluded by the "general Q&A" scope-exclusion clause in shared/spine/SKILL.meta.yml. Paired with P12 (self-application boundary). |

### Medical / Clinical Lookup Class (new in v3.13)

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N20 | "What antibiotic classes are typically used to treat MRSA infections?" | NO-DELEGATE | Medical / clinical lookup | Clinical factual lookup in the same domain (medicine/biology) as P13 — general Q&A; no causal or first-principles framing; asking for a clinical answer, not an underlying mechanism; excluded by the "general Q&A" scope-exclusion clause in shared/spine/SKILL.meta.yml. Paired with P13 (worked-examples-domain boundary). |

---

## Catalog History

### v3.13 (Phase 55) — 2026-06-03

Extended the v3.9/v3.6 catalog with three new framing-coverage P-prompts and paired N-prompts, and rescaled battery thresholds proportionally.

- **P11 (TAX-01)**: Education-domain (academic credit hours) assumption-taxonomy framing. Domain: education (new). Trigger Phrase Matched: `"challenge assumptions"`. Framing: assumption-taxonomy — asks to map distinct categories of assumptions and evaluate each; "challenge assumptions" drawn from existing description vocabulary (no description edit required).
- **P12 (META-01)**: Methodology-domain self-application framing. Domain: methodology / meta. Trigger Phrase Matched: `"analyze from first principles"`. Framing: self-application — the first-principles method applied to evaluating the reliability of itself; "analyze from first principles" drawn from existing description vocabulary.
- **P13 (WKEX-01)**: Biology/medicine-domain worked-examples-domain framing. Domain: biology / medicine (new). Trigger Phrase Matched: `"reason from ground truth"`. Framing: worked-examples-domain — causal mechanism question suitable for a worked example; mirrors P3/P9 mid-sentence embedding form; "reason from ground truth" drawn from existing description vocabulary.
- **N18 / N19 / N20 (TAX-02, META-02, WKEX-02)**: Paired negative controls. N18 Off-Topic Class: `Taxonomy / classification request` (education/cognitive-science, paired with P11). N19 Off-Topic Class: `Methodology explanation` (meta domain, paired with P12). N20 Off-Topic Class: `Medical / clinical lookup` (biology/medicine, paired with P13). All three Rationales cite the existing `"general Q&A"` scope-exclusion clause in `shared/spine/SKILL.meta.yml`. Three new H3 sections added under the N-section.
- **Threshold rescale (INFRA-01/INFRA-02)**: Battery thresholds rescaled to P ≥ 11/13 DELEGATE and N ≥ 18/20 NO-DELEGATE (applied in Plan 55-02). Rationale: proportional scaling from the v3.1 Key Decision (tolerate single-prompt non-determinism) — P-side 11/13 ≈ 84.6% (nearest integer preserving ~1-flip tolerance for 13 prompts); N-side 18/20 = 90% (2-flip tolerance, consistent with v3.6 precedent).
- **Description budget constraint**: Description is at 1977/2000 chars — no description edits made. All trigger phrases for P11/P12/P13 drawn from existing description vocabulary.

P-prompts P1-P10 are unchanged. N-prompts N1-N17 are unchanged.

### v3.9 (Phase 47) — 2026-05-29

Fixed P8 Skill-vs-Task routing confusion:

- **P8 prompt rewrite (P8-03)**: replaced bare "Decompose this problem:" command-label framing with mid-sentence first-principles question leading with "Help me reason from the ground up"; smartphone form-factor topic and epistemic anchor ("what do we actually know is true") preserved. v3.8 baseline evidence: P8 0/3 main + 2/5 disambig — "Decompose this problem" triggered Skill(skill: "first-principles:first-principles") invocation rather than Task delegation; Signal A (which only detects Task tool_use) produced false NO-DELEGATE scores. Post-fix: 2/3 PASS under --repeat 3 --min-pass 2.
- **N-side regression check (P8-04)**: full 17 N-cases re-run; result: N 17/17. No regressions introduced.

P-prompts P1-P7, P9-P10 are unchanged. N-prompts N1-N17 are unchanged.

### v3.6 (Phase 39) — 2026-05-25

Extended the v3.5 catalog with two new science-domain P-prompts and paired N-prompts, and rescaled battery thresholds proportionally.

- **P9 (CAT-01, CAT-02, CAT-03)**: Chemistry (colligative properties) first-principles question in mid-sentence trigger embedding form. Domain: science / chemistry. Trigger Phrase Matched: `"reason from ground truth"`. Adds chemistry to the distinct-disciplines count (previously physics-thermodynamics + neuroscience from P3/P7). Rationale: colligative-property mechanism question requires reasoning about underlying intermolecular physics, not formula recall — cleanly DELEGATE.
- **P10 (CAT-01, CAT-02, CAT-03)**: Earth-science (thermohaline circulation / deep-ocean thermodynamics) first-principles question in mid-sentence trigger embedding form. Domain: science / earth-science. Trigger Phrase Matched: `"fundamental ground truths" + "reason up from first principles"`. Rationale: multi-trigger annotation mirrors P7 form; thermohaline question requires causal first-principles reasoning, not factual lookup.
- **N16 / N17 (CAT-04, CAT-05)**: Paired science-domain N-prompts covering the same disciplines as P9 / P10. N16 Off-Topic Class: `Science formula/homework lookup` (chemistry, paired with P9). N17 Off-Topic Class: `Science factual lookup` (earth-science, paired with P10). Both Rationales cite the existing `"general Q&A"` scope-exclusion clause in `shared/spine/SKILL.meta.yml`. New H3 section `### Science Lookup Class (new in v3.6)` added under the N-section.
- **Threshold rescale (CAT-06)**: Battery thresholds rescaled to P ≥ 8/10 DELEGATE and N ≥ 15/17 NO-DELEGATE. Rationale: the v3.1 Key Decision states that routing battery thresholds are designed to "tolerate single-prompt non-determinism" — CAT-06's literal example of N ≥ 15/17 deliberately widens from strict single-flip tolerance (which would be N ≥ 16/17) to 2-flip tolerance, absorbing the ±3 P-prompt same-session noise floor documented in v3.4/v3.5; this widening is intentional and consistent with the spirit of the v3.1 principle even though the denominator math shifts from 1-flip to 2-flip. The N-side now tolerates 2 flips (15/17 = 88.2%); P-side maintains near-80% pass rate (8/10), closest integer cutoff preserving single-flip tolerance for 10 prompts. `check-routing.py` defaults updated; catalog header line updated in lockstep.
- **Description update (CAT-05)**: None — both N16 and N17 Rationales cite the existing `"general Q&A"` clause in `shared/spine/SKILL.meta.yml`; the four locked `_REQUIRED_PHRASES` are unchanged.

P-prompts P1-P8 are unchanged. N-prompts N1-N15 are unchanged.

### v3.5 (Phase 37) — 2026-05-25

Fixed P3 structural embedding defect and updated P3/P7 annotations with v3.4 root-cause evidence:

- **P3 prompt rewrite (FRAG-05)**: replaced command-label-plus-colon framing ("Reason from ground truth: why…") with natural mid-sentence trigger embedding ("Help me reason from ground truth about why…"); Newton's law of cooling / coffee cooling substance preserved. v3.4 baseline evidence: P3 0/3 — the bare label-plus-colon construction suppressed delegation in all three runs (structural defect per D-03).
- **P7 annotation update (FRAG-06)**: updated "Trigger Phrase Matched" to "fundamental ground truths" + "reason up from first principles" and expanded Rationale to cite the v3.4 1/3 pass rate and vocabulary gap root cause: description lacked plural noun "fundamental ground truths" and particle-verb "Reason up from them"; closed by FRAG-03 description fix (Plan 01) which appended both paraphrases to the agent description.

P-prompts P1-P2, P4-P8 are unchanged. N-prompts N1-N15 are unchanged.

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
