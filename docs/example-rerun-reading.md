# Worked examples re-run on v9.13.0 — the reading

**A recorded reading with its N. Not a gate.**
**Protocol:** [`docs/example-rerun-protocol.md`](example-rerun-protocol.md), registered before any
run. **Captures:** `tests/example-rerun/` (frozen) — each re-run's stream, the agent's own
transcript, the delivered file, and `comparison.json`. **Re-derive the mechanical table:**
`python3 tests/example-rerun/run_examples.py compare`

---

## The answer in one paragraph

On all 14 worked examples, v9.13.0 delivered a complete six-section file, every one read by the
caller, with no output-limit cut-off. Judged against the shipped examples, **the re-runs are
more rigorous about evidence and the examples are cleaner on form**. The re-runs fetch and quote
sources the examples only cite, mark what they could not verify, catch three substantive points
the examples miss — **including a genuine defect in the shipped `estimate-fermi` example** — and
reach the same recommendation in 5 of 14, a partly overlapping one in 4, and a different one in
5. They are also 1.6–3.2× longer, carry more `?`-marked ground truths and lower confidence, and show the live-output defect
rates this repository has measured before, where the curated examples score almost zero. **Two
re-runs contain real errors** (an arithmetic slip; a missed hybrid option), and **one re-run is
contaminated** (it read the example it was compared against).

## Mechanical comparison — `run_examples.py compare`

Defects: untraced conclusion claims / malformed chain blocks / nonconforming verdict cells.

| Example | Words | GT ids | `?` GTs | Chains | Defects | Confidence |
|---|---|---|---|---|---|---|
| composed-inversion-second-order | 3,052 → 6,937 | 5 → 11 | 1 → 5 | 1 → 5 | 0/0/0 → 0/0/0 | MEDIUM → MEDIUM |
| decompose-irreducibility | 2,722 → 5,937 | 8 → 9 | 2 → 4 | 1 → 8 | 2/0/0 → 0/0/0 | MEDIUM → MEDIUM |
| estimate-fermi | 3,639 → 11,669 | 4 → 17 | 1 → 10 | 1 → 11 | 0/0/0 → 0/4/10 | MEDIUM → LOW |
| ishikawa-fishbone | 3,386 → 8,852 | 5 → 14 | 1 → 7 | 3 → 7 | 0/0/0 → 0/0/0 | MEDIUM → LOW |
| personal-general-2 | 4,824 → 8,028 | 6 → 11 | 1 → 4 | 3 → 4 | 0/0/0 → 0/0/0 | LOW → LOW |
| personal-general | 2,975 → 7,379 | 5 → 10 | 0 → 1 | 2 → 4 | 0/0/0 → 0/0/5 | MEDIUM → LOW |
| product-business-2 | 3,021 → 6,866 | 5 → 5 | 1 → 5 | 3 → 3 | 0/0/0 → 0/0/0 | MEDIUM → MEDIUM |
| product-business | 2,301 → 6,869 | 4 → 7 | 1 → 6 | 3 → 4 | 0/0/0 → 0/0/0 | MEDIUM → LOW |
| science-engineering-2 | 3,441 → 9,615 | 7 → 15 | 2 → 12 | 2 → 7 | 0/0/0 → 0/0/2 | MEDIUM → MEDIUM |
| science-engineering | 2,538 → 4,279 | 5 → 13 | 1 → 11 | 2 → 4 | 0/0/0 → 0/0/0 | MEDIUM → MEDIUM¹ |
| self-application² | 4,929 → 10,937 | 9 → 16 | 1 → 2 | 3 → 5 | 0/0/0 → 4/0/6 | MEDIUM → MEDIUM |
| software-systems-2 | 4,554 → 7,347 | 7 → 11 | 1 → 7 | 3 → 4 | 0/0/0 → 0/1/7 | MEDIUM → MEDIUM |
| software-systems | 4,699 → 8,690 | 5 → 12 | 0 → 2 | 3 → 9 | 0/0/0 → 3/1/0 | HIGH → MEDIUM |
| theoretical-limit-carnot | 3,574 → 7,896 | 4 → 0³ | 0 → 0³ | 1 → 5 | 0/0/0 → 0/5/1 | HIGH → LOW |
| **Totals** | | | | | **2/0/0 of 80/31/79 → 7/11/31 of 76/80/211** | |

¹ Read manually: the re-run states `**Confidence:** MEDIUM`; the section slicer missed it.
² Contaminated — see below. ³ The Carnot re-run wrote ids as `GT6`, not the contract's `GT-6`;
the id count reads 0 and the detector scores its hop lines malformed. A format defect, not a
reasoning one.

**Reading the defect totals.** 7 of 14 re-runs are defect-free. Pooled, the re-runs sit at
9% untraced, 14% malformed, 15% nonconforming — the same range as this repository's earlier live
corpora (`docs/live-conformance-v9.14-reading.md`: 5%, 6%, 14%). The curated examples are
near-zero because they are curated. This is the gap between shipped exemplars and live output,
not a change introduced by v9.13.0.

## Qualitative comparison — one judge per example

A judge read both documents of each pair. **These are judgements, not measurements** (the
protocol's §4); each finding below that names a number or a defect was checked against the
documents before it was written here.

| Example | Conclusion vs example | Judge's net | The point that decides it |
|---|---|---|---|
| composed-inversion-second-order | partly overlapping → different (full context) | mixed | with full context: a more conservative default, but misses the example's stale-read insight |
| decompose-irreducibility | **same** | improvement | live-verified sources; completes the cost estimate the example left partial |
| estimate-fermi | **different** | improvement (mixed) | **catches a defect in the example** — see below |
| ishikawa-fishbone | different | mixed | the example's HIGH root cause rests on internal data a standalone prompt cannot carry |
| personal-general-2 | **different** | mixed | invest-all vs split 60–70% to the mortgage; real/nominal basis unreconciled in the re-run |
| personal-general | partly overlapping | improvement | catches the equity **one-year vesting cliff** the example misses |
| product-business-2 | **same** | comparable → improvement | adds a weighted trade-off with a flip test |
| product-business | **same** | improvement | surfaces **cannibalisation** of the $2.4M ARR base, which the example never raises |
| science-engineering-2 | partly overlapping | improvement | catches that the operator's premise is physically backwards (cold oil is thicker, not thinner) |
| science-engineering | different sizing | mixed | right method (December design month) undercut by an **arithmetic error** |
| self-application | continuation | — (contaminated) | it read the example first |
| software-systems-2 | **different** | mixed → **regression** | **never considers the hybrid** the example finds dominant |
| software-systems | **same** | improvement | live-sourced, better-calibrated confidence, pre-mortem with tripwires |
| theoretical-limit-carnot | **same** | comparable | correct cold reservoir; weaker evidence (no measured Solar Two anchor) |

## Improvements

- **A real defect in a shipped example, found by the re-run.** `estimate-fermi` concludes that
  molten-salt storage is cost-competitive with lithium-ion "once both sides are on a common
  electrical basis". Its installed-cost rebuild prices the tanks, insulation, foundations,
  piping, pumps and the salt-to-steam heat exchanger — **not the turbine, generator or charging
  heater** that turning stored heat back into electricity requires — and then divides by an
  efficiency, which changes the unit without adding the missing equipment. It then compares that
  figure with lithium-ion's *installed system* price. Verified against the example's own text
  (its `system_factor` definition and Conclusion C1). **This should be filed and fixed.**
- **Evidence discipline.** Most re-runs fetch and quote sources the examples only cite (Vanguard's
  current forecast, Tax Foundation brackets, Fowler and DORA, conversion benchmarks) and log failed
  fetches as failures instead of citing past them.
- **Substantive catches the examples miss:** the equity vesting cliff (`personal-general`),
  free-tier cannibalisation (`product-business`), the inverted cold-oil premise
  (`science-engineering-2`), worst-month sizing (`science-engineering`).

## Regressions

- **`science-engineering` — an arithmetic error.** Chain C3 combines 4.4 sun-hours at latitude
  tilt with a further 10–20% gain from steeper tilt and reports "roughly 4.3" — below either
  input. The correct combination is ~4.8–5.3, which would bring the recommended array from
  ~800 W to ~670 W. Conservative in direction, but wrong.
- **`software-systems-2` — a missed option.** The re-run's own success criterion ("names exactly
  one of Build/Buy") foreclosed the hybrid — buy the identity provider for passwords, MFA and
  recovery; build tenancy, audit and authorisation — that the example finds dominant.
- **`theoretical-limit-carnot` — format and evidence.** Ground-truth ids written as `GT6`, and no
  measured current-practice anchor where the example has Solar Two's 34.1%.
- **`personal-general-2` — an unreconciled basis.** The re-run's opposite recommendation rests on
  a forecast whose real/nominal basis it never states against its break-even rate.
- **Length and hedging.** Re-runs are 1.6–3.2× longer; `?`-marked ground truths rise in 13 of 14
  and confidence falls in 6. Part of this is accurate — prompt-supplied facts are marked
  unverified when no source was opened — but it makes documents heavier to read.

## What limits this comparison

- **Curated vs live.** Each example was authored and revised across many phases; each re-run is a
  single generation. Differences mix the agent with the curation.
- **Prompt gaps, partly structural.** Several examples embed facts their fictional analyst
  *discovered* mid-analysis — exit-interview counts, bonding-ring conductance, figures handed over
  from companion examples. A standalone prompt cannot supply a discovery without supplying the
  answer. Where the judge found one, the table says so; `composed-inversion-second-order`'s gap
  was a prompt omission of mine, re-run with the full context below.
- **`self-application` is contaminated.** Its re-run followed its own reference paths to this
  repository and read the example it was being compared against. The protocol's statement that it
  "can see none of" the repository was wrong. No other re-run read an example or the repository.
- **One run per example; one judge per pair.**

## Supplementary — `composed-inversion-second-order` with the full scenario

My first prompt for this example carried only the one-sentence claim, and omitted the context its
scenario states: that the claim comes from the platform team lead's architecture-review document
citing peak read-QPS and the next-tier cost, the two decision options, and the upgrade's
procurement lead time. Without it, the re-run never chose between the options. A supplementary
run (`composed-inversion-second-order.full-context`, 8,908 words, same body and transport) was
given that context.

- **It now reaches a decision, and it is not the example's.** The example approves the cache
  rollout and cancels the upgrade *conditional on* a shadow-read hit-rate check and event-driven
  invalidation. The full-context re-run ships the cache but **keeps the upgrade on schedule**,
  deferring it only after a pre-defined evidence checkpoint with an independent owner — the
  conservative default inverted.
- **Better:** it raises a mechanism the example never does — database load can be structurally
  independent of read-QPS (vacuum, connection slots) — cites Postgres and AWS documentation read at
  source, and runs a weighted trade-off whose arithmetic the judge recomputed (57 against 72;
  crossing at weight 17).
- **Worse:** it **misses the example's central second-order finding** — that stale reads become a
  customer-visible contract with downstream consumers — and rates every chain LOW.
- **Evidence treatment:** the scenario's figures enter as given-but-unverified (`GT-7?`,
  "asserted, not independently observed"), neither ignored nor treated as fabricated.

Net: mixed. The prompt gap explained the first re-run's indecision; it did not explain the
difference in recommendation.
