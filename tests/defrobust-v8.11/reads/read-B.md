I'll apply the pre-registered D-03 rule to each document.

---

# Q-N2

## 1. Load-bearing-claim set

Under Rule (1), §6's load-bearing claims (recommendations, decisions, quantitative results, causal assertions the conclusion rests on), at paragraph/bullet granularity:

**LB-1** — "**Do none of the three things as posed. Stage it.**"

**LB-2** — "**The 35kg roaster is sized to demand you do not have yet (C1).** At 20% annual growth it takes about 4.6 years to fill. You would be paying $103,000 today for headroom that sits idle for roughly three of those years, while the two accounts underwriting the growth can leave with thirty days' notice."

**LB-3** — "**Do not adopt a permanent double shift as the end state either (C5).** It doubles duty cycle on a single machine with zero redundancy — raising outage probability exactly when your commitments peak. It is a fine bridge and a poor destination."

**LB-4** — "**Do not hold off (C2, C3).** Capacity binds now, the machine has roughly 4.7x physical headroom that only a staffing convention is blocking, and the margin you are turning away likely exceeds the cost of either fix by an order of magnitude."

**LB-5** — "**Now — add a partial second shift**, not a full one. A four-to-five-hour evening turn at roughly $2,100–2,500/mo buys most of the capacity at half the cost and half the wear, and it is cancellable at thirty days (C2, C4, C7). This is the bridge across the equipment lead time, which you will need regardless of what you eventually buy."

**LB-6** — "**Within 30 days — get the one number that decides this.** What percentage of volume do those two accounts represent? Rough thresholds from C1's arithmetic: if their combined share is **under ~20%**, growth alone keeps you capacity-bound through their loss and you should buy. If it is **over ~35%**, losing them returns you to slack capacity and you should not commit capital until the account base is broader."

**LB-7** — "**Within 60–90 days — convert the terms.** Offer locked pricing, priority peak allocation, or a volume rebate in exchange for a six-to-twelve-month commitment or a monthly volume floor. Do not make a bare ask: it invites them to shop (A-17, C7 second-order). A signed floor is also financeable collateral that improves your eventual loan terms."

**LB-8** — "**Then buy — but price a twin, not the 35kg (C6).** A second 15–25kg machine gives you the same ~2x capacity, full redundancy against the failure mode that scares me most, identical roast profiles with no re-development risk to your flagship blends, and roughly half the capital outlay. Get that quote before you sign anything for the 35kg."

**LB-9** — "**Pre-register the trigger now, while you are calm.** Write it down: *"We order when (a) contracted or floor-committed volume covers X kg/week, or (b) the two at-risk accounts fall below Y% of volume, whichever comes first."* Deciding the rule before the data arrives is what stops a good month from being mistaken for a trend."

**LB-10** — "**Cost is not the deciding variable here (C3).** The $35k/yr spread between your two original options is a rounding error against the ~$100–250k/yr of margin that hinges on whether the demand is durable. Spend the next ninety days buying information about that, not equipment."

*Excluded under Rule (1):* the "**What to do, in order:**" line (section-intro label); the §6 opening line is retained as LB-1 because it is itself the decision, not a label; the Phase 5 "Overall confidence: MEDIUM-HIGH…" line (confidence/caveat field).

## 2. Traced / untraced marks

- **LB-1 — traced.** §4 C7 ("bridge with a partial second shift now; resolve account terms within 60–90 days; then buy a right-sized second machine on a pre-registered trigger"), supported by C1 and C4.
- **LB-2 — traced.** §4 C1: "a 35kg run as primary lifts capacity ~2.3x, while 20%/yr compounding needs `ln(2.3) ÷ ln(1.2) ≈ 4.6 years` to consume it → the $103,000 asset runs below 50% utilisation for roughly its first three years." Thirty-days' notice rests on GT-8.
- **LB-3 — traced.** §4 C5: "doubling duty cycle on a single machine roughly halves calendar time to major service while leaving zero redundancy → … the second shift is defensible as a bridge and indefensible as an end state," on GT-14 + GT-15?.
- **LB-4 — traced.** §4 C2 (theoretical-limit sub-step: "Gap: ~4.7x"; "one shift is a staffing convention, not a machine limit") + C3 ("unmet demand at ~1,000 incremental kg/wk × $6–10/kg contribution is roughly $100k–250k/yr of margin"), with GT-9.
- **LB-5 — traced.** §4 C2 (shift delivers ~2x, machine sustains 2–2.5 shifts), C4 (thirty-day cancellability from GT-13 + A-13), C7 (bridge across the 3–6 month lead time, GT-12?). The specific $2,100–2,500/mo figure is a pro-rata halving of GT-6's $4,200/mo, arithmetically derivable but not itself stated in a §4 chain — it does not carry the claim, which is the partial-shift recommendation.
- **LB-6 — traced.** §4 C1's arithmetic (2.33x headroom vs. `ln(1.2)` growth) plus GT-16? explicitly named as the unknown; §3 GT-16? and A-4 ("direction-changing").
- **LB-7 — traced.** §4 C7's chain (resolve account terms within 60–90 days) and C7 →[2nd] ("The term-conversion ask may itself prompt an account to re-evaluate and shop the market. `[Assumes: A-17]` — mitigate by pairing the ask with something they want: locked pricing, priority allocation during peak, or a volume rebate") and →[3rd] ("A successful term conversion becomes financeable evidence, improving equipment-loan terms").
- **LB-8 — traced.** §4 C6: "a second machine matched to your current batch size delivers the same ~2x as the shift, adds full redundancy, preserves existing profiles … and costs roughly half of $103,000," with GT-3 and the C6 trade-off matrix (E = 105 > A = 95).
- **LB-9 — traced.** §4 C7's terminal step ("then buy a right-sized second machine on a pre-registered trigger") and C4's time-bounding ("rational for exactly as long as the account-terms uncertainty is live").
- **LB-10 — traced.** §4 C3: "the cost difference between the two options is a fraction of the margin at stake, so the decision should be optimised for demand durability and supply reliability, not for lowest cost," from GT-5 + GT-6 + GT-11?.

## 3. Document verdict

**TRACED**

---

# Q-N3

## 1. Load-bearing-claim set

**LB-1** — "**Recommendation: Option 3 — structured deferral. Do not start the migration now; do not settle into "keep both native" either.**"

**LB-2** — "**Ship the two customer features natively, starting now.** This is the only option that keeps the renewal outside the risk window (C1, C4). Size them this week — if they are larger than 3 engineers can carry, that changes the plan (A11)."

**LB-3** — "**Run a bounded Flutter spike in parallel — 2–3 engineer-weeks, no more.** Its job is to answer GT-9?, not to impress anyone. Target the *hardest* surface: your oldest supported device class, plus whichever native integration you most fear porting. A spike that ships a pretty demo on a flagship phone has told you nothing (C3, pre-mortem item 2)."

**LB-4** — "**Set a dated checkpoint — I would put it at month 4–5 — with the decision rule written down before results arrive.** Something of the form: *"If the spike shows cold-start and frame-time within X% of native on the oldest supported device, and the two features have shipped, we commit to migration starting month 10."* Pre-registering the rule is what stops the deferral from silently becoming permanent (C5, pre-mortem item 1)."

**LB-5** — "**Verify this week whether the renewal decision actually commits at month 9 or earlier** (GT-8?). It is one conversation, and it is the load-bearing input to C1."

**LB-6** — "**What would change this.** If you verify that (a) the renewal decision truly lands at month 9 with no earlier evaluation, **and** (b) the two features are not renewal conditions, **and** (c) the customer is a modest revenue share — then C1 largely dissolves and consolidating now becomes defensible. All three would have to hold. Conversely, if the customer is a large revenue share and the features are conditions, Option 3 stops being merely preferable and becomes the only responsible choice."

**LB-7** — "**The honest cost of my recommendation:** Option 3 is not free. Every month both codebases stay alive, you pay duplicated feature cost, and each native feature you ship enlarges the eventual migration (C5, A7). What you are buying with that money is the conversion of a 35-engineer-month bet on an unmeasured premise into a 3-engineer-week measurement — and, if the renewal lands, a clean 12-month window with no dated external constraint, which is structurally the best migration conditions you are likely to see."

**LB-8** — "**Flutter may well be the right destination.** In the trade-off it scores highest of all options on long-run cost efficiency, and nothing in this analysis argues against it as a technology. The argument is entirely about *when* — and right now you would be starting the largest engineering commitment in your recent history seven months before a nine-month deadline, on a performance premise you have never tested against a third of your users."

*Excluded under Rule (1):* "Concretely, for the next 9 months:" (section-intro label); "**Confidence: MEDIUM-HIGH.** The recommendation *against consolidating now* is the robust part…" (the `**Confidence:**` / caveat field).

## 2. Traced / untraced marks

- **LB-1 — traced.** §4 C4 trade-off: "Option 3 (108) > Option 2 (92) > Option 1 (45)"; C1 (schedule collision) supplies the "not now."
- **LB-2 — traced.** §4 C1 (renewal commits months 5–7, inside the stall) + C4 (Option 3 scores 5 on renewal protection). The A11 sizing caveat is itself in the §2 table and audited in C4 step 1.
- **LB-3 — traced.** §4 C3: "the consolidation's viability depends on an unmeasured quantity → committing 35+ engineer-months before measuring it inverts the normal order of risk retirement… when the test costs perhaps 2–3 engineer-weeks," plus C4's A13 assumption ("only if the spike targets the riskiest surface").
- **LB-4 — traced.** §4 C5 →[3rd]: "an *undated* deferral silently converts into Option 2 by default. This is why the checkpoint must carry a date and a pre-registered decision rule, not a review meeting."
- **LB-5 — traced.** §4 C1 and its confidence note: "verifying GT-8? is the single highest-value hour of work available to you this week."
- **LB-6 — traced.** §4 C1 (the chain is explicitly capped by GT-8?, GT-5?) and the §2/§3 entries GT-10?/A4 and GT-5?/A10. The conditional structure is the negation of C1's own stated dependencies.
- **LB-7 — traced.** §4 C5 →[2nd] ("Both codebases keep accruing duplicated feature cost during the deferral. **Adverse — this is the real price of Option 3**") and →[3rd] ("a clean 12-month runway with no dated external constraint — structurally the best migration window you will get"); the 35-engineer-month figure from C2, the 3-engineer-week figure from C3.
- **LB-8 — traced.** §4 C4's matrix row "Long-run cost efficiency | 3 | 5 | 2 | 3" — Option 1 scores highest (5) on that criterion, exactly as claimed; the "third of your users" premise from GT-4 + GT-9? via C3.

## 3. Document verdict

**TRACED**

---

# Q-N4

## 1. Load-bearing-claim set

**LB-1** — "**Use the 3PL. Do not build the warehouse. Do not split 50/50.**"

**LB-2** — "**The decisive number:** the warehouse breaks even against $3.10/order at roughly **8,000 west-coast orders per week**. You have **1,575**. You would need to grow west-coast volume ~5× — to nearly double your entire current company throughput — before the build pays for itself, and you would be committing $1.26M of lease plus 8 jobs for three years to a growth rate you have not quantified (A-2)."

**LB-3** — "**The gap is not close.** In-house runs ≈$1.0M/yr [$880k–$1.13M] against ≈$254k for the 3PL — about **$9.10 per order** you would be paying for control. Modelled worst-case control damage (a 5-point return-rate deterioration) is ≈$82k/yr, roughly one-ninth of that premium. Even under the most warehouse-favourable reading of your figures (if $420k already includes the 8 hires), the ranking does not flip."

**LB-4** — "**The split is the worst of the three.** Half the volume through a facility carrying full fixed cost pushes in-house unit cost *up*, to ≈$14.55/order, while still not giving you the end-to-end control the build was supposed to buy."

**LB-5** — "**Verify A-9 before anything else.** Get a fully-burdened 3PL quote — receiving, storage, accessorials, returns processing, peak surcharges. $3.10 is conventionally a pick-pack rate. If the landed rate is materially higher, re-run C3; the decision would still favour the 3PL, but the margin matters for term negotiation."

**LB-6** — "**Buy optionality, not the lowest rate.** Negotiate a **2-year term (not 3+)**, volume-tiered pricing with a step-down, contractual 2-day SLA with penalties, a defined packaging specification with audit rights, returns-data ownership, and a clean exit/transition clause. The second-order analysis says your leverage is highest now and decays with every month of dependence."

**LB-7** — "**Pre-register the revisit trigger.** Re-open the build decision when west-coast volume sustains **≥6,000 orders/week** for two consecutive quarters, or if audited 3PL packaging/returns quality breaches the SLA. Write the number down now, before you have a result you want to justify."

**LB-8** — "**Test the option this analysis rejected as a false binary (A-15).** A 50/50 split is dominated — but an *asymmetric* hybrid is not the same thing: 3PL for standard volume, with a control-critical segment (subscription boxes, high-AOV, custom packaging) retained in your existing facility and shipped west at higher transit cost. That requires no second lease and no 8 hires. Whether it's worth it depends on whether such a segment actually exists in your order mix — which is a data question you can answer this week."

*Excluded under Rule (1):* "**What to do instead of just signing:**" (section-intro label); "**Confidence:** HIGH that the 3PL beats the build at current volume…" (the `**Confidence:**` / caveat field).

## 2. Traced / untraced marks

- **LB-1 — traced.** §4 C1 + C2 (cost comparison) and C4 (split dominated); mirrored in the closure ledger.
- **LB-2 — traced with a discrepancy.** §4 C3 derives "**V ≈ 416,000 orders/yr ≈ 8,000 WC orders/week** → **breakeven requires ~5× current west-coast volume**"; GT-1 supplies 1,575/wk; GT-3 supplies "$420,000/year × 3 years = $1,260,000 committed"; A-2 supplies the unquantified growth rate. Note the internal arithmetic tension: 416,000/yr ÷ 52 ≈ 8,000/wk, and 8,000 ÷ 1,575 ≈ 5.1×, so the chain is self-consistent — the claim is traced.
- **LB-3 — traced.** §4 C2 ("**≈$1.0M/yr [bracket: $880k – $1.13M]**… **in-house costs ≈$746k/yr more than the 3PL today**, i.e. a **~$9.10/order control premium**"; and its own note "If A-4 is false and $420k is all-in, in-house is still $420k vs $254k — same direction"), C1 (≈$254,000/yr), C5 (≈$82k/yr, "~9× smaller than the $746k cost gap").
- **LB-4 — traced.** §4 C4: "a 50/50 split routes ~40,950 orders/yr through a node carrying the **full** $520k fixed cost → in-house cost/order rises to **≈$14.55** … **dominated on cost by the pure 3PL option and dominated on control by the pure build option**."
- **LB-5 — traced.** §2 A-9 ("**Likely FALSE as stated**", "Demand a fully-burdened quote") and C1's confidence note ("MEDIUM on scope — depends on A-9"). The specific sub-claim "the decision would still favour the 3PL" rests on C2's bracket-end argument ("the bracket's lower bound $880k still exceeds $254k by 3.5×, so both ends drive the same decision").
- **LB-6 — traced.** §4 C1 →[2nd] ("Dependence on a single provider grows with tenure; renewal leverage shifts to them [Assumes: A-14]") and →[3rd] ("Switching cost … rises each year → mitigate now via term length, exit clause, and data-ownership terms, not later"), plus C5 →[2nd] on packaging spec/audits/SLA penalties. GT-10 supports the reversibility framing.
- **LB-7 — untraced (partially).** The pre-registration principle is supported by C3 + GT-9, and the SLA-breach trigger by C5 →[2nd]. But the specific quantitative threshold **≥6,000 orders/week** appears nowhere in §4 or §3. C3's derived breakeven is **~8,000/wk**; the only other figure in the chain is the optimistic-throughput sensitivity "at the optimistic 150/day it falls to ~5,900/wk," which is a sensitivity bound on the breakeven, not a stated revisit trigger, and 6,000 is not derived from it anywhere in the document. No §4 chain or ground truth yields 6,000/wk. The closure ledger does not list this claim at all.
- **LB-8 — traced.** §4 C4 (split dominated) and §2 A-15 ("**FALSE** — asymmetric hybrid exists"); the closure ledger records "An asymmetric hybrid may be worth testing" → chain **C4 + A-15 rejection**. Note the support is a chain plus an assumption-table rejection rather than a chain alone, but a §4 chain (C4) is cited and does support it.

## 3. Document verdict

**PARTIAL** — LB-1 through LB-6 and LB-8 are traced to §4 chains; LB-7's load-bearing quantitative threshold (≥6,000 orders/week) has no §4 derivation or §3 ground truth supporting it.

---

# Q-N6

## 1. Load-bearing-claim set

**LB-1** — "**Do not buy yet, and do not walk away. Spend 30–60 days and a few hundred dollars closing the two unknowns that the whole decision rests on** *(chain C6)*."

**LB-2** — "**Audit your last 75–100 referrals** (three to four months) and tag each with the *actual* reason it left the building: no machine · specialist interpretation needed · surgical co-treatment · insurance steering · patient preference. Only the first category converts. **Your break-even is 15–18 scans/month — 60–72% capture** *(chain C1)*. If the audit shows you'd retain 20+, buy without further deliberation. If it shows 12 or fewer, the machine loses money over its entire life and the answer is a clean no. Between 15 and 18, it is a coin flip on financial grounds and you should decide on clinical and strategic grounds instead."

**LB-3** — "**Get a healthcare attorney's read on the neighbor arrangement before it influences the purchase.** It is the most legally exposed element here, not the safest first step, and it is currently doing load-bearing work in a $110,000 decision on the strength of a verbal offer *(chains C3, C4)*. Structure it as a fair-market-value technical fee fixed in advance and independent of volume, or not at all."

**LB-4** — "**Settle the overread question in the same window.** Whether a dentist reads the full field of view or you pay a radiologist per scan is what moves your per-scan contribution between $100 and $180 — the second-largest lever in the model, and one you control by choosing *(chain C5)*."

**LB-5** — "Two things the model deliberately does not count, both of which favor buying: incremental case acceptance on implant and endodontic treatment made possible by same-day 3D imaging, and the patients you stop losing to specialists who retain them. If your referral audit lands near break-even, these are the reasons to lean yes. Against them, weigh the reciprocity loss from specialists you stop feeding *(chain C5)* — a decline of two to three restorative cases a month can quietly exceed the entire scan contribution."

**LB-6** — "**The single sentence:** your decision hinges on one number you have never measured, that number is cheap to measure, and the machine will still be for sale in sixty days."

*Excluded under Rule (1):* "Concretely:" (section-intro label). §6 carries no `**Confidence:**` field (it sits in the collapsed process-output block, which also holds the closure ledger and rubric).

## 2. Traced / untraced marks

- **LB-1 — traced.** §4 C6: "**C1 (bracket straddles the threshold) + C3 (key input unenforceable) + C4 (legal structure unresolved) → the two decisive unknowns are both cheap to resolve and expensive to be wrong about → measuring first strictly dominates → Option 3**," with the weighted matrix (Opt 3 = 108 vs 85 and 78) and its sensitivity check. The 30–60 day / few-hundred-dollar figures are not themselves in a chain, but the decision they attach to is.
- **LB-2 — traced.** §4 C1: "**break-even ≈ 15–18 scans/month → you must retain 60–72% of your existing 25 monthly referrals just to reach zero**," and C1's bracket table supplying the branch thresholds (Conservative 12/mo → −$600/yr, "never" payback → the "12 or fewer … loses money over its entire life" branch; Aggressive 25/mo → +$45,000 → the "retain 20+" branch). A3 in §2 supports "only the first category converts," reinforced by the §2 fishbone pass ("Only the *Technology* branch is fixed by buying a machine").
- **LB-3 — traced.** §4 C4: "an arrangement in which one practice directs patients to another practice's revenue-generating equipment is the exact fact pattern federal referral law scrutinizes → … it is the step requiring counsel before any money moves"; and C4's remedy sentence "fair-market-value per-scan technical fees set in advance, not varying with volume or value of referrals." §4 C3 supplies "an unenforceable input is doing load-bearing work in a $110,000 decision." GT-9? underwrites the legal premise (conditional on A11, disclosed).
- **LB-4 — traced.** §4 C5 →[3rd] item 3a: "either a dentist reads regions outside their training (liability) or you pay $25–60/scan for radiologist overread (**this is what reduces GT-3? from $180 to ~$140 — the effect feeds directly back into C1's dominant term**)"; GT-3? gives the $100–$180 bracket. The ranking as "second-largest lever" is consistent with C1 naming capture rate (A3) as the dominant factor.
- **LB-5 — traced.** The reciprocity half is squarely §4 C5 →[3rd] item 1a: "a reciprocity loss of even 2–3 restorative or surgical cases per month can exceed $2,000/mo in production, dwarfing the ~$1,700/mo net scan contribution." The two "not counted" upside items (incremental case acceptance; patients retained) appear in no §4 chain and no §3 ground truth — but the document explicitly labels them as things "the model deliberately does not count," i.e. it discloses them as outside the derivation rather than asserting them as derived. Marked **traced for the load-bearing half (the reciprocity comparison, C5); the uncounted-upside half is self-declared as outside the model** and is not offered as a derived result.
- **LB-6 — traced.** §4 C1's stop-criterion failure ("**Stop-criterion result: FAILED** … The dominant uncertain factor is capture rate (A3) … this escalates: **tighten that factor with a measurement before deciding**") and C6's dominance conclusion. "Cheap to measure" is supported by C6's "both cheap to resolve and expensive to be wrong about."

## 3. Document verdict

**TRACED**
