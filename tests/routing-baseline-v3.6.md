# Routing-Battery Canonical Baseline — v3.6 (post-CAT-expansion, P9/P10/N16/N17)

**Recorded:** 2026-05-26
**Script version:** v3.6 (`--repeat 3 --min-pass 2` for P1-P8/N1-N15; `--repeat 5 --min-pass 3` for P9/P10/N16/N17 via mini-battery)
**Battery verdict:** PASS
**Summary:** P 8/10, N 17/17

---

## Per-prompt results

| # | Expected | Runs | Matches | K/N | Verdict |
|---|----------|------|---------|-----|---------|
| P1 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P2 | DELEGATE | 3 | 1 | 1/3 | FAIL |
| P3 | DELEGATE | 3 | 1 | 1/3 | FAIL |
| P4 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P5 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P6 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P7 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P8 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P9 | DELEGATE | 5 | 3 | 3/5 | PASS |
| P10 | DELEGATE | 5 | 5 | 5/5 | PASS |
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
| N16 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |
| N17 | NO-DELEGATE | 5 | 5 | 5/5 | PASS |

---

## How this baseline was produced

**P1-P8 and N1-N15** were measured in Phase 38 (v3.5 baseline) using:

```bash
python3 scripts/check-routing.py --catalog tests/routing-catalog.md --repeat 3 --min-pass 2
```

Run date: 2026-05-25. Source: `tests/routing-baseline-v3.5.md`. These rows are carried forward verbatim — no catalog row changes, no skill description changes, and no script changes occurred between the v3.5 baseline and Phase 40.

**P9, P10, N16, N17** (new in Phase 39 / v3.6) were measured in Phase 40 Plan 01 (CAT-08 mini-battery) using:

```bash
python3 scripts/check-routing.py --catalog tests/routing-mini-catalog-v3.6.md --repeat 5 --min-pass 3 --p-threshold 2 --n-threshold 2
```

Run date: 2026-05-26. The mini-catalog (`tests/routing-mini-catalog-v3.6.md`) contains only P9, P10, N16, N17 — rows copied verbatim from `tests/routing-catalog.md`. The `--repeat 5 --min-pass 3` protocol applies stricter per-prompt thresholds than the full-battery `--repeat 3 --min-pass 2` standard; all four prompts exceeded their individual thresholds (P9: 3/5, P10: 5/5, N16: 5/5, N17: 5/5).

**Battery verdict computation (CAT-06 scaled thresholds):**
- P-threshold: >= 8/10. Achieved: 8/10 (P2 and P3 remain FAIL — same as v3.5; within documented noise envelope).
- N-threshold: >= 15/17. Achieved: 17/17.

This baseline records the Phase 39 catalog expansion (CAT-01 through CAT-07: two P-prompts and two N-prompts added covering science/chemistry and earth-science domains, thresholds rescaled to P >= 8/10 and N >= 15/17) and Phase 40 validation (CAT-08 mini-battery gate, CAT-09 measurement, CAT-10 baseline commit).

---

## Changes from v3.5

**New prompts (P9, P10, N16, N17):** All four PASS on first measurement.

**Continuing failures (P2, P3):** Both remained below K=2 out of 3, consistent with v3.5. Not regressions — P2 and P3 have been within the documented ±3 noise envelope since v3.4. See `tests/routing-baseline-v3.5.md` (Failure modes section) for full investigation notes.

**Summary line change:** v3.5 recorded `P 6/8, N 15/15`; v3.6 records `P 8/10, N 17/17` — the denominator increase reflects catalog expansion, not scoring regression.

---

## Coexistence note

`tests/routing-baseline-v3.5.md` remains the v3.5 historical record per D-04 and is unmodified. No references in `ROADMAP.md` or `PROJECT.md` are updated to point at v3.6 in this plan — coexistence is the contract.
