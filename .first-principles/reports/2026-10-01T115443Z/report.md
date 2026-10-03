# PMO Design for a 30-Project Biotech Portfolio

*First-principles analysis · 1 October 2026*

## Executive Summary

**Recommendation:** Run a hard-timeboxed 6-week Phase 0 diagnostic (re-baseline the delay definition, build a root-cause distribution, build a cost-of-delay model) before building any structure (chain C2); then stand up a lean Supportive PMO (~3–4 FTE, COO-sponsored, governed through a Portfolio Governance Board of all 10 department heads) with a pre-committed, evidence-gated path to selective Controlling authority, Directive authority deferred indefinitely (chains C4, C5, C6).

**Band (from §6):** LOW overall by the chain-capping rule — the structural sequencing logic (diagnose-before-build, visibility-before-authority) is MEDIUM confidence, while the specific headcount bracket (chain C6) is LOW confidence and explicitly flagged as provisional pending Phase 0 data.

**Would change it:** Org-specific confirmation of the two unverified industry-general patterns (GT-8?, GT-9?) via the Phase 0 diagnostic itself would raise the structural-logic band toward HIGH; Phase 0's actual root-cause distribution and PM-headcount data would replace the industry-pattern staffing bracket (chain C6) with this organization's own figures.

## 1. Problem Essence

**Essence Statement:** Given a stated 43%-of-projects "significant delay" rate across ~30 concurrent projects embedded in 10 departments with no central PMO, and given that leadership's only proposed response so far (more reporting, more tracking, more resource-utilization management) was generated from intuition rather than diagnosis — what organizational structure, if any, should the organization build, and what is the evidence chain connecting diagnosed causes (not assumed ones) to that structure?

**Success criteria** (checkable against the Conclusion, section 6):

1. The analysis separates what is actually known about the 43% figure from what is merely assumed about it, before using it as a diagnostic signal.
2. At least six alternative root-cause hypotheses for the delay rate are enumerated and reasoned about for relative likelihood from the organization's structural facts, before any structural recommendation is made.
3. For every hypothesis a PMO cannot fix, the Conclusion names that limitation explicitly rather than implying a PMO is a universal fix.
4. A specific PMO type, reporting line, and staffing ratio is produced, with the reasoning shown as a derivation from the diagnosis — not asserted as industry convention.
5. A phased rollout is produced with explicit sequencing logic — in particular, the claim "visibility must precede resource-utilization control" is derived, not stated as received wisdom.
6. Headcount and build-vs-buy tooling reasoning is shown, tied numerically to the 30-project/10-department scale.
7. Falsifiable success metrics with pre-intervention baselines are produced, such that leadership can later determine the PMO investment failed, not only that it succeeded.
8. Second-order risks and a structured pre-mortem are produced, with each named structural weakness converted into either a plan change or an explicitly accepted, mitigated risk.

No success criterion requires the answer to be "build a PMO" — a finding that the correct response is a targeted non-PMO intervention, or a staged/partial PMO, would equally satisfy this essence statement.

## 2. Assumptions Table

Methodology note: this is a strategy problem with no external document corpus, data room, or codebase to cite. "Verification" below therefore means either (a) the fact is directly stipulated by the problem statement as given (treated as accepted without further challenge, since it is the client's own first-hand statement of their situation), or (b) the claim is a general industry pattern not yet confirmed for this specific organization, in which case it is flagged `unverified — flagged` and routed to the Phase 0 diagnostic recommended in section 4.

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | The 43% delay figure is measured using a consistent, shared definition of "significant delay" across all 10 departments | untested belief | verify — audit each department's reporting methodology before treating 43% as a comparable cross-org signal | Challenge — no evidence a shared definition or baseline exists; GT-1 (no PMO) implies no entity currently owns a shared standard | unverified — flagged |
| A-2 | Leadership's proposed fix (more reporting/tracking/resource-utilization management) addresses the true cause(s) of delay | convention | explicitly challenge — this is the "how we've always responded" pattern, not a diagnosis-derived response | Challenge — explicitly rejected as a premise by the user; treated as one candidate intervention among several, never as a default | unverified — flagged |
| A-3 | A PMO (of any type) is the correct structural response to the 43% delay rate | untested belief | do not assume; derive from the diagnosis in section 4, test via inversion | Challenge — this is the conclusion to be earned, not an input; see chain C4 | unverified — flagged, resolved in C4 |
| A-4 | Delays are primarily caused by factors inside an individual PM's control (discipline, scope management) rather than cross-department structural factors outside it | untested belief | verify via fishbone discriminating-observation step | Challenge — no current data distinguishes these; see C3 | unverified — flagged |
| A-5 | Specialist functions (regulatory affairs, QA, biostatistics, clinical operations) are shared across departments and subject to contention | current constraint (industry-typical biotech org pattern) | record expiry condition: confirmed or disconfirmed by a Phase 0 resource-conflict audit | Challenge — plausible given biotech org norms, but org-specific confirmation is required before sizing any resource-arbitration authority | unverified — flagged (GT-8?) |
| A-6 | No portfolio-level prioritization mechanism currently exists | current constraint | accept — follows near-deductively from GT-1 (no PMO = no entity tasked with cross-project prioritization) | Accept — this is a structural consequence of GT-1, not an independent claim | derived, not separately verified |
| A-7 | PMs are individually understaffed or overloaded (project-per-PM ratio too high) | untested belief | verify via a PM headcount/ratio audit — this data does not currently exist in the problem statement | Challenge — total PM headcount and PM:project ratio are unknown (see Ground Truths, "Known unknowns") | unverified — flagged |
| A-8 | Unclear scope/requirements at project initiation is a contributing cause | untested belief | verify via fishbone/stage-gate audit | Challenge — plausible, untested | unverified — flagged |
| A-9 | Lack of standardized stage-gates across the 10 departments is a contributing cause | current constraint | accept as structurally near-certain — no PMO means no entity owns a shared methodology mandate | Accept — follows from GT-1 and GT-2 jointly | derived, not separately verified |
| A-10 | Regulatory/QA review-cycle timelines are a contributing cause common to biotech portfolios | current constraint (industry-typical pattern) | record expiry condition: confirmed or disconfirmed by Phase 0 data | Challenge — a well-documented industry pattern, not yet confirmed for this organization | unverified — flagged (GT-8?) |
| A-11 | Executive leadership is willing to grant a new PMO function real cross-department authority (controlling or directive level) from day one | untested belief | do not assume; no data exists on executive appetite for ceding departmental authority | Challenge — explicitly tested via the trade-off's political-feasibility criterion (C4) rather than assumed in either direction | unverified — flagged |
| A-12 | Delays are costly to the business in a way that justifies new central overhead | current constraint (biotech-general: regulatory milestones, trial timelines, and patent/competitive clocks typically carry real schedule-cost sensitivity) | record expiry condition: the Phase 0 cost-of-delay model (section 6) either confirms or bounds this | Accept, provisionally — industry-general pattern strong enough to justify the low-cost Phase 0 investment, but the specific dollar magnitude is unverified | unverified — flagged (GT-8?) |

*Rows A-13 through A-18 below were surfaced by the end-of-phase Assumption Audit (section 4, after the Derivation Chains were built) and added back to this table per the methodology's audit-and-return rule — they were not visible before the chains were constructed.*

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-13 | Regulatory review timelines and specialist headcount levels are outside the PMO's own authority to change | current constraint | accept — structurally near-certain; a coordination function cannot compress an external agency clock or create FTEs it was not funded to hire | Accept | derived, not separately verified — surfaced at chain C3, step 3 |
| A-14 | The cost of a 6-week diagnostic delay is smaller than the cost of committing to the wrong structure | untested belief | verify qualitatively — priced explicitly as an accepted, mitigated risk rather than ignored | Challenge, provisionally accepted with mitigation | unverified — flagged; addressed as pre-mortem cluster C5 (section 4.10) — surfaced at chain C2, step 3 |
| A-15 | The standardized measurement methodology established in Phase 0 remains stable and unchanged through the Phase 2/3 measurement window | untested belief | verify by governance discipline — methodology changes after Phase 0 should be logged and flagged in reporting | Challenge | unverified — flagged; a methodology change mid-measurement would itself need disclosure to keep later comparisons falsifiable — surfaced at chain C7, step 2 |
| A-16 | The locked trade-off criterion weights (4.5) reasonably approximate this leadership team's actual priorities | untested belief | verify by confirming the weights with the actual executive sponsor before Phase 1 kickoff, not merely with this analysis's own judgment | Challenge | unverified — flagged; the flip test (4.5) shows the ranking is robust to reasonable disagreement about these weights, which bounds but does not eliminate this risk — surfaced at chain C4, step 1 |
| A-17 | An executive exists who both lacks direct departmental P&L stake and is willing to sponsor the PMO | untested belief | verify directly with leadership before finalizing the reporting line in chain C5 | Challenge | unverified — flagged — surfaced at chain C5, step 2 |
| A-18 | A commodity SaaS PPM tool exists that fits this organization's needs and budget without heavy customization | untested belief | verify via a short Phase 0/1 vendor evaluation | Challenge | unverified — flagged — surfaced at chain C6, step 2 |

## 3. Ground Truths

**Provenance scoping note.** This engagement has no external document corpus, data room, or system access to open — the only source for organization-specific facts is the problem statement itself, stipulated directly by the client. Facts stipulated this way (GT-1 through GT-7) carry no `?` — there is no deeper source to read, and the client's own first-hand statement of their situation is the ground floor of evidence available in this engagement. Facts drawn from general domain knowledge of biotech/PMO organizational patterns rather than from this organization's own data (GT-8, GT-9) are marked `?` as unverified for this specific org, per the Phase 3 provenance rule — no source was available to attempt opening for them, so no Phase 3 failure record applies; the mitigation is that the roadmap's own Phase 0 (section 4) is designed to produce the org-specific data that would resolve them.

1. **GT-1** — No Project Management Office currently exists in the organization. *Source: stipulated by problem statement.*
2. **GT-2** — Project Managers execute projects embedded within 10 different departments; there is no central office they report through. *Source: stipulated by problem statement.*
3. **GT-3** — Projects run at an average of 3 concurrent projects per department across 10 departments, ~30 projects total. *Source: stipulated by problem statement.*
4. **GT-4?** — 43% of projects are experiencing "significant delays." *Source: stipulated by problem statement* — marked `?` because the problem statement discloses no shared definition of "significant delay" and no description of the measurement methodology behind this figure (self-reported by PM, department-head estimate, or measured against a formal baseline schedule are all consistent with the given text). The figure is accepted as the client's own stated headline number, but its comparability across departments is unverified — see A-1 and chain C1.
5. **GT-5** — The cause of the delays is currently undiagnosed; leadership attributes them to "various reasons" with no attribution to specific root causes. *Source: stipulated by problem statement.*
6. **GT-6** — Leadership's currently-proposed response (more reporting, more tracking, more resource-utilization management) was generated from past experience/intuition, not from root-cause diagnosis. *Source: stipulated by problem statement — this is the explicit constraint governing this engagement.*
7. **GT-7** — The organization operates in the biotech industry. *Source: stipulated by problem statement.*
8. **GT-8?** — Biotech project portfolios commonly depend on shared, centrally-constrained specialist functions (regulatory affairs, QA/quality systems, biostatistics, clinical operations) serving multiple concurrent projects across departments, and commonly experience externally-controlled review-cycle timelines (IRB, agency review) as critical-path items. *Source: general domain pattern in biotech R&D organizational design; not verified against this organization's actual structure. Unverified — flagged.*
9. **GT-9?** — In multi-project, multi-department organizations, standardized cross-project visibility/data collection is a logical and commonly-observed prerequisite for distinguishing contention-, process-, and external-driven causes of delay, and typical supportive-PMO coordination staffing for pure reporting/coordination functions runs on the order of one portfolio analyst per 15–20 actively tracked projects. *Source: general domain pattern in project/portfolio management practice; not verified against this organization. Unverified — flagged.*

**Known unknowns (explicitly not ground truths — named rather than silently assumed):**

- Total PM headcount and the PM-to-project ratio within each department (the problem statement states projects-per-department, not PMs-per-department — these are not interchangeable, and the gap matters directly for diagnosing "PM overload" as a cause and for sizing any new structure).
- The specific definition and measurement method behind the 43% figure (see GT-4?).
- Whether delayed projects cluster in particular departments/project types or are evenly distributed.
- Whether delayed projects share common named dependencies (e.g., the same specialist resource pool).
- Quantified cost of delay per project (revenue, trial-timeline, or competitive impact).
- Whether 43% is a new/worsening figure or a long-standing baseline for this organization.
- Executive appetite for granting a new function real cross-department authority (A-11).

Per the Phase 3 verification step: no load-bearing ground truth in this analysis cites an external source that could be opened with Read/Grep/WebFetch — the entire evidentiary base is the client's own stipulated statement plus explicitly `?`-flagged industry-general patterns. `?`-marked: **GT-4, GT-8, GT-9 (3 of 9).**

## 4. Derivation Chains

### 4.1 Is the 43% figure itself trustworthy as a diagnostic signal? (chain C1)

```text
GT-4? (43% delay figure, methodology undisclosed) + GT-2 (PMs embedded in 10 separate departments, no shared standard)
→ absent a common definition of "delay" and a common schedule baseline, department-level self-reporting of "significant delay" is not guaranteed to be comparable across departments
→ the 43% headline may combine real schedule slip with definitional noise, in an unknown proportion
→ before 43% can be used as a diagnostic signal at all, the organization must first standardize the delay definition and re-baseline the measurement
```

**Confidence: MEDIUM.** Downgrade cause: GT-4? — the figure's measurement methodology is undisclosed; the verification that would remove this cause is the Phase 0 measurement-standardization audit named in section 4.4.

### 4.2 Alternative explanations for the 43% delay rate — fishbone (breadth-first cause-category brainstorm)

Decision rule: fishbone (causal breadth across categories) rather than five-whys (causal depth within one chain) was selected because, at this stage, no single cause is yet favored over the others — the task is to enumerate plausible categories before narrowing, which is exactly the condition fishbone is built for.

**Custom category set** (chosen over the generic default six because the domain signal — a multi-department project-delivery organization with embedded PMs and specialist dependencies — maps cleanly onto it): **People, Process, Resources/Dependencies, Visibility/Information, Governance/Prioritization, External/Regulatory.**

| Category | Candidate causes | Discriminating observation needed |
|---|---|---|
| People | PM overload (too many concurrent projects per PM); PM skill/experience gaps; inconsistent PM authority to escalate; high PM turnover | Same PMs appearing disproportionately across delayed projects; PM:project ratio data (currently unknown — see §3) |
| Process | No standardized stage-gates across the 10 departments; inconsistent scope/requirements definition at initiation; no change-control process | Delays concentrated at specific phase transitions, or in projects with significant mid-project scope changes |
| Resources/Dependencies | Contention for shared specialist resources (regulatory affairs, QA, biostatistics, clinical ops) across departments; no cross-project resource calendar | Delayed projects sharing common named resources/skillsets |
| Visibility/Information | No standardized status reporting; dependencies across departments invisible until they cause a block; delay discovered late | Long lag between when a delay-causing event occurs and when it is first visible in any report (a detection-lag metric) |
| Governance/Prioritization | No portfolio-level prioritization; each department optimizes locally for its own ~3 projects with no arbitration mechanism when they compete for the same scarce specialist | Informal de-prioritization of shared resources for other departments' projects; undocumented/conflicting priority calls |
| External/Regulatory | Regulatory review cycles (IRB, agency interactions); QA/quality-system reviews; CRO/vendor turnaround; clinical enrollment timelines | Delays clustering at specific external-dependency milestones (submission queues, IRB cycles, CRO turnaround) |

**Finding (the step itself, not a guess at the answer):** every one of the six discriminating observations above requires standardized cross-project data the organization does not currently have — because GT-1 (no PMO) means no entity currently collects it. This is itself the load-bearing result of the fishbone pass: **the organization cannot currently distinguish between any of these six hypotheses**, which is a structural fact about the organization's current information state, independent of which hypothesis eventually turns out to dominate.

```text
GT-1 (no PMO) + GT-2 (embedded PMs, no shared standard) + GT-8? (biotech shared-specialist/external-regulatory pattern)
→ none of the six candidate cause categories above currently have an available discriminating observation, because no standardized cross-project data exists to generate one
→ this absence of discriminating data is structural evidence that visibility infrastructure — not authority, and not headcount — is the first unmet capability gap, regardless of which specific cause eventually proves dominant
→ two of the six categories (External/Regulatory, and a pure specialist-capacity shortage within Resources/Dependencies) are, even if confirmed dominant, not addressed by better internal coordination — a PMO cannot shorten an agency review clock or manufacture specialist headcount it was not funded to hire [Assumes: A-13]
```

**Confidence: MEDIUM.** Downgrade cause: GT-8? — the biotech-general pattern is well documented in the field but unconfirmed for this specific organization; removed by the Phase 0 resource/dependency audit named in 4.4.

### 4.3 Inversion — what would guarantee a PMO fails to improve the delay rate, and what a PMO would NOT fix

Applying inversion to the premise "standing up a PMO will fix the 43% delay rate": the following conditions would each independently guarantee that premise is false, and each yields a necessary precondition for the premise to hold.

| Failure-guaranteeing condition | Necessary precondition it implies | Load-bearing? | Status |
|---|---|---|---|
| Delays are driven primarily by externally-controlled regulatory/CRO timelines | Delays must be at least partially attributable to internally-controllable factors (coordination, process, visibility) | load-bearing | unverified — resolved only by Phase 0 |
| Delays are driven by a true specialist-capacity shortage (not a coordination problem) | A PMO must not be asked to solve a capacity problem with a coordination tool; new headcount, not new process, is the fix if this holds | load-bearing | unverified — resolved only by Phase 0 |
| The 43% figure is a measurement artifact of inconsistent definitions, not real degradation | The delay definition must be standardized before any structure is sized against it | load-bearing | addressed directly by C1 / 4.4 Phase 0 |
| Department heads do not cede any real authority to a new function | A PMO's authority model must be calibrated to what department heads will actually accept, not asserted | load-bearing | unverified — addressed by the political-feasibility criterion in the trade-off (4.5) |
| Projects across the 10 departments are heterogeneous enough that one uniform process standard misfits most of them | Any standardized methodology must be tiered by project risk/type, not applied uniformly | load-bearing | addressed as a named plan change in section 4.10 |

**What a PMO would not fix, stated explicitly (direct answer to the user's point 2):**

- **Regulatory agency timelines** (FDA-type review clocks, IRB cycles) — a PMO can improve internal submission readiness and reduce *self-inflicted* regulatory delay, but cannot compress agency-controlled review time itself.
- **True specialist-capacity shortages** — if there are simply not enough regulatory affairs/QA/biostatistics FTEs for current demand, a PMO without new hires only relocates and makes visible the bottleneck; it does not resolve it (though the visibility it produces is exactly what would justify the hire to finance/leadership).
- **Deep technical/scientific uncertainty inherent to R&D** (an assay fails and needs rework) — inherent to the work itself, not a project-management structural issue.
- **Fundamental misalignment among department heads on strategic priorities** — a PMO can enforce and surface a prioritization decision once leadership makes one, and can supply the data that decision needs, but it cannot manufacture executive consensus; that remains a governance function above the PMO, not a PMO function.

### 4.4 Why diagnosis must precede any structural build (chains C2, C7)

```text
GT-5 (cause of delay currently undiagnosed) + GT-1 (no PMO, no standing resourcing decision today)
→ committing headcount and budget to any specific PMO structure against an undiagnosed cause spends real organizational capital (money, political capital with 10 department heads, PM trust) on a bet the organization cannot yet justify
→ the stakes-escalation rule therefore applies: a conclusion this consequential must rest on verified ground truth, not on the convention leadership already proposed (GT-6) or on an unexamined default ("build a PMO")
→ the responsible first move is a bounded, timeboxed diagnostic phase producing a root-cause distribution — not an immediate structural build [Assumes: A-14]
```

**Confidence: MEDIUM.** The Inputs axis is clean (HIGH), but the Rivals axis is short: a live rival — "skip diagnosis, build the full structure now, as leadership's informal proposal implicitly does" — exists and is not settled within this chain alone; it is ruled out by the political-feasibility and robustness-to-undiagnosed-cause scoring in the trade-off (4.5) and by the pre-mortem's cluster W5 (section 4.10), which price the cost of skipping diagnosis explicitly rather than assuming it away.

```text
GT-4? (headline delay figure, methodology unverified) + C2 (Phase 0 must precede Phase 1 build)
→ because the headline metric itself is not yet verified as comparable across departments, Phase 0 must also re-baseline the delay definition and capture root-cause-distribution and cost-of-delay baselines before Phase 1 begins — otherwise no later before/after comparison is falsifiable
→ the business-value measurement plan's baselines (section 6 of this document's user-facing deliverable) must therefore be captured as a named Phase 0 deliverable, not assembled after the fact [Assumes: A-15]
```

**Confidence: MEDIUM** (chain capped at the lowest-rated chain its head cites, C2 = MEDIUM).

### 4.5 Trade-off: which PMO type follows from the diagnosis? (chain C4)

Per the trade-off procedure: options are always compared against doing nothing, and against a composite, not only against the named conventional types.

**Must-have (knockout) applied before scoring:** any option must be capable of producing standardized, comparable cross-project data within ~90 days (this follows directly from 4.2's finding that visibility is the one unmet capability gap common to every hypothesis). **Status quo (continue as-is, no new structure) fails this must-have** — without a centrally accountable owner, a standardization mandate has no enforcement mechanism (shared responsibility behaves as no responsibility in practice) — and is knocked out rather than scored.

**Criteria and locked weights** (1–5, locked before scoring): Diagnostic capability (5), Coordination authority (3), Political feasibility (4), Cost/headcount (3), Speed to initial value (4), Robustness to the still-undiagnosed cause (5), Differentiation from leadership's rejected "more reporting" proposal (4). Total weight = 28.

**Anchored scores (1 = weak anchor, 5 = strong anchor; anchors stated in full in the companion engagement notes, abbreviated here for space):**

| Option | Diag (5) | Auth (3) | PolFeas (4) | Cost (3) | Speed (4) | Robust (5) | Trap-diff (4) | **Weighted total** |
|---|---|---|---|---|---|---|---|---|
| Supportive | 5 | 1 | 5 | 4 | 5 | 5 | 3 | **117** |
| Controlling | 5 | 4 | 3 | 3 | 3 | 4 | 5 | **110** |
| Directive | 5 | 5 | 1 | 2 | 1 | 2 | 5 | **84** |
| **Phased composite (Supportive → selective Controlling)** | 5 | 2 | 5 | 4 | 5 | 5 | 5 | **128** |

**Flip test:** the phased composite leads Supportive by 11 points, driven by the "Robustness" and "Trap-differentiation" criteria. Reducing either criterion's weight to its floor (1, since the scale is bounded 1–5) still leaves the composite ahead by a positive margin against every other option. **No single-criterion weight change within the valid 1–5 range reverses this ranking** — the result is robust to reasonable disagreement about priority weighting, not a near-tie dressed up as a finding.

```text
C2 (Phase 0 must precede build) + C3 (4.2's finding: visibility is the first unmet gap; authority value unproven for 2 of 6 candidate causes)
→ applying the weighted trade-off above, the phased Supportive-to-Controlling composite scores highest (128) and status quo is knocked out on the diagnostic-capability must-have [Assumes: A-16]
→ the flip test shows no single-criterion weight change reverses this ranking, so the result is robust rather than a borderline call
→ the correct initial PMO type is Supportive, with a pre-committed, evidence-gated evolution path toward selective Controlling-level authority, and Directive authority deferred indefinitely absent strong evidence plus explicit executive mandate
```

**Confidence: MEDIUM** (capped by both cited chains).

### 4.6 Reporting line and governance structure (chain C5)

```text
GT-3 (10 peer departments, no existing hierarchy among them) + C4 (Supportive PMO is the starting structure)
→ embedding the new PMO's reporting line under any one of the 10 departments creates a structural conflict-of-interest and credibility problem for the other nine peer departments, who would reasonably see the function as captured by a competitor department
→ the PMO must therefore report to an executive sponsor with no direct departmental P&L stake (e.g., the COO, or directly to the CEO), with a cross-functional Portfolio Governance Board — the 10 department heads plus the PMO Director plus the executive sponsor — serving as the prioritization-arbitration venue that GT-1/A-6 show is currently absent [Assumes: A-17]
→ this design gives the organization its missing prioritization venue without requiring the PMO itself to hold unilateral authority in Phase 1, which is exactly what keeps the structure Supportive rather than Controlling at this stage
```

**Confidence: MEDIUM** (capped by C4).

### 4.7 Staffing and build-vs-buy (chain C6) — Fermi-style bracket

```text
GT-3 (~30 projects / 10 departments) + GT-9? (industry-general PPM coordination-staffing and tooling pattern)
→ bracketing against typical supportive-PMO coordination ratios (~1 portfolio analyst per 15-20 actively tracked projects) yields roughly 2 analyst FTE for 30 projects, plus 1 PMO Director, plus a partial (0.5-1.0 FTE) process/methodology-standard role — a lower bound of 2 FTE (lean: Director + 1 analyst), a central estimate of 3-4 FTE, and an upper bound of 6 FTE pending what Phase 0 reveals about actual data-wrangling and department heterogeneity
→ standard PPM functions (status reporting, resource calendars, dependency tracking) are a mature, commodity SaaS category; building bespoke software is not justified for a 3-4 FTE team with no software-delivery capacity of its own, and buy already dominates on the cost/speed-to-value criteria established in the trade-off (4.5) [Assumes: A-18]
→ Phase 1 resourcing: ~3-4 FTE central PMO team, plus a lightweight/mid-market SaaS PPM tool (not a bespoke build, and not an enterprise-tier platform, which is deferred until Phase 2 needs — e.g., formal resource-capacity planning — exceed what the lightweight tool supports)
```

**Confidence: LOW.** Downgrade causes: (1) GT-9? — the staffing ratio is an industry-general pattern, not org-specific data; (2) the estimate itself carries a 3x bracket (2 to 6 FTE) reflecting genuine uncertainty about this organization's data-wrangling burden. Both are removed by Phase 0, which should re-derive the actual bracket from this organization's department count, system fragmentation, and confirmed root-cause distribution before Phase 1 headcount is finalized.

### 4.8 Second-order consequences of standing up the phased PMO (chain C8)

Walking both lenses required by the second-order procedure:

- **Actor lens.** Department heads (lose some autonomy; may under-resource data requests or route around the PMO for priority projects). PMs (gain a second reporting relationship on top of department loyalty; risk of role confusion and attrition among senior PMs who valued full embedded autonomy). PMO staff (new, unproven function; risk of overreaching into Controlling-level authority before Phase 2 data supports it, burning political capital early). Executive sponsor (bears the political cost of defending a new overhead line against results that take two or more quarters to materialize).
- **Time lens.** Immediately: a genuine, bounded productivity dip as PMs and department staff respond to new data requests and a new reporting cadence — a real short-term cost, not merely a perception risk, and should be budgeted and disclosed rather than hidden. After a few cycles: department heads who see Phase 0 findings point at their own department specifically may disengage if the framing reads as audit rather than diagnosis. Once established (a year or more): risk of PMO scope creep and bureaucratic entrenchment — the organizational-inertia mirror image of the under-investment problem this engagement starts from.

```text
C4 (phased Supportive-to-Controlling structure) + C5 (governance-board reporting line)
→ the actor-lens and time-lens walk above surfaces five concrete structural-weakness clusters (detailed in full in section 4.10's pre-mortem): evidence-to-authority follow-through failure; process-fit mismatch; stakeholder trust/inclusion failure; unproven-ROI/patience mismatch; and the diagnostic phase's own opportunity cost
→ none of these five clusters contradicts a named ground truth, so the conclusion is not returned to Phase 2 — each instead converts into a named plan change or an explicitly accepted, mitigated risk, folded directly into the roadmap below rather than left as a generic risk list
→ the roadmap this analysis recommends is therefore the derivation above (C2 through C6) plus these five named mitigations — which is what distinguishes it from a plan that looks identical on paper but fails for the specific reasons the pre-mortem names
```

**Confidence: MEDIUM** (capped by both cited chains).

### 4.9 The phased roadmap itself, assembled from the chains above

**Phase 0 — Diagnose (weeks 0–6, hard timeboxed).** Standardize the definition of "delay" and re-baseline the 43% figure against it (chain C1); pull existing status/resource/dependency data for all ~30 projects; run structured interviews with all 10 department heads and a PM sample to collect the discriminating observations the fishbone pass (4.2) shows are currently missing; build the Finance-partnered cost-of-delay valuation model named in section 6; produce a root-cause distribution across the six fishbone categories. *Why first:* chain C2 — the stakes-escalation rule means no structural commitment (headcount, authority, reporting-line change) can be sized responsibly before this data exists, and the diagnostic itself is cheap (weeks, not months) relative to the cost of guessing wrong.

**Phase 1 — Stand up the Supportive PMO / visibility layer (weeks 6–14).** Hire/assign the PMO Director plus 1–2 Portfolio Analysts (chain C6); deploy the lightweight SaaS PPM tool; establish one standardized status-reporting cadence and one shared delay definition across all 10 departments; stand up the Portfolio Governance Board (chain C5) as the venue for resource-conflict visibility and voluntary negotiation — not yet resolution authority. *Why visibility before control, derived rather than asserted:* chain C4's trade-off shows Authority scores low on political feasibility absent evidence, and chain C2/4.3's inversion shows that asking department heads to cede resource-reallocation authority before the data exists to justify it invites exactly the resistance the political-feasibility criterion penalizes; visibility-first is also the structural feature that differentiates this plan from leadership's rejected "more reporting" proposal (4.5's Trap-differentiation criterion) — this reporting has a named owner, a shared standard, and feeds a governance decision loop, rather than producing dashboards nobody is accountable for acting on.

**Phase 2 — Selective Controlling-level authority (months 4–9, contingent on confirmed Phase 0/1 data).** Grant authority only where the confirmed root-cause distribution supports it: if resource contention is confirmed dominant, give the Governance Board real arbitration rights over shared specialist allocation; if stage-gate/process variance is confirmed dominant, mandate a standard methodology with PMO sign-off at phase transitions, tiered by project risk (4.3's heterogeneity precondition) rather than applied uniformly. If External/Regulatory or pure specialist-capacity shortage is confirmed dominant instead, the correct action is to redirect investment toward regulatory capacity or external-dependency management rather than expanding PMO authority — and this document states that as a legitimate possible Phase 0 outcome rather than hiding it.

**Phase 3 — Reassess Directive-level need (month 9–12+).** Only after Phase 2 operating data exists is full Directive authority (PMs reporting into the PMO) revisited; it is explicitly not committed to in this roadmap, consistent with chain C4's trade-off scoring.

### 4.10 Pre-mortem: how this initiative fails (structured, stakeholder-generated)

**Premise (past tense, as the technique requires):** it is 18 months from now, and the PMO initiative has failed — quietly dismantled or starved of support.

**Causes, generated from three stakeholder viewpoints, unfiltered before clustering:**

*Department heads:* the PMO became another layer of approval without producing usable improvement, read as bureaucracy; the standardized process was a poor fit for a genuinely different project type (e.g., a manufacturing-scale-up project forced through a clinical-ops stage-gate template), causing justified friction; department heads were never genuinely included in Phase 0, felt the data was used to assign blame rather than diagnose, and disengaged.

*PMs:* felt caught between department loyalty and PMO standard compliance with no clarity on who evaluates them, and the best PMs left; the reporting burden increased in Phase 1 but the promised Phase 2 authority/decision-making benefit never actually arrived once it became politically inconvenient, leaving extra reporting work with no structural payoff.

*Executive sponsor:* results took two-plus quarters to show (as the metrics design predicts) and leadership patience ran out first, especially if a budget-cutting cycle hit mid-rollout; the cost-of-delay valuation model was never actually built or was not credible, so the PMO could never state its ROI in terms Finance trusted, making it an easy target; Phase 0 was skipped under time pressure, reverting straight to "stand up a PMO" as leadership's original informal proposal — defeating the entire premise of this engagement.

*Adversarial/competitive lens:* while the organization spends six weeks on Phase 0 diagnosis, a less-diagnosed but faster competitor reorg captures a real market or regulatory-timing advantage — the "diagnose first" approach carries a genuine opportunity cost, not a free one, and this analysis should not pretend otherwise.

**Clusters, each naming the chain(s) it bears on, each with a named disposition:**

| Cluster | Bears on | Disposition |
|---|---|---|
| **W1 — Evidence-to-authority follow-through failure** (Phase 2 authority never materializes after Phase 1 data collection) | C4 (robustness), roadmap 4.9 | **Plan change:** calendar the Phase 2 authority-expansion decision date at Phase 1 kickoff, owned by the executive sponsor, as a standing Governance Board agenda item — not an open-ended "someday." |
| **W2 — Process-fit mismatch** (uniform methodology applied to heterogeneous project types) | 4.3's heterogeneity precondition | **Plan change:** tier the standardized methodology by project risk/type from the start (a light template for low-risk/low-regulatory projects, a full template for high-regulatory/high-complexity ones) rather than one uniform standard. |
| **W3 — Stakeholder trust/inclusion failure** (data-as-blame dynamic, department-head disengagement) | C5 (political feasibility) | **Plan change:** frame and communicate Phase 0 explicitly as "diagnosing the system, not auditing departments"; include department heads as active Governance Board participants, not just data sources, from day one; the exec sponsor personally communicates this framing before data collection begins. |
| **W4 — Unproven ROI / patience mismatch** (cost-of-delay model never built or not credible; leadership patience shorter than the falsification window) | section 6 measurement plan | **Plan change:** make the Finance-partnered cost-of-delay valuation model a named, resourced Phase 0 deliverable, not an afterthought. |
| **W5 — Own-process opportunity cost** (the diagnostic phase itself delays action in a time-sensitive environment) | roadmap 4.9, Phase 0 | **Accepted risk, named mitigation:** accept the ~6-week diagnostic delay as a real cost, mitigated by a hard timebox (6 weeks, not open-ended) and by triaging any project already in a regulatory-critical window for expedited, manual attention in parallel with Phase 0 rather than waiting for the general rollout. |

**Falsification condition for the overall recommendation:** this recommendation (a phased Supportive-to-Controlling PMO gated by a Phase 0 diagnostic) is wrong if, after Phase 0, root causes turn out to be overwhelmingly external/regulatory or a pure specialist-capacity shortage rather than internal coordination, process, or visibility factors. In that case the correct action is to redirect the Phase 1 budget toward regulatory-capacity hiring or external-dependency management instead of PMO infrastructure — and Phase 0 is explicitly designed to surface that outcome, not obscure it.

### 4.11 Business-value measurement plan (falsifiable, baselined in Phase 0)

| Metric | Baseline capture point | What confirms the investment is working | What disconfirms it |
|---|---|---|---|
| Standardized delay rate (re-baselined definition) | Phase 0 | Statistically meaningful downward trend within 2 quarters of Phase 1 going live | Flat or worsening despite 2+ quarters of operation |
| Root-cause distribution across the 6 fishbone categories | Phase 0, re-measured each phase gate | Share attributable to internally-controllable causes (process/visibility/resource contention) shrinks over time | Share attributable to internal causes is flat while external/capacity share grows — signals a pivot is needed per 4.10's falsification condition |
| Cost of delay avoided ($, via the Phase 0 Finance-partnered model) | Phase 0 (model build), tracked quarterly thereafter | Modeled $ avoided exceeds PMO operating cost within a stated payback window | PMO cost exceeds modeled value avoided with no narrowing trend |
| Resource-utilization variance across shared specialist pools | Phase 0 (if resource contention is confirmed a cause) | Variance decreases once Phase 2 arbitration is live | No change despite arbitration authority being granted |
| Time-to-detect (lag between a delay-causing event and its first appearance in reporting) | Phase 0 | Sharp decrease once Phase 1 visibility infrastructure is live — the fastest-moving, earliest leading indicator | No improvement despite standardized reporting being in place |
| Department-head / PM sentiment and perceived autonomy (survey) | Phase 0 | No severe degradation — tracks the political-feasibility and autonomy-loss risk named in 4.8/4.10 | Sharp drop — an early warning the political-feasibility assumption (A-11) is being violated in practice |

This table is the operational form of chain C7: none of these comparisons is falsifiable unless every baseline is captured in Phase 0, before Phase 1 begins.

## 5. Abandoned Reasoning

**What was tried:** Score a Directive PMO (full centralized reporting of all PMs) as the default recommendation, on the reasoning that centralizing authority most directly attacks GT-1's clearest derived consequence (no central prioritization mechanism exists).

**Why abandoned:** The weighted trade-off (4.5, chain C4) shows Directive scores lowest of all four scored options on political feasibility (1/5) and robustness to the still-undiagnosed cause (2/5); the inversion analysis (4.3) shows a necessary precondition for any PMO authority model — confirmed internal-coordination root cause plus department-head buy-in — is unverified at this stage, and committing to Directive without it directly violates the stakes-escalation rule from the Assumptions Table.

**What it ruled out:** "Go straight to full reorganization" as the Phase 1 recommendation. Redirected reasoning toward the phased, evidence-gated authority model in chain C4.

**What was tried:** Use the 43% delay figure directly as an input to the fishbone discriminating-observation step — e.g., "delays cluster in department X, therefore department X is the dominant cause."

**Why abandoned:** GT-4? flags the figure's own measurement methodology as undisclosed and possibly inconsistent across departments (chain C1); using an unverified, possibly non-comparable metric to localize a cause risks diagnosing a measurement artifact rather than a real pattern.

**What it ruled out:** Skipping measurement standardization and reasoning straight from 43% to a root-cause conclusion. Redirected to chains C1/C7's "re-baseline before diagnosing" sequencing, which is why Phase 0 explicitly includes re-baselining the delay definition before building the root-cause distribution.

**What was tried:** Apply a hard knockout rule to Directive PMO at the must-have stage ("no confirmed executive mandate for directive authority exists, therefore Directive is ineligible").

**Why abandoned:** No actual data exists in this engagement on executive appetite for ceding departmental authority (A-11) — asserting a knockout in either direction without evidence would itself be exactly the kind of unverified-assumption move this engagement exists to avoid.

**What it ruled out:** Using a hard knockout for Directive PMO. Redirected to scoring it through the full weighted trade-off instead (4.5), where it still loses decisively on the merits rather than being excluded by assertion — a stronger and more defensible result than a knockout would have been.

## 6. Conclusion

**Recommended approach:** Run a hard-timeboxed 6-week Phase 0 diagnostic — re-baseline the delay definition, build a root-cause distribution across the six fishbone categories, and build a Finance-partnered cost-of-delay model — before building any new structure (chains C2, C7). Then stand up a lean Supportive PMO (~3–4 FTE: a Director, 1–2 Portfolio Analysts, a partial process-lead role) reporting to a C-level sponsor with no departmental P&L stake (e.g., COO), through a cross-functional Portfolio Governance Board seating all 10 department heads (chains C4, C5, C6), using a lightweight/mid-market SaaS PPM tool rather than a bespoke build or enterprise platform (chain C6). Pre-commit, at Phase 1 kickoff, to an evidence-gated evolution path toward selective Controlling-level authority — granted only where Phase 0/1 data confirm internal coordination (not external/regulatory timelines or pure specialist-capacity shortage) is the dominant cause — with Directive-level authority deferred indefinitely absent strong evidence and an explicit executive mandate (chain C4).

**Key insight:** The organization cannot currently distinguish between any of the six plausible delay-cause categories — including two (external/regulatory timelines, specialist-capacity shortage) that no PMO can fix regardless of its design — because it has no standardized cross-project data to generate a discriminating observation for any of them (chain C3). This is what makes visibility infrastructure, not authority or headcount, the one investment that is correct regardless of which cause eventually proves dominant: the sequencing recommendation does not rest on a guess about which cause is real, it rests on the fact that the organization cannot yet tell.

**Trade-offs acknowledged:** This approach accepts a real ~6-week delay before any structural fix begins, a genuine near-term reporting-burden cost on PMs and department staff during Phase 1, and the risk that Phase 2 authority expansion never follows through on the Phase 1 data once it becomes politically inconvenient. The pre-mortem (4.10) names five specific structural-failure clusters and converts each into either a named plan change (calendared Phase 2 decision date, risk-tiered methodology, governance-board inclusion from day one, a funded cost-of-delay model) or an explicitly accepted, mitigated risk (the diagnostic phase's own opportunity cost, mitigated by a hard timebox and parallel expediting of regulatory-critical projects) (chain C8).

**Confidence: LOW overall, by the chain-capping rule — but this single band hides a real split that leadership should read separately.** The *structural sequencing logic* — diagnose before building (C2), visibility before authority (C3), the phased Supportive-to-Controlling type and its governance-board reporting line (C4, C5) — is MEDIUM confidence: well-supported by the stipulated ground truths and a trade-off result that survives the flip test, but still resting on two unverified industry-general patterns (GT-8?, GT-9?) this engagement had no data to confirm. The *specific headcount bracket* (chain C6: 2–6 FTE, central estimate 3–4) is LOW confidence — an industry-pattern estimate with a 3x bracket, explicitly flagged for correction once Phase 0 produces this organization's own data. Reporting a single LOW band rather than quietly rounding up to MEDIUM is the honest reading: the one number in this recommendation genuinely least supported by evidence (the headcount bracket) is also the one number leadership is most likely to fixate on, and it is the one this document most explicitly flags as provisional. Would change the structural-logic band to HIGH: org-specific confirmation of GT-8/GT-9 via the Phase 0 diagnostic itself. Would change the headcount band to MEDIUM or HIGH: Phase 0's actual root-cause distribution and data-wrangling burden, replacing the industry-pattern bracket with this organization's own figures.
