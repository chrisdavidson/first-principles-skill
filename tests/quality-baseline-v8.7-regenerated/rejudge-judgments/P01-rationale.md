I read both files in full. (Note: `analysis.md` lines 107–110 carry a trailing harness artifact — an `agentId`/`<usage>` block appended after the final sentence. It is transport noise, not authored content, and I scored nothing against it.)

---

## Assumption Audit (completed before scoring)

Every derivation chain in section 4 was enumerated and each step visited in order.

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|-------------------|----------------------|-----------------|
| A (mean-latency win) | 1 | `GT-2 + GT-3 → per-hop saving 15–45 µs + ~2 µs wire ≈ 0.02–0.05 ms` | A9: representative payload is ~5 KB and services run a compiled runtime (both are GT-2/GT-3 preconditions, not stated as ours) | yes |
| A | 2 | "assume a request traverses 3–6 *sequential* hops" | A10: sequential hop depth is 3–6 — declared in prose, absent from the Assumptions Table | yes |
| A | 3 | `GT-4 → a typical p50 of 50–200 ms` | A11: our p50 sits in the industry-typical band (distinct from A1/A7, which concern *composition*, not magnitude) | yes |
| A | 4 | "→ full migration cannot deliver a perceptible mean-latency improvement" | A12: "perceptible" means ≳1 ms at the user-facing boundary — threshold never defined | yes |
| B (tail exception) | 1 | `GT-7 + GT-8? → p99 contains 10s–100s ms of queueing delay` | A13: connection contention actually materialises at current traffic levels (GT-7's mechanism requires load, not just HTTP/1.1) | yes |
| B | 2 | "→ attributable to HTTP/2, not to protobuf or to gRPC" | A14: HTTP/2 is separably deployable on the existing REST stack without the gRPC toolchain | yes |
| C (theoretical ceiling) | 1 | "assume *zero-cost* serialization; GT-1 + GT-4 → floor is RTT + downstream I/O" | none | n/a |
| C | 2 | "Conventional figure: current transport cost ~0.3 ms" | A15: current transport cost ≈ 0.3 ms — a figure carried by no GT and no citation; it is the load-bearing input to the "Gap: ≈ 0" result | yes |
| C | 3 | "**Gap: ≈ 0.** ... Protocol is not the constraint" | none (follows from step 2) | n/a |
| D (cost) | 1 | `GT-6 + A5 → cost scales with call-graph edges plus fixed tooling/observability/CI` | none (A5, A6 already in Table) | n/a |
| D | 2 | "→ expect a multi-quarter program with a prolonged dual-stack period" | A16: team size and delivery velocity are within normal range for a 40-service program — no staffing input supplied | yes |
| Second-order pass | 1 | "*2nd order:* dual-stack lengthens; debuggability degrades; codegen becomes a release-coupling bottleneck" | none | n/a |
| Second-order pass | 2 | "*3rd order:* engineering attention diverted ... latency may *worsen*" | A17: the org treats the migration as *the* latency fix and will not staff GT-4 work in parallel | yes |

**Assumptions Table addendum (A9–A17 added before scoring Criterion 2).** All nine are Type: *untested belief* except A10 and A16 (*current constraint*) and A12 (*convention*). All nine carry Verdict: **unverified — flagged**; Verification for A10/A11/A15 is the same distributed-trace span breakdown named in Conclusion step 1, which also resolves A9; A13/A14 resolve via the client connection-config inspection named in Chain B; A12/A16/A17 require a product-threshold and staffing input from leadership.

The scan was exhaustive over the named derivation chain steps in section 4 — it is not an open-ended survey of conceivable assumptions.

---

**Criterion 1: Identify Essence**
Quoted span: "**Core question:** Is transport-protocol substitution the binding constraint on our latency, and does the expected latency gain exceed the cost and risk of rewriting the interface layer of 40 services?" ... "1. Quantify the latency actually attributable to REST/JSON transport, separately from everything else in the request path. ... 4. Survive the case where the latency measurement is not yet available."
Band: **Rigorous**
Justification: The statement is a single sentence naming the underlying decision rather than the triggering event — a distinction the section makes explicit ("Leadership has stated a solution, not a problem") — and each of the four success criteria is a verb+subject+outcome triplet a reviewer can pass/fail by scanning section 6, with wording ("REST/JSON transport," "the dual-stack transition period") that could not transfer unmodified to a different problem.

**Criterion 2: Challenge Assumptions**
Quoted span: "| A3 | Existing REST clients use HTTP/1.1 without connection pooling | untested belief | Verify | **Unverified — decisive.** If false, the multiplexing win largely evaporates | Inspect client configs |"
Band: **Sound**
Justification: All eight rows carry Type values drawn from the four-type scheme with matching Treatment vocabulary and specific Verification cells, and A1/A4/A5 are genuinely challenged rather than accepted — but the Verdict column departs from the prescribed Accept/Challenge/Discard vocabulary in seven of eight rows ("Rejected as default," "True but small," "False"), and A3, which feeds Chain B while unverified, carries "Inspect client configs" in its Verification cell rather than the required "unverified — flagged" notation; the un-tabled chain assumptions A9–A17 surfaced in the audit above are a further specific shortfall, now remedied in the addendum.

**Criterion 3: Establish Ground Truths**
Quoted span: "**GT-4:** Database queries, cache misses, downstream I/O, and GC pauses in typical backend services occupy **1–3 orders of magnitude more** of a request's wall-clock than transport encoding. *(measurement, near-universal in traced systems)*"
Band: **Sound**
Justification: GT-IDs are stable and match every reference in section 4, GT-8? correctly carries the `?` suffix and is consistently rendered with it inside Chain B, and no Discard-verdict assumption appears in the list — but GT-4, the single most load-bearing fact in the document, cites an evidence *class* ("near-universal in traced systems") rather than a specific source, as does GT-2's "standard benchmarks," which is the identifiable shortfall of the Sound band rather than the specific citation Rigorous requires.

**Criterion 4: Reason Upward**
Quoted span: "GT-2 + GT-3 → per-hop saving of 15–45 µs serialization + ~2 µs wire ≈ **0.02–0.05 ms** → assume a request traverses 3–6 *sequential* hops (fan-out in parallel does not add) → **total saving 0.06–0.30 ms**."
Band: **Sound**
Justification: All four chains name the GT-IDs they consume and carry genuine intermediate claims statable from no single GT alone (the per-hop-to-per-request aggregation, Chain C's zero-cost-serialization ceiling, Chain B's HTTP/2-vs-protobuf attribution), and Abandoned Reasoning documents three dead ends with specific structural reasons — including an exemplary refusal of analogy-as-evidence ("Discarded — analogy, not evidence. Their ground truths ... are not established as ours") — but the assumptions introduced mid-chain are declared in running prose rather than with the prescribed `[Assumes: X]` token, which appears nowhere in the document, and Conclusion step 4's positive case for gRPC ("streaming, strict schema contracts, polyglot codegen") is asserted without a chain; the latter is banded here per the precedence rule and only noted under Criterion 6.

**Criterion 5: Validate**
Quoted span: "**Confidence: MEDIUM**, inherited from unverified GT-8?. Verification: inspect one high-traffic client's connection config. If it already pools well or sits behind an HTTP/2 mesh, this chain collapses to zero."
Band: **Sound**
Justification: The one chain consuming a `GT-N?` input is correctly capped below HIGH with the causing input named and a specific confidence-raising verification attached, the HIGH rating on Chain A is defended by robustness ("survives an order-of-magnitude error in every input"), and the document closes with a named weakest link tied to a specific GT — but Chain C carries no confidence rating at all despite being cited in the Conclusion as co-support for the central recommendation, an isolated omission of the per-chain weak-link identification Rigorous requires of *every* chain.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "its third-order effect — diverting attention from the real latency sources — makes latency *more* likely to stay bad."
Band: **Rigorous**
Justification: Each Conclusion claim traces to a named chain — the refusal to migrate to Chains A and C, step 2 to Chain B, step 3 to GT-4, the cost framing to Chain D — and the key insight is a genuinely non-obvious inversion produced in section 4's second-order pass ("That last effect **contradicts the stated goal**") rather than a restatement of the recommendation, so the Conclusion synthesises rather than introduces; the one unchained claim (step 4's affirmative case for gRPC) is noted here but banded under Criterion 4 per the precedence rule and does not lower this band.

---

**Gate:** no criterion scores Absent. **Hand-wavy cap:** zero criteria score Hand-wavy. Both conditions clear.

=== QUALITY-HARNESS-SCORELINE-START ===
C1: Rigorous
C2: Sound
C3: Sound
C4: Sound
C5: Sound
C6: Rigorous
Verdict: PASS
=== QUALITY-HARNESS-SCORELINE-END ===