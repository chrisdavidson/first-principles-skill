# Phase 5: Domain-Spread Worked Examples — Research

**Researched:** 2026-05-17
**Domain:** Content authoring — first-principles analysis worked examples (pure Markdown)
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01 (problems):** Four concrete problems, one per domain — not negotiable:
  - EX-01 software/systems: A team wants to break a monolith into microservices to fix slow deploys — is that the right move?
  - EX-02 product/business: Should a SaaS product add a free tier to grow adoption?
  - EX-03 personal/general: Should I take a higher-paying job that requires relocating?
  - EX-04 science/engineering: How should an off-grid solar install be sized (battery and panels)?

- **D-02 (register):** Problems lean realistic and domain-authentic — the kind a real practitioner would face. Domain facts stay illustrative, not authoritative. Unverifiable domain facts go through the `GT-N?` mechanism.

- **D-03 (differentiation):** Each example makes a different part of the methodology its deepest section:
  - EX-01: Phase 1 Essence re-framing (symptom vs cause) + large Abandoned Reasoning section
  - EX-02: Phase 2 Challenge Assumptions — Classified Assumptions Table carries the analysis; dead-end is an analogy-ban violation
  - EX-03: Phase 1 Essence again but a different re-framing move (stated goal vs real goal); lighter derivation chains, human stakes
  - EX-04: Phases 3–4 Ground Truths + Derivation Chains (quantitative, physics-anchored) + Phase 5 confidence caveats with `GT-N?` input

- **D-04 (no contrived demonstrations):** Structural variety must be natural. Do not force "Nothing material here" escape valves, competing-conclusions, or GT-N? into examples where the problem does not genuinely call for them.

- **D-05 (no companion tools):** Examples are pure 5-phase. No 5-Whys, pre-mortem, or trade-off analysis appears in any example.

- **D-06 (no fixed length target):** Each example's length follows its problem and designated emphasis.

- **D-07 (no inline rubric verdict blocks):** Each file is a clean specimen of the output format. The rubric gate is checked at verification time; verdicts are not embedded in the example file.

### Claude's Discretion

- The specific framing, scenario details, and numbers within each locked problem
- The exact content of each example's six sections
- The precise per-example length band
- How many derivation chains and abandoned-reasoning entries each example carries (≥1 dead-end is the floor)
- Whether examples are authored one-per-plan or grouped, and the wave/dependency structure

### Deferred Ideas (OUT OF SCOPE)

- Self-referential "the skill analyzing its own design" example (tracked as META-01 in v2 requirements)
- Phase 6 navigation map wiring (this phase only authors the files; does not touch SKILL.md)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| EX-01 | `examples/` contains a software/systems worked example that follows the output format and shows at least one abandoned reasoning step | Scenario framing, ground truths, and dead-end documented in Sections 4–5 below |
| EX-02 | `examples/` contains a product/business worked example that follows the output format and shows a dead-end | Scenario framing, classified assumptions, and analogy dead-end documented in Sections 4–5 below |
| EX-03 | `examples/` contains a personal/general worked example that follows the output format and shows a dead-end | Scenario framing, real-goal re-framing, and relocation dead-end documented in Sections 4–5 below |
| EX-04 | `examples/` contains a science/engineering worked example that follows the output format and shows a dead-end | Solar scenario, physics ground truths, GT-N? input, and quantitative chains documented in Sections 4–5 below |
</phase_requirements>

---

## Summary

This is a pure content-authoring phase. There are no packages to install, no code to write, and no build steps. The research task is to gather the domain-authentic scenario details, realistic illustrative numbers, and plausible assumption structures the planner needs to hand authors a concrete brief for each of the four locked examples.

The four examples are independent of each other — no shared state, no cross-references between them. Each fills a 3-line stub file in `first-principles-thinking/examples/`. The canonical authoring contract is `references/output-template.md` (six fixed sections, strict order) and `references/validation-rubric.md` (six criteria, gate + hand-wavy cap). Both documents were read during this research and their requirements are reflected in every scenario brief below.

The differentiation strategy from D-03 is the key structural constraint: EX-01 emphasizes Phase 1 + large Abandoned Reasoning; EX-02 emphasizes Phase 2 (the Assumptions Table carries the weight); EX-03 emphasizes Phase 1 with a different re-framing type (stated-goal vs real-goal); EX-04 emphasizes Phases 3–4 with quantitative chains anchored in physical law plus a genuine GT-N? input and confidence caveat. These emphases are natural to the problems chosen — they do not need to be manufactured.

**Primary recommendation:** Author one example per plan in four independent parallel-eligible plans (EX-01 through EX-04), each with a single verification step that runs the validation rubric against the completed file.

---

## Architectural Responsibility Map

There is no multi-tier architecture in this phase. Every deliverable is a Markdown file.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Example authoring | Markdown file (`examples/*.md`) | — | Pure content; no code |
| Format compliance | `references/output-template.md` (consulted) | — | Template defines the six sections |
| Rubric gate | `references/validation-rubric.md` (consulted at verify time) | — | Gate check is a human/model review step, not a build step |
| Navigation wiring | Out of scope (Phase 6) | — | Phase 5 only authors the files |

---

## Standard Stack

No packages. No tools. No installation.

**Authoring contract:**
- Format: `first-principles-thinking/references/output-template.md` [VERIFIED: read in session]
- Gate: `first-principles-thinking/references/validation-rubric.md` [VERIFIED: read in session]
- Methodology spine: `first-principles-thinking/SKILL.md` [VERIFIED: read in session]
- Encoding: UTF-8, LF line endings, forward-slash paths (CLAUDE.md constraint)

---

## Package Legitimacy Audit

Not applicable — this phase installs no external packages.

---

## Architecture Patterns

### Recommended Project Structure

The four files to fill in are already in place:

```
first-principles-thinking/
└── examples/
    ├── software-systems.md    ← EX-01 (3-line stub; keep H1 heading)
    ├── product-business.md    ← EX-02 (3-line stub; keep H1 heading)
    ├── personal-general.md    ← EX-03 (3-line stub; keep H1 heading)
    └── science-engineering.md ← EX-04 (3-line stub; keep H1 heading)
```

Each stub currently contains only the `# Worked Example: [Domain]` H1 and a one-line description. The planner replaces everything below the H1 with the six-section output format. The H1 heading is preserved verbatim.

### Pattern: Six-Section Output Format

Every example follows this fixed section order with no omissions (from `output-template.md`):

```
## 1. Problem Essence
## 2. Assumptions Table
## 3. Ground Truths
## 4. Derivation Chains
## 5. Abandoned Reasoning
## 6. Conclusion
```

Each derivation chain uses the format:
```
GT-N + GT-M → [intermediate claim] → [conclusion]
```

Ground truth identifiers are stable (GT-1 stays GT-1 throughout the document). Unverified inputs carry the `?` suffix (GT-N?) and any chain consuming them must end with MEDIUM or LOW confidence plus a verification path.

### Anti-Patterns to Avoid

- **Omitting a section:** All six must appear. Use the honest-depth escape valve if a section has no genuine content — but the escape valve must be specific to this problem, not generic.
- **Missing intermediate step in a chain:** A chain that goes GT-N → conclusion directly is incomplete. The intermediate is where the reasoning lives.
- **Using the analogy-as-evidence move:** "Competitors do X" or "the industry standard is Y" cannot anchor a derivation chain. Analogies must be grounded in a named GT about the other situation.
- **Embedding rubric verdict blocks in the example file:** D-07 prohibits this. The example is a clean analysis specimen only.
- **Forcing `GT-N?` where the problem does not genuinely require it:** D-04 — only EX-04 authentically has an unverifiable input (daily energy load).
- **Adding companion-tool procedure inside an example:** D-05 prohibits 5-Whys, pre-mortem, or trade-off analysis appearing in any of the four files.

---

## Scenario Briefs (Per-Example Research Findings)

### EX-01: Software and Systems — Monolith-to-Microservices

**[ASSUMED]** Scenario framing below is illustrative and domain-authentic; specific numbers are chosen for plausibility, not empirical accuracy.

**Scenario setup:**
A 6-year-old e-commerce platform (catalog, cart, checkout, fulfillment all in one Rails/Django monolith, ~350 KLOC). The team has 12 engineers. CI/CD pipeline takes ~45 minutes end-to-end. A deploy requires a full test suite run and a coordinated restart; this makes it impossible to deploy faster than twice per day. The immediate complaint from engineering leadership: "deploys are too slow, we need microservices."

**Phase 1 Essence re-framing (D-03 emphasis):**
The triggering question is "should we move to microservices?" The re-framing operation for EX-01 is symptom→cause. The real question is: *What is actually causing slow deploys, and is architecture the bottleneck?* This distinction is the centerpiece of the example. Plausible causes that are architecture-neutral:
- The test suite is slow (not architecture — it is a test infrastructure problem)
- All services deploy together because of a shared database schema (a coupling problem solvable without splitting the monolith)
- The deploy pipeline has no parallelism (a CI/CD tooling problem)

The first-principles analysis should show that the Essence Statement rejects "should we do microservices?" as the question and replaces it with "what is the actual bottleneck in the deploy cycle, and what is the minimum intervention to remove it?"

**Assumptions to classify (for the Assumptions Table):**
| Assumption | Type | Note |
|------------|------|------|
| Microservices enable faster deploys | convention / untested belief | Widely believed but depends on team maturity and pipeline design; not a physical law |
| The deploy bottleneck is architectural coupling | untested belief | Never measured; the test suite may dominate |
| A 12-person team can operate a distributed system | untested belief | Microservices carry substantial ops overhead per service |
| Slow deploys are causing meaningful business harm | current constraint | Real but needs quantification |
| A rewrite is required to change the architecture | untested belief (false) | Strangler fig pattern is an alternative; assumption should be discarded |

**Ground truths (verified/verifiable facts):**
- GT-1: The full test suite runs 45 minutes on the current pipeline (measured)
- GT-2: A deploy requires a full pipeline pass (observed CI config)
- GT-3: The team currently ships ~2 deploys/day maximum (measured)
- GT-4: Operating microservices requires per-service monitoring, independent deployment pipelines, and inter-service communication contracts (architectural fact — source: published microservices literature, e.g., Newman "Building Microservices")
- GT-5: The current monolith uses a single shared relational database schema (observed codebase)

**Plausible dead-end (Abandoned Reasoning, the centerpiece per D-03):**

Dead end: "Split the monolith as specified." What was tried: reason from "microservices = faster deploys" directly to a migration plan. Why abandoned: the chain requires accepting "microservices enable faster deploys" as a ground truth, but that claim is an untested belief — it is not physically or logically true (a monolith with a parallelized test suite and blue-green deploys can deploy in minutes; a microservices system with synchronous inter-service dependencies can be slower). The chain collapses because its GT is actually an untested belief that does not survive Phase 2 scrutiny. What it rules out: the assumption that architecture is the primary bottleneck — ruling this out redirects the analysis to measuring the actual bottleneck first.

**Conclusion direction:** The first-principles analysis does not recommend microservices. It recommends: (1) measure the actual bottleneck (test parallelization and pipeline profiling first), (2) decouple the shared database schema if coupling is confirmed as the deploy barrier, (3) revisit the microservices question only after bottleneck removal. The key insight is that "slow deploys" is not an architecture diagnosis — it is a symptom that could be caused by several independent factors, and architecture migration is the highest-cost intervention.

**Structural notes for planner:**
- Recommended length band: 350–450 lines (long Abandoned Reasoning is the point of EX-01)
- Abandoned Reasoning should have 2 dead-ends: (1) the "just split the monolith" path, (2) an intermediate "move the test suite to a faster runner" path that was explored but found insufficient on its own
- Derivation chains: 3 chains covering (a) why the architecture is not the primary bottleneck, (b) why the coupling problem is separable from microservices, (c) what the minimum viable intervention is
- All six rubric criteria should score Rigorous; EX-01 has no genuine GT-N? input (the relevant facts are measurable)

---

### EX-02: Product and Business — Free Tier for SaaS Adoption

**[ASSUMED]** Scenario framing below is illustrative and domain-authentic; specific numbers are chosen for plausibility, not empirical accuracy.

**Scenario setup:**
A B2B SaaS project-management tool, 3 years old, $2.4M ARR, 240 paying teams (average $10K/year contract). No free tier currently. The product team wants to add a free tier (up to 5 users, limited projects) to drive top-of-funnel adoption and convert free users to paid. The stated assumption driving the proposal: "all our competitors have a free tier, so we need one to compete."

**Phase 2 Assumptions emphasis (D-03):**
The Classified Assumptions Table carries the analysis for EX-02. The key move is to classify the competitor-comparison statement as an analogy-as-evidence attempt (a convention or untested belief) and show that it cannot anchor a derivation chain without being grounded in a named GT about those competitors' actual conversion economics. The Table should be visibly the densest section of this example.

**Assumptions to classify (for the Assumptions Table):**
| Assumption | Type | Note |
|------------|------|------|
| A free tier drives top-of-funnel growth | untested belief | Not measured for this product; true for some products, not for others |
| Free users convert to paid at a meaningful rate | untested belief | The conversion rate is the core question; no data for this product |
| Competitors' free tiers are profitable / growing them | untested belief | Competitor economics are not observable without published data |
| Free tier acquisition cost is lower than current paid acquisition cost | untested belief | Unverified; free users require support and infrastructure |
| The product's current ICP (ideal customer profile) responds to free trials | convention / untested belief | B2B enterprise buyers often do not self-serve into free tiers; buying is procurement-driven |
| "All our competitors have a free tier" is evidence we should have one | convention | Analogy-as-evidence; violates the no-analogies-as-direct-evidence rule unless grounded in a named GT |
| Adding a free tier has no opportunity cost | untested belief (false) | Engineering bandwidth, support load, pricing-page complexity, and deal-desk overhead are all real |

**Ground truths (verified/verifiable facts):**
- GT-1: Current ARR is $2.4M from 240 teams at approximately $10K/team/year (measured)
- GT-2: The product's current acquisition model is primarily outbound sales and referrals (known channel mix)
- GT-3: Free tier infrastructure and support must be budgeted separately from the paid-tier cost structure (accounting fact)
- GT-4: Free-to-paid conversion rate for the specific product in this ICP segment is unknown and has not been measured (verified gap)

**Note on GT-4:** GT-4 is verified as a gap — the rate is genuinely unknown, not merely unquantified. This is a current constraint (the company hasn't run the experiment), not a physical law. In the Assumptions Table, "free users convert at a meaningful rate" is an untested belief with Verdict: Challenge, Verification: "unverified — flagged."

**Plausible dead-end (Abandoned Reasoning, per D-03):**

Dead end: "Competitors have free tiers, therefore we need one." What was tried: use competitor behavior as direct evidence that a free tier is necessary for competitive parity. Why abandoned: this is an analogy-as-evidence move — the competitors' free tiers may operate in a different ICP segment, at a different ARR stage, or with a different cost structure. Without a named GT about their conversion economics, the competitor evidence cannot anchor a derivation chain. The no-analogies-as-direct-evidence rule (Phase 4 operation) requires the argument to be grounded in a verified fact about this product, not in observed competitor behavior. What it rules out: competitor parity as a sufficient justification. A free tier decision must be justified on this product's own economics.

**Conclusion direction:** The first-principles analysis does not recommend adding a free tier at this time. It recommends: run a time-boxed pilot (limited cohort, 90-day window) to generate the empirically-missing conversion rate data (GT-4 verification). If the pilot shows conversion above a pre-specified threshold, adopt the free tier; if not, the decision changes. The key insight is that "competitors do it" is not a valid reason to restructure a B2B pricing model — the question is whether this product's economics support a free tier, which is an empirical question, not a convention to follow.

**Structural notes for planner:**
- Recommended length band: 250–350 lines (Assumptions Table is the widest section)
- Assumptions Table: 6–8 rows, all populated with non-generic Treatment and Verification cells
- Derivation chains: 2–3 chains; the main chain should show how the missing conversion rate data (GT-4 as an unverified gap, referenced from the assumptions) causes the conclusion to be "pilot first" rather than "yes" or "no"
- Abandoned Reasoning: 1 clear dead-end (the competitor-parity argument)
- EX-02 does not use `GT-N?` notation — GT-4 is a verified gap (we know we don't have the data), not an unverified belief used in a chain. The chain's conclusion is "pilot to get the data" — so no chain depends on an unverified belief.

---

### EX-03: Personal and General — Higher-Paying Job Requiring Relocation

**[ASSUMED]** Scenario framing below is illustrative and domain-authentic; specific numbers are chosen for plausibility, not empirical accuracy.

**Scenario setup:**
A software engineer, 5 years at current company in a mid-sized city (Portland, OR). Offer from a large tech company in San Francisco: $70K annual compensation increase (base + equity), but requires physical relocation and in-office 3 days/week. Current role allows full remote. Partner has an established career in Portland. The surface question: "should I take this job?"

**Phase 1 Essence re-framing (D-03 emphasis):**
The re-framing operation for EX-03 is stated-goal vs real-goal. The stated question is "should I take this job?" — framed as a binary decision. The re-framing reveals that the real goal is not maximizing compensation; it is something like "am I on a career trajectory that will let me achieve what I care about in 5–10 years, and does this offer accelerate or threaten that trajectory?" This is a different re-framing from EX-01 (which was symptom→cause). The key phase 1 move: identify what the person actually cares about, then ask whether the offer addresses it.

**Why this is structurally distinct from EX-01 despite both emphasizing Phase 1:**
EX-01's re-framing is diagnosis-level (what is actually causing the problem?). EX-03's re-framing is goals-level (what is the person actually trying to achieve?). They demonstrate two different re-framing operations: EX-01 strips away a proxy solution to find the real constraint; EX-03 strips away a proxy metric (compensation) to find the real objective. The analysis structure and the tone (human stakes, not technical) are visibly different.

**Assumptions to classify (for the Assumptions Table):**
| Assumption | Type | Note |
|------------|------|------|
| Higher compensation = better career outcome | convention / untested belief | Depends on what the person values and what the money enables |
| San Francisco cost of living increase partially offsets the compensation gain | current constraint | SF CoL is measurable; an estimate can be verified |
| The partner's career cannot relocate | current constraint | Should be treated as a real constraint; but the expiry condition is "if the partner's employer offers remote work or a SF transfer" |
| In-office 3 days/week is a stable requirement | current constraint | May change; but should be treated as real for the decision horizon |
| The new company's prestige will accelerate future opportunities | untested belief | Not verifiable in advance; depends on specific team, manager, and company trajectory |
| The decision is about the compensation delta | untested belief (the stated-goal assumption to discard) | This assumption frames the decision as financial, which may not reflect the actual objective |

**Ground truths (verified/verifiable facts):**
- GT-1: Annual compensation increase is $70K (stated in offer letter)
- GT-2: San Francisco median 1-BR rent is approximately $2,800/month vs Portland approximately $1,500/month — a gap of approximately $1,300/month or $15,600/year (approximate, verifiable via rental listings; illustrative)
- GT-3: State income tax difference: California top marginal rate ~13.3% vs Oregon ~9.9% on income above $125K — meaning a meaningful portion of the nominal increase is taxed at higher rates (verifiable from state tax schedules)
- GT-4: Partner's career is currently rooted in Portland-based employment with no remote option (current constraint; stated)
- GT-5: The analyst's stated long-term goal is [stated explicitly by the person — left as a blank to be filled from the conversation; this is not assumed]

**Note on GT-5:** This is the crux of the Phase 1 re-framing. The real-goal identification requires the person to state what they actually care about. The analysis cannot proceed from first principles if the real goal is substituted with "take the higher salary." This is the point where EX-03's Essence Statement is most interesting: the success criteria must be stated in terms of the real goal, not the compensation delta.

**Plausible dead-end (Abandoned Reasoning, per D-03):**

Dead end: "Take the job — $70K more is always better." What was tried: treat the compensation delta as the primary decision variable and reason from "more money = better decision." Why abandoned: this framing treats the decision as financially optimizable, but GT-2 and GT-3 show the effective gain after CoL and tax is substantially smaller than $70K (rough estimate: ~$45–50K effective after CoL gap and marginal tax difference). More importantly, the chain assumes the analyst's goal is to maximize compensation — but that assumption was discarded in Phase 2 as the stated-goal assumption. The real goal (GT-5, as stated) may involve things the compensation delta does not address: partner's career, lifestyle continuity, proximity to community. What it rules out: treating this as a financial optimization problem.

**Conclusion direction:** The analysis does not produce a binary "yes" or "no" — it produces a decision framework: the offer is worth taking only if (a) the effective after-CoL-and-tax gain is sufficient relative to what the person values, AND (b) the partner situation has a viable path (negotiated relocation, remote role, etc.), AND (c) the career acceleration the new role offers demonstrably serves the real goal. The key insight is that framing this as a compensation decision obscures the real trade-offs, most of which are not financial.

**Structural notes for planner:**
- Recommended length band: 200–300 lines (lighter derivation chains, human stakes — per D-03)
- Assumptions Table: 5–6 rows; the stated-goal assumption gets Verdict: Discard
- Derivation chains: 2–3 chains; the main chain should reason from the real goal (GT-5) and the effective compensation delta (GT-1 + GT-2 + GT-3) to the conditional recommendation
- Abandoned Reasoning: 1 dead-end (the pure-compensation framing)
- Tone: personal and human, not technical — the analysis should read as something a thoughtful person would actually do before making a life decision

---

### EX-04: Science and Engineering — Off-Grid Solar Sizing

**[ASSUMED]** Scenario framing and numbers below are illustrative. The physics relationships are genuine (Ohm's law, energy conservation, solar irradiance relationships). Specific numbers are plausible for the described site but not empirically derived.

**Scenario setup:**
A cabin in the high desert of New Mexico (35° N latitude). Year-round occupancy by 2 adults, no grid connection available. Loads: LED lighting (6 fixtures × 10 W, average 4 hours/day), a 12 V DC refrigerator (45 W average draw, runs ~50% duty cycle), a laptop (65 W, 6 hours/day), a water pump (250 W, 30 minutes/day), and a small inverter for occasional AC loads (estimated 100 W average, 2 hours/day). The question: what panel array and battery bank are needed?

**Phase 3–4 emphasis (D-03):**
EX-04 is the designated home for quantitative derivation chains anchored in physical law. The Ground Truths section is the longest and most structured section of this example. Each chain has real intermediate steps where unit conversions and physical relationships are made explicit.

**Physics relationships (genuine ground truths):**

- Energy in = Energy out × (1 / system efficiency) — conservation of energy, no exceptions
- Peak Sun Hours (PSH): average daily solar irradiance equivalent to 1,000 W/m² for a given location and season. High-desert NM at 35° N: approximately 5.5–6.5 PSH (annual average); winter minimum approximately 4.5 PSH. [ASSUMED — plausible; actual values vary by exact site and elevation; verifiable via NREL PVWatts or similar]
- Panel output: rated wattage × PSH × system derating factor = daily Wh from one panel
- System derating factor: accounts for temperature losses, wiring losses, MPPT efficiency, inverter efficiency — typically 0.75–0.85 for a well-designed system [ASSUMED — industry convention, verifiable from NREL documentation]
- Battery capacity rule: size for N days of autonomy (days without solar generation) at the target depth-of-discharge (DoD). Lithium iron phosphate (LiFePO4): 80% DoD safe; lead-acid: 50% DoD
- Days of autonomy for off-grid desert: 2–3 days typical (winter storms can cause 2 consecutive overcast days) [ASSUMED — conventional design practice; verifiable from NABCEP or similar]

**Load calculation (the GT-N? input):**

| Load | Power (W) | Hours/day | Daily energy (Wh) |
|------|-----------|-----------|-------------------|
| LED lighting | 60 W total | 4 h | 240 Wh |
| 12 V refrigerator | 22.5 W avg (45 W × 50% duty) | 24 h | 540 Wh |
| Laptop | 65 W | 6 h | 390 Wh |
| Water pump | 250 W | 0.5 h | 125 Wh |
| AC inverter loads | 100 W | 2 h | 200 Wh |
| **Total daily load** | | | **~1,495 Wh/day ≈ 1.5 kWh/day** |

The daily load estimate (1.5 kWh/day) is the **GT-N? input**. Why it is genuinely unverifiable: actual usage depends on occupant behavior, season (lighting hours vary, refrigerator duty cycle varies with ambient temperature), and what "occasional AC loads" actually means in practice. The 1.5 kWh/day figure is a best-estimate from stated load descriptions, not a measured value. Any chain depending on it must carry MEDIUM confidence and state what verification would raise it (install a energy monitor for 30 days before committing to a system size, or size conservatively with margin).

**Derived ground truths (physics-based):**
- GT-1: Peak Sun Hours (annual average) at the site: approximately 5.5 PSH — source: NREL solar radiation maps (illustrative; verifiable via NREL PVWatts for the specific coordinates)
- GT-2: System derating factor: 0.80 (conservative, accounts for all losses) — source: standard design practice
- GT-3: Battery technology: LiFePO4, 80% DoD safe — source: battery chemistry fact
- GT-4: Desired autonomy: 3 days (covers winter storm scenarios) — current constraint / design decision
- GT-5?: Daily energy load estimate: 1.5 kWh/day — unverified (GT-5? because it cannot be verified without a monitoring period or on-site measurement)

**Derivation Chains:**

Chain 1 — Panel sizing:
```
GT-1 (5.5 PSH) + GT-2 (0.80 derating) + GT-5? (1.5 kWh/day load)
→ Required daily panel output = 1.5 kWh / 0.80 = 1,875 Wh/day
→ Panel capacity needed = 1,875 Wh / 5.5 PSH = ~341 W of panels
→ Recommendation: 400 W array (e.g., 2 × 200 W panels) with 17% margin for winter PSH variability
Confidence: MEDIUM — depends on GT-5? (unverified daily load). Verification: install energy monitor for 30 days; if load exceeds 1.8 kWh/day consistently, upsize to 3 × 200 W.
```

Chain 2 — Battery sizing:
```
GT-5? (1.5 kWh/day) + GT-3 (80% DoD) + GT-4 (3 days autonomy)
→ Total energy to store = 1.5 kWh × 3 days = 4.5 kWh of usable capacity
→ Required battery capacity = 4.5 kWh / 0.80 DoD = 5.625 kWh total rated capacity
→ Recommendation: 6 kWh LiFePO4 bank (e.g., 2 × 100 Ah × 24 V = 4.8 kWh, or 1 × 200 Ah × 24 V = 4.8 kWh; round up to 6 kWh for practical sizing)
Confidence: MEDIUM — depends on GT-5? (unverified daily load). If measured load is significantly higher, additional battery capacity is required.
```

**Plausible dead-end (Abandoned Reasoning, per D-03):**

Dead end: "Size to the peak instantaneous load, not the daily energy." What was tried: reason from the highest-wattage load (water pump at 250 W) as the sizing constraint — build a system that can deliver 250 W continuously. Why abandoned: the pump runs only 30 minutes/day. Sizing the battery and panel array to sustain 250 W continuously would produce a massively overbuilt system (6× the required capacity). The relevant constraint is daily energy throughput, not peak instantaneous power — the correct variable for sizing storage and generation is Wh/day, not W. Peak power matters only for inverter sizing and wire gauge, not for panel and battery capacity. What it rules out: using peak load as the primary sizing metric.

**Structural notes for planner:**
- Recommended length band: 350–450 lines (Ground Truths + Derivation Chains are the longest sections)
- Ground Truths: 5 entries (GT-1 through GT-4 verified/conventional; GT-5? unverified)
- Derivation chains: 2 main chains (panel sizing, battery sizing) with explicit intermediate unit-conversion steps
- Abandoned Reasoning: 1 dead-end (peak-load fallacy)
- Confidence: both main chains are MEDIUM; Conclusion confidence is MEDIUM; the verification path (install monitor, re-measure) must be stated explicitly
- The `GT-N?` suffix and MEDIUM confidence rating are the structurally novel features of EX-04 — they appear here because the problem genuinely has an unverifiable input, not as a contrived demonstration (D-04)

---

## Structural Distinctiveness Confirmation (Success Criterion 4)

The concern is whether any two examples collapse into the same skeleton. Checking D-03's four emphases against each example's actual structural shape:

| Feature | EX-01 | EX-02 | EX-03 | EX-04 |
|---------|-------|-------|-------|-------|
| Deepest section | Phase 1 Essence + Abandoned Reasoning (2 dead-ends) | Phase 2 Assumptions Table (6–8 rows, carries the analysis) | Phase 1 Essence (different re-framing type) | Phases 3–4 Ground Truths + quantitative chains |
| Tone | Technical/engineering | Business/product | Personal/human | Quantitative/physical |
| Abandoned Reasoning size | Large (centerpiece) | Small (1 dead-end) | Small (1 dead-end) | Small (1 dead-end) |
| Derivation chains | 3 chains (qualitative) | 2–3 chains (qualitative with empirical gap) | 2–3 chains (mixed qualitative/quantitative) | 2 chains (explicit unit arithmetic) |
| GT-N? notation | No | No | No | Yes (GT-5?) |
| Conclusion confidence | HIGH | MEDIUM (pilot recommended) | MEDIUM (conditional) | MEDIUM (load unverified) |
| Key re-framing move | Symptom→cause | Untested belief dominates the table | Stated-goal→real-goal | Unverifiable input forces caveat |
| Size band | 350–450 lines | 250–350 lines | 200–300 lines | 350–450 lines |

**Risk assessment:** EX-01 and EX-03 share Phase 1 emphasis, as noted in D-03. The risk that they collapse into the same skeleton is LOW because:
- EX-01 is domain-technical, uses engineering measurements as GTs, and has a large Abandoned Reasoning section as its centerpiece
- EX-03 is personal, uses human stakes (partner career, CoL delta, real-goal identification), has a lighter chain structure, and the Phase 1 re-framing is a different logical operation (goals vs diagnosis)
- A reader who reads both examples in sequence will not mistake one for the other

No two examples share the same deepest section, tone, or primary structural feature. Success Criterion 4 is satisfiable with the scenarios as scoped.

---

## Wave/Plan Structure Recommendation

**Recommendation:** Four independent plans, one per example, fully parallel-eligible.

**Rationale:**
- No shared state between EX-01, EX-02, EX-03, EX-04. Each writes one file.
- No cross-references between example files (those are wired in Phase 6, not here).
- Parallelism reduces risk: a problem with one example does not block the others.
- Each plan should have a single verification step: apply the validation rubric from `references/validation-rubric.md` against the completed file. The example passes if no criterion scores Absent and at most one scores Hand-wavy.

**Suggested wave structure:**

| Wave | Plans | Note |
|------|-------|------|
| Wave 1 | EX-01, EX-02, EX-03, EX-04 (all parallel) | Independent; no sequencing needed |

If the planner chooses sequential ordering for any reason (e.g., author capacity), the natural ordering is EX-01 first (highest complexity, most to learn from) and EX-04 second (most structurally novel due to GT-N?). EX-02 and EX-03 are lower-complexity and could be authored quickly once EX-01 is complete.

**Per-plan structure (each of the four plans):**
1. Read `references/output-template.md` and `references/validation-rubric.md` (authoring contract)
2. Author the six-section analysis from the scenario brief in this RESEARCH.md
3. Apply the validation rubric: quote-and-score each criterion; fix any Absent or second Hand-wavy
4. Write the completed file to `first-principles-thinking/examples/<domain>.md`

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Output format definition | A custom section structure | The existing `output-template.md` verbatim | The template is already the authoring contract; diverging creates an inconsistency with what the methodology spec promises |
| Rubric scoring | A new scoring scheme | `validation-rubric.md` as-is | The rubric is the gate; inventing new criteria undermines the self-consistency of the skill |
| Solar physics formulas | A derived or approximated version | The documented relationships (energy conservation, PSH × derating = daily output) | These are physical law; the only variable is which inputs are verified vs GT-N? |

---

## Common Pitfalls

### Pitfall 1: Writing the Example as a Recommendation Document, Not an Analysis

**What goes wrong:** The author writes "here's our recommendation: do X" without showing the Phase 1–5 operations that produced it. The output reads like a consulting deck, not a first-principles analysis.

**Why it happens:** It is natural to jump to conclusions. The methodology explicitly requires each phase's artifact to be visible in the output.

**How to avoid:** Write from the artifact chain forward: Essence Statement first (one sentence, success criteria), then the Assumptions Table (every row populated), then Ground Truths (each with a source or `?` suffix), then Derivation Chains (each with an explicit intermediate step). The analysis should be auditable — a reader should be able to verify each phase was executed, not just that a good recommendation was made.

**Warning signs:** A short Problem Essence section with no success criteria; an Assumptions Table with empty Verification cells; Derivation Chains with no intermediate step (GT-N → conclusion directly).

### Pitfall 2: Using the Analogy-as-Evidence Move

**What goes wrong:** The chain for EX-02 might say: "Competitors use free tiers, therefore we should." This is a direct violation of the Phase 4 no-analogies-as-direct-evidence rule.

**Why it happens:** Analogies feel like evidence. They are persuasive in informal reasoning.

**How to avoid:** Any reference to what others have done must be grounded in a named GT about their situation. Since we typically cannot verify competitor conversion economics, the analogy collapses into an untested belief.

**Warning signs:** Any derivation chain that cites "industry standard," "competitors do X," or "similar companies have found" without a named GT anchoring the claim.

### Pitfall 3: Dropping the Intermediate Step from a Derivation Chain

**What goes wrong:** A chain reads "GT-1 + GT-2 → [conclusion]" with no intermediate claim. This is structurally invalid per the output template and will score Sound (at best) on Criterion 4 of the rubric.

**Why it happens:** When the conclusion feels obvious from the GTs, the intermediate step is skipped.

**How to avoid:** The intermediate must be a claim that could not be stated from either GT alone. For EX-04: "GT-1 + GT-2 → Required daily panel output = 1.5 kWh / 0.80 = 1,875 Wh/day" is a valid intermediate because neither GT-1 nor GT-2 alone implies this value — it requires combining them with the load figure.

**Warning signs:** Any chain with exactly two steps (GT-IDs → conclusion).

### Pitfall 4: Embedding Rubric Verdict Blocks in the Example File

**What goes wrong:** The author includes a rubric scoring section at the end of the example file ("Criterion 1: Rigorous. Criterion 2: Rigorous..."). D-07 prohibits this.

**Why it happens:** The rubric is the verification step, so it feels natural to show the result.

**How to avoid:** The verification is done at plan verification time, not embedded in the file. The example file must be a clean specimen of the output format only.

### Pitfall 5: Generic Escape Valve Use

**What goes wrong:** The Abandoned Reasoning section of EX-02 or EX-03 reads "Nothing material here — no dead ends were encountered." This is the generic escape valve (copy-pasteable to any analysis) and scores Hand-wavy on Criterion 4.

**Why it happens:** The specific dead-end is not obvious.

**How to avoid:** Each of the four examples has a domain-authentic dead-end identified in the scenario briefs above. Use those. If the escape valve is genuinely needed for some sub-section, the reason must be specific: "Nothing material here — the problem's constraint space reduces to a single feasible path after GT-2 eliminates the peak-load sizing approach; the dead-end documenting that elimination appears above."

---

## Runtime State Inventory

Not applicable — this is a greenfield content-authoring phase. No rename, refactor, or migration is involved.

---

## Environment Availability

Not applicable — pure Markdown content authoring. No external tools, services, or runtimes are required beyond a text editor and git.

---

## Validation Architecture

The validation rubric is `references/validation-rubric.md`. It is applied manually (human or model review), not by an automated command. There is no test framework.

**Per-example gate:**
- Read the completed example file
- Apply all 6 rubric criteria in order; produce one verdict block per criterion (quoted span + band + justification)
- Gate cleared = no criterion scores Absent AND at most one criterion scores Hand-wavy
- If gate not cleared: revise the flagged sections and re-score

**Wave gate:** All four examples clear their individual rubric gates before Phase 5 is marked complete.

No automated test commands exist or are appropriate for this phase. The verification is document-quality review.

---

## Security Domain

Not applicable — pure Markdown skill content, no executable code, no user data, no network access, no secrets.

---

## Open Questions

1. **GT-5? in EX-04 — how much detail in the load table?**
   - What we know: the scenario brief provides a per-load breakdown summing to 1.5 kWh/day
   - What's unclear: whether the load table should appear in the Ground Truths section (as supporting evidence for GT-5?) or be presented inline in the Derivation Chain
   - Recommendation: put the load breakdown in the Ground Truths section as the derivation of GT-5? — it makes the unverified input's basis visible and shows why it cannot be verified without monitoring. The chain then references GT-5? by ID.

2. **EX-03 real goal (GT-5) — how is it populated?**
   - What we know: the scenario brief notes that GT-5 ("the analyst's stated long-term goal") must be stated by the person
   - What's unclear: for a worked example (not a live conversation), the author must choose a specific goal to instantiate GT-5
   - Recommendation: the planner should instantiate GT-5 with a concrete stated goal, e.g., "build expertise in distributed systems within 3 years and reach a principal-level role" — something plausible for a 5-year engineer considering a large-tech-company offer. This makes the analysis traceable rather than abstract.

3. **EX-02 conclusion confidence — HIGH or MEDIUM?**
   - What we know: the chain leading to "pilot first" rests on the verified absence of conversion data (GT-4 is a known gap, not an unverified belief used in a chain); the chain itself does not depend on any GT-N? input
   - What's unclear: should the conclusion confidence be HIGH (the recommendation to pilot is well-supported) or MEDIUM (uncertainty about whether the pilot is the right framing)?
   - Recommendation: HIGH confidence for the "run a pilot" conclusion (the recommendation follows from the verified data gap); the uncertainty is acknowledged in the trade-offs section (the pilot has a cost and a time horizon).

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | EX-01 scenario setup (350 KLOC monolith, 45 min CI, 12 engineers) | Scenario Briefs — EX-01 | If implausible, the analysis reads as a toy example; adjust numbers for plausibility |
| A2 | EX-01 test suite is 45 minutes end-to-end | Scenario Briefs — EX-01 | Plausible for a large monolith; illustrative |
| A3 | EX-02 $2.4M ARR, 240 teams at $10K/year | Scenario Briefs — EX-02 | Illustrative B2B SaaS figures; plausible |
| A4 | EX-03 Portland vs SF rent gap ~$1,300/month | Scenario Briefs — EX-03 | Based on approximate 2024–2025 rental market levels; plausible; author should verify rough order of magnitude |
| A5 | EX-03 California vs Oregon marginal tax rate difference | Scenario Briefs — EX-03 | Rates from training knowledge; plausible; author should note they are illustrative |
| A6 | EX-04 Peak Sun Hours 5.5 at 35° N high desert NM | Scenario Briefs — EX-04 | Plausible; NREL PVWatts would give a more precise value; the illustrative number is in the right range |
| A7 | EX-04 system derating factor 0.80 | Scenario Briefs — EX-04 | Industry convention; plausible; tagged as conventional in the analysis |
| A8 | EX-04 daily load estimate 1.5 kWh/day | Scenario Briefs — EX-04 | This is the GT-5? input; explicitly flagged as unverified in the analysis |

**All A-numbered claims above are tagged [ASSUMED]. They are plausible and internally consistent, but they have not been verified against authoritative data sources in this session. They are chosen to be realistic for the domain, and D-02 explicitly states domain facts stay illustrative — this is by design, not a deficiency.**

---

## Sources

### Primary (HIGH confidence)
- `first-principles-thinking/references/output-template.md` — read in session; authoritative for the six-section format, section prescriptions, escape valve rules, GT-N? notation, derivation chain format
- `first-principles-thinking/references/validation-rubric.md` — read in session; authoritative for the 6 scoring criteria, 4-level scale, gate conditions, hand-wavy cap, verdict block format
- `first-principles-thinking/SKILL.md` — read in session; authoritative for the 5-phase methodology, four assumption types, prescribed treatments, Phase 4 no-analogies rule
- `.planning/phases/05-domain-spread-worked-examples/05-CONTEXT.md` — read in session; authoritative for locked decisions D-01 through D-07 and success criteria

### Secondary (MEDIUM confidence)
- Solar physics relationships (energy conservation, PSH × derating formula, DoD rules) — training knowledge consistent with NREL documentation; tagged [ASSUMED] for specific numbers; relationships are physical law
- B2B SaaS free tier economics and microservices architecture trade-offs — training knowledge; treated as plausible illustrative context per D-02

### Tertiary (LOW confidence)
- Specific illustrative numbers (Portland/SF rent gap, California/Oregon tax rates, monolith LOC, CI pipeline time) — [ASSUMED]; plausible but not verified in this session; treated as illustrative per D-02

---

## Metadata

**Confidence breakdown:**
- Output format and rubric requirements: HIGH — read directly from authoritative source files
- Scenario framings (structural, which assumptions to classify, which dead-ends to use): HIGH — derived from the methodology structure and locked problem descriptions
- Illustrative numbers (rent, tax, LOC, CI time, solar PSH): ASSUMED — plausible, explicitly tagged, not verified

**Research date:** 2026-05-17
**Valid until:** This phase; scenario details are fixed by CONTEXT.md D-01 and D-02 and will not change within v1.
