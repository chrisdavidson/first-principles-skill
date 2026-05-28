# Routing-Battery Canonical Baseline — v3.7 (post-rubric-hardening)

**Recorded:** 2026-05-27
**Script version:** v3.7 (`--repeat 3 --min-pass 2`)
**Battery verdict:** PASS
**Summary:** P 10/10, N 17/17

---

## Per-prompt results

| # | Expected | Runs | Matches | K/N | Verdict |
|---|----------|------|---------|-----|---------|
| P1 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P2 | DELEGATE | 3 | 2 | 2/3 | PASS |
| P3 | DELEGATE | 3 | 2 | 2/3 | PASS |
| P4 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P5 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P6 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P7 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P8 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P9 | DELEGATE | 3 | 2 | 2/3 | PASS |
| P10 | DELEGATE | 3 | 3 | 3/3 | PASS |
| N1 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N2 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N3 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N4 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N5 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N6 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N7 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N8 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N9 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N10 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N11 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N12 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N13 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N14 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N15 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N16 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N17 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |

---

## How this baseline was produced

**P1–P10 and N1–N17** were measured in Phase 44 (v3.7 routing regression validation) using:

```bash
python3 scripts/check-routing.py \
  --catalog tests/routing-catalog.md \
  --repeat 3 --min-pass 2 \
  2>&1 | tee /tmp/routing-44-01/full.log
```

Run date: 2026-05-27. Output directory: `/tmp/routing-44-01/` (transient; full log at `/tmp/routing-44-01/full.log`).

**Battery verdict computation (CAT-06 scaled thresholds):**
- P-threshold: >= 8/10. Achieved: 10/10.
- N-threshold: >= 15/17. Achieved: 17/17.

This baseline validates the Phase 42/43 rubric-hardening changes (descriptions and response-format guidance updated for clarity and precision). No catalog rows were added or removed relative to v3.6.

---

## Changes from v3.6

# NO REGRESSIONS

All 25 PASS-obligation prompts (P1, P4–P10, N1–N17) retained PASS in v3.7.

**Improvements (P2, P3):** Both were FAIL in v3.6 (1/3 each). In v3.7 they improved to 2/3 PASS. These continuing FAIL-to-PASS improvements are NOT regressions per D-04 — P2 and P3 carried no PASS obligation in v3.6. Recorded for traceability only.

**P9:** Was 3/5 PASS in v3.6 (measured with `--repeat 5 --min-pass 3`). Is 2/3 PASS in v3.7 (measured with `--repeat 3 --min-pass 2`). No regression — both K/N ratios satisfy their respective thresholds.

**Overall improvement:** v3.6 recorded P 8/10; v3.7 records P 10/10. The rubric changes in Phases 42/43 did not degrade routing — they strengthened two previously borderline prompts.

Full regression comparison: `/tmp/routing-44-01/regression-table.md`

---

## Coexistence note

`tests/routing-baseline-v3.6.md` remains the v3.6 historical record per D-04 and is unmodified. No references in `ROADMAP.md` or `PROJECT.md` are updated to point at v3.7 in this plan — coexistence is the contract.
