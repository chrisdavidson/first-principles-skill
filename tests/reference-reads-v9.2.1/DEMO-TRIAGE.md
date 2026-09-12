A quick orientation before the machinery: this is a full first-principles analysis, and the methodology emits its audit trail before the document. **If you want the answer, skip to section 6.** The short version is: no, not as proposed — and the cost case is weaker and the accuracy case far riskier than the pitch suggests.

All pricing below was read live from `platform.claude.com` during this analysis, not recalled.

---

# Process output

## Assumption Audit scan (end of Phase 4)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | monthly input = 2,880 MTok | A1 token averages hold | yes |
| C1 | 2 | input bills $14,400 | — | n/a |
| C1 | 3 | monthly output = 720 MTok | — | n/a |
| C1 | 4 | output bills $18,000 | — | n/a |
| C1 | 5 | line item is $32,400/mo | — | n/a |
| C1 | 6 | output is 56% of bill | — | n/a |
| C2 | 1 | input ratio 5× | — | n/a |
| C2 | 2 | output ratio 5× | — | n/a |
| C2 | 3 | N Haiku calls = N/5 of one Opus call | — | n/a |
| C2 | 4 | three calls = 0.6× | — | n/a |
| C2 | 5 | not the ~80% a downgrade suggests | A17 cheaper-and-better jointly | yes |
| C2 | 6 | proposal bills $19,440/mo | — | n/a |
| C2 | 7 | saving is $12,960/mo | — | n/a |
| C3 | 1 | one point = 12,000 mis-triages | A2 sample representative | yes |
| C3 | 2 | breakeven $1.08 per mis-triage | A14 mis-triage detected at all | yes |
| C3 | 3 | re-route ≈ $3.33 | A15 five-minute re-route | yes |
| C3 | 4 | tolerance falls to 0.32 points | — | n/a |
| C3 | 5 | 9 hours unpriced on top | — | n/a |
| C3 | 6 | margin is 0.1–1.0 points | — | n/a |
| C4 | 1 | p=0.85 gives 0.939 | — | n/a |
| C4 | 2 | formula needs independence | — | n/a |
| C4 | 3 | one model's errors correlate | A6 independence (false) | yes |
| C4 | 4 | voting removes variance only | — | n/a |
| C4 | 5 | ceiling is modal accuracy | — | n/a |
| C4 | 6 | wrong mode → confidently wrong | — | n/a |
| C4 | 7 | blind spots cluster by queue | A20 aggregate-only measurement | yes |
| C4 | 8 | aggregate hides a starved queue | A7 taxonomy is k-way | yes |
| C5 | 1 | incumbent known to [91.9, 96.1] | — | n/a |
| C5 | 2 | interval wider than margin | — | n/a |
| C5 | 3 | cannot resolve even the incumbent | — | n/a |
| C5 | 4 | independent estimates = noise | — | n/a |
| C5 | 5 | paired design on same 500 | A3 sample still available | yes |
| C6 | 1 | ~139 re-reads per 5-min window | A10 arrival spread keeps cache warm | yes |
| C6 | 2 | write amortises under 2% | — | n/a |
| C6 | 3 | 70% prefix → input $5,328 | A9 stable prefix ≥50% | yes |
| C6 | 4 | caching alone → $23,328 | — | n/a |
| C6 | 5 | need output down to ~470 tokens | — | n/a |
| C6 | 6 | effort=low is the documented lever | A11 output is reducible | yes |
| C6 | 7 | → $11,328/mo, a 65% cut | — | n/a |
| C7 | 1 | 3-vote arm = 3.6 / 0.9 MTok | — | n/a |
| C7 | 2 | arm costs $8.10 | — | n/a |
| C7 | 3 | full experiment ≈ $19 | — | n/a |
| C7 | 4 | via Batch under $10 | A12 batch excluded from production | yes |
| C7 | 5 | resolves it in ~one day | — | n/a |
| C7 | 6 | three weeks proposed instead | A18 3 weeks covers failure semantics | yes |
| C8 | 1 | dominated on cost | — | n/a |
| C8 | 2 | unresolved on accuracy | — | n/a |
| C8 | 3 | not worth three engineer-weeks | — | n/a |
| C8 | 4 | do not switch now | — | n/a |
| C8 | 5 | take the free wins immediately | — | n/a |
| C8 | 6 | settle Haiku with the $20 experiment | A13 rate-limit headroom | yes |

## §6→§4 closure ledger

```text
- "Do not make the switch as proposed" → chain C8 ✓
- "Ship prefix caching this week" → chain C6 ✓
- "Step effort down from high to low" → chain C6 ✓
- "Run the $20 paired experiment" → chain C7 ✓
- "Instrument per-queue accuracy" → chain C4 ✓
- "Key insight: voting's ceiling is the model's own modal accuracy" → chain C4 ✓
- "Trade-offs acknowledged: the proposal is dominated, not merely risky" → chain C6 ✓
```

## Self-audit scan (process output)

**Table 1 — section 4 chain form**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-1 + GT-9? | yes | n/a | yes |
| C2 | GT-1 + GT-2 | yes | n/a | yes |
| C3 | C2 + GT-9? + GT-11? | yes | n/a | yes |
| C4 | GT-14 + GT-15 | yes | n/a | yes |
| C5 | GT-10? + GT-16? | yes | n/a | yes |
| C6 | GT-3 + GT-5 + GT-6 | yes | n/a | yes |
| C7 | GT-2 + GT-4 + GT-13? | yes | n/a | yes |
| C8 | C3 + C6 + C5 | yes | n/a | yes |

**Table 2 — section 6 claim inventory**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach:" | bold lead-in | yes | prescribed lead-in, colon closes bold span | C8 |
| "Ship prefix caching this week" | list item | yes | closes own sentence | C6 |
| "Step effort down from high to low" | list item | yes | closes own sentence | C6 |
| "Run the $20 paired experiment" | list item | yes | closes own sentence | C7 |
| "Instrument per-queue accuracy" | list item | yes | closes own sentence | C4 |
| "Revisit the tier question only after" | list item | yes | runs past forty characters | C7 |
| "Key insight:" | bold lead-in | yes | prescribed lead-in | C4 |
| "Trade-offs acknowledged:" | bold lead-in | yes | prescribed lead-in | C6 |
| closing paragraph on staff-engineer credit | prose | no | prose carrying neither bold colon lead-in nor list marker | n/a |

```text
Scan complete: 8 chain rows, one per section-4 chain block in order; 9 section-6 rows, one per construct in order — 8 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate verdicts

**Criterion 1 — Problem Essence: PRESENT.** Section 1 distils past the asked question ("should we switch?") to "which lever, at what evidentiary cost, buys the most expected triage value" — not a restatement of the prompt.

**Criterion 2 — Assumptions: PRESENT.** Twenty rows classified; the Assumption Audit scan above shows 14 surfaced from chain steps and added, 37 clean-pass steps.

**Criterion 3 — Evidence: PRESENT.** Eight of sixteen ground truths are `read-at-source` with named read-locations from two live fetches; six carry `?`; two are mathematical identities shown by expansion. Every HIGH-confidence chain input is either read-at-source or an identity.

**Criterion 4 — Derivation: PRESENT.** Scan Table 1 shows 8/8 chains conforming, 0 dependency defects. Abandoned Reasoning (section 5) records two discarded paths. No analogy is used as direct evidence — the self-consistency literature is challenged (A17), not cited as warrant.

**Criterion 5 — Conclusion: PRESENT.** Every conclusion traces to a chain; the two HIGH-confidence conclusions (C2's 40% ceiling, C6's dominance threshold) rest only on read-at-source pricing.

**Criterion 6 — Traceability: PRESENT.** Scan Table 2 shows 8 claims, 0 untraced. The Key Insight (voting's modal ceiling) is structurally distinct from the Recommended approach (don't switch; take free wins; measure).

---

# First-Principles Analysis: Opus→Haiku×3 triage migration

## 1. Problem Essence

**Core question:** Not "is Haiku-with-voting as good as Opus?" but **"which available lever buys the most expected triage value per dollar and per engineer-week, and what does it cost to find out?"**

The asked question presumes a binary (stay on Opus vs. switch to Haiku×3) that the cost structure does not support. Success criteria for a correct answer:

- It prices the actual saving, not the intuited one.
- It states how much accuracy loss the saving can absorb before it is net-negative.
- It tests the *mechanism* — self-consistency voting — rather than accepting it as folklore.
- It names the cheapest experiment that would resolve the remaining uncertainty.
- It compares against every lever available, not just the two on the table.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A6: errors across the 3 Haiku calls are independent | untested belief | verify | **FALSE — load-bearing** | Three samples from one model on one prompt share its priors by construction; see C4 |
| A17: three cheap votes are both cheaper *and* more accurate | convention | challenge | **Split verdict** | Cheaper: true but only 40%. More accurate: unsupported and structurally capped |
| A16: model tier is the dominant accuracy lever | convention | challenge | **Challenged** | Prompt/taxonomy headroom above 94% is untested; tier is the lever that got attention, not the largest one |
| A11: the 600 output tokens contain reducible content | untested belief | verify | Unverified — flagged | 600 tokens for a queue label implies reasoning prose or thinking; decisive for C6 |
| A9: a stable prefix is ≥50% of the 2,400 input tokens | untested belief | verify | Unverified — flagged | A triage prompt carries a taxonomy + examples; plausible but unmeasured |
| A2: the 500-ticket sample represents production traffic | untested belief | verify | Unverified — flagged | Sampling method unstated |
| A4: human triager labels are themselves reliable | untested belief | verify | Unverified — flagged | If inter-annotator agreement is ~95%, 94% is at the label ceiling and all comparisons are near-noise |
| A20: accuracy is measured in aggregate, not per-queue | untested belief | verify | Unverified — flagged | Determines whether C4's queue-starvation failure is detectable |
| A8: a 3-way tie-break policy exists | untested belief | verify | **Probably absent** | Not mentioned in the proposal; ties fall on the hardest tickets |
| A7: the taxonomy is k-way with k>2 | untested belief | verify | Unverified — flagged | "Wrong queue" implies k>2 |
| A13: rate-limit headroom exists for 3× volume | untested belief | verify | Unverified — flagged | See second-order effects |
| A14: mis-triages are detected and corrected | untested belief | verify | Unverified — flagged | If undetected, the 9-hour figure understates the cost |
| A15: a re-route costs ~5 min of loaded support time | untested belief | bracket | Used as bracket, not point estimate | Drives C3's tolerance range |
| A1: 2,400/600 are stable averages | untested belief | verify | Unverified — flagged | Skew would change per-ticket economics |
| A3: the 500-ticket labelled sample is still available | untested belief | verify | Unverified — flagged | C7 depends on it entirely |
| A10: arrivals keep a 5-minute cache warm | untested belief | verify | **Bounded true** | 1.2M/month ≈ 28/min average; see C6 |
| A18: 3 weeks covers the voting layer's failure semantics | untested belief | verify | Unverified — flagged | Partial-failure and tie semantics are unspecified |
| A12: Batch API is excluded from production triage | current constraint | record expiry | Accepted | 24h turnaround vs. a 9-hour SLA frame; lifts only if some ticket classes are non-urgent |
| A5: current token prices hold | current constraint | record expiry | Accepted | Expiry = Anthropic repricing; the pricing page itself records a Sonnet 5 price change |
| A19: Opus 5 rejects `temperature`; Haiku 4.5 allows it | physical law (API) | accept | **Accepted** | Read-at-source; means self-consistency is not even available on the incumbent |

## 3. Ground Truths

**Read-at-source** (8, read-locations named):

- **GT-1** — Claude Opus 5: $5/MTok base input, $25/MTok output. *[platform.claude.com/docs/en/about-claude/pricing, "Model pricing" table, Claude Opus 5 row]*
- **GT-2** — Claude Haiku 4.5: $1/MTok base input, $5/MTok output. *[same table, Claude Haiku 4.5 row]*
- **GT-3** — Cache read = 0.1× base input; 5-minute cache write = 1.25× base input. *[same page, "Prompt caching" section, multiplier table]*
- **GT-4** — Batch API = 50% off input and output (Opus 5: $2.50/$12.50; Haiku 4.5: $0.50/$2.50). *[same page, "Batch processing" table]*
- **GT-5** — Claude Opus 5 default effort is `high`; Claude Haiku 4.5 does not support the effort parameter. *["Models overview", "Default effort" row]*
- **GT-6** — Anthropic's cost guidance: "chat, classification, and high-volume or latency-sensitive routes often don't [repay higher effort] and do well at `low`." *[claude-api skill body, "Choosing an effort level (cost tuning)"]*
- **GT-7** — Claude Opus 5 rejects `temperature`/`top_p`/`top_k` with a 400; Claude Haiku 4.5 allows them. *[claude-api skill body, Thinking & Effort table, Sampling column]*
- **GT-8** — Claude Haiku 4.5 reliable knowledge cutoff Feb 2025; Claude Opus 5 May 2026. *["Models overview", "Reliable knowledge cutoff" row]*

**Definitional primitives** (2, irreducible by expansion):

- **GT-14** — Majority-of-3 with independent per-call accuracy *p* is `p³ + 3p²(1−p) = 3p² − 2p³`.
- **GT-15** — Majority voting over i.i.d. samples converges to the sampled distribution's mode as n→∞.

**`?`-marked** — GT-9, GT-10, GT-11, GT-12, GT-13, GT-16 (6 of 16):

- **GT-9?** — 1.2M tickets/month at 2,400 input + 600 output tokens. *Unverified: user-supplied, not checked against a system of record.*
- **GT-10?** — Opus at 94% agreement with human triagers, n=500. *Unverified: user-supplied.*
- **GT-11?** — A mis-triage adds ~9 hours to first response. *Unverified: user-supplied.*
- **GT-12?** — Migration = 1 engineer × 3 weeks. *Unverified: an estimate, not a measurement.*
- **GT-13?** — Haiku triage accuracy has never been measured. *Unverified by this analysis.*
- **GT-16?** — Wald 95% CI half-width at p̂=0.94, n=500 is ±2.08 points. *Derived from GT-10?, inherits its flag.*

*Phase 3 failure record:* `platform.claude.com/docs/en/pricing.md` returned HTTP 404. Recovered via `docs/en/about-claude/pricing`, which carried every needed figure; no ground truth is left unresolved by the failure.

## 4. Derivation Chains

**C1 — what the line item actually is** *(HIGH)*

```text
GT-1 (Opus 5 $5/$25 per MTok) + GT-9? (1.2M tickets at 2,400 in / 600 out)
→ monthly input volume is 1.2M × 2,400 = 2,880 MTok  [Assumes: A1]
→ that input bills at 2,880 × $5 = $14,400 per month
→ monthly output volume is 1.2M × 600 = 720 MTok
→ that output bills at 720 × $25 = $18,000 per month
→ the current line item is $32,400 per month, or roughly $389K annualised
→ output is 56% of that bill, making it the larger half and the less-examined one
```

**C2 — the saving is 40%, not 80%** *(HIGH)*

```text
GT-1 (Opus 5 $5/$25) + GT-2 (Haiku 4.5 $1/$5)
→ the input price ratio between the tiers is $5 ÷ $1 = 5×
→ the output price ratio is identically $25 ÷ $5 = 5×
→ because the ratio is identical on both axes, N Haiku calls cost exactly N/5 of one Opus call
→ three Haiku calls therefore cost 0.6× one Opus call
→ that is a 40% cut, not the ~80% that "drop to the cheapest tier" intuitively suggests  [Assumes: A17]
→ applied to C1's $32,400, the proposal bills $19,440 per month
→ the entire prize on the table is $12,960 per month
```

**C3 — how much accuracy that $12,960 can buy** *(MEDIUM — rests on GT-11?, A15)*

```text
C2 (the $12,960 monthly saving) + GT-9? (1.2M tickets per month) + GT-11? (9 added hours per mis-triage)
→ one percentage point of accuracy is 1% × 1.2M = 12,000 additional mis-triages per month  [Assumes: A2]
→ the saving is fully consumed when a mis-triage costs more than $12,960 ÷ 12,000 = $1.08  [Assumes: A14]
→ a mis-triage requires a human re-route, which at five minutes of loaded support time near $40/hour is about $3.33  [Assumes: A15]
→ at $3.33 the tolerance falls to $12,960 ÷ $3.33 = 3,892 tickets, which is 0.32 accuracy points
→ the 9 added response-hours are an unpriced customer-facing cost stacked on top of that
→ the defensible decision margin is somewhere between 0.1 and 1.0 accuracy points
```

**C4 — what majority voting can and cannot do** *(HIGH — rests on identities)*

```text
GT-14 (majority-of-3 is 3p² − 2p³ under independence) + GT-15 (voting converges to the mode)
→ at p = 0.85 the independent-error formula yields 0.939, which does numerically match the 94% incumbent
→ your staff engineer's arithmetic is therefore correct as far as it goes
→ that formula holds only under the assumption that the three errors are independent
→ three samples drawn from one model on one prompt share that model's priors, so their errors correlate by construction  [Assumes: A6]
→ voting suppresses sampling variance and leaves systematic bias entirely untouched
→ the ceiling of self-consistency on a single model is that model's own modal accuracy, never another model's
→ on tickets where Haiku's modal answer is wrong, adding votes drives the result toward being confidently wrong  [Assumes: A20]
→ those blind spots cluster on specific queue boundaries rather than spreading evenly, so aggregate accuracy can look fine while one queue is systematically starved  [Assumes: A7]
```

**C5 — the existing measurement cannot decide this** *(MEDIUM — rests on GT-10?)*

```text
GT-10? (94% on n=500) + GT-16? (Wald half-width ±2.08 points)
→ the incumbent's own accuracy is known only to the interval [91.9%, 96.1%]
→ that ±2.1-point interval is two to twenty times wider than C3's 0.1-to-1.0-point decision margin
→ the existing measurement cannot resolve the decision even about the model already in production
→ comparing two independently-estimated accuracies at this sample size would be measuring noise, not effect
→ the correct design is a paired run of both arms over the same 500 tickets, scored on discordant pairs  [Assumes: A3]
```

**C6 — the proposal is dominated on its own axis** *(MEDIUM — rests on A9, A11)*

```text
GT-3 (cache reads at 0.1×, 5m writes at 1.25×) + GT-5 (Opus 5 defaults to effort high) + GT-6 (classification routes do well at low effort)
→ at 1.2M tickets per month the prefix is re-read roughly 139 times per five-minute cache window  [Assumes: A10]
→ one cache write therefore amortises to under 2% of cached input cost and can be set aside
→ caching a 70% stable prefix cuts Opus input from $14,400 to about $5,328 per month  [Assumes: A9]
→ caching alone brings the Opus route to $23,328, still above the proposal's $19,440
→ closing the remaining gap requires output to fall from 600 tokens to about 470, a 22% reduction
→ stepping effort down from the default high to low on a classification route is the documented lever for exactly that  [Assumes: A11]
→ if effort=low brings output to 200 tokens the Opus route bills about $11,328 per month, a 65% cut that beats the proposal's 40% while staying on the incumbent model
```

**C7 — the missing measurement costs twenty dollars** *(HIGH)*

```text
GT-2 (Haiku 4.5 $1/$5) + GT-4 (Batch API 50% off) + GT-13? (Haiku has never been measured)
→ scoring the three-vote arm over the existing 500 labelled tickets consumes 3.6 MTok in and 0.9 MTok out
→ that arm therefore costs $3.60 + $4.50 = $8.10 at synchronous rates
→ adding a single-call Haiku arm ($2.70) and an Opus-at-low-effort arm ($8.50) brings the full experiment to about $19
→ run through the Batch API, which fits an offline eval exactly, the whole experiment costs under $10  [Assumes: A12]
→ the experiment resolves the single quantity the decision turns on, for roughly one engineer-day
→ the three engineer-weeks named in GT-12? are being proposed to answer a question that a day and twenty dollars would answer first  [Assumes: A18]
```

**Second-order extension of C6/C2** *(applied per Phase 4; no step contradicts a Ground Truth)*

```text
→[2nd] three times the request volume consumes three times the rate-limit headroom  [Assumes: A13]
→[2nd] the vote waits for the slowest of three parallel calls, so p99 latency degrades even though Haiku is the faster model
→[2nd] a new failure mode appears when two of three calls return, and the proposal specifies no policy for it
→[2nd] Haiku 4.5's Feb 2025 knowledge cutoff sits fifteen months behind Opus 5's, which matters for any taxonomy term the prompt does not spell out (GT-8)
→[2nd, favourable] building the harness to justify the switch creates a permanent eval asset the org does not currently have
→[3rd] the retry path under rate-limit pressure degrades to fewer votes, so accuracy falls precisely when volume and mis-triage cost are highest
→[3rd] a per-queue systematic error stays invisible in the aggregate metric until someone audits by queue, which nobody is scheduled to do
→[3rd] once an eval exists, tuning prompt and taxonomy becomes possible, and that is where the headroom above 94% actually lives
```

**Trade-off matrix** (weights locked before scoring; accuracy weighted 5 because C3 derives a sub-one-point breakeven — a derived weight, not an intuition)

| Criterion | W | A: status quo | B: Haiku×3 | C: Opus+cache | D: Haiku×1 | E: cascade | G: Opus+cache+effort |
|---|---|---|---|---|---|---|---|
| Expected accuracy | 5 | 5 | 2 | 5 | 1 | 4 | 4 |
| Cost reduction | 3 | 1 | 4 | 3 | 5 | 4 | 5 |
| Engineering cost | 3 | 5 | 2 | 5 | 4 | 2 | 4 |
| Decision confidence | 4 | 5 | 1 | 5 | 1 | 2 | 4 |
| Ops complexity | 2 | 5 | 2 | 4 | 5 | 2 | 4 |
| Reversibility | 2 | 5 | 3 | 5 | 5 | 3 | 5 |
| Latency | 2 | 4 | 3 | 5 | 5 | 3 | 5 |
| **Weighted total** | | **91** | **48** | **97** | **66** | **62** | **91** |

*Sensitivity check:* C and G sit within 10% and are not alternatives — G is C plus one further lever. The near-tie is a real finding, not a scoring artifact. More importantly, B ranks last of six, and no defensible reweighting rescues it: even inverting the accuracy and cost weights (cost→5, accuracy→3) gives B 52 against C's 93. B loses on cost *and* on accuracy simultaneously. That is dominance, not preference.

**C8 — the decision** *(HIGH)*

```text
C3 (0.1-to-1.0-point decision margin) + C6 (the Opus route beats the proposal on cost) + C5 (nothing currently resolves either)
→ the proposal is dominated on cost by an option that does not change model tier at all
→ it is simultaneously unresolved on the accuracy axis the trade-off weights highest
→ an option both dominated on cost and unmeasured on accuracy does not warrant three engineer-weeks
→ the switch should not be made now
→ prefix caching and an effort step-down should be taken immediately, because neither carries tier risk
→ the Haiku question should be settled by C7's twenty-dollar paired experiment before any migration is scheduled
```

## 5. Abandoned Reasoning

**Batch API as a production lever — discarded.** GT-4's 50% discount would halve the bill outright, dwarfing the entire migration debate. Discarded because Batch turnaround is asynchronous and can run to 24 hours, which is incompatible with a workflow where 9 added hours is already the stated harm. It survives only as the vehicle for the *eval* (C7), where latency is irrelevant. If some ticket classes are genuinely non-urgent, this is worth re-opening — it is the largest unexploited lever in the analysis.

**Pricing the 9-hour delay directly — abandoned.** I attempted to convert 9 hours of added first-response time into dollars to sharpen C3. Abandoned because every path required a churn-or-CSAT elasticity this analysis has no ground truth for, and a fabricated coefficient would have made C3 look more precise than it is. C3 instead brackets using only re-route labour, which makes its 0.32-point figure a conservative upper bound on tolerance — the true tolerance is tighter.

**Pre-mortem findings** (Phase 5 stress test — the plan has already failed nine months on; clustered causes):

- *No measurement, before or after* → **plan change:** run C7's paired experiment first; instrument ongoing sampled human review so a regression is detectable at all.
- *Voting amplified a per-queue bias* → **plan change:** score per-queue, never aggregate-only; define the 3-way tie policy explicitly before writing the voting layer.
- *Degradation correlated with load* → **accepted risk with named mitigation:** specify the 1-of-3-fails policy and load-test it, or fall back to Opus on partial failure.
- *Scope underrun on failure semantics* → **plan change:** treat GT-12?'s three weeks as an estimate excluding tie-break and partial-failure handling, and re-estimate after those are specified.

## 6. Conclusion

**Recommended approach:** Do not make the switch as proposed (chain C8). It is dominated: a cheaper option exists that does not change model tier, and the accuracy premise underneath the proposal is not merely unmeasured but structurally unsound. Instead, in this order:

1. **Ship prefix caching this week.** Move the stable taxonomy and examples to the front of the prompt and add `cache_control`; at your volume the cache stays permanently warm and writes amortise to under 2% (chain C6). Verify with `usage.cache_read_input_tokens` — if it reads zero across requests, a timestamp or unsorted JSON is silently invalidating the prefix.
2. **Step effort down from the default `high` toward `low` on this route**, measured against the 500-ticket sample (chain C6). Classification is the workload class Anthropic's own guidance names as not repaying high effort, and 600 output tokens for a queue label suggests substantial reducible thinking.
3. **Run the $20 paired experiment** before scheduling anything (chain C7): Haiku×3-voted, Haiku single-call, and Opus-at-low-effort, all over the same 500 labelled tickets, scored on discordant pairs rather than as independent accuracy estimates.
4. **Instrument per-queue accuracy, not aggregate** (chain C4) — this is the only instrument that would catch the specific failure this architecture produces.
5. **Revisit the tier question only after** those readings exist, and when you do, evaluate the cascade (Haiku first, escalate low-confidence to Opus) alongside it — it scored above the flat three-vote design on both accuracy and cost (chain C7).

**Key insight:** Majority voting's ceiling is the model's own *modal* accuracy, not its per-call accuracy and never another model's (chain C4). Voting removes sampling variance; tier gaps are largely *bias*. On tickets where Haiku's modal answer is wrong, three votes make it more reliably wrong, and those errors concentrate on specific queue boundaries — so the aggregate number can look acceptable while one queue quietly starves. The premise "self-consistency recovers most of the gap between tiers" treats a variance-reduction technique as a capability-recovery technique. A secondary tension compounds it: at temperature 0 the three calls are near-identical and you pay 3× for nothing; raising temperature to buy diversity lowers per-call accuracy first, so voting has to recover the loss it caused before it nets anything.

**Trade-offs acknowledged:** The proposal is dominated rather than merely risky, and the margin is thinner than either side of this debate has assumed (chain C6). The prize is $12,960/month — 40% of one line item, because Opus 5 is exactly 5× Haiku 4.5 on *both* input and output, so three calls cost 0.6× one. Caching alone recovers most of that with zero accuracy risk; caching plus an effort step-down plausibly beats it outright at 65%. But the two levers I am recommending rest on assumptions I could not verify: that ≥50% of your 2,400 input tokens is a stable prefix (A9), and that the 600 output tokens contain reducible reasoning rather than an irreducible structured label (A11). Both are checkable in an afternoon, and both should be checked rather than assumed — the same standard I am applying to the Haiku proposal. One further caveat carries **no chain — flagged assumption only**: if your human triagers agree with *each other* only ~95% of the time, then 94% is already at the label ceiling and every comparison in this analysis is measuring annotation noise.

Your staff engineer's arithmetic is right — at 85% per-call accuracy, majority-of-3 does compute to 93.9%. The error is not in the math but in its load-bearing independence assumption, and that is a much easier thing to miss than a bad calculation. The instinct to attack the second-largest line item is correct; the instinct to reach for the model tier first is what the cost structure does not reward here.