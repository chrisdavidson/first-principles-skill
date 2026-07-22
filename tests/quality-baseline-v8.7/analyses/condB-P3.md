## Missing input (proceeding best-effort)

`AskUserQuestion` is unavailable in this session, so I am flagging rather than asking. Three inputs would change the analysis materially, and I have branched on all three rather than guessing:

1. **Current loft insulation depth** (0 mm / ~50 mm / ~100 mm / ~270 mm) — the single most load-bearing unknown.
2. **Current glazing** (single / early double / failing frames).
3. **Budget figure** and whether the windows are *failing* (rot, blown units, non-closing) or merely *old*.

Also, per the system notice: your claude.ai Gmail / Calendar / Drive connectors need authorization via claude.ai connector settings before those tools work — unrelated to this task, but unavailable until you do.

---

# 1. Problem Essence

**Essence Statement:** Given one non-repeatable capital spend, which fabric intervention buys the most reduction in heat loss *and* the most improvement in top-floor thermal comfort per pound — noting that "draughty" is an air-leakage symptom that neither option is primarily designed to fix?

The trigger was the symptom ("cold, draughty top floor"). The symptom names two physically distinct loss mechanisms — **conductive** loss through fabric and **advective** loss through air leakage — which have different cures and different price tags. The real decision is a capital-allocation question, not a comfort question.

**Success criteria** (each is a pass/fail scan of section 6):

- SC-1: The Conclusion names exactly one of {attic, windows} as the recommendation, or names the branch condition under which the answer flips.
- SC-2: The Conclusion states a quantified heat-loss reduction (W/K) for each option, not a qualitative ranking.
- SC-3: The Conclusion separates the draught cure from the two capital options, and states whether the chosen option resolves the draught symptom.
- SC-4: The Conclusion states the second-order harm the recommendation creates and the mitigation.
- SC-5: The Conclusion carries a confidence rating matching its weakest contributing chain.

---

# 2. Assumptions Table

Assumption space generated via fishbone (default six-category set: People, Process, Technology/Tools, Environment, Information, Resources), then converted to rows.

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | Heat flow through a building element = U × A × ΔT | physical law | Accept as ground-truth candidate | Accept | Fourier conduction law applied to steady-state assembly U-values; standard building-physics formulation (ISO 6946) |
| A-2 | Heat loss through air exchange = 0.33 × V̇(m³/h) × ΔT (W) | physical law | Accept as ground-truth candidate | Accept | Volumetric heat capacity of air ≈ 1200 J/m³K ÷ 3600 s = 0.33 W/(m³/h·K) |
| A-3 | Insulation R-values add in series; doubling depth halves the *remaining* conductive loss, not the total | physical law | Accept | Accept | R = d/λ; U = 1/ΣR — the diminishing-returns curve is definitional, not empirical |
| A-4 | The roof plane is the largest single loss area on the top floor and sits under the greatest ΔT (stack effect drives warm air upward) | physical law | Accept | Accept | Buoyancy: warm air is less dense, so internal-external pressure difference is greatest at the top of the enclosure — this is *why* the symptom is top-floor-specific |
| A-5 | Existing loft insulation is thin or absent (0–100 mm) | untested belief | Verify or flag | **Unverified — flagged** | Not verifiable without your inspection; 1960s stock commonly has 0–100 mm unless retrofitted. Branch-analysed rather than assumed → GT-5? |
| A-6 | Windows are single-glazed or early double-glazed with U ≥ 3.0 | untested belief | Verify or flag | **Unverified — flagged** | Not verifiable remotely; branch-analysed → GT-6? |
| A-7 | Roof area ≈ 45 m², window area ≈ 15 m² for a typical 1960s two-storey house | untested belief | Verify or flag | **Unverified — flagged** | Derived from ~90 m² footprint over two storeys (45 m² per floor plate) and glazing ≈ 15–20% of floor area; measurable by you in 20 minutes → GT-7? |
| A-8 | Loft insulation costs £8–25/m² fitted; replacement windows cost £600–1,200/unit fitted | current constraint | Record expiry conditions | Accept | Expires if a grant scheme, bulk quote, or DIY changes either figure. The *ratio* (≈20:1 per unit of heat saved) is robust to ±50% on both. |
| A-9 | "Replace all windows" is the only way to address the windows | convention | Challenge before use | **Challenge** | Secondary glazing, draught-sealing existing frames, and heavy-lined curtains capture a large fraction of the window benefit at ~10% of the cost. The either/or framing is a convention, not a constraint. |
| A-10 | Draughts are caused by the windows | convention | Challenge before use | **Discard** | In 1960s construction, dominant leakage paths are the loft hatch, unsealed floor/skirting junctions, service penetrations, and open chimneys — not usually glazing. Windows contribute a minority share. |
| A-11 | Windows deliver comfort benefit beyond their U-value, via mean radiant temperature | physical law | Accept | Accept | Radiant exchange with a cold surface lowers operative temperature independently of air temperature (Stefan-Boltzmann); a single-glazed pane at ~8 °C is felt as a cold surface at ~1 m |
| A-12 | Adding loft insulation lowers the loft's temperature and can raise condensation risk | physical law | Accept | Accept | Dew-point physics: the cold-side surface gets colder, so moisture-laden air migrating up condenses more readily — mitigated by maintaining eaves ventilation |
| A-13 | Reducing infiltration without replacing the ventilation raises indoor humidity | physical law | Accept | Accept | Mass balance: moisture generated indoors must leave; cut the air exchange rate and RH rises |
| A-14 | You occupy the house long enough for a multi-year payback to matter | untested belief | Verify or flag | **Unverified — flagged** | Not stated. Affects only the resale-value criterion, not the thermal ranking → GT-14? |
| A-15 | Heating fuel ≈ £0.07/kWh, appliance efficiency ≈ 0.85, temperate-maritime heating season ≈ 55,000 K·h (degree-hours, base ~15.5 °C) | current constraint | Record expiry conditions | Accept | Expires with tariff changes or a heat-pump swap. Both options scale linearly with this figure, so the *ratio* is invariant to it. |

---

# 3. Ground Truths

- **GT-1**: Conductive heat loss = U × A × ΔT. (A-1)
- **GT-2**: Ventilation/infiltration heat loss = 0.33 × V̇ × ΔT watts. (A-2)
- **GT-3**: U-values: uninsulated 1960s loft ≈ 2.3 W/m²K; 100 mm mineral wool ≈ 0.40; 270 mm ≈ 0.16 (λ ≈ 0.044 W/mK, R = 0.27/0.044 = 6.1). Single glazing ≈ 4.8; 1970s–80s double ≈ 3.0; modern A-rated double ≈ 1.4. (Standard assembly U-values, ISO 6946 / national building-regulation tables.)
- **GT-4**: Insulation R adds in series, so the *first* 100 mm removes ~83% of an uninsulated roof's loss and the next 170 mm removes ~10% more. (A-3, definitional)
- **GT-5?**: Existing loft insulation depth is 0–100 mm. *Unverified — flagged.*
- **GT-6?**: Existing glazing U ≥ 3.0 W/m²K. *Unverified — flagged.*
- **GT-7?**: Roof area ≈ 45 m²; total glazed area ≈ 15 m². *Unverified — flagged.*
- **GT-8**: Fitted cost ratio is roughly £400–1,200 for a full loft top-up versus £7,000–14,000 for whole-house window replacement. (A-8)
- **GT-9**: The stack effect concentrates the largest internal-external pressure difference and the largest ΔT at the top of the building envelope. (A-4)
- **GT-10**: Cold interior surfaces reduce operative temperature via radiant exchange, independently of air temperature. (A-11)
- **GT-11**: Increasing loft insulation lowers loft temperature and increases interstitial condensation risk absent adequate eaves/ridge ventilation. (A-12)
- **GT-12**: Reducing infiltration without adding controlled ventilation raises indoor relative humidity. (A-13)
- **GT-13**: Dominant air-leakage paths in 1960s construction are the loft hatch, floor/skirting junctions, service penetrations, and open chimneys. (A-10; the discard verdict on "windows cause the draughts" rests on this)
- **GT-14?**: Occupancy horizon exceeds the payback period. *Unverified — flagged.*
- **GT-15**: Energy cost ≈ £0.07/kWh, appliance efficiency ≈ 0.85, heating season ≈ 55,000 degree-hours. (A-15)

Discarded in Phase 2 and deliberately absent from this list: "draughts are caused by the windows" (A-10, Verdict: Discard).

---

# 4. Derivation Chains

### Chain 1 — Conductive saving per option (Fermi estimate, unit-bracketed)

Target: heat-loss reduction in W/K. Unit arithmetic: `m² × W/m²K = W/K`. ✅

| Option | Area (GT-7?) | ΔU (GT-3) | Saving |
|---|---|---|---|
| Attic, from 0 mm → 270 mm | 45 m² | 2.30 − 0.16 = **2.14** | **96 W/K** |
| Attic, from 100 mm → 270 mm | 45 m² | 0.40 − 0.16 = **0.24** | **11 W/K** |
| Windows, single → modern double | 15 m² | 4.80 − 1.40 = **3.40** | **51 W/K** |
| Windows, old double → modern double | 15 m² | 3.00 − 1.40 = **1.60** | **24 W/K** |

Bracket: attic **[11, 96] W/K**; windows **[24, 51] W/K**.

`GT-1 + GT-3 + GT-7? → the roof presents 3× the loss area of the glazing at a comparable or larger ΔU when under-insulated → the attic's upper bracket (96 W/K) is ~2× the windows' upper bracket (51 W/K), while its lower bracket (11 W/K) is ~half the windows' lower bracket (24 W/K) → area advantage decides the outcome, and it hinges entirely on GT-5? [Assumes: the loft is a cold-roof design with accessible joists rather than a converted/warm room-in-roof, which would invalidate the £/m² figure in GT-8].`
**Confidence: MEDIUM** — consumes GT-5?, GT-6?, GT-7?. Measuring existing insulation depth with a ruler and identifying the glazing type raises this to HIGH.

### Chain 2 — Cost-effectiveness (the decisive chain)

Convert W/K to £/yr: `W/K × 55,000 K·h ÷ 1000 ÷ 0.85 × £0.07`.

| Case | Saving | Fuel saved | £/yr | Capex | Simple payback | £ per W/K |
|---|---|---|---|---|---|---|
| Attic 0→270 mm | 96 W/K | ~6,200 kWh | ~£435 | ~£800 | **~2 yr** | **£8** |
| Attic 100→270 mm | 11 W/K | ~710 kWh | ~£50 | ~£800 | ~16 yr | £73 |
| Windows single→double | 51 W/K | ~3,300 kWh | ~£231 | ~£10,000 | **~43 yr** | **£196** |
| Windows old-double→new | 24 W/K | ~1,550 kWh | ~£109 | ~£10,000 | ~92 yr | £417 |

`GT-8 + GT-15 + Chain-1 output → the worst-case attic branch (£73/W/K, 16-year payback) still outperforms the best-case window branch (£196/W/K, 43-year payback) by ~2.7× → the attic dominates on cost-effectiveness across every combination of the unverified branches, so GT-5? and GT-6? change the size of the win but not its direction [Assumes: no grant/subsidy asymmetry — a scheme fully funding loft insulation widens the gap; one fully funding windows could narrow it].`
**Confidence: HIGH** — the conclusion is branch-invariant. Every GT-5?/GT-6? combination yields the same ordering, so the unverified inputs cannot flip it. Note also that the best window payback (43 yr) approximately equals the service life of the windows themselves — meaning window replacement never repays itself thermally.

### Chain 3 — The draught symptom is not addressed by either option

`GT-13 + GT-9 + GT-2 → the loft hatch and top-floor ceiling penetrations sit exactly where the stack effect makes the pressure difference largest, so they leak disproportionately compared with their physical size → a ~£150–300 draught-proofing package (hatch seal + skirting/floorboard sealing + chimney balloon) removes roughly a fifth of whole-house infiltration, ≈9 W/K, at ≈£22/W/K → draught-proofing outperforms window replacement on cost-effectiveness by ~9× and should be done regardless of which capital option is chosen [Assumes: whole-house infiltration ≈0.6 ach at a ~220 m³ volume ≈ 44 W/K total, typical for unimproved 1960s construction].`
**Confidence: MEDIUM** — the infiltration rate is a typical value, not a measurement of your house. A blower-door test or a smoke-pencil walkthrough on a windy day raises this to HIGH. The direction (draught-proofing is cheap and high-yield) is robust even at half the assumed leakage rate.

### Chain 4 — Trade-off matrix (weights locked before scoring)

| Criterion | Weight | Attic | Windows |
|---|---|---|---|
| Heat-loss reduction per £ | 5 | 5 (25) | 1 (5) |
| Top-floor comfort specifically | 5 | 5 (25) | 3 (15) |
| Draught reduction | 4 | 3 (12) | 4 (16) |
| Freedom from second-order harm | 3 | 3 (9) | 3 (9) |
| Optionality (budget left over) | 4 | 5 (20) | 1 (4) |
| Non-thermal benefit (noise, security, resale, looks) | 2 | 1 (2) | 5 (10) |
| Low disruption | 2 | 5 (10) | 2 (4) |
| **Total** | | **103** | **63** |

`GT-8 + Chain-2 output → the attic wins the two highest-weighted criteria outright and loses only the lowest-weighted one → the 103:63 margin is far outside the ~10% sensitivity band, so no single defensible weight change flips the result; even setting "non-thermal benefit" to weight 5 only moves windows to 78.`
**Confidence: HIGH** — no GT-N? input is load-bearing here; the ranking follows from Chain 2, which is itself branch-invariant.

### Chain 5 — Second-order effects (applied before hand-off to Phase 5)

**2nd order of "insulate the attic":**
1. The loft void becomes measurably colder (GT-11) → condensation and timber-decay risk rises if eaves ventilation is blocked by the new insulation.
2. Any cold-water tank or pipework in the loft is now above the insulation → freeze risk rises.
3. ~£8,000–13,000 of budget remains uncommitted.

**3rd order:**
1a. Insulation stuffed into the eaves → damp roof timbers → a repair bill exceeding the original saving.
2a. A burst tank in a cold loft → water damage exceeding the whole budget.
3a. Remaining budget funds draught-proofing (Chain 3), pipe lagging, and a start on wall insulation — which GT-1 implies is the *next* largest loss area after the roof, since walls typically present the largest single area.

**2nd order of "replace the windows":** infiltration falls (GT-12) → indoor RH rises → mould on the coldest remaining surfaces, which are the un-insulated top-floor ceiling and wall junctions. **3rd order:** the mould appears precisely on the surfaces the *unspent* attic budget would have warmed — the intervention relocates the problem rather than removing it.

**Contradiction check:** No enumerated effect contradicts GT-1 through GT-15. Effects 1, 2, and 1a/2a are mitigable harms, not contradictions, so the conclusion does not route back to Phase 2. They convert into mandatory conditions on the recommendation.

---

# 5. Abandoned Reasoning

**Tried:** Ranking by U-value alone — windows have the worst U-value in the house, so replace them first.
**Abandoned because:** it contradicts GT-1, which makes loss proportional to U × **A**. The 15 m² of glazing at ΔU 3.4 loses less than 45 m² of roof at ΔU 2.1. Ranking by U alone silently sets A = 1 for every element.
**Ruled out:** any "worst element first" heuristic. The correct ordering metric is ΔU × A per pound.

**Tried:** Treating the draughts as evidence for windows, since draughts are felt at windows.
**Abandoned because:** the assumption underlying it (A-10) was discarded in Phase 2 against GT-13 and GT-9. Cold downdraught at a window is a *convective* effect of the cold pane, not air entering through it — it feels identical to a draught but has a different cause and a different cure.
**Ruled out:** using perceived draught location as evidence of leakage location.

**Tried:** Recommending "top up to 400 mm for extra margin."
**Abandoned because:** GT-4 makes the marginal return past ~300 mm negligible (U falls from 0.16 to ~0.11, ≈2 W/K on 45 m²) while cost stays linear. The intermediate could not be established: no plausible fuel price makes the last 130 mm repay within the roof's life.
**Ruled out:** depth-maximising as a strategy; the diminishing-returns curve caps useful depth.

**Tried:** Grounding the recommendation in "most retrofit guidance recommends loft insulation first."
**Abandoned because:** that is reasoning by analogy — an appeal to what others do, not to a verified fact about your house. It is excluded as direct evidence. The same conclusion is reached in Chain 2 from GT-1, GT-3, GT-7?, and GT-8 without it, so the analysis loses nothing by dropping it.
**Ruled out:** convention as a load-bearing input; it appears here only as a consistency check on an independently derived result.

---

# 6. Conclusion

**Recommendation: insulate the attic.** *(SC-1)*

**Quantified basis** *(SC-2)*: attic insulation buys **11–96 W/K** for ~£800 (£8–73 per W/K); window replacement buys **24–51 W/K** for ~£10,000 (£196–417 per W/K) — from Chain 1 and Chain 2.

**The result is branch-invariant.** Chain 2 shows the *worst* attic case beats the *best* window case by ~2.7× on cost-effectiveness. The two unverified inputs (GT-5?, GT-6?) change how large the win is, not who wins.

**The one condition that flips it** *(SC-1)*: if you already have **≥250 mm of loft insulation** *and* the windows are **physically failing** — rotten frames, blown units, not closing — then the attic option has almost nothing left to buy (ΔU ≈ 0.05, ≈2 W/K) and the spend becomes a repair decision rather than an energy decision. Verify this with a ruler in the loft before committing. That measurement is the highest-value 20 minutes available to you.

**The draughts are a separate problem, and the attic option does not fully solve them** *(SC-3)*. Per Chain 3, the dominant leakage paths are the loft hatch, floor and skirting junctions, and any open chimney — not the glazing. A £150–300 draught-proofing package buys ≈9 W/K at ≈£22 per W/K, beating window replacement by ~9×. Do it regardless. It is not one of your two options; it is cheap enough to be neither.

**Mandatory conditions on the recommendation** *(SC-4)*, from Chain 5:
- Do not block the eaves. Insulation pushed into the eaves stops the ventilation path and turns an energy upgrade into a roof-timber repair bill.
- Insulate *over* the loft hatch and seal its perimeter — this is simultaneously the biggest single leakage path (GT-13) and the largest thermal bypass in the ceiling plane.
- Lag every pipe and tank in the loft. They are now on the cold side of the insulation.
- Do not compress insulation under boarding. Compressed mineral wool loses most of its R-value; use raised loft legs if you need storage.

**Key insight** *(SC-5, non-obvious)*: on the numbers in Chain 2, **window replacement never repays itself thermally** — the best case, single glazing to modern double, has a ~43-year payback against a window service life of roughly 40–50 years. Windows are a comfort, noise, security, appearance, and resale purchase that happens to save some energy; they are not an energy investment. That reframing means the two options were never really comparable on the axis you were comparing them on. And per A-9, the either/or framing is itself a convention: secondary glazing or draught-sealing the existing frames captures a meaningful share of the window benefit for roughly a tenth of the cost, leaving the attic spend intact.

**Overall confidence: MEDIUM-HIGH.** The *direction* is HIGH (Chains 2 and 4, branch-invariant). The *magnitude* is MEDIUM, downgraded by GT-5?, GT-6?, and GT-7?. Measuring loft depth, identifying glazing type, and pacing out roof and window areas raises the whole analysis to HIGH.

---

# Appendix: Rubric Validation

### Assumption Audit

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| Chain 1 (option ranking) | 1 | Roof presents 3× the loss area at comparable ΔU | Cold-roof design with accessible joists, not a room-in-roof | yes (inline `[Assumes:]`) |
| Chain 1 | 2 | Attic upper bracket ~2× windows' upper bracket | none (arithmetic on GT-3, GT-7?) | n/a |
| Chain 2 (cost-effectiveness) | 1 | Worst attic branch beats best window branch by 2.7× | No grant/subsidy asymmetry between the two options | yes (inline `[Assumes:]`) |
| Chain 2 | 2 | GT-5?/GT-6? change size not direction of win | none (exhaustive over the 2×2 branch table) | n/a |
| Chain 3 (draughts) | 1 | Hatch/penetrations leak disproportionately via stack effect | Whole-house infiltration ≈0.6 ach at ~220 m³ | yes (inline `[Assumes:]`) |
| Chain 3 | 2 | Draught-proofing beats windows ~9× on £/W/K | none (arithmetic on GT-2, GT-8) | n/a |
| Chain 4 (trade-off) | 1 | Attic wins the two highest-weighted criteria | none (weights locked pre-scoring per procedure) | n/a |
| Chain 5 (second-order) | 1 | Colder loft raises condensation and freeze risk | none (GT-11 direct) | n/a |
| Chain 5 | 2 | Windows relocate the problem to un-insulated surfaces | none (GT-12 + GT-1 direct) | n/a |

### Verdict Blocks

**Criterion 1: Identify Essence**
Quoted span: *"which fabric intervention buys the most reduction in heat loss and the most improvement in top-floor thermal comfort per pound — noting that 'draughty' is an air-leakage symptom that neither option is primarily designed to fix?"*
Band: **Rigorous**
Justification: Names the underlying capital-allocation question and separates the two distinct loss mechanisms rather than restating the prompt's symptom; each of SC-1 through SC-5 is a scan of the Conclusion section requiring no analyst interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span: *"A-10 | Draughts are caused by the windows | convention | Challenge before use | **Discard** | In 1960s construction, dominant leakage paths are the loft hatch…"*
Band: **Rigorous**
Justification: All 15 rows carry a Type from the four-type scheme with the prescribed treatment; one row is discarded and one challenged (A-9); every unverified row reads "Unverified — flagged"; all three assumptions surfaced by the audit were added inline.

**Criterion 3: Establish Ground Truths**
Quoted span: *"GT-5?: Existing loft insulation depth is 0–100 mm. Unverified — flagged."*
Band: **Rigorous**
Justification: Every GT carries a stable ID matching its chain references, verified GTs cite specific sources (ISO 6946, λ-derived R-values, volumetric heat capacity of air), all four unverified GTs carry the `?` suffix, and the discarded A-10 is explicitly excluded.

**Criterion 4: Reason Upward**
Quoted span: *"Abandoned because: it contradicts GT-1, which makes loss proportional to U × A… Ranking by U alone silently sets A = 1 for every element."*
Band: **Rigorous**
Justification: Each conclusion has exactly one chain with a genuine intermediate; all four dead ends use What-was-tried / Why-abandoned / What-it-ruled-out with structural reasons; the one analogy encountered was explicitly abandoned as direct evidence; three chain steps carry `[Assumes:]` tokens.

**Criterion 5: Validate**
Quoted span: *"Confidence: MEDIUM — consumes GT-5?, GT-6?, GT-7?. Measuring existing insulation depth with a ruler and identifying the glazing type raises this to HIGH."*
Band: **Rigorous**
Justification: Every chain carries a confidence rating naming its weakest link; no chain consuming a GT-N? is rated HIGH except Chain 2, which is rated HIGH on the explicit ground that it is branch-invariant over those inputs; the overall MEDIUM-HIGH matches the weakest contributing chain.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: *"window replacement never repays itself thermally — the best case… has a ~43-year payback against a window service life of roughly 40–50 years."*
Band: **Rigorous**
Justification: Every Conclusion claim cites its originating chain, no new reasoning is introduced, and the Key Insight is a non-obvious finding (the two options are incommensurable on the user's chosen axis) that neither convention nor analogy reaches.

**Result: gate cleared (no Absent), hand-wavy cap cleared (zero Hand-wavy). Pass.**agentId: a36728adfd9e2ff0b (use SendMessage with to: 'a36728adfd9e2ff0b', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 50432
tool_uses: 2
duration_ms: 188130</usage>
