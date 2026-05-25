# 38-01 Mini-Battery Result — FRAG-07 Gate

**Date run:** 2026-05-25
**Catalog:** `tests/routing-mini-catalog-p3p7.md` (P3 + P7 only)
**Command:**
```
python3 scripts/check-routing.py --catalog tests/routing-mini-catalog-p3p7.md --repeat 5 --min-pass 3
```

---

## Per-Prompt K/N Scores

| Prompt | K/N Score | Threshold | Verdict |
|--------|-----------|-----------|---------|
| P3     | 4/5       | >= 3/5    | PASS    |
| P7     | 2/5       | >= 3/5    | FAIL    |

---

## Gate Verdict

**GATE FAIL**

P7 scored 2/5 DELEGATE (threshold: >= 3/5). Per D-04, the full battery (FRAG-08, Plan 02 `38-02-PLAN.md`) WILL NOT be run. Phase 38 is incomplete.

**Required next step:** Return to Phase 37 diagnosis. Investigate why P7 is still failing despite the FRAG-03 description fix (plural noun "fundamental ground truths" and particle-verb "Reason up from them" were added). The Phase 37 fix appears insufficient — the 2/5 score is marginally improved from the v3.4 baseline of 1/3, but does not meet the 3/5 gate threshold.

---

## Raw Battery Output

```
check-routing: catalog has 2 P + 0 N (total 2)
  plugin-dir: /home/chrisdavidson/programming/first-principles-skills/first-principles
  out:        /tmp/check-routing-20260525T102420Z
  thresholds: P >= 6, N >= 14
  repeat:     5 (K-of-N, min-pass=3)
[1/2] P3: expected=DELEGATE ...
    -> 4/5 PASS
[2/2] P7: expected=DELEGATE ...
    -> 2/5 FAIL
BATTERY: FAIL
P: 1/2  N: 0/0

Failed prompts:
  P7: expected=DELEGATE 2/5 match

Per-prompt K/N (best-of-5, K=3):
  P3: 4/5 PASS
  P7: 2/5 FAIL
```

---

*Log file: `/tmp/routing-38-01-mini.log`*
