<!-- GENERATED — DO NOT EDIT. Source: shared/references/five-whys-detail.md. Regenerate via: scripts/sync-content.py --write. -->

<!-- markdownlint-disable MD041 -->

## Example

### Causal mode — bread going stale

**Symptom:** The bread keeps going stale before it is finished.

- Why? → The loaf is too large for one person to finish quickly.
  - Why? → Only standard-size loaves are bought.
    - Why else? — considered: the household eats less bread than it used to;
      rejected, weekly bread consumption has not changed — only the loaf size on
      offer has.
    - Why? → Half-loaves were not known to be available.
      - **Stop:** Corrective action — check the store for half-loaves or switch to a
        smaller format. Specific, in control, prevents recurrence. **(Branch ends here.)**
- Why (else at level 1)? → The bread is stored on the counter.
  - Why? → No one sealed the bag after the first slice.
    - Why else? — considered: the bag itself is defective and will not seal;
      rejected, the bag seals fine when the clip is used — the issue is that the
      clip is not at hand.
    - Why? → The bag clip is kept in a different drawer.
      - **Stop:** Corrective action — keep a clip at the bread storage point.
        Specific, in control, prevents recurrence. **(Branch ends here.)**

Both branches reach actionable corrective actions. The root causes are a purchasing
habit and a storage habit — not the bread itself.

### Reduce-to-primitives mode — solar panel claim

**Claim:** "A 200 W solar panel can charge a 100 Ah / 12 V battery from flat in roughly
one day of good sunlight."

**Immediate constituents:** C1: rated panel output ≈ 200 W; C2: "good sunlight" ≈ 5 peak
sun hours/day; C3: usable energy = wattage × peak sun hours × efficiency; C4: battery
capacity = 100 Ah × 12 V = 1,200 Wh.

- C1: datasheet spec under IEC 61215 → **Verified (measurement).**
- C2: site-specific empirical value; no specific site named → **Assumed — unverified.**
- C3: energy conservation / first law of thermodynamics → **Verified (physical law).**
- C4: watt-hour = watts × hours = volts × amp-hours (unit-conversion definition) →
  **Verified (definition).**

**Verdict:** C2 unverified → parent claim inherits the `?` flag. Also: the energy balance
is tight even before C2: 200 W × 5 PSH = 1,000 Wh before efficiency losses, already
below the 1,200 Wh demand — the decomposition surfaces both the site-uncertainty gap and
a quantitative shortfall independently.

---

## Failure modes

### Causal mode failure modes

**Stopping on a count, not a test.** Asking "why" exactly five times and declaring done
is the most common failure. Five is a typical depth, not a rule. Stop when the test is
met, not when the count is reached.

**Single-thread drilling.** Moving straight down one causal chain without asking "What
else caused this?" at each level. This misses parallel causes and produces an incomplete
picture.

**Inference without evidence.** Writing "probably because X" and continuing down that
branch. Every causal link needs observable evidence, or must be flagged as assumed.

**Confirmation bias.** Starting with a suspected cause and steering the chain toward it.
The lateral scan at each level ("What else caused this?") is the check against this — it
forces consideration of causes that contradict the hypothesis.

### Reduce-to-primitives mode failure modes

**Stopping on familiarity, not on the test.** Accepting a constituent as "obviously true"
because it feels familiar — an industry rule of thumb, a remembered figure — without
checking whether it passes the physical-law / definition / measurement stop test. Every
branch must reach an irreducible anchor, not just feel reducible enough.

**Halting the recursion mid-branch.** Decomposing two levels and then treating a
still-compound claim as a leaf because it became harder to unpack. The stop test is the
correct halt criterion, not the depth or the effort.

**Confusing the two modes.** Asking "Why is this wrong?" when you should be asking "What
is this made of?" If you find yourself tracing backwards through event chains or corrective
actions, you have drifted into causal mode. Recognize the shift and restart in the correct
mode — both are available here.

**Treating "it's in the spec" as a verified primitive.** A spec value bottoms out at a
direct measurement only if the spec was produced by a calibrated, traceable process. A
vendor promise in a slide deck is not a measurement; it is an untested belief and must be
flagged as assumed.

**Over-decomposing definitions.** Continuing to recursively unpack a formal definition
beyond its defined boundary — the definition of a watt-hour does not need to be derived
from quantum electrodynamics. A definition terminates the chain.

---

## Handoff

Both modes feed the 5-phase methodology but hand off different outputs.

**Causal mode (root-cause drill):** The root cause(s) identified here are inputs to the
5-phase methodology. If you reached for this mode during Phase 2 (Challenge Assumptions),
add each root cause as a challenged assumption row in the Classified Assumptions Table.
If you reached for it during Phase 3 (Establish Ground Truths), promote each
evidence-backed root cause to a ground truth — give it a stable GT-N identifier and a
source citation, or the `GT-N?` suffix if its causal link is still assumed rather than
verified. If you reached for it during Phase 4 (Reason Upward), add each cause as a
validated step in the relevant Derivation Chain.

**Reduce-to-primitives mode (irreducibility drill):** The primitives produced here are the
natural inputs to Phase 3 (Establish Ground Truths). Each branch that passes the stop test
(physical law / definition / measurement) becomes a candidate ground truth — assign it a
stable GT-N identifier and record the source citation (law name, definition reference,
measurement provenance). A branch that stops as `Assumed — unverified` enters the ground
truths list with the `GT-N?` suffix, inheriting the confidence caveat rules: any derivation
chain that consumes it is rated MEDIUM until the assumption is verified.

If reached during Phase 2 (Challenge Assumptions): add each verified primitive as an
`Accept` verdict in the Classified Assumptions Table; add each assumed branch as an
`untested belief` row with a `Challenge` verdict and a stated verification path.

If reached during Phase 4 (Reason Upward): add each verified primitive as a validated step
in the relevant Derivation Chain, citing the GT-N identifier that anchors it.

**Boundary between the two modes at handoff:** Causal mode hands off *causal root causes*
(the actionable correctives that stop recurrence); reduce-to-primitives mode hands off
*verified primitives* (the irreducible facts that anchor a claim). Both may enter Phase 3,
but they populate different rows of the Ground Truths list.
