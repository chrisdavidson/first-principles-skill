I've read both files in full. Now I'll apply the rubric exactly as its "How to Apply This Rubric" section instructs — Assumption Audit first, then one verdict block per criterion.

---

## Assumption Audit (verify before scoring)

Per the rubric, my job here is narrow: confirm the audit table is **present** and **exhaustive** over every named derivation chain step in section 4 — not to re-run the scan.

The analysis contains the audit artifact under "Process output — Phase 4 Assumption Audit scan." The named derivation chains in section 4 are C1, C2, C3, C4, C5 (plus a supplementary "Second-order pass" extension, which is not one of the enumerated `C#` chains and does not take the `GT-N → intermediate → conclusion` form).

Cross-checking the audit table against the section-4 chains:

| Chain | Steps in §4 | Rows in audit table | Covered? |
|---|---|---|---|
| C1 | split → 73.5% removed → annual-cost payback | C1/1, C1/2, C1/3 | ✓ in order |
| C2 | split → existing-glazing R → payback | C2/1, C2/2 | ✓ in order |
| C3 | cost-per-$-saved ratio | C3/1 | ✓ |
| C4 | asset-life vs payback | C4/1 | ✓ |
| C5 | horizon recovery + resale | C5/1 | ✓ |

Every named derivation chain (C1–C5) has one row per step, in order, with no step skipped. The Second-order pass is an extension rather than a named `C#` chain, so its exclusion does not make the audit non-exhaustive over the named chains. **Audit confirmed present and exhaustive.** Proceeding to verdict blocks.

---

**Criterion 1: Identify Essence**
Quoted span: "Given a fixed home-improvement budget this year, which envelope upgrade — attic insulation, window replacement, both, or neither — returns the most value over a ≥10-year horizon?" ... "Ranks the four options by energy-dollar return per dollar spent." / "Separates energy savings (measurable) from comfort/aesthetic value (real but not an energy return)." / "States confidence given the unknowns."
Band: **Rigorous**
Justification: The statement is a single sentence naming the core decision (and explicitly rejects the triggering "35% is lost" framing as *not* the decision), and each success criterion is a verb+subject+outcome test checkable directly against the Conclusion section (ranking of four options, energy-vs-comfort separation, stated confidence), specific to this problem.

**Criterion 2: Challenge Assumptions**
Quoted span: "| A-1 | Heat loss through a surface ∝ 1/R | physical law | accept as GT | HOLDS | Steady-state conduction, U = 1/R |" ... "| A-4 | **Split of the 35% between attic and windows** | untested belief | **challenge — load-bearing** | UNVERIFIED — bracket f_attic ∈ [0.15, 0.22]... |"
Band: **Sound**
Justification: All rows use the four-type scheme, every Verification cell is specific (e.g., "1 − 13/49 = 0.735", "1948 house, glazing not stated"), and challenges are present — but the prescribed **Verdict** cell records HOLDS/UNVERIFIED/LIKELY rather than the required Accept/Challenge/Discard (those tokens live in the Treatment column instead), an identifiable departure from the prescribed form that stops short of any Hand-wavy trigger (no out-of-scheme Types, no empty cells, challenges attempted).

**Criterion 3: Establish Ground Truths**
Quoted span: "**GT-4?:** Split unknown; f_attic ≈ 0.15–0.22, f_window ≈ 0.13–0.20. (unverified — A-4)" ... "**GT-2:** Attic R-13→R-49 ⇒ 73.5% less attic conductive loss. (derived, GT-1)"
Band: **Rigorous**
Justification: Every fact carries a stable GT-ID that matches the identifiers consumed in the section-4 chains, every unverified fact carries the `?` suffix (GT-3?, GT-4?, GT-7?), each verified GT cites a basis more specific than "common knowledge" (physical law / derived from GT-1 / given / convention), and no Discard-verdict assumption appears in the list.

**Criterion 4: Reason Upward**
Quoted span: "**C1** ... GT-1 + GT-2 + GT-4? + GT-5 → attic ≈ 18% of a ~$2,000 annual bill = ~$360/yr of loss, of which 73.5% is removed → **~$265/yr saved** ... → payback $4,200 / $265 ≈ **16 yr central (11–23 yr)**. `[Assumes: A-4, A-5]`" ... "**Metered sub-load split:** I could have tried to nail A-4 exactly. Abandoned — you don't have the data, and C3 shows the ranking doesn't need it."
Band: **Rigorous**
Justification: Each conclusion has exactly one chain naming its consumed GT-IDs with genuine intermediate inferences (loss-share → fraction-removed → dollar-saving → payback), every chain step introducing a new assumption declares it inline via `[Assumes: X]`, no analogy is used as standalone evidence, and Abandoned Reasoning documents specific dead ends with what-was-tried / why-abandoned / what-it-ruled-out structure.

**Criterion 5: Validate**
Quoted span: "**Windows — NO, not on energy grounds.** ... Confidence: **HIGH** (verdict robust across all unknowns via C3/C4)."
Band: **Sound**
Justification: Weak links are named and MEDIUM/HIGH ratings are tied to specific unverified inputs (e.g., insulation "MEDIUM on the exact payback (A-4/A-5 unverified)"), but the windows verdict is rated **HIGH** while resting on C2/C3, chains that consume the GT-7? and GT-4? inputs — matching the Sound descriptor "a chain is rated HIGH confidence while consuming a GT-N? input," notwithstanding the (well-argued) robustness claim.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "**Do the insulation this year. Do not replace the windows for energy reasons.** (→ C1, C3, C4, C5)" ... "**Windows are ~5× less cost-effective per dollar than insulation** ($81 vs $16 per $1/yr saved). (→ C3)"
Band: **Rigorous**
Justification: Every Conclusion claim carries an explicit `(→ C#)` back-reference to a section-4 chain, no new reasoning is introduced (air-sealing and storm-window measures both originate in the section-4 second-order pass), and the key insight — the ~5× cost-effectiveness gap robust to the split — is a non-obvious derived finding rather than a restatement of the recommendation.

---

**Gate check:** No criterion is Absent. **Hand-wavy cap check:** Zero criteria at Hand-wavy (≤1 permitted). Both conditions met → PASS.

=== QUALITY-HARNESS-SCORELINE-START ===
C1: Rigorous
C2: Sound
C3: Rigorous
C4: Rigorous
C5: Sound
C6: Rigorous
Verdict: PASS
=== QUALITY-HARNESS-SCORELINE-END ===