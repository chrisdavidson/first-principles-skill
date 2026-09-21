# Fixture: OBS-02 SC3 — Confidence Pre-Check / Roll-Up Composition Fixture

**Synthetic fixture, not evidence of model behaviour.** Hand-authored directly against
`shared/spine/references/output-template.md`'s confidence pre-check shape (OBS-01) to pin the
mechanical composition detector's non-zero case. No transport is involved.

---

## 1. Problem Essence

**Core problem:** Fixture problem statement for the OBS-02 SC3 pre-check/roll-up fixture.

**Success criteria:** The fixture deliberately carries a §6 roll-up rated above both of its own
cited §4 chains, while every §4 chain and the §6 roll-up itself carry a well-formed pre-check.

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | Fixture assumption | convention | Challenge before use | Accept — survives challenge | Fixture source |

---

## 3. Ground Truths

- **GT-1** Fixture ground truth one — source: fixture; read-at-source: fixture
- **GT-2** Fixture ground truth two — source: fixture; read-at-source: fixture
- **GT-3?** Fixture unverified ground truth three — unverified: fixture reason

---

## 4. Derivation Chains

### Conclusion C1: Fixture conclusion one

GT-1 + GT-3? → fixture intermediate claim one → fixture conclusion one.

**Pre-check:** head GT-1, GT-3? · ?-marked: GT-3? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. GT-3? is unverified; verifying it at source would remove it as a cause of the downgrade.

### Conclusion C2: Fixture conclusion two

GT-2 → fixture intermediate claim two → fixture conclusion two.

**Pre-check:** head GT-2 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM. The downgrade is driven by an unpriced inference step between the intermediate claim and the conclusion; recomputing that step independently of the chain text would remove it as a cause of the downgrade.

---

## 5. Abandoned Reasoning

Nothing material here — this fixture has no abandoned reasoning to record.

---

## 6. Conclusion

**Recommended approach:** Adopt the fixture recommendation the two chains jointly establish (chains C1 and C2).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** (chains C1 and C2) HIGH

**Criterion 5: Conclusion**
Band: **Rigorous**
Justification: fixture self-audit claim.
