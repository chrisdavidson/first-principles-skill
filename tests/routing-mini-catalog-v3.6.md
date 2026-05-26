# Routing Mini-Catalog — v3.6 (P9/P10/N16/N17 catalog-expansion validation)

**Purpose:** This is a subset of `tests/routing-catalog.md` containing only the four new
v3.6 prompts (P9, P10, N16, N17), used for the CAT-08 mini-battery gate. Run with:

```
python3 scripts/check-routing.py --catalog tests/routing-mini-catalog-v3.6.md --repeat 5 --min-pass 3
```

Unlike the P3+P7 mini-catalog (`tests/routing-mini-catalog-p3p7.md`), this fixture includes
both new P-cases and their paired N-cases because the v3.6 catalog expansion added both new
P-prompts (P9, P10 — chemistry and earth-science domains) and new N-prompts (N16, N17 —
paired science-lookup off-topic cases for the same domains). The mini-battery confirms all
four new prompts meet their per-prompt thresholds before running the full expanded battery.

---

## Positive Cases — Expected Verdict: DELEGATE

| # | Prompt | Expected Routing | Trigger Phrase Matched | Rationale |
|---|--------|-----------------|----------------------|-----------|
| P9 | "Help me reason from ground truth about why dissolving table salt in water lowers the freezing point — what do we actually know is true about the underlying mechanism?" | DELEGATE | "reason from ground truth" | Self-contained (science / chemistry domain); natural mid-sentence embedding of trigger phrase; colligative-properties substance requires reasoning from primitives, not lookup; chemistry discipline (new in v3.6) |
| P10 | "What are the fundamental ground truths about why the deep ocean stays cold even directly under the equator? Reason up from them to evaluate whether thermohaline circulation alone explains it." | DELEGATE | "fundamental ground truths" + "reason up from first principles" | Self-contained (science / earth-science domain); multi-trigger annotation mirrors P7 form; requires reasoning from first principles about ocean thermodynamics, not factual lookup; earth-science discipline (new in v3.6) |

---

## Negative Cases — Expected Verdict: NO-DELEGATE

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N16 | "What's the formula for calculating the freezing-point depression of a 5% NaCl solution?" | NO-DELEGATE | Science formula/homework lookup | Factual formula recall — general Q&A; excluded by the "general Q&A" scope-exclusion clause in shared/spine/SKILL.meta.yml. Domain: chemistry (paired with P9). |
| N17 | "How deep is the average ocean thermocline, and which latitudes have the steepest gradient?" | NO-DELEGATE | Science factual lookup | Factual lookup question — general Q&A; excluded by the "general Q&A" scope-exclusion clause in shared/spine/SKILL.meta.yml. Domain: earth-science (paired with P10). |
