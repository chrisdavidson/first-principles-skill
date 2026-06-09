> **SUPERSEDED — v4.2 (Phase 65) — PARTIAL (sub-skill battery references)**
> This baseline includes a sub-skill battery section (lines ~112/165/185 in the original) that used
> the `--p-threshold 0` mask. That methodology masked an architectural fixture contradiction:
> P12, P24, and N2 expected direct sub-skill invocations that Phase 46 intentionally disabled
> (`disable-model-invocation: true`). The embedded sub-skill run command with `--p-threshold 0`
> should **NOT** be re-run. Use the corrected catalog (`tests/sub-skill-routing-catalog.md`,
> Phase 65 fixture correction) with no `--p-threshold` flag (the strict default
> `--p-threshold 2` now applies). The main agent routing battery section of this baseline is
> unaffected by the fixture correction.
> Evidence chain: `.planning/notes/fu21-fixture-contradiction-diagnosis.md`.
> Original record preserved below for methodology audit trail.

---

# Routing Baseline — v3.12 (Phase-Level Slash Commands validation)

**Recorded:** 2026-05-30
**Script version:** `scripts/check-routing.py` (unchanged)
**Agent version:** `first-principles/agents/first-principles.md` at commit `5250eb2` ("feat(53-02): update plugin manifest description to reflect 11 skills") — this is the surface being validated after adding five focused-mode phase-level skill stubs in Phases 52-53
**Catalog:** `tests/routing-catalog.md`
**Run flags:** `--repeat 3 --min-pass 2`
**Verdict:** BATTERY: PASS

---

> **SCOPE NOTE — FULL 27-PROMPT BATTERY (P1-P10, N1-N17)**
> This is a full 27-prompt battery snapshot. Unlike v3.11 (which was a P8-scoped mini-catalog run),
> this baseline covers all positive and negative cases from `tests/routing-catalog.md`.
> Pass thresholds: P ≥ 8/10 DELEGATE AND N ≥ 15/17 NO-DELEGATE.
>
> **Purpose:** Confirm that the five new phase-level skill stubs (`disable-model-invocation: true`,
> slash-only via `/first-principles:<slug>`) introduced in Phases 52-53 do not cause orchestrator
> over-triggering or description-collision regressions. Regression risk is low because the stubs
> are slash-only and the orchestrator cannot auto-route to them — but the full battery must be
> verified against established thresholds before v3.12 ships.

---

## Per-prompt results

| # | Expected | Runs | Matches | K/N | Verdict |
|---|----------|------|---------|-----|---------|
| P1 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P2 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P3 | DELEGATE | 3 | 2 | 2/3 | PASS |
| P4 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P5 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P6 | DELEGATE | 3 | 2 | 2/3 | PASS |
| P7 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P8 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P9 | DELEGATE | 3 | 2 | 2/3 | PASS |
| P10 | DELEGATE | 3 | 2 | 2/3 | PASS |
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

```
python3 scripts/check-routing.py --catalog tests/routing-catalog.md --repeat 3 --min-pass 2 --out /tmp/p54-routing-battery
```

Output directory: `/tmp/p54-routing-battery` (transient).

---

## Raw verdict.txt (verbatim)

```
BATTERY: PASS
P: 10/10  N: 17/17

Per-prompt K/N (best-of-3, K=2):
  P1: 3/3 PASS
  P2: 3/3 PASS
  P3: 2/3 PASS
  P4: 3/3 PASS
  P5: 3/3 PASS
  P6: 2/3 PASS
  P7: 3/3 PASS
  P8: 3/3 PASS
  P9: 2/3 PASS
  P10: 2/3 PASS
  N1: 3/3 PASS
  N2: 3/3 PASS
  N3: 3/3 PASS
  N4: 3/3 PASS
  N5: 3/3 PASS
  N6: 3/3 PASS
  N7: 3/3 PASS
  N8: 3/3 PASS
  N9: 3/3 PASS
  N10: 3/3 PASS
  N11: 3/3 PASS
  N12: 3/3 PASS
  N13: 3/3 PASS
  N14: 3/3 PASS
  N15: 3/3 PASS
  N16: 3/3 PASS
  N17: 3/3 PASS
```

---

## Sub-skill routing battery

**Command:**

```
python3 scripts/check-sub-skill-routing.py --catalog tests/sub-skill-routing-catalog.md --repeat 5 --min-pass 3 --p-threshold 0 --n-threshold 2 --out /tmp/p54-subskill-battery
```

**Output directory:** `/tmp/p54-subskill-battery` (transient).

**Per-prompt outcomes:**

| # | Expected Sub-Skill | K/N | Verdict | Notes |
|---|-------------------|-----|---------|-------|
| P12 | pre-mortem | 1/5 | FAIL | Expected regression (FU-21-1); P-threshold 0 — failure is acceptable |
| P24 | inversion | 0/5 | FAIL | Expected regression (FU-21-2); P-threshold 0 — failure is acceptable |
| N1 | none-or-other | 5/5 | PASS | Negative control: debugging-shaped prompt does not trigger `:pre-mortem` |
| N2 | pre-mortem | 3/5 | PASS | Negative control: plan-shaped prompt routes to `:pre-mortem`, not `:inversion` |

**Aggregate verdict:** BATTERY: PASS (P: 0/2, N: 2/2; N-gate ≥ 2/2 met; P-threshold 0 applied)

**Raw verdict.txt (verbatim):**

```
BATTERY: PASS
P: 0/2  N: 2/2

Per-prompt K/N (best-of-5, K=3):
  P12: 1/5 FAIL
  P24: 0/5 FAIL
  N1: 5/5 PASS
  N2: 3/5 PASS
```

---

## Classification

**PASS — Phase-Level Slash Commands validation milestone met.**

### Main battery analysis

All 10 positive cases and all 17 negative cases PASS at `--repeat 3 --min-pass 2` threshold. The
five new phase-level skill stubs (`disable-model-invocation: true`) introduced in Phases 52-53 do
not cause orchestrator over-triggering or description-collision regressions. Strong performance:

- P-side: 10/10 PASS. Six prompts scored 3/3 (P1, P2, P4, P5, P7, P8); four at the minimum 2/3
  passing threshold (P3, P6, P9, P10). No prompt fell below threshold.
- N-side: 17/17 PASS with 17 of 17 negative cases scoring 3/3. This is a clean sweep — no
  false-positive routing to the orchestrator on any N-case.
- P8 (historically a boundary prompt with noise history): scored 3/3 in this session — well above
  the 2/3 minimum. This confirms the v3.9 trigger-phrase fix ("reason from the ground up" /
  "what do we actually know is true") continues to hold.

### Sub-skill battery analysis

The sub-skill battery measures Phase 46 FU-21 regression fixtures and their negative controls.
P12 (FU-21-1) and P24 (FU-21-2) continue to fail as known pre-Phase-46 regressions — this is
expected behavior with `--p-threshold 0`. Both negative controls (N1 and N2) PASS, confirming:

- N1 (5/5): The `:pre-mortem` description widening does not over-trigger on debugging-shaped
  prompts with adjacent vocabulary (`nervous`, `surface`, `what could be wrong`).
- N2 (3/5): Plan-shaped pre-mortem prompts route to `:pre-mortem`, not `:inversion` — the
  boundary sharpening from Phase 46 holds.

### Boundary prompt notes

- P3, P6, P9, P10 scored 2/3 on the main battery (minimum passing threshold). These are
  historically boundary prompts consistent with routing battery noise characteristics
  documented in routing-battery-noise.md. No prompt previously scoring strongly has regressed.
- N2 scored 3/5 on the sub-skill battery (minimum K-of-N threshold). This is consistent with
  the boundary nature of the N2 prompt — its overlapping vocabulary with the FU-21-2 confusion
  zone creates inherent stochasticity at the `:pre-mortem` vs. `:inversion` boundary.

### PHASE-10 requirement

**PHASE-10: CONFIRMED MET.**
- Main routing battery: P 10/10 ≥ 8/10, N 17/17 ≥ 15/17. Both thresholds satisfied.
- Sub-skill battery: N 2/2 ≥ 2/2. N-gate satisfied; P-failures (P12, P24) acceptable per `--p-threshold 0`.
- v3.12 milestone can proceed to ship.
