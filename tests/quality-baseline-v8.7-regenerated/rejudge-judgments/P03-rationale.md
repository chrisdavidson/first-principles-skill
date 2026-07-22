I've read both files in full. Applying the rubric in its prescribed order: Assumption Audit first, then six verdict blocks.

## Assumption Audit

Chains enumerated from section 4: **Chain A** (energy saved per unit spent), **Chain B** (the draught symptom), **Chain C** (second-order effects). Each step visited in order.

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| A (attic beats windows per £) | 1 | "A temperate heating season is on the order of 2,000 K·days = 48,000 K·h" | **Yes** — A11: the house's location has a ~2,000 K·day heating season (current constraint; expires in a milder/harsher climate). Not in table. | yes |
| A | 2 | "*Attic (50 m² ceiling):* ΔU ≈ 2.15 W/m²K → 50 × 2.15 = 107 W/K" | **Yes** — A12: this specific house sits at the mid-point of GT-4's 40–60 m² range (untested belief). GT-4 gives a range; the chain silently picks a point value. | yes |
| A | 3 | "derated for real-world loft-void temperature and boiler efficiency, bracket: 1,500–5,000 kWh/yr" | **Yes** — A13: the derating factor from theoretical to delivered heat is ~0.3–1.0 (untested belief); no source or method given for the bracket width. | yes |
| A | 4 | "*Windows (18 m²):* ΔU ≈ 3.4 W/m²K → 18 × 3.4 = 61 W/K" | **Yes** — A14: window area is 18 m², a point value inside GT-4's 12–20 m² range (untested belief). | yes |
| A | 5 | "GT-5 (attic ≈ £500–1,000) … GT-5 (windows ≈ £8,000–15,000)" | none — arithmetic follows from GT-5 × the areas already assumed in steps 2 and 4. | n/a |
| A | 6 | "→ Attic insulation buys 5–15× more heat-loss reduction per pound" | none — division of steps 2/4 by step 5. | n/a |
| A | 7 | "windows ≈ 30–60 years, which by GT-9/A9 exceeds the service life of the sealed units" | **Yes** — A15: an energy price and discount rate exist that make the payback arithmetic hold (untested belief); no price is stated anywhere yet a payback period is asserted. Also note: **GT-9 is cited but does not exist** in section 3. | yes |
| B (draught mechanism) | 1 | "GT-6 + A7 → the top floor is the pressurised zone, so cold inleakage occurs low in the house" | none — restates GT-6 with A7, both already tabled. | n/a |
| B | 2 | "→ the 'draught' is most likely (i) convective downdraught off cold glass and radiant asymmetry, and (ii) warm-air loss through ceiling penetrations" | **Yes** — A16: the neutral pressure plane sits below the top-floor ceiling in this house (physical law applied to an unverified geometry). Stack-effect direction at the top floor depends on it. | yes |
| B | 3 | "only (ii) is fixed by insulation *if the hatch and penetrations are sealed* → sealing the ceiling plane is a separate, near-free task" | **Yes** — A17: ceiling-plane penetrations are accessible and sealable at negligible cost (current constraint). "Near-free" is asserted, not costed. | yes |
| B | 4 | "**secondary glazing** or heavy lined curtains with a pelmet does that for roughly 5–10% of replacement cost" | **Yes** — A18: secondary glazing costs 5–10% of full replacement (untested belief); GT-5 prices replacement only, not secondary glazing. | yes |
| C | 1 | "Insulating the ceiling makes the loft void colder → tank/pipework moves closer to freezing" | **Yes** — A19: there is a water tank or pipework in the loft (current constraint) — true of much 1960s stock, not verified here. | yes |
| C | 2 | "Sealing the ceiling plane reduces the accidental ventilation rate → condensation and mould risk" | **Yes** — A20: current ventilation is at or near the minimum needed for moisture control (untested belief); if the house is over-ventilated the risk does not arise. | yes |
| C | 3 | "A colder loft with a warm, moist ceiling below can drive interstitial condensation on the roof underside" | none — follows from C1 plus A2/GT-6 already tabled. | n/a |

**Result of the audit:** ten assumptions (A11–A20) are required by named chain steps and are absent from the Assumptions Table. They are added to the table for the purposes of scoring Criterion 2. The scan was exhaustive over the named steps of Chains A, B, and C only — it is not an open-ended survey of conceivable assumptions. Critically, **none of these ten is declared inline with the `[Assumes: X]` token**; scanning every chain step for the `[Assumes:` string returns zero hits document-wide. This is a Criterion 4 finding and is banded there.

---

## Verdict Blocks

**Criterion 1: Identify Essence**
Quoted span: "Given one fixed pot of money, which single fabric intervention buys the largest reduction in heat loss *and* draught discomfort on the top floor of a 1960s temperate-climate house? … 1. Identifies which mechanism dominates the stated symptom. 2. Ranks the two options on heat-energy saved per unit of money spent. 3. Ranks them on top-floor comfort improvement, which is not the same ranking. 4. Names the conditions under which the ranking flips. 5. Flags any second-order harm the recommended option creates."
Band: **Rigorous**
Justification: The Essence Statement is a single sentence naming the underlying decision rather than the symptom — it explicitly separates the stated symptom ("cold, draughty top floor") from the two conduction remedies asked about — and each of the five success criteria is a verb + subject + outcome triplet whose outcome is a scannable property of the Conclusion section (a reviewer checks criterion 4 by looking for a "ranking flips if" list, which section 6 contains), with wording specific enough to this problem that it could not appear unmodified in a different analysis.

**Criterion 2: Challenge Assumptions**
Quoted span: "| A7 | Draughts come from the windows | untested belief | Verify or flag | **Probably false as sole cause** | Under stack effect the top floor is the *pressurised* zone…"
Band: **Sound**
Justification: The table is present with all six prescribed columns and every Type value drawn from exactly the four-type scheme (physical law, current constraint, convention, untested belief), with genuine challenges recorded (A6 "Rejected as framing", A9 "Rejected") and specific verification sources cited (BS EN ISO 6946, service-life data), but several Verdict cells depart from the prescribed Accept/Challenge/Discard vocabulary — "Probably false as sole cause", "Unverified — load-bearing", "Accepted from user framing" — and A7, which is consumed by Chain B while unverified, carries no "unverified — flagged" notation in its Verification cell; these are identifiable per-row departures rather than the systemic pattern (freeform Types, empty cells, or all-Accept) that the Hand-wavy descriptor names. Noted but not double-counted: the ten assumptions surfaced by the audit above are absent from the table, but their more direct defect is the missing inline `[Assumes:` declaration in the chains themselves, banded under Criterion 4 per the precedence rule.

**Criterion 3: Establish Ground Truths**
Quoted span: "**GT-5.** Loft insulation is roughly £5–20/m² installed; window replacement is roughly £400–900/m² of opening installed. *Market pricing; ~40–100× difference per square metre treated.*"
Band: **Sound**
Justification: GT-IDs are stable and are the same identifiers the chains consume, the two unverified entries carry the `?` suffix (GT-7?, GT-8?) and retain it at every downstream use including the Conclusion, and no Discard-verdict assumption (A6, A9) reappears in the list — but GT-5's citation is the bare category "Market pricing" and GT-3's is "Manufacturer and standards data", neither naming a specific source the way GT-2's "BS EN ISO 6946 / national building-regulation tables" does, which is exactly the Sound descriptor's "one or more verified GTs cite … no source at all" in its weaker form. Noted without lowering this band: Chain A cites "GT-9", which appears nowhere in this section; that dangling reference is a defect of the chain, banded under Criterion 4.

**Criterion 4: Reason Upward**
Quoted span: "Payback: attic ≈ 2–5 years; windows ≈ 30–60 years, which by GT-9/A9 exceeds the service life of the sealed units themselves."
Band: **Hand-wavy**
Justification: Three distinct structural failures recur across the section rather than sitting in one entry: (i) this step cites **GT-9**, a GT-ID that does not appear in the Ground Truths section — the literal Hand-wavy descriptor "chains reference GT-IDs that do not appear in the Ground Truths section"; (ii) scanning every chain step for the `[Assumes:` token returns zero hits, while the audit above identifies ten assumptions that chain steps require and the Assumptions Table does not contain (the heating-season figure, the point-value areas inside GT-4's ranges, the derating factor, the 5–10% secondary-glazing cost, the loft tank); and (iii) the Conclusion's first ranked recommendation, "Balance the heating system and check top-floor radiator sizing", has no derivation chain in section 4 at all — it enters via the Abandoned Reasoning section — matching "some conclusions lack derivation chains". Offsetting these, and the reason the band does not fall to Absent: Chains A and B are correctly formed with named GT inputs and genuine intermediate claims (the per-pound normalisation in A and the pressurised-zone inference in B are both non-restatements), the Abandoned Reasoning section documents four dead ends with specific structural abandonment reasons rather than vague ones, and the analogy ban is honoured explicitly — "Reasoning by analogy from 'everyone replaces their windows first.' Abandoned per the no-analogies rule."

**Criterion 5: Validate**
Quoted span: "**Insulate the attic.** [HIGH confidence, conditional on GT-7? and GT-8?]"
Band: **Sound**
Justification: Confidence ratings are attached to individual chains rather than only to the Conclusion (Chain A carries two [HIGH confidence] marks, Chain B carries "[MEDIUM confidence — depends on unverified A7; a smoke-pencil or thermal-camera check on a windy day resolves it to HIGH]", which names both the specific unverified input and the verification that would raise it), and the weakest link is named concretely rather than generally — "the entire recommendation rests on GT-7? and GT-8?, both unverified and both resolvable in ten minutes with a ladder and a ruler" — but the quoted span rates the load-bearing overall conclusion HIGH while, by its own admission, conditioning it on two GT-N? inputs, which is precisely the Sound descriptor's "a chain is rated HIGH confidence while consuming a GT-N? input"; Chain C additionally carries no confidence rating of any kind.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "**The loft is already at 100 mm+** (GT-7?). Topping up 100 → 300 mm saves roughly 12 W/K rather than 107 — an order of magnitude less."
Band: **Sound**
Justification: The great majority of Conclusion claims trace to named chains and the Conclusion cites them explicitly ("(Chain A)", "(Chain B)", "per Chain C effect 2"), and the Key Insight — "the real answer is that your budget is not actually constrained to one option" — is a genuinely non-obvious finding that inverts the question's either/or framing rather than restating "insulate the attic", but the quoted span introduces a specific quantitative result (12 W/K for a 100→300 mm top-up) that appears in no derivation chain in section 4, which is the Sound descriptor's "one claim is introduced for the first time in the Conclusion section". Noted without further lowering: the heating-balance recommendation is likewise unchained, but that defect is banded under Criterion 4 per the precedence rule and is not counted twice here.

---

**Gate:** no criterion scores Absent — cleared. **Hand-wavy cap:** exactly one criterion (C4) scores Hand-wavy — cleared. Both conditions satisfied.

=== QUALITY-HARNESS-SCORELINE-START ===
C1: Rigorous
C2: Sound
C3: Sound
C4: Hand-wavy
C5: Sound
C6: Sound
Verdict: PASS
=== QUALITY-HARNESS-SCORELINE-END ===