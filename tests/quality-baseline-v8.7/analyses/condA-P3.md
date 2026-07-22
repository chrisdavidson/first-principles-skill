# First-Principles Analysis: Attic Insulation vs. Window Replacement

---

## 1. Problem Essence

**Essence Statement:** Given one fixed pot of money, which single fabric intervention buys the largest reduction in heat loss *and* draught discomfort on the top floor of a 1960s temperate-climate house?

Note the framing artifact: you described a *symptom* ("cold, draughty top floor") but asked about two *conduction* remedies. Cold ≠ draughty. These are two distinct physical mechanisms (conductive/radiative loss vs. advective air exchange), and the winning option differs depending on which dominates. The analysis must answer both.

**Success criteria** (checkable against the conclusion):
1. Identifies which mechanism dominates the stated symptom.
2. Ranks the two options on heat-energy saved per unit of money spent.
3. Ranks them on top-floor comfort improvement, which is not the same ranking.
4. Names the conditions under which the ranking flips.
5. Flags any second-order harm the recommended option creates.

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | Heat loss through a building element = U × A × ΔT | physical law | Accept as GT candidate | **Accepted** | Fourier conduction, steady-state form; BS EN ISO 6946 |
| A2 | Warm air rises, creating positive pressure at the top of the building envelope (stack effect) | physical law | Accept as GT candidate | **Accepted** | Buoyancy from density difference of air at differing temperature |
| A3 | The loft is a conventional cold ventilated roof void with an accessible ceiling plane | current constraint | Record expiry conditions | **Unverified — load-bearing** | If the top floor is a room-in-roof / loft conversion, "insulate the attic" means insulating between rafters at 3–8× the cost and the whole cost comparison shifts. Flagged as GT-8? |
| A4 | The loft currently has little or no insulation | untested belief | Verify or flag | **Unverified — load-bearing** | 1960s stock was typically built with 0–25 mm; many have since been topped to 100 mm. Determines whether savings are large or marginal. Flagged as GT-7? |
| A5 | Windows are original single-glazed units | untested belief | Verify or flag | **Unverified** | 1960s original = single glazing; many have been replaced once already, in which case the window case collapses entirely |
| A6 | "Replace the windows" is a thermal upgrade | **convention — challenged** | Challenge before use | **Rejected as framing** | Window replacement is predominantly a *rot/rattle/security/aesthetics* purchase. Treating it as an energy measure imports an unexamined convention. See §5 |
| A7 | Draughts come from the windows | untested belief | Verify or flag | **Probably false as sole cause** | Under stack effect the top floor is the *pressurised* zone — air exfiltrates there. Cold-feeling air at the top floor more often originates from ceiling/loft-hatch penetrations and downdraught off cold glass, not window-frame inleakage |
| A8 | The budget is sized to cover whole-house window replacement | current constraint | Record expiry conditions | **Accepted from user framing** | Implies a budget of roughly 10–20× the cost of loft insulation. This asymmetry is itself the decisive fact — see §6 |
| A9 | Both measures last the same length of time | convention | Challenge before use | **Rejected** | Mineral wool in an undisturbed loft: 40+ yr, effectively the life of the building. Sealed double-glazed units: ~20–30 yr before seal failure. Windows depreciate; insulation does not |
| A10 | Space heating is the dominant energy end-use in a temperate-climate 1960s house | current constraint | Record expiry conditions | **Accepted** | Holds for temperate heating-dominated climates; expires if the house is cooling-dominated, in which case solar gain through glazing (g-value) — not U-value — becomes the driver |

**Fishbone sweep (Phase 2 breadth check).** Cause categories for "cold draughty top floor," to check the assumption space was not enumerated by intuition alone:
- **Envelope:** ceiling U-value; loft hatch uninsulated/unsealed; window U-value; wall U-value; gaps at eaves
- **Air paths:** loft hatch, downlighter penetrations, service risers/soil-pipe boxing, floorboard gaps, window frame perimeter, chimney
- **Systems:** undersized/unbalanced radiators upstairs, no thermostatic radiator valves, gravity-fed system with poor upper-circuit flow, boiler flow temperature
- **Occupancy:** upstairs unheated by habit, doors left open, bedroom setback
- **Measurement:** perceived cold from radiant asymmetry rather than low air temperature

Categories 3 and 5 generate a real possibility neither of your two options addresses — see §5.

---

## 3. Ground Truths

- **GT-1.** Conductive heat loss through an element = U × A × ΔT (W). *Physical law.*
- **GT-2.** An uninsulated 1960s ceiling to a ventilated loft has U ≈ 2.0–2.5 W/m²K; the same ceiling with ~300 mm of mineral wool has U ≈ 0.15–0.16 W/m²K. *Standard construction values, BS EN ISO 6946 / national building-regulation tables.*
- **GT-3.** Single glazing has U ≈ 4.8–5.6 W/m²K; a modern A-rated double-glazed unit has U ≈ 1.2–1.6 W/m²K. *Manufacturer and standards data.*
- **GT-4.** In a typical two-storey house, the top-floor ceiling area (≈ 40–60 m²) substantially exceeds total window area (≈ 12–20 m²). *Geometry of the housing type.*
- **GT-5.** Loft insulation is roughly £5–20/m² installed; window replacement is roughly £400–900/m² of opening installed. *Market pricing; ~40–100× difference per square metre treated.*
- **GT-6.** Stack effect pressurises the top of a heated envelope, so unsealed ceiling-plane penetrations drive continuous warm-air exfiltration, which must be replaced by cold infiltration lower down. *Consequence of GT/A2.*
- **GT-7?** *(unverified)* Your loft is currently at or below 100 mm of insulation.
- **GT-8?** *(unverified)* Your top floor sits beneath a conventional accessible cold loft, not within a room-in-roof.

---

## 4. Derivation Chains

### Chain A — Energy saved per unit spent

Estimate, with unit cancellation shown: `W/m²K × m² = W/K`; `W/K × K·h = Wh`. A temperate heating season is on the order of 2,000 K·days = 48,000 K·h.

*Attic (50 m² ceiling):* ΔU ≈ 2.15 W/m²K → 50 × 2.15 = **107 W/K** → × 48,000 K·h ≈ 5,100 kWh/yr of delivered heat; derated for real-world loft-void temperature and boiler efficiency, **bracket: 1,500 – 5,000 kWh/yr**, central ≈ 3,000.

*Windows (18 m²):* ΔU ≈ 3.4 W/m²K → 18 × 3.4 = **61 W/K** → × 48,000 K·h ≈ 2,900 kWh/yr; **bracket: 1,000 – 3,000 kWh/yr**, central ≈ 2,000.

So the raw energy saving is of the *same order* — windows are not thermally useless. The decision is not made on energy saved; it is made on energy saved *per pound*:

> **GT-1 + GT-2 + GT-4 → attic saves ≈ 107 W/K → GT-5 (attic ≈ £500–1,000) → ≈ 3–6 W/K per £100 spent**
>
> **GT-1 + GT-3 + GT-4 → windows save ≈ 61 W/K → GT-5 (windows ≈ £8,000–15,000) → ≈ 0.4–0.8 W/K per £100 spent**
>
> **→ Attic insulation buys 5–15× more heat-loss reduction per pound. [HIGH confidence]**

Payback: attic ≈ 2–5 years; windows ≈ 30–60 years, which by GT-9/A9 exceeds the service life of the sealed units themselves. **A window replacement bought as an energy measure never repays its capital.** [HIGH confidence]

### Chain B — The draught symptom

> **GT-6 + A7 → the top floor is the pressurised zone, so cold inleakage predominantly occurs low in the house, not at top-floor windows → the top-floor "draught" is most likely (i) convective downdraught off cold glass and radiant asymmetry, and (ii) warm-air loss through ceiling penetrations → neither is fixed by whole-house window replacement alone, and only (ii) is fixed by insulation *if the hatch and penetrations are sealed* → sealing the ceiling plane is a separate, near-free task that must be done alongside either option. [MEDIUM confidence — depends on unverified A7; a smoke-pencil or thermal-camera check on a windy day resolves it to HIGH]**

Downdraught off cold glass is real and is the one thing insulation genuinely does not fix. But the first-principles remedy for a 4.8 W/m²K surface is to raise its U-value — and **secondary glazing** or heavy lined curtains with a pelmet does that for roughly 5–10% of replacement cost. Replacement windows are not the only route to that outcome.

### Chain C — Second-order effects of the recommendation

1. **2nd order:** Insulating the ceiling makes the loft void colder. **3rd order:** any water tank, pipework or condensing-boiler condensate line in the loft moves closer to freezing → *mitigation: insulate pipes and tank sides/top, and never lay insulation directly beneath a tank.*
2. **2nd order:** Sealing the ceiling plane reduces the accidental ventilation rate. **3rd order:** moisture that was previously exfiltrating now stays indoors → condensation and mould risk on the coldest remaining surface, which will be the windows you did *not* replace → *mitigation: deliberate ventilation — extract fans in kitchen/bathroom, trickle vents or purge ventilation.* This is the one effect that materially qualifies the recommendation.
3. **2nd order:** A colder loft with a warm, moist ceiling below can drive interstitial condensation on the roof underside. **3rd order:** rot in rafters → *mitigation: keep eaves ventilation paths clear; do not block them with insulation.*

None of these contradict a Ground Truth, so the conclusion stands with mitigations attached rather than returning to Phase 2.

---

## 5. Abandoned Reasoning

- **"Windows are the visible cold surface, so windows are the problem."** Abandoned: this reasons from perception, not from U × A. Glass *feels* colder to the hand and to radiant exchange, but GT-4 says the ceiling is 2.5–4× the area, and an uninsulated ceiling's U-value is within a factor of two of single glazing's. The larger loss is overhead, unseen.
- **Reasoning by analogy from "everyone replaces their windows first."** Abandoned per the no-analogies rule. Its ground truth is a fact about *sales channels and visible kerb appeal*, not about heat transfer.
- **Framing the question as a strict either/or.** Deliberately abandoned as a false dichotomy, and this is the highest-value abandoned branch. By GT-5 and A8, a budget sized for whole-house glazing is 10–20× the cost of loft insulation. The two options are not comparable-cost alternatives; one is a rounding error against the other.
- **Heating-system causes (fishbone category 3).** Not pursued in depth because you asked a fabric question — but flagged honestly: if upstairs radiators are undersized, unbalanced, or valve-throttled, a cold top floor is a *distribution* fault, and no amount of fabric spend fixes it. Balancing the system costs near zero. Check this before spending anything.

---

## 6. Conclusion

**Insulate the attic.** [HIGH confidence, conditional on GT-7? and GT-8?]

It buys 5–15× more heat-loss reduction per pound (Chain A), pays back in single-digit years against windows' multi-decade payback that outlives the product, and it is irreversible-in-a-good-way: mineral wool does not degrade, whereas sealed units do.

**But the real answer is that your budget is not actually constrained to one option.** The correct plan, ranked by return per pound:

1. **Balance the heating system and check top-floor radiator sizing** — near-free; rules out a distribution fault that no fabric measure would fix.
2. **Insulate the loft to ~300 mm, and seal + insulate the loft hatch and all ceiling penetrations** — the hatch sealing is the part most often skipped and is what actually addresses the draught (Chain B). Add pipe/tank insulation per Chain C.
3. **Ensure deliberate ventilation** — mandatory, not optional, per Chain C effect 2.
4. **Spend the large remainder on the glazing problem selectively**: secondary glazing or draught-strip-plus-heavy-lined-curtains on the coldest top-floor rooms, and full replacement only for windows that are genuinely failing (rot, broken seals, insecure). Judge those on condition, not on energy.

That sequence gets you all of the insulation benefit, most of the glass-comfort benefit, and leaves money unspent.

**The ranking flips if any of these hold — verify before acting:**
- **The top floor is a loft conversion / room-in-roof** (GT-8?). Then there is no attic to insulate cheaply, insulation means rafter-level work at far higher cost, and the two options become genuinely comparable. *Check: is there a hatch to an empty void above?*
- **The loft is already at 100 mm+** (GT-7?). Topping up 100 → 300 mm saves roughly 12 W/K rather than 107 — an order of magnitude less. Still cheap enough to be worth doing, but the margin over windows narrows sharply. *Check: put a ruler in the loft.*
- **Windows are rotten, insecure, or have failed units.** Then they are a maintenance liability, and the analysis above simply does not apply — you replace them because they have failed, not because of their U-value.

**Weakest link, stated plainly:** the entire recommendation rests on GT-7? and GT-8?, both unverified and both resolvable in ten minutes with a ladder and a ruler. Do that before you spend anything.agentId: ac88eff697cddae02 (use SendMessage with to: 'ac88eff697cddae02', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 34994
tool_uses: 0
duration_ms: 100435</usage>
