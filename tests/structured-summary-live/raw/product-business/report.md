**Disclosed:** No figures for this product were supplied: no serving cost per free account, ARPA, gross margin, churn, cannibalisation, downgrade exposure or competitor data. Interactive clarification was unavailable, so this is a best-effort analysis. It derives the test the figures must pass, shows how sensitive that test is using clearly labelled hypothetical values, and names the measurements that would settle it.

## Answer

**Recommendation:** Do not launch a permanent free tier on the current case. Compute this product's break-even conversion p* = (s + δ − r)/((1 − q)·L) from existing data first, then run a time-boxed experiment only if p* falls between 0% and 100% (chains C1, C5).

**Band (from §6):** MEDIUM (chains C2, C4, C5)

**Would change it:** This product's measured serving cost, ARPA, margin, churn and downgrade exposure, plus naming any competitor relied on (chains C2, C4, C5).

## 1. Problem Essence

**Core problem:** Do this product's own measured unit economics show that a free tier creates more contribution than it costs? Or is every input to that case (conversion, serving cost, cannibalisation, customer value) an unverified belief or a figure borrowed from a competitor?

**Success criteria:**

1. The answer names the exact condition that a free tier's economics must satisfy. It is written as an inequality over named quantities, so a reader can test it against real figures.
2. Every input to that condition is classified as measured for this product, unverified, or borrowed by analogy. The classification is visible per input.
3. The answer says whether the evidence available to this analysis settles the condition. If it does not, the answer names the smallest set of measurements that would.
4. Every computed figure shows its arithmetic and is recomputed independently in the Phase 5 record.
5. The answer is not limited to "add a free tier" or "do not." Composite options (time-boxed trial, capped or reverse trial, a bounded cohort experiment) are tested as options in their own right.

---

## 2. Assumptions Table

Symbols used below and throughout: **N** = free sign-ups in a cohort; **p** = fraction of free sign-ups that convert to paid; **q** = fraction of those converters who would have paid without a free tier (cannibalised conversions); **L** = contribution lifetime value of one paying account; **s** = cost to serve and support one free account over its free lifetime; **δ** = contribution lost per free sign-up to existing paying customers downgrading; **r** = non-conversion value per free account (referrals, word-of-mouth).

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A free tier's net value is incremental contribution from conversions, plus other value, minus serving cost and downgrade loss | physical law | Accept as ground-truth candidate (accounting identity) | Accept — a definition of net contribution; nothing is asserted about the world | Identity stated as GT-1 and checkable by inspection |
| Contribution LTV equals ARPA times gross margin divided by monthly churn | physical law | Accept as ground-truth candidate (definition, steady state) | Accept — the standard closed form for a constant-churn geometric lifetime; it is approximate only when churn varies with tenure | Stated as GT-2; the derivation is the sum of the geometric series |
| This product's free-user serving and support cost s is known | untested belief | Verify, or flag | Challenge — no figure for this product was supplied to this analysis | unverified — flagged GT-3? |
| This product's ARPA, gross margin and churn (hence L) are known | untested belief | Verify, or flag | Challenge — no figure supplied; these exist in the product's own billing data and are measurable now | unverified — flagged GT-4? |
| A free tier will convert at a rate p high enough to pay for itself | untested belief | Verify, or flag | Challenge — no free tier exists, so this product has no observed p; any figure in hand is a belief or borrowed | unverified — flagged GT-5? |
| Few converters would have paid anyway (q small) and few paying customers downgrade (δ small) | untested belief | Verify, or flag | Challenge — no figure supplied; δ can be bounded now from current customers' usage against the proposed free-tier limits | unverified — flagged GT-6? |
| A competitor's free tier works, so ours will | convention | Explicitly challenge before use | Discard — analogy; competitor success shows only that the competitor's parameters satisfy the inequality (chain C4) | unverified — flagged GT-7? as a fact about the competitor only |
| Free-to-paid conversion for B2B SaaS free tiers runs in the low single-digit percent | untested belief | Verify, or flag | Challenge — widely repeated industry figure; no source was opened and it describes other products | unverified — flagged GT-8? |
| A quantity defined on a population that does not yet exist cannot be observed before that population exists | physical law | Accept as ground-truth candidate (logic) | Accept — p for a not-yet-launched tier is counterfactual by definition | Stated as GT-9 |
| Launching a free tier is cheap to reverse | untested belief | Verify, or flag | Challenge — surfaced by the second-order pass; withdrawing a free tier imposes a cost on its users and on reputation | unverified — flagged; surfaced in the Assumption Audit (A-10) |
| The hypothetical parameter values in chain C2 span the plausible range for B2B SaaS | untested belief | Verify, or flag | Challenge — they are constructed for illustration, not measured; they demonstrate sensitivity, not this product's position | unverified — flagged; surfaced in the Assumption Audit (A-11) |
| Downgrade loss and cannibalisation can be estimated from existing data before launch | current constraint | Record expiry conditions | Accept — expires once a free tier launches, after which they become directly observable; until then they are bounded from current-customer usage | Surfaced in the Assumption Audit (A-12) |

---

## 3. Ground Truths

- **GT-1** Net contribution of a free tier, per free sign-up, is defined as **v = p·(1−q)·L + r − s − δ**. Only conversions that would not otherwise have occurred count (the (1−q) factor). Contribution from downgrading existing payers is lost (δ). Serving cost is paid on every free account, converted or not (s). Source: definition (accounting identity); the reduction bottoms out at the definition of incremental contribution. Provenance: definitional. There is no external figure to read; the identity is checkable by inspection, as written here.
- **GT-2** For a constant monthly churn rate c, the expected lifetime of a paying account is 1/c months (geometric series Σ(1−c)^k for k = 0 to ∞ = 1/c). So **L = ARPA × gross margin / c**. Source: definition plus the sum of a geometric series. Provenance: definitional / mathematical, checkable by inspection. It is approximate where churn depends on tenure.
- **GT-3?** This product's free-account serving and support cost s. Unverified: no figure for this product was supplied to the analysis.
- **GT-4?** This product's ARPA, gross margin and churn, and therefore L via GT-2. Unverified: no figure supplied. They are measurable now from the product's billing and cost data.
- **GT-5?** This product's free-to-paid conversion rate p. Unverified: no free tier exists, so no observed value exists (see GT-9).
- **GT-6?** This product's cannibalisation fraction q, downgrade loss δ and non-conversion value r. Unverified: no figure supplied.
- **GT-7?** Some competitors operate free tiers. Unverified: no competitor was named and no source was supplied or opened. Even if true, it is a fact about the competitor's parameters only.
- **GT-8?** Free-to-paid conversion for B2B SaaS free tiers is commonly quoted in the low single-digit percent (roughly 2–5%). Unverified: industry rule of thumb, no source opened. It describes other products.
- **GT-9** A quantity defined on a population that does not yet exist cannot be observed before that population exists. p is defined on free sign-ups to a tier that has not launched. Source: logic. Provenance: definitional, checkable by inspection.
- **GT-10** The product does not currently offer a free tier. Source: the user's problem statement. Read-at-source: "Does this B2B SaaS product's own economics support *adding* a free tier"; adding presupposes the tier does not yet exist.

**Irreducibility (five-whys, reduce-to-primitives mode):** The compound claim "a free tier pays for itself here" reduces to "v > 0" (GT-1). That reduces to the six parameters p, q, L, r, s, δ, and L reduces further to ARPA, margin and churn (GT-2). Each parameter is a direct measurement of this product. None was measured, so every branch below the identity is `Assumed — unverified`, and the parent claim is flagged `?`.

**Provenance summary:**

```text
?-marked: GT-3?, GT-4?, GT-5?, GT-6?, GT-7?, GT-8? (6 of 10)
Unsuffixed: GT-1, GT-2, GT-9 — definitional/logical; no external source exists to open. The read-location is the statement itself in this section, checkable by inspection.
Read-at-source: GT-10 — problem statement, the phrase "support adding a free tier"
```

**Phase 3 verification step:** None of the `?`-marked ground truths names a source that could be opened. GT-3? to GT-6? are this product's own figures and none was supplied. GT-7? names no competitor. GT-8? is a rule of thumb with no cited source. Phase 3 failure record, for each of GT-3? to GT-8?: *source not supplied / ambiguous citation — no read possible*. All keep their `?`.

---

## 4. Derivation Chains

### Conclusion C1: A free tier pays only if this product's conversion rate exceeds a break-even rate set entirely by this product's own parameters

GT-1 (net value identity) + GT-2 (lifetime value definition)
→ setting v = 0 and solving for p gives the break-even rate p* = (s + δ − r) / ((1 − q) · L)
→ a free tier adds contribution only when this product's p exceeds p* computed from this product's own s, δ, r, q and L

Arithmetic (rearrangement): v = p·(1−q)·L + r − s − δ = 0 ⇒ p·(1−q)·L = s + δ − r ⇒ p* = (s + δ − r)/((1−q)·L), valid for q < 1 and L > 0.

**Pre-check:** head GT-1, GT-2 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH. Both inputs are definitional and checkable by inspection, and the hop is algebra that recomputes (Phase 5 record). The strongest rival is that a free tier's value is strategic and not captured by a contribution formula. §5 "Dead End: Strategic value outside the identity" rules it out using GT-1, whose r term carries any such value once it is stated in money.

### Conclusion C2: Across parameter sets nothing about this product excludes, the break-even rate moves by more than two orders of magnitude, so the decision turns on this product's own figures

C1 (break-even p*) + GT-3? (serving cost s) + GT-4? (ARPA, margin, churn) + GT-6? (q, δ, r) + GT-8? (2–5% quoted conversion)
→ hypothetical case A (s=$5, δ=$0, r=$0, q=0.2, ARPA $100/mo, margin 0.8, churn 2%/mo) gives L = 100×0.8/0.02 = $4,000 and p* = 5/(0.8×4,000) = 5/3,200 = 0.15625% [Assumes: A-11]
→ hypothetical central case (s=$20, δ=$5, r=$0, q=0.3, ARPA $50/mo, margin 0.75, churn 3%/mo) gives L = 50×0.75/0.03 = $1,250 and p* = 25/(0.7×1,250) = 25/875 = 2.857% [Assumes: A-11]
→ hypothetical case B (s=$60, δ=$10, r=$0, q=0.5, ARPA $30/mo, margin 0.7, churn 5%/mo) gives L = 30×0.7/0.05 = $420 and p* = 70/(0.5×420) = 70/210 = 33.33% [Assumes: A-11]
→ across the three cases p* spans 33.333% / 0.15625% = 213.3×, more than two orders of magnitude
→ in the central case v = 0.02×875 − 25 = −$7.50 at p = 2% but v = 0.05×875 − 25 = +$18.75 at p = 5%
→ the sign of v flips inside the conversion band GT-8? quotes, so that band cannot decide the question
→ only this product's own s, δ, r, q and L can locate p*

**Pre-check:** head C1 (HIGH), GT-3?, GT-4?, GT-6?, GT-8? · ?-marked: GT-3?, GT-4?, GT-6?, GT-8? · lowest cited: HIGH · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. The Inputs axis is short. GT-3?, GT-4? and GT-6? are unsupplied product figures, and the hypothetical values stand in for them. Supplying the product's measured serving cost, ARPA, margin, churn, and downgrade exposure would remove them as causes. GT-8? is an unsourced rule of thumb; opening a published conversion benchmark would remove it. A-11 (the grid spans the plausible range) is priced: if the realistic range were narrower, the central case alone still flips sign inside the GT-8? band, so the endpoint stands. Rivals: §5 "Dead End: Use the industry conversion band as this product's p" rules out the competing reading.

### Conclusion C3: This product's conversion rate for a tier that does not exist has no observed value, so the break-even test cannot be passed on its own evidence before an experiment

GT-9 (counterfactual quantities are unobservable) + GT-10 (no free tier exists today)
→ this product's p is defined on a free-sign-up population that does not yet exist and so has no observed value
→ any p figure now supporting a free-tier case is an internal belief or a figure measured on another product
→ the C1 test of p against p* cannot be passed on this product's evidence until a bounded experiment produces a measured p

**Pre-check:** head GT-9, GT-10 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH. GT-9 is logical and GT-10 was read in the problem statement. Each hop is a deduction. The strongest rival is that an existing proxy, such as free-trial conversion, already measures p. §5 "Dead End: Treat free-trial conversion as the free-tier p" rules it out using GT-9: a trial measures a different, time-boxed population, so it bounds p but does not observe it.

### Conclusion C4: Competitor analogy adds no independent evidence, because confirming that it transfers needs the same product measurements it was meant to replace

GT-1 (net value identity) + GT-7? (competitors run free tiers)
→ a competitor's working free tier shows at most that the competitor's own p exceeds the competitor's own p*
→ that result transfers only if this product's s, δ, r, q and L give a p* no higher than the p the competitor achieves
→ confirming that transfer condition requires this product's own measurements, so the analogy supplies no evidence those measurements would not

**Pre-check:** head GT-1, GT-7? · ?-marked: GT-7? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. The Inputs axis is short on GT-7?: no competitor was named and no source was opened. Naming the competitor and reading its disclosed free-tier figures would remove it as a cause. The endpoint does not depend on GT-7? being true; if it were false, the analogy would have even less to offer. Inference and Rivals are clean. The endpoint is itself a ruling-out of analogy as evidence.

### Conclusion C5: As presented, the case for a free tier rests on unverified beliefs and analogy, not on this product's economics, so the next step is to measure, then run a bounded experiment

C1 (HIGH) + C2 (MEDIUM) + C3 (HIGH) + C4 (MEDIUM)
→ every term of the break-even test is either unmeasured for this product (s, δ, r, q, L) or unmeasurable before launch (p)
→ the case for a free tier, as presented to this analysis, therefore rests entirely on unverified beliefs and competitor analogy
→ this product's economics neither support nor refute a free tier yet
→ the move that decides it is to compute L, s and δ from existing billing, cost and usage data now and derive p*, then run a bounded, reversible free-tier experiment that measures p against p* [Assumes: A-12]
→ a computed p* at or below 0% settles the case for launch, and one at or above 100% settles it against, so the experiment runs only when p* falls strictly between them
→[2nd] actor lens: existing payers whose usage fits under the free limits are the δ exposure, so the experiment admits new sign-ups only
→[2nd] actor lens: support and sales absorb free-account load, so s must include support time, not only infrastructure cost
→[2nd] time lens: an experiment costs build time plus s per sign-up immediately, and yields a measured p only after cohorts have aged past the typical conversion window
→[3rd] time lens: a free tier left in place long enough to be assumed becomes costly to withdraw, so the experiment must be announced as time-boxed or cohort-limited from launch [Assumes: A-10]

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (HIGH), C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. The Inputs axis is short because C2 and C4 are MEDIUM; their own lines carry the verification paths. A-12 (δ and L can be bounded from existing data before launch) is priced: if it failed, the experiment would also have to measure δ, which delays the decision but does not change the endpoint. A-10 qualifies only the third-order extension, not the endpoint. Rivals: the competing conclusion, "the product's own unseen data already supports a free tier," is outside the scoped claim "as presented to this analysis." §5 "Dead End: Infer the answer from data not supplied" records why it was not used.

---

## 5. Abandoned Reasoning

### Dead End: Strategic value outside the identity

**What was tried:** The rival reading of C1: a free tier's value is "strategic" (market presence, top-of-funnel, brand) and so cannot be judged by a contribution formula.

**Why abandoned:** GT-1 already carries a term, r, for any non-conversion value per free account. Strategic value that cannot be stated even as a range in money cannot be weighed against s and δ, which are paid in money. An unpriced strategic benefit can justify any cost, so it does not discriminate between options.

**What it ruled out:** "It's strategic" as a reason to skip the break-even test. The reader is instead asked to put a number, or a range, on r.

### Dead End: Use the industry conversion band as this product's p

**What was tried:** The rival reading of C2: take the commonly quoted 2–5% free-to-paid conversion (GT-8?) as p, compare it with a p* computed from typical figures, and conclude.

**Why abandoned:** C2's arithmetic shows the sign of v flips inside that band in the central case (−$7.50 at 2%, +$18.75 at 5%). The band also describes other products, which is the analogy C4 rules out.

**What it ruled out:** Deciding with a borrowed conversion rate, even a widely repeated one.

### Dead End: Treat free-trial conversion as the free-tier p

**What was tried:** The rival reading of C3: if the product runs a time-boxed trial, its conversion rate already measures p.

**Why abandoned:** GT-9: a time-boxed trial and a perpetual free tier sign up different populations under different deadlines. A trial's conversion rate is a measurement of a neighbouring quantity, so it is a prior on p and not an observation of it.

**What it ruled out:** Skipping the bounded experiment on the strength of trial data. Trial data can still narrow the experiment's expected range.

### Dead End: Infer the answer from data not supplied

**What was tried:** The rival reading of C5: the product team may hold measured s, L, q and δ, and those figures might already clear the bar, so "rests entirely on unverified beliefs" may be false of the product even if true of what this analysis saw.

**Why abandoned:** The analysis cannot use figures it was not given without inventing them. C5's claim is therefore scoped to the case as presented. This rival is the conclusion's falsification condition (Phase 5 record), not a competing finding.

**What it ruled out:** Reading C5 as a claim that no supporting data exists anywhere. It is a claim that none was presented.

### Dead End: Launch a permanent free tier now

**What was tried:** The composite and status-quo options in success criterion 5. Option (a) is to launch a permanent free tier now. Option (b) is to keep the status quo with no free tier and no experiment. Option (c) is the composite: measure existing figures, then run a bounded or capped free-tier experiment (a reverse trial is one variant).

**Why abandoned:** Option (a) fails the must-have that a decision rest on this product's evidence (C3, C5). The second-order pass on C5 adds that it is the hardest option to reverse (A-10). Between (b) and (c), the first step of (c), computing p* from existing data, costs little and is required by either path. That is why the recommendation is a sequence rather than a weighted pick.

**What it ruled out:** A launch decision taken before p* is known.

---

## 6. Conclusion

**Recommended approach:** Do not launch a permanent free tier on the current case (chain C5). First, compute this product's break-even conversion rate p* = (s + δ − r)/((1 − q)·L) from existing billing, cost and usage data (chain C1). If p* is at or below 0% or at or above 100%, the existing data settles the question without an experiment (chain C5). Otherwise, run a time-boxed, new-sign-ups-only free-tier experiment and launch only if its measured conversion clears p* (chain C5).

**Key insight:** As presented, the case for a free tier rests entirely on unverified beliefs and competitor analogy (chain C5). The decisive quantity, the break-even rate, can sit anywhere from about 0.16% to 33% depending on this product's own figures, so a borrowed 2–5% conversion rate cannot settle it (chain C2). A competitor's success transfers only after the very measurements it was meant to replace (chain C4).

**Trade-offs acknowledged:** Measuring first delays any free-tier upside by at least one conversion window, and the experiment spends serving and support cost on sign-ups that may never convert (chain C5). Before launch, conversion can only be bounded, not observed (chain C3).

**Pre-check:** head C1 (HIGH), C2 (MEDIUM), C3 (HIGH), C4 (MEDIUM), C5 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. C2, C4 and C5 are rated below HIGH, and their §4 lines carry the verification paths: supplying this product's serving cost, ARPA, margin, churn and downgrade exposure, and naming any competitor relied on (chains C2, C4, C5). The conclusion has no downgrade cause of its own beyond those chains.
## Appendix — process output

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | solve v = 0 for p* | no | n/a |
| C1 | 2 | free tier pays only if p > p* | no | n/a |
| C2 | 1 | case A: L = $4,000, p* = 0.15625% | yes — A-11 (hypothetical grid spans plausible range) | yes (row 11) |
| C2 | 2 | central: L = $1,250, p* = 2.857% | yes — A-11 (same assumption, not duplicated) | already present |
| C2 | 3 | case B: L = $420, p* = 33.33% | yes — A-11 (same assumption, not duplicated) | already present |
| C2 | 4 | span 213.3× | no | n/a |
| C2 | 5 | v = −$7.50 at 2%, +$18.75 at 5% | no | n/a |
| C2 | 6 | sign flips inside the GT-8? band | no | n/a |
| C2 | 7 | only product figures locate p* | no | n/a |
| C3 | 1 | p has no observed value | no | n/a |
| C3 | 2 | current p figures are belief or borrowed | no | n/a |
| C3 | 3 | test cannot pass before an experiment | no | n/a |
| C4 | 1 | competitor shows only its own p > p* | no | n/a |
| C4 | 2 | transfer needs this product's p* ≤ competitor p | no | n/a |
| C4 | 3 | analogy adds no independent evidence | no | n/a |
| C5 | 1 | every term unmeasured or unmeasurable | no | n/a |
| C5 | 2 | case rests on beliefs and analogy | no | n/a |
| C5 | 3 | economics neither support nor refute | no | n/a |
| C5 | 4 | measure, then run a bounded experiment | yes — A-12 (δ, L boundable from existing data) | yes (row 12) |
| C5 | 5 | p* outside (0%, 100%) settles it without an experiment | no — p is a fraction, bounded by definition | n/a |
| C5 | 2nd-a | new sign-ups only (δ exposure) | no | n/a |
| C5 | 2nd-b | s includes support time | no | n/a |
| C5 | 2nd-c | measured p only after the conversion window | no | n/a |
| C5 | 3rd | announce as time-boxed (irreversibility) | yes — A-10 (launch cheap to reverse: challenged) | yes (row 10) |

Techniques not applied:
- theoretical-limit — not applicable — Phase 1: the question turns on a product's measured unit economics, not on whether a figure is a convention or a physical bound
- fishbone — not applicable — Phase 2: the assumption space is fixed by the six terms of the GT-1 identity, so a category brainstorm adds no branches
- inversion — not applicable — Phase 2: the assumption set was not thin; inversion is applied instead to the headline claim in Phase 5
- trade-off — not applicable — Phase 4: only the composite option survives the evidentiary must-have, and its first step is a precondition of every path (§5 "Launch a permanent free tier now")
- theoretical-limit — not applicable — Phase 4: no conclusion needs a law-permitted ceiling; the break-even rate is an accounting threshold, not a physical bound

Techniques applied: five-whys (reduce-to-primitives, Phase 3), estimate (C2 three-case bracket, Phase 4 — the bracket straddles the threshold, so the uncertainty is escalated to "measure the product's figures"), second-order (C5 extension, Phase 4), inversion (headline claim, Phase 5).

## Adversarial pass (process output)

**Recompute:** Each figure is redone below by a different grouping from the chain text, and each was also checked with an exact-fraction calculator.
- C1: v = p(1−q)L + r − s − δ = 0 → p(1−q)L = s + δ − r → p* = (s + δ − r)/((1−q)L). Substituting back gives p*(1−q)L + r − s − δ = (s + δ − r) + r − s − δ = 0 ✓
- C2 case A: ARPA × margin = 100 × 0.8 = 80; 80 / 0.02 = 4,000 ✓. (1 − 0.2) × 4,000 = 3,200; (5 + 0 − 0) / 3,200 = 1/640 = 0.0015625 = 0.15625% ✓
- C2 central case: 50 × 0.75 = 37.5; 37.5 / 0.03 = 1,250 ✓. 0.7 × 1,250 = 875; (20 + 5 − 0) / 875 = 1/35 = 0.028571 = 2.857% ✓
- C2 case B: 30 × 0.7 = 21; 21 / 0.05 = 420 ✓. 0.5 × 420 = 210; (60 + 10 − 0) / 210 = 1/3 = 33.33% ✓
- C2 span: (1/3) / (1/640) = 640/3 = 213.33× ✓. Direction check: the larger threshold divided by the smaller gives a factor above 1, as it must.
- C2 sign flip: 0.02 × 875 = 17.5; 17.5 − 25 = −7.50 ✓. 0.05 × 875 = 43.75; 43.75 − 25 = +18.75 ✓. Consistency: the central p* of 2.857% lies between 2% and 5%, so v must change sign inside the band, and it does.
- C5 range gate: p is a fraction in [0, 1]. If p* ≤ 0, then v ≥ 0 even at p = 0; if p* ≥ 1, then v ≤ 0 even at p = 1. Both follow from C1's rearrangement ✓

**Sensitivity:** Two flip points:
- The headline claim "as presented, rests entirely on unverified beliefs and analogy" flips if GT-3?, GT-4? or GT-6? were in fact measured and supplied. Those are `?`-marked, and this analysis cannot verify them because no source exists to read, so C2 and C5 carry MEDIUM with that verification path named.
- The recommendation's ordering (measure, then experiment) flips if GT-9 were false. GT-9 is unsuffixed and logical.

Weakest link per chain:
- C1: the r term, which is the hardest to put in money.
- C2: A-11, the hypothetical grid.
- C3: the step from "no observed p" to "every current p figure is borrowed" (it assumes no prior free-tier history; see cluster K1).
- C4: GT-7?, since no competitor was named.
- C5: A-12, that δ and L are computable now.

**Rival:**
- C1: §5 "Strategic value outside the identity".
- C2: §5 "Use the industry conversion band as this product's p".
- C3: §5 "Treat free-trial conversion as the free-tier p".
- C4: rival not applicable — the endpoint is itself a ruling-out of analogy as evidence.
- C5 (headline): §5 "Infer the answer from data not supplied". The option rival is §5 "Launch a permanent free tier now".

**Premise:** The headline claim is already false: this product's own economics did support (or refute) a free tier, and the case did not rest only on unverified beliefs and analogy. Technique: inversion, because the headline is a claim; the plan attached to it is covered by clusters K1–K3.

**Causes:**
- *Finance lead:* "We had measured serving cost, ARPA, margin and churn all along; nobody passed them to the analysis."
- *Finance lead:* "Free accounts cost almost nothing to serve and refer paying users, so r ≥ s + δ and p* ≤ 0. Any conversion at all was profit."
- *Finance lead:* "Our churn and margin made (1 − q)L smaller than s + δ, so p* exceeded 100% and no conversion rate could save it."
- *Product manager:* "We ran a free tier two years ago and withdrew it, so we had an observed p for this product."
- *Product manager:* "Our trial conversion data put an upper bound on p well below p*, so the answer was already no."
- *Growth lead:* "Free-tier converters cost far less to acquire than paid-channel converters. That CAC saving is real money that the identity's terms did not obviously carry."
- *Growth lead:* "Expansion revenue from free-sourced accounts was higher, so L for those converters differs from the base L."
- *Competitor:* "Our free tier's published numbers matched theirs closely enough to transfer." (C4 still requires checking the match against their own figures.)

**Clusters:**
- **K1 Unpresented product evidence** (finance measured figures, prior free-tier history, trial bounds). Bears on C3, C5, GT-3?, GT-4?, GT-6?, GT-10.
- **K2 Threshold outside (0%, 100%)** (p* ≤ 0 or p* ≥ 1, so the decision is settled without p). Bears on C1, C5.
- **K3 Identity terms mis-specified** (CAC saving, converter-specific L). Bears on GT-1, C1.

**Disposition:**
- **K1 — accepted risk, named mitigation.** C5's claim is scoped "as presented to this analysis." The recommendation's first step (compute p* from existing billing, cost and usage data, and collect any prior free-tier or trial data) surfaces any such evidence before any spend.
- **K2 — plan change.** A range-gate hop was added to C5 and to §6's recommended approach. If p* is at or below 0% or at or above 100%, the question is settled without an experiment.
- **K3 — accepted risk, named mitigation.** When p* is computed, any measured CAC saving per converter goes into r, and converter-specific expansion revenue goes into L. GT-1's terms are general enough to carry both once they are stated in money.

**Falsification:** The conclusion is false if, at the time of the decision, this product already had measured values for s, L, q and δ (or an observed free-tier conversion rate for this product) and the decision-makers had them in hand. The case would then have rested on the product's economics, not on beliefs and analogy, whatever this analysis was shown.

## §6→§4 closure ledger (process output)

```text
- "Do not launch a permanent free tier on the current case; compute p* first; settle by range gate or bounded experiment" → chain C5 ✓ (and C1 for the p* formula) ✓
- "As presented, the case rests entirely on unverified beliefs and competitor analogy; p* spans ~0.16% to 33%; analogy transfers only after the measurements" → chain C5, C2, C4 ✓
- "Measuring first delays upside and spends s on non-converters; conversion is only boundable pre-launch" → chain C5, C3 ✓
- "Pre-check: head C1–C5 with bands; Inputs ceiling MEDIUM" → chains C1, C2, C3, C4, C5 ✓
- "Confidence: MEDIUM — C2, C4, C5 below HIGH" → chain C2, C4, C5 ✓
```

No claim cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 + GT-2 | unreached | n/a — non-final head input outside the check's reach; hand-inspected, no violation | yes | HIGH | no | none |
| C2 | C1 + GT-3? + GT-4? + GT-6? + GT-8? | unreached | n/a — non-final head inputs and hops 3–7 outside the check's reach; hand-inspected, no violation | yes | MEDIUM | no | none |
| C3 | GT-9 + GT-10 | unreached | n/a — non-final head input and hop 3 outside the check's reach; hand-inspected, no violation | yes | HIGH | yes | none |
| C4 | GT-1 + GT-7? | unreached | n/a — non-final head input and hop 3 outside the check's reach; hand-inspected, no violation | yes | MEDIUM | no | none |
| C5 | C1 + C2 + C3 + C4 | unreached | n/a — non-final head inputs and hops 3–9 outside the check's reach; hand-inspected, no violation | yes | MEDIUM | no | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: do not launch permanently; compute p*; gate or experiment | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C5, C1 |
| Key insight: case rests on beliefs/analogy; p* 0.16%–33%; analogy needs the measurements | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C5, C2, C4 |
| Trade-offs acknowledged: delay, s on non-converters; p only boundable | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C5, C3 |
| Pre-check: head C1–C5, Inputs ceiling MEDIUM | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C2, C3, C4, C5 (via head) |
| Confidence: MEDIUM | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C2, C4, C5 |

```text
Scan complete: 5 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

Pre-scoring checks:
- The Assumption Audit scan is present with one row per chain step in order. It has 25 rows: C1 2, C2 7, C3 3, C4 3, C5 10 (5 first-order, 3 second-order, 1 third-order, plus step 5).
- The self-audit scan is present with 5 chain rows and 5 §6 rows, and its reconciliation line recounts against sections 4 and 6.

**Criterion 1: Identify Essence**
Quoted span: "Do this product's own measured unit economics show that a free tier creates more contribution than it costs? Or is every input to that case (conversion, serving cost, cannibalisation, customer value) an unverified belief or a figure borrowed from a competitor?"
Band: **Sound**
Justification: The statement names the real question, net incremental contribution, rather than the prompt's either/or framing. The success criteria are pass/fail tests on the Conclusion. However, the Essence Statement runs to two sentences rather than one and keeps the prompt's two-part shape, which is an identifiable departure from the Rigorous descriptor.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C5 | 3rd | announce as time-boxed (irreversibility) | yes — A-10 (launch cheap to reverse: challenged) | yes (row 10) |" together with the table row "| Launching a free tier is cheap to reverse | untested belief | Verify, or flag | Challenge — surfaced by the second-order pass; ... | unverified — flagged; surfaced in the Assumption Audit (A-10) |"
Band: **Rigorous**
Justification: Every row uses a four-type value, a type-matched treatment, an em-dash verdict and a specific verification cell. Six assumptions are challenged and one is discarded, and the audit scan covers every chain step, with each surfaced assumption (A-10, A-11, A-12) recorded in the table.

**Criterion 3: Establish Ground Truths**
Quoted span: comparison, not quotation. The enumeration lists GT-3?, GT-4?, GT-5?, GT-6?, GT-7?, GT-8?; the Ground Truths list carries `?` on exactly those six and on no others (GT-1, GT-2, GT-9, GT-10 unsuffixed). For the HIGH chains: GT-10 names its read location, "the phrase \"support adding a free tier\""; GT-1, GT-2 and GT-9 give "definitional/logical ... the statement itself in this section".
Band: **Sound**
Justification: The enumeration matches the list, and every unsuffixed GT feeds a HIGH chain (GT-1 and GT-2 to C1, GT-9 and GT-10 to C3). However, three unsuffixed GTs rest on "definition/logic" with the statement itself as their read location, which is a generic rather than externally checkable citation. Overlap note: GT-7? (competitors run free tiers) is a different claim from the discarded transfer inference, so this is not a Discard-in-list defect.

**Criterion 4: Reason Upward**
Quoted span: "| C5 | C1 + C2 + C3 + C4 | unreached | n/a — non-final head inputs and hops 3–9 outside the check's reach; hand-inspected, no violation | yes | MEDIUM | no | none |" and the C5 hop "→ a computed p* at or below 0% settles the case for launch, and one at or above 100% settles it against, so the experiment runs only when p* falls strictly between them"
Band: **Sound**
Justification: Every chain is dependency-clean, has an intermediate step, declares its assumptions with `[Assumes:]`, and recomputes in the adversarial record. §5 documents five structured dead ends, and the analogy enters only through GT-7? and is ruled out as evidence. However, the quoted C5 hop, and the C2 hop "the sign of v flips ... so that band cannot decide the question", each join two inferences, departing from the one-inference rule in an identifiable way.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM. C2, C4 and C5 are rated below HIGH, and their §4 lines carry the verification paths: supplying this product's serving cost, ARPA, margin, churn and downgrade exposure, and naming any competitor relied on (chains C2, C4, C5)." together with the record's "**K2 — plan change.** A range-gate hop was added to C5 and to §6's recommended approach."
Band: **Rigorous**
Justification: Every MEDIUM line names its own `?` inputs or sub-HIGH chains with a verification path. The Conclusion's MEDIUM equals its weakest contributing chain. HIGH is given only to C1 and C3, whose inputs are unsuffixed and whose rivals are ruled out in §5. The adversarial record carries every part, each cluster has a disposition, and the weakest link is named per chain. No EXCEPT clause is claimed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight: case rests on beliefs/analogy; p* 0.16%–33%; analogy needs the measurements | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C5, C2, C4 |" and the scan's "5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced."
Band: **Rigorous**
Justification: All five §6 claims cite section-4 chains, and none is new reasoning. The Key Insight is a non-obvious finding, that the break-even rate spans more than 200× and the quoted 2–5% band straddles the sign flip, not a restatement of the recommendation.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {
      "id": "A-1",
      "type": "physical law",
      "verdict": "Accept"
    },
    {
      "id": "A-2",
      "type": "physical law",
      "verdict": "Accept"
    },
    {
      "id": "A-3",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-4",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-5",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-6",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-7",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-8",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-9",
      "type": "physical law",
      "verdict": "Accept"
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
      "type": "current constraint",
      "verdict": "Accept"
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": true
    },
    {
      "id": "GT-2",
      "read_at_source": true
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
      "read_at_source": false
    },
    {
      "id": "GT-6",
      "read_at_source": false
    },
    {
      "id": "GT-7",
      "read_at_source": false
    },
    {
      "id": "GT-8",
      "read_at_source": false
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
      "confidence": "HIGH",
      "rests_on": [
        "GT-1",
        "GT-2"
      ]
    },
    {
      "id": "C2",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "GT-3?",
        "GT-4?",
        "GT-6?",
        "GT-8?"
      ]
    },
    {
      "id": "C3",
      "confidence": "HIGH",
      "rests_on": [
        "GT-9",
        "GT-10"
      ]
    },
    {
      "id": "C4",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-1",
        "GT-7?"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C2",
        "C3",
        "C4"
      ]
    }
  ],
  "dead_ends": [
    "Strategic value outside the identity",
    "Use the industry conversion band as this product's p",
    "Treat free-trial conversion as the free-tier p",
    "Infer the answer from data not supplied",
    "Launch a permanent free tier now"
  ],
  "techniques": {
    "applied": [
      "five-whys",
      "estimate",
      "second-order",
      "inversion"
    ],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "Phase 1: the question turns on a product's measured unit economics, not on whether a figure is a convention or a physical bound"
      },
      {
        "technique": "fishbone",
        "phase": 2,
        "reason": "Phase 2: the assumption space is fixed by the six terms of the GT-1 identity, so a category brainstorm adds no branches"
      },
      {
        "technique": "inversion",
        "phase": 2,
        "reason": "Phase 2: the assumption set was not thin; inversion is applied instead to the headline claim in Phase 5"
      },
      {
        "technique": "trade-off",
        "phase": 4,
        "reason": "Phase 4: only the composite option survives the evidentiary must-have, and its first step is a precondition of every path (§5 \"Launch a permanent free tier now\")"
      },
      {
        "technique": "theoretical-limit",
        "phase": 4,
        "reason": "Phase 4: no conclusion needs a law-permitted ceiling; the break-even rate is an accounting threshold, not a physical bound"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Sound",
          "Rigorous",
          "Sound",
          "Sound",
          "Rigorous",
          "Rigorous"
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
    "recommendation": "Do not launch a permanent free tier on the current case (chain C5). First, compute this product's break-even conversion rate p* = (s + δ − r)/((1 − q)·L) from existing billing, cost and usage data (chain C1). If p* is at or below 0% or at or above 100%, the existing data settles the question without an experiment (chain C5). Otherwise, run a time-boxed, new-sign-ups-only free-tier experiment and launch only if its measured conversion clears p* (chain C5).",
    "confidence": "MEDIUM"
  }
}
```
