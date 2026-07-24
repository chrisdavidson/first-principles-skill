## Scope note before the analysis

One input is missing that changes exactly one conclusion: **jurisdiction**. The dollar figures and "CBCT" suggest a US practice, and the shared-referral chain (C4) below is derived under that assumption. If you are outside the US, treat C4 as unverified and substitute your local self-referral/inducement rules — every other chain is jurisdiction-independent. I proceeded rather than blocking because the primary answer does not depend on it.

**Step 0 — technique selection:** No focused-technique trigger phrase fired. `MODE = full-composer`. All five phases run; Phase 4 walks the eight companion techniques.

---

# 1. Problem Essence

**Essence Statement:** Does the contribution margin recoverable from scans you currently refer out exceed the full cost of owning the capacity to produce them — and is that margin robust enough to survive being wrong about how many referrals you can actually keep?

Success criteria for a correct answer:

- [ ] States a break-even scan volume, not just a payback period
- [ ] Distinguishes the volume you *send out* from the volume you can *keep in-house*
- [ ] Treats the neighboring-practice offer at its actual structural role, not as stated
- [ ] Names what would have to be measured to move the answer from "probably" to "yes"

**Reframe applied.** The question as posed is "buy / refer / explore" — three options. The analysis below finds that is not the real structure (see Abandoned Reasoning §5.2). The essence also strips out one framing artifact immediately: *"the machine would sit idle much of the week"* is presented as a cost. It is not one. See chain C2.

---

# 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | $110,000 capital cost is complete | current constraint | Record expiry conditions | **Likely incomplete** | Quoted price typically excludes room shielding/lead lining, electrical, operatory downtime, staff certification, and software licensing. Ask the vendor for an all-in installed figure. |
| A2 | $9,000/yr covers all recurring cost | current constraint | Record expiry conditions | **Likely incomplete** | Omits radiologist overread fees (see A9) and staff chair-time. Expires if you contract a teleradiology service. |
| A3 | All 25 monthly referrals are convertible to in-house scans | untested belief | Verify or flag | **UNVERIFIED — load-bearing** | Some referrals go out for specialist *interpretation*, patient insurance steering, or surgical co-treatment — not because you lack a machine. This is the single highest-stakes unverified input in the analysis. |
| A4 | $180/scan is net revenue | untested belief | Verify or flag | **False as stated** | $180 is gross. Reclassified to contribution margin ≈$140 in GT-3. |
| A5 | Machine useful life ≈7 years | convention | Challenge before use | **Accepted with caveat** | 7 yrs is the conservative end of the 7–10 yr industry/depreciation convention. Sensor and software obsolescence, not mechanical failure, usually sets the real horizon. Conservative choice favors the "don't buy" side — appropriate. |
| A6 | Purchase is cash, not financed | untested belief | Verify or flag | **Assumed** | Financing at ~8%/5yr adds ~$24k total interest. Changes timing and magnitude, not the sign of the answer. |
| A7 | Neighbor's offer is firm and durable | untested belief | Verify or flag | **UNVERIFIED** | A verbal offer from a party with no contractual exposure. Treated as zero-value in the base case. |
| A8 | Referral volume is stable at 25/mo | untested belief | Verify or flag | **Assumed** | Derived from your own stated average; seasonality and case-mix drift not modeled. |
| A9 | You can interpret the full CBCT field of view | untested belief | Verify or flag | **UNVERIFIED — surfaced by C5** | Owning the scan creates a duty of care over the *entire* imaged volume, including incidental findings outside the dental region of interest. Either a dentist takes that liability or you pay per-scan overread. |
| A10 | Stopping referrals has no cost | untested belief | Verify or flag | **False — surfaced by C5** | Specialist referral relationships are frequently reciprocal. |
| A11 | US jurisdiction | untested belief | Verify or flag | **ASSUMED — flagged** | Governs C4 only. |
| A12 | Scan indications stay constant post-purchase | untested belief | Verify or flag | **UNVERIFIED — surfaced by C5** | Owning imaging capacity reliably increases ordering rates ("indication creep"). Cuts both ways: revenue up, dose-stewardship and payer-scrutiny exposure up. |

**Inversion pass** (what would guarantee this purchase fails): capture rate below ~60%; overread fees materially eroding the $180; the neighbor deal evaporating after purchase; a reciprocity collapse costing more inbound patients than the scans earn; obsolescence before year 7. A3, A7, A9, A10 above are the preconditions those failure modes attack — each is currently unverified.

**Fishbone pass** (cause categories for "referrals leave the practice"): *People* — dentist comfort with 3D interpretation; *Process* — referral is habitual, not clinical; *Technology* — no machine (the assumed cause); *Information* — specialist wants their own imaging protocol; *Resources* — chair time; *Environment* — insurance networks steering the patient. Only the *Technology* branch is fixed by buying a machine. This is the direct source of A3's doubt.

---

# 3. Ground Truths

- **GT-1:** Capital outlay ≈$110,000, quoted (user-supplied; understated per A1).
- **GT-2:** Recurring cost ≈$9,000/yr, quoted (user-supplied; understated per A2).
- **GT-3?:** Contribution margin per scan ≈**$140** (bracket $100–$180). Derived: $180 gross, less ~$20–40 loaded staff/chair time, less $0–60 optional overread. *Unverified — depends on your overread decision.*
- **GT-4:** ~25 CBCT referrals leave the practice monthly (user-supplied, direct measurement).
- **GT-5:** Four dentists share the practice (user-supplied).
- **GT-6?:** Useful life ≈7 years (convention, conservative end — A5).
- **GT-7:** *Definitional:* fixed costs accrue per unit of time, not per unit of use. Idle hours generate no incremental cash cost.
- **GT-8:** *Derived from GT-7:* marginal cash cost of one additional scan on an owned machine ≈ staff time only, near zero relative to the $180 fee.
- **GT-9?:** Under US federal law (Anti-Kickback Statute; Stark Law where applicable), remuneration exchanged between providers in connection with patient referrals is restricted, and arrangements structured as per-referral or volume-linked value transfer carry criminal and civil exposure. *Conditional on A11.*
- **GT-10:** *Irreducibility drill on "the machine pays for itself":* reduces to → (scans captured/mo) × (contribution/scan) × 12 ≥ (capital ÷ life) + (annual fixed). Every term bottoms out at a measurement or a definition. No further reduction available.

---

# 4. Derivation Chains

### C1 — The break-even volume, not the payback period *(estimate / Fermi)*

Target quantity: **scans per month required to break even**, units = scans/month.

Unit cancellation: `($/yr required) ÷ ($/scan) ÷ (12 mo/yr) → scans/month` ✓

Annualized capital recovery, undiscounted: $110,000 ÷ 7 yr = **$15,714/yr**
At an 8% cost of capital (7-yr annuity factor 5.206): $110,000 ÷ 5.206 = **$21,130/yr**

> **GT-1 + GT-2 + GT-6? + GT-3? → required annual contribution = $15,714–$21,130 (capital) + $9,000 (fixed) = $24,714–$30,130 → ÷ $140/scan ÷ 12 → break-even ≈ 15–18 scans/month → you must retain 60–72% of your existing 25 monthly referrals just to reach zero.**

Full bracket on annual net cash:

| Scenario | Capture | Contribution | Fixed | Annual net | Payback |
|---|---|---|---|---|---|
| Conservative | 12/mo (48%) | $100 | $15,000 | **−$600** | never |
| Central | 18/mo (72%) | $140 | $9,000 | **+$21,240** | 5.2 yr |
| Aggressive | 25/mo (100%) | $180 | $9,000 | **+$45,000** | 2.4 yr |

**Stop-criterion result: FAILED.** The decision-resolution rule requires both bracket ends to drive the same decision. They do not — the lower end loses money over the machine's entire life while the upper end pays back in under two and a half years. The dominant uncertain factor is capture rate (A3). Per the procedure, this escalates: **tighten that factor with a measurement before deciding.** Confidence: **HIGH** in the break-even band, **LOW** in which side of it you land on.

### C2 — Idle time is not a cost

> **GT-7 + GT-8 → the machine's fixed cost is identical whether it runs 4 hours a week or 40 → utilization is not a term in the break-even equation → "it would sit idle much of the week" is emotionally salient and economically irrelevant.**

The only question idle capacity raises is whether *filling* it (i.e., the neighbor) is a legitimate route to volume — which is C4's problem, not a cost problem. Confidence: **HIGH**.

### C3 — What the neighbor's offer actually is

> **GT-6? (offer is verbal, non-binding, from a party with no exposure) + C1 (base case is uncomfortably near break-even) → the offer's function is to make a marginal purchase look clearly positive → an unenforceable input is doing load-bearing work in a $110,000 decision → the offer must be valued at zero in the base case and treated strictly as upside.**

If the deal is real and legal, it plausibly adds 10–20 scans/month, which would push you decisively clear of break-even. That is precisely why it must be verified *before* it influences the purchase, not after. Confidence: **HIGH**.

### C4 — The shared-referral arrangement is the highest-risk element, not the safest *(conditional on A11)*

> **GT-9? + C3 → an arrangement in which one practice directs patients to another practice's revenue-generating equipment is the exact fact pattern federal referral law scrutinizes → "explore the shared-referral arrangement" is not a low-commitment first step; it is the step requiring counsel before any money moves → [Assumes: A11 — US jurisdiction].**

This does not mean the arrangement is unlawful. Compliant structures exist (fair-market-value per-scan technical fees set in advance, not varying with volume or value of referrals; written agreements of at least one year; safe-harbor-conforming terms). It means the structure must be designed by a healthcare attorney rather than agreed over coffee. Confidence: **MEDIUM** (HIGH on the need for counsel; LOW on the outcome, which depends on structure and state law).

### C5 — Second-order consequences

Applying the second-order pass to the C1 conclusion ("buying is marginally positive at central assumptions"):

**2nd-order effects:**
1. Referrals to oral surgeons/endodontists drop → those specialists' reciprocal inbound referrals to you may drop `[Assumes: A10]`
2. In-house availability increases scanning frequency beyond current clinical indications `[Assumes: A12]`
3. You acquire a duty of care over the full imaged volume, including non-dental incidental findings `[Assumes: A9]`
4. The neighbor practice becomes operationally dependent on your equipment uptime

**3rd-order effects:**
1a. Net patient flow could decline even as scan revenue rises — a reciprocity loss of even 2–3 restorative or surgical cases per month can exceed $2,000/mo in production, dwarfing the ~$1,700/mo net scan contribution
2a. Higher scan volume → cumulative patient dose stewardship obligations, malpractice exposure on over-ordering, and payer utilization scrutiny
3a. Duty over the full FOV means either a dentist reads regions outside their training (liability) or you pay $25–60/scan for radiologist overread (**this is what reduces GT-3? from $180 to ~$140 — the effect feeds directly back into C1's dominant term**)
4a. Equipment downtime becomes a relationship failure, not just an internal inconvenience

**Contradiction check:** effect 3a materially undercuts the naive $180/scan premise. Per the routing rule, this returned to Phase 2 for re-challenging — A4 was reclassified as **false as stated** and GT-3? was rebuilt at $140. No remaining effect contradicts a ground truth. Confidence: **MEDIUM** on magnitudes, **HIGH** on direction.

### C6 — Weighted trade-off *(weights locked before scoring)*

Options: **(1)** Buy now · **(2)** Keep referring indefinitely · **(3)** Measure and clear the two unknowns first, then decide

| Criterion | Wt | Opt 1 | Opt 2 | Opt 3 |
|---|---|---|---|---|
| Expected 7-yr net cash | 5 | 4 | 2 | 4 |
| Downside protection / reversibility | 4 | 2 | 5 | 5 |
| Legal & regulatory safety | 5 | 3 | 5 | 5 |
| Diagnostic quality & speed of care | 3 | 5 | 2 | 3 |
| Specialist relationship preservation | 2 | 2 | 5 | 4 |
| Decision speed / cost to pursue | 2 | 4 | 5 | 3 |
| Information gained on the key unknown | 4 | 2 | 1 | 5 |
| **Weighted total** | | **78** | **85** | **108** |

**Sensitivity check:** Options 1 and 2 sit within 9% of each other — a genuine near-tie, meaning *buying now and never buying are roughly equally defensible on today's information*. That near-tie is itself the finding: it is what makes the information criterion decisive. Option 3 clears both by >25%; no weight adjustment flips it.

> **C1 (bracket straddles the threshold) + C3 (key input unenforceable) + C4 (legal structure unresolved) → the two decisive unknowns are both cheap to resolve and expensive to be wrong about → measuring first strictly dominates → Option 3.**

Confidence: **HIGH**.

### Assumption Audit (end-of-Phase-4 scan)

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| C1 | 1 | Annualized capital recovery | Useful life = 7 yr | Already present (A5) |
| C1 | 2 | ÷ $140/scan | Contribution ≠ gross fee | Already present (A4) |
| C1 | 3 | Break-even 15–18/mo | Capture rate unknown | Already present (A3) |
| C1 | 4 | Bracket table | Cash purchase | Already present (A6) |
| C2 | 1 | Fixed cost time-invariant | — | Clean pass |
| C2 | 2 | Utilization not a term | — | Clean pass |
| C3 | 1 | Offer non-binding | Offer durability | Already present (A7) |
| C3 | 2 | Value at zero in base case | — | Clean pass |
| C4 | 1 | Federal referral law applies | **Jurisdiction** | **Added — A11** |
| C4 | 2 | Counsel required pre-commitment | — | Clean pass |
| C5 | 2a | Reciprocity loss | **Referral reciprocity** | **Added — A10** |
| C5 | 2b | Indication creep | **Ordering-rate stability** | **Added — A12** |
| C5 | 2c | Full-FOV duty of care | **Interpretation competence/liability** | **Added — A9** |
| C5 | 3a | Overread fee feeds back to GT-3? | — | Routed to Phase 2; A4 reclassified |
| C6 | 1 | Weights locked pre-scoring | — | Clean pass |
| C6 | 2 | Option 3 dominates | — | Clean pass |

---

# 5. Abandoned Reasoning

**5.1 — Utilization framing.** The initial framing treated "sits idle much of the week" as a cost to be offset. Abandoned at C2: idle capacity is a psychological cost, not a cash cost, and including it would have biased the analysis toward chasing volume (the neighbor deal) for its own sake. This is the exact reasoning error the neighbor's offer is positioned to exploit.

**5.2 — Three-option framing.** The question presents buy / refer / share as parallel alternatives. Abandoned: the shared-referral arrangement is not an alternative to buying — it is a *volume modifier on the buy option* that only has value if you own a machine. Recognizing this collapses the decision to buy-vs-don't with a contingent upside, which is what made C6's third option (measure first) constructible.

**5.3 — Lease-vs-buy.** Explored and set aside. Financing changes the timing and total cost (~$24k interest at 8%/5yr) but does not change the sign of the answer or the break-even volume materially. It becomes relevant *after* the capture-rate question is settled, not before.

**5.4 — Reasoning from "most practices this size own one."** Rejected as analogy. Any comparable practice's decision would only be evidence if their capture rate and case mix were verified — at which point their capture rate, not their decision, is the useful datum.

---

# 6. Conclusion

**Do not buy yet, and do not walk away. Spend 30–60 days and a few hundred dollars closing the two unknowns that the whole decision rests on** *(chain C6)*.

Concretely:

1. **Audit your last 75–100 referrals** (three to four months) and tag each with the *actual* reason it left the building: no machine · specialist interpretation needed · surgical co-treatment · insurance steering · patient preference. Only the first category converts. **Your break-even is 15–18 scans/month — 60–72% capture** *(chain C1)*. If the audit shows you'd retain 20+, buy without further deliberation. If it shows 12 or fewer, the machine loses money over its entire life and the answer is a clean no. Between 15 and 18, it is a coin flip on financial grounds and you should decide on clinical and strategic grounds instead.

2. **Get a healthcare attorney's read on the neighbor arrangement before it influences the purchase.** It is the most legally exposed element here, not the safest first step, and it is currently doing load-bearing work in a $110,000 decision on the strength of a verbal offer *(chains C3, C4)*. Structure it as a fair-market-value technical fee fixed in advance and independent of volume, or not at all.

3. **Settle the overread question in the same window.** Whether a dentist reads the full field of view or you pay a radiologist per scan is what moves your per-scan contribution between $100 and $180 — the second-largest lever in the model, and one you control by choosing *(chain C5)*.

Two things the model deliberately does not count, both of which favor buying: incremental case acceptance on implant and endodontic treatment made possible by same-day 3D imaging, and the patients you stop losing to specialists who retain them. If your referral audit lands near break-even, these are the reasons to lean yes. Against them, weigh the reciprocity loss from specialists you stop feeding *(chain C5)* — a decline of two to three restorative cases a month can quietly exceed the entire scan contribution.

**The single sentence:** your decision hinges on one number you have never measured, that number is cheap to measure, and the machine will still be for sale in sixty days.

---

<details>
<summary><b>Process output — §6→§4 closure ledger and rubric pass</b></summary>

**Closure ledger (every §6 claim → its §4 chain):**

- "Do not buy yet, do not walk away; measure first" → chain **C6** ✓
- "Break-even is 15–18 scans/month, 60–72% capture" → chain **C1** ✓
- "Neighbor offer is load-bearing on a verbal commitment" → chain **C3** ✓
- "Legal structure must precede purchase influence" → chain **C4** ✓
- "Overread decision moves contribution $100–$180" → chain **C5** ✓
- "Reciprocity loss can exceed scan contribution" → chain **C5** ✓
- "Idle time is not a reason against buying" → chain **C2** ✓ *(carried implicitly in §6's framing; chain present)*
- ~~"Most comparable practices own one"~~ → **CUT** (analogy, no chain — removed at §5.4)

Ledger clean; no §6 claim survives without a named chain. Re-verified after the Fix pass below; no chain was renamed or merged.

**Rubric pass:** Essence names a question distinct from the one asked (reframed from three-option to two-option-plus-measurement) ✓ · All four assumption types represented, treatments applied ✓ · Ground truths carry IDs, `?` flags on GT-3/6/9 ✓ · Every chain has ≥1 intermediate step ✓ · Second-order pass ran and one effect (3a) routed back to Phase 2, reclassifying A4 ✓ · Assumption audit ran, four assumptions added (A9–A12) ✓ · Weakest link identified and flagged: **A3, capture rate** — it is the load-bearing unverified input, it is explicitly named as such, and the entire recommendation is structured around verifying it rather than assuming past it ✓ · Estimate stop-criterion honestly reported as FAILED rather than papered over ✓ · Abandoned reasoning non-empty and substantive ✓ · Jurisdiction gap disclosed at the top rather than silently assumed ✓

Gate cleared.

</details>