# Feature Research

**Domain:** Structured-reasoning / methodology Claude Code skill (pure Markdown)
**Researched:** 2026-05-16
**Confidence:** HIGH (skill-authoring guidance from official Anthropic docs; reasoning-tool guidance from established practitioner sources, multiple corroborating)

## Context

This skill is a methodology skill, not a code/automation skill. The "features" are not
runtime capabilities — they are content-and-structure properties of a Markdown skill that
make Claude reason better when the skill loads. The relevant feature landscape is therefore
two-layered:

1. **Skill-mechanics features** — what every well-authored Claude Code skill must have
   (frontmatter, triggers, progressive disclosure, conciseness). Largely table stakes.
2. **Methodology-content features** — what makes the *reasoning instruction* itself good
   (rigor, examples, rubric, companion tools). This is where the v1 gaps and the
   differentiators live.

The four v1 gaps from PROJECT.md map onto features as follows:

- **Gap 1 — more worked examples** → "Domain-spread worked examples" (differentiator)
- **Gap 2 — sharper methodology** → "Tightened 5-phase process" + "Stricter output format" (table stakes / differentiator boundary)
- **Gap 3 — Markdown validation rubric** → "Self-check scoring rubric" (differentiator)
- **Gap 4 — deeper integration** → "Companion tool reference components" (differentiator)

## Feature Landscape

### Table Stakes (Users Expect These)

Features any usable, reliable methodology skill must have. Missing these = the skill fails
to trigger, bloats context, or produces hand-wavy analysis.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Valid `SKILL.md` frontmatter (`name`, `description`; `version` recommended) | Skill will not load/validate without it. `name` ≤64 chars, lowercase-hyphen, no reserved words "anthropic"/"claude"; `description` ≤1024 chars, third person | LOW | Already present in original; v1 just preserves it |
| Trigger-rich `description` (what it does + when to use it, third person, explicit phrases, multilingual EN+ZH) | Claude under-triggers skills; the description is the *only* thing pre-loaded for selection among 100+ skills | LOW | Original has multilingual triggers — keep and sharpen. Pack with both positive triggers and the contexts that fire it |
| The 5-phase methodology as the spine | This is the skill's reason to exist. Without an explicit phased process, output is unstructured reasoning | MEDIUM | Gap 2: tighten phase boundaries, entry/exit criteria, what each phase must produce |
| Standardized output format / template | Reproducibility — every analysis looks the same so a skeptic can audit it. Methodology skills live or die on consistent structure | MEDIUM | Gap 2: make the template stricter — required sections, the assumptions table, an explicit traceability section |
| Progressive disclosure (lean `SKILL.md`, details in `references/`) | `SKILL.md` body must stay <500 lines / ~1,500–2,000 words; context window is a shared public good | MEDIUM | Companion tools, rubric, long examples belong in `references/` and `examples/`, not inline |
| References one level deep from `SKILL.md` | Claude partially-reads (`head -100`) nested references → incomplete information | LOW | All of `references/*` and `examples/*` must link directly from `SKILL.md` |
| At least one complete worked example | A methodology with zero demonstrations reads as theory; Claude generalizes better from input→output pairs | LOW | Original has the microservices example — baseline met |
| Imperative/infinitive instruction voice, consistent terminology | Second-person ("you should") and synonym drift degrade instruction-following | LOW | Pick one term per concept (e.g. always "ground truth", never "fundamental"/"axiom" interchangeably) |
| Installable by copy/symlink into a skills directory | Compatibility constraint from PROJECT.md; matches original's install model | LOW | No build step — pure Markdown means this is free |
| No time-sensitive content | Skills go stale; dated claims become wrong | LOW | Use a "superseded patterns" `<details>` block if anything must be versioned |

### Differentiators (Competitive Advantage)

Features that separate an excellent methodology skill from a mediocre one. These align with
PROJECT.md's Core Value: *"reasoning a skeptic cannot dismiss as hand-waving."*

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Self-check validation rubric** (Gap 3) | Turns "did this follow first principles?" from vibes into a scored audit Claude applies to its own analysis. The single biggest rigor multiplier | HIGH | Implements the "validator → fix → repeat" feedback-loop pattern with a Markdown rubric as the validator. Structure detailed below |
| **Domain-spread worked examples** (Gap 1) | Examples across software/systems, product/business, personal/general, science/engineering teach Claude the method *transfers* — prevents over-fitting to one domain's vocabulary | MEDIUM | 4 domains. Each example must show the *whole* method including a failure/dead-end, not a clean march. Structure detailed below |
| **Companion tools as usable reference components** (Gap 4) | 5-Whys, pre-mortem, trade-off analysis become invokable sub-procedures, not just a "see also" list. Lets the skill reach root cause, stress-test, and decide — things bare first-principles does poorly | MEDIUM-HIGH | Each tool = one `references/` file with when-to-use, steps, worked mini-example, failure modes, handoff back to the 5-phase spine. Detailed below |
| **Entry/exit criteria per phase** (Gap 2) | "Reasoning by analogy" leaks in when phase boundaries are fuzzy. Explicit "this phase is done when X" stops Claude skipping decomposition | MEDIUM | Sharpen, don't rewrite — the 5 phases stay; add gates |
| **Explicit traceability requirement** | The Core Value: every conclusion traces to a verified ground truth. Make the output format *demand* a conclusion→ground-truth map | LOW-MEDIUM | A required output section: each recommendation cites which ground truth(s) support it. The rubric scores its presence |
| **Reasoning-over-imperatives instruction style** | Stating *why* a rule exists (not just ALL-CAPS MUST) lets Claude generalize the method to unanticipated problem types | MEDIUM | Anthropic explicitly flags imperative-string skills as brittle. Each phase explains its purpose, not just its steps |
| **Assumption-classification scheme** | Distinguishing "physical law" vs "current constraint" vs "convention" vs "untested belief" makes "challenge assumptions" concrete instead of performative | MEDIUM | A small taxonomy in the Challenge-Assumptions phase; the rubric checks each assumption is classified |
| **Worked self-application (dogfooding) note** | PROJECT.md wants the project designed *using* the methodology. A reference showing the skill analyzing itself is a credibility proof and a meta-example | LOW | Optional but cheap; reinforces the method |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create scope traps or over-engineering for a v1 pure-Markdown
single skill.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Executable validation script (scoring tool) | "Automate the rubric so scoring is objective" | Violates PROJECT.md pure-Markdown constraint; v1 has no code. A script is a separate deliverable with its own testing burden | Markdown rubric the model applies as a self-check. Scripted scoring is an explicit later milestone |
| Splitting into multiple skills (one per tool) | "5-Whys / pre-mortem deserve their own skills" | Explicitly milestone 2. Splitting now fragments triggering and duplicates the methodology spine | Companion tools as `references/` components inside the single skill |
| Exhaustive example library (10+ examples) | "More examples = better coverage" | Bloats the repo, dilutes signal, each example is maintenance surface. Diminishing returns past one strong example per domain | 4 examples — one per domain — each high-quality and showing a dead-end |
| Heavy ALL-CAPS imperative rules ("ALWAYS", "NEVER", "MUST" strings) | "Forceful rules make Claude comply" | Anthropic flags this as a top anti-pattern — rigid rules without rationale miss edge cases | State the rule + the reason so Claude generalizes |
| A rubric with many fine-grained criteria (15+ items, 1–10 scales) | "More granular = more rigorous" | Long rubrics are inconsistently applied; fine scales (1–10) have low inter-rater reliability even for LLMs | ~6–8 criteria, 3–4 discrete levels each, concrete descriptors |
| Deeply nested references (`SKILL.md`→`a.md`→`b.md`) | "Organize content into a hierarchy" | Claude partial-reads nested files → incomplete info | Flat: every reference one level deep from `SKILL.md` |
| Generic critical-thinking content (logical fallacies, bias lists, debate tactics) | "Round out the reasoning toolkit" | Scope creep — that is not first-principles thinking; adds tokens Claude already knows | Only add content that pushes Claude beyond its default reasoning |
| Domain-specific deep content (e.g. a rocket-physics primer) | "The SpaceX example needs real physics" | Methodology skill, not a domain skill; ages badly and bloats | Keep examples about the *method*; treat domain facts as illustrative, not authoritative |
| Prescriptive "use exactly N whys / N failure modes" | "Give Claude a concrete number" | 5-Whys' "five" is a guideline; pre-mortem failure counts vary. Hard numbers cause premature stopping or padding | Stop-criteria by *test* (actionable cause found) not by count |
| Auto-trigger on every analytical request | "Maximize skill usefulness" | Over-triggering injects the methodology where lighter reasoning suffices; annoys users | Scoped triggers + a boundaries section saying when *not* to use it |

## Deep Dive: Validation Rubric (Gap 3)

What makes a Markdown self-check rubric the model can apply reliably:

**Type — analytic, not holistic.** Score each dimension of rigor separately. A holistic
"rate this analysis 1–10" gives Claude nowhere to anchor and no actionable fix. Analytic
scoring per criterion produces a punch-list of what to repair.

**Criteria count — ~6–8.** Enough to cover the 5 phases plus traceability; few enough to
apply consistently. Suggested criteria, each mapping to a phase or the Core Value:
1. Problem essence is the *actual* fundamental challenge, not a restated symptom
2. Assumptions are enumerated *and classified* (law / constraint / convention / belief)
3. Each challenged assumption is either verified, discarded, or flagged as unverified
4. Ground truths are irreducible and evidence-backed (not themselves assumptions)
5. Reasoning chain builds upward from ground truths with no analogy shortcuts
6. Every conclusion traces to specific ground truth(s) — explicit map present
7. The analysis names what would falsify it / where it is weakest
8. (Optional) A companion tool was applied where appropriate, or its omission justified

**Levels — 3 or 4 discrete bands with concrete descriptors.** Not a 1–10 scale (low
reliability). Use named levels — e.g. **Rigorous / Adequate / Hand-wavy** (3) or add
**Absent** (4). Each level needs an observable descriptor, not an adjective:
- *Rigorous:* "every assumption classified and each non-law assumption has a verification
  note or explicit unverified flag"
- *Hand-wavy:* "assumptions listed but not classified, or challenged only rhetorically"

**Scoring structure.** Per-criterion level → simple aggregate. Two viable models:
- *Gate model (recommended):* any criterion at the lowest band = analysis fails the
  rubric and must be revised. Mirrors the Core Value ("a skeptic cannot dismiss it") —
  one hand-wavy link sinks the chain.
- *Tally model:* count bands; require e.g. all criteria ≥ Adequate and ≥N at Rigorous.
  Gate model is stricter and better matches first-principles intent.

**Application as a feedback loop.** The rubric is the "validator" in Anthropic's
validator→fix→repeat pattern: after producing an analysis, Claude scores it against the
rubric, and if any criterion fails, revises and re-scores. Make this loop explicit in
`SKILL.md`.

**Self-application caveats to bake in.** LLM self-grading is lenient and inconsistent
without anchors. Mitigations: concrete observable descriptors (above), require Claude to
*quote the specific span* of its analysis that satisfies/fails each criterion (evidence,
not assertion), and keep the rubric short enough to apply faithfully.

**Format.** A single `references/validation-rubric.md` table — criterion rows, level
columns, descriptor cells — plus a short "how to apply" preamble and the
pass/revise gate. ToC at top if >100 lines (unlikely; keep it tight).

## Deep Dive: Worked Examples (Gap 1)

What makes a worked first-principles example instructive vs filler:

**Domain spread — exactly 4, one per PROJECT.md domain:** software/systems,
product/business, personal/general, science/engineering. One per domain proves transfer;
more per domain is maintenance bloat (see anti-features).

**It must show the whole method, including a dead-end.** A clean, frictionless example
teaches Claude that first-principles is a tidy march. Real rigor includes: an assumption
that turned out true (so not everything is overturned), an assumption that was discarded,
and at least one reasoning step that was tried and abandoned. The microservices example in
the original is the model — extend, don't replace.

**Structure — mirror the output format exactly.** Each example walks the 5 phases with the
standardized template, so the example doubles as a format demonstration. Anthropic's
"examples pattern": concrete input→output pairs teach style better than prose.

**Length — medium, not exhaustive.** Long enough to show real decomposition (not a toy),
short enough that the point is the *method* not the domain. Each example is its own file
in `examples/`; they cost zero context until read (progressive disclosure).

**Each example should ideally exercise one companion tool** — e.g. the product/business
example uses trade-off analysis, the systems example uses pre-mortem — showing integration
in action rather than as a separate claim.

**Anti-filler test:** if you could swap the domain facts and the reasoning is unchanged,
it is filler. A good example's decomposition is *specific* to its domain's real constraints.

## Deep Dive: Companion Tool Reference Components (Gap 4)

"Fully usable reference component" means each of 5-Whys, pre-mortem, and trade-off analysis
is a self-contained `references/` file Claude can execute as a sub-procedure — not a
one-line "see also". Each file should contain:

**Common structure (all three):**
- **When to use / when not to use** — the decision criterion for invoking it
- **How it connects to the 5-phase spine** — which phase it plugs into, and the handoff
  back (e.g. 5-Whys feeds Phase 3 Ground Truths; pre-mortem stress-tests Phase 5 Validate)
- **Step-by-step procedure** — concrete, ordered, with stop criteria
- **One short worked mini-example** — input→output, in the standard voice
- **Failure modes** — the documented pitfalls of that tool (this is the highest-value
  content per Anthropic — the "gotchas" section)
- **Output shape** — what the tool produces and how it folds into the main output format

**5-Whys specifics:**
- Stop criterion is a *test*, not a count: stop when the cause is actionable (a concrete
  fix would prevent recurrence) — "five" is a guideline
- Branch, don't thread: ask "what else?" at each level — multiple causal branches, a cause
  *tree*, not a single line (the #1 documented pitfall is linear single-cause thinking)
- "Human error" is never a root cause — it signals a system weakness; keep digging
- Validate each why→link with evidence; keep it fact-based and blame-free

**Pre-mortem specifics:**
- Premise framing: "assume the plan has already failed completely — explain why"
  (prospective hindsight). This is the mechanism — must be stated, not paraphrased
- Generate failure modes broadly *before* triaging
- Triage to the top concerns, then attach concrete mitigations to each
- Plugs into Phase 5 (Validate): it is how the analysis names what would falsify it

**Trade-off analysis specifics:**
- Make criteria and their relative weight explicit *before* scoring options (Ousterhout's
  "no voodoo constants" applied to decision-making)
- Force the alternatives to be real (including "do nothing")
- Name which trade-offs are fundamental (rooted in ground truths) vs incidental
- Output a defensible recommendation with the trade-off accepted, stated plainly

**Integration note:** PROJECT.md says these live *inside* the single skill as references —
not separate skills (that is milestone 2). `SKILL.md` should briefly say what each tool is
for and link to its file; the depth lives in the reference.

## Feature Dependencies

```
Valid SKILL.md frontmatter + trigger-rich description
    └──required by──> everything (skill must load and trigger first)

Tightened 5-phase process (Gap 2)
    └──required by──> Standardized output format (format encodes the phases)
            └──required by──> Validation rubric (Gap 3) (rubric scores the format/phases)
            └──required by──> Worked examples (Gap 1) (examples demonstrate the format)

Companion tool references (Gap 4)
    └──requires──> Tightened 5-phase process (tools must name their handoff phase)
    └──enhances──> Worked examples (examples exercise the tools)
    └──enhances──> Validation rubric (rubric can check "tool applied where apt")

Progressive disclosure (lean SKILL.md)
    └──required by──> rubric, examples, companion tools (all live in references/ + examples/)

Reasoning-over-imperatives style ──enhances──> 5-phase process, rubric (rationale travels)

Executable scoring script ──conflicts──> pure-Markdown v1 constraint (anti-feature)
Multiple separate skills  ──conflicts──> single-skill v1 scope (anti-feature)
```

### Dependency Notes

- **Output format requires the tightened process:** the template is the phases made
  concrete; sharpen the methodology (Gap 2) before/with hardening the format.
- **Rubric requires the output format:** the rubric scores whether an analysis populated
  the format with real rigor — define what "done" looks like before scoring it.
- **Examples require the output format:** each example *is* a filled-in template; finalize
  the template first or examples will need rework.
- **Companion tools require the 5-phase spine:** a tool reference must state which phase it
  plugs into — so the spine must be stable before the tools are written.
- **Companion tools enhance examples and rubric:** examples that exercise tools, and a
  rubric criterion checking tool use, only work once the tool references exist.
- **Progressive disclosure underpins everything Gap 1/3/4:** all new content must land in
  `references/`/`examples/` to keep `SKILL.md` <500 lines — this constrains *where*
  features live, not whether they ship.

## MVP Definition

### Launch With (v1) — all four gaps are in scope per PROJECT.md

- [ ] Tightened 5-phase methodology with entry/exit criteria — Gap 2; the spine everything depends on
- [ ] Hardened standardized output format with explicit traceability section — Gap 2; encodes the phases, prerequisite for rubric + examples
- [ ] `references/validation-rubric.md` — analytic, ~6–8 criteria, 3–4 levels, gate scoring, applied as a feedback loop — Gap 3
- [ ] 4 domain-spread worked examples in `examples/` (software/systems, product/business, personal/general, science/engineering), each showing a dead-end — Gap 1
- [ ] 3 companion tool references (`5-whys.md`, `pre-mortem.md`, `trade-off-analysis.md`), each a fully usable component — Gap 4
- [ ] Preserved valid frontmatter, multilingual triggers, copy/symlink install — table stakes, inherited from original
- [ ] Lean `SKILL.md` (<500 lines) linking all references one level deep — table stakes

### Add After Validation (v1.x)

- [ ] Self-application / dogfooding reference (skill analyzing its own design) — add if the v1 examples feel thin on meta-credibility
- [ ] Additional examples within a domain — only if real usage shows a domain where one example is insufficient
- [ ] Assumption-classification taxonomy expansion — refine after observing how Claude classifies in practice

### Future Consideration (v2+)

- [ ] Splitting into a collection of thinking skills — explicitly milestone 2
- [ ] Executable validation script for scored self-check — explicitly a later milestone; needs the rubric stable first
- [ ] Python skill-builder — explicitly milestone 3

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Tightened 5-phase process (Gap 2) | HIGH | MEDIUM | P1 |
| Hardened output format + traceability (Gap 2) | HIGH | MEDIUM | P1 |
| Validation rubric (Gap 3) | HIGH | HIGH | P1 |
| Companion tool references (Gap 4) | HIGH | MEDIUM-HIGH | P1 |
| 4 domain-spread worked examples (Gap 1) | HIGH | MEDIUM | P1 |
| Trigger-rich multilingual description | HIGH | LOW | P1 (preserve/sharpen) |
| Progressive disclosure / lean SKILL.md | MEDIUM | LOW | P1 |
| Reasoning-over-imperatives style pass | MEDIUM | MEDIUM | P2 |
| Assumption-classification scheme | MEDIUM | MEDIUM | P2 |
| Self-application dogfooding reference | LOW-MEDIUM | LOW | P3 |

## Competitor Feature Analysis

No direct competitor "first-principles skill" beyond the original being enhanced. The
relevant comparison is against (a) generic critical-thinking prompts and (b) Anthropic's
own reference skills.

| Feature | Generic CoT / "think step by step" prompt | Anthropic reference skills (pdf, docx, etc.) | Our Approach |
|---------|-------------------------------------------|----------------------------------------------|--------------|
| Structured phases | Absent — freeform | N/A (task skills, not reasoning) | Explicit 5-phase spine with entry/exit gates |
| Self-validation | Absent | Validator-loop pattern (often via scripts) | Markdown rubric applied as a feedback loop |
| Worked examples | Rarely | Examples pattern, input→output pairs | 4 domain-spread examples, each with a dead-end |
| Companion methods | Absent | N/A | 5-Whys / pre-mortem / trade-off as usable references |
| Triggering | User must invoke manually | Trigger-rich description | Trigger-rich multilingual (EN+ZH) description |
| Progressive disclosure | N/A | Core pattern | Lean SKILL.md + references/ + examples/ |

## Sources

- [Skill authoring best practices — Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — HIGH confidence (official)
- [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills) — HIGH confidence (official)
- [Equipping agents for the real world with Agent Skills — Anthropic Engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — HIGH confidence (official)
- [anthropics/claude-code skill-development SKILL.md](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md) — HIGH confidence (official reference skill)
- [Skill Authoring Patterns from Anthropic's Best Practices — generativeprogrammer.com](https://generativeprogrammer.com/p/skill-authoring-patterns-from-anthropics) — MEDIUM confidence (corroborates official docs)
- [chrisdavidson/first-principles-skill](https://github.com/chrisdavidson/first-principles-skill) — HIGH confidence (the skill being enhanced)
- [Premortem — Gary Klein](https://www.gary-klein.com/premortem) — HIGH confidence (technique originator)
- [Performing a Project Premortem — Klein, HBR/ResearchGate](https://www.researchgate.net/publication/3229642_Performing_a_Project_Premortem) — HIGH confidence
- [Five whys — Wikipedia](https://en.wikipedia.org/wiki/Five_whys) and [5 Whys — MindTools](https://www.mindtools.com/a3mi00v/5-whys/) — MEDIUM-HIGH confidence (multiple corroborating)
- [5 Whys Root Cause Analysis — ReliaMag](https://reliamag.com/articles/5-whys-root-cause-analysis-maintenance/) — MEDIUM confidence (corroborates pitfalls: linear thinking, stop criteria)
- [LLM-Rubric: A Multidimensional, Calibrated Approach — arXiv](https://arxiv.org/html/2501.00274v1) — MEDIUM confidence (rubric design for LLM self-assessment)
- [Rubric-Based Evaluations & LLM-as-a-Judge — Medium/Adnan Masood](https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80) — MEDIUM confidence (analytic vs holistic, level granularity, self-grading leniency)
- [First principles — Untools](https://untools.co/first-principles/) and [fs.blog](https://fs.blog/first-principles/) — MEDIUM confidence (methodology framing)

---
*Feature research for: Structured-reasoning / methodology Claude Code skill*
*Researched: 2026-05-16*
