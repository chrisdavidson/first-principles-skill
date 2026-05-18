# Phase 3: Validation Rubric - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-17
**Phase:** 3-Validation Rubric
**Areas discussed:** Criterion coverage, Gate model strictness, Level scale, Fail-demonstration artifact, Cap threshold, Band names, Verdict form, Escape-valve scoring, Absent-verdict evidence

---

## Criterion Coverage & Granularity

| Option | Description | Selected |
|--------|-------------|----------|
| Lean 6 — one per phase + traceability | One criterion per phase plus a traceability criterion; each criterion does more work | ✓ |
| 7–8 — carve out rigor-critical sub-features | Extra slots give assumption-classification quality, dead-end honesty, or confidence-caveat discipline their own criterion | |

**User's choice:** Lean 6 — one per phase + traceability
**Notes:** Rigor-critical sub-features fold into the relevant per-phase criterion rather than getting standalone criteria.

---

## Gate Model Strictness

| Option | Description | Selected |
|--------|-------------|----------|
| Pure single-band gate | Only the lowest band fails; an analysis full of second-lowest scores still passes | |
| Gate + hand-wavy cap | Lowest band fails outright AND too many second-lowest scores also fail | ✓ |

**User's choice:** Gate + hand-wavy cap
**Notes:** Catches the "mediocre everywhere, terrible nowhere" analysis the single-band gate would pass.

---

## Level Scale Uniformity

| Option | Description | Selected |
|--------|-------------|----------|
| One shared 4-level scale across all criteria | Same named bands everywhere; descriptors stay criterion-specific | ✓ |
| Per-criterion tailored levels | Each criterion gets its own 3–4 level names fitted to what it measures | |

**User's choice:** One shared 4-level scale across all criteria

---

## Fail-Demonstration Artifact

| Option | Description | Selected |
|--------|-------------|----------|
| Embedded in validation-rubric.md as a worked fail-scoring example | The shipped rubric contains the weak analysis + worked scoring pass | |
| Separate .planning/ verification artifact | Weak analysis + scoring as a non-shipped verification draft (like Phase 1's test-run-draft.md) | ✓ |
| Shipped examples/-style file | A standalone shipped file demonstrating a failed analysis | |

**User's choice:** Separate .planning/ verification artifact
**Notes:** Mirrors Phase 1's verification-artifact pattern; keeps the shipped rubric lean and avoids a file outside the nav map.

---

## Cap Threshold

| Option | Description | Selected |
|--------|-------------|----------|
| Strict — 2 or more hand-wavy fails | Aggressive; 2+ second-lowest scores force revision | |
| Moderate — 3 or more (half the criteria) fails | Tolerates 2 hand-wavy criteria; 3+ forces revision | |
| Let research/planner set it | Defer the exact number to the analytic-rubric research pass | ✓ |

**User's choice:** Let research/planner set it
**Notes:** CONTEXT.md locks that a cap exists and what it must catch; research justifies the threshold.

---

## Band Names

| Option | Description | Selected |
|--------|-------------|----------|
| Lock the stub names | Use Rigorous / Adequate / Hand-wavy / Absent | |
| Leave naming to the planner | Lock the 4-level structure and gate/cap mechanics; planner chooses final labels | ✓ |

**User's choice:** Leave naming to the planner

---

## Verdict Form (evidence-quoting, VALID-04)

| Option | Description | Selected |
|--------|-------------|----------|
| Per-criterion verdict block | Each criterion gets a self-contained block: quoted span + band + one-line justification | ✓ |
| Single scoring table with a quote column | One compact table for all 6 verdicts | |
| Leave format to the planner | Lock the verdict contents; planner chooses block vs table | |

**User's choice:** Per-criterion verdict block
**Notes:** Makes every verdict unmissable and auditable on its own.

---

## Escape-Valve Scoring

| Option | Description | Selected |
|--------|-------------|----------|
| Rubric judges the reason's genuineness | An escape-valved section scores top band only if the rubric confirms the reason is genuine | ✓ |
| Escape valve auto-passes that criterion | A properly-formatted "Nothing material here" satisfies the criterion without second-guessing | |

**User's choice:** Rubric judges the reason's genuineness
**Notes:** The escape valve is not a free pass — the rubric is the mechanism that stops it being abused.

---

## Absent-Verdict Evidence

| Option | Description | Selected |
|--------|-------------|----------|
| Cite the gap explicitly | The verdict names what is missing and where it should have appeared; the absence is the evidence | ✓ |
| Quote the nearest failing span | Quote whatever partial/flawed content is closest and mark it Absent | |

**User's choice:** Cite the gap explicitly

---

## Claude's Discretion

- The exact hand-wavy cap threshold (deferred to the phase researcher, who must justify it).
- The final 4 band labels.
- The wording of each criterion and its 4 observable level descriptors.
- Criterion ordering within the rubric.
- The precise construction of the weak sample analysis and how concisely the shipped rubric demonstrates the verdict-block format.

## Deferred Ideas

None — discussion stayed within phase scope.
