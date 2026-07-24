I'll read the four documents and apply the rule mechanically.

## Q-N2

**1. Load-bearing-claim set** (paragraph/bullet-level claims in §6 the conclusion rests on — recommendations, decisions, quantitative results, causal assertions; excluding section-intro labels, restatements of already-cited content, and confidence/caveat fields):

- *"**Do none of the three things as posed. Stage it.**"*
- *"**The 35kg roaster is sized to demand you do not have yet (C1).** At 20% annual growth it takes about 4.6 years to fill. You would be paying $103,000 today for headroom that sits idle for roughly three of those years, while the two accounts underwriting the growth can leave with thirty days' notice."*
- *"**Do not adopt a permanent double shift as the end state either (C5).** It doubles duty cycle on a single machine with zero redundancy — raising outage probability exactly when your commitments peak. It is a fine bridge and a poor destination."*
- *"**Do not hold off (C2, C3).** Capacity binds now, the machine has roughly 4.7x physical headroom that only a staffing convention is blocking, and the margin you are turning away likely exceeds the cost of either fix by an order of magnitude."*
- *"**Now — add a partial second shift**, not a full one. A four-to-five-hour evening turn at roughly $2,100–2,500/mo buys most of the capacity at half the cost and half the wear, and it is cancellable at thirty days (C2, C4, C7). This is the bridge across the equipment lead time, which you will need regardless of what you eventually buy."*
- *"**Within 30 days — get the one number that decides this.** What percentage of volume do those two accounts represent? Rough thresholds from C1's arithmetic: if their combined share is **under ~20%**, growth alone keeps you capacity-bound through their loss and you should buy. If it is **over ~35%**, losing them returns you to slack capacity and you should not commit capital until the account base is broader."*
- *"**Within 60–90 days — convert the terms.** Offer locked pricing, priority peak allocation, or a volume rebate in exchange for a six-to-twelve-month commitment or a monthly volume floor. Do not make a bare ask: it invites them to shop (A-17, C7 second-order). A signed floor is also financeable collateral that improves your eventual loan terms."*
- *"**Then buy — but price a twin, not the 35kg (C6).** A second 15–25kg machine gives you the same ~2x capacity, full redundancy against the failure mode that scares me most, identical roast profiles with no re-development risk to your flagship blends, and roughly half the capital outlay. Get that quote before you sign anything for the 35kg."*
- *"**Pre-register the trigger now, while you are calm.** Write it down: *"We order when (a) contracted or floor-committed volume covers X kg/week, or (b) the two at-risk accounts fall below Y% of volume, whichever comes first."* Deciding the rule before the data arrives is what stops a good month from being mistaken for a trend."*
- *"**Cost is not the deciding variable here (C3).** The $35k/yr spread between your two original options is a rounding error against the ~$100–250k/yr of margin that hinges on whether the demand is durable. Spend the next ninety days buying information about that, not equipment."*

**2. Traced / untraced marks:**

| Claim | Mark | §4 support |
|---|---|---|
| "Do none of the three things as posed. Stage it." | **traced** | C7 (staged path: "bridge with a partial second shift now… then buy a right-sized second machine on a pre-registered trigger") |
| 35kg sized to demand you don't have (4.6 yrs, $103k, idle ~3 yrs) | **traced** | C1 — `ln(2.3) ÷ ln(1.2) ≈ 4.6 years`, "$103,000 asset runs below 50% utilisation for roughly its first three years"; GT-5, GT-7, GT-8 |
| No permanent double shift (doubled duty, zero redundancy, outage probability) | **traced** | C5 — GT-14 + GT-15?, "doubling duty cycle… while leaving zero redundancy → the failure probability rises fastest exactly when volume and commitments are highest" |
| Do not hold off (binds now, 4.7x headroom, margin exceeds cost by an order of magnitude) | **traced** | C2 (theoretical-limit sub-step, "Gap: ~4.7x"; GT-9) and C3 (~$35k/yr spread vs $100–250k/yr contribution) |
| Now — partial second shift, ~$2,100–2,500/mo, cancellable at 30 days, bridges lead time | **traced** | C2 (second shift is the matched increment), C4 (shift downside ≈$5–10k, one month's notice; GT-13), C7 (staged path relieves capacity inside the 3–6 month lead time, GT-12?). The *partial*-shift halving of the full $4,200/mo figure is arithmetic on GT-6. |
| Within 30 days — get the concentration number; ~20% / ~35% thresholds | **partially traced** — the need for the number is traced; the specific 20%/35% numbers are not | Traced to GT-16? (declared "the single highest-leverage missing fact") and A-4 (flagged direction-changing). But C1's arithmetic derives 2.3x headroom and 4.6 years — it never derives ~20% or ~35%. The claim cites "Rough thresholds from C1's arithmetic"; no §4 chain contains that computation. **Untraced on the quantitative part.** |
| Within 60–90 days — convert terms, don't make a bare ask | **traced** | C7 and its →[2nd] extension ("the term-conversion ask may itself prompt an account to re-evaluate… mitigate by pairing the ask with something they want: locked pricing, priority allocation…, or a volume rebate"); →[3rd] on financeable evidence; A-17 |
| Then buy a twin, not the 35kg (same ~2x, redundancy, identical profiles, ~half outlay) | **traced** | C6 — "delivers the same ~2x as the shift, adds full redundancy, preserves existing profiles…, and costs roughly half of $103,000"; GT-3; A-14, A-15 |
| Pre-register the trigger now | **traced** | C7 ("buy a right-sized second machine on a pre-registered trigger") and C4 (reversibility premium rational only while the terms uncertainty is live) |
| Cost is not the deciding variable ($35k/yr vs $100–250k/yr) | **traced** | C3 verbatim — GT-5 + GT-6 + GT-11?, "a spread of ~$35k/yr… roughly $100k–250k/yr of margin" |

**3. Document verdict: PARTIAL**

One load-bearing claim (the ~20%/~35% decision thresholds in step 2) asserts a quantitative result attributed to "C1's arithmetic" that C1 does not contain. All other load-bearing claims trace to a named §4 chain.

---

## Q-N3

**1. Load-bearing-claim set** (§6 "Conclusion"; excluding the `**Confidence:**` paragraph as the protocol's caveat field, and excluding the "What would change this" and "honest cost" paragraphs insofar as they are caveats — see marks below for those retained as substantive causal/decision claims):

- *"**Recommendation: Option 3 — structured deferral. Do not start the migration now; do not settle into "keep both native" either.**"*
- *"**Ship the two customer features natively, starting now.** This is the only option that keeps the renewal outside the risk window (C1, C4). Size them this week — if they are larger than 3 engineers can carry, that changes the plan (A11)."*
- *"**Run a bounded Flutter spike in parallel — 2–3 engineer-weeks, no more.** Its job is to answer GT-9?, not to impress anyone. Target the *hardest* surface: your oldest supported device class, plus whichever native integration you most fear porting. A spike that ships a pretty demo on a flagship phone has told you nothing (C3, pre-mortem item 2)."*
- *"**Set a dated checkpoint — I would put it at month 4–5 — with the decision rule written down before results arrive.** Something of the form: *"If the spike shows cold-start and frame-time within X% of native on the oldest supported device, and the two features have shipped, we commit to migration starting month 10."* Pre-registering the rule is what stops the deferral from silently becoming permanent (C5, pre-mortem item 1)."*
- *"**Verify this week whether the renewal decision actually commits at month 9 or earlier** (GT-8?). It is one conversation, and it is the load-bearing input to C1."*
- *"**The honest cost of my recommendation:** Option 3 is not free. Every month both codebases stay alive, you pay duplicated feature cost, and each native feature you ship enlarges the eventual migration (C5, A7). What you are buying with that money is the conversion of a 35-engineer-month bet on an unmeasured premise into a 3-engineer-week measurement — and, if the renewal lands, a clean 12-month window with no dated external constraint, which is structurally the best migration conditions you are likely to see."*
- *"**Flutter may well be the right destination.** In the trade-off it scores highest of all options on long-run cost efficiency, and nothing in this analysis argues against it as a technology. The argument is entirely about *when* — and right now you would be starting the largest engineering commitment in your recent history seven months before a nine-month deadline, on a performance premise you have never tested against a third of your users."*

*Excluded under Rule 1:* the "**Confidence: MEDIUM-HIGH**" paragraph (confidence/caveat field) and the "**What would change this**" paragraph (a caveat on the recommendation's conditions, not a claim the conclusion rests on).

**2. Traced / untraced marks:**

| Claim | Mark | §4 support |
|---|---|---|
| Option 3 structured deferral; don't migrate now, don't settle into keep-both-native | **traced** | C4 trade-off — "Option 3 (108) > Option 2 (92) > Option 1 (45)"; C1 (schedule collision); C2 (bracket straddles the 9-month renewal) |
| Ship two features natively now — only option keeping renewal outside the risk window | **traced** | C1 (`GT-3 + GT-5? + GT-8?` → renewal commits months 5–7, inside the stall) and C4 (renewal-protection scores: Opt 1 = 1, Opt 3 = 5); A11 flagged in the table and in C4's `[Assumes: A11, A13]` |
| Bounded Flutter spike, 2–3 engineer-weeks, target the hardest surface | **traced** | C3 — "you would be spending your largest engineering investment in years on an untested premise, when the test costs perhaps 2–3 engineer-weeks"; GT-4 + GT-7 + GT-9? |
| Dated checkpoint at month 4–5 with a pre-registered decision rule | **traced** | C5 →[3rd] — "an *undated* deferral silently converts into Option 2 by default. This is why the checkpoint must carry a date and a pre-registered decision rule, not a review meeting." (The specific month 4–5 figure is stated as the author's own placement, not derived; the rule itself is chained.) |
| Verify the renewal decision date this week; load-bearing input to C1 | **traced** | C1's confidence note — "capped by GT-8?… verifying GT-8? is the single highest-value hour of work available to you this week"; GT-8? |
| Deferral is not free — duplicated cost, re-port scope growth, 35 engineer-months → 3 engineer-weeks | **traced** | C5 →[2nd] ("Both codebases keep accruing duplicated feature cost during the deferral. **Adverse — this is the real price of Option 3**" `[Assumes: A7]`; re-port scope `[Assumes: A12]`); C2 (35 engineer-months); C3 (2–3 engineer-weeks); C5 →[3rd] (clean 12-month runway) |
| Flutter may be the right destination; scores highest on long-run cost efficiency | **traced** | C4 table — Opt 1 scores 5 on "Long-run cost efficiency," highest of the three |

**3. Document verdict: TRACED**

Every load-bearing claim traces to a named §4 chain or ground truth in the same document. (The one non-derived numeric — "month 4–5" — is presented explicitly as the author's recommendation of where to put the checkpoint rather than as a derived quantitative result, and the checkpoint-must-be-dated claim it sits inside is chained to C5.)

---

## Q-N4

**1. Load-bearing-claim set** (§6 "Conclusion"; excluding the `**Confidence:**` field):

- *"**Use the 3PL. Do not build the warehouse. Do not split 50/50.**"*
- *"**The decisive number:** the warehouse breaks even against $3.10/order at roughly **8,000 west-coast orders per week**. You have **1,575**. You would need to grow west-coast volume ~5× — to nearly double your entire current company throughput — before the build pays for itself, and you would be committing $1.26M of lease plus 8 jobs for three years to a growth rate you have not quantified (A-2)."*
- *"**The gap is not close.** In-house runs ≈$1.0M/yr [$880k–$1.13M] against ≈$254k for the 3PL — about **$9.10 per order** you would be paying for control. Modelled worst-case control damage (a 5-point return-rate deterioration) is ≈$82k/yr, roughly one-ninth of that premium. Even under the most warehouse-favourable reading of your figures (if $420k already includes the 8 hires), the ranking does not flip."*
- *"**The split is the worst of the three.** Half the volume through a facility carrying full fixed cost pushes in-house unit cost *up*, to ≈$14.55/order, while still not giving you the end-to-end control the build was supposed to buy."*
- *"**Verify A-9 before anything else.** Get a fully-burdened 3PL quote — receiving, storage, accessorials, returns processing, peak surcharges. $3.10 is conventionally a pick-pack rate. If the landed rate is materially higher, re-run C3; the decision would still favour the 3PL, but the margin matters for term negotiation."*
- *"**Buy optionality, not the lowest rate.** Negotiate a **2-year term (not 3+)**, volume-tiered pricing with a step-down, contractual 2-day SLA with penalties, a defined packaging specification with audit rights, returns-data ownership, and a clean exit/transition clause. The second-order analysis says your leverage is highest now and decays with every month of dependence."*
- *"**Pre-register the revisit trigger.** Re-open the build decision when west-coast volume sustains **≥6,000 orders/week** for two consecutive quarters, or if audited 3PL packaging/returns quality breaches the SLA. Write the number down now, before you have a result you want to justify."*
- *"**Test the option this analysis rejected as a false binary (A-15).** A 50/50 split is dominated — but an *asymmetric* hybrid is not the same thing: 3PL for standard volume, with a control-critical segment (subscription boxes, high-AOV, custom packaging) retained in your existing facility and shipped west at higher transit cost. That requires no second lease and no 8 hires. Whether it's worth it depends on whether such a segment actually exists in your order mix — which is a data question you can answer this week."*

**2. Traced / untraced marks:**

| Claim | Mark | §4 support |
|---|---|---|
| Use the 3PL; don't build; don't split | **traced** | C1 + C2 (cost comparison), C3 (breakeven), C4 (split dominated), C5 (control gap) |
| Breakeven ~8,000 WC orders/week; 1,575 today; ~5×; $1.26M + 8 jobs against an unquantified growth rate | **traced** | C3 — "V ≈ 416,000 orders/yr ≈ 8,000 WC orders/week → breakeven requires ~5× current west-coast volume"; GT-1 (81,900/yr, 1,575/wk), GT-3 ($1.26M committed), GT-4 (8 hires); C3 →[2nd] cites A-2 explicitly |
| Gap not close: ≈$1.0M/yr [$880k–$1.13M] vs ≈$254k; $9.10/order; $82k/yr ≈ one-ninth; ranking doesn't flip under the A-4-false reading | **traced** | C2 (≈$1.0M/yr bracket, $9.10/order control premium, and the explicit "if A-4 is false and $420k is all-in, in-house is still $420k vs $254k — same direction"); C1 ($254k); C5 (≈$82k/yr, "~9× smaller than the $746k cost gap") |
| Split is worst; ≈$14.55/order | **traced** | C4 verbatim — "in-house cost/order rises to ≈$14.55 … dominated on cost by the pure 3PL option and dominated on control by the pure build option" |
| Verify A-9 first; re-run C3 if landed rate higher; decision would still favour 3PL | **traced** | A-9 in §2 ("**Likely FALSE as stated**"); C1's confidence note ("MEDIUM on scope — depends on A-9"); C2's bracket argument establishes the direction is robust ("both ends drive the same decision") |
| Buy optionality: 2-year term, tiered pricing, SLA penalties, packaging spec + audit rights, data ownership, exit clause; leverage highest now | **traced** | C1 →[2nd] and →[3rd] — "Dependence on a single provider grows with tenure; renewal leverage shifts to them"; "Switching cost … rises each year → mitigate now via term length, exit clause, and data-ownership terms, not later"; C5 →[2nd] (packaging spec, mystery-shop audits, SLA penalties); GT-10 |
| Pre-register the revisit trigger at **≥6,000 orders/week** for two consecutive quarters | **untraced (quantitative part)** | The *existence* of a revisit threshold is supported by C3 (breakeven ≈8,000/wk) and GT-9. But no §4 chain derives 6,000/week or the two-consecutive-quarters rule. C3's own sensitivity note gives 8,000/wk central and "~5,900/wk" only at the *optimistic* 150/day end — the conclusion does not tie 6,000 to that branch, and the closure ledger contains no entry for this claim at all. |
| Test the asymmetric hybrid (A-15 rejection); no second lease, no 8 hires | **traced** | C4 (`[Assumes: A-12 — no proportionally smaller facility available]`, establishing the split's dominance is conditional on facility granularity) plus A-15's rejection in §2; the closure ledger names "chain C4 + A-15 rejection" |

**3. Document verdict: PARTIAL**

The 6,000-orders/week revisit trigger is a quantitative result the conclusion rests on (it is the pre-registered decision rule) with no derivation in §4 and no entry in the document's own closure ledger; every other load-bearing claim traces.

---

## Q-N6

**1. Load-bearing-claim set** (§6 "Conclusion"; the `<details>` closure-ledger/rubric block is process output, not conclusion claims):

- *"**Do not buy yet, and do not walk away. Spend 30–60 days and a few hundred dollars closing the two unknowns that the whole decision rests on** *(chain C6)*."*
- *"**Audit your last 75–100 referrals** (three to four months) and tag each with the *actual* reason it left the building: no machine · specialist interpretation needed · surgical co-treatment · insurance steering · patient preference. Only the first category converts. **Your break-even is 15–18 scans/month — 60–72% capture** *(chain C1)*. If the audit shows you'd retain 20+, buy without further deliberation. If it shows 12 or fewer, the machine loses money over its entire life and the answer is a clean no. Between 15 and 18, it is a coin flip on financial grounds and you should decide on clinical and strategic grounds instead."*
- *"**Get a healthcare attorney's read on the neighbor arrangement before it influences the purchase.** It is the most legally exposed element here, not the safest first step, and it is currently doing load-bearing work in a $110,000 decision on the strength of a verbal offer *(chains C3, C4)*. Structure it as a fair-market-value technical fee fixed in advance and independent of volume, or not at all."*
- *"**Settle the overread question in the same window.** Whether a dentist reads the full field of view or you pay a radiologist per scan is what moves your per-scan contribution between $100 and $180 — the second-largest lever in the model, and one you control by choosing *(chain C5)*."*
- *"Two things the model deliberately does not count, both of which favor buying: incremental case acceptance on implant and endodontic treatment made possible by same-day 3D imaging, and the patients you stop losing to specialists who retain them. If your referral audit lands near break-even, these are the reasons to lean yes. Against them, weigh the reciprocity loss from specialists you stop feeding *(chain C5)* — a decline of two to three restorative cases a month can quietly exceed the entire scan contribution."*
- *"**The single sentence:** your decision hinges on one number you have never measured, that number is cheap to measure, and the machine will still be for sale in sixty days."*

**2. Traced / untraced marks:**

| Claim | Mark | §4 support |
|---|---|---|
| Don't buy yet, don't walk away; spend 30–60 days closing the two unknowns | **traced** | C6 — "C1 (bracket straddles the threshold) + C3 (key input unenforceable) + C4 (legal structure unresolved) → the two decisive unknowns are both cheap to resolve and expensive to be wrong about → measuring first strictly dominates → Option 3." Trade-off table: Opt 3 = 108 vs 85 / 78. |
| Audit last 75–100 referrals; only "no machine" converts | **traced** | A3 (referrals leave for interpretation, insurance steering, surgical co-treatment — "Only the first category converts" restates A3's verification note) and the **Fishbone pass** in §2 ("Only the *Technology* branch is fixed by buying a machine. This is the direct source of A3's doubt"). Note: the fishbone/A3 support sits in §2, not §4; C1's stop-criterion escalation ("tighten that factor with a measurement before deciding") is the §4 anchor for *doing the audit*. |
| Break-even 15–18 scans/month = 60–72% capture | **traced** | C1 verbatim — "break-even ≈ 15–18 scans/month → you must retain 60–72% of your existing 25 monthly referrals just to reach zero" |
| Retain 20+ → buy; 12 or fewer → loses money over its entire life; 15–18 → coin flip | **traced** | C1's bracket table — Conservative 12/mo → **−$600** annual net, "Payback: never"; Aggressive 25/mo → +$45,000, 2.4 yr payback; the 15–18 band is the break-even band C1 derives. (The 20+ cut is between C1's Central 18/mo (+$21,240) and Aggressive 25/mo rows.) |
| Attorney read before the offer influences the purchase; most legally exposed element; FMV fixed fee or not at all | **traced** | C4 — "the exact fact pattern federal referral law scrutinizes → 'explore the shared-referral arrangement' is not a low-commitment first step; it is the step requiring counsel before any money moves"; and C4's compliant-structure note ("fair-market-value per-scan technical fees set in advance, not varying with volume or value of referrals"); C3 (verbal offer doing load-bearing work in a $110,000 decision); GT-9? |
| Overread question moves contribution $100–$180; second-largest lever | **traced** | C5 →3a — "either a dentist reads regions outside their training (liability) or you pay $25–60/scan for radiologist overread (**this is what reduces GT-3? from $180 to ~$140 — the effect feeds directly back into C1's dominant term**)"; GT-3? bracket $100–$180 |
| Two uncounted upsides favor buying: incremental case acceptance on implant/endo from same-day 3D imaging, and patients you stop losing to specialists | **untraced** | No §4 chain and no ground truth addresses incremental case acceptance or patient retention from same-day imaging. C1–C6 model only capture rate × contribution against fixed cost; §3 has no GT on case acceptance or patient loss to specialists. The document's own closure ledger contains no entry for this claim. It is presented as a reason to "lean yes" at the decision boundary, so the conclusion rests on it. |
| Reciprocity loss: 2–3 restorative cases/month can exceed the entire scan contribution | **traced** | C5 →1a — "a reciprocity loss of even 2–3 restorative or surgical cases per month can exceed $2,000/mo in production, dwarfing the ~$1,700/mo net scan contribution"; A10 |
| The single sentence: decision hinges on one unmeasured, cheap-to-measure number | **traced** | C1's stop-criterion FAILED result ("The dominant uncertain factor is capture rate (A3)… escalates: tighten that factor with a measurement before deciding") and C6 |

**3. Document verdict: PARTIAL**

One load-bearing claim — the two uncounted buy-favoring factors (incremental case acceptance from same-day 3D imaging, and patients retained rather than lost to specialists), offered as the tiebreaker when the audit lands near break-even — has no supporting §4 chain or §3 ground truth in the document, and is absent from its own closure ledger. All other load-bearing claims trace.
