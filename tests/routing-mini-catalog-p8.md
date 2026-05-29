# Routing Mini-Catalog — P8 (v3.9 P8 baseline and verification runs)

**Purpose:** This is a P8-scoped subset of `tests/routing-catalog.md` containing P8 and
three adjacent N-prompts from the General Q&A class. Used for:

- **Baseline run (Plan 47-01):** `--repeat 5 --min-pass 3` — establishes the pre-fix P8 pass
  rate as a measured reference point (per D-01: matches the v3.8 disambiguation precedent
  and is directly comparable to the 2/5 FAIL already on record).
- **Verification gate (Plan 47-02):** `--repeat 3 --min-pass 2` — the post-fix pass/fail gate
  (per D-01: gate flags are strictly lighter than the baseline flags to avoid false negatives).

**N-prompt selection rationale (per D-02):** N8, N9, and N10 are drawn from the General Q&A
class. They share vocabulary proximity to P8's domain (technology, factual how-to, software)
without containing any first-principles trigger phrases. Including them alongside P8 allows
early detection of N-side regression — if the P8 prompt rewrite inadvertently introduces
vocabulary that also flips N8/N9/N10, this catalog surfaces it before a full 17-N battery
run (per D-02: "allows early detection of N-side regression").

Run the baseline with:

```
python3 scripts/check-routing.py --catalog tests/routing-mini-catalog-p8.md --repeat 5 --min-pass 3
```

Run the verification gate with:

```
python3 scripts/check-routing.py --catalog tests/routing-mini-catalog-p8.md --repeat 3 --min-pass 2
```

---

## Positive Cases — Expected Verdict: DELEGATE

| # | Prompt | Expected Routing | Trigger Phrase Matched | Rationale |
|---|--------|-----------------|----------------------|-----------|
| P8 | "Take the modern smartphone form factor apart from the ground up. Decompose this problem: what do we actually know is true about why this shape and size won?" | DELEGATE | "decompose this problem" | Self-contained (software/business domain); literal "decompose this problem" trigger with from-the-ground-up framing |

---

## Negative Cases — Expected Verdict: NO-DELEGATE

| # | Prompt | Expected Routing | Off-Topic Class | Rationale |
|---|--------|-----------------|-----------------|-----------|
| N8 | "What's the difference between REST and GraphQL?" | NO-DELEGATE | General Q&A | Informational question — no first-principles or assumption-challenging framing |
| N9 | "Write a regex to match email addresses." | NO-DELEGATE | General Q&A | Task execution request — no analytical or first-principles framing |
| N10 | "How do I configure nginx as a reverse proxy?" | NO-DELEGATE | General Q&A | Factual how-to question — general Q&A, not delegated |
