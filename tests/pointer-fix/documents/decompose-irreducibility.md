## Essence

The claim bundles two separable assertions about a 5 MWh molten‑salt TES system running 290–565 °C:

1. **Technical**: electricity → heat → electricity round‑trip efficiency > 85%.
2. **Economic**: at that same 5 MWh nameplate, it's cost‑competitive with a Li‑ion BESS.

Both need to hold for the claim to stand. I'll test each against physics and current market data, then flag the definitional sleight-of-hand that makes "85%" sound plausible in the first place.

## What's actually true about the 290–565 °C range

290 °C (cold tank) and 565 °C (hot tank) aren't arbitrary numbers — they're almost exactly the design temperatures of commercial nitrate-salt CSP plants: Gemasolar (cold tank 290 °C, hot tank 565 °C) and Crescent Dunes (cold ~288 °C, hot 565 °C), both using Solar Salt with a steam Rankine power block. [Gemasolar — SolarPACES/NREL](https://solarpaces.nrel.gov/project/gemasolar-thermosolar-plant-solar-tres); [Crescent Dunes](https://jameystillings.com/PROJECTS-+-SERIES/CHANGING-PERSPECTIVES-%E2%80%A2-CRESCENT-DUNES/2). 565 °C is also close to the thermal decomposition ceiling of nitrate salts — it's not a free dial, it's the practical ceiling for this chemistry. So the claim is implicitly describing a scaled-down "electric CSP" / Carnot-battery architecture: resistive heaters charge the salt instead of a solar field, and a turbine-generator discharges it back to the grid.

## The efficiency claim: fails on physics, not just engineering

**The decisive constraint is Carnot, applied to the discharge leg alone.** A heat engine converting stored heat back to electricity, with source temperature 565 °C (838 K) and a realistic sink (ambient/condenser, ~25–40 °C, 298–313 K):

Carnot limit = 1 − T_c/T_h ≈ 1 − 298/838 to 1 − 313/838 ≈ **62–64%**

That's the *idealized, frictionless, infinite-time* ceiling for that one step — using the hottest possible source temperature, which is itself generous (the salt actually cools from 565→290 °C while giving up heat, so the real exergy-weighted bound is lower still).

Round-trip efficiency is a product of three sequential factors, each ≤ 1:
- Charge (resistive heating of salt): ~98–99% — this part really is near-free, it's simple Joule heating.
- Storage (standing losses over a real cycle): ~95–99% for a well-insulated tank.
- Discharge (heat → electricity via Rankine/ORC/sCO2): capped at ~62–64% by Carnot, and *real* turbines run well below their Carnot limit — Gemasolar-class steam Rankine power blocks operate around 35–42% thermal-to-electric.

Since the overall round trip can never exceed its most restrictive factor, **the system is capped at ~62–64% before engineering losses are even applied** — and realistically lands around:

0.98 (charge) × 0.97 (storage) × 0.40 (discharge) × 0.98 (generator/BOP) ≈ **37%**

even with an optimistic future sCO2 Brayton discharge (~50%), you get ≈ **47%**.

This isn't a pessimistic engineering estimate — it's corroborated by the literature on dedicated "Carnot batteries": published round-trip (power-to-power) efficiencies cluster at **30–70%**, with one highly optimized research design claiming up to ~81% under idealized conditions — never 85%, let alone "above" it. [Carnot battery efficiency survey](https://www.ess-news.com/2025/05/26/optimizing-carnot-batteries-for-renewables-storage/).

**So where does ">85%" actually come from?** It comes from a real but *different* technology: electric-heated thermal storage that delivers heat directly (no reconversion to electricity). Rondo Energy's firebrick heat battery, just brought online at 100 MWh scale, claims >97% round-trip efficiency — but that figure is electricity-in to **heat-delivered** (steam/hot air to an industrial process), not electricity-in to **electricity-out**. [Rondo 100 MWh heat battery](https://pv-magazine-usa.com/2025/10/17/rondo-energys-100-mwh-heat-battery-powered-by-20-mw-of-onsite-solar/). The claim in the prompt borrows that >85–97% figure but applies it to a power-to-power system, which is the conflation: **thermal storage/delivery efficiency and electrical round-trip efficiency are different quantities that differ by exactly the size of the heat-engine conversion step** — the step the Carnot bound constrains to ~40–50% in practice.

## The cost claim: also fails, independently

Even setting the efficiency problem aside, 5 MWh is the wrong scale for molten-salt TES economics to work:

- Two-tank molten salt storage cost has historically run $30–40/kWh-thermal at CSP scale (hundreds of MWh), and NREL's current real-world estimate is closer to **$60/kWh-thermal — about 4x the DOE SETO target of <$15/kWh-th** even at that larger scale. [NREL TES cost modeling](https://research-hub.nrel.gov/en/publications/developing-a-cost-model-and-methodology-to-estimate-capital-costs/). At 5 MWh, tank fixed costs (foundation, freeze-protection, piping, controls) don't shrink proportionally with volume, so $/kWh-th rises sharply — likely several hundred $/kWh-th.
- Note "5 MWh" of *electrical* output capacity, at ~40% discharge efficiency, requires roughly **12–14 MWh of thermal storage** — the small-scale cost penalty applies to that larger thermal quantity, not the nameplate number.
- Unlike Li-ion's commoditized inverter, the discharge side needs a small custom/semi-custom turbine-generator package (condenser, feedwater, cooling) — there's no mass-produced, cheap product at ~1 MW scale analogous to a BESS PCS, and small Rankine/ORC packages run well over $1,500–3,000/kW.
- Meanwhile, utility-scale Li-ion is already commoditized at **~$250–400/kWh installed** for 2024–2025 vintage systems (NREL ATB; costs rising further for short-duration/small systems due to fixed BOP amortized over less energy, but nowhere near the custom power-island penalty above). [NREL ATB utility-scale battery storage](https://atb.nrel.gov/electricity/2024/utility-scale_battery_storage).

The oft-cited TES cost advantage ("storage media is cheap, only the power block is expensive, so add more hours") only materializes at **long duration (8+ hours) and large scale (tens to hundreds of MWh)**, where cheap incremental salt/tank volume is amortized against one expensive power island. A 5 MWh short-duration system sits exactly where that logic doesn't apply — it's Li-ion's home turf.

## Conclusion

**The claim fails as stated, on both legs, and the two failures are connected by the same conflation.**

- **Efficiency**: >85% electricity-to-electricity round-trip at these temperatures is not an engineering shortfall — it's disallowed by the Carnot limit on the discharge step alone (~62–64% ceiling, ~35–50% realistic). Demonstrated Carnot-battery designs cluster at 30–70%. The >85–97% figures that genuinely exist in this temperature/technology space (e.g., Rondo) describe electricity-to-**heat** delivery with no reconversion — a different product.
- **Cost**: even granting the efficiency claim, 5 MWh is below the scale/duration threshold where molten-salt TES's economics beat Li-ion; small-scale tank diseconomies plus a non-commoditized turbine-generator package make it more likely to cost *more* per kWh than Li-ion at this size, not competitive.
- **The claim only becomes defensible if silently redefined** as an electric-heat-delivery system (no power reconversion) compared against a Li-ion battery delivering electricity — at which point it's no longer the "round-trip to electricity" system the prompt describes, and the cost comparison becomes apples-to-oranges (heat vs. electricity), not a validation of the original statement.

**Confidence: high** on the efficiency conclusion (it rests on the Carnot limit, a hard physical bound, independently corroborated by published Carnot-battery performance data and by Rondo's own heat-vs-electricity distinction). **Medium-high** on the cost conclusion (directionally robust — small-scale/short-duration TES economics are a well-established disadvantage — but the exact $/kWh gap depends on vendor-specific design choices I haven't priced out in detail).