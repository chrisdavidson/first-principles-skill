# First-Principles Analysis: gRPC Migration — Commit Now vs. Hold

Running full-composer mode (no single-technique trigger fired; this is a decision under uncertainty, analyzed holistically).

---

## Process output (required before conclusions)

### Phase 4 Assumption Audit — scan table

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| C1 | 1 | serialization/transport is a small slice of 48ms | Assumes modest payloads, in-datacenter hops | A3 (already present) → `[Assumes: A3]` |
| C1 | 2 | gRPC can't deliver a large *median* gain | none new | — |
| C2 | 1 | the 30% figure is a *p99* number | benchmark methodology unknown | **A8 added** |
| C2 | 2 | tail gain comes mostly from HTTP/2 multiplexing | assumes our tail is connection-contention-bound | **A9 added** |
| C3 | 1 | 5 engineers pulled while on-call is 3 | assumes migration/on-call staff overlap | **A10 added** |
| C3 | 2 | dual-protocol window raises incident surface | none new | — |
| C4 | 1 | stub-regen + redeploy is a fixed org tax | none new (A5) | `[Assumes: A5]` |
| C4 | 2 | consumer lag prolongs dual-protocol limbo | none new | — |
| C5 | all | synthesis of C1–C4 | none new | — |

### §6 → §4 closure ledger

```
- "Do not commit the team now"                         → chain C5 ✓
- "Hold, but convert the year into an evidence spike"  → chain C5 (2nd-order) ✓
- "gRPC cannot materially cut our median latency"      → chain C1 ✓
- "The claimed benefit is tail-specific and unmeasured"→ chain C2 ✓
- "On-call staffing is the binding execution risk"     → chain C3 ✓
- "Coordination cost is concrete and front-loaded"     → chain C4 ✓
```

Ledger clean; every §6 claim carries a chain. Rubric gate cleared (weakest links flagged with confidence caveats in Phase 5).

---

## 1. Problem Essence

**Core decision:** Does *this specific* gRPC migration, *at this time, with this team*, clear the bar of expected value over its concrete cost and operational risk — and is there any reason "now" beats "later"?

Note what the essence is **not**: it is not "is gRPC faster than REST" (a general claim), and it is not "did the competitor benefit" (a fact about a different system). Those are the framings the request arrives wrapped in; neither is the question that must be answered.

**Success criteria (checkable):**
1. Resolves commit-now vs. hold with an explicit derivation.
2. Grounded in *our* verified facts, not the competitor analogy.
3. Accounts for the on-call/capacity constraint.
4. Separates "is latency a problem?" from "is gRPC the solution?"

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | The 30% p99 benefit transfers to our system | convention/untested (analogy) | challenge before use | **Unverified** | no in-system data → flagged GT-7? |
| A2 | p99 latency is actually a business problem for us | untested belief | verify or flag | **Unverified** | no SLO cited (GT-8) |
| A3 | Serialization + transport is a material fraction of the 48ms | untested belief | verify via estimate | **Likely false** | Fermi estimate → GT-9 |
| A4 | 5 engineers exist as spare capacity | untested belief | verify | **Doubtful** | on-call is 3 (GT-5) |
| A5 | Consumer teams can regenerate stubs + redeploy inside the window | untested belief | flag | **Unverified** | GT-3 |
| A6 | The tail benefit is unobtainable without gRPC | untested belief | challenge | **Likely false** | HTTP/2 + connection-pool tuning on REST reaches much of it |
| A7 | The 48ms median and 340k req/min are accurate | current measurement | accept as GT | **Verified** | given |
| A8 | The competitor's 30% is a p99 figure under representative load | untested belief | flag | **Unverified** | methodology not disclosed |
| A9 | Our tail latency is connection-contention-bound | untested belief | verify | **Unverified** | no p99 breakdown exists |
| A10 | Migration engineers and on-call responders are non-overlapping | untested belief | verify | **Doubtful** | small platform team |

**Inversion pass** (what would *guarantee* this migration wastes effort): p99 isn't the bottleneck (A2); the benefit doesn't transfer because our latency is app/DB-dominated (A3); on-call collapses during the dual-protocol window (A10); consumers stall their redeploys (A5); the 30% was a best-case marketing benchmark (A8). Every one of these is an *unverified* precondition of "commit now" — which is the load-bearing observation of this analysis.

---

## 3. Ground Truths

- **GT-1:** Median inter-service latency = 48 ms. *(measured, given)*
- **GT-2:** Peak load = 340,000 req/min ≈ 5,667 req/s. *(measured, given)*
- **GT-3:** 6 of 22 services targeted; every consuming team must regenerate client stubs and redeploy. *(given — an org-wide coordination fact)*
- **GT-4:** Migration cost = 5 engineers × ~10 weeks = **~50 engineer-weeks**. *(given)*
- **GT-5:** On-call rotation = 3 people. *(given)*
- **GT-6:** gRPC uses binary protobuf serialization over multiplexed, persistent HTTP/2 connections; REST/JSON uses text serialization, classically over HTTP/1.1 connection pools. *(definitional/technical — irreducible)*
- **GT-7?:** Competitor benchmark claims 30% lower p99. **Unverified for our context** — this is an analogy about a different system, not a fact about ours.
- **GT-8:** We have **no stated p99 baseline for our own system and no cited latency SLO**. *(verified by omission — an absence that is itself load-bearing)*
- **GT-9 (estimated):** In-datacenter, JSON (de)serialization of a few-KB payload is order **1–20 µs**, and connection/transport overhead order **0.1–2 ms**; the 48 ms median is therefore dominated by application logic + downstream DB/cache calls. *(Fermi estimate — see Phase 4; central case: serialization+transport ≤ ~2–4% of 48 ms.)*

---

## 4. Derivation Chains

**Fermi estimate underpinning GT-9** (target unit: ms of the 48 ms median attributable to protocol):
few-KB payload ÷ JSON parse throughput (~hundreds of MB/s–GB/s) → ~1–20 µs serialization; in-DC RTT ~0.2–0.5 ms; pooled connections amortize setup → protocol-attributable slice ≈ **[0.1 ms, ~2 ms]**, i.e. **~0.2%–4%** of 48 ms. Bracket lower/upper both drive the same conclusion, so the estimate is decision-resolving.

**C1 — gRPC cannot materially cut our *median*:**
GT-1 + GT-6 + GT-9 → protocol overhead is a small fraction of the 48 ms `[Assumes: A3]` → eliminating it entirely yields only a few-percent median improvement → **the protocol swap is not a median-latency lever for us.** *(Confidence: MEDIUM — rests on the GT-9 estimate; a real measurement would settle it.)*

**C2 — the advertised benefit is tail-specific and, for us, unmeasured:**
GT-6 + GT-7? + GT-8 → the 30% is a *p99* figure, and tail gains come chiefly from HTTP/2 multiplexing removing HTTP/1.1 head-of-line/pool exhaustion → **without our own p99 baseline (GT-8) the expected benefit is uncomputable**, and much of the reachable tail gain is obtainable by enabling HTTP/2 + tuning connection pools on the *existing* REST stack (A6, A9). *(Confidence: MEDIUM.)*

**C3 — the on-call constraint is the binding execution risk:**
GT-4 + GT-5 → committing 5 engineers for 10 weeks while on-call is only 3 people (likely overlapping staff, A10), combined with a dual-protocol operating window (GT-3 + GT-6) that adds new failure modes → **incident surface rises exactly when operational capacity is thinnest.** *(Confidence: HIGH.)*

**C4 — coordination cost is concrete and front-loaded:**
GT-3 → org-wide stub regeneration + redeploy is a fixed tax paid regardless of the latency payoff `[Assumes: A5]`, and any consumer team that lags prolongs the dual-protocol limbo → **cost is certain and immediate; benefit is speculative and deferred.** *(Confidence: HIGH.)*

**C5 — decision:**
C1 + C2 + C3 + C4 → concrete, front-loaded cost and risk set against an unquantified, likely-small, tail-only, analogy-sourced benefit → **do not commit now.**

**Second-order extension of C5:** A *passive* "hold a year" leaves the identical evidence gap next year and wastes the time. Extending the chain forward: a **conditional hold** — spend a small spike now to (a) measure our own p99, (b) prototype gRPC on **one** high-traffic service to get an *in-system* delta, (c) A/B it against simply enabling HTTP/2 + pool tuning on REST as the cheap comparator, and (d) fix on-call staffing — de-risks *and* pre-qualifies any future migration. No extension step contradicts a ground truth. So the recommendation is **conditional hold, not indefinite hold.**

---

## 5. Abandoned Reasoning

- **"Commit because gRPC is the industry standard / the competitor did it."** Rejected: this is reasoning by analogy from GT-7?, which is unverified for our topology. Analogy is barred as direct evidence — it may motivate the spike, not the commitment.
- **"Reject gRPC outright."** Also rejected: GT-6 is a real efficiency difference and C2 concedes a plausible tail benefit. The problem is *unmeasured*, not *disproven* — which is exactly why the answer is "measure," not "no."

---

## 6. Conclusion

**Do not commit the team to this migration now. Hold — but make the hold an active evidence-gathering quarter, not a passive year.** (→ C5)

The recommendation rests on a clean asymmetry:

- **The benefit is unquantified and probably mis-attributed.** gRPC cannot meaningfully move your *median* 48 ms, because serialization and transport are only a few percent of it (C1). The competitor's 30% is a *tail* number you cannot even compare against — you have no p99 baseline of your own (C2, GT-8). And much of a genuine tail win is likely reachable by enabling HTTP/2 and tuning connection pools on your existing REST stack, at a fraction of 50 engineer-weeks (C2/A6).
- **The cost and risk are concrete and front-loaded.** 50 engineer-weeks, an org-wide stub-regen-and-redeploy tax (C4), and a dual-protocol window that widens your incident surface precisely while on-call sits at 3 people against a 5-engineer draw (C3).

**Before revisiting the decision, close the four unverified preconditions cheaply:**
1. **Measure your own p99** on the six candidate services — you are currently deciding on a metric you don't track (GT-8).
2. **Confirm there is an SLO the tail actually threatens** (A2). If nothing user-facing is at risk at p99, the entire premise weakens.
3. **Run a one-service bake-off:** gRPC prototype vs. HTTP/2 + pool-tuned REST, measured in *your* environment (C2). This replaces the analogy with a ground truth.
4. **Fix on-call staffing first** (C3) — it is the binding constraint on *any* large platform change, migration or not.

If, after that quarter, your own p99 shows a material, SLO-relevant tail problem that the REST-tuning comparator does *not* resolve, then commit — with a real in-system delta, a trained team, and a staffed rotation. That is a far stronger position than committing today on a competitor's benchmark.

**Confidence:** HIGH on the decision *given the inputs*; the two MEDIUM-confidence links (C1, C2) both hinge on the same missing measurement — your own p99 — which is exactly what step 1 of the recommendation produces. Verifying it is what would move those to HIGH.