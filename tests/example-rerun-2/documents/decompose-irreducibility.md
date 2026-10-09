# First-Principles Analysis: Molten-Salt Electro-Thermal Storage Claim

## Verdict: **False** (the efficiency claim is physically impossible as stated; the cost-competitiveness claim is unsupported for the system described)

The claim bundles two assertions that must be checked separately: (1) round-trip efficiency >85%, and (2) cost-competitiveness with Li-ion at the same nameplate capacity. Assertion (1) fails a hard physical-law test. Assertion (2) fails on economic structure even before efficiency is considered.

---

## 1. Essence of the claim

Strip the framing: *does a standalone 5 MWh sensible-heat molten-salt store, charged resistively and discharged through a heat engine, return >85% of the input electricity as electricity, at a cost per usable kWh competitive with Li-ion?*

## 2. Ground truths

- **GT-1 (physical law):** Carnot limit, η = 1 − T_cold/T_hot. At T_hot = 565 °C (838 K) discharging to a realistic condenser sink of 25–45 °C (298–318 K): η_Carnot ≈ 62–64%. This is the *absolute* ceiling on converting the stored heat back to work — no real heat engine (Rankine, ORC, sCO2) exceeds it, and real cycles typically achieve 55–70% of the Carnot value.
- **GT-2 (engineering fact, read-at-source, search-confirmed):** Solar salt (60/40 NaNO₃/KNO₃) is the standard CSP tower/trough medium, operating ~270–290 °C (cold tank) to 565 °C (hot tank) — the claim's temperature range matches real CSP practice (e.g., Gemasolar-class systems).
- **GT-3 (literature, reported-by-delegate):** Real Carnot-battery round-trip efficiencies cluster 25–50% for simple single-hot-reservoir sensible-heat designs; the highest reported figures (SPIC "Chuno," "over 65%") require an *additional* engineered cold-side reservoir (down to −60 °C), which is a different, more complex system than a single 290–565 °C salt tank.
- **GT-4? (unverified for this specific scale):** Small (few-MW) Rankine/ORC turbines run at markedly lower cycle efficiency and higher $/kW than utility-scale turbines, due to isentropic losses, part-load operation, and poor economies of scale in the power block.
- **GT-5 (market data, reported-by-delegate):** Utility-scale Li-ion BESS installed costs are roughly $125–400/kWh (2024–2025 range depending on source/region), with real-world AC-AC round-trip efficiency of ~85–92%.
- **GT-6 (market data, reported-by-delegate):** Large CSP molten-salt tank storage costs ~$20–30/kWh-thermal, but this figure is realized only at hundreds-of-MWh scale with shared solar-field and power-block infrastructure.

## 3. Derivation chains

**Chain A — efficiency is impossible, not merely optimistic:**
GT-1 (Carnot ceiling ≈ 62–64% at 565 °C/ambient sink) → the discharge leg alone cannot exceed ~64%, regardless of engineering quality → even with a perfect (lossless) charging step and zero storage loss, round-trip electricity-to-electricity efficiency is capped below 64% → the claimed >85% exceeds the second-law ceiling by ~20+ points.
**Confidence: HIGH** (rests on GT-1, a physical law; no `?`-marked input; no credible rival reading of Carnot's theorem).

**Chain B — realistic multiplicative efficiency, decomposed:**
GT-1 + GT-3 (real cycles achieve 55–70% of Carnot) → discharge (heat→electricity) efficiency realistically ≈ 35–45% at utility scale, lower at small scale →
→ charging (electricity→heat, resistive) efficiency ≈ 95–98% (not Carnot-limited; this is where the "above 85%" intuition likely leaks in from, since charging alone looks nearly lossless) →
→ storage efficiency (thermal loss to ambient over the hold period) ≈ 90–98%, worse for a *small* 5 MWh tank than a large CSP tank (higher surface-area-to-volume ratio) →
→ multiplying the three legs gives a realistic standalone round-trip figure of roughly **25–40%**, not 85%.
**Confidence: MEDIUM** — GT-4 is `?`-marked (small-turbine efficiency at exactly 5 MWh/few-MW scale wasn't independently verified at source); the band would rise to HIGH with a vendor-specific small-ORC performance curve.

**Chain C — the "above 85%" figure is explainable as a conflation, not a measurement:**
Chain B's charging-only efficiency (~95–98%) is the only leg of this system that plausibly exceeds 85% → a claim quoting ">85% system efficiency" is consistent with someone citing *only the charging or storage leg* and mislabeling it as round-trip → this is the most likely origin of the number in the prompt, i.e., exactly the charge/storage/discharge conflation the question anticipated.
**Confidence: MEDIUM** (this is a diagnostic inference about the claim's likely error, not a measured fact — flagged as interpretive).

**Chain D — economics, independent of the efficiency error:**
GT-6 (favorable thermal $/kWh is a *large-CSP-scale* phenomenon, driven by shared solar-field/power-block/BOP costs) + GT-4? (small turbines are expensive per kW and inefficient) → a *standalone* 5 MWh unit must carry its own dedicated power block (turbine, condenser, cooling, heat exchangers, controls, freeze protection for the salt) with none of the cost-sharing that makes CSP-scale thermal storage cheap → the $/kWh for an isolated 5 MWh electro-thermal system is dominated by this fixed power-block overhead, not by tank cost, and does not benefit from the economies of scale that the GT-6 figure depends on →
→ combined with Chain B's ~25–40% round-trip efficiency (vs. Li-ion's ~85–92%), the system needs roughly 2–3× as much input electricity per unit delivered →
→ nameplate-capacity-only comparison is itself invalid: Li-ion and thermal systems decouple power (kW) and energy (kWh) differently (Li-ion economics scale with duration roughly linearly via added cells; this thermal system's economics are dominated by the fixed turbine/BOP cost regardless of tank size) → a fair comparison requires matching both power rating and duration, which the claim never specifies.
**Confidence: MEDIUM** — directionally robust (every input points the same way: worse efficiency, worse $/kWh at small scale, no duration match), but no vendor quote for a real 5 MWh standalone unit was located, so the magnitude is not pinned down. Rival reading: if this is actually a shared/retrofit addition to an *existing* CSP plant's power block (not a standalone product), the economics shift substantially — this rival is plausible and not ruled out by the evidence gathered, which is why the Conclusion is scoped explicitly to a "standalone" reading.

## 4. Key assumptions challenged

- *"Round-trip efficiency" meant electricity-to-electricity* (convention, confirmed — the claim's own wording, "round-trip electricity into heat and back," forces this reading; a looser reading as thermal-only efficiency would be a different, much weaker claim than the one stated).
- *A heat pump is used for charging* (untested belief — not stated, and irrelevant: heat pumps cannot economically reach 565 °C with useful COP, so resistive heating is the only realistic charging path at these temperatures; this doesn't change the second-law ceiling on discharge).
- *5 MWh is large enough to access CSP-scale BOP economics* (convention, rejected — 5 MWh is roughly 2 orders of magnitude below typical commercial CSP storage, e.g., Gemasolar ~1,100 MWh-thermal; small scale loses the cost-sharing that makes the $20–30/kWh figure possible).

## 5. Abandoned/rival readings

- **Rival ruled out by Chain A:** "Maybe 85% refers to a Carnot-battery with a cryogenic cold reservoir (à la SPIC Chuno) rather than simple sensible heat." Ruled out because the claim specifies only a 290–565 °C molten-salt tank with no cold-side thermal store — a materially different, more complex architecture than what's described.
- **Rival not ruled out:** "This is a thermal-storage retrofit integrated into an existing CSP plant's shared power block," which would improve the economics (Chain D) but not the fundamental efficiency ceiling (Chain A, which is scale- and integration-independent).

## 6. Conclusion

**Recommended approach / finding:** The claim is **false** as stated. The >85% round-trip efficiency figure exceeds the Carnot thermodynamic ceiling (~62–64% at 565 °C against any realistic ambient sink) for converting stored heat back into electricity — this is not an engineering shortfall but a second-law impossibility for this temperature spread (chain A). A realistic standalone round-trip figure for this exact configuration is **~25–40%** (chain B), with the best published real-world "Carnot battery" results (~50–65%) requiring an engineered sub-ambient cold reservoir not present in the claim's description. Cost-competitiveness with Li-ion at the same nameplate capacity is also unsupported: the favorable $/kWh economics of molten-salt storage are a large-CSP-scale, shared-infrastructure phenomenon, and collapse at 5 MWh standalone scale, where a dedicated small power block dominates cost and nameplate-kWh comparison ignores the power-rating/duration mismatch between the two technologies (chain D).

**Confidence:** HIGH on the efficiency falsification (physical law, chain A); MEDIUM on the cost-competitiveness conclusion (directionally consistent evidence from chains B and D, but no at-scale vendor cost data for a real standalone 5 MWh unit was verified at source — this is the input that would most change the picture if obtained).

**What would change this:** A vendor-quoted installed cost and measured round-trip efficiency for an actual standalone 5 MWh molten-salt electro-thermal unit, or confirmation that the proposal is really a CSP-integrated retrofit rather than standalone — either would let the MEDIUM-confidence economic conclusion be verified or revised. Nothing can change the HIGH-confidence physics verdict: 85%+ round-trip at 565 °C/ambient is not achievable by any heat engine.

---

**Sources** (search-result provenance — not independently opened at source, so treat magnitudes as indicative rather than verified):
- [SPIC "Chuno" 560°C Carnot battery, ESS News](https://www.ess-news.com/?p=7856) — fetched directly, read-at-source
- Solar salt composition/temperature range — multiple academic/NREL-adjacent sources (search-confirmed, reported-by-delegate)
- Carnot battery round-trip efficiency literature (various, 25–65% range) — reported-by-delegate
- NREL ATB / Lazard / Ember Li-ion BESS cost data — reported-by-delegate
- NREL CSP thermal storage cost ($20–30/kWh-th at scale) — reported-by-delegate

No files were written for this analysis — the complete reasoning is in this message.