---
phase: 04-companion-tool-references
verified: 2026-05-17T23:59:00Z
status: passed
score: 4/4 must-haves verified
overrides_applied: 0
re_verification:
  previous_status: human_needed
  previous_score: 4/4
  gaps_closed:
    - "WR-01: Trade-off example used 4 criteria, violating the 5–8 procedure mandate — expanded to 6 criteria (commit ec0f209)"
    - "WR-02: 'Reliability risk' criterion name contradicted higher-is-better scale — renamed to 'Reliability' and Step 4 now carries explicit higher-is-better instruction (commit ec0f209)"
    - "WR-03: Five-whys example showed lateral scan only at level 1, demonstrating Single-thread drilling at deeper levels — considered-and-rejected alternate causes added at level 2 in both branches (commit 3593c23)"
  gaps_remaining: []
  regressions: []
---

# Phase 4: Companion Tool References Verification Report

**Phase Goal:** Three companion thinking tools — 5-Whys, pre-mortem, and trade-off analysis — exist as self-contained `references/` components, each fully usable as a sub-procedure and promotion-ready for the future milestone-2 split.
**Verified:** 2026-05-17T23:59:00Z
**Status:** passed
**Re-verification:** Yes — after gap closure (WR-01, WR-02, WR-03 fixed in commits ec0f209 and 3593c23)

---

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | `references/five-whys.md` is a usable component with when-to-use, a branching procedure with a test-based stop criterion, a mini-example, failure modes, and an explicit handoff to the 5-phase spine (ROADMAP SC-1, TOOL-01) | VERIFIED | File at 98 lines; all five `##` sections present; stop criterion is the Corrective Action Test — "Five is a typical depth, not a rule. Stop when the test is met, not when the count is reached"; branching instruction "What else caused this?" present in the procedure and demonstrated at level 2 of both example branches (WR-03 fix); Handoff names Phase 2 and Phase 4 |
| 2 | `references/pre-mortem.md` is a usable component with prospective-hindsight framing, a procedure, a mini-example, failure modes, and an explicit handoff to Phase 5 (Validate) (ROADMAP SC-2, TOOL-02) | VERIFIED | File at 106 lines; six `##` sections present (adds `## Framing`); past-tense framing blockquote ("This plan has failed — not merely underperformed, but failed badly. That outcome is a fact.") precedes Procedure; Framing is re-invoked as Step 1 of the procedure; Handoff names Phase 5 (Validate) |
| 3 | `references/trade-off-analysis.md` is a usable component with a weighted-criteria-before-scoring procedure, a mini-example, failure modes, and a handoff to the 5-phase spine (ROADMAP SC-3, TOOL-03) | VERIFIED | File at 118 lines; all five `##` sections present; Step 3 "Assign weights. Lock them now." is a discrete ordered step preceding Step 4 (scoring); rationale for locking stated in both the scope callout and the procedure step; example has 6 criteria (WR-01 fix); all criteria phrased higher-is-better with Step 4 carrying the explicit instruction (WR-02 fix); arithmetic correct (A=64, B=82, verified independently); Handoff names Phase 4 (Reason Upward) |
| 4 | No companion tool file carries its own YAML frontmatter (ROADMAP SC-4) | VERIFIED | All three files begin with `# <Title>` as first line; first `---` in each file is a section divider at line 7, not a frontmatter fence; no `---` block appears above any H1 |

**Score:** 4/4 truths verified

---

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `first-principles-thinking/references/five-whys.md` | 5-Whys companion tool component; contains `## Procedure` | VERIFIED | 98 lines; frontmatter-free; sections: When to reach for this, Procedure, Example, Failure modes, Handoff |
| `first-principles-thinking/references/pre-mortem.md` | Pre-mortem companion tool component; contains `## Framing` | VERIFIED | 106 lines; frontmatter-free; sections: When to reach for this, Framing, Procedure, Example, Failure modes, Handoff |
| `first-principles-thinking/references/trade-off-analysis.md` | Trade-off analysis companion tool component; contains `## Procedure` | VERIFIED | 118 lines; frontmatter-free; sections: When to reach for this, Procedure, Example, Failure modes, Handoff |

---

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `five-whys.md` | Phase 2 (Challenge Assumptions) / Phase 4 (Reason Upward) | Handoff section | WIRED | Names both phases and both artifacts (Classified Assumptions Table; Derivation Chain) matching SKILL.md |
| `pre-mortem.md` | Phase 5 (Validate) | Handoff section | WIRED | "The probable failure causes identified here feed Phase 5 (Validate)"; names the adversarial validation pass artifact |
| `trade-off-analysis.md` | Phase 4 (Reason Upward) | Handoff section | WIRED | "Return to Phase 4 (Reason Upward)"; names the Derivation Chain artifact |
| `SKILL.md` nav-map | All three reference files | Lines 165–167: direct relative links | WIRED | Links at `references/five-whys.md`, `references/pre-mortem.md`, `references/trade-off-analysis.md` with trigger phrases verified present |

---

### WR-01 and WR-02 Fixes Verified (trade-off-analysis.md, commit ec0f209)

**WR-01 — Criteria count fixed:** Example now has 6 criteria (Performance, Reliability, Cost, Warranty/support, Portability, Ease of setup), satisfying the 5–8 mandate from Step 2 of the procedure. The previous state (4 criteria) directly contradicted the procedure's lower bound; the example now models compliance.

**WR-02 — Scale direction fixed:** Step 4 now reads: "Phrase every criterion so that a higher score is always more desirable (e.g., use 'Reliability' not 'Reliability risk'). A scale where higher is sometimes better and sometimes worse silently inverts the result." The criterion is renamed from "Reliability risk" to "Reliability" throughout the example, eliminating the ambiguity.

**Arithmetic verification (computed independently):**
- Option A (Refurb): (4×4)+(2×5)+(5×3)+(2×4)+(3×2)+(3×3) = 16+10+15+8+6+9 = **64** — matches file
- Option B (New): (2×4)+(5×5)+(3×3)+(5×4)+(4×2)+(4×3) = 8+25+9+20+8+12 = **82** — matches file

Both totals are correct. The code review summary note referencing "A = 49, B = 62" described the pre-fix 4-criterion version and is superseded.

---

### WR-03 Fix Verified (five-whys.md, commit 3593c23)

**WR-03 — Lateral scan at deeper levels fixed:** The example now shows considered-and-rejected alternate causes at level 2 in both branches:

- Branch 1, level 2: "Why else? — considered: the household eats less bread than it used to; rejected, weekly bread consumption has not changed — only the loaf size on offer has."
- Branch 2, level 2: "Why else? — considered: the bag itself is defective and will not seal; rejected, the bag seals fine when the clip is used — the issue is that the clip is not at hand."

The example now models the procedure's branching mandate at depth, not just at level 1. The "Single-thread drilling" anti-pattern is no longer demonstrated by the canonical example.

---

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|---------|
| TOOL-01 | 04-01-PLAN.md | `references/five-whys.md` — branching procedure with test-based stop criterion, mini-example, failure modes, handoff | SATISFIED | All components present and correct; lateral scan demonstrated at depth (WR-03 fix) |
| TOOL-02 | 04-02-PLAN.md | `references/pre-mortem.md` — prospective-hindsight framing, procedure, mini-example, failure modes, handoff to Phase 5 | SATISFIED | Framing is mandatory first step before Procedure; past-tense blockquote present |
| TOOL-03 | 04-03-PLAN.md | `references/trade-off-analysis.md` — weighted-criteria-before-scoring, mini-example, failure modes, handoff | SATISFIED | Lock-weights step (Step 3) precedes scoring (Step 4); 6-criteria example obeys procedure; arithmetic correct |

Note: TOOL-04 is assigned to Phase 6 by the REQUIREMENTS.md Traceability table — not a gap for Phase 4. The SKILL.md nav-map links already exist and resolve correctly.

**Orphan check:** REQUIREMENTS.md assigns only TOOL-01, TOOL-02, TOOL-03 to Phase 4. No orphaned requirements.

---

### Anti-Patterns Found

No debt markers (TBD, FIXME, XXX, TODO, HACK, PLACEHOLDER) found in any of the three deliverable files. No stub patterns, no empty implementations. The `trade-off-analysis.md` file at 118 lines slightly exceeds the "roughly under 100 lines" D-06 guideline — the expansion was a required fix for WR-01 (adding two criteria with table rows) and the file remains substantive throughout with no filler.

---

### Data-Flow Trace (Level 4)

Not applicable — pure-Markdown static content; no data sources, state variables, or dynamic rendering.

---

### Behavioral Spot-Checks

Not applicable — no runnable code by design (pure-Markdown constraint). Step 7b skipped.

---

### Probe Execution

No probes declared in any plan file. No `scripts/*/tests/probe-*.sh` present. Step 7c skipped.

---

### Human Verification Required

None. All consistency defects identified in the code review have been resolved in code. The phase goal is fully verified.

---

### Gaps Summary

No gaps. All four ROADMAP success criteria are VERIFIED. The three code-review warnings (WR-01, WR-02, WR-03) are confirmed resolved in commits ec0f209 and 3593c23. The phase goal is achieved.

---

_Verified: 2026-05-17T23:59:00Z_
_Verifier: Claude (gsd-verifier)_
_Re-verification: Yes — WR-01, WR-02, WR-03 closed_
