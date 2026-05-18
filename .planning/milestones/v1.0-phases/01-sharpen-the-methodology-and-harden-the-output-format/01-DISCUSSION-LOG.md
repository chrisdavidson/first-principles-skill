# Phase 1: Sharpen the Methodology and Harden the Output Format - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-16
**Phase:** 1-Sharpen the Methodology and Harden the Output Format
**Areas discussed:** Output template strictness, Reason Upward's freedom, Assumption-class actions, Methodology test-run

---

## Output Template Strictness

### Section completeness enforcement

| Option | Description | Selected |
|--------|-------------|----------|
| Strict shape, honest depth | All sections present and in order, but a section may be marked 'Nothing material here — [reason]' when justified. Strict shape, flexible depth, prevents box-ticking. | ✓ |
| Every section mandatory | Every section must be substantively filled, no exceptions. Risks box-ticking — Claude pads empty sections. | |
| Core required, rest optional | Only assumptions table + traceability map + conclusion mandatory; per-phase sections optional. Weakens the auditable trace. | |

**User's choice:** Strict shape, honest depth

### Traceability map form

| Option | Description | Selected |
|--------|-------------|----------|
| Explicit linking table | A table: each conclusion row lists the ground-truth IDs it derives from. Most auditable at a glance. | |
| Inline ID citations | Conclusions as prose with bracketed ground-truth IDs inline. Reads naturally, harder to audit completeness. | |
| Derivation chains | Each conclusion shown as a step chain: GT-1 + GT-2 → intermediate → conclusion. Richest, but verbose. | ✓ |

**User's choice:** Derivation chains

### Home for abandoned reasoning

| Option | Description | Selected |
|--------|-------------|----------|
| Dedicated section | The template includes an explicit 'Abandoned Reasoning' / 'Dead Ends' section. | ✓ |
| Inline in Challenge Assumptions | Dead-ends live inside the Challenge Assumptions phase output. No separate section. | |
| No required home | The template doesn't mandate it; examples show dead-ends wherever they occur. | |

**User's choice:** Dedicated section

**Notes:** Choices consistently favor strict, auditable structure while leaving an honest escape valve to avoid box-ticking (research Pitfall 2).

---

## Reason Upward's Freedom

### Where the freedom lives

| Option | Description | Selected |
|--------|-------------|----------|
| Free method, fixed boundaries | Entry/exit criteria and a named artifact, but no prescribed sub-steps for HOW to reason upward. | |
| Genuinely unstructured | Prose guidance only — no mandatory artifact, no hard exit gate. | |
| Free but self-documenting | No prescribed sub-steps, but Claude must narrate its own reasoning path as it goes. | ✓ |

**User's choice:** Free but self-documenting

### Exit criterion

| Option | Description | Selected |
|--------|-------------|----------|
| Every conclusion traced | Done when every conclusion has a complete self-documented derivation chain back to ground truths. | |
| Core question answered | Done when the central question has at least one candidate answer built from ground truths. | |
| Both: traced AND answered | Done when the core question is answered AND every conclusion offered is fully traced. Strictest. | ✓ |

**User's choice:** Both: traced AND answered

**Notes:** Freedom is in the method, not the boundaries — the phase keeps a hard exit gate and mandatory transparency.

---

## Assumption-Class Actions

### Whether categories prescribe treatment

| Option | Description | Selected |
|--------|-------------|----------|
| Each maps to an action | Classification prescribes what to do per category (accept / record-expiry / challenge / verify-or-flag). | |
| Diagnostic labels only | Categories help see the assumption type; each analysis decides case-by-case. | |
| Action + escalation | Each maps to an action, plus: higher stakes force the assumption down toward physical law / verified ground truth. | ✓ |

**User's choice:** Action + escalation

### Unverified assumptions in a derivation chain

| Option | Description | Selected |
|--------|-------------|----------|
| Allowed but flagged | A chain may include an unverified node, visibly marked; dependent conclusions inherit a confidence caveat. | ✓ |
| Verified ground truths only | A conclusion may derive only from verified ground truths; unverified ones resolved or dropped. | |
| Allowed, with a verification to-do | Like 'allowed but flagged', plus each unverified node listed as an explicit follow-up. | |

**User's choice:** Allowed but flagged

**Notes:** Rigor scales with stakes; uncertainty is made visible rather than eliminated or hidden.

---

## Methodology Test-Run

### Sample problem

| Option | Description | Selected |
|--------|-------------|----------|
| Dogfood a project decision | Apply the methodology to a real open design decision from this skill build. Serves PROJECT.md's dogfooding goal. | ✓ |
| Neutral generic problem | A standalone classic first-principles case unrelated to the project. | |
| Throwaway, smallest viable | The smallest problem that exercises all 5 phases. Purely proves the machinery. | |

**User's choice:** Dogfood a project decision

### Fate of the test-run

| Option | Description | Selected |
|--------|-------------|----------|
| Verification only, discarded | Proves the methodology works, then discarded — lives only in the verification record. | |
| Kept as a working draft | Saved in .planning/ as a reference draft Phase 5 can later polish. Not shipped as-is. | ✓ |
| Kept and shipped | The test-run becomes a real examples/ file. Risk: pulls Phase 5 scope into Phase 1. | |

**User's choice:** Kept as a working draft

**Notes:** Dogfooding satisfies a stated PROJECT.md goal; keeping the draft avoids redoing the work in Phase 5 without shipping example content prematurely.

---

## Claude's Discretion

- Exact wording of each phase's entry/exit criteria and the precise names of each phase's output artifact.
- How the per-phase artifacts accumulate into the final output document.
- The phrasing of each phase's rationale statement (METH-06).
- The exact section list and ordering of the output template, beyond the mandated assumptions table, derivation-chain traceability map, and Abandoned Reasoning section.
- Which specific open project design decision is chosen as the test-run subject.

## Deferred Ideas

None — discussion stayed within phase scope. Scope-adjacent items (validation rubric, companion tools, shipped worked examples, `SKILL.md` and frontmatter) belong to Phases 2–6 and were not pulled forward.
