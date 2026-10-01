## Answer

**Recommendation:** Do not name a root cause yet; none can be identified from the information supplied (chain C7). For four to six weeks, re-measure churn as the non-renewal rate among accounts due for renewal (chain C3) and cut the churned accounts against per-cause discriminators (chain C5). At the same time, flag at-risk renewals for outreach that does not depend on the cause. Then fund only the cause or causes the cuts implicate (chain C6).

**Band (from §6):** MEDIUM (chain C6)

**Would change it:** A pull from billing/CRM, ticketing and product analytics would verify GT-1? to GT-4? (chain C1, chain C3, chain C4).

## 1. Problem Essence

**Core problem:** Before funding any fix, Northbrook must establish whether the move in quarterly churn from 4.1% to 9.2% is a real fall in retention or an artefact of measurement, renewal timing or small numbers, and then which observations would tell the candidate causes apart, so that the money goes to the mechanism or mechanisms actually driving it and not to a correlate of it.

Leadership's instruction ("find the root cause of churn and fix it") is what set off this analysis. It is not the question the analysis has to answer. The instruction assumes three things: that one root cause exists, that the cause can be found from the signals already in hand, and that the rise itself is real. Each of those is tested below. None is taken as given.

**Success criteria:**

1. Every computed figure is shown with its arithmetic and recomputed independently.
2. The analysis states whether the rise from 4.1% to 9.2% can be told apart from (a) noise from a small customer base and (b) a change in how many contracts came up for renewal. Where it cannot be told apart yet, the analysis says what data would decide it.
3. Each candidate cause has a discriminating observation: something that is true if that cause is at work and false if a sibling cause is the real one. The candidates are offer gaps, pricing pressure, onboarding failure, service quality, competitive displacement, measurement artefact, and causes on the customer's own side.
4. The recommendation says what Northbrook does *before* the cause is known and what changes once it is known. It may combine actions. It is not required to name a single cause.
5. The premise that there is a single root cause is tested, not assumed.
## 2. Assumptions Table

**How the candidate causes were generated (fishbone, Phase 2).** The possible causes span many independent mechanisms, so they were brainstormed by category before any were judged. The effect being explained is: *quarterly churn rose from 4.1% (Q1) to 9.2% (Q3)*. This is software and knowledge work, so the default six-category set was used and fixed before brainstorming began:

- **People:** service quality fell (CS or support staffing, turnover, slower response); the customer's internal champion left.
- **Process:** onboarding failed to reach time-to-value before the first renewal; the renewal or price-change process went wrong.
- **Technology and Tools:** offer gaps (a missing connector, report or scale limit); reliability or regression problems after a release.
- **Environment:** a competitor displaced Northbrook; the customer's own budget was cut or the customer was acquired or went bankrupt.
- **Information:** an artefact in how churn is measured. This covers a different metric definition, a different denominator, timing that concentrates renewals in one quarter, and the noise of small numbers.
- **Resources:** pricing pressure (a list-price rise or discount expiry at renewal); a mismatch between price and the value received.

Each branch enters the table below as an `untested belief`. No branch has evidence for or against it in the problem statement. Every branch also predicts the two signals Customer Success has flagged, as chain C4 shows.

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| The quarterly churn figures 4.1% (Q1) and 9.2% (Q3) are accurate | untested belief | Verify, or flag | Challenge — supplied without a source; used as GT-1? and GT-2? | unverified — flagged (Phase 3 failure record on GT-1?) |
| "Churn rate" means the same metric (logo or revenue, same denominator) in both quarters | convention | Challenge before use | Challenge — the definition is not stated; logo churn and revenue churn can move differently when contracts range from $18k to $40k | unverified — flagged; GT-10 records that the definition is absent |
| A customer can leave only at its annual renewal date | current constraint | Record expiry | Accept — this holds only while contracts have no termination-for-convenience clause and non-payment terminations stay negligible; GT-8 keeps an early-termination term so that the identity does not depend on it | unverified — flagged; contract terms not supplied (GT-3?) |
| About 25% of the customer base comes up for renewal in each quarter | untested belief | Verify, or flag | Challenge — sales seasonality a year earlier could concentrate renewals in Q3; used only as a scenario in C3 | unverified — flagged |
| Churn has a single root cause | convention | Challenge before use | Discard — this is leadership's framing, and no ground truth supports it; kept as one hypothesis among several (C5) | GT-9, GT-10 |
| Rising support tickets and falling adoption scores *cause* churn | untested belief | Verify, or flag | Challenge — they move together with churn, and the direction of cause is not established (C4) | GT-9; unverified — flagged |
| The rise from 4.1% to 9.2% is larger than sampling noise | untested belief | Verify, or flag | Challenge — this depends on the customer count, which was not supplied (C2) | unverified — flagged |
| The rise is a renewal-mix effect, not a fall in retention | untested belief | Verify, or flag | Challenge — the renewal calendar is not supplied (C3) | unverified — flagged |
| Offer gaps drove the rise | untested belief | Verify, or flag | Challenge — no evidence either way; discriminator in C5 | unverified — flagged |
| Pricing pressure drove the rise | untested belief | Verify, or flag | Challenge — no evidence either way; discriminator in C5 | unverified — flagged |
| Onboarding failure drove the rise | untested belief | Verify, or flag | Challenge — no evidence either way; discriminator in C5 | unverified — flagged |
| A fall in service quality drove the rise | untested belief | Verify, or flag | Challenge — no evidence either way; discriminator in C5 | unverified — flagged |
| Competitive displacement drove the rise | untested belief | Verify, or flag | Challenge — no evidence either way; discriminator in C5 | unverified — flagged |
| Causes on the customer's side (budget cuts, acquisitions, champion turnover) drove the rise | untested belief | Verify, or flag | Challenge — the Customer Success signals do not cover this branch, and it is the one no product fix can reach | unverified — flagged |
| Reaching out to at-risk accounts with ticket and adoption flags ahead of renewal does no net harm, whatever the cause (surfaced by the Assumption Audit at C6) | untested belief | Verify, or flag | Challenge — save offers built on discounts could hide the pricing branch, and taking Customer Success capacity could worsen the service branch; the effect of failure is priced on C6 | unverified — flagged |
| The reasons churned customers give at exit are reliable enough to separate the causes (surfaced by the Assumption Audit at C5) | untested belief | Verify, or flag | Challenge — stated exit reasons lean toward "price"; C5 pairs each stated reason with a behavioural observation for that reason | unverified — flagged |
## 3. Ground Truths

Assumptions are referred to below as A-1 to A-16, numbered in the row order of the Section 2 table.

- **GT-1?** Northbrook's quarterly churn rate in Q1 was 4.1% (reported value; whether it is logo or revenue churn is not stated) — unverified: given in the problem statement without a source. **Phase 3 failure record:** the underlying source is Northbrook's billing/CRM churn records. No file, path or dataset was supplied, and the attempt to find one turned up no churn data (path not found).
- **GT-2?** Northbrook's quarterly churn rate at the end of Q3 was 9.2% (reported value; definition not stated) — unverified: same source and same failure record as GT-1?.
- **GT-3?** Contracts run $18,000–$40,000 a year and renew annually (reported range) — unverified: given in the problem statement without a source. No contract terms were supplied (path not found).
- **GT-4?** Customer Success reports rising support-ticket volume and falling feature-adoption scores (a qualitative report; no figures and no time alignment with churn) — unverified: a team observation passed on without data. No ticket or adoption data was supplied (path not found).
- **GT-5** The relative change from a value *a* to a value *b* is (b − a) / a. Over two periods with a constant per-period growth factor *g*, b / a = g² — source: definition (arithmetic); read-at-source: n/a, a mathematical definition, applied and recomputed in C1.
- **GT-6** If the per-quarter churn rate *p* stays constant and losses compound on the surviving base, retention over one year is (1 − p)⁴ and the annual-equivalent churn is 1 − (1 − p)⁴ — source: definition of compounding survival; read-at-source: n/a, a mathematical identity, recomputed in C1.
- **GT-7** For *N* accounts that each churn independently with probability *p*, the number lost has variance N·p·(1 − p). Two such proportions are compared with the pooled two-proportion z-statistic z = (p₂ − p₁) / √(p̄(1 − p̄)·(2/N)), where p̄ is the pooled rate — source: binomial distribution (a mathematical law); read-at-source: n/a, a standard statistical identity, recomputed in C2.
- **GT-8** For any quarter, churn = d × r + e. Here d is the share of the starting base whose contracts come up for renewal in that quarter, r is the non-renewal rate among those due, and e is the share lost to early termination or non-payment — source: an accounting identity (every lost account either reached its renewal date or left before it); read-at-source: n/a, true by construction.
- **GT-9** Two series moving together do not show which one drives the other, or whether a third factor drives both — source: formal logic (correlation does not identify causal direction); read-at-source: n/a, a principle of inference.
- **GT-10** The problem statement does not give the customer count, whether churn means logos or revenue, the renewal calendar, how churners split by segment, tenure or contract size, exit reasons, or magnitudes for tickets and adoption — source: the problem statement as delivered; read-at-source: the full problem-statement paragraph, read in its entirety (its only figures are 4.1%, 9.2%, 124% and $18,000–$40,000).

**Provenance summary.**

```text
?-marked: GT-1?, GT-2?, GT-3?, GT-4? (4 of 10)
Read-at-source: GT-10 — the problem statement, read in full
Definitional or mathematical (no external source; each recomputed where used): GT-5, GT-6, GT-7, GT-8, GT-9
```

The four `?`-marked ground truths feed every chain. They cannot be checked from here: the only source is Northbrook's own data, and none was supplied. The verification that would remove each `?` is a pull from billing/CRM (GT-1?, GT-2?), the contract template (GT-3?) and the ticketing and product-analytics data (GT-4?).
## 4. Derivation Chains

**Run mode.** The problem statement asks to "find the root cause", which selects the focused **five-whys (causal mode)** technique for Phase 4. The fishbone above supplied the breadth in Phase 2. The second-order pass runs as Phase 4 requires.

**Five-whys causal drill.** Symptom: quarterly churn was 9.2% in Q3 against 4.1% in Q1.

*Level 1: why was more of the base lost in Q3?* By GT-8, every lost account sits in exactly one of these terms, so the lateral scan below is complete:

| Level-1 cause | Counterfactual test (without it, would the symptom remain?) | Verdict |
|---|---|---|
| (a) A larger share of the base, *d*, came up for renewal in Q3 | Cannot tell: the renewal calendar is not supplied (GT-10) | `Unresolved ? — share of the starting base with a Q1 renewal date vs. a Q3 renewal date` |
| (b) A larger share of the accounts due, *r*, declined to renew | Cannot tell: *r* cannot be computed without *d* | `Unresolved ? — non-renewal rate among accounts due, per quarter` |
| (c) Early terminations or non-payment, *e*, rose | Cannot tell | `Unresolved ? — count of losses dated before the contract's renewal date` |
| (d) The metric changed (definition, denominator, or a one-off bulk loss) | Cannot tell | `Unresolved ? — the churn query or definition used in Q1 vs. Q3` |
| (e) Noise from a small number of accounts | Cannot tell: the customer count is not supplied (C2) | `Unresolved ? — customer count N at the start of each quarter` |

*Level 2, drilled only under branch (b):* why did more of the due accounts decline? The candidates are the six Phase 2 branches: offer gaps, pricing, onboarding, service quality, competitive displacement, and causes on the customer's side. The one signal on hand (GT-4?) does not tell them apart (C4), so each is `Unresolved ?` with the discriminating observation listed under C5.

*Depth guard.* The drill stops at level 2 because no level-1 cause has passed a counterfactual test. Going deeper now would only produce a story, not a cause. On present evidence the honest verdict for every branch is `Unresolved ?`. That is the finding: the "root cause" cannot yet be identified from what is known.

### Conclusion C1: The rise is +5.1 percentage points (+124.4%), equal to about 49.8% growth per quarter; annualised, churn went from about 15.4% to about 32.0%

GT-1? (Q1 4.1%) + GT-2? (Q3 9.2%) + GT-5 (relative change) + GT-6 (compounding survival)
→ the absolute rise is 9.2 − 4.1 = 5.1 percentage points
→ the relative rise is 5.1 / 4.1 = 1.2439, i.e. +124.4%, which confirms the stated "124%"
→ the ratio 9.2 / 4.1 = 2.2439 over two quarter-steps implies a growth factor of √2.2439 = 1.4980, i.e. about +49.8% per quarter
→ at Q1's rate, one-year retention is 0.959⁴ = 0.919681² = 0.845813, so annual-equivalent churn is 1 − 0.845813 = 15.4%
→ at Q3's rate, one-year retention is 0.908⁴ = 0.824464² = 0.679741, so annual-equivalent churn is 1 − 0.679741 = 32.0%
→ if the Q3 rate held, Northbrook would lose about one customer in three per year, against about one in six and a half at the Q1 rate (1 / 0.154 = 6.5)

**Pre-check:** head GT-1?, GT-2?, GT-5, GT-6 · ?-marked: GT-1?, GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: GT-1? and GT-2? are reported figures without a source. Pulling the Q1 and Q3 churn counts and their denominators from billing/CRM would remove both as causes of the downgrade. The Inference axis is clean: every hop was recomputed independently, and the results matched to four decimal places. The Rivals axis does not apply, because arithmetic on stated inputs has no competing reading. The annualised figures assume each rate stays constant for four quarters, so they are run-rates, not forecasts.

### Conclusion C2: Whether the rise is real or noise cannot be decided without the customer count; below about 184 accounts per quarter it does not clear a 5% significance threshold

GT-1? (Q1 4.1%) + GT-2? (Q3 9.2%) + GT-7 (two-proportion z) + GT-10 (no customer count supplied)
→ the pooled rate is p̄ = (0.041 + 0.092) / 2 = 0.0665
→ the pooled variance term is p̄(1 − p̄) = 0.0665 × 0.9335 = 0.062078
→ the standard error is √(0.062078 × 2/N), so z = 0.051 / √(0.124156/N)
→ for N = 100 the standard error is √0.00124156 = 0.035236 and z = 0.051 / 0.035236 = 1.45, below the 1.96 threshold
→ for N = 200 the standard error is √0.00062078 = 0.024915 and z = 0.051 / 0.024915 = 2.05, just above the threshold
→ z = 1.96 is reached at N = 0.124156 × (1.96 / 0.051)² = 0.124156 × 1476.97 = 183.4, i.e. about 184 accounts
→ at N = 100 the rise means 4.1 against 9.2 accounts lost, a difference of about five customers *[Assumes: A-7]*
→ the size of the relative change ("124%") says nothing about whether the rise is real until N is known

**Pre-check:** head GT-1?, GT-2?, GT-7, GT-10 · ?-marked: GT-1?, GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: GT-1? and GT-2? are unverified, and the customer count from billing/CRM would close it. The [Assumes: A-7] hop only illustrates the counts. The endpoint is conditional on N whether or not A-7 holds, so the assumption's failure is priced and does not change the endpoint. The test treats the two quarters as independent samples and ignores the Q2 figure, which was not supplied; a run of quarterly figures would be stronger evidence than two points.

### Conclusion C3: The quarterly rate mixes renewal timing with retention, so the first measurement must be the non-renewal rate among accounts due for renewal

GT-8 (churn = d·r + e) + GT-3? (annual renewal) + GT-1? (Q1 4.1%) + GT-2? (Q3 9.2%)
→ if renewals are spread evenly (d = 0.25 every quarter) and e = 0, the non-renewal rate among accounts due is 0.041 / 0.25 = 16.4% in Q1 *[Assumes: A-4]*
→ on the same basis, the Q3 non-renewal rate among accounts due is 0.092 / 0.25 = 36.8%, so more than one in three of the accounts that came up for renewal left
→ if *r* had instead stayed at 16.4%, Q3 would need d = 0.092 / 0.164 = 56.1% of the base due, so a Q3 renewal pile-up could produce the whole rise with no change in retention
→ the same 9.2% can therefore mean "retention collapsed" or "more contracts came due", and those call for opposite responses
→ the measurement that separates them is *r* per quarter, the non-renewal rate among accounts actually due, with *e* counted separately

**Pre-check:** head GT-8, GT-3?, GT-1?, GT-2? · ?-marked: GT-3?, GT-1?, GT-2? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: GT-1?, GT-2? and GT-3? are unverified. The renewal calendar and contract terms from billing/CRM would close it. The [Assumes: A-4] hop sets d = 0.25 only as a scenario. If renewals are not even, the 16.4% and 36.8% figures change, but the endpoint does not, because that endpoint is the claim that *d* must be measured. The failure is priced. The rival reading, that the quarterly rate is an adequate metric, is ruled out in §5 by GT-8.

### Conclusion C4: Rising tickets and falling adoption fit every candidate cause, so they are account-level warning signals, not evidence of which cause is at work

GT-4? (tickets up, adoption down) + GT-9 (correlation does not give direction)
→ onboarding failure, offer gaps, falling service quality and an active competitor evaluation each predict more tickets and less adoption
→ an account that has already decided to leave also uses the product less, so the direction can run from intent-to-churn to the signals
→ the two signals therefore do not tell any candidate branch apart from its siblings
→ they remain usable as per-account risk flags ahead of renewal, which needs no knowledge of the cause

**Pre-check:** head GT-4?, GT-9 · ?-marked: GT-4? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the Inputs axis is short: GT-4? is a qualitative report. Ticket and adoption data per account, lined up with renewal outcomes, would close it, and would also show whether the flags actually predict churn before renewal. The rival reading, that the signals point to onboarding or product as the cause, is ruled out in §5 by GT-9.

### Conclusion C5: No root cause can be named yet; each candidate branch has a discriminating observation, and the observations are cheap because they are cuts of data Northbrook already holds

C3 (measure r, not the quarterly rate) + C4 (signals do not discriminate) + GT-10 (no segmentation or exit data supplied)
→ every level-1 and level-2 branch of the drill is `Unresolved ?`, so naming one root cause now would mean picking the branch that sounds most plausible
→ a branch is told apart only by an observation that comes out differently depending on which branch is true *[Assumes: A-16]*
→ the discriminators are listed in the table below this chain, one per branch, each drawn from records of the churned accounts
→ the cause question becomes a 4–6 week cut of the Q1–Q3 churned and renewed accounts, run before any structural fix is funded

| Branch | Discriminating observation (true if this branch, false for its siblings) |
|---|---|
| Renewal mix / measurement | *r* (the non-renewal rate among accounts due) is flat from Q1 to Q3 while *d* rose; or the churn query or definition changed |
| Onboarding failure | Q3 churn is concentrated in **first-renewal** accounts (tenure ≤ 12 months), and those accounts had a long time-to-first-live-integration; longer-tenure accounts renew at the Q1 rate |
| Pricing pressure | Churn is concentrated in renewals that carried a price increase or discount expiry; churned accounts asked to downgrade before leaving; accounts renewing at an unchanged price kept their rate |
| Service quality | Churned accounts show worse first-response and resolution times *on the same ticket types* than renewed accounts; the decline starts after a support staffing change |
| Offer gaps | Churned accounts' tickets and feature requests cluster on the same few missing capabilities (connectors, report types, scale limits); the churn is concentrated in the segment or use case that needs them |
| Competitive displacement | Churned accounts requested data exports or API bulk pulls ahead of renewal; a named competitor appears in loss reasons from the account's own users, not only from the CSM's notes; win/loss records show the same competitor |
| Customer side (budget, M&A, champion) | The churned account went out of business, was acquired, or lost its champion (a change in admin or login), and none of the product signals above apply |

**Pre-check:** head C3 (MEDIUM), C4 (MEDIUM), GT-10 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C3 and C4, each rated MEDIUM, whose own confidence lines carry their verification paths. The [Assumes: A-16] hop matters because stated exit reasons lean toward "price". Each branch therefore pairs any stated reason with behavioural data (tenure, price-change flag, export events, ticket timings). If A-16 fails, the behavioural columns still separate the branches, so the endpoint stands. The rival reading, that a single root cause can be named now, is ruled out in §5 by C4 and GT-10.

### Conclusion C6: Run diagnosis and a cause-neutral rescue effort together; commit structural fixes only to the branch or branches the C5 cuts implicate

C1 (about 32% annualised at the Q3 rate) + C3 (measure r) + C4 (signals are risk flags) + C5 (discriminator table)
→ at the Q3 run-rate, losses compound at about one customer in three per year, so waiting a whole quarter for a diagnosis has a cost
→ flagging renewals due in the next 120 days by low adoption and high ticket volume for CS outreach is the one action whose value does not depend on which branch is true *[Assumes: A-15]*
→ the C5 cuts identify which branch or branches carry the rise, and possibly more than one
→ structural spend (onboarding redesign, pricing change, support staffing, roadmap, competitive response) goes only to the branches the cuts implicate
→[2nd] actor lens (CS team): outreach at fixed capacity takes time away from healthy accounts, which could create the service-quality branch it is meant to fix
→[2nd] actor lens (sales and finance): saves won with discounts teach customers that threatening to churn earns a discount
→[3rd] time lens (a few renewal cycles): discount-led saves wear down price realisation and hide the pricing-branch signal, which defeats success criterion 3
→[2nd] actor lens (leadership): a diagnosis that ends in "several branches" or "renewal mix" may read as failing the instruction to "find the root cause"
→[2nd] time lens (once established): the non-renewal rate among accounts due becomes the standing retention metric, so the next rise is diagnosed in weeks rather than quarters

**Pre-check:** head C1 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C1, C3, C4 and C5, each rated MEDIUM, whose own confidence lines carry their verification paths. The [Assumes: A-15] hop is priced as follows. If outreach does harm (it drains CS capacity, or its discounts hide the pricing signal), the rescue half shrinks to flagging only, with every concession logged. The diagnose-then-commit half, which is the core of the endpoint, still stands. No second-order effect contradicts a ground truth. The discount effect does work against success criterion 3, and is handled in the Phase 5 disposition, which requires every concession to be logged and permits no discount without approval. A Phase 5 weak link is also named here: if N is small enough that branch cells hold fewer than about 10 churners, the C5 cut cannot discriminate on historical data alone. The diagnosis horizon then extends past 4–6 weeks while prospective exit data builds up. The verification is the week-1 report of N per branch.
### Conclusion C7: No cause can be identified from the information supplied, whatever the true figures turn out to be

GT-8 (churn = d·r + e) + GT-7 (significance depends on N) + GT-9 (correlation does not give direction) + GT-10 (no N, calendar, definition or segmentation supplied)
→ a change in quarterly churn can come from d, r, e, a changed metric or noise, and separating these needs the renewal calendar, the metric definition and N
→ the problem statement supplies none of the renewal calendar, the metric definition or N
→ the only causal-looking evidence it supplies is a pair of signals that move with churn, and such signals cannot show direction
→ no level-1 or level-2 branch of the drill can be identified as the cause from the information supplied

**Pre-check:** head GT-8, GT-7, GT-9, GT-10 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — Inputs: every head identifier is unsuffixed. GT-7, GT-8 and GT-9 are mathematical or logical identities. GT-10 was read in the problem statement. Inference: each hop is a deduction, and the endpoint does not depend on whether GT-1? to GT-4? are accurate, which is why none of them is on the head. Rivals: "a root cause can be named now" is ruled out in §5 by this chain together with GT-9 and GT-10, all unsuffixed.

## 5. Abandoned Reasoning

### Dead End: Rising tickets and falling adoption show the root cause is onboarding or the product

**What was tried:** Reading the two Customer Success signals as evidence that the cause is onboarding failure or a product gap, because those are the branches the signals most obviously suggest.

**Why abandoned:** GT-9: co-movement does not give causal direction. C4 shows that every candidate branch predicts the same two signals, and so does an account that has already decided to leave.

**What it ruled out:** Funding an onboarding or product fix on the strength of the Customer Success flags alone. Rival to C4.

### Dead End: Pick the cause by industry pattern ("mid-market SaaS churn is usually onboarding")

**What was tried:** Filling the missing evidence with what is typical at comparable companies.

**Why abandoned:** This is reasoning by analogy. No ground truth here describes Northbrook's churners, and GT-10 records that the segmentation needed to check the analogy was not supplied.

**What it ruled out:** Any cause assignment not drawn from Northbrook's own churned-account records.

### Dead End: A 124% increase is too large to be noise

**What was tried:** Treating the size of the relative change as proof that retention has really worsened.

**Why abandoned:** GT-7 and C2: whether the rise is significant depends on N. At N = 100 the rise is about five customers (4.1 against 9.2), and z = 1.45 does not clear 1.96.

**What it ruled out:** Treating the rise as established before the customer count is known. Rival to C2.

### Dead End: The quarterly churn rate is an adequate measure of retention

**What was tried:** Comparing 4.1% with 9.2% directly as a change in how well Northbrook keeps customers.

**Why abandoned:** GT-8 and C3: in an annual-renewal business the quarterly rate is d × r + e. A change in *d* alone (56.1% of the base due in Q3 against 25%) reproduces 9.2% with no change in retention.

**What it ruled out:** Any diagnosis that starts from the quarterly rate instead of from the non-renewal rate among accounts due. Rival to C3.

### Dead End: Name a single root cause now, as instructed

**What was tried:** Choosing the most plausible of the six branches and declaring it the root cause, as leadership's instruction asks.

**Why abandoned:** C7, which rests on GT-8, GT-9 and GT-10 (all unsuffixed): nothing on hand separates the branches. In the five-whys drill every level-1 cause is `Unresolved ?`, so any branch named now would be picked for plausibility, not on evidence.

**What it ruled out:** A single-cause verdict before the C5 cuts are run. Rival to C5 and C7.

### Dead End: Wait for the diagnosis and do nothing in the meantime

**What was tried:** Holding all action until the cause is known, so that no money goes to the wrong branch.

**Why abandoned:** C1: at the Q3 run-rate, annualised churn is about 32.0%, so each quarter of waiting has a cost. C4: per-account risk flags support outreach that does not depend on the cause.

**What it ruled out:** A diagnosis-only plan. Rival to C6.

### Dead End: Launch a broad fix now (a price cut, an onboarding overhaul, more support staff) to cover all bases

**What was tried:** Treating several branches at once in place of diagnosis.

**Why abandoned:** C5: the branches can be told apart cheaply from data Northbrook already holds. C6 second-order: a broad discount would hide the pricing signal, and the measures would muddy each other's results, so afterwards nobody could tell which one worked.

**What it ruled out:** Fixing everything before diagnosing anything. Rival to C6.
## 6. Conclusion

**Recommended approach:** Do not name a root cause yet, because none can be identified from the information supplied (chain C7). Run two tracks at the same time for four to six weeks. First, re-measure churn as the non-renewal rate among accounts actually due for renewal, with early terminations counted separately (chain C3), and cut the Q1–Q3 churned and renewed accounts against the discriminator table in C5 (chain C5). Second, flag renewals due in the next 120 days by low adoption and high ticket volume for Customer Success outreach. Concessions need approval and are logged (chain C6). In week 1, confirm that renewal dates and the churn definition can be rebuilt and report N; if branch cells would hold fewer than about 10 churners, add structured exit interviews for Q4 churners (chain C5). Commit structural spend only to the branch or branches the cuts implicate (chain C6).

**Key insight:** The rise from 4.1% to 9.2% (+5.1 points, +124.4%; about 15.4% → 32.0% annualised, chain C1) may not be a fall in retention at all. In an annual-renewal business, a Q3 renewal pile-up of 56.1% of the base would produce it with retention unchanged (chain C3). Below about 184 accounts it cannot be told apart from noise (chain C2). And the two signals Customer Success flagged fit every candidate cause equally well (chain C4).

**Trade-offs acknowledged:** The plan gives leadership a diagnosis in place of an immediate single-cause answer. It also accepts four to six weeks before structural spend, a cost bounded by the Q3 run-rate (chain C6). The outreach track competes with healthy accounts for CS capacity, and any save won with a discount could hide the pricing signal (chain C6).

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (HIGH) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the recommendation rests on C1, C2, C3, C4, C5 and C6, each rated MEDIUM, whose confidence lines carry the verification paths. The "no cause can be named yet" part rests on C7 and holds at HIGH. All of them trace back to the unverified inputs GT-1?, GT-2?, GT-3? and GT-4?, and a single billing/CRM, ticketing and product-analytics pull would remove all four. That pull would also not move the recommendation itself, only which branch it funds (chain C6).
## Appendix — process output

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | 9.2 − 4.1 = 5.1 points | no | n/a |
| C1 | 2 | 5.1 / 4.1 = +124.4% | no | n/a |
| C1 | 3 | √2.2439 = 1.498 per quarter | no (constant growth is a stated identity, GT-5) | n/a |
| C1 | 4 | Q1 annualised 15.4% | no (constant rate, stated in the confidence line as a run-rate) | n/a |
| C1 | 5 | Q3 annualised 32.0% | no | n/a |
| C1 | 6 | one in three vs one in 6.5 | no | n/a |
| C2 | 1 | pooled p̄ = 0.0665 | no | n/a |
| C2 | 2 | p̄(1 − p̄) = 0.062078 | no | n/a |
| C2 | 3 | SE formula | no | n/a |
| C2 | 4 | N = 100, z = 1.45 | no | n/a |
| C2 | 5 | N = 200, z = 2.05 | no | n/a |
| C2 | 6 | threshold N ≈ 184 | no | n/a |
| C2 | 7 | at N = 100, about 5 customers | yes — A-7 (the rise exceeds noise) is what is in question here | already in table (A-7); marked `[Assumes: A-7]` |
| C2 | 8 | 124% uninformative without N | no | n/a |
| C3 | 1 | d = 0.25 → r = 16.4% | yes — A-4 (renewals spread evenly) | already in table (A-4); marked `[Assumes: A-4]` |
| C3 | 2 | Q3 r = 36.8% | no (same A-4, mark on step 1) | n/a |
| C3 | 3 | d needed = 56.1% | no | n/a |
| C3 | 4 | same 9.2% has two readings | no | n/a |
| C3 | 5 | measure r per quarter | no | n/a |
| C4 | 1 | all branches predict the signals | no | n/a |
| C4 | 2 | reverse causation possible | no | n/a |
| C4 | 3 | signals do not discriminate | no | n/a |
| C4 | 4 | usable as risk flags | no (whether the flags predict churn is named in the confidence line as a verification) | n/a |
| C5 | 1 | all branches Unresolved | no | n/a |
| C5 | 2 | discrimination needs differing observations | yes — A-16 (exit reasons are reliable enough) | yes — added as A-16; marked `[Assumes: A-16]` |
| C5 | 3 | discriminator table | no | n/a |
| C5 | 4 | 4–6 week cut before spend | no | n/a |
| C6 | 1 | waiting has a cost | no | n/a |
| C6 | 2 | cause-neutral outreach | yes — A-15 (outreach does no net harm) | yes — added as A-15; marked `[Assumes: A-15]` |
| C6 | 3 | cuts identify branch(es) | no | n/a |
| C6 | 4 | spend only on implicated branches | no | n/a |
| C6 | 5 | [2nd] CS capacity diverted | no | n/a |
| C6 | 6 | [2nd] discount conditioning | no | n/a |
| C6 | 7 | [3rd] price realisation and pricing signal | no | n/a |
| C6 | 8 | [2nd] leadership reception | no | n/a |
| C6 | 9 | [2nd] r becomes the standing metric | no | n/a |
| C7 | 1 | five separable sources need calendar, definition, N | no | n/a |
| C7 | 2 | none of those supplied | no | n/a |
| C7 | 3 | signals cannot give direction | no | n/a |
| C7 | 4 | no branch identifiable | no | n/a |
## Adversarial pass (process output)

**Recompute:** Every figure was redone independently in Python, separately from the chain text:

| Figure | Chain | Recomputed value | Matches? |
|---|---|---|---|
| 9.2 − 4.1 | C1 | 0.051 → 5.1 points | yes |
| 5.1 / 4.1 | C1 | 1.243902 → +124.4% | yes |
| 9.2 / 4.1 | C1 | 2.243902 | yes |
| √2.243902 − 1 | C1 | 0.497966 → +49.8%/quarter | yes |
| 0.959² ; ² | C1 | 0.919681 ; 0.845813 → annual 15.42% | yes |
| 0.908² ; ² | C1 | 0.824464 ; 0.679741 → annual 32.03% | yes |
| 1 / 0.154 | C1 | 6.49 | yes |
| p̄ ; p̄(1 − p̄) | C2 | 0.0665 ; 0.06207775 | yes (0.062078 rounded) |
| SE, z at N = 100 | C2 | 0.035236 ; 1.4474 | yes |
| SE, z at N = 200 | C2 | 0.024915 ; 2.0469 | yes |
| z at N = 400 (check) | C2 | 2.8948 | n/a (not in chain) |
| N at z = 1.96 | C2 | 0.124156 × 1476.97 = 183.37 → 184 | yes |
| 0.041 × 100 ; 0.092 × 100 | C2 | 4.1 ; 9.2 | yes |
| 0.041 / 0.25 ; 0.092 / 0.25 | C3 | 0.164 ; 0.368 | yes |
| 0.092 / 0.164 | C3 | 0.560976 → 56.1% | yes |

Direction checks: 15.4% annual is greater than 4.1% quarterly, and 32.0% is greater than 9.2%. A per-quarter growth factor of 1.498, squared, gives 2.244. Each r is greater than its quarterly rate, because d < 1. Every combined figure lands on the side its operation puts it. One defect was found and corrected while writing: the C2 heading first said "roughly 190", which was rounding drift from 184, and it was corrected to "about 184".

**Sensitivity:** The ground truth whose falsity flips the conclusion is **GT-10** (the segmentation and renewal-calendar data were not supplied). It is not `?`-marked: it was read in the problem statement. If Northbrook in fact already holds a churned-account cut, the "do not name a cause yet" half of the recommendation flips to naming the cause from that cut. The plan absorbs this, because the first track *is* running that cut. Weakest link in each chain: C1, inputs GT-1? and GT-2?. C2, the two-point independent-sample test, with Q2 unknown. C3, A-4 (d = 0.25, scenario only). C4, GT-4? has no magnitudes. C5, A-16 (exit reasons reliable), together with possibly small cell sizes. C6, A-15 (outreach does no net harm).

**Rival:** C1: rival not applicable — arithmetic on stated inputs has no competing reading. C2: "124% is too large to be noise", ruled out by GT-7 (§5, "A 124% increase is too large to be noise"). C3: "the quarterly rate is an adequate retention measure", ruled out by GT-8 (§5, same-named entry). C4: "the signals show onboarding or the product is the cause", ruled out by GT-9 (§5). C5 and C7: "name a single root cause now", ruled out by C7, GT-9 and GT-10 (§5). C6 (headline): "wait for the diagnosis" and "broad fix now", ruled out by C1, C4 and C5 (two §5 entries). No rival is left live.

**Premise:** It is March 2027. The diagnose-and-rescue plan has failed. Quarterly churn is still above 9%, and Northbrook still does not know why.

**Causes:** (written before grouping, from four viewpoints)
- *RevOps / analytics (implementer):* renewal dates in the CRM were missing or overwritten at renewal, so d and r could not be rebuilt for Q1.
- *RevOps:* the Q1 churn query was never saved, so nobody could tell whether the definition had changed.
- *RevOps:* the base was about 120 accounts, so each branch's cell held 2–4 churners and no discriminator separated anything.
- *RevOps:* the cut took 14 weeks, not 4–6, because ticket, product-analytics and billing IDs did not join.
- *Customer Success (implementer of the rescue):* outreach to flagged accounts swamped the team, and response times for healthy accounts slipped.
- *Customer Success:* most flagged accounts had already decided, since procurement had started 90 days before renewal, so outreach in the renewal quarter came too late.
- *Customer Success:* CSMs gave out discounts to hit save targets, and the pricing signal disappeared.
- *Customers (living with the result):* outreach read as a sales push; churned customers refused exit calls, so stated reasons were missing.
- *Leadership / finance (paying):* at week 3, impatience led to an approved across-the-board price cut, which confounded every cut.
- *Leadership:* a readout of "two branches plus renewal mix" was rejected as "not a root cause", and the work was shelved.
- *Competitor (benefiting):* it timed migration offers to Northbrook's renewal window and offered free data migration, beating outreach that started late.

Adversarial interrogation: two causes embarrass the conclusion itself. The first is the 2–4-churner cells, which contradict C5's claim that the cuts are cheap *and discriminating*. The second is the decision being made 90 days early, which contradicts C6's claim that renewal-quarter outreach is the cause-neutral action. Both are treated as fatal or costly below, not softened.

**Clusters:**
- **K1 Data cannot support the diagnosis.** Absorbs the missing renewal dates, the unsaved query, the 2–4-churner cells and the unjoinable IDs. Bears on C2, C3, C5 and GT-10. Triage: **fatal**, because the diagnosis is the plan.
- **K2 The rescue arrives after the decision.** Absorbs the 90-day procurement lead and the competitor's timed offers. Bears on C4 and C6. Triage: **costly but survivable**.
- **K3 The rescue distorts the evidence and the capacity.** Absorbs the CS swamping, the save discounts and the refused exit calls. Bears on C6, C5 and A-15. Triage: **costly but survivable**.
- **K4 Leadership commits before the readout, or rejects a multi-branch answer.** Absorbs the week-3 price cut and the rejected readout. Bears on C5, C6 and the A-5 discard. Triage: **costly but survivable**.

**Disposition:**
- **K1, plan change.** Add a week-1 feasibility gate. RevOps confirms that renewal date and churn reason can be reconstructed for at least 90% of Q1–Q3 accounts, and reports N. If any branch cell would hold fewer than about 10 churners, the plan adds structured, behaviour-anchored exit interviews for every Q4 churner as prospective data, and extends the readout. Tripwire: no r-per-quarter table by the end of week 1. Owner: RevOps lead.
- **K2, plan change.** Raise risk flags on renewals due in the next 120 days, not just this quarter. Tripwire: more than 30% of flagged accounts have already given notice or requested a data export at first contact. Owner: CS lead, weekly.
- **K3, plan change plus accepted risk with mitigation.** Every concession needs approval and is logged with its reason. Outreach is capped at about 20% of CS hours. Tripwire: first-response time on accounts that are not flagged worsens against the Q3 baseline, or more than a quarter of saves include a discount. Owner: VP Customer Success.
- **K4, plan change.** Set a fixed readout date (week 6) with weekly interim readings of r. Agree in advance that "implicated" means the branch's discriminator separates churned from renewed accounts. Approve no structural spend before the readout. Tripwire: any structural fix is approved before week 6. Owner: executive sponsor.

The dispositions have been folded into the analysis. K2's 120-day window is now in C6's second hop and in §6. K1 is now a named weak link on C6's confidence line, and its week-1 gate is in §6, cited to C5. K3 is C6's priced A-15 hop together with the concession-approval rule in §6.

**Falsification:** The conclusion is false if the C5 cuts on Northbrook's existing data cannot separate any branch from its siblings, even after prospective exit data is added. The cuts would then not be the cheap discriminators C5 claims, and the diagnosis track would need a different instrument, such as a controlled intervention on one branch. It is also false if a cut Northbrook already holds shows one branch carrying the whole rise. In that case naming the cause now was possible.
## §6→§4 closure ledger (process output)

```text
- "Recommended approach: Do not name a root cause yet — none identifiable from supplied information; re-measure as non-renewal rate among accounts due … cut against C5 discriminators … flag 120-day renewals … week-1 feasibility … commit spend only to implicated branches" → chain C7, C3, C5, C6 ✓
- "Key insight: the rise may not be a retention collapse at all — renewal pile-up (C3), noise below ~184 accounts (C2), non-discriminating signals (C4); figures from C1" → chain C1, C2, C3, C4 ✓
- "Trade-offs acknowledged: diagnosis instead of single-cause answer; 4–6 weeks before structural spend; CS capacity and discount masking" → chain C6 ✓
- "Pre-check: head C1–C6 (MEDIUM), C7 (HIGH) · Inputs ceiling MEDIUM" → chain C1, C2, C3, C4, C5, C6, C7 ✓
- "Confidence: MEDIUM — C1–C6 each MEDIUM; one data pull removes GT-1?–GT-4?; pull changes which branch is funded, not the recommendation; the "no cause yet" part HIGH via C7" → chain C1, C2, C3, C4, C5, C6, C7 ✓
```

Ledger clean: 5 claims, 5 traced, 0 cut.
## Self-audit scan (process output)

Table 1: chain form (Section 4)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1? + GT-2? + GT-5 + GT-6 | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-1? + GT-2? + GT-7 + GT-10 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-8 + GT-3? + GT-1? + GT-2? | yes | n/a | yes | MEDIUM | yes | none |
| C4 | GT-4? + GT-9 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | C3 + C4 + GT-10 | yes | n/a | yes | MEDIUM | yes | none |
| C6 | C1 + C3 + C4 + C5 | yes | n/a | yes | MEDIUM | yes | none |
| C7 | GT-8 + GT-7 + GT-9 + GT-10 | yes | n/a | yes | HIGH | yes | none |

The `yes` cells cover every hop position, including those the mechanical check does not reach, for this reason: every arrow-led line in Section 4 was checked by pattern for a leading `GT-` identifier and for a terminal period, and none matched. The one compound hop found (C2, "pooled rate … and p̄(1 − p̄) …") was split before this scan was run. The dependencies form an acyclic graph: C5 uses C3 and C4; C6 uses C1, C3, C4 and C5. Every GT on a chain's head line resolves to Section 3.

Table 2: claim inventory (Section 6)

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: do not name a root cause yet; two tracks … | bold lead-in | yes | a bold lead-in whose colon closes the bold span (a prescribed lead-in) | C7, C3, C5, C6 |
| Key insight: the rise may not be a retention collapse … | bold lead-in | yes | a bold lead-in whose colon closes the bold span (a prescribed lead-in) | C1, C2, C3, C4 |
| Trade-offs acknowledged: diagnosis instead of a single cause … | bold lead-in | yes | a bold lead-in whose colon closes the bold span (a prescribed lead-in) | C6 |
| Pre-check: head C1–C6 (MEDIUM), C7 (HIGH) … | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C5, C6, C7 |
| Confidence: MEDIUM — C1 to C6 each MEDIUM; the "no cause yet" part rests on C7 at HIGH … | bold lead-in | yes | a bold lead-in whose colon closes the bold span (a prescribed lead-in) | C1, C2, C3, C4, C5, C6, C7 |

```text
Scan complete: 7 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```
## Self-Audit Gate (process output)

Assumption Audit check: the scan has one row for every arrow-led step of C1–C7, in order (C1 6, C2 8, C3 5, C4 4, C5 4, C6 9, C7 4 = 40 rows). Self-audit scan check: 7 chain rows match the 7 chain blocks in section 4; 5 claim rows match the 5 constructs in section 6; the reconciliation line recounts.

**Criterion 1: Identify Essence**
Quoted span: "Before funding any fix, Northbrook must establish whether the move in quarterly churn from 4.1% to 9.2% is a real fall in retention or an artefact of measurement, renewal timing or small numbers, and then which observations would tell the candidate causes apart … Every computed figure is shown with its arithmetic and recomputed independently."
Band: **Sound**
Justification: The essence is a single sentence specific to this problem, and it names the underlying question rather than leadership's instruction. But success criterion 1 cannot be checked by scanning the Conclusion section alone: it is checked against §4 and the Recompute record. So one criterion departs from the requirement that every outcome be a property of the Conclusion.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C5 | 2 | discrimination needs differing observations | yes — A-16 (exit reasons are reliable enough) | yes — added as A-16; marked `[Assumes: A-16]` |"
Band: **Rigorous**
Justification: All 16 rows use the four-type scheme, with the treatment for their type and token-first em-dash verdicts. Every unverified assumption used in a chain reads "unverified — flagged". A-5 is challenged and discarded. The audit covers all 40 chain steps and added A-15 and A-16 back into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: comparison, not a quote of the summary: the enumeration lists "GT-1?, GT-2?, GT-3?, GT-4? (4 of 10)", and the list carries `?` on exactly those four. The unsuffixed GT-7, GT-8, GT-9 and GT-10 each feed C7 (HIGH). The unsuffixed GT-5 and GT-6 feed only C1 (MEDIUM).
Band: **Hand-wavy**
Justification: The enumeration matches the list, the IDs are stable, and GT-10's read-at-source location is named. But two unsuffixed ground truths whose sources are reachable (the definitional GT-5 and GT-6) feed only a MEDIUM chain. Under the rubric's multiple-GT clause that bands Hand-wavy. C1's MEDIUM comes from GT-1? and GT-2? on the same head, which no read available here can lift, so this is accepted as a residual and not "fixed" by inventing a HIGH chain for arithmetic definitions.

**Criterion 4: Reason Upward**
Quoted span: "| C7 | GT-8 + GT-7 + GT-9 + GT-10 | yes | n/a | yes | HIGH | yes | none |" (and rows C1–C6, each `yes | n/a | yes`); for hop validity: "→ z = 1.96 is reached at N = 0.124156 × (1.96 / 0.051)² = 0.124156 × 1476.97 = 183.4, i.e. about 184 accounts"
Band: **Rigorous**
Justification: All seven chains conform in form, with clean dependencies, and each has genuine intermediates. Every figure recomputes independently (Recompute table). The assumed premises carry `[Assumes: A-4/A-7/A-15/A-16]`. §5 records seven dead ends in the What-was-tried / Why-abandoned / What-it-ruled-out structure, and the one analogy considered is itself abandoned, not used.

**Criterion 5: Validate**
Quoted span: "**Pre-check:** head GT-8, GT-7, GT-9, GT-10 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH" alongside C1–C6 MEDIUM lines that each name GT-1?/GT-2?/GT-3?/GT-4? or a cited MEDIUM chain, and the record's "**K1, plan change.** Add a week-1 feasibility gate … Owner: RevOps lead."
Band: **Rigorous**
Justification: The bands are calibrated in both directions. C7 is HIGH because its axes license it. C1–C6 are MEDIUM, each naming the axis that is short and how to close it. The §6 MEDIUM equals the weakest contributing chain. The adversarial record has every part, and each of its four clusters is dispositioned with an owner and a tripwire. K1 and K2 were folded back into C6 and §6.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Recommended approach: do not name a root cause yet; two tracks … | bold lead-in | yes | … | C7, C3, C5, C6 |"; for the Key Insight: "In an annual-renewal business, a Q3 renewal pile-up of 56.1% of the base would produce it with retention unchanged (chain C3)."
Band: **Sound**
Justification: All five §6 claims trace to named chains, and the Key Insight is a non-obvious finding, not a restatement of the recommendation. However, the recommended approach includes the week-1 feasibility gate and prospective exit interviews, which appear in C6's confidence line and the adversarial record but in no chain hop. That is one claim not fully established by a §4 chain.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "focused-five-whys",
  "assumptions": [
    {
      "id": "A-1",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-2",
      "type": "convention",
      "verdict": "Challenge"
    },
    {
      "id": "A-3",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-4",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-5",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-6",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-7",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-8",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-9",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-10",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-11",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-12",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-13",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-14",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-15",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-16",
      "type": "untested belief",
      "verdict": "Challenge"
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": false
    },
    {
      "id": "GT-2",
      "read_at_source": false
    },
    {
      "id": "GT-3",
      "read_at_source": false
    },
    {
      "id": "GT-4",
      "read_at_source": false
    },
    {
      "id": "GT-5",
      "read_at_source": true
    },
    {
      "id": "GT-6",
      "read_at_source": true
    },
    {
      "id": "GT-7",
      "read_at_source": true
    },
    {
      "id": "GT-8",
      "read_at_source": true
    },
    {
      "id": "GT-9",
      "read_at_source": true
    },
    {
      "id": "GT-10",
      "read_at_source": true
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-1?",
        "GT-2?",
        "GT-5",
        "GT-6"
      ]
    },
    {
      "id": "C2",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-1?",
        "GT-2?",
        "GT-7",
        "GT-10"
      ]
    },
    {
      "id": "C3",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-8",
        "GT-3?",
        "GT-1?",
        "GT-2?"
      ]
    },
    {
      "id": "C4",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-4?",
        "GT-9"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "C3",
        "C4",
        "GT-10"
      ]
    },
    {
      "id": "C6",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C3",
        "C4",
        "C5"
      ]
    },
    {
      "id": "C7",
      "confidence": "HIGH",
      "rests_on": [
        "GT-8",
        "GT-7",
        "GT-9",
        "GT-10"
      ]
    }
  ],
  "dead_ends": [
    "Rising tickets and falling adoption show the root cause is onboarding or the product",
    "Pick the cause by industry pattern (\"mid-market SaaS churn is usually onboarding\")",
    "A 124% increase is too large to be noise",
    "The quarterly churn rate is an adequate measure of retention",
    "Name a single root cause now, as instructed",
    "Wait for the diagnosis and do nothing in the meantime",
    "Launch a broad fix now (a price cut, an onboarding overhaul, more support staff) to cover all bases"
  ],
  "techniques": {
    "applied": [
      "fishbone",
      "five-whys",
      "second-order",
      "pre-mortem"
    ],
    "not_applied": []
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Sound",
          "Rigorous",
          "Hand-wavy",
          "Rigorous",
          "Rigorous",
          "Sound"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": false,
    "cleared": true
  },
  "re_entry": {
    "fired": false,
    "edges": []
  },
  "conclusion": {
    "recommendation": "Do not name a root cause yet, because none can be identified from the information supplied (chain C7). Run two tracks at the same time for four to six weeks. First, re-measure churn as the non-renewal rate among accounts actually due for renewal, with early terminations counted separately (chain C3), and cut the Q1–Q3 churned and renewed accounts against the discriminator table in C5 (chain C5). Second, flag renewals due in the next 120 days by low adoption and high ticket volume for Customer Success outreach. Concessions need approval and are logged (chain C6). In week 1, confirm that renewal dates and the churn definition can be rebuilt and report N; if branch cells would hold fewer than about 10 churners, add structured exit interviews for Q4 churners (chain C5). Commit structural spend only to the branch or branches the cuts implicate (chain C6).",
    "confidence": "MEDIUM"
  }
}
```
