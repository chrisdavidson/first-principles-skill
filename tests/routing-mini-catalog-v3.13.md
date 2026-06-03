# Routing Mini-Catalog — v3.13 (P11/P12/P13/N18/N19/N20 catalog-expansion validation)

**Purpose:** This is a subset of `tests/routing-catalog.md` containing only the six new
v3.13 prompts (P11, P12, P13, N18, N19, N20), used for the INFRA-03 mini-battery gate.
Run with:

```
python3 scripts/check-routing.py --catalog tests/routing-mini-catalog-v3.13.md --repeat 5 --min-pass 3 --p-threshold 3 --n-threshold 3
```

Like the v3.6 mini-catalog (`tests/routing-mini-catalog-v3.6.md`), this fixture includes
both new P-cases and their paired N-cases because the v3.13 catalog expansion added both new
P-prompts (P11, P12, P13 — assumption-taxonomy, self-application, and worked-examples-domain
framings) and new N-prompts (N18, N19, N20 — paired off-topic cases for the same framings).
The mini-battery confirms all six new prompts meet their per-prompt thresholds before running
the full 33-prompt expanded battery. This fixture mirrors the v3.6 both-sides precedent.

Note: N19 contains the literal token "first-principles" — flagged as an info-level risk in
the Phase 55 code review. The 2-flip N-side tolerance in the full battery is the mitigation
per D-02. If N19 misfires in the mini-gate, apply the gate failure protocol (D-03).

---

## Positive Cases — Expected Verdict: DELEGATE

| # | Prompt | Expected Routing | Trigger Phrase Matched | Rationale |
|---|--------|-----------------|----------------------|-----------|
| P11 | "I want to challenge the assumptions embedded in how modern universities assign academic credit hours — can you map out the distinct categories of assumptions baked into that model and evaluate whether each one actually holds?" | DELEGATE | "challenge assumptions" | Self-contained (education domain); "challenge assumptions" trigger in natural mid-sentence embedding; framing asks for assumption-taxonomy (categorize + evaluate) rather than a single-assumption refutation — cleanly DELEGATE |
| P12 | "Help me analyze from first principles whether first-principles reasoning itself is a reliable method — what fundamental assumptions does the approach rest on, and do they actually hold under scrutiny?" | DELEGATE | "analyze from first principles" | Self-contained (methodology / meta domain); "analyze from first principles" trigger in natural mid-sentence embedding; self-application framing: the method is applied to an evaluation of itself; cleanly DELEGATE |
| P13 | "I want to reason from ground truth about why antibiotics stop working against bacteria that were once sensitive to them — what do we actually know is true about the underlying biological mechanism?" | DELEGATE | "reason from ground truth" | Self-contained (biology / medicine domain); "reason from ground truth" trigger in natural mid-sentence embedding; worked-examples-domain framing: biology/medicine is a distinct discipline not yet represented in the P-table; requires causal reasoning from first principles, not clinical lookup — cleanly DELEGATE |

---

## Negative Cases — Expected Verdict: NO-DELEGATE

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N18 | "What are the main categories of cognitive biases that affect human decision-making?" | NO-DELEGATE | Taxonomy / classification request | Enumeration request about a cognitive-science taxonomy — general Q&A; no first-principles framing, no trigger phrase from the description; excluded by the "general Q&A" scope-exclusion clause in shared/spine/SKILL.meta.yml. Paired with P11 (assumption-taxonomy boundary). |
| N19 | "What is first-principles reasoning and how does it differ from analogical thinking?" | NO-DELEGATE | Methodology explanation | Factual explanation request about a reasoning methodology — general Q&A; no analytical trigger framing; asking "what is" not "analyze / challenge / reason from ground truth"; excluded by the "general Q&A" scope-exclusion clause in shared/spine/SKILL.meta.yml. Paired with P12 (self-application boundary). |
| N20 | "What antibiotic classes are typically used to treat MRSA infections?" | NO-DELEGATE | Medical / clinical lookup | Clinical factual lookup in the same domain (medicine/biology) as P13 — general Q&A; no causal or first-principles framing; asking for a clinical answer, not an underlying mechanism; excluded by the "general Q&A" scope-exclusion clause in shared/spine/SKILL.meta.yml. Paired with P13 (worked-examples-domain boundary). |
