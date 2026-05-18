# Phase 5: Domain-Spread Worked Examples - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-17
**Phase:** 05-domain-spread-worked-examples
**Areas discussed:** Problem selection, Differentiation axis, Companion-tool integration, Depth & rubric scoring

---

## Problem Selection

### How the four problems are chosen

| Option | Description | Selected |
|--------|-------------|----------|
| Claude proposes a slate | Claude picks four concrete problems; user approves or swaps | ✓ |
| You specify each | User names the specific problem for each domain | |
| Reuse original repo cases | Anchor on original first-principles-skill cases where they fit | |

**User's choice:** Claude proposes a slate.

### Register of the problems

| Option | Description | Selected |
|--------|-------------|----------|
| Realistic, domain-authentic | Problems a real practitioner in that domain would actually face | ✓ |
| Accessible to any reader | Mechanics graspable without domain expertise | |
| Mixed by domain | Realistic where the domain rewards it, accessible where it doesn't | |

**User's choice:** Realistic, domain-authentic.

### Slate approval

Claude proposed: monolith→microservices (software), SaaS free tier (product/business),
relocate for a higher-paying job (personal/general), off-grid solar sizing (science/engineering).

| Option | Description | Selected |
|--------|-------------|----------|
| Approve all four | Lock the slate as proposed | ✓ |
| Swap software example | Pick a different software/systems problem | |
| Swap science example | Pick a different science/engineering problem | |
| Let me adjust freely | User describes which problems to change | |

**User's choice:** Approve all four.
**Notes:** Slate locked as D-01 in CONTEXT.md.

---

## Differentiation Axis

### Per-example methodology emphasis

Claude proposed: microservices = Phase 1 Essence + large Abandoned Reasoning; free tier =
Phase 2 Assumptions; relocation = Phase 1 Essence (stated-goal vs real-goal); solar =
Phases 3–4 Ground Truths + Derivation Chains + Phase 5 confidence caveats.

| Option | Description | Selected |
|--------|-------------|----------|
| Approve mapping | Lock the per-example emphasis | ✓ |
| Spread Essence wider | Re-assign so all four heaviest sections are distinct | |
| Let me adjust | User describes a different emphasis assignment | |

**User's choice:** Approve mapping.
**Notes:** Two Phase-1-heavy examples (microservices, relocation) accepted as intentional —
they demonstrate two distinct re-framing operations (symptom→cause vs stated-goal→real-goal).

### How far structural variety should go

| Option | Description | Selected |
|--------|-------------|----------|
| Natural variety only | Differences fall out of the problems; no contrivance | ✓ |
| Deliberately exercise edge cases | Force escape valve, GT-N?, competing conclusions, single chain across the four | |

**User's choice:** Natural variety only.

---

## Companion-Tool Integration

| Option | Description | Selected |
|--------|-------------|----------|
| Light touch — one or two examples | Brief note where a tool is a natural fit | |
| Pure 5-phase, no tools | Every example demonstrates only the 6-section output format | ✓ |
| Each example shows one tool | Cover all three companion tools across the four examples | |

**User's choice:** Pure 5-phase, no tools.
**Notes:** Companion tools already illustrated by their Phase 4 mini-examples; a second
procedure layer inside worked examples would dilute focus.

---

## Depth & Rubric Scoring

### Example length

| Option | Description | Selected |
|--------|-------------|----------|
| Substantial (~200-300 lines) | Room for a meaty analysis | |
| Tight (~120-180 lines) | Lean, minimal sufficient content | |
| No fixed target | Length follows each problem; planner sets a rough band per example | ✓ |

**User's choice:** No fixed target.

### Inline rubric verdict blocks

| Option | Description | Selected |
|--------|-------------|----------|
| Pure analysis, no verdict blocks | Each file is exactly the 6-section output format | ✓ |
| Append verdict blocks to each | Each file ends with its own 6 rubric verdict blocks | |
| One example shows scoring | Three pure analyses; one appends verdict blocks | |

**User's choice:** Pure analysis, no verdict blocks.
**Notes:** Passing the rubric is verified at verification time, not baked into the file.

---

## Claude's Discretion

- Specific framing, scenario details, and numbers within each locked problem.
- The content of each example's six sections (assumptions, ground truths, chains, dead-ends).
- The precise per-example length band.
- How many derivation chains and abandoned-reasoning entries each example carries (≥1 floor).
- Whether examples are authored one-per-plan or grouped, and the wave/dependency structure.

## Deferred Ideas

None — discussion stayed within phase scope. A self-referential "skill analyzing its own
design" example is already tracked as v2 requirement META-01 and is out of scope here.
