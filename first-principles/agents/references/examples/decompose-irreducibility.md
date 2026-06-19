<!-- GENERATED — DO NOT EDIT. Source: shared/examples/decompose-irreducibility.md. Regenerate via: scripts/sync-content.py --write. -->

# Worked Example: Decompose — Irreducibility Drill (Thermal Energy Storage)

A focused demonstration of the **decompose** (reduce-to-primitives) technique applied to
a science and engineering cost-feasibility claim, showing how the recursive drill terminates
at a physical law and how the verified primitives feed **Phase 3 (Establish Ground Truths)**.
The drill makes the stop test visible: each branch either reaches an irreducible anchor
(physical law / definition / direct measurement) or is flagged as assumed.

**Claim under analysis.** "A 5 MWh molten-salt thermal energy storage tank operating at
290–565 °C can round-trip electricity into heat and back with a system efficiency above 85%,
making it cost-competitive with a lithium-ion battery system of the same nameplate capacity."

**Why this claim is compound.** The claim bundles at least four distinct sub-claims:
a thermodynamic efficiency assertion, a round-trip loss budget, a cost-per-kWh comparison,
and an implicit assumption about operating temperature range. Each must reduce to an
irreducible primitive before the composite claim can be trusted.

---

## Decompose Drill

### Level 0 — The composite claim

**C0:** A 5 MWh molten-salt thermal energy storage (TES) system has a round-trip efficiency
above 85% and is cost-competitive with a lithium-ion battery system at the same nameplate
capacity.

**Immediate constituents:**

- C1: The round-trip efficiency of the TES system exceeds 85%.
- C2: The molten-salt medium can store and release thermal energy across the 290–565 °C
  operating window without degradation over the intended design life.
- C3: The system's levelised cost of storage (LCOS) is at or below that of a lithium-ion
  battery system of the same nameplate capacity in the same application context.

---

### Level 1 — Decompose C1 (round-trip efficiency > 85%)

Round-trip efficiency decomposes into the product of three conversion efficiencies:

- C1a: Electricity-to-heat conversion efficiency (the resistive or induction heater
  converting grid electricity to thermal energy in the salt).
- C1b: Thermal storage efficiency (fraction of heat retained in the insulated tank
  over the storage period — a function of thermal losses to the environment).
- C1c: Heat-to-electricity conversion efficiency (the power cycle, typically a
  steam Rankine cycle, converting stored heat back to electricity).

Round-trip efficiency = C1a × C1b × C1c. The 85% claim requires the product to exceed 0.85.

---

#### Level 2 — Decompose C1a (electricity-to-heat conversion)

Resistive heating converts electrical energy to thermal energy via Joule heating
(P = I²R). In an ideal resistive element, the conversion is 100%; real systems
approach 95–99% depending on element design and control losses.

- **Constituent:** Joule heating law (P = I²R, equivalently P = V²/R = VI).
  **Stop — physical law (Joule's first law / Ohm's law). Irreducible.**
  C1a is anchored in physics; the limiting factor is engineering loss (< 5%),
  verifiable from equipment specifications (a direct measurement).

**Branch verdict — C1a:** Verified. Electricity-to-heat conversion approaches
95–99% efficiency, grounded in Joule heating (physical law) + equipment datasheet
(direct measurement).

---

#### Level 2 — Decompose C1b (thermal storage efficiency)

Thermal loss from an insulated tank is governed by Fourier's law of heat conduction
(q = –k∇T): heat flux is proportional to the thermal conductivity of the insulation
and the temperature gradient across it. Over a 24-hour storage period, a well-insulated
large-scale tank at 500 °C loses on the order of 0.2–1% of stored energy per hour,
depending on insulation thickness and surface area.

- **Constituent 1:** Fourier's law of heat conduction.
  **Stop — physical law (Fourier's law). Irreducible.**
- **Constituent 2:** Specific heat capacity and heat loss rate for this tank
  geometry and insulation specification — a site- and design-specific parameter.
  **Stop — direct measurement (requires the tank's engineering specification and
  insulation material datasheet). Assumed here; mark unverified.**

**Branch verdict — C1b:** Partially verified. The governing physics is anchored
(Fourier's law); the actual loss rate for a specific tank design is
`Assumed — unverified` until the engineering specification and site thermal profile
are confirmed.

---

#### Level 2 — Decompose C1c (heat-to-electricity, Rankine cycle)

The Rankine cycle heat-to-electricity efficiency is bounded above by the Carnot
limit: η_Carnot = 1 − T_cold / T_hot (temperatures in Kelvin). At T_hot = 565 °C
= 838 K and T_cold ≈ 30 °C = 303 K, the Carnot limit is:

    η_Carnot = 1 − 303/838 ≈ 63.8%

Real Rankine cycles achieve 35–45% net electrical efficiency at these temperatures
(accounting for pump work, condenser losses, and turbine isentropic efficiency).
This is well below the Carnot limit — consistent with the second law — and is
confirmed by published data for commercial utility-scale steam turbines.

- **Constituent 1:** Carnot efficiency formula (η_Carnot = 1 − T_cold/T_hot).
  **Stop — physical law (second law of thermodynamics / Carnot's theorem).
  Irreducible.**
- **Constituent 2:** Real Rankine cycle efficiency ≈ 35–45% at these temperatures.
  **Stop — direct measurement (published operational data for commercial steam
  turbines at these inlet conditions; verifiable against, e.g., NREL CSP
  efficiency surveys). Verified.**

**Branch verdict — C1c:** Verified. The upper bound is anchored by the second
law; the real operating efficiency range is confirmed by published measurement.
Note: C1c ≈ 0.35–0.45, which is the dominant loss in the round-trip chain.

---

#### Verdict on C1 (round-trip efficiency > 85%)

Round-trip = C1a × C1b × C1c ≈ 0.97 × 0.99 × 0.40 ≈ 38%.

**The 85% claim fails the irreducibility drill.** The constituent C1c (Rankine
cycle efficiency ≈ 35–45%) is anchored at a physical law and confirmed by direct
measurement, and it prevents the product from reaching 85%. An 85% round-trip
efficiency for a heat-storage-to-electricity system is inconsistent with the
Carnot limit at these temperatures. The claim, as stated, is refuted by the
physical law that terminates C1c.

*(Clarification: systems that store and return heat — not electricity — can
achieve higher thermal round-trip efficiency; the 85% figure is only achievable
if the "round-trip" is heat-in to heat-out, not electricity-in to electricity-out.
The claim as stated implies electricity round-trip.)*

---

### Level 1 — Decompose C2 (molten salt stability across 290–565 °C)

The most common molten-salt heat-transfer fluid in TES is Solar Salt (60% NaNO₃ /
40% KNO₃). Published literature and commercial plant experience establish:

- Melting point: ~220 °C (definition: established by phase-diagram measurement).
- Decomposition onset: ~600 °C (direct measurement from differential thermal
  analysis studies).
- Operating window 290–565 °C is within the verified stable range.

**Constituent:** Thermal stability data for Solar Salt in its documented operating
window.

**Stop — direct measurement (published phase diagrams and differential thermal
analysis; commercial plant operating records from Andasol, Crescent Dunes, etc.).
Verified.**

**Branch verdict — C2:** Verified. The operating window 290–565 °C is within the
documented stable range for Solar Salt, anchored in direct measurement.

---

### Level 1 — Decompose C3 (LCOS competitive with lithium-ion)

LCOS = (total capital cost + operating cost) / (lifetime energy throughput).
Each factor decomposes further:

- Capital cost per MWh for molten-salt TES: approximately $20–50/kWh (published
  NREL estimates, 2023) — a direct measurement from engineering cost studies.
  **Stop — direct measurement. Verified (as a range; project-specific costs may vary).**
- Capital cost per MWh for utility-scale lithium-ion: approximately $150–300/kWh
  installed (BNEF, BloombergNEF 2023 surveys) — a direct measurement.
  **Stop — direct measurement. Verified (as a current market survey figure).**
- Lifetime cycle degradation for molten salt vs. lithium-ion: molten salt has
  no electrochemical degradation mechanism at operating temperatures; lithium-ion
  degrades ~2–3% per year.
  **Constituent for molten salt:** No electrochemical side reactions at 290–565 °C
  for an inorganic salt mixture — grounded in electrochemistry and the absence of
  redox-active species at these conditions.
  **Stop — physical law / definition (inorganic salt chemistry; no electrochemical
  cycling degradation by construction). Irreducible.**

**Branch verdict — C3:** The capital cost comparison favors molten-salt TES on a
per-kWh-installed basis (by roughly 5–10×). The LCOS comparison is verified in
direction but not in magnitude without project-specific discount rates, capacity
factors, and operating cost data. Mark as `Assumed — partially verified` pending
those site-specific inputs.

---

## Summary of Drill Results

| Branch | Anchor | Status |
|--------|--------|--------|
| C1a — electricity-to-heat (Joule heating) | Physical law (Joule/Ohm) + equipment datasheet | Verified |
| C1b — thermal storage loss rate | Physical law (Fourier) anchored; specific loss rate per design | Partially verified |
| C1c — heat-to-electricity (Rankine) | Physical law (2nd law / Carnot) + published turbine data | Verified |
| **C1 — round-trip efficiency > 85%** | Refuted by C1c physical-law anchor (≈38%, not 85%) | **Refuted** |
| C2 — molten-salt stability window | Direct measurement (phase diagrams, plant records) | Verified |
| C3 — LCOS vs. lithium-ion | Direct measurement (cost surveys); site-specific factors missing | Partially verified |

**Key finding:** The claim's 85% round-trip electricity efficiency is physically
impossible at these operating temperatures — it is refuted by the Carnot limit,
which is irreducible. The cost-competitiveness comparison (C3) is directionally
supported but not fully verified without site-specific LCOS inputs.

---

## Phase 3 Handoff — Ground Truths

The verified primitives produced by the decompose drill become the anchor points
for **Phase 3 (Establish Ground Truths)**:

- **GT-1** Joule heating law: electrical energy converts to thermal energy at
  95–99% efficiency in resistive elements (physical law: P = I²R / Ohm's law;
  confirmed by equipment specifications for commercial resistive heaters).

- **GT-2** Fourier's law governs thermal loss from the storage tank (physical law:
  heat flux proportional to conductivity × temperature gradient). Actual loss rate
  for a specific tank geometry is design-dependent and must be sourced from the
  engineering specification.

- **GT-3** Carnot efficiency limit for the Rankine heat-to-electricity cycle at
  T_hot = 838 K, T_cold = 303 K: η_Carnot ≈ 63.8%; real Rankine cycle efficiency
  ≈ 35–45% (physical law: second law of thermodynamics / Carnot's theorem; confirmed
  by published operational data for commercial steam turbines at these inlet conditions).

- **GT-4** Solar Salt (60% NaNO₃ / 40% KNO₃) is thermally stable across the
  290–565 °C operating window (direct measurement: published phase diagrams and
  differential thermal analysis; verified in commercial CSP plant operating records).

- **GT-5** Capital cost of molten-salt TES: approximately $20–50/kWh installed
  (direct measurement: NREL engineering cost estimates, 2023).

- **GT-6** Capital cost of utility-scale lithium-ion battery storage: approximately
  $150–300/kWh installed (direct measurement: BloombergNEF 2023 market survey).

- **GT-7?** Thermal storage loss rate for the specific tank under analysis:
  unverified — requires the tank engineering specification and insulation material
  datasheet (source: not yet obtained).

- **GT-8?** Project-specific LCOS inputs (discount rate, capacity factor, operating
  and maintenance costs) for the LCOS comparison: unverified — requires the
  project financial model.

**Phase 3 consequence:** GT-3 (Carnot / second-law anchor) immediately refutes the
85% round-trip electricity efficiency claim in C1. No further evidence is needed —
the physical law is the irreducible terminal condition. GT-1 through GT-6 anchor the
remaining sub-claims, and GT-7? / GT-8? mark the remaining gaps that Phase 3 must
close before a verified cost-competitiveness conclusion can be drawn.
