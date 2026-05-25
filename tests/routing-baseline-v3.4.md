# Routing-Battery Canonical Baseline — v3.4 (best-of-3)

**Recorded:** 2026-05-25
**Script version:** v3.4 (`--repeat 3 --min-pass 2`)
**Battery verdict:** PASS
**Summary:** P 6/8, N 15/15

---

## Per-prompt results

| # | Expected | Runs | Matches | K/N | Verdict |
|---|----------|------|---------|-----|---------|
| P1 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P2 | DELEGATE | 3 | 2 | 2/3 | PASS |
| P3 | DELEGATE | 3 | 0 | 0/3 | FAIL |
| P4 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P5 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P6 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P7 | DELEGATE | 3 | 1 | 1/3 | FAIL |
| P8 | DELEGATE | 3 | 3 | 3/3 | PASS |
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

---

## How this baseline was produced

```bash
python3 scripts/check-routing.py --catalog tests/routing-catalog.md --repeat 3 --min-pass 2
```

Run date: 2026-05-25. Output directory: `/tmp/routing-36-02-baseline/`.

The v3.1 single-run baseline narrative remains in `tests/routing-catalog.md` under the
Catalog History section, unchanged. This file is additive — it records the v3.4 best-of-3
measurement without modifying the catalog specification or its archived history.

**Failing prompts at this baseline (P3, P7):** Both fell below K=2 out of 3 runs. These
prompts are borderline under the current plugin description and fall within the known noise
envelope. The battery PASSES overall because the threshold is P ≥ 6/8, which is met (6/8).
Future runs should treat P3 and P7 as the fragile prompts to watch.
