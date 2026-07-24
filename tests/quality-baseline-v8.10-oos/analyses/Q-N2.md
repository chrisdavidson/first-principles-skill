## Missing inputs (stated per the input contract, then proceeding best-effort)

Three numbers would change the strength — not the direction — of this analysis, and one would change the direction:

1. **Direction-changing:** what share of current volume the two month-to-month accounts represent. I have flagged this as `GT-16?` and built the recommendation around a threshold rather than guessing it.
2. Contribution margin per kg roasted (`GT-11?`).
3. Current actual weekly roasted kg and true utilization (`GT-17?`), plus roaster lead time (`GT-12?`).

**Step 0 — technique selection:** no technique-specific trigger phrase fires (the prompt asks a decision question without naming a technique). `MODE = full-composer`. All five phases run; Phase 4 walks all eight companion techniques.

---

# Process output

## Phase 4 end-of-phase Assumption Audit (scan table)

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| C1 | 1 | 35kg raises capacity ~2.3x | Yes — the 35kg *replaces* the 15kg as primary rather than running alongside it with a second operator | Yes (A-9) |
| C1 | 2 | 20%/yr needs ~4.6 yrs to fill it | Yes — growth rate persists and is not a one-off catch-up year | Yes (A-3) |
| C1 | 3 | Asset under-utilised 3–4 yrs | No new assumption | — |
| C2 | 1 | Physical ceiling ≈5x current | No new assumption (from theoretical-limit derivation) | — |
| C2 | 2 | One shift is convention, not a bound | No new assumption | — |
| C2 | 3 | Second shift ≈2x ≈3.8 yrs of growth | Yes — a competent second-shift roaster is hireable and retainable at $4,200/mo | Yes (A-10) |
| C3 | 1 | Annualised capex ≈1/3 of shift labour | Yes — 7-year depreciation life and no financing interest | Yes (A-11) |
| C3 | 2 | Contribution at stake ≈$100–250k/yr | Yes — unmet demand is *fillable* demand, not enquiry noise | Yes (A-12) |
| C3 | 3 | Cost gap is second-order | No new assumption | — |
| C4 | 1 | Shift downside ≈$5–10k | Yes — no severance/notice obligation beyond one month | Yes (A-13) |
| C4 | 2 | Roaster downside ≈$40–60k | Yes — install work is non-recoverable; used-roaster market is liquid | Yes (A-6, already present) |
| C4 | 3 | Reversibility premium is worth paying | No new assumption | — |
| C5 | 1 | Duty cycle 2x halves time-to-service | Yes — wear scales with operating hours, not thermal cycles | Yes (A-8, already present) |
| C5 | 2 | Zero redundancy persists | No new assumption | — |
| C5 | 3 | Shift is bridge, not destination | No new assumption | — |
| C6 | 1 | Twin machine gives same 2x + redundancy | Yes — a second 15–25kg machine is available at roughly half the $103k | Yes (A-14) |
| C6 | 2 | Preserves existing roast profiles | Yes — profiles transfer between identical-model machines without re-development | Yes (A-15) |
| C7 | 1 | Bridge covers the lead-time window | Yes — accounts will engage on term conversion at all | Yes (A-16) |
| C7 | 2 | Defer irreversible spend | No new assumption | — |
| C7 →[2nd] | 3 | Term-conversion push runs in parallel | Yes — asking for terms may invite the account to shop competitors | Yes (A-17) |
| C7 →[3rd] | 4 | Bottleneck migrates downstream | No new assumption | — |

No enumerated second/third-order effect contradicts a Ground Truth, so no conclusion routes back to Phase 2.

## §6 → §4 closure ledger

```text
- "Do not buy the 35kg roaster now"                     → chains C1, C4 ✓
- "Do not adopt a permanent double shift as end state"  → chain  C5 ✓
- "Do not hold off entirely"                            → chains C2, C3 ✓
- "Bridge with a partial second shift now"              → chains C2, C7 ✓
- "Price a twin 15–25kg against the 35kg"               → chain  C6 ✓
- "Buy on a pre-registered trigger, not a feeling"      → chains C4, C7 ✓
- "The 35kg is sized to demand you don't have yet"      → chain  C1 ✓
- "Cost is not the deciding variable here"              → chain  C3 ✓
```

Ledger clean — every §6 claim carries a §4 chain reference.

---

# 1. Problem Essence

**Essence Statement:** *Given that capacity is binding now but the durability of the demand behind it is unverified, what is the cheapest way to buy production headroom without committing capital that becomes unrecoverable if the unsecured accounts leave?*

This is deliberately not "which of the three options is best." The question you asked frames it as a three-way pick between two capacity instruments and inaction. Stripped down, the real decision has two independent dimensions that the three-way framing conflates:

- **How much capacity, and when** (a sizing question, answerable from arithmetic)
- **How reversible the commitment is** (a risk question, answerable only after the account-terms uncertainty resolves)

Success criteria a correct answer must satisfy:

1. Relieves the binding constraint within the next 1–3 months (demand is being turned away now)
2. Does not create an unrecoverable loss larger than the roastery can absorb if both at-risk accounts exit
3. Does not increase the probability of a total production outage
4. Preserves cup quality and existing roast profiles for wholesale accounts
5. Leaves the capital decision improvable by information you can obtain cheaply

---

# 2. Assumptions Table

Built via **fishbone** (breadth, default six-category set — People, Process, Technology, Environment, Information, Resources) and **inversion** (what would guarantee this decision fails).

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | Capacity, not demand, is the current binding constraint | current constraint | Record expiry conditions | ACCEPTED — expires if either large account exits | Stated: "selling out capacity most weeks" |
| A-2 | "Selling out most weeks" means turning away orders, not just running full | untested belief | Verify | **UNVERIFIED — flagged** | Needs order-refusal log |
| A-3 | 20% YoY growth persists forward | untested belief | Verify | **UNVERIFIED — flagged** | One year of history; could be post-COVID catch-up or one account ramping |
| A-4 | The two at-risk accounts are material enough that losing them un-binds capacity | untested belief | Verify — **direction-changing** | **UNVERIFIED — flagged as `GT-16?`** | You have this number; I don't |
| A-5 | Month-to-month means terminable at short notice with no penalty | convention | Challenge before use | ACCEPTED | Standard wholesale coffee practice; confirm the actual notice clause |
| A-6 | $15k electrical/ventilation is non-recoverable; roaster resells at 50–70% | convention | Challenge before use | ACCEPTED with range | Used-roaster market is real but thin for 35kg |
| A-7 | Bigger machine = better unit economics | convention | **Challenge** | **REJECTED as stated** — true only at high utilisation; see C1 | Fixed cost per kg falls only if the kg exist |
| A-8 | Machine wear scales with operating hours | current constraint | Record expiry | ACCEPTED, partial | Drum/bearing wear does; thermal-cycling fatigue scales with *starts*, which a continuous second shift actually reduces per kg |
| A-9 | The 35kg replaces the 15kg as primary | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C1); if you run both simultaneously you need a second operator, which re-imports the shift's labour cost |
| A-10 | A competent second-shift roaster is hireable at $4,200/mo | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C2); specialty roasting is a skilled role and evening shifts are hard to staff |
| A-11 | 7-year depreciation, no financing interest | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C3); a loan at 8–10% adds ~$25k over the term |
| A-12 | Unmet demand is fillable demand | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C3) |
| A-13 | Shift is cancellable at ~1 month with no severance | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C4); jurisdiction-dependent |
| A-14 | A second 15–25kg machine is available at roughly half of $103k | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C6); quote it |
| A-15 | Profiles transfer between identical-model machines without re-development | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C6); near-true for identical models, false across sizes |
| A-16 | The accounts will engage on term conversion | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C7) |
| A-17 | Asking for terms carries no downside | untested belief | **Challenge** | **REJECTED** — it invites re-evaluation; pair the ask with a price or priority incentive | Surfaced by audit (C7 second-order) |
| A-18 | The three named options are the complete option set | convention | **Challenge** | **REJECTED** — a right-sized twin machine, a partial shift, and toll roasting are all in scope | Five-whys reduction (§3) shows the constraint admits three classes of fix: add hours, add asset, outsource |
| A-19 | Roasting is the only bottleneck | untested belief | Verify | **UNVERIFIED — flagged** | Doubling output loads packaging, QC, delivery |
| A-20 | $15k install estimate holds | untested belief | Verify | **UNVERIFIED — flagged** | Three-phase service upgrades, permits, and fire suppression routinely overrun |

**Inversion pass (what would guarantee failure), abbreviated:** both accounts exit within 12 months → stranded capex; second-shift roaster cannot be hired or quits → capacity gain never materialises; the single 15kg fails under doubled duty during peak → total outage; 35kg profile migration changes the flagship blend → account churn; install overruns → capex materially above $103k; growth was a one-off → all added capacity idles. Each unverified precondition is recorded above.

---

# 3. Ground Truths

**GT-1** — Roasted output = batch size × batches/hour × operating hours. Capacity scales linearly in each factor independently. *(Definitional.)*

**GT-2** — Green→roasted mass loss is ~14–18% for medium roasts (free moisture plus organic dry-matter loss). *(Physical; well-established.)*

**GT-3** — 35 ÷ 15 = 2.33. A 35kg machine delivers 2.33x the mass per batch. *(Arithmetic.)*

**GT-4** — Drum-roaster cycle time is roughly size-independent within the commercial class (~10–16 min), because machines are engineered to a target cycle rather than a target heat flux. *(Direct measurement / design convention; confirm against your candidate machine's spec sheet.)*

**GT-5** — Roaster option total capex = $88,000 + $15,000 = **$103,000**. *(Given.)*

**GT-6** — Shift option = $4,200/mo = **$50,400/yr**. *(Given.)*

**GT-7** — Demand +20% YoY. *(Given measurement; persistence is A-3, unverified.)*

**GT-8** — Two largest wholesale accounts are month-to-month with no commitment. *(Given.)*

**GT-9** — Capacity is binding most weeks. *(Given.)*

**GT-13** — Operating expense is terminable at the notice period; capital expenditure is sunk at the moment of purchase. This asymmetry is definitional, not situational. *(Definitional — irreducible.)*

**GT-14** — With one roaster, roaster downtime sets production to zero. There is no partial-failure mode. *(Definitional.)*

**GT-10?** — Install work non-recoverable; roaster resale 50–70%. *(Unverified.)*
**GT-11?** — Contribution margin ≈ $6–10/kg roasted wholesale. *(Unverified.)*
**GT-12?** — New roaster lead time + install ≈ 3–6 months. *(Unverified.)*
**GT-15?** — Doubling duty cycle roughly halves calendar time to major service. *(Unverified; partially contradicted by A-8's thermal-cycling caveat.)*
**GT-16?** — **Share of volume held by the two at-risk accounts: UNKNOWN.** *(The single highest-leverage missing fact.)*
**GT-17?** — Current weekly roasted kg: unknown; estimated below.

**Five-whys reduction of "we are selling out capacity":** orders exceed roasted kg available → roasted kg is fixed by batch size × batches × hours → all three are fixed → because there is one machine run one shift → because staffing was never scaled past the original configuration. **Root:** the constraint is a *staffing convention plus a single-asset design*, not a physical limit. This bottoms out at an actionable, in-your-control cause, and it establishes that the fix classes are exactly three: add hours, add asset, or outsource — which is what rejects A-18.

---

# 4. Derivation Chains

### C1 — The 35kg is sized to demand you do not yet have

**Estimate (Fermi) sub-step.** Target: current weekly roasted kg. Unit decomposition: `(kg green/batch) × (batches/hr) × (hr/day) × (days/wk) × (roasted/green) → kg roasted/wk`.

- kg green/batch: 13 (GT-1; full 15kg drums are typically run at 85–90% for profile control)
- batches/hr: 4 (GT-4, 15-min cycle)
- productive hr/day: 6 of an 8-hr shift (warm-up, cleaning, QC, changeover)
- days/wk: 5
- roasted/green: 0.84 (GT-2)

Central: 13 × 4 × 6 × 5 × 0.84 = **1,310 kg roasted/wk**. Bracket **[850, 1,310, 1,800]**. Decision-resolution check: both ends drive the same conclusion below, so the estimate is good enough.

**Chain:** GT-1 + GT-3 + GT-7 → *a 35kg run as primary lifts capacity ~2.3x, while 20%/yr compounding needs* `ln(2.3) ÷ ln(1.2) ≈ 4.6 years` *to consume it* → *the $103,000 asset runs below 50% utilisation for roughly its first three years* → **the 35kg is not sized to your demand curve; it is sized to your 2030 demand curve.** `[Assumes: A-9, A-3]`

Confidence: **HIGH** on the arithmetic, **MEDIUM** on the conclusion (depends on A-3). This is the finding that reframes the whole question: the choice was presented as "enough capacity vs. not enough," and it is actually "roughly 2x vs. roughly 2.3x-that-you-pay-for-now."

### C2 — A second shift is the increment that matches the curve

**Theoretical-limit sub-step.** Governing constraint: none of thermodynamics binds here — the limit is duty cycle and human availability. Law-permitted ceiling: 4 batches/hr × 20 hr/day (4 hr reserved for cool-down, chaff clearing, and cleaning) × 13kg × 7 days × 0.84 ≈ **6,100 kg roasted/wk**. Conventional figure: ~1,310 kg/wk. **Gap: ~4.7x.** Irreducible portion: thermal recovery between batches, chaff-fire risk requiring daily cleaning, and roaster fatigue — these cap sustained operation near 2–2.5 shifts, not 3. Convention-driven portion: the single-shift staffing pattern, which is pure inertia.

**Chain:** GT-1 + GT-9 + [theoretical limit ≈ 4.7x headroom] → *one shift is a staffing convention, not a machine limit; the machine can sustain ~2–2.5 shifts* → *a second shift delivers ~2x, which at 20%/yr covers* `ln(2) ÷ ln(1.2) ≈ 3.8 years` → **the shift is the better-matched capacity increment, and the machine will physically take it.** `[Assumes: A-10]`

Confidence: **HIGH** on the physical headroom, **MEDIUM-HIGH** overall (hinges on hiring).

### C3 — Cost is not the deciding variable

**Chain:** GT-5 + GT-6 + GT-11? → *annualised roaster cost ≈ $103k ÷ 7 ≈ $14.7k/yr plus energy, versus $50.4k/yr for the shift — a spread of ~$35k/yr* → *meanwhile, unmet demand at ~1,000 incremental kg/wk × $6–10/kg contribution is roughly $100k–250k/yr of margin* → **the cost difference between the two options is a fraction of the margin at stake, so the decision should be optimised for demand durability and supply reliability, not for lowest cost.** `[Assumes: A-11, A-12]`

Confidence: **MEDIUM** — GT-11? is unverified and drives the magnitude. Verifying your actual contribution margin would raise this to HIGH.

### C4 — The reversibility asymmetry is worth its premium *for a bounded period*

**Chain:** GT-8 + GT-13 + GT-10? → *shift downside if demand evaporates ≈ one month's notice + hiring and training sunk ≈ $5–10k; roaster downside in the same scenario ≈ $15k install (unrecoverable) + 30–50% of $88k depreciation on forced resale ≈ $40–60k* → *the shift costs ~$35k/yr more but caps the bad outcome roughly 6x lower* → **paying the reversibility premium is rational for exactly as long as the account-terms uncertainty is live — and irrational after it resolves.** `[Assumes: A-13, A-6]`

Confidence: **MEDIUM-HIGH.** The time-bounding is the load-bearing part: this chain does not argue for the shift permanently, and C5 explains why it must not be permanent.

### C5 — A permanent double shift makes the fragility worse

**Chain:** GT-14 + GT-15? → *doubling duty cycle on a single machine roughly halves calendar time to major service while leaving zero redundancy* → *the failure probability rises fastest exactly when volume and commitments are highest* → **the second shift is defensible as a bridge and indefensible as an end state.** `[Assumes: A-8]`

Confidence: **MEDIUM-HIGH.** Softened by A-8's caveat — continuous running actually reduces thermal cycling per kg, so wear may scale sub-linearly. The redundancy half of the argument is unaffected by that caveat and carries the conclusion on its own.

### C6 — The 35kg is not the only capital option, and probably not the best one

**Trade-off analysis sub-step.** Criteria and weights locked before any scoring:

| Criterion | Weight | A: 35kg | B: full 2nd shift | C: hold | D: staged | E: twin 15–25kg |
|---|---|---|---|---|---|---|
| Capacity headroom vs growth | 5 | 5 | 3 | 1 | 4 | 3 |
| Reversibility under demand loss | 5 | 2 | 5 | 5 | 4 | 3 |
| Capital preservation | 4 | 2 | 5 | 5 | 4 | 4 |
| Supply reliability (redundancy) | 4 | 5 | 1 | 2 | 4 | 5 |
| Quality / profile continuity | 3 | 3 | 3 | 5 | 4 | 5 |
| Speed to relief | 4 | 2 | 5 | 1 | 5 | 3 |
| Unit economics at 2–3 yrs | 3 | 5 | 2 | 1 | 4 | 4 |
| **Weighted total** | | **95** | **99** | **80** | **116** | **105** |

*Sensitivity:* A (95) and B (99) sit within 4% — a genuine near-tie, and both are defensible as pure plays. The criterion that would flip them is redundancy (weight 4); I do not believe that weight is wrong, so the near-tie is a real finding rather than a scoring artefact. D and E separate cleanly from both and from each other by more than the noise band.

**Chain:** C1 + C5 + GT-3 → *a second machine matched to your current batch size delivers the same ~2x as the shift, adds full redundancy, preserves existing profiles because thermal mass and drum geometry are unchanged, and costs roughly half of $103,000* → **the capital question is not "35kg or nothing" — a right-sized twin dominates the 35kg on every criterion except raw headroom you will not use for four years.** `[Assumes: A-14, A-15]`

Confidence: **MEDIUM** — A-14 and A-15 are both unverified and both cheap to verify (one quote, one conversation with the manufacturer).

### C7 — The staged path, with second-order extension

**Chain:** C2 + C4 + C6 + GT-12? → *only a staged path relieves capacity inside the 3–6 month equipment lead time, preserves reversibility while the terms uncertainty is live, and defers the irreversible spend until it can be sized on better information* → **bridge with a partial second shift now; resolve account terms within 60–90 days; then buy a right-sized second machine on a pre-registered trigger.** `[Assumes: A-16]`

→**[2nd]** Hiring a second-shift roaster in a thin labour market may take 4–8 weeks and adds cross-shift quality variance requiring a documented profile and QC protocol. `[Assumes: A-10]`
→**[2nd]** Doubling green throughput lengthens the cash-conversion cycle — more green inventory, more capital tied up, before any additional receivable lands.
→**[2nd]** The term-conversion ask may itself prompt an account to re-evaluate and shop the market. `[Assumes: A-17]` — mitigate by pairing the ask with something they want: locked pricing, priority allocation during peak, or a volume rebate.
→**[3rd]** A successful term conversion becomes financeable evidence, improving equipment-loan terms and lowering the effective cost of the eventual capex.
→**[3rd]** At 2x output the bottleneck migrates downstream to packaging, QC cupping, and delivery — neither original option addresses this, and it will surface within weeks of the shift starting.
→**[3rd]** Excess capacity, once installed, creates pressure to fill it with private-label or co-packing work, which is itself a hedge against wholesale concentration.

Stopping at the 3rd order; the 4th becomes speculation. **Contradiction check:** no enumerated effect contradicts GT-1 through GT-17?. The A-17 effect refines GT-8 rather than contradicting it. No route back to Phase 2 is triggered.

Confidence: **MEDIUM-HIGH.**

---

# 5. Abandoned Reasoning

**Framed as an NPV cost-minimisation.** My first pass built a discounted-cash-flow comparison of $103k capex against a $50.4k/yr opex stream, yielding a ~24-month crossover. Abandoned once C3 showed the annual spread (~$35k) is small relative to the contribution at stake (~$100–250k/yr). A model that optimises a second-order variable to three decimal places while the first-order variable is unmeasured is precision theatre.

**Recommending an outright "buy" on asymmetric payoff.** I built a case that bounded downside (~$55k stranded) versus unbounded upside (~$250k/yr of margin) favours buying even at p(demand holds) ≈ 0.5. Abandoned because C1 broke the premise: the upside is not gated on *35kg* capacity specifically. A cheaper twin captures nearly all of the same margin, so the asymmetry argues for buying *something*, not for buying *this*.

**Toll roasting / co-packing as the bridge.** Retained as a fallback, rejected as primary. It transfers your profiles and green sourcing to a third party, most co-packers will not take specialty-scale volumes at acceptable quality, and the QC exposure lands precisely on the two accounts you can least afford to disappoint.

**"Hold off" as a standing option.** Rejected outright: capacity is binding now (GT-9), so holding is the only option that carries an ongoing cost — foregone margin — while purchasing no option value in return. Its 80 in the trade-off matrix is the lowest of the five for exactly this reason.

**Buying the 35kg but running both machines simultaneously.** Considered as a way to defeat C1's utilisation argument. Abandoned because it requires a second operator, which re-imports the shift's ~$50k/yr labour cost on top of the $103k capex — the worst of both options rather than the best.

---

# 6. Conclusion

**Do none of the three things as posed. Stage it.**

**The 35kg roaster is sized to demand you do not have yet (C1).** At 20% annual growth it takes about 4.6 years to fill. You would be paying $103,000 today for headroom that sits idle for roughly three of those years, while the two accounts underwriting the growth can leave with thirty days' notice.

**Do not adopt a permanent double shift as the end state either (C5).** It doubles duty cycle on a single machine with zero redundancy — raising outage probability exactly when your commitments peak. It is a fine bridge and a poor destination.

**Do not hold off (C2, C3).** Capacity binds now, the machine has roughly 4.7x physical headroom that only a staffing convention is blocking, and the margin you are turning away likely exceeds the cost of either fix by an order of magnitude.

**What to do, in order:**

1. **Now — add a partial second shift**, not a full one. A four-to-five-hour evening turn at roughly $2,100–2,500/mo buys most of the capacity at half the cost and half the wear, and it is cancellable at thirty days (C2, C4, C7). This is the bridge across the equipment lead time, which you will need regardless of what you eventually buy.
2. **Within 30 days — get the one number that decides this.** What percentage of volume do those two accounts represent? Rough thresholds from C1's arithmetic: if their combined share is **under ~20%**, growth alone keeps you capacity-bound through their loss and you should buy. If it is **over ~35%**, losing them returns you to slack capacity and you should not commit capital until the account base is broader.
3. **Within 60–90 days — convert the terms.** Offer locked pricing, priority peak allocation, or a volume rebate in exchange for a six-to-twelve-month commitment or a monthly volume floor. Do not make a bare ask: it invites them to shop (A-17, C7 second-order). A signed floor is also financeable collateral that improves your eventual loan terms.
4. **Then buy — but price a twin, not the 35kg (C6).** A second 15–25kg machine gives you the same ~2x capacity, full redundancy against the failure mode that scares me most, identical roast profiles with no re-development risk to your flagship blends, and roughly half the capital outlay. Get that quote before you sign anything for the 35kg.
5. **Pre-register the trigger now, while you are calm.** Write it down: *"We order when (a) contracted or floor-committed volume covers X kg/week, or (b) the two at-risk accounts fall below Y% of volume, whichever comes first."* Deciding the rule before the data arrives is what stops a good month from being mistaken for a trend.

**Cost is not the deciding variable here (C3).** The $35k/yr spread between your two original options is a rounding error against the ~$100–250k/yr of margin that hinges on whether the demand is durable. Spend the next ninety days buying information about that, not equipment.

---

## Phase 5 — Validation

**Weakest links, flagged rather than resolved:**

- **`GT-16?` (account concentration) is load-bearing for the entire recommendation.** Every threshold in §6 step 2 is derived arithmetic, but the input is yours to supply. This is the single verification that would move the whole analysis from MEDIUM to HIGH confidence.
- **`GT-11?` (contribution margin) is load-bearing for C3**, which is what demotes cost from a primary to a secondary criterion. If your true contribution is nearer $3/kg than $8/kg, C3 weakens materially and the cost comparison re-enters as a first-order concern.
- **A-14/A-15 (twin machine price and profile transfer) are load-bearing for C6**, my most actionable recommendation. Both are unverified. Both cost one phone call to verify. Do not act on C6 before making those calls.
- **A-10 (hireability) is load-bearing for C2 and C7.** If you cannot hire a competent evening roaster, the bridge does not exist and the decision collapses back to a straight buy-or-hold — in which case, given C1 and C6, buy the twin.
- **A-8 partially contradicts GT-15?**, softening C5's wear argument. C5's conclusion survives on the redundancy argument alone, which is unaffected.

**Pre-mortem (prospective hindsight — "the plan has already failed; what caused it?"):** the recurring cluster across enumerated failure causes is not cost overrun or misjudged demand. It is **the single point of failure combined with the unmeasured concentration number** — the same two roots appear in five of seven failure paths. That clustering is a structural weakness in your current position, independent of which option you pick, and it is why redundancy carries a weight of 4 in the matrix and why C6 ends up dominating. The staged plan addresses both roots: step 2 measures the concentration, step 4 removes the single point of failure. If you take nothing else from this, take those two.

**Rubric gate:** Essence answered ✓ · every §6 claim traced to a named chain ✓ (see ledger) · every chain contains at least one intermediate step ✓ · all assumptions classified and verdicted ✓ · unverified inputs marked `?` and their dependent conclusions caveated ✓ · abandoned paths recorded ✓ · no analogy used as standalone evidence ✓ · second-order pass run with contradiction check ✓ · Assumption Audit run and table updated ✓.

**Overall confidence: MEDIUM-HIGH on the sequencing, MEDIUM on the thresholds.** The sequencing (bridge → measure → convert → buy right-sized) is robust across the full range of my unverified inputs. The specific 20%/35% thresholds move with `GT-16?` and `GT-11?`.