# Fixture: OBS-03 D-04 — Hop-Validity Non-Sequitur Observation Fixture

**Synthetic fixture, not evidence of model behaviour.** Hand-authored directly against
`shared/spine/references/output-template.md`'s chain-hop shape to pin the pure non-sequitur
case (D-04): a well-formed chain whose endpoint-bearing hop's arithmetic is correct but does
not follow, carrying a Criterion 4 Rigorous self-verdict.

---

## 1. Problem Essence

**Core problem:** Fixture problem statement for the OBS-03 D-04 non-sequitur observation
fixture — a service's latency headroom against its SLO ahead of a traffic doubling.

**Success criteria:** The fixture deliberately carries an endpoint-bearing hop (C1's
headroom-to-doubling hop) that is a pure non-sequitur — correct arithmetic, but the inference
does not follow from it — while every other rubric limb is satisfied and the chain carries a
Criterion 4 Rigorous self-verdict.

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | Fixture assumption | convention | Challenge before use | Accept — survives challenge | Fixture source |

---

## 3. Ground Truths

- **GT-1** The service's p99 latency is 180 ms — source: fixture; read-at-source: fixture
- **GT-2** The SLO requires p99 at most 200 ms — source: fixture; read-at-source: fixture
- **GT-3** Traffic doubled last quarter — source: fixture; read-at-source: fixture

---

## 4. Derivation Chains

### Conclusion C1: No capacity work is needed before the next traffic doubling

GT-1 (p99 180 ms) + GT-2 (SLO 200 ms) + GT-3 (traffic doubled)
→ the service has 200 − 180 = 20 ms of p99 headroom today
→ 20 ms of headroom means the service will stay within its SLO when traffic doubles again
→ no capacity work is needed before the next traffic doubling

**Pre-check:** head GT-1, GT-2, GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH

---

## 5. Abandoned Reasoning

### Dead End: Provisioning additional capacity ahead of the next doubling

**What was tried:** Considered provisioning additional capacity now, ahead of the next traffic
doubling, as a precaution.

**Why abandoned:** Chain C1 establishes that today's p99 headroom already covers the SLO, so
provisioning ahead of need was treated as unnecessary cost.

**What it ruled out:** Pre-emptive capacity provisioning as a standing response to the current
headroom reading.

---

## 6. Conclusion

**Recommended approach:** Do not provision additional capacity before the next traffic doubling (chain C1).

**Pre-check:** head C1 (HIGH) · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** (chain C1) HIGH

**Criterion 4: Reason Upward**
Band: **Rigorous**
Justification: fixture self-audit claim.
