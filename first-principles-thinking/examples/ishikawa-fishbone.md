# Worked Example: Service Business and B2B SaaS

A complete first-principles analysis of a B2B SaaS customer-churn problem, following the
standardized output format and showing at least one abandoned reasoning path. A "Fishbone
Brainstorm" preamble precedes the six sections, demonstrating how a fishbone diagram
generates hypotheses that enter Phase 2 as `untested belief` rows — not verified findings.
Authored in Phase 8.

**Scenario.** Northbrook Analytics is a B2B SaaS company offering a data-integration and
reporting platform to mid-market operations teams. Contracts run $18,000–$40,000 per year
and renew annually. In Q1 the quarterly churn rate was 4.1%; by the end of Q3 it had risen
to 9.2% — a 124% increase over two quarters. The Customer Success team has flagged rising
support-ticket volume and a drop in feature-adoption scores, but the company has not
identified whether churn is driven by offer gaps, pricing pressure, onboarding failure,
service quality, competitive displacement, or some combination. Leadership has instructed
the team to "find the root cause of churn and fix it."

---

## Fishbone Brainstorm

*Pre-analysis artifact, not a numbered output section. Its outputs — category-selection
decision, cause map, and 5-Whys root cause — feed directly into the six output sections below.*

### Category-selection decision

**Effect:** Northbrook Analytics' quarterly churn rose from ~4% to ~9% over two quarters.

Three candidate category sets:

- **Default six** (People, Process, Technology & Tools, Environment, Information, Resources):
  domain-neutral and always valid, but does not surface the offer, pricing, and channel axes
  most relevant to subscription-business churn.
- **8P** (Product, Price, Place, Promotion, People, Process, Physical Evidence, Productivity):
  built for a service or marketing context; all eight axes map plausibly onto B2B SaaS churn
  drivers.
- **4S** (Surroundings, Suppliers, Systems, Skills): too narrow — churn spans offer design
  and pricing, outside 4S's scope.

**Decision: lock 8P.** The churn signal is diffuse across offer, channel, and delivery axes
— precisely the scenario 8P targets. ISH-04 says to prefer a named preset when the domain
maps clearly and labels are not forced; 8P is not forced here. Two labels that need a SaaS
reading: **Physical Evidence** — tangible quality signals the customer sees (UI,
documentation, report formatting); **Place** — the delivery channel (onboarding path,
support access, account-management touchpoints).

---

### Fishbone cause map

**Effect:** Northbrook Analytics quarterly churn rose from ~4% to ~9% over two quarters.

- **Product** — feature gaps vs. competitors; data-refresh reliability below contracted SLA
- **Price** — perceived value does not justify renewal; new entrants offering lower pricing
- **Place** *(delivery channel)* — onboarding leaves customers under-activated; $18K–$25K
  tier accounts have no dedicated CSM; renewals not initiated until 30 days before expiry
- **Promotion** — new feature value not communicated to existing customers; no 6-month
  business-review to make the renewal case proactively
- **People** — CSM headcount grew 10% while the customer base grew 40% over 18 months;
  no training on health-score interpretation or proactive intervention
- **Process** — no systematic health scoring surfaced to the CS team; renewal-initiation
  trigger is 60 days before expiry; evidence suggests decisions are made 90–120 days out
- **Physical Evidence** *(UI, docs, report outputs)* — dashboard UI not refreshed in 18
  months; help articles not updated to reflect recent releases
- **Productivity** *(customer-realised gain)* — workflow-automation rate ~40% below the
  sales-demo benchmark; time-to-first-insight averages 6 weeks vs. the 2-week sales figure

---

### Prioritise and verify — 5-Whys depth drill

**Selected branch: "Account management coverage gaps" (Place category)**

**Evidence reasoning:** Exit-interview data from 11 of 23 churned accounts in Q2–Q3
explicitly cites "felt unsupported" or "no one checked in" — the highest-frequency explicit
signal in available qualitative data.

**Symptom:** Northbrook Analytics customers in the $18K–$25K tier are churning at a
disproportionately high rate relative to higher-value tiers.

- Why? → Accounts in this tier have no dedicated Customer Success Manager.
  - Why? → CSM headcount growth (10%) has not kept pace with customer-base growth (40%),
    so coverage thresholds were raised and the lowest-value tier was de-prioritised.
    - Why? → The CS coverage model was not revised as the company scaled; no formal trigger
      exists to revisit coverage thresholds when headcount ratios drift.
      - Why? → There is no owned process for reviewing CS capacity ratios at a cadence
        faster than the annual planning cycle; gaps accumulate silently between rounds.
        - **Stop:** Root cause — absence of a recurring CS capacity-review process that
          adjusts coverage thresholds when customer-base growth outpaces headcount growth.
          Corrective action: establish a quarterly CS capacity review with a defined ratio
          trigger (CSM-to-account ratio exceeds 1:45 in any tier → coverage model reviewed
          and revised). Specific, within the company's control, prevents recurrence.

---

## 1. Problem Essence

**Core problem:** Which causal factors are actually driving Northbrook Analytics' churn
increase from ~4% to ~9%, and which interventions will address those factors at the lowest
cost and highest reversibility — evaluated independently of any single proposed fix?

The triggering instruction — "find the root cause of churn and fix it" — treats churn as
if it has a single cause. A 124% increase over two quarters in a B2B SaaS business is
almost never mono-causal: the fishbone brainstorm confirms plausible contributors across
at least five category axes. The analysis reframes the question from "what is the one root
cause?" to "which factors are verified, which are hypotheses, and what is the minimum
intervention set that addresses the verified ones?"

**Success criteria:**

- At least one causal factor is identified with supporting evidence; specific enough that an
  intervention can be designed, executed, and measured.
- The analysis distinguishes verified contributors from unverified hypotheses — no fishbone
  branch is treated as a confirmed finding without evidence.
- The recommended intervention set addresses verified contributors without requiring all
  eight 8P branches to be executed simultaneously.
- After the recommended interventions, quarterly churn is measurably lower than 9.2% within
  two renewal cohorts.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| Feature gaps versus competitors are causing churn | untested belief | Verify — establish whether churned accounts requested specific missing features available from competitors they switched to. | Challenge | unverified — flagged; exit interviews mention feature gaps in 7 of 23 churned accounts but do not specify which features; requires win/loss analysis |
| Competitor pricing is undercutting Northbrook's renewals | untested belief | Verify — benchmark competitor pricing against Northbrook's average contract value before treating this as a confirmed contributor. | Challenge | unverified — flagged; two new entrants have launched but their pricing has not been benchmarked against Northbrook's contract structure |
| Onboarding failure leaves customers under-activated | untested belief | Verify — compare feature-adoption scores and time-to-first-insight between churned and retained cohorts. | Challenge | unverified — flagged; adoption scores are collected but not segmented by churn outcome; requires a data pull |
| Accounts without a dedicated CSM churn at a higher rate | untested belief | Verify — segment churn rate by CSM coverage status; if the $18K–$25K tier has a materially higher rate than covered tiers, the coverage gap is a confirmed contributor. | Challenge | unverified — flagged; exit-interview signal is present (11 of 23 churned accounts) but cohort-level comparison has not been run |
| The absence of a recurring CS capacity-review process is the structural root cause of the coverage gap | untested belief | Verify — confirm that no capacity-review process exists and that the ratio has drifted beyond the design threshold; confirmed via CS Director debrief. | Accept | Confirmed: CS Director confirmed ratios are reviewed only at annual planning; CSM-to-account ratio in the $18K–$25K tier is currently 1:67 vs. a design threshold of 1:40 |
| New feature value is not communicated to existing customers | untested belief | Verify — measure open and click-through rates on in-app changelog and renewal-cycle emails. | Challenge | unverified — flagged; CS team reports low feature-awareness anecdotally but engagement data has not been pulled |
| Customers are not achieving the productivity outcome promised at sale | untested belief | Verify — compare workflow-automation rate across a statistically valid sample of active accounts against the sales-demo benchmark. | Challenge | unverified — flagged; ~40% shortfall is a preliminary estimate from 4 accounts only |
| A full product overhaul is required to halt churn | convention | Explicitly challenge — the instinct to "fix the product" when churn rises is a common convention; the highest-frequency exit-interview signal is "felt unsupported," not a product-feature complaint. | Challenge | Not supported by available evidence; product-overhaul framing is premature |

---

## 3. Ground Truths

- **GT-1** Northbrook Analytics' quarterly churn rate rose from 4.1% in Q1 to 9.2% by the
  end of Q3 — a 124% increase over two quarters — source: company subscription and CRM
  records, verified against the billing system by the finance team

- **GT-2** Exit-interview data from 11 of 23 accounts that churned in Q2–Q3 explicitly cites
  "felt unsupported" or "no one checked in" as a primary or secondary churn reason — source:
  CS team exit-interview log (raw verbatims, Q2–Q3), reviewed and confirmed by the CS Director

- **GT-3** The CS team's headcount grew 10% over 18 months while the customer base grew 40%;
  the CSM-to-account ratio in the $18K–$25K tier is currently 1:67 against a design threshold
  of 1:40 — source: CS Director debrief; headcount and customer-count figures from HR and CRM
  records respectively

- **GT-4** Coverage ratios are reviewed only at annual planning; no recurring process exists
  to adjust coverage thresholds when the CSM-to-account ratio drifts beyond the design
  threshold mid-year — source: CS Director debrief; no documented mid-year capacity-review
  procedure exists in CS operations documentation

- **GT-5?** The average workflow-automation rate achieved by active Northbrook accounts is
  approximately 40% below the benchmark figure used in sales demos — source: unverified;
  preliminary estimate from 4 accounts, not a statistically valid sample

---

## 4. Derivation Chains

### Conclusion: The primary verified contributor to churn is the CSM coverage gap in the $18K–$25K tier

GT-2 (11 of 23 churned accounts cite "felt unsupported") + GT-3 (CSM-to-account ratio
1:67 vs. design threshold 1:40 in the uncovered tier)
→ The "felt unsupported" signal maps onto the structurally uncovered account segment — the
  specific tier where no dedicated CSM exists; the ratio drift quantifies the structural
  cause, explaining why the signal concentrates in this tier rather than spreading uniformly.
→ The CSM coverage gap is a verified contributor, supported by both qualitative exit data
  and quantitative capacity data.

**Confidence:** HIGH

---

### Conclusion: The structural root cause of the coverage gap is the absence of a recurring CS capacity-review process

GT-3 (ratio drifted to 1:67, 68% above the 1:40 threshold) + GT-4 (ratios reviewed only at
annual planning; no mid-year trigger exists)
→ The ratio drifted 68% beyond its design threshold without correction — the predicted
  outcome of a review cadence too infrequent for the company's growth rate.
→ Adding headcount alone without a recurring capacity review will reproduce the same gap at
  the next growth inflection; the structural fix is the review process, not a one-time hire.

**Confidence:** HIGH

---

### Conclusion: Additional causal contributors likely exist but remain unverified hypotheses

GT-1 (churn rose 124%) + GT-5? (productivity-outcome gap ~40% below demo benchmark,
preliminary estimate from 4 accounts)
→ The CSM coverage gap explains 11 of 23 churned accounts; 12 remain unaccounted for;
  the productivity-outcome gap is a plausible additional contributor — customers not
  achieving the promised outcome have a weaker economic case for renewal.
→ The full causal picture is not yet established; remaining churned accounts likely represent
  a second causal cluster requiring further evidence gathering.

**Confidence:** MEDIUM — GT-5? is unverified (4 accounts). Raising to HIGH requires a
statistically valid workflow-automation survey (minimum n=40 accounts).

---

## 5. Abandoned Reasoning

### Dead End: Treat the full 8P fishbone as a finding and fix all eight categories simultaneously

**What was tried:** After the fishbone brainstorm, the first instinct was to design
interventions for every populated branch — feature roadmap work, price-lock programmes,
onboarding redesign, email campaigns, CS hiring, health-scoring process, UI refresh, and an
ROI-tracking dashboard — approximately 14 engineering sprints and 6 months of CS-team effort.

**Why abandoned:** Every entry on the fishbone is an `untested belief` on entry to the
Assumptions Table. Of 8 rows, only one reaches Accept; the rest remain at Challenge.
Committing 14 sprints to all-category fixes when only two categories have verified Ground
Truths inverts minimum-viable-intervention reasoning. This is the failure mode the
ishikawa-diagram.md reference labels "Treating the diagram as a verified conclusion."

**What it ruled out:** Breadth of a cause map is not evidence of breadth of verified causes.
Any future all-category intervention plan must verify which branches are confirmed contributors
via the Assumptions Table before committing resources.

---

### Dead End: Attribute churn primarily to the product UI appearing dated

**What was tried:** Five of 23 exit interviews cited the UI as a churn factor: churned
accounts cite UI quality → competitors have more modern interfaces → a UI refresh is the
primary churn intervention.

**Why abandoned:** The UI assumption stayed at Verdict `Challenge` — the `untested belief`
classification could not be lifted to Accept because the evidence does not meet the
verification standard. The signal count (5 of 23 = 22%) is lower than the "felt unsupported"
signal (11 of 23 = 48%); all five accounts citing UI also cited at least one other factor;
none cited UI as the sole reason. GT-2 and GT-3 together explain the majority of the churn
signal at far lower intervention cost; investing ~8 sprints in a UI refresh before verifying
it is a standalone contributor inverts the cost-benefit ordering.

**What it ruled out:** UI-citation frequency is insufficient to anchor a high-confidence
causal claim. UI investment must be preceded by NPS and usability data confirming UI quality
is a standalone contributor, not a symptom of support absence that a service intervention
would address more cheaply.

---

## 6. Conclusion

**Recommended approach:** Execute in two ordered stages.

Stage 1 — fix the verified structural cause (4–8 weeks): establish a quarterly CS capacity
review with a ratio trigger (CSM-to-account ratio exceeds 1:45 → coverage model reviewed
before next quarter begins), addressing GT-4; reassign or add CSM coverage for the $18K–$25K
tier to bring the ratio below the 1:40 design threshold (GT-3), addressing the verified
cause of the "felt unsupported" signal (GT-2).

Stage 2 — verify remaining hypotheses (6–10 weeks) before any intervention commitment: run
a productivity-outcome survey (n=40 accounts) to test GT-5?; pull CRM data to test whether
decisions are made 90–120 days before expiry; segment adoption scores by churn outcome.

Do not commit to a product overhaul, UI refresh, or all-8P programme until Stage 2 is done.

**Key insight:** A fishbone brainstorm generates a well-organised list of hypotheses — it
does not generate verified causes. After Phase 2 classification, two of eight category
branches produced verified Ground Truths and the highest-confidence intervention set is
narrow, cheap, and fast relative to the 14-sprint programme the brainstorm appeared to
demand. The Phase 2 challenge step is the mechanism that separates the two outcomes.

**Trade-offs acknowledged:** Stage 1 addresses the verified cause of ~48% of the churn
signal; the remaining ~52% represent an unresolved causal cluster Stage 2 is designed to
illuminate. Adding CSM coverage has an immediate cost and may require trade-offs in
higher-value-tier coverage; the quarterly capacity review makes that trade-off governed.
Deferring the UI refresh accepts the risk that a second verified contributor emerges
requiring longer-lead-time product investment.

**Confidence:** MEDIUM — Stage 1 is HIGH confidence (GT-1 through GT-4, all verified).
Overall is MEDIUM because the full causal picture depends on GT-5? (unverified). Raising
to HIGH requires the Stage 2 productivity-outcome survey with a statistically valid sample.

---

## Validation Rubric Verdict

*Scored against `references/validation-rubric.md`. Six criteria evaluated in order.*

**Criterion 1: Identify Essence**
Quoted span: "Which causal factors are actually driving Northbrook Analytics' churn increase
from ~4% to ~9%, and which interventions will address those factors at the lowest cost and
highest reversibility — evaluated independently of any single proposed fix?"
Band: **Rigorous**
Justification: The Essence Statement names the core question, strips the proposed-solution
framing from the triggering instruction, is specific to this company and symptom profile, and
cannot be copied to a different churn scenario without modification; success criteria are
measurable and checkable against the conclusion without further clarification.

---

**Criterion 2: Challenge Assumptions**
Quoted span: "Every entry on the fishbone is an `untested belief` on entry to the Assumptions
Table. Of 8 rows, only one reaches Accept … the rest remain at Challenge."
Band: **Rigorous**
Justification: All 8 rows carry a Type value from the four-type scheme; Treatment cells apply
the prescribed vocabulary per type; every unverified row used in a derivation chain is marked
"unverified — flagged"; the one Accept row cites specific confirmatory evidence; the convention
row is challenged with specific counter-evidence rather than dismissed generically.

---

**Criterion 3: Establish Ground Truths**
Quoted span: "GT-5? The average workflow-automation rate achieved by active Northbrook accounts
is approximately 40% below the benchmark figure used in sales demos — source: unverified;
preliminary estimate from 4 accounts, not a statistically valid sample"
Band: **Rigorous**
Justification: All five GTs carry stable identifiers; every verified GT has a specific source
citation naming the data type and confirming party; the single unverified GT is marked with
the `?` suffix and explained with a specific reason; no discarded assumption appears in the
GT list.

---

**Criterion 4: Reason Upward**
Quoted span: "GT-2 (11 of 23 churned accounts cite 'felt unsupported') + GT-3 (CSM-to-account
ratio 1:67 vs. design threshold 1:40 in the uncovered tier) → The 'felt unsupported' signal
maps onto the structurally uncovered account segment"
Band: **Rigorous**
Justification: All three Section 6 conclusions have exactly one corresponding chain in Section
4; each chain names the GT-IDs consumed, contains at least one intermediate claim statable
from the combination but not from either GT alone; Abandoned Reasoning documents two dead ends
with GT-level or Phase-2-type abandonment reasons; no analogy is used as direct evidence.

---

**Criterion 5: Validate**
Quoted span: "Confidence: MEDIUM — GT-5? is unverified (4 accounts). Raising to HIGH requires
a statistically valid workflow-automation survey (minimum n=40 accounts)."
Band: **Rigorous**
Justification: Every derivation chain carries an explicit Confidence rating; the two HIGH
chains consume only verified GTs; the MEDIUM chain names the specific unverified input (GT-5?),
explains the downgrade, and states the exact verification that would raise confidence to HIGH;
the overall Conclusion's MEDIUM rating matches the weakest chain; no chain consuming GT-5? is
rated HIGH.

---

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "Do not commit to a product overhaul, UI refresh, or all-8P programme until
Stage 2 is done."
Band: **Rigorous**
Justification: Every Conclusion claim (Stage 1 actions, Stage 2 sequencing, deferral of
product overhaul) traces to a specific derivation chain or named GT; no new reasoning appears
in Section 6 that did not appear in Sections 3–4; the Key Insight names a non-obvious
finding — that Phase 2 collapsed the eight 8P cause-map branches and their sub-causes to a
narrow verified set — which conventional reasoning would have missed.

---

**Overall verdict: PASS**

All six criteria score Rigorous. No criterion is at Hand-wavy or Absent. Gate cleared (no
Absent); hand-wavy cap cleared (zero Hand-wavy criteria).
