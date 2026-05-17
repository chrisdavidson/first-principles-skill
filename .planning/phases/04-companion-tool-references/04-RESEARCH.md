# Phase 4: Companion Tool References — Research

**Researched:** 2026-05-17
**Domain:** Thinking-tool sub-procedure authoring (pure Markdown, Claude Code skill reference components)
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** Each file is shaped to its own tool — not a single shared section template across all three.
  5-Whys is structured around its branching drill-down, pre-mortem around its prospective-hindsight
  framing, trade-off around its weighted matrix. Headings and ordering vary per tool.
- **D-02:** Two shared anchors: every file opens with a clear "when to reach for this" framing and
  ends with the handoff to the methodology. Everything between is per-tool.
- **D-03:** Regardless of per-tool shaping, all five ROADMAP components must appear in each file —
  when-to-use, the procedure, a mini-example, failure modes, and the handoff. Per-tool shaping
  changes arrangement and emphasis, never presence.
- **D-04:** All three mini-examples draw from one shared domain: everyday / non-technical scenarios.
- **D-05:** Within that shared everyday domain, each tool gets a separate scenario chosen to play to
  that tool's strength — 5-Whys on a recurring problem, pre-mortem on a plan that could fail,
  trade-off on a real choice.
- **D-06:** Each file is a tight sub-procedure — lean, roughly under ~100 lines, no table of
  contents.
- **D-07:** "Promotion-ready for the milestone-2 split" means self-contained body content only. No
  forward-looking notes about what a split would add.
- **D-08:** The handoff is written as a pointer back to the methodology, not a hard dependency —
  applying the tool from its own file alone must not require having read the 5-phase spine.
- **SC-4:** No companion tool file carries its own YAML frontmatter — each is a reference component,
  not a separate skill.

### Claude's Discretion

- The exact per-tool structure of each file's procedure section (D-01).
- The specific everyday scenario chosen for each tool's mini-example (D-05).
- The wording of each "when to reach for this" opener and each handoff (D-02).
- Which failure modes to surface for each tool.
- The test-based stop criterion's exact phrasing for the 5-Whys branching procedure.

### Deferred Ideas (OUT OF SCOPE)

- SKILL.md tool descriptions (TOOL-04) — Phase 6.
- Final nav-map audit / README / schema validation — Phase 6.
- Four shipped worked examples — Phase 5.
- Future split of companion tools into separate skills — milestone 2.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| TOOL-01 | `references/five-whys.md` is a usable component — when-to-use, branching procedure with test-based stop criterion, mini-example, failure modes, and handoff to the 5-phase spine | §5-Whys Tool: Canonical Structure, §Stop Criterion, §Failure Modes: 5-Whys |
| TOOL-02 | `references/pre-mortem.md` is a usable component — prospective-hindsight framing, procedure, mini-example, failure modes, and handoff to Phase 5 (Validate) | §Pre-Mortem Tool: Canonical Structure, §Framing, §Failure Modes: Pre-Mortem |
| TOOL-03 | `references/trade-off-analysis.md` is a usable component — weighted-criteria-before-scoring procedure, mini-example, failure modes, and handoff to the 5-phase spine | §Trade-Off Analysis Tool: Canonical Structure, §Weights-Before-Scoring Discipline, §Failure Modes: Trade-Off |
</phase_requirements>

---

## Summary

Phase 4 fills the three stub files (`five-whys.md`, `pre-mortem.md`, `trade-off-analysis.md`) with
full sub-procedure content. Each file is a Layer-3 reference — loaded on-demand when the resident
methodology in SKILL.md says "reach for a companion tool." The three tools address distinct moments
in an analysis: 5-Whys surfaces the causal chain beneath a symptom (usable during Phase 2 Challenge
Assumptions or Phase 4 Reason Upward); pre-mortem stress-tests a proposed plan before committing
(feeding Phase 5 Validate); trade-off analysis compares options with explicit criteria (usable
during Phase 4 Reason Upward when multiple viable paths exist).

All three tools are mature, well-documented thinking techniques with canonical structures and
well-understood failure modes. The canonical sources (Gary Klein on pre-mortem, Sakichi Toyoda /
Toyota Production System on 5-Whys, multi-criteria decision analysis literature on trade-off
matrices) converge on the same discipline the CONTEXT.md decisions encode: the test-based stop
criterion (not count-based), prospective hindsight framing (not forward-looking risk listing), and
weights-before-scoring (not reverse-engineering weights to a preferred answer).

The research findings confirm that the three specific success criteria in ROADMAP (SC-1, SC-2, SC-3)
each correspond to a documented canonical best practice that distinguishes rigorous application from
the common failure mode.

**Primary recommendation:** Author each file in a single writing pass shaped tightly to its tool.
The procedure section is the most critical — it must be runnable from the file alone (D-07) and
must encode the canonical discipline that makes the tool non-trivial (SC-1/SC-2/SC-3). Keep each
file under 100 lines by making every sentence carry weight: no introductory prose that says what
first-principles thinking is, no restating the tool's name, no "feel free to adapt."

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| five-whys.md content | Content layer (the reference file itself) | Invoked from SKILL.md nav-map | File is the entire artifact; no backend, no runtime |
| pre-mortem.md content | Content layer | Feeds Phase 5 Validate in SKILL.md | Handoff points to a named phase in the resident methodology |
| trade-off-analysis.md content | Content layer | Feeds Phase 4 Reason Upward in SKILL.md | Handoff points to a named phase in the resident methodology |
| SKILL.md nav-map link targets | Already wired (Phase 2) | — | Stubs at correct paths; Phase 4 fills content only |

---

## Standard Stack

### Core

This phase produces pure Markdown files. There is no executable stack. The "standard stack" is the
authoring discipline:

| Element | Spec | Purpose | Why Standard |
|---------|------|---------|--------------|
| CommonMark Markdown | No formal version; plain fenced blocks + ATX headings | File body | Universal render; Agent Skills spec mandates plain Markdown body |
| No YAML frontmatter | SC-4 (hard constraint) | File header | These are reference components, not separate skills |
| Forward-slash cross-references | `references/output-template.md` | Any link back to the methodology | Cross-platform; required by CLAUDE.md and the Agent Skills spec |
| UTF-8, LF line endings | CLAUDE.md / Agent Skills spec | Encoding | Cross-platform; official best practice |

[CITED: CLAUDE.md — "UTF-8, LF line endings, forward-slash paths ... official best practices"]
[CITED: first-principles-thinking/SKILL.md — existing companion tool nav-map link format]

### Supporting

| Element | Purpose | When to Use |
|---------|---------|-------------|
| `references/output-template.md` | Authoritative section names; handoff wording references real artifacts (Derivation Chains, Signed-off analysis) | When writing handoff sections — name real artifacts from the methodology |
| `first-principles-thinking/SKILL.md` Phase 5 description | Confirms the pre-mortem handoff target ("Phase 5: Validate") and what that phase does | Writing the pre-mortem handoff |
| `references/validation-rubric.md` | Quality bar for an authored reference component — tone, terseness, how observable descriptors read | Sanity-checking prose quality, NOT a length model |

---

## Package Legitimacy Audit

Not applicable. This phase installs no packages. All deliverables are pure Markdown text files.

---

## Architecture Patterns

### System Architecture Diagram

```
SKILL.md nav-map
    │
    ├─ "Stuck on why" ──────────────► references/five-whys.md
    │                                    └─ handoff ──► 5-phase spine (Phase 2 or 4)
    │
    ├─ "Stress-testing a solution" ─► references/pre-mortem.md
    │                                    └─ handoff ──► Phase 5 (Validate)
    │
    └─ "Choosing between options" ──► references/trade-off-analysis.md
                                         └─ handoff ──► 5-phase spine (Phase 4)
```

Each file is a terminal node — it does not load any further reference files. The handoffs point
back to the resident methodology in SKILL.md, not to other reference files.

### Recommended Project Structure

The three files fill existing stubs at:

```
first-principles-thinking/
└── references/
    ├── five-whys.md          ← fill this stub (canonical: five-whys.md, not 5-whys.md)
    ├── pre-mortem.md         ← fill this stub
    └── trade-off-analysis.md ← fill this stub
```

No new files. No path changes. No SKILL.md edits.

### Pattern: Tight Sub-Procedure Shape

**What:** Each file has exactly five named components (D-03), ordered to serve the tool's own
logic (D-01), opening with when-to-use and closing with handoff (D-02).

**When to use:** Always — this is the mandated pattern for all three files.

**Implied section order per tool:**

*five-whys.md* — shaped around the branching drill-down:
1. When to reach for this tool (use-case + contrast: when NOT to use)
2. Procedure (branching drill-down with test-based stop criterion)
3. Mini-example (recurring everyday problem)
4. Failure modes
5. Handoff to the 5-phase spine

*pre-mortem.md* — shaped around the prospective-hindsight framing:
1. When to reach for this tool
2. Framing instruction (the grammatical shift: failure already happened)
3. Procedure (individual write → share → pattern)
4. Mini-example (a plan that could fail)
5. Failure modes
6. Handoff to Phase 5 (Validate)

*trade-off-analysis.md* — shaped around the weighted matrix:
1. When to reach for this tool
2. Procedure (weights fixed before scoring — this is the core discipline)
3. Mini-example (a real everyday choice)
4. Failure modes
5. Handoff to the 5-phase spine

Note: pre-mortem has an extra framing section because the prospective-hindsight shift is the
mechanism — it must be stated explicitly before the procedure steps (SC-2). The other two tools
embed their core discipline (test-based stop, weights-before-scoring) inside the procedure section
rather than as a separate preamble.

### Anti-Patterns to Avoid

- **Shared section template across all three files:** Violates D-01; obscures the tool's own logic
  and produces files that read as the same skeleton with headings swapped.
- **Count-based 5-Whys stop criterion ("ask why five times"):** This is the canonical failure mode.
  The correct criterion is test-based: stop when a corrective action can be stated that would
  prevent recurrence. [CITED: reliamag.com/articles/5-whys-root-cause-analysis-maintenance/]
- **Forward-looking pre-mortem framing ("what could go wrong?"):** Loses the prospective hindsight
  mechanism and degrades to a standard risk list. The canonical instruction is to assume failure has
  already occurred and ask what happened. [CITED: nesslabs.com/pre-mortem-anticipate-failure-with-prospective-hindsight]
- **Weights set after scoring in trade-off analysis:** Allows reverse-engineering weights to favor a
  preferred option. Weights must be finalized before any option is scored.
  [CITED: goalsandprogress.com/weighted-decision-matrix/]
- **Including YAML frontmatter:** Violates SC-4; turns a reference component into a separate skill
  with its own trigger, breaking the v1 single-skill scope discipline. [CITED: PITFALLS.md Pitfall 7]
- **Files over ~100 lines:** Violates D-06; Layer-3 on-demand files incur a token cost every time
  they are read. A 200-line companion tool file also warrants a table of contents
  (per CLAUDE.md Integration Gotchas), which D-06 explicitly forbids.
- **"Nothing to say in failure modes" omission:** D-03 mandates all five ROADMAP components appear.
  A failure modes section with no content gets the honest-depth escape valve, not a silent omission.
- **Handoff that imports the full methodology:** Violates D-08. The handoff says "return to the
  5-phase methodology" or "continue to Phase 5 (Validate)" — it does not reproduce methodology
  content. A reader applying the tool standalone must not be blocked.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Test-based stop criterion for 5-Whys | Invent a novel stop rule | Corrective Action Test: stop when you can state an action that would prevent recurrence, AND that action is within your ability to take | This is the documented canonical criterion; count-based ("five times") is the documented failure mode |
| Prospective hindsight framing | Write a risk-listing procedure | Gary Klein's grammatical shift: "It is [future date]. The plan has failed badly. What happened?" | Proven to increase risk identification accuracy over forward-looking alternatives; the shift is the mechanism |
| Weights-before-scoring discipline | Build a scoring-then-weighting procedure | Finalize all criteria weights before scoring any option | The reverse-engineering failure mode is documented; fixing weights first is the canonical countermeasure |

**Key insight:** All three tools' critical disciplines are canonical, well-documented, and correspond
exactly to the failure modes the ROADMAP success criteria are preventing. The research confirms there
is no novel design work here — the job is faithful implementation of established practice.

---

## Tool-by-Tool Research Findings

### 5-Whys: Canonical Structure

**When to use:** A symptom keeps recurring and the surface cause is known but fixing it doesn't
prevent recurrence. The problem has a causal chain that can be traced. NOT the right tool when
multiple interacting system failures are suspected (use a fishbone/Ishikawa diagram for those).
[CITED: flowfuse.com/blog/2025/12/five-whys-root-cause-analysis-definition-examples/]
[ASSUMED: the "not for complex multi-system failures" contrast clause is a standard practitioner
guideline; specific phrasing is Claude's discretion per CONTEXT.md]

**The branching requirement:** The tool is correctly modeled as a cause tree, not a linear thread.
At each level, ask "What else could cause this?" before going deeper. Multiple valid causes at a
level each get their own branch. Discipline: complete one branch before exploring alternatives.
[CITED: reliamag.com/articles/5-whys-root-cause-analysis-maintenance/]

**Test-based stop criterion (SC-1):** Stop when BOTH of the following hold:
1. You can state a specific, implementable corrective action that would prevent this from recurring.
2. That action is within your practical ability to take (organizational boundary check).

If the required action is vague ("improve the process"), too costly to be realistic, or outside your
control, continue drilling. A branch that reaches a root cause with no actionable corrective is a
dead branch — record it and switch to a different branch.
[CITED: reliamag.com/articles/5-whys-root-cause-analysis-maintenance/ — "Corrective Action Test",
"Organizational Boundary Check"]

**Stop criterion framing note:** The count of five is a mnemonic heuristic (Sakichi Toyoda's
original framing), not an operational criterion. The procedure file must not say "ask why five
times." The number of iterations varies per problem. [ASSUMED: this is training knowledge about
the Toyota origin; the corrective-action test is independently verified above]

**Validation of each causal link:** Each "because" answer in the chain must be supported by
observable evidence, not inference. Stating "probably because X" without a verification step is
a known failure mode. [CITED: reliamag.com/articles/5-whys-root-cause-analysis-maintenance/]

### Pre-Mortem: Canonical Structure

**Origin and evidence base:** Gary Klein, first published in Harvard Business Review (2007). The
prospective hindsight mechanism is documented to increase risk-identification accuracy by ~30% vs.
forward-looking approaches. [CITED: nesslabs.com/pre-mortem-anticipate-failure-with-prospective-hindsight]
[CITED: strategicdecisionsolutions.com/premortem-method/ — "A pre-mortem stipulates that the project
has already definitively failed"]

**The framing instruction (SC-2):** The grammatical shift is the mechanism. The canonical framing is:
> "It is [specific future date]. The plan has completely failed — not merely underperformed, but
> failed badly. Working backward from that fact: what happened?"

The past tense is not rhetorical. It bypasses the optimism bias that makes forward-looking risk
lists generic. [CITED: get-alfred.ai/blog/pre-mortem-technique]

**Procedure shape:**
1. Frame: read the prospective-hindsight premise aloud or to yourself before writing anything.
2. Write: independently list every cause of the failure you can think of. Silently, before sharing.
3. Share: surface the list, one item at a time. No filtering.
4. Pattern: identify which failure modes appear across multiple independent responses.

The independent-write step before sharing is essential — it prevents the first speaker from
anchoring the room. [CITED: get-alfred.ai/blog/pre-mortem-technique — "Klein's recommendation"]

**Timing:** Most effective after the plan has enough specificity to reason about particular failure
modes, but before the plan is finalized and has organizational momentum. Running it too early
produces generic risks. [CITED: nesslabs.com/pre-mortem-anticipate-failure-with-prospective-hindsight]

**For solo use (no room to facilitate):** Write the failure list independently, then re-read the
list adversarially — "Which of these would I have suppressed in a group setting?" These are the
most valuable entries.

### Trade-Off Analysis: Canonical Structure

**When to use:** Two or more options are genuinely viable (none is obviously dominant). The choice
involves multiple criteria that pull in different directions. A single intuitive pick would be hard
to justify to others.

**Weights-before-scoring discipline (SC-3):** This is the core mechanism. The canonical rule:
define ALL criteria and their relative weights before examining how any option scores on any
criterion. [CITED: goalsandprogress.com/weighted-decision-matrix/ — "Setting criteria and weights
BEFORE looking at options is the most important rule"]

Rationale: if weights are set after scoring, they will unconsciously be adjusted until the preferred
option wins. The weights-first rule is the only structural countermeasure against this.

**Criteria count:** 5–8 criteria. More than 8–10 dilutes the signal — each additional criterion
reduces the weight of every other one. [CITED: deckary.com/blog/decision-matrix-guide]

**Procedure shape:**
1. Name the options being compared.
2. List criteria (5–8 max). Lock them — no new criteria after this step.
3. Assign weights to criteria (e.g., 1–5 or percentage shares). Lock them before any scoring.
4. Score each option on each criterion independently.
5. Compute weighted scores (weight × score per criterion, sum per option).
6. Read the result: the highest score is the analysis's recommendation, not an automatic decision —
   if the result surprises you, re-examine the weights (they may not reflect what you actually value).

**Sensitivity check:** If two options score within ~10% of each other, the difference is likely
within scoring noise. The correct response is not to refine scores — it is to identify which single
criterion, if its weight changed, would flip the result. That criterion is the real decision.

---

## Mini-Example Scenarios (Claude's Discretion — recommendations)

Per D-04/D-05: one shared everyday/non-technical domain, separate scenario per tool, avoiding the
four Phase 5 domains (software/product/personal/science).

**Recommended domain:** household/logistics decisions — familiar enough that the tool's mechanics
are visible rather than domain knowledge.

**Scenario recommendations (Claude's discretion to adopt or adapt):**

| Tool | Recommended Scenario | Why It Plays to the Tool's Strength |
|------|---------------------|-------------------------------------|
| 5-Whys | Bread keeps going stale before it's finished (a recurring household waste problem) | Recurring symptom with a causal chain — fits "something keeps happening" 5-Whys use case; produces a non-obvious root cause (buying too large a loaf because of a habit/assumption) |
| Pre-mortem | Planning to host a dinner party for 12 people in two weeks | A concrete plan with enough specificity to reason about failures; prospective hindsight surfaces the most probable failure modes (timing, dietary needs, space) that optimism would suppress |
| Trade-off | Choosing between two laptops for a family member (e.g., a refurbished mid-range vs. a new entry-level) | A genuine everyday choice with competing criteria (price, reliability, longevity, ease of use) where intuition is unreliable; shows weighted scoring catching a non-obvious answer |

Note: these are recommendations under Claude's discretion (D-05). The planner and implementer should
adopt these or substitute alternatives that equally satisfy D-04/D-05 constraints. The constraint is
everyday/non-technical and separate scenarios — not these specific scenarios.

---

## Common Pitfalls

### Pitfall 1: Count-Based Stop Criterion in 5-Whys

**What goes wrong:** The file says "ask why five times" or "stop after 5 iterations." The procedure
becomes count-driven, not evidence-driven. Analyses stop when the count hits five even if the
corrective action is still vague; or they run past the real root cause because five hasn't been
reached.

**Why it happens:** "5-Whys" has the number in its name; authors default to using the count as the
criterion. The original mnemonic was "you often get to root cause in ~5 iterations" — not "stop
at 5."

**How to avoid:** The stop criterion is the Corrective Action Test, not a count. Write it as a
conditional: "Stop drilling when you can state a specific action that would prevent recurrence AND
that action is within your control." If the count of iterations is mentioned at all, frame it as
typical range, not a stop rule.

**Warning signs:** The procedure section mentions a specific number of "why" iterations as the stop
condition.

### Pitfall 2: Forward-Looking Pre-Mortem Framing

**What goes wrong:** The procedure says "list what could go wrong." This produces a standard risk
list — the same list the team would produce in a normal risk assessment, anchored by what they
already know is risky. The prospective hindsight mechanism is lost.

**Why it happens:** "Pre-mortem" sounds like it should mean "think about risks before they happen."
The prospective-hindsight shift (assume it already failed) feels unnatural and is easy to drop.

**How to avoid:** The framing instruction must be a mandatory first step, not an optional context
note. The past tense ("the plan has failed") must appear in the procedure, not just in the
introduction. The word "already" or "has happened" does work that "could happen" cannot.

**Warning signs:** The procedure says "identify risks" or "think about what might go wrong."

### Pitfall 3: Weights Set After Scoring in Trade-Off Analysis

**What goes wrong:** The procedure allows (or encourages) scoring options first, then assigning
weights. The analyst consciously or unconsciously adjusts weights until their preferred option wins.
The matrix produces a justified appearance for a decision already made intuitively.

**Why it happens:** It feels natural to score first (you know the options better) and weight after.
The reverse-engineering failure mode is not obvious until pointed out.

**How to avoid:** The procedure explicitly says weights are locked before any option is scored. The
word "lock" or "finalize" must appear before the scoring step. Consider noting: "if the result
surprises you, revisit your weights — but only if you can articulate why a weight was wrong before
seeing the result."

**Warning signs:** The procedure says "score options, then assign weights" or does not explicitly
say when weights are set.

### Pitfall 4: Files That Describe Rather Than Instruct

**What goes wrong:** The file explains what the tool is and why it works, but doesn't give a reader
the steps to run it. Prose like "5-Whys helps you find root causes by iteratively asking why" is
descriptive. A user reading it still doesn't know what to write down, when to stop, or what to do
with the output.

**Why it happens:** Reference files naturally drift toward description because description is easier
to write than instruction. The companion tools come after the validation rubric, which has a
heavily explanatory style.

**How to avoid:** Every procedure section should be written in imperative mood ("State the symptom.
Ask why it occurred. Write the answer."). A reader should be able to work through the procedure with
no prior knowledge of the tool. The validation-rubric.md (~19 KB) is explicitly not the length or
style model (D-06).

**Warning signs:** The procedure section uses third person ("the analyst asks...") or passive voice
("the failure modes are identified...") instead of second person / imperative.

### Pitfall 5: Handoff That Re-Explains the Methodology

**What goes wrong:** The handoff section reproduces phase names, artifacts, or instructions from
the resident 5-phase methodology. This creates maintenance risk (the handoff must be updated every
time the methodology changes) and bloats the file toward or past the ~100-line limit.

**Why it happens:** The implementer wants to make the handoff "useful" by giving context about the
target phase.

**How to avoid:** The handoff is a pointer, not a summary. One to three sentences: what the tool's
output is, where it feeds in the methodology, and which artifact it contributes to. Example:
"Return to the 5-phase methodology. The root cause(s) identified here feed Phase 2 (Challenge
Assumptions) — add each root cause as a challenged assumption row in the Classified Assumptions
Table." That is the complete handoff.

**Warning signs:** The handoff section is more than 3–4 lines. It re-explains what Phase 5
(Validate) does.

---

## Code Examples

There is no executable code in this phase. The "examples" are structural patterns.

### Five-Whys Procedure Section Pattern

```markdown
## Procedure

**State the symptom.** Write one sentence: the observable problem that keeps occurring.

**Ask: Why did this happen?** Write every cause you can identify — do not filter yet.

**For each cause, ask why again.** At each level, ask "What else caused this?" before
going deeper. Multiple valid causes each become their own branch.

**Stop drilling a branch when BOTH hold:**
- You can state a specific corrective action that would prevent recurrence.
- That action is within your practical control.

If a branch produces a cause with no actionable corrective, record it and move to the
next branch. A cause outside your control is a real finding — note it, do not discard it.

**Validate each causal link** with observable evidence, not inference. If you cannot
point to evidence for a link, flag it as assumed.
```

### Pre-Mortem Framing Block Pattern

```markdown
## Framing

Before any other step, adopt this premise explicitly:

> It is [date approximately 6 months from now]. This plan has failed — not
> merely underperformed, but failed badly. That outcome is a fact.
> Working backward: what caused it?

This past-tense framing is not rhetorical. It bypasses the optimism bias that makes
forward-looking risk lists generic. Do not skip it or soften it to "might fail."
```

### Trade-Off Weights-Lock Pattern

```markdown
## Procedure

1. **Name the options.** List each option being compared.
2. **List criteria.** Identify 5–8 criteria that matter. Lock this list — no new
   criteria after this step.
3. **Assign weights. Lock them now.** Give each criterion a relative weight
   (e.g., 1–5). Lock the weights before scoring any option. If you cannot assign
   weights without looking at how options score, you are not ready to use this tool.
4. **Score each option** on each criterion independently (e.g., 1–5).
5. **Compute:** weight × score per criterion; sum per option.
6. **Read the result** and check: if it surprises you, re-examine the weights
   — but only if you can state why a weight was wrong before seeing the result.
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 5-Whys as linear single-thread | 5-Whys as a branching cause tree | Documented in industrial RCA literature; widely accepted | Prevents single-track tunnel vision; makes multiple contributing causes visible |
| Pre-mortem as a meeting technique (group required) | Pre-mortem adaptable to solo use via independent writing discipline | Klein's original was group-based; solo adaptation is a documented extension | Companion tools must be usable by a single analyst (Claude) without a room |
| Trade-off matrix: score then weight | Trade-off matrix: weight then score | Best-practice consensus in MCDA literature | The "weights-before-scoring" rule is the primary structural countermeasure against motivated reasoning |

**Deprecated/outdated:**

- **5-Whys count rule ("ask why five times"):** Still widely cited in introductory material but
  deprecated as an operational stop criterion in serious RCA practice. Never use as the stop rule
  in the procedure file. [CITED: reliamag.com/articles/5-whys-root-cause-analysis-maintenance/]

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | "NOT the right tool when multiple interacting system failures are suspected" (5-Whys contrast clause) | §5-Whys: Canonical Structure | Low — this is a standard practitioner guideline. If wrong, the contrast clause is slightly over-broad but not harmful. |
| A2 | The "~30% increase in risk identification accuracy" figure for prospective hindsight | §Pre-Mortem: Canonical Structure | Low — cited from a secondary source (nesslabs.com citing Klein); the directional claim is sound. Do not put this percentage in the procedure file. |
| A3 | Bread-going-stale / dinner-party / laptop scenario recommendations | §Mini-Example Scenarios | None — these are under Claude's discretion (D-05). The planner can substitute freely. |
| A4 | Sensitivity check "~10% threshold" for trade-off near-ties | §Trade-Off Analysis: Canonical Structure | Low — this is a rule of thumb, not a formal threshold. Useful framing, but the exact number is discretionary. |

---

## Open Questions

1. **Procedure depth for 5-Whys branching tree**
   - What we know: the procedure is a branching cause tree, not a linear sequence; branches are
     explored one at a time; the stop criterion is per-branch.
   - What's unclear: whether to show the tree as a diagram, a numbered list, or prose. Given the
     ~100-line limit and no-table-of-contents constraint, a nested list is likely the only viable
     format without blowing the line budget.
   - Recommendation: use a nested bullet list for the mini-example; describe the branching
     procedure as numbered steps in imperative mood.

2. **Pre-mortem: solo vs. facilitated framing**
   - What we know: Gary Klein's original is a group facilitation technique; companion tools must
     be usable by a single analyst.
   - What's unclear: whether to present it as solo-first (with a note about group use) or
     group-first (with a solo adaptation note).
   - Recommendation: write the procedure as solo-compatible (independent writing, no room needed),
     since Claude applies this alone during an analysis. The group facilitation notes can appear
     briefly as a failure-mode contrast ("if facilitated: run before finalizing the plan, without
     senior authority in the room").

3. **Handoff wording: "5-phase spine" vs. specific phase**
   - What we know: CONTEXT.md fixes handoff targets — five-whys and trade-off → "5-phase spine";
     pre-mortem → "Phase 5 (Validate)" specifically.
   - What's unclear: whether "5-phase spine" should name specific phases (Phase 2 or Phase 4 for
     five-whys; Phase 4 for trade-off) or stay generic.
   - Recommendation: be specific. Five-whys feeds Phase 2 (Challenge Assumptions) when drilling
     on a Why-is-this-true question, or Phase 4 (Reason Upward) when drilling on a causal claim
     mid-derivation. Trade-off feeds Phase 4 (Reason Upward) when choosing between viable options.
     Naming the phase is more useful than "the 5-phase spine" — a reader knows where to return.

---

## Environment Availability

Step 2.6: SKIPPED — this phase is pure Markdown content authoring with no external tool or service
dependencies. The three files are written by hand; no CLI tools, compilers, databases, or runtimes
are required.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Manual review against ROADMAP success criteria (pure-Markdown skill; no automated test runner) |
| Config file | None |
| Quick run command | Read each file and check against SC-1 / SC-2 / SC-3 / SC-4 checklist |
| Full suite command | Apply `references/validation-rubric.md` scoring to each file; check all five ROADMAP components appear (D-03) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| TOOL-01 | five-whys.md has all 5 components; procedure is branching + test-based stop | Manual | Read file; verify stop criterion is test-based (not count-based); verify branching described | ❌ Wave 0 (fill stub) |
| TOOL-02 | pre-mortem.md has all 5 components; framing assumes failure already occurred | Manual | Read file; verify past-tense framing instruction appears as a mandatory step | ❌ Wave 0 (fill stub) |
| TOOL-03 | trade-off-analysis.md has all 5 components; weights locked before scoring | Manual | Read file; verify "lock weights before scoring" instruction appears as a discrete step | ❌ Wave 0 (fill stub) |
| SC-4 | No file contains YAML frontmatter | Manual / grep | `grep -n "^---" first-principles-thinking/references/five-whys.md first-principles-thinking/references/pre-mortem.md first-principles-thinking/references/trade-off-analysis.md` | ❌ Wave 0 (fill stub) |

Note: `nyquist_validation` is enabled in config.json; this pure-Markdown phase has no automated
test runner. Verification is gate-checked by the `/gsd:verify-work` step reading each file against
the ROADMAP success criteria.

### Sampling Rate

- **Per task commit:** Read the authored file; verify against its ROADMAP success criterion.
- **Per wave merge:** Read all three files; run the SC-4 frontmatter grep; verify all five ROADMAP
  components appear in each.
- **Phase gate:** All three files present, no frontmatter, all five components in each, SC-1/SC-2/SC-3
  disciplines encoded before `/gsd:verify-work`.

### Wave 0 Gaps

All three target files are stubs and must be authored in Wave 1:

- [ ] `first-principles-thinking/references/five-whys.md` — covers TOOL-01, SC-1
- [ ] `first-principles-thinking/references/pre-mortem.md` — covers TOOL-02, SC-2
- [ ] `first-principles-thinking/references/trade-off-analysis.md` — covers TOOL-03, SC-3

No test framework install needed. No shared fixtures. No config files.

---

## Security Domain

This phase authors pure Markdown files with no executable code, no user input handling, no
authentication, no cryptography, and no external service calls. ASVS categories V2–V6 do not apply.

The only integrity consideration relevant to this project's security model is:

> Methodology that defers to "common knowledge" as ground truth encodes unverified claims
> as fact — an integrity flaw, not a CVE.

Per PITFALLS.md Security Mistakes: the companion tool files must not use analogy-as-evidence or
appeal to "standard practice" as a justification without a verifiable source. The research findings
for all three tools are cited above and tagged appropriately.

---

## Sources

### Primary (HIGH confidence)

- `first-principles-thinking/SKILL.md` — existing nav-map link text, companion tool descriptions,
  Phase 5 Validate definition (handoff target for pre-mortem)
- `.planning/phases/04-companion-tool-references/04-CONTEXT.md` — locked decisions D-01 through
  D-08, success criteria SC-1 through SC-4, canonical refs list
- `.planning/ROADMAP.md` §Phase 4 — phase goal, success criteria, requirements TOOL-01/02/03
- `.planning/research/PITFALLS.md` — Pitfall 7 (scope creep), Integration Gotchas (reference file
  length, no YAML frontmatter on companion tools), Performance Traps

### Secondary (MEDIUM confidence)

- [reliamag.com — 5 Whys Root Cause Analysis: When to Stop Asking Why in Maintenance](https://reliamag.com/articles/5-whys-root-cause-analysis-maintenance/) — Corrective Action Test, Organizational Boundary Check, branching procedure, link-validation requirement. MEDIUM (practitioner domain, consistent with multiple sources).
- [nesslabs.com — Pre-mortem: how to anticipate failure with prospective hindsight](https://nesslabs.com/pre-mortem-anticipate-failure-with-prospective-hindsight) — prospective hindsight mechanism, ~30% accuracy improvement claim, framing instruction, timing guidance.
- [get-alfred.ai — The Pre-Mortem: Gary Klein's Technique for Killing Bad Plans Before They Kill You](https://get-alfred.ai/blog/pre-mortem-technique) — Klein's procedure (silent writing → round-robin → pattern), senior-presence failure mode.
- [goalsandprogress.com — Weighted decision matrix](https://goalsandprogress.com/weighted-decision-matrix/) — weights-before-scoring rule as the primary structural countermeasure.
- [deckary.com — Decision Matrix Guide](https://deckary.com/blog/decision-matrix-guide) — 5–8 criteria recommendation.
- [strategicdecisionsolutions.com — Premortem Method](https://strategicdecisionsolutions.com/premortem-method/) — "definitively failed" framing; grammatical shift is not rhetorical.
- [flowfuse.com — Five Whys Root Cause Analysis](https://flowfuse.com/blog/2025/12/five-whys-root-cause-analysis-definition-examples/) — when NOT to use 5-Whys (complex multi-system failures).

### Tertiary (LOW confidence — not used for structural decisions)

- [easyrca.com — Common Limitations of 5-Whys Analysis](https://easyrca.com/blog/common-limitations-of-5-whys-analysis-and-how-to-avoid-them/) — confirmation bias, multiple-cause limitations (corroborates primary findings).

---

## Metadata

**Confidence breakdown:**
- Tool canonical structures: HIGH — multiple cross-referencing sources converge; consistent with the CONTEXT.md decisions
- Stop criterion / framing discipline / weights-before-scoring rule: HIGH — each is the documented best practice directly corresponding to the ROADMAP success criterion
- Mini-example scenario recommendations: ASSUMED (Claude's discretion under D-05)
- Handoff wording recommendations: ASSUMED (Claude's discretion under D-02); targets are fixed by CONTEXT.md

**Research date:** 2026-05-17
**Valid until:** 2026-07-17 (these are stable, mature techniques; 60-day window)
