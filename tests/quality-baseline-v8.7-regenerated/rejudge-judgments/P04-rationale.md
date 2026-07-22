I read both files in full. Scoring below is my own independent pass; the analysis's own "Appendix: Rubric Validation" is treated as document content to be scored, not as evidence of its own bands.

*(Housekeeping, unrelated to this task: the claude.ai Gmail, Calendar, and Drive connectors are unauthorized and unusable in this non-interactive session — authorize them via claude.ai connector settings if you need them.)*

---

## Assumption Audit

Scan performed over every step of every derivation chain in section 4 (Chains 1–5), naming assumptions each step requires that are **not** already in the section-2 Assumptions Table.

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| Chain 1 (conductive saving per option) | 1 | Roof presents 3× the loss area of glazing at comparable-or-larger ΔU | Cold-roof design with accessible joists, not a room-in-roof | yes (declared inline `[Assumes:]`) |
| Chain 1 | 2 | 45 m² × ΔU and 15 m² × ΔU are compared as directly commensurable W/K | **Ceiling and window sit under the same ΔT** — a cold-roof ceiling faces a buffered loft void, not outdoor air, so its effective ΔT is lower than the glazing's | **no** — not in table, not declared inline |
| Chain 1 | 3 | Attic upper bracket 96 W/K ≈ 2× windows' 51 W/K; lower bracket 11 vs 24 | none (arithmetic on GT-3 and GT-7?) | n/a |
| Chain 2 (cost-effectiveness) | 1 | W/K × 55,000 K·h ÷ 0.85 × £0.07 → £/yr | **Full savings are banked as fuel rather than taken as raised indoor temperature** (comfort take-back) | **no** — not in table, not declared inline |
| Chain 2 | 2 | Worst attic branch (£73/W/K) beats best window branch (£196/W/K) by ~2.7× | No grant/subsidy asymmetry between the options | yes (declared inline `[Assumes:]`) |
| Chain 2 | 3 | GT-5?/GT-6? change size, not direction, of the win | Exhaustive over the 2×2 depth/glazing branch table — but **GT-7? (areas) is held fixed, not branched**; the invariance claim does not cover it | **no** — the un-branched status of GT-7? is undeclared |
| Chain 3 (draughts) | 1 | Hatch and ceiling penetrations leak disproportionately via stack effect | Whole-house infiltration ≈0.6 ach at ~220 m³ ≈ 44 W/K | yes (declared inline `[Assumes:]`) |
| Chain 3 | 2 | A £150–300 package removes ~⅕ of infiltration ≈ 9 W/K | **An open chimney exists** (the package is costed with a chimney balloon); **and the ⅕ share is itself an estimate with no stated basis** | **no** |
| Chain 4 (trade-off matrix) | 1 | Weights locked before scoring; attic wins the two highest-weighted criteria | **The analyst's weight vector represents the user's priorities** — weights were never elicited (AskUserQuestion unavailable per the preamble) | **no** — load-bearing for Chain 4's entire result |
| Chain 4 | 2 | 103:63 margin is outside a ~10% sensitivity band | none (arithmetic on the stated weights) | n/a |
| Chain 5 (second-order) | 1 | Colder loft → condensation/timber-decay risk | none (GT-11 direct) | n/a |
| Chain 5 | 2 | Freeze risk to tank and pipework in the loft | **A cold-water tank / pipework is present in this loft, and eaves ventilation currently exists to be blocked** | **no** |
| Chain 5 | 3 | Windows relocate the problem to un-insulated surfaces | none (GT-12 + GT-1 direct) | n/a |

**Audit result:** the document's own audit table (in its appendix) records 3 surfaced assumptions and marks the remaining steps "none." This independent scan finds **five further assumptions** that chain steps require and that appear neither in the Assumptions Table nor as inline `[Assumes:]` tokens — the ceiling/window ΔT equivalence (Chain 1), comfort take-back (Chain 2), GT-7? being held fixed rather than branched (Chain 2), the chimney/⅕-share basis (Chain 3), and the provenance of the trade-off weights (Chain 4). These are carried forward into the scoring of Criteria 2, 4, and 5 under the precedence rule.

---

## Verdict Blocks

**Criterion 1: Identify Essence**
Quoted span: *"Given one non-repeatable capital spend, which fabric intervention buys the most reduction in heat loss and the most improvement in top-floor thermal comfort per pound — noting that 'draughty' is an air-leakage symptom that neither option is primarily designed to fix?"*
Band: **Rigorous**
Justification: A single sentence that names the underlying capital-allocation decision rather than the triggering symptom, explicitly separates conductive from advective loss, and could not be transplanted into a different analysis unmodified; each of SC-1 through SC-5 is a verb + subject + outcome test whose outcome is a scannable property of section 6 ("names exactly one of {attic, windows}", "states a quantified heat-loss reduction (W/K) for each option"), applicable with no analyst interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span: *"A-4 | The roof plane is the largest single loss area on the top floor and sits under the greatest ΔT (stack effect drives warm air upward) | physical law | Accept | Accept | Buoyancy: warm air is less dense…"*
Band: **Sound**
Justification: The table is structurally complete — all 15 rows draw Type from exactly the four-type scheme, Treatment matches the prescribed treatment for each Type, Verdicts are Accept/Challenge/Discard with genuine challenge (A-9) and discard (A-10) present, and every unverified row reads "Unverified — flagged" — but two identifiable entries fall short: A-4's headline claim ("the largest single loss area on the top floor") is an empirical, house-specific proposition classified as a *physical law* and thereby exempted from verification, and the exhaustive-surfacing requirement is not met, since the Assumption Audit above finds five chain-step assumptions (notably the provenance of Chain 4's weights and the ΔT equivalence in Chain 1) absent from the table.

**Criterion 3: Establish Ground Truths**
Quoted span: *"GT-13: Dominant air-leakage paths in 1960s construction are the loft hatch, floor/skirting junctions, service penetrations, and open chimneys. (A-10; the discard verdict on 'windows cause the draughts' rests on this)"*
Band: **Sound**
Justification: IDs are stable and every ID referenced in section 4 (GT-1, 2, 3, 5?, 6?, 7?, 8, 9, 11, 12, 13, 15) resolves in section 3, all four unverified entries carry the `?` suffix, and the discarded A-10 proposition is explicitly excluded — but GT-13, GT-8, and GT-15 are verified-status GTs whose only citation points back to their own assumption row, whose Verification cell restates the same claim rather than naming a source, matching the Sound trigger "one or more verified GTs cite … no source at all"; GT-13 is load-bearing for the draught conclusion, so the circularity is not cosmetic.

**Criterion 4: Reason Upward**
Quoted span: *"if you already have ≥250 mm of loft insulation and the windows are physically failing … then the attic option has almost nothing left to buy (ΔU ≈ 0.05, ≈2 W/K) and the spend becomes a repair decision rather than an energy decision."*
Band: **Sound**
Justification: The chain machinery is strong — each chain names the GT-IDs it consumes, carries a genuine non-restating intermediate, and three steps declare `[Assumes:]` inline; all four dead ends in section 5 use What-was-tried / Why-abandoned / What-it-ruled-out with structural reasons (contradicts GT-1; assumption discarded in Phase 2; intermediate could not be established), and the one analogy encountered is explicitly barred as direct evidence — but the quoted flip condition, the "do not compress insulation under boarding" condition, and the secondary-glazing alternative all appear for the first time in section 6 with no corresponding chain in section 4 (the ≈2 W/K figure in section 5 covers the 270→400 mm case, not the 250→270 mm case quoted), and the recommendation is carried by two chains (Chain 2 and Chain 4) where the prescribed form is exactly one.

**Criterion 5: Validate**
Quoted span: *"**Confidence: HIGH** — the conclusion is branch-invariant. Every GT-5?/GT-6? combination yields the same ordering, so the unverified inputs cannot flip it."*
Band: **Sound**
Justification: Four of five chains name a specific weakest link and the specific verification that would raise them to HIGH, which clears the Hand-wavy descriptors — but Chain 2, the self-declared decisive and load-bearing chain, is rated HIGH while transitively consuming GT-7? through Chain 1's output, and its branch-invariance defence enumerates only GT-5?/GT-6?, leaving the unverified 45 m²/15 m² area ratio — the very quantity the analysis says "decides the outcome" — unmentioned in the confidence line; this is precisely the Sound trigger "a chain is rated HIGH confidence while consuming a GT-N? input," compounded by Chain 5 carrying no confidence rating at all and the overall rating being given as "MEDIUM-HIGH" rather than the prescribed HIGH/MEDIUM/LOW.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: *"window replacement never repays itself thermally — the best case, single glazing to modern double, has a ~43-year payback against a window service life of roughly 40–50 years. Windows are a comfort, noise, security, appearance, and resale purchase that happens to save some energy; they are not an energy investment."*
Band: **Rigorous**
Justification: The Conclusion cites its originating chain for each substantive claim ("from Chain 1 and Chain 2", "Per Chain 3", "from Chain 5"), contains nothing that contradicts section 4, and the Key Insight is a genuinely non-obvious result — that the two options are incommensurable on the axis the user proposed, reached by comparing payback against service life rather than by restating the recommendation, and reachable by neither convention nor analogy; per the precedence rule, the section-6-only claims noted above are banded under Criterion 4 and are recorded here as overlap without lowering this band.

---

**Result:** gate cleared (no criterion at Absent); hand-wavy cap cleared (zero criteria at Hand-wavy).

=== QUALITY-HARNESS-SCORELINE-START ===
C1: Rigorous
C2: Sound
C3: Sound
C4: Sound
C5: Sound
C6: Rigorous
Verdict: PASS
=== QUALITY-HARNESS-SCORELINE-END ===