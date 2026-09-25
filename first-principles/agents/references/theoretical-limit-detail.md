<!-- GENERATED — DO NOT EDIT. Source: shared/references/theoretical-limit-detail.md. Regenerate via: scripts/sync-content.py --write. -->

<!-- markdownlint-disable MD041 -->

## Example A — thermal (coal steam cycle)

**Target:** thermal-to-electric conversion efficiency of a coal-fired steam
plant.

**Conventions embedded:** fleet-average efficiency reflects the age mix of
installed units, part-load operation, and decades-old steam conditions — all
engineering and economic choices, not hard constraints.

**Governing hard constraint:** the Carnot efficiency bound (Second Law of
Thermodynamics): η_Carnot = 1 − T_cold / T_hot (kelvin). No heat engine
operating between two reservoirs can exceed this, regardless of engineering
sophistication.

**Ideal ceiling, derived.** A modern ultra-supercritical (USC) unit runs main
steam at ≈ 600 °C = 873 K, condensing at ≈ 40 °C = 313 K:

    η_Carnot = 1 − 313/873 = 1 − 0.3585 = 0.6415 → 64.1%

**Best demonstrated, observed.** Modern USC units achieve ≈ 47% (LHV basis).
This is a cited observation, not a calculation.

**Conventional figure.** The US coal fleet averaged a heat rate of
10,018 Btu/kWh in 2024 (EIA):

    η = 3,412.14 / 10,018 = 0.3406 → 34.1% (HHV basis)

**Bracket:**

| Tier | Figure | Kind |
|---|---|---|
| Ideal ceiling (Carnot, 873 K → 313 K) | 64.1% | derived |
| Best demonstrated (modern USC) | ~47% (LHV) | observed, cited |
| Conventional (US fleet average, 2024) | 34.1% (HHV) | observed, cited |

- **Conventional → best demonstrated: ~13 points.** Headroom somebody has
  already proven reachable — it is an equipment and capital question, not a
  physics question.
- **Best demonstrated → ideal ceiling: ~17 points.** Headroom nobody has
  reached. Most of it is irreducible in practice: real cycles need finite ΔT
  across heat exchangers, and finite ΔT is exactly what Carnot's reversible
  idealisation assumes away.

**Basis caveat — read this before quoting the 13-point gap.** The 47% figure is
LHV and the 34.1% figure is HHV, and LHV efficiency for coal runs roughly 2–5
points higher than HHV for the *same physical plant*, because LHV leaves the
latent heat of flue-gas water vapour out of the denominator. The two figures also
describe different populations (a modern unit vs. a whole ageing fleet). So the
13 points is an upper estimate of the real gap, not a measured one. Putting two
bases in one bracket without saying so is how a comparison that looks like
arithmetic becomes an overstatement.

**Why this example does not use Curzon-Ahlborn as the middle tier.** For the
same reservoirs, the Curzon-Ahlborn efficiency is:

    η_CA = 1 − √(313/873) = 1 − 0.5988 = 0.4012 → 40.1%

That is tighter than Carnot and looks like the "practical" bound — but the
demonstrated 47% **exceeds it by about 7 points**. CA is the efficiency of an
endoreversible engine *at maximum power*, and a plant tuned for efficiency
rather than power density beats it. Treating it as a ceiling would have
understated what is already built. This is the "a model-dependent bound is not a
ceiling" rule, demonstrated on the technique's own worked numbers.

---

## Example B — non-thermal (network latency floor)

Theoretical-limit is not a thermodynamics tool. Here the governing hard
constraint is the speed of light. Latency is a quantity where lower is
better, so the governing bound is a **floor**, and the bracket runs downward.

**Target:** round-trip latency between New York and London for a web service,
conventionally ~70 ms.

**Conventions embedded:** routing that is not great-circle, switching and
queueing hops, protocol round trips, server think time.

**Governing hard constraint:** signal propagation cannot exceed *c*, and in
fibre it travels at *c/n*.

**Ideal floor, derived.** c = 299,792,458 m/s (exact, by SI definition); fibre
group index n ≈ 1.5:

    v = 299,792,458 / 1.5 ≈ 199,862 km/s
    one-way = 5,570 km / 199,862 km/s = 27.9 ms
    round trip = 55.7 ms

**Best demonstrated, observed.** Purpose-built low-latency transatlantic
routes beat ordinary commercial routing. Hibernia Express, in service since
September 2015, is **measured at 58.95 ms** round trip between the Equinix
NY4 data centre in Secaucus, New Jersey and LD4 in Slough, England. Cite it
as a **tested figure**, not an advertised one — the technique's own
failure-modes section demands an observed, cited figure, and this one is a
published test result. Name the endpoints explicitly, because they are not
the floor's endpoints (see the caveat below).

**Conventional figure.** Ordinary commercial routing runs ≈ 70 ms RTT.

**Bracket:**

| Tier | Figure | Kind |
|---|---|---|
| Ideal floor (fibre, great circle) | 55.7 ms RTT | derived |
| Best demonstrated (Hibernia Express, NY4 Secaucus - LD4 Slough) | 58.95 ms RTT | observed, measured |
| Conventional (commercial routing) | ~70 ms RTT | observed |

- **Conventional -> best demonstrated: ~11 ms.** Headroom somebody has already
  proven reachable — a procurement decision, not a physics one.
- **Best demonstrated -> ideal floor: ~3 ms.** Headroom nobody has reached.
  This is what is actually left to engineering once the best available route
  is bought.

**What this bracket tells you, and it is the opposite of Example A.** The
~14 ms gap splits roughly 11/3: most of it is a route you can buy, and only
~3 ms is beyond any engineering once you have bought it. *Stop looking here*
still applies, but scoped correctly — it is the **engineering** path that is
closed, not the procurement one, and a real latency budget still has to come
from fewer round trips, caching, or moving computation closer to the user.
This is the worked case for the core file's own warning: the collapsed
two-tier bracket merged a purchasable 11 ms with an unreachable 3 ms and
returned the wrong instruction.

**Basis caveat.** The 55.7 ms floor is derived over the 5,570 km NY-London
great circle; the 58.95 ms is measured Secaucus-to-Slough, which carries metro
tails at both ends and the cable's Halifax/Brean landing detour, so it
traverses a **longer** path than the floor's basis. The like-for-like gap to
the physical floor is therefore **smaller** than the 3.25 ms the raw
subtraction gives. The mismatch makes the residual engineering headroom look
larger than it is, so the bracket's lesson holds a fortiori.

*Note on n:* real single-mode fibre has a group index nearer 1.46–1.48, giving
v ≈ 202,000–205,000 km/s and a floor 2–3% lower. Immaterial at this precision,
stated so the number is reproducible.

---

## Failure modes

**Citing best-in-class practice as the ceiling.** Using "the best plant in
the world achieves X%" as the theoretical limit. That is still an observation —
a bound must derive from a named constraint, not from incumbents. Even the best
incumbent may be far below the ideal ceiling. Note this is *not* an argument
against the demonstrated tier: recording the best achieved figure is required,
and calling it the ceiling is the error. Keep the tiers labelled, and the
distinction stays visible.

**Omitting the bracket.** Deriving the ideal ceiling without comparing it to
what is demonstrated and what is conventional defeats the purpose. The bracket —
three tiers and both gaps — is the deliverable. A theoretical-limit analysis
that reports only a ceiling is half-finished.

**Collapsing the two gaps into one.** Reporting a single "gap to the limit"
merges headroom somebody has already demonstrated with headroom nobody has ever
reached. Those carry very different risk: the first is a procurement question,
the second may be unreachable in principle. Report them separately.

**Using a model-dependent bound as the demonstrated tier.** A published "limit"
often answers a narrower question than the one being asked, and real systems
exceed it — Curzon-Ahlborn is the worked case in Example A, where the observed
figure beats the "bound" by ~7 points. Ask what the bound actually constrains
and under what assumptions before promoting it to a tier. The demonstrated tier
takes an observed, cited figure, never a calculated one.

**Bracketing across mismatched bases or populations.** Comparing an LHV figure
with an HHV figure, a thermal quantity with an electrical one, or one modern
unit with a whole fleet average, produces a gap that is an artifact of the
accounting rather than a fact about the system. State the basis of every tier;
where they differ and cannot be reconciled, say so and mark the gap as an upper
estimate rather than a measurement.

**Confusing theoretical-limit with estimate.** If the question is "how big is
this quantity rebuilt from units?" reach for estimate. Theoretical-limit answers
"what is the highest this quantity can be, given the governing laws?" — it is
asking about a bound, not a magnitude rebuild.

**Confusing theoretical-limit with inversion.** If the question is "what would
guarantee this claim fails?" reach for inversion. Theoretical-limit asks what
is *possible* once conventions are stripped; inversion asks what is *fatal* if
a necessary precondition breaks.

**Naming the law but not deriving the bound from first-principles values.**
Saying "the Carnot bound applies" without computing η_Carnot from the actual
reservoir temperatures is an incomplete analysis. The ceiling must be derived
from the specific physical constants, definitions, or measurements at hand —
not stated in the abstract.

---

## Handoff

The law-permitted ceiling and the bracketed gap produced by a theoretical-limit
drill are the natural input to **Phase 4 (Reason Upward)**, which is
theoretical-limit's primary destination in the 5-phase methodology.

**Feeding Phase 4:** The governing law, the law-permitted ceiling and the
bracketed gap to convention become the steps of a quantitative **Derivation
Chain** — see output-template.md §4 ("Derivation Chains") for the chain form
and its head grammar. Each step cites the ground truth that anchors it — a
physical constant, a definition, or a measurement assigned a GT-N identifier
in Phase 3. The gap is the key intermediate claim: a conclusion that depends
on a figure being near its physical limit is sound only if the gap confirms
that; a conclusion that depends on substantial remaining headroom is
contingent only if the gap confirms there is headroom to capture.

**Lighter Phase 1 anchor:** A theoretical-limit analysis often reframes the
core question identified in **Phase 1 (Identify the Essence)**. Establishing
the law-permitted ceiling forces the essence question into sharper focus: "Is
the performance limited by the laws, or by a convention we have not questioned?"
If the analysis reveals the conventional figure is far below the Carnot ceiling,
the Essence Statement may need to be revised to name the real constraint — not
"can we exceed 42%?" but "what engineering convention is blocking capture of the
21-point headroom the laws allow?"

**Cross-technique continuity (five-whys reduce-to-primitives → estimate → theoretical-limit):**
In the molten-salt running example, the five-whys reduce-to-primitives pass (Phase 3) produced the verified
primitives for the operating window and material properties; estimate (Phase 4)
rebuilt the cost magnitude from unit-factors. Theoretical-limit takes the same
domain and asks: given the reservoir temperatures that the five-whys reduce-to-primitives pass established as
ground truths, what does the Second Law permit? The three techniques form a
traceable chain across the same set of GT-N identifiers.

Theoretical-limit differs from estimate at the handoff boundary: estimate hands
off a *bracketed magnitude* (a quantity with explicit lower/upper bounds from
factor uncertainty); theoretical-limit hands off a *law-permitted ceiling and
a gap* (a hard bound the laws impose, and the distance current practice sits
below it). Both feed Phase 4, but they populate different steps in a Derivation
Chain — estimate populates the quantitative magnitude step; theoretical-limit
populates the physical-bound step.
