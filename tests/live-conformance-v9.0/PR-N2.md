## Missing information (stated up front, per the Input Contract)

`AskUserQuestion` is not available in this session, and no image-pipeline source exists in this working directory — I grepped it, and every hit was vendored Python or this repo's own gate scripts. So I am proceeding best-effort, and four inputs that would materially change the analysis were never supplied:

1. **The bill's line-item split** — storage at rest vs. requests vs. data transfer out. This one is decisive: chain C4 shows a lever aimed at the wrong term.
2. **Average original size, and how many derivative variants you store per upload.** These are the two dominant uncertain factors; without them the cost estimate spans eightyfold (C6).
3. **Whether any retention policy exists, and whether you are legally free to delete.** C5 shows this is the only lever that bounds the problem.
4. **Whether originals are retained and your resize/encode is deterministic.** This gates the single largest structural option (C2).

Everything below is structurally sound without these; the *magnitudes* are not.

---

## §6→§4 closure ledger (process output)

```text
- "Measure three quantities before choosing any lever..." → chains C6, C1, C5 ✓
- "Read the bill's split between storage at rest, requests and transfer out first" → chain C4 ✓
- "Census bytes and objects by prefix... and check whether the total grows linearly" → chains C6, C1 ✓
- "Apply lifecycle tiering to originals above 128 KB only, to Glacier Instant Retrieval" → chains C3, C8 ✓
- "Move derivative generation on demand behind a cache, with a variant whitelist" → chains C2, C7, C3 ✓
- "Open the retention question with product and legal now" → chain C5 ✓
- "A bill that rises every month is the arithmetic signature of indefinite retention" → chains C1, C5 ✓
- "Each lever buys a smaller bill with something else" → chains C8, C7, C5 ✓
- CUT: "deduplication is a promising early win" (no chain; claim removed — see §5)
- CUT: "re-encode the back catalogue to AVIF" (no chain; claim removed — see §5)
```

---

# 1. Problem Essence

**Essence Statement:** Which term of the object-storage cost function is actually growing — bytes at rest, retention time, or data transfer — and which lever reduces total cost of ownership without violating an unstated retention or latency requirement?

The triggering event is "storage costs are climbing." That is not the question. A pipeline ingesting at a constant rate with no deletion produces a monotonically rising bill *by arithmetic*, with nothing wrong anywhere (C1). The real question is which term is growing and whether the growth is linear or faster.

**Success criteria** (each checkable against section 6 by scanning it):

1. The Conclusion names which cost term to measure before recommending any change.
2. The Conclusion distinguishes levers that reduce the *slope* of the cost curve from levers that change its *shape*.
3. The Conclusion states, for at least one option, a specific condition under which that option *increases* cost.
4. The Conclusion sequences actions by lead time, not by expected saving.

---

# 2. Assumptions Table

Assumption space enumerated breadth-first with a fishbone over the default six-category set, then attacked with inversion on the claim "reducing stored bytes will reduce our bill."

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | The pipeline stores pre-computed derivative variants alongside originals | untested belief | verify or flag | Challenge — determines whether the multiplier term exists at all | unverified — flagged |
| A2 | Originals are retained indefinitely; no deletion policy runs | untested belief | verify or flag | Challenge — C5 turns entirely on this | unverified — flagged |
| A3 | "Storage costs" names the storage-at-rest line, not the whole object-storage bill | untested belief | verify or flag | Challenge — C4 attacks this directly | unverified — flagged |
| A4 | The provider is AWS S3 or an S3-compatible store | untested belief | verify or flag | Accept provisionally — affects which price constants apply, not the structure | unverified — flagged |
| A5 | Images are served to end users through a CDN | untested belief | verify or flag | Challenge — if false, egress almost certainly dominates | unverified — flagged |
| A6 | Object versioning is off and no orphaned incomplete multipart uploads accumulate | untested belief | verify or flag | Challenge — a classic invisible leak that shows in no object count | unverified — flagged |
| A7 | The upload rate is roughly constant, not itself growing | current constraint | record expiry conditions | Accept — expires if upload volume is growing, in which case cost is quadratic in time and C1's diagnostic inverts | unverified — flagged; check month-over-month upload counts |
| A8 | The team is legally and contractually free to delete user images | untested belief | verify or flag | Challenge — E is blocked outright if false | unverified — flagged; needs legal, not engineering |
| A9 | Storage is billed at list rate per byte-month, with no committed-spend contract | convention | challenge before use | Challenge — an enterprise agreement or reserved-capacity commit makes marginal reduction worth less than list arithmetic suggests | unverified — flagged |
| A10 | Storage price per GB is uniform across objects with no per-object floor | convention | challenge before use | **Discard — false.** GT-5 and GT-6 show tier transitions impose per-object minimums and a fixed 40 KB overhead | verified false, read-at-source (AWS S3 User Guide, lifecycle transitions) |
| A11 | Resize/encode is deterministic across encoder versions | untested belief | verify or flag | Challenge — feeds GT-11?; if false, regenerated derivatives may differ visibly from stored ones | unverified — flagged |
| A12 | The climbing cost is attributable to the image pipeline at all, rather than to logs, backups, or non-production buckets on the same bill line | untested belief | verify or flag | Challenge — the fishbone's highest-value output; cheapest thing on this list to check | unverified — flagged |
| A13 | Modern codecs (WebP, AVIF) save roughly 25–50% over JPEG at comparable perceptual quality | untested belief | verify or flag | Challenge — widely repeated, not read at source by this analysis | unverified — flagged |
| A14 | Per-item request traffic on an uploaded image decays with age | untested belief | verify or flag | Challenge — surfaced by the Phase 4 audit on C2 step 5 | unverified — flagged; check CDN age-of-object hit distribution |
| A15 | The number of stored variants per upload is single-digit | untested belief | verify or flag | Challenge — surfaced by the Phase 4 audit on C4 step 1 | unverified — flagged |
| A16 | Average original size falls between 0.5 MB and 8 MB | untested belief | verify or flag | Challenge — surfaced by the Phase 4 audit on C6 step 2; the dominant uncertainty | unverified — flagged |
| A17 | Derivative URLs carry free-form resize parameters rather than an enumerated variant set | untested belief | verify or flag | Challenge — surfaced by the Phase 4 audit on C7 step 2 | unverified — flagged |
| A18 | The product may need synchronous access to old images | untested belief | verify or flag | Challenge — surfaced by the Phase 4 audit on C8 step 1 | unverified — flagged |
| A19 | Thumbnail-class derivatives are on the order of tens of KB | untested belief | verify or flag | Challenge — surfaced by the Phase 4 audit on C3 step 1 | unverified — flagged |

Inversion produced no precondition not already listed, which is weak evidence the table is complete.

---

# 3. Ground Truths

**Provenance labels:** `read-at-source` = this analysis opened the cited source and located the asserted wording. `user-asserted` = supplied by the requester about their own system, treated as a fixed starting point per the Input Contract. `definitional` = a definition, which the irreducibility test accepts as a stopping point.

| ID | Fact | Provenance | Read location |
|---|---|---|---|
| GT-1 | Uploads run at approximately 40,000 per day | user-asserted | requester's statement |
| GT-2 | The storage cost line is rising over time | user-asserted | requester's statement; growth *shape* not supplied |
| GT-3 | Storage cost at rest = Σ(object size × time retained × price per GB-month) | definitional | corroborated by the billing structure of both sources read below |
| GT-4 | Object-storage bills comprise at minimum three distinct charge types: storage at rest, request operations, and data transfer out | read-at-source | Cloudflare R2 pricing docs, pricing table (storage / Class A / Class B / egress rows); AWS S3 pricing page, "You pay for all bandwidth into and out of Amazon S3" |
| GT-5 | S3 Lifecycle will not transition objects smaller than 128 KB to any storage class by default; AWS states "for smaller objects, the transition costs can outweigh the storage savings" | read-at-source | AWS S3 User Guide, "Transitioning objects using Amazon S3 Lifecycle" → "Constraints and considerations for transitions" → heading "Objects smaller than 128 KB will not transition by default to any storage class" |
| GT-6 | Each object archived to Glacier Flexible Retrieval or Deep Archive carries 8 KB of metadata billed at S3 Standard rates plus 32 KB of index billed at Glacier rates — 40 KB total per object | read-at-source | same page, "Cost considerations" → "Storage overhead charges"; restated in the closing Note as "the per-object storage overhead (40 KB total, of which 8 KB is charged at S3 Standard rates and 32 KB at the destination Glacier rate)" |
| GT-7 | Minimum storage durations: Glacier Instant Retrieval 90 days, Glacier Flexible Retrieval 90 days, Deep Archive 180 days; exiting early incurs a prorated charge for the remainder | read-at-source | same page, "You are charged for transitioning objects before their minimum storage duration" and "Number of days you plan to keep objects archived" |
| GT-8 | Glacier Flexible Retrieval and Deep Archive objects "are not available in real time"; restoring one bills both the archive rate and a temporary copy at S3 Standard rates | read-at-source | same page, "General considerations" bullet 2, and the Note under "Restoring archived objects" |
| GT-9 | Cloudflare R2: $0.015/GB-month standard storage, $0.01/GB-month infrequent access, Class A $4.50/million, Class B $0.36/million, egress to internet free | read-at-source | Cloudflare R2 pricing docs, pricing table; "Egressing directly from R2 ... does not incur data transfer (egress) charges and is free" |
| GT-10? | S3 Standard is near $0.023/GB-month and internet egress near $0.09/GB in a primary US region | **unverified** | **Phase 3 failure record:** WebFetch of `https://aws.amazon.com/s3/pricing/` succeeded but the pricing tables did not render — the retrieved text states "the actual numerical pricing tables appear to exist on the original page but aren't fully legible in this text extraction." Reason: *citation does not support the claim*. Figures are from prior knowledge, unread. |
| GT-11? | Derivative images are deterministically reconstructible from the retained original | **unverified** | Near-definitional for a deterministic pipeline, but contingent on A2 (originals retained) and A11 (encoder determinism), neither of which this analysis can observe |

**`?`-marked ground truths, enumerated by ID: GT-10, GT-11 (2 of 11).**

I deliberately did not retry GT-10 through search. The estimate procedure's stop criterion says to tighten the *dominant* uncertain factor; in C6 the dominant factors are bytes per original and the derivative multiplier, which swing the answer eightyfold, while the unit price swings it by perhaps ±20%. Tightening a non-dominant factor while the dominant one is entirely unobserved would not resolve any decision.

---

# 4. Derivation Chains

**C1 — A rising storage bill is not a diagnosis.** Confidence: **HIGH** (all inputs unsuffixed and read-at-source or user-asserted).

```text
GT-1 (40,000 uploads a day) + GT-2 (the storage bill is rising) + GT-3 (cost at rest is bytes times time times price)
→ with a constant upload rate and no deletion, total stored bytes grow linearly in elapsed time [Assumes: A7]
→ the bill therefore rises by a constant increment every month with no change in traffic, image size or configuration
→ a rising storage bill is the expected steady state of an append-only pipeline rather than evidence of a defect
→ so the diagnostic question is whether the rise is faster than linear, which is what separates a regression from a retention policy
```

Weakest link: hop 1, which rests on A7 (constant upload rate). If uploads are themselves growing, cost is quadratic in time and the linear baseline this chain establishes is the wrong yardstick.

At central values this increment is about **$126/month added every month, forever**, with nothing changing.

**C2 — Derivatives are a cache, not data.** Confidence: **MEDIUM**, downgraded by GT-11? (reconstructibility unverified). Verification that raises it to HIGH: confirm originals are retained and the resize/encode path is deterministic across encoder versions.

```text
GT-3 (cost at rest is bytes times time times price) + GT-11? (derivatives are reconstructible from retained originals)
→ stored bytes decompose into originals, which accumulate with time, and derivatives, which are a multiple of the originals
→ the originals term is an integral over retention time and is reduced by moving it to a cheaper tier or deleting it
→ the derivatives term is a multiplier on catalogue size and is reduced only by not storing derivatives at all
→ derivative storage cost scales with the size of the catalogue, whereas derivative regeneration cost scales with request traffic
→ in a corpus that grows without bound while per-item traffic decays, regeneration is asymptotically cheaper than storage [Assumes: A14]
→ generating derivatives on demand behind a cache is therefore the structurally correct treatment of the multiplier term
```

Weakest link: hop 5, which needs A14 (traffic decays with object age). If old images are read as often as new ones, the asymptotic argument fails and storing derivatives is defensible.

**C3 — Archiving small derivatives increases cost.** Confidence: **HIGH** (both inputs read-at-source).

```text
GT-6 (Glacier adds 40 KB of billed overhead per object) + GT-5 (objects under 128 KB do not transition by default)
→ for any object smaller than 40 KB the archive metadata overhead exceeds the object's own payload [Assumes: A19]
→ a 20 KB thumbnail moved to Glacier is billed for roughly three times the bytes it contains, split across two price tiers
→ AWS blocks that transition by default rather than letting a lifecycle policy lose money silently
→ lifecycle tiering is therefore a lever that applies to originals and never to the small-derivative population
```

Weakest link: hop 1's dependence on A19, the assumed thumbnail size band. The conclusion is unaffected for any derivative under 128 KB, which is the population AWS's own default already excludes.

**C4 — The bill may be dominated by a term no storage lever touches.** Confidence: **HIGH** (all three inputs unsuffixed; the request-term arithmetic uses R2's read-at-source price, so it does not inherit GT-10?).

```text
GT-4 (bills split into storage, requests and transfer out) + GT-9 (R2 charges $4.50 per million writes and nothing for egress) + GT-1 (40,000 uploads a day)
→ at 40,000 uploads a day with a single-digit number of variants each, monthly write operations land near ten million [Assumes: A15]
→ ten million writes priced at $4.50 per million is under fifty dollars a month, so the request term cannot be driving the bill
→ the bill is therefore dominated by storage at rest or by transfer out, and those two respond to disjoint levers
→ a major provider makes free egress its headline commercial position, which is only rational if egress is material for real workloads
→ an image workload is read-heavy by nature, so its transfer-out volume tracks traffic rather than catalogue size
→ a line item labelled "storage" can therefore be dominated by a term no tiering, codec or dedup change touches, so the split must be read off the bill first
```

Weakest link: hop 4's inference from a competitor's pricing stance to a claim about typical bills. It is evidence, not proof — but it is evidence from a company that priced its product on the belief.

**C5 — Only deletion bounds the problem.** Confidence: **HIGH** (both inputs unsuffixed). This is the theoretical-limit result: it names what the cost function permits once conventions are stripped.

```text
GT-1 (constant upload rate) + GT-3 (cost at rest is bytes times time times price)
→ under indefinite retention the stored-byte total has no upper bound, so the bill grows without limit
→ tiering, re-encoding and deduplication each multiply that total by some constant factor below one
→ a constant factor applied to an unbounded quantity leaves it unbounded
→ deleting at a fixed age instead caps total stored bytes at the upload rate multiplied by that age [Assumes: A8]
→ a capped byte total converts a bill that grows forever into one that levels off, which is a change in kind rather than degree
```

Weakest link: hop 4, gated entirely on A8 (freedom to delete). This is a legal question, not an engineering one, and it has the longest lead time of anything in this analysis.

**C6 — The magnitude is unknown to within two orders of magnitude.** Confidence: **MEDIUM**, downgraded by GT-10? (unit price unread — see the Phase 3 failure record). Verification that raises it to HIGH: read current per-GB storage and egress prices at source, *and* measure A16.

```text
GT-1 (40,000 uploads a day) + GT-10? (storage priced near $0.023 per GB-month)
→ multiplying uploads per day by days by bytes per upload by price per GB-month reconstructs a monthly bill in dollars
→ at a central 3 MB original and a 1.5x total multiplier the twelve-month figure lands near $1,500 a month [Assumes: A16]
→ at a conservative 0.5 MB original with no stored derivatives the same arithmetic gives roughly $170 a month
→ at an aggressive 8 MB original with a 5x multiplier it gives roughly $13,400 a month
→ that bracket spans roughly eightyfold and straddles the threshold at which engineering effort is worth spending
→ the dominant uncertain factors are bytes per original and the derivative multiplier, so measuring those two is what resolves the decision
```

Unit check: (uploads/day) × (days) × (GB/upload) × ($/GB-month) → $/month. Weakest link: hop 2, resting on A16. The bracket fails the decision-resolution stop criterion — its ends drive *opposite* decisions, which is precisely why measurement must precede selection rather than follow it.

**C7 — On-demand derivatives create a cost-amplification attack surface.** Confidence: **MEDIUM**, inherited from C2's dependence on GT-11?. Second-order extension of C2; no step contradicts a ground truth.

```text
C2 (generate derivatives on demand behind a cache) + GT-1 (40,000 uploads a day)
→ [2nd] serving a derivative now costs CPU at request time instead of storage at rest, so cost becomes coupled to traffic
→ [2nd] a cache key derived from arbitrary resize parameters in the URL admits an unbounded set of distinct variants [Assumes: A17]
→ [3rd] an attacker requesting many distinct widths forces unbounded cache misses and unbounded origin compute
→ [3rd] restricting the permitted variants to a signed or enumerated whitelist is a precondition of the design rather than optional hardening
```

Weakest link: hop 2, gated on A17. If your URLs already carry an enumerated variant set, this risk does not exist.

**C8 — Tiering mortgages future product optionality.** Confidence: **HIGH** (C3 is HIGH; GT-7 and GT-8 are read-at-source). Second-order extension of C3; no step contradicts a ground truth.

```text
C3 (tiering applies to originals only) + GT-8 (archived objects need a paid, non-real-time restore) + GT-7 (90- and 180-day minimum storage durations)
→ [2nd] any product feature that surfaces old content synchronously now incurs retrieval latency and a retrieval charge [Assumes: A18]
→ [2nd] the minimum durations mean a tiering decision cannot be cheaply reversed within three to six months of taking it
→ [3rd] a future bulk read of the corpus, for a search reindex or model training, becomes a budgeted multi-hour operation
→ [3rd] choosing Glacier Instant Retrieval over the colder classes buys back real-time access at a smaller discount, which is the right trade while access patterns are unmeasured
```

Weakest link: hop 1's dependence on A18. If you can guarantee old images are never surfaced synchronously, Deep Archive becomes defensible and the discount is much larger.

## Weighted trade-off

Criteria and weights locked before any option was scored. All criteria phrased so higher is better.

| Criterion | Weight | A: tier originals | B: on-demand derivatives | C: re-encode on ingest | D: dedup | E: retention policy | F: zero-egress provider |
|---|---|---|---|---|---|---|---|
| Cost reduction magnitude | 5 | 3 | 4 | 3 | 2 | 5 | 4 |
| Reversibility | 4 | 4 | 5 | 2 | 4 | 1 | 3 |
| Implementation speed | 3 | 5 | 2 | 3 | 3 | 2 | 2 |
| Product-risk safety | 5 | 4 | 3 | 3 | 4 | 2 | 4 |
| Payoff certainty without further measurement | 3 | 4 | 3 | 3 | 2 | 5 | 3 |
| Durability (fixes growth rate, not just level) | 4 | 2 | 4 | 3 | 2 | 5 | 3 |
| **Weighted total** | | **86** | **86** | **68** | **69** | **80** | **79** |

**Sensitivity check.** A and B tie exactly. The flipping criterion is implementation speed (A scores 5, B scores 2); dropping its weight from 3 to 1 gives B the win. Per the procedure I did not refine scores on a near-tie, and the honest reading is that **A and B are not competitors** — A attacks the retention integral, B attacks the derivative multiplier, and they compose. The tie is telling us the sequencing, not the winner.

---

# 5. Abandoned Reasoning

**Dead end 1 — pricing S3 at source.**
*What was tried:* WebFetch of the AWS S3 pricing page to read per-GB-month and egress figures directly.
*Why abandoned:* The fetch returned the page but not its pricing tables — the retrieved text explicitly states the numerical tables "aren't fully legible in this text extraction." Recorded as a Phase 3 failure record against GT-10?. I chose not to retry via search because the dominant uncertainty in C6 is byte volume, not unit price, and the estimate procedure's stop criterion directs effort at the dominant factor.
*What it ruled out:* Any HIGH-confidence dollar figure. C6 is capped at MEDIUM as a direct result.

**Dead end 2 — deduplication as a headline lever.**
*What was tried:* Ranking content-addressed dedup among the primary options, on the reasoning that UGC pipelines carry real duplicate rates.
*Why abandoned:* Camera-originated photographs are near-unique at the byte level — EXIF timestamps alone differ between two shots of the same scene. Dedup's payoff therefore concentrates entirely in *retry duplicates and reposts*, which is a bug in the upload path, not a storage strategy. It scored 69, second-lowest, dragged down by the lowest payoff-certainty score in the table.
*What it ruled out:* Dedup as a first move. It stays in the table as a cheap check on whether your retry path is writing duplicate objects.

**Dead end 3 — bulk re-encoding the back catalogue to a modern codec.**
*What was tried:* Treating a corpus-wide AVIF/WebP migration as a large one-time saving.
*Why abandoned:* It requires reading every object (paying retrieval), re-encoding, and rewriting — the most expensive possible way to touch a corpus — and it is irreversible if originals are discarded. C5 shows the reason it is dominated: if the corpus is worth the cost of touching every object, it is worth *deleting* or *tiering* instead, and both of those beat re-encoding on every criterion except speed. Its supporting figure (A13, 25–50% codec saving) is also unverified.
*What it ruled out:* Re-encoding as a lever against the back catalogue. Re-encoding *on ingest*, forward-only, survives as option C at 68 — the lowest score in the table.

**Dead end 4 — grounding the analysis in your actual pipeline.**
*What was tried:* Searching the working directory for pipeline source, config, or infrastructure definitions.
*Why abandoned:* No such code exists here; every match was vendored Python or this repo's own validation scripts.
*What it ruled out:* Any read-at-source ground truth about your system specifically. Recorded so that the `?` marks and the flagged assumptions are attributable to genuine absence rather than to not looking.

---

# 6. Conclusion

**Overall confidence: MEDIUM.** Three contributing chains (C2, C6, C7) are MEDIUM, downgraded by GT-10? and GT-11?. The *structure* below is HIGH-confidence; the *magnitudes* are not.

**Recommended approach:** Measure three quantities before choosing any lever, then sequence the cheap tiering win ahead of the structural derivative rebuild, and open the retention decision in parallel because it has by far the longest lead time (chains C6, C1, C5).

1. **Read the bill's split between storage at rest, requests and transfer out before touching anything** — if transfer out dominates, every option below is aimed at the wrong term and a CDN or a zero-egress provider is the whole answer (chain C4).
2. **Census bytes and objects by prefix with a size histogram, splitting originals from derivatives, and check whether the total is growing linearly or faster than linearly** — linear growth is a retention decision, super-linear growth is a regression, and they need opposite responses (chains C6, C1). While you are in there, check for object versioning and orphaned incomplete multipart uploads, which accumulate invisibly and appear in no object count.
3. **Apply lifecycle tiering to originals above 128 KB only, targeting Glacier Instant Retrieval rather than the colder classes** — this is hours of work with no code change, and the tier choice preserves the real-time access that Flexible Retrieval and Deep Archive would cost you (chains C3, C8).
4. **Move derivative generation on demand behind a cache, with an enumerated or signed variant whitelist shipped as part of the same change** — derivatives are a reconstructible cache whose storage cost scales with catalogue size while their regeneration cost scales with traffic, and the whitelist is what stops the saving being handed straight back as an origin-compute bill (chains C2, C7, C3).
5. **Open the retention question with product and legal now, in parallel with the engineering work** — it is the only lever that bounds the problem, and it is the only one whose lead time is measured in weeks of other people's calendars rather than days of yours (chain C5).

**Key insight:** A storage bill that rises every month is the arithmetic signature of indefinite retention at a constant upload rate, not a symptom of anything being wrong — so every lever except deletion multiplies an unbounded quantity by a constant and leaves it unbounded, and the only decision that changes the *shape* of the curve rather than its slope is deciding what to stop keeping (chains C1, C5).

**Trade-offs acknowledged:** Every lever buys a smaller bill by spending something that does not appear on the storage line — tiering pays in future retrieval latency, a three-to-six-month lock-in from minimum durations, and a quiet constraint on any future corpus-wide read such as a search reindex or model training (chain C8); on-demand derivatives pay in compute that is now coupled to traffic and in a new abuse surface that must be closed in the same change (chain C7); and deletion pays in irreversibility, which is why it needs a decision from people who are not on the engineering team (chain C5).

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | constant rate, no deletion → linear byte growth | A7 (upload rate constant) | already present — marked inline |
| C1 | 2 | bill rises by constant increment monthly | none | n/a |
| C1 | 3 | rising bill is expected steady state | none | n/a |
| C1 | 4 | diagnostic is linear vs. super-linear | none | n/a |
| C2 | 1 | bytes decompose into originals and derivatives | A1 (derivatives are stored) | already present |
| C2 | 2 | originals term is a retention integral | A2 (indefinite retention) | already present |
| C2 | 3 | derivatives term is a catalogue multiplier | none | n/a |
| C2 | 4 | storage scales with catalogue, regen with traffic | none | n/a |
| C2 | 5 | corpus unbounded while per-item traffic decays | **A14 (traffic decays with age)** | **yes — added** |
| C2 | 6 | on-demand behind a cache is structurally correct | none | n/a |
| C3 | 1 | objects under 40 KB have overhead exceeding payload | **A19 (thumbnails are tens of KB)** | **yes — added** |
| C3 | 2 | 20 KB thumbnail billed for ~3x its bytes | none | n/a |
| C3 | 3 | AWS blocks the transition by default | none | n/a |
| C3 | 4 | tiering applies to originals, never small derivatives | none | n/a |
| C4 | 1 | ~10M monthly write operations | **A15 (single-digit variant count)** | **yes — added** |
| C4 | 2 | request term under $50/month | none | n/a |
| C4 | 3 | bill dominated by storage or transfer out | none | n/a |
| C4 | 4 | free egress as headline position implies egress is material | none | n/a |
| C4 | 5 | image workloads are read-heavy; egress tracks traffic | A5 (CDN in front) | already present |
| C4 | 6 | split must be read off the bill first | A3 ("storage" names the at-rest line) | already present |
| C5 | 1 | indefinite retention gives unbounded byte total | A2 (indefinite retention) | already present |
| C5 | 2 | other levers multiply by a constant below one | A9 (list-rate billing), A13 (codec saving) | already present |
| C5 | 3 | constant factor on unbounded quantity stays unbounded | none | n/a |
| C5 | 4 | deletion at fixed age caps total bytes | A8 (free to delete) | already present — marked inline |
| C5 | 5 | capped total is a change in kind | none | n/a |
| C6 | 1 | unit-factor product reconstructs monthly bill | none | n/a |
| C6 | 2 | central case ≈ $1,500/month | **A16 (original size 0.5–8 MB)** | **yes — added** |
| C6 | 3 | conservative case ≈ $170/month | none | n/a |
| C6 | 4 | aggressive case ≈ $13,400/month | A1 (derivatives stored) | already present |
| C6 | 5 | bracket spans ~80x and straddles the threshold | none | n/a |
| C6 | 6 | dominant factors are size and multiplier | none | n/a |
| C7 | 1 | cost becomes coupled to traffic | none | n/a |
| C7 | 2 | arbitrary URL parameters admit unbounded variants | **A17 (free-form resize params)** | **yes — added** |
| C7 | 3 | attacker forces unbounded misses and compute | none | n/a |
| C7 | 4 | whitelist is a precondition, not optional | none | n/a |
| C8 | 1 | old-content features incur latency and charge | **A18 (product may need old images synchronously)** | **yes — added** |
| C8 | 2 | minimum durations block cheap reversal | none | n/a |
| C8 | 3 | bulk corpus read becomes a budgeted operation | none | n/a |
| C8 | 4 | Instant Retrieval buys back real-time access | none | n/a |

Audit visited all 39 chain steps across 8 chains, in order. Six previously-undeclared assumptions surfaced (A14–A19) and were added to the section 2 table.

---

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | `GT-1 (...) + GT-2 (...) + GT-3 (...)` | yes | n/a | yes |
| C2 | `GT-3 (...) + GT-11? (...)` | yes | n/a | yes |
| C3 | `GT-6 (...) + GT-5 (...)` | yes | n/a | yes |
| C4 | `GT-4 (...) + GT-9 (...) + GT-1 (...)` | yes | n/a | yes |
| C5 | `GT-1 (...) + GT-3 (...)` | yes | n/a | yes |
| C6 | `GT-1 (...) + GT-10? (...)` | yes | n/a | yes |
| C7 | `C2 (...) + GT-1 (...)` | yes | n/a | yes — C2 resolves, no cycle |
| C8 | `C3 (...) + GT-8 (...) + GT-7 (...)` | yes | n/a | yes — C3 resolves, no cycle |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Overall confidence: MEDIUM." | bold lead-in | no | closing `**` not immediately preceded by the colon — not matched | n/a |
| "Three contributing chains (C2, C6, C7) are MEDIUM..." | prose | no | prose carrying neither bold colon lead-in nor list marker | n/a |
| "**Recommended approach:** Measure three quantities..." | bold lead-in | yes | prescribed lead-in; always a claim | C6, C1, C5 |
| "Read the bill's split... before touching anything" | list item | yes | closes its own sentence, over forty characters | C4 |
| "Census bytes and objects by prefix..." | list item | yes | closes its own sentence, over forty characters | C6, C1 |
| "Apply lifecycle tiering to originals above 128 KB only..." | list item | yes | closes its own sentence, over forty characters | C3, C8 |
| "Move derivative generation on demand behind a cache..." | list item | yes | closes its own sentence, over forty characters | C2, C7, C3 |
| "Open the retention question with product and legal now..." | list item | yes | closes its own sentence, over forty characters | C5 |
| "**Key insight:** A storage bill that rises every month..." | bold lead-in | yes | prescribed lead-in; always a claim | C1, C5 |
| "**Trade-offs acknowledged:** Every lever buys a smaller bill..." | bold lead-in | yes | prescribed lead-in; always a claim | C8, C7, C5 |

```text
Scan complete: 8 chain rows, one per section-4 chain block in order; 10 section-6 rows, one per construct in order — 8 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced.
```

---

## Self-Audit Gate

**Criterion 1: Identify Essence**
Quoted span: "Which term of the object-storage cost function is actually growing — bytes at rest, retention time, or data transfer — and which lever reduces total cost of ownership without violating an unstated retention or latency requirement?"
Band: **Rigorous**
Justification: A single sentence naming the underlying question rather than the trigger ("costs are climbing"), followed by four success criteria each carrying a verb-subject-outcome triplet checkable by scanning section 6 — criterion 3, "states a specific condition under which that option increases cost," is satisfied by C3 and could not be transplanted to an unrelated analysis.

**Criterion 2: Challenge Assumptions**
Quoted span: from the Assumption Audit scan — "Audit visited all 39 chain steps across 8 chains, in order. Six previously-undeclared assumptions surfaced (A14–A19) and were added to the section 2 table."
Band: **Rigorous**
Justification: All 19 rows carry a Type from exactly the four-type scheme, every Verdict leads with Accept/Challenge/Discard followed by a specific justification, every unverified row reads "unverified — flagged," A10 was genuinely challenged and discarded with a read-at-source refutation, and the audit scan is exhaustive over named chain steps rather than an open-ended survey.

**Criterion 3: Establish Ground Truths**
Quoted span: enumerated GT-10, GT-11; the list carries `?` on exactly those two entries and on no others — checked by reading the eleven-row table rather than by quoting the enumeration line.
Band: **Rigorous**
Justification: All eleven GTs carry stable IDs matching the chain heads, every unsuffixed GT names a specific read location (page and section heading, not "common knowledge"), every unsuffixed GT feeds at least one HIGH-confidence chain, and GT-10's `?` is backed by a Phase 3 failure record naming the source and the reason (*citation does not support the claim* — the pricing page opened but its tables did not render). Exception (a), unreachable source, is **claimed** here for GT-10, which consequently feeds only the MEDIUM chain C6.

**Criterion 4: Reason Upward**
Quoted span: from the self-audit scan chain-form table — all eight rows read "Form conforming? yes / Rule applied: n/a / Dependency clean? yes," with C7 and C8 additionally noted "C2 resolves, no cycle" and "C3 resolves, no cycle."
Band: **Rigorous**
Justification: Every chain uses the prescribed head-plus-arrow-led form with one hop per physical line, each carries at least one genuine intermediate not restatable from any single input, Abandoned Reasoning documents four dead ends in What-was-tried / Why-abandoned / What-it-ruled-out structure with specific structural reasons rather than "seemed unlikely," six chain steps carry `[Assumes: X]` declarations, and the one comparative reference (Cloudflare's pricing stance, C4 hop 4) is grounded in named GT-9 rather than offered as standalone analogy. Noted without lowering the band: several section-6 items cite two or three chains, but these are composite recommendations drawing on distinct chains for distinct parts — C3 scopes the tiering lever while C8 selects the tier — rather than the redundant restatement the Sound clause names.

**Criterion 5: Validate**
Quoted span: "Confidence: **MEDIUM**, downgraded by GT-11? (reconstructibility unverified). Verification that raises it to HIGH: confirm originals are retained and the resize/encode path is deterministic across encoder versions."
Band: **Rigorous**
Justification: Every chain carries a confidence rating and a named weakest link; both GT-N? inputs appear in the confidence line of every chain that consumes them, each stating the specific verification that raises the rating; no chain consuming a `?` input is rated HIGH; every section-6 claim rests on at least one HIGH chain; and the overall Conclusion rating is stated as MEDIUM, matching the weakest contributing chains (C2, C6, C7) rather than being reported as HIGH alongside them. Neither the speculative nor the absent-fails exception is claimed.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: from the self-audit scan claim-inventory table — 8 claims under R11, every one naming a section-4 chain, "0 claims untraced."
Band: **Rigorous**
Justification: All eight section-6 claims trace to named chains, no claim introduces reasoning absent from section 4, and the Key Insight — that a rising bill is the arithmetic signature of indefinite retention, so every lever but deletion multiplies an unbounded quantity by a constant — is a non-obvious result from C5's theoretical-limit derivation rather than a restatement of the recommended approach, which is the operationally distinct claim that measurement must precede lever selection.

**Gate: PASS.** No criterion Absent; zero criteria at Hand-wavy, within the cap of one. No re-entry edge fired; no Fix/Repeat pass was required.

---

**Two things to hand back to me and this gets much sharper:** the bill's storage/requests/egress split, and a byte-and-object count split between originals and derivatives. Those two numbers collapse the eightyfold bracket in C6 and settle whether C4's warning applies to you.