# Rubric Application: `analysis.md`

## Assumption Audit (verified before scoring)

Per "How to Apply This Rubric," I first confirm the audit table is present and exhaustive over every named derivation chain step in section 4.

- **Present:** Yes — the audit table appears in the validation appendix (analysis lines 156–166).
- **Coverage check** against section 4's named chains (A–E):

| Chain | Steps in §4 | Rows in audit | Match |
|---|---|---|---|
| A (ceiling) | ceiling calc; zero-loss forbidden | A/1, A/2 | ✓ in order |
| B (Fermi split) | conductances; 70% vs 47% | B/1, B/2 | ✓ in order |
| C (trade-off) | normalise ΔUA; $/annual-$ | C/1, C/2 | ✓ in order |
| D (unquoted option) | air-sealing $/yr | D/1 | ✓ |
| E (second-order) | penetrations buried; K&T precondition | E/1, E/2 | ✓ in order |

Every named chain step has a corresponding row, in order, with no step skipped, and the GT-9? row it surfaced was carried into the Assumptions Table before scoring. **The audit ran exhaustively.** Proceeding to verdict blocks.

---

**Criterion 1: Identify Essence**
Quoted span: *"which capital expenditure — if any — buys the most reduction in that spend per dollar committed?"*
Band: **Rigorous**
Justification: A single sentence naming the underlying decision (explicitly reframing away from the prompt's contractor-defined menu), followed by four success criteria each written as a verb+subject+outcome test scannable against section 6 (e.g., "states a dollar-per-annual-dollar-saved figure for each option") — specific to this problem, not a template phrase.

**Criterion 2: Challenge Assumptions**
Quoted span: *"Challenged and rejected. The menu is contractor-defined. Air leakage is a third path... and no one quoted it"*
Band: **Rigorous**
Justification: All 14 rows carry a Type from exactly the four-type scheme, Treatment cells use the prescribed vocabulary for each type, Verdicts record Accept/Challenge/Discard with multiple genuine Challenge and Discard verdicts, unverified-in-chain rows read "Unverified — flagged," and the audit-surfaced GT-9? row was added to the table before scoring.

**Criterion 3: Establish Ground Truths**
Quoted span: *"GT-8? ... Unverified for this house — population statistics from weatherization program data, not a measurement of your building."*
Band: **Rigorous**
Justification: Every GT carries a stable ID matching the chain references, verified GTs cite specific sources (Fourier's law/ASHRAE, NFRC ranges), all four unverified entries carry the `?` suffix, and no assumption assigned a Discard verdict in section 2 (attic-only menu, no-prerequisite, 25C credit) appears in the list.

**Criterion 4: Reason Upward**
Quoted span: *"the intermediate claim 'a better window price makes the project pay back' could not be established — reaching a 10-year payback... requires a total price near $3,100... and does not exist."*
Band: **Rigorous**
Justification: Section 4 provides one chain per conclusion in `GT → intermediate → conclusion` form with genuine intermediate inferences, section 5 documents three dead ends each with a structural What-tried / Why-abandoned / What-it-ruled-out reason (contradiction, unestablishable intermediate, discarded assumption), no analogy is used as standalone evidence, and every chain-surfaced assumption was routed into the table rather than left as an undeclared inline assumption.

**Criterion 5: Validate**
Quoted span: *"Confidence: HIGH despite the GT-6? input, because the conclusion (no payback in horizon on the combined program) survives across the full plausible range of GT-6?."*
Band: **Sound**
Justification: Confidence ratings and named weakest links are present on Chains A–D, but Chain A is rated HIGH confidence while consuming the unverified GT-6? input — the exact departure the Sound descriptor names ("a chain is rated HIGH confidence while consuming a GT-N? input") — and Chain E (load-bearing for the sequencing conclusion) names no weakest link at all; these are specific, identifiable shortfalls that do not invalidate the rest of the validation pass. *(No double-count: GT-6? correctly carries its `?` suffix, so this is not a C2/C3 defect — it is solely the C5 confidence-rating rule.)*

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: *"consider that storm windows or interior inserts capture roughly 50–70% of the triple-pane gain for 15–25% of the cost."*
Band: **Sound**
Justification: Nearly every Conclusion claim cites its originating chain inline and the Key Insight ("nobody sized them to the bill") is a genuinely non-obvious finding from Chain A rather than a restatement of the recommendation — but this quantitative storm-window/insert claim is introduced for the first time in section 6 with no supporting derivation chain in section 4, matching the Sound descriptor's "one claim is introduced for the first time in the Conclusion section."

---

**Gate:** No criterion scored Absent — gate cleared. **Hand-wavy cap:** zero criteria at Hand-wavy — cap cleared. **Result: PASS.**

=== QUALITY-HARNESS-SCORELINE-START ===
C1: Rigorous
C2: Rigorous
C3: Rigorous
C4: Rigorous
C5: Sound
C6: Sound
Verdict: PASS
=== QUALITY-HARNESS-SCORELINE-END ===