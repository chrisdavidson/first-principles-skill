<!-- GENERATED — DO NOT EDIT. Source: shared/examples/composed-inversion-second-order.md. Regenerate via: scripts/sync-content.py --write. -->

# Worked Example: Composed Inversion + Second-Order Thinking

A complete first-principles analysis demonstrating how **inversion** (Phase 11 negative-direction
tool) and **second-order thinking** (Phase 12 positive-direction tool) compose — not duplicate —
on a single software-systems claim. Inversion populates the Assumptions Table with the
preconditions the claim silently depends on; second-order extends the Derivation Chain with
the consequences of the first-order conclusion. The two tools attack opposite directions of
the same conclusion and meet in the middle.

**Claim under analysis.** "Adding a Redis read-through cache in front of our Postgres-backed
product-listings API will cut p95 latency and reduce database load enough to defer the
otherwise-scheduled Postgres vertical-scale upgrade for at least two quarters."

**One-sentence composition summary.** Inversion forces the negative-direction question
("what must hold for the cache to not pay back?") and populates untested-belief rows about
hit rate, key cardinality, and invalidation; second-order forces the positive-direction
question ("if the cache pays back, what follows downstream?") and surfaces a stale-read
consequence that revises the first-order conclusion from "defer the upgrade" to "defer the
upgrade conditional on a documented staleness budget."

---

## 1. Problem Essence

**The claim.** "Adding a Redis read-through cache in front of our Postgres-backed
product-listings API will cut p95 latency and reduce database load enough to defer the
otherwise-scheduled Postgres vertical-scale upgrade for at least two quarters."

**Who is asserting it.** The platform team lead, in an architecture-review document
circulated ahead of the quarterly capacity-planning meeting. The document cites peak
read-QPS on the listings endpoint and the next-tier Postgres instance cost.

**What decision hinges on it.** Whether to (a) approve a two-engineer-week effort to ship
the Redis cache and cancel the vertical-scale upgrade work for this and the next quarter, or
(b) execute the scheduled upgrade now and revisit caching later as an independent
optimisation. The decision is reversible at the cache-rollout boundary but the scheduled
upgrade has a procurement lead time that makes a late reversal expensive.

**Why the analysis needs both tools.** The surface claim is plausible enough that a
fast-thinker would accept it — Redis in front of Postgres is a textbook pattern. Inversion
surfaces the silent preconditions that a textbook pattern hides (read pattern shape, cache
hit rate, key cardinality, invalidation correctness); second-order surfaces the downstream
consequences that the first-order "defer the upgrade" conclusion sets in motion (stale-read
exposure, on-call surface area). Either tool alone reaches a partial answer.

---

## Inversion Pass (Phase 2 hand-back)

Running the procedure documented in `references/inversion.md` against the surface claim, in
its negative-direction form, to surface preconditions that enter the Classified Assumptions
Table as `untested belief` rows.

**Step 1 — state the claim precisely.** "The Redis cache will cut p95 latency and reduce
database load enough to defer the upgrade for at least two quarters."

**Step 2 — invert it.** "The Redis cache will not cut p95 latency enough, or will not reduce
database load enough, to defer the upgrade for at least two quarters."

**Step 3 — enumerate failure-guaranteeing conditions.**

- Cache hit rate is below the level needed for the read-QPS reduction to push Postgres back
  below the upgrade threshold (the long-tail of listing keys is too cold for the cache to be
  warm on most requests).
- Cached payload size is large enough that Redis memory pressure forces eviction before keys
  see a second hit, collapsing effective hit rate.
- Invalidation correctness on listing updates is hard enough that the team ships a
  conservative TTL-only invalidation, which either serves stale data (failure mode visible
  to customers) or sets TTL so short that hit rate is suppressed.
- A non-trivial fraction of listing reads are personalised (per-user pricing, per-user
  availability) and therefore not cacheable at the listing-id key alone.
- The next-tier Postgres upgrade is being driven by write-side or storage-size limits, not
  read-side QPS, in which case a read-side cache does not relieve the binding constraint.

**Step 4 — derive necessary preconditions.** For each failure-guaranteeing condition, the
precondition whose absence would cause it:

- Hit rate at steady state is high enough that read-QPS reduction crosses the upgrade
  threshold (a specific numeric threshold the platform team can name).
- The working-set fits in the Redis memory budget at the cached-payload size — eviction is
  not the binding constraint.
- A correct, low-latency invalidation path exists from listing-write to cache-invalidate
  with a known maximum staleness window.
- Listing reads are predominantly the non-personalised shape, or the cache key includes the
  personalisation axis without exploding key cardinality.
- The Postgres upgrade is being driven by the read side and not by writes, WAL, or storage.

**Step 5 — check each precondition's status.** Four of the five preconditions are not
verified against measurement data and are `untested belief` on entry to Phase 2. The fifth —
the upgrade being driven by the read side — is already confirmed by GT-2 (the capacity-planning
document's upgrade-justification section, checked against the monitoring dashboard), so it
enters as a `current constraint` accepted on that ground truth.

**Step 6 — record as rows.** The Classified Assumptions Table below carries each precondition
as a row attributed to the inversion pass: the four open ones as `untested belief`, the
confirmed one as an Accept resting on GT-2.

---

## 2. Assumptions Table

Each row carries a Type drawn from the spine's four types (`physical law` / `current
constraint` / `convention` / `untested belief`). The Treatment cell attributes each row to either
the claim's surface text (`direct`) or the negative-direction procedure above (`inversion
pass`); the Verification cell records what is confirmed, or flags the row `unverified — flagged`
with the step that would lift it.

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| The listings endpoint is the dominant contributor to Postgres read-QPS at peak | current constraint | Direct. Verify against the existing query-log sample. | Accept — confirmed against the Q3 query-log sample; the listings endpoint is the highest read-QPS contributor at peak | Confirmed by GT-1 (Q3 query-log analysis). |
| Redis-in-front-of-Postgres is a viable read-through pattern at our scale | convention | Direct. Explicitly challenge — convention is correct in general but says nothing about whether our specific read shape benefits. | Challenge — pattern viability is not pattern fit | unverified — flagged; pattern fit for this read shape is what the inversion-pass rows below test |
| Cache hit rate at steady state is high enough to cross the read-QPS upgrade-threshold | untested belief | Inversion pass. Verify — run a shadow-read simulation against a recorded production trace, measure simulated hit rate, compare against the named QPS threshold. | Challenge — unverified; requires the scoped shadow-read simulation before this precondition can be accepted | unverified — flagged; the shadow-read simulation is scoped but not run (GT-5?) |
| The cached working set fits in the Redis memory budget at the cached-payload size | untested belief | Inversion pass. Verify — measure unique listing-keys seen per hour and multiply by mean cached payload size; compare against the proposed Redis instance memory. | Challenge — unverified; requires the working-set-size measurement against the proposed instance memory | unverified — flagged; the working-set-size measurement has not been run |
| A correct invalidation path exists from listing-write to cache-invalidate with a known maximum staleness window | untested belief | Inversion pass. Verify — name the invalidation mechanism (event-bus, write-through wrapper, or TTL-only) and the staleness window it guarantees. | Challenge — unverified; requires naming the invalidation mechanism and confirming its staleness window | unverified — flagged; no mechanism or staleness window is named yet (GT-4 shows event-driven invalidation is feasible, not chosen) |
| Listing reads are predominantly non-personalised at the key-cardinality level | untested belief | Inversion pass. Verify — segment the recorded trace by request shape; compute the share of reads that are cacheable at the listing-id key alone. | Challenge — unverified; requires the request-shape segmentation of the recorded trace | unverified — flagged; the request-shape segmentation has not been run |
| The scheduled Postgres upgrade is driven by read-side QPS and not by writes, WAL, or storage | current constraint | Inversion pass. Verify — read the upgrade-justification document and confirm the binding constraint is read-side. | Accept — confirmed by GT-2; the upgrade-justification section, checked against the CPU, write-IOPS and storage dashboard, shows the binding constraint is read-side CPU saturation | Confirmed by GT-2 (capacity-planning document's upgrade-justification section, verified against the monitoring dashboard). |
| A two-engineer-week cache rollout is the lowest-cost intervention to defer the upgrade | convention | Direct. Explicitly challenge — challenge the framing that "defer the upgrade" is the right outcome to optimise for if the upgrade addresses a different constraint. | Challenge — outcome-framing; the upgrade-driver row above is now confirmed read-side, so the open question is whether the cache is the lowest-cost route, not whether it addresses the right constraint | unverified — flagged; no cost comparison against the upgrade has been made, and the two-week estimate (GT-3) covers TTL invalidation only |

The inversion pass contributes five rows. Four are of type `untested belief`, attributed in the
Treatment column to `inversion pass`; the fifth (the upgrade-driver precondition) is a
`current constraint` that GT-2 confirms. Each open row carries a specific Treatment naming the
verification step that would lift it.

---

## 3. Ground Truths

Verified facts available at the point of analysis. Stable GT-IDs; `GT-N?` marks an
unverified-but-load-bearing entry per the spine's Phase 3 discipline.

- **GT-1** The listings endpoint accounts for the largest share of Postgres read-QPS at
  peak in the Q3 query-log sample — source: the platform team's Q3 query-log analysis,
  reviewed in the architecture-review document.

- **GT-2** The scheduled Postgres vertical-scale upgrade is driven by the binding
  constraint of peak read-QPS approaching the current instance's CPU saturation point,
  not by write throughput, WAL retention, or storage size — source: the capacity-planning
  document's upgrade-justification section, verified against the most recent monitoring
  dashboard for CPU, write IOPS, and storage utilisation.

- **GT-3** A two-engineer-week effort delivers a working Redis read-through cache in
  front of the listings endpoint, with TTL-based invalidation as the baseline mechanism
  — source: the platform team's implementation-estimate document, supported by a prior
  comparable Redis rollout in front of the catalog-search endpoint.

- **GT-4** Listings update events are emitted on the existing internal event bus on every
  catalog write — source: the catalog service's published event schema, verified by
  inspecting the event-bus consumer registry.

- **GT-5?** A shadow-read simulation against a one-hour recorded production trace shows
  a steady-state hit rate above the named QPS-reduction threshold needed to defer the
  upgrade — source: unverified; the shadow-read simulation has been scoped but not run;
  this entry is load-bearing for the first-order conclusion and is the highest-priority
  verification step.

```text
?-marked: GT-5? (1 of 5)
Read-at-source: GT-1 — the platform team's Q3 query-log analysis, reviewed in the architecture-review document
Read-at-source: GT-2 — the capacity-planning document's upgrade-justification section, verified against the most recent monitoring dashboard for CPU, write IOPS and storage utilisation
```

---

## 4. Derivation Chains

### Conclusion C1: The Redis cache plausibly defers the upgrade if and only if `GT-5?` resolves to a measured hit rate above the named threshold

GT-1 (listings endpoint is the dominant Postgres read-QPS contributor at peak) + GT-2 (upgrade is driven by read-QPS, not writes, WAL, or storage) + GT-5? (steady-state hit rate above the named threshold — load-bearing, unverified)
→ A read-side cache placed in front of the dominant read contributor reduces the read-QPS the binding-constraint resource sees, because the upgrade's binding constraint is read-QPS on the same resource — the same axis the upgrade was scheduled to relieve
→ The defer-the-upgrade outcome therefore depends on whether the cache's steady-state hit rate is large enough to cross the named QPS-reduction threshold — exactly the unverified load-bearing input GT-5? names.

**Pre-check:** head GT-1, GT-2, GT-5? · ?-marked: GT-5? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the chain consumes GT-5? as a load-bearing input. Raising to HIGH
requires running the scoped shadow-read simulation against the recorded production trace and
confirming the measured steady-state hit rate clears the named threshold.

---

## Second-Order Extension (Phase 4 continuation)

Running the procedure documented in `references/second-order-thinking.md` against the
first-order conclusion above, before Phase 5, to extend the Derivation Chain with the
downstream effects of acting on it.

**Step 1 — state the first-order conclusion precisely.** "The Redis cache defers the upgrade
if and only if `GT-5?` resolves to a measured hit rate above the named threshold."

**Step 2 — enumerate 2nd-order consequences.**

- **2nd-order: stale-read exposure.** Deferring the upgrade locks in the cache as a
  load-bearing component for at least two quarters. TTL-only invalidation (the baseline
  per GT-3) means listing reads served from cache lag listing writes by up to the TTL
  window — a staleness budget that did not exist on the direct-Postgres path.
- **2nd-order: on-call surface area grows.** A Redis instance, a cache-population path, and
  a cache-invalidation path are added to the on-call rotation's responsibilities. Listing
  incidents now require correlating cache state with database state at the time of failure.
- **2nd-order: invalidation correctness becomes load-bearing.** GT-4 confirms listings
  update events are emitted on the existing event bus, which makes event-driven
  invalidation feasible — but only if the cache subscribes to those events and applies
  invalidations correctly. If it does not, the staleness budget is the TTL.

**Step 3 — enumerate 3rd-order consequences.**

- **3rd-order: customer-visible staleness incidents become possible.** If a listing price
  or availability changes and a customer reads the cached pre-change value within the TTL,
  the customer sees a stale listing — a customer-facing failure mode that did not exist
  pre-cache.
- **3rd-order: the staleness budget becomes a product-level contract.** Whatever staleness
  window the cache permits silently becomes a contract with downstream systems (search
  indexing, recommendation pipelines, analytics) that previously read live data.
- **3rd-order: on-call runbooks must be rewritten.** Incident response now branches on
  "is this a cache problem or a database problem?" — the rotation must learn the new
  branch before it can respond within SLO.

**Step 4 — apply the stopping rule.** Stop at the 3rd order. Further layers (e.g., the
analytics-pipeline contract implications of step 3.2) become non-actionable in the
two-quarter decision window.

**Step 5 — check for undermining contradictions.** The 2nd-order "stale-read exposure" and
the 3rd-order "customer-visible staleness incidents become possible" introduce a customer-
facing failure mode that the surface claim did not name. This does not contradict any
Ground Truth — GT-1 through GT-4 do not assert anything about staleness — but it
contradicts the *unstated* premise that the cache is an internal optimisation invisible
to customers. The first-order conclusion is therefore incomplete: deferring the upgrade is
the wrong outcome to commit to without a documented staleness budget.

**Step 6 — route the result.** The non-contradicting consequences (on-call surface area,
runbook rewrites) extend the Derivation Chain as recorded follow-on work. The
undermining-of-an-unstated-premise effect routes the conclusion through a revision rather
than back to Phase 2 — the conclusion stands, conditional on a new acceptance criterion.

---

## 5. Abandoned Reasoning

### Dead End: Skip inversion and accept the surface claim because Redis-in-front-of-Postgres is a textbook pattern

**What was tried.** The first instinct on reading the architecture-review document was to
accept the claim on convention grounds — Redis read-through caching is a textbook pattern
with abundant prior art — and recommend approval of the two-engineer-week effort directly.

**Why abandoned.** Convention says the pattern is viable at scale; it does not say the
pattern fits this specific read shape. Without the inversion pass, the four open `untested
belief` rows would not have entered the Assumptions Table, GT-5? would not have been
identified as the load-bearing unverified input, and the first-order conclusion would not
have been gated on a measurable hit-rate threshold. Convention is not pattern fit.

**What it ruled out.** Convention-grounded approval of a cache rollout is insufficient
evidence for an upgrade-deferral decision when the upgrade-deferral outcome is the actual
question. Any future "we should add a cache" architecture proposal must pass the inversion
pass before the deferral question is even on the table.

---

## 6. Conclusion

**The second-order pass revised the first-order conclusion.** The first-order conclusion
("defer the upgrade if and only if GT-5? resolves above the threshold") is necessary but
not sufficient. Second-order surfaced a customer-facing staleness consequence that did not
appear in the original claim and that the first-order chain did not name. The revised
conclusion adds a documented staleness budget as a second acceptance criterion.

**Recommended approach:** Approve the cache rollout (chain C1) conditional
on (a) running the scoped shadow-read simulation to resolve GT-5? and confirming the
measured steady-state hit rate clears the named threshold, and (b) committing to
event-driven invalidation against the existing event bus (GT-4) with a documented staleness
budget — not TTL-only — before the cache is taken as load-bearing for the upgrade-deferral
decision. GT-3's two-engineer-week estimate covers a cache with TTL-based invalidation; the
event-bus subscription and invalidation work in (b) lies outside it, so the approval
carries a revised estimate that includes that work as a further condition. Keep the
upgrade's procurement live until both acceptance criteria are met, with a decision date
set before procurement's last cancellable point. If either acceptance criterion fails,
execute the scheduled Postgres upgrade as originally planned.

**Pre-check:** head C1 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — matches the weakest link, chain C1, which consumes GT-5? as a
load-bearing input. Raising to HIGH requires GT-5? resolved and the staleness-budget
acceptance criterion documented and signed off by the team owning downstream consumers.

---

## Appendix — process output

## Self-Audit Gate (process output)

*Scored against `references/validation-rubric.md`. Six criteria evaluated in order.*

**Criterion 1: Identify Essence**
Band: **Rigorous**
> the Redis cache and cancel the vertical-scale upgrade work for this and the next quarter, or

Justification: The Problem Statement names the specific decision under analysis, not the
triggering event or a restatement of the architecture-review document; the decision frame is
specific to this team's two-quarter capacity-planning window and could not be copied to a
different analysis without alteration.

---

**Criterion 2: Challenge Assumptions**
Band: **Rigorous**
> The inversion pass contributes five rows. Four are of type `untested belief`, attributed in the

Justification: Every row in the Classified Assumptions Table carries a Type, a specific
Treatment (attributing the row to the claim or the inversion pass), a Verdict and a
Verification cell; every open row used as a load-bearing precondition is marked
`unverified — flagged` in its Verification cell; the inversion-attributed rows carry the
verification step that would lift each one, and the one confirmed by GT-2 says so.

---

**Criterion 3: Establish Ground Truths**
Band: **Sound**
> **Confidence:** MEDIUM — the chain consumes GT-5? as a load-bearing input. Raising to HIGH

Justification: GT-1 and GT-2 are unsuffixed and their sources are reachable (no Phase 3
failure record marks either unreachable), but both feed only the single first-order chain,
which is rated MEDIUM — neither feeds a HIGH-confidence chain, which the tightened Rigorous
descriptor requires absent an unreachable-source exception; no such exception applies here.

---

**Criterion 4: Reason Upward**
Band: **Rigorous**
> A read-side cache placed in front of the dominant read contributor reduces the read-QPS

Justification: The first-order chain names the inputs it consumes — here, ground truths — in
the prescribed head form, contains an intermediate claim statable from the combination but not
from any single named input alone, and reaches a conclusion; the Abandoned Reasoning section
documents a substantive dead end with a specific structural abandonment reason; no analogy is
used as direct evidence.

---

**Criterion 5: Validate**
Band: **Rigorous**
> MEDIUM — the chain consumes GT-5? as a load-bearing input. Raising to HIGH

Justification: The derivation chain's weakest link is named (GT-5?); the chain's confidence
rating matches the unverified-input rule; the overall Conclusion section's confidence
rating matches the weakest chain; the specific verification that would raise confidence to
HIGH is named. The same GT-5?-driven MEDIUM chain is named by Criterion 3 and banded there;
it is noted here without independently lowering this criterion's band, per the rubric's
precedence rule.

---

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Band: **Rigorous**
> The second-order pass revised the first-order conclusion.

Justification: Every claim in the Conclusion section traces to a chain or a named
consequence in the Second-Order Extension section; the Key Insight that the second-order
pass revised the first-order conclusion names a non-obvious finding that convention-
grounded approval would have missed; no new reasoning is introduced in the Conclusion
section that did not appear earlier.

---

**Overall verdict: PASS**

No criterion is at Hand-wavy or Absent. Gate cleared; hand-wavy cap cleared.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": null,
  "assumptions": [
    {
      "id": "A-1",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-2",
      "type": "convention",
      "verdict": "Challenge"
    },
    {
      "id": "A-3",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-4",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-5",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-6",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-7",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-8",
      "type": "convention",
      "verdict": "Challenge"
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": true
    },
    {
      "id": "GT-2",
      "read_at_source": true
    },
    {
      "id": "GT-3",
      "read_at_source": true
    },
    {
      "id": "GT-4",
      "read_at_source": true
    },
    {
      "id": "GT-5",
      "read_at_source": false
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-1",
        "GT-2",
        "GT-5?"
      ]
    }
  ],
  "dead_ends": [
    "Skip inversion and accept the surface claim because Redis-in-front-of-Postgres is a textbook pattern"
  ],
  "techniques": null,
  "gate": {
    "passes": [
      {
        "bands": [
          "Rigorous",
          "Rigorous",
          "Sound",
          "Rigorous",
          "Rigorous",
          "Rigorous"
        ],
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
    "recommendation": "Approve the cache rollout (chain C1) conditional\non (a) running the scoped shadow-read simulation to resolve GT-5? and confirming the\nmeasured steady-state hit rate clears the named threshold, and (b) committing to\nevent-driven invalidation against the existing event bus (GT-4) with a documented staleness\nbudget — not TTL-only — before the cache is taken as load-bearing for the upgrade-deferral\ndecision. GT-3's two-engineer-week estimate covers a cache with TTL-based invalidation; the\nevent-bus subscription and invalidation work in (b) lies outside it, so the approval\ncarries a revised estimate that includes that work as a further condition. Keep the\nupgrade's procurement live until both acceptance criteria are met, with a decision date\nset before procurement's last cancellable point. If either acceptance criterion fails,\nexecute the scheduled Postgres upgrade as originally planned.",
    "confidence": "MEDIUM",
    "rests_on": [
      "C1"
    ]
  }
}
```
