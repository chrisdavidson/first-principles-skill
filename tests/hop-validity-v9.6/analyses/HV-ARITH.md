# Fixture: OBS-03 D-01 — Hop-Validity Arithmetic Trip Fixture

**Synthetic fixture, not evidence of model behaviour.** Hand-authored directly against
`shared/spine/references/output-template.md`'s chain-hop shape to pin the hop-arithmetic
detector's trip case (D-01): a well-formed chain whose endpoint-bearing hop's stated
arithmetic does not recompute, carrying a Criterion 4 Rigorous self-verdict.

---

## 1. Problem Essence

**Core problem:** Fixture problem statement for the OBS-03 D-01 hop-arithmetic trip fixture —
a fuel depot's delivery fleet and its daily fuel balance.

**Success criteria:** The fixture deliberately carries an endpoint-bearing hop (C2's fuel-burn
hop) whose stated arithmetic does not recompute, while every chain and the §6 roll-up carry a
well-formed pre-check and a Criterion 4 Rigorous self-verdict.

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | Fixture assumption | convention | Challenge before use | Accept — survives challenge | Fixture source |

---

## 3. Ground Truths

- **GT-1** The delivery fleet has 40 vans — source: fixture; read-at-source: fixture
- **GT-2** Each van averages 150 km per day — source: fixture; read-at-source: fixture
- **GT-3** Fuel consumption is 0.25 L per km — source: fixture; read-at-source: fixture
- **GT-4** The depot delivers 1,300 L of fuel per day — source: fixture; read-at-source: fixture

---

## 4. Derivation Chains

### Conclusion C1: The fleet's daily distance is 6,000 km

GT-1 (40 vans) + GT-2 (150 km per van per day)
→ the fleet drives 40 × 150 = 6,000 km per day
→ over a five-day week that is 40 × 150 × 5 = 30,000 km
→ the fleet's daily distance is 6,000 km

**Pre-check:** head GT-1, GT-2 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH

### Conclusion C2: The depot's daily fuel delivery covers the fleet's daily burn

C1 (6,000 km per day) + GT-3 (0.25 L per km) + GT-4 (1,300 L per day)
→ daily fuel burn is 6,000 × 0.25 = 1,200 L
→ the 1,300 L daily delivery covers the fleet's burn with 100 L to spare

**Pre-check:** head C1 (HIGH), GT-3, GT-4 · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** HIGH

---

## 5. Abandoned Reasoning

### Dead End: Running a second delivery route to cover a projected shortfall

**What was tried:** Considered scheduling a second daily delivery run to the depot as a hedge
against a fuel shortfall.

**Why abandoned:** Chain C2 establishes that the existing 1,300 L delivery already covers the
fleet's daily burn with 100 L to spare, so a second run adds cost against no shortfall.

**What it ruled out:** A second delivery run as a standing operational change.

---

## 6. Conclusion

**Recommended approach:** Keep the single daily 1,300 L delivery; no change to the depot's delivery schedule is needed (chain C2).

**Pre-check:** head C2 (HIGH) · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** (chain C2) HIGH

**Criterion 4: Reason Upward**
Band: **Rigorous**
Justification: fixture self-audit claim.
