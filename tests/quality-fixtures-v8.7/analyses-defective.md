# Fixture: D-18 Detector Self-Test — Defective Analysis

**Synthetic fixture, not evidence.** Hand-authored directly against
`shared/spine/references/output-template.md` to pin the mechanical defect
detector's non-zero case. Same skeleton as `analyses-conformant.md`, with
the original three deliberate defects — one untraced Conclusion claim, one
non-conforming Verdict cell, and one malformed Derivation Chains block —
plus three more (Phase 41, 999.120 H1): one HIGH chain over an unverified
ground truth, one HIGH chain over a MEDIUM chain, and one chain whose
confidence label cannot be parsed. No transport is involved — the
discretion resolution requiring real captures applies to transport
fixtures only.

---

## 1. Problem Essence

**Core problem:** Fixture problem statement for the D-18 detector's
defective self-test case.

**Success criteria:** The fixture deliberately violates all three defect
families exactly once.

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | Fixture assumption one | physical law | Accept as ground-truth candidate | Accept — physical law, confirmed by GT-1 | Fixture source |
| A2 | Fixture assumption two | untested belief | Verify or flag | **Unverified — flagged** | Fixture source |
| A3 | Fixture assumption three | convention | Challenge before use | Challenge — convention unconfirmed, needs probing | Fixture source |

---

## 3. Ground Truths

- **GT-1** Fixture ground truth one — source: fixture
- **GT-2** Fixture ground truth two — source: fixture
- **GT-3?** Fixture unverified ground truth three — source: fixture (unverified)

---

## 4. Derivation Chains

### Chain A — fixture chain one (well-formed)

GT-1 → fixture intermediate claim one → fixture conclusion one.

**Confidence: HIGH**

### Chain B — fixture chain two (malformed, presented as a table)

| Factor | Value |
|---|---|
| Fixture factor one | Fixture value one |
| Fixture factor two | Fixture value two |

**Confidence: HIGH**

### Chain C1 — fixture chain three (HIGH over an unverified ground truth)

GT-3? → fixture intermediate claim three → fixture conclusion three.

**Confidence:** HIGH

### Chain C2 — fixture chain four (MEDIUM)

GT-1 → fixture intermediate claim four → fixture conclusion four.

**Confidence: MEDIUM**

### Chain C3 — fixture chain five (HIGH over a MEDIUM chain)

C2 + GT-1 → fixture intermediate claim five → fixture conclusion five.

**Confidence:** HIGH

### Chain C4 — fixture chain six (unparsable confidence label)

GT-2 → fixture intermediate claim six → fixture conclusion six.

**Confidence:** [HIGH / MEDIUM / LOW]

---

## 5. Abandoned Reasoning

Nothing material here — this fixture has no abandoned reasoning to record.

---

## 6. Conclusion

**Recommended approach:** Per Chain A, adopt the fixture recommendation
because the intermediate claim establishes it directly for this synthetic
case.

**Key insight:** The fixture asserts a new finding here that names no chain
and no ground truth pair at all, so this claim is deliberately untraceable
to section 4.

1. Per Chain A, this fixture demonstrates one traced claim alongside the
   deliberately untraced one above.
