# Routing Mini-Catalog — P3 + P7 (v3.5 fragility validation)

**Purpose:** This is a subset of `tests/routing-catalog.md` containing only P3 and P7,
used for the FRAG-07 mini-battery gate. Run with:

```
python3 scripts/check-routing.py --catalog tests/routing-mini-catalog-p3p7.md --repeat 5 --min-pass 3
```

No N-cases are included because the mini-battery scope is the two fragile P-prompts only.
These two prompts had low baseline pass rates in v3.4 (P3: 0/3, P7: 1/3) and are the
primary target of the Phase 37 fixes. The mini-battery confirms both prompts cross the
DELEGATE threshold before running the full 23-prompt battery.

---

## Positive Cases — Expected Verdict: DELEGATE

| # | Prompt | Expected Routing | Trigger Phrase Matched | Rationale |
|---|--------|-----------------|----------------------|-----------|
| P3 | "Help me reason from ground truth about why a hot cup of coffee cools faster in its first ten minutes than in its second — what do we actually know is true?" | DELEGATE | "reason from ground truth" | Self-contained (science domain); natural mid-sentence embedding of trigger phrase per D-03 structural fix (v3.4 baseline: 0/3 — command-label-plus-colon framing suppressed delegation) |
| P7 | "What are the fundamental ground truths about why human memory degrades over time? Reason up from them to evaluate whether spaced repetition really works." | DELEGATE | "fundamental ground truths" + "reason up from first principles" | Self-contained (science domain); v3.4 baseline 1/3 — vocabulary gap: description lacked plural noun "fundamental ground truths" and particle-verb "Reason up from them"; closed by FRAG-03 description fix adding both paraphrases (Plan 01) |
