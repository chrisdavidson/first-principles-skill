## Process output — Assumption Audit (Phase 4, end-of-phase scan)

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | 81,900 WC orders/yr × $3.10 | 3PL rate is all-in (no accessorials/storage/receiving) | Yes → A-9 |
| C1 | 2 | → 3PL = $253,890/yr | Rate holds at this volume tier | Yes → A-10 |
| C2 | 1 | $420k lease is facility-only | Lease figure excludes labor | Yes → A-4 |
| C2 | 2 | 8 hires × fully-loaded cost | Fully-loaded ≈ 1.3× base | Yes → A-5 |
| C2 | 3 | + other opex (WMS, MHE, utilities, shrink) | Omitted-cost line exists and is non-zero | Yes → A-6 |
| C2 | 4 | → ~$1.0M/yr, ~$12.20/order | — (clean) | n/a |
| C3 | 1 | per-head throughput ~32,500 orders/yr | Pick/pack productivity benchmark | Yes → A-7 |
| C3 | 2 | fixed $520k + $1.85/order variable | Lease/overhead does not step up with volume | Yes → A-11 |
| C3 | 3 | → breakeven V ≈ 416,000 orders/yr | — (clean) |  n/a |
| C4 | 1 | split diverts volume from fixed-cost node | No fixed-cost reduction available at half scale | Yes → A-12 |
| C4 | 2 | → split dominated on cost | — (clean) | n/a |
| C5 | 1 | 5pp return-rate deterioration scenario | Return handling ≈ $15–25 each | Yes → A-8 |
| C5 | 2 | → ~$82k/yr vs $746k/yr gap | Control damage is bounded and quantifiable | Yes → A-13 |
| C1 | →[2nd] | 3PL dependency / renewal pricing | Provider has pricing power at renewal | Yes → A-14 |
| C3 | →[2nd] | 3-year lease locks ~$1.26M | Growth is unquantified | Yes → A-2 (existing) |

---

# 1. Problem Essence

**Core question:** At current and near-term west-coast volume, which fulfillment structure delivers 2-day west-coast delivery at the lowest total cost per order without foreclosing future options?

This is not "do we want a west-coast warehouse." It is a **capacity-utilization decision under demand uncertainty**: a warehouse is a large fixed cost that only beats a per-unit price above a threshold volume. The triggering event (growth) is not the question; the question is whether current volume clears that threshold.

**Success criteria** (checkable against the conclusion):
1. Both options deliver the stated 2-day west-coast SLA.
2. Total annual cost is compared on a like-for-like basis (all-in, not lease-vs-rate).
3. The volume at which the ranking flips is stated numerically.
4. The commitment's reversibility under demand uncertainty is addressed.
5. The non-cost factor (packaging/returns control) is priced, not asserted.

---

# 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | 35% of 4,500/wk = 1,575 WC orders/wk | current constraint | Expires if mix shifts | Accepted | Given |
| A-2 | "Growing" — rate unquantified | untested belief | Verify or flag | **UNVERIFIED — flagged** | Needs 8-quarter WC trendline |
| A-3 | Both options meet 2-day SLA | current constraint | Recorded as stated | Accepted | Given; 3PL side needs contractual SLA |
| A-4 | $420k/yr is facility-only, excludes the 8 hires | untested belief | Verify | **UNVERIFIED — flagged**; analysis run both ways | Read the lease term sheet |
| A-5 | Fully-loaded warehouse labor $50–70k/head | untested belief | Bracketed | Flagged with range | Regional comp data |
| A-6 | Startup + running opex beyond lease/labor is non-zero (WMS, racking, MHE, utilities, insurance, shrink) | physical law–adjacent (definitional: a warehouse cannot operate on rent alone) | Accept as ground-truth candidate | Accepted | Structurally necessary |
| A-7 | ~125 orders/person/day pick-pack-ship | untested belief | Bracketed 80–150 | Flagged with range | Industry benchmark |
| A-8 | Return handling ≈ $15–25 per return | untested belief | Bracketed | Flagged | Own current returns cost |
| A-9 | $3.10 is all-in (no receiving/storage/accessorial) | **convention — challenged** | 3PL quotes conventionally exclude storage and inbound | **Likely FALSE as stated** | Demand a fully-burdened quote |
| A-10 | $3.10 holds at 81,900/yr | convention | Challenge | Probably tier-dependent | Get the rate card |
| A-11 | Lease/overhead is flat across relevant volume | current constraint | Expires at facility capacity | Accepted in range | Sq-ft capacity check |
| A-12 | No half-size facility option exists at ~half cost | untested belief | Verify | **UNVERIFIED** | Test smaller-footprint quotes |
| A-13 | Control loss is bounded (returns + packaging quality) | untested belief | Verify | Flagged — brand damage is not fully bounded | See §5 |
| A-14 | 3PL has renewal pricing power once you depend on it | convention → verified pattern | Challenge, then mitigate contractually | Accepted as a risk to price in | Structural |
| A-15 | Only two structures exist (build / 3PL / 50-50) | **convention — challenged and REJECTED** | Challenge before use | **FALSE** — asymmetric hybrid exists | See §6 |

**Inversion pass (what would guarantee the 3PL recommendation is wrong):** (i) $3.10 is not all-in and true landed cost is 2–3×; (ii) WC volume is on a trajectory to 5× within the lease term; (iii) a control-critical revenue segment exists whose loss exceeds $746k/yr; (iv) the 8 hires are already inside the $420k; (v) no 3PL will contract for 2-day SLA with penalties. Each is now a row above.

---

# 3. Ground Truths

- **GT-1:** 1,575 WC orders/week = **81,900/year**. (4,500 × 0.35 × 52; arithmetic from given figures.)
- **GT-2:** 3PL quoted rate = **$3.10/order** (as stated; scope caveat A-9).
- **GT-3:** Warehouse lease = **$420,000/year × 3 years = $1,260,000 committed**.
- **GT-4:** Warehouse requires **8 new hires**.
- **GT-5?:** Fully-loaded labor $50–70k/head → **$400k–$560k/yr** (unverified, bracketed).
- **GT-6?:** Non-lease, non-labor opex **$60k–$150k/yr** plus **$200k–$600k one-time fit-out** (unverified, bracketed; structurally necessary per A-6).
- **GT-7?:** Throughput **~32,500 orders/head/year** (125/day × 260 days) (unverified, bracketed 80–150/day).
- **GT-8?:** Return handling **$15–25 each** (unverified).
- **GT-9:** A fixed cost divided by volume falls monotonically as volume rises — **definitional**, not empirical. This is the load-bearing structural truth of the whole analysis.
- **GT-10:** A 3-year lease plus 8 employment relationships is **materially harder to reverse** than a logistics contract. (Definitional: real property leases and employment carry exit costs; a service contract's exit cost is set by its term.)

---

# 4. Derivation Chains

**C1 — 3PL annual cost**
GT-1 + GT-2 → 81,900 × $3.10 → **3PL ≈ $254,000/yr, fully variable**. *(Confidence: HIGH on arithmetic, MEDIUM on scope — depends on A-9.)*
→[2nd] Dependence on a single provider grows with tenure; renewal leverage shifts to them [Assumes: A-14].
→[3rd] Switching cost (re-integration, inventory transfer) rises each year → mitigate now via term length, exit clause, and data-ownership terms, not later.

**C2 — In-house annual cost**
GT-3 + GT-4 + GT-5? + GT-6? → $420k + $480k (central) + $100k (central) → **≈$1.0M/yr [bracket: $880k – $1.13M]**, plus $200–600k one-time → **≈$12.20/order at current volume** → **in-house costs ≈$746k/yr more than the 3PL today**, i.e. a **~$9.10/order control premium**. *(Confidence: MEDIUM-HIGH — the bracket's lower bound $880k still exceeds $254k by 3.5×, so both ends drive the same decision. If A-4 is false and $420k is all-in, in-house is still $420k vs $254k — same direction.)*

**C3 — Breakeven volume**
GT-9 + GT-3 + GT-6? (fixed ≈ $520k) + GT-7? (variable labor ≈ $1.85/order) → cost/order = $520,000 ÷ V + $1.85 → set equal to $3.10 → $520,000 ÷ V = $1.25 → **V ≈ 416,000 orders/yr ≈ 8,000 WC orders/week** → **breakeven requires ~5× current west-coast volume — nearly 2× the company's entire current order book (4,500/wk)**. *(Confidence: MEDIUM — sensitive to GT-7?. At the pessimistic 80 orders/day the breakeven rises further; at the optimistic 150/day it falls to ~5,900/wk, still 3.7× current. The bracket does not straddle the decision threshold.)*
→[2nd] The 3-year lease commits $1.26M against a growth rate that is **unquantified** [Assumes: A-2] — the commitment's term exceeds the horizon over which the growth assumption is verified.

**C4 — The split option**
C2 + C3 + GT-9 → a 50/50 split routes ~40,950 orders/yr through a node carrying the **full** $520k fixed cost → in-house cost/order rises to **≈$14.55**, worse than the unsplit $12.20 → **the split is dominated on cost by the pure 3PL option and dominated on control by the pure build option** [Assumes: A-12 — no proportionally smaller facility available]. *(Confidence: HIGH, conditional on A-12.)*

**C5 — Pricing the control gap**
C2 + GT-8? → worst-case 5pp return-rate deterioration = 4,095 extra returns × $20 → **≈$82k/yr** → the modelled control damage is **~9× smaller than the $746k cost gap** → **control considerations alone cannot justify the build at current volume**. *(Confidence: MEDIUM — bounds the *measurable* control cost. Unmeasured brand/repeat-purchase damage is not captured [Assumes: A-13]; see §5.)*
→[2nd] Poor 3PL packaging degrades unboxing → repeat-purchase rate → this is the one channel through which control loss could plausibly reach $746k, and it is **not** bounded by C5 → therefore it must be handled contractually (packaging spec, mystery-shop audits, SLA penalties), not waved away.
**Contradiction check:** no second-order effect contradicts GT-1, GT-3, GT-9, or GT-10. No return to Phase 2 required beyond the rows already added.

---

# 5. Abandoned Reasoning

- **"Do it in-house to build a strategic capability asset."** Abandoned as an *analogy-based* argument (Amazon built its own network, therefore we should). Amazon's ground truth was volume 4+ orders of magnitude above GT-1; the analogy transfers no verified fact about *this* situation. Rejected per the no-analogy-as-evidence rule.
- **Straight 50/50 split.** Pursued seriously through C4 and abandoned on the arithmetic: it worsens the very ratio that makes the build unattractive.
- **Cost-per-order-only framing.** Abandoned mid-analysis as insufficient — it cannot price irreversibility (GT-10) or lock-in, which is why C1/C3 carry second-order extensions rather than stopping at the dollar figures.
- **Bounding brand damage.** Attempted in C5 and **explicitly not completed** — repeat-purchase elasticity to packaging quality is not knowable from available data. Flagged rather than fabricated.

---

## Process output — §6→§4 closure ledger

- "Use the 3PL" → chain **C1 + C2** ✓
- "Warehouse is ~$746k/yr more expensive today" → chain **C2** ✓
- "Breakeven needs ~8,000 WC orders/week" → chain **C3** ✓
- "The 50/50 split is dominated" → chain **C4** ✓
- "Control alone doesn't justify the build" → chain **C5** ✓
- "Contract for optionality, not lowest rate" → chain **C1 →[2nd]/[3rd]** ✓
- "An asymmetric hybrid may be worth testing" → chain **C4 + A-15 rejection** ✓
- ~~"3PLs generally deliver better unit economics at small scale"~~ → **CUT** (no chain; unsupported generalization removed)

---

# 6. Conclusion

**Use the 3PL. Do not build the warehouse. Do not split 50/50.**

**The decisive number:** the warehouse breaks even against $3.10/order at roughly **8,000 west-coast orders per week**. You have **1,575**. You would need to grow west-coast volume ~5× — to nearly double your entire current company throughput — before the build pays for itself, and you would be committing $1.26M of lease plus 8 jobs for three years to a growth rate you have not quantified (A-2).

**The gap is not close.** In-house runs ≈$1.0M/yr [$880k–$1.13M] against ≈$254k for the 3PL — about **$9.10 per order** you would be paying for control. Modelled worst-case control damage (a 5-point return-rate deterioration) is ≈$82k/yr, roughly one-ninth of that premium. Even under the most warehouse-favourable reading of your figures (if $420k already includes the 8 hires), the ranking does not flip.

**The split is the worst of the three.** Half the volume through a facility carrying full fixed cost pushes in-house unit cost *up*, to ≈$14.55/order, while still not giving you the end-to-end control the build was supposed to buy.

**What to do instead of just signing:**

1. **Verify A-9 before anything else.** Get a fully-burdened 3PL quote — receiving, storage, accessorials, returns processing, peak surcharges. $3.10 is conventionally a pick-pack rate. If the landed rate is materially higher, re-run C3; the decision would still favour the 3PL, but the margin matters for term negotiation.
2. **Buy optionality, not the lowest rate.** Negotiate a **2-year term (not 3+)**, volume-tiered pricing with a step-down, contractual 2-day SLA with penalties, a defined packaging specification with audit rights, returns-data ownership, and a clean exit/transition clause. The second-order analysis says your leverage is highest now and decays with every month of dependence.
3. **Pre-register the revisit trigger.** Re-open the build decision when west-coast volume sustains **≥6,000 orders/week** for two consecutive quarters, or if audited 3PL packaging/returns quality breaches the SLA. Write the number down now, before you have a result you want to justify.
4. **Test the option this analysis rejected as a false binary (A-15).** A 50/50 split is dominated — but an *asymmetric* hybrid is not the same thing: 3PL for standard volume, with a control-critical segment (subscription boxes, high-AOV, custom packaging) retained in your existing facility and shipped west at higher transit cost. That requires no second lease and no 8 hires. Whether it's worth it depends on whether such a segment actually exists in your order mix — which is a data question you can answer this week.

**Confidence:** HIGH that the 3PL beats the build at current volume (every bracket end drives the same decision). MEDIUM on the precise breakeven point (sensitive to unverified GT-7?). The single assumption that could most change this is **A-9** — if $3.10 is not the real all-in rate, verify it before signing anything.