# Assumption Audit (verify-before-scoring step)

The rubric's "How to Apply" section requires me to first confirm that an **Assumption Audit table** — the `Chain | Step | Step Text | Assumption surfaced? | Added to Table?` artifact — is present in the analysis and covers every named derivation-chain step in section 4, one row per chain per step.

**Result of the check:** No such Assumption Audit table appears anywhere in `analysis.md`. Section 4 contains six named chains (A–F), each with a one-line chain summary of the form `GT-N + GT-M → … → conclusion`, but there is no step-by-step audit table enumerating those steps and recording whether each surfaced an assumption. The analysis also uses a 4-column Assumptions Table (`# | Assumption | Type | Treatment | Verdict`) rather than the prescribed 5-column form that includes a dedicated **Verification** column.

Per the rubric's explicit instruction, I do **not** re-perform the scan to fill the missing table; the missing/incomplete audit "is itself the evidence to score against," and it is designated "a Criterion 2 defect (see Criterion 2's descriptors below), not a separate gate." I therefore proceed to the verdict blocks, carrying this defect into Criterion 2.

---

**Criterion 1: Identify Essence**
Quoted span: "Is $310,000/year the cheapest way to buy back 1.8 points of monthly churn — and is churn even the thing that program can move? … It is not 'should we have a loyalty program' and not 'should we respond to the rival.' The triggering event (rival launch, board deadline) is not the question."
Band: **Rigorous**
Justification: The Essence Statement is a single sentence naming the underlying purchase decision, explicitly distinguished from the triggering event and prompt restatement, and each of the four success criteria (cost-vs-margin comparison, addressability of the actual churn, cheapest comparative alternative, fit-the-window) is a verb+subject+outcome test scannable against the Conclusion — all specific to this problem and non-generic.

**Criterion 2: Challenge Assumptions**
Quoted span: "| # | Assumption | Type | Treatment | Verdict |" (the table's column header — no Verification column), together with the document-wide absence of the `Chain | Step | … | Added to Table?` Assumption Audit artifact.
Band: **Hand-wavy**
Justification: The four-type classification, treatments, and `unverified — flagged` discipline (A3/A4/A6/A7) are otherwise strong, but the prescribed table structure is not followed (no Verification column, so verification is merged into the Verdict cell across every row) **and** the Assumption Audit artifact the rubric requires is missing entirely — a whole-artifact structural gap rather than one isolated weak row, which is the Hand-wavy pattern.

**Criterion 3: Establish Ground Truths**
Quoted span: "| GT-9? | Effect size = 1.8 pp | *Unverified — stated as a bet* | … | GT-11? | Gross margin | *Unverified — not supplied* |"
Band: **Rigorous**
Justification: Every GT carries a stable ID matching the IDs consumed in section 4's chains, every verified GT cites a source more specific than "common knowledge" (Given / arithmetic / definitional / timeline), every unverified GT bears the `?` suffix and is consumed with that suffix intact in the chains, and no Phase-2 Discard assumption (A2/A5/A8/A9/A10) is smuggled in as a ground truth.

**Criterion 4: Reason Upward**
Quoted span: "GT-1 + GT-8 + A2-rejected → redemption credit is a second, larger, revenue-scaling cost line → all-in cost is $419k–$1,185k, not $310k." (Chain B), with Abandoned Reasoning: "Per-member LTV framing … Discarded: it books multi-year lifetime value against a one-year cost, which flatters the program."
Band: **Rigorous**
Justification: Each conclusion has exactly one chain naming its consumed GT-IDs and carrying a genuine intermediate inference (not a GT restatement); the rival analogy is explicitly barred as direct evidence ("Discarded per the no-analogy rule"); and Abandoned Reasoning documents multiple dead ends with specific what-was-tried / why-abandoned / what-it-ruled-out structure rather than the generic escape valve.

**Criterion 5: Validate**
Quoted span: "Chain A + Chain B + GT-11? → the bracket straddles zero → … this estimate does not resolve the decision. **Confidence: HIGH** that it does not resolve"
Band: **Sound**
Justification: Confidence ratings, per-chain weakest-link naming, and a dedicated "Weakest links" section resolving GT-9?/GT-11?/GT-6? are all present, but one chain (Chain C) is rated HIGH while consuming the unverified GT-11? input — a specific, identifiable departure from the no-HIGH-on-`GT-N?` rule (even though the HIGH is defensibly scoped to the non-resolution meta-claim), which is exactly the Sound-level shortfall.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "The price is not $310k. … All-in cost is $419k–$1,185k. … *(Chain B)*" and "The mechanism may not touch the problem. … *(Chain D)*"
Band: **Rigorous**
Justification: Every Conclusion claim cites the specific chain that produced it (Chain B/C/D/E/F), the board-pilot recommendation traces to Chain F and A8/A9 rather than being new reasoning, and the key insights (cost understated ~2×; generic treatment for an undiagnosed cause) are non-obvious findings reasoning-by-convention would not reach, not restatements of the recommended action.

---

**Gate:** No criterion is Absent → gate cleared. **Hand-wavy cap:** exactly one criterion (C2) is Hand-wavy → cap cleared. Both conditions met → **PASS**.

=== QUALITY-HARNESS-SCORELINE-START ===
C1: Rigorous
C2: Hand-wavy
C3: Rigorous
C4: Rigorous
C5: Sound
C6: Rigorous
Verdict: PASS
=== QUALITY-HARNESS-SCORELINE-END ===