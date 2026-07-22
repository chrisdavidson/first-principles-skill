I read both files in full. Scoring `analysis.md` against `validation-rubric.md`, following the rubric's own application order: Assumption Audit first, then six verdict blocks.

---

## Assumption Audit

Scan of every derivation chain in section 4 (Chains A–D and the Second-order pass), step by step, for assumptions each step requires that are not already rows in the section-2 Assumptions Table. This is a scoring pass, so surfaced assumptions cannot be written into the analysis's own table; each such finding is recorded and carried into Criterion 2.

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| A (split of the 35%) | 1 | `GT-1 + GT-3 + GT-10? → compute UA (area ÷ R) for each path` | Effective attic assembly R = 15 (nominal R-13 + ~R-2 films/framing) — a delivered-R claim distinct from A1's physics | n/a — not in table; C2 gap |
| A | 2 | Table rows: attic 1,300 ft² @ U 0.067; windows 210 ft² @ U 1.04 / 0.49 | Attic and windows exhaust GT-8?'s "35%" — no doors, rim joists, or wall share inside that pool | n/a — not in table; C2 gap |
| A | 3 | `→ attic 29% / windows 71% … attic 10 pts, windows 25 pts of total heating energy` | UA ratio equals delivered-energy ratio — same ΔT and same operating hours across both planes | n/a — not in table; C2 gap |
| A | 4 | `Confidence: MEDIUM (rests on GT-8? and GT-10?)` | none (dependency stated explicitly) | n/a |
| B (attic insulation) | 1 | `Chain A + GT-2 → 71% of a 10–16 point share → 7–11% of total heating energy saved` | none new (GT-2 arithmetic on GT-1) | n/a |
| B | 2 | `applied to GT-6 discounted for baseload (A4: $1,150–$1,640 heating-attributable)` | none — A4 is in the table with an explicit 70–100% bracket | n/a |
| B | 3 | `even with 3%/yr fuel escalation, cumulative savings ≈ $1,650` | Fuel-price escalation of 3%/yr over the 10-year horizon | n/a — not in table; C2 gap |
| B | 4 | `re-run with A5's challenge — a market-rate $2,400 quote: payback ≈ 17 years` | none — A5 is in the table with a cited $/ft² range | n/a |
| C (triple-pane) | 1 | `Chain A + GT-3 → triple-pane cuts window loss by 80% (from single) or 60% (from double)` | Whole-window installed U tracks the NFRC glazing figures — frame, spacer, and install losses do not erode the ratio | n/a — not in table; C2 gap |
| C | 2 | `→ 11–20% of heating energy → applied to A4's bracket → Savings: $145–$310/yr` | none new | n/a |
| C | 3 | `Confidence: HIGH — the gap is two full orders of magnitude wider than the uncertainty` | Combined error in GT-8? and GT-10? is bounded near 2× (partially stated inline in the same sentence) | n/a — partially inline; C5 note |
| D (unquoted options) | 1 | `GT-1 + A6 + the observation that a 1948 house's infiltration is typically 25–40% of heating load` | Infiltration share of 25–40% for *this* house — carried as a bare "observation," neither a GT nor a table row | n/a — not in table; C2 gap |
| D | 2 | `Attic air sealing … $800–$1,500 … $80–$200 … 5–14 yrs` | Accessible leakage at top plates/chases/can lights, and that sealing captures a large enough fraction of infiltration to yield $80–$200/yr | n/a — not in table; C2 gap |
| D | 3 | `Interior low-e storm panels, 14 windows … $1,400–$3,500 … $80–$160` | none new — efficacy claim is A6 in the table | n/a |
| Second-order (§4) | 4 | `windows recoup roughly 60–70% of cost in typical markets … shortens the effective 10-year window loss … to roughly ~$6,000` | Resale recoup rate of 60–70% applies to this market and this house | n/a — not in table; C2 gap |
| Second-order (§4) | 1–3 | Moisture/dew point, ASHRAE 62.2 ventilation floor, non-energy window failure modes | none material — each is stated as a consequence, not consumed as a chain input | n/a |

**Audit result:** seven assumptions are required by named chain steps but appear in neither the Assumptions Table nor an inline `[Assumes: X]` declaration. Per the precedence rule, this single underlying defect bands under Criterion 2 (lowest-numbered criterion whose descriptor names it) and is noted-only under Criteria 3 and 4.

---

## Verdict Blocks

**Criterion 1: Identify Essence**
Quoted span: "Which of these two capital expenditures, if either, returns more value than it costs over a ≥10-year hold — where 'value' is dollars saved on heat *plus* comfort and durability?" … "Attributes the 35% loss between the two paths rather than treating it as one pool. / Converts each intervention to $/year saved, with an explicit uncertainty bracket. / Compares against the 10-year horizon, not an unbounded one. / States which assumption, if wrong, flips the recommendation."
Band: **Rigorous**
Justification: The statement is a single sentence naming the underlying investment decision rather than the triggering "insulation, windows, both, or neither" framing (which it explicitly names as a false binary), and each of the four success criteria is a verb + subject + outcome test a reviewer applies by scanning section 6 — the 35% attribution, the $/yr brackets, the 10-year comparison, and the "What would change this answer" table each resolve pass/fail without analyst interpretation, and all four name properties unique to this problem.

**Criterion 2: Challenge Assumptions**
Quoted span: "| # | Assumption | Type | Treatment | Verdict |" … "| A9 | House stays occupied by you ≥10 years | given ground truth | Accept | → GT-7 |"
Band: **Hand-wavy**
Justification: The artifact's prescribed five-column structure is not followed as a pattern rather than in an isolated row — the Verification column is absent across all nine rows (its content folded into Verdict, so Verdict no longer records Accept/Challenge/Discard, which has migrated to Treatment), A9's Type "given ground truth" falls outside the four-type scheme, and the Assumption Audit above shows the required exhaustive scan over named chain steps was not performed, leaving seven chain-consumed assumptions (3%/yr fuel escalation, 25–40% infiltration share, whole-window U tracking glazing U, UA-ratio-equals-energy-ratio, R-15 effective, air-sealing capture fraction, 60–70% resale recoup) off the table entirely. Not Absent: eight of nine Type cells do map cleanly to the four-type scheme, A2/A8 carry correct "Unverified — flagged" discipline, and five assumptions are genuinely challenged with cited evidence.

**Criterion 3: Establish Ground Truths**
Quoted span: "**GT-9** — Federal 25C credit unavailable for 2026 placements. *(Current constraint; verify locally.)*"
Band: **Sound**
Justification: GT-IDs are stable and match every reference in section 4, both unverified entries carry the `?` suffix and are used as `GT-8?`/`GT-10?` inside chains, and no Discard-verdict assumption (A3, A4, A6) appears in the list — but GT-9 is presented as a verified current constraint with a "verify locally" instruction in place of a source citation, the identifiable single-entry shortfall that separates Sound from Rigorous. (Noted, not double-counted: the un-tabled chain assumptions from the audit also bear on this section's completeness; banded under Criterion 2.)

**Criterion 4: Reason Upward**
Quoted span: "GT-1 + A6 + the observation that a 1948 house's infiltration is typically 25–40% of heating load (outside GT-8?'s conduction accounting entirely) →"
Band: **Sound**
Justification: All four chains carry genuine intermediate steps that cannot be stated from either named GT alone (Chain A's UA table, Chain B's 71%-of-share conversion, Chain C's 80%/60% U-reduction step), and Abandoned Reasoning documents three dead ends with specific structural reasons — "this DOE-style statistic is about the *share of loss*, not the *cost of eliminating it*", NPV as "false precision the inputs cannot support", HDD modeling as "an assumption layer without narrowing the bracket" — with the first explicitly refusing an analogy as direct evidence; the identifiable shortfall is that Chain D departs from the prescribed `GT-N + GT-M →` form by consuming an assumption ID and a bare unnumbered observation as inputs. (Noted, not double-counted: no chain step uses the `[Assumes: X]` token despite the audit's seven surfaced assumptions; that defect bands under Criterion 2.)

**Criterion 5: Validate**
Quoted span: "Confidence: **HIGH** — the gap is two full orders of magnitude wider than the uncertainty in GT-8?/GT-10?." … "**Weakest link, stated plainly:** the entire attic/window split rests on **GT-8?** (unverified 35%) and **GT-10?** (assumed geometry). … **Chain B's verdict does not.**"
Band: **Sound**
Justification: Weak links are named at the specific-input level rather than in general terms, per-chain confidence lines exist on A, B and C, and the closing statement reconciles each chain's rating against its unverified inputs — but Chain C is rated HIGH while consuming GT-8? and GT-10? through Chain A, which is precisely the Sound descriptor's "chain is rated HIGH confidence while consuming a GT-N? input," and load-bearing Chain D (the sole support for conclusion step 2) carries no confidence line at all.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "**At $2,000–$2,500 bundled with the air sealing, do it** — the combined package plausibly pays back in 10–14 years"
Band: **Sound**
Justification: Every recommendation otherwise traces to a named chain — step 2 to Chain D's air-sealing row, step 3 to Chain B re-run at A5's market price, step 4 to Chain C's 60–128-year payback and Chain D's storm-panel row — and Chain B's "Attic insulation is conventionally 'obvious,' and at *this quote and this bill* it does not pay back inside your horizon" is a genuinely non-obvious finding that convention does not reach rather than a restatement of the recommendation; the shortfall is the bundled 10–14-year payback, a new combined-package figure computed for the first time in section 6 and derivable from no chain in section 4 (Chain D prices air sealing at 5–14 years and market-rate insulation at 17 years, separately).

---

=== QUALITY-HARNESS-SCORELINE-START ===
C1: Rigorous
C2: Hand-wavy
C3: Sound
C4: Sound
C5: Sound
C6: Sound
Verdict: PASS
=== QUALITY-HARNESS-SCORELINE-END ===