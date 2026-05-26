# Worked Example: Science and Engineering (Failure Analysis)

A complete first-principles analysis of an in-service mechanical component failure,
following the standardized output format. Reasoning shape is **diagnostic**: starting
from observed failure-surface evidence and reasoning backward to a verified root cause,
ruling out a tempting alternative attribution along the way. Distinct from
`science-engineering.md`, which is a forward derivation from physical law (off-grid
solar sizing). Authored in Phase 33.

**Scenario.** A 1.5 MW upwind wind turbine's high-speed-shaft (HSS) gearbox bearing — a
generator-end cylindrical roller bearing on the HSS — was removed from service after the
condition-monitoring system flagged a step increase in HSS vibration kurtosis at roughly
14,000 operating hours, well short of the bearing's L10 design life of ~130,000 hours.
On disassembly the inner race shows axial-aligned spalling roughly 18 mm long, with
crescent-shaped microcracks ("beach marks") propagating from a subsurface origin point
about 0.4 mm below the raceway surface. White-etching cracks (WEC) and a butterfly
microstructure are visible in metallographic sections taken through the spall. The
operator's first hypothesis: "the lubricant failed — viscosity too low in the cold-snap
months drove a boundary-lubrication regime and the race wore through." The analyst's
job is to verify the root cause before authorising the replacement specification.

---

## 1. Problem Essence

**Core problem:** What is the verified root cause of the HSS generator-end cylindrical
roller bearing's premature spalling failure at ~14,000 hours, and does that root cause
prescribe a counter-intervention different from the operator's first hypothesis
(lubricant viscosity)?

**Success criteria:**

- The proposed root cause predicts the *specific* failure-surface markers observed
  (subsurface crack origin ~0.4 mm deep, axial spall geometry, white-etching cracks,
  butterfly microstructure) — not merely "a bearing failure consistent with the
  hypothesis."
- A counter-intervention targeting the proposed root cause would, in a controlled
  re-test, prevent recurrence within the L10 design horizon — whereas an intervention
  targeting the operator's first hypothesis (lubricant change-out) would not.
- Every causal claim traces to a named ground truth (failure-surface observation,
  measured operating condition, material certification, or textbook physical-law model
  with stated validity range) — no post-hoc storytelling.
- The analysis explicitly walks and closes the operator's tempting first hypothesis
  rather than leaving it as a live alternative.

---

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| Hertzian contact theory predicts subsurface shear-stress maximum at depth ~0.78·a (half-contact-width) for line contact in cylindrical roller bearings | physical law | Accept as ground-truth candidate; promote to GT | Accept | Classical contact mechanics; Hertz (1882); standard derivation in any tribology text. Independent of failure mode. |
| Rolling-contact fatigue (RCF) life follows the Lundberg-Palmgren / ISO 281 L10 model: life ∝ (C/P)^p with p = 10/3 for roller bearings, valid for clean, well-lubricated, properly mounted bearings under load below the C_u fatigue limit | physical law (derived) | Accept as ground-truth candidate; record constituent assumptions (clean lube, p = 10/3 for roller geometry, P below C_u) as expiry conditions | Accept | ISO 281:2007; derived from Weibull statistics of subsurface crack initiation. Validity range: classical RCF only — does not model WEC failures, which are a separate mechanism. |
| A 9× life shortfall against the ISO 281 L10 baseline (observed ~14,000 h vs calculated ~130,000 h L10) is too large to be attributed to load-spectrum estimation uncertainty or material-cleanliness variance within the classical RCF Weibull model — a non-classical mechanism is required | untested belief (quantitative threshold) | Accept with verification — the Chain 2 inference that a non-classical mechanism is required depends on this threshold claim; the magnitude (9×) must be compared against documented Weibull scatter in classical RCF studies to confirm it falls outside the scatter envelope | Accept | A 9× shortfall is far outside the ~2–3× scatter band documented in classical RCF Weibull analysis; Stadler & Stubenrauch 2013 (Table 2) documents WEC failures at 5–20% of L10 life — the ~11% observed here (14,000 / 130,000) falls inside that published EIBD range and outside the classical RCF scatter range, confirming the threshold claim. |
| The bearing's operating-condition history is captured by the SCADA log: HSS torque trace, generator-converter switching events, grid faults, cold-start transients | current constraint (quantifiable-cost) | Quantify what the log captures vs misses: 10-minute averaging window means sub-second transients are invisible; switching-event counts and grid-fault codes are logged at event resolution | Accept | SCADA log retained at 10-min averages for trend variables and event-resolution for faults; verified against turbine SCADA archive for the 14,000 operating hours preceding removal. |
| The bearing is manufactured to ISO 6336 / DIN 5401 with steel of certified composition (100Cr6 / SAE 52100, vacuum-degassed) and inclusion rating per ISO 4967 method A | current constraint | Record expiry: certification is fixed by procurement; the certificate either documents conformance or it does not | Accept | Verified against mill certificate retained in the wind-farm asset-management system; cleanliness rating within DIN spec. |
| White-etching cracks (WEC) and butterfly microstructure are caused by stray electrical currents through the rolling contact (electrically-induced bearing damage, EIBD) — i.e. a `convention — design-practice (codified)` belief grounded in IEC TS 60034-25 and the published WEC literature for wind-turbine generator bearings | convention (design-practice (codified)) | Accept tentatively if traceable; record expiry: WEC has multiple proposed mechanisms in the literature (hydrogen embrittlement from lubricant additive breakdown, transient overload, electrical current). Domain of validity for the EIBD attribution: doubly-fed induction generator (DFIG) drivetrains with IGBT inverter switching and inadequate shaft-to-ground bonding | Accept | Source: IEC TS 60034-25:2014 §8; Stadler & Stubenrauch 2013 "Premature Bearing Failures in Wind Gearboxes" — establishes the WEC-EIBD link in DFIG drivetrains and prescribes shaft-grounding rings as the codified counter-measure. |
| The operator's first hypothesis — "low-viscosity lubricant in cold-snap months drove a boundary-lubrication regime and wore the race through" | untested belief (diagnostic) | Challenge by ruling out with differential evidence: the wear morphology predicted by boundary lubrication (adhesive scuffing, smearing, polishing of the contact band) differs from the observed morphology (subsurface-origin spalling, WEC, butterfly) | Discard | Ruled out — see §5 Abandoned Reasoning. Cited mechanism would predict surface-origin damage; observed damage initiates subsurface and is accompanied by WEC, which lubricant viscosity alone cannot produce. |
| The shaft-to-ground bonding ring on the generator-end of the HSS was either absent at commissioning or had degraded below effective conductance | untested belief (diagnostic) | Verify by physical inspection of the bonding-ring assembly and conductance measurement; this is the load-bearing diagnostic claim for the EIBD attribution | Challenge | Verified: bonding ring was installed at commissioning per design but on-removal inspection shows brush-block carbon dust accumulated to a depth that interrupts brush-to-slipring contact; measured conductance 2 orders of magnitude below the IEC TS 60034-25 threshold. |

---

## 3. Ground Truths

- **GT-1** Subsurface crack origin depth: ~0.4 mm below the inner-race surface, measured
  on metallographic cross-section through the spall — source: metallographic report
  from accredited failure-analysis lab; image set retained.

- **GT-2** Hertzian subsurface shear-stress maximum for this bearing geometry under
  rated HSS load: ~0.35-0.45 mm depth (computed from contact-patch half-width using
  rated radial load 12 kN, roller diameter 22 mm, race radii, and steel
  E = 207 GPa, ν = 0.3) — source: Hertz contact-mechanics calculation; consistent with
  the textbook range 0.78·a for line contact. **The observed crack-origin depth (GT-1)
  falls inside the predicted Hertz subsurface-stress band — this confirms a subsurface-
  initiated fatigue mechanism, not a surface-initiated wear mechanism.**

- **GT-3** White-etching cracks and butterfly microstructure are present in the
  metallographic sections, distributed in a band coincident with the subsurface
  shear-stress zone — source: same metallographic report; SEM imagery confirms the
  characteristic WEC morphology (Stadler & Stubenrauch 2013, Fig. 4 reference geometry).

- **GT-4** L10 design life for this bearing under the certified load spectrum: ~130,000
  hours; observed life to spall: ~14,000 hours, a factor of ~9 below L10 — source:
  bearing manufacturer's life calculation per ISO 281; SCADA-derived load spectrum.
  **A 9× shortfall against ISO 281 is not consistent with classical RCF (which
  the L10 model already covers); a non-classical mechanism is required.**

- **GT-5** Shaft-to-ground bonding-ring conductance at the time of removal: measured
  ~10⁻⁴ S, vs the IEC TS 60034-25 prescribed minimum of ~10⁻² S — source: on-removal
  electrical-test report from the same failure-analysis lab. **The bonding path was
  effectively open, allowing rotor-shaft voltage to discharge through the bearing
  rolling contact.**

- **GT-6** The drivetrain uses a doubly-fed induction generator with an IGBT converter
  switching at ~3 kHz on the rotor side — source: turbine OEM data sheet; matches the
  IEC TS 60034-25 domain of applicability for EIBD risk.

- **GT-7?** Wear morphology predicted by sustained boundary-lubrication operation
  in this bearing class: surface-origin adhesive wear, scuffing, micropitting of the
  rolling band, and a polished or smeared contact track — unverified: a tribology
  textbook reference (Stachowiak & Batchelor, *Engineering Tribology*, Ch. 14) supports
  the morphology mapping, but no in-house controlled test has been run on this specific
  bearing under the disputed lubricant regime. The unverified status only matters if
  the analysis hinges on this GT alone — it does not, because GT-1 plus GT-3 already
  contradict the boundary-lubrication hypothesis on independent grounds.

---

## 4. Derivation Chains

### Conclusion: The failure is subsurface-initiated rolling-contact damage, not a surface-origin wear mechanism

GT-1 (crack origin ~0.4 mm subsurface) + GT-2 (Hertz subsurface-stress maximum
~0.35-0.45 mm at rated load)
→ The observed origin depth coincides with the depth band where Hertzian subsurface
  shear stress is maximised under the bearing's actual loading. Neither GT alone fixes
  the mechanism: GT-1 alone could in principle be a void or inclusion at depth; GT-2
  alone is a stress-field prediction without an observed crack. Together they place
  the observed initiation site exactly where the physical-law model predicts subsurface
  fatigue cracks would nucleate.
→ The failure mechanism is subsurface-initiated, ruling out every surface-origin
  mechanism (boundary lubrication wear, contamination indentation, mounting damage,
  electrical pitting on the running surface) as the *primary* cause of the spall.

**Confidence: HIGH** — both inputs are verified ground truths from independent
sources (metallographic measurement; classical contact-mechanics calculation).

---

### Conclusion: The subsurface mechanism is electrically-induced bearing damage (EIBD) producing WEC, not classical rolling-contact fatigue

GT-3 (WEC + butterfly microstructure in the subsurface shear-stress band) + GT-4
(9× life shortfall vs ISO 281 L10) + GT-5 (bonding ring conductance ~100× below the
IEC TS 60034-25 threshold) + GT-6 (DFIG drivetrain with IGBT switching — within the
IEC TS 60034-25 EIBD domain of applicability)
→ Classical RCF is already modelled by ISO 281 and its L10 figure. A 9× shortfall
  inside that envelope (GT-4) demands a *non-classical* mechanism — i.e., a degradation
  pathway that ISO 281 does not capture. [Assumes: a 9× L10 shortfall exceeds classical RCF Weibull variance — see Assumptions Table row.] WEC morphology (GT-3) is the published fingerprint of that non-classical
  pathway in wind-turbine HSS bearings. GT-5 supplies the proximate physical cause
  (open bonding path → rotor voltage discharges through the bearing rolling contact)
  and GT-6 confirms the drivetrain falls inside the IEC-defined domain where this
  mechanism is known to apply. None of these GTs alone fixes the mechanism: WEC has
  multiple published candidate causes; bonding-ring failure alone need not produce WEC
  if voltage is below threshold; L10 shortfall alone could be misload or material
  defect. Combined, they trace a single causal chain.
→ The root cause is electrically-induced bearing damage from a degraded shaft-to-ground
  bonding path, producing WEC-mediated subsurface degradation that drives premature
  spalling at the Hertz-stress depth.

**Confidence: HIGH** — all four inputs are verified GTs; the chain is co-supported by
the codified mechanism in IEC TS 60034-25, which prescribes exactly the failure
fingerprint observed here.

---

## 5. Abandoned Reasoning

### Dead End: Low-viscosity lubricant in cold-snap months drove boundary lubrication and surface-origin wear-through

**What was tried:** The operator's first hypothesis. The reasoning: ambient temperature
at the site dropped to −18 °C in the months preceding the failure; the gearbox lubricant
is an ISO VG 320 mineral oil whose viscosity rises sharply at low temperature, which
*intuitively* sounds like it would worsen lubrication — and operators in the wind-power
fleet have a culturally available story that "cold-snap viscosity problems" cause
gearbox bearing failures. The walk: assume the cold-snap drove the elastohydrodynamic
(EHD) film thickness below the composite surface roughness, putting the bearing into a
boundary-lubrication regime; expect surface-origin wear (scuffing, micropitting,
polishing of the running track) to result.

**Why abandoned:** Two independent contradictions with verified ground truths.

First and dispositive: GT-1 places the crack origin ~0.4 mm *below* the raceway surface,
inside the Hertz subsurface-stress band (GT-2). Boundary-lubrication damage
*by definition* initiates at the contact surface — the loss of EHD separation is a
surface-asperity-contact phenomenon. A subsurface-initiated spall cannot be the primary
product of a boundary-lubrication regime. **GT-1 alone falsifies the boundary-
lubrication attribution as the primary mechanism**, independent of GT-7?'s wear-
morphology prediction.

Second, corroborative: GT-3 reports WEC and butterfly microstructure in the subsurface
band. WEC is not a documented product of boundary lubrication; it is the published
fingerprint of either electrical-current discharge through the contact or
hydrogen-driven embrittlement from lubricant additive decomposition under transient
overload (Stadler & Stubenrauch 2013). The boundary-lubrication hypothesis has no
explanatory pathway to the observed microstructure; the EIBD hypothesis does.

Counter to the corrective intervention the operator's hypothesis would prescribe
(switch to a lower-viscosity-grade oil or add a pour-point depressant): GT-5 plus GT-6
show the bonding-ring conductance was two orders of magnitude below the IEC threshold
in a DFIG drivetrain known to be EIBD-prone. Changing lubricant grade would not address
the open electrical path; the bearing would continue to discharge rotor voltage and the
next bearing would fail by the same mechanism.

**What it ruled out:** Two things. First, lubricant viscosity / boundary lubrication as
the *primary* cause of this failure — the surface vs subsurface origin alone settles it.
Second, the corresponding counter-intervention (lube change-out). A skeptic re-running
this diagnosis on the next HSS bearing failure in the fleet should not re-explore the
lubricant pathway unless that bearing's failure surface shows surface-origin damage —
in which case GT-1's analogue would itself look different and the diagnosis restarts
from a different observation set.

---

## 6. Conclusion

**Recommended approach:** Replace the failed HSS bearing with a new bearing of the same
specification AND simultaneously restore the shaft-to-ground bonding path — clean and
re-seat the brush-block, restore conductance to the IEC TS 60034-25 prescribed range
(≥10⁻² S), and add to the turbine's preventive-maintenance schedule a quarterly
bonding-ring conductance check. Do NOT change the lubricant specification on the basis
of the operator's initial hypothesis — that intervention would not address the
verified root cause and would consume maintenance budget on a non-causal lever.

**Key insight:** The diagnosis hinged on a single observation that the operator's first
hypothesis cannot accommodate: a *subsurface* crack origin. Boundary-lubrication damage
initiates at the contact surface by mechanism; an interior crack origin is structurally
incompatible with that attribution regardless of how plausible the cold-snap-viscosity
narrative sounds. Reasoning by analogy ("cold months → lube problems → bearing failure")
would have led to the wrong intervention; reasoning from the failure-surface evidence
through the Hertz stress-field model led to the right one. The corollary is procedural:
when a failure surface is available, the analyst's first move is to characterise the
origin geometry (surface vs subsurface, single vs distributed) — that single observation
discriminates between large families of mechanisms before any narrative is entertained.

**Trade-offs acknowledged:** The recommended bonding-ring restoration adds quarterly
inspection labour the operator was not previously budgeting; the alternative (continue
without restoration) accepts a near-certain repeat failure on the replacement bearing
within a comparable ~10⁴-hour horizon, at materially higher cost (crane time, gearbox
risk, lost generation). The analysis also accepts that GT-7? (boundary-lubrication
wear-morphology mapping) is supported by textbook reference rather than in-house
controlled test — which is acceptable because GT-1 alone is dispositive against the
boundary-lubrication attribution; GT-7? is corroborative, not load-bearing.

**Confidence: HIGH** — the primary causal chain rests on GT-1 through GT-6, all of
which are verified independently. The single unverified item (GT-7?) is not load-
bearing for the root-cause finding and not load-bearing for the recommended
counter-intervention. The only residual uncertainty material to the next decision is
fleet-scope: whether other turbines in the same site share the same bonding-ring
degradation pattern — verification path is a one-day fleet-wide bonding-ring
conductance survey before the next scheduled gearbox inspection cycle.
