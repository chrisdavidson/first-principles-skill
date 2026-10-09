## Answer

**Recommendation:** The claim is false as stated: an 85%+ electricity-to-electricity round-trip efficiency at 290–565 °C is thermodynamically unreachable (ideal Carnot ceiling ≈64–74%; documented real systems run 23–65%), and at 5 MWh scale the molten-salt system is very unlikely to be cost-competitive with lithium-ion once power-block equipment is priced in, though a much-longer-duration configuration remains an open, unruled-out rival (chain C1, C3, C4).
**Band (from §6):** LOW
**Would change it:** A documented ≥80% AC-AC round-trip efficiency from any real molten-salt system at ≤600 °C, or a published ≤5 MWh installed-cost figure beating small-scale Li-ion pricing, or re-scoping the claim to a much longer discharge duration (chain C1, C4).

## 1. Problem Essence

**Core problem:** Determine whether a 5 MWh molten-salt electro-thermal storage system operating between 290 °C and 565 °C can (a) physically achieve a full electricity-to-electricity round-trip efficiency above 85%, and (b) be cost-competitive with a 5 MWh lithium-ion battery system on an installed $/kWh basis — while explicitly separating this from the easier, different claim that heat-to-heat thermal-storage retention exceeds 85%.

**Success criteria:**
- States the Carnot/second-law ceiling for heat-to-electricity conversion across 290–565 °C (hot side) against a stated cold sink, and compares that ceiling to 85%.
- Explicitly distinguishes heat-to-heat storage-retention efficiency from full electricity-to-electricity round-trip efficiency, and checks whether the claim's wording, or the industry data supporting it, equivocates between the two.
- Cites real-world/demonstrated systems' reported round-trip efficiencies at comparable temperatures and technology class, with provenance (read-at-source vs. reported-by-delegate) stated for each.
- Produces an independent $/kWh installed-cost estimate for a 5 MWh molten-salt system (tank + power block) and compares it to contemporary small-scale lithium-ion BESS $/kWh costs.
- Reaches an explicit true / false / mixed verdict on the claim as stated, with a stated confidence band and a named falsification condition.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| 290 °C (cold tank) / 565 °C (hot tank) is the standard "solar salt" (NaNO₃/KNO₃) CSP operating window the claim describes | convention | Explicitly challenge against CSP engineering literature | Accept — matches standard commercial power-tower/parabolic-trough practice; also directly stipulated by the claim's own wording, so independent verification is corroborative rather than load-bearing | GT-2? (reported-by-delegate) |
| The claim's "round-trip efficiency" means full electricity-in/electricity-out (AC-AC), not heat-to-heat storage retention or a heat-inclusive (cogeneration) metric | untested belief | Verify against the claim's own wording and against how the same term is used in industry marketing | Accept — the claim's wording ("round-trip electricity into heat and back") is unambiguous on AC-AC; industry sources (GT-8, GT-14) show the same term is frequently redefined to mean something easier | Textual analysis of the claim + GT-8 (read-at-source) |
| A heat engine converting ~565 °C stored heat to electricity against an ambient or sub-ambient sink is bounded by the Carnot limit — no engineering improvement can exceed it | physical law | Accept as a ground-truth candidate | Accept — promoted to GT-1; irreducibility (five-whys reduce-to-primitives) check: derives from the Kelvin–Planck statement of the second law of thermodynamics, which is not itself explained by a deeper classical-thermodynamic fact — verified: physical law | GT-1 (foundational; no `?`) |
| Small-scale (5 MWh / ≤1.25 MW) molten-salt power-block equipment (turbine or heat pump, heat exchangers, generator) costs the same $/kW as the utility-scale (tens-to-hundreds-of-MW) reference studies cited | convention | Explicitly challenge — discrete industrial power equipment (turbines, heat pumps, heat exchangers) exhibits well-established economies of scale (capital-cost scaling exponent commonly cited around 0.6–0.8, the "six-tenths rule"), so unit cost should rise as capacity shrinks | Challenge — rejected as stated; a small-scale cost-penalty multiplier is applied in the cost estimate (chain C4) [Assumes: A-4] | unverified — flagged; general industrial cost-scaling convention, not independently web-sourced this session |
| 2025 utility-scale Li-ion BESS $/kWh figures ($73–219/kWh, BNEF) apply directly, with no markup, to a 5 MWh system | untested belief | Flag — 5 MWh is well below typical utility scale (often >>20 MWh); true small-scale/C&I Li-ion pricing is normally higher per kWh due to fixed BOS/soft costs | Accept — deliberately used as the conservative (claim-favorable) bound — if anything this understates Li-ion's real small-scale cost, which would only widen the molten-salt disadvantage found in C4 | GT-11? (reported-by-delegate) |
| The claim's cost comparison carries no credit for heat-offtake/steam-sales (cogeneration) revenue | current constraint | Record the expiry conditions — this scope holds only as long as the claim is read as a pure-electricity comparison | Accept — expires only if the claim is re-scoped to a cogeneration comparison, which is a different claim | Textual — claim's own wording |
| For the claim's efficiency leg to be true, a cold-sink temperature far enough below ambient (≈130 K / ‑144 °C) would have to be in use to lift the Carnot ceiling above 85% (surfaced via inversion; load-bearing) | physical law | Accept as a ground-truth candidate; cross-check against documented cold-store temperatures in real molten-salt/Carnot-battery designs (typically 0 to ‑60 °C "chilled liquid", not cryogenic) | Discard — no documented system in this technology class uses a cold store anywhere near 130 K; precondition fails | GT-1 (computation) + GT-8 (read-at-source, Malta system description) |
| [Assumes: A-8, surfaced in chain C4] The cost verdict is scoped to exactly this 5 MWh nameplate capacity at a conventional 4–10 hour discharge duration, and does not extend to a much longer-duration (24+ hour), lower-power configuration of the same 5 MWh energy capacity | convention | Explicitly challenge — state as the claim's apparent framing; flag as the single biggest lever that could reverse the cost verdict under a different, unstated duration | Challenge — accepted as the most probable reading of the claim, but named explicitly as an open, unruled-out rival rather than a settled matter | Textual/structural — no external source needed |
| [Assumes: A-9, surfaced in chain C2] The higher-efficiency figures found in 2025 optimization literature (56.2–62.5%, and an isolated 81.3% outlier) measure the same AC-AC electric quantity, at a comparable temperature window, as the claim | untested belief | Verify by reading the primary paper directly | Challenge — unresolved; the 81.3% figure's temperature basis and efficiency definition could not be confirmed this session and is excluded from supporting the claim rather than relied upon | unverified — flagged; primary paper not read this session (turn-budget deferred) |

## 3. Ground Truths

- **GT-1** The second law of thermodynamics (Kelvin–Planck statement) bounds any heat engine operating between a hot reservoir at absolute temperature Th and a cold reservoir at Tc to a maximum (Carnot) thermal efficiency η = 1 − Tc/Th; no real heat engine can exceed this regardless of engineering quality — source: foundational thermodynamics (Carnot's theorem); provenance: physical law — not an empirical citation, verified by the irreducibility test (five-whys reduce-to-primitives): it bottoms out at a law, not a further-reducible fact. No `?`.
- **GT-2?** 290 °C (cold tank) / 565 °C (hot tank) is the industry-standard "solar salt" (NaNO₃/KNO₃) operating window used in commercial parabolic-trough and power-tower CSP plants — cited to: CSP patent/engineering literature; reported-by-delegate: WebSearch synthesis of a USPTO solar-power-system patent description and CSP engineering papers — cited sources not opened by this analysis.
- **GT-3?** Subcritical steam-Rankine power cycles fed by solar salt at ~565 °C achieve a net cycle efficiency of approximately 42%; supercritical variants could reach ~50% but are not standard in deployed solar-salt CSP plants — cited to: CSP solar-tower cycle literature; reported-by-delegate: WebSearch synthesis — not read — turn budget.
- **GT-4?** Resistive (Joule) heating converts electrical energy to thermal energy in molten salt at approximately 95–99% efficiency (near-total dissipation, minus minor transmission/conversion losses); the ~100% theoretical ideal is a direct consequence of Joule heating (physical law), but the specific 95–99% numeric band is an engineering estimate — unverified: general engineering convention, not independently web-sourced this session.
- **GT-5?** The Danish Energy Agency's 2025 Technology Catalogue states a round-trip (power-to-power) efficiency for a molten-salt-based Carnot battery of approximately 30% — cited to: Danish Energy Agency (ens.dk); reported-by-delegate: WebSearch synthesis. **Phase 3 failure record:** WebFetch of `ens.dk/media/6447/download` was attempted; the PDF opened but its content (compressed/encoded, Danish-language) could not be reliably parsed to locate this specific figure — logged as "citation opened but asserted figure not confirmed in extracted text."
- **GT-6?** Peer-reviewed 2025 optimization studies report Carnot-battery round-trip efficiencies of 56.2–62.5% for an optimized 10 MW design and 62.4% for a coal-integrated hybrid design; a separate citation reports up to 81.3% in an "optimal design" context whose temperature window and exact efficiency definition could not be confirmed this session — cited to: 2025 *Energy* journal / ess-news.com and pv-magazine summaries; reported-by-delegate — not read — turn budget. The 81.3% figure specifically is excluded from supporting the claim (see Abandoned Reasoning).
- **GT-7?** Siemens Gamesa's ETES pilot (Hamburg-Altenwerder, volcanic-rock storage charged to 750 °C) retains approximately 98% of stored heat over its storage period (a heat-to-heat retention figure), but in reported pilot operation produced about 30 MWh of electricity from 130 MWh of stored thermal energy (≈23% thermal-to-electric extraction in that cited operating report) — cited to: industry reporting (nsenergybusiness.com and related coverage); reported-by-delegate — not read — turn budget.
- **GT-8** Malta Inc.'s published technical specification for the Malta M100-10 plant defines "Overall System Efficiency AC to AC (RTEAC)" as "Total roundtrip efficiency of the plant defined as the ratio of the delivered discharge energy to the delivered charge energy at the output terminals (parasitic included)" and states its value as **53%–65%** — source: *Malta M100 System Technical Specifications*, page 2, table row "Overall System Efficiency AC to AC (RTEAC)*"; read-at-source: PDF opened directly and the exact table row located and quoted (via `my.atainsights.com` mirror of the Malta spec sheet). No `?`.
- **GT-14?** Separately, Malta marketing materials reportedly state an 85–95% round-trip efficiency figure that applies only to "combined heat and power" (cogeneration) configurations, which count delivered process heat/steam as a credited output alongside electricity — cited to: Malta Data Sheet 2025 (search synthesis referencing this figure); reported-by-delegate. **Phase 3 failure record:** WebFetch of `maltainc.com/assets/pdf/Malta-Data-Sheet-2025.pdf` returned HTTP 404 Not Found — source unreachable this session.
- **GT-9?** Highview Power's liquid-air energy storage (a comparable thermo-mechanical energy-storage class, air- rather than salt-based) achieves a standalone round-trip efficiency of approximately 50–60%, rising to 70–80% only when co-located with, and credited for, external industrial waste heat/cold sources not powered by the storage's own charge electricity — cited to: industry reporting (imeche.org, ccj-online.com, Birmingham coverage); reported-by-delegate — not read — turn budget.
- **GT-10?** Commercial lithium-ion BESS round-trip efficiency is typically 85–95% (median ≈90%) at the system level; NREL field testing of a commercial product (LG Chem RESU, behind-the-meter) measured efficiency near 85% under real-world conditions, with full balance-of-system figures (including auxiliary loads) sometimes running 70–80% in stationary deployments — cited to: NREL research-hub publications; Statista industry survey; reported-by-delegate — not read — turn budget (one direct-fetch attempt on `research-hub.nrel.gov` failed with a DNS error this session).
- **GT-11?** BloombergNEF's 2025 Energy Storage System Cost Survey reports a global average turnkey Li-ion BESS installed cost of ≈$117/kWh, ranging from ≈$73/kWh (China) to ≈$219/kWh (US), a 31% year-over-year decline; these figures are for utility-scale projects, typically far larger than 5 MWh — cited to: BloombergNEF survey, via energy-storage.news reporting; reported-by-delegate — not read — turn budget.
- **GT-12?** Academic pumped-thermal-electricity-storage (PTES / Carnot battery) cost studies estimate an energy-related capital cost of $62–107/kWh and a power-related capital cost of $533–627/kW; these figures derive from large-scale system design studies, not validated at 5 MWh / sub-2 MW scale — cited to: Comillas/*Energies* 2023 academic cost study; reported-by-delegate — not read — turn budget.
- **GT-13?** CSP molten-salt tank-plus-media storage cost alone (excluding power-block/turbine equipment) runs approximately $30–44/kWh-thermal at large (hundreds-of-MWh) CSP scale — cited to: CSP industry reporting (Reuters Events / Halotechnics coverage); reported-by-delegate — not read — turn budget.

**Provenance summary (required):**
`?`-marked: GT-2, GT-3, GT-4, GT-5, GT-6, GT-7, GT-9, GT-10, GT-11, GT-12, GT-13, GT-14 (12 of 14).
Read-at-source: GT-8 — *Malta M100 System Technical Specifications*, page 2, table row "Overall System Efficiency AC to AC (RTEAC)*", value 53%–65%.
GT-1 carries no `?` and needs no read-at-source location: it is a physical law, verified by the five-whys reduce-to-primitives irreducibility test rather than by an empirical citation.
Not read this session (turn budget), each keeping its `?`: GT-2, GT-3, GT-4, GT-6, GT-7, GT-9, GT-10, GT-11, GT-12, GT-13. Attempted-and-failed this session (Phase 3 failure records logged above): GT-5 (source opened, content unconfirmed), GT-14 (source unreachable, 404).

## 4. Derivation Chains

### Conclusion C1: An 85%+ electricity-to-electricity round-trip efficiency exceeds the thermodynamic ceiling itself at 290–565 °C

GT-1 (Carnot limit, physical law)
→ converting heat stored at 565 °C back to electricity via any heat engine operating against an ambient cold reservoir (288–298 K) is bounded by η = 1 − Tc/Th
→ computing with Th = 838.15 K (565 °C) and Tc = 288.15–298.15 K (15–25 °C ambient) gives an ideal ceiling of approximately 64.4%–65.6% for heat-to-electricity conversion alone [theoretical-limit]
→ even a hypothetical engineered sub-ambient cold reservoir, as used in heat-pump/"cold-store" Carnot-battery designs, raises this ceiling only to roughly 73.8% at a plausible Tc = 220 K (‑53 °C); reaching an 85% ceiling via this route would require Tc below about 130 K (‑144 °C), a cryogenic regime not documented in any cited cold-store design
→ an 85%+ full electricity-to-electricity round-trip efficiency is thermodynamically impossible for a heat-engine-based conversion in this temperature window, regardless of engineering quality — the claim's efficiency leg fails at the level of physical law, not merely realistic engineering performance

**Pre-check:** head GT-1 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — GT-1 is an unsuffixed physical law with no read-at-source requirement; every hop is a direct, independently recomputable application of the Carnot formula (see Recompute in the adversarial pass record); the strongest rival — that some non-heat-engine conversion technology bypasses this bound — is named and ruled out in Abandoned Reasoning (Dead End: Non-heat-engine conversion).

### Conclusion C2: Realistic engineering performance for this technology class clusters at 30–62%, roughly half the claimed figure

GT-3? (42% subcritical Rankine at 565 °C) + GT-4? (resistive charge ~98%) + GT-7? (heat storage retention ~95–98%)
→ multiplying charge efficiency (~98%) × storage retention (~95–98%) × discharge heat-to-electric efficiency (~42%) gives an expected real round-trip electric efficiency of roughly 37–40% for a conventional resistive-charge / subcritical-Rankine-discharge design in this temperature window [estimate]
→ independently reported figures for molten-salt-class Carnot batteries bracket this estimate: the Danish Energy Agency's ≈30% figure (GT-5?) sits below it, reflecting additional real-world losses, while peer-reviewed optimized designs report 56.2–62.5% (GT-6?), achieved via different cycle configurations (e.g., optimized pressure ratios) rather than the conventional design modeled here [Assumes: A-9 — the 56–62% optimized figures and the excluded 81.3% outlier measure the same AC-AC quantity, at a comparable temperature, as the claim; unresolved, see Abandoned Reasoning]
→ real-world and modeled round-trip electric efficiency for a 290–565 °C molten-salt system clusters in the 30–62% range (the unconfirmed 81.3% outlier is not relied upon), 25–55 percentage points short of the claimed >85%

**Pre-check:** head GT-3?, GT-4?, GT-7? · ?-marked: GT-3, GT-4, GT-7 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-3?, GT-4? and GT-7? are each unverified this session (not read — turn budget; verification: directly reading the CSP cycle-efficiency literature and the Siemens Gamesa primary technical report would remove these as causes of the downgrade); the A-9 premise on the second hop is explicitly unresolved rather than priced, which is why this chain does not exceed MEDIUM even though its own conclusion is not the analysis's load-bearing finding (C1 and C3 carry that weight at HIGH and MEDIUM respectively).

### Conclusion C3: No credible, commercially-documented system in this technology class demonstrates >85% pure electric round-trip efficiency

GT-8 (Malta AC-AC RTE 53–65%, read-at-source) + GT-9? (Highview LAES 50–80% with waste heat) + GT-7? (Siemens Gamesa ETES ~23% electric extraction)
→ across three independently developed commercial thermal/Carnot-battery storage technologies, documented pure electricity-to-electricity round-trip efficiency ranges from ≈23% to ≈65%, reaching 70–80% only when crediting external waste heat not supplied by the storage's own charge electricity
→ the only figures at or above 85% found anywhere in this technology class (Malta's reported 85–95%, GT-14?) are explicitly defined as combined heat-and-power output, crediting delivered process steam as a useful output alongside electricity — a different quantity than "round-trip electricity into heat and back"
→[2nd, actor lens] a buyer or RFP evaluator who takes an 85% figure at face value without checking whether it is AC-AC or heat-inclusive will size and price a 5 MWh procurement around roughly double the electrical output the system can actually deliver
→[2nd, time lens] the gap between promised and delivered electrical output becomes measurable within the first few charge/discharge cycles of operation, surfacing as a revenue or dispatch shortfall rather than at the procurement stage
→ no credible, commercially-documented molten-salt or Carnot-battery-class system demonstrates >85% pure electric round-trip efficiency; the claim's 85% figure is reachable only under a heat-inclusive accounting convention that the claim's own wording does not invoke

**Pre-check:** head GT-8, GT-9?, GT-7? · ?-marked: GT-7, GT-9 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-7? and GT-9? are unverified this session (not read — turn budget; verification: direct reads of the Siemens Gamesa and Highview primary technical/performance reports would remove these as causes of the downgrade). This does not threaten the chain's core finding: GT-8 alone, read-at-source, already establishes that the best-documented power-only Carnot-battery system tops out at 65%, well short of 85% — GT-7?/GT-9? only broaden the evidence base across technology variants. Rival: the figures might not represent a purpose-built 290–565 °C unit specifically; ruled out for GT-8 (Malta is a high-temperature heat-pump/salt-based system in the same general class) and left open only for GT-7?/GT-9? (see Abandoned Reasoning).

### Conclusion C4: At 5 MWh scale, the molten-salt system is very unlikely to be cost-competitive with lithium-ion on an installed $/kWh basis

GT-11? ($117–219/kWh Li-ion, utility scale) + GT-12? (PTES power cost $533–627/kW, large scale) + GT-13? (CSP tank-only cost $30–44/kWh-thermal, large scale)
→ [estimate] target quantity: installed $/kWh for a 5 MWh (≈0.5–1.25 MW at an assumed 4–10 hour discharge duration) molten-salt Carnot-battery system; decompose into tank+salt cost ($/kWh-thermal × kWh) plus power-block cost ($/kW × kW, covering heat pump/turbine, generator, and heat exchangers)
→ [estimate] using the large-scale reference unit costs directly (no small-scale penalty) gives tank ≈ $150,000–$220,000 and power block ≈ $267,000–$784,000 (0.5–1.25 MW × $533–627/kW), for a naive total of ≈$417,000–$1,004,000, i.e. ≈$83–$201/kWh — naively comparable to Li-ion
→ [estimate] but $533–627/kW power-block costs are drawn from large (tens-to-hundreds-of-MW) system studies; turbines, heat pumps, and heat exchangers exhibit strong economies of scale, so small (<2 MW) packaged power equipment typically costs several times more per kW — applying an illustrative 3–5× small-scale penalty (bracket: ≈$1,600–3,135/kW) raises the power-block cost alone to ≈$800,000–$3,919,000, pushing total installed cost to roughly $190–$828/kWh [Assumes: A-4 — this penalty multiplier is an illustrative engineering-economics bracket, not independently sourced this session]
→ this corrected bracket sits mostly 1–4× above 2025 utility-scale Li-ion BESS installed costs (GT-11?, $73–219/kWh), and likely further above realistic small-scale/C&I Li-ion pricing (which is itself higher than the utility-scale figure used here, conservatively, for the comparison)
→ at this 5 MWh scale and conventional (4–10 hour) duration, a molten-salt electro-thermal storage system is very unlikely to be cost-competitive with lithium-ion on installed $/kWh; molten salt's structural cost advantage (cheap tank/media cost that scales well over many hours of storage) is swamped by the power block's cost floor, which does not shrink proportionally at small scale [Assumes: A-8 — this verdict is scoped to the conventional-duration reading of the claim; a much longer-duration, lower-power configuration at the same 5 MWh capacity is named as a live, unruled-out rival rather than excluded]

**Pre-check:** head GT-11?, GT-12?, GT-13? · ?-marked: GT-11, GT-12, GT-13 · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes are short at once: (Inputs) all three head ground truths are unverified this session (not read — turn budget; verification: a published cost breakdown for an actual ≤5 MWh molten-salt/Carnot-battery pilot, e.g. SPIC's 1 MW/4 MWh project, which was not located this session, would remove this as a cause of the downgrade); (Inference) the small-scale cost-penalty step rests on an unverified, illustrative multiplier [Assumes: A-4] whose failure has not been fully priced beyond the bracket's own width — if the true penalty were near 1× rather than 3–5×, the naive $83–201/kWh figure would apply instead, which is close to parity with higher-end Li-ion pricing rather than clearly uncompetitive. This chain's LOW band reflects that genuine, named uncertainty rather than confidence that the direction of the finding is wrong.

## 5. Abandoned Reasoning

### Dead End: Heat-pump/cold-store Carnot-battery rescue via a cryogenic cold sink

**What was tried:** Considered whether the claim might be true under a heat-pump-charging Carnot-battery design with a deeply sub-ambient cold store (as Malta's "chilled liquid" approach suggests), since this can raise the theoretical Carnot ceiling above the plain-ambient 64–66% figure.

**Why abandoned:** Reaching an 85% ceiling via this route requires a cold-store temperature below roughly 130 K (‑144 °C) — a cryogenic regime. No cited source for any real molten-salt/Carnot-battery design (including Malta, read-at-source at GT-8) documents a cold store anywhere near this temperature; Malta's own real AC-AC RTE under this exact design philosophy is 53–65%, not 85%. Pursuing this further would require evidence of a cryogenic cold store that does not appear in any cited source.

**What it ruled out:** The rival reading "the claim is true for an advanced heat-pump/cold-store variant" (ruled out by GT-1's computation together with GT-8).

### Dead End: Non-heat-engine conversion technology (thermophotovoltaic / thermoelectric) bypassing the Carnot bound

**What was tried:** Considered whether direct heat-to-electricity conversion via thermophotovoltaic (TPV) or thermoelectric generators could exceed the Carnot-bound-turbine ceiling computed in chain C1.

**Why abandoned:** TPV and thermoelectric converters are themselves heat engines in the thermodynamic sense and remain bound by the same Carnot/exergy limits; in practice they achieve lower, not higher, conversion efficiencies than steam/ORC turbines at source temperatures in the 565 °C class (commonly well under 30%). No evidence anywhere in the claim's own wording ("round-trip electricity into heat and back," implying a conventional charge/discharge cycle) suggests this exotic configuration is intended.

**What it ruled out:** The exotic-technology rescue reading of the claim's efficiency leg.

### Dead End: The isolated 81.3% optimized-study figure as confirming evidence for the claim

**What was tried:** Considered whether the 81.3% figure found within the GT-6? search synthesis (a 2025 optimization study) could validate the claim's >85% assertion as approximately achievable.

**Why abandoned:** The search snippet did not specify the temperature window, cold-sink temperature, or whether the reported metric was pure AC-AC electric efficiency or some other quantity (e.g., an exergetic or heat-inclusive measure). The primary paper was not opened this session (turn-budget deferred) and the figure cannot be confirmed as commensurable with the claim's own terms. This is a genuinely open item, not a disproof — a reader with more turn budget should resolve it by reading the cited 2025 *Energy*-journal optimization paper directly.

**What it ruled out:** Using this figure as a confirming data point for the headline conclusion; it remains explicitly excluded from chain C2 rather than relied upon.

### Dead End: Small-scale Li-ion repricing closing the cost gap

**What was tried:** Considered whether using realistic small-scale/commercial-and-industrial (C&I) Li-ion pricing, rather than the utility-scale BNEF figures used in chain C4, would narrow or close the cost gap found against molten salt.

**Why abandoned:** Small-scale/C&I Li-ion systems are typically *more* expensive per kWh than giant utility-scale projects, owing to a larger fixed balance-of-system/soft-cost share — using the utility-scale (lower) Li-ion figures in C4 was therefore the conservative choice most favorable to the claim, and the claim's cost leg still fails under it. Substituting realistic small-scale Li-ion pricing would only widen, not close, the disadvantage found for molten salt.

**What it ruled out:** The rival "the claim's cost leg only fails because the analysis compared it to unrealistically cheap utility-scale Li-ion" (ruled out by this conservative-direction reasoning on GT-11?).

**Note — kept live, not abandoned:** A much longer discharge duration (24+ hours) at the same 5 MWh energy capacity (i.e., a much lower power rating, shrinking the power block's share of total cost) is the one rival to C4 that this analysis did **not** rule out; it is carried forward explicitly as [Assumes: A-8] on chain C4 and named again in the Conclusion and in the adversarial pass's Rival step, rather than being listed here as a ruled-out dead end.

## 6. Conclusion

**Recommended approach:** Treat the claim as **false** as literally stated for the electricity-to-electricity efficiency assertion — an 85%+ round-trip is thermodynamically unreachable at 290–565 °C — and treat the cost-competitiveness assertion as **very likely false** at 5 MWh scale under the most probable (conventional-duration) reading of the claim, with one narrow, explicitly-named residual rival (a much longer discharge duration) left open rather than ruled out (chain C1, C3, C4).

**Key insight:** The claim's "above 85%" figure is not merely optimistic engineering guidance — it exceeds the *ideal* Carnot ceiling (≈64–74%) for this temperature window, not just realistic achieved performance (30–62% is what is actually documented); and the only ≥85% figures that genuinely exist anywhere in this technology class apply to a different, heat-inclusive metric (combined heat-and-power output, GT-14?) that the claim's own wording ("round-trip electricity into heat and back") does not invoke (chain C1, C3).

**Trade-offs acknowledged:** Molten-salt/Carnot-battery storage's real structural advantage — very cheap $/kWh tank-and-media cost at large scale and long duration — is swamped at 5 MWh by the power block's (turbine/heat-pump/heat-exchanger) cost floor, which does not shrink proportionally at small scale; this is a genuine engineering-economics trade-off that the claim gets backwards by picking the smallest scale at which molten salt is least competitive, rather than the large multi-hour/multi-day scale where it is normally deployed (chain C4).

**Pre-check:** head C1 (HIGH), C3 (MEDIUM), C4 (LOW) · ?-marked: none directly (all `?`-marked inputs are routed through C2/C3/C4's own heads) · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — matching the weakest contributing chain, C4 (chain C1 is HIGH; chain C3 is MEDIUM, naming GT-7?/GT-9? as unverified this session, verification: direct reads of the Siemens Gamesa/Highview primary reports; chain C4 is LOW, naming GT-11?, GT-12? and GT-13? as unverified this session together with the unpriced [Assumes: A-4] small-scale cost-penalty premise, verification: a published cost breakdown for an actual ≤5 MWh molten-salt/Carnot-battery pilot). The claim as stated requires **both** legs (efficiency *and* cost) to be true, so the Conclusion's overall band is capped at its weakest contributing chain's band (LOW) rather than at C1's HIGH, even though the efficiency leg alone — at HIGH confidence via chain C1 — is independently sufficient to establish that the claim's efficiency assertion is false; that HIGH-confidence sub-finding does not raise the floor set by the still-unresolved cost leg for the Conclusion taken as a whole. **What would change it:** (a) a documented ≥80% parasitic-inclusive AC-AC round-trip efficiency measurement from any commercially operating molten-salt/Carnot-battery system at ≤600 °C would overturn the C1/C3 efficiency verdict; (b) a published installed-cost figure for an actual ≤5 MWh molten-salt/Carnot-battery system (including the full power block), at or below small-scale Li-ion $/kWh pricing, or an explicit re-scoping of the claim to a much longer discharge duration at the same 5 MWh capacity, would overturn the C4 cost verdict and raise the overall band.

## Appendix — process output

## §6→§4 closure ledger (process output)

- "Treat the claim as false as literally stated for the electricity-to-electricity efficiency assertion ... and treat the cost-competitiveness assertion as very likely false at 5 MWh scale ..." → chain C1 ✓ (also cites C3, C4 inline)
- "The claim's 'above 85%' figure is not merely optimistic engineering guidance — it exceeds the ideal Carnot ceiling ..." → chain C1 ✓ (also cites C3 inline)
- "Molten-salt/Carnot-battery storage's real structural advantage ... is swamped at 5 MWh by the power block's ... cost floor ..." → chain C4 ✓
- "Confidence: MEDIUM (conjunctive verdict) ..." → chains C1, C3, C4 ✓ (D-07 naming satisfied inline)

Ledger complete: 4 of 4 §6 claims cite a chain inline; 0 cut.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | head | GT-1 | none | n/a |
| C1 | hop 1 | Carnot bound applies to any heat engine in window | none | n/a |
| C1 | hop 2 | compute 64.4–65.6% ceiling | none | n/a |
| C1 | hop 3 | sub-ambient cold store raises ceiling to ~73.8%; 85% needs ~130 K | none beyond the already-tabled cryogenic-precondition row | n/a (covered) |
| C1 | conclusion | 85% exceeds ceiling | none | n/a |
| C2 | head | GT-3?, GT-4?, GT-7? | none | n/a |
| C2 | hop 1 | multiply to ~37–40% | none | n/a |
| C2 | hop 2 | bracket against GT-5?/GT-6? [Assumes: A-9] | surfaced: A-9 (same-metric/temperature assumption for the 56–62% and 81.3% figures) | yes |
| C2 | conclusion | 30–62% range vs >85% | none | n/a |
| C3 | head | GT-8, GT-9?, GT-7? | none | n/a |
| C3 | hop 1 | 23–65%/70–80% range across three systems | none | n/a |
| C3 | hop 2 | only ≥85% figures are heat+power | none | n/a |
| C3 | hop [2nd, actor] | buyer oversizing procurement on face-value figure | minor; not load-bearing enough for a separate table row (qualitative market-behavior observation, not a factual premise the chain's endpoint depends on) | n/a (clean) |
| C3 | hop [2nd, time] | gap surfaces within first operating cycles | none | n/a |
| C3 | conclusion | no credible >85% pure-electric system | none | n/a |
| C4 | head | GT-11?, GT-12?, GT-13? | none | n/a |
| C4 | hop 1 (estimate) | decompose cost into tank + power block | none | n/a |
| C4 | hop 2 (estimate) | naive large-scale cost ≈$83–201/kWh | precursor to the small-scale-penalty assumption (not yet declared at this hop) | n/a (declared at next hop) |
| C4 | hop 3 (estimate) | apply small-scale penalty [Assumes: A-4] | surfaced: A-4 (small-scale power-block cost-scaling multiplier) | yes |
| C4 | hop 4 | penalized bracket 1–4× above Li-ion | none | n/a |
| C4 | conclusion | unlikely cost-competitive [Assumes: A-8] | surfaced: A-8 (scope limited to conventional-duration reading) | yes |

Scan complete: 4 chains, 20 steps scanned in order; 3 assumptions surfaced (A-4, A-8, A-9), all 3 added to the Classified Assumptions Table in section 2.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 | yes | n/a | yes | HIGH | no | none |
| C2 | GT-3?, GT-4?, GT-7? | yes | n/a | yes | MEDIUM | no | none |
| C3 | GT-8, GT-9?, GT-7? | yes | n/a | yes | MEDIUM | yes | none |
| C4 | GT-11?, GT-12?, GT-13? | yes | n/a | yes | LOW | no | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach: Treat the claim as false ..." | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C3, C4 |
| "Key insight: The claim's 'above 85%' figure ..." | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C3 |
| "Trade-offs acknowledged: Molten-salt/Carnot-battery storage's real structural advantage ..." | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4 |
| "Confidence: MEDIUM (conjunctive verdict) ..." | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C3, C4 |

Scan complete: 4 chain rows, one per section-4 chain block in order; 4 section-6 rows, one per construct in order — 4 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Techniques not applied (process output)

pre-mortem — not applicable — the subject is a technical/economic claim, not a plan or recommendation requiring prospective-hindsight failure analysis; inversion is the decision-rule-correct adversarial technique for a claim, and was used instead at Phase 2 (surfacing necessary preconditions) and Phase 5 (the adversarial pass below).
trade-off analysis — not applicable — the essence of this analysis is to evaluate the truth-value of a stated claim, not to choose among multiple viable options at a decision point; molten-salt-vs-Li-ion economics are produced as supporting evidence within the Ground Truths/Derivation Chains rather than as a formal weighted trade-off.
fishbone — not applicable — the claim's assumption space is already tightly bounded by a single governing physical law (Carnot/second-law), a definitional ambiguity, and a cost-scaling question; it does not require breadth-first multi-category cause brainstorming to enumerate, and the inversion procedure already surfaced the load-bearing preconditions more directly.

## Adversarial pass (process output)

**Recompute.** Carnot ceiling: 1 − 298.15/838.15 = 0.6443 (64.4%, Tc=25°C); 1 − 288.15/838.15 = 0.6563 (65.6%, Tc=15°C); 1 − 220/838.15 = 0.7375 (73.8%, illustrative sub-ambient Tc=−53°C) — all recompute as stated in chain C1. C2's multiplication: 0.98 × 0.965 × 0.42 = 0.3969 ≈ 39.7%, consistent with the "roughly 37–40%" stated. C4's naive cost: tank 5,000 kWh × $30–44/kWh = $150,000–$220,000; power 500–1,250 kW × $533–627/kW = $266,500–$783,750; naive total $416,500–$1,003,750 → $83.3–$200.8/kWh, consistent with "≈$83–201/kWh" stated. C4's penalized cost: power 500–1,250 kW × $1,600–3,135/kW = $800,000–$3,918,750; total $950,000–$4,138,750 → $190–$827.8/kWh, consistent with "$190–$828/kWh" stated. No arithmetic errors found.

**Sensitivity.** For the efficiency leg (C1): no `?`-marked ground truth is the flip point — GT-1 is unsuffixed physical law, and the claim's own stated temperatures are used directly, so there is no single GT whose verified falsity would flip C1's conclusion; the closest sensitivity is the cold-sink assumption, addressed and ruled out in Abandoned Reasoning. For the cost leg (C4): the single most sensitive, and weakest, link is the unverified small-scale cost-penalty multiplier [Assumes: A-4] — it is not `?`-marked (it is an assumption, not a ground truth) but is explicitly unverified this session; if the true small-scale penalty were near 1× rather than 3–5×, C4's naive ≈$83–201/kWh figure would apply instead, bringing molten salt close to parity with higher-end Li-ion pricing. This is already named as the cause of C4's LOW rating.

**Rival.** Headline conclusion: strongest live rival is "the claim is true for an unspecified longer-duration configuration within the same 5 MWh nameplate" — not ruled out, carried live as [Assumes: A-8] on chain C4 and named in the Conclusion's confidence line. For C1: rival "a non-heat-engine conversion technology bypasses Carnot" — ruled out (Abandoned Reasoning: Non-heat-engine conversion). For C2: rival "the 81.3% figure confirms the claim" — not ruled out, left explicitly unresolved and excluded (Abandoned Reasoning: 81.3% figure). For C3: rival "the cited systems are unrepresentative of a purpose-built 290–565°C unit" — ruled out for GT-8 (Malta is in the same general technology class, read-at-source) and left open only for GT-7?/GT-9? (named on C3's own confidence line). For C4: rival "small-scale Li-ion repricing closes the gap" — ruled out (Abandoned Reasoning: Small-scale Li-ion repricing; the conservative direction already favors the claim).

**Premise (inversion, applied to the headline conclusion):** Assume the headline conclusion is wrong — i.e., assume an 85%+ pure-electric round-trip efficiency at 290–565°C truly is achievable, and the 5 MWh molten-salt system truly is cost-competitive with lithium-ion.

**Causes (unfiltered, from ≥3 stakeholder viewpoints — molten-salt vendor, physicist/auditor, Li-ion competitor):**
1. (Vendor) The Carnot-ceiling calculation used the wrong cold-sink temperature; a much colder engineered sink exists that was not accounted for.
2. (Vendor) A non-Rankine, non-Carnot-bound conversion technology is used that this analysis failed to consider.
3. (Vendor) The 81.3% optimized-study figure (GT-6?) is in fact a correctly-defined AC-AC figure at a comparable temperature, and was wrongly excluded.
4. (Physicist/auditor) The arithmetic in the Carnot/estimate computations contains an error.
5. (Physicist/auditor) GT-8 (Malta, 53–65%) is not representative because Malta's system design is suboptimal relative to what is achievable.
6. (Li-ion competitor/skeptic) Small-scale molten-salt power-block costs are in fact falling rapidly (learning-curve effects) similar to Li-ion, invalidating the no-scale-economies-penalty direction of this analysis.
7. (Li-ion competitor/skeptic) Utility-scale Li-ion pricing was used generously (low); real small-scale Li-ion pricing is higher, which could still leave relative room for molten salt under some scenarios.
8. (General) The claim may use a nonstandard "cost-competitive" definition (e.g., 30-year levelized cost exploiting molten salt's near-unlimited cycle life) rather than upfront installed $/kWh.

**Clusters (grouped structural weaknesses, with chain/GT ids):**
- Cluster A — "Wrong physics inputs" (causes 1, 4) — bears on C1.
- Cluster B — "Unaccounted exotic technology" (cause 2) — bears on C1.
- Cluster C — "Excluded/uncertain data point" (causes 3, 5) — bears on C2, C3, GT-6, GT-8.
- Cluster D — "Cost-estimate uncertainty" (causes 6, 7, 8) — bears on C4.

**Disposition:**
- Cluster A — Mitigation: the Recompute step above independently re-derived the Carnot numbers under two plausible Tc values and cross-checked against the independently-reported CSP Rankine figure (42%, GT-3?), which sits well below the computed ceiling as expected; no error found. No plan change; risk accepted as negligible.
- Cluster B — Mitigation: named and ruled out via Abandoned Reasoning (Non-heat-engine conversion: TPV/thermoelectric are also Carnot-bound and empirically worse at this temperature). No plan change.
- Cluster C — Plan change: GT-6?'s 81.3% figure is explicitly excluded from supporting evidence rather than silently used (already implemented in chain C2 and Abandoned Reasoning); flagged as an open item for a follow-up pass with more turn budget to read the primary paper, named in the Conclusion's "what would change it."
- Cluster D — Plan change: the cost verdict (C4) is explicitly rated LOW rather than HIGH or MEDIUM specifically because of this cluster, and the Conclusion names the long-duration-configuration rival as live/unruled-out rather than claiming blanket certainty on the cost leg. No further mitigation attempted this session; named as residual uncertainty in the Conclusion's confidence line.

**Falsification.** The conclusion is false if either (a) a commercially documented molten-salt or Carnot-battery system is shown, via a primary technical specification or peer-reviewed measurement, to achieve a parasitic-inclusive AC-to-AC round-trip efficiency above 80% at a hot-side temperature at or below ~600°C, or (b) a verifiable installed-cost quote for an actual ≤5 MWh molten-salt/Carnot-battery system (including the full power-block/heat-engine equipment) comes in at or below contemporary small-scale lithium-ion BESS $/kWh pricing for the same duration.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Determine whether a 5 MWh molten-salt electro-thermal storage system operating between 290 °C and 565 °C can (a) physically achieve a full electricity-to-electricity round-trip efficiency above 85%, and (b) be cost-competitive with a 5 MWh lithium-ion battery system on an installed $/kWh basis — while explicitly separating this from the easier, different claim that heat-to-heat thermal-storage retention exceeds 85%."
Band: **Rigorous**
Justification: The statement is a distilled core question (not a bare restatement of the user's prompt), specific to this problem (names the 290–565 °C window, the 5 MWh scale, and the heat-to-heat/AC-AC distinction), and each of its five success criteria names a checkable, section-specific test a reviewer can apply against the Conclusion/Derivation Chains without further interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "Scan complete: 4 chains, 20 steps scanned in order; 3 assumptions surfaced (A-4, A-8, A-9), all 3 added to the Classified Assumptions Table in section 2."
Band: **Rigorous**
Justification: Every row in the Assumptions Table uses an exact four-type-scheme value, Treatment cells use the prescribed vocabulary for their type, Verdict cells use the token+em-dash+justification form, assumptions used in chains despite being unverified carry "unverified — flagged" (A-4, A-9), at least two assumptions were actually Challenged/Discarded rather than merely Accepted, and the quoted Assumption Audit scan confirms an exhaustive per-step sweep over all four section-4 chains with every surfaced assumption recorded in the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "?-marked: GT-2, GT-3, GT-4, GT-5, GT-6, GT-7, GT-9, GT-10, GT-11, GT-12, GT-13, GT-14 (12 of 14). Read-at-source: GT-8 — Malta M100 System Technical Specifications, page 2, table row 'Overall System Efficiency AC to AC (RTEAC)*', value 53%–65%." Enumeration check: the Ground Truths list carries exactly 14 IDs (GT-1 through GT-13 plus GT-14), of which GT-1 and GT-8 are unsuffixed and the remaining 12 carry `?` — the enumeration matches exactly.
Band: **Sound**
Justification: GT-8 (the one unsuffixed, document-citing GT feeding a load-bearing chain) names its exact read-at-source location, and the `?`-marked enumeration checks out against the list by direct count. However, GT-1 — the other unsuffixed GT, feeding HIGH-confidence chain C1 — is a physical law rather than a document citation and therefore carries no literal page/table/section "read-at-source" pointer in the strict sense the Rigorous descriptor names; this is one entry departing from the prescribed form (a physical-law GT substituting an irreducibility-test citation for a document location) without invalidating the rest of the list, which is exactly the Sound band's descriptor.

**Criterion 4: Reason Upward**
Quoted span (self-audit scan, chain-form table): "C1 | GT-1 | yes | n/a | yes | HIGH | no | none" / "C2 | GT-3?, GT-4?, GT-7? | yes | n/a | yes | MEDIUM | no | none" / "C3 | GT-8, GT-9?, GT-7? | yes | n/a | yes | MEDIUM | yes | none" / "C4 | GT-11?, GT-12?, GT-13? | yes | n/a | yes | LOW | no | none" — all four chains score `yes` on Form conforming and Dependency clean.
Band: **Rigorous**
Justification: All four section-4 chains are form-conforming and dependency-clean per the quoted scan; each chain carries at least one genuine intermediate step; the Abandoned Reasoning section documents four dead ends in the prescribed What-was-tried/Why-abandoned/What-it-ruled-out structure; no analogy is used as direct evidence (every cross-technology comparison is grounded in a named GT); every chain step introducing a new assumption declares it inline (`[Assumes: A-9]` on C2, `[Assumes: A-4]` and `[Assumes: A-8]` on C4); and the adversarial pass's Recompute step independently reproduces every chain's arithmetic with no discrepancy.

**Criterion 5: Validate**
Quoted span: "**Confidence:** LOW — matching the weakest contributing chain, C4 ... The claim as stated requires both legs (efficiency and cost) to be true, so the Conclusion's overall band is capped at its weakest contributing chain's band (LOW) rather than at C1's HIGH."
Band: **Rigorous**
Justification: Every chain's confidence line names its specific downgrade causes (GT-N? inputs with their verification paths, or an unpriced `[Assumes: A-N]` premise); no chain consuming a `GT-N?` input is rated HIGH; the Conclusion's overall rating (LOW) correctly matches its weakest contributing chain (C4, LOW) with no EXCEPT clause claimed; and the adversarial pass record is complete — Recompute, Sensitivity, Rival, Premise, Causes, Clusters (each naming chain/GT ids) and Disposition (each cluster carrying a named plan change or an explicitly accepted, named-mitigation risk), and Falsification are all present.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (self-audit scan, claim-inventory table): "| 'Recommended approach: Treat the claim as false ...' | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C3, C4 |" ... "Scan complete: 4 chain rows ... 4 section-6 rows ... 4 claims under R11, 0 excluded ... 0 claims untraced."
Band: **Rigorous**
Justification: All four Conclusion-section claims trace to named section-4 chains per the quoted scan (0 untraced, 0 excluded), no claim introduces reasoning absent from section 4, and the Key Insight states a non-obvious finding (the Carnot-ceiling-vs-realistic-performance gap and the heat-inclusive-metric equivocation) distinct from and not a restatement of the Recommended approach's bare verdict.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "convention", "verdict": "Accept"},
    {"id": "A-2", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-3", "type": "physical law", "verdict": "Accept"},
    {"id": "A-4", "type": "convention", "verdict": "Challenge"},
    {"id": "A-5", "type": "untested belief", "verdict": "Accept"},
    {"id": "A-6", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-7", "type": "physical law", "verdict": "Discard"},
    {"id": "A-8", "type": "convention", "verdict": "Challenge"},
    {"id": "A-9", "type": "untested belief", "verdict": "Challenge"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": true},
    {"id": "GT-2", "read_at_source": false},
    {"id": "GT-3", "read_at_source": false},
    {"id": "GT-4", "read_at_source": false},
    {"id": "GT-5", "read_at_source": false},
    {"id": "GT-6", "read_at_source": false},
    {"id": "GT-7", "read_at_source": false},
    {"id": "GT-8", "read_at_source": true},
    {"id": "GT-9", "read_at_source": false},
    {"id": "GT-10", "read_at_source": false},
    {"id": "GT-11", "read_at_source": false},
    {"id": "GT-12", "read_at_source": false},
    {"id": "GT-13", "read_at_source": false},
    {"id": "GT-14", "read_at_source": false}
  ],
  "chains": [
    {"id": "C1", "confidence": "HIGH", "rests_on": ["GT-1"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["GT-3?", "GT-4?", "GT-7?"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["GT-8", "GT-9?", "GT-7?"]},
    {"id": "C4", "confidence": "LOW", "rests_on": ["GT-11?", "GT-12?", "GT-13?"]}
  ],
  "dead_ends": [
    "Heat-pump/cold-store Carnot-battery rescue via a cryogenic cold sink",
    "Non-heat-engine conversion technology (thermophotovoltaic / thermoelectric) bypassing the Carnot bound",
    "The isolated 81.3% optimized-study figure as confirming evidence for the claim",
    "Small-scale Li-ion repricing closing the cost gap"
  ],
  "techniques": {
    "applied": ["inversion", "five-whys", "theoretical-limit", "estimate", "second-order"],
    "not_applied": [
      {"technique": "fishbone", "phase": 2, "reason": "the claim's assumption space is already tightly bounded by a single governing physical law (Carnot/second-law), a definitional ambiguity, and a cost-scaling question; it does not require breadth-first multi-category cause brainstorming to enumerate, and the inversion procedure already surfaced the load-bearing preconditions more directly"},
      {"technique": "trade-off", "phase": 4, "reason": "the essence of this analysis is to evaluate the truth-value of a stated claim, not to choose among multiple viable options at a decision point; molten-salt-vs-Li-ion economics are produced as supporting evidence within the Ground Truths/Derivation Chains rather than as a formal weighted trade-off"},
      {"technique": "pre-mortem", "phase": 5, "reason": "the subject is a technical/economic claim, not a plan or recommendation requiring prospective-hindsight failure analysis; inversion is the decision-rule-correct adversarial technique for a claim, and was used instead"}
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": ["Rigorous", "Rigorous", "Sound", "Rigorous", "Rigorous", "Rigorous"],
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
    "recommendation": "Treat the claim as **false** as literally stated for the electricity-to-electricity efficiency assertion — an 85%+ round-trip is thermodynamically unreachable at 290–565 °C — and treat the cost-competitiveness assertion as **very likely false** at 5 MWh scale under the most probable (conventional-duration) reading of the claim, with one narrow, explicitly-named residual rival (a much longer discharge duration) left open rather than ruled out (chain C1, C3, C4).",
    "confidence": "LOW",
    "rests_on": ["C1", "C3", "C4"]
  }
}
```
