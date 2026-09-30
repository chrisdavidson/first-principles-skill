<!-- GENERATED — DO NOT EDIT -->
<!-- Source: scripts/gen-evidence-card.py -->
<!-- Regenerate: python3 scripts/gen-evidence-card.py -->

# Evidence

What has actually been measured about this agent — with sample sizes, dates, and
the known blind spots of every instrument that produced a number.

**There is no overall quality score on this page, and that is deliberate.** The
first section explains why: we built one, checked whether it tracked the thing it
appeared to measure, and found that it did not. Publishing it anyway would have
been the easier choice and a dishonest one.

Every figure below is re-read from its cited source each time this page is
generated. If a source changes so that it no longer says what this page claims,
the page fails to build rather than going stale.

---

## What we found when we checked our own metrics

These are the findings that constrain everything else on this page.
They are published because they came out badly.

### Our own format-conformance score does not predict whether the analysis is right

**The most arithmetically accurate document (100% correct) FAILED the rubric; the least accurate (50% correct) PASSED it**

*Sample: 6 documents · Measured: 2026-07-22 · Source: [`docs/v8.7-correctness-spot-check.md`](v8.7-correctness-spot-check.md)*

What this does not say: One six-document sample. It is why this page publishes no composite quality score — but it does not prove the rubric is worthless, only that it is a formatting instrument being asked a question it cannot answer.

### The same pattern appeared again on real work, independently

**On a genuine (non-test) task the better of two answers was the one that conformed less — 0 of 6 prescribed sections**

*Sample: 1 task, 2 runs · Measured: 2026-07-27 · Source: [`docs/use-journal.md`](use-journal.md)*

What this does not say: A single journal entry, n=1. Its value is that it is independent of the six-document study above and points the same way; it is not a second study.

### We measured our own judge and found it drifts — upward

**Re-scoring six byte-identical documents on a different day moved the total +7 points out of 108 and flipped one verdict from FAIL to PASS; five of six documents moved up, none moved down**

*Sample: 6 documents, re-scored · Measured: 2026-07-22 · Source: [`docs/v8.7-quality-baseline-freeze.md`](v8.7-quality-baseline-freeze.md)*

What this does not say: This is the reason any improvement we report has to clear roughly +7/108 before it means anything. It also means a favourable-looking result is exactly what noise produces here, which is why comparative claims on this page require a threshold fixed before the run.

### When we A/B tested a change we expected to matter, it didn't

**Both arms 2/3 PASS, band total 35 each — no detectable difference**

*Sample: 6 documents (3 problems × 2 arms) · Measured: 2026-07-22 · Source: [`docs/v8.6-quality-ab-experiment.md`](v8.6-quality-ab-experiment.md)*

What this does not say: The contrast tested was a 3.6% change in the agent's instruction length. It supports 'this particular compression cost nothing measurable', not 'size never matters'. Published because it came out null.

### Our automatic defect detector misses most planted defects

**10 of 13 deliberately-wrong test analyses were NOT caught**

*Sample: 13 adversarial fixtures · Measured: 2026-09-18 · Source: [`docs/conformance-baseline.md`](conformance-baseline.md)*

What this does not say: This is published so that a clean reading from that detector is read correctly: it means the instrument found nothing, never that the analysis is correct. Nine of the thirteen produced no signal at all.

---

## What the output looks like when measured

### When we re-derived the numbers in six analyses by hand, most held up

**47 correct / 6 wrong / 12 unverifiable, across 65 load-bearing quantitative claims**

*Sample: 65 claims across 6 analyses · Measured: 2026-07-22 · Source: [`docs/v8.7-correctness-spot-check.md`](v8.7-correctness-spot-check.md)*

What this does not say: Six documents is a directional finding, not a statistical claim, and the phase's own text says so. `unverifiable` means the claim rested on an external fact the check had no authorisation to look up — it is not a silent pass.

### None of the errors changed a recommendation

**Zero material errors in 65 examined load-bearing claims**

*Sample: 65 claims across 6 analyses · Measured: 2026-07-22 · Source: [`docs/v8.7-correctness-spot-check.md`](v8.7-correctness-spot-check.md)*

What this does not say: 'Material' was defined before the results were known: an error whose correction would change the recommendation or its direction. Six of the 65 claims were still simply wrong.

### On live runs, most output is structurally clean — but not all

**5 of 8 live runs scored zero form defects**

*Sample: 8 live runs · Measured: 2026-09-06 · Source: [`docs/conformance-baseline.md`](conformance-baseline.md)*

What this does not say: Conditional on the agent having been dispatched — it is not an end-to-end rate for an ordinary user prompt. One failing run had 31 of 31 verdict cells non-conforming, so the failures are not marginal when they happen. And per the line above, 'clean' means this detector found nothing.

---

## Compared against not using it

The question any measurement above leaves open: does the analysis come out
better than the same model answering the same problem without this plugin?

**agent arm scored +3.40 points higher on a 15-point rubric across 10 paired problems**

*Sample: 10 per arm · Measured: 2026-09-30 · Run: `trackb-run-v9.15`*

**Caveat:** The scored arm-T document is identifiable by its format with near certainty, so this result cannot separate reasoning quality from a format or halo effect.

*Partial context, not part of the threshold: the same effect measured on the orchestrator's final message instead of the delivered file differs by +0.60 points.*

The effect threshold and the full analysis plan were fixed in writing
before any run took place — see [the pre-registration](trackb-2-preregistration.md).
The pre-registered threshold was: paired permutation p < 0.05; effect > 2.0x in-run drift; direction holds in >= 3 of 4 domains.

---

## What this page does not claim

- **No overall quality score.** See the first section.
- **No accuracy rate for analyses in general.** The correctness check covered
  six documents, once, by hand.
- **Nothing about domains we have not tested.** The measured problems are drawn
  from software, policy, biology and ethics. That is a spread, not a sample.
- **Nothing about how often the agent is reached automatically.** Phrase-based
  routing is unreliable; use the slash command. The last measurement of that rate
  is old and labelled as such in [Getting Started](GETTING-STARTED.md).

---

## Reproducing these numbers

```sh
# regenerate this page from its sources (fails if any source no longer matches)
python3 scripts/gen-evidence-card.py --check

# the full offline gate battery
bash scripts/check-firewall-battery.sh

# the structural defect detector's own control battery
python3 scripts/check-quality-harness.py --self-test
```

The measurement apparatus behind each reading is described in
[MEASUREMENT-MAP.md](MEASUREMENT-MAP.md) and
[TESTING.md](TESTING.md).
