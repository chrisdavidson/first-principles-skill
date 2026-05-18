---
phase: 05-domain-spread-worked-examples
plan: "04"
subsystem: documentation
tags: [first-principles, worked-example, science-engineering, solar-sizing, GT-N?, markdown]

requires:
  - phase: 03-validation-rubric
    provides: validation-rubric.md — the six criteria this example must clear
  - phase: 01-sharpen-methodology
    provides: output-template.md — the six-section format all examples follow

provides:
  - "EX-04: science/engineering worked example — six-section first-principles analysis of off-grid solar sizing with physics-anchored quantitative chains and a genuine GT-5? unverified input"

affects: [06-navigation-wiring, any plan that reads examples/ to calibrate format and rigor]

tech-stack:
  added: []
  patterns:
    - "GT-N? notation: unverified input elevated for use in derivation chains, with MEDIUM confidence and explicit verification path on every consuming chain"
    - "Load breakdown table in Ground Truths section as auditable basis for the GT-N? input"
    - "Quantitative derivation chains with explicit unit-conversion intermediate steps (Wh/day arithmetic)"

key-files:
  created: []
  modified:
    - "first-principles-thinking/examples/science-engineering.md — EX-04 complete six-section analysis (190 lines)"

key-decisions:
  - "D-01: Off-grid solar sizing (panel array + battery bank) is the locked science/engineering problem — no substitution"
  - "D-03: Deepest sections are Ground Truths (GT-5? with load table) + Derivation Chains (quantitative unit arithmetic)"
  - "D-04: GT-5? is genuine here — the daily energy load cannot be verified without a monitoring period"
  - "D-07: No inline rubric verdict blocks in the example file — scoring recorded in SUMMARY only"

patterns-established:
  - "GT-N? pattern: unverified input in Ground Truths with explicit unverified: clause naming WHY it cannot be verified, load breakdown table as derivation basis, MEDIUM confidence on every consuming chain, verification path stated"

requirements-completed: [EX-04]

duration: 10min
completed: 2026-05-18
---

# Phase 05 Plan 04: Science/Engineering Worked Example Summary

**Off-grid solar sizing analysis (EX-04): physics-anchored quantitative chains with GT-5? unverified daily load, MEDIUM-confidence sizing outputs, and peak-load dead-end — the only example using GT-N? notation**

## Performance

- **Duration:** ~10 min
- **Started:** 2026-05-18T03:07:00Z
- **Completed:** 2026-05-18T03:17:26Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments

- Authored the complete six-section EX-04 analysis of the locked off-grid solar sizing
  problem: 400 W panel array and 6 kWh LiFePO4 battery bank, derived from NREL PSH data,
  system derating factor, LiFePO4 DoD limit, and the 3-day autonomy design decision.
- Implemented the GT-5? pattern correctly: daily energy load (~1.5 kWh/day) is the only
  genuinely unverifiable input in the four examples; both sizing chains consume it and
  both end with MEDIUM confidence and identical verification paths (30-day energy monitor).
- Documented the peak-instantaneous-load dead-end, showing that 250 W pump × 24 h =
  6 kWh/day (4× the actual load) — making the structural wrongness quantitative, not vague.
- EX-04 clears the validation rubric gate: all six criteria score Rigorous.

## Task Commits

1. **Task 1: Author EX-04 six-section analysis** — `07b645e` (feat)
2. **Task 2: Score EX-04 against validation rubric** — no file changes; scoring recorded here; gate cleared

## Files Created/Modified

- `first-principles-thinking/examples/science-engineering.md` — Complete EX-04 analysis
  replacing the 3-line stub; 190 lines; H1 preserved verbatim

## Decisions Made

- Placed the per-appliance load breakdown table inside Section 3 (Ground Truths) as the
  visible derivation of GT-5?, per RESEARCH.md Open Question 1 recommendation — this makes
  the unverified input's basis auditable without moving it to Section 4.
- Kept the 400 W recommendation slightly undersized for worst-case winter PSH (~4.5 h)
  and documented it as a trade-off in Section 6, rather than recommending an oversized
  array — more realistic to how a practitioner would size.
- Named all GT-IDs explicitly in the Section 6 Conclusion paragraph to satisfy Criterion 6
  (every Conclusion claim traces to named GTs via chains in Section 4).

## Deviations from Plan

None — plan executed exactly as written.

## Validation Rubric Scoring (Task 2 — recorded here, not in the example file per D-07)

**Criterion 1: Identify Essence**
Quoted span: "Given a fixed site (high-desert New Mexico, 35° N, year-round occupancy by 2 adults, no grid connection), what panel array capacity and battery bank capacity are required to meet the cabin's daily electrical load reliably?"
Band: **Rigorous**
Justification: Single sentence naming the core sizing question (not the triggering event or a symptom); four success criteria are checkable conditions verifiable against the Conclusion without asking the analyst for clarification.

**Criterion 2: Challenge Assumptions**
Quoted span: "| The daily energy load is approximately 1.5 kWh/day | untested belief | Flag as unverified; may be used in chains but must carry GT-5? notation; any conclusion depending on it inherits MEDIUM confidence and a stated verification path | Accept | unverified — flagged |"
Band: **Rigorous**
Justification: Every row uses a Type drawn from the four-type scheme; Treatment cells match the prescribed vocabulary for each type; the untested belief used in chains carries "unverified — flagged"; the discarded assumption (peak-load sizing) is present with Verdict: Discard.

**Criterion 3: Establish Ground Truths**
Quoted span: "- **GT-5?** Daily energy load estimate: approximately 1.5 kWh/day — unverified: this figure is derived from the per-appliance load breakdown below, which depends on occupant behavior (actual hours of use), seasonal variation..."
Band: **Rigorous**
Justification: GT-1 through GT-5? carry stable IDs matching Section 4 references; GT-1 through GT-4 have specific source citations (NREL, NABCEP, manufacturer specs, design constraint); GT-5? carries the `?` suffix with a specific unverified clause naming WHY the input cannot be verified; no discarded assumption appears in the list.

**Criterion 4: Reason Upward**
Quoted span: "GT-2 (0.80 derating factor) + GT-5? (1.5 kWh/day estimated load)\n→ Required daily panel output = 1.5 kWh ÷ 0.80 = 1,875 Wh/day\n  (Neither GT-2 nor GT-5? alone specifies how many watt-hours the panels must generate; combining them via the energy-conservation relationship yields the gross generation target.)"
Band: **Rigorous**
Justification: Two conclusions in Section 6, exactly two chains in Section 4; each chain has a genuine intermediate step explicitly called out as a new claim not statable from either GT alone; the dead-end uses the What-was-tried / Why-abandoned / What-it-ruled-out structure with a specific, quantitative abandonment reason; no analogy-as-evidence moves.

**Criterion 5: Validate**
Quoted span: "**Confidence: MEDIUM** — GT-5? (daily energy load estimate of 1.5 kWh/day) is unverified. If measured load consistently exceeds 1.8 kWh/day, the required panel capacity exceeds 400 W and the array must be upsized (e.g., to 3 × 200 W = 600 W). Verification: install energy monitor for 30 days; confirm measured load before finalizing the array specification."
Band: **Rigorous**
Justification: Both GT-5?-consuming chains end with MEDIUM confidence lines naming GT-5? and stating a specific verification path; neither is rated HIGH; Section 6 Conclusion confidence is MEDIUM, names GT-5? as the cause, and states the verification path to raise it to HIGH.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "These sizes are derived from the site's 5.5 PSH annual average (GT-1), the 0.80 system derating factor (GT-2), the 80% DoD limit of LiFePO4 chemistry (GT-3), the 3-day autonomy target (GT-4), and the estimated 1.5 kWh/day daily load (GT-5?)."
Band: **Rigorous**
Justification: Every Conclusion claim (400 W array, 6 kWh bank, MEDIUM confidence, trade-offs) traces to named chains in Section 4; the Key Insight (daily energy throughput vs peak power as the correct sizing variable, and load estimate as dominant uncertainty) is a non-obvious finding that peak-power reasoning would have missed; no new claims appear in Section 6.

**Gate result:** No criterion Absent. Zero criteria Hand-wavy. All six criteria Rigorous. Gate CLEARED.

## Known Stubs

None — the analysis is complete and all sizing numbers trace to named ground truths or derivation chains. GT-5? is explicitly flagged as unverified (not a stub — it is a genuine unverifiable input that the methodology handles via the confidence-caveat mechanism).

## Threat Flags

None — pure Markdown skill content, no attack surface.

## Issues Encountered

None.

## Next Phase Readiness

- EX-04 is complete and clears the validation rubric gate.
- The science-engineering.md file is ready for Phase 6 navigation wiring (adding a link
  from SKILL.md to the example).
- All four phase-5 example files now exist; phase 5 is complete when all four clear
  their individual rubric gates.

---
*Phase: 05-domain-spread-worked-examples*
*Completed: 2026-05-18*
