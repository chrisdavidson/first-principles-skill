# Analysis: Should the payments team keep the new fee schedule or roll it back?

A first-principles analysis of whether to keep last month's fee-schedule change for the payments
platform or roll it back before the next merchant billing cycle.

---

## 1. Problem Essence

**Core problem:** The fee-schedule change introduced last month raised per-transaction revenue
but coincided with a rise in merchant churn. Should the payments team keep the new schedule, or
roll it back before the next merchant billing cycle?

**Success criteria:**

- The revenue case for keeping the schedule is derived from the measured per-transaction figures,
  not from the headline revenue total alone.
- The churn case for rolling it back is derived from the measured merchant-retention figures, not
  from anecdotal merchant complaints.
- The recommendation states which measured facts justify it and which do not.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| The churn increase is caused by the fee-schedule change specifically | untested belief | Challenge before use — churn could also be driven by unrelated seasonal or competitive factors during the same window | Challenge — the retention report attributes only part of the churn increase to fee-related cancellation reasons | The cancellation-survey data records fee-related reasons for a majority, not all, of the additional churned merchants; other reasons are also present in the same window |
| Rolling back the schedule would fully restore the pre-change churn rate | untested belief | Challenge before use — a rollback removes the fee driver but does not reverse merchants who have already switched providers | Discard — churned merchants who have already migrated are not recoverable by a rollback alone | The retention team's own post-mortem on prior rollbacks confirms churned merchants rarely return within the same billing cycle |

---

## 3. Ground Truths

- **GT-1** Per-transaction net revenue rose from $0.34 to $0.41 in the four weeks following the
  fee-schedule change — source: the billing system's own per-transaction revenue report.

- **GT-2** Merchant cancellations attributing "pricing" as the stated reason rose from 6 per week
  to 14 per week over the same four-week window — source: the merchant-retention team's exit
  survey report, filtered to the "pricing" reason code.

---

## 4. Derivation Chains

### Conclusion C1: The revenue gain from the fee-schedule change is real and material
GT-1 (per-transaction net revenue rose from $0.34 to $0.41) → the $0.07 per-transaction increase, applied across the platform's measured transaction volume for the same four-week window, produces a revenue gain large enough to be material at the portfolio level → the fee-schedule change is producing a real, measurable revenue gain

This gain is only worth keeping once the retention picture in Conclusion C2 has been weighed
against it, since a revenue gain that is offset by an equal or larger loss from churned merchant
volume would not be a net improvement — and C2's own churn-driven revenue loss is itself
calculated by assuming the fee-schedule change in this chain stays in place.

**Confidence: MEDIUM** — the per-transaction figure (GT-1) is directly measured; whether the gain
is net-positive depends on weighing it against C2.

---

### Conclusion C2: The churn-driven revenue loss should be weighed against keeping the schedule
GT-2 (pricing-attributed cancellations rose from 6/week to 14/week) → the additional 8 pricing-attributed cancellations per week, valued at the platform's average per-merchant transaction revenue, produces a recurring revenue loss that compounds with each additional week the schedule remains in place → the churn-driven loss is a real, growing cost of keeping the fee-schedule change

This loss is only a fair comparison against the revenue gain in Conclusion C1 once C1's per-
transaction gain is confirmed to persist under the new schedule, since the churn-driven loss
calculated here is itself premised on the new schedule — the one C1 justifies keeping — remaining
in effect for the merchants who have not yet churned.

**Confidence: MEDIUM** — the cancellation figure (GT-2) is directly measured; whether the loss
outweighs the gain depends on weighing it against C1.

---

## 5. Abandoned Reasoning

### Dead End: Decide from the headline revenue total alone

**What was tried:** Treat the platform's month-over-month total revenue figure as sufficient on
its own — reason directly from "total revenue is up" to "therefore keep the schedule."

**Why abandoned:** The headline total blends the per-transaction gain (GT-1) with the volume
effect of the churned merchants (GT-2) in a single number, which obscures whether the gain would
survive further churn. The two ground truths were separated into distinct chains specifically
because the blended total cannot be decomposed back into "gain per transaction" and "loss per
churned merchant" once merged.

**What it ruled out:** Treating the single blended revenue total as a sufficient basis for the
keep-or-rollback decision.

---

## 6. Conclusion

1. (chain C1) The fee-schedule change is producing a real, measurable per-transaction revenue
   gain of $0.07 on average.
2. (chain C2) The churn-driven revenue loss from pricing-attributed cancellations is real and
   growing, and should be weighed directly against the gain in chain C1 before the next billing
   cycle.

**Confidence: MEDIUM** — both chains rest on real measured ground truths (GT-1, GT-2); each
chain's own confidence in its practical conclusion also depends on the other chain's figure.
