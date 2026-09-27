# Live-output conformance — the v9.14 reading

**A recorded reading with its N. Not a gate, and it may not become one.**
Emission rates are K-of-N live observations, and
[`docs/v8.7-constraint-teardown.md`](v8.7-constraint-teardown.md) §2 item 3 bars those from
gating. `EMIT-STAGE-A`'s control C19 fails if `cmd_conformance` ever acquires a failing exit
code.

**Corpus:** `tests/emission-stage-a-v9.14/documents/` (frozen) · **Detector:**
`check-quality-harness.detect_defects`, the same instrument the v9.0 surface uses
**Re-derive:** `python3 scripts/check-emission-stage-a.py conformance --out-dir tests/emission-stage-a-v9.14`

---

## Why this exists

Every analysis-quality gate in this repository reads one of three layers: the **shipped prose**
(`shared/`, `first-principles/`), the **frozen exemplars**, or its **own fixtures**. None reads
what the agent actually produced at runtime. The apparatus is enforced one layer away from where
quality happens.

That was tolerable while no live corpus existed. One does now, and it has defects.

## The reading

**N = 9 scored, 1 unreadable.**

| Reading | Numerator / denominator | Rate |
|---|---|---|
| Untraced conclusion claims | 3 / 61 | **4.9%** |
| Malformed chain blocks | 3 / 49 | **6.1%** |
| Nonconforming verdict cells | 17 / 120 | **14.2%** |

### The unreadable document is the point, not a footnote

`TB-08` raises `SectionResolutionError` — it carries 2 of 6 section headings and no traceable
identifiers. It was **dispatched and it reasoned well**: it separates the given facts from the
causal story, challenges baseline comparability, and states what three runs cannot establish. It
simply did not emit the contract.

**Every rate above is therefore conditional on readability.** An unreadable document contributes
to no numerator and no denominator, so a run that abandons the output contract *entirely* leaves
the population rather than lowering any rate. Contract-emission reliability and conformance are
two different numbers, and only the second is a rate. Control C18 fails if unreadable documents
stop being counted.

## Against the older corpus

`tests/live-conformance-v9.0/` predates v9.11's EMIT-01..03 work on verdict-cell emission shape.

| Reading | v9.0 (n=8) | v9.14 (n=9) |
|---|---|---|
| Nonconforming verdict cells | 21.6% | **14.2%** |
| Untraced conclusion claims | 0.0% | **4.9%** |
| Malformed chain blocks | 0.0% | **6.1%** |

**This is directional and nothing more.** Different prompts, different corpora, n≈9 per side, one
run each, no control arm and no pairing. Verdict conformance moving the right way is *consistent
with* EMIT-01..03 landing at runtime; it does not establish it. The other two moving the wrong way
is a **question**, not a regression finding — the honest test is a paired re-run on identical
prompts, which this corpus cannot supply.

Read the 0.0% figures with particular care: a detector that fires 3 times on one corpus and 0 on
another may be reading a genuine difference or a difference in document shape.

## Limits

- **One run per prompt, one model.** Within-arm variance is uncontrolled; this repository has
  measured swings of up to 3 band points on an identical prompt.
- **Nothing here says the analyses are good.** Every figure counts artifacts.
  `docs/v8.7-correctness-spot-check.md` measured that conformance does not predict correctness,
  and that applies to every number on this page.
- **The reading is deterministic only because the corpus is frozen.** Re-running the *agent* would
  not reproduce it. That is precisely why it may not gate.
- **No comparison against working without the agent.** `docs/EVIDENCE.md` keeps its standing
  disclaimer.

## Falsifiers

```sh
# 1. The published figures are what the tool emits — not hand-typed.
python3 scripts/check-emission-stage-a.py conformance \
    --out-dir tests/emission-stage-a-v9.14 | grep -q '3/61'
python3 scripts/check-emission-stage-a.py conformance \
    --out-dir tests/emission-stage-a-v9.14 | grep -q '17/120'

# 2. N is 9 scored and 1 unreadable, and the unreadable one is named.
python3 scripts/check-emission-stage-a.py conformance \
    --out-dir tests/emission-stage-a-v9.14 | grep -q "N = 9 scored, 1 unreadable \['TB-08'\]"

# 3. The reading is not a gate: it exits 0 on a corpus carrying defects.
python3 scripts/check-emission-stage-a.py conformance --out-dir tests/emission-stage-a-v9.14

# 4. The controls that keep 1-3 true are registered and pass.
python3 scripts/check-emission-stage-a.py --self-test
```
